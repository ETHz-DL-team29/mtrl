"""Minimal DAPO trainer with optional critical-token-only updates."""
import argparse, json, math, os, re, shutil, signal, time, torch
from nightlib import (load_model, chat_texts, rollout, score_items,
                      reward_and_gate, append_jsonl)
from peft import LoraConfig, get_peft_model, get_peft_model_state_dict, set_peft_model_state_dict

STOP = False
def _stop(sig, frame):
    global STOP
    STOP = True

TARGETS = ["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj",
           "in_proj_qkv","in_proj_z","in_proj_b","in_proj_a","out_proj"]
WORK = "/work/courses/dl/team-29/w_night-exp"

def build_targets(model, kind="all", layers="0-23"):
    if kind == "all":
        return TARGETS
    if "-" in layers:
        lo, hi = layers.split("-"); wanted = set(range(int(lo), int(hi)+1))
    else:
        wanted = {int(x) for x in layers.split(",")}
    pat = {
        "mlp": r"\.layers\.(\d+)\.mlp\.(gate_proj|up_proj|down_proj)$",
        "attn": r"\.layers\.(\d+)\.(self_attn|linear_attn)\.(q_proj|k_proj|v_proj|o_proj|in_proj_qkv|in_proj_z|in_proj_b|in_proj_a|out_proj)$",
    }[kind]
    names = [n for n, _ in model.named_modules() if (m := re.search(pat, n)) and int(m.group(1)) in wanted]
    print(f"LoRA targets: {kind} layers {layers} -> {len(names)} modules", flush=True)
    return names

def make_model(mid, r=16, kind="all", layers="0-23"):
    tok, model = load_model(mid)
    model.gradient_checkpointing_enable()
    model.enable_input_require_grads()
    names = build_targets(model, kind, layers)
    model = get_peft_model(model, LoraConfig(
        r=r, lora_alpha=2*r, lora_dropout=0.0, bias="none",
        target_modules=names, task_type="CAUSAL_LM"))
    model.train()
    return tok, model

def save_ckpt(model, opt, step, mode, ckpt_dir, best=None):
    os.makedirs(ckpt_dir, exist_ok=True)
    state = {"step": step, "mode": mode, "best": best,
             "model": get_peft_model_state_dict(model),
             "optim": opt.state_dict()}
    tmp = f"{ckpt_dir}/.tmp.pt"
    torch.save(state, tmp)
    os.replace(tmp, f"{ckpt_dir}/latest.pt")
    os.makedirs(f"{ckpt_dir}/step_{step:05d}", exist_ok=True)
    torch.save(state, f"{ckpt_dir}/step_{step:05d}/state.pt")
    if not os.path.isdir(WORK):
        return
    dst = f"{WORK}/ckpt/{mode}"
    os.makedirs(dst, exist_ok=True)
    try:
        shutil.copyfile(f"{ckpt_dir}/latest.pt", f"{dst}/latest.pt")
        if os.environ.get("WORK_KEEP_STEPS") == "1":
            shutil.copyfile(f"{ckpt_dir}/step_{step:05d}/state.pt", f"{dst}/step_{step:05d}.pt")
    except Exception as e:
        print("WORK copy failed", e, flush=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default="data/train.jsonl")
    ap.add_argument("--val", default="data/val.jsonl")
    ap.add_argument("--langs", required=True)
    ap.add_argument("--mode", choices=["full","crit"], default="full")
    ap.add_argument("--crit-json", default="results/critical_tokens.json")
    ap.add_argument("--steps", type=int, default=200)
    ap.add_argument("--group", type=int, default=8)
    ap.add_argument("--bs", type=int, default=2)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--max-new", type=int, default=224)
    ap.add_argument("--temperature", type=float, default=0.8)
    ap.add_argument("--rep-penalty", type=float, default=1.05)
    ap.add_argument("--eps-low", type=float, default=0.2)
    ap.add_argument("--eps-high", type=float, default=0.28)
    ap.add_argument("--ckpt-every", type=int, default=100)
    ap.add_argument("--val-every", type=int, default=50)
    ap.add_argument("--val-limit", type=int, default=0)
    ap.add_argument("--retries", type=int, default=2)
    ap.add_argument("--lid", type=int, default=1)
    ap.add_argument("--mask-mode", choices=["full","vocab","randpos","entpos","lowent","content","semi","block"], default="full")
    ap.add_argument("--mask-q", type=float, default=0.05)
    ap.add_argument("--init-ckpt", default="")
    ap.add_argument("--reward-mode", choices=["qe","ref"], default="qe")
    ap.add_argument("--ent-coef", type=float, default=0.0)
    ap.add_argument("--semi-lambda", type=float, default=0.3)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--outdir", default="results")
    ap.add_argument("--tag", default="")
    ap.add_argument("--targets", choices=["all","mlp","attn"], default="all")
    ap.add_argument("--layers", default="0-23")
    args = ap.parse_args()
    torch.manual_seed(args.seed)
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    langs = set(args.langs.split(","))
    mode = args.mode
    tag = args.tag or mode
    os.makedirs(f"{args.outdir}", exist_ok=True)
    log_path = f"{args.outdir}/dapo_{tag}.jsonl"
    ckpt_dir = os.path.join(os.environ.get("CKPT_ROOT", "/scratch/users/yimiwang/night-exp/ckpt"), tag)

    train = [json.loads(l) for l in open(args.train) if json.loads(l)["tgt_lang"] in langs]
    val = [json.loads(l) for l in open(args.val) if json.loads(l)["tgt_lang"] in langs]
    if args.val_limit: val = val[:args.val_limit]
    print("train", len(train), "val", len(val), "langs", langs, flush=True)

    tok, model = make_model("Qwen/Qwen3.5-0.8B", kind=args.targets, layers=args.layers)
    if args.init_ckpt:
        ist = torch.load(args.init_ckpt, map_location="cpu", weights_only=False)
        set_peft_model_state_dict(model, ist["model"])
        print("initialised from", args.init_ckpt, "step", ist.get("step"), flush=True)
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=args.lr, betas=(0.9, 0.99), weight_decay=0.0)
    start = 0
    if os.path.exists(f"{ckpt_dir}/latest.pt"):
        st = torch.load(f"{ckpt_dir}/latest.pt", map_location="cpu", weights_only=False)
        set_peft_model_state_dict(model, st["model"])
        opt.load_state_dict(st["optim"])
        start = st["step"] + 1
        print("resumed", start, flush=True)

    crit_mask = None
    if mode == "crit" or args.mask_mode == "vocab":
        ids = [t["id"] for t in json.load(open(args.crit_json))["tokens"]]
        crit_mask = torch.zeros(len(tok), dtype=torch.bool, device="cuda")
        crit_mask[torch.tensor(ids, device="cuda")] = True
        print("crit vocab", len(ids), flush=True)

    pad = tok.pad_token_id or tok.eos_token_id
    alpha_mask = torch.zeros(len(tok), dtype=torch.bool, device="cuda")
    for i in range(len(tok)):
        w = tok.convert_ids_to_tokens(i).lstrip("Ġ▁")
        if re.fullmatch(r"[^\W\d_]{2,}", w): alpha_mask[i] = True
    rng = torch.Generator().manual_seed(args.seed)
    t0 = time.time(); gen_tokens = 0; update_tokens = 0
    for step in range(start, args.steps):
        if STOP:
            print("stopping on signal at", step, flush=True)
            break
        t_step = time.time()
        G, B = args.group, args.bs
        live = torch.zeros(B, dtype=torch.bool)
        for attempt in range(args.retries + 1):
            idx = torch.randint(0, len(train), (B,), generator=rng).tolist()
            batch = [train[i] for i in idx]
            model.eval()
            r = rollout(model, tok, batch, group=G, max_new=args.max_new,
                        temperature=args.temperature, rep_penalty=args.rep_penalty)
            model.train()
            hyps = r["hyps"]
            items = [(batch[j]["source"], hyps[j*G+s]) for j in range(B) for s in range(G)]
            if args.reward_mode == "ref":
                refs = [batch[k // args.group].get("ref") or "" for k in range(len(items))]
                mx = score_items(items, refs=refs)
            else:
                mx = score_items(items)
            rew, gate_ok = [], []
            for k, ((src, hyp), m) in enumerate(zip(items, mx)):
                tgt = batch[k // G]["tgt_lang"]
                rw, ok, _ = reward_and_gate(src, hyp, tgt, m, lid=bool(args.lid))
                rew.append(rw); gate_ok.append(ok)
            rewards = torch.tensor(rew, dtype=torch.float32)
            gen_tokens += r["T"] * B * G
            R = rewards.view(B, G)
            stds = R.std(dim=1, unbiased=False)
            live = stds > 1e-6
            if live.sum() > 0:
                break
            append_jsonl(log_path, {"step": step, "skip": "zero_var", "attempt": attempt,
                                    "reward": float(R.mean()), "sec": round(time.time()-t_step, 2)})
            print(f"step {step} attempt {attempt} zero-var, resampling", flush=True)
            del r, rewards, R
            torch.cuda.empty_cache()
        if live.sum() == 0:
            print(f"step {step} skip zero-var after {args.retries+1} tries", flush=True)
            continue
        adv = torch.zeros_like(R)
        adv[live] = (R[live] - R[live].mean(1, keepdim=True)) / (stds[live, None] + 1e-8)
        A = adv.reshape(-1).to("cuda")

        seqs, toks, plen, T = r["seqs"], r["tokens"], r["plen"], r["T"]
        ids = seqs[:, :plen+T]
        attn = (ids != pad).long()
        valid_all = toks != pad
        mm = args.mask_mode
        if mm == "vocab":
            mask_all = crit_mask[toks] & valid_all
        elif mm == "randpos":
            mask_all = (torch.rand_like(toks, dtype=torch.float) < args.mask_q) & valid_all
        elif mm == "content":
            mask_all = alpha_mask[toks] & valid_all
        elif mm == "semi":
            sel = (torch.rand_like(toks, dtype=torch.float) < args.mask_q) & valid_all
            mask_all = torch.where(sel, torch.ones_like(toks, dtype=torch.float),
                                   torch.full_like(toks, args.semi_lambda, dtype=torch.float)) * valid_all.float()
        elif mm == "block":
            mask_all = torch.zeros_like(valid_all)
            for rr in range(valid_all.shape[0]):
                n = int(valid_all[rr].sum())
                if n == 0: continue
                L = max(1, int(n * args.mask_q))
                st = torch.randint(0, max(1, n - L + 1), (1,), device="cuda").item()
                mask_all[rr, st:st+L] = True
            mask_all = mask_all & valid_all
        elif mm in ("entpos", "lowent"):
            ent = torch.zeros((ids.shape[0], T), device="cuda")
            with torch.no_grad():
                for r0 in range(ids.shape[0]):
                    oe = model(input_ids=ids[r0:r0+1], attention_mask=attn[r0:r0+1],
                               logits_to_keep=T+1, use_cache=False)
                    lp = torch.log_softmax(oe.logits[:, :T].float(), dim=-1)
                    ent[r0] = -(lp.exp() * lp).sum(-1)[0]
                    del oe, lp
                    torch.cuda.empty_cache()
            mask_all = torch.zeros_like(valid_all)
            for rr in range(valid_all.shape[0]):
                v = valid_all[rr]
                if v.sum() == 0: continue
                e = ent[rr][v]
                q = 1 - args.mask_q if mm == "entpos" else args.mask_q
                thr = torch.quantile(e, q)
                mask_all[rr] = v & ((ent[rr] >= thr) if mm == "entpos" else (ent[rr] <= thr))
        else:
            mask_all = valid_all
        n_crit = int((mask_all > 0).sum()) if crit_mask is not None or mm in ("semi",) else int(mask_all.sum())
        denom = mask_all.sum().clamp(min=1)
        opt.zero_grad(set_to_none=True)
        loss_val = 0.0; ratio_sum = 0.0; clip_num = 0; ent_sum = 0.0; n_valid = 0
        for mb in range(0, B*G, 2):
            sl = slice(mb, min(mb+2, B*G))
            out = model(input_ids=ids[sl], attention_mask=attn[sl],
                        logits_to_keep=T+1, use_cache=False)
            logits = out.logits[:, :T].float()
            logp = torch.log_softmax(logits, dim=-1)
            new = logp.gather(2, toks[sl][..., None]).squeeze(-1)
            ratio = torch.exp(new - new.detach())
            surr = torch.minimum(ratio * A[sl, None],
                                 torch.clamp(ratio, 1-args.eps_low, 1+args.eps_high) * A[sl, None])
            m = mask_all[sl]
            loss_mb = -(surr * m).sum() / denom
            if args.ent_coef:
                ent_mb = (-(logp.exp() * logp).sum(-1))[valid_all[sl]].mean()
                loss_mb = loss_mb - args.ent_coef * ent_mb
            loss_mb.backward()
            with torch.no_grad():
                loss_val += float(-(surr * m).sum())
                v = valid_all[sl]
                n_valid += int(v.sum())
                ratio_sum += float(ratio[v].sum())
                clip_num += int(((ratio < 1-args.eps_low) | (ratio > 1+args.eps_high))[v].sum())
                ent_sum += float((-(logp.exp() * logp).sum(-1)[v]).sum())
            del out, logits, logp, new, ratio, surr
        gn = torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        update_tokens += int(denom)

        clip_frac = clip_num / max(1, n_valid)
        ent = ent_sum / max(1, n_valid)
        ratio_mean = ratio_sum / max(1, n_valid)
        rec = {"step": step, "tag": tag, "loss": loss_val, "reward": float(R.mean()),
               "reward_std": float(stds.mean()), "gate_pass": sum(gate_ok)/len(gate_ok),
               "zero_var_groups": int((~live).sum()), "n_tokens": int(valid_all.sum()),
               "n_crit": n_crit, "ratio": ratio_mean,
               "clip_frac": clip_frac, "entropy": ent, "grad_norm": float(gn),
               "lr": opt.param_groups[0]["lr"], "vram_gb": torch.cuda.max_memory_allocated()/2**30,
               "sec": round(time.time()-t_step, 2), "gen_tokens": gen_tokens,
               "update_tokens": update_tokens}
        append_jsonl(log_path, rec)
        print(json.dumps(rec), flush=True)

        if (step+1) % args.ckpt_every == 0 or step == args.steps-1:
            save_ckpt(model, opt, step, tag, ckpt_dir)
        if args.val_every and (step+1) % args.val_every == 0:
            from nightlib import generate_greedy, chrf
            hyps_v = generate_greedy(model, tok, val, max_new=args.max_new)
            mx_v = score_items([[x["source"], h] for x, h in zip(val, hyps_v)])
            rw_v = [reward_and_gate(x["source"], h, x["tgt_lang"], m)[0] for x, h, m in zip(val, hyps_v, mx_v)]
            vr = {"step": step, "val_reward": sum(rw_v)/len(rw_v),
                  "val_metricx": sum(mx_v)/len(mx_v),
                  "val_chrf": chrf(hyps_v, [x["ref"] for x in val])}
            append_jsonl(f"{args.outdir}/val_{tag}.jsonl", vr)
            print("VAL", vr, flush=True)
        del r, seqs, toks
        torch.cuda.empty_cache()

    save_ckpt(model, opt, step, tag, ckpt_dir)
    print("DONE", tag, "steps", args.steps, "hrs", (time.time()-t0)/3600, flush=True)

if __name__ == "__main__":
    main()

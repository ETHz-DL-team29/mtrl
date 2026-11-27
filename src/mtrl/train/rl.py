"""Group policy-gradient RL for MT (GRPO / DAPO family).

One step:
  1. rollout    B source sentences x G samples (mtrl.generation.hf_generate.sample_group)
  2. reward     gate x (1 - MetricX/25), MetricX-QE or reference-based (mtrl.scoring.reward)
  3. advantage  standardised within each group; if no group has reward variance, resample
                up to `zero_var_retries` times (DAPO dynamic sampling) or skip the step
  4. mask       token weights (mtrl.train.masks)
  5. update     clipped surrogate, token-level normalisation (mtrl.train.losses), repeated
                `ppo_epochs` times on the same rollouts (1 = on-policy, as in results/ym)
  6. log        runs/{run}/train_log.jsonl; validation -> val_log.jsonl; checkpoints

Tokens of zero-variance groups stay in the normaliser with advantage 0, as in results/ym.
Rollouts of one step share a single prompt when prompts_per_step = 1 (the default), so
there is no left padding inside the prompt; for B > 1 the loss forward runs without
explicit position ids, like results/ym did.
"""
from __future__ import annotations

import json
import random
import time

from mtrl.common.flops_accounting import forward_flops, train_flops
from mtrl.train.common import Session, checkpoint, release_cuda_cache, start, validate


def token_logprobs(model, input_ids, attention_mask, tokens, *, want_entropy: bool):
    """log p(token) for the T completion tokens, and optionally the entropy per position."""
    import torch

    T = tokens.shape[1]
    out = model(input_ids=input_ids, attention_mask=attention_mask, logits_to_keep=T + 1, use_cache=False)
    logp_all = torch.log_softmax(out.logits[:, :T].float(), dim=-1)
    logp = logp_all.gather(2, tokens[..., None]).squeeze(-1)
    ent = -(logp_all.exp() * logp_all).sum(-1) if want_entropy else None
    return logp, ent


def _sample_until_signal(s: Session, step: int, scorer_items_fn):
    """Rollout + reward with DAPO dynamic sampling. Returns (batch, scores, R, attempts, sec_gen, sec_score)."""
    import torch

    from mtrl.generation.hf_generate import sample_group
    from mtrl.train.advantage import group_advantages

    t = s.cfg
    a, ro = t.algorithm, t.rollout
    B, G = a["prompts_per_step"], a["group"]
    sec_gen = sec_score = 0.0
    for attempt in range(a["zero_var_retries"] + 1):
        rng = random.Random(t.seed * 1_000_003 + step * 101 + attempt)
        segs = [s.train_segs[rng.randrange(len(s.train_segs))] for _ in range(B)]
        s.model.eval()
        t0 = time.time()
        batch = sample_group(s.model, s.tok, segs, [s.lang_of(x) for x in segs], template=t.prompt_template,
                             thinking=t.thinking, group=G, temperature=ro["temperature"], top_p=ro["top_p"],
                             rep_penalty=ro["rep_penalty"], max_new_tokens=ro["max_new_tokens"],
                             model_name=t.model["name"])
        sec_gen += time.time() - t0
        s.model.train()
        t0 = time.time()
        rep = [x for x in segs for _ in range(G)]
        scores = scorer_items_fn([(seg, r.translation, r.parse_ok, s.lang_of(seg))
                                  for seg, r in zip(rep, batch.rollouts)])
        sec_score += time.time() - t0
        R = torch.tensor([x["reward"] for x in scores], dtype=torch.float32).view(B, G)
        adv, live = group_advantages(R)
        if live.any():
            return batch, scores, R, adv, live, attempt, sec_gen, sec_score
        s.log("train_log.jsonl", {"step": step, "skip": "zero_var", "attempt": attempt, "reward": float(R.mean())})
        print(f"[rl] step {step} attempt {attempt}: zero reward variance, resampling", flush=True)
    return batch, scores, R, adv, live, attempt, sec_gen, sec_score


def train(run) -> None:
    import torch

    from mtrl.scoring.reward import score_translations
    from mtrl.train.losses import pg_loss
    from mtrl.train.masks import NEEDS_ENTROPY, MaskContext, build_mask, content_vocab_mask

    s = start(run, need_scorer=True)
    t = s.cfg
    a, sched = t.algorithm, t.schedule
    mask_cfg = dict(t.mask)
    mask_name = mask_cfg.pop("name")
    vocab_file = mask_cfg.pop("vocab_file", None)
    ctx_extra = {}
    if mask_name == "content":
        ctx_extra["content_mask"] = content_vocab_mask(s.tok).cuda()
    if mask_name == "vocab":
        ids = [x["id"] for x in json.load(open(vocab_file))["tokens"]]
        vm = torch.zeros(len(s.tok), dtype=torch.bool)
        vm[torch.tensor(ids)] = True
        ctx_extra["vocab_mask"] = vm.cuda()
    mb = a.get("micro_batch", 2)
    n_params = t.model["n_params"]
    gen = torch.Generator().manual_seed(t.seed)

    def score_fn(items):
        return score_translations(items, mode=t.reward["mode"], gate_mode=t.reward["gate"], scorer=s.scorer,
                                  lid_model=s.lid, copy_ratio_max=t.reward["copy_ratio_max"])

    step = s.start_step - 1
    try:
        for step in range(s.start_step, sched["steps"]):
            if s.out_of_time():
                print(f"[rl] max_hours reached at step {step}", flush=True)
                step -= 1
                break
            t_step = time.time()
            batch, scores, R, adv, live, attempts, sec_gen, sec_score = _sample_until_signal(s, step, score_fn)
            if not live.any():
                print(f"[rl] step {step}: no reward variance after {attempts + 1} tries, skipped", flush=True)
                continue
            A = adv.reshape(-1).cuda()
            ids, att, toks, valid = batch.input_ids, batch.attention_mask, batch.tokens, batch.valid
            N = toks.shape[0]

            ent_ctx = None
            old = None
            if mask_name in NEEDS_ENTROPY or a["ppo_epochs"] > 1:
                with torch.no_grad():
                    parts = [token_logprobs(s.model, ids[i:i + mb], att[i:i + mb], toks[i:i + mb],
                                            want_entropy=mask_name in NEEDS_ENTROPY) for i in range(0, N, mb)]
                old = torch.cat([p[0] for p in parts])
                if mask_name in NEEDS_ENTROPY:
                    ent_ctx = torch.cat([p[1] for p in parts])
            weights = build_mask(mask_name, MaskContext(tokens=toks, valid=valid, generator=gen, entropy=ent_ctx,
                                                        **ctx_extra), **mask_cfg)
            denom = weights.sum().clamp(min=1)

            t0 = time.time()
            loss_sum = ent_sum = ratio_sum = 0.0
            n_tok = n_clip = 0
            gn = 0.0
            for epoch in range(a["ppo_epochs"]):
                s.optimizer.zero_grad(set_to_none=True)
                for i in range(0, N, mb):
                    sl = slice(i, i + mb)
                    logp, ent = token_logprobs(s.model, ids[sl], att[sl], toks[sl], want_entropy=True)
                    ref = old[sl] if old is not None else logp.detach()
                    loss, st = pg_loss(logp, ref, A[sl], weights[sl], clip_low=a["clip_low"],
                                       clip_high=a["clip_high"], denom=denom)
                    if a["ent_coef"]:
                        loss = loss - a["ent_coef"] * ent[valid[sl]].mean()
                    loss.backward()
                    if epoch == a["ppo_epochs"] - 1:
                        loss_sum += float(loss)
                        ent_sum += float(ent[valid[sl]].sum())
                        ratio_sum += st["ratio_sum"]
                        n_tok += st["n_tokens"]
                        n_clip += st["n_clipped"]
                    del logp, ent, loss
                gn = float(torch.nn.utils.clip_grad_norm_(s.params, t.optim["grad_clip"]))
                s.optimizer.step()
            sec_update = time.time() - t0

            n_gen = int(valid.sum())
            n_prompt = sum(r.n_prompt_tokens for r in batch.rollouts)
            n_valid = max(1, n_gen)
            s.extra["gen_tokens"] = s.extra.get("gen_tokens", 0) + n_gen * (attempts + 1)
            s.extra["update_tokens"] = s.extra.get("update_tokens", 0) + int((weights > 0).sum()) * a["ppo_epochs"]
            reasons = {}
            for x in scores:
                reasons[x["gate_reason"]] = reasons.get(x["gate_reason"], 0) + 1
            mx = [x["metricx"] for x in scores if x["metricx"] is not None]
            rec = {"step": step, "loss": loss_sum, "reward": float(R.mean()), "reward_std": float(R.std(1, unbiased=False).mean()),
                   "metricx": sum(mx) / len(mx) if mx else None, "gate_pass": sum(x["gate_ok"] for x in scores) / len(scores),
                   "gate_reasons": reasons, "live_groups": int(live.sum()), "attempts": attempts + 1,
                   "entropy": ent_sum / n_valid, "ratio": ratio_sum / max(1, n_tok), "clip_frac": n_clip / max(1, n_tok),
                   "grad_norm": gn, "n_gen_tokens": n_gen, "n_update_tokens": int((weights > 0).sum()),
                   "update_weight": float(denom), "len_mean": n_gen / N,
                   "truncated": sum(r.finish_reason == "length" for r in batch.rollouts) / N,
                   "B_test_flops": forward_flops(n_prompt + n_gen, n_params) * (attempts + 1),
                   "B_back_flops": train_flops(n_prompt + n_gen, n_params) * a["ppo_epochs"],
                   "sec_gen": round(sec_gen, 2), "sec_score": round(sec_score, 2), "sec_update": round(sec_update, 2),
                   "sec": round(time.time() - t_step, 2), "vram_gb": round(torch.cuda.max_memory_allocated() / 2**30, 2),
                   "sample": batch.rollouts[0].translation[:200]}
            s.log("train_log.jsonl", rec)
            if step % sched.get("log_every", 1) == 0:
                print("[rl]", json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in rec.items()
                                          if k not in ("gate_reasons", "sample")}), flush=True)
            if (step + 1) % sched["ckpt_every"] == 0:
                checkpoint(s, step)
            if sched.get("val_every") and (step + 1) % sched["val_every"] == 0:
                validate(s, step)
            del batch, ids, att, toks, valid, weights, old, ent_ctx, A
            release_cuda_cache()   # the next step's rewards are scored by the service on this GPU
        if step >= s.start_step and (step + 1) % sched["ckpt_every"] != 0:   # not saved in the loop
            checkpoint(s, step)
        print(f"[rl] done: {t.run_name} at step {step} ({(time.time() - s.t0) / 3600:.2f} h)", flush=True)
    finally:
        s.close()

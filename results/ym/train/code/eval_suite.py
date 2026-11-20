"""One consistent evaluation pass over base + every adapter."""
import argparse, collections, json, os, re, statistics, torch
from nightlib import load_model, generate_greedy, score_items, chrf
from gate import gate, script_frac, TGT_SCRIPT
from lang_gate import lang_ok
from peft import set_peft_model_state_dict

SYSTEMS = [
    ("base", None, "all"),
    ("1080_full", "ckpt/full_v2/latest.pt", "all"),
    ("1080_crit", "ckpt/crit_v2/latest.pt", "all"),
    ("gate_ent", "ckpt/gate_ent/latest.pt", "all"),
    ("gate_rand", "ckpt/gate_rand/latest.pt", "all"),
    ("gate_freq", "ckpt/gate_freq/latest.pt", "all"),
    ("t4_mlp_full", "t4ckpt/mlp_full.pt", "mlp"),
    ("t4_mlp_crit", "t4ckpt/mlp_crit.pt", "mlp"),
    ("t4_attn_full", "t4ckpt/attn_full.pt", "attn"),
    ("lid_full", "ckpt/lid_full/latest.pt", "all"),
    ("lid_freq", "ckpt/lid_freq/latest.pt", "all"),
    ("lid_ent", "ckpt/lid_ent/latest.pt", "all"),
    ("lid_attn", "ckpt/lid_attn/latest.pt", "attn"),
    ("lid_mlp", "ckpt/lid_mlp/latest.pt", "mlp"),
    ("long_full", "ckpt/long_full/latest.pt", "all"),
    ("long_attn", "ckpt/long_attn/latest.pt", "attn"),
    ("sft_full", "ckpt/sft_full/latest.pt", "all"),
    ("sme_full", "ckpt/sme_full/latest.pt", "all"),
    ("mask_rand05", "ckpt/mask_rand05/latest.pt", "all"),
    ("mask_ent05", "ckpt/mask_ent05/latest.pt", "all"),
    ("mask_low05", "ckpt/mask_low05/latest.pt", "all"),
    ("mask_content", "ckpt/mask_content/latest.pt", "all"),
    ("mask_rand20", "ckpt/mask_rand20/latest.pt", "all"),
    ("mask_rand10", "ckpt/mask_rand10/latest.pt", "all"),
    ("mask_ent01", "ckpt/mask_ent01/latest.pt", "all"),
    ("content_long", "ckpt/content_long/latest.pt", "all"),
    ("sft_rl", "ckpt/sft_rl/latest.pt", "all"),
    ("ref_attn", "ckpt/ref_attn/latest.pt", "attn"),
    ("ref_full", "ckpt/ref_full/latest.pt", "all"),
    ("early_attn", "ckpt/early_attn/latest.pt", "attn"),
    ("early_mlp", "ckpt/early_mlp/latest.pt", "mlp"),
    ("ref_sft", "ckpt/ref_sft/latest.pt", "attn"),
    ("early_ent", "ckpt/early_ent/latest.pt", "attn"),
    ("early_lr", "ckpt/early_lr/latest.pt", "attn"),
    ("early_ref", "ckpt/early_ref/latest.pt", "attn"),
    ("early_lr1e5", "ckpt/early_lr1e5/latest.pt", "attn"),
    ("early_s1", "ckpt/early_s1/latest.pt", "attn"),
    ("early_wide", "ckpt/early_wide/latest.pt", "attn"),
    ("wide_ref", "ckpt/wide_ref/latest.pt", "attn"),
    ("wide_long", "ckpt/wide_long/latest.pt", "attn"),
    ("wide_all", "ckpt/wide_all/latest.pt", "attn"),
    ("wide_all_ref", "ckpt/wide_all_ref/latest.pt", "attn"),
    ("wide_s1", "ckpt/wide_s1/latest.pt", "attn"),
    ("all_lr1e5", "ckpt/all_lr1e5/latest.pt", "attn"),
    ("all_ref_lr1e5", "ckpt/all_ref_lr1e5/latest.pt", "attn"),
    ("ref_long6", "ckpt/ref_long6/latest.pt", "attn"),
    ("ref_s1", "ckpt/ref_s1/latest.pt", "attn"),
    ("ref_full_lr2e5", "ckpt/ref_full_lr2e5/latest.pt", "all"),
    ("ref_attn_lr3e5", "ckpt/ref_attn_lr3e5/latest.pt", "attn"),
    ("ref_semi", "ckpt/ref_semi/latest.pt", "attn"),
    ("ref_block", "ckpt/ref_block/latest.pt", "attn"),
    ("ref_randvocab", "ckpt/ref_randvocab/latest.pt", "attn"),
    ("ref_randpos", "ckpt/ref_randpos/latest.pt", "attn"),
    ("sft_long", "ckpt/sft_long/latest.pt", "all"),
    ("sft_long2", "ckpt/sft_long2/latest.pt", "all"),
    ("sft_s1", "ckpt/sft_s1/latest.pt", "all"),
    ("sft_s2", "ckpt/sft_s2/latest.pt", "all"),
    ("sft_sme", "ckpt/sft_sme/latest.pt", "all"),
    ("wide_ref_s1", "ckpt/wide_ref_s1/latest.pt", "attn"),
    ("wide_ref_s2", "ckpt/wide_ref_s2/latest.pt", "attn"),
    ("ref_early_s1", "ckpt/ref_early_s1/latest.pt", "attn"),
    ("ref_early", "ckpt/ref_early/latest.pt", "attn"),
    ("ref_semi01", "ckpt/ref_semi01/latest.pt", "attn"),
    ("lay_mlp_0", "ckpt/lay_mlp_0/latest.pt", "mlp"),
    ("lay_mlp_4", "ckpt/lay_mlp_4/latest.pt", "mlp"),
    ("lay_mlp_8", "ckpt/lay_mlp_8/latest.pt", "mlp"),
    ("lay_mlp_12", "ckpt/lay_mlp_12/latest.pt", "mlp"),
    ("lay_mlp_16", "ckpt/lay_mlp_16/latest.pt", "mlp"),
    ("lay_mlp_20", "ckpt/lay_mlp_20/latest.pt", "mlp"),
    ("lay_mlp_23", "ckpt/lay_mlp_23/latest.pt", "mlp"),
    ("lay_attn_0", "ckpt/lay_attn_0/latest.pt", "attn"),
    ("lay_attn_4", "ckpt/lay_attn_4/latest.pt", "attn"),
    ("lay_attn_8", "ckpt/lay_attn_8/latest.pt", "attn"),
    ("lay_attn_12", "ckpt/lay_attn_12/latest.pt", "attn"),
    ("lay_attn_16", "ckpt/lay_attn_16/latest.pt", "attn"),
    ("lay_attn_20", "ckpt/lay_attn_20/latest.pt", "attn"),
    ("lay_attn_23", "ckpt/lay_attn_23/latest.pt", "attn"),
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--val", default="data/val.jsonl")
    ap.add_argument("--langs", default="isl_Latn,kaz_Cyrl,lij_Latn,lld_Latn")
    ap.add_argument("--out", default="results/suite")
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--max-new", type=int, default=192)
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    keep = set(args.langs.split(","))
    recs = [json.loads(l) for l in open(args.val)]
    recs = [r for r in recs if r["tgt_lang"] in keep]
    print("segments", len(recs), flush=True)

    seg_path = args.out + "_segments.jsonl"
    open(seg_path, "w").close()
    summary = {}
    for name, ckpt, kind in SYSTEMS:
        if args.only and name not in args.only.split(","): continue
        print("=== system", name, flush=True)
        if ckpt is None:
            tok, model = load_model()
        else:
            if not os.path.exists(ckpt):
                print("skip missing", ckpt, flush=True); continue
            from run_dapo import make_model
            tok, model = make_model("Qwen/Qwen3.5-0.8B", kind=kind, layers="0-23")
            st = torch.load(ckpt, map_location="cpu", weights_only=False)
            set_peft_model_state_dict(model, st["model"])
        model.eval()
        hyps = generate_greedy(model, tok, recs, max_new=args.max_new, batch_size=args.batch_size)
        qe = score_items([[r["source"], h] for r, h in zip(recs, hyps)])
        rows = []
        with open(seg_path, "a") as f:
            for r, h, q in zip(recs, hyps, qe):
                ok, why = gate(r["source"], h, r["tgt_lang"])
                words = re.findall(r"\w+", h or "")
                lr = len(words) / max(1, len(re.findall(r"\w+", r["source"])))
                sf = script_frac(h or "", TGT_SCRIPT[r["tgt_lang"]])
                html = bool(re.search(r"<\s*[a-zA-Z/][^>]*>", h or ""))
                uniq = len(set(words)) / max(1, len(words))
                lok, lwhy = lang_ok(h or "", r["tgt_lang"])
                rec = {"system": name, "lang": r["tgt_lang"], "id": r["id"],
                       "hyp": h, "qe": q, "gate": ok, "reason": why,
                       "len_ratio": round(lr, 3), "script": round(sf, 3),
                       "html": html, "uniq": round(uniq, 3),
                       "lid": lok, "lid_reason": lwhy}
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                rows.append(rec)
        by = collections.defaultdict(list)
        for x in rows: by[x["lang"]].append(x)
        summary[name] = {}
        for lang, xs in sorted(by.items()):
            reasons = collections.Counter(x["reason"] for x in xs)
            summary[name][lang] = {
                "n": len(xs),
                "qe": statistics.mean(x["qe"] for x in xs),
                "reward": statistics.mean((1 - x["qe"]/25) if x["gate"] else 0 for x in xs),
                "gate": sum(x["gate"] for x in xs)/len(xs),
                "chrf": chrf([x["hyp"] for x in xs], [r["ref"] for r in recs if r["tgt_lang"] == lang]),
                "len_ratio": statistics.mean(x["len_ratio"] for x in xs),
                "script": statistics.mean(x["script"] for x in xs),
                "html": sum(x["html"] for x in xs)/len(xs),
                "uniq": statistics.mean(x["uniq"] for x in xs),
                "lid_pass": sum(x["lid"] for x in xs)/len(xs),
                "reasons": dict(reasons),
            }
        del model
        torch.cuda.empty_cache()
        json.dump(summary, open(args.out + ".json", "w"), indent=1)

    print(f"{'system':12} {'lang':8} {'QE':>6} {'chrF':>6} {'gate':>6} {'len':>5} {'scr':>5} {'uniq':>5} reasons")
    for name, langs in summary.items():
        for lang, m in langs.items():
            print(f"{name:12} {lang.replace('_Latn','').replace('_Cyrl',''):8} {m['qe']:6.2f} "
                  f"{(m['chrf'] or 0):6.1f} {100*m['gate']:5.0f}% {m['len_ratio']:5.2f} "
                  f"{m['script']:5.2f} {m['uniq']:5.2f} {m['reasons']}")

if __name__ == "__main__":
    main()

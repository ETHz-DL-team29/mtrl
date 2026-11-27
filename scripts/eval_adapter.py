"""Evaluate the base model and / or trained adapters with greedy decoding (training env):

    python scripts/eval_adapter.py configs/train/ym/wide_all_ref.yaml            # that run's latest checkpoint
    python scripts/eval_adapter.py configs/train/quick_rl.yaml --base            # base model, same data/prompt
    python scripts/eval_adapter.py configs/train/quick_rl.yaml --adapter path/to/adapter --name ym_wide_all_ref

Data, prompt and decoding come from the config's `eval` section (split, limit per
direction, max_new_tokens, batch_size); --split / --limit override them. Writes
runs/{name}/eval/{split}_segments.jsonl and {split}_summary.json, where name is the run
name, "base" for --base, or --name. Metrics: see mtrl.train.evaluate.
"""
import argparse
import json

from mtrl.common.train_config import load_train_config


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config")
    ap.add_argument("--env")
    ap.add_argument("--base", action="store_true", help="evaluate the base model without adapter")
    ap.add_argument("--adapter", help="adapter directory (default: the run's latest checkpoint)")
    ap.add_argument("--name", help="output name under runs/ (default: run name, or 'base')")
    ap.add_argument("--split")
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()
    run = load_train_config(args.config, args.env)

    from mtrl.common.env_setup import setup_env

    setup_env(run.env)
    from mtrl.common.jsonl_io import write_jsonl
    from mtrl.scoring.client import ensure_server
    from mtrl.scoring.rule_gate import load_lid
    from mtrl.train.checkpoint import latest_adapter
    from mtrl.train.common import load_split
    from mtrl.train.evaluate import evaluate
    from mtrl.train.policy import load_policy

    t = run.train
    split = args.split or t.eval["split"]
    limit = args.limit if args.limit is not None else t.eval.get("limit")
    adapter = None
    if not args.base:
        adapter = args.adapter or latest_adapter(run.ckpt_dir)
        if adapter is None:
            raise SystemExit(f"no checkpoint in {run.ckpt_dir}; pass --adapter or --base")
    name = args.name or ("base" if args.base else t.run_name)
    out_dir = run.env.path("runs_dir") / name / "eval"
    out_dir.mkdir(parents=True, exist_ok=True)

    segs = load_split(run, split, limit)
    print(f"[eval] {name}: {len(segs)} segments of {split}, adapter={adapter}", flush=True)
    tok, model = load_policy(t.model["name"], run.env, adapter)
    scorer, proc = ensure_server(run.env, log_path=out_dir / "scorer.log")
    try:
        rows, summary = evaluate(model, tok, segs, [run.lang(x.direction) for x in segs],
                                 template=t.prompt_template, thinking=t.thinking,
                                 max_new_tokens=t.eval["max_new_tokens"], batch_size=t.eval["batch_size"],
                                 model_name=t.model["name"], scorer=scorer,
                                 lid_model=load_lid(run.env.path("fasttext_lid")))
    finally:
        if proc is not None:
            proc.terminate()
    write_jsonl(out_dir / f"{split}_segments.jsonl", rows)
    summary["_meta"] = {"adapter": str(adapter) if adapter else None, "split": split, "limit": limit,
                        "config": args.config, "max_new_tokens": t.eval["max_new_tokens"]}
    (out_dir / f"{split}_summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps({k: v for k, v in summary.items() if k != "_meta"}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()

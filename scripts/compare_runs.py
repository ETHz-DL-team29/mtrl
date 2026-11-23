"""Table of evaluation summaries across runs:

    python scripts/compare_runs.py [--split ntrex_dev] [--runs-dir runs]

Reads runs/*/eval/{split}_summary.json (written by scripts/eval_adapter.py) and prints
one row per run and direction; writes runs/compare_{split}.csv.
"""
import argparse
import csv
import json
from pathlib import Path

from mtrl.common.config import REPO_ROOT

COLS = ["chrf", "metricx_ref", "qe_all", "reward", "gate_pass", "ym_gate_pass", "truncated", "n"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="ntrex_dev")
    ap.add_argument("--runs-dir", default=str(REPO_ROOT / "runs"))
    args = ap.parse_args()
    rows = []
    for p in sorted(Path(args.runs_dir).glob(f"*/eval/{args.split}_summary.json")):
        summary = json.loads(p.read_text())
        for d, v in summary.items():
            if d.startswith("_"):
                continue
            rows.append({"run": p.parent.parent.name, "direction": d, **{c: v.get(c) for c in COLS}})
    if not rows:
        raise SystemExit(f"no {args.split}_summary.json under {args.runs_dir}")
    out = Path(args.runs_dir) / f"compare_{args.split}.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["run", "direction"] + COLS)
        w.writeheader()
        w.writerows(rows)
    print(f"{'run':24} {'dir':7} " + " ".join(f"{c:>12}" for c in COLS))
    for r in rows:
        print(f"{r['run']:24} {r['direction']:7} " + " ".join(
            f"{r[c]:>12.3f}" if isinstance(r[c], float) else f"{str(r[c]):>12}" for c in COLS))
    print(f"-> {out}")


if __name__ == "__main__":
    main()

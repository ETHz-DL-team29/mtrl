"""Does a system translate into the target language or into a bigger neighbour?

    python scripts/check_language_drift.py [--split flores_devtest] [--pivot ita_Latn]

For lij (Ligurian) and lld (Ladin) neither lid.176 nor, as it turns out, MetricX tells
the language apart from Italian, so a policy optimised on MetricX can drift into plain
Italian and still score well. This script scores every evaluated output
(runs/*/eval/{split}_segments.jsonl) against both the target-language reference and the
FLORES+ reference of the pivot language (same sentence, same row index):

  chrf_tgt    corpus chrF++ against the target reference
  chrf_pivot  corpus chrF++ against the pivot (Italian) reference
  pivot_share share of outputs whose sentence chrF++ is higher against the pivot

The human target references themselves give chrf_pivot of about 28 (lij) / 25 (lld).
Needs data/raw/flores_plus/{devtest}_{pivot}.jsonl (downloaded by hand or with
huggingface_hub from openlanguagedata/flores_plus).
"""
import argparse
import json
from pathlib import Path

from mtrl.common.config import REPO_ROOT

DIRECTIONS = {"en-lij": "lij", "en-lld": "lld"}
SPLIT_FILES = {"flores_devtest": "devtest", "flores_dev": "dev"}


def main():
    from sacrebleu.metrics import CHRF

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--split", default="flores_devtest")
    ap.add_argument("--pivot", default="ita_Latn")
    ap.add_argument("--runs-dir", default=str(REPO_ROOT / "runs"))
    ap.add_argument("--data-dir", default=str(REPO_ROOT / "data"))
    args = ap.parse_args()
    pivot_path = Path(args.data_dir) / "raw" / "flores_plus" / f"{SPLIT_FILES[args.split]}_{args.pivot}.jsonl"
    pivot = [json.loads(x)["text"] for x in pivot_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    chrf = CHRF(word_order=2)

    print(f"{'run':24} {'dir':7} {'n':>4} {'chrf_tgt':>9} {'chrf_pivot':>11} {'pivot_share':>12}")
    out = []
    for p in sorted(Path(args.runs_dir).glob(f"*/eval/{args.split}_segments.jsonl")):
        rows = [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
        for d in DIRECTIONS:
            rs = [r for r in rows if r["direction"] == d and r["ref"]]
            if not rs:
                continue
            piv = [pivot[int(r["seg_id"].rsplit("/", 1)[1])] for r in rs]
            hyps = [r["hyp"] for r in rs]
            ct = chrf.corpus_score(hyps, [[r["ref"] for r in rs]]).score
            cp = chrf.corpus_score(hyps, [piv]).score
            share = sum(chrf.sentence_score(h, [pv]).score > chrf.sentence_score(h, [r["ref"]]).score
                        for h, pv, r in zip(hyps, piv, rs)) / len(rs)
            run = p.parent.parent.name
            out.append({"run": run, "direction": d, "n": len(rs), "chrf_tgt": round(ct, 2),
                        "chrf_pivot": round(cp, 2), "pivot_share": round(share, 3)})
            print(f"{run:24} {d:7} {len(rs):>4} {ct:>9.2f} {cp:>11.2f} {share:>12.3f}")
    dest = Path(args.runs_dir) / f"language_drift_{args.split}.json"
    dest.write_text(json.dumps(out, indent=1))
    print(f"-> {dest}")


if __name__ == "__main__":
    main()

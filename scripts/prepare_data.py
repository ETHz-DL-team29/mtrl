"""Convert the downloaded WMT26 test set into data/processed/{direction}/{split}.jsonl.

Offline: reads data/raw/wmt26-genmt.jsonl, which the `download` stage fetches.
Directions that already have a processed file are skipped unless --force is given.
"""
from _cli import base_parser

from mtrl.common.config import load_config
from mtrl.common.jsonl_io import write_jsonl
from mtrl.common.records import Segment
from mtrl.data.segment_loader import segments_path
from mtrl.data.wmt26_converter import from_wmt26, wmt26_raw_path


def main():
    ap = base_parser(__doc__)
    ap.add_argument("--force", action="store_true", help="rebuild existing processed files")
    args = ap.parse_args()
    cfg = load_config(args.config, args.env)
    e, data_dir = cfg.exp, cfg.env.path("data_dir")
    raw = wmt26_raw_path(data_dir)
    if not raw.exists():
        raise SystemExit(f"{raw} missing: run the download stage first "
                         f"(python scripts/run.py {args.config} --stages download)")

    for d in e.directions:
        out = segments_path(data_dir, d, e.split)
        if out.exists() and not args.force:
            print(f"[prepare] {out} exists, skipping")
            continue
        rows = from_wmt26(raw, cfg.lang(d))
        if not rows:
            raise SystemExit(f"[prepare] no WMT26 rows for {d}")
        segs = [Segment(seg_id=f"{d}/{e.split}/{i:06d}", direction=d, src=r["src"], ref=r["ref"],
                        meta=r["meta"]) for i, r in enumerate(rows)]
        write_jsonl(out, [s.to_dict() for s in segs])
        print(f"[prepare] {d}: {len(segs)} segments ({sum(s.ref is not None for s in segs)} with ref) -> {out}")


if __name__ == "__main__":
    main()

"""Download FLORES+ and write training / validation segments for a training config:

    python scripts/prepare_train_data.py configs/train/ym/wide_all_ref.yaml

  data/raw/flores_plus/{dev,devtest}_{code}.jsonl         (downloaded once; gated dataset:
                                                           accept its terms with the HF_TOKEN account)
  data/processed/{direction}/{flores_dev,flores_devtest}.jsonl   (Segment rows)

Segment ids are "{direction}/{split}/{index:06d}". Existing processed files are kept
unless --force is given.
"""
import argparse
import shutil

from mtrl.common.env_setup import setup_env
from mtrl.common.jsonl_io import write_jsonl
from mtrl.common.records import Segment
from mtrl.common.train_config import load_train_config
from mtrl.data.flores_converter import FLORES_REPO, FLORES_SRC, SPLITS, flores_raw_path, from_flores
from mtrl.data.segment_loader import segments_path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config")
    ap.add_argument("--env")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    run = load_train_config(args.config, args.env)
    setup_env(run.env)
    data_dir = run.env.path("data_dir")
    t = run.train
    splits = sorted({t.data["train_split"], t.data["val_split"], t.eval["split"]} & set(SPLITS))

    codes = {FLORES_SRC} | {run.lang(d)["wmt26"] for d in t.data["directions"]}
    for split in splits:
        for code in sorted(codes):
            dest = flores_raw_path(data_dir, SPLITS[split], code)
            if dest.exists():
                continue
            from huggingface_hub import hf_hub_download

            dest.parent.mkdir(parents=True, exist_ok=True)
            p = hf_hub_download(FLORES_REPO, f"{SPLITS[split]}/{code}.jsonl", repo_type="dataset")
            shutil.copy(p, dest)
            print(f"[data] {FLORES_REPO} {SPLITS[split]}/{code} -> {dest}")

    for split in splits:
        for d in t.data["directions"]:
            out = segments_path(data_dir, d, split)
            if out.exists() and not args.force:
                print(f"[data] {out} exists, skipping")
                continue
            rows = from_flores(data_dir, SPLITS[split], run.lang(d)["wmt26"])
            segs = [Segment(seg_id=f"{d}/{split}/{i:06d}", direction=d, src=r["src"], ref=r["ref"],
                            meta=r["meta"]) for i, r in enumerate(rows)]
            write_jsonl(out, [s.to_dict() for s in segs])
            print(f"[data] {d} {split}: {len(segs)} segments -> {out}")


if __name__ == "__main__":
    main()

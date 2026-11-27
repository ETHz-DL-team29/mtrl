"""Build the post-training data: training pairs, development sets, WMT26 test.

    python scripts/prepare_train_data.py                      # everything in configs/train_data.yaml
    python scripts/prepare_train_data.py --directions en-hy   # one direction
    python scripts/prepare_train_data.py --force              # rebuild existing files

Reads configs/train_data.yaml (which datasets and why: docs/data.md) and writes
data/processed/{direction}/{split}.jsonl (Segment rows, ids "{direction}/{split}/{i:06d}"):

  wmt_train   cleaned, deduplicated, decontaminated, capped pairs from the WMT26 mtdata
              recipe corpora; data/processed/{direction}/wmt_train.stats.json counts what
              each rule removed
  ntrex_val   NTREX-128, 200 sentences (validation during training)
  ntrex_dev   NTREX-128, 1797 sentences (development evaluation)
  wmt26_test  WMT26 General MT documents, human reference or PseudoRef

Downloads (skipped when present): mtdata datasets into data/raw/mtdata/{direction}/ with
the `mtdata` tool of the env config's python.mtdata interpreter, NTREX-128 files into
data/raw/ntrex/, the WMT26 test set and PseudoRef into data/raw/.
"""
import argparse
import json
import subprocess
import urllib.request
from pathlib import Path

import yaml

from mtrl.common.config import REPO_ROOT, load_env, resolve_env_name
from mtrl.common.env_setup import setup_env
from mtrl.common.jsonl_io import write_jsonl
from mtrl.common.records import Segment
from mtrl.data import ntrex_converter as NT
from mtrl.data import wmt26_converter as W
from mtrl.data.parallel_corpus import build_pairs, normalize, read_mtdata_parts
from mtrl.data.segment_loader import segments_path

DEFAULT_DATA_CONFIG = REPO_ROOT / "configs" / "train_data.yaml"


def mtdata_download(env, data_dir: Path, direction: str, lang: dict, datasets: list[str]) -> Path:
    out = data_dir / "raw" / "mtdata" / direction
    parts = out / "train-parts"
    missing = [d for d in datasets if not any(parts.glob(f"{d}.*"))] if parts.exists() else datasets
    if missing:
        exe = Path(env.python_for("mtdata", default="python")).parent / "mtdata"
        tgt3 = lang["wmt26"].split("_")[0]
        cmd = [str(exe), "get", "-l", f"eng-{tgt3}", "--no-merge", "-tr", *missing, "-o", str(out)]
        print("[data] " + " ".join(cmd), flush=True)
        subprocess.run(cmd, check=True)
    return parts


def fetch(url: str, dest: Path) -> Path:
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(urllib.request.urlopen(url, timeout=300).read())
        print(f"[data] {url} -> {dest}", flush=True)
    return dest


def blocked_sentences(data_dir: Path, sources: list[str]) -> set[str]:
    """Normalised English sentences of every development / test set."""
    out = set()
    if "ntrex" in sources:
        out |= {normalize(s) for s in NT.all_sources(data_dir)}
    if "flores_plus" in sources:
        for p in (data_dir / "raw" / "flores_plus").glob("*_eng_Latn.jsonl"):
            out |= {normalize(json.loads(x)["text"]) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()}
    if "wmt26_test" in sources:
        for line in W.wmt26_raw_path(data_dir).read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            if r["src_lang"] == W.WMT26_SRC_LANG:
                out |= {normalize(s) for s in W.html_to_text(r["src_text"]).split("\n") if s.strip()}
    out.discard("")
    return out


def write_split(data_dir: Path, direction: str, split: str, rows: list[dict], force: bool) -> None:
    out = segments_path(data_dir, direction, split)
    if out.exists() and not force:
        print(f"[data] {out} exists, skipping (--force rebuilds)")
        return
    segs = [Segment(seg_id=f"{direction}/{split}/{i:06d}", direction=direction, src=r["src"], ref=r["ref"],
                    meta=r["meta"]) for i, r in enumerate(rows)]
    write_jsonl(out, [s.to_dict() for s in segs])
    print(f"[data] {direction} {split}: {len(segs)} segments ({sum(s.ref is not None for s in segs)} with ref) -> {out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default=str(DEFAULT_DATA_CONFIG), help="data config (default: configs/train_data.yaml)")
    ap.add_argument("--env")
    ap.add_argument("--directions", nargs="*", help="subset of the config's directions")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    cfg = yaml.safe_load(Path(args.data).read_text(encoding="utf-8"))
    env = load_env(resolve_env_name(args.env))
    setup_env(env)
    languages = yaml.safe_load((REPO_ROOT / "configs" / "languages.yaml").read_text(encoding="utf-8"))
    data_dir = env.path("data_dir")
    directions = args.directions or cfg["directions"]
    unknown = set(directions) - set(cfg["directions"])
    if unknown:
        raise SystemExit(f"directions not in {args.data}: {sorted(unknown)}")

    lang = {d: {"code": d.split("-", 1)[1], **languages[d.split("-", 1)[1]]} for d in directions}
    fetch(W.WMT26_URL, W.wmt26_raw_path(data_dir))
    if cfg["test"].get("pseudoref"):
        fetch(W.PSEUDOREF_URL, W.pseudoref_path(data_dir))

    # development and test sets first: training data is decontaminated against them
    for d in directions:
        for split in (cfg["dev"]["val_split"], cfg["dev"]["dev_split"]):
            write_split(data_dir, d, split, NT.from_ntrex(data_dir, lang[d], split), args.force)
        pseudo = W.read_pseudoref(W.pseudoref_path(data_dir)) if cfg["test"].get("pseudoref") else None
        rows = W.from_wmt26(W.wmt26_raw_path(data_dir), lang[d], pseudo)
        missing = sum(r["ref"] is None for r in rows)
        if missing:
            print(f"[data] WARNING {d} wmt26_test: {missing}/{len(rows)} documents without any reference")
        write_split(data_dir, d, cfg["test"]["split"], rows, args.force)

    tr = cfg["train"]
    blocked = blocked_sentences(data_dir, cfg["decontaminate"])
    print(f"[data] {len(blocked)} development / test sentences blocked from training", flush=True)
    from mtrl.scoring.rule_gate import load_lid

    lid = load_lid(env.path("fasttext_lid"))
    for d in directions:
        if segments_path(data_dir, d, tr["split"]).exists() and not args.force:
            print(f"[data] {d} {tr['split']} exists, skipping (--force rebuilds)")
            continue
        parts = mtdata_download(env, data_dir, d, lang[d], tr["corpora"][d])
        pairs = read_mtdata_parts(parts, tr["corpora"][d])
        f = tr["filter"]
        rows, stats = build_pairs(pairs, lang[d], lid_model=lid, blocked=blocked, cap=tr["cap"], seed=tr["seed"],
                                  min_words=f["min_words"], max_words=f["max_words"],
                                  copy_ratio_max=f["copy_ratio_max"])
        write_split(data_dir, d, tr["split"], rows, True)
        stats_path = segments_path(data_dir, d, tr["split"]).with_suffix(".stats.json")
        stats_path.write_text(json.dumps(stats, indent=1))
        print(f"[data] {d} {tr['split']} stats: read {sum(stats['read'].values())}, "
              f"kept before cap {sum(stats['kept_before_cap'].values())}, kept {len(rows)}; "
              f"dropped {stats['dropped']} -> {stats_path}", flush=True)


if __name__ == "__main__":
    main()

"""FLORES+ (openlanguagedata/flores_plus, gated on Hugging Face) -> Segment rows.

Historical: the first exploration (2026-11-22, en-is / en-lij / en-lld) trained on FLORES+.
The current data is configs/train_data.yaml (docs/data.md); FLORES+ is now only a
decontamination list and the pivot for scripts/check_language_drift.py.

Used as training / validation data so that the WMT26 test set is never trained on:
  flores_dev     <- FLORES+ dev     (997 sentences, the training split)
  flores_devtest <- FLORES+ devtest (1012 sentences, validation / development eval)
Every language file of a split holds the same sentences in the same order (row i of
eng_Latn translates row i of isl_Latn); rows are paired by the `id` field and checked.
Verified 2026-11-21: is, lij, lld, kk, hy, et present; be absent.
"""
from __future__ import annotations

import json
from pathlib import Path

FLORES_REPO = "openlanguagedata/flores_plus"
FLORES_SRC = "eng_Latn"
SPLITS = {"flores_dev": "dev", "flores_devtest": "devtest"}


def flores_raw_path(data_dir: Path, split: str, code: str) -> Path:
    """Local copy of one FLORES+ language file, e.g. data/raw/flores_plus/dev_isl_Latn.jsonl."""
    return Path(data_dir) / "raw" / "flores_plus" / f"{split}_{code}.jsonl"


def _read(path: Path) -> list[dict]:
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]


def pair_rows(src_rows: list[dict], tgt_rows: list[dict]) -> list[dict]:
    """Pair source and target rows by id; returns [{src, ref, meta}] in source order."""
    tgt = {str(r["id"]): r for r in tgt_rows}
    missing = [r["id"] for r in src_rows if str(r["id"]) not in tgt]
    if missing:
        raise ValueError(f"{len(missing)} FLORES+ ids have no target row, e.g. {missing[:3]}")
    out = []
    for r in src_rows:
        t = tgt[str(r["id"])]
        out.append({"src": r["text"].strip(), "ref": t["text"].strip(),
                    "meta": {"flores_id": str(r["id"]), "domain": r.get("domain"),
                             "topic": r.get("topic"), "url": r.get("url")}})
    return out


def from_flores(data_dir: Path, split: str, tgt_code: str) -> list[dict]:
    return pair_rows(_read(flores_raw_path(data_dir, split, FLORES_SRC)),
                     _read(flores_raw_path(data_dir, split, tgt_code)))

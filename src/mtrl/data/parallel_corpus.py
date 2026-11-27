"""Training pairs from mtdata downloads: read, clean, deduplicate, decontaminate, cap.

The choice of corpora and every filter rule is explained in docs/data.md. In short:

  1. read     data/raw/mtdata/{direction}/train-parts/{dataset}.{lang} (one dataset per
              file pair, as written by `mtdata get --no-merge`)
  2. clean    English side 4..80 words and identified as English; the target side must pass
              the same rule gate the RL reward uses (not empty, not a copy of the source,
              right script, right fastText language, plausible length ratio). A reference
              the reward would score 0 is not a target we want SFT to imitate.
  3. dedup    one pair per normalised English sentence (first seen wins, datasets in
              config order)
  4. decontam drop pairs whose normalised English sentence occurs in any development or
              test set (NTREX-128, FLORES+, WMT26 test)
  5. cap      a seeded random sample of at most `cap` pairs per direction
"""
from __future__ import annotations

import random
import re
import unicodedata
from collections import Counter
from pathlib import Path

from mtrl.common.records import Segment


def normalize(text: str) -> str:
    """Key for deduplication / decontamination: NFKC, lower case, letters and digits only."""
    text = unicodedata.normalize("NFKC", text).lower()
    return re.sub(r"[\W_]+", " ", text).strip()


def read_mtdata_parts(parts_dir: Path, datasets: list[str]) -> dict[str, list[tuple[str, str]]]:
    """{dataset: [(english, target), ...]} for the given mtdata dataset ids.

    `mtdata get --no-merge` writes {id}.{lang} files; the English file ends in .eng or
    .eng_XX, the target file is the other one of the pair."""
    parts_dir = Path(parts_dir)
    out = {}
    for ds in datasets:
        files = [p for p in parts_dir.glob(f"{ds}.*") if not p.name.endswith((".meta.jsonl.gz", ".gz"))]
        eng = [p for p in files if p.suffix.lstrip(".").startswith("eng")]
        tgt = [p for p in files if p not in eng]
        if len(eng) != 1 or len(tgt) != 1:
            raise FileNotFoundError(f"{parts_dir}/{ds}.*: expected one English and one target file, "
                                    f"found {[p.name for p in files]} (run the mtdata download first)")
        e = eng[0].read_text(encoding="utf-8", errors="replace").split("\n")
        t = tgt[0].read_text(encoding="utf-8", errors="replace").split("\n")
        if len(e) != len(t):
            raise ValueError(f"{ds}: {len(e)} English lines vs {len(t)} target lines")
        out[ds] = [(a.strip(), b.strip()) for a, b in zip(e, t)]
    return out


def check_pair(en: str, tgt: str, lang_cfg: dict, *, lid_model, min_words: int, max_words: int,
               copy_ratio_max: float) -> str:
    """'ok' or the reason the pair is dropped."""
    from mtrl.scoring.rule_gate import gate, predict_lang

    if not en or not tgt:
        return "empty"
    n = len(en.split())
    if n < min_words:
        return "too_short"
    if n > max_words:
        return "too_long"
    if lid_model is not None and predict_lang(lid_model, en) != "en":
        return "source_not_english"
    seg = Segment(seg_id="", direction="", src=en, ref=None)
    ok, reason = gate(seg, tgt, True, lang_cfg, lid_model=lid_model, copy_ratio_max=copy_ratio_max)
    return "ok" if ok else f"target_{reason}"


def build_pairs(by_dataset: dict[str, list[tuple[str, str]]], lang_cfg: dict, *, lid_model,
                blocked: set[str], cap: int | None, seed: int, min_words: int = 4,
                max_words: int = 80, copy_ratio_max: float = 0.8) -> tuple[list[dict], dict]:
    """Clean, dedup, decontaminate and cap. Returns (rows [{src, ref, meta}], stats)."""
    stats = {"read": Counter(), "dropped": Counter(), "kept_before_cap": Counter()}
    seen: set[str] = set()
    kept = []
    for ds, pairs in by_dataset.items():
        for en, tgt in pairs:
            stats["read"][ds] += 1
            reason = check_pair(en, tgt, lang_cfg, lid_model=lid_model, min_words=min_words,
                                max_words=max_words, copy_ratio_max=copy_ratio_max)
            key = normalize(en)
            if reason == "ok" and key in blocked:
                reason = "in_dev_or_test"
            elif reason == "ok" and key in seen:
                reason = "duplicate"
            if reason != "ok":
                stats["dropped"][reason] += 1
                continue
            seen.add(key)
            stats["kept_before_cap"][ds] += 1
            kept.append({"src": en, "ref": tgt, "meta": {"dataset": ds}})
    random.Random(seed).shuffle(kept)
    if cap is not None:
        kept = kept[:cap]
    stats["kept"] = Counter(r["meta"]["dataset"] for r in kept)
    return kept, {k: dict(v) for k, v in stats.items()}

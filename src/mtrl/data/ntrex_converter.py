"""NTREX-128 -> development Segment rows (docs/data.md explains why NTREX).

NTREX-128 (github.com/MicrosoftTranslator/NTREX) is the English newstest2019 source
(1997 sentences) translated by professional translators into 128 languages; line i of
every file is the same sentence. One fixed, seeded split for every language:

  ntrex_val  200 sentences: greedy validation during training (checkpoint curves)
  ntrex_dev  the other 1797: model selection and development evaluation

The English side is public since 2019, so like FLORES+ it may be in the pretraining data:
it is used for development only, never for headline results (those are on WMT26).
"""
from __future__ import annotations

import random
import urllib.request
from pathlib import Path

NTREX_URL = "https://raw.githubusercontent.com/MicrosoftTranslator/NTREX/main/NTREX-128/newstest2019-{}.txt"
NTREX_N = 1997
VAL_SIZE, SPLIT_SEED = 200, 0
SPLITS = ("ntrex_val", "ntrex_dev")


def ntrex_code(lang: dict) -> str:
    """NTREX file code from the WMT26 code: hye_Armn -> hye, ces_Latn -> ces."""
    return lang["wmt26"].split("_")[0]


def ntrex_path(data_dir: Path, name: str) -> Path:
    return Path(data_dir) / "raw" / "ntrex" / f"newstest2019-{name}.txt"


def ensure_file(data_dir: Path, name: str) -> Path:
    p = ntrex_path(data_dir, name)
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(urllib.request.urlopen(NTREX_URL.format(name), timeout=120).read())
        print(f"[data] NTREX {name} -> {p}")
    return p


def split_indices() -> dict[str, list[int]]:
    idx = list(range(NTREX_N))
    random.Random(SPLIT_SEED).shuffle(idx)
    return {"ntrex_val": sorted(idx[:VAL_SIZE]), "ntrex_dev": sorted(idx[VAL_SIZE:])}


def from_ntrex(data_dir: Path, lang: dict, split: str) -> list[dict]:
    src = ensure_file(data_dir, "src.eng").read_text(encoding="utf-8").splitlines()
    ref = ensure_file(data_dir, f"ref.{ntrex_code(lang)}").read_text(encoding="utf-8").splitlines()
    if len(src) != NTREX_N or len(ref) != NTREX_N:
        raise ValueError(f"NTREX: expected {NTREX_N} lines, got {len(src)} English / {len(ref)} target")
    return [{"src": src[i].strip(), "ref": ref[i].strip(), "meta": {"source": "ntrex128", "line": i}}
            for i in split_indices()[split]]


def all_sources(data_dir: Path) -> list[str]:
    return ensure_file(data_dir, "src.eng").read_text(encoding="utf-8").splitlines()

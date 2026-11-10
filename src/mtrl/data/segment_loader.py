"""Load processed segments: data/processed/{direction}/{split}.jsonl (one Segment per line)."""
from __future__ import annotations

import random
from pathlib import Path

from mtrl.common.jsonl_io import read_jsonl
from mtrl.common.records import Segment


def segments_path(data_dir: Path, direction: str, split: str) -> Path:
    return Path(data_dir) / "processed" / direction / f"{split}.jsonl"


def load_segments(direction: str, split: str, n: int | None, seed: int, *,
                  data_dir: Path) -> list[Segment]:
    path = segments_path(data_dir, direction, split)
    if not path.exists():
        raise FileNotFoundError(f"{path} missing - run scripts/prepare_data.py first")
    segs = [Segment.from_dict(d) for d in read_jsonl(path)]
    if n is not None and n < len(segs):
        segs = random.Random(seed).sample(segs, n)
        segs.sort(key=lambda s: s.seg_id)
    return segs

"""jsonl helpers with crash-safe append and resume-by-key."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Iterable


def read_jsonl(path) -> list[dict]:
    """Read all records; a truncated/corrupt line (e.g. after Ctrl+C) is skipped with a warning."""
    path = Path(path)
    if not path.exists():
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"[io] skipping corrupt line {i} in {path}", file=sys.stderr)
    return out


def write_jsonl(path, records: Iterable[dict]) -> None:
    """Atomically (re)write a whole file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def append_jsonl(path, records: Iterable[dict]) -> None:
    """Append records and fsync. If a previous write was cut mid-line, start on a fresh line."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    needs_newline = False
    if path.exists() and path.stat().st_size > 0:
        with open(path, "rb") as f:
            f.seek(-1, os.SEEK_END)
            needs_newline = f.read(1) != b"\n"
    with open(path, "a", encoding="utf-8") as f:
        if needs_newline:
            f.write("\n")
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def done_keys(path, key_fields: tuple[str, ...]) -> set[tuple]:
    return {tuple(r.get(k) for k in key_fields) for r in read_jsonl(path)}

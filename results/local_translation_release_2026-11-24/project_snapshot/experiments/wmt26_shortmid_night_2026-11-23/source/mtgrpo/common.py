from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]


def configure_environment() -> None:
    """Keep task-owned caches on the project drive, not in the home directory."""
    defaults = {
        "HF_HOME": str(ROOT / ".cache" / "huggingface"),
        "TORCH_HOME": str(ROOT / ".cache" / "torch"),
        "HF_HUB_DISABLE_TELEMETRY": "1",
        "TOKENIZERS_PARALLELISM": "false",
    }
    for name, value in defaults.items():
        os.environ.setdefault(name, value)


configure_environment()


def read_jsonl(path: str | Path) -> list[dict]:
    with Path(path).open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_json(path: str | Path, value) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def write_jsonl(path: str | Path, rows: Iterable[dict]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    temporary.replace(path)


def append_jsonl(path: str | Path, row: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        handle.flush()


def sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def source_key(text: str) -> str:
    return " ".join(text.split()).casefold()


def copy_key(text: str) -> str:
    """Ignore HTML layout, whitespace and typographic variants when auditing copies."""
    import html
    import re
    import unicodedata
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-"}))
    return " ".join(text.split()).casefold()


def extract_translation(text: str) -> str:
    # Keep the raw response in logs; only final text is sent to MetricX.
    if "</think>" in text:
        text = text.rsplit("</think>", 1)[1]
    elif "<think>" in text:
        # A truncated reasoning-only response is not a translation.
        return ""
    return text.strip()


def validate_training_rows(rows: list[dict]) -> None:
    if not rows:
        raise ValueError("Training data is empty.")
    for row in rows:
        if row.get("split") != "train" or row.get("usage") != "training":
            raise ValueError(f"Refusing non-training record {row.get('id')}: split/usage must be train/training.")
        if not row.get("source", "").strip():
            raise ValueError("Empty training source.")
        if row.get("src_lang") != "en" or row.get("tgt_lang") != "is":
            raise ValueError("This pilot supports English -> Icelandic only.")

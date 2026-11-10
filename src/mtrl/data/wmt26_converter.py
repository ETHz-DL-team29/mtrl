"""Convert the WMT26 General MT test set into Segment rows.

WMT26 General MT (verified 2026-11-10 against data/wmt26-genmt.jsonl of
github.com/wmt-conference/wmt26-general-mt):
  - fields: doc_id, domain, src_lang, tgt_lang, src_text, video, screenshot,
    gold_transcript, prompt_instruction, multimodal_instruction,
    evaluation_instruction, refs
  - language codes are FLORES-style, e.g. eng_Latn, isl_Latn, ekk_Latn (Estonian)
  - 198 documents per English->X direction, the same English sources for every X
  - src_text is document-level HTML-ish text (<p>, <br>, &amp; ...); converted to
    plain text with one paragraph / line break per newline
  - refs is {} or {"refA": ...}; en->is and en->et have refs, en->hy/be/kk do not
  - speech-domain src_text is an ASR transcript; the manual transcript is kept in
    meta["gold_transcript"]. Video / screenshot inputs are ignored (text-only MT).
  - this is the official TEST set; there is no separate dev set.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

WMT26_URL = "https://raw.githubusercontent.com/wmt-conference/wmt26-general-mt/main/data/wmt26-genmt.jsonl"
WMT26_RAW_NAME = "wmt26-genmt.jsonl"   # stored as data/raw/wmt26-genmt.jsonl by scripts/download.py
WMT26_SRC_LANG = "eng_Latn"


def html_to_text(text: str) -> str:
    """'<p>a<br>b</p>\\n<p>c</p>' -> 'a\\nb\\nc'; HTML entities unescaped."""
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</p>\s*<p>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</?p>", "", text, flags=re.IGNORECASE)
    text = html.unescape(text)
    return "\n".join(line.strip() for line in text.split("\n")).strip()


def wmt26_raw_path(data_dir: Path) -> Path:
    return Path(data_dir) / "raw" / WMT26_RAW_NAME


def from_wmt26(path: Path, lang: dict) -> list[dict]:
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    out = []
    for r in rows:
        if r["src_lang"] != WMT26_SRC_LANG or r["tgt_lang"] != lang["wmt26"]:
            continue
        refs = r.get("refs") or {}
        ref = refs[sorted(refs)[0]] if refs else None
        out.append({
            "src": html_to_text(r["src_text"]),
            "ref": html_to_text(ref) if ref else None,
            "meta": {"source": "wmt26", "orig_id": r["doc_id"], "domain": r["domain"],
                     "has_video": bool(r.get("video")), "has_screenshot": bool(r.get("screenshot")),
                     "gold_transcript": html_to_text(r["gold_transcript"]) if r.get("gold_transcript") else None},
        })
    return out

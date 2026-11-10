"""Prompt construction and output parsing (the reasoning / translation split).

The thinking switch is NOT in the prompt; it is the chat-template kwarg
`enable_thinking`. Qwen3.5's template opens `<think>` inside the prompt when thinking
is on, so the output usually contains only the closing `</think>`.
"""
from __future__ import annotations

import re

from mtrl.common.records import Segment

THINK_OPEN, THINK_CLOSE = "<think>", "</think>"

# Wrappers stripped from the translation, applied repeatedly until nothing changes.
# Prefix patterns (case-insensitive, anchored at the start):
PREFIX_PATTERNS = [
    r"^(here is|here's) (the|my) translation\s*:\s*",
    r"^[\w ()-]{0,30}translation\s*:\s*",   # "Translation:", "Icelandic translation:"
    r"^translated text\s*:\s*",
]
# Surrounding pairs (open, close): stripped only when they enclose the whole text.
# Non-ASCII quotes are written as escapes: \u201c/\u201d curly, \u201e low-9, \u00ab/\u00bb guillemets.
QUOTE_PAIRS = [('"', '"'), ("'", "'"), ("\u201c", "\u201d"), ("\u201e", "\u201c"), ("\u00ab", "\u00bb"), ("```", "```")]


def build_messages(seg: Segment, lang_cfg: dict, template: str) -> list[dict]:
    content = template.format(tgt_lang_name=lang_cfg["name"], src=seg.src).strip()
    return [{"role": "user", "content": content}]


def strip_wrappers(text: str) -> str:
    prev = None
    text = text.strip()
    while text != prev:
        prev = text
        for pat in PREFIX_PATTERNS:
            text = re.sub(pat, "", text, count=1, flags=re.IGNORECASE).strip()
        for op, cl in QUOTE_PAIRS:
            if len(text) >= len(op) + len(cl) and text.startswith(op) and text.endswith(cl):
                inner = text[len(op):len(text) - len(cl)]
                if op == "```":  # drop an optional language tag after the opening fence
                    inner = re.sub(r"^[a-zA-Z]*\n", "", inner)
                text = inner.strip()
    return text


def parse_output(raw: str, thinking: bool) -> tuple[str, str, bool]:
    """Return (reasoning, translation, parse_ok).

    Thinking on: the reasoning ends at the first `</think>`; no closing tag (typically
    truncation at max_tokens) -> parse_ok False, everything counted as reasoning.
    Thinking off: a leading empty `<think></think>` block is tolerated; any other think
    tag means a malformed output -> parse_ok False. The text (tags removed) is kept as
    the translation so that its tokens are still counted, but it is not scored.
    """
    if thinking:
        if THINK_CLOSE in raw:
            reasoning, answer = raw.split(THINK_CLOSE, 1)
            return reasoning.replace(THINK_OPEN, "").strip(), strip_wrappers(answer), True
        return raw.replace(THINK_OPEN, "").strip(), "", False
    text = re.sub(r"^\s*<think>\s*</think>", "", raw)
    if THINK_OPEN in text or THINK_CLOSE in text:
        return "", strip_wrappers(text.replace(THINK_OPEN, " ").replace(THINK_CLOSE, " ")), False
    return "", strip_wrappers(text), True

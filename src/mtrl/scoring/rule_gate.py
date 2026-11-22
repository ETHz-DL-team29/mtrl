"""Rule-based gate on a translation (CPU only). First failing rule wins.

Rules, in order: parse_fail, empty, copy_source, wrong_script, wrong_lang, length_ratio.
`ym_gate` reproduces the cheaper gate of the results/ym experiments (empty, word-length
ratio, script share), selected in training configs with `reward.gate: ym_compat`.
"""
from __future__ import annotations

import difflib
import re

from mtrl.common.records import Segment

# Unicode ranges per ISO 15924 script code (letters only; digits/punctuation are ignored).
SCRIPT_RANGES = {
    "Latn": [(0x0041, 0x005A), (0x0061, 0x007A), (0x00C0, 0x024F), (0x1E00, 0x1EFF)],
    "Cyrl": [(0x0400, 0x04FF), (0x0500, 0x052F)],
    "Armn": [(0x0530, 0x058F)],
}
MIN_SCRIPT_SHARE = 0.5


def load_lid(path):
    import fasttext

    fasttext.FastText.eprint = lambda *a, **k: None  # silence load warning
    return fasttext.load_model(str(path))


def predict_lang(lid_model, text: str) -> str:
    text = " ".join(text.split())
    try:
        labels, _ = lid_model.predict(text, k=1)
        label = labels[0]
    except ValueError:  # fasttext + numpy>=2: np.array(copy=False) error; use the raw binding
        label = lid_model.f.predict(text, 1, 0.0, "strict")[0][1]
    return label.replace("__label__", "")


def script_share(text: str, script: str) -> float:
    """Share of alphabetic characters that belong to `script` (0.0 if there are none)."""
    ranges = SCRIPT_RANGES[script]
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    return sum(any(a <= ord(c) <= b for a, b in ranges) for c in letters) / len(letters)


def gate(seg: Segment, translation: str, parse_ok: bool, lang_cfg: dict, *,
         lid_model, copy_ratio_max: float) -> tuple[bool, str]:
    if not parse_ok:
        return False, "parse_fail"
    hyp = translation.strip()
    if not hyp:
        return False, "empty"
    if difflib.SequenceMatcher(None, seg.src, hyp).ratio() > copy_ratio_max:
        return False, "copy_source"
    script = lang_cfg.get("script")
    if script and script_share(hyp, script) < MIN_SCRIPT_SHARE:
        return False, "wrong_script"
    expected = lang_cfg.get("fasttext")
    predicted = predict_lang(lid_model, hyp)
    if (predicted != expected) if expected else (predicted == "en"):
        return False, "wrong_lang"
    lo, hi = lang_cfg["len_ratio"]
    if not lo <= len(hyp) / max(len(seg.src), 1) <= hi:
        return False, "length_ratio"
    return True, "ok"


def ym_gate(seg: Segment, translation: str, parse_ok: bool, lang_cfg: dict, *,
            lo: float = 0.4, hi: float = 2.5) -> tuple[bool, str]:
    """results/ym gate: word-count ratio in [lo, hi] and >= 50% letters in the target script.
    (Its optional language-ID step lived in a lang_gate.py that was never committed.)"""
    if not parse_ok:
        return False, "parse_fail"
    hyp = translation.strip()
    if not hyp:
        return False, "empty"
    n_src, n_hyp = len(re.findall(r"\w+", seg.src)), len(re.findall(r"\w+", hyp))
    if n_src and not lo <= n_hyp / n_src <= hi:
        return False, "length_ratio"
    if script_share(hyp, lang_cfg["script"]) < MIN_SCRIPT_SHARE:
        return False, "wrong_script"
    return True, "ok"

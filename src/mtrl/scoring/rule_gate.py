"""Rule-based gate on a translation (CPU only). First failing rule wins."""
from __future__ import annotations

import difflib

from mtrl.common.records import Segment


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


def gate(seg: Segment, translation: str, parse_ok: bool, lang_cfg: dict, *,
         lid_model, copy_ratio_max: float) -> tuple[bool, str]:
    if not parse_ok:
        return False, "parse_fail"
    hyp = translation.strip()
    if not hyp:
        return False, "empty"
    if difflib.SequenceMatcher(None, seg.src, hyp).ratio() > copy_ratio_max:
        return False, "copy_source"
    if predict_lang(lid_model, hyp) != lang_cfg["fasttext"]:
        return False, "wrong_lang"
    lo, hi = lang_cfg["len_ratio"]
    if not lo <= len(hyp) / max(len(seg.src), 1) <= hi:
        return False, "length_ratio"
    return True, "ok"

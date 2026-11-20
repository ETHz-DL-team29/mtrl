"""Cheap gate checks: empty, script, length ratio."""
import re, unicodedata

SCRIPT_RANGES = {
    "Latn": [(0x0041,0x007A),(0x00C0,0x024F),(0x1E00,0x1EFF)],
    "Cyrl": [(0x0400,0x04FF)],
    "Armn": [(0x0530,0x058F)],
}
TGT_SCRIPT = {"isl_Latn":"Latn","sme_Latn":"Latn","lij_Latn":"Latn","lld_Latn":"Latn",
              "kaz_Cyrl":"Cyrl","hye_Armn":"Armn"}

def _in(ranges, cp):
    return any(a <= cp <= b for a,b in ranges)

def script_frac(text, script):
    rs = SCRIPT_RANGES[script]
    letters = [c for c in text if c.isalpha()]
    if not letters: return 0.0
    return sum(_in(rs, ord(c)) for c in letters) / len(letters)

def gate(src, hyp, tgt, lo=0.4, hi=2.5):
    h = (hyp or "").strip()
    if not h:
        return False, "empty"
    sl = len(re.findall(r"\w+", src)); hl = len(re.findall(r"\w+", h))
    if sl and (hl / sl < lo or hl / sl > hi):
        return False, f"length_ratio={hl/sl:.2f}"
    if script_frac(h, TGT_SCRIPT[tgt]) < 0.5:
        return False, "wrong_script"
    return True, "ok"

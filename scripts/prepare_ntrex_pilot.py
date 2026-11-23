"""Pilot split from NTREX-128 (newstest2019 English, 1997 sentences, human refs):
120 sentences, the same English for every direction -> data/processed/en-X/ntrex_pilot.jsonl.

    python scripts/prepare_ntrex_pilot.py

Reads data/raw/ntrex/newstest2019-{src.eng,ref.XXX}.txt; missing files are fetched from
github.com/MicrosoftTranslator/NTREX.
"""
import json
import os
import random
import urllib.request

from mtrl.common.config import REPO_ROOT

BASE = "https://raw.githubusercontent.com/MicrosoftTranslator/NTREX/main/NTREX-128/newstest2019-{}.txt"
CODES = {"is": "ref.isl", "et": "ref.est", "cs": "ref.ces", "hy": "ref.hye", "kk": "ref.kaz", "be": "ref.bel"}
N, SEED = 120, 0


RAW = REPO_ROOT / "data" / "raw" / "ntrex"


def lines(name):
    path = RAW / f"newstest2019-{name}.txt"
    if not path.exists():
        RAW.mkdir(parents=True, exist_ok=True)
        path.write_bytes(urllib.request.urlopen(BASE.format(name), timeout=60).read())
    return path.read_text(encoding="utf-8").splitlines()


def main():
    src = lines("src.eng")
    ok = [i for i, s in enumerate(src) if 40 <= len(s) <= 400]
    pick = sorted(random.Random(SEED).sample(ok, N))
    for t, name in CODES.items():
        ref = lines(name)
        assert len(ref) == len(src), (t, len(ref), len(src))
        d = f"en-{t}"
        out = REPO_ROOT / "data" / "processed" / d
        os.makedirs(out, exist_ok=True)
        with open(out / "ntrex_pilot.jsonl", "w", encoding="utf-8") as f:
            for k, i in enumerate(pick):
                f.write(json.dumps({"seg_id": f"{d}/ntrex_pilot/{k:06d}", "direction": d, "src": src[i],
                                    "ref": ref[i], "meta": {"ntrex_line": i}}, ensure_ascii=False) + "\n")
        print(d, N)


if __name__ == "__main__":
    main()

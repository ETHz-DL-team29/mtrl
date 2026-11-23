"""Pilot split (python scripts/prepare_wmt24pp_pilot.py): 120 WMT24++ English sources (same for every direction) -> data/processed/en-X/wmt24pp_pilot.jsonl.
Refs where WMT24++ has the language (is, et, arz=ar_EG, cs); QE-only for lij, lld, sme."""
import json, os, random
from huggingface_hub import hf_hub_download
from mtrl.common.config import REPO_ROOT
D = str(REPO_ROOT / "data" / "processed")
REF = {"is": "en-is_IS", "et": "en-et_EE", "arz": "en-ar_EG", "cs": "en-cs_CZ"}
load = lambda lp: [json.loads(l) for l in open(hf_hub_download("google/wmt24pp", lp + ".jsonl", repo_type="dataset"))]
base = load("en-is_IS")
ok = [i for i, r in enumerate(base) if not r["is_bad_source"] and r["domain"] != "canary" and 40 <= len(r["source"]) <= 400]
pick = sorted(random.Random(0).sample(ok, 120))
refs = {}
for t, lp in REF.items():
    rows = load(lp); by_src = {r["source"]: r["target"] for r in rows}
    refs[t] = [by_src.get(base[i]["source"]) for i in pick]
for t in ["is", "et", "arz", "cs", "lij", "lld", "sme"]:
    d = f"en-{t}"; os.makedirs(f"{D}/{d}", exist_ok=True)
    with open(f"{D}/{d}/wmt24pp_pilot.jsonl", "w") as f:
        for k, i in enumerate(pick):
            r = base[i]
            f.write(json.dumps({"seg_id": f"{d}/wmt24pp_pilot/{k:06d}", "direction": d, "src": r["source"],
                                "ref": refs[t][k] if t in refs else None,
                                "meta": {"domain": r["domain"], "doc": r["document_id"]}}, ensure_ascii=False) + "\n")
    print(d, sum(x is not None for x in refs.get(t, [None]*120)), "refs")
from collections import Counter; print(Counter(base[i]["domain"] for i in pick))

"""Training-data building blocks: pair cleaning, NTREX split, WMT26 PseudoRef merge."""
import json

from mtrl.data import ntrex_converter as NT
from mtrl.data.parallel_corpus import build_pairs, normalize, read_mtdata_parts
from mtrl.data.wmt26_converter import from_wmt26

IS = {"code": "is", "fasttext": "is", "len_ratio": [0.6, 1.8], "script": "Latn"}


class FakeLid:
    """English if the text contains 'the', Icelandic if it contains 'ð', else German."""

    def predict(self, text, k=1):
        lab = "en" if " the " in f" {text.lower()} " else "is" if "ð" in text else "de"
        return [f"__label__{lab}"], [1.0]


def test_normalize():
    assert normalize("Hello, World!  ") == normalize("hello world") == "hello world"


def test_read_mtdata_parts(tmp_path):
    (tmp_path / "OPUS-x-v1-eng-isl.eng").write_text("a b\nc d")
    (tmp_path / "OPUS-x-v1-eng-isl.isl").write_text("x y\nz w")
    assert read_mtdata_parts(tmp_path, ["OPUS-x-v1-eng-isl"]) == {"OPUS-x-v1-eng-isl": [("a b", "x y"), ("c d", "z w")]}


def test_build_pairs_rules():
    good = ("the cat sat on the mat today", "kötturinn sat á mottunni í dag með")
    pairs = {"ds1": [
        good,
        ("the cat sat on the mat today", "annað köttur sat á mottu í dag með"),   # duplicate English
        ("the end", "endirinn með"),                                              # too short
        ("the dog ran away from home", "the dog ran away from home"),             # copy of source
        ("der Hund lief weg von zu Hause", "hundurinn hljóp að heiman með"),      # source not English
        ("the dog ran far away from home", "der Hund lief weit weg von zu Hause"),  # target wrong language
        ("the bird sang in the tree all day", "fuglinn söng í trénu allan daginn með"),  # blocked (dev/test)
    ]}
    rows, stats = build_pairs(pairs, IS, lid_model=FakeLid(), blocked={normalize("the bird sang in the tree all day")},
                              cap=None, seed=0)
    assert [(r["src"], r["ref"]) for r in rows] == [good]
    assert stats["dropped"] == {"duplicate": 1, "too_short": 1, "target_copy_source": 1, "source_not_english": 1,
                                "target_wrong_lang": 1, "in_dev_or_test": 1}


def test_build_pairs_cap_is_seeded():
    pairs = {"ds": [(f"the cat number {i} sat on the mat", f"köttur númer {i} sat á mottunni með") for i in range(50)]}
    a, _ = build_pairs(pairs, IS, lid_model=FakeLid(), blocked=set(), cap=10, seed=1)
    b, _ = build_pairs(pairs, IS, lid_model=FakeLid(), blocked=set(), cap=10, seed=1)
    assert len(a) == 10 and a == b


def test_ntrex_split_is_fixed_and_disjoint():
    s = NT.split_indices()
    assert len(s["ntrex_val"]) == NT.VAL_SIZE and len(s["ntrex_dev"]) == NT.NTREX_N - NT.VAL_SIZE
    assert not set(s["ntrex_val"]) & set(s["ntrex_dev"])
    assert s == NT.split_indices()
    assert NT.ntrex_code({"wmt26": "hye_Armn"}) == "hye"


def test_wmt26_pseudoref_fills_missing_refs(tmp_path):
    rows = [{"doc_id": "d1", "src_lang": "eng_Latn", "tgt_lang": "hye_Armn", "domain": "news", "src_text": "<p>Hi</p>",
             "refs": {}},
            {"doc_id": "d2", "src_lang": "eng_Latn", "tgt_lang": "hye_Armn", "domain": "news", "src_text": "Yo",
             "refs": {"refA": "human"}}]
    p = tmp_path / "t.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows))
    out = from_wmt26(p, {"wmt26": "hye_Armn"}, {"d1": "<p>synthetic</p>", "d2": "synthetic2"})
    assert [(r["ref"], r["meta"]["ref_type"]) for r in out] == [("synthetic", "pseudoref"), ("human", "human")]
    assert out[1]["meta"]["pseudoref"] == "synthetic2"
    assert from_wmt26(p, {"wmt26": "hye_Armn"})[0]["ref"] is None

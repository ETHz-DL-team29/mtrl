from mtrl.scoring.rule_gate import gate, ym_gate
from mtrl.common.records import Segment

LANG = {"code": "is", "fasttext": "is", "len_ratio": [0.6, 1.8], "script": "Latn"}
SRC = "The weather in Reykjavik was cold and windy yesterday."


class FakeLid:
    def __init__(self, label):
        self.label = label

    def predict(self, text, k=1):
        return (f"__label__{self.label}",), (0.99,)


def run(hyp, parse_ok=True, label="is", lang=LANG):
    seg = Segment("en-is/dev/0", "en-is", SRC, None, {})
    return gate(seg, hyp, parse_ok, lang, lid_model=FakeLid(label), copy_ratio_max=0.8)


GOOD = "Vedrid i Reykjavik var kalt og hvasst i gaer."


def test_ok():
    assert run(GOOD) == (True, "ok")


def test_parse_fail_first():
    assert run(GOOD, parse_ok=False) == (False, "parse_fail")


def test_empty():
    assert run("   \n") == (False, "empty")


def test_copy_source():
    assert run(SRC) == (False, "copy_source")
    assert run(SRC.replace("cold", "cool")) == (False, "copy_source")


def test_wrong_lang():
    assert run(GOOD, label="en") == (False, "wrong_lang")


def test_length_ratio():
    assert run("Kalt.") == (False, "length_ratio")
    assert run(GOOD * 3) == (False, "length_ratio")


def test_wrong_script():
    assert run("Погода в Рейкьявике вчера была холодной и ветреной.") == (False, "wrong_script")
    assert run(GOOD, lang={k: v for k, v in LANG.items() if k != "script"}) == (True, "ok")


def test_language_without_lid_label_only_rejects_english():
    lij = {"code": "lij", "fasttext": None, "len_ratio": [0.6, 1.8], "script": "Latn"}
    assert run(GOOD, label="it", lang=lij) == (True, "ok")
    assert run(GOOD, label="en", lang=lij) == (False, "wrong_lang")


def test_ym_gate():
    seg = Segment("en-is/dev/0", "en-is", SRC, None, {})
    assert ym_gate(seg, GOOD, True, LANG) == (True, "ok")
    assert ym_gate(seg, "Kalt.", True, LANG) == (False, "length_ratio")
    assert ym_gate(seg, "Погода в Рейкьявике вчера была холодной и ветреной.", True, LANG) == (False, "wrong_script")
    assert ym_gate(seg, "", True, LANG) == (False, "empty")

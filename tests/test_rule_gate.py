from mtrl.scoring.rule_gate import gate
from mtrl.common.records import Segment

LANG = {"code": "is", "fasttext": "is", "len_ratio": [0.6, 1.8]}
SRC = "The weather in Reykjavik was cold and windy yesterday."


class FakeLid:
    def __init__(self, label):
        self.label = label

    def predict(self, text, k=1):
        return (f"__label__{self.label}",), (0.99,)


def run(hyp, parse_ok=True, label="is"):
    seg = Segment("en-is/dev/0", "en-is", SRC, None, {})
    return gate(seg, hyp, parse_ok, LANG, lid_model=FakeLid(label), copy_ratio_max=0.8)


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

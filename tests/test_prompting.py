from mtrl.generation.prompting import build_messages, parse_output, strip_wrappers
from mtrl.common.records import Segment

LANG = {"code": "is", "name": "Icelandic"}
TEMPLATE = "Translate the following English text into {tgt_lang_name}.\nOutput only the translation.\n\n{src}\n"


def test_build_messages_fills_template():
    seg = Segment("en-is/dev/0", "en-is", "Hello {world}", None, {})
    msgs = build_messages(seg, LANG, TEMPLATE)
    assert len(msgs) == 1 and msgs[0]["role"] == "user"
    assert "Icelandic" in msgs[0]["content"] and msgs[0]["content"].endswith("Hello {world}")


def test_normal_think_block():
    r, t, ok = parse_output("<think>\nLet me think.\n</think>\n\nHallo heimur", thinking=True)
    assert (r, t, ok) == ("Let me think.", "Hallo heimur", True)


def test_think_block_without_open_tag():  # Qwen3.5 puts <think> in the prompt
    r, t, ok = parse_output("Reasoning here.</think>\n\nHallo", thinking=True)
    assert (r, t, ok) == ("Reasoning here.", "Hallo", True)


def test_no_think_block_thinking_off():
    assert parse_output("  Hallo heimur \n", thinking=False) == ("", "Hallo heimur", True)


def test_empty_think_block_thinking_off():
    assert parse_output("<think>\n\n</think>\n\nHallo", thinking=False) == ("", "Hallo", True)


def test_unclosed_think_is_parse_fail():
    r, t, ok = parse_output("<think>\nStill thinking and got trunc", thinking=True)
    assert ok is False and t == "" and r.startswith("Still thinking")


def test_thinking_on_but_no_tags_is_parse_fail():
    assert parse_output("Hallo", thinking=True)[2] is False


def test_quotes_and_prefix_stripped():
    assert parse_output('"Hallo heimur"', thinking=False)[1] == "Hallo heimur"
    assert parse_output("Translation: Hallo", thinking=False)[1] == "Hallo"
    assert parse_output('Icelandic translation: \u201eHallo\u201c', thinking=False)[1] == "Hallo"
    assert parse_output("Here is the translation:\n\u00abHallo\u00bb", thinking=False)[1] == "Hallo"
    assert parse_output("```\nHallo\n```", thinking=False)[1] == "Hallo"


def test_inner_quotes_kept():
    assert strip_wrappers('Hann sagdi "ja" strax') == 'Hann sagdi "ja" strax'


def test_empty_output():
    assert parse_output("", thinking=False) == ("", "", True)
    assert parse_output("   ", thinking=False)[1] == ""
    r, t, ok = parse_output("<think>x</think>", thinking=True)
    assert ok and t == ""


def test_stray_think_tag_with_thinking_off_is_parse_fail():
    # seen on the server: thinking off, the model emitted text, then </think>, then more text
    r, t, ok = parse_output("Melbourne vann leikinn </think> Hallo heimur", thinking=False)
    assert ok is False and r == "" and "</think>" not in t and "Hallo heimur" in t
    r, t, ok = parse_output("Hallo <think> hmm", thinking=False)
    assert ok is False and r == ""

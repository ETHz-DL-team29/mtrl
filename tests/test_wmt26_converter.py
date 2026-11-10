import json

from mtrl.data.wmt26_converter import from_wmt26, html_to_text

LANG_IS = {"name": "Icelandic", "wmt26": "isl_Latn"}


def test_html_to_text():
    assert html_to_text("<p>Hello &amp; welcome</p>\n<p>Line one<br>Line two</p>") == \
        "Hello & welcome\nLine one\nLine two"
    assert html_to_text("no tags &lt;b&gt;") == "no tags <b>"


def test_from_wmt26_filters_direction_and_reads_refs(tmp_path):
    rows = [
        {"doc_id": "d1", "domain": "news", "src_lang": "eng_Latn", "tgt_lang": "isl_Latn",
         "src_text": "<p>Hi</p>", "refs": {"refA": "<p>Hae</p>"}, "video": None, "screenshot": None,
         "gold_transcript": None},
        {"doc_id": "d2", "domain": "speech", "src_lang": "eng_Latn", "tgt_lang": "isl_Latn",
         "src_text": "asr text", "refs": {}, "video": {"id": "v", "path": "x.mp4"}, "screenshot": None,
         "gold_transcript": "gold text"},
        {"doc_id": "d3", "domain": "news", "src_lang": "eng_Latn", "tgt_lang": "hye_Armn",
         "src_text": "<p>Hi</p>", "refs": {}, "video": None, "screenshot": None, "gold_transcript": None},
        {"doc_id": "d4", "domain": "edu", "src_lang": "ces_Latn", "tgt_lang": "isl_Latn",
         "src_text": "Ahoj", "refs": {}, "video": None, "screenshot": None, "gold_transcript": None},
    ]
    path = tmp_path / "wmt26.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    out = from_wmt26(path, LANG_IS)
    assert [r["meta"]["orig_id"] for r in out] == ["d1", "d2"]
    assert out[0]["src"] == "Hi" and out[0]["ref"] == "Hae"
    assert out[1]["ref"] is None and out[1]["meta"]["has_video"] and out[1]["meta"]["gold_transcript"] == "gold text"

import json

import pytest

from mtrl.data.flores_converter import flores_raw_path, from_flores, pair_rows


def test_pair_rows_by_id():
    src = [{"id": "0", "text": " Hello. ", "domain": "wikinews"}, {"id": "1", "text": "Bye."}]
    tgt = [{"id": "1", "text": "Bless."}, {"id": "0", "text": "Halló."}]
    rows = pair_rows(src, tgt)
    assert [(r["src"], r["ref"]) for r in rows] == [("Hello.", "Halló."), ("Bye.", "Bless.")]
    assert rows[0]["meta"]["flores_id"] == "0" and rows[0]["meta"]["domain"] == "wikinews"
    with pytest.raises(ValueError):
        pair_rows(src, tgt[:1])


def test_from_flores_reads_local_files(tmp_path):
    for code, text in [("eng_Latn", "Hi."), ("isl_Latn", "Hæ.")]:
        p = flores_raw_path(tmp_path, "dev", code)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"id": 0, "text": text}) + "\n", encoding="utf-8")
    assert from_flores(tmp_path, "dev", "isl_Latn")[0]["ref"] == "Hæ."

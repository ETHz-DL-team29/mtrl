from mtrl.common.jsonl_io import append_jsonl, done_keys, read_jsonl
from mtrl.common.records import KEY_FIELDS, Rollout


def roll(seg, idx):
    return Rollout(seg_id=seg, sample_idx=idx, model="m", thinking=False, temperature=1.0,
                   raw_output="x", reasoning="", translation="x", n_prompt_tokens=1,
                   n_reasoning_tokens=0, n_translation_tokens=1, finish_reason="stop", parse_ok=True)


def test_append_and_done_keys(tmp_path):
    p = tmp_path / "r.jsonl"
    assert done_keys(p, KEY_FIELDS) == set()
    append_jsonl(p, [roll("a", -1).to_dict(), roll("a", 0).to_dict()])
    append_jsonl(p, [roll("b", 0).to_dict()])
    assert done_keys(p, KEY_FIELDS) == {("a", -1, "m", False), ("a", 0, "m", False), ("b", 0, "m", False)}
    assert Rollout.from_dict(read_jsonl(p)[0]) == roll("a", -1)


def test_resume_after_truncated_line(tmp_path):
    """Simulate Ctrl+C mid-write: a partial last line is ignored and the next append starts clean."""
    p = tmp_path / "r.jsonl"
    append_jsonl(p, [roll("a", 0).to_dict()])
    with open(p, "a") as f:
        f.write('{"seg_id": "b", "sample_')
    assert done_keys(p, KEY_FIELDS) == {("a", 0, "m", False)}
    append_jsonl(p, [roll("b", 0).to_dict()])
    assert done_keys(p, KEY_FIELDS) == {("a", 0, "m", False), ("b", 0, "m", False)}


def test_resume_skips_done_work(tmp_path):
    """The pending-filter used by scripts/generate.py: only missing keys are regenerated."""
    p = tmp_path / "r.jsonl"
    append_jsonl(p, [roll("a", i).to_dict() for i in range(8)] + [roll("b", i).to_dict() for i in range(3)])
    done = done_keys(p, KEY_FIELDS)
    pending = [s for s in ["a", "b", "c"] if any((s, i, "m", False) not in done for i in range(8))]
    assert pending == ["b", "c"]

"""summarize() on a tiny hand-built frame; every expected value is computed by hand below.

Layout: one direction (en-is), one model (n_params = 1e9), two groups (thinking off / on),
each with 2 segments x (1 greedy + 3 samples) = 8 rollouts.
"""
import math

import pandas as pd
import pytest

from mtrl.analysis.zeroshot_stats import run, summarize
from mtrl.common.jsonl_io import append_jsonl
from mtrl.common.records import Rollout, Score

MODEL = "m"
N_PARAMS = {MODEL: 1e9}
EPS = 0.02

# (seg, sample_idx, thinking, gate_ok, gate_reason, reward, qe, kiwi, finish, n_reasoning, n_translation)
# Every rollout has n_prompt_tokens = 10.
ROWS = [
    # --- thinking off ---
    ("s1", -1, False, True, "ok", 0.8, 5.0, 0.7, "stop", 0, 5),
    ("s1", 0, False, True, "ok", 0.2, 20.0, 0.2, "stop", 0, 5),
    ("s1", 1, False, True, "ok", 0.5, 12.5, 0.5, "stop", 0, 5),
    ("s1", 2, False, True, "ok", 0.8, 5.0, 0.7, "length", 0, 5),
    ("s2", -1, False, False, "wrong_lang", 0.0, 20.0, 0.3, "stop", 0, 5),
    ("s2", 0, False, False, "empty", 0.0, None, None, "stop", 0, 5),
    ("s2", 1, False, False, "copy_source", 0.0, 1.0, 0.9, "stop", 0, 5),
    ("s2", 2, False, False, "length_ratio", 0.0, 3.0, 0.8, "stop", 0, 5),
    # --- thinking on ---
    ("s1", -1, True, True, "ok", 0.6, 8.0, 0.6, "stop", 30, 10),
    ("s1", 0, True, True, "ok", 0.6, 10.0, 0.6, "stop", 30, 10),
    ("s1", 1, True, True, "ok", 0.6, 10.0, 0.6, "stop", 30, 10),
    ("s1", 2, True, True, "ok", 0.6, 10.0, 0.6, "stop", 30, 10),
    ("s2", -1, True, True, "ok", 0.4, 12.0, 0.8, "stop", 30, 10),
    ("s2", 0, True, True, "ok", 0.1, 22.5, 0.1, "stop", 30, 10),
    ("s2", 1, True, True, "ok", 0.3, 17.5, 0.3, "stop", 30, 10),
    ("s2", 2, True, True, "ok", 0.5, 12.5, 0.5, "stop", 30, 10),
]


def frame() -> pd.DataFrame:
    """Same columns as load_frame() produces."""
    recs = []
    for seg, idx, think, ok, why, rw, qe, kiwi, fin, nr, nt in ROWS:
        recs.append({"seg_id": f"en-is/test/{seg}", "sample_idx": idx, "model": MODEL, "thinking": think,
                     "n_prompt_tokens": 10, "n_reasoning_tokens": nr, "n_translation_tokens": nt,
                     "finish_reason": fin, "parse_ok": True, "gate_ok": ok, "gate_reason": why,
                     "reward": rw, "direction": "en-is",
                     "m_metricx24_qe": float("nan") if qe is None else qe,
                     "m_cometkiwi22": float("nan") if kiwi is None else kiwi})
    return pd.DataFrame(recs)


@pytest.fixture(scope="module")
def summary():
    scoring = {("en-is", MODEL, False): 1e10}   # no entry for thinking on -> 0
    s = summarize(frame(), N_PARAMS, scoring, EPS)
    return {bool(r.thinking): r for _, r in s.iterrows()}


def test_one_row_per_group(summary):
    assert set(summary) == {False, True}
    assert summary[False].n_segments == 2 and summary[False].n_rollouts == 8


def test_greedy_means(summary):
    off, on = summary[False], summary[True]
    # greedy only (sample_idx -1): off QE (5 + 20) / 2, kiwi (0.7 + 0.3) / 2, reward (0.8 + 0) / 2
    assert off.qe_greedy_mean == pytest.approx(12.5)
    assert off.kiwi_greedy_mean == pytest.approx(0.5)
    assert off.reward_greedy_mean == pytest.approx(0.4)
    # on: QE (8 + 12) / 2, kiwi (0.6 + 0.8) / 2, reward (0.6 + 0.4) / 2
    assert on.qe_greedy_mean == pytest.approx(10.0)
    assert on.kiwi_greedy_mean == pytest.approx(0.7)
    assert on.reward_greedy_mean == pytest.approx(0.5)


def test_gate_failures(summary):
    off, on = summary[False], summary[True]
    # off: all 4 rollouts of s2 fail -> 4 / 8; one per reason -> 1 / 8 each
    assert off.gate_fail_rate == pytest.approx(0.5)
    for reason in ["wrong_lang", "empty", "copy_source", "length_ratio"]:
        assert off[f"gate_fail_{reason}"] == pytest.approx(0.125)
    assert off.gate_fail_parse_fail == 0.0
    assert on.gate_fail_rate == 0.0


def test_within_group_variance(summary):
    off, on = summary[False], summary[True]
    # off: s1 samples [0.2, 0.5, 0.8], mean 0.5, pop. var (0.09 + 0 + 0.09) / 3 = 0.06
    #      s2 samples [0, 0, 0] (all gated out), std 0
    s1 = math.sqrt(0.06)
    assert off.reward_std_within_group_mean == pytest.approx((s1 + 0.0) / 2)
    assert off.frac_low_variance_groups == pytest.approx(0.5)      # s2 only
    assert off.best_of_G_minus_mean == pytest.approx((0.8 - 0.5 + 0.0) / 2)
    # on: s1 [0.6, 0.6, 0.6] std 0; s2 [0.1, 0.3, 0.5], mean 0.3, var (0.04 + 0 + 0.04) / 3
    s2 = math.sqrt(0.08 / 3)
    assert on.reward_std_within_group_mean == pytest.approx((0.0 + s2) / 2)
    assert on.frac_low_variance_groups == pytest.approx(0.5)       # s1 only
    assert on.best_of_G_minus_mean == pytest.approx((0.0 + (0.5 - 0.3)) / 2)


def test_tokens_and_truncation(summary):
    off, on = summary[False], summary[True]
    assert off.reasoning_token_share == 0.0
    assert on.reasoning_token_share == pytest.approx(30 / 40)
    assert on.reasoning_tokens_mean == 30 and on.translation_tokens_mean == 10
    assert off.truncation_rate == pytest.approx(1 / 8)             # one "length"
    assert on.truncation_rate == 0.0


def test_flops(summary):
    off, on = summary[False], summary[True]
    # off: 8 rollouts x (10 + 0 + 5) tokens = 120 tokens; 2 * 1e9 * 120 = 2.4e11
    assert off.gen_flops == pytest.approx(2.4e11)
    assert off.score_flops == pytest.approx(1e10)
    assert off.B_test_flops == pytest.approx(2.5e11)
    # on: 8 x (10 + 30 + 10) = 400 tokens; 2 * 1e9 * 400 = 8e11; no scoring entry
    assert on.gen_flops == pytest.approx(8e11)
    assert on.score_flops == 0.0
    assert on.B_test_flops == pytest.approx(8e11)


def test_run_writes_report(tmp_path):
    ro, sc = [], []
    for seg, idx, think, ok, why, rw, qe, kiwi, fin, nr, nt in ROWS:
        sid = f"en-is/test/{seg}"
        ro.append(Rollout(seg_id=sid, sample_idx=idx, model=MODEL, thinking=think,
                          temperature=0.0 if idx < 0 else 1.0, raw_output="x", reasoning="r" * bool(nr),
                          translation="y", n_prompt_tokens=10, n_reasoning_tokens=nr,
                          n_translation_tokens=nt, finish_reason=fin, parse_ok=True).to_dict())
        metrics = {k: v for k, v in [("metricx24_qe", qe), ("cometkiwi22", kiwi)] if v is not None}
        sc.append(Score(seg_id=sid, sample_idx=idx, model=MODEL, thinking=think, gate_ok=ok,
                        gate_reason=why, metrics=metrics, reward=rw).to_dict())
    append_jsonl(tmp_path / "rollouts.jsonl", ro)
    append_jsonl(tmp_path / "scores.jsonl", sc)
    append_jsonl(tmp_path / "compute.jsonl", [{"type": "score", "direction": "en-is", "model": MODEL,
                                               "thinking": False, "flops": 1e10}])
    s = run(tmp_path, N_PARAMS, EPS)
    assert (tmp_path / "report" / "summary.csv").exists()
    assert (tmp_path / "report" / "summary.md").exists()
    off = s[s.thinking == False].iloc[0]  # noqa: E712
    assert off.qe_greedy_mean == pytest.approx(12.5) and off.B_test_flops == pytest.approx(2.5e11)

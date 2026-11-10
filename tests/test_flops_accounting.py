import pytest

from mtrl.common.flops_accounting import forward_flops, rollout_cost, scoring_cost, train_flops


def test_flops():
    assert forward_flops(10, 1e9) == 2e10
    assert train_flops(10, 1e9) == 6e10


def test_rollout_cost_dicts():
    rs = [{"n_prompt_tokens": 10, "n_reasoning_tokens": 5, "n_translation_tokens": 3},
          {"n_prompt_tokens": 10, "n_reasoning_tokens": 0, "n_translation_tokens": 4}]
    c = rollout_cost(rs, 1e9)
    assert c["prompt_tokens"] == 20 and c["reasoning_tokens"] == 5 and c["translation_tokens"] == 7
    assert c["total_flops"] == pytest.approx(2e9 * 32)


def test_scoring_cost():
    assert scoring_cost(4, 100.0, 1e9) == pytest.approx(8e11)


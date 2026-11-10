import pytest

from mtrl.scoring.reward import reward


def test_reward():
    assert reward(False, 0.0) == 0.0
    assert reward(True, 0.0) == 1.0
    assert reward(True, 25.0) == 0.0
    assert reward(True, 30.0) == 0.0 and reward(True, -1.0) == 1.0
    assert reward(True, 5.0) == pytest.approx(0.8)

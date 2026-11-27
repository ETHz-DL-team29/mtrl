import pytest

torch = pytest.importorskip("torch")

from mtrl.train.advantage import group_advantages   # noqa: E402
from mtrl.train.losses import pg_loss               # noqa: E402


def test_group_advantages_standardise_and_flag_zero_variance():
    r = torch.tensor([[0.2, 0.4, 0.6, 0.8], [0.5, 0.5, 0.5, 0.5]])
    adv, live = group_advantages(r)
    assert live.tolist() == [True, False]
    assert torch.allclose(adv[0].mean(), torch.tensor(0.0), atol=1e-6)
    assert torch.allclose(adv[0].std(unbiased=False), torch.tensor(1.0), atol=1e-5)
    assert torch.equal(adv[1], torch.zeros(4))


def ym_loss(new, adv, mask, eps_low=0.2, eps_high=0.28):
    """The loss exactly as written in results/ym/train/code/run_dapo.py."""
    ratio = torch.exp(new - new.detach())
    surr = torch.minimum(ratio * adv[:, None],
                         torch.clamp(ratio, 1 - eps_low, 1 + eps_high) * adv[:, None])
    return -(surr * mask).sum() / mask.sum().clamp(min=1)


def test_on_policy_loss_matches_ym_gradient():
    torch.manual_seed(0)
    logits = torch.randn(4, 6, requires_grad=True)
    adv = torch.randn(4)
    mask = (torch.rand(4, 6) > 0.3).float()
    g_ym = torch.autograd.grad(ym_loss(logits.log_softmax(-1), adv, mask), logits)[0]
    new = logits.log_softmax(-1)
    loss, st = pg_loss(new, new.detach(), adv, mask, clip_low=0.2, clip_high=0.28, denom=mask.sum())
    g_new = torch.autograd.grad(loss, logits)[0]
    assert torch.allclose(g_ym, g_new, atol=1e-7)
    assert st["n_clipped"] == 0 and st["ratio_sum"] == pytest.approx(st["n_tokens"])


def test_clipping_stops_gradient_beyond_bounds():
    new = torch.zeros(1, 2, requires_grad=True)
    old = torch.log(torch.tensor([[1 / 1.5, 1.0]]))   # ratio 1.5 (clipped for A>0), 1.0
    loss, st = pg_loss(new, old, torch.tensor([1.0]), torch.ones(1, 2), clip_low=0.2, clip_high=0.28, denom=2)
    g = torch.autograd.grad(loss, new)[0]
    assert g[0, 0] == 0 and g[0, 1] != 0 and st["n_clipped"] == 1

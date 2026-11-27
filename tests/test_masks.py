import pytest

torch = pytest.importorskip("torch")

from mtrl.train.masks import MASKS, MaskContext, build_mask   # noqa: E402


def ctx(**kw):
    valid = torch.ones(4, 50, dtype=torch.bool)
    valid[1, 30:] = False            # padding
    valid[3, :] = False              # empty rollout
    base = dict(tokens=torch.randint(0, 100, (4, 50)), valid=valid,
                generator=torch.Generator().manual_seed(0), entropy=torch.rand(4, 50))
    base.update(kw)
    return MaskContext(**base)


@pytest.mark.parametrize("name,params", [("full", {}), ("randpos", {"q": 0.2}), ("semi", {"q": 0.2, "lam": 0.3}),
                                         ("block", {"q": 0.3}), ("highent", {"q": 0.2}), ("lowent", {"q": 0.2}),
                                         ("translation", {})])
def test_masks_respect_padding_and_range(name, params):
    c = ctx()
    w = build_mask(name, c, **params)
    assert w.shape == c.valid.shape and w.dtype == torch.float32
    assert (w[~c.valid] == 0).all() and (w >= 0).all() and (w <= 1).all()


def test_semi_weights_and_rate():
    w = build_mask("semi", ctx(), q=0.2, lam=0.3)
    vals = w[ctx().valid]
    assert torch.all(torch.isclose(vals, torch.tensor(0.3)) | (vals == 1.0))
    frac = (w == 1).float().sum() / ctx().valid.sum()
    assert 0.1 < frac < 0.3


def test_block_is_contiguous_with_expected_length():
    c = ctx()
    w = build_mask("block", c, q=0.3)
    for i in range(3):
        idx = w[i].nonzero().flatten()
        n = int(c.valid[i].sum())
        assert len(idx) == max(1, int(n * 0.3)) and (idx[-1] - idx[0] + 1) == len(idx)


def test_vocab_and_translation_masks():
    tokens = torch.tensor([[1, 2, 3, 4]])
    vm = torch.zeros(10, dtype=torch.bool)
    vm[2] = True
    c = MaskContext(tokens=tokens, valid=torch.ones(1, 4, dtype=torch.bool), vocab_mask=vm,
                    translation_start=torch.tensor([2]))
    assert build_mask("vocab", c).tolist() == [[0, 1, 0, 0]]
    assert build_mask("translation", c).tolist() == [[0, 0, 1, 1]]


def test_unknown_mask_and_registry():
    with pytest.raises(KeyError):
        build_mask("nope", ctx())
    assert {"full", "randpos", "semi", "block", "vocab", "content", "highent", "lowent", "translation"} <= set(MASKS)

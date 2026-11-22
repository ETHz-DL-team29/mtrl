from pathlib import Path

import pytest
import yaml

from mtrl.common.train_config import deep_merge, load_train_config, read_train_yaml

ROOT = Path(__file__).resolve().parents[1]
TRAIN_CONFIGS = sorted((ROOT / "configs" / "train").rglob("*.yaml"))


def test_deep_merge_child_wins_and_keeps_siblings():
    base = {"a": {"x": 1, "y": 2}, "b": 1}
    assert deep_merge(base, {"a": {"y": 3}}) == {"a": {"x": 1, "y": 3}, "b": 1}
    assert base == {"a": {"x": 1, "y": 2}, "b": 1}   # not mutated


@pytest.mark.parametrize("path", [p for p in TRAIN_CONFIGS if not p.name.startswith("_")],
                         ids=lambda p: str(p.relative_to(ROOT)))
def test_every_runnable_train_config_loads(path):
    run = load_train_config(path, "local_4070S_12G")
    t = run.train
    assert t.run_name and t.method in ("rl", "sft")
    assert run.ckpt_dir.name in ("ckpt", t.run_name)


def test_ym_presets_match_original_json():
    cfg = load_train_config(ROOT / "configs/train/ym/wide_all_ref.yaml", "local_4070S_12G").train
    assert (cfg.adapter["targets"], cfg.optim["lr"], cfg.reward["mode"]) == ("attn", 2e-5, "ref")
    assert cfg.algorithm["group"] == 8 and cfg.rollout["max_new_tokens"] == 224
    assert cfg.rollout["temperature"] == 0.9 and cfg.rollout["rep_penalty"] == 1.0
    semi = load_train_config(ROOT / "configs/train/ym/ref_semi.yaml", "local_4070S_12G").train
    assert semi.mask == {"name": "semi", "q": 0.2, "lam": 0.3} and semi.reward["mode"] == "ref"
    sft = load_train_config(ROOT / "configs/train/ym/sft_full.yaml", "local_4070S_12G").train
    assert sft.adapter["targets"] == "all" and sft.sft["grad_accum"] == 8 and sft.sft["max_len"] == 1024


def _write(tmp_path, d, name="x.yaml"):
    p = tmp_path / name
    p.write_text(yaml.safe_dump(d))
    return p


def test_validation_errors(tmp_path):
    good = read_train_yaml(ROOT / "configs/train/quick_rl.yaml")
    for patch, msg in [({"method": "ppo"}, "method"), ({"reward": {"mode": "bleu"}}, "reward.mode"),
                       ({"adapter": {"targets": "embed"}}, "adapter.targets"),
                       ({"algorithm": {"group": 1}}, "group")]:
        with pytest.raises(ValueError, match=msg):
            load_train_config(_write(tmp_path, deep_merge(good, patch)), "local_4070S_12G")
    bad = deep_merge(good, {})
    del bad["rollout"]["temperature"]
    with pytest.raises(ValueError, match="rollout"):
        load_train_config(_write(tmp_path, bad), "local_4070S_12G")


def test_cyclic_base(tmp_path):
    _write(tmp_path, {"base": "b.yaml"}, "a.yaml")
    _write(tmp_path, {"base": "a.yaml"}, "b.yaml")
    with pytest.raises(ValueError, match="cyclic"):
        read_train_yaml(tmp_path / "a.yaml")

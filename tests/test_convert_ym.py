import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "convert_ym_ckpt", Path(__file__).resolve().parents[1] / "scripts" / "convert_ym_ckpt.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_convert_keys_rewrites_prefix_and_lists_targets():
    old = "base_model.model.model.language_model.layers.3.self_attn.q_proj"
    state = {f"{old}.lora_A.weight": 1, f"{old}.lora_B.weight": 2,
             "base_model.model.model.language_model.layers.0.mlp.up_proj.lora_A.weight": 3}
    out, targets = mod.convert_keys(state)
    assert "base_model.model.model.layers.3.self_attn.q_proj.lora_A.weight" in out
    assert targets == ["model.layers.0.mlp.up_proj", "model.layers.3.self_attn.q_proj"]


def test_convert_keys_rejects_foreign_keys():
    with pytest.raises(ValueError):
        mod.convert_keys({"base_model.model.model.visual.blocks.0.attn.qkv.lora_A.weight": 1})

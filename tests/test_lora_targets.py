from mtrl.train.policy import parse_layers, select_target_modules

SELF_ATTN_LAYERS = {3, 7, 11, 15, 19, 23}


def qwen35_names(prefix="model"):
    """Module names of Qwen3_5ForCausalLM (verified on the server, transformers 5.19)."""
    names = []
    for i in range(24):
        if i in SELF_ATTN_LAYERS:
            names += [f"{prefix}.layers.{i}.self_attn.{p}" for p in ("q_proj", "k_proj", "v_proj", "o_proj")]
            names += [f"{prefix}.layers.{i}.self_attn.q_norm"]
        else:
            names += [f"{prefix}.layers.{i}.linear_attn.{p}"
                      for p in ("in_proj_qkv", "in_proj_z", "in_proj_b", "in_proj_a", "out_proj")]
        names += [f"{prefix}.layers.{i}.mlp.{p}" for p in ("gate_proj", "up_proj", "down_proj")]
    return names + ["lm_head", "model.embed_tokens"]


def test_parse_layers():
    assert parse_layers("0-23") == set(range(24))
    assert parse_layers("0,4,8") == {0, 4, 8}
    assert parse_layers([1, 2]) == {1, 2}


def test_module_counts_match_ym_report():
    names = qwen35_names()
    assert len(select_target_modules(names, "attn", "0-23")) == 114
    assert len(select_target_modules(names, "mlp", "0-23")) == 72
    assert len(select_target_modules(names, "all", "0-23")) == 186


def test_layer_subset_and_prefix_independence():
    names = qwen35_names("model.language_model")
    sel = select_target_modules(names, "attn", "0,3")
    assert len(sel) == 5 + 4 and all(".layers.0." in s or ".layers.3." in s for s in sel)
    assert not any("q_norm" in s or "lm_head" in s for s in select_target_modules(names, "all", "0-23"))

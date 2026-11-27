"""Policy model: load Qwen3.5 (text-only), attach / save / load LoRA adapters.

Qwen3.5 checkpoints are image-text-to-text; AutoModelForCausalLM loads only the
language model (Qwen3_5ForCausalLM, no vision tower), which is all MT needs. Its 24
decoder layers mix two attention types (verified 2026-11-21, transformers 5.19):
  18 layers  linear_attn.{in_proj_qkv, in_proj_z, in_proj_b, in_proj_a, out_proj}
   6 layers  self_attn.{q_proj, k_proj, v_proj, o_proj}   (every 4th layer: 3, 7, ..., 23)
  24 layers  mlp.{gate_proj, up_proj, down_proj}
so LoRA scope "attn" = 114 modules, "mlp" = 72, "all" = 186 (as in results/ym).
"""
from __future__ import annotations

import re

ATTN_NAMES = ("q_proj", "k_proj", "v_proj", "o_proj",
              "in_proj_qkv", "in_proj_z", "in_proj_b", "in_proj_a", "out_proj")
MLP_NAMES = ("gate_proj", "up_proj", "down_proj")
_PATTERNS = {
    "attn": re.compile(r"\.layers\.(\d+)\.(?:self_attn|linear_attn)\.(" + "|".join(ATTN_NAMES) + r")$"),
    "mlp": re.compile(r"\.layers\.(\d+)\.mlp\.(" + "|".join(MLP_NAMES) + r")$"),
}
DTYPES = {"bf16": "bfloat16", "fp16": "float16", "fp32": "float32"}


def parse_layers(layers) -> set[int]:
    """"0-23" -> {0..23}; "0,4,8" or [0, 4, 8] -> {0, 4, 8}."""
    if isinstance(layers, (list, tuple)):
        return {int(x) for x in layers}
    layers = str(layers).strip()
    if "-" in layers:
        lo, hi = layers.split("-")
        return set(range(int(lo), int(hi) + 1))
    return {int(x) for x in layers.split(",") if x.strip()}


def select_target_modules(module_names, targets: str, layers) -> list[str]:
    """Full names of the modules that get LoRA, for targets in {all, attn, mlp}."""
    wanted = parse_layers(layers)
    kinds = ["attn", "mlp"] if targets == "all" else [targets]
    out = []
    for name in module_names:
        for kind in kinds:
            m = _PATTERNS[kind].search(name)
            if m and int(m.group(1)) in wanted:
                out.append(name)
                break
    return out


def torch_dtype(env_dtype: str):
    import torch

    return getattr(torch, DTYPES[env_dtype])


def load_base(model_name: str, env_dtype: str, attn_impl: str = "sdpa"):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(model_name)
    tok.padding_side = "left"
    if tok.pad_token_id is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_name, dtype=torch_dtype(env_dtype),
                                                 attn_implementation=attn_impl, device_map={"": 0})
    model.eval()
    return tok, model


def attach_lora(model, adapter_cfg: dict, *, grad_checkpointing: bool = True):
    """Wrap `model` with a fresh trainable LoRA adapter. LoRA weights are kept in fp32
    (peft default autocast_adapter_dtype) so fp16 training on a 1080 Ti does not underflow."""
    from peft import LoraConfig, get_peft_model

    names = select_target_modules([n for n, _ in model.named_modules()],
                                  adapter_cfg["targets"], adapter_cfg.get("layers", "0-23"))
    if not names:
        raise ValueError(f"no modules match adapter {adapter_cfg}")
    if grad_checkpointing:
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
        model.enable_input_require_grads()
    cfg = LoraConfig(r=adapter_cfg["r"], lora_alpha=adapter_cfg["alpha"],
                     lora_dropout=adapter_cfg.get("dropout", 0.0), bias="none",
                     target_modules=names, task_type="CAUSAL_LM")
    model = get_peft_model(model, cfg)
    print(f"[policy] LoRA {adapter_cfg['targets']} layers {adapter_cfg.get('layers')}: "
          f"{len(names)} modules, {sum(p.numel() for p in model.parameters() if p.requires_grad):,} params",
          flush=True)
    return model


def load_adapter(model, adapter_dir, *, trainable: bool):
    from peft import PeftModel

    return PeftModel.from_pretrained(model, str(adapter_dir), is_trainable=trainable)


def load_policy(model_name: str, env_cfg, adapter_dir=None):
    """Base model plus (optionally) a saved adapter, for evaluation."""
    tok, model = load_base(model_name, env_cfg.dtype, env_cfg.attn_impl)
    if adapter_dir:
        model = load_adapter(model, adapter_dir, trainable=False)
        model.eval()
    return tok, model

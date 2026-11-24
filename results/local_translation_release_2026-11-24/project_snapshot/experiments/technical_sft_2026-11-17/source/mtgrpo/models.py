from __future__ import annotations

import gc
import json
import time
from pathlib import Path

from .common import ROOT, copy_key, extract_translation

POLICY_DIR = ROOT / "models" / "qwen3.5-0.8b"
METRICX_DIR = ROOT / "models" / "metricx-24-hybrid-large"
METRICX_TOKENIZER_DIR = ROOT / "models" / "metricx-tokenizer"


def resolve_device(value: str):
    import torch
    if value == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    if value == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is not available.")
    return value


def synchronize(device: str):
    import torch
    if device.startswith("cuda"):
        torch.cuda.synchronize()


def dtype_for(device: str):
    import torch
    if device.startswith("cuda"):
        # Recent torch also reports emulated BF16 as supported on T4 (SM75).
        # Require native Ampere-or-newer support for this training precision.
        native_bf16 = torch.cuda.get_device_capability()[0] >= 8 and torch.cuda.is_bf16_supported()
        return torch.bfloat16 if native_bf16 else torch.float16
    return torch.float32


def environment_info() -> dict:
    import platform
    import torch
    import transformers
    result = {"python": platform.python_version(), "torch": torch.__version__, "transformers": transformers.__version__, "cuda_build": torch.version.cuda}
    if torch.cuda.is_available():
        properties = torch.cuda.get_device_properties(0)
        result.update(gpu=properties.name, vram_bytes=properties.total_memory)
    for name, directory in (("policy", POLICY_DIR), ("metricx", METRICX_DIR)):
        manifest = directory / "download_manifest.json"
        if manifest.exists():
            result[f"{name}_manifest"] = json.loads(manifest.read_text(encoding="utf-8"))
    return result


def make_prompt(row: dict, *, thinking: bool = False) -> list[dict]:
    instruction = row.get("instruction") or (
        "Translate the following English text into Icelandic. "
        "Preserve the meaning, names, numbers and any original formatting. "
        "Return only the Icelandic translation, without explanations."
    )
    return [{"role": "user", "content": f"{instruction}\n\n{row['source']}"}]


class Policy:
    def __init__(self, device="auto", adapter: str | None = None, trainable=False, checkpointing=True,
                 lora_config=None, disable_dropout=True, attention_implementation="eager"):
        import torch
        from transformers import AutoTokenizer, Qwen3_5ForConditionalGeneration

        self.device = resolve_device(device)
        self.dtype = dtype_for(self.device)
        start = time.perf_counter()
        self.tokenizer = AutoTokenizer.from_pretrained(POLICY_DIR, local_files_only=True)
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "left"
        self.model = Qwen3_5ForConditionalGeneration.from_pretrained(
            POLICY_DIR, local_files_only=True, dtype=self.dtype, attn_implementation=attention_implementation,
        ).to(self.device)
        if adapter:
            from peft import PeftModel
            self.model = PeftModel.from_pretrained(self.model, adapter, is_trainable=trainable)
        elif trainable:
            from peft import LoraConfig, get_peft_model
            self.model = get_peft_model(self.model, lora_config or LoraConfig(
                task_type="CAUSAL_LM", r=8, lora_alpha=16, lora_dropout=0.0,
                target_modules=["q_proj", "v_proj"], bias="none",
            ))
        if trainable and checkpointing:
            self.model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
            self.model.enable_input_require_grads()
        if trainable and disable_dropout:
            for module in self.model.modules():
                if isinstance(module, torch.nn.Dropout):
                    module.p = 0.0
        # Deterministic policy forwards (no dropout) still permit autograd.
        self.model.eval()
        self.load_seconds = time.perf_counter() - start

    def prompt_ids(self, row: dict, *, max_prompt_tokens: int, thinking=False):
        text = self.tokenizer.apply_chat_template(
            make_prompt(row, thinking=thinking), tokenize=False, add_generation_prompt=True,
            enable_thinking=thinking,
        )
        inputs = self.tokenizer(text, add_special_tokens=False, return_tensors="pt")
        length = inputs.input_ids.shape[1]
        if length > max_prompt_tokens:
            raise ValueError(f"Prompt has {length} tokens, exceeding {max_prompt_tokens}; source was NOT silently truncated.")
        return inputs.input_ids.to(self.device)

    def generate(self, prompt_ids, *, max_new_tokens: int, sample=False, thinking=False):
        import torch
        from transformers import GenerationConfig

        # Sample exactly from the raw policy for GRPO: T=1, no top-k/p truncation.
        # This keeps generation and old/new policy token probabilities consistent.
        sampling_settings = {"temperature": 1.0, "top_p": 1.0, "top_k": 0} if sample else {}
        config = GenerationConfig(
            max_new_tokens=max_new_tokens, do_sample=sample,
            repetition_penalty=1.0, num_beams=1,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.pad_token_id,
            use_cache=True,
            **sampling_settings,
        )
        self.model.eval()
        synchronize(self.device)
        start = time.perf_counter()
        with torch.inference_mode():
            output = self.model.generate(
                input_ids=prompt_ids, attention_mask=torch.ones_like(prompt_ids), generation_config=config,
            )
        synchronize(self.device)
        completion = output[0, prompt_ids.shape[1]:].detach().clone()
        raw = self.tokenizer.decode(completion, skip_special_tokens=True)
        ids = completion.tolist()
        ended = bool(ids) and ids[-1] == self.tokenizer.eos_token_id
        return {
            "completion_ids": completion,
            "raw_output": raw, "hypothesis": extract_translation(raw),
            "prompt_tokens": prompt_ids.shape[1], "completion_tokens": len(ids),
            "truncated": len(ids) >= max_new_tokens and not ended,
            "generation_seconds": time.perf_counter() - start,
        }

    def log_probabilities(self, prompt_ids, completion_ids):
        import torch
        import torch.nn.functional as functional

        # HF gradient checkpointing is enabled only in training mode. Dropout is
        # disabled above so old/new probability estimates remain deterministic.
        self.model.train(torch.is_grad_enabled())
        completion_ids = completion_ids.to(self.device)
        length = len(completion_ids)
        if length == 0:
            raise ValueError("Cannot optimize an empty completion token sequence.")
        full = torch.cat((prompt_ids, completion_ids.unsqueeze(0)), dim=1)
        output = self.model(
            input_ids=full, attention_mask=torch.ones_like(full), use_cache=False,
            logits_to_keep=length + 1,
        )
        logits = output.logits[0, -(length + 1):-1, :]
        return -functional.cross_entropy(logits.float(), completion_ids, reduction="none")

    def close(self):
        import torch
        del self.model
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


class MetricX:
    """Official MetricX-24 regression readout using the stock MT5 architecture.

    Official metricx24/models.py uses the MT5 encoder/decoder and reads vocabulary
    logit 250089 (<extra_id_10>) after one decoder token [0], clipped to [0, 25].
    Stock MT5ForConditionalGeneration has those same checkpoint parameter names.
    This avoids vendoring the old Transformers-specific custom implementation.
    """
    def __init__(self, device="cpu", max_input_tokens=1024):
        from transformers import AutoTokenizer, MT5ForConditionalGeneration
        if max_input_tokens < 2:
            raise ValueError("MetricX max_input_tokens must be at least 2.")
        self.device = resolve_device(device)
        self.max_input_tokens = max_input_tokens
        self.tokenizer = AutoTokenizer.from_pretrained(METRICX_TOKENIZER_DIR, local_files_only=True, use_fast=False)
        self.model, info = MT5ForConditionalGeneration.from_pretrained(
            METRICX_DIR, local_files_only=True, dtype=dtype_for(self.device), output_loading_info=True,
        )
        bad = {key: info.get(key) for key in ("missing_keys", "unexpected_keys", "mismatched_keys", "error_msgs") if info.get(key)}
        if bad:
            raise RuntimeError(f"MetricX checkpoint architecture mismatch: {bad}")
        self.model = self.model.to(self.device).eval()

    def score(self, source: str, hypothesis: str) -> dict:
        import torch
        text = f"source: {source} candidate: {hypothesis}"
        # Match official predict.py: tokenize with truncation, then remove EOS.
        all_ids = self.tokenizer(text, add_special_tokens=True)["input_ids"]
        ids = all_ids[:self.max_input_tokens]
        if ids:
            ids = ids[:-1]
        if not ids:
            raise ValueError("MetricX received an empty tokenized input.")
        inputs = torch.tensor([ids], dtype=torch.long, device=self.device)
        synchronize(self.device)
        start = time.perf_counter()
        with torch.inference_mode():
            result = self.model(
                input_ids=inputs, attention_mask=torch.ones_like(inputs),
                decoder_input_ids=torch.zeros((1, 1), dtype=torch.long, device=self.device),
                use_cache=False,
            )
            score = float(result.logits[0, 0, 250089].float().clamp(0, 25).item())
        import math
        if not math.isfinite(score):
            raise FloatingPointError("MetricX returned a non-finite score.")
        synchronize(self.device)
        return {"metricx_qe": score, "qe_reward": 1.0 - score / 25.0,
                "metricx_truncated": len(all_ids) > self.max_input_tokens,
                "metricx_input_tokens": len(ids), "metricx_decoder_tokens": 1,
                "metricx_untruncated_tokens": len(all_ids), "metricx_forward_calls": 1,
                "metricx_device": self.device, "metricx_dtype": str(next(self.model.parameters()).dtype),
                "scoring_seconds": time.perf_counter() - start}

    def close(self):
        import torch
        del self.model
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


def output_gate(source: str, hypothesis: str, *, truncated=False, reject_truncated=True) -> dict:
    failures = []
    if not copy_key(hypothesis):
        failures.append("empty_translation")
    if hypothesis.strip().casefold() == source.strip().casefold():
        failures.append("exact_source_copy")
    elif copy_key(hypothesis) == copy_key(source):
        failures.append("normalized_source_copy")
    ratio = len(hypothesis) / max(len(source), 1)
    if ratio < 0.15 or ratio > 6.0:
        failures.append("character_length_ratio")
    if truncated and reject_truncated:
        failures.append("generation_truncated")
    return {"gate": not failures, "gate_failures": failures, "length_ratio": ratio,
            "language_id_checked": False, "gate_version": "nonempty-normalized-copy-length-truncation-v2"}

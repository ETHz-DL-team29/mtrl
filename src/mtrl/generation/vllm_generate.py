"""Rollout generation with vLLM (the only backend in this stage).

Qwen3.5 small models are published as image-text-to-text; text-only prompts work
through vLLM's multimodal class (verified in the Oct-2026 zero-shot runs on the
4070S). TODO: re-confirm if the vLLM version changes.
"""
from __future__ import annotations

import zlib

from mtrl.common.config import EnvConfig
from mtrl.generation.prompting import build_messages, parse_output
from mtrl.common.records import Rollout, Segment


def load_llm(model_name: str, env_cfg: EnvConfig, seed: int):
    from vllm import LLM

    v = env_cfg.vllm
    dtype = {"bf16": "bfloat16", "fp16": "float16", "fp32": "float32"}[env_cfg.dtype]
    return LLM(model=model_name, dtype=dtype, seed=seed,
               gpu_memory_utilization=v["gpu_memory_utilization"],
               max_model_len=v["max_model_len"],
               limit_mm_per_prompt=v.get("limit_mm_per_prompt"))


def seg_seed(seed: int, seg_id: str) -> int:
    """Per-segment sampling seed: reproducible regardless of chunking / resume order."""
    return (seed * 1_000_003 + zlib.crc32(seg_id.encode())) % (2**31)


def generate(llm, model_name: str, segments: list[Segment], *, lang_cfg: dict, template: str,
             thinking: bool, n: int, temperature: float, top_p: float, max_tokens: int,
             seed: int) -> list[Rollout]:
    """One vLLM call. temperature == 0 -> greedy (n must be 1, sample_idx = -1)."""
    from vllm import SamplingParams

    greedy = temperature == 0
    if greedy and n != 1:
        raise ValueError("greedy decoding uses n=1")
    tok = llm.get_tokenizer()
    prompts = [tok.apply_chat_template(build_messages(s, lang_cfg, template), tokenize=False,
                                       add_generation_prompt=True, enable_thinking=thinking)
               for s in segments]
    params = [SamplingParams(n=n, temperature=temperature, top_p=1.0 if greedy else top_p,
                             max_tokens=max_tokens, seed=None if greedy else seg_seed(seed, s.seg_id))
              for s in segments]
    outputs = llm.generate(prompts, params, use_tqdm=True)

    def count(text: str) -> int:
        return len(tok.encode(text, add_special_tokens=False)) if text else 0

    rollouts = []
    for seg, out in zip(segments, outputs):
        n_prompt = len(out.prompt_token_ids)
        for i, comp in enumerate(out.outputs):
            reasoning, translation, ok = parse_output(comp.text, thinking)
            rollouts.append(Rollout(
                seg_id=seg.seg_id, sample_idx=-1 if greedy else i, model=model_name,
                thinking=thinking, temperature=temperature, raw_output=comp.text,
                reasoning=reasoning, translation=translation, n_prompt_tokens=n_prompt,
                n_reasoning_tokens=count(reasoning), n_translation_tokens=count(translation),
                finish_reason=str(comp.finish_reason), parse_ok=ok))
    return rollouts

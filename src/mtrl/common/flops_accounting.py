"""FLOPs accounting from token counts (pure functions; no torch).

Approximations: forward ~ 2*N*tokens, training step ~ 6*N*tokens.
Prompt tokens are counted once per rollout (no credit for vLLM prefix caching),
i.e. an upper bound on generation cost.
"""
from __future__ import annotations

from typing import Iterable


def forward_flops(n_tokens: int, n_params: float) -> float:
    return 2.0 * n_params * n_tokens


def train_flops(n_tokens: int, n_params: float) -> float:
    return 6.0 * n_params * n_tokens


def _get(r, k):
    return r[k] if isinstance(r, dict) else getattr(r, k)


def rollout_cost(rollouts: Iterable, n_params: float) -> dict:
    """Rollouts may be Rollout objects or dicts. Returns token totals and forward FLOPs per part."""
    tok = {"prompt": 0, "reasoning": 0, "translation": 0}
    for r in rollouts:
        tok["prompt"] += _get(r, "n_prompt_tokens")
        tok["reasoning"] += _get(r, "n_reasoning_tokens")
        tok["translation"] += _get(r, "n_translation_tokens")
    out = {f"{k}_tokens": v for k, v in tok.items()}
    out.update({f"{k}_flops": forward_flops(v, n_params) for k, v in tok.items()})
    out["total_flops"] = sum(out[f"{k}_flops"] for k in tok)
    return out


def scoring_cost(n_inputs: int, avg_tokens: float, n_params_scorer: float) -> float:
    return forward_flops(n_inputs * avg_tokens, n_params_scorer)

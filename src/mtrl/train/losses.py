"""Policy-gradient loss on token log-probabilities (pure torch).

Shapes: logp_new / logp_old / weights are [N, T] (N rollouts, T completion tokens),
adv is [N]. `weights` is the token mask from mtrl.train.masks (0 = no gradient,
fractional = down-weighted); padding must already be 0 there.

The surrogate is PPO's clipped objective with asymmetric bounds (DAPO clip-higher):
    ratio = exp(logp_new - logp_old)
    J = min(ratio * A, clip(ratio, 1 - clip_low, 1 + clip_high) * A)
summed over weighted tokens and divided by `denom` (DAPO token-level normalisation:
the total weight of all tokens in the step, so long and short rollouts count per token).

With a single update per rollout batch (ppo_epochs = 1) logp_old == logp_new.detach(),
the ratio is exactly 1, clipping never triggers and the gradient equals REINFORCE with
group-normalised advantages. That is what results/ym ran under the name "DAPO".
"""
from __future__ import annotations


def pg_loss(logp_new, logp_old, adv, weights, *, clip_low: float, clip_high: float, denom):
    """Returns (loss, stats) where stats holds detached diagnostics for logging."""
    import torch

    ratio = torch.exp(logp_new - logp_old)
    a = adv[:, None]
    surr = torch.minimum(ratio * a, torch.clamp(ratio, 1 - clip_low, 1 + clip_high) * a)
    loss = -(surr * weights).sum() / denom
    with torch.no_grad():
        valid = weights > 0
        clipped = ((ratio < 1 - clip_low) | (ratio > 1 + clip_high)) & valid
        stats = {"ratio_sum": float(ratio[valid].sum()), "n_tokens": int(valid.sum()),
                 "n_clipped": int(clipped.sum())}
    return loss, stats


def token_entropy(logits):
    """Entropy (nats) per position of [N, T, V] logits -> [N, T]."""
    import torch

    logp = torch.log_softmax(logits.float(), dim=-1)
    return -(logp.exp() * logp).sum(-1)

"""Group-relative advantages (GRPO / DAPO).

Rewards come as a [B, G] tensor: B source sentences, G sampled translations each. A
sample's advantage is its reward standardised within its own group, so the policy is
pushed towards translations that beat their siblings. A group whose rewards are all
equal carries no signal ("zero-variance"); its advantages are 0 and DAPO's dynamic
sampling resamples when no group in the step has signal.
"""
from __future__ import annotations

ZERO_VAR_EPS = 1e-6


def group_advantages(rewards, eps: float = 1e-8):
    """rewards [B, G] -> (advantages [B, G], live [B] bool).

    A = (r - mean_g) / (std_g + eps) with the population std (unbiased=False), as in
    results/ym; groups with std <= ZERO_VAR_EPS get A = 0 and live = False.
    """
    import torch

    r = rewards.float()
    mean = r.mean(dim=1, keepdim=True)
    std = r.std(dim=1, unbiased=False, keepdim=True)
    live = std.squeeze(1) > ZERO_VAR_EPS
    adv = torch.where(live[:, None], (r - mean) / (std + eps), torch.zeros_like(r))
    return adv, live

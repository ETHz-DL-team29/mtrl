"""Post-training (LoRA SFT and group policy-gradient RL); see docs/training.md.

    policy      model loading, LoRA targets, adapters
    advantage   group-relative advantages
    losses      clipped policy-gradient loss
    masks       token masks (registry)
    rl, sft     trainers; common holds their shared setup
    checkpoint  atomic save / resume
    evaluate    greedy evaluation shared by validation and scripts/eval_adapter.py
    prefixes    reasoning-prefix reuse (planned, not implemented)
"""

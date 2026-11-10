"""GRPO training loop (later stage; not implemented).

Rollouts come from mtrl.generation.vllm_generate, rewards from mtrl.scoring.reward (gate x MetricX-QE).
Token-selective backprop uses mtrl.train.masks; reasoning-prefix reuse uses
mtrl.train.prefixes. Every step logs B_test (generation + scoring) and B_back.
"""

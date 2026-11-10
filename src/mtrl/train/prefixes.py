"""Reasoning-prefix reuse (later stage; not implemented).

Generate a few reasoning prefixes per segment, share them across a GRPO group
(Rollout.prefix_id), resample only the translation, and optionally mask prefixes
at random. Purpose: reduce B_test (generation tokens per group).
"""

"""SFT training loop (later stage; not implemented).

Will fine-tune a Qwen3.5 policy on (src, ref) pairs and log B_back via
mtrl.common.flops_accounting.train_flops using the token counts of the supervised tokens.
"""

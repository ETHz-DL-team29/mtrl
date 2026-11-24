# qwen25-3b-sft-r0

2026-11-24 · English → Icelandic research adapter

- Stage
- Base `Qwen/Qwen2.5-3B-Instruct`.
- Base revision: `aa8e72537993ba99e69dfaafa59ed015b17504d1`.
- LoRA r=64, alpha=128; adapter weights are FP32 safetensors.
- Weight SHA256: `7f7a4914c5f403e757fdb882c3576ac68f2b0fa6edc00e537087716b28ddb07e`.
- Source experiment `r0_3b_recovery_sft_2026-11-21`.
- Base license

This is a LoRA delta, not standalone base weights. Load it over the pinned base for inference or further training. The loader overrides historical absolute base paths explicitly. Copies are hash-identical to the source: no merging, training or quantization occurred.

Only `qwen25-3b-sft-r0`, `qwen25-3b-dapo-reference` and `qwen25-3b-dapo-shortmid` have the matched WMT26 comparison in this delivery. Historical variants are not claimed to outperform the main baseline. Do not compare different data sets or multilingual means as if they were one benchmark.

Only the three specified 3B models have the matched WMT26 comparison; other models retain their own historical evidence. Research models still mistranslate negation, terminology and critical facts, and are not certified production systems. Use and redistribution remain subject to base-model and source-data terms.

## Public Hugging Face release

[huaq99/mtrl-qwen25-3b-en-is-sft-r0](https://huggingface.co/huaq99/mtrl-qwen25-3b-en-is-sft-r0) · revision `ae660dd4ea272fff7caf840d2c9ccc76401e6780`.

Public adapter download requires no HF login. Base-model and data license terms still apply.

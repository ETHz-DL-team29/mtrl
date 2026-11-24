# archive-r0-3b-round1-2026-11-17-final-trained-adapter

2026-11-24 · English → Icelandic research adapter

- Stage
- Base `Qwen/Qwen2.5-3B-Instruct`.
- Base revision: `aa8e72537993ba99e69dfaafa59ed015b17504d1`.
- LoRA r=16, alpha=32; adapter weights are FP32 safetensors.
- Weight SHA256: `1ecf014712c7eb0004eaa20de58f54b0346cc4bd67b0ce07e3c7e30084e6c41f`.
- Source experiment `r0_3b_round1_2026-11-17`.
- Base license

This is a LoRA delta, not standalone base weights. Load it over the pinned base for inference or further training. The loader overrides historical absolute base paths explicitly. Copies are hash-identical to the source: no merging, training or quantization occurred.

Only `qwen25-3b-sft-r0`, `qwen25-3b-dapo-reference` and `qwen25-3b-dapo-shortmid` have the matched WMT26 comparison in this delivery. Historical variants are not claimed to outperform the main baseline. Do not compare different data sets or multilingual means as if they were one benchmark.

Only the three specified 3B models have the matched WMT26 comparison; other models retain their own historical evidence. Research models still mistranslate negation, terminology and critical facts, and are not certified production systems. Use and redistribution remain subject to base-model and source-data terms.

# archive-r0-3b-filtered-sft-resume-2026-11-20-final-selected-adapter

2026-11-24 · English → Icelandic research adapter

- Stage
- Base `Qwen/Qwen2.5-3B-Instruct`.
- Base revision: `aa8e72537993ba99e69dfaafa59ed015b17504d1`.
- LoRA r=16, alpha=32; adapter weights are FP32 safetensors.
- Weight SHA256: `8eb880545d238f4af2695d08d6aba4f8f2f6f7a204b411d77d19539936b01ce0`.
- Source experiment `r0_3b_filtered_sft_resume_2026-11-20`.
- Base license

This is a LoRA delta, not standalone base weights. Load it over the pinned base for inference or further training. The loader overrides historical absolute base paths explicitly. Copies are hash-identical to the source: no merging, training or quantization occurred.

Only `qwen25-3b-sft-r0`, `qwen25-3b-dapo-reference` and `qwen25-3b-dapo-shortmid` have the matched WMT26 comparison in this delivery. Historical variants are not claimed to outperform the main baseline. Do not compare different data sets or multilingual means as if they were one benchmark.

Only the three specified 3B models have the matched WMT26 comparison; other models retain their own historical evidence. Research models still mistranslate negation, terminology and critical facts, and are not certified production systems. Use and redistribution remain subject to base-model and source-data terms.

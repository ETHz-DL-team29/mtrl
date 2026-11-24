# archive-r0-v2-colab-2026-11-12-best-adapter

2026-11-24 · English → Icelandic research adapter

- Stage
- Base `Qwen/Qwen3.5-0.8B`.
- Base revision: `2fc06364715b967f1860aea9cf38778875588b17`.
- LoRA r=16, alpha=32; adapter weights are FP32 safetensors.
- Weight SHA256: `806b9857024868131140da43ad3975d7c8653b97e5687420e4499a3769995847`.
- Source experiment `r0_v2_colab_2026-11-12`.
- Base license

This is a LoRA delta, not standalone base weights. Load it over the pinned base for inference or further training. The loader overrides historical absolute base paths explicitly. Copies are hash-identical to the source: no merging, training or quantization occurred.

Only `qwen25-3b-sft-r0`, `qwen25-3b-dapo-reference` and `qwen25-3b-dapo-shortmid` have the matched WMT26 comparison in this delivery. Historical variants are not claimed to outperform the main baseline. Do not compare different data sets or multilingual means as if they were one benchmark.

Only the three specified 3B models have the matched WMT26 comparison; other models retain their own historical evidence. Research models still mistranslate negation, terminology and critical facts, and are not certified production systems. Use and redistribution remain subject to base-model and source-data terms.

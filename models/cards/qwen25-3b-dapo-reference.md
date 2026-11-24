# qwen25-3b-dapo-reference

2026-11-24 · English → Icelandic research adapter

- Stage
- Base `Qwen/Qwen2.5-3B-Instruct`.
- Base revision: `aa8e72537993ba99e69dfaafa59ed015b17504d1`.
- LoRA r=64, alpha=128; adapter weights are FP32 safetensors.
- Weight SHA256: `104ad503ce563a46b54fcf6d6580e5da01c7fc9228f5e741e3adeb1d232d5852`.
- Source experiment `dapo_metricx_reference_2026-11-23`.
- Base license

This is a LoRA delta, not standalone base weights. Load it over the pinned base for inference or further training. The loader overrides historical absolute base paths explicitly. Copies are hash-identical to the source: no merging, training or quantization occurred.

Only `qwen25-3b-sft-r0`, `qwen25-3b-dapo-reference` and `qwen25-3b-dapo-shortmid` have the matched WMT26 comparison in this delivery. Historical variants are not claimed to outperform the main baseline. Do not compare different data sets or multilingual means as if they were one benchmark.

Only the three specified 3B models have the matched WMT26 comparison; other models retain their own historical evidence. Research models still mistranslate negation, terminology and critical facts, and are not certified production systems. Use and redistribution remain subject to base-model and source-data terms.

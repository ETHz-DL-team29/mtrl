# qwen25-3b-dapo-reference

2026-11-24 · English → Icelandic research adapter / 英→冰岛语研究适配器

- Stage / 阶段: dapo; role / 用途: dapo_historical.
- Base / 必需基座: `Qwen/Qwen2.5-3B-Instruct`.
- Base revision: `aa8e72537993ba99e69dfaafa59ed015b17504d1`.
- LoRA r=64, alpha=128; adapter weights are FP32 safetensors.
- Weight SHA256: `104ad503ce563a46b54fcf6d6580e5da01c7fc9228f5e741e3adeb1d232d5852`.
- Source experiment / 来源: `dapo_metricx_reference_2026-11-23`.
- Base license / 基座许可: qwen-research; https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/blob/aa8e72537993ba99e69dfaafa59ed015b17504d1/README.md

这是LoRA增量，不含完整基座；可以用同一固定基座加载推理或继续训练。保存配置中的历史绝对路径只作出处，统一加载器显式指定基座及revision。适配器与原文件逐字节校验一致，没有合并、重新训练或量化。

This is a LoRA delta, not standalone base weights. Load it over the pinned base for inference or further training. The loader overrides historical absolute base paths explicitly. Copies are hash-identical to the source: no merging, training or quantization occurred.

Only `qwen25-3b-sft-r0`, `qwen25-3b-dapo-reference` and `qwen25-3b-dapo-shortmid` have the matched WMT26 comparison in this delivery. Historical variants are not claimed to outperform the main baseline. Do not compare different data sets or multilingual means as if they were one benchmark.

仅上述三份3B模型具有本次匹配WMT26结果；其余模型以各自报告为准。研究模型仍会误译否定、术语和关键事实，不是经认证的生产翻译系统。用途及再分发遵守基座许可和原始语料条款，本交付不替换上游许可。

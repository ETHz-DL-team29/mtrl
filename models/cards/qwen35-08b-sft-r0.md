# qwen35-08b-sft-r0

2026-11-24 · English → Icelandic research adapter / 英→冰岛语研究适配器

- Stage / 阶段: sft; role / 用途: sft_baseline.
- Base / 必需基座: `Qwen/Qwen3.5-0.8B`.
- Base revision: `2fc06364715b967f1860aea9cf38778875588b17`.
- LoRA r=16, alpha=32; adapter weights are FP32 safetensors.
- Weight SHA256: `ebb4575fda36002c76ddb7e999a4e12c44a0be9ddb20b1e4e092d708e6a050e9`.
- Source experiment / 来源: `r0_v3_colab_2026-11-13`.
- Base license / 基座许可: Apache-2.0; https://huggingface.co/Qwen/Qwen3.5-0.8B/blob/2fc06364715b967f1860aea9cf38778875588b17/README.md

这是LoRA增量，不含完整基座；可以用同一固定基座加载推理或继续训练。保存配置中的历史绝对路径只作出处，统一加载器显式指定基座及revision。适配器与原文件逐字节校验一致，没有合并、重新训练或量化。

This is a LoRA delta, not standalone base weights. Load it over the pinned base for inference or further training. The loader overrides historical absolute base paths explicitly. Copies are hash-identical to the source: no merging, training or quantization occurred.

Only `qwen25-3b-sft-r0`, `qwen25-3b-dapo-reference` and `qwen25-3b-dapo-shortmid` have the matched WMT26 comparison in this delivery. Historical variants are not claimed to outperform the main baseline. Do not compare different data sets or multilingual means as if they were one benchmark.

仅上述三份3B模型具有本次匹配WMT26结果；其余模型以各自报告为准。研究模型仍会误译否定、术语和关键事实，不是经认证的生产翻译系统。用途及再分发遵守基座许可和原始语料条款，本交付不替换上游许可。

## Public Hugging Face release

[huaq99/mtrl-qwen35-08b-en-is-sft-r0](https://huggingface.co/huaq99/mtrl-qwen35-08b-en-is-sft-r0) · revision `c95800cbefea66cbe449a482c7515a74a6984564`.

Public adapter download requires no HF login. Base-model and data license terms still apply.

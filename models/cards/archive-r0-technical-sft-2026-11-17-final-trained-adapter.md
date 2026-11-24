# archive-r0-technical-sft-2026-11-17-final-trained-adapter

2026-11-24 · English → Icelandic research adapter / 英→冰岛语研究适配器

- Stage / 阶段: sft; role / 用途: sft_historical.
- Base / 必需基座: `Qwen/Qwen3.5-0.8B`.
- Base revision: `2fc06364715b967f1860aea9cf38778875588b17`.
- LoRA r=16, alpha=32; adapter weights are FP32 safetensors.
- Weight SHA256: `32dd7931c828d3c5ae069391cb7a4411acb70d8a93c670a1864276b375a2df52`.
- Source experiment / 来源: `r0_technical_sft_2026-11-17`.
- Base license / 基座许可: Apache-2.0; https://huggingface.co/Qwen/Qwen3.5-0.8B/blob/2fc06364715b967f1860aea9cf38778875588b17/README.md

这是LoRA增量，不含完整基座；可以用同一固定基座加载推理或继续训练。保存配置中的历史绝对路径只作出处，统一加载器显式指定基座及revision。适配器与原文件逐字节校验一致，没有合并、重新训练或量化。

This is a LoRA delta, not standalone base weights. Load it over the pinned base for inference or further training. The loader overrides historical absolute base paths explicitly. Copies are hash-identical to the source: no merging, training or quantization occurred.

Only `qwen25-3b-sft-r0`, `qwen25-3b-dapo-reference` and `qwen25-3b-dapo-shortmid` have the matched WMT26 comparison in this delivery. Historical variants are not claimed to outperform the main baseline. Do not compare different data sets or multilingual means as if they were one benchmark.

仅上述三份3B模型具有本次匹配WMT26结果；其余模型以各自报告为准。研究模型仍会误译否定、术语和关键事实，不是经认证的生产翻译系统。用途及再分发遵守基座许可和原始语料条款，本交付不替换上游许可。

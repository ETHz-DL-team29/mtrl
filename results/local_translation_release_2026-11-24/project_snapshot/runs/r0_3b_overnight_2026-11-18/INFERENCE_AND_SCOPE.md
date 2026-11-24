# Saved3B R0 candidate / 已保存3B候选 —2026-11-18

Base: D:/deep learning project/models/qwen2.5-3b-instruct
Revision: aa8e72537993ba99e69dfaafa59ed015b17504d1
Selected adapter: final_selected_adapter/
Read verdict.json and the full report before claiming DAPO readiness.
晋升与DAPO资格见verdict和完整报告；保存成功不代表语义或奖励已合格。

Explicitly load the pinned base with AutoModelForCausalLM,then PeftModel.from_pretrained(base,adapter_path). Ignore stale /content base paths in the adapter configuration.
显式加载base并附加adapter，不依赖配置中的/content路径。

Matched evaluation: BF16 base checkpoint loaded then full model.float(),FP32 adapter,TF32off,SDPA,greedy max320,prompt limit1024 with no silent source truncation,enable_thinking=False.
匹配评估：全模型FP32、关闭TF32、greedy最多320；不同精度/硬件可能改变输出。

Selected and last-trained adapters may differ. Exact resume requires the matching full snapshot,optimizer/RNG/cursor,data order,protocol and source identities. Do not use the last optimizer with an earlier selected adapter. Cross-stage SFT uses fresh AdamW and is not exact optimizer resume.
最佳与最后权重可能不同；精确断点续训须匹配同一完整快照，不能混配不同检查点。跨阶段使用新AdamW。

Old0.8B and original3B checkpoints were preserved. Budget records are historical fixed absolute timestamps;future runs require a separately authorized new directory and budget,not editing these frozen records.
旧模型保留。预算中的绝对截止时间是历史记录；新训练需另建目录和预算，不改写本轮冻结证据。

Run `python inference.py --text "This is a test."` with the recorded Torch/Transformers/PEFT environment. Default CUDA requires sufficient VRAM; `--device cpu` is slower. This helper does not allocate Colab or train. / 使用已记录的软件环境运行推理脚本；CPU较慢。脚本不申请Colab、不训练。

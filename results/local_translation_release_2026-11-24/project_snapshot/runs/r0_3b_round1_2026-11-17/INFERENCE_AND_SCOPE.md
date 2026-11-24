# 3B checkpoint / 3B检查点 — 2026-11-17

Base: D:/deep learning project/models/qwen2.5-3b-instruct
HF revision: aa8e72537993ba99e69dfaafa59ed015b17504d1
Candidate adapter: selected_candidate_adapter/
Final trained adapter: final_trained_adapter/ (may differ from selected)

Load the base explicitly with AutoModelForCausalLM,then attach PeftModel.from_pretrained(base,adapter_path). Do not depend on saved /content paths.
显式加载本地base再附加adapter，不依赖配置内/content路径。

Recorded final evaluation loads the base BF16 and FP32 adapter,then model.float().eval(),with TF32 disabled,greedy max320. G8 usesT=.7,top_p1,top_k0.
训练使用原生BF16冻结base和FP32 adapter；最终匹配评估提升FP32、关闭TF32。L4上运行；本机可用性取决于显存。

Read verdict.json/report before treating the candidate as a qualified R0. Saved successfully does not imply translation or reward readiness.
是否晋升必须查看verdict与报告，保存成功不等于翻译或奖励就绪。
Full-state snapshots retain optimizer/RNG/cursor/config/order identity. The adapter alone supports inference or a fresh optimizer,not an exact optimizer resume.
完整快照保留optimizer/RNG/cursor/配置及数据顺序；仅adapter不等于精确断点续训。

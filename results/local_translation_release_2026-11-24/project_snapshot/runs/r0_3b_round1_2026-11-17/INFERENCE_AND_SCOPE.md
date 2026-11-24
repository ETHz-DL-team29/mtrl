# 3B checkpoint

Base: D:/deep learning project/models/qwen2.5-3b-instruct
HF revision: aa8e72537993ba99e69dfaafa59ed015b17504d1
Candidate adapter: selected_candidate_adapter/
Final trained adapter: final_trained_adapter/ (may differ from selected)

Load the base explicitly with AutoModelForCausalLM,then attach PeftModel.from_pretrained(base,adapter_path). Do not depend on saved /content paths.
Explicitly load the local base, then attach the adapter; ignore historical /content base paths in the configuration.

Recorded final evaluation loads the base BF16 and FP32 adapter,then model.float().eval(),with TF32 disabled,greedy max320. G8 usesT=.7,top_p1,top_k0.
Training uses a native BF16 frozen base and FP32 adapter. Final matched evaluation promotes to FP32 with TF32 off. Execution was on L4; local usability depends on memory.

Read verdict.json/report before treating the candidate as a qualified R0. Saved successfully does not imply translation or reward readiness.
Check the verdict/report before promotion; successful saving does not establish translation/reward readiness.
Full-state snapshots retain optimizer/RNG/cursor/config/order identity. The adapter alone supports inference or a fresh optimizer,not an exact optimizer resume.
Full snapshots retain optimizer, RNG, cursor, configuration and data order. An adapter alone is not an exact resume.

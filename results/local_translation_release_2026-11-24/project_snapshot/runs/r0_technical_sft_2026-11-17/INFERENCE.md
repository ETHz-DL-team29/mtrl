# R0-TechSFT-v1 — inference

Original R0 fully preserved: D:/deep learning project/runs/r0_v3_colab_2026-11-13/nll_adapter.
Original R0 remains unchanged.

Frozen dev selection chooses t200000,step165,targettokens200770.
Selected candidate: selected_candidate_adapter. Final training endpoint: final_trained_adapter. If step0 is selected, the candidate contains original R0 weights and is not a new training gain.
If selection is step0,the selected adapter is original R0. The trained-final checkpoint remains separate.

Base: Qwen/Qwen3.5-0.8B revision2fc06364715b967f1860aea9cf38778875588b17。
Explicitly load the base, then PeftModel.from_pretrained(base,adapter_path,is_trainable=False). Do not let the old /content path in adapter_config determine base location.
Load the base explicitly,then attach the chosen adapter. Do not rely on a saved remote /content path as a local base location.

To match reported FP32: load the base through its original BF16 path, attach FP32 LoRA, then model.float().eval(), with TF32 off. Substituting another originally high-precision base does not reproduce the same setup.
For the recorded FP32 path,promote the originally loaded BF16-rounded base+FP32 LoRA with model.float().eval(),TF32 disabled.

Complete code/frozen data are in the experiment source bundle. The Colab notebook is a reproduction entry point; rerunning incurs additional training/CU and is unnecessary for reading the report.
The source bundle and notebook reproduce the run;re-running them consumes additional GPU time.

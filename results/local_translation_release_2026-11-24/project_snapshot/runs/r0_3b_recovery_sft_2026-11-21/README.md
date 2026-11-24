# P18 · 2026-11-21 / 22 · SFT recovery

未通过本项目预设候选能力门槛；作为已验收的实验候选归档，不应宣称合格DAPO基座。 / Failed the project qualification gate; archive as an evaluated candidate, not a qualified DAPO baseline.

原R0完整保留，拟合诊断权重没有用于正式续训。 / Original R0 preserved; fit-diagnostic weights never initialize production.

- Checkpoint: final_selected_adapter/ (read manifest before promotion)
- Inference: inference.py, FP32, greedy batch8, Colab
- Selected weights and qualification: final_selected_adapter_manifest.json
- Matched output metrics, semantic audit, training integrity: analysis/
- Immutable recovery snapshots: snapshots/
- Full source/data/evaluation/update logs: exported/
- Console logs: console_logs/
- Full bilingual MD/HTML report: D:\deep learning project\reports\r0_3b_recovery_sft_2026-11-21
- Frozen inputs and annotations: D:\deep learning project\experiments\r0_3b_recovery_sft_2026-11-21

# 0.8B检查点快速选择 / 0.8B checkpoint quick reference — 2026-11-17

- **冻结对照 / Frozen comparator**：`runs/r0_v3_colab_2026-11-13/nll_adapter`。旧DAPO与后续SFT的共同起点；同一128条匹配FP32诊断集chrF++34.567，BLEU15.701。
- **技术SFT选中候选 / Selected technical SFT200**：`runs/r0_technical_sft_2026-11-17/selected_candidate_adapter`。新增200770目标token、165更新；同一128条chrF++36.037，BLEU16.031。提升区间跨零，技术G8覆盖仍3/24，不能称已可靠改善。
- **技术SFT末期 / Final SFT400**：`runs/r0_technical_sft_2026-11-17/final_trained_adapter`。新增399895目标token、330更新；未选为最佳候选，不要与SFT200混用。
- **旧本地SFT / Earlier local SFT**：`runs/sft_round1/best`。保留历史结果；已核对其原始日志：step250在50条旧开发句上chrF++30.003（max_new_tokens96），step200为30.303；这里的count50是样本数。此前提到的约50分尚未在本清单中映射到确切评估协议，不能写成该checkpoint的原始综合分数。旧集与当前128条仍不可直接比较。
- **DAPO30 / Experimental DAPO30**：`experiments/dapo_fp32_control_2026-11-16/attempt_B/snapshots/step_030/files/adapter`。完整状态与记录保留；未证明翻译提升，不替代冻结R0。
- **32条拟合探针 / Tiny fitting probes**：`runs/r0_cause_diagnosis_2026-11-17/snapshots/A_lowLR/files/adapter`和`B_highLR/files/adapter`。能记住32条，开发集变差，不作为更强R0。

All paths are relative to D:/deep learning project. Full SHA256s and available state files are in CHECKPOINT_ALIASES_08B_2026-11-17.json;all57 canonical checkpoint paths are in the complete inventory.
以上路径均相对D:/deep learning project；快捷别名JSON包含完整SHA与状态路径，完整清单含57个检查点路径。

These are adapters. Load the local Qwen3.5-0.8B base explicitly,revision2fc06364715b967f1860aea9cf38778875588b17,then attach the chosen PEFT adapter. Saved historical /content paths are not current local paths. Adapter-only loading does not restore AdamW/RNG/data cursor.
这些文件是adapter，需要匹配base；精确续跑还需要完整optimizer、RNG及数据顺序等，不能只加载adapter。

Historical files such as R0_SELECTION_2026-11-13.json contain decisions made at the time,including needs_more_sft=true. The Nov17 diagnosis supersedes that certainty:neither an absolute0.8B SFT ceiling nor the necessity of moreSFT has been established. Preserve old files as provenance rather than silently rewriting them.
旧文件中的needs_more_sft=true是当时判断；11月17日诊断没有证明必须继续SFT或已到容量上限。旧文件原样保留供追溯，不应当作最新因果结论。

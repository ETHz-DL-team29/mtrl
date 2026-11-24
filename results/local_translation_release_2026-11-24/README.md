**最新实验优先 / Latest first: [P25结果摘要](../../LATEST_RESULTS.md)**

# 本地SFT/DAPO交付结果 / Local SFT/DAPO results

2026-11-24 · This index distinguishes official WMT data from historical ParIce project holdouts.

## 本次匹配WMT26对照 / Matched WMT26 comparison

198个官方英语→冰岛语文档，源文单元分别翻译后重组；完整官方refA不切分、不进入actor。三模型共享同样输入、greedy/FP32协议。

|Registry ID|chrF++|BLEU|
|---|---:|---:|
|`qwen25-3b-sft-r0`|39.7189|19.7572|
|`qwen25-3b-dapo-reference`|39.9116|20.8688|
|`qwen25-3b-dapo-shortmid`|40.8347|21.6973|

新DAPO相对SFT的chrF++差值95%区间[-0.0642,2.5631]，BLEU区间[-0.0685,5.2166]；点估计向好，仍未通过预设全量可靠提升门槛。240步实际训练，开发集选120步，没有按暂时下降早停；没有新增SFT。

Full-test paired intervals still include zero. The153-document source-length secondary analysis is positive but exploratory; the55all-short documents show no reliable gain. The original SFT R0 remains preserved. The new DAPO adapter is a research candidate, not a proven universally stronger SFT baseline.

- [完整双语报告 / Full bilingual report](project_snapshot/reports/wmt26_shortmid_night_2026-11-23/WMT26_AND_SHORTMID_DAPO_RESULTS_2026-11-23.html)
- [结论和下一步 / Interpretation](project_snapshot/reports/wmt26_shortmid_night_2026-11-23/CONCLUSIONS_AND_NEXT_STEP_2026-11-24.html)
- [全部24条逐例 / Complete24-source casebook](project_snapshot/reports/wmt26_shortmid_night_2026-11-23/WMT26_SEMANTIC_CASEBOOK_2026-11-24.html)
- [步骤与版本 / Executed workflow](project_snapshot/reports/wmt26_shortmid_night_2026-11-23/EXECUTION_REPRODUCIBILITY_2026-11-24.html)
- [原始科学结果ZIP / Raw scientific export](project_snapshot/runs/wmt26_shortmid_night_2026-11-23/p25_export.zip)
- [CPU分析 / CPU analyses](project_snapshot/runs/wmt26_shortmid_night_2026-11-23/analysis/)

## SFT模型及历史报告 / SFT models and historical reports

0.8B的R0-v3与技术候选在历史ParIce128条上的chrF++为34.567→36.037；这不是WMT26成绩，也不是与3B的匹配规模消融。历史SFT不同版本使用不同开发/评估集，不能拿最高数字排序成同口径模型排行榜。模型文件以registry相对路径为准；报告和JSON内原D盘路径仅作出处，不用于朋友加载。

0.8B historical ParIce numbers are not WMT scores. Other historical runs have different data/selection criteria and are not directly rankable. Use registry-relative artifact paths; original absolute D:/ paths in reports are provenance only. The archive retains reports, selected/final adapter variants with inference folders, and lightweight recorded outputs. It excludes base weights, private runtime controls, optimizer snapshots and every intermediate training weight.

- [dapo_metricx_reference_2026-11-23](project_snapshot/reports/dapo_metricx_reference_2026-11-23/DAPO_METRICX_REFERENCE_RESULTS_2026-11-23.html)
- [r0_3b_continue_2026-11-17](project_snapshot/reports/r0_3b_continue_2026-11-17/R0_3B_SFT_CONTINUATION_PLAN_2026-11-17.html)
- [r0_3b_coverage_sft_2026-11-20](project_snapshot/reports/r0_3b_coverage_sft_2026-11-20/R0_3B_COVERAGE_SFT_RESULTS_2026-11-20.html)
- [r0_3b_filtered_sft_2026-11-19](project_snapshot/reports/r0_3b_filtered_sft_2026-11-19/R0_3B_SFT_SEGMENT1_PAUSED_RESULTS_2026-11-19.html)
- [r0_3b_filtered_sft_resume_2026-11-20](project_snapshot/reports/r0_3b_filtered_sft_resume_2026-11-20/R0_3B_FILTERED_SFT_FINAL_RESULTS_2026-11-20.html)
- [r0_3b_fit_first_plan_2026-11-21](project_snapshot/reports/r0_3b_fit_first_plan_2026-11-21/R0_FIT_FIRST_PLAN_2026-11-21.html)
- [r0_3b_low_lr_recovery_2026-11-21](project_snapshot/reports/r0_3b_low_lr_recovery_2026-11-21/CONDITIONAL_RECOVERY_2026-11-21.html)
- [r0_3b_overnight_2026-11-18](project_snapshot/reports/r0_3b_overnight_2026-11-18/R0_3B_OVERNIGHT_RESULTS_2026-11-18.html)
- [r0_3b_recovery_sft_2026-11-21](project_snapshot/reports/r0_3b_recovery_sft_2026-11-21/R0_3B_RECOVERY_RESULTS_2026-11-21.html)
- [r0_3b_round1_2026-11-17](project_snapshot/reports/r0_3b_round1_2026-11-17/R0_3B_ROUND1_RESULTS_2026-11-17.html)
- [r0_3b_systematic_sft_2026-11-18](project_snapshot/reports/r0_3b_systematic_sft_2026-11-18/R0_3B_SYSTEMATIC_SFT_PLAN_2026-11-18.html)
- [r0_3b_systematic_sft_2026-11-19](project_snapshot/reports/r0_3b_systematic_sft_2026-11-19/R0_3B_SYSTEMATIC_SFT_DATA_QA_RESULTS_2026-11-19.html)
- [r0_3b_transition_2026-11-17](project_snapshot/reports/r0_3b_transition_2026-11-17/TRANSITION_AND_CHECKPOINTS_2026-11-17.html)
- [r0_cause_diagnosis_2026-11-17](project_snapshot/reports/r0_cause_diagnosis_2026-11-17/R0_CAUSE_DIAGNOSIS_RESULTS_2026-11-17.html)
- [r0_cause_review_2026-11-17](project_snapshot/reports/r0_cause_review_2026-11-17/R0_CAUSE_REVIEW_2026-11-17.html)
- [r0_g8_candidate_audit_2026-11-16](project_snapshot/reports/r0_g8_candidate_audit_2026-11-16/R0_G8_COVERAGE_AND_REWARD_AUDIT_2026-11-16.html)
- [r0_gpu_data_filter_2026-11-19](project_snapshot/reports/r0_gpu_data_filter_2026-11-19/R0_GPU_DATA_FILTER_RESULTS_2026-11-19.html)
- [r0_technical_sft_2026-11-17](project_snapshot/reports/r0_technical_sft_2026-11-17/TECHNICAL_SFT_RESULTS_2026-11-17.html)
- [r0_v2_2026-11-12](project_snapshot/reports/r0_v2_2026-11-12/R0_V2_RESULTS_2026-11-12.html)
- [r0_v3_2026-11-13](project_snapshot/reports/r0_v3_2026-11-13/R0_V3_RESULTS_2026-11-13.html)
- [wmt26_shortmid_night_2026-11-23](project_snapshot/reports/wmt26_shortmid_night_2026-11-23/WMT26_AND_SHORTMID_DAPO_RESULTS_2026-11-23.html)

## Source code / 执行源码

- [r0_3b_recovery_sft_2026-11-21](project_snapshot/experiments/r0_3b_recovery_sft_2026-11-21/source)
- [technical_sft_2026-11-17](project_snapshot/experiments/technical_sft_2026-11-17/source)
- [wmt26_shortmid_night_2026-11-23](project_snapshot/experiments/wmt26_shortmid_night_2026-11-23/source)

旧脚本的绝对Colab路径与历史预算没有被偷偷改写，不能用过期预算自动启动另一轮。合作者现有代码保留原样；新统一入口是 `scripts/models.py` 和 `mtrl.checkpoints`。原始完整实验目录仍在本机D盘备份中。

公开模型 / Public model downloads: [Hugging Face guide](../../models/HUGGING_FACE.md). GitHub has not been pushed.

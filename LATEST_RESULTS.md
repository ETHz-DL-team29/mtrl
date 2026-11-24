# 最新实验结果 / Latest experiment results

**2026-11-23—24 · P25短中句DAPO · 最新已完成 / Latest completed run**

原R0是P18的Qwen2.5-3B-Instruct SFT适配器；本轮从它重新开始，完成240次DAPO更新，按开发集固定规则选择120步。原R0与所有旧模型保留。本轮没有新增SFT。

Original R0 is the P18 Qwen2.5-3B-Instruct SFT adapter. The latest arm starts from it, completes240updates and selects step120 using dev only. Original R0 is preserved and no new SFT was performed.

## WMT26主对照 / Primary WMT26 comparison

198篇官方英语→冰岛语文档，源文切分翻译后重组，官方refA保持完整；FP32/greedy同口径。不是官方竞赛人工排名。

|模型 / Model|加载ID / Registry ID|chrF++|BLEU|
|---|---|---:|---:|
|原SFT R0|`qwen25-3b-sft-r0`|39.72|19.76|
|旧DAPO-120|`qwen25-3b-dapo-reference`|39.91|20.87|
|**最新专项DAPO-120**|**`qwen25-3b-dapo-shortmid`**|**40.83**|**21.70**|

**最新模型相对SFT：chrF++ +1.12，95%区间[-0.06,+2.56]；BLEU +1.94，区间[-0.07,+5.22]。点估计向好，但全量区间仍跨零，未通过事前固定的全量可靠提升标准。**

**The latest point estimates improve, but both full-test95%intervals include zero; the predeclared primary gain rule is not met. This is a promising candidate, not a proven universally stronger translation model.**

## 短中句与语义 / Length subsets and fidelity

- 153篇所有源单元≤40词的完整文档：chrF++40.42→41.88，BLEU17.33→20.33，配对区间均为正；分析是探索性补充、以speech为主、未校正多重比较，不能替代198篇主结论。
- 55篇所有单元≤12词的完整文档：未见可靠改善；不能宣称纯短句变强。
- 24个事前抽样源单元的同一助手盲化核查：19条实质内容中P4→5；另5条为格式/计数，单独报告。这不是独立母语认证或总体正确率。

The153-document short/medium secondary subset is positive but exploratory; the55all-short documents show no reliable gain. A small same-assistant audit gives limited semantic evidence and is not native-expert certification. All difficult cases remain in the primary benchmark.

## 打开结果 / Open the evidence

- [完整中英HTML报告](results/local_translation_release_2026-11-24/project_snapshot/reports/wmt26_shortmid_night_2026-11-23/WMT26_AND_SHORTMID_DAPO_RESULTS_2026-11-23.html)
- [完整Markdown报告](results/local_translation_release_2026-11-24/project_snapshot/reports/wmt26_shortmid_night_2026-11-23/WMT26_AND_SHORTMID_DAPO_RESULTS_2026-11-23.md)
- [结论、资源与下一步](results/local_translation_release_2026-11-24/project_snapshot/reports/wmt26_shortmid_night_2026-11-23/CONCLUSIONS_AND_NEXT_STEP_2026-11-24.html)
- [全部逐例核查](results/local_translation_release_2026-11-24/project_snapshot/reports/wmt26_shortmid_night_2026-11-23/WMT26_SEMANTIC_CASEBOOK_2026-11-24.html)
- [执行步骤与复现](results/local_translation_release_2026-11-24/project_snapshot/reports/wmt26_shortmid_night_2026-11-23/EXECUTION_REPRODUCIBILITY_2026-11-24.html)
- [结果图](results/local_translation_release_2026-11-24/project_snapshot/reports/wmt26_shortmid_night_2026-11-23/results_overview.png)
- [机器可读主指标](results/local_translation_release_2026-11-24/project_snapshot/runs/wmt26_shortmid_night_2026-11-23/wmt_shortmid/paired_metrics.json)
- [所有SFT/历史结果入口](results/local_translation_release_2026-11-24/README.md)
- [加载模型 / Use the models](models/README.md)

下一步建议固定本配方做独立seed复现，再开展选择性token更新或前缀复用的效率对照；建议的复现尚未启动。Baseline comparisons must continue to share the same original SFT R0.

公开模型 / Public model downloads: [Hugging Face guide](models/HUGGING_FACE.md). GitHub has not been pushed.

# 通用Qwen 3B翻译R0：过滤数据SFT结果 / Filtered-data SFT results

2026-11-20 · Europe/Berlin · Report UTC: 2026-11-20T13:48:45.976891+00:00

本轮有明确提升，新3B是这三个固定检查点中同集整体指标最好的版本；但还没有达到你要求的综合可靠翻译R0。主要剩余问题是冰岛语技术术语和中长句关键约束的生成。技术长句G8仍是0/24确认正确、3/24不确定。已核实从正确完整状态恢复、参数实际更新；模型容量上限没有被证明。

This continuation delivers clear gains and the best overall matched metrics among the three fixed checkpoints. It does not yet establish the comprehensive reliable translation R0 you requested. Remaining failures concern Icelandic technical vocabulary and key medium/long-sentence constraints. Long-sentence G8 has 0/24 confirmed positives and 3/24 uncertain groups. Full-state restoration and actual parameter updates were verified; a model-capacity ceiling was not established.

| 固定模型 / Fixed model | chrF++ (256) | BLEU (256) | G8确认覆盖 / Confirmed P | Greedy确认正确 / Confirmed P |
| --- | --- | --- | --- | --- |
| 保留0.8B / Historical 0.8B | 33.77 | 11.65 | 4/64 | 8/80 |
| 旧3B A / Original 3B A | 35.40 | 12.72 | 4/64 | 7/80 |
| 本轮3B / Selected 3B | 43.67 | 19.66 | 12/64 | 18/80 |

相对旧3B，整体chrF++提升+8.27，配对95%区间[6.76, 9.74]；技术中长句由35.27升至44.42。

Relative to original 3B, overall chrF++ improves by +8.27, with paired 95% interval [6.76, 9.74]. Technical medium/long chrF++ changes from 35.27 to 44.42.

<details><summary>权重身份、恢复与项目筛查记录 / Identity, recovery and screening details</summary>

最终交付开发集选中的t2999996，权重SHA256为8eb880545d238f4af2695d08d6aba4f8f2f6f7a204b411d77d19539936b01ce0。本轮保留轨迹累计2,999,996个新增目标token；今天从2,116,552目标token和1753步的完整状态恢复。固定256条最终样本chrF++为35.40→43.67，差值+8.27，配对95%区间[6.7563882858521636, 9.735427514090967]。技术中长句为35.27→44.42。

Deliver the development-selected t2999996 adapter, SHA256: 8eb880545d238f4af2695d08d6aba4f8f2f6f7a204b411d77d19539936b01ce0. The retained trajectory consumes 2,999,996 new target tokens, resuming today from 2,116,552 targets and 1753 updates. On 256 fixed final sources, corpus chrF++ changes 35.40→43.67, delta +8.27, paired 95% interval [6.76, 9.74]. Technical medium/long changes 35.27→44.42.

Semantic project screen / 语义项目筛查: SEMANTIC_PROJECT_TARGETS_NOT_DEMONSTRATED

Combined semantic/metric project screen / 语义及指标综合筛查: {"status": "PROJECT_SCREEN_NOT_DEMONSTRATED", "semantic_checks": {"G8_total_P_ge39": false, "G8_short_P_ge8": false, "G8_medium_P_ge12": false, "G8_long_P_ge12": false, "greedy_general_P_ge14": false, "greedy_technical_P_ge30": false}, "metric_checks": {"overall_chrf_delta_nonnegative": true, "technical_chrf_delta_nonnegative": true, "general_chrf_delta_at_least_minus1_5": true}, "not_a_universal_DAPO_gate": true, "not_native_certification": true}

</details>

同一64条技术源文、每条8候选，确认存在正确译文的覆盖为4/64→12/64；所选模型另有12组不确定U。固定80条greedy语义样本的确认正确数为7/80→18/80。U不等于错误，P也不是母语认证。

On the same 64 technical sources with 8 candidates each, confirmed-positive coverage is 4/64→12/64; the selected model has 12 additional uncertain groups. Confirmed correct greedy translations on the fixed 80-source semantic audit are 7/80→18/80. U is not an error label, and P is not native certification.

语义筛查与词面指标分开。只有已确认正确P计为覆盖，不确定U单列，未审查样本不冒充U或错误。即使未证明综合正式基线达标，也不意味着不能开展受限DAPO试验；MetricX奖励排序是否可靠仍需独立校准，本轮没有运行DAPO或MetricX。

Semantic screening is separate from overlap metrics. Credit only confirmed P; keep U separate and do not relabel unreviewed sources as U or incorrect. Failure to demonstrate a comprehensive formal baseline does not establish that a restricted DAPO pilot is impossible. MetricX ranking still needs independent calibration; no DAPO or MetricX is run in this phase.

## 1. 模型、任务和比较对象 / Actors,task and comparators

任务是英→冰岛语句段翻译，覆盖一般、技术短、中、长句；不是整篇文档或跨段一致性测试。主模型始终是通用Qwen/Qwen2.5-3B-Instruct，固定revision aa8e72537993ba99e69dfaafa59ed015b17504d1；原保留3B A为零更新对照。没有使用NLLB或其他专用翻译模型初始化。

The task is English-to-Icelandic segment translation across general and technical short/medium/long sources, not whole-document or cross-paragraph consistency. The actor remains general-purpose Qwen/Qwen2.5-3B-Instruct at revision aa8e72537993ba99e69dfaafa59ed015b17504d1; preserved 3B A is the zero-update comparator. No NLLB/translation-specialist initialization is used.

Original A SHA256: 9acc23c9595ac0b771bf8f21d125d18f3e993c3f449775377262e7ab73020199

0.8B对照在最终输出前固定为历史selected200k技术补强模型：Qwen/Qwen3.5-0.8B，revision2fc06364715b967f1860aea9cf38778875588b17，adapter SHA89c874b1e04b011c6ee3f41f499c373b47826a7f106b9d61eaa83fdce85c77ae。它是明确命名的历史保留版本，不是看到当前测试后重新挑出的“最优”。不同架构、分词器和训练历史意味着这不是纯参数规模消融。

The 0.8B comparator was fixed before final outputs: historical selected200k technical continuation of Qwen/Qwen3.5-0.8B, revision2fc06364715b967f1860aea9cf38778875588b17, adapterSHA89c874b1e04b011c6ee3f41f499c373b47826a7f106b9d61eaa83fdce85c77ae. It is an explicitly named historical retained version, not selected after this test. Different architectures, tokenizers and training histories prevent a pure parameter-count interpretation.

## 2. 数据、混合与保留集 / Data,mixture and holdouts

| 项目 / Item | 值 / Value |
| --- | --- |
| Frozen training pairs | 100642 |
| Unique-pool target tokens inclEOS | 4748344 |
| Pool SHA256 | ed37570b262f7653f7b9a240c1691753095664a85558c7a6f037f7107b0e3f73 |
| General/technical short/medium/long target-token mix | 25%/20%/30%/25% |
| Dev greedy / semantic / G8 | 128 /32 /24 |
| Final greedy / semantic / G8 | 256 /80 /64 |
| Retained unique exposed examples | 67382 |
| Retained example exposures | 81348 |

训练来自已GPU过滤的平行语料池，包括ParIce的EMA、EEA、ESO、OpenSubtitles、Tatoeba、TED和统计来源，并非全部WMT。阈值、隔离、抽检和来源处理完整记录在2026-11-19过滤报告；本轮没有降低质量阈值或把评估句加入训练。每对本轮新顺序最多2次，允许分层内重放；累计历史训练次数与被回滚的82次更新另计。

Training uses the GPU-filtered parallel pool including ParIce EMA/EEA/ESO/OpenSubtitles/Tatoeba/TED/statistics, not all-WMT data. Thresholds, isolation, audits and source handling are in the 2026-11-19 filter report. This phase neither relaxes quality thresholds nor trains evaluation sources. Each pair appears at most twice in this new schedule, with within-stratum replay; earlier history and82 rolled-back updates are separate.

开发/最终集合是官方ParIce21.10历史留出集的固定子集，不声称此前从未被评估。当前训练池和已追溯A训练源文的精确重叠为0。0.8B五个已保存候选训练池与当前开发/最终源文也未发现规范化精确重叠，但不能据此声称所有历史调用、文档近重复或预训练污染已排除。官方参考经结构检查，非母语专家逐句认证。

Development/final sources are fixed subsets of historical official ParIce21.10 holdouts, not never-evaluated benchmarks. Exact overlap with the current training pool and traced A training sources is zero. Five saved0.8B candidate training pools also show no normalized exact overlap with current dev/final sources; this does not exclude every historical invocation, document near-duplicate or pretraining contamination. Official references passed structural checks, not item-wise native certification.

## 3. 优化、恢复与预算 / Optimization,recovery and budget

| 项目 / Item | 设置 / Setting |
| --- | --- |
| Training objective | Global valid target-token mean causalCE inclEOS;prompt/pad excluded |
| LoRA | rank16,alpha32,dropout0.05,all7 q/k/v/o/gate/up/down projections |
| Measured trainable parameters | 29,933,568 in504 FP32 tensors;BF16 base frozen |
| Optimizer | AdamW betas0.9/0.999,eps1e-8,weight_decay0.01,clip1,initialpeakLR5e-5 |
| LR schedule | 60k target-token warmup,peak to first timing lock,cosine to1e-5 at3M |
| Batch / context | 32effective,micro4 withOOMfallback2/1;prompt1024,target512,total1536;no packing |
| Recovery origin | step1753,target2,116,552,cursor56096,fullAdam/RNG |
| First resumed update | {"step": 1754, "target_tokens": 2117740, "lr": 1.8599002056327167e-05, "grad_norm": 4.159056663513184, "mean_loss": 0.8679697039954188, "group_target_tokens": 1188} |

原3M计划的优化器、游标、随机状态、模型和学习率连续恢复，没有重新热身或重新从A开始。代码差异只涉及明确分段预算与一次可选500k尾段；原loss、更新函数、数据、顺序和协议逐项字节校验一致。新预算替代旧单段截止有独立SHA与清单修订证据；原协议和原预算副本保留。

The 3M schedule resumes full optimizer/cursor/RNG/model/LR state without new warmup or restarting from A. Code differences concern explicit segment budgeting and one optional 500k tail; loss/update/data/order/original-protocol files remain byte-verified. The new budget replacing the old continuous deadline has independent SHA/manifest proof; original protocol/budget copies remain preserved.

Extension gate / 追加门槛记录: {"accepted": false, "decision": {"UTC": "2026-11-20T12:49:37.495081+00:00", "checkpoint_sha256": "8eb880545d238f4af2695d08d6aba4f8f2f6f7a204b411d77d19539936b01ce0", "checks": {"technical_chrf_gain_ge_half": true, "coverage_not_down": true, "greedy_not_down": false, "general_preserved": true, "midlong_G8_not_down": true, "midlong_greedy_not_down": true, "some_midlong_semantic_gain": true, "tail_can_finish_and_be_reviewed_before_worker_selection": false}, "previous_checkpoint": "t2000188", "current_checkpoint": "t2999996", "midlong_before": {"greedy": 1, "G8": 4}, "midlong_after": {"greedy": 1, "G8": 6}, "reason": "Require observed medium/long semantic progress,not overlap improvement alone;runtime additionally enforces conservative time gate", "final_test_not_used": true, "tail_review_timing": {"estimated_training_and_dev_seconds": 3630.4331529475294, "review_reserve_seconds": 600, "worker_review_window_end_unix": 1795180877.7181003, "remaining_until_worker_review_end_seconds": 1900.2229936122894, "timing_amendment": "tail_review_feasibility_2026-11-20.json"}, "continue": false}, "estimated_required_seconds": 3627.854039740842, "remaining_training_seconds": 3397.919429540634, "no_LR_reset": true}

追加最多500k仅在已审查开发语义不下降、技术chrF至少+0.5、一般句不回退及保守计时足够时允许；尾段固定1e-5，不重置Adam或伸展已执行退火。今天用户上限4小时包含准备、上传、环境、训练、评估和导出，原两段累计GPU上限8小时保持；不为用满预算强训。

At most 500k extra targets are allowed only with reviewed non-regressing semantics, technical chrF gain≥0.5, general preservation and conservative timing feasibility. The tail uses1e-5 without resetting Adam or stretching executed decay. Today 4h includes preparation/upload/setup/training/evaluation/export and the original cumulative 8h GPU ceiling remains; no training is forced merely to fill time.

本轮未追加500k：3M的G8确认覆盖比2M多2组，但greedy确认正确数9→8，未通过预设“不下降”条件；此外保守尾段加复核不能赶上正在运行代码的最终开发复核截止。这个预算约束在查看3M语义输出前记录，未修改运行中的训练代码，也不代表已证明继续SFT无效。

The 500k tail was not taken:3M adds 2 confirmed G8 sources over 2M, but greedy P changes 9→8 and fails the prespecified non-regression condition. A conservative tail plus review also cannot fit the running worker’s final development-review cutoff. This timing constraint was recorded before viewing 3M semantic outputs, without changing running training code; it does not prove that further SFT is ineffective.

## 4. 开发轨迹与最终选择 / Development trajectory and final selection

![固定开发集、语义覆盖与保留轨迹 / Development,semantic coverage and retained trajectory](training_development_and_semantics.png)

| Targets | Overall chrF++ | General chrF++ | Technical mid/long chrF++ | G8 P/24 | Greedy P/32 |
| --- | --- | --- | --- | --- | --- |
| 0 | 36.32 | 32.50 | 36.61 | 2 | 4 |
| 500990 | 40.68 | 35.26 | 40.98 | not reviewed | not reviewed |
| 1001129 | 43.64 | 41.10 | 44.14 | 4 | 6 |
| 1501089 | 45.56 | 38.68 | 46.26 | not reviewed | not reviewed |
| 2000188 | 45.77 | 37.98 | 46.66 | 6 | 9 |
| 2501000 | 46.25 | 39.09 | 46.83 | not reviewed | not reviewed |
| 2999996 | 46.49 | 38.61 | 47.61 | 8 | 8 |

<details><summary>封存选择完整记录 / Complete sealed selection</summary>

{"tag": "t2999996", "step": 2543, "target_tokens": 2999996, "metrics": {"nll": 1.1306406443526344, "technical_nll": 1.113438619060956, "dev_target_tokens": 7762, "by_stratum": {"general": {"n": 32, "chrfpp": 38.614636057116606, "bleu": 15.534062052183817}, "technical_short": {"n": 32, "chrfpp": 43.358207627688806, "bleu": 20.36600694956158}, "technical_medium": {"n": 32, "chrfpp": 44.56981532302277, "bleu": 19.714936961743554}, "technical_long": {"n": 32, "chrfpp": 48.9653759111669, "bleu": 25.666730227525626}}, "overall_chrfpp": 46.48956123692833, "technical_chrfpp": 47.100046286045774, "technical_medium_long_chrfpp": 47.61391705001332, "failures": 0}, "adapter_sha256": "8eb880545d238f4af2695d08d6aba4f8f2f6f7a204b411d77d19539936b01ce0", "semantic": true, "review_summary": {"labels_locked": true, "adapter_sha256": "8eb880545d238f4af2695d08d6aba4f8f2f6f7a204b411d77d19539936b01ce0", "technical_sources": 24, "greedy_sources": 32, "coverage_P": 8, "coverage_U": 5, "greedy_P": 8, "greedy_U": 3, "labels_sha256": "e99c778143a20b252c74f2686985282ad9c2c814dc82efc1545675435042c409"}, "selection_reason": "Reviewed eligible maximum-coverage tie set,then greedy P,technical medium/long CHRF,earlier checkpoint"}

</details>

只有审查锁定且一般句chrF≥A−1.5、结构失败≤A+2的开发候选可选择。先比较G8确认覆盖；在最高覆盖相差≤1组的集合内，按greedy语义正确数、技术中长chrF、较早检查点选择。最终测试在权重封存后生成，未用来重选。相邻检查点单项分数波动不等同于综合退化或新最优。

Select only locked-review candidates with general chrF≥A−1.5 and failure count≤A+2. Use G8 confirmed coverage, then within 1 group of the maximum use greedy semantic P, technical medium/long chrF and earlier checkpoint. Final outputs are generated after sealing, without reselection. A one-metric checkpoint fluctuation is neither comprehensive regression nor a new overall optimum.

## 5. 最终同集翻译指标 / Matched final translation metrics

![同一最终源文的匹配精度评估 / Same-source,matched-precision final evaluation](matched_final_quality.png)

| Subset | n | A chrF++ | Selected chrF++ | Delta [95%CI] | A BLEU | Selected BLEU |
| --- | --- | --- | --- | --- | --- | --- |
| overall | 256 | 35.40 | 43.67 | +8.27 [6.76, 9.74] | 12.72 | 19.66 |
| general | 64 | 39.64 | 42.64 | +3.00 [0.30, 5.57] | 20.90 | 22.70 |
| technical_short | 64 | 33.05 | 38.61 | +5.56 [3.50, 7.74] | 14.37 | 17.09 |
| technical_medium | 64 | 34.45 | 43.97 | +9.52 [7.18, 11.82] | 11.38 | 18.91 |
| technical_long | 64 | 35.64 | 44.62 | +8.98 [6.48, 11.39] | 11.76 | 19.63 |
| technical | 192 | 35.00 | 43.71 | +8.71 [7.15, 10.30] | 11.97 | 19.36 |
| technical_medium_long | 128 | 35.27 | 44.42 | +9.15 [7.41, 10.93] | 11.66 | 19.65 |

| Subset | n | Historical0.8B chrF++ | Old3B A | Selected3B | Selected−0.8B [95%CI] |
| --- | --- | --- | --- | --- | --- |
| overall | 256 | 33.77 | 35.40 | 43.67 | +9.90 [7.98, 11.73] |
| general | 64 | 40.57 | 39.64 | 42.64 | +2.07 [-0.95, 4.88] |
| technical_short | 64 | 32.09 | 33.05 | 38.61 | +6.52 [3.65, 9.40] |
| technical_medium | 64 | 33.89 | 34.45 | 43.97 | +10.08 [7.55, 12.62] |
| technical_long | 64 | 33.07 | 35.64 | 44.62 | +11.55 [8.82, 14.28] |
| technical_medium_long | 128 | 33.31 | 35.27 | 44.42 | +11.11 [8.94, 13.29] |

所有3B最终生成均为nativeBF16 base+FP32LoRA、TF32关闭、greedy batch8，采样G8为T0.7/top_p1/top_k0/max512、固定源文种子。2,000次配对bootstrap重采样源文并重算语料充分统计，不平均单句分数充当corpus指标。区间仅描述当前样本，未覆盖训练种子、文档聚类、反复开发选择或语义审查误差。

Final3B inference uses native BF16 base+FP32LoRA, TF32off, greedy batch8; G8 usesT0.7/top_p1/top_k0/max512 and fixed source seeds. The 2,000 paired bootstrap resamples sources and recomputes corpus sufficient statistics, rather than substituting sentence-score averages. Intervals cover this source sample, not training seeds, document clusters, adaptive development selection or annotation errors.

## 6. 最终源文语义与DAPO起点判断 / Final source semantics and R0 interpretation

![相同技术源文八候选的确认覆盖、不确定与全错误组 / Confirmed,uncertain and fully rejected G8 groups on matched technical sources](final_candidate_semantic_coverage.png)

| Model | Role/stratum | Expected | Reviewed | P/F/U | Not reviewed |
| --- | --- | --- | --- | --- | --- |
| before | greedy_general | 20 | 20 | {"F": 15, "U": 1, "P": 4} | 0 |
| before | greedy_technical_short | 20 | 20 | {"P": 3, "F": 15, "U": 2} | 0 |
| before | greedy_technical_medium | 20 | 20 | {"F": 19, "U": 1} | 0 |
| before | greedy_technical_long | 20 | 20 | {"F": 20} | 0 |
| before | G8_technical_short | 16 | 16 | {"F": 13, "U": 2, "P": 1} | 0 |
| before | G8_technical_medium | 24 | 24 | {"F": 20, "P": 3, "U": 1} | 0 |
| before | G8_technical_long | 24 | 24 | {"F": 24} | 0 |
| after | greedy_general | 20 | 20 | {"P": 10, "F": 10} | 0 |
| after | greedy_technical_short | 20 | 20 | {"F": 16, "P": 3, "U": 1} | 0 |
| after | greedy_technical_medium | 20 | 20 | {"P": 5, "F": 14, "U": 1} | 0 |
| after | greedy_technical_long | 20 | 20 | {"F": 20} | 0 |
| after | G8_technical_short | 16 | 16 | {"F": 8, "P": 5, "U": 3} | 0 |
| after | G8_technical_medium | 24 | 24 | {"P": 7, "U": 6, "F": 11} | 0 |
| after | G8_technical_long | 24 | 24 | {"F": 21, "U": 3} | 0 |
| old08 | greedy_general | 20 | 20 | {"F": 13, "P": 6, "U": 1} | 0 |
| old08 | greedy_technical_short | 20 | 20 | {"F": 17, "P": 2, "U": 1} | 0 |
| old08 | greedy_technical_medium | 20 | 20 | {"F": 18, "U": 2} | 0 |
| old08 | greedy_technical_long | 20 | 20 | {"F": 20} | 0 |
| old08 | G8_technical_short | 16 | 16 | {"F": 14, "P": 2} | 0 |
| old08 | G8_technical_medium | 24 | 24 | {"P": 2, "F": 21, "U": 1} | 0 |
| old08 | G8_technical_long | 24 | 24 | {"F": 24} | 0 |

Paired confirmed-coverage analysis / 配对确认覆盖分析: {"before": 4, "after": 12, "net_source_gain": 8, "gain95CI_sources": [2.0, 14.0], "replicates": 2000, "interpretation": "Confirmed-positive audit coverage only;U is not called incorrect. Interval conditions on this AI-assisted annotation and source sample,not native truth/training seeds."}

Prespecified project screening / 预设项目筛查: {"status": "SEMANTIC_PROJECT_TARGETS_NOT_DEMONSTRATED", "checks": {"G8_total_P_ge39": false, "G8_short_P_ge8": false, "G8_medium_P_ge12": false, "G8_long_P_ge12": false, "greedy_general_P_ge14": false, "greedy_technical_P_ge30": false}, "not_a_universal_DAPO_gate": true, "meaning": "Comprehensive project baseline screen;does not establish that a restricted DAPO pilot is impossible if targets are missed."}

P要求关键含义、角色、数字、否定和子句保留，允许轻微屈折/风格问题；G8至少一个未截断P才计覆盖，F须看完全部不同候选。U不冒充错误，未审查数量单独记录。只评存在性覆盖，不因找到一个P就假设另外7个均正确或均错误，也不据此估计逐候选正确概率。

P requires key meaning, roles, numbers, negation and clauses with minor inflection/style errors allowed. G8 coverage needs at least one untruncated P; F requires every distinct candidate. U is not represented as error, and unreviewed counts stay separate. This audits existential coverage, not per-candidate accuracy: finding oneP does not label the other seven.

预设39/64及分层/greedy目标只是本项目综合基座筛查，并非DAPO通用硬门槛。若未证明达标，结论是综合可靠性未建立；可以另行在正确候选与奖励对照通过的任务上开展受限试验。没有本轮MetricX数据，不能把SFT进步解释为评分器已修好，也不能根据一次小规模DAPO或这次SFT推断模型容量上限。

The 39/64 and stratum/greedy targets are project screening criteria, not universal DAPO admission rules. Missing them means comprehensive reliability is not established; restricted pilots may still be reasonable on separately calibrated tasks. This phase has no new MetricX evidence: SFT gains do not repair the reward model, and neither one small DAPO pilot nor this SFT proves a capacity ceiling.

语义审查由同一AI助手完成，卡片隐藏检查点名称但上下文无法完美隔离，非母语专家认证。最终80条greedy样本在输出前按源文哈希冻结，G8使用全部固定64条；最终标签仅用于评估，不选择权重或修改训练数据。

Semantic review uses the same AI assistant with checkpoint names hidden but imperfect context blinding, without native-speaker certification. The 80 greedy sources were hash-frozen before outputs and G8 uses all 64 fixed sources. Final labels evaluate the sealed model and never select weights or alter training data.

0.8B补充卡片在两组3B完成后加入，因此其所属阶段可推断，并非严格双盲比较；所有432张最终卡均已完成，标签和卡片哈希另行锁定。相同源文/译文的2059项确定性审查记录未发现P/F矛盾。

Supplementary0.8B cards were added after the two3B banks, so their phase is inferable; this is not a strict double-blind comparison. All 432 final cards are complete and card/label hashes are locked. The 2059 definitively reviewed identical source/hypothesis texts have no P/F contradiction.

## 7. 限制和描述性原因线索 / Limitations and descriptive diagnostic clues

<details><summary>改善示例 / Improvement example · p13official21:test:ema:1152</summary>

English: Change from baseline in body weight was similar for patients treated with sitagliptin relative to placebo.

Old3B A [F]: Þyngdarskammtur frá upphafsgildi var svipað fyrir sjúklinga sem fengu sitagliptín samanborið við lyfleysu.

Body-weight change is replaced by weight dose.

Selected3B [P]: Breyting frá grunngildi á líkamsþyngd var svipuð hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.

Body-weight change from baseline similar for sitagliptin versus placebo retained.

</details>

<details><summary>退步示例 / Regression example · p13official21:test:eea:1503</summary>

English: If this kind of costs exists, they will be reported separately.

Old3B A [P]: Ef slík kostnað er til stöður verða þær greint í sér.

Conditional existence of costs and separate reporting retained despite inflection.

Selected3B [F]: Ef slík kosti eru til koma þeir til skýrslu í sérstökum skilyrðum.

Separately reported becomes reporting under special conditions.

</details>

<details><summary>持续错误示例 / Persistent-error example · p13official21:test:eea:1144</summary>

English: Successful participation in interlaboratory studies that assess laboratory proficiency is the best way to prove the competence in specific analyses.

Old3B A [F]: Viðurkenning í samanburðum milli rannsóknarstofa sem meta hæfni rannsóknarstofa er besta aðferð til að sýna fram á skilvirkleika í sérstökri greiningu.

Successful participation becomes recognition and analytical competence becomes efficiency.

Selected3B [F]: Reynsla í samstarfsrannsóknum á rannsóknarþjálfun sem meta þjálfa rannsóknarstofa er besta leiðin til að sýna fram á færni í sérstökum greiningum.

Successful interlaboratory participation becomes experience; laboratory-proficiency relation corrupted.

</details>

以上示例各取对应标签变化类别中源文ID排序第一条，只作定性说明，不代表错误比例；完整样本和标签在逐条附录中。

Each example is the first source ID in its label-transition category, for qualitative illustration rather than an error-rate estimate. The complete sample and labels appear in the item-level appendix.

Domain/exposure diagnostic / 来源暴露诊断: [{"target_limit": 2116552, "actual_targets": 2116552, "unique_sources": 50908, "source_target_tokens": {"OpenSubtitles18": 326512, "eea": 437621, "statisl": 38546, "ema": 1050577, "tatoeba": 132449, "eso": 99247, "ted2020": 31600}, "source_fractions": {"OpenSubtitles18": 0.15426599488224244, "eea": 0.20676127966617405, "statisl": 0.018211695247742556, "ema": 0.4963624801091587, "tatoeba": 0.06257772074581679, "eso": 0.0468908866874048, "ted2020": 0.014929942661460716}}, {"target_limit": 3000000, "actual_targets": 2999996, "unique_sources": 67382, "source_target_tokens": {"OpenSubtitles18": 541894, "eea": 601784, "statisl": 38546, "ema": 1522187, "tatoeba": 137938, "eso": 126047, "ted2020": 31600}, "source_fractions": {"OpenSubtitles18": 0.18063157417543224, "eea": 0.20059493412657883, "statisl": 0.012848683798245065, "ema": 0.5073963431951243, "tatoeba": 0.04597939463919285, "eso": 0.04201572268763025, "ted2020": 0.010533347377796504}}, {"target_limit": 3500000, "actual_targets": 3499972, "unique_sources": 73302, "source_target_tokens": {"OpenSubtitles18": 666897, "eea": 694781, "statisl": 38546, "ema": 1788953, "tatoeba": 137938, "eso": 141257, "ted2020": 31600}, "source_fractions": {"OpenSubtitles18": 0.1905435243481948, "eea": 0.19851044522641895, "statisl": 0.011013230962990561, "ema": 0.5111335176395697, "tatoeba": 0.0394111724322366, "eso": 0.04035946573286872, "ted2020": 0.00902864365772069}}]

3M保留顺序中EMA约50.7%目标token、ESO约4.2%，而最终源文中ESO66/256；来源和长度混合并不等于所有技术子领域均衡。字面短语出现次数只是描述性覆盖线索，不是因果证明，也不能据此修改受保护测试句。语义错误可能涉及词汇、数值、条件和长依赖；更低NLL或更高重合度不能单独排除这些问题。

At 3M, EMA supplies about 50.7% of target exposure and ESO about 4.2%, while ESO contributes66/256 final sources. Length/source mixing is not balanced coverage of every technical subdomain. Literal phrase counts are descriptive clues, not causal evidence or permission to train protected test cases. Errors can concern terminology, numbers, conditions and long dependencies; lowerNLL/higher overlap alone does not exclude them.

Literal cue counts / 字面短语计数: {"frequency band": {"unique_train_source_occurrences": 3, "note": "Literal substring count only;not semantic/tokenizer coverage or proof of causality"}, "tilt of the orbit": {"unique_train_source_occurrences": 0, "note": "Literal substring count only;not semantic/tokenizer coverage or proof of causality"}, "yellow fever": {"unique_train_source_occurrences": 13, "note": "Literal substring count only;not semantic/tokenizer coverage or proof of causality"}, "pharmacodynamic": {"unique_train_source_occurrences": 119, "note": "Literal substring count only;not semantic/tokenizer coverage or proof of causality"}, "gamma-ray burst": {"unique_train_source_occurrences": 2, "note": "Literal substring count only;not semantic/tokenizer coverage or proof of causality"}, "maturity band": {"unique_train_source_occurrences": 0, "note": "Literal substring count only;not semantic/tokenizer coverage or proof of causality"}}

实际保留更新覆盖67,382/100,642个不重复训练对，涉及2,638,284/4,748,344个不重复目标token；另有33,260对、2,110,060目标token尚未进入本轮保留轨迹，主要是EMA/EEA。这里的未见仅指本轮新顺序，不代表模型历史或预训练从未接触。

The retained updates cover67,382/100,642 unique pairs and2,638,284/4,748,344 unique target tokens. Another 33,260 pairs and2,110,060 targets have not entered this retained schedule, primarily EMA/EEA. Unseen here refers to the new schedule, not all previous training or pretraining.

这不足以证明3B容量已达上限。也不能把“补齐剩余训练池”直接等同于修复天文长句：剩余未覆盖样本只有EMA/EEA，而天文ESO在当前池内已被覆盖；需要区分总训练量与薄弱子领域的数据量。

This does not prove a3B capacity ceiling. Completing the remaining pool also cannot be equated with repairing astronomical long sentences: remaining sources are EMA/EEA, while the current ESO pool has already been exposed. Total training volume and weak-domain data volume are distinct.

这是一次单训练种子的有界连续SFT，数据过滤、训练规模和混合共同变化，不能单独把收益归因于某一因素；对0.8B的比较也非同训练量对照。没有验证整篇文档、跨段一致性或其他语向。下一步以已保存最优模型为起点，是否继续SFT或进入DAPO应分别依据候选能力和独立奖励排序证据，避免仅凭某个chrF数值或短句正确率决定。

This is a bounded single-seed continuation with jointly changed filtering, scale and mixture, not an isolated causal ablation. The 0.8B comparison is not matched training exposure. Whole documents, cross-paragraph consistency and other language directions are untested. Future SFT versus DAPO decisions should separately examine candidate capability and independent reward ranking, not one chrF number or short-sentence correctness.

G8覆盖结论只适用于本次固定T=0.7及8候选配置，不是模型可产生正确译文的理论上界。没有在最终集上搜索温度、增加G或重选模型；低温采样是否能改善候选供给仍属未测试方案。

G8 coverage applies to the fixed T=0.7/eight-candidate configuration, not a theoretical capability ceiling. No final-test temperature search, increased G or model reselection was performed. Whether lower-temperature sampling improves candidate supply remains untested.

## 8. 计算、保存与复现 / Compute,persistence and reproduction

| 计算 / Compute | 本轮记录 / Recorded value |
| --- | --- |
| GPU allocated | 150.2 minutes |
| Observed compute-unit balance drop | 4.82 |
| Cumulative filtered-SFT GPU allocation | 5.95 hours |
| GPU released / Deadline met | True / True |
| Today retained target tokens | 883444 |

<details><summary>完整资源账本 / Complete resource ledger</summary>

{"UTC": "2026-11-20T13:41:05.130751+00:00", "owned_runtime_released": true, "account_assigned_runtime_count": 0, "current_account_consumption": {"paid_compute_units_balance": 239.41670526926325, "consumption_rate_hourly": 0.0, "assignments_count": 0}, "segment2_allocated_seconds": 9012.361103534698, "segment2_allocated_minutes": 150.20601839224497, "segment1_allocated_seconds": 12395.729388237, "cumulative_filtered_SFT_GPU_hours": 5.946691803269916, "today_hard_deadline_unix": 1795186877.7181003, "released_unix": 1795182000.2210627, "hard_deadline_met": true, "initial_compute_units": 244.23880510341385, "final_compute_units": 239.41670526926325, "observed_account_compute_unit_drop": 4.822099834150606, "account_balance_drop_not_claimed_exact_invoice": true, "segment1_observed_compute_unit_drop": 6.577003469176191, "new_retained_training_seconds": 4179.083923874003, "new_retained_target_tokens": 883444, "new_training_target_tokens_per_second": 211.39656826538413, "retained_total_target_tokens": 2999996, "NVML_peak_total_GPU_used_MiB": 20340.0}

</details>

所有新完整检查点保存adapter、Adam、RNG、游标和绑定哈希，并经分块/整包SHA与文件清单校验同步D盘。最终导出双份校验；所选adapter单独交付，原A和0.8B文件保留。首个新checkpoint已证明adapter权重变化，恢复合同、控制通道重连、预算清单修订及所有源代码均归档。

Every new full state preserves adapter, Adam, RNG, cursor and hashes with per-chunk/archive/file verification on D. Final export has two verified copies, the selected adapter is delivered separately, and original A/0.8B remain preserved. The first new checkpoint demonstrates changed weights. Recovery contracts, channel recovery, budget-manifest amendment and all code are archived.

| 内容 / Content | 文件 / Artifact |
| --- | --- |
| Selected usable adapter | D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\final_selected_adapter |
| Selected identity manifest | D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\final_selected_adapter_manifest.json |
| Verified final export | D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\verified_export.json |
| All new full states | D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\snapshots |
| All prior full states | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\snapshots |
| Matched metrics and bootstrap | D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\analysis\matched_final_metrics.json |
| 0.8B comparison | D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\analysis\matched_08b_3b_metrics.json |
| Final semantic analysis | D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\analysis\final_semantic_analysis.json |
| Development cards/labels | D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\development_review |
| Final cards/labels | D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\final_semantic_review |
| Original frozen source | D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\source |
| Execution manifest and amendments | D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\control_evidence |
| Budget/extension protocol | D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\protocol_amendment.json |
| All execution tools | D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\execution_tools |
| Running record | D:\deep learning project\reports\r0_3b_filtered_sft_resume_2026-11-20\R0_3B_FULL_STATE_CONTINUATION_RECORD_2026-11-20.html |

## 9. 明确下一步 / Concrete next step

保留本轮3M检查点作为当前最强实验R0。若目标仍是综合技术翻译，下一轮SFT应优先补足有可靠冰岛语目标文本的技术术语、法律/科学说明及带条件/否定/数值约束的中长句，并同时保留一般句；训练量按不重复目标token和领域分别核算。只消耗剩余EMA/EEA或沿相同配比追加少量步数，不是有证据保证能修复天文长句的办法。

Preserve the 3M checkpoint as the strongest current experimental R0. For comprehensive technical translation, the next SFT data revision should prioritise reliable Icelandic targets covering technical vocabulary, legal/scientific explanations and medium/long conditional/negative/numeric constraints, while retaining general examples. Account for unique target tokens and domains separately. Consuming remaining EMA/EEA or adding a few steps at the same mixture is not an evidenced guarantee of fixing astronomical long sentences.

新增训练材料必须来自训练侧，不能把本次开发或最终句及其改写加入训练；下一轮确认性评估应另行预留独立样本。先把可用新增领域数据的数量、质量和训练预算写清楚，再启动一次有明确规模的续训，避免多轮碎片试验。当前数据只证明继续学习仍有机会，不能承诺再训固定几小时就达标。

New material must come from training-side sources, excluding these dev/final sentences and their paraphrases. Reserve separate independent sources for the next confirmatory evaluation. Establish available domain-data quantity, quality and an explicit training budget before one substantial continuation, rather than repeated fragmented runs. Current evidence supports remaining learning potential, not a guarantee that another fixed number of hours will qualify the model.

DAPO可以先限定在已有正确候选的任务上做小预算对照：温度/G在开发集确定，独立检查奖励能否把正确候选排在已确认错译之上，然后冻结R0、数据、奖励和采样设置。全任务正式效率比较暂不作为本轮验收结论；这不是“不能跑DAPO”，也不是“已证明MetricX是唯一问题”。本轮GPU已释放，不自动申请下一轮。

A small DAPO comparison remains possible on tasks with established correct candidates: choose temperature/G on development sources, independently verify that reward ranks correct translations above confirmed errors, and freeze R0/data/reward/sampling. This run does not qualify a comprehensive all-task efficiency comparison, nor prove that DAPO is impossible or MetricX is the sole problem. The GPU has been released and no next allocation starts automatically.

## 10. 完整逐条审查与输出 / Complete item-level audit and predictions

下列附录展示全部语义审查卡片与各卡全部候选。256条完整greedy预测、completion token ID和其余未抽入80条语义子集的输出，另完整保存在JSONL原始结果中；未作语义标注不等于生成结果缺失。

The appendix shows every semantic-review card and every candidate on those cards. Complete256-source greedy predictions, completion-token IDs and sources outside the 80-item semantic subset are retained in raw JSONL. Absence of a semantic label does not mean a missing generation.

| Raw results / 原始结果 | File / 文件 |
| --- | --- |
| before_greedy.jsonl | D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\exported\run\evaluation\before_greedy.jsonl |
| after_greedy.jsonl | D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\exported\run\evaluation\after_greedy.jsonl |
| before_g8.jsonl | D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\exported\run\evaluation\before_g8.jsonl |
| after_g8.jsonl | D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\exported\run\evaluation\after_g8.jsonl |

| Historical0.8B / 历史0.8B | File / 文件 |
| --- | --- |
| old08_greedy.jsonl | D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\comparison08_exported\evaluation\old08_greedy.jsonl |
| old08_g8.jsonl | D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\comparison08_exported\evaluation\old08_g8.jsonl |

<details><summary>development_review #0 · t2000188 · greedy · technical_medium · U</summary>

Source ID: p13official21:dev:eso:1051

English: The technique used by Teague, which derived averaged variations in the flow of the gas as small as a few percent, revealed the impact of multiple planets on the gas motions nearer to the star.

Reference (shown after audit): Tæknin sem Teague beitti sýndi meðalbreytingarnar á gasflæðinu niður í nokkur prósent og leiddi í ljós áhrif nokkurra plánetna á hreyfingu gassins nær stjörnunni.

Review: Average gas-flow variation and planetary phrase are malformed; fidelity uncertain.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Tæknið sem Teague notaði, sem leiddi til meðalþéttnar breytinga á flæði gassins eins minnar og nokkrum prozentum, sýndi áhrif fjölskyldu reikistjarna á flæði gassins nálægri stjörnunni.

</details>

<details><summary>development_review #1 · t2000188 · G8 · technical_short · U</summary>

Source ID: p13official21:dev:ema:767

English: Therefore, docetaxel must not be used during pregnancy unless clearly indicated.

Reference (shown after audit): Dócetaxel á því ekki að nota á meðgöngu nema brýna nauðsyn beri til.

Review: Pregnancy prohibition retained but clear clinical indication not reliably rendered.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Því má ekki nota docetaxel á meðgöngu nema áhrifin séu skýra til kynna.

Candidate 1: Því má ekki nota docetaxel á meðgöngu nema sprautur leggja á.

Candidate 2: Því má ekki nota doketaxel á meðgöngu nema tilkynnt sé á klárlegan hátt.

Candidate 3: Því má ekki nota docetaxel á meðgöngu nema greinilega áhuga komi fram.

Candidate 4: Því má ekki nota docetaxel á meðgöngu nema að greinilega viðtak til þess sé fram.

Candidate 5: Því verður að ekki nota dócetaxel á meðgöngu nema ávallt talið sé um það.

Candidate 6: Því má engin tíðnir af doketaxeli haft á meðgöngu nema fram á sé greinilega þörf.

Candidate 7: Því má ekki nota dócetaxel á meðgöngu nema skýrt séð til bæði um notkun.

</details>

<details><summary>development_review #2 · A · greedy · general · F</summary>

Source ID: p13official21:dev:opensubtitles:1169

English: They're pretty as can be, aren't they?

Reference (shown after audit): Fallegri er ekki hægt að vera, ekki satt?

Review: Pretty/beautiful changed to good.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þeir eru mjög góðar, ekki satt?

</details>

<details><summary>development_review #3 · t2000188 · greedy · technical_short · P</summary>

Source ID: p13official21:dev:eso:446

English: “Astronomers have waited for data like this for over a decade.

Reference (shown after audit): „Stjörnufræðingar hafa beðið eftir gögnum eins og þessum í yfir áratug.

Review: Astronomers waiting for such data for over ten years retained; inflection errors.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: „Stjörnufræðingar höfðu bíðið um þessar gögn í meira en tíu ár.

</details>

<details><summary>development_review #4 · A · G8 · technical_medium · F</summary>

Source ID: p13official21:dev:eea:698

English: Only days that can be worked should be included when Saturdays and Sundays are not worked they should not be included, the same with public holidays).

Reference (shown after audit): Eingöngu skal telja með þá daga sem unnt er að vinna (ef ekki er unnið á laugardögum og sunnudögum skal ekki telja þá með; hið sama gildir um lögboðna frídaga).

Review: No candidate correctly preserves weekend/holiday inclusion rules.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Bara dagar, sem unnt er að vinnast, skulu tekið í bil, ef engin veikir á Sástóðum og Döggnum skulu þá ekki tekið í bil, sama fyrir almenningardagaleið.

Candidate 1: Einungis dagir sem má vinna skulu tekið í tæki þegar sólarhöfundur og sunnudagir eru ekki vinnameðstofir, eins og á algrei almenni helgum).

Candidate 2: Klárast að einungis dagsetninga sem má vinnu skal. Dagsetningar eigi að gerast um stundum en staðar og sundagar sem hægt er að vinnu. Sama við lausnaldagana).

Candidate 3: Einnig að eiginlegum fyrirmætti skulu fá til að taka til þeirra daganna þegar veikningar eru ekki gjört á sómrorna og óverkum, samt að eiginlegum fyrirmætti skulu fá til að taka til þeirra daganna þegar óverk eru ekki gjört á stundum.

Candidate 4: Þegar á Sármás og Sunnudagi ekki er einmiki skal ekki taka daganna við. Sama við opinberar helgarmögnun.

Candidate 5: Eina skal túr að setja dagar sem geta verið lausr, og ekki dagar sem eru ekki verið laús þegar á sæðisverðir og súður eru ekki verið, svo er að sameiginlega tímabil.

Candidate 6: Bara dagsetningar sem eru hæfilegir skal taka við þegar eftirheyrslan á Sástur og Sunnudagana er ekki hæfileg og sama við allt launarverk).

Candidate 7: Þegar sundagur og sólarríki eru óvinnar skulu einungis dagarnir sem má vinnast í tölustarf sem komið.

</details>

<details><summary>development_review #5 · t1001129 · G8 · technical_short · P</summary>

Source ID: p13official21:dev:eea:922

English: Development of CPE is checked as described in Part I.III.4.

Reference (shown after audit): Fylgst er með því hvort frumuskemmdir verða eins og lýst er í I.III.4.

Review: Candidate1 retains checking CPE development and ordered Part I/III/4 reference.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [1]

Candidate 0: Rannsókn á þróun CPE er gerð samkvæmt sem lýst er í IV.4. þátttöku I. hluta.

Candidate 1: Rannsókn á þróun CPE er gerð samkvæmt grein 4 í III. skilbibla I.

Candidate 2: Frekari útreikning CPE er skoðað eins og lýst er í IV.4. hópi I. hafa.

Candidate 3: Framdæling CPE er endurskoðað sem lýst er í kafla I.III.4.

Candidate 4: Framdæming CPE er athugað samkvæmt leiðbeiningum í þeim kafla í I. III. 4.

Candidate 5: Meðferði á CPE er samanburður með það sem lýst er í IV.4 í I. III. hærðinu.

Candidate 6: Sjáskiljanleika CPE er endurhöfund á samræmi við grein, sem er gerð á I. III. 4.

Candidate 7: Rannsókn eru gerðar á þróun CPE samkvæmt þeirri sem lýst er í 4. þátt I. III. 4.

</details>

<details><summary>development_review #6 · t2000188 · G8 · technical_long · U</summary>

Source ID: p13official21:dev:eso:765

English: “If it keeps spinning rapidly it might end its life in one of the most energetic explosions in the Universe, known as a long-duration gamma-ray burst,” says the lead scientist of the project, Hugues Sana, of the University of Leuven in Belgium.

Reference (shown after audit): „Haldi hún áfram að snúast mjög hratt gæti hún endað ævina sem langur gammablossi, ein orkumesta sprenging í alheiminum,“ segir Hugues Sana við Leuvenháskóla í Belgíu sem hafði umsjón með rannsókninni.

Review: Some explosion/spinning content recognizable but gamma-burst/university terminology not certifiable.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: „Ef hún helst snúast hratt getur hún endið lífi sínu í meiri kröftungu viðjarvaka, kallað mér lengd-virkjasetningu,“ segir hefðbundinn vísindamálið um verkefnið, Hugues Sana, hjá Leuven universíti í Belgíu.

Candidate 1: „Ef það snurst hratt kann það að enda lífi sínum í einum af sterkustu sprengingu í alheiminum, þegar þau kallast langtíma gamma-ormurka,“ sagði Hugues Sana, leiðræðandi stjörnufræðingur á verkefninu við stofnuninu í Leuven í Belgíu.

Candidate 2: „Ef hann helst hreyfja áfram hratt er það tengd að enda lífi sínu í einum af háþrengistækkustyklurnar í alheiminu, sem er kallað langvinnur gamma-rampi,“ sagði Hugues Sana, aðalhæfileikarfæri verkefnisins, í Leuven universitý í Belgíu.

Candidate 3: „Ef það stokkar hraðlega er það kannst það enda lífi sínu eftir einhverjum langlegri gama- röðun í alheiminu, sem kallast langvirkur gama- röðun,“ sagði Hugues Sana, aðalhöfundur verkefnisins við stofnun Leuven í Belgíu.

Candidate 4: „Ef það hreyfir hratt jöfnu kann það að enda lífi sínu í einum af öflugustu sprengingunum í alheiminu, sem kallast langtíma gama-rasaburst,“ segir leiðandi vísindamaðurinn á verkefninu, Hugues Sana, frá Leuven hæfileikaskóla í Belgíu.

Candidate 5: „Ef það hækkar áfram í hraðri vetrarviki verður það lífið endurt á einhverju langvinsræktu gamma-blásturinn sem hefur náin heiti,“ sagði Hugues Sana, aðalaði verkefnisins, frá Leuven universítí sinu í Belgíu.

Candidate 6: „Ef það holdir áfram að snúa hröðt getur það endað lífi sínu í einum af öflugustu sprengingu víxurinnar, þekktur sem langtíma γ-losi,“ segir Hugues Sana, leiðtogur verkefnisins, umfræðingur í Leuven-universitetsi í Belgíu.

Candidate 7: „Ef það eyðir áfram um vél gæti fyrir það lokið líf sínu á einhverju styrklegustu sprengingu alheimisins, þekktu sem langvarandi gammagrepsstyrkur,“ sagði Hugues Sana, aðalhöfundur verkefnisins við stofnuninni í Leuven í Belgíu.

</details>

<details><summary>development_review #7 · A · G8 · technical_short · F</summary>

Source ID: p13official21:dev:eea:609

English: Special payments for shift work.

Reference (shown after audit): Sérstakar greiðslur vegna vaktavinnu.

Review: No candidate faithfully renders shift-work special payments.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Sérfræðilegar greiðslur fyrir skiptarvinnslur.

Candidate 1: Áætlanlega greiðslur fyrir stefnun.

Candidate 2: Tiltekna greiðslur fyrir skiptamarkað.

Candidate 3: Sérlegum borgum vegna skipti í vinnunni.

Candidate 4: Sérstakt brott fyrir skiptaskrúð.

Candidate 5: Sérstæðu greiðslur fyrir skrána.

Candidate 6: Sérstakar borgningar fyrir skrúðvinn.

Candidate 7: Sérþekjur eftir störfahaf.

</details>

<details><summary>development_review #8 · A · greedy · general · F</summary>

Source ID: p13official21:dev:opensubtitles:2508

English: Rose, we have a guest in the living room.

Reference (shown after audit): Rósa, það er gestur í stofunni.

Review: Guest replaced by gift and living-room specificity lost.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Rose, við höfum gjöf í herberginu.

</details>

<details><summary>development_review #9 · t1001129 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eea:574

English: All rear-window, roof-panel and partition switches intended for use by occupants in the rear of the vehicle shall be capable of being switched off by a driver-controlled switch which is located forward of a vertical transverse plane passing through the R points of the front seats.

Reference (shown after audit): Allir rofar í hliðarrúðum að aftan, þaklúgum og skilrúmum sem farþegum baka til í ökutækinu er ætlað að nota skulu gerðir með þeim hætti að unnt sé að rjúfa straum til þeirra með rofa sem ökumaður stjórnar og er staðsettur framan við lóðrétt þverplan sem gengur í gegnum R-punkta framsætanna.

Review: All candidates lose key switches,driver-control and geometric-position requirements.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Allar bakglas, skuggavallir og breytingar á spillingarmálum sem ætlaðir eru fyrir notendur á bakstöðvum ökutækisins skulu hafa það mun kann að slökkva af skjallum sem eru lykil handa ökumaður og er í færi við hlið þess sem sagð er þegar R-stöður fyrstu sæta frá enda.

Candidate 1: Allir opinbreykur, skjaldreifir og miðlægur sértöldir sem eru ætlaðir fyrir notendur í eftirrás ökutækisins skal gæta að slíkrar séstölu kunna að slökkva með rannsóknarmunum þeim, sem er í eftirhlið, sem eru áfram frá hendilagnum sem fer á fyrirmerki fyrstu sætranna.

Candidate 2: Allir baka-gluggi, tegundarglöð og rammasölur sem ætlunin er að nota sjúklingum að endanum af ökutækinu skal getað vera faststöðugum hætti sem virka veitur við að slökkva, sem er stjórnvaldið á meðalfram við lykilhlið sem fer eftir R-stöðum á búsetu.

Candidate 3: Allar höðvitraðir, skjólskapar og hlífðarhlaður á endastjörnunum, sem ætlaðir eru til notkunar aðilanna á endustöðum ökutækisins, skulu vera hæfilegir til að slökkva á með ökusrannsóknartilvægi sem er gerð af umsjónaráðstefnun, sem er staðsett fyrir framhlið á hæðsskálu sem fer úr þeim þegar sem R á stöðum framan í öskjuna.

Candidate 4: Hverja bakglugg, þjóðþekkja og hlífðarrúmmál sem ætlað eru fyrir notendum að hreinast í bakrásinu vagns skal hægt að slökkva við að skrifa af byrjun framfangssemfístar sem er í borð með hreyfanlegu leitarmiði sem fer gegn fárgjafar í framhanda.

Candidate 5: Allar bakið gluggi, teglu- og skiptir húð á öxlana svo að notendum í hinni aðalstan skal bein að slökkva með dráttum kællu sem er í færi við aðalsetur sem fer á sér sá plan sem fer að rist á R-punkti á fyrri sætinu.

Candidate 6: Allir bakglas, ökki- og þurringssteiðir sem ætluð eru fyrir notendum þegar í bak hlíf til eftirstöðu vélins skulu vera hæra á að skiptast niður við hæfilegri, eftirdirgeirri sem kemur fram í viðgangarveg sem fer úr R-stigum fyrirhærs setts skulu.

Candidate 7: Öll bakgluggasvirkjarnir, húðplana og andstruðaklósar fyrir búsetu í bakrásum ökumanns, sem venjulega eru notuð, skulu geta verið flýttarð á upphafi borðsins sem er stjórnvona bóta og er á borð í borðhliðstrið.

</details>

<details><summary>development_review #10 · t2000188 · greedy · technical_short · F</summary>

Source ID: p13official21:dev:eea:1991

English: Paragraph AG27 is amended and after paragraph AG29, paragraph AG29A is added.

Reference (shown after audit): Ákvæðum liðar AG27 er breytt og á eftir lið AG29 er lið AG29A bætt við.

Review: Legal AG identifiers AG27/AG29/AG29A lose AG prefix.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Í 27. lið er breytt og eftir 29. lið bætist við 29. liður A.

</details>

<details><summary>development_review #11 · t1001129 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eso:726

English: They wanted to study the interaction between a young generation of stars and the cold clumps that were assembling into these first galaxies.

Reference (shown after audit): Stjörnufræðingarnir vildu rannsaka víxlverkunina milli ungrar kynslóðar stjarna og köldu kekkjanna sem voru að safnast saman í þessum fyrstu vetrarbrautum.

Review: Cold clumps become pressures; assembly relation garbled.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þau vildi rannsaka milliverkanir milli unga stjarnaframsins og kaltu þrýstingum sem var að samhliða í þessum fyrstu vetrarbrautum.

</details>

<details><summary>development_review #12 · t1001129 · G8 · technical_medium · F</summary>

Source ID: p13official21:dev:ema:1406

English: Concomitant use with yellow fever vaccine and with live virus and bacterial vaccines (see section 4.5).

Reference (shown after audit): Samhliða notkun með bóluefni gegn gulusótt og bóluefni með lifandi veirum og bakteríum (sjá kafla 4.5).

Review: Yellow-fever/live-virus/bacterial vaccine requirements not faithfully retained.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Rannsókn með geislameðferð með gallarfríuhörnu og með geislameðferð með lifandi veirum og sveppum (sjá kafla 4.5).

Candidate 1: Samhliða notkun með geislaviruhvítavirkjum og með lifandi virki og bakteriavirkjum (sjá kafla 4.5).

Candidate 2: Eftirlipt notkun samhliða barnaofnæmisbóluefni og lifandi veirubóluefni og bakteríubóluefni (sjá kafla 4.5).

Candidate 3: Eftirlifandi notkun með fínni fæðingarbólgubóluefni og með lifandi veira og bakteríum bóluefni (sjá kafla 4.5).

Candidate 4: Samhliða notkun á aðeins heilbrigðisbóluefni gegn gulvirkurum (gripasjónamjólkur) og lifandi veirum og bakteríum (sjúkdómstofnun 4.5).

Candidate 5: Samhliða notkun millivefja gegn oranýr og lifandi veirum og bakteríum (sjá kafla 4.5).

Candidate 6: Eingöngu samhliða notkun ára og alvarlegu gleri bóluefna og lifandi veiruaðferðar og myndandi bóluefni (sjá kafla 4.5).

Candidate 7: Notkun samhliða smitsýki gegn gultsýki og lifandi vira- og bakteríuvíssi (sjá kafla 4.5).

</details>

<details><summary>development_review #13 · A · G8 · technical_medium · F</summary>

Source ID: p13official21:dev:ema:1718

English: Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.

Reference (shown after audit): Gjöf edoxabans samtímis P-gp virkjanum rífampisíni leiddi til lækkunar á meðalgildi AUC fyrir edoxaban og styttri helmingunartíma, með hugsanlegri minnkun á lyfhrifum þess.

Review: No candidate preserves half-life and pharmacodynamic effects correctly.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Samhliða nota edoxabans og P-gp aukandi rifampicins leiddi til minnkaðar miðgildi edoxabans AUC og minnkaðu hálfdýlingar, með tilhlýðilegum minnkunum á lyfiþróaáhrifum.

Candidate 1: Samhliða nota edoxaban og P-gp aukandi rifampicins leiðaði til minnkunar á meðallit eða AUC og smáðrar tíðni eða mögulega minnkunar á líftryggingarverkanir eða lyfjahvörf.

Candidate 2: Samhliða nota edoxabans og P-gp aukandi rifampicin færðir minnka meðittölu edoxabans og það hratt tíðni, svo um getur að minnka lyfjahvörfum af lyfjum.

Candidate 3: Samhliða lyfjagjöf edoxaban með rifampicin, lyf sem valdi P-gp, var aukin meðal eðli edoxabans og skammtar skammtímis edoxabans, með hugsanlegum aukunum á lífshækkunar á því.

Candidate 4: Samhliða notkun edoxaban og rifampícins sem P-gp aukið er hefur leitt til þess að meðalgildi AUC edoxaban minni og haldað framlengingar tíðnið, með væntumminnri minnkaðum lyfjahvörfum.

Candidate 5: Samhliða nota edoxaban og P-gp ávallskunningsmál, rifampicin, leiddi til minnkaðar meðallit hvarfseðisekningu edoxabans og skammtar á hálfbreidd, með hættuleika á því að geinar verði rýmdir við lyfjahvörf efna.

Candidate 6: Samhliða nota edoxaban með P-gp aukandi rifampicin hefur leitt til minnkaðar meðalgildi edoxaban AUC og skerta sæfisíðu, með hættuleg ráðstafanir á minnkaðar lyfjahvörfi.

Candidate 7: Samhliða lyfjagjöf af edoxabandi og rifampicini, sem er P-gp aukið, voru liður hjá meðal því að meðaltal edoxabandi-AUC (Area Under the Curve) minnkist og hlutfallsstundin breytist, með hættuleika á aukin lyfjameðhöndlunarhrifum.

</details>

<details><summary>development_review #14 · t1001129 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eso:1051

English: The technique used by Teague, which derived averaged variations in the flow of the gas as small as a few percent, revealed the impact of multiple planets on the gas motions nearer to the star.

Reference (shown after audit): Tæknin sem Teague beitti sýndi meðalbreytingarnar á gasflæðinu niður í nokkur prósent og leiddi í ljós áhrif nokkurra plánetna á hreyfingu gassins nær stjörnunni.

Review: Averaged few-percent flow variations are not coherently preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Aðferðin sem Teague notaði, sem fannst með það að meðalhöfundar breytingum á fljóttum gassfljóti sem var stutt eftir nokkra prozentum, benda til áhrifanna fjölda reikistjarna á fljóttum gassfljóti í nærri stjörnunni.

</details>

<details><summary>development_review #15 · t1001129 · greedy · technical_short · F</summary>

Source ID: p13official21:dev:ema:704

English: The most frequently reported adverse reaction was acne, which was generally mild.

Reference (shown after audit): Algengasta aukaverkunin sem greint var frá er þrymlabólur (acne), sem voru venjulega vægar.

Review: Acne mistranslated as cow disease.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Algengasta aukaverkunin sem greint var frá var kúasýki sem var almennt væg.

</details>

<details><summary>development_review #16 · t2000188 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eea:1194

English: It should provide the Commission and the Member States with objective, reliable and comparable information and data on maritime safety and on ship pollution prevention to enable them to take any necessary initiatives to enhance the measures in place and to evaluate their effectiveness.

Reference (shown after audit): Henni ber að sjá framkvæmdastjórninni og aðildarríkjunum fyrir hlutlægum, áreiðanlegum og sambærilegum upplýsingum og gögnum um siglingaöryggi og varnir gegn mengun frá skipum til að gera þeim kleift að vinna hvers kyns nauðsynleg framtaksverkefni til að efla þær ráðstafanir sem gerðar hafa verið og að meta skilvirkni þeirra.

Review: Ship pollution prevention becomes an unrelated inflammation expression.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Hún skal veita framkvæmdastjórninni og aðildarríkjunum réttar, áreiðanlegar og samanburðarhæfar upplýsingar og gögn um öryggi sjómála og um aðferðir til að koma í veg fyrir útrennslisbólgu í skipum til þess að þau geti tekið nauðsynlegar aðgerðir til að auka ráðstafanir sem eru í gildi og meti áframhaldsnæmi þeirra.

</details>

<details><summary>development_review #17 · A · G8 · technical_medium · U</summary>

Source ID: p13official21:dev:eea:1585

English: The Commission shall submit a final evaluation report at the end of the Programme.

Reference (shown after audit): Framkvæmdastjórnin skal leggja fram endanlega matskýrslu við lok áætlunarinnar.

Review: Closest candidate4 is an audit/review report, without clear final evaluation qualification.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Framkvæmdastjórnin skal leggja fram endurskoðunaraðlag eftir hliðar áætlunarinni.

Candidate 1: Framkvæmdastjórnin skal leggja fram síðasta matið á lok viðbætisins.

Candidate 2: Framkvæmdastjórnin skal leggja fram endurskoðunaraðskrift að lok meðferðarstefnu.

Candidate 3: Framkvæmdastjórnin skal leggja fram endurskýringu um framkvæmd á lok hálfar af áætluninni.

Candidate 4: Framkvæmdastjórnin skal leggja fram endurskoðunarskýrslu við lok áætlunarinnar.

Candidate 5: Framkvæmdastjórnin skal leggja fram endalausan matsskil á lok viðrarfarannsóknarinnar.

Candidate 6: Framkvæmdastjórnin skal leggja fram endurskoðunarskýrslu innan þeirrar loku sem á að stafa á áætluninni.

Candidate 7: Framkvæmdastjórnin skal leggja fram endurskoðunarkröfuna á lok samstarfsins.

</details>

<details><summary>development_review #18 · t1001129 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eea:1716

English: The competent authorities of Gabon have reacted promptly to these concerns, indicating their commitment to take all measures necessary to implement applicable ICAO standards and enforce compliance with these standards as soon as possible.

Reference (shown after audit): Lögbær yfirvöld í Gabon brugðust tafarlaust við þessum áhyggjum og létu í ljós eindreginn vilja til að gera allar nauðsynlegar ráðstafanir til að koma í framkvæmd gildandi stöðlum Alþjóðaflugmálastofnunarinnar og tryggja að farið yrði að ákvæðum þeirra eins fljótt og auðið er.

Review: Aviation competent authorities changed to drug-safety agencies.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Lyfjaöryggisstofnanir í Gabón hafa svarað þessum ábendingum tafarlaust og benda til þess að gera allar nauðsynlegar ráðstafanir til að framfylgja viðeigandi staðlum ICAO og fylgjast með þeim við eftir það sem best er.

</details>

<details><summary>development_review #19 · t1001129 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eea:1552

English: The analytical result shall be reported as x +/– U whereby x is the analytical result and U is the expanded measurement uncertainty, using a coverage factor of 2 which gives a level of confidence of approximately 95 % (U = 2u).

Reference (shown after audit): Greina skal frá niðurstöðum úr greiningunum sem x +/– U þar sem x er niðurstaða greiningarinnar og U er útvíkkaða mælióvissan með þekjustuðlinum 2 sem gefur 95% öryggisstig (U = 2u).

Review: Expanded measurement uncertainty and coverage-factor concepts mistranslated.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Greina skal niðurstöður greiningar sem x +/– U þar sem x er niðurstöður greiningar og U er útsetningu á mælingum, með því að nota 2 fyrir samkeppnishönnun, sem gefur umtalsbótartryggingu um um 95% (U = 2u).

</details>

<details><summary>development_review #20 · A · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:ema:1765

English: Take this leaflet or some tablets with you so that your doctor knows exactly what you have taken.

Reference (shown after audit): Hafa skal þennan fylgiseðil eða eitthvað af töflum meðferðis svo læknirinn viti nákvæmlega hvað tekið hefur verið.

Review: Leaflet and doctor knowing exactly are replaced by unrelated expressions.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Taktu þessu leifa eða töflur með þér svo að læknirinn veitir allt áhuga af því hvað þú hefur tekið.

</details>

<details><summary>development_review #21 · t2000188 · G8 · technical_short · P</summary>

Source ID: p13official21:dev:eea:922

English: Development of CPE is checked as described in Part I.III.4.

Reference (shown after audit): Fylgst er með því hvort frumuskemmdir verða eins og lýst er í I.III.4.

Review: Candidate6 faithfully states CPE development is checked as described in I.III.4.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [6]

Candidate 0: Ekki er gerð annaðhvort varðandi þróun CPE sem lýst er í lið II.4 í hluta I.

Candidate 1: Rannsókn á þróun CPE er gerð samkvæmt grein 4 í III. hliðssniði I. hliðssniðar.

Candidate 2: Frekari öryggi CPE er metað eins og lýst er í I. III.4.

Candidate 3: Framdæling CPE er endurskoðað sem lýst er í III.4. hjálfaskil I. þátttöflu.

Candidate 4: Framdæming CPE er rannsakað eins og lýst er í III.4. hluta I. hliðs.

Candidate 5: Skoðun varðar þróun á CPE eftir því sem lýst er í I.ÍII.4.

Candidate 6: Skoðað er þróun CPE eins og fram kemur í kafla I.III.4.

Candidate 7: Verið er að kanna þróun CPE eins og lýst er í I.III.4 hluta.

</details>

<details><summary>development_review #22 · t1001129 · greedy · general · U</summary>

Source ID: p13official21:dev:opensubtitles:1012

English: I'll do whatever you ask.

Reference (shown after audit): Ég geri hvað sem þið viljið.

Review: Ask/wait verb form is ambiguous; cannot certify intended request.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ég geri hvað sem þú beið.

</details>

<details><summary>development_review #23 · t2000188 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eso:206

English: The survey was sensitive to planets between 75 million kilometres and 1.5 billion kilometres from their stars (in the Solar System this range would include all the planets from Venus to Saturn) and with masses ranging from five times the Earth up to ten times Jupiter.

Reference (shown after audit): Mælingarnar voru næmar fyrir reikistjörnum sem eru milli 75 milljón til 1,5 milljarða km frá móðurstjörnunum (í sólkerfinu okkar inniheldur þetta fjarlægðarbil allar reikistjörnur frá Venusi til Satúrnusar) og frá fimm sinnum massameiri en jörðin upp í tíu sinnum massameiri en Júpíter.

Review: All candidates change1.5billion distance or other material ranges.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Skoðunin var snað fyrir plöntur sem eru á milli 75 milljón km og 1,5 milljón km frá stjörnunum (í sólarssjónaukinni gæti það náð allar plönturnar frá Venus til Saturn) og massafjölda voru á milli fimm sinnum Jörðstjarna og tíu sinnum Júpítra.

Candidate 1: Skoðanirnar voru áhæfar að skipta við reikistjörnu í 75 milljón km og 1,5 milljón milljarða frá stjörnunum (á sólkerfinu voru svæðið fyrir allar reikistjörnurnar frá Venus til Satar) og massafjölda rannsóknarvarnar á milli fimm af jörð og tíu af Júpíter.

Candidate 2: Skoðunin var næm til reikistjörnu í milli 75 milljón km og 1,5 milljón milljón km frá stjörnunum (á sólkerfinu burðast allar reikistjörnurnar frá Venus til Saturns) og þar með tímabili massa frá fimm sinnum Heimurinni upp í tíu sinnum Júpítu.

Candidate 3: Til greiningar var næm við reikistjörnur á milli 75 milljón km og 1,5 milljón milljón km frá stjörnunum (í sólkerfinu catchesum allar reikistjörnurnar frá Venus til Saturn) og á massafjölda á milli fimm sinnum Jörðar til tíu sinnum Júpítu.

Candidate 4: Rannsóknin var næm við reikistjörnurnar á milli 75 milljón km og 1,5 milljón km frá stjörnunum (hér á sólarssjóarnafinu eru takmörkuð öll reikistjörnur frá Venus til Sáters) og miðað við massafjölda sem var allt fyrir fimm sinnum jörðinni og allt fyrir tíu sinnum Júpíturni.

Candidate 5: Skoðanirnar höfðu nákvæm áhrif á reikistjörnu á milli 75 milljón km og 1,5 milljón milljón km frá sólinum og á massakvota á milli fimm og títilli Júpítrs.

Candidate 6: Rannsóknin var nægileg á bænum á milli 75 milljón km og 1,5 milljón km frá stjörnunum (síðar í Jörðaheimsins næst allar bænum frá Venus til Svelli) og massakvörðan var á milli fimm sinnum þess og tíu sinnum Júpíturnar.

Candidate 7: Rannsóknin var næm við körlun á milli 75 milljón km og 1,5 milljón milljón km frá stjörnum (í sólkerfinu þynnu allar körlunum frá Vensu til Sæturs) og massamæli á milli fimm tals jörðar og tíu þings Júpíters.

</details>

<details><summary>development_review #24 · t2000188 · greedy · technical_short · U</summary>

Source ID: p13official21:dev:eso:768

English: Both components are classed as O-type stars.

Reference (shown after audit): Báðar stjörnurnar eru af O-gerð.

Review: Both components/O-type stars are recognizable but malformed lexical forms leave fidelity uncertain.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Bæði innihaldsefnið er flokkt sem O-sterrar.

</details>

<details><summary>development_review #25 · t1001129 · greedy · general · P</summary>

Source ID: p13official21:dev:opensubtitles:3209

English: Because it's not safe there.

Reference (shown after audit): Af því að það er ekki öruggt.

Review: Unsafe location retained with awkward grammar.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Það er ekki örugg í því.

</details>

<details><summary>development_review #26 · t1001129 · greedy · technical_short · F</summary>

Source ID: p13official21:dev:eso:491

English: ALMA can observe in different frequency bands.

Reference (shown after audit): ALMA getur gert mælingar á mismunandi böndum.

Review: Different frequency bands omitted and replaced by unrelated content.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: ALMA getur fylgst með breytum á öllum frekari bænum.

</details>

<details><summary>development_review #27 · t2000188 · G8 · technical_medium · P</summary>

Source ID: p13official21:dev:eea:85

English: For the estimation of these concentrations all relevant information on the plant protection product and on the active substance must be taken into account.

Reference (shown after audit): Við mat á framangreindum styrk ber að taka allar viðeigandi upplýsingar um plöntuvarnarefnið og virka efnið til greina.

Review: Candidate0 retains concentration estimate and all relevant plant-protection/active-substance information.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [0]

Candidate 0: Til að meta þessar styrk verður að taka tillit til allrar viðeigandi upplýsinga um plöntuverndarefnið og virka efninu.

Candidate 1: Við mat á þessum styrkleikum ber að taka tillit til allrar viðeigandi upplýsinga um plöntuverndarefnið og virka efninu.

Candidate 2: Til að meta þessar innihaldsrúmmál verður að taka tillit til allra viðeigandi upplýsinga um væntvörnarefni og virka efnið.

Candidate 3: Við mat á þessum styrkleikum verður að taka tillit til allra viðeigandi upplýsinga um plöntuverndarvörn og virka efnið.

Candidate 4: Við mat á þessum styrkleikafjölda ætti að taka tillit til allrar viðeigandi upplýsinga um plöntuvarnarefnið og virka efnið.

Candidate 5: Við mat á þessum styrkleikum skal taka tillit til allra viðeigandi upplýsinga um plöntuverndarvörn og virka efnið.

Candidate 6: Við áætlanir á þessum styrkleikafjölda verður að taka allar viðkomandi upplýsingar um plöntuverndarlyfið og virka efninu í tillit.

Candidate 7: Við mat á þessum styrk skulu taka til athygli allra viðeigandi upplýsinga um plöntuverndarlyf og virka efnið.

</details>

<details><summary>development_review #28 · A · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eso:464

English: With an estimated mass of four to five times that of Jupiter, it would be the least massive planet to be directly observed outside the Solar System.

Reference (shown after audit): Massi fyrirbærisins er talinn milli fjórum til fimm sinnum meiri en massi Júpíters, svo hér gæti verið um að ræða massaminnstu reikistjörnu sem ljósmynduð hefur verið fyrir utan sólkerfið okkar.

Review: Least massive directly observed extrasolar planet proposition garbled.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Því er það minnst massaður heimil í almenningu, sem hægt er að sékja áfram út frá Solssjóðnum, með því að það er fjögur til fimm sinnum massa Júpíturs.

</details>

<details><summary>development_review #29 · t1001129 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eea:1216

English: That task shall be coordinated with the existing regional cooperation programmes and shall include, where appropriate, the organisation of relevant training activities.

Reference (shown after audit): Samræma skal það verkefni svæðisbundnum samstarfsáætlunum sem eru fyrir hendi og skal það fela í sér, eftir því sem við á, skipulag viðeigandi þjálfunar.

Review: Cooperation programmes and organisation of training not faithfully retained.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það verkefni skal samræma við tilstaðar rannsóknaráætlunum um sameiginlega starfi á svæðum og skulu þau, eftir því sem við á, vera að því er varðar að hafa fengið nauðsynlega þjálfunarskyldur.

</details>

<details><summary>development_review #30 · t2000188 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eea:281

English: The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.

Reference (shown after audit): Fjárhæð þeirra fyrrnefndu (síðarnefndu) sem eru jafnaðar á móti þeim síðarnefndu (fyrrnefndu) í tilteknum binditímaflokki skal teljast jafnaðar stöður þess flokks en eftirstöðvar langra eða stuttra staðna telst ójöfnuð staða þess flokks.

Review: No candidate preserves financial maturity-band and matched/unmatched relations.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Skömmtun á því í beifaðum (endanlega) sem níðast í (meðan það er níðst) í tilteknum þroskaseglum skal vera samrýmist staðstæður í þeim glöggum, þrátt fyrir því að niðurfallur langa eða stöllu staðstæður skal vera ósamrýmist staðstæður í sömu glöggum.

Candidate 1: Hlutfall upplandaðra (upplandaðra) sem stunda í lögðu hliðstæða (hliðstæða) eigiðu saman við hliðstæða í sínu hliðstæðuhópi skal vera samansamkeppna staðstöður í þessu hliðstæðuhópi, þar eftir lausir stunda að skammtinu eða stunda að skammtinu skal vera ósamansamkeppnum staðstöður í sama hliðstæðuhópi.

Candidate 2: Íkoma fyrir (lagar) sem sambærilegt kleift er við síðar (fyrri) skal vera sambærileg staðstöður í því vikulstyrkarmót sem náðirist, að því er varðar stöðuðu stöðu, og ósamþykktur langt eða skortar staðstöður um það sama vikulstyrkarmót.

Candidate 3: Magnur fyrri (sá eða síðari) sem samhæfir svörunin sjálfur (fyrri eða síðari) á tiltekinni þegari styrkusviki skal vera samhæfðir staðarlíkurnar í þeirri styrkusviki en þeirur staðarlíkurnar eftir það skal vera samhæfðir staðarlíkurnar í þeirri styrkusviki.

Candidate 4: Magn miðlaðrar (næmstriðar) aðilanna, sem samræma vera (næmstriða) miðlaðrar aðilanna í staðnar (endurtekinnar) styrk, skal vera samræmdar staðurinn í þeirri styrk, en miðlaður styrk er ekki samræmdur styrk ef það er styrk með litið (lengur) styrk.

Candidate 5: Fjöldi fráfyrri (sá fyrsti) sem samþykktur verður af fyrsti (fráfyrri) í ákveðnu nafnumælisríki skal vera samþykktar stöðurnar í þessum ríki, þar sem eftirfarandi stöð varður ekki samþykkt.

Candidate 6: Framvinsta (sákasta) skammtur, sem samaríðast við síðanefnda (fyrriefnda), á við ákveðinn viðmiðunarbrennslisbrun, skal vera samaríðstöðvar í þeirri brún, en eftirfyrir langa eða stánar stöður skal vera ósamaríðstöður í sama brún.

Candidate 7: Aka skammtinum af fyrri (sáskemmtast) sem síðastirna (fyrsta) samsvarar, skammstöðvar, skammstöðvar skammtinum í tilteknum fullorðnum, þar sem henni stofnast aukinni (lengri) eða stofnandi (svæði) skammta.

</details>

<details><summary>development_review #31 · A · greedy · technical_long · F</summary>

Source ID: p13official21:dev:ema:325

English: If you get lower abdominal pain, gain any weight rapidly, feel sick or are vomiting or if you have difficulty in breathing, talk to your doctor straight away who might ask you to stop using this medicine (see in section 4 under “Serious side effects”).

Reference (shown after audit): Ef þú færð verk í neðri hluta kviðar, þyngist hratt, finnur fyrir ógleði eða kastar upp eða ef þú átt erfitt með að anda, skaltu hafa tafarlaust samband við lækninn sem gæti beðið þig að hætta að nota lyfið (sjá 4. kafla „Alvarlegar aukaverkanir“).

Review: Key symptoms including rapid weight gain and breathing difficulty garbled.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef þú færð smári kviðbólgu, fært þyngd eða þú færð illkynningu, er þér skjald eða þú hefur íhugaðtökum við andskotnilegri aukaverkunum skal þú tala til læknis áfram og hún getur spurnið um að þú stöðvir þessarar lyfja (sjá í kafla 4 undir „Alvarlegar aukaverkunir“).

</details>

<details><summary>development_review #32 · t2000188 · greedy · technical_medium · P</summary>

Source ID: p13official21:dev:ema:1765

English: Take this leaflet or some tablets with you so that your doctor knows exactly what you have taken.

Reference (shown after audit): Hafa skal þennan fylgiseðil eða eitthvað af töflum meðferðis svo læknirinn viti nákvæmlega hvað tekið hefur verið.

Review: Bring leaflet/tablets so doctor knows exactly what was taken retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Taktu þessi fylgiseðil eða töflur með þér svo að læknirinn veit allt nákvæmlega hvað þú hefur tekið.

</details>

<details><summary>development_review #33 · A · G8 · technical_short · F</summary>

Source ID: p13official21:dev:eso:491

English: ALMA can observe in different frequency bands.

Reference (shown after audit): ALMA getur gert mælingar á mismunandi böndum.

Review: No candidate preserves different frequency bands.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: ALMA getur athygliðað í mismunandi fjölda fjölda.

Candidate 1: ALMA getur fylgt í mismunandi frekarihópum.

Candidate 2: ALMA getur skýrslugjafar á mismununar framsöfn.

Candidate 3: ALMA getur gernir í mismunandi frekariðförum.

Candidate 4: ALMA hægt er að skoða sama á milli á mismunandi framskiptargreiningum.

Candidate 5: ALMA getur sett áhættuotkunnandi á milli í mismunandi loftþráttíma.

Candidate 6: ALMA gagni allt í mismunandi hreyfilingar.

Candidate 7: ALMA telur fyrir allt mörgum framsökum.

</details>

<details><summary>development_review #34 · t2000188 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eso:919

English: "Thanks to several giant telescopes currently under construction, including ESOs E-ELT and the NASA/ESA/CSA James Webb Space Telescope due to launch for 2018, we will soon be able to study the atmospheric composition of these planets and to explore them first for water, then for traces of biological activity.

Reference (shown after audit): „Þökk sé nokkrum risasjónaukum sem nú eru í smíðum, þeirra á meðal E-ELT sjónauka ESO og James Webb geimsjónauka NASA; ESA og CSA sem skotið verður á loft árið 2018, munum við fljótlega geta rannsakað efnasamsetningu lofthjúpa þessara reikistjarna og kannað þær fyrst í leit að vatni og síðan leitað að merkjum um líf.

Review: Atmospheric composition missing and agency acronyms corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: „Takinn við nokkrar stóra sjónauka sem eru í framhaldshús, þar á meðal ESOs E-ELT og James Webb geimsjónaukuna NASA/ESO/CSC, sem ætla að koma til reynd árið 2018, getum við náið nægilega í þessum reikistjörnur og rannsakað þær fyrst um vatn, síðan um eftirvirkni líffræðilegra.

</details>

<details><summary>development_review #35 · A · greedy · technical_short · F</summary>

Source ID: p13official21:dev:eso:768

English: Both components are classed as O-type stars.

Reference (shown after audit): Báðar stjörnurnar eru af O-gerð.

Review: Components replaced by waiting in town.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Bíða í bænum eru skilgreindar sem O-stjarna.

</details>

<details><summary>development_review #36 · t2000188 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eea:534

English: Council Directive 74/60/EEC of 17 December 1973 on the approximation of the laws of the Member States relating to the interior fittings of motor vehicles.

Reference (shown after audit): Tilskipun ráðsins 74/60/EBE frá 17. desember 1973 um samræmingu laga aðildarríkjanna varðandi innréttingar vélknúinna ökutækja.

Review: Vehicle interior fittings mistranslated as interior phenomena.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Tilskipun ráðsins 74/60/EBE frá 17. desember 1973 um samræmingu á lögum aðildarríkjanna varðandi innri fyrirbæri ökutækja.

</details>

<details><summary>development_review #37 · t1001129 · G8 · technical_medium · F</summary>

Source ID: p13official21:dev:ema:1718

English: Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.

Reference (shown after audit): Gjöf edoxabans samtímis P-gp virkjanum rífampisíni leiddi til lækkunar á meðalgildi AUC fyrir edoxaban og styttri helmingunartíma, með hugsanlegri minnkun á lyfhrifum þess.

Review: Candidates reverse half-life change or lose pharmacodynamic effect qualification.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Samhliða lyfjagjöf edoxaban og rifampicins, P-gp aukandi lyfja, hafði áhrif á lækkun á meðaltal AUC fyrir edoxaban og tilslæmt hækkun á helmingunartíma, með hættulegum lækkunum á lyfhrifum.

Candidate 1: Samhliðagjöf edoxaban og P-gp hvarfefnis rifampicins leiði til minnkaðs AUC eða meðalþroska edoxabans og skerta helmingardaðs, með hugsanlega lágskerðingu á lyfjahvörfum þess.

Candidate 2: Samhliða lyfjagjöf edoxabans og rifampicins, sem er P-gp aukandi lyf, færðu lækkun á meðal AUC (Area Under Curve) fyrir edoxaban og skorti á helmingunartíma, með hugsanlegt minnkaða áhrifum lyfsfæðunar á lyfjaheilkenni.

Candidate 3: Samhliða lyfjagjöf edoxaban með rifampicin, P-gp frystu, færði lækkun á meðal AUC fyrir edoxaban og skammtarmörkun, með hættu á aukinum virkni lyfjafrásamsvarandi áhrifa.

Candidate 4: Samhliða lyfjagjöf edoxabans og ifjumleysa (P-gp inducer) rifampicins færði lækkun á meðal AUC (area under the curve) sem fylgdi edoxaban og skort um hálfburtími, sem getur það valdið á fíknifum lyfjafræðilegra áhrifa þess.

Candidate 5: Samhliða lyfjagjöf edoxaban með rifampicini, lyfjahefandi geymslu P-gp, gaf minnkaðar meðal AUC gildi edoxaban og skammliðvirkni, sem geta verið minnkað þegar lyfin varðar lyfhrif.

Candidate 6: Samhliða lyfjagjöf edoxaban og rifampicins, P-gp-augandi lyfja, fór til lækkunar á meðal AUC fyrir edoxaban og skerðaðan helmingunartíma, með hættu á þessari áhrifum.

Candidate 7: Samhliða lyfjagjöf edoxaban og P-gp örvunarhvarfasýnarefna rifampicins vann viðlægð þess að meðalhverfis AUC fyrir edoxaban minnkaði og að hálfbilinn þroskaði, með possibility af að lækkast lyfjahvörfum.

</details>

<details><summary>development_review #38 · t1001129 · G8 · technical_short · F</summary>

Source ID: p13official21:dev:eso:302

English: This is because the tilt of the orbit is normally unknown.

Reference (shown after audit): Þetta er vegna þess að venjulega er brautarhallinn óþekktur.

Review: Orbital tilt normally unknown not correctly expressed.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Það er vegna þess að það er óþekkt hvar flogurinn snúist.

Candidate 1: Þetta er vegna þess að hringin í yfirborði er að eiginleikum óþekkt.

Candidate 2: Það er vegna þess að bláæð sviðsauka er eiginlega óþekkt.

Candidate 3: Þetta er vegna þess að þjóðgerð ramma fyrir að vera óþekkt.

Candidate 4: Það er vegna þess að hálfan aroundsins er aðallega óþekkt.

Candidate 5: Þetta kemur fyrir vegna þess að umferðarfljótan reyndar ekki þekkt.

Candidate 6: Þetta er vegna þess að fylgisskráningur í reikistillinu er að staðsetningu þess okkur óþekkt.

Candidate 7: Þetta er vegna þess að um yfirborðið er ekki þekkt það sem hliður umferðarins er.

</details>

<details><summary>development_review #39 · t2000188 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eea:50

English: Similar studies, for at least three soil types, must be reported for all relevant metabolites, degrada tion and reaction products which in soil degradation studies account at any time for more than 10 % of the amount of active substance added.

Reference (shown after audit): Gera skal grein fyrir svipuðum rannsóknum á þremur jarðvegsgerðum hið minnsta með tilliti til allra viðkomandi umbrots-, niðurbrots- og hvarfaefna sem í rannsóknum á niðurbroti í jarðveginum nema á einhverjum tímapunkti meira en 10% af viðbættu magni virka efnisins.

Review: Soil types and degradation/reaction products mistranslated.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Tilgreina verður sömu rannsóknir á að minnsta kosti þremur jarðefnum fyrir öllum viðeigandi umbrotsefnum, brotthvarfinu og framleiðsluefnum sem í rannsóknum á jarðbrottum taka stærri en 10% af skömmtum virka efnisins sem bætt er við.

</details>

<details><summary>development_review #40 · A · greedy · general · P</summary>

Source ID: p13official21:dev:opensubtitles:1012

English: I'll do whatever you ask.

Reference (shown after audit): Ég geri hvað sem þið viljið.

Review: Whatever you call for/request retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Ég geri hvað sem þú kallar til.

</details>

<details><summary>development_review #41 · t2000188 · G8 · technical_short · U</summary>

Source ID: p13official21:dev:eea:609

English: Special payments for shift work.

Reference (shown after audit): Sérstakar greiðslur vegna vaktavinnu.

Review: Special payments retained; shift-work terminology is an uncertain calque.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Sérstakur greiðslur fyrir mótskráða starf.

Candidate 1: Sérstök greiðslur fyrir skiptarverka.

Candidate 2: Sérstakar greiðslur vegna skipta- starfseðlis.

Candidate 3: Sérstakar greiðslur til skipta.

Candidate 4: Sérstakur greiðslur fyrir skrúðaönnun.

Candidate 5: Sérstækku greiðslur fyrir skiptarstarf.

Candidate 6: Sérstakar greiðslur fyrir stöðugan verk.

Candidate 7: Sérstakar greiðslur fyrir skipta- starf.

</details>

<details><summary>development_review #42 · A · greedy · technical_short · F</summary>

Source ID: p13official21:dev:eea:1461

English: All industrial uses of gas are considered.

Reference (shown after audit): Öll notkun á gasi í atvinnurekstri er talin með.

Review: Industrial gas uses replaced by unrelated space/work expression.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Allar vinnuþætti úr geimu eru í talið.

</details>

<details><summary>development_review #43 · A · greedy · general · P</summary>

Source ID: p13official21:dev:opensubtitles:3209

English: Because it's not safe there.

Reference (shown after audit): Af því að það er ekki öruggt.

Review: Unsafe place retained; minor grammar.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Það er ekki örugg í því stað.

</details>

<details><summary>development_review #44 · t1001129 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:ema:1394

English: The most commonly reported adverse reactions (≥ 20%) among patients treated with both belatacept- based regimens (MI and LI) up to Year 3 are diarrhoea, anaemia, urinary tract infection, peripheral oedema, constipation, hypertension, pyrexia, nausea, graft dysfunction, cough, vomiting, leukopenia, hypophosphataemia, and headache.

Reference (shown after audit): Algengustu aukaverkanirnar (≥ 20%) hjá sjúklingum sem fengu báðar belatacept meðferðirnar (MI og LI) fram að 3. ári eru niðurgangur, blóðleysi, þvagfærasýking, bjúgur á útlimum, hægðatregða, háþrýstingur, hiti, ógleði, ófullnægjandi starfsemi græðlings, hósti, uppköst, hvítfrumnafæð, blóðfosfatskortur og höfuðverkur.

Review: All candidates corrupt multiple named adverse reactions or timing.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Algengustu aukaverkanir, sem fylgt er fram hjá sjúklingum sem fengu bæði reglubundnar meðferð með belatacepti (MI og LI) allt að þriðja ári (≥ 20%) eru niðurgangur, blóðleysi, þvagrekki, í bundiðum frumunum, truflingu, hýði, hita, ógleði, ofningartafla, hóll, uppköst, blóðleysi, blóðfosfatsseniaði, og höfuðverki.

Candidate 1: Algengst verndstöfunum sem færðust meðan þeir verða með meðferð með beina reglum (MI og LI) eftir 3 árum eru niðurganga, blóðleysi, þvaggefsbólga, þurrætti, kraftabrisi, háþrýsting, hita, ógleði, blöðruðreykingar, hótt, uppköst, blóðleysi, blóðfosfenosýlslækkun og heilablóðsýkingar.

Candidate 2: Yfirleitt tilkynntar aukaverkanir (≥ 20%) hjá sjúklingum sem fengu bæði reglan með belatacept (MI- og LI) á aldrin 3 er niðurgang, blóðleysi, þol í þungnefnd, bólga í umhverfi, æðabresti, háþrýstingur, hita, ógleði, nýrnabilun, hógg, uppköst, blóðleysi, blóðfosfóratfjarlæggð, og heilablóðsýkingi.

Candidate 3: Algengustu aukaverkanirnar sem fram kemur hjá sjúklingum sem fengu beiningar meðferð með báðum meðferðarskefnum sem byggjast á belatacepti (MI og LI) í allt fram til árs 3 eru niðurgang, blóðleysi, niðurgang í þvagvegnum, bólga í umborði, þrónstig, háþrýstingur, heitarþol, ógleði, skömmu, uppköstum, blóðfalli, blóðfosfat í blóði, og höfuðverk.

Candidate 4: Algengustu aukaverkanirum (≥ 20%) sem greint hefur verið frá (sjúklingum sem fengu beðli með belatacept-bundiðum meðferðabreytingum) í allt fram yfir árið 3, eru niðurganga, blóðleysi, kveikjusýki í þvagvöðruninu, þrotamassa í altliðum, straxbólgu, háþrýsting, hita, ógleði, grífða starfsemi, hixtar, uppköst, blóðfall, blóðfosfatsfall, og höfuðverk.

Candidate 5: Algengustu aukaverkanir sem fylgt var fram hjá sjúklingum sem fengu meðferð með bæði reglum á basis belatacepti (MI- og LI) í aðri árum (≥ 20%) eru niðurgang, blóðleysi, kvefseýrissýkingur, frumaskerð, sem af mörkuðu umhverfi, háþrýstingur, hita, upvarmi, andi, kvöldlög, uppköst, blóðleysi, blóðfosferfið, og höfuðverk.

Candidate 6: Algengustu aukaverkanir (≥ 20%) sem greindust hjá sjúklingum sem fengu meðferð með bæði reglum sem byggðar eru á belatacepti (MI og LI) allt í 3. ár eru niðurgang, blóðleysi, insjólyfjamein, bólga, trapa, háþrýsting, hita, ógleði, áhrifum ónæmisafurða, hógg, uppköst, blóðfall, blóðfosfóratskort og höfuðverk.

Candidate 7: Fyrst og fremst fyrir yfirleitt tilkynnta aukaverkanir (≥ 20%) hjá sjúklingum sem fengu meðferð með beina reglum með belatacepti (MI og LI) eftir 3 ár eru niðurgang, blóðleysi, niðurgangsgeir, bláæð í ytri hlið, truflun, þrýsting, hitastig, uppköst, þunglyndi, hósk, uppköst, blóðlysaþrýsting, blóðstorkum, og höfuðverk.

</details>

<details><summary>development_review #45 · t1001129 · greedy · general · P</summary>

Source ID: p13official21:dev:opensubtitles:1159

English: Somebody get me a picture of the girl.

Reference (shown after audit): Útvegið mér mynd af stelpunni.

Review: Someone get me a picture of the girl retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Einhver fá mér mynd af stúlkunni.

</details>

<details><summary>development_review #46 · A · G8 · technical_long · F</summary>

Source ID: p13official21:dev:ema:1394

English: The most commonly reported adverse reactions (≥ 20%) among patients treated with both belatacept- based regimens (MI and LI) up to Year 3 are diarrhoea, anaemia, urinary tract infection, peripheral oedema, constipation, hypertension, pyrexia, nausea, graft dysfunction, cough, vomiting, leukopenia, hypophosphataemia, and headache.

Reference (shown after audit): Algengustu aukaverkanirnar (≥ 20%) hjá sjúklingum sem fengu báðar belatacept meðferðirnar (MI og LI) fram að 3. ári eru niðurgangur, blóðleysi, þvagfærasýking, bjúgur á útlimum, hægðatregða, háþrýstingur, hiti, ógleði, ófullnægjandi starfsemi græðlings, hósti, uppköst, hvítfrumnafæð, blóðfosfatskortur og höfuðverkur.

Review: All candidates have extensive adverse-reaction-list corruption.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þeir mismunandi aukaverkanir sem fengin eru flest (≥ 20%) hjá sjúklingum sem fengu bæði meðferð með beitliða tilteknunastarfsemi (MI og LI) í almenningi í 3. ár eru meðfylling, blóðfæð, bóluefni í blöndu, fyrirvörðum úrræða, stungulyfjagreining, þrýsting, þrýstingeyggjandi þrýsting, hita, hætt, sýking, upprösum, blóðfána, blóðpóntlega smit og heilkenni.

Candidate 1: Hæst vernda aukaverkanir (≥ 20%) hjá sjúklingum sem fengu bæði meðferð með belatacept-bundinum meðferðsklársemi (MI- og LI-meðferð) í þriðja ári eru þurrka, albúnmjögnun, skrám, hálfsýrissvæðisbrot, nýthreysting, áhættuvara, hit, ógreiðsleika, bráðbrot, gegnverk, þræling, uppköst, blóðfall, nýsól, óósfúði og hettuglest.

Candidate 2: Hámarkslega greindandi aukaverkanir hjá sjúklingum sem fengu bæði lyfja með belatácept-bundnum samsetningarjöfnum (MI og LI) allt að þriðju ári eru dagsetning, blóðleysi, skjúkling í þræla, frumvaldsblóðþyggjandi, standðæg, ofhamaskammt, sykurgang, upplausk, slýkunardrott, kvalslá, uppköst, smitblöndu, blóðþyngdarbólgu, og heilum.

Candidate 3: Bætur sem hafa verið tilgreindast flest tímum (≥ 20%) hjá sjúklingum sem hafa fengið bæði lyf sem byggjast á belatacept (MI- og LI-reglubundnu lyfjakerfi) til 3. ára eru dröl, blóðflæðisminning, þvaglaus, umbóðsbólgu, því því kassir, of ótaus, súrt, kælingur, skjaldandi, aðhæm, dýra, uppiþjáing, blóðflæðisminning, ópísaðurblóði og höfuðveri.

Candidate 4: Mest oft upplýst neikvæð áhættur (≥ 20%) hjá sjúklingum sem fengu bæði bélátácept-bundnu meðferð með miðlægði (MI) og meðferð með lífleyti (LI) á alls tímabili til 3. ári eru kjölfjölda, þvagpróf, þvagi í þunguhópi, þvagi í blóðblöndu, þvagi í blóðbúði, þvaglegri blóðþvagi, þvagi í blóðlyfi, þvagi í brastlausn, þvagi í cútum, þvagi í kælingu, þvagi í blöðrútni, hollfjölda, hollfjóði og þvagi í heilfjölda.

Candidate 5: Meiri áhættuverkefna (≥ 20%) sem var tilkynnta hjá sjúklingum sem fengu bæði bæta meðferð á grundvelli belatacept (MI- og LI) áður en í ár 3 eru þróun, blóðlausn, þvaglausn í þvaglausnarefninum, þungdæm, þvagstungd, offlýsandi þvag, heildarþvag, háþvag, uppköst, lífshjálp sem stöðvar ekki skilgreind, þvagþvag, uppþvag, leikliður, smáphosfatiðskammt, og heilbrigði.

Candidate 6: Fjöllumst aukaverkanir (≥ 20%) sem sjúklingar á meðferð með beitið með belatacept (MI- og LI- meðferð) um þrjú árin eru dagsetning, blóðfalls, skjúklóðauki, brjóstáka, þroð, óþægnað, hita, ógreiðslu, gafnafjár, sykka, kæling, leikumfeðileg skemmtugrið, niðurgildi, og hettugreining.

Candidate 7: Mátað er besta meðalega verulega aukaverkanir (≥ 20%) hjá sjúklingum sem fengu bæði meðferð með kviklegum gróðurséðum bólusetningum (MI og LI) fyrir árið 3 er kjörring, blóðblöðruðu, skrýta í þjóðblóðkerfinu, hægður í hliða frumunguna, kald, hita, böngur, gróður í misvirkun, svali, uppköst, hvítblóðtækni, blóðflókinu og heilahöfuður.

</details>

<details><summary>development_review #47 · A · G8 · technical_medium · P</summary>

Source ID: p13official21:dev:eea:85

English: For the estimation of these concentrations all relevant information on the plant protection product and on the active substance must be taken into account.

Reference (shown after audit): Við mat á framangreindum styrk ber að taka allar viðeigandi upplýsingar um plöntuvarnarefnið og virka efnið til greina.

Review: Candidate0 retains estimated concentration,all relevant product/active-substance information and consideration requirement.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [0]

Candidate 0: Til að meta þessar styrk gilda allar viðeigandi upplýsingar um plöntuverndarefnið og virk efnin og skal taka tillit til þess.

Candidate 1: Að því er varðar þann þéttni sem verði fengin skal taka áhuga allar árangrar upplýsingar um plöntuvaran og virka efnið.

Candidate 2: Til áætlunar á þessum hámarkshluti skal taka allar viðeigandi upplýsingar um plöntuvaranir og virk efnið inn.

Candidate 3: Til matar á þessum styrkum verður að taka tillit til allra viðeigandi upplýsinganna um plöntuverndarvörur og virk efnið.

Candidate 4: Til matar í þessu styrk gilda allar viðeigandi upplýsingar um plöntuverndarvörur og virku efnið.

Candidate 5: Vegna ákvarðananna á þessum styrkum verður að taka tillit til allra viðeigandi upplýsinga um plöntuvaranir og virka efnið.

Candidate 6: Til að meta þessar styrk á öllum viðeigandi upplýsingum um plöntuverndarefnið og virk efnið sem gefið er á.

Candidate 7: Upptrúa skal við mat á þessum styrkleika að því tilskildu tilvikum allar viðeigandi upplýsingar um plöntuvarðandi lyfið og virk efnið.

</details>

<details><summary>development_review #48 · t2000188 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eso:924

English: ESO was delighted to welcome Italys Minister of Education, Universities and Research, H.E. Stefania Giannini, to the ceremony, which was also attended by the Italian Consul General in Munich, Renato Cianfarani, the ESO Council President, Patrick Roche, and the Italian ESO Council Delegates, Nicolò DAmico (who is also President of INAF) and Matteo Pardo, Scientific Attaché at the Italian Embassy in Berlin.

Reference (shown after audit): Viðstödd undirritunina voru H.E. Stefania Giannini, mennta- og vísindamálaráðherra Ítalíu, ítalski konsúllinn í München, Renato Cianfarani; Patrick Roche, forseti ESO ráðsins, Nicolò DAmico, forseti ESO ráðsins (sem er líka forseti INAF) og Matteo Pardo, fulltrúi vísinda í ítalska sendiráðinu í Berlín.

Review: Minister roles, ceremony and institutional details corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: ESO var ánægður við því að velja Stefania Giannini, yfirmaður niðurlandsins um náms- og rannsóknarræktir, til sérstakrar þáttar í þessari veitingaherbergi sem Rensato Cianfarani, yfirvaldsmaður Ítalíu í Múnich, Patrick Roche, forseti ESO ráðsins og Nícolò DAmico, hinn er einnig forseti INAF, og Matteo Pardo, vísindamálaráðherra Ítalíu í Berlín, tóku einnig þátt í þessari veitingaherbergi.

</details>

<details><summary>development_review #49 · t1001129 · greedy · general · P</summary>

Source ID: p13official21:dev:opensubtitles:996

English: What kind of man would that make me?

Reference (shown after audit): Hvers konar maður væri ég þá?

Review: Rhetorical question about the kind of man this makes the speaker retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Hvers konar maður myndi það vera mér?

</details>

<details><summary>development_review #50 · t1001129 · G8 · technical_medium · F</summary>

Source ID: p13official21:dev:eso:70

English: This is only the sixth of these huge storms to be spotted since 1876.

Reference (shown after audit): Stormurinn er sá sjötti sem menn verða vitni að á Satúrnusi frá árinu 1876.

Review: No candidate correctly renders sixth huge storm since1876.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þetta er aðeins sjö af svona alvarlegum stormi sem hafa verið greint af síðan 1876.

Candidate 1: Þetta er aðeins sjö stöðugum og stórum vetrarbrautar sem hefur farið út síðan 1876.

Candidate 2: Þetta er aðeins sjö af þessu alþjóðlegum hurðum sem fyrir eftir hafa komið fram sinnum eftir 1876.

Candidate 3: Þetta er aðeins sjö græn gátugáturnar sem hafa verið birtir síðan 1876.

Candidate 4: Þetta er aðeins sjö þessara alvarlegra skjálfbreyturna sem fengist síðast 1876.

Candidate 5: Þetta er aðeins sjökthóð af slæmum þrýstingum sem hafa verið gengin síðan árið 1876.

Candidate 6: Þetta er aðeins sjötta þessara miklum slátum sem hafa verið fyrir sig sánu síðar en 1876.

Candidate 7: Þetta er aðeins sex af þessum umborðsæðum sem fæst síðan 1876.

</details>

<details><summary>development_review #51 · A · greedy · general · F</summary>

Source ID: p13official21:dev:opensubtitles:480

English: Now we have enough evidence to charge you with murder.

Reference (shown after audit): Við höfum næg sönnunargögn til að ákæra ykkur fyrir morð.

Review: Evidence and charge with murder garbled.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Nú er við nægilega fullnægjandi einkenna til að skipta þig í mörkun.

</details>

<details><summary>development_review #52 · t1001129 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eso:924

English: ESO was delighted to welcome Italys Minister of Education, Universities and Research, H.E. Stefania Giannini, to the ceremony, which was also attended by the Italian Consul General in Munich, Renato Cianfarani, the ESO Council President, Patrick Roche, and the Italian ESO Council Delegates, Nicolò DAmico (who is also President of INAF) and Matteo Pardo, Scientific Attaché at the Italian Embassy in Berlin.

Reference (shown after audit): Viðstödd undirritunina voru H.E. Stefania Giannini, mennta- og vísindamálaráðherra Ítalíu, ítalski konsúllinn í München, Renato Cianfarani; Patrick Roche, forseti ESO ráðsins, Nicolò DAmico, forseti ESO ráðsins (sem er líka forseti INAF) og Matteo Pardo, fulltrúi vísinda í ítalska sendiráðinu í Berlín.

Review: Named attendees roles, minister and Berlin location corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: ESO var ánægð við því að velja Stefania Giannini, yðurherra menntamálsminsturs Ítalíu, til þess að fella á um veitinguna sem einnig tókst í hana Renato Cianfarani, samræðavarnarbær Ítalíu í Múnich, Patrick Roche, forseti ráðsins ESO og Nicolò DAmico (sem er einnig forseti INAF) og Matteo Pardo, vísindasjónarstjórnar í Ítalíu í Börsleitinu.

</details>

<details><summary>development_review #53 · t2000188 · greedy · technical_short · F</summary>

Source ID: p13official21:dev:ema:704

English: The most frequently reported adverse reaction was acne, which was generally mild.

Reference (shown after audit): Algengasta aukaverkunin sem greint var frá er þrymlabólur (acne), sem voru venjulega vægar.

Review: Acne replaced by unrelated cow/udder disease term.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Algengasta aukaverkunin sem greint hefur verið frá var kúupjúgur, sem var almennt væg.

</details>

<details><summary>development_review #54 · t1001129 · G8 · technical_short · U</summary>

Source ID: p13official21:dev:ema:767

English: Therefore, docetaxel must not be used during pregnancy unless clearly indicated.

Reference (shown after audit): Dócetaxel á því ekki að nota á meðgöngu nema brýna nauðsyn beri til.

Review: Pregnancy prohibition retained but clear indication qualification unreliable.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Því má ekki nota docetaxel meðan á meðgöngu stendur nema myndist upplýsingar um að nota það.

Candidate 1: Því má ekki nota doketaxel á meðgöngu nema ákveðnar tilvik komi fram.

Candidate 2: Því má ekki nota doketaxel á meðgöngu nema fyrir hag sé greinilega bætt.

Candidate 3: Þar af leiðandi má ekki nota dócetaxel á meðgöngu nema ákvarðanlegt sé um það.

Candidate 4: Því má ekki nota docetaxel á meðgöngu nema að greinileg viðbót er fyrir um.

Candidate 5: Því verður að ekki nota dócetaxel á meðgöngu nema áður að það er greint fyrir.

Candidate 6: Því má ekki nota dócetaxel á meðgöngu nema felldar tilgreiningar komi fyrir.

Candidate 7: Því má ekki nota dócetaxel á meðgöngu nema skýrt erðu bætt fyrir.

</details>

<details><summary>development_review #55 · t1001129 · greedy · technical_short · U</summary>

Source ID: p13official21:dev:ema:2013

English: There is no evidence to suggest that eptotermin alfa alters fertility.

Reference (shown after audit): Ekkert bendir til þess að eptotermin alfa hafi áhrif á frjósemi.

Review: No-evidence/fertility recognizable but extra malformed predicate and drug-name fidelity uncertain.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ekki er nokkuð sýnt til að bleyri eptetermin alfa hafi áhrif á frjósemi.

</details>

<details><summary>development_review #56 · t1001129 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eso:765

English: “If it keeps spinning rapidly it might end its life in one of the most energetic explosions in the Universe, known as a long-duration gamma-ray burst,” says the lead scientist of the project, Hugues Sana, of the University of Leuven in Belgium.

Reference (shown after audit): „Haldi hún áfram að snúast mjög hratt gæti hún endað ævina sem langur gammablossi, ein orkumesta sprenging í alheiminum,“ segir Hugues Sana við Leuvenháskóla í Belgíu sem hafði umsjón með rannsókninni.

Review: Gamma-ray burst and energetic explosion terminology corrupted throughout.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: „Ef hún helst er að snúast hraðlega getur hún það endur á lífi sínu í einu af lengstu sprengingum í alheiminu sem kallast langtímabilu gammaldreifingum,“ sagði Hugues Sana, aðalhöfundur verkefnsins í Leuven universitíðum í Belgíu.

Candidate 1: „Ef það hreyfir hraða um sig, getur það endað lífi sínu í eina af stórum skrælum í alheiminu, sem kallast langmótaleka,“ sagði Hugues Sana, aðalvísindamannur í verkefnið, í Leuven-universiteteni í Belgíu.

Candidate 2: „Ef þetta hörður stóð í gæðum kann það að endast lífi sínu í eina af meiri orkuþurrindum alheimisins sem hefur þegar verið kynsetur sem langtímameðdýrskapur,“ sagði Hugues Sana, hópafræðingur á verkefnið við Universitäð Leuven í Belgíu.

Candidate 3: „Ef hún virkar til umfram áfram endast hún til smást í björtustu sprengingu sem er varðar er í alheiminu og kallast langtímamein magnhvarfsbrún,“ sagði Hugues Sana, aðalhagsmaður verkefnisins, frá Leuven-í Belgíu.

Candidate 4: „Ef það hreyfir á hraði hæstar endurteknum stærsta sprautu sem okkar er með, sem víst umstungur sér í alhovunum sem ketjuðu áhrif í spjald,“ sagði Hugues Sana, aðalhagsaðilar verkefnisins, sem er á vísindasemilarík við Leuven í Belgíu.

Candidate 5: „Ef það hreyfir hraða móti má það færi loku síns í einhverjum langvarandi geimrennsli í heimi, sem heitir langvarandi geimsemiði,“ sagði Hugues Sana, framsærihlerð verkefnisins, af Leuven skó last í Belgíu.

Candidate 6: „Ef það virkar tíðlega að snúa, kann það að endast líf síðar í einhverjum langlengdum líffarsbrosum um heim, sem vart er með þýðingu um langvarið gammabreikja-shift,“ sagði urðarhagurur vinnslunnarins, Hugues Sana, af Leuven universitetas í Belgíu.

Candidate 7: „Ef það spinnir of hratt mun það enda líf sitt í einu af stórum mjólkustu styrk sem verður á alheimsverðinu, sem kallast langhringsspeglinga,“ sagði aðalvísindan efnasamfelldarverkefinu, Hugues Sana, af Leuven universitý í Belgíu.

</details>

<details><summary>development_review #57 · t2000188 · G8 · technical_medium · P</summary>

Source ID: p13official21:dev:ema:1718

English: Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.

Reference (shown after audit): Gjöf edoxabans samtímis P-gp virkjanum rífampisíni leiddi til lækkunar á meðalgildi AUC fyrir edoxaban og styttri helmingunartíma, með hugsanlegri minnkun á lyfhrifum þess.

Review: Candidate2 preserves rifampicin P-gp inducer,AUC reduction,shortened half-life and possible reduced pharmacodynamic effects.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [2]

Candidate 0: Samtímis gjöf edoxabans og P-gp örva rífampicins leiddi til minnkaðrar meðalástandar AUC eftir töflu fyrir edoxaban og minnkaðrar helmingunartíma, sem gæti valdið minnkuðum lyfhrifum.

Candidate 1: Samtímis gjöf edoxaban og P-gp viðbragðagerans rifampicins leiddi til minnkaðrar meðaltals AUC gildi edoxaban og skömmu helmingunartíma, sem getur aukið vart við minnkaðar lyfhrifum.

Candidate 2: Samtímis gjöf edoxabans og P-gp örva, rifampicins, leiddi til minnkar meðal AUC fyrir edoxaban og minnkunar helmingunartíma, sem hugsanlega valdið minnkun á lyfhrifum.

Candidate 3: Samtímis gjöf edoxaban og P-gp örva, rifampicins, leiddi til minnkaðrar meðaltals AUC fyrir edoxaban og minnkunar helmingunartíma, með aðalhætta á lækkun á lyfhrifum.

Candidate 4: Samtímis lyfjagjöf edoxaban og P-gp ifnæmisli rifampicins leiddi til minnkaðs meðaltals AUC fyrir edoxaban og skerðingar á helmingunartími, sem gæti haft mögulega áhrif á lyfhrif.

Candidate 5: Samtímis gjöf edoxaban og P-gp örvunar með rifampicini leiddi til minnkaðrar meðaltals AUC fyrir edoxaban og styttra helmingunartíma, með hættulegan hætta á lyfhrifum.

Candidate 6: Samtímis gjöf edoxaban og P-gp örvið rifampicins leiddi til minnkaðrar meðalleggjaðar AUC fyrir edoxaban og skammar helmingunartíma, mögulega minnkaðri lyfhrifum þess.

Candidate 7: Samhliða lyfjagjöf edoxaban og P-gp-örvuhvörfarinnar rífampicíns leiddi til minnkunar á meðal AUC fyrir edoxaban og minnkaðri helmingunartími, sem gæti haft áhrif á lyfhrif.

</details>

<details><summary>development_review #58 · t2000188 · G8 · technical_medium · P</summary>

Source ID: p13official21:dev:eea:1585

English: The Commission shall submit a final evaluation report at the end of the Programme.

Reference (shown after audit): Framkvæmdastjórnin skal leggja fram endanlega matskýrslu við lok áætlunarinnar.

Review: Candidate2 preserves Commission submission of final evaluation report at programme end.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [2]

Candidate 0: Framkvæmdastjórnin skal leggja fram endanleg matsskjöld eftir hafsáætluninni.

Candidate 1: Framkvæmdastjórnin skal leggja fram lokasag með endanlegum mati eftir endanum á umferðaráætluninni.

Candidate 2: Framkvæmdastjórnin skal leggja fram endanlega matsskýrslu eftir lok áætlunarinnar.

Candidate 3: Framkvæmdastjórnin skal leggja fram endanlega matsskil á lok áætlunarinnar.

Candidate 4: Framkvæmdastjórnin skal leggja fram endanleg matsskil á lok áætlunarinnar.

Candidate 5: Framkvæmdastjórnin skal lagðar fram endanlegar matsskrit á lokum áætlunarinnar.

Candidate 6: Framkvæmdastjórnin skal lagða fram endanlegur matsskýrslu innan þeirrar loku sem áætlað er á áætluninni.

Candidate 7: Framkvæmdastjórnin skal leggja fram endanlegar matarannsóknarályður eftir lok áætlunarinnar.

</details>

<details><summary>development_review #59 · A · G8 · technical_short · U</summary>

Source ID: p13official21:dev:eea:2037

English: Those criteria should not be considered to be exhaustive.

Reference (shown after audit): Þessar viðmiðanir skulu ekki teljast tæmandi.

Review: Not perfect/complete is not unambiguously the intended non-exhaustive criterion.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Einnig skal ekki taka þessar viðmiðanir sem fullkomnir.

Candidate 1: Þessi viðmiðanir skulu ekki teljast fullkomnir.

Candidate 2: Þessar viðmiðanir skulu ekki teljast fullkomnir.

Candidate 3: Vegna þessarar viðmiðana skal ekki telja þeir fullkomnir.

Candidate 4: Þessi viðmiðanir skulu ekki telst fullkomnir.

Candidate 5: Einnig skal ekki telja þessar viðmiðanir fullkomnir.

Candidate 6: Sem skilmálirnar eru ekki fullfangvirði.

Candidate 7: Lækni skal ekki telja þessar viðmiðanir fullkomin.

</details>

<details><summary>development_review #60 · t2000188 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eso:323

English: They were able to make the sharpest direct observation ever , of the centre of a distant galaxy, the bright quasar 3C 279, which contains a supermassive black hole with a mass about one billion times that of the Sun, and is so far from Earth that its light has taken more than 5 billion years to reach us.

Reference (shown after audit): Þannig tókst þeim að gera skörpustu beinu mælingarnar sem gerðar hafa verið á miðju fjarlægrar vetrarbrautar, bjarta dulstirninu 3C 279 sem geymir risasvarthol sem er eins milljarðs sinnum massameira en sólin og er svo langt frá jörðinni að ljós þess er 5 milljarða ára að berast til okkar.

Review: Billion-year and billion-solar-mass values changed to millions; black hole lost.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þau gengu fram að gera skarpsamlega beinu sjónauki á miðju langt fjarlægðar vetrarbrautarins, 3C 279, sem er bjart og inniheldur öflugan svöl, með massafjölda um bil milli milljónum sólarmassa, og er svo langt frá Jörðinni að ljósinn hennar hefur tekið meira en 5 milljón ára til okkar.

</details>

<details><summary>development_review #61 · t1001129 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eso:464

English: With an estimated mass of four to five times that of Jupiter, it would be the least massive planet to be directly observed outside the Solar System.

Reference (shown after audit): Massi fyrirbærisins er talinn milli fjórum til fimm sinnum meiri en massi Júpíters, svo hér gæti verið um að ræða massaminnstu reikistjörnu sem ljósmynduð hefur verið fyrir utan sólkerfið okkar.

Review: Estimated mass and directly observed proposition mistranslated.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef það hefði fjarlægð massafjölda sem er fjórar til fimm sinnum stærri en Júpíturnar væri það minnst massaverðan jörð sem hefur verið eftirskrifað frá utan sólkerfinu.

</details>

<details><summary>development_review #62 · t2000188 · greedy · general · P</summary>

Source ID: p13official21:dev:opensubtitles:1159

English: Somebody get me a picture of the girl.

Reference (shown after audit): Útvegið mér mynd af stelpunni.

Review: Request for someone to supply a picture of the girl retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Einhvern geri mér mynd af stúlku.

</details>

<details><summary>development_review #63 · t2000188 · G8 · technical_short · P</summary>

Source ID: p13official21:dev:ema:1192

English: It is used to prevent pregnancy.

Reference (shown after audit): Lyfið er notað til að koma í veg fyrir þungun.

Review: Candidate2 correctly states use to prevent pregnancy.

Inspected original candidate indices: [0, 1, 2, 3, 5, 7]; confirmed correct indices: [2]

Candidate 0: Hann er notað til að koma fyrir barnshafa.

Candidate 1: Hann er notað til að koma í veg fyrir þungun.

Candidate 2: Það er notað til að koma í veg fyrir þungun.

Candidate 3: Það er notað til að dökkja þungun.

Candidate 5: Það er notað til að forðast þungun.

Candidate 7: Hann er notað að koma í veg fyrir þungun.

</details>

<details><summary>development_review #64 · t1001129 · G8 · technical_medium · F</summary>

Source ID: p13official21:dev:eea:698

English: Only days that can be worked should be included when Saturdays and Sundays are not worked they should not be included, the same with public holidays).

Reference (shown after audit): Eingöngu skal telja með þá daga sem unnt er að vinna (ef ekki er unnið á laugardögum og sunnudögum skal ekki telja þá með; hið sama gildir um lögboðna frídaga).

Review: No candidate correctly preserves both weekend days and conditional inclusion/exclusion.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Aðeins dagsetningar sem fáið að vinna skulu vera í skrá þegar ekki er vinna á sástóru eða sunnudagum, eitt og sama við opinbera helgum).

Candidate 1: Einungis daga sem má vinna skulu fylgt út, ef ekki er vinna á sólarhringum og á sólarhringum, skulu þau ekki fylgt út, og sama við opinberar helgi).

Candidate 2: Aðeins daga sem má vinnast eiga að taka að skrá þegar eigi verndast í laugardagana og laugardagsmóndaðum skal aðeins taka að skrá það ekki, eins og að eigi verndast í opinberum fríar).

Candidate 3: Einnig aðeins daga sem ná ekki við að vinna skulu tekið með í hlutum, ef ekki er vinna á laugardagum og sonsdagum skulu þeim ekki tekið með í hlutum, eins og við opinbera ferðadaganna.

Candidate 4: Aðeins dagar sem má vinna skal skaltu taka in í matinn, ef eigi að vinna á Söndagum og sunnudögum ætti það ekki að taka in, eins og við borgarheildagum).

Candidate 5: Eina sinni skulu daga sem má auðvöld þegar eða með sáster og sólarhringum skerða skipta fram en ekki að þeim skuli sú hins vegar, að sama fylgja opinberum fríum).

Candidate 6: Bara skal fá til að verka dagir sem reyndar eru að velja skal ekki þegar mánadagur og sunnudagur eru ekki verka, samfærð berast með opinberum ferðadagum).

Candidate 7: Aðeins dagar sem eru hæfilegar til að virka skulu skiptast við þegar ekki er virkt á Söndagum og sunnudögum, skulu ekki vera skiptar við, eins og um opinbera frí.

</details>

<details><summary>development_review #65 · A · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eso:206

English: The survey was sensitive to planets between 75 million kilometres and 1.5 billion kilometres from their stars (in the Solar System this range would include all the planets from Venus to Saturn) and with masses ranging from five times the Earth up to ten times Jupiter.

Reference (shown after audit): Mælingarnar voru næmar fyrir reikistjörnum sem eru milli 75 milljón til 1,5 milljarða km frá móðurstjörnunum (í sólkerfinu okkar inniheldur þetta fjarlægðarbil allar reikistjörnur frá Venusi til Satúrnusar) og frá fimm sinnum massameiri en jörðin upp í tíu sinnum massameiri en Júpíter.

Review: All distance units/numbers or mass ranges corrupted.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Skoðunin hefur verið sérstakt á þá umhverfi sem eru á milljónu km milli 75 milljóna km frá stjarna (hér í Solæðamálum ætti þetta umræði að ná alltaf umhverfinu frá Venus til Saturn) og með massaverkunum á milljónu km milli fimm gilda Erðis og tíu gilda Júpítar.

Candidate 1: Tölunnar var hrá við fjölda plöntu á milljónum milljónum klukkustundum að 1,5 billjón klukkustundar af þeim stjörnu (þar sem viðkomandi milljónir eru allir plönturnar frá Venus til Saturn) og með massa sem verið er áfram frá fimm fálaðum jörðu og að meira en tíu fálaðum Júpítu.

Candidate 2: Slíkt sýnslag var háð við hátt í íplaneteðunum milljarðar (75 m.j. frá þeirri stjarna til 1,5 billjón milljarða) og með þroskun í milljúrgang (fyrir Sjóplaneteðuna milli Venus og Saturn).

Candidate 3: Tilskilunin var háttur við geð í umhverfisfarið sem liggur fyrir milljónum milljóna km. og fyrir milljónum milljónum km. frá stjarnunum (sjáskildar vinnu í himinninni eru það öll geð frá Venus til Saturn) og með massu á milli fyrir fimm sinnum heims í júlíjaðri og fyrir tíu sinnum Júlíus.

Candidate 4: Tilvísunin var snyrt að úr féllu sem eru milljan milljóna km frá stjörnunum (í Solhjóðaverði gildir það meginfjölda hinna féllanna frá Venus til Saturn) og með massa sem var á milli fimm fylgju miðaltraða Júpítu og tíu fylgju miðaltraða öðru júpítu.

Candidate 5: Sýnaði var hönnulega varanir á planítu sem eru um 75 million km og 1,5 billjón km frá stjarnanum (þar í Solasjóðinu forðast allir plönturnar frá Venus til Saturn) og vegna massa varananna stendur frá fimm tíðum jörðu til tíða Júpítu.

Candidate 6: Rannsóknin var sérstakt á geislum úr þrúgum ngaða milljóna km fyrir umhverfisstjarna og 1,5 billióna km fyrir umhverfisstjarna (á stjórnsýsluhólsnum voru svo sérhæfð um allar þrúgur úr Venus til Saturn) og með massa sem var á milli fimm fylgir jörðs og tíu fylgjara Júpítu.

Candidate 7: Sýnið var hámarkssvifandi fyrir hreyfill sem voru með 75 milljóna miljóna gekk yfir enginn stjarnan og 150 milljóna miljóna gekk yfir (í Solvædirnýjunni mæltið af Vénus til Saturni), með þyngd úr fimm til júlíus tíðina Júpíturs að Júpítur.

</details>

<details><summary>development_review #66 · t2000188 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eea:574

English: All rear-window, roof-panel and partition switches intended for use by occupants in the rear of the vehicle shall be capable of being switched off by a driver-controlled switch which is located forward of a vertical transverse plane passing through the R points of the front seats.

Reference (shown after audit): Allir rofar í hliðarrúðum að aftan, þaklúgum og skilrúmum sem farþegum baka til í ökutækinu er ætlað að nota skulu gerðir með þeim hætti að unnt sé að rjúfa straum til þeirra með rofa sem ökumaður stjórnar og er staðsettur framan við lóðrétt þverplan sem gengur í gegnum R-punkta framsætanna.

Review: All switch,driver-control and geometry constraints corrupted.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Allar bakgondastillar, haldið veggir og salgurnar sem notendur á aðinn eftir rútinu í ökutækinu skulu hægt að slípa við af handteknar skiptivissu sem er í fyrstu stæði, á hraðu við rúðinu við þriðjaða þaknum ökutækisins.

Candidate 1: Allir opinbreytingar á bakglugga, húðmælinum og víðblandingum, sem notendur afhenda í bakinn á ökutækinu, skulu geta verið skiptar ofsýnt af kjölfylgni með ölastilhöndluninni sem er settu fyrir aftan á hliðar lynggripaðs.

Candidate 2: Allir bakgluggssvirkur, veggur og rammasvikur sem ætlaðir eru fyrir notendum í reyri ökutækisins megast einstaklingur geta kláraðu við skipteyra sem veitir berjalíka lokagentur sem er staðsettur fyrir aftan við hvörfþyngd, sem fer út fyrir fyrstu sæta.

Candidate 3: Allar höðvaka, aðlaga og þilfarihraða, sem ætlaðir eru til notkunar hæfur fyrir einstaklinga í eftirhlið ökutækisins, skulu vera takmörkuð til að gráta á við um leiðtogi ökuna sem er stjórnunarlífi og er í borð við hægri hljóðplan sem fer úr R-stjörnunum á framansetur.

Candidate 4: Hverja afturslögun, skuggaskipti og voru skipti sem ætlaðir eru fyrir notendum á eftirrásinni ökutækisins verða getur hægt að slökkva með skipti sem annast auglýsandi handir í fyrir framhliðar lígrífalli sem snertir R-staðar fyrir framseturar sætur.

Candidate 5: Allar bakiót, takfölutöflur og þrífræðiröskur svo geymdur og á undanþágu ökutækisins, sem áttu aðeinst að nota einstaklingur yfirleitti að henni, skulu tækifærslu sem aðskilnar eða takarauki af ökumönnum sem eru á borðum að vera takinn af þá aðskilnaðar eða takarauki af ökumönnum sem falli yfir mjög hlutfallinn yfir borðafurðirinn.

Candidate 6: Allir bakglas, tegli og dílslökkur sem ætlaðar eru til notkunar af innersætum á aftan af ökutækinu skulu geta verið slökkt á af blokkkenndri vélkommunum sem eru fram í gegnum R-stjörnum í framansetningum.

Candidate 7: Öll bakgluggasvirkjarnir, baklægur og andalkerfi, sem ætlaðir eru til notkunar fyrir sjúklinga í bakrásni ökutækisins, skulu sjálft séu takmörkuð til að slaka á með vélur sem stjórnað er fyrir af hálfastöðum sem ferðast í baki hjá innri raskarásum.

</details>

<details><summary>development_review #67 · t1001129 · G8 · technical_medium · P</summary>

Source ID: p13official21:dev:eea:1914

English: This Regulation shall enter into force on the third day following that of its publication in the Official Journal of the European Union.

Reference (shown after audit): Reglugerð þessi öðlast gildi á þriðja degi eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.

Review: Candidate5 faithfully states third day after publication in EU Official Journal.

Inspected original candidate indices: [0, 1, 2, 4, 5, 6, 7]; confirmed correct indices: [5]

Candidate 0: Reglugerð þessi öðlast gildi fyrri degi eftir að hún er birt í Stjórnartíðindum Evrópusambandsins.

Candidate 1: Reglugerð þessi öðlast gildi fyrstu dagins eftir að hún var birt í Stjórnartíðindum Evrópusambandsins.

Candidate 2: Reglugerð þessi öðlast gildi þriggja daga eftir að hún var birt í Stjórnartíðindum Evrópusambandsins.

Candidate 4: Reglugerð þessi öðlast gildi þriðju degi eftir að hún er birtir í Stjórnartíðindum Evrópusambandsins.

Candidate 5: Reglugerð þessi öðlast gildi á þriðja degi eftir að hún er birt í Stjórnartíðindum Evrópusambandsins.

Candidate 6: Reglugerð þessi öðlast gildi fyrir þriðja degi eftir að hún er birt í Stjórnartíðindum Evrópusambandsins.

Candidate 7: Reglugerð þessi öðlast gildi þriggja daga eftir að hún er birt í Stjórnartíðindum Evrópusambandsins.

</details>

<details><summary>development_review #68 · t2000188 · G8 · technical_medium · U</summary>

Source ID: p13official21:dev:ema:1582

English: The treatment-free period, however, should take into account the pharmacological properties of the products used previously.

Reference (shown after audit): Meðferðarlausa tímabilið verður þó að taka mið af lyfjafræðilegum eiginleikum lyfja sem voru notuð áður.

Review: Treatment-free period not unambiguously retained.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Meðan á meðferðarstöðinni stendur skal íhuga lyfjafræðilega eiginleikar lyfjanna sem notuð er áður.

Candidate 1: Meðal eftir lyfjameðferð, skal þó taka tillit til lyfjamæralíkana lyfja sem notað hafa verið áður.

Candidate 2: Meðalhvarfatriðis skal þó að taka tillit til lyfjaheilkenni lyfjanna sem notaðir hafa verið.

Candidate 3: Hins vegar ætti meðferðarfraslanturinn að taka tillit til lyfjafræðilegra eiginleika lyfja sem notuð voru áður.

Candidate 4: Meðferðarfrávik skal þó taka tillit til lyfjafræðilegra eiginleika lyfjaða áður.

Candidate 5: Meðan um hefur verið að ræða meðferðarfrasláttur, skal taka tillit til lyfjafræðilegra eiginleika lyfjanna sem notuð voru.

Candidate 6: Meðan án meðferðar tímaningin skal athuga lyfjaheilkenni í öðrum vörnum.

Candidate 7: Meðan umferð er meðferðsnæmi skal taka í tillit til lyfjafræðilega eiginleika lyfsins sem notaður var áður.

</details>

<details><summary>development_review #69 · t2000188 · greedy · technical_short · P</summary>

Source ID: p13official21:dev:ema:1100

English: If you miss a dose, take your next dose as scheduled.

Reference (shown after audit): Ef þú gleymir skammti skaltu taka næsta skammt eins og venjulega.

Review: Missed dose and next dose as scheduled retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Ef þú gleymir skammtinum, taktu næsta skammt eins og áætlað er.

</details>

<details><summary>development_review #70 · t1001129 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eso:323

English: They were able to make the sharpest direct observation ever , of the centre of a distant galaxy, the bright quasar 3C 279, which contains a supermassive black hole with a mass about one billion times that of the Sun, and is so far from Earth that its light has taken more than 5 billion years to reach us.

Reference (shown after audit): Þannig tókst þeim að gera skörpustu beinu mælingarnar sem gerðar hafa verið á miðju fjarlægrar vetrarbrautar, bjarta dulstirninu 3C 279 sem geymir risasvarthol sem er eins milljarðs sinnum massameira en sólin og er svo langt frá jörðinni að ljós þess er 5 milljarða ára að berast til okkar.

Review: Galaxy, black hole and billion values corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þau fengu að gera skarpsamlega beint séslag á miðju fjölskyldunnar sem er fjarlægur, 3C 279, sem er bjartan kvarnafjöll sem inniheldur stórfjölgunarskugga með massu um bilin einni milljónum af þeirri sem sólininn, og er svo fjarlægt frá Jörðinni að ljósið hennar hefur komið yfir um fleiri en 5 milljón ára.

</details>

<details><summary>development_review #71 · t1001129 · greedy · technical_short · P</summary>

Source ID: p13official21:dev:eso:446

English: “Astronomers have waited for data like this for over a decade.

Reference (shown after audit): „Stjörnufræðingar hafa beðið eftir gögnum eins og þessum í yfir áratug.

Review: Astronomers waiting for these data over ten years retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: „Stjörnufræðingar hafa bíðið á þessum gögnum í meira en tíu árum.

</details>

<details><summary>development_review #72 · t2000188 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eso:501

English: The team used data from the UVES spectrograph on ESOs Very Large Telescope in Chile (to determine the properties of the star accurately), the Carnegie Planet Finder Spectrograph (PFS) at the 6.5-metre Magellan II Telescope at the Las Campanas Observatory in Chile, the HIRES spectrograph mounted on the Keck 10-metre telescope on Mauna Kea, Hawaii as well as extensive previous data from HARPS (the High Accuracy Radial velocity Planet Searcher) at ESOs 3.6-metre telescope in Chile (gathered through the M dwarf programme led by X. Bonfils and M. Mayor 2003–2010 described here).

Reference (shown after audit): Hópurinn notaði gögn frá UVES litrófsritanum á Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjörnunnar nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5 metra Magellan II sjónaukanum í Las Campanas stjörnustöðinni í Chile, HIRES litrófsritann á 10 metra Keck sjónaukanum á Mauna Kea á Hawaii sem og eldri gögn frá HARPS litrófsritanum (High Accuracy Radial velocity Planet Searcher) á 3,6 metra sjónauka ESO í Chile (aflað í M dwarf verkefninu undir forystu X. Bonfils og M. Mayor milli áranna 2003-2010 sem lýst er hér).

Review: All candidates lose or corrupt instrument/programme provenance and technical details.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Hópurinn notuði gögn úr UVES fyrirfarins við Very Large Telescope ESO í Chile (takinn til að meta eiginleikar stjarnunnar á nákvæmri hætti) Carnegie Planet Finder Spectrograph (PFS) á Magellan II stjörnustjörnunum 6,5 m á Las Campanas stjörnustöðinni í Chile, HIRES fyrirfarins á Keck 10 m á Mauna Kea í Hawaii svo og umfangsrikra gagna úr HARPS (High Accuracy Radial velocity Planet Searcher) við ESO fyrstu stjörnustjörnu við 3,6 m í Chile (sagað í þessum greinum á M daífum (M dwarf) átta X. Bonfils og M. Mayor, 2003-2010).

Candidate 1: Hópurinn notuði gögn úr UVES-lyfsins ESO Very Large Telescope í Chile (til að ákvarða eignarvorum stjarna), Carnegie Planet Finder Spectrograph (PFS) á Magellan II sjónauknum í Las Campanas stjörnustöðinni í Chile, HIRES-lyfsins sternastarfssjónaukans við Keck 10-metra sjónauka í Mauna Kea í Hawaii og frekar fyrrgengum gögn úr HARPS (High Accuracy Radial velocity Planet Searcher) sjónauka í 3,6 metra í Chile (sá upptaka var sú eftir M dwarf verkefni, fyrir framhaldandi stjórnaðarhætti X. Bonfils og M. Mayor 2003-2010 sem talin er hér á eftir).

Candidate 2: Hópurinn notaði þátttöku úr Uves skýrasjonum á Very Large Telescope ESO í Chile (um að meta eiginleika stjarnans), Carnegie Planet Finder Spectrograph (PFS) á 6,5 m Magellan II sjónauknum í Las Campanas stjörnustöðinni í Chile, HIRES skýrasjonin sem gert er á Keck 10 m sjónauka á Mauna Kea í Hawaii og endaðir fyrri þátttöku úr HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6 m sjónauknum ESO í Chile (söfnuð í ráðgjöfinni M dwarfgreiningar X. Bonfils og M. Mayor 2003 – 2010 sem lýst er hér fyrir sig).

Candidate 3: Hópurinn notaði þátttaka úr UVES mæliskjálkinu á Very Large Telescope ESO í Chile (til að meta eðlilega eiginleika stjarnanns), Carnegie Planet Finder Spectrograph (PFS) á 6,5 metra Magellan II sjónauknum á Las Campanas stjörnustöðinni í Chile, HIRES mæliskjálkinu á Keck 10 metra sjónauknum á Mauna Kea í Hawaii og upplýsanum fyrri upplýsingum úr HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6 metra sjónauknum ESO í Chile (feiliblaðs eðlilega frá stjarnstyrksrannsókninni X. Bonfils og M. Mayor 2003–2010 sem lýsir hér á).

Candidate 4: Lífræna meðalstarfsmannsins notuðu gögn úr UVES-geimsjónauki ESO Very Large Telescope í Chile (til að athuga eiginleg af þá mænu stjörnunnar), Carnegie Planet Finder Spectrograph (PFS) á 6,5-meters Magellan II-geimsjónauki í Las Campanas stjörnustöð í Chile, HIRES geimsjónauki sem stendur á Keck 10-meters-geimsjoninu í Mauna Kea í Hawaii og einnig mikla fyrri gögn úr HARPS (High Accuracy Radial Velocity Planet Searcher) í Chile (sem fara fram í 3,6-meter geimsjónunni ESO sem stórið hamastjörnuþýði X. Bonfils og M. Mayor samstæðuð 2003-2010 og lýst er hér).

Candidate 5: Teiminn notaði upplýsingum úr UVES gagnaframlögum ESO Very Large Telescope í Chile ( til að ákvarða eiginleikar stjarnanum nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5-metrar Magellan II gjörginu á Las Campanas stjörnustöðinni í Chile, HIRES gagnaframlög sem stofnast á Keck 10 metra gjörginu í Mauna Kea í Hawaii og langtíma fyrri upplýsingum úr HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6 metra stjörnustofnun ESO í Chile (söfnuð í M dwarf prófið sem X. Bonfils og M. Mayor fram ljúkaðu 2003-2010, sem upplýsingarnar eru lýst heðar sem hér á eftir).

Candidate 6: Liðið notuðu upplýsingar úr UVES mælinum á Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjarnans nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5 m Stjörnustjörnunni Magellan II í Las Campanas stjörnustöðinni í Chile, HIRES mælinu á Keck 10 m stjörnustjörnunni á Mauna Kea í Hawaii og umfangslega fyrri upplýsingar úr HARPS (High Accuracy Radial velocity Planet Searcher) í Chile (búið fram samkvæmt M-döfullskemmtun um 2003–2010 sem lýsir hér að framan) á 3,6 m stjörnustjörnunni ESO.

Candidate 7: Hópurinn notaði gögn úr UVES-gefingralisti við Very Large Telescope hjá ESO í Chile (til að ákvarða eiginleika stjarna) PFS-sáfarniðuvarðan á 6,5 m stjörnustjörnunni Magellan II í Las Campanas stjörnustöðinni í Chile, HIRES-gefingralistið á Keck 10 m stjörnustjörnunni á Mauna Kea í Hawaii og endurtekinn gögn úr HARPS (HARPS High Accuracy Radial velocity Planet Searcher) í Chile (gerin á grundvelli vísindamála gagnasafnsins X. Bonfils og M. Mayor 2003–2010 sem lýst er hér).

</details>

<details><summary>development_review #73 · A · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eea:1552

English: The analytical result shall be reported as x +/– U whereby x is the analytical result and U is the expanded measurement uncertainty, using a coverage factor of 2 which gives a level of confidence of approximately 95 % (U = 2u).

Reference (shown after audit): Greina skal frá niðurstöðum úr greiningunum sem x +/– U þar sem x er niðurstaða greiningarinnar og U er útvíkkaða mælióvissan með þekjustuðlinum 2 sem gefur 95% öryggisstig (U = 2u).

Review: Measurement uncertainty, coverage factor and confidence concepts corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Tilgreiningi á greiningartökun skal gefið upp sem x +/– U þar sem x er greiningartökunin og U er útreiknaður hættuleiki miðlunara, með 2 gagnvart, sem gefur tiltekin skyns konan 95% (U = 2u).

</details>

<details><summary>development_review #74 · t1001129 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eea:50

English: Similar studies, for at least three soil types, must be reported for all relevant metabolites, degrada tion and reaction products which in soil degradation studies account at any time for more than 10 % of the amount of active substance added.

Reference (shown after audit): Gera skal grein fyrir svipuðum rannsóknum á þremur jarðvegsgerðum hið minnsta með tilliti til allra viðkomandi umbrots-, niðurbrots- og hvarfaefna sem í rannsóknum á niðurbroti í jarðveginum nema á einhverjum tímapunkti meira en 10% af viðbættu magni virka efnisins.

Review: Soil types and metabolite/degradation/reaction concepts not retained.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Í öllum viðeigandi rannsóknum á umhverfi yfirbærs skulu greina svipaðar rannsóknir á að minnsta kosti þremur grunnföllum og vera skýrskrift á eitur- og framleiðslufyrirliggjendur sem í rannsóknum á umhverfi yfirbærs bera að minnsta kosti meira en 10% af magni virka efna sem bært er við.

</details>

<details><summary>development_review #75 · A · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:ema:1718

English: Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.

Reference (shown after audit): Gjöf edoxabans samtímis P-gp virkjanum rífampisíni leiddi til lækkunar á meðalgildi AUC fyrir edoxaban og styttri helmingunartíma, með hugsanlegri minnkun á lyfhrifum þess.

Review: Half-life and pharmacodynamic concepts mistranslated.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Samhliða nota edoxabans og P-gp aukandi rifampicins leiddi til minnkaðar meðalþéttni edoxabans AUC og skortuðum hálfdagsetningu, með væntunum um minnkun á lyfjahvörfum efnið.

</details>

<details><summary>development_review #76 · A · G8 · technical_medium · F</summary>

Source ID: p13official21:dev:ema:1406

English: Concomitant use with yellow fever vaccine and with live virus and bacterial vaccines (see section 4.5).

Reference (shown after audit): Samhliða notkun með bóluefni gegn gulusótt og bóluefni með lifandi veirum og bakteríum (sjá kafla 4.5).

Review: Yellow-fever/live-virus/bacterial vaccine meanings not jointly retained.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Notkun hefur verið samhliða með fíngrafrekjaskotvaxandi, vaxandi heilvirku og bakteríusköt (sjá kafla 4.5).

Candidate 1: Samhliða notkun með geislavirkjunum fyrir gílafræði og lífverkum og -geislum (sjá kafla 4.5).

Candidate 2: Eftirlit með sólarbruðsvefnum og lifandi virkjunum og bakteríumvigju (sjá kafla 4.5).

Candidate 3: Eftirlit með gefingu ylívægjaprófunar og lifandi virustíkum og bakteríusíkum (sjá kafla 4.5).

Candidate 4: Samhliða notkun með vaxtarfæðum frjóspöngs (yellow fever vaccine) og lifandi vírus- og bakteiravaxtar (sjá kafla 4.5).

Candidate 5: Samhliða notkun með bausarofurýn og lifandi ofnæmis og bakteríusýni (sjá kafla 4.5).

Candidate 6: Efnasamhæitt notkun með geislavirkjusýru (gulýsverkjavirkjusýru) og með lifandi verkunar og bakteríuverkunar (sjá kafla 4.5).

Candidate 7: Notkun samhliða efninum með leysi í lefsefni og lifandi vírus og skrýta leysinum (sjá kafla 4.5).

</details>

<details><summary>development_review #77 · t1001129 · G8 · technical_medium · P</summary>

Source ID: p13official21:dev:eea:1585

English: The Commission shall submit a final evaluation report at the end of the Programme.

Reference (shown after audit): Framkvæmdastjórnin skal leggja fram endanlega matskýrslu við lok áætlunarinnar.

Review: Candidate3 retains final evaluation deliverable at end of Programme.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [3]

Candidate 0: Framkvæmdastjórnin skal leggja fram endanleg matsskýrslu að lokum á aðferðinni.

Candidate 1: Framkvæmdastjórnin skal leggja fram endanleg matsskil á lok rannsóknarins.

Candidate 2: Framkvæmdastjórnin skal leggja fram endanlega matsskýrslu fyrir lok áætlunarinnar.

Candidate 3: Framkvæmdastjórnin skal leggja fram endanlega matsskil á lokum á áætluninum.

Candidate 4: Framkvæmdastjórnin skulu leggja fram endanleg matsskýrslu um áætlunina undan.

Candidate 5: Framkvæmdastjórnin skal lagða fram endanlegar matsskýrslu á lok Programmanons.

Candidate 6: Framkvæmdastjórnin skal lagða fram endanlegan matsskýrslu fyrir lok áætlunarinnar.

Candidate 7: Framkvæmdastjórnin skal leggja fram endanlegar matsskjölin á lok samstarfsins.

</details>

<details><summary>development_review #78 · t1001129 · G8 · technical_short · U</summary>

Source ID: p13official21:dev:eea:2037

English: Those criteria should not be considered to be exhaustive.

Reference (shown after audit): Þessar viðmiðanir skulu ekki teljast tæmandi.

Review: Exhaustiveness changed to sufficiency/perfection; cannot certify intended meaning.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þessara viðmiðanir skulu ekki teljast fullnægjandi.

Candidate 1: Þessi viðmiðanir skulu ekki teljast vera upplauslegar.

Candidate 2: Þessum viðmiðunum ber að hafa ekki fullnægjandi.

Candidate 3: Ekki skal telja þessi viðmiðanir fullnægjandi.

Candidate 4: Ekki skal telja þessar viðmiðanir fullkomnir.

Candidate 5: Ekki skal telja að þessum viðmiðunum sé ekki fullnægjandi.

Candidate 6: Sem skilgreiningunum skulu ekki teljast fullkomnir.

Candidate 7: Ekki skulu tekið mið af þessum viðmiðunum.

</details>

<details><summary>development_review #79 · A · greedy · technical_short · P</summary>

Source ID: p13official21:dev:ema:2013

English: There is no evidence to suggest that eptotermin alfa alters fertility.

Reference (shown after audit): Ekkert bendir til þess að eptotermin alfa hafi áhrif á frjósemi.

Review: No evidence of drug effect on fertility retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Engin sönnun tilbyrðir að eptotermin alfa hafi áhrif á frjósemi.

</details>

<details><summary>development_review #80 · t2000188 · greedy · general · F</summary>

Source ID: p13official21:dev:opensubtitles:480

English: Now we have enough evidence to charge you with murder.

Reference (shown after audit): Við höfum næg sönnunargögn til að ákæra ykkur fyrir morð.

Review: Charging with murder replaced by writing about murder.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Nú hafa við nægilega sönnunargögn til að skrifa þig um morð.

</details>

<details><summary>development_review #81 · t1001129 · greedy · technical_short · U</summary>

Source ID: p13official21:dev:ema:1100

English: If you miss a dose, take your next dose as scheduled.

Reference (shown after audit): Ef þú gleymir skammti skaltu taka næsta skammt eins og venjulega.

Review: Next dose retained but schedule phrase unreliable.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef þú missti skammt, taktu næsta skammt eins og áður hafin verið.

</details>

<details><summary>development_review #82 · t1001129 · greedy · technical_long · U</summary>

Source ID: p13official21:dev:eea:1194

English: It should provide the Commission and the Member States with objective, reliable and comparable information and data on maritime safety and on ship pollution prevention to enable them to take any necessary initiatives to enhance the measures in place and to evaluate their effectiveness.

Reference (shown after audit): Henni ber að sjá framkvæmdastjórninni og aðildarríkjunum fyrir hlutlægum, áreiðanlegum og sambærilegum upplýsingum og gögnum um siglingaöryggi og varnir gegn mengun frá skipum til að gera þeim kleift að vinna hvers kyns nauðsynleg framtaksverkefni til að efla þær ráðstafanir sem gerðar hafa verið og að meta skilvirkni þeirra.

Review: Broad maritime information/prevention purpose recognizable; technical fidelity uncertain.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Hún skal veita framkvæmdastjórnin og aðildarríkjunum marktækur, áreiðanlega og samanburðarræða upplýsingar og gögnum um öryggis á sjávarbifreiðum og um að forðast losun skipa til að þau geti tekið nauðsynlegar aðgerðir til að auka ráðstafanir sem eru í gildi og metast hvernig áhrif þeirra voru.

</details>

<details><summary>development_review #83 · A · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eso:323

English: They were able to make the sharpest direct observation ever , of the centre of a distant galaxy, the bright quasar 3C 279, which contains a supermassive black hole with a mass about one billion times that of the Sun, and is so far from Earth that its light has taken more than 5 billion years to reach us.

Reference (shown after audit): Þannig tókst þeim að gera skörpustu beinu mælingarnar sem gerðar hafa verið á miðju fjarlægrar vetrarbrautar, bjarta dulstirninu 3C 279 sem geymir risasvarthol sem er eins milljarðs sinnum massameira en sólin og er svo langt frá jörðinni að ljós þess er 5 milljarða ára að berast til okkar.

Review: Galaxy/black hole and billion-year values corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þau gafu fyrst skilvirkri, óskarlegri grein á miði langt fjölskyldu, 3C 279, sem er mjög ljósandi og inniheldur sterkum, óhægum hvitfjöllum, sem eru um um milljóna milljóna sinnum stærri en Solinn og er svo frá Jörðu að ljósið hennar hefur takað morgun meira en 5 milljóna ára til okkar.

</details>

<details><summary>development_review #84 · t1001129 · G8 · technical_medium · F</summary>

Source ID: p13official21:dev:eea:85

English: For the estimation of these concentrations all relevant information on the plant protection product and on the active substance must be taken into account.

Reference (shown after audit): Við mat á framangreindum styrk ber að taka allar viðeigandi upplýsingar um plöntuvarnarefnið og virka efnið til greina.

Review: Plant-protection product consistently omitted or replaced by unrelated terms.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Til að áætla þessi þéttni skulu taka til greina allar viðeigandi upplýsingar um vörlunarbóta og virka efninu.

Candidate 1: Við mat á þessum þéttni skulu taka yfir allar þar til viðeigandi upplýsingar um vörnplástik og virka efninu.

Candidate 2: Ef um er að ræða þessa styrk, skal taka allar viðeigandi upplýsingar um vörnplant aðila og virka efnið til tillits.

Candidate 3: Vegna matar á þessum þéttni skal taka tillit til alls viðeigandi upplýsinga um framhalds- lyfið og virka efnisins.

Candidate 4: Við mat á þessum þéttni skulu athugast allar viðeigandi upplýsingar um vænt vörnafæð og virka efnið.

Candidate 5: Vegna matar á þessum þéttni skulu taka tillit til allra viðeigandi upplýsinga um vörn vetrarlyfsins og virka efnisins.

Candidate 6: Við mat á þessum þéttni skulu taka neyslu til allra viðeigandi upplýsinga um vörnplantunn og virka efninu.

Candidate 7: Ef mat er gerð á þessum þéttni þarf að fylla í ljós öll viðeigandi upplýsingar um vörnarefnið og virka efninu.

</details>

<details><summary>development_review #85 · t2000188 · greedy · general · P</summary>

Source ID: p13official21:dev:opensubtitles:3209

English: Because it's not safe there.

Reference (shown after audit): Af því að það er ekki öruggt.

Review: Unsafe there retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Þar er ekki öruggur.

</details>

<details><summary>development_review #86 · t2000188 · greedy · general · P</summary>

Source ID: p13official21:dev:opensubtitles:1169

English: They're pretty as can be, aren't they?

Reference (shown after audit): Fallegri er ekki hægt að vera, ekki satt?

Review: Very pretty/cute plus tag question retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Þær eru mjög sæt, ekki satt?

</details>

<details><summary>development_review #87 · t1001129 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:ema:1718

English: Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.

Reference (shown after audit): Gjöf edoxabans samtímis P-gp virkjanum rífampisíni leiddi til lækkunar á meðalgildi AUC fyrir edoxaban og styttri helmingunartíma, með hugsanlegri minnkun á lyfhrifum þess.

Review: Half-life becomes half-blocking and pharmacodynamic term wrong.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Samhliða lyfjagjöf edoxabans og rifampicins, P-gp auðveldara, leiddi til minnkaðrar meðal AUC fyrir edoxaban og skerta hálfblokkun, sem getur valdið minnkaðum lyfjahvarfaáhrifum.

</details>

<details><summary>development_review #88 · t1001129 · G8 · technical_short · U</summary>

Source ID: p13official21:dev:eea:1461

English: All industrial uses of gas are considered.

Reference (shown after audit): Öll notkun á gasi í atvinnurekstri er talin með.

Review: Gas work-use recognizable but industrial scope uncertain.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Í öllum atvinnuefnum er athugað að notkun gasa.

Candidate 1: Í allum vinnuflokkum er athugað.

Candidate 2: Heimildir allra seint með gasi.

Candidate 3: Allar vinnunarnotkun gasins er íhugað.

Candidate 4: Hverjum starfsemi ásamt stofnunartengdum notkunum er tekið tillit.

Candidate 5: Taka er með öll úðað svið í vetrarbréfum.

Candidate 6: Ráðlagt er að taka til allra gjöfnefndar notkunar á gasi.

Candidate 7: Ráðið er um allar vinnuveitirnoti gas.

</details>

<details><summary>development_review #89 · A · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eea:1216

English: That task shall be coordinated with the existing regional cooperation programmes and shall include, where appropriate, the organisation of relevant training activities.

Reference (shown after audit): Samræma skal það verkefni svæðisbundnum samstarfsáætlunum sem eru fyrir hendi og skal það fela í sér, eftir því sem við á, skipulag viðeigandi þjálfunar.

Review: Regional cooperation programmes replaced by operators; training organisation lost.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þessi vinnu skal samræmt við þá rekstraraðilar sem eru í gildi og skal hún taka til þess að stjórna viðeigandi kennsluefnagreiningar.

</details>

<details><summary>development_review #90 · t1001129 · greedy · technical_short · U</summary>

Source ID: p13official21:dev:eea:1461

English: All industrial uses of gas are considered.

Reference (shown after audit): Öll notkun á gasi í atvinnurekstri er talin með.

Review: Gas use retained but industrial scope/quantification uncertain.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Í allum vinnuþjónustum er tekið tillit til notkunar gasa.

</details>

<details><summary>development_review #91 · t2000188 · G8 · technical_medium · P</summary>

Source ID: p13official21:dev:eea:1914

English: This Regulation shall enter into force on the third day following that of its publication in the Official Journal of the European Union.

Reference (shown after audit): Reglugerð þessi öðlast gildi á þriðja degi eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.

Review: Candidate5 preserves third-day entry into force after Official Journal publication.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [5]

Candidate 0: Reglugerð þessi öðlast gildi fyrri daginn eftir að hún er birt í Stjórnartíðindum Evrópusambandsins.

Candidate 1: Reglugerð þessi öðlast gildi síðar á þriðju degi eftir birtu henni í Stjórnartíðindum Evrópusambandsins.

Candidate 2: Reglugerð þessi öðlast gildi þriðja daga eftir birtu hún í Stjórnartíðindum Evrópusambandsins.

Candidate 3: Reglugerð þessi öðlast gildi þriðju degi eftir framaki hennar í Stjórnartíðindum Evrópusambandsins.

Candidate 4: Reglugerð þessi öðlast gildi þriðju degi eftir að hún er birtir í Stjórnartíðindum Evrópusambandsins.

Candidate 5: Reglugerð þessi öðlast gildi þriðju degi eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.

Candidate 6: Reglugerð þessi öðlast gildi fyrri daginn eftir að hún breytti í Stjórnartíðindum Evrópusambandsins.

Candidate 7: Reglugerð þessi öðlast gildi þriggja daga eftir talið fyrstu dag útgefnar hennar í Stjórnartíðindum Evrópusambandsins.

</details>

<details><summary>development_review #92 · A · greedy · technical_short · F</summary>

Source ID: p13official21:dev:eso:491

English: ALMA can observe in different frequency bands.

Reference (shown after audit): ALMA getur gert mælingar á mismunandi böndum.

Review: Different frequency bands not retained.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: ALMA getur fylgt á mismunandi framsöfnum.

</details>

<details><summary>development_review #93 · t2000188 · G8 · technical_medium · F</summary>

Source ID: p13official21:dev:eso:70

English: This is only the sixth of these huge storms to be spotted since 1876.

Reference (shown after audit): Stormurinn er sá sjötti sem menn verða vitni að á Satúrnusi frá árinu 1876.

Review: Storm or sixth count mistranslated in every candidate.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þetta er aðeins sjötta af þessum stórum andrúm sem koma fram síðan 1876.

Candidate 1: Þetta er bara sjöstyrmið í þessu stórum stormi sem hafa komið fram síðan 1876.

Candidate 2: Þetta er aðeins sjö af þessu mikilri stormi sem hafa komið fram síðan 1876.

Candidate 3: Þetta er aðeins sjöstyrtingur þessum miklu stormi sem fékkst síðan árið 1876.

Candidate 4: Þetta er einungis sjötta þessara og eigi alvarlega sköstur sem sýndast síðan 1876.

Candidate 5: Þetta er aðeins sjökthugur af þessum stórum stormi sem fengist hefur sjá um það frá árinu 1876.

Candidate 6: Þetta er aðeins sjötta þessi miklir slímhærnir sem heyra síðan 1876.

Candidate 7: Þetta er aðeins sex af þessum umtalsverðum tæki sem séstist eftir árið 1876.

</details>

<details><summary>development_review #94 · t1001129 · G8 · technical_short · P</summary>

Source ID: p13official21:dev:ema:1192

English: It is used to prevent pregnancy.

Reference (shown after audit): Lyfið er notað til að koma í veg fyrir þungun.

Review: Candidate7 correctly expresses use to prevent pregnancy.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [7]

Candidate 0: Hún er notað til að koma fyrir barnshafa.

Candidate 1: Hún er notað til að koma fyrir þungun.

Candidate 2: Það er notað til að útiloka þungun.

Candidate 3: Hún er notað til að koma í frambu um þungun.

Candidate 4: Hún er notað til að koma til bráðabara fæðingar.

Candidate 5: Það er notað til að forðast þungun.

Candidate 6: Það er notað til að koma fyrir þungun.

Candidate 7: Hún er notað að koma í veg fyrir þungun.

</details>

<details><summary>development_review #95 · t1001129 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eea:534

English: Council Directive 74/60/EEC of 17 December 1973 on the approximation of the laws of the Member States relating to the interior fittings of motor vehicles.

Reference (shown after audit): Tilskipun ráðsins 74/60/EBE frá 17. desember 1973 um samræmingu laga aðildarríkjanna varðandi innréttingar vélknúinna ökutækja.

Review: Interior fittings rendered as interior phenomena.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Tilskipun ráðsins 74/60/EBE frá 17. desember 1973 um samræmingu lögjaðra aðildarríkjanna varðandi innri fyrirbæri ökutækja.

</details>

<details><summary>development_review #96 · t2000188 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eea:281

English: The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.

Reference (shown after audit): Fjárhæð þeirra fyrrnefndu (síðarnefndu) sem eru jafnaðar á móti þeim síðarnefndu (fyrrnefndu) í tilteknum binditímaflokki skal teljast jafnaðar stöður þess flokks en eftirstöðvar langra eða stuttra staðna telst ójöfnuð staða þess flokks.

Review: Maturity-band financial concept garbled.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það skammtur af fyrri (sá eftirfarandi) sem samræmi við síðari (fyrri) er náður á tilteknum fulltrúaþöldum skal vera samræmd staðstöður í þeim þöldum, en eftirfarandi langa eða stuttu staðstöður skulu vera ósamræmd staðstöður í sama þöldum.

</details>

<details><summary>development_review #97 · t1001129 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eso:501

English: The team used data from the UVES spectrograph on ESOs Very Large Telescope in Chile (to determine the properties of the star accurately), the Carnegie Planet Finder Spectrograph (PFS) at the 6.5-metre Magellan II Telescope at the Las Campanas Observatory in Chile, the HIRES spectrograph mounted on the Keck 10-metre telescope on Mauna Kea, Hawaii as well as extensive previous data from HARPS (the High Accuracy Radial velocity Planet Searcher) at ESOs 3.6-metre telescope in Chile (gathered through the M dwarf programme led by X. Bonfils and M. Mayor 2003–2010 described here).

Reference (shown after audit): Hópurinn notaði gögn frá UVES litrófsritanum á Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjörnunnar nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5 metra Magellan II sjónaukanum í Las Campanas stjörnustöðinni í Chile, HIRES litrófsritann á 10 metra Keck sjónaukanum á Mauna Kea á Hawaii sem og eldri gögn frá HARPS litrófsritanum (High Accuracy Radial velocity Planet Searcher) á 3,6 metra sjónauka ESO í Chile (aflað í M dwarf verkefninu undir forystu X. Bonfils og M. Mayor milli áranna 2003-2010 sem lýst er hér).

Review: Instrument types/programme provenance corrupted in all candidates.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Hópan notuðu gagnasafnanum UVES á Very Large Telescope við ESO í Chile (að því er varðar að ákvarða eiginleika stjarnanna betur), Carnegie Planet Finder Spectrograph (PFS) á Magellan II 6,5 metra stjörnustjörnunni í Las Campanas stjörnustöð í Chile, HIRES gagnasafnið í Keck 10 metra stjörnustjörnunni í Mauna Kea í Hawaii ásamt fyrri gagnasafnið við HARPS (High Accuracy Radial velocity Planet Searcher) sem ESO fer á 3,6 metra stjörnustjörnunni í Chile (lögð á með M dwarf (Björtun og hentugleiki stjarna) árangurskipu X. Bonfils og M. Mayor 2003-2010 sem lýst er hér).

Candidate 1: Hópan notuðu gögn úr UVES röntgendýra ESO Very Large Telescope í Chile (um að ákvarða eiginleikar stjarnanna) Carnegie Planet Finder Spectrograph (PFS) á 6,5 m mestri Magellan II rannsóknarstjörnin á Las Campanas stjörnustöð í Chile, HIRES röntgendýr sem er á Keck 10 m mestri stjörnustjörnunni á Mauna Kea í Oíavíti sem og umfangsmikil leiðtöl frá HARPS (Höfdingstalgreyddir rannsóknarstjörnunni um að fá aðferðar til að finna hreyfanleika kring starra) á 3,6 m mestri stjörnustjörnunni á Chile (efnaheppni fyrri upplýsingar greint af X. Bonfils og M. Mayor 2003-2010 sem lýst er hér fyrir sig á grundvelli M-dwarfkerfisins).

Candidate 2: Hópurin notuði gögn úr UVES-gefni ESO Very Large Telescope í Chile (að ákvarða eiginleikar stjarna á betur burtu) fyrir Carnegie Planet Finder Spectrograph (PFS) á 6,5 m Magellan II-teglsinu á Las Campanas stjörnustöðinni í Chile, HIRES gagnaútreikningarkerfið á Keck 10 m-tekslunni á Mauna Kea í Hawaii, og umfangsmælum áður gagna úr HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6 m-tegslunni ESO í Chile (hér sem koma í ljós í M-dýrvísi sem stóð fram á X. Bonfils og M. Mayor 2003–2010 sem lýst er hér).

Candidate 3: Hópan notuðu það gögn frá UVES mæliskjálfinu ESO Very Large Telescope í Chile (til að ákvarða eiginleika stjarna á öruggu grundvelli), Carnegie Planet Finder Spectrograph (PFS) á 6,5-þátti Magellan II-teglsins í Las Campanas stjörnustöðinni í Chile, HIRES mæliskjálfinu á Keck 10-þátt teglunni á Mauna Kea í Hawaii, og endurtekna g öllum upplýsingunum frá HARPS (High Accuracy Radial Velocity Planet Searcher), með það 3,6-þátt teglunni í Chile (samsett í M-dýra-áætluninni X. Bonfils og M. Mayor 2003-2010 sem lýst er hér upp).

Candidate 4: Líffærið notaði gagna frá UVES skýrafyrirvísunum á Very Large Telescope (VLTI) ESO í Chile (til að ákvarða eiginleika stjarna á betur marki) fyrir PFS (Planet Finder Spectrograph) af Carnegie Institute í Las Campanas stjörnustöðvinni í Chile, HIRES skýrafyrirvísun um Keck 10 mælismálum að Mauna Kea í Hawaii og ofar aðalmerki úr fyrri reikningar á HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6 metra skýra við Hesperus (leda X. Bonfils og M. Mayor 2003–2010) sem lýst er hér.

Candidate 5: Sólarstjörnufræðingarinnar notaði upplýsingar úr UVES glæpamælisins ESOs Very Large Telescope í Chile (að því er varðar að ákvarða eiginleika stjarna), Carnegie Planet Finder Spectrograph (PFS) á 6,5-metrum Magellan II glæpamælisins í Las Campanas stjörnustöð í Chile, HIRES glæpamælisins sem er á Keck 10-metrar stjörnustjörnunni á Mauna Kea í Hawaii og jafnvel villustu upplýsingar úr HARPS (High Accuracy Radial velocity Planet Searcher), eftir að framhaldið var í 3,6-metrar stjörnustjörnunni ESO í Chile (engin til greina var að fá upplýsingar um sárstjörnurnar, sem framhaldið var í M-dýr með X. Bonfils og M. Mayor 2003-2010, sem lýst er hér).

Candidate 6: Hópan skrefið út úr geimskipum UVES (Very Large Telescope) í Chile, sem ESO er, (um að ákvarða eiginleikum stjarnannar eftir sér), geimskipu Carnegie Planet Finder Spectrograph (PFS) á 6,5-metrar Magellan II geimskipi í Las Campanas stjörnustöð í Chile, geimskipu HIRES á Keck 10-metrar geimskapi í Mauna Kea í Hawaii, ásamt umfangsgrunnum fyrri upplýsingum um HARPS (High Accuracy Radial velocity Planet Searcher) í Chile í 3,6-metrar geimskapi ESOs (skráðar um hlutaðar af upplýsingum frá stjörnurfjöldustarfsemi X. Bonfils og M. Mayor 2003-2010 sem lýst er hér).

Candidate 7: Hópurinn notaði gögnum úr UVES myndavisti við Very Large Telescope ESO í Chile (að ákvarða eiginleikar stjarna á nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) í Magellan II 6,5 m stjörnutegundarmyndavistann í Las Campanas stjörnustöð í Chile, HIRES myndavistann á Keck 10 m stjörnutegundarmyndavistann í Mauna Kea á Hawaii og aðrar vists stjórnir úr HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6 m stjörnutegundarmyndavistann ESO í Chile (vist hefur verið saman með M-lyndumprojíktímamálum X. Bonfils og M. Mayor 2003-2010 sem lýst er hér).

</details>

<details><summary>development_review #98 · t2000188 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eea:1216

English: That task shall be coordinated with the existing regional cooperation programmes and shall include, where appropriate, the organisation of relevant training activities.

Reference (shown after audit): Samræma skal það verkefni svæðisbundnum samstarfsáætlunum sem eru fyrir hendi og skal það fela í sér, eftir því sem við á, skipulag viðeigandi þjálfunar.

Review: Regional cooperation programmes and training activities not retained.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þessi verkefni skal samræma við tilstaðarregjastöðvar og skal það taka tillit til viðeigandi starfsmeðferðar á því máli sem viðkomandi verkefnið hefur í för með sér.

</details>

<details><summary>development_review #99 · t1001129 · greedy · technical_short · P</summary>

Source ID: p13official21:dev:eso:768

English: Both components are classed as O-type stars.

Reference (shown after audit): Báðar stjörnurnar eru af O-gerð.

Review: Both components classed as O stars retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Bæði hluta eru skilgreindar sem O- stjörnur.

</details>

<details><summary>development_review #100 · A · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eso:501

English: The team used data from the UVES spectrograph on ESOs Very Large Telescope in Chile (to determine the properties of the star accurately), the Carnegie Planet Finder Spectrograph (PFS) at the 6.5-metre Magellan II Telescope at the Las Campanas Observatory in Chile, the HIRES spectrograph mounted on the Keck 10-metre telescope on Mauna Kea, Hawaii as well as extensive previous data from HARPS (the High Accuracy Radial velocity Planet Searcher) at ESOs 3.6-metre telescope in Chile (gathered through the M dwarf programme led by X. Bonfils and M. Mayor 2003–2010 described here).

Reference (shown after audit): Hópurinn notaði gögn frá UVES litrófsritanum á Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjörnunnar nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5 metra Magellan II sjónaukanum í Las Campanas stjörnustöðinni í Chile, HIRES litrófsritann á 10 metra Keck sjónaukanum á Mauna Kea á Hawaii sem og eldri gögn frá HARPS litrófsritanum (High Accuracy Radial velocity Planet Searcher) á 3,6 metra sjónauka ESO í Chile (aflað í M dwarf verkefninu undir forystu X. Bonfils og M. Mayor milli áranna 2003-2010 sem lýst er hér).

Review: Instrument,observatory and programme facts corrupted throughout.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Tímabilið notuðu gögn frá UVES tímamæla upplýsingaskipti ESO-skírteinið í Chile (til að ákvarða einkenni stjarnans nálægt) Carnegie Planet Finder Spectrograph (PFS) á 6,5-metri, Magellan II-teknalaustu á Las Campanas-ögrunarvarð í Chile, HIRES tímamæla upplýsingaskipti sem fylgir Keck 10-meteru teknala við Mauna Kea, Hawaii, og áframleg skráð gagni frá HARPS (High Accuracy Radial Velocity Planet Searcher) við ESO-teknala við 3,6 metri í Chile (þar sem gagnan er fylgt samkvæmt aðferð með X. Bonfils og M. Mayor 2003-2010 sem lýst er hér) .

Candidate 1: Töflunin notaði gögn frá gluggamælistofnun Stefni í Vélta (UVES) á íslensku Véltaástæðinu (þar sem stæðir eru á því að meta eiginleika stjarnananna) og gluggamælistaftur, Planet Finder Spectrograph (PFS) á 6,5 metra við Mauna Kea á Las Campanas áhlutdeildinu í Chile, gluggamælistænum á kekktu 10 metra teigu í Keck 10 metra teigu í Mauna Kea, Hawaii eins og hæfur magnkunnugjörurfyrirtæki, HARPS, (High Accuracy Radial velocity Planet Searcher) í ESO 3,6 metra teigu í Chile (fyrir uppáhrifa á M-dýranefnd með X. Bonfils og M. Mayor 2003–2010 sem lýst er hér).

Candidate 2: Týnin nytist gagni frá UVES stelptónum í Vistvörunum í Vistvörunarhald ESO í Chile (til að ákvarða eiginleika stjórnsýsanna á réttri háttur) stelptónu Carnegie Planet Finder Spectrograph (PFS) á 6,5 m á Magellan II á optíkasið í Las Campanas hald í Chile, stelptónu HIRES á Keck 10 m á hæstupetill á Maúna Kea í Hawaii, og öðrum merkilegar gagna frá HARPS (High Accuracy Radial velocity Planet Searcher) á Vistvörunum í Chile (gruðuð í tveimur stundum af m. dwarfsæfnum sem leidist af X. Bonfils og M. Mayor 2003 - 2010, sem lýst er hér) í sömu málsgrunni og um bergt gagninn í því skyni að segja líkur á áður.

Candidate 3: Töflunin notaði gagnkvæma gögn frá UVES spjaldgreiðslu þann ESO Véltra mikilvægur teínu í Chile (til ákvarða eiginleika steins á miklu nálægis hátt), Carnegie Planet Finder Spectrograph (PFS) í 6,5 m teíni á Las Campanas-áæð í Chile, HIRES spjaldgreiðslu sem var sett á Keck 10 m teíni á Mauna Kea í Hawaii, og endurteknum gagnum frá HARPS (High Accuracy Radial velocity Planet Searcher) í ESO 3,6 m teíni í Chile (hafnað í M dwarfið í vektli frá X. Bonfils og M. Mayor 2003 - 2010 sem lýst er hér) .

Candidate 4: Faraðilinn notuði gagna frá UVES skýrsluskýrslunni ESOs stóra tækniskjá í Chile (til að ákvarða eiginleika stjarnunnar með áreiðanlega nákvæmni) á Carnegie Planet Finder Spectrograph (PFS) á 6,5 m tækniskýrslun í 2. ikur Magellan II tækniskýrslun í Las Campanas astríðstöð í Chile, á HIRES skýrsluskýrslunni, sem er sett á Keck 10 m tækniskýrslun í Mauna Kea í Hawaii, og ofaneska fyrri gagn frá HARPS (High Accuracy Radial Velocity Planet Searcher) á 3,6 m tækniskýrslun í ESOs í Chile og þessu varðandi M-dýraiðferð (x. Bonfils og M. Mayor 2003-2010 sem lýst er hér) sem er samanburði á með X. Bonfils og M. Mayor.

Candidate 5: Fjölgaður náði að gæta gagna úr UVES ræktunarmiðli í ESO-ótutækinum í Chile (til að ákvarða eiginleika stjarnananna verulega nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5 m magellan-II-tektúlúmi í Las Campanas-æði í Chile, Hires ræktunarmiðli ímaðu 10 m að mánuði á Keck-tektúlúmi í Mauna Kea í Hawaii, og fyrir því öllum fyrrfelltum gagna úr HARPS (Høyri, áhættuþættun ringralyfsstjarna hreinandi) í 3,6 m ræktunarmiðli í ESO-ótutækinu í Chile (tryggt í meðaðafurðinni sem stjórnar X. Bonfils og M. Mayor 2003-2010, sem lýst er eftir hér á).

Candidate 6: Félögurinn notaði gagnir frá UVES skýrunarhlutvissunarmál ESO-ótastæðunnar í Chile (til að ákvarða eignir stjórnsætans skilgreind í nokkurra mæli) skýrunárnar Carnegie Planet Finder (PFS) á 6,5 m á Magellan II ótaumurum í Las Campanas-æði í Chile, skýrunarhlutvissunarmalana HIRES á Keck 10 m ótaumum á Mauna Kea í Hawaii, eins og umfjölgjarnar gagnir frá HARPS (hæsta nýtt áhættugæði til ásetningar um hlutabliuðustjórna) á ótaumum í Chile (skráð með meðaltalinni M-klátursáttmálamálinni X. Bonfils og M. Mayor 2003–2010 sem er lýst hér).

Candidate 7: Félöginn notaði gögn úr UVES-gefni útbreytingaskrá rannsóknarskynissjónar á stjörnu í ESO-órásarrannsóknarsjónina í Chili (að því tilvísun hlutaðeigandi stjórnsins), Carnegie Planet Finder Spectrograph (PFS) í 6,5-métrikerum Magellan II rannsóknarsjón í Las Campanas-áætlun í Chili, HIRES gefni í telescopia eins og Keck í 10 metrikerum í Mauna Kea í Hawaii og í megin upphafið gagn vísu á HARP-gefni (myndandi fyrir líftryggingu á stjórnu) í ESO-órásarrannsóknarsjón í Chili (gerð með aflskírteini frá 2003 til 2010 sem gefið er af X. Bonfils og M. Mayor, sem leittir í hliði á, sem lýst er hér á).

</details>

<details><summary>development_review #101 · A · G8 · technical_short · F</summary>

Source ID: p13official21:dev:eea:922

English: Development of CPE is checked as described in Part I.III.4.

Reference (shown after audit): Fylgst er með því hvort frumuskemmdir verða eins og lýst er í I.III.4.

Review: Checking development of CPE and exact reference not jointly retained.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Tilgreiningar á þróun CPE eru hægt að kanna í samræmi við þær sem lýst er í IV. mgr. I. þjóðaþáttar I. hluta.

Candidate 1: Rannsókn í stöðluðu fínunni hentast við þann sem skétur er á í I. III.4 lið.

Candidate 2: Frekari hliðsjón varðar þróun CPE í samræmi við I. hliða III. þaðalins.

Candidate 3: Hannað af þróun CPE er lausn því sem lýst er í 4. lið III. hluta I. þátt.

Candidate 4: Rannsóknarhæfi CPE er endurskoðuð eins og lýst er í lið 4 í III. hópi I. þættisins.

Candidate 5: Meðhöndlað er þróun CPE eins og fram kemur í IV. lið I. hluta I. þátt.

Candidate 6: Hundraðseymnisýkið er öryggist að ákvarðað er eins og lýst er í kafla III.4 í I. hluta.

Candidate 7: Viðurkenningu er fram kemur á þróun CPE eins og lýst er í stað III.4 í I. hluta.

</details>

<details><summary>development_review #102 · t2000188 · greedy · technical_short · F</summary>

Source ID: p13official21:dev:eso:491

English: ALMA can observe in different frequency bands.

Reference (shown after audit): ALMA getur gert mælingar á mismunandi böndum.

Review: Frequency bands replaced by two quantities.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: ALMA getur fylgst með breytum á milli tveggja fjölda.

</details>

<details><summary>development_review #103 · t1001129 · G8 · technical_short · F</summary>

Source ID: p13official21:dev:eso:491

English: ALMA can observe in different frequency bands.

Reference (shown after audit): ALMA getur gert mælingar á mismunandi böndum.

Review: No candidate preserves frequency-band observation.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: ALMA getur athugað á skuggum í mismunandi fjarskiptavíssum.

Candidate 1: ALMA getur fylgst með framhaldsborði að skuggu sem skiptast undir öðrum fjölda hópurar.

Candidate 2: ALMA getur fylgst með milliverkunum í mismunandi framanum.

Candidate 3: ALMA getur fylgst með differentum segjubréfum.

Candidate 4: ALMA bendir til að mæla á annarra bóndum.

Candidate 5: ALMA getur fylgt eftir útborf á mismunandi röntingahópi.

Candidate 6: ALMA getur fylgt eftir bólgum í annarri umfangi.

Candidate 7: ALMA getur fylgst með bókningum á mismunandi viðtakum.

</details>

<details><summary>development_review #104 · t2000188 · greedy · technical_medium · U</summary>

Source ID: p13official21:dev:ema:1718

English: Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.

Reference (shown after audit): Gjöf edoxabans samtímis P-gp virkjanum rífampisíni leiddi til lækkunar á meðalgildi AUC fyrir edoxaban og styttri helmingunartíma, með hugsanlegri minnkun á lyfhrifum þess.

Review: AUC/half-life/effects partly retained; P-gp inducer role and malformed mean term uncertain.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Samtímis gjöf edoxabans og P-gp örvaðs rífampicins leiddi til minnkaðrar meðaláxinháður AUC fyrir edoxaban og skemmja helmingunartíma, sem getur valdið minnkun á lyfhrifum.

</details>

<details><summary>development_review #105 · A · G8 · technical_medium · F</summary>

Source ID: p13official21:dev:ema:1582

English: The treatment-free period, however, should take into account the pharmacological properties of the products used previously.

Reference (shown after audit): Meðferðarlausa tímabilið verður þó að taka mið af lyfjafræðilegum eiginleikum lyfja sem voru notuð áður.

Review: Treatment-free period missing or replaced in every candidate.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þó skal taka tillit til lyfjafræðilegri eiginleika lyfsins sem notaður varðið fyrir innan dagsfrumurs.

Candidate 1: Heimilt er að gera fyrirhugað m.a. lyfjahvörf íferðavara sem notað hefur verið.

Candidate 2: Háverð er, þó, að teknu tillit til lyfjafræðilegu eiginleika lyfjanna sem notað var áður.

Candidate 3: Áherslaframleikið skal þó taka í bót á lyfjafræðileg eiginleikum lyfjanna sem notað hefur áður.

Candidate 4: Þó skal taka í tilliti við lyfjafræðilega eiginleika lyfja sem höfði verið notuð.

Candidate 5: Hugtakandi skal hlýturhvarf til að taka tillit til lyfjahvörfþætti lyfsins sem notaður var áður.

Candidate 6: Á meðferðsfarlegu tíma skal þó athuga lyfjafræðilega eiginleggir eiginleika lyfjanna sem notað hefur áður.

Candidate 7: Meðal megin skal taka tillit til lyfjafræðilega eiginleika efnanna sem notað eru áður.

</details>

<details><summary>development_review #106 · t2000188 · G8 · technical_long · U</summary>

Source ID: p13official21:dev:eso:775

English: A team of astronomers, led by Istvan Dékány of the Pontificia Universidad Católica de Chile, has now used data from this survey, taken between 2010 and 2014, to make a remarkable discovery - a previously unknown component of our home galaxy, the Milky Way.

Reference (shown after audit): Hópur stjörnufræðinga undir forystu Istvan Dékány við Pontificia Universidad Católica de Chile, notaði gögn úr verkefninu sem aflað var milli 2010 og 2014 og gerði merkilega uppgötvun á áður óþekktu svæði í Vetrarbrautinni okkar.

Review: Discovery/date/name partly retained; leadership and unknown Milky-Way component wording uncertain.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Hópur stjörnufræðinga, lögð undir Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notað gögnum úr sjónaukunni, sem hafa verið tekin á milli árs 2010 og 2014, til að ná til mikilvægs uppgötvunar - einstaka sem var aldrei þekkt í húðvöðvarann, milífjölinu.

Candidate 1: Hópur stjörnufræðinga hjá Pontificia Universidad Católica de Chile, Hilda Jaccard, leiddi af Istvan Dékányi, hefur nú notuð gagna af þessari skoðun, sem gerð var á milli 2010 og 2014, til tilætta óvart þess - einstök nemur fra heimakvæðinu, Vetrarbrautarinni.

Candidate 2: Hópur stjörnufræðinga, gefinn stjörnustöðvarinnar stjörnulífinu (Pontificia Universidad Católica de Chile) leitaði aftur á liðinu, sem var ekki þekkt áður, í þessum skoðun, sem tókst á milli 2010 og 2014, og fundið óvart á einhverju þess konar hlutar á sjónbúnaði okkar, Galdrarvindinu.

Candidate 3: Hópur stjörnufræðinga, leit frá Istvan Dékány, Pontificia Universidad Católica de Chile, hefur nú notað gögn úr þessari skoðun, sem tóku sér stað á tímabilið 2010-2014, til til þess á þessum svona frábæra uppgötvunum - undirrituður hlutur heimetaalans, Vetrarbrautarinnar.

Candidate 4: Hópur stjörnufræðinga, yfirhugaður Istvan Dékány hjá Pontificia Universidad Católica de Chile, hefur nú notað gögn úr þessari rannsókn, sem tekin voru á tímabilið 2010-2014, til að ná til mikiðar sönnunar - dýranauðsýni heimskyldunni, vetrarbrautarinnar.

Candidate 5: Hópur stjörnufræðinga, leitur eftir Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur notuð gögn úr slíkri skoðun, sem tóku sér stað á milli 2010 og 2014, til að gera hreint uppgötvun - einstaklega óþekktur hluti heimaláttarinnar, Vetrarbrautarinnar.

Candidate 6: Hópur stjörnufræðinga, yfirskipuð af Istvan Dékány úr Pontificia Universidad Católica de Chile, hefur náið úr þessum mælingum, sem samanstendu milli 2010 og 2014, um frávæglegan uppgötvun - aðra aldrei þekktan hluti húsvetrarhvarfanna, Vetrarbrautarinnar.

Candidate 7: Hópur stjörnufræðinga, leitt af István Dékány við Pontificia Universidad Católica de Chile, hefur nú notuð niðurstöður úr þessu rannsókn, tækt á milli 2010 og 2014, til að gera mikilvægri uppgötvun - annan hluta heimakvellsins, Vetrarbrautarinnar.

</details>

<details><summary>development_review #107 · t1001129 · G8 · technical_short · U</summary>

Source ID: p13official21:dev:eea:609

English: Special payments for shift work.

Reference (shown after audit): Sérstakar greiðslur vegna vaktavinnu.

Review: Shift-work phrase is an uncertain calque; not certified.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Sérstakar borgningar við skiptarvinnslu.

Candidate 1: Sérstakar greiðslur fyrir skiptaða vinnsla.

Candidate 2: Sérstakar greiðslur vegna skipta vinnunar.

Candidate 3: Sérstakar greiðslur til skipta.

Candidate 4: Sérstakar borgningar fyrir starfsstöðum.

Candidate 5: Sérstakar sendir fyrir starf eða van.

Candidate 6: Sérstakar borgningar við skiptir.

Candidate 7: Sérstakar ráðbætur fyrir skipta starf.

</details>

<details><summary>development_review #108 · A · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eea:534

English: Council Directive 74/60/EEC of 17 December 1973 on the approximation of the laws of the Member States relating to the interior fittings of motor vehicles.

Reference (shown after audit): Tilskipun ráðsins 74/60/EBE frá 17. desember 1973 um samræmingu laga aðildarríkjanna varðandi innréttingar vélknúinna ökutækja.

Review: Interior fittings rendered as interior companies.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Stjórnvaldiríð tilskipun 74/60/EBE frá 17. desember 1973 um samræmingu lögum aðildarríkja varðandi innri fyrirtæki ökutækis.

</details>

<details><summary>development_review #109 · A · greedy · technical_short · F</summary>

Source ID: p13official21:dev:eso:446

English: “Astronomers have waited for data like this for over a decade.

Reference (shown after audit): „Stjörnufræðingar hafa beðið eftir gögnum eins og þessum í yfir áratug.

Review: Astronomers changed to politicians.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: „Stjórnmálarnir hafa bíðið á þessu upplýsingum í meira en tíu ár.“

</details>

<details><summary>development_review #110 · A · greedy · technical_short · U</summary>

Source ID: p13official21:dev:ema:1100

English: If you miss a dose, take your next dose as scheduled.

Reference (shown after audit): Ef þú gleymir skammti skaltu taka næsta skammt eins og venjulega.

Review: Missed/next dose retained but scheduled timing reduced to as before.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef þú mistar skammt skal taka næsta skammt eins og áður.

</details>

<details><summary>development_review #111 · t1001129 · greedy · general · F</summary>

Source ID: p13official21:dev:opensubtitles:2508

English: Rose, we have a guest in the living room.

Reference (shown after audit): Rósa, það er gestur í stofunni.

Review: Guest/living room mistranslated.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Rose, við er með fæðinga í heimilisvélinu.

</details>

<details><summary>development_review #112 · A · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eso:919

English: "Thanks to several giant telescopes currently under construction, including ESOs E-ELT and the NASA/ESA/CSA James Webb Space Telescope due to launch for 2018, we will soon be able to study the atmospheric composition of these planets and to explore them first for water, then for traces of biological activity.

Reference (shown after audit): „Þökk sé nokkrum risasjónaukum sem nú eru í smíðum, þeirra á meðal E-ELT sjónauka ESO og James Webb geimsjónauka NASA; ESA og CSA sem skotið verður á loft árið 2018, munum við fljótlega geta rannsakað efnasamsetningu lofthjúpa þessara reikistjarna og kannað þær fyrst í leit að vatni og síðan leitað að merkjum um líf.

Review: Atmospheric composition and biological activity not faithfully retained.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Því að með margum stórum teklum sem eru í búnúðu og þar meðt ESO-ELT og James Webb Space Telescope frá NASA, ESO og CSA, sem ætlað er til flugfars í 2018, verðum við nánar á loftsgildi þessara heimsölva og rannsaka þau fyrst með vatn eftir því með líkamlegri virkni.

</details>

<details><summary>development_review #113 · t2000188 · greedy · technical_short · U</summary>

Source ID: p13official21:dev:eea:1461

English: All industrial uses of gas are considered.

Reference (shown after audit): Öll notkun á gasi í atvinnurekstri er talin með.

Review: Industrial/all-use scope broadened/restructured; fidelity uncertain.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Í allri starfsemi er tekið tillit til notkunar á gasi.

</details>

<details><summary>development_review #114 · A · greedy · general · F</summary>

Source ID: p13official21:dev:opensubtitles:3607

English: Well, that makes you ugly and stupid.

Reference (shown after audit): Þá ert þú ljótur og heimskur.

Review: Ugly/stupid replaced by scared/incomprehensible.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það gerir þig hrædd og óskiljanlegt.

</details>

<details><summary>development_review #115 · t1001129 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eea:281

English: The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.

Reference (shown after audit): Fjárhæð þeirra fyrrnefndu (síðarnefndu) sem eru jafnaðar á móti þeim síðarnefndu (fyrrnefndu) í tilteknum binditímaflokki skal teljast jafnaðar stöður þess flokks en eftirstöðvar langra eða stuttra staðna telst ójöfnuð staða þess flokks.

Review: Maturity and matching relationships not faithfully rendered.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Að það er varðar eða síðustu, sem staðfestur fyrst og síðasti, beruð af síðustu (efra) í tilteknu undirhöfundamál eftir skuldbindingum skal vera það undirhöfundamál sem í staðfestu, svo sem undirhöfundamál sem ekki er staðfest í sama undirhöfundamál.

Candidate 1: Hjá þeim millifikningu sem er samræmd með þeim (sem er samræmd með það) skal vera samrýmanleg staða í þeirri millifikningu, en í millið er samrýmanleg staða á sameiginlegum millið.

Candidate 2: Í það umfang sem meðalforða (eða endurforða) hafa líkað við endurforðina (í slíkt umfang sem meðalforða) skulu vera samræmd staðferðir í þeirri sveitalinu, en eftirfallin longa (eða stoppað) stöðu skal vera ósamræmd stöða í slíka sveitalinu.

Candidate 3: Það magn, sem fyrri (síðustu) er samrýmist svörunni (lýsingi) síðustu (fyrstu), á við álíkaða útanaðalhópi viðmiðunarmassa skal vera samrýmissviðin í því hópi en það eftirasta ánemiðlega aðstöðu er án samrýmisins við við álíkaða útanaðalhópi.

Candidate 4: Magn miðla (úrmiðla) sem uppsamsið er miðað við síðasta (fyrsta) í við tekið útframlag skal vera samræmd staða í því lágningarbrøðrunni, að því er varðar niðurstaðan langa eða stakna staða, sem er ekki samræmd við viðkomandi lágningarbrøðrun.

Candidate 5: Það er að vera að mismunandi hlutfall sem síðaste (fyrri) hentar síðaste (fyrri) í felldir, sem settar eru í þann gildingu, sem mismunandi staðal undir því, og hlutfall eftir (efra) sem ekki sem mistaða varðar samræmdu staða í sama gildi.

Candidate 6: Höfundur (látinn) breytis séu hana sem fyrirbæri (sá sem fyrirbæri) samantektur og færst (sá sem færst) í viðkomandi útansvarta (haldarfjölda) skal vera samantektuð staðstöður í þeirri hald, en eftirradandi langa (sá langan) eða skorta (sá skorta) staðstöður séu ósamantektuðar staðstöður í sömu hald.

Candidate 7: Akaða (nýsta) áhættu sem fylgi (sá viðfylgi) fyrir fyrsta (henni) áhættuna í þeim hringum sem fylgi er aldrei (henni) áhættu og umþolnir áhættusvörunum er þeir óviðurkenndur áhættu í samstæða hringi.

</details>

<details><summary>development_review #116 · t2000188 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:ema:1394

English: The most commonly reported adverse reactions (≥ 20%) among patients treated with both belatacept- based regimens (MI and LI) up to Year 3 are diarrhoea, anaemia, urinary tract infection, peripheral oedema, constipation, hypertension, pyrexia, nausea, graft dysfunction, cough, vomiting, leukopenia, hypophosphataemia, and headache.

Reference (shown after audit): Algengustu aukaverkanirnar (≥ 20%) hjá sjúklingum sem fengu báðar belatacept meðferðirnar (MI og LI) fram að 3. ári eru niðurgangur, blóðleysi, þvagfærasýking, bjúgur á útlimum, hægðatregða, háþrýstingur, hiti, ógleði, ófullnægjandi starfsemi græðlings, hósti, uppköst, hvítfrumnafæð, blóðfosfatskortur og höfuðverkur.

Review: Multiple adverse reactions wrong,including leukopenia replaced by platelet deficiency.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Algengustu aukaverkanirnar (≥ 20%) sem tilkynntum fyrir voru hjá sjúklingum sem fengu bertra meðferð með belatacepti til fyrstu ára (MI) eða meðferð með belatacepts við meðferð á meðferðarrekstrarvið (LI), allt til ára 3, eru niðurgangur, blóðleysi, sýking í þvagæðum, þroti í hliðslum, þrota, háþrýstingur, hægðatengda kvefingar, óvirkni þroska, hóll, uppköstur, blóðflagnafæð, blóðfosfatsfallsminnun og höfuðverkur.

Candidate 1: Algengustu aukaverkanirnar sem greint hefur verið frá (≥ 20%) hjá sjúklingum sem fengu meðferð með belatacept-bundiðum meðferðaráætlunum (MI og LI) allt að þriðja ári voru niðurgangur, blóðleysi, sjúkdómi í þvagmyndun, bólga í útlægum, tráhristlyndi, háþrýstingur, hita, ógleði, misvirkun greina, hóss, uppköst, blóðflagnafæð, blóðfosfatsþéttni og höfuðverkur.

Candidate 2: Yfirleitt tilkynntar aukaverkanir (≥ 20%) hjá sjúklingum sem hafa fengið beitaðar meðferð með belatacepti starfseminum (MI- og LI- reglum) allt að ári 3 eru niðurgangur, blóðleysi, sýking í þvagæðum, bólga í hliðstæðum, sykri, háþrýstingur, hiti, ógleði, skertur frumuríki, hóstu, uppköst, slembuæxli, blóðfosfatósíði og höfuðverkur.

Candidate 3: Algengustu aukaverkanirnar sem fram komu hjá sjúklingum á meðferð með bæði belatacept-bundnum meðferðir (MI og LI) allt að ári 3 eru niðurgangur, blóðleysi, sýking í niðurbakrúfa, bólga, trængsla, háþrýstingur, hita, ógleði, vartvirkni æðar, hósti, uppköst, blóðflagnafæð, blóðfosfatsfalli og höfuðverkur.

Candidate 4: Algengustu aukaverkanirnar sem fram komu hjá sjúklingum sem fengu bæði reglur með belatacepti (MI og LI) allt til árs 3 eru niðurgangur, blóðleysi, sýking í þvagæðum, þyngdarkerl, træstarleysi, háþrýstingur, hiti, ógleði, skerta áfengissvörun, hósta, uppköst, blóðflagnafæð, osteósarkbilsnotkun, og höfuðverkur.

Candidate 5: Algengustu aukaverkanirnar sem greint hefur verið frá hjá sjúklingum sem fengu bæði belatacept-bundið meðferð (MI- og LI-) fram að þriðja ári eru niðurgangur, blóðleysi, sýking í þvagæðum, bólga í undaneyðarbólur, hvíldur, háþrýstingur, hiti, uppköst, stökkbreytingar á æðum, hólllaga, uppköst, blóðleysi, blóðfosfatskort og höfuðverkur.

Candidate 6: Algengustu aukaverkanirnar (≥ 20%) sem greint hefur verið frá hjá sjúklingum sem fengu meðferð með belatacept-bundnum meðferðum (MI og LI) allt að þriðja ári eru niðurgangur, blóðleysi, niðurgangsvefsbólga, bólga hjá helmingum, træst, háþrýstingur, kveikjandi hiti, ógleði, misvirkun á gegnumhengsi, hólgliði, uppköst, blóðflagnafæð, blóðfosfatíðni og höfuðverkur.

Candidate 7: Algengustu aukaverkanirnar sem greint hefur verið frá hjá sjúklingum sem fengu bæði belatacept-bundna meðferð (MI og LI) allt að þriðjung og engu eftir það voru niðurgangur, blóðleysi, sýking í þvagvörvi, þéttni í umhverfi, træðarleysi, háþrýstingur, hiti, ógleði, misvirkun viðbótarræðis, hóllleysi, uppköst, hvítblóðfall, blóðfosfatsþéttni minni og höfuðverkur.

</details>

<details><summary>development_review #117 · t2000188 · G8 · technical_medium · U</summary>

Source ID: p13official21:dev:eea:698

English: Only days that can be worked should be included when Saturdays and Sundays are not worked they should not be included, the same with public holidays).

Reference (shown after audit): Eingöngu skal telja með þá daga sem unnt er að vinna (ef ekki er unnið á laugardögum og sunnudögum skal ekki telja þá með; hið sama gildir um lögboðna frídaga).

Review: Closest candidates imply worked-day rule but weekend/public-holiday wording incomplete or malformed.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Aðeins skulu tímarnar farið við sem verkar er, þó ekki tímarnar frá sástíónum og sunnudagar þegar þær eru ekki tímarnar skal ekki taka til neinar (aukeð við opinbera ferðalíka).

Candidate 1: Einungis daga sem geta verið notað má taka til að rýmini, þegar ekki er tekinn við sólarhringa og sundagum, má því ekki taka til, eins og frelsistöðvar).

Candidate 2: Aðeins daga skal taka við þegar virka er og skal ekki taka við daga sem virka ekki og þó sama við opinbera helg (public holidays).

Candidate 3: Einnig aðeins dagar sem ná ekki við að vinna eiga að fela í skýrinum, ef sára og sunnudögur eru ekki vinna skaða þeir ekki, sama við opinbera helgur).

Candidate 4: Einungis skal tölur fyrir daga sem hægt er að vinna í samanstaða rammaseiði og helgar (sunnudagur) eða helganna (freiddagur).

Candidate 5: Einnig skal taka bara dagir að auði að því er varðar að vinna, er ekki vinnt á laugardagum og sunnudagum, sýna það sú sama við opinberar helgdagana.

Candidate 6: Einungis dagar sem geta verið virkt skulu fylgt saman þegar Söndagur og sólarhringur eru ekki virkt og svo og af sömu sátti berast lausnárvinnulausn (public holidays).

Candidate 7: Aðeins þær daga skulu tekið til meðaltals þegar sólarhringar og sólarhringar eru ekki starfsemi, eins og sama við opinbera helgi).

</details>

<details><summary>development_review #118 · A · G8 · technical_medium · F</summary>

Source ID: p13official21:dev:eso:70

English: This is only the sixth of these huge storms to be spotted since 1876.

Reference (shown after audit): Stormurinn er sá sjötti sem menn verða vitni að á Satúrnusi frá árinu 1876.

Review: No candidate faithfully renders sixth huge storm since1876.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þetta er aðeins sjöturstaðar á þessum stórri stjörnum síðan 1876.

Candidate 1: Þetta er bara sjöðuð stöðugu hvarfar sem hefur komið fram í síðan árið 1876.

Candidate 2: Þetta er bara sjötissexthálfur af slíkum sæmugjörum sem fyrir eftir hafa verið stendur síðan 1876.

Candidate 3: Þetta er aðeins sjö grækkur þessum lentum Þurrningar í síðustu árið frá 1876.

Candidate 4: Þetta er einungis sjötta þessara og stóra skjólum sem hefðu verið fangin í síðan 1876.

Candidate 5: Þetta er bara sjösturgök, þessu stóra stjórna, sem hefur verið sjáð í tíðanum síðan 1876.

Candidate 6: Þetta er í eftirri sást þosstafarni úr þessum stórum streymnum síðan 1876.

Candidate 7: Þetta er aðeins sex af þessum umtækar stormi sem hafa verið tekin í gegnum tíð og þau voru tekt sem síðasti 1876.

</details>

<details><summary>development_review #119 · A · G8 · technical_short · U</summary>

Source ID: p13official21:dev:eea:1461

English: All industrial uses of gas are considered.

Reference (shown after audit): Öll notkun á gasi í atvinnurekstri er talin með.

Review: Closest gas-use candidate changes modality/scope; fidelity uncertain.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Alla notkun gerða í stofnunarmót eru í tali.

Candidate 1: Allar notkun á loftþyngjum í vinnslulegum vörufélagum eru íhugaðar.

Candidate 2: Heimilt er að taka tillit til allra notkunar lofttegunda í starfsemi.

Candidate 3: Allar vinnunarnotkun úr loftfyrirtækjum eru í ljósi.

Candidate 4: Hvaða vinnustarfsemi af ölu er tekin til.

Candidate 5: Tilgreina er allan notkun eldsneytis í fána.

Candidate 6: Allar starfsemi með ågusímum er í ljós.

Candidate 7: Allar viðskiptum í efni úr gæði eru íhugaðar.

</details>

<details><summary>development_review #120 · t1001129 · G8 · technical_medium · U</summary>

Source ID: p13official21:dev:ema:1582

English: The treatment-free period, however, should take into account the pharmacological properties of the products used previously.

Reference (shown after audit): Meðferðarlausa tímabilið verður þó að taka mið af lyfjafræðilegum eiginleikum lyfja sem voru notuð áður.

Review: Treatment-free timing is malformed or omitted in closest candidates.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Meðan á meðferðarfraslum í bólgustundinni er að ræða skulu það taka tillit til lyfjafræðilegra eiginleika lyfsins sem notuð varð áður.

Candidate 1: Að því er varðar fylgni meðferðar, skal í þar til borið vera að tekur tillit til lyfjafræðilegra eiginleika lyfinna sem notað voru áður.

Candidate 2: Hins vegar skal fylgjast með lyfjafræðilegar eiginleikum lyfja sem notað verði áður.

Candidate 3: Hins vegar skal fylgjast með lyfjafræðilegum eiginleikum lyfinna sem notuð var áður.

Candidate 4: Í meðferðarfrásjálfstöðvun skal fylgjast með lyfjafræðilegum eiginleikum lyfsins sem þegar hafist.

Candidate 5: Hins vegar ber að fylgjast með lyfjafræðilegum eiginleikum lyfinu sem voru notaðir áður.

Candidate 6: Meðan án meðferðarstöðu skal athuga lyfjaheilkenni í vöru sem notað hefur verið.

Candidate 7: Meðferðarfraslæðið, þó, ætti að ná á lyfjafræðilega eiginleikum lyfsins sem notuð hefur verið áður.

</details>

<details><summary>development_review #121 · t1001129 · greedy · general · U</summary>

Source ID: p13official21:dev:opensubtitles:3607

English: Well, that makes you ugly and stupid.

Reference (shown after audit): Þá ert þú ljótur og heimskur.

Review: Stupid retained; ugly term not reliable.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það gerir þig skamm og heimskur.

</details>

<details><summary>development_review #122 · t1001129 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eso:775

English: A team of astronomers, led by Istvan Dékány of the Pontificia Universidad Católica de Chile, has now used data from this survey, taken between 2010 and 2014, to make a remarkable discovery - a previously unknown component of our home galaxy, the Milky Way.

Reference (shown after audit): Hópur stjörnufræðinga undir forystu Istvan Dékány við Pontificia Universidad Católica de Chile, notaði gögn úr verkefninu sem aflað var milli 2010 og 2014 og gerði merkilega uppgötvun á áður óþekktu svæði í Vetrarbrautinni okkar.

Review: Leadership,discovery or unknown home-galaxy component corrupted in every candidate.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Hópur stjörnufræðinga, búa til hreyfla Istitanu Dékány, Pontificia Universidad Católica de Chile, hefur nú notað gögn úr þessari rannsókn, sem gerð var á meðal ára, frá árinu 2010 til 2014, til að gera óvartjánum, spennandi undirtreinsöfn okkar heimastjörnun, Hvarfjörðunin.

Candidate 1: Hópur stjörnufræðinga hjá Pontificia Universidad Católica de Chile, frá ledandi Istvan Dékány, hefur fyrst og fremst notað gögnum úr þessum skoðanum, sem gerð var á milli 2010 og 2014, til tilæysa sem er að enda sér – einhverja hún sem fengu ekki ofan með fætur í alheimsrýkjunni okkar, Vetrarbrautinn.

Candidate 2: Hópur stjörnufræðinga, gefnu ræðu af Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notuð gögn úr þessum rannsókn, sem gerð var á meðal árið 2010 til 2014, til smábrimirar framfæran - aðgang að aðra aldrei vitaðri hluti heimakauparinnar, Vetrarbrautinn.

Candidate 3: Hópur stjörnufræðinga, fylgjandi Istvan Dékány frá Pontificación Universidad Católica de Chile, hefur nýlega notað gögnum úr þessum mælingum, sem voru gerðar á bilinu 2010 til 2014, til að fá fram örveru sem áður hefur ekki verið þekkt - hins vegar óþekktur hlutur heimsúrsins, stjörnumyrennunar.

Candidate 4: Hópur stjörnufræðinga, fylgda Istvan Dékány hinni Pontificia Universidad Católica de Chile, hefur nú notað upplýsingum úr slíkmáli úr 2010 til 2014 til að fá undirhugsvægi - aðferð mælibila sem var eftirfaldið og á sitt heimskálafjölda, Mjög í.

Candidate 5: Hópur stjörnufræðinga, leit helstu af Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notuð upplýsingar úr þessum rannsókn, sem voru gerðar á ársframtíma 2010-2014, til hreinsa uppgjör - einhvern voru óvænlegur hlutur heimsliða, Vetrarbrautinn.

Candidate 6: Hópur stjörnufræðinga, ledin ástæða Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notað upplýsingar úr þessum samanburði, sem gerð var á bilinu 2010-2014, til að ná í það sem minna, áhugaverandi, nýskostið í heimstjörnunni okkar, Mjólkurhúðinni.

Candidate 7: Hópur stjörnufræðinga, leitt af István Dékány af Pontificia Universidad Católica de Chile, hefur þegar notið gögnum úr þessari rannsóknum, sem voru gerðar á bilinu 2010 til 2014, til vistskilyrðisstöðugri upplýsinga – þessari undirhópi um heimastjörnuna, Mjólkurvægið.

</details>

<details><summary>development_review #123 · t2000188 · greedy · technical_short · P</summary>

Source ID: p13official21:dev:ema:2013

English: There is no evidence to suggest that eptotermin alfa alters fertility.

Reference (shown after audit): Ekkert bendir til þess að eptotermin alfa hafi áhrif á frjósemi.

Review: No evidence drug alters fertility retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Ekki er einhverja sönnunargögn til að benda til þess að eptotermin alfa hafi áhrif á frjósemi.

</details>

<details><summary>development_review #124 · A · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eso:924

English: ESO was delighted to welcome Italys Minister of Education, Universities and Research, H.E. Stefania Giannini, to the ceremony, which was also attended by the Italian Consul General in Munich, Renato Cianfarani, the ESO Council President, Patrick Roche, and the Italian ESO Council Delegates, Nicolò DAmico (who is also President of INAF) and Matteo Pardo, Scientific Attaché at the Italian Embassy in Berlin.

Reference (shown after audit): Viðstödd undirritunina voru H.E. Stefania Giannini, mennta- og vísindamálaráðherra Ítalíu, ítalski konsúllinn í München, Renato Cianfarani; Patrick Roche, forseti ESO ráðsins, Nicolò DAmico, forseti ESO ráðsins (sem er líka forseti INAF) og Matteo Pardo, fulltrúi vísinda í ítalska sendiráðinu í Berlín.

Review: Severe name repetition and truncation omit event payload.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0 [TRUNCATED]: ESO var hrifinn við því að veita Þessari innlendu yfirvöldskonu í menntun og reynslu, hnn. Stefania Giannini, til þessarar veitingar sem einnig tókst í henni í gegnum íkonu Ítalíu, Renato Cianfarani, herra íkonu Ítalíu í Múnðúr, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche, herra Patrick Roche

</details>

<details><summary>development_review #125 · A · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eso:775

English: A team of astronomers, led by Istvan Dékány of the Pontificia Universidad Católica de Chile, has now used data from this survey, taken between 2010 and 2014, to make a remarkable discovery - a previously unknown component of our home galaxy, the Milky Way.

Reference (shown after audit): Hópur stjörnufræðinga undir forystu Istvan Dékány við Pontificia Universidad Católica de Chile, notaði gögn úr verkefninu sem aflað var milli 2010 og 2014 og gerði merkilega uppgötvun á áður óþekktu svæði í Vetrarbrautinni okkar.

Review: Astronomer team and Milky-Way discovery proposition lost in all candidates.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Kennarhópur fyrirtækja, yfirleitt ástæðu István Dékány frá Pontificia Universidad Católica de Chile, hafa nýlega notið gögn frá þessu skoðun, sem komið var á milli 2010 og 2014, til mikilvægs neytis - einhverja gagn, sem voru aldrei kennd úr húðgallið okkar, milífjöður.

Candidate 1: Tímabundið astríðarfréttur á stofnun Pontificia Universidad Católica de Chile, með Istvan Dékány í fylgum, hefur nú notuð gagna af þessum skoðun, sem gerð var annaðhvort á milli 2010 og 2014, til að ná grænlegu upplýsingu - einhverja ofanveginn af heimgalanir okkar, Milóskyggð.

Candidate 2: Aðildarstjórnar af æðastaðlarmenn, hreyfisstjórinn István Dékány frá Pontificia Universidad Católica de Chile, hafa nynju að nota gagnanotkun frá þessu rannsókn, sem gerð er milli 2010 og 2014, til skýra fráritana - einhvernð sem fjarskiptið hefur ekki haldið áður.

Candidate 3: Hóp áhættufrænda, ledin á framburð og Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notið gögnum í þessum skoðun, sem ástæður voru taktu um tímabilið 2010 til 2014, til skemmtilegri aðferðar - undirúterni, sem var þátttöku óþekktur hlutur heimhússvæðis okkar, hvílt-stræðis.

Candidate 4: Framleiðandi af hópsins, István Dékány frá Pontificia Universidad Católica de Chile, hefur notuð gögn úr þessu merkingu, sem gerð hefur verið milli 2010 og 2014, til tilfinningar í nokkru þróun - einhvers vegar óþekktur hluti í heimágalinu, Svipuða vínið.

Candidate 5: Tálin af æðum, leit til vöktunar á István Dékány, Pontificia Universidad Católica de Chile, hafi nú notið upplýsingum í þessu skoðun, sem tókir voru fram um tíðina 2010-2014, til óvískaðs rannsóknarriðis í smágalátinni okkar, "Miltaketjuna".

Candidate 6: Týmisjóð af æðnirnirmenn, uppsenkrifinu Istvani Dékány frá Pontificia Universidad Católica de Chile, hefur nú notað gögn úr þessum samanburði, sem fengist var 2010 til 2014, til að ná áskriflegri fundi - einhvern hinn óvískaður hlutur heimgalans, Þekki.

Candidate 7: Fjölskyldubóta sem leistrast með Istvan Dékány, frá Pontificia Universidad Católica de Chile, er nú innan þess að nota gagnir úr þessu skoðun, sem tókst á milli 2010 og 2014, til að gera óvartunandi frátölvu - annar hluta á heimgaldrarinni, miljusýpnum.

</details>

<details><summary>development_review #126 · A · greedy · technical_short · F</summary>

Source ID: p13official21:dev:ema:704

English: The most frequently reported adverse reaction was acne, which was generally mild.

Reference (shown after audit): Algengasta aukaverkunin sem greint var frá er þrymlabólur (acne), sem voru venjulega vægar.

Review: Acne omitted and frequency statement garbled.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Hæsta merki um aukaverkanir var meðhöndlaða, sem var algengt vægleg.

</details>

<details><summary>development_review #127 · t2000188 · greedy · general · P</summary>

Source ID: p13official21:dev:opensubtitles:996

English: What kind of man would that make me?

Reference (shown after audit): Hvers konar maður væri ég þá?

Review: What kind of man would that make me retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Hvers konar maður myndi það gera mig?

</details>

<details><summary>development_review #128 · t2000188 · greedy · technical_long · U</summary>

Source ID: p13official21:dev:ema:325

English: If you get lower abdominal pain, gain any weight rapidly, feel sick or are vomiting or if you have difficulty in breathing, talk to your doctor straight away who might ask you to stop using this medicine (see in section 4 under “Serious side effects”).

Reference (shown after audit): Ef þú færð verk í neðri hluta kviðar, þyngist hratt, finnur fyrir ógleði eða kastar upp eða ef þú átt erfitt með að anda, skaltu hafa tafarlaust samband við lækninn sem gæti beðið þig að hætta að nota lyfið (sjá 4. kafla „Alvarlegar aukaverkanir“).

Review: Most symptoms/action retained but lower-abdominal qualifier and nausea fidelity uncertain.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef þú færð kviðverki, færð þig hratt þyngd, færð sársauk eða hafir uppköst eða ef þér er erfitt við öndun, skaltu tafarlaust ræða við lækninn, sem kann að spyrja þig um að hætta notkun lyfsins (sjá kafla 4 undir „Alvarlegar aukaverkanir“).

</details>

<details><summary>development_review #129 · t1001129 · greedy · general · F</summary>

Source ID: p13official21:dev:opensubtitles:480

English: Now we have enough evidence to charge you with murder.

Reference (shown after audit): Við höfum næg sönnunargögn til að ákæra ykkur fyrir morð.

Review: Evidence and charge concepts mistranslated.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Nú er okkur nægilega tilkynningar til að skilla þig um morð.

</details>

<details><summary>development_review #130 · t2000188 · greedy · technical_medium · U</summary>

Source ID: p13official21:dev:eea:1716

English: The competent authorities of Gabon have reacted promptly to these concerns, indicating their commitment to take all measures necessary to implement applicable ICAO standards and enforce compliance with these standards as soon as possible.

Reference (shown after audit): Lögbær yfirvöld í Gabon brugðust tafarlaust við þessum áhyggjum og létu í ljós eindreginn vilja til að gera allar nauðsynlegar ráðstafanir til að koma í framkvæmd gildandi stöðlum Alþjóðaflugmálastofnunarinnar og tryggja að farið yrði að ákvæðum þeirra eins fljótt og auðið er.

Review: ICAO measures broadly retained but compliance and final timing clause unclear.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Lögbæra yfirvald í Gabón hafa svarað þessum ábendingum tafarlaust og benda til þess að þau séu skyldur til að gera allar nauðsynlegar ráðstafanir til að framfylgja gildandi staðlar ICAO og gera þær gildi svo snemma og skilið eftir sem mögulegt er.

</details>

<details><summary>development_review #131 · A · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eea:281

English: The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.

Reference (shown after audit): Fjárhæð þeirra fyrrnefndu (síðarnefndu) sem eru jafnaðar á móti þeim síðarnefndu (fyrrnefndu) í tilteknum binditímaflokki skal teljast jafnaðar stöður þess flokks en eftirstöðvar langra eða stuttra staðna telst ójöfnuð staða þess flokks.

Review: Maturity-band/matched-position relationship not retained.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Upplýsingarnar um íættniaðstæðu sem staðfestur fyrir á því stig sem staðfestur í látinn (andskotinn) ástæðu, skal bera til upplýsingarna um íættniaðstæðu sem staðfestur í látinn (andskotinn) ástæðu, þar sem óskiptu aðstæður fyrir stigina, fyrir ástæðuna sem látist (andskotinn).

Candidate 1: Hjá dæmigildingssvæðum sem merkjaðir eru saman skulu fá það að lengi fyrir (samtímis gengið fyrir) sem samræmda stöður í svæðinum og það áfram skoðuð stöður sem ekki er samræmd í svæðinu.

Candidate 2: Íþætti fyrstu (sisti) sem jafngildar eru í síðustu (fyrsta) í nú vísuðu umtöksskralu skal vera jafngildu stöður í þessu skralu, og óhjálgildu stöður í tengslum við sama skralu.

Candidate 3: Það skammtur, sem ber ásta við fyrstu (sisti) svörun, sem ber ásta við síðustu (fyrsta) svörun í við ásetuðu teínu skal vera viðstaður í þeirri teíni, og niðurstöðuna slíkra fyrirhastaðar eða fráhastaðar skal vera óviðstaður í svörun til sama teína.

Candidate 4: Hámarkið sem fyrri (helgið) eru samhöfðað af sínum (slíkum) í tilteknum útgefningaskra skal vera samhöfður stöðurinn í þeim skrá, svo henni viðkomandi skuldbæru stöður sem ekki eru samhöfðaðar á samhöfðunareininginu.

Candidate 5: Það skal vera fjárhæðir, sem fyrsta (sista) voru samræmdar fyrsta (sássta) í tiltekna áfökunarmatvaka, í samræmdum staðlum (en mældu staðlum) og það sem enn er í langa (skorta) staðla sem samræmt er ekki í samanvirkni ákveðinnar áfökunarmatvika.

Candidate 6: Höfundur skal halda til þess að brottaðu fyrir (lágmarkinni), sem upptakir eru um samantektina, sé uðtakur á samantektu (búta) og undanþegin skammta og stuttagangur, sem ekki hefur verið samantekt, sé óhugdri skammti (búta).

Candidate 7: Hlutar af fyrri (hjá síðast) sem sjálfur (vart síðast) samhæfi í tilteknum skammstíðni, skulu vera samhæfðum stöðum í þeirri skammstíðni, þar sem ósamhæfðar langa eða loka stöðuð skal vera ósamhæfðar stöðurnar í sama skammstíðninu.

</details>

<details><summary>development_review #132 · A · greedy · technical_short · U</summary>

Source ID: p13official21:dev:eea:1991

English: Paragraph AG27 is amended and after paragraph AG29, paragraph AG29A is added.

Reference (shown after audit): Ákvæðum liðar AG27 er breytt og á eftir lið AG29 er lið AG29A bætt við.

Review: Identifiers/action retained; invented paragraph term makes legal fidelity uncertain.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: AG27-álfærð er breytt og eftir AG29-álfærðinni bætist við AG29A-álfærðinni.

</details>

<details><summary>development_review #133 · A · G8 · technical_medium · P</summary>

Source ID: p13official21:dev:eea:1914

English: This Regulation shall enter into force on the third day following that of its publication in the Official Journal of the European Union.

Reference (shown after audit): Reglugerð þessi öðlast gildi á þriðja degi eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.

Review: Candidate3 correctly states third-day entry into force after EU Official Journal publication.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [3]

Candidate 0: Þessi reglugerð gerir gildi að þrjú daga eftir afkastan hennar í opinbera líkur Evrópusambandsins.

Candidate 1: Á þriðju daga eftir að þessi reglugerð er birt í Stjórnmálum Evrópubandalaganna skal hún gilda.

Candidate 2: Á þriðju daga eftir birtingu þessarar reglugerðar í Stjórnartíðindum Evrópusambandsins skal hún gilda.

Candidate 3: Á þriðju degi eftir birtun þessarar reglugerðar í Stjórnartíðindum Evrópusambandsins skal hún gilda.

Candidate 4: Á þriðju degi eftir þegar reglugerðin er birt í Upplýsingajöður Evrópusambandsins skal reglugerðin innkoma í gildi.

Candidate 5: Þessi reglugerð íhuga skal koma ráðstöfun í staðinn á þriðja daginn eftir birtun hennar í Stjórnartíðindum Evrópusambandsins.

Candidate 6: Reglugerð þessa skal ráðstafanir fyrir þriðju daga eftir því sem hún er birti í Stjórnartíðindum Evrópusambandsins.

Candidate 7: Reglugerð þessa skal gilda þrjá dag frá því sem hún er birti í Stjórnartíðindum Evrópuþingsins.

</details>

<details><summary>development_review #134 · t2000188 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eso:464

English: With an estimated mass of four to five times that of Jupiter, it would be the least massive planet to be directly observed outside the Solar System.

Reference (shown after audit): Massi fyrirbærisins er talinn milli fjórum til fimm sinnum meiri en massi Júpíters, svo hér gæti verið um að ræða massaminnstu reikistjörnu sem ljósmynduð hefur verið fyrir utan sólkerfið okkar.

Review: Direct observation replaced by unrelated walking/progress phrase.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þar sem þyngdarhækkur er fjórar til fimm sinnum þungari en Júpíter, væri það minnst þungasta reikistjarnan sem hefur verið gengið áfram utan sólarkerfisins.

</details>

<details><summary>development_review #135 · t1001129 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eea:281

English: The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.

Reference (shown after audit): Fjárhæð þeirra fyrrnefndu (síðarnefndu) sem eru jafnaðar á móti þeim síðarnefndu (fyrrnefndu) í tilteknum binditímaflokki skal teljast jafnaðar stöður þess flokks en eftirstöðvar langra eða stuttra staðna telst ójöfnuð staða þess flokks.

Review: Former/latter matching relationship omitted and maturity band garbled.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Hjá þeim hópum sem samræmaðar eru í viðkomandi útsetningahópi skulu vera samræmd staðfestir, en eftirfylgni langa eða stutta staðfestis skulu vera ósamrýmandir staðfestir í sömu hópi.

</details>

<details><summary>development_review #136 · t1001129 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:ema:325

English: If you get lower abdominal pain, gain any weight rapidly, feel sick or are vomiting or if you have difficulty in breathing, talk to your doctor straight away who might ask you to stop using this medicine (see in section 4 under “Serious side effects”).

Reference (shown after audit): Ef þú færð verk í neðri hluta kviðar, þyngist hratt, finnur fyrir ógleði eða kastar upp eða ef þú átt erfitt með að anda, skaltu hafa tafarlaust samband við lækninn sem gæti beðið þig að hætta að nota lyfið (sjá 4. kafla „Alvarlegar aukaverkanir“).

Review: Lower abdominal pain changed to abdominal inflammation.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef þú færð kviðbólga, færð þig að þyngjast hratt, færð þér óþægind eða þú hefur uppköst eða ef þú hefur verulega vart með öndun, skaltu tala við lækninn strax sem kann að spyrja þig um að hætta notkun lyfsins (sjá í kafla 4 undir „Alvarlegar aukaverkanir“).

</details>

<details><summary>development_review #137 · A · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eea:574

English: All rear-window, roof-panel and partition switches intended for use by occupants in the rear of the vehicle shall be capable of being switched off by a driver-controlled switch which is located forward of a vertical transverse plane passing through the R points of the front seats.

Reference (shown after audit): Allir rofar í hliðarrúðum að aftan, þaklúgum og skilrúmum sem farþegum baka til í ökutækinu er ætlað að nota skulu gerðir með þeim hætti að unnt sé að rjúfa straum til þeirra með rofa sem ökumaður stjórnar og er staðsettur framan við lóðrétt þverplan sem gengur í gegnum R-punkta framsætanna.

Review: Driver-control/switch and geometry requirements lost.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Allar plána skiptir í bakvindur, húðmörkum og vörðum sem ætlað er við notkun af samtökum í bak yfirleitt skal vera smíðaðar til að fjarlægja með skiptisölun sem er stjórnlaust og er staðsett við fyrir við hliðbúðina.

Candidate 1: Allir opinbreytingar á skilfagna, húðbrúða og víðbreytingar í bænum af ökumannum sem eru í eftirhliði bílnar skulu gæta að unna við hæfur í aðgengilagi ökumannsinni sem er settu í fyrirhlið samtækin lyngslega lyg.

Candidate 2: Allir upphæðsfjölra, tegundsmennar og veggismálir, sem ætlaðir eru til notkunar hjá starfsmenn á enda ökutækisins, skulu kleift að hætta með veitingsbúnaði sem er að staðar fyrir við yfirhúslið sem skipulegir yfir hlutaðeigandi R-stöðu á fyrstu sætrum.

Candidate 3: Allar höðvísir, þeirr sem falla hennir undan hálsinni og hlífveranir sem hægt er að nota einstaklingarnir í eftirhliðum ökutækisins skulu vera hægt að taka ofst á með fylgiseðri hæðindu sem er staðsett frá hliðnum í létilegri leifar sem snúaðir eru á R-stigum á fyrstu sætinu.

Candidate 4: Hverja hluta á hreinihlutar, þörfhluta og hluta í gegnumbreytinni sem eru ætlaðir til notkunar af fyrirtækin í rými ökutækisins skal hægt að krefjast af með áhættumálastungri hluta sem er meðhöndlaður af ökumaður og er staðsettur fyrir bak á vertuða tengt ágræðli sem gangur um R-stig fyrri sætan.

Candidate 5: Allar bakið gluggi, rassglæði og haldandi á meðal skiptir sem ætlað eru til notkunar hjá innevinnum í hinni höndu verkisins skulu heimilt að vera hægt að skipta eytt af með skiptisviðum sem er kunnin og eftirgefandi og er stað sett fyrir loftrekkið, horfið leiti sem nýta aðgang að R-stigum fyrstu kyrrsætans.

Candidate 6: Allir bakglas, öll gagnaskiptir úr háðlageri og gesti, sem ætlaðir eru til notkunar af fólki í bak, skulu vera reynd til að gangra á við klúðra sem er kunnast með af hæfileikum og er í fænistrið en við alla hluttagjörtu, sem gönguðar sé með þrúg í fyrstu sittingar.

Candidate 7: Allar bakgluggi, húðafæð í rútinu og þyrsturinn skal heimilt að gangast af við afhöldur sem er handleyslanleg og eru staðsett í fyrirhvarf fyrir vertuð áhættuvæg sem berast við fyrstu sjónhúsið.

</details>

<details><summary>development_review #138 · t1001129 · greedy · technical_short · F</summary>

Source ID: p13official21:dev:eea:1991

English: Paragraph AG27 is amended and after paragraph AG29, paragraph AG29A is added.

Reference (shown after audit): Ákvæðum liðar AG27 er breytt og á eftir lið AG29 er lið AG29A bætt við.

Review: Paragraph identifiers referred to as document/definition.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: AG27-skjalinn er breytt og eftir skilgreiningu AG29 bætist við skjali AG29A.

</details>

<details><summary>development_review #139 · A · greedy · general · P</summary>

Source ID: p13official21:dev:opensubtitles:996

English: What kind of man would that make me?

Reference (shown after audit): Hvers konar maður væri ég þá?

Review: Question about what kind of man this makes speaker retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Hvaða maður myndi þetta gera mig?

</details>

<details><summary>development_review #140 · A · greedy · technical_long · U</summary>

Source ID: p13official21:dev:eea:1194

English: It should provide the Commission and the Member States with objective, reliable and comparable information and data on maritime safety and on ship pollution prevention to enable them to take any necessary initiatives to enhance the measures in place and to evaluate their effectiveness.

Reference (shown after audit): Henni ber að sjá framkvæmdastjórninni og aðildarríkjunum fyrir hlutlægum, áreiðanlegum og sambærilegum upplýsingum og gögnum um siglingaöryggi og varnir gegn mengun frá skipum til að gera þeim kleift að vinna hvers kyns nauðsynleg framtaksverkefni til að efla þær ráðstafanir sem gerðar hafa verið og að meta skilvirkni þeirra.

Review: Maritime/prevention purpose recognizable but objective and pollution terminology uncertain.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Hún skal veita framkvæmdastjórninni og aðildarríkjunum reynileg, áreiðanlegar og samanburðar upplýsingar og gögn um öryggis á sjóum og um aðferðir til að koma í veg fyrir útburð af skipum til að þau geti gert það nauðsynlegt aðgerðir til að auka ráðstafanir sem eru í stað og meta hvernig hennar eru virka.

</details>

<details><summary>development_review #141 · t2000188 · G8 · technical_short · U</summary>

Source ID: p13official21:dev:eea:1461

English: All industrial uses of gas are considered.

Reference (shown after audit): Öll notkun á gasi í atvinnurekstri er talin með.

Review: Closest candidate broadens industry to occupational uses and changes considered to specified.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Í öllum atvinnufinnnum notkunum breiðir opinbókin.

Candidate 1: Íframtekinn er á öllum atvinnuhindrunarnotkunum af gassvörunum.

Candidate 2: Heimilt er að taka tillit til allra vinnusamstæða gasins.

Candidate 3: Tilgreind eru öll atvinnuleg notkun gasa.

Candidate 4: Í allar gjöfgerðir af gasi er tekin tillit.

Candidate 5: Tilgreina er allan notkun eldsneytis í vinnustöðvar.

Candidate 6: Tilgreint er um öllum starfsmunarefnum, sem gjöfin eru notaðar til.

Candidate 7: Tilgreint er um öll vinnuveitandi notkun gas.

</details>

<details><summary>development_review #142 · t2000188 · greedy · general · F</summary>

Source ID: p13official21:dev:opensubtitles:2508

English: Rose, we have a guest in the living room.

Reference (shown after audit): Rósa, það er gestur í stofunni.

Review: Living-room location reduced to unspecified home.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Rose, við höfum gest í heimilinu.

</details>

<details><summary>development_review #143 · t2000188 · greedy · general · P</summary>

Source ID: p13official21:dev:opensubtitles:1012

English: I'll do whatever you ask.

Reference (shown after audit): Ég geri hvað sem þið viljið.

Review: Commitment to do what addressee asked retained; minor inflection.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Ég geri hvað þú baðir.

</details>

<details><summary>development_review #144 · t1001129 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:ema:1765

English: Take this leaflet or some tablets with you so that your doctor knows exactly what you have taken.

Reference (shown after audit): Hafa skal þennan fylgiseðil eða eitthvað af töflum meðferðis svo læknirinn viti nákvæmlega hvað tekið hefur verið.

Review: Doctor knowing exactly what was taken changed to knowing reasons.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Fáðu þessum fylgiseðli eða töflur með þér svo að læknirinn þekki allt ástæðan sem þú hefur tekið.

</details>

<details><summary>development_review #145 · t2000188 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eea:15

English: Where studies are conducted using active substance produced in the laboratory or in a pilot plant production system, the studies must be repeated using active substance as manufactured, unless it can be justified that the test material used is essentially the same for the purposes of environmental testing and assessment.

Reference (shown after audit): Ef rannsóknir eru gerðar með því að nota virkt efni sem er framleitt á rannsóknarstofu eða í tilraunaframleiðslukerfi verður að endurtaka rannsóknirnar með því að nota verksmiðju-framleitt virkt efni, nema hægt sé að færa rök fyrir því að prófunarefnið sem er notað sé í megindráttum hið sama og er notað við umhverfsirannsóknir og umhverfismat.

Review: Pilot-plant and/or justified-equivalence condition wrong throughout.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Ef rannsóknir eru framkvæmdar með virkum efni sem framleitt er í rannsóknarstofu eða í stefnumarkaðarframleiðsluskyni, skal endurtakast rannsóknirnar með virkum efni eins og þau eru framleiddar, nema réttlætist hægt að útskýra því að prófunarefnið skilvirkt er eins í þeim tilvikum þar sem staðreyrðingurinn tekur sér stað í mælingum um umhverfið.

Candidate 1: Ef rannsóknir eru gert með virkar efni sem framleidd er í húsið eða í anflætt vinnuáætlun skal endurtaka rannsóknina með virkum efnið sem framleiðið er, nema ástæðu sé lagðar fram að prófunarefnið, sem notuð er, sé af essi þýði svæðilegt sama við umhverfisrannsóknir og mat á þeim.

Candidate 2: Ef rannsóknir eru gerðar með virka efninu sem framleiðið er í rannsóknarstofunni eða við styrkuð framleiðslussölu, verður að endurtaktu rannsóknirnar með virku efninu eins og þau eru framleidd, nema til versnunar sé kynnt að prófuninu sé eins efnalega af því áhrifum í umhverfismati í tengslum við umræður og mat á efninu.

Candidate 3: Ef rannsóknir eru gerðar með virka efni sem framleidd er í rannsóknarstofu eða í starfsmálætu framleiðslusettuleikum, skal endurskoða rannsóknirnar með virka efni eins og framleidd er, nema á viðurkenningu geti reyndst að prófunarefnið sé til í öllu orsaki sá sömu til um rannsóknir á umhverfisástand.

Candidate 4: Ef rannsóknir eru gerðar með virkirum efninum sem framleidd er í rannsóknarkerfinni eða í bein síðanframlagða efnaframleiðsluvirkjum þarf að endurtaka rannsóknirnar með virkirum efninu eins og þau eru framleidd, nema það sé gerlegt réttan að þau séu, af öllum hætti, svipuður efnið til að tilrita umhverfisrannsóknir og mat á því.

Candidate 5: Ef rannsóknir eru gerðar með virka efninum, framleiddum í rannsóknarstofu eða í framleiðsluæðabúnaði, verður að endurtaka rannsóknir með virka efninu sem framleiddur hefur verið nema mælt sé til þess að prófunarsamsettni sé aðallega sá sama við umhverfisrannsóknir og mat á því.

Candidate 6: Ef rannsóknir eru gerðar með virku efninu sem framleidd er í rannsóknarstofu eða í forstæðubólusetningu skal endurtaka rannsóknirnar með virku efninu sem framleidd er, nema reyni sé hægt að ræða að prófunarefninu sé framleidd með svipaðum hætti.

Candidate 7: Ef rannsóknir eru gerðar með virka efninu sem framleiddur er í rannsóknarfyrirtækjum eða í rannsóknarskírteini frá framleiðsluþáttum verður að endurskoða rannsóknirinnar með virka efninu sem framleidd er, nema hægt sé að grundvelli rannsóknarefnisins ber að vera sambærilegur að því er varðar umhverfisrannsóknir og mat.

</details>

<details><summary>development_review #146 · t2000188 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eea:1552

English: The analytical result shall be reported as x +/– U whereby x is the analytical result and U is the expanded measurement uncertainty, using a coverage factor of 2 which gives a level of confidence of approximately 95 % (U = 2u).

Reference (shown after audit): Greina skal frá niðurstöðum úr greiningunum sem x +/– U þar sem x er niðurstaða greiningarinnar og U er útvíkkaða mælióvissan með þekjustuðlinum 2 sem gefur 95% öryggisstig (U = 2u).

Review: Expanded uncertainty and confidence-factor terminology garbled.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Greina skal niðurstöður greiningarinnar sem x +/– U þar sem x er niðurstöður greiningarinnar og U er útsetningarráðstafanirnar, með því að nota 2 gildi fyrir umfryndingargildi, sem gefur umframvísitengingu um 95% (U = 2u).

</details>

<details><summary>development_review #147 · A · G8 · technical_short · U</summary>

Source ID: p13official21:dev:ema:1192

English: It is used to prevent pregnancy.

Reference (shown after audit): Lyfið er notað til að koma í veg fyrir þungun.

Review: Pregnancy word in closest candidate is malformed; cannot certify.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Hún er notuð til að koma í veg fyrir barnslyfjum.

Candidate 1: Hún er notuð til að koma í veg fyrir barnshaf.

Candidate 2: Það er notuð til að koma í veg fyrir þjóna.

Candidate 3: Koma er notuð til að dregja úr því að fæði stendur.

Candidate 4: Hún er notuð til að koma í veg fyrir barnabreiðslu.

Candidate 5: Það er notuð til að koma í veg fyrir frjósemin.

Candidate 6: Það er notað til að koma í veg við berst.

Candidate 7: Hún er notað til að koma í veg fyrir giftun.

</details>

<details><summary>development_review #148 · A · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eso:1051

English: The technique used by Teague, which derived averaged variations in the flow of the gas as small as a few percent, revealed the impact of multiple planets on the gas motions nearer to the star.

Reference (shown after audit): Tæknin sem Teague beitti sýndi meðalbreytingarnar á gasflæðinu niður í nokkur prósent og leiddi í ljós áhrif nokkurra plánetna á hreyfingu gassins nær stjörnunni.

Review: Flow-variation method and planetary relationship garbled.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Tæknið sem Teague notuði, sem fengið var ásamt meðalháttum þróun í flutningi lofttegunda eins og nokkrar hundraðshluti, sýndi áhrif múltupla heims á flutninga lofttegundanna nærri stjarnanum.

</details>

<details><summary>development_review #149 · t1001129 · greedy · general · P</summary>

Source ID: p13official21:dev:opensubtitles:1169

English: They're pretty as can be, aren't they?

Reference (shown after audit): Fallegri er ekki hægt að vera, ekki satt?

Review: As pretty as can be and tag question retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Þeir eru fallegar eins og getur verið, ekki satt?

</details>

<details><summary>development_review #150 · t2000188 · G8 · technical_short · F</summary>

Source ID: p13official21:dev:eso:302

English: This is because the tilt of the orbit is normally unknown.

Reference (shown after audit): Þetta er vegna þess að venjulega er brautarhallinn óþekktur.

Review: Orbital tilt not faithfully rendered in any candidate.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Það er vegna þess að það er venjulega óþekktur típ svæðisins.

Candidate 1: Þetta er vegna þess að hringriska yfirborðsins er venjulega ekki þekkt.

Candidate 2: Það er vegna þess að bláæður ormdsins er vanalega óþekkt.

Candidate 3: Þetta er vegna þess að þjóðgerð rótisins er venjulega óþekkt.

Candidate 4: Það er vegna þess að hálfan aroundurskölduninni er venjulega óþekkt.

Candidate 5: Þetta kemur fram vegna þess að þjóðabrisið er venjulega ekki þekkt.

Candidate 6: Þetta er vegna þess að gildistæði kring kursins er venjulega óþekkt.

Candidate 7: Þetta er vegna þess að umhanga stjörnustungsins er venjulega óþekkt.

</details>

<details><summary>development_review #151 · A · G8 · technical_short · F</summary>

Source ID: p13official21:dev:eso:302

English: This is because the tilt of the orbit is normally unknown.

Reference (shown after audit): Þetta er vegna þess að venjulega er brautarhallinn óþekktur.

Review: Orbital tilt replaced by unrelated biological/mechanical concepts.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Það kveðið á veg fyrir því að það er óþekkt hvort tilháður er stenginn eða opinn.

Candidate 1: Það er fyrir því að ástæðurum þessar eru einkenni tilhögunar á úrmyndunum.

Candidate 2: Það er vegna þess að bláæð ökutækis er vanalega óþekkt.

Candidate 3: Þetta er vegna þess að þjóðorháttur æxlans er vanalega óvænt.

Candidate 4: Það er vegna þess að hálfalengd umferðarhálfar er alltaf óþekkt.

Candidate 5: Það er vegna þess að framstöngur í umflutningu er vanalega óþekkt.

Candidate 6: Þetta er vegna þess að fæðingur hreyfilsins er vanalega óviss.

Candidate 7: Þetta verður vegna þess að þættun í loftkrasti er almennlega óvísnumið.

</details>

<details><summary>development_review #152 · t1001129 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eso:206

English: The survey was sensitive to planets between 75 million kilometres and 1.5 billion kilometres from their stars (in the Solar System this range would include all the planets from Venus to Saturn) and with masses ranging from five times the Earth up to ten times Jupiter.

Reference (shown after audit): Mælingarnar voru næmar fyrir reikistjörnum sem eru milli 75 milljón til 1,5 milljarða km frá móðurstjörnunum (í sólkerfinu okkar inniheldur þetta fjarlægðarbil allar reikistjörnur frá Venusi til Satúrnusar) og frá fimm sinnum massameiri en jörðin upp í tíu sinnum massameiri en Júpíter.

Review: All candidates corrupt distance units/ranges or mass endpoints.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Skoðunin hefur verið sérstakur fyrir reikistjörnurnar á milli 75 milljón klst og 1,5 milljarðsklst frá stjörnur sínum (í Jörðavarnamálum fylgir það allar reikistjörnurnar frá Venus til Saturn) og með þyngdhreifingum af fimm til tíu gildi Júpítrar.

Candidate 1: Skýrslugjöfin var klínver að verða við reikistjörnu sem eru á milli 75 milljón klst. og 1,5 milljón klst. frá stjörnunum (á sólkerfinu eru þetta rist í allar reikistjörnurnar frá Venus til Saturn) og með vega sem röðast frá fimm til ára jörðu til ára Júpíturna.

Candidate 2: Slíkt rannsókn var tilgreind með hlutfallslegri mununum á sáttmálum sem liggja á geimnum milli 75 milljón kílómetra og 1,5 milljón milljón kílómetra frá stjörnunum (hér á kjölfjöllsins hefði aðeins hvarfla um öll geimsvæði frá Venus til Surtíðarinnar) og með eðlilegum massamæli á að frá fimm til deysins að tíu síðustu gildum Júpurs.

Candidate 3: Til greiningar var næm við reikistjörnurnar á bilinu 75 milljónir kílómetra að 1,5 milljónir kílómetra frá stjörnunum (í Jörðamála vart um öllu reikistjörnurnar frá Venus til Saturns) og þekkingum á þeirra massabreytu frá fimm síðustu megin af jörðinni til tíu síðustu megin af Júpíturnum.

Candidate 4: Rannsóknin var sérstakur fyrir reikistjörnur á milli 75 milljónra og 1,5 milljónra ársferða af starfi þeirra (í sólkerfinu birta sína í tíðni allar reikistjörnurnar frá Venus til Sárga) og með þyngd frá fimm fali áður en tíu fali á Júpíturnum.

Candidate 5: Sýna var skýr og vart var alkomið á planitusins á milli 75 milljón kílómetra og 1,5 milljón biljanir kílómetra frá stjörnunum (í sólkerfinu falli allur yfirbúin af Venus til Saturns) og markaðssetning fyrir úr fimm að tíu fyrir Júpíturnar.

Candidate 6: Rannsóknin var nægileg á geimþjóðum í milli 75 milljón km og 1,5 milljón milljón km frá stjörnunum (sem næstu í sólkerfinu) og með þyngdartíðni á bilinu frá fimm fali jörða að tíu fali Júpítra.

Candidate 7: Rannsóknin var hessfæra á reikistjörnurnar á milli 75 milljón km og 1,5 milljón milljón km frá stjörnunum (í sólarbrautinni gæti hún komið fram allar reikistjörnurnar frá Venus til Saturn), með þyngd úr fimm að tíu gildum júpurtímarstöðva.

</details>

<details><summary>development_review #153 · A · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eso:765

English: “If it keeps spinning rapidly it might end its life in one of the most energetic explosions in the Universe, known as a long-duration gamma-ray burst,” says the lead scientist of the project, Hugues Sana, of the University of Leuven in Belgium.

Reference (shown after audit): „Haldi hún áfram að snúast mjög hratt gæti hún endað ævina sem langur gammablossi, ein orkumesta sprenging í alheiminum,“ segir Hugues Sana við Leuvenháskóla í Belgíu sem hafði umsjón með rannsókninni.

Review: Rapid spinning/energetic gamma-ray explosion proposition corrupted throughout.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: „Ef hún helst er að snurra of hægt að betur enda líf hennar í einhverju stórtu krafti mörkunarstöðugleika í heiminum, sem kallast langtímið grámæliákarburði,“ segir framsviðsáttarinn í verkefninu, Hugues Sana, frá Leuven-universitetsins í Belína.

Candidate 1: „Ef það tekur áfram á umferð kemur svo að það leiðir svo fyrir að svo mjög skrælulegri endurgerði í Heiminn, sem er kallað langt tíði grámeiniótferður,” segir stjórnavísindan framkvæmdaðarlega, Hugues Sana, af Leuven universítí í Belgíu.

Candidate 2: „Ef hann helst hreyfir stórt og gengur í línum getur hann leiddi lífi sínu í einu af sterkustu upptökum sem eru tekin á áherslu í almanum sem kallast langt tíma gamma-ráðskuðlinu“, segir leikfræðingur í stefnumálum, Hugues Sana, af leikfræðiskonungríkinni Leuven í Belízíu.

Candidate 3: „Ef hún flætur um rótt endar hún tilhöndun og er alveg áfram með erfiðri öndun og kallast langvinna gama-ugni.“, segir mikilvæginn vísindamennur frá vísindanefndinu í Leuven í Belgíu, Hugues Sana.

Candidate 4: „Ef það hreyfir áfram jafnframt getur það stökkinn í einum langar tíma og meiri skrýstungn í heiminn, kveðið af líðbólfrakrengun,“ segir framseldi leiðrannæmarni í vísindanefndinni á vísindanefndunni í Leuven í Belgía, Hugues Sana.

Candidate 5: „Ef það hittur áfram háttur máttan það endalausíti í einhversi langaðuhraða nogvökubrjótann í alheiðinum, sem heitir langvarandi brjótafla.“, segir vitneslisfréttinn á vísindanefndunni, Hugues Sana, af Sárgárðarfræðisaðilunni í Leuven í Belígna.

Candidate 6: „Ef það virkar tíðlega að snúa, kannski endar lífið með eins stórar efnisjökuna sem heitir langt tíðtökur ógammalegra ljóskotina.«, segir frábúinni vísindamenn stefnunnar, Hugues Sana, frá Rannsóknarfréttinu í Leuven í Belgíu.

Candidate 7: „Ef hún hreyfir á of hrifandi marki getur fyrir það lokið líf hennar í meistarri styrkri bera á almanaskotanum sem kallast langt tíma gammaljörnarstyrk,” segir lífrænda þánstvellur í vísindanefndinni, Hugues Sana, af Leuven-universiteten í Belgíu.

</details>

<details><summary>development_review #154 · t2000188 · G8 · technical_short · U</summary>

Source ID: p13official21:dev:eea:2037

English: Those criteria should not be considered to be exhaustive.

Reference (shown after audit): Þessar viðmiðanir skulu ekki teljast tæmandi.

Review: Not exhaustive changed to perfection/sufficiency/precision; uncertain.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Ekki ætti að taka þessi viðmiðanir til að vera fullkomnir.

Candidate 1: Þessi viðmiðanir skulu ekki teljast nákvæma.

Candidate 2: Ekki skal talast á þessum viðmiðunum um fullkomnulega.

Candidate 3: Ekki skal telja þessi viðmiðanir fullkomnir.

Candidate 4: Ekki skal talinn að skilgreiningarnar séu aðfullar.

Candidate 5: Ekki skal talast að þessar viðmiðanir séu takmörkuðar.

Candidate 6: Ekki skal taka þessi viðmiðanir til þess að vera fullnægjandi.

Candidate 7: Ekki skal telja þær viðmiðanir alveg upplaus.

</details>

<details><summary>development_review #155 · t2000188 · G8 · technical_short · F</summary>

Source ID: p13official21:dev:eso:491

English: ALMA can observe in different frequency bands.

Reference (shown after audit): ALMA getur gert mælingar á mismunandi böndum.

Review: Frequency bands not retained in any candidate.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: ALMA getur athugað á mismunandi fyrirbirgðum.

Candidate 1: ALMA getur fylgst með framförum á mismunandi beitingaskjaldri.

Candidate 2: ALMA getur skýrslugjaf í mismunandi fjölli.

Candidate 3: ALMA getur fylgst með breytum á tvær mörgum sjónverða.

Candidate 4: ALMA getur skýrar á mismunandi breiðslumálum.

Candidate 5: ALMA getur mælt á mismunandi fjölda ár.

Candidate 6: ALMA getur metað á fleiri breyturbandum.

Candidate 7: ALMA getur fylgst með breytum á mismunandi fjölda.

</details>

<details><summary>development_review #156 · t2000188 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eso:726

English: They wanted to study the interaction between a young generation of stars and the cold clumps that were assembling into these first galaxies.

Reference (shown after audit): Stjörnufræðingarnir vildu rannsaka víxlverkunina milli ungrar kynslóðar stjarna og köldu kekkjanna sem voru að safnast saman í þessum fyrstu vetrarbrautum.

Review: Cold clumps replaced by cold pressures.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þeir vildu rannsaka milliverkanir milli ungri stjarnafurs og kaltar þrýstinga sem voru samanbúin í þessum fyrstu vetrarbrautum.

</details>

<details><summary>development_review #157 · t1001129 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eea:15

English: Where studies are conducted using active substance produced in the laboratory or in a pilot plant production system, the studies must be repeated using active substance as manufactured, unless it can be justified that the test material used is essentially the same for the purposes of environmental testing and assessment.

Reference (shown after audit): Ef rannsóknir eru gerðar með því að nota virkt efni sem er framleitt á rannsóknarstofu eða í tilraunaframleiðslukerfi verður að endurtaka rannsóknirnar með því að nota verksmiðju-framleitt virkt efni, nema hægt sé að færa rök fyrir því að prófunarefnið sem er notað sé í megindráttum hið sama og er notað við umhverfsirannsóknir og umhverfismat.

Review: Pilot-plant/repeat-study and equivalence exception corrupted.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Ef rannsóknir eru framkvæmdar með virkum efni sem verður fram fram á rannsóknastöðvun eða í kemmtustöðvum skulu endurtekja rannsóknirnar með virkum efni sem verið er, nema það sé rétt að valda að prófunarháttin, sem notað er, sé hlýðilega samanborið við prófunarháttin sem notað er fyrir umhverfisprófanir og -mat.

Candidate 1: Ef rannsóknir eru gert með virkum efni sem verður fram hópa í rannsóknaráðstöðvinni eða í rannsóknaráðsetningu fyrir stöðu, þá verða nákvæmlega að endurskoða rannsóknirnar með virkum efni eins og það er framleitt, aðra en samræmdist getur vera að það er rétt að hagmyndin sem er notaður sé ekki aðallega samanborið við umhverfisrannsóknir og mat.

Candidate 2: Ef rannsóknir eru gerðar með virka efni sem framleitt er í rannsóknarkerfi eða í prófunaræxlum við rannsóknarkerfi skulu endurkalla rannsóknirnar með virku efni sem framleitt er, nema framleiðslunóknun hafi staðfest að prófunarhópið, sem er notað í rannsóknunum, sé í raun svipuður hjá þeim tilgangi sem er það að þá geti verið metin fyrir umhverfisrannsóknir og mat.

Candidate 3: Ef rannsóknir eru gerðar með virka efni sem framleitt er í rannsóknarkerfi á fagvísindasamhengingu eða á fæðubúnaði skal endurskoða rannsóknirinn með virka efni eins og það er framleitt, nema geta verið reynd að það sé óþekkt að prófunarsýnun sem notuð var sé áframhaldandi af hins vegar.

Candidate 4: Ef rannsóknir eru gerðar með virkum efna sem eru framleiddar í rannsóknarkerfinu eða í fyrirbúinum úr forðatryggingum, verða þær endurtekna með virkum efnum eins og þau eru framleiddar, nema valið verði staðfest að prófunarefnið sem notað er sé framleiðsluð, í öllu allt, jafnvægur til að rannsóknir á umhverfismilun og eftirlit með umhverfi insjóga.

Candidate 5: Ef rannsóknir eru gerðar með virka efnunni, sem framleitt hefur verið í rannsóknarkerfinu eða efnasvíti í sýslusjóknunni, skulu rannsóknirnar endurtaktu með virku efnunni í þeirri samsettu framleiðslu- kerfi, nema eftirlit geti staðfest af því að prófunarefnin, sem notað er, er í heil fyrir umhverfisrannsóknir og mat.

Candidate 6: Ef rannsóknir eru gerðar með virku efni sem framleitt er í vinnsluferð í vinnslustöðvum eða í vinnsluferð í rannsóknarstöðum, skulu rannsóknirnar endurtaka með virku efni sem framleitt er, nema útreikningar reiknuðar úr þeim að mismunandi virku efni er nauðsynlegt að nota til að greina útvegslagið sem notuð er, ef notuður prófunarmarkmið er hluti af slíkum í gildi fyrir reynslu um umhverfisráðstöfun og rannsóknar.

Candidate 7: Ef rannsóknir eru gerðar með virka efna sem framleitt eru í rannsóknarkennslunum eða í stefnumyndunarstofum, þarf að endurtaka rannsóknir þar sem virka efnið er uppfærð við framleiðslunni eftir einungis að skýrðist það að prófunarhiefið sem notað var verði sé í raun hins vegar eins ef prófunarhiefið er notað í umhverfisprófunum og -gögnunum.

</details>

<details><summary>development_review #158 · t1001129 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eso:919

English: "Thanks to several giant telescopes currently under construction, including ESOs E-ELT and the NASA/ESA/CSA James Webb Space Telescope due to launch for 2018, we will soon be able to study the atmospheric composition of these planets and to explore them first for water, then for traces of biological activity.

Reference (shown after audit): „Þökk sé nokkrum risasjónaukum sem nú eru í smíðum, þeirra á meðal E-ELT sjónauka ESO og James Webb geimsjónauka NASA; ESA og CSA sem skotið verður á loft árið 2018, munum við fljótlega geta rannsakað efnasamsetningu lofthjúpa þessara reikistjarna og kannað þær fyrst í leit að vatni og síðan leitað að merkjum um líf.

Review: Under-construction/atmosphere/water concepts not faithfully rendered.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: „Við fáum það þakka fyrir nokkrum stórum sjónaukum sem eru í framrúmmáli og þar á meðal ESOs E-ELT og James Webb Space Telescope NASA/ESA/CSA sem er að fara í reynd fyrir árið 2018, getum við nánast umhverfisbundna samsetningu þessara jörðanna og rannsaka þær fyrst með vökva, síðan með einkenni líffræðilegra virkjunar.

</details>

<details><summary>development_review #159 · A · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eea:281

English: The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.

Reference (shown after audit): Fjárhæð þeirra fyrrnefndu (síðarnefndu) sem eru jafnaðar á móti þeim síðarnefndu (fyrrnefndu) í tilteknum binditímaflokki skal teljast jafnaðar stöður þess flokks en eftirstöðvar langra eða stuttra staðna telst ójöfnuð staða þess flokks.

Review: Maturity band and residual long/short relation lost.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Hægt er að setja fjárhæð fyrri (sisti) sem samræmt var með síðar (fyrri) í tilteknum útsetningartengslum og þá skal hún samræmd staðurinn í tengslum, svo þá henni sem ósamræmd staður í tengslum við sama tengsl.

</details>

<details><summary>development_review #160 · A · greedy · general · F</summary>

Source ID: p13official21:dev:opensubtitles:1159

English: Somebody get me a picture of the girl.

Reference (shown after audit): Útvegið mér mynd af stelpunni.

Review: Picture of girl request lost.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Láttu einhverja skýra mig á súgengi.

</details>

<details><summary>development_review #161 · A · greedy · technical_medium · U</summary>

Source ID: p13official21:dev:eea:1716

English: The competent authorities of Gabon have reacted promptly to these concerns, indicating their commitment to take all measures necessary to implement applicable ICAO standards and enforce compliance with these standards as soon as possible.

Reference (shown after audit): Lögbær yfirvöld í Gabon brugðust tafarlaust við þessum áhyggjum og létu í ljós eindreginn vilja til að gera allar nauðsynlegar ráðstafanir til að koma í framkvæmd gildandi stöðlum Alþjóðaflugmálastofnunarinnar og tryggja að farið yrði að ákvæðum þeirra eins fljótt og auðið er.

Review: ICAO commitment largely recognizable but prompt reaction mistranslated and compliance wording uncertain.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Viðkomandi yfirvöld í Gabón hafa svöngt svarað á þessum áhyggjum og tilgreint að þeir hafi skuldbinding við að gera öllum þær ráðstafanir sem nauðsynleg eru til að framfylgja gildandi stöðlunarkerfi ICAO og koma til samræmis við þessar stöðlunarkerfi eins fljótt og mögulegt er.

</details>

<details><summary>development_review #162 · t2000188 · greedy · general · F</summary>

Source ID: p13official21:dev:opensubtitles:3607

English: Well, that makes you ugly and stupid.

Reference (shown after audit): Þá ert þú ljótur og heimskur.

Review: Ugly replaced by weird.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það gerir þig skríti og heimskur.

</details>

<details><summary>development_review #163 · A · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eea:50

English: Similar studies, for at least three soil types, must be reported for all relevant metabolites, degrada tion and reaction products which in soil degradation studies account at any time for more than 10 % of the amount of active substance added.

Reference (shown after audit): Gera skal grein fyrir svipuðum rannsóknum á þremur jarðvegsgerðum hið minnsta með tilliti til allra viðkomandi umbrots-, niðurbrots- og hvarfaefna sem í rannsóknum á niðurbroti í jarðveginum nema á einhverjum tímapunkti meira en 10% af viðbættu magni virka efnisins.

Review: Soil types and degradation/reaction product specification not retained.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Sjálfar sambærilegar rannsóknir, í minnst þremur jarðtökum, verða að gefa fram fyrir öllum viðeigandi umbrotsefni, umbrotsefnin og afleiðingar sem í umbrotsefnisrannsóknum taka meira en 10% af skammti virka efna sem bætt er við í jarðtökunum.

</details>

<details><summary>development_review #164 · A · G8 · technical_short · U</summary>

Source ID: p13official21:dev:ema:767

English: Therefore, docetaxel must not be used during pregnancy unless clearly indicated.

Reference (shown after audit): Dócetaxel á því ekki að nota á meðgöngu nema brýna nauðsyn beri til.

Review: Clear clinical indication condition not reliably rendered.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Til þess á að notkun docetaxels sé ekki notað á meðgöngu nema það komist fram að gera því.

Candidate 1: Því má ekki nota docetaxel með mótefni nema það sé skýrt út.

Candidate 2: Því má ekki nota doketaxel á meðgöngu nema það sé skýrt til.

Candidate 3: Því má ekki nota docetaxel á meðgöngu nema ákvarðanir komi frá.

Candidate 4: Því má ekki nota docetaxel á meðgöngu aðra en það er greint um.

Candidate 5: Því verður að ekki nota docetaxel á meðgöngu án þess að það sé greidd áður.

Candidate 6: Því má ekki nota docetaxel með útsetningu á meðgöngu nema það sé kveðið á um.

Candidate 7: Því ætti ekki að nota docetaxel með hliðsjón af því að það er notað meðan á meðgöngu stendur, nema það sé birt sem verður.

</details>

<details><summary>development_review #165 · t2000188 · G8 · technical_medium · F</summary>

Source ID: p13official21:dev:ema:1406

English: Concomitant use with yellow fever vaccine and with live virus and bacterial vaccines (see section 4.5).

Reference (shown after audit): Samhliða notkun með bóluefni gegn gulusótt og bóluefni með lifandi veirum og bakteríum (sjá kafla 4.5).

Review: Yellow-fever vaccine and other live vaccines not jointly retained.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Rannsókn með bóluefnum gegn hellingareikistreiði og lifandi veiru- og bakteriafræðilegum bóluefnum (sjá kafla 4.5).

Candidate 1: Samhliða notkun bleygjalyfja gegn gultsýki og lifandi veirulyfja og sýklalyfja (sjá kafla 4.5).

Candidate 2: Samhliða meðferð með barnavefju- bóluefni til bólusetningar við fulvestur og með lifandi veirusjúkdómsbóluefni og bakteríusbóluefni (sjá kafla 4.5).

Candidate 3: Samhliða notkun barnlífvefja og lifandi veiru- og bakteríuhvítlykju (sjá kafla 4.5).

Candidate 4: Samhliða notkun á barnaleifingavefni fyrir gulverri sýkingu og lifandi veira og baktería (sjá kafla 4.5).

Candidate 5: Samhliða notkun barnaöndunarlyfs við gulvístgigtarælum og lifandi veiru- og bakteriafrællu bóluefnum (sjá kafla 4.5).

Candidate 6: Eingöngu samhliða notkun berafls gegn gultfíflisbólgu og lifandi veiru- og bakteríusbóluefna (sjá kafla 4.5).

Candidate 7: Samhliða notkun eftirveiru bóluefnisins gegn tinnfæri og lifandi veira- og bakteríubóluefnisins (sjá kafla 4.5).

</details>

<details><summary>development_review #166 · A · greedy · technical_medium · U</summary>

Source ID: p13official21:dev:eso:726

English: They wanted to study the interaction between a young generation of stars and the cold clumps that were assembling into these first galaxies.

Reference (shown after audit): Stjörnufræðingarnir vildu rannsaka víxlverkunina milli ungrar kynslóðar stjarna og köldu kekkjanna sem voru að safnast saman í þessum fyrstu vetrarbrautum.

Review: Young stars/cold clumps recognizable but interaction/assembly/galaxy wording unreliable.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þau vildu rannsaka samhliða áhrif á þá yngri stjarnafélagi og kaltum klumpum sem var að samfylgja í þessarir fyrstu galænir.

</details>

<details><summary>development_review #167 · A · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eea:15

English: Where studies are conducted using active substance produced in the laboratory or in a pilot plant production system, the studies must be repeated using active substance as manufactured, unless it can be justified that the test material used is essentially the same for the purposes of environmental testing and assessment.

Reference (shown after audit): Ef rannsóknir eru gerðar með því að nota virkt efni sem er framleitt á rannsóknarstofu eða í tilraunaframleiðslukerfi verður að endurtaka rannsóknirnar með því að nota verksmiðju-framleitt virkt efni, nema hægt sé að færa rök fyrir því að prófunarefnið sem er notað sé í megindráttum hið sama og er notað við umhverfsirannsóknir og umhverfismat.

Review: Pilot production and repeat-study/exception requirements not faithfully retained.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Ef rannsóknir eru framkvæmd með virkum efni sem framleidd er í rannsóknaraðstöðvar eða í rannsóknaraðstæði sem er notað í prófunarstörfi, verða þær endurnýja með því að nota virkum efni í viðkomandi hætti nema til réttar sé greint að prófunarfjöldaði sem notuð er sé framleiðslaður og hægt sé að hlýfti hennar í sér að hanna umhverfisreikningar og úttekin.

Candidate 1: Ef rannsóknir eru gert með virkum efni sem verður fram í rannsóknaráætluninni eða í rannsóknarstofu skal að röksett rannsóknir gera sér neinu með virkum efni og þegar ekki er hægt að ræða að prófunarvökturinn sé í grundvelli aðra sama efni við umhverfisrannsóknir og mat á henni.

Candidate 2: Ef rannsóknir eru gerðar með virka efni sem er framleitt í rannsóknarstofu eða í íæxlustýringustörfunni skal endurskoða þær með virku efni í þeinni tilgangi, nema valin sé að því tilkynnt sé hægt að ræða að prófunargreina sem notað er sé tiltekinn af samkvæmum tilgangi fyrir umhverfisprufanir og mælingar.

Candidate 3: Ef rannsóknir eru framkvæmd með virka efni sem eru framleidd á vinnslustöðnum eða í fylgustæðan framleiðslusjármörkin skal endurskoða rannsóknina með virku efni sem framleiðið er og ekki er hægt að ræða afhenda að nýtingar efnið sé í öllum kringum aðstæðum jafnaði í lífaverndarprufunum og mati.

Candidate 4: Ef rannsóknir eru framkvæmd með virka efni sem er framleidd á rannsóknaráðstöðinu eða í síðastjórartæki efniframleiðsluvettvangi þá verður þær endurskoðuð með virku efni eins og þetta er framleidd, nema staðfest sé á að prófunarefnið, sem notuð er, sé í grundvelli sambærileg fyrir aðgerðir til að ræða umhverfisráðstöfun og mat.

Candidate 5: Ef rannsóknir eru framkvæmd með virkan efni sem er framleidd í rannsóknarkerfi í rannsóknarkerfi í fæðu eða í rannsóknarkerfi með áætlaðri framleiðslu skal endurskoða þær með virkanu efni sem er framleidd, nema má rökstuddið að kostið prófunarvöð við referið sé í grundvelli öðru efni sem til þess er núllt meginlega samsvarandi í þá huga að prófun í nytjaherillinu og á mat.

Candidate 6: Ef rannsóknir geraðar eru með virka efni sem framleidd er í stofninu eða í þýðingu til ákvarðaðs efni, verður að endurskoða þær með virka efni sem framleidd er og ekki þegar í þátt er grein fyrir að prófunarvirkjunin sem notaður er sé í grundvelli samsvarandi fyrir eftirlit með umhverfið og mat.

Candidate 7: Ef rannsóknir eru framkvæmd með virkum efnum sem eru framleidd á vettvangi eða í annarrar stjórnunarkerfis, skal endurskoða rannsóknina með virkum efnum eins og þau eru framleidd, nema framleiðandi geti ræði áður og skýtlað það á áður að tilraunasmittin, sem notuð er, sé í almennum sambandi við umhverfisrannsóknir og mat.

</details>

<details><summary>development_review #168 · t2999996 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eso:919

English: "Thanks to several giant telescopes currently under construction, including ESOs E-ELT and the NASA/ESA/CSA James Webb Space Telescope due to launch for 2018, we will soon be able to study the atmospheric composition of these planets and to explore them first for water, then for traces of biological activity.

Reference (shown after audit): „Þökk sé nokkrum risasjónaukum sem nú eru í smíðum, þeirra á meðal E-ELT sjónauka ESO og James Webb geimsjónauka NASA; ESA og CSA sem skotið verður á loft árið 2018, munum við fljótlega geta rannsakað efnasamsetningu lofthjúpa þessara reikistjarna og kannað þær fyrst í leit að vatni og síðan leitað að merkjum um líf.

Review: Opening construction/launch and atmospheric-composition clauses are corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: „Takinn hefur nokkrar stóra sjónaukar sem eru í framhaldshús, þar með talið ESOs E-ELT og James Webb Space Telescope NASA/ESA/CSA sem er til að fara í reynd árið 2018, munum við náið nánar á geimkemmdi þessara planeta og rannsaka þær fyrst með vatni, síðan með einkennum líffræðilegra virkni.

</details>

<details><summary>development_review #169 · t2999996 · G8 · technical_medium · P</summary>

Source ID: p13official21:dev:eea:1914

English: This Regulation shall enter into force on the third day following that of its publication in the Official Journal of the European Union.

Reference (shown after audit): Reglugerð þessi öðlast gildi á þriðja degi eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.

Review: Exact source/hypothesis semantic reuse from card91: Candidate5 preserves third-day entry into force after Official Journal publication.

Inspected original candidate indices: [4]; confirmed correct indices: [4]

Candidate 0: Reglugerð þessi öðlast gildi fyrri daginn eftir að hún er birt í Stjórnartíðindum Evrópusambandsins.

Candidate 1: Reglugerð þessi öðlast gildi síðar á þriðju degi eftir birtun hennar í Stjórnartíðindum Evrópusambandsins.

Candidate 2: Reglugerð þessi öðlast gildi þriðja daga eftir greiningu hennar í Stjórnartíðindum Evrópusambandsins.

Candidate 3: Reglugerð þessi öðlast gildi fyrri um þriðju degi eftir birtu henni í Stjórnartíðindum Evrópusambandsins.

Candidate 4: Reglugerð þessi öðlast gildi þriðju degi eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.

Candidate 5: Reglugerð þessi öðlast gildi á þriðja degi eftir birtun hennar í Stjórnartíðindum Evrópusambandsins.

Candidate 6: Reglugerð þessi öðlast gildi fyrir þriðja dag eftir birtun hennar í Stjórnartíðindum Evrópusambandsins.

Candidate 7: Reglugerð þessi öðlast gildi þriggja daga eftir talið er hún birt í Stjórnartíðindum Evrópusambandsins.

</details>

<details><summary>development_review #170 · t2999996 · greedy · technical_short · P</summary>

Source ID: p13official21:dev:ema:1100

English: If you miss a dose, take your next dose as scheduled.

Reference (shown after audit): Ef þú gleymir skammti skaltu taka næsta skammt eins og venjulega.

Review: Missed dose and next scheduled dose retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Ef þú gleymir skammtinum, taktu næsta skammt samkvæmt áætlun.

</details>

<details><summary>development_review #171 · t2999996 · G8 · technical_medium · P</summary>

Source ID: p13official21:dev:eso:70

English: This is only the sixth of these huge storms to be spotted since 1876.

Reference (shown after audit): Stormurinn er sá sjötti sem menn verða vitni að á Satúrnusi frá árinu 1876.

Review: Candidate6 retains only sixth huge storm detected since1876 despite inflection.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [6]

Candidate 0: Þetta er aðeins sexustur af þessum stórum andrúm sem koma fram síðan 1876.

Candidate 1: Þetta er bara sexstríðarinn í þessu fjarlægnum stormi sem sást síðan árið 1876.

Candidate 2: Þetta er aðeins sjöttni af þessum stórum stormum sem komu fram frá 1876.

Candidate 3: Þetta er aðeins sjötta af þessu stórum stormi sem greint hefur verið í sér frá árið 1876.

Candidate 4: Þetta er aðeins sjötta þessar eirir sinna sem fyrir sé sýnt í gegnum ár frá 1876.

Candidate 5: Þetta er aðeins sjökthugbúið stormið sem gegnast fyrir 1876.

Candidate 6: Þetta er aðeins sjötta þessara miklum storma sem greinst hefur eftir 1876.

Candidate 7: Þetta er aðeins sex af þessum umræðum sem tækt hefur verið síðan 1876.

</details>

<details><summary>development_review #172 · t2999996 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eso:323

English: They were able to make the sharpest direct observation ever , of the centre of a distant galaxy, the bright quasar 3C 279, which contains a supermassive black hole with a mass about one billion times that of the Sun, and is so far from Earth that its light has taken more than 5 billion years to reach us.

Reference (shown after audit): Þannig tókst þeim að gera skörpustu beinu mælingarnar sem gerðar hafa verið á miðju fjarlægrar vetrarbrautar, bjarta dulstirninu 3C 279 sem geymir risasvarthol sem er eins milljarðs sinnum massameira en sólin og er svo langt frá jörðinni að ljós þess er 5 milljarða ára að berast til okkar.

Review: Billion is changed to million for both mass and light-travel time.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þau komu að gera skarpsmári beinu sjónauki á miðju fjarlægri vetrarbrauta, 3C 279, sem er björtur kvarnir 3C 279, sem inniheldur öflugan massamikla svarthol með massi um milljóna tímann stærri en sólin og er svo fjarlægt frá Jörðinni að ljósinn hennar hefur tekið meira en 5 milljón ára til okkar.

</details>

<details><summary>development_review #173 · t2999996 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eso:775

English: A team of astronomers, led by Istvan Dékány of the Pontificia Universidad Católica de Chile, has now used data from this survey, taken between 2010 and 2014, to make a remarkable discovery - a previously unknown component of our home galaxy, the Milky Way.

Reference (shown after audit): Hópur stjörnufræðinga undir forystu Istvan Dékány við Pontificia Universidad Católica de Chile, notaði gögn úr verkefninu sem aflað var milli 2010 og 2014 og gerði merkilega uppgötvun á áður óþekktu svæði í Vetrarbrautinni okkar.

Review: All candidates corrupt discovery/component/MilkyWay or leading/survey relation; none preserves the whole claim.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Hópur stjörnufræðinga, lögð undir Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notuð gögnum frá þessari yfirríki, sem komu frá 2010 til 2014, til stuttu uppgötvunar - hinn fyrir sig óþekkti hlutur við sjóðinni Vetrarbraut.

Candidate 1: Hópur stjarnvísindamanna, hjá stjörnufræðingum Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notuð gögnum af þessari rannsókn, sem gerðar voru á bilinu 2010 til 2014, til bæði innánlega vörusöfnun og bæði til bæði sérhæfis uppgöngu í heimsstjörnu okkar, Galldrekkjunni.

Candidate 2: Hópur stjörnufræðinga, gefnu félagi Istvan Dékány hjá Pontificia Universidad Católica de Chile, hefur nýlega notið gögnum úr þessari rannsókn, sem gerð var á bilinu 2010 til 2014, til sérstakrar uppgötvunar - aðgang að sér, sem var ekki tilgreint áður, að borginni vetrarbraut, Vetrarbrautinni.

Candidate 3: Hópur stjörnufræðinga, leitt frá Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nýlega notað gögnum úr þessum mælingum, sem gerðar voru á bilinu 2010 til 2014 til að gera mikilvægi upplýsingu - nýtt eining af heimilinu vetrarbrautarinnar, Vetrarbrautinu.

Candidate 4: Hópur stjörnufræðinga, yfirhugaður Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notað gögn úr þessari rannsókn, sem gerður var á tímabilið 2010-2014, til að ná til mikiðar uppáhaldsins - einn áletrunarmiði víðtæku Vetrarbrautarinnar.

Candidate 5: Hópur stjörnufræðinga, leitur eftir Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur notuð gögn úr slíku losunar, sem gerðar voru á bilinu 2010-2014, til að koma að frábendingi sem við höfum ekki sést áður - aðrar hluti um heimaliku svæðisins, Vetrarbrautar.

Candidate 6: Hópur stjörnufræðinga, gefinn um stjörnustarfsemi af István Dékány, Pontificia Universidad Católica de Chile, hefur nýlega notað gögn úr þessu skoðun, sem tekin voru á bilinu 2010-2014, til þess að ná undir mikill uppgötvun - aðgang til þess fyrirleitt þols sem er á móti viðfundi.

Candidate 7: Hópur stjörnufræðinga, leitt af István Dékány við Pontificia Universidad Católica de Chile, hefur nú notuð niðurstöður úr mælikvarðanum, sem tókjast milli 2010 og 2014, til að gera ósæmu uppgötvun - aðra, fyrir hliðsjónu, hlutu vetrarbrautarnar okkar.

</details>

<details><summary>development_review #174 · t2999996 · greedy · technical_short · F</summary>

Source ID: p13official21:dev:eea:1991

English: Paragraph AG27 is amended and after paragraph AG29, paragraph AG29A is added.

Reference (shown after audit): Ákvæðum liðar AG27 er breytt og á eftir lið AG29 er lið AG29A bætt við.

Review: The AG prefixes identifying the amended paragraphs are lost.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Í 27. lið er breytt og eftir 29. lið bætist við 29. lið A.

</details>

<details><summary>development_review #175 · t2999996 · G8 · technical_short · F</summary>

Source ID: p13official21:dev:eea:1461

English: All industrial uses of gas are considered.

Reference (shown after audit): Öll notkun á gasi í atvinnurekstri er talin með.

Review: No candidate preserves industrial uses being considered; closest5 substitutes work in general.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Í þeim tali er um öll starfsmenyki gasins.

Candidate 1: Ífram er að taka til allra gjafir tekjur í gjöf.

Candidate 2: Í öllum vinnuauðkenni gas.

Candidate 3: Takmörkuð er allar notkun gass í vinnu.

Candidate 4: Tilgreind eru allar notkun öndu í rekstri.

Candidate 5: Taka er mið af öllum notkun gass í vinnunni.

Candidate 6: Tilkynnt er um öllum tæknikerfinu, sem meðferð er fyrir gjöfinni, um gas.

Candidate 7: Tilgreint er um öll atvinnuauðgjöf gasins.

</details>

<details><summary>development_review #176 · t2999996 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eso:206

English: The survey was sensitive to planets between 75 million kilometres and 1.5 billion kilometres from their stars (in the Solar System this range would include all the planets from Venus to Saturn) and with masses ranging from five times the Earth up to ten times Jupiter.

Reference (shown after audit): Mælingarnar voru næmar fyrir reikistjörnum sem eru milli 75 milljón til 1,5 milljarða km frá móðurstjörnunum (í sólkerfinu okkar inniheldur þetta fjarlægðarbil allar reikistjörnur frá Venusi til Satúrnusar) og frá fimm sinnum massameiri en jörðin upp í tíu sinnum massameiri en Júpíter.

Review: All candidates corrupt billion scale and/or mass bounds and objects.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Skoðunin hefur verið sérfræðilega til stjörnum á milli 75 milljón km og 1,5 milljón km frá stjörnunum (í Jörðavetrarbrautinni umfarið allar stjörnurinnar frá Vensu yfir í Saturn) með massamagni á bilinu frá fimm sinnum jörðunum til tíu sinnum Júpíturnum.

Candidate 1: Skýrslan var næmur fyrir plöntum á bilinu 75 milljón km til 1,5 milljón milljón km frá stjörnunum (í sólkerfinu birta allar plönturnar frá Venus til Saturn) og massaverk fyrir allar plönturnar var á bilinu fyrir fimm sinnum jörðina upp á tíu sinnum Júpíturni.

Candidate 2: Skoðunin var næmur til reikistjarna milli 75 milljón km og 1,5 milljón km frá stjörnunum (í sólarkerfinu fingi hún öll reikistjörnurnar frá Venus til Saturns) og massahófur sem fengur var fyrir sig fimm sinnum gildi Bergsins og títtinga í tíu sinnum gildi Júpítrs.

Candidate 3: Til greiningar var næm við reikistjörnur sem eru á bilinu 75 milljón km til 1,5 milljón km frá stjörnunum (í sólkerfinu catches tilvísunin við öll reikistjörnurnar frá Venus til Saturn) og massakvörðun var á bilinu fimm sinnum jörði til tennum Júpítr.

Candidate 4: Skoðuninni var næm við reikistjörnur sem eru á bilinu 75 milljón km til 1,5 milljón króna frá stjörnunum (í sólarbrautinni í þessa bil er allan reikistjörnin frá Venus til Saturn) og með þyngd á bilinu fyrir fjögurra gildi jörðar til tíu gildum Júpítra.

Candidate 5: Skoðanirnar höfðu nákvæmni við reikistjörnu sem eru á milli 75 milljón km og 1,5 milljón km frá stjörnunum (í Jörðareikjunni gætu nar einnig reikistjörnin af Venus til Saturn) og eru með massa á milli fimm sinna jörða og tíu jörða.

Candidate 6: Rannsóknin var nægileg fyrir reikistjörnur á bilinu 75 milljón kílómetra og 1,5 milljón milljón kílómetra frá stjörnunum (í sólarráðinu nefnar allar reikistjörnurnar frá Vensu til Saturn) og með massar á bilinu frá fimm sinnum þjóðinu í Júpíturnum til upp í tíu sinnum.

Candidate 7: Skoðunin var meðvæn fyrir reikistjörnur á bilinu 75 milljón km til 1,5 milljón km frá stjörnunum (ég hafi í sólkerfinu fengið allar reikistjörnurnar frá Vensu til Sáterni), með vettvangi úr fimm til tíu gildum jörðu.

</details>

<details><summary>development_review #177 · t2999996 · G8 · technical_short · U</summary>

Source ID: p13official21:dev:eea:609

English: Special payments for shift work.

Reference (shown after audit): Sérstakar greiðslur vegna vaktavinnu.

Review: Payments retained in several; shift-work wording is nonstandard and cannot confidently confirm a fully correct candidate.

Inspected original candidate indices: [0, 1, 2, 3, 4, 6, 7]; confirmed correct indices: []

Candidate 0: Sérstök greiðslur við skiptatíma.

Candidate 1: Sérstök greiðslur fyrir skiptaríki.

Candidate 2: Sérstakt greiðslur í starfsmeðaltali.

Candidate 3: Sérstök borgun vegna skipti í vinnu.

Candidate 4: Sérstök greiðslur fyrir starfsstöðum.

Candidate 6: Sérstakar greiðslur fyrir stöðugir verk.

Candidate 7: Sérstakar greiðslur fyrir skipta verki.

</details>

<details><summary>development_review #178 · t2999996 · greedy · technical_short · F</summary>

Source ID: p13official21:dev:ema:704

English: The most frequently reported adverse reaction was acne, which was generally mild.

Reference (shown after audit): Algengasta aukaverkunin sem greint var frá er þrymlabólur (acne), sem voru venjulega vægar.

Review: Acne is replaced by kúu; the named adverse reaction is not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Algengasta aukaverkunin sem greint var frá var kúu, sem var yfirleitt væg.

</details>

<details><summary>development_review #179 · t2999996 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eea:1194

English: It should provide the Commission and the Member States with objective, reliable and comparable information and data on maritime safety and on ship pollution prevention to enable them to take any necessary initiatives to enhance the measures in place and to evaluate their effectiveness.

Reference (shown after audit): Henni ber að sjá framkvæmdastjórninni og aðildarríkjunum fyrir hlutlægum, áreiðanlegum og sambærilegum upplýsingum og gögnum um siglingaöryggi og varnir gegn mengun frá skipum til að gera þeim kleift að vinna hvers kyns nauðsynleg framtaksverkefni til að efla þær ráðstafanir sem gerðar hafa verið og að meta skilvirkni þeirra.

Review: Objective/reliable/comparable information and ship-pollution-prevention concepts are corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Hún skal veita framkvæmdastjórninni og aðildarríkjunum vísanir og upplýsingar sem eru áframhaldandi, öruggar og jafngiltar um öryggi á sjávarbærum og um að forðast losun í skipum til þess að hún geti tekið nauðsynlegar aðgerðir til að auka ráðstafanir sem eru í gildi og meti árangur þeirra.

</details>

<details><summary>development_review #180 · t2999996 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eea:281

English: The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.

Reference (shown after audit): Fjárhæð þeirra fyrrnefndu (síðarnefndu) sem eru jafnaðar á móti þeim síðarnefndu (fyrrnefndu) í tilteknum binditímaflokki skal teljast jafnaðar stöður þess flokks en eftirstöðvar langra eða stuttra staðna telst ójöfnuð staða þess flokks.

Review: Maturity band, former/latter relation and residual position are mistranslated.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Hlutfall fyrri (sáttmálans) sem samsvarar sáttamálum sínum í tilteknu vinnuþætti skal vera samsvarandi stöður í þeirri vinnuþætti, en hlutabúnaður á lengi eða stuttu tíma skal vera ósamsvarandi stöður í sama vinnuþætti.

</details>

<details><summary>development_review #181 · t2999996 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eea:574

English: All rear-window, roof-panel and partition switches intended for use by occupants in the rear of the vehicle shall be capable of being switched off by a driver-controlled switch which is located forward of a vertical transverse plane passing through the R points of the front seats.

Reference (shown after audit): Allir rofar í hliðarrúðum að aftan, þaklúgum og skilrúmum sem farþegum baka til í ökutækinu er ætlað að nota skulu gerðir með þeim hætti að unnt sé að rjúfa straum til þeirra með rofa sem ökumaður stjórnar og er staðsettur framan við lóðrétt þverplan sem gengur í gegnum R-punkta framsætanna.

Review: All corrupt controls and specified geometric driver-switch location; some reverse front/rear or on/off.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Allir plássskiptir í bakgondunum, tegliðgu eða vekjudegiinn eftir rútinu sem ætlaðir eru innlendum í rútinu á vagninu, skulu fylgja að meðferðum handa handstjórnandi skiptu sem er staðsett fyrir viðri hlið yfir lágkvennsri tegundra velfær frá deilunum í veflungunum í fyrstu sætur.

Candidate 1: Allir opinum-og meðalvinna skiptir, sem gefnar eru út á bak hluta ökutækisins, skulu vera færir til að skipta á með skipti sem umhverfur er í skipti með ökumað.

Candidate 2: Allir slíkar snjallavirkir á aftursvæði, fjallvirkju eða ristilvirkju sem notaðir eru af innbyggjendum í aftur svæði ökutækisins, eiga að vera að slíkum snjálfavirkum snjallavirkjum sem beitt er við á borð við hlutaðeigandi veggir og er búin frá hlutar fyrir fjölskyldu.

Candidate 3: Allar höðvaka, loftmælin og partína, sem ætlaðar eru til notkunar um eykil í eftirbilinu, skulu geta verið hægt að slökkva með þeim hlévigum sem stjórnmandur tekur stjórn á og er í framan á flatri yfirgegnum sem fer í R-stöðum á framan hljóðar.

Candidate 4: Hverja afturslögun, skuggaskipti og voru skipti sem ætlaðir eru fyrir notendum á eftirrásum ökutækisins, skulu hafna hægt að slökkva með skipti sem annar eru í stjórn ökutækisins og er meðferðir fyrir gegn hægri, levurlega ás og snúa gegn R stigum í framanstaðum.

Candidate 5: Allar beldir til að setja aftan, eftir húð á rútinu og málur á höfuðsviðum, sem inngjafa einstaklingar á aftan í ökutækinu, skulu geta verið skiptir aftur á með skipti sem er leyft með skipti sem er í stjórn við hendi ökumanns og er í fyrirlaga við hliðsviðinn sem flugi yfir R-stöðum í fyrirsviðum.

Candidate 6: Allir bakglas, tegli og dílslökkur sem ætlaðir eru til notkunar fyrir einstaklinga í framan við ökutæki skulu geta verið slökkt af með skjallu sem einstaklingur hafði takmarka í fyrirriða við lygrarplan sem fer úr R-stigum fyrir sæti.

Candidate 7: Öll bakgluggi, húðafæð og rækur sem ætlað eru til notkunar innsæitöku í aftur af vélinn skal geta verið skiptur á til aftur af skipti sem er fluttur með áhættuvarnir sem er settur fyrir ofan frá lyngir þrúgengu hliðar sem snúa um R-stig innri rúms í skrifstöðum.

</details>

<details><summary>development_review #182 · t2999996 · G8 · technical_short · P</summary>

Source ID: p13official21:dev:eea:922

English: Development of CPE is checked as described in Part I.III.4.

Reference (shown after audit): Fylgst er með því hvort frumuskemmdir verða eins og lýst er í I.III.4.

Review: Candidate0 retains checking development of CPE and the I.III.4 cross-reference; duplicated preposition only.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [0]

Candidate 0: Tilvik um þróun CPE er rannsakað eins og lýst er í í I.III.4.

Candidate 1: Rannsókn á þróun CPE er farið fram samkvæmt grein 4 í III.4. I.h.

Candidate 2: Frekari þroska CPE er lokið eftir þeirri rök sem lýst er í IV. 4. hlið I. hliðar III. þáttar.

Candidate 3: Fylgjar er eftirliti með þróun CPE eins og lýst er í 4. horn I. III. þáttar.

Candidate 4: Framdæmi CPE (continuing parental education) er rannsakað eins og lýst er í III.4. hlið í I. hluta greinar.

Candidate 5: Meðhöndlun á þróun á CPE er gerð samkvæmt grein 4 í III.4. bönd I. hliðar.

Candidate 6: Skoðað er þróun CPE eins og lýst er í III.4. hloð I. lyklans.

Candidate 7: Verið er viss um þróun CPE eins og lýst er í I.III.4.

</details>

<details><summary>development_review #183 · t2999996 · greedy · general · P</summary>

Source ID: p13official21:dev:opensubtitles:1169

English: They're pretty as can be, aren't they?

Reference (shown after audit): Fallegri er ekki hægt að vera, ekki satt?

Review: Pretty/cute and the confirmation question retained; inflection is imperfect.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Þau eru mjög sætir, ekki satt?

</details>

<details><summary>development_review #184 · t2999996 · G8 · technical_short · U</summary>

Source ID: p13official21:dev:eso:491

English: ALMA can observe in different frequency bands.

Reference (shown after audit): ALMA getur gert mælingar á mismunandi böndum.

Review: Candidate0 mentions observing between different frequencies but omits/changes band relation; remaining candidates clearly corrupt it. Cannot confirm full correctness.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: ALMA getur athugað á milli mismunandi tíðni.

Candidate 1: ALMA getur fylgst með framkallargreindum að skugga sem eru í mismunandi fjölbreyttingarbundnum geimsjónum.

Candidate 2: ALMA getur fylgst með öðrum frumunarhliðum.

Candidate 3: ALMA getur fylgst með segðu upp hægða fyrir tilgreiningu.

Candidate 4: ALMA má fara beina í mismunandi framsöfnum.

Candidate 5: ALMA getur mælt í mismunandi fjölda ár.

Candidate 6: ALMA getur fylgt eftir á milli varir í samhliða öryggismæli.

Candidate 7: ALMA getur fylgst með tjörnunum á mismunandi fyrningum.

</details>

<details><summary>development_review #185 · t2999996 · greedy · technical_medium · P</summary>

Source ID: p13official21:dev:ema:1765

English: Take this leaflet or some tablets with you so that your doctor knows exactly what you have taken.

Reference (shown after audit): Hafa skal þennan fylgiseðil eða eitthvað af töflum meðferðis svo læknirinn viti nákvæmlega hvað tekið hefur verið.

Review: Take leaflet/tablets so doctor knows what was taken; minor inflection only.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Takið þessi fylgiseðil eða töflur með þér svo að læknirinn þekki nákvæmlega hvað þú hefur tekið.

</details>

<details><summary>development_review #186 · t2999996 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eea:1716

English: The competent authorities of Gabon have reacted promptly to these concerns, indicating their commitment to take all measures necessary to implement applicable ICAO standards and enforce compliance with these standards as soon as possible.

Reference (shown after audit): Lögbær yfirvöld í Gabon brugðust tafarlaust við þessum áhyggjum og létu í ljós eindreginn vilja til að gera allar nauðsynlegar ráðstafanir til að koma í framkvæmd gildandi stöðlum Alþjóðaflugmálastofnunarinnar og tryggja að farið yrði að ákvæðum þeirra eins fljótt og auðið er.

Review: Enforcing compliance with ICAO standards becomes following reactions.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Lögbær yfirvöld í Gabón hafa svarað þessum ábendingum tafarlaust og benda til þess að þau séu bundnar til að gera allar nauðsynlegar ráðstafanir til að framfylgja gildandi staðli ICAO og fylgja þeim viðbrögðum eins fljótt og unnt er.

</details>

<details><summary>development_review #187 · t2999996 · greedy · general · F</summary>

Source ID: p13official21:dev:opensubtitles:2508

English: Rose, we have a guest in the living room.

Reference (shown after audit): Rósa, það er gestur í stofunni.

Review: Living room becomes an unspecified room.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Rose, við höfum gest í herberginu.

</details>

<details><summary>development_review #188 · t2999996 · greedy · technical_short · P</summary>

Source ID: p13official21:dev:ema:2013

English: There is no evidence to suggest that eptotermin alfa alters fertility.

Reference (shown after audit): Ekkert bendir til þess að eptotermin alfa hafi áhrif á frjósemi.

Review: No evidence of altered fertility and drug identity retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Ekki er neitt til staðar til að sýna fram á að eptotermin alfa breytir frjósemi.

</details>

<details><summary>development_review #189 · t2999996 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eso:765

English: “If it keeps spinning rapidly it might end its life in one of the most energetic explosions in the Universe, known as a long-duration gamma-ray burst,” says the lead scientist of the project, Hugues Sana, of the University of Leuven in Belgium.

Reference (shown after audit): „Haldi hún áfram að snúast mjög hratt gæti hún endað ævina sem langur gammablossi, ein orkumesta sprenging í alheiminum,“ segir Hugues Sana við Leuvenháskóla í Belgíu sem hafði umsjón með rannsókninni.

Review: All corrupt energetic explosion/long-duration gamma-ray burst and/or rotation condition and attribution.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: „Ef hún helst snúa hratt, kannski hægt að betur enda líf hennar í einu vonum stóru geislun efnis í alheiminu sem kallast langtímagerma- föstu,“ sagði Hugues Sana, leiðandi vísindamannnar á verkefninu, í Leuven-háskóla í Belgíu.

Candidate 1: „Ef það hreyfir hraða um sig, kann að enda lífi sínu í eins af verulegustu mjúksteifjunum í alheiminu, sem kallast lengdar gammalekaflug,“ sagði Hugues Sana, aðalhálfur verkefnisins í Leuven háskóla í Belgíu.

Candidate 2: „Ef hann helst hreyfa hraða gæti hann farið fyrir létinu af einu af mesta kjarnasprautum í alheiminu, sem hefur þýðið lengdarsamprunnar“, sagði letri vísindamaður um verkefnið, Hugues Sana, frá Leuven-universíti í Belgíu.

Candidate 3: „Ef hún hefur styrkur hraða er mögulegt að hún studdi á einu af erfiðasta sprengingunum alheimisins, sem kallast langtíma gama gegnburður,“ sagði Hugues Sana, leiðsögnarhæfileiki verkefnisins, um frá Sturtarháskólanum í Belgíu.

Candidate 4: „Ef það hreyfir hratt getur það endað líf síðarinn í einum langvinnu rassliði úr vetrarbrauta sem kallast langvinn rassliður,” sagði Hugues Sana, leiðbeinandi vísindamaður á verkefnið á vísindagardinu í Leuven í Belgíu.

Candidate 5: „Ef það hreyfir sér hratt, getur það fengið einhverju lengstu gamma-losunarins í alheiminu, sem kallast langvarandi gamma-losunarins,“ sagði Hugues Sana, leiðbeinandi vísindamanna á verkefnið, frá Leuven universítíti í Belgíu.

Candidate 6: „Ef það virðist snúast hraðlega kann það að enda lífið í sjónið eins langvarandi gammablárbrot sem er hefði náð í vetrarbraut,“ sagði Hugues Sana, letri vettvangi verkefnisins, frá Leuven-í Belgía.

Candidate 7: „Ef það haldar að snúast hraðlega, getur það komið fyrir í einkennilega segara fyrir sér, sem þjónustu er kallað á móttöku á alheiminu“ segir Hugues Sana, aðalhæfileikarmanninn í verkefninu, sem er stjörnufræðingur í Leuven-í Belíegeiðinu.

</details>

<details><summary>development_review #190 · t2999996 · G8 · technical_medium · P</summary>

Source ID: p13official21:dev:eea:1585

English: The Commission shall submit a final evaluation report at the end of the Programme.

Reference (shown after audit): Framkvæmdastjórnin skal leggja fram endanlega matskýrslu við lok áætlunarinnar.

Review: Candidates0/2/5 retain Commission submitting final evaluation report at programme end.

Inspected original candidate indices: [0, 1, 2, 3, 5, 6, 7]; confirmed correct indices: [0, 2, 5]

Candidate 0: Framkvæmdastjórnin skal leggja fram endanleg matsskýrslu að lokum áætlunarinnar.

Candidate 1: Framkvæmdastjórnin skal leggja fram endanleg mataráðgerð eftir að áætlunin er lokið.

Candidate 2: Framkvæmdastjórnin skal leggja fram endanlega matsskýrslu eftir að áætlunin er lokið.

Candidate 3: Framkvæmdastjórnin skal leggja fram endanlega matsskil á lokum áætluninnar.

Candidate 5: Framkvæmdastjórnin skal leggja fram endanlega matsskýrslu eftir áætlunin er lokið.

Candidate 6: Framkvæmdastjórnin skal leggja fram endanlega ávísað skýrslu að lokum áætlunarinnar.

Candidate 7: Framkvæmdastjórnin skal leggja fram endanlegar matarannsóknarskýrslu eftir lok áætlunarinnar.

</details>

<details><summary>development_review #191 · t2999996 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:ema:1718

English: Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.

Reference (shown after audit): Gjöf edoxabans samtímis P-gp virkjanum rífampisíni leiddi til lækkunar á meðalgildi AUC fyrir edoxaban og styttri helmingunartíma, með hugsanlegri minnkun á lyfhrifum þess.

Review: Possible decreases in pharmacodynamic effects become unspecified possible effects.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Samhliða lyfjagjöf edoxabans og P-gp örvaðs rífampicins leiddi til minnkaðrar meðal AUC fyrir edoxaban og skerðingar helmingunartíma, sem geta haft mögulega áhrif á lyfhrifum.

</details>

<details><summary>development_review #192 · t2999996 · greedy · general · P</summary>

Source ID: p13official21:dev:opensubtitles:996

English: What kind of man would that make me?

Reference (shown after audit): Hvers konar maður væri ég þá?

Review: Exact source/hypothesis semantic reuse from card127: What kind of man would that make me retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Hvers konar maður myndi það gera mig?

</details>

<details><summary>development_review #193 · t2999996 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eea:534

English: Council Directive 74/60/EEC of 17 December 1973 on the approximation of the laws of the Member States relating to the interior fittings of motor vehicles.

Reference (shown after audit): Tilskipun ráðsins 74/60/EBE frá 17. desember 1973 um samræmingu laga aðildarríkjanna varðandi innréttingar vélknúinna ökutækja.

Review: Interior fittings becomes inner phenomena, losing the regulated object.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Tilskipun ráðsins 74/60/EBE frá 17. desember 1973 um samræmingu á lögum aðildarríkjanna varðandi innri fyrirbæri vélkrafta ökutækja.

</details>

<details><summary>development_review #194 · t2999996 · greedy · technical_short · F</summary>

Source ID: p13official21:dev:eea:1461

English: All industrial uses of gas are considered.

Reference (shown after audit): Öll notkun á gasi í atvinnurekstri er talin með.

Review: Industrial uses becomes use at work, losing the specific scope.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Íhugað er allar notkun gass í vinnu.

</details>

<details><summary>development_review #195 · t2999996 · greedy · general · P</summary>

Source ID: p13official21:dev:opensubtitles:3209

English: Because it's not safe there.

Reference (shown after audit): Af því að það er ekki öruggt.

Review: Exact source/hypothesis semantic reuse from card25: Unsafe location retained with awkward grammar.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Það er ekki örugg í því.

</details>

<details><summary>development_review #196 · t2999996 · greedy · technical_medium · U</summary>

Source ID: p13official21:dev:eso:464

English: With an estimated mass of four to five times that of Jupiter, it would be the least massive planet to be directly observed outside the Solar System.

Reference (shown after audit): Massi fyrirbærisins er talinn milli fjórum til fimm sinnum meiri en massi Júpíters, svo hér gæti verið um að ræða massaminnstu reikistjörnu sem ljósmynduð hefur verið fyrir utan sólkerfið okkar.

Review: Mass comparison and observation claim mostly recognizable, but invented mass/superlative wording prevents confident confirmation.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef það er með fjögur til fimm sinnum stærri massafjölda en Júpíter væri það minnst massaverulegur reikistjarnan sem hefur verið tekið beinu sjón af utan sólkerfinu.

</details>

<details><summary>development_review #197 · t2999996 · G8 · technical_medium · P</summary>

Source ID: p13official21:dev:ema:1718

English: Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.

Reference (shown after audit): Gjöf edoxabans samtímis P-gp virkjanum rífampisíni leiddi til lækkunar á meðalgildi AUC fyrir edoxaban og styttri helmingunartíma, með hugsanlegri minnkun á lyfhrifum þess.

Review: Candidate6 retains co-administration, P-gp inducer, decreased mean AUC, shortened half-life and possible reduced pharmacodynamic effects.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [6]

Candidate 0: Samhliða lyfjagjöf edoxaban og P-gp hvötarefnisins rífampicins leiddi til minnkaðs meðaltals AUC fyrir edoxaban og skemmings helmingunartíma, sem gæti hægt að lækka lyfhrifum þess.

Candidate 1: Samhliða lyfjagjöf edoxaban og P-gp örvaðs rifampicins leiddi til minnkaðrar meðal AUC fyrir edoxaban og skerta helmingunartíma, sem geta áttað minnkuð lyfhrif.

Candidate 2: Samtímis gjöf edoxabans og P-gp örva, rifampicins, leiddi til minnkar á meðal AUC fyrir edoxaban og minnkaðs helmingunartíma, sem gæti skerðað lyfhrifum.

Candidate 3: Samhliða lyfjagjöf edoxabans og P-gp örva rifampicins leiddi til minnkaðs AUC fyrir edoxaban og minnkaðs helmingunarsíðu, sem hugsanlega leikur á að færi lyfhrifum eins.

Candidate 4: Samhliða lyfjagjöf edoxabans og P-gp örva (rifampicins) leiddi til minnkaðs meðal AUC fyrir edoxaban og skerðingar helmingunartíma, sem gæti haft mögulega áhrif á lyfhrif.

Candidate 5: Samhliða lyfjagjöf edoxabans og P-gp örvaðar rifampicins leiddi til minnkunar á meðal AUC fyrir edoxaban og skerðingar á helmingunartíma, í tengslum við hugsanlega minnkun á lyfhrifum.

Candidate 6: Samtímis gjöf edoxaban með P-gp örva rifampicini leiddi til minnkaðs á meðal AUC fyrir edoxaban og styttingar á helmingunartíma, sem hugsanlega leiddi til minnkaðs lyfhrifins.

Candidate 7: Samhliða lyfjagjöf edoxabans og P-gp örva rífampicins leiddi til minnkaðs meðaltals AUC fyrir edoxaban og styttrar helmingunartíma, sem geta orðið minnkað lyfhrifinn.

</details>

<details><summary>development_review #198 · t2999996 · greedy · general · P</summary>

Source ID: p13official21:dev:opensubtitles:1012

English: I'll do whatever you ask.

Reference (shown after audit): Ég geri hvað sem þið viljið.

Review: Promise to do whatever is asked retained despite tense/inflection.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Ég geri hvað sem þú baðir.

</details>

<details><summary>development_review #199 · t2999996 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eso:726

English: They wanted to study the interaction between a young generation of stars and the cold clumps that were assembling into these first galaxies.

Reference (shown after audit): Stjörnufræðingarnir vildu rannsaka víxlverkunina milli ungrar kynslóðar stjarna og köldu kekkjanna sem voru að safnast saman í þessum fyrstu vetrarbrautum.

Review: Young generation of stars becomes star formations; assembling into galaxies becomes already assembled in them.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þau vildu rannsaka milliverkun á ungu stjörnumyndunum og kaltum klumpum sem voru samanbúin í þessum fyrstu vetrarbrautum.

</details>

<details><summary>development_review #200 · t2999996 · G8 · technical_short · U</summary>

Source ID: p13official21:dev:eea:2037

English: Those criteria should not be considered to be exhaustive.

Reference (shown after audit): Þessar viðmiðanir skulu ekki teljast tæmandi.

Review: Several render exhaustive as perfect/complete. Cannot confidently certify the intended non-exhaustiveness distinction.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Einnig skal ekki taka þessi viðmiðanir sem fylgja alveg.

Candidate 1: Þessi viðmiðanir skulu ekki teljast nákvæmar.

Candidate 2: Ekki skal telja þessar viðmiðanir fullkomlínar.

Candidate 3: Ekki skal telja þessi viðmiðanir fullkomi.

Candidate 4: Ekki skal telja þessar viðmiðanir fullkomnir.

Candidate 5: Ekki skal telja þessar viðmiðanir fullkomin.

Candidate 6: Sem ekki séu upplýsandi skal ekki telja þessi viðmiðanir fullkomin.

Candidate 7: Ekki skal telja þær viðmiðanir alveg upplaus.

</details>

<details><summary>development_review #201 · t2999996 · G8 · technical_medium · P</summary>

Source ID: p13official21:dev:eea:85

English: For the estimation of these concentrations all relevant information on the plant protection product and on the active substance must be taken into account.

Reference (shown after audit): Við mat á framangreindum styrk ber að taka allar viðeigandi upplýsingar um plöntuvarnarefnið og virka efnið til greina.

Review: Candidate7 preserves concentration estimation and taking all relevant plant-protection-product/active-substance information into account.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [7]

Candidate 0: Til að áætla niðurstöður við þessar styrkur verður að taka tillit til allra viðeigandi upplýsinga um plöntuvarnarefnið og virka innihaldsefnið.

Candidate 1: Við mat á þessum styrk á að taka yfir allar þær upplýsingar sem tengjast vörublöðvörn og virka innihaldsefnið.

Candidate 2: Til áætlunar á þessum styrk, gilda allar viðeigandi upplýsingar um plöntuverndar lyf og virka efnið.

Candidate 3: Vegna matar á þessum styrkur áður sem meðferð er beitt verður að taka í tillit til allra viðeigandi upplýsinga um plöntuverndarvörn og virka efnin.

Candidate 4: Við mat á þessum styrkleika skulu taka til athygli á allar viðeigandi upplýsingar um plöntuvarnarefnið og virka efnin.

Candidate 5: Vegna matar á þessum styrkleikum verður að taka tillit til allra viðeigandi upplýsinga um plöntsöng og virka innihaldsefnin.

Candidate 6: Við áætlanir á þessum þéttni skulu taka tillit til allrar viðeigandi upplýsinga um plöntuhem ertu og virku innihaldsefnin.

Candidate 7: Við mat á þessum styrk skulu taka til athygli allar viðeigandi upplýsingar um plöntuverndarlyf og virka efnið.

</details>

<details><summary>development_review #202 · t2999996 · greedy · technical_short · U</summary>

Source ID: p13official21:dev:eso:768

English: Both components are classed as O-type stars.

Reference (shown after audit): Báðar stjörnurnar eru af O-gerð.

Review: Both objects classified as O stars is recognizable, but component is rendered ingredient and the technical relation is uncertain.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Bæði innihaldsefnið er flokkt sem O- stjörnur.

</details>

<details><summary>development_review #203 · t2999996 · G8 · technical_medium · P</summary>

Source ID: p13official21:dev:ema:1582

English: The treatment-free period, however, should take into account the pharmacological properties of the products used previously.

Reference (shown after audit): Meðferðarlausa tímabilið verður þó að taka mið af lyfjafræðilegum eiginleikum lyfja sem voru notuð áður.

Review: Candidate6 conveys period without treatment and consideration of pharmacological properties of previously used drugs despite rough case/word order.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [6]

Candidate 0: Meðan á meðferðarfrasluminni stendur skal íhuga lyfjafræðilega eiginleika lyfju sem notað er áður.

Candidate 1: Meðferðarframanstundin skal þó taka tillit til lyfjafræðilegra eiginleikanna tilneyttu lyfja.

Candidate 2: Meðferðarframtíminn skal þó taka tillit til lyfjafræðilegra eiginleika lyfja sem notaðir hafa verið áður.

Candidate 3: Meðferðarfjöldaði skal þó hafa í huga lyfjafræðileg eiginleikar lyfjanna sem notaðir hafa verið áður.

Candidate 4: Meðferðarframanum skal því athugasemdir til hvað varðar lyfjafræðilega eiginleikar lyfinna sem notaðir voru áður.

Candidate 5: Meðferðarframsýni þótt skal íhuga lyfjamengun lyfja sem notaðir voru áður.

Candidate 6: Meðan án meðferðar tímann skal hafa í huga lyfjafræðileg eiginleikar lyfjanna sem notað voru áður.

Candidate 7: Meðferðarfraslengdinni skal þó íhuga lyfjafræðilegar eiginleikar lyfinna sem notuð hefur verið áður.

</details>

<details><summary>development_review #204 · t2999996 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eea:281

English: The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.

Reference (shown after audit): Fjárhæð þeirra fyrrnefndu (síðarnefndu) sem eru jafnaðar á móti þeim síðarnefndu (fyrrnefndu) í tilteknum binditímaflokki skal teljast jafnaðar stöður þess flokks en eftirstöðvar langra eða stuttra staðna telst ójöfnuð staða þess flokks.

Review: All corrupt maturity band/former-latter matching and residual long/short-position definition.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Skömmtur af því (því sem er síðasta sem), sem staðfestur fyrir síðasta (því sem er fyrsta) í tilteknu þurrðarfar, skal vera staðallir í þeirri far, sem óstaðaðir langa eða stór og lágar staðaliðið skal vera óstaðað staðaliði í sama þurrðarfar.

Candidate 1: Hlutfall fyrri (sári) sem fyrirbyggja sér sári (fyrri) í tilteknu útbrotserfi skal vera sári í því útbrotserfi, þar sem óbillaður lengur eða stuttur ástand ásættast í sama útbrotserfi.

Candidate 2: Hlutfall fyrstu (sá eftirfarandi) sem samsvarar sá eftirfarandi (fyrsti) í tiltekinni þroskaþyngd skulu vera samsvarandi staðsetningar í þessum þroskaþyngdina en hlutabúnaður til biliðar eða skuldbandið skulu vera ósamsvarandi staðsetningar í sama þroskaþyngd.

Candidate 3: Skammtur af þeim sem eru upptekin fyrir (síðar) af þeim sem eru upptekin fyrir (síðar) í viðkomandi ákvörðunarhópi skal vera upptekin staðan í þeim hópi, en eftirskipti langa eða skorta skal vera upptekin staðan í sama hópi.

Candidate 4: Magn miðla (frummið) sem samhæft er af síðari (fyrri) miðla (frummið) yfir í viðkomandi vörnaklófa skal vera samhæft staður í þeirri klófi, en ósamhæft staður yfir í sömu klófi skal vera staður yfir á milli.

Candidate 5: Fjöldi framskeðinnar (-fylginnar) sem samsvarar framskeðinni (-fylginni) í við ákvörðuðum blöndu skal vera samhæft stað (jaður), samanborið með því unnt er, sem samsvarandi staður, en fjölda eftirfarandi staða (eða endurstaða) á sama blöndu skal vera ósamsvarandi staður.

Candidate 6: Stöð fanar (látara) sem upptalta eru á meðan viðkomandi stöðvar eru í stöðu á viðkomandi stigsástanda eða stöðvar sem eru ekki upptala á viðkomandi stigsástandi skal vera staðstillar stöður í stigsástandinu, en áframhaldandi stöður sem ekki er upptala á viðkomandi stigsástandi skal vera ekki staðstillar stöður á viðkomandi stigsástandi.

Candidate 7: Hlutfall fyrri (sáttasamræmkaðri) eldri (sáttasamræmkaðra) er samsvarar sáttamál samsvarandi (sáttasamræmkaðri) í tilteknum meginþolarmálum skal vera samsvarandi stöður í því meginþölmum, en hlutfall eðlilega langa eða stuttar stöðu skal vera ósamræmd stöður í sambærilegum meginþölmum.

</details>

<details><summary>development_review #205 · t2999996 · G8 · technical_short · P</summary>

Source ID: p13official21:dev:ema:1192

English: It is used to prevent pregnancy.

Reference (shown after audit): Lyfið er notað til að koma í veg fyrir þungun.

Review: Exact source/hypothesis semantic reuse from card63: Candidate2 correctly states use to prevent pregnancy.

Inspected original candidate indices: [2]; confirmed correct indices: [2]

Candidate 0: Hann er notað til að koma í veg fyrir þungun.

Candidate 2: Það er notað til að koma í veg fyrir þungun.

Candidate 5: Það er notað til að forðast þungun.

</details>

<details><summary>development_review #206 · t2999996 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:eea:15

English: Where studies are conducted using active substance produced in the laboratory or in a pilot plant production system, the studies must be repeated using active substance as manufactured, unless it can be justified that the test material used is essentially the same for the purposes of environmental testing and assessment.

Reference (shown after audit): Ef rannsóknir eru gerðar með því að nota virkt efni sem er framleitt á rannsóknarstofu eða í tilraunaframleiðslukerfi verður að endurtaka rannsóknirnar með því að nota verksmiðju-framleitt virkt efni, nema hægt sé að færa rök fyrir því að prófunarefnið sem er notað sé í megindráttum hið sama og er notað við umhverfsirannsóknir og umhverfismat.

Review: No candidate preserves pilot-plant production plus the full justified environmental-equivalence exception.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Ef rannsóknir eru framkvæmdar með virkum efni sem framleitt er í rannsóknarstofu eða í flagna kemmtustóla skal endurskoða rannsóknina með virkum efnið, samkvæmt framleiðslum áræði fyrir virk efnið, nema við eftirkvæði geti komið fram á að prófunarinnihaldsefnið er í alvöru svipað fyrir umhverfisskrutningu og mat á umhverfisins.

Candidate 1: Ef rannsóknir eru gert með virkum efni sem framleidd er í rannsóknaráðstöðu eða í rannsóknarstofum, skulu rannsóknirnar endurtekin með virkum efnum eins og þau eru framleidd, nema það sé greinilegt að prófunarinnihaldsefnið, sem notað er, sé næstum svipuð fyrir umhverfisrannsóknir og mat.

Candidate 2: Ef rannsóknir eru gerðar með virkum efni sem framleitt er í rannsóknartegundum eða í rannsóknartegundum í rannsóknarstofu verður að endurtaka rannsóknirnar með virkum efnum eins og þau eru framleidd, nema valdið sé á grundvelli þess að prófunarvörunin er í sambandi með umhverfisrannsóknir og við mat á umhverfið.

Candidate 3: Ef rannsóknir eru framkvæmdar með virkum efni sem framleitt er í rannsóknarkerpi eða í rannsóknarstofu, gerast þær endurtaka með virkum efni sem framleitt er, nema það sé greinilegt að prófunarinnihaldsefnið sé í raun svipuð til þess að gefast sé í rannsóknir á umhverfisástandi.

Candidate 4: Ef rannsóknir eru gerðar með virkum efni sem framleiðir er í rannsóknarkerfi í rannsóknarkerfi síðan hefur verið sett á eða í rannsóknarkerfi í rannsóknarkerfi síðan hefur verið sett á, skulu rannsóknirnar endurtakið með virkum efni eins og það er framleiðið, nema hægt sé að ræða að tilrauninu sem er notað er sé að essi eingöngu sambærilegt á þýðingu fyrir um rannsóknir á umhverfi.

Candidate 5: Ef rannsóknir eru gerðar með virka efninum, sem framleitt hefur verið í rannsóknarstofunni eða í rannsóknarskírði með lyfjaskiptum, skulu rannsóknirnar endurtakið með virku efnið eins og það er framleitt, nema má rökseiga að prófunarinnu sé í alvöru sömu til þess að rannsaka umhverfið.

Candidate 6: Ef verkefnið er gert með virku innihaldsefninu sem framleiðið er í rannsóknarskýrslunni eða í rannsóknaræði, þarf að endurtaka rannsóknina með virku innihaldsefninu sem framleiðið er, nema rétt sé kallað á að tilstilli að mismunandi virku innihaldsefninu sé í öllu orkun til að framkvæma rannsókn á umhverfið og meta á það.

Candidate 7: Ef rannsóknir eru gerðar með virka efni sem framleiðið er í rannsóknastofunni eða í áætlunarrannsóknarstjórn, þarf að endurtaka rannsóknina með virku efni eins og það er framleiðið, nema ótímis sé hægt að ræða að prófunarmattið sem notað er sé í aðtraði sambærilegt við umhverfi rannsókn og mat.

</details>

<details><summary>development_review #207 · t2999996 · greedy · general · U</summary>

Source ID: p13official21:dev:opensubtitles:480

English: Now we have enough evidence to charge you with murder.

Reference (shown after audit): Við höfum næg sönnunargögn til að ákæra ykkur fyrir morð.

Review: Evidence/murder retained; skrá fyrir does not confidently establish the intended charge-with relation.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Nú hafa við nægilega sönnunargögn til að skrá þig fyrir morði.

</details>

<details><summary>development_review #208 · t2999996 · G8 · technical_long · U</summary>

Source ID: p13official21:dev:eso:501

English: The team used data from the UVES spectrograph on ESOs Very Large Telescope in Chile (to determine the properties of the star accurately), the Carnegie Planet Finder Spectrograph (PFS) at the 6.5-metre Magellan II Telescope at the Las Campanas Observatory in Chile, the HIRES spectrograph mounted on the Keck 10-metre telescope on Mauna Kea, Hawaii as well as extensive previous data from HARPS (the High Accuracy Radial velocity Planet Searcher) at ESOs 3.6-metre telescope in Chile (gathered through the M dwarf programme led by X. Bonfils and M. Mayor 2003–2010 described here).

Reference (shown after audit): Hópurinn notaði gögn frá UVES litrófsritanum á Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjörnunnar nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5 metra Magellan II sjónaukanum í Las Campanas stjörnustöðinni í Chile, HIRES litrófsritann á 10 metra Keck sjónaukanum á Mauna Kea á Hawaii sem og eldri gögn frá HARPS litrófsritanum (High Accuracy Radial velocity Planet Searcher) á 3,6 metra sjónauka ESO í Chile (aflað í M dwarf verkefninu undir forystu X. Bonfils og M. Mayor milli áranna 2003-2010 sem lýst er hér).

Review: Candidate0 retains many names/numbers but instrument terminology, found-versus-used data and HARPS attribution are too uncertain for confirmed correctness. Others have clear omissions/corruption.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Hópurinn fann gögn frá UVES rannsóknartækinu sem ESO notar á Very Large Telescope í Chile (um að ákvarða eðli stjarna á nákvæmri hátt) Carnegie Planet Finder Spectrograph (PFS) á Magellan II stjörnustjörnunum sem er 6,5 metra í Las Campanas stjörnustöðinni á Chile, HIRES rannsóknartækinu á Keck 10 metra stjörnustjörnunni Mauna Kea á Hawaii og líka umfangskenndar gögn frá HARPS (HARPS radial velocity planet hunter) í 3,6 metra stjörnustjörnunni í Chile, ESO sem var framkvæmd með M dwarf stjörnumála (X. Bonfils og M. Mayor 2003-2010 sem lýst er hér) .

Candidate 1: Hópurinn notuðu gögn úr UVES gæðasprautunni á Very Large Telescope (VLT) ESO á Chile (til að ákvarða eiginleikar stjarnanna) Carnegie Planet Finder Spectrograph (PFS) á Magellan II sjónauki (6,5 litra) á Las Campanas stjörnustöðinni á Chile við 6,5 m stjörnustjörnuna Keck, Hawaii sem viðkomandi gæðisprautu sem stendur á 10 m stjörnustjörnu, HIRES, (Highe Accurecy Radial Veocity Planet Searcher), sem er á 3,6 m stjörnustjörnunni ESO á Chile (með M dwarf verkefninu sem leitar eftir prótaðir (lead by X. Bonfils and M. Mayor 2003-2010) sem lýst er hér, gengu í samhengi M dwarf verkefnisins).

Candidate 2: Hópurinn notaði gagna úr UVES litrófið ESO Very Large Telescope í Chile (að ákvarða eðlis stjarna á ákvarðanlegt hátt) Carnegie Planet Finder Spectrograph (PFS) í 6,5 m á Magellan II litrófi í Las Campanas stjörnustöðinni í Chile, HIRES litrófið sem hafi verið sett á Keck 10 m litrófið í Mauna Kea í Hawaii og líka mörg gagnir frá HARPS (High Accuracy Radial velocity Planet Searcher) litrófið í 3,6 m litrófið í Chile eftir M dwarfs úrræði X. Bonfils og M. Mayor 2003-2010 sem lýst er hér.

Candidate 3: Hópurinn notaði þau gögn úr UVES skýrasmiði í Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjarna), Carnegie Planet Finder Spectrograph (PFS) á 6,5- metra Magellan II sjónauka í Las Campanas stjörnustöðinni í Chile, HIRES skýrasmiðin á Keck 10- metrasetjunni í Mauna Kea á Hawaii og í aðra mælikvarða TAGAS og HARPS (The High Accuracy Radial velocity Planet Searcher) í ESO 3,6- metrasetjunni í Chile (myndast innan af M dwarf örlögum X. Bonfils og M. Mayor 2003-2010 sem lýst er hér).

Candidate 4: Líkamsrannsóknin varðandi stjörnu í jörðu notuð gögn úr UVES tæknifotslitinu á Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjarna á nákvæm handtak), Carnegie Planet Finder Spectrograph (PFS) í 6,5 m stjörnustjörnunni Magellan II í Las Campanas stjörnustöðinni í Chile, HIRES tæknifotslitinn á Keck 10 m stjörnustjörnunni í Mauna Kea í Hawaii, ásamt mikilvægu gögnum frá HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6 m stjörnustjörnunni í Chile (þar sem gögnin voru safnað með M dwarf prófið, sem framkvæmdastjórið var X. Bonfils og M. Mayor á tíðum 2003-2010 sem lýst er hér).

Candidate 5: Teiminn notaði upplýsingum úr UVES litrófsmáli ESO Very Large Telescope í Chile (til að ákvarða eiginleikar stjarnanar nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5-metrar Magellan II litskýrinu í Las Campanas stjörnustöðinni í Chile, HIRES litrófsmálið á Keck 10-metrar litskynni í Mauna Kea í Hawaii, og helvítis fyrri upplýsingum úr HARPS (High Accuracy Radial velocity Planet Searcher) í Chile (hafnað við M dwarf-æðinni X Bonfils og M Mayor 2003-2010 sem lýst er hér, og sem ljúkurðir vart gagnið úr 3,6-metrar litrófsmailli ESO í Chile).

Candidate 6: Hópurinn notuði upplýsingum úr UVES mælinum á Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjarnans nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5 m Magellan II mælinu í Las Campanas stjörnustöðinni í Chile, HIRES mælini á Keck 10 m litilvanslensnu í Mauna Kea í Hawaii og umfangsrikum gögnum í HARPS (High Accuracy Radial velocity Planet Searcher) í Chile (gerðirnar rannsóknar í M litilvöxtum, framkvæmdar af X. Bonfils og M. Mayor 2003-2010, sem lýst er hér).

Candidate 7: Hópurinn notaði gögn úr UVES litrófi á Very Large Telescope ESO í Chile (til að ákvarða eiginleikastarfsemi stjarna á nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) í Magellan II sjónaukinni í Las Campanas stjörnustöðinni í Chile (6,5 metra svarthæð), HIRES litrófið á Keck 10 metra sjónauka á Mauna Kea í Hawaii (stöðuð á sama stjörnustöð ESO í Chile, 3,6 metra svarthæði) og fyrri gögn í HARPS (High Accuracy Radial velocity Planet Searcher) sem ESO gaf í Chile (á M dwarfs verkefni X. Bonfils og M. Mayor 2003-2010 sem lýst er hér)

</details>

<details><summary>development_review #209 · t2999996 · G8 · technical_medium · F</summary>

Source ID: p13official21:dev:ema:1406

English: Concomitant use with yellow fever vaccine and with live virus and bacterial vaccines (see section 4.5).

Reference (shown after audit): Samhliða notkun með bóluefni gegn gulusótt og bóluefni með lifandi veirum og bakteríum (sjá kafla 4.5).

Review: None preserves yellow-fever vaccine and the entire concomitant vaccine-use list.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Rannsókn með geislunir á bóluefnum gegn gulþjálfandi eitilvöxti og lifandi veiru- og bakteríu+bóluefnum (sjá kafla 4.5).

Candidate 1: Samhliða notkun með llúpurfíkninu og lifandi veiru- og bakteríufíkninu (sjá kafla 4.5).

Candidate 2: Samhliða meðferð með brúðu-æxlisbóluefni og með lifandi veiru- og bakteríubóluefni (sjá kafla 4.5).

Candidate 3: Samhliða notkun með fasafræðiseftirlyfjum og lifandi veiru- og bakteríufyrirbyggjandi bóluefnum (sjá kafla 4.5).

Candidate 4: Samhliða notkun á geislalyfsfleiri og lifandi veiru- og bakteríuhvata (sjá kafla 4.5).

Candidate 5: Samhliða notkun millivefja fyrir gulvind og lifandi veirusjúkdóm og bakteríusjúkdóm (sjá kafla 4.5).

Candidate 6: Samhliða notkun gegnsæðis gegn gultsótt og lifandi veirus- og bakteríusótt (sjá kafla 4.5).

Candidate 7: Notkun samhliða eitlafræðisefna og lifandi veirusjónum og sýklum, fyrir lifur (sjá kafla 4.5).

</details>

<details><summary>development_review #210 · t2999996 · greedy · technical_short · F</summary>

Source ID: p13official21:dev:eso:491

English: ALMA can observe in different frequency bands.

Reference (shown after audit): ALMA getur gert mælingar á mismunandi böndum.

Review: Frequency bands becomes concerts/different numbers of bands.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: ALMA getur fylgst með tónleikum á mismunandi fjölda banda.

</details>

<details><summary>development_review #211 · t2999996 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eea:1552

English: The analytical result shall be reported as x +/– U whereby x is the analytical result and U is the expanded measurement uncertainty, using a coverage factor of 2 which gives a level of confidence of approximately 95 % (U = 2u).

Reference (shown after audit): Greina skal frá niðurstöðum úr greiningunum sem x +/– U þar sem x er niðurstaða greiningarinnar og U er útvíkkaða mælióvissan með þekjustuðlinum 2 sem gefur 95% öryggisstig (U = 2u).

Review: Expanded measurement uncertainty and coverage/confidence concepts are corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Greina skal niðurstöður greiningar sem x +/– U þar sem x er niðurstöður greiningar og U er útþekktur málstöfunartími, með því að nota 2 gildi fyrir umfrymisstig sem gefur umframvísitengingu um 95% (U = 2u).

</details>

<details><summary>development_review #212 · t2999996 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eea:1216

English: That task shall be coordinated with the existing regional cooperation programmes and shall include, where appropriate, the organisation of relevant training activities.

Reference (shown after audit): Samræma skal það verkefni svæðisbundnum samstarfsáætlunum sem eru fyrir hendi og skal það fela í sér, eftir því sem við á, skipulag viðeigandi þjálfunar.

Review: Existing regional cooperation programmes becomes research programmes at community level.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það verkefni skal samræma við tilstaðar rannsóknaráætlunum á sviði bandalagsins og skal það innihalda, eftir því sem við á, stjórna viðeigandi þjálfunartaknum.

</details>

<details><summary>development_review #213 · t2999996 · greedy · general · F</summary>

Source ID: p13official21:dev:opensubtitles:1159

English: Somebody get me a picture of the girl.

Reference (shown after audit): Útvegið mér mynd af stelpunni.

Review: The receiver me is missing from the request to obtain a picture.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Einhver fá mynd af stúlkunni.

</details>

<details><summary>development_review #214 · t2999996 · G8 · technical_medium · F</summary>

Source ID: p13official21:dev:eea:698

English: Only days that can be worked should be included when Saturdays and Sundays are not worked they should not be included, the same with public holidays).

Reference (shown after audit): Eingöngu skal telja með þá daga sem unnt er að vinna (ef ekki er unnið á laugardögum og sunnudögum skal ekki telja þá með; hið sama gildir um lögboðna frídaga).

Review: All corrupt Saturday/Sunday or their conditional exclusion; generic non-working-day paraphrase omits the specified days.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Aðeins dagar sem má vinna skal taka til þeirra þegar ekki er tekið á sásterumog sunnudagum (sama með opinbera fríum).

Candidate 1: Einungis daga sem má vinna á skaltu taka inn þegar riddarogur og laugardagur eru ekki vinna á, þegar ekki maga skal taka í skrá borgardagsdögum (public holiday).

Candidate 2: Aðeins daga sem má vinnast eiga aukið þegar Söndag og sunnudagur koma ekki í vinnuna. Sama má við borgarkennidayggi).

Candidate 3: Einnig skal taka til eitt fyrir hvern dag sem er hægt að vinna þegar ekki er að vinna á sólarhringum og sólarhringardagum, sama skal fyrir opinbera frídagana.).

Candidate 4: Einungis skal taka til daga sem má vinna og ekki einu sinni dögum sem ekki ræði að vinna skal ekki taka til þeirra, svo og opinbera frídaga).

Candidate 5: Einnig skal taka bara dagirnar sem auðvelda að starfræði, þegar sjónda og sólarhringar eru ekki starfræði skal ekki taka það, samt í opinbera fríar).

Candidate 6: Einungis daga sem geta verið virkt skulu fylgt saman þegar Söndagur og sunnudagar eru ekki virkt eða einnig að sama máli berast lausnardagur í opinbersamfélagi.

Candidate 7: Aðeins daga sem eru hægt að vinna eiga að skrá inn þegar sár og sunnudagar eru ekki vinna eiga ekki að skrá þau inn, sama við opinbera helgana).

</details>

<details><summary>development_review #215 · t2999996 · greedy · technical_medium · F</summary>

Source ID: p13official21:dev:eso:1051

English: The technique used by Teague, which derived averaged variations in the flow of the gas as small as a few percent, revealed the impact of multiple planets on the gas motions nearer to the star.

Reference (shown after audit): Tæknin sem Teague beitti sýndi meðalbreytingarnar á gasflæðinu niður í nokkur prósent og leiddi í ljós áhrif nokkurra plánetna á hreyfingu gassins nær stjörnunni.

Review: Multiple planets becomes family of Earths and derived small variations becomes caused average changes.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Tæknið sem Teague notaði, sem leiddi til meðalbreytinga á flæði gassins eins minnka og nokkrar prósentar, sýndi áhrif fjölskyldu jörðanna á flæði gassins nálægri stjörnunni.

</details>

<details><summary>development_review #216 · t2999996 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:ema:325

English: If you get lower abdominal pain, gain any weight rapidly, feel sick or are vomiting or if you have difficulty in breathing, talk to your doctor straight away who might ask you to stop using this medicine (see in section 4 under “Serious side effects”).

Reference (shown after audit): Ef þú færð verk í neðri hluta kviðar, þyngist hratt, finnur fyrir ógleði eða kastar upp eða ef þú átt erfitt með að anda, skaltu hafa tafarlaust samband við lækninn sem gæti beðið þig að hætta að nota lyfið (sjá 4. kafla „Alvarlegar aukaverkanir“).

Review: Lower abdominal pain is corrupted and feeling sick becomes getting infections.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef þú færð magavart, færð þig hratt þyngd, færð sýkingar eða er uppköst, eða hefur vandamál við öndun, skaltu tafarlaust ræða við lækninn sem kann að spyrja þig um að hætta notkun lyfsins (sjá kafla 4 undir „Alvarlegar aukaverkanir“).

</details>

<details><summary>development_review #217 · t2999996 · G8 · technical_short · F</summary>

Source ID: p13official21:dev:eso:302

English: This is because the tilt of the orbit is normally unknown.

Reference (shown after audit): Þetta er vegna þess að venjulega er brautarhallinn óþekktur.

Review: None preserves unknown orbital inclination; outputs substitute side, vein, car, or unrelated terms.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Það er vegna þess að hliðin kringliðarhringarinnar er venjulega ekki þekkt.

Candidate 1: Það er vegna þess að stojakiltur í kringlunum er venjulega ekki þekkt.

Candidate 2: Það er vegna þess að bláæðin er venjulega ekki þekkt.

Candidate 3: Þetta er vegna þess að þjóðor meginfirarðið er venjulega ekki þekkt.

Candidate 4: Það er vegna þess að hálfan bílinn er venjulega ekki þekktur.

Candidate 5: Þetta kemur fyrir vegna þess að umhverfisstig um reikninga sé vanlega ekki þekkt.

Candidate 6: Þetta er vegna þess að fækkun ró á meginborði er venjulega óþekkt.

Candidate 7: Þetta er vegna þess að um námi banvændisins er venjulega ekki vitað.

</details>

<details><summary>development_review #218 · t2999996 · G8 · technical_long · F</summary>

Source ID: p13official21:dev:ema:1394

English: The most commonly reported adverse reactions (≥ 20%) among patients treated with both belatacept- based regimens (MI and LI) up to Year 3 are diarrhoea, anaemia, urinary tract infection, peripheral oedema, constipation, hypertension, pyrexia, nausea, graft dysfunction, cough, vomiting, leukopenia, hypophosphataemia, and headache.

Reference (shown after audit): Algengustu aukaverkanirnar (≥ 20%) hjá sjúklingum sem fengu báðar belatacept meðferðirnar (MI og LI) fram að 3. ári eru niðurgangur, blóðleysi, þvagfærasýking, bjúgur á útlimum, hægðatregða, háþrýstingur, hiti, ógleði, ófullnægjandi starfsemi græðlings, hósti, uppköst, hvítfrumnafæð, blóðfosfatskortur og höfuðverkur.

Review: Every candidate changes several named adverse reactions, including graft dysfunction, peripheral oedema, leukopenia or hypophosphataemia.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Algengustu aukaverkanirnar sem greint hefur verið frá (≥ 20%) hjá sjúklingum sem fengu bæði belatacept-bundna meðferðir (MI- og LI-) allt til ári 3 eru niðurgangur, blóðleysi, bakterýatrygging í þvagmálum, bólgu í burtíkjum, lálægða, háþrýstingur, hiti, ógleði, grunnvirkjunarskerðingar, hósti, uppköst, hvítblöðrufæð, lágkornamyndun, ofkornamyndun og höfuðverkur.

Candidate 1: Algengustu aukaverkanirnar sem greinst eru hjá sjúklingum sem fá bæði meðferð með belatacepti (MI) og meðferð með belatacepti í samsettri meðferð (LI) og eru fjöldi þess í algeru árinu 3 (≥ 20%) eru niðurgangur, blóðleysi, sýking í þvagvegasjónar, þynnu, trægð, háþrýstingur, hiti, ógleði, vansköpun æða, hósti, uppköst, blóðflagnafæð, blóðfosfatslækkun og höfuðverkur.

Candidate 2: Yfirleitt tilkynntar aukaverkanir (≥ 20%) hjá sjúklingum sem fá bæði reglan með belatacept (MI- og LI) allt að 3 árs, eru niðurgangur, blóðleysi, sýking í þvagvegnum, bólgu í hluta af kviði, hægðatregða, háþrýstingur, hiti, uppköst, stofnunarbilun á græðslu, hósta, uppköst, hvítblóðfall, jafngildisblóðfalls, og höfuðverkur.

Candidate 3: Algengustu aukaverkanirnar sem fram koma (≥ 20%) hjá sjúklingum sem fá bæði meðferð með belatacept-bundnum meðferðum (MI og LI) til ára 3 eru niðurgangur, blóðleysi, kveikjun í þvagvegin, bólga í utan blóðvegar, truflun í geymslu, háþrýstingur, hiti, ógleði, ónæmingur, hósti, uppköst, blóðleysi, blóðsólarhægðatap, og höfuðverkur.

Candidate 4: Algengustu aukaverkanirnar sem fram komu hjá sjúklingum sem fengu bæði reglur sem byggðar voru á belatacepti (MI og LI) til árs 3 (≥ 20%) eru niðurgangur, blóðleysi, sýking í þvagmyndun, þyngdar bólga í útlöndum, trægæði, háþrýstingur, hiti, ógleði, skerta vegna stofnun, hósti, uppköst, blóðflagnafæð, blóðódsýraskort og höfuðverkur.

Candidate 5: Algengustu aukaverkanirnar sem greint var frá (≥20%) hjá sjúklingum sem fengu bæði meðferð með belataceptu-bundnum meðferðaráætlunum (MI og LI) fram í 3. ári eru niðurgangi, blóðleysi, ofnæmisbólga í niðurbolti, hvíldrofi í kringum taugahlaup, tráháðir þyngdarleysi, háþrýstingur, hiti, ógleði, skertferli í græðli, hósta, uppköst, blóðfall, blóðfosfatófsvildi, og höfuðverkur.

Candidate 6: Algengustu aukaverkanirnar (≥ 20%) sem greindust hjá sjúklingum sem fengu bæði belatacept-bundna meðferð (MI og LI) allt að ári 3 eru niðurgangur, blóðleysi, nýrnasjúkdóm í nýrnaræði, bólga í ljósi, trægðleysi, háþrýstingur, hiti, ógleði, vanskuldaður nýrna, hósti, uppköst, blóðflagnafæð, blóðfosfatsþéttni lág og höfuðverkur.

Candidate 7: Algengustu aukaverkanirnar sem greindust hjá sjúklingum sem fengu meðferð með bæði belatacept-bundið meðferð (MI og LI) allt að 3 árs (≥ 20%) eru niðurgangi, blóðleysi, sýking í þvagrann, bólga í umhverfi, hægðatregða, háþrýstingur, hiti, uppköst, truflun í veirum, hósti, uppköst, blóðflagnafæð, blóðfosfatarmilti og höfuðverkur.

</details>

<details><summary>development_review #219 · t2999996 · G8 · technical_short · U</summary>

Source ID: p13official21:dev:ema:767

English: Therefore, docetaxel must not be used during pregnancy unless clearly indicated.

Reference (shown after audit): Dócetaxel á því ekki að nota á meðgöngu nema brýna nauðsyn beri til.

Review: Drug/pregnancy prohibition preserved in several, but clearly-indicated exception is ambiguous; candidate7 indication wording is closest but not confidently correct.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Því má ekki nota docetaxel á meðgöngu nema ákvarðanir séu klárar.

Candidate 1: Því má ekki nota docetaxel á meðgöngu nema sprauta sé tilkynnt á tæka hátt.

Candidate 2: Því má ekki nota doketaxel á meðgöngu nema tilkynnt sé greinilega til þess.

Candidate 3: Því má ekki nota docetaxel á meðgöngu nema greinilega áður sé til.

Candidate 4: Því má ekki nota docetaxel á meðgöngu nema greinilega megi gefa það.

Candidate 5: Því verður ekki að nota docetaxel á meðgöngu nema brýna markmiði sé fylgt.

Candidate 6: Því má ekki nota dócetaxel á meðgöngu nema greinilega fylgjast með því.

Candidate 7: Því má ekki nota dócetaxel á meðgöngu nema algjörlegar ábendingar fylgi.

</details>

<details><summary>development_review #220 · t2999996 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eea:50

English: Similar studies, for at least three soil types, must be reported for all relevant metabolites, degrada tion and reaction products which in soil degradation studies account at any time for more than 10 % of the amount of active substance added.

Reference (shown after audit): Gera skal grein fyrir svipuðum rannsóknum á þremur jarðvegsgerðum hið minnsta með tilliti til allra viðkomandi umbrots-, niðurbrots- og hvarfaefna sem í rannsóknum á niðurbroti í jarðveginum nema á einhverjum tímapunkti meira en 10% af viðbættu magni virka efnisins.

Review: Soil types and degradation/reaction products are corrupted, with the at-any-time qualifier missing.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Tilkynna verður um svipaðar rannsóknir á að minnsta kosti þremur grunnfærum fyrir öll viðeigandi umbrotsefni, umbrot og framleiðsluefni sem í rannsóknum á umbrotnun grunnfæra gefa stærri en 10% af skömmtum virka efna sem bætt er við.

</details>

<details><summary>development_review #221 · t2999996 · greedy · general · F</summary>

Source ID: p13official21:dev:opensubtitles:3607

English: Well, that makes you ugly and stupid.

Reference (shown after audit): Þá ert þú ljótur og heimskur.

Review: Ugly becomes strange; singular you also changes.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Jæja, það gerir ykkur skríti og heimskur.

</details>

<details><summary>development_review #222 · t2999996 · greedy · technical_short · P</summary>

Source ID: p13official21:dev:eso:446

English: “Astronomers have waited for data like this for over a decade.

Reference (shown after audit): „Stjörnufræðingar hafa beðið eftir gögnum eins og þessum í yfir áratug.

Review: Astronomers waiting over ten years for such data retained; grammatical errors do not alter the claim.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: „Stjörnufræðingar höfðu bíðið um gögn eins og þetta í meira en tíu ár.

</details>

<details><summary>development_review #223 · t2999996 · greedy · technical_long · F</summary>

Source ID: p13official21:dev:eso:924

English: ESO was delighted to welcome Italys Minister of Education, Universities and Research, H.E. Stefania Giannini, to the ceremony, which was also attended by the Italian Consul General in Munich, Renato Cianfarani, the ESO Council President, Patrick Roche, and the Italian ESO Council Delegates, Nicolò DAmico (who is also President of INAF) and Matteo Pardo, Scientific Attaché at the Italian Embassy in Berlin.

Reference (shown after audit): Viðstödd undirritunina voru H.E. Stefania Giannini, mennta- og vísindamálaráðherra Ítalíu, ítalski konsúllinn í München, Renato Cianfarani; Patrick Roche, forseti ESO ráðsins, Nicolò DAmico, forseti ESO ráðsins (sem er líka forseti INAF) og Matteo Pardo, fulltrúi vísinda í ítalska sendiráðinu í Berlín.

Review: Ministerial position, countries, event attendance and named roles are extensively corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: ESO var ánægð af því að viðtaka Stefania Giannini, íslandsskonar menntamaður yfir höndir, í sérstökum sérhæfis, sem var einnig áttur í sérstökum sérhæfis í Ítalíu, Renato Cianfarani, forseta- og stjórnmann ESO, Patrick Roche, og tilskipunaraðilar ESO frá Ítalíu, Nicolò DAmico (sem er líka forseta- og stjórnmann INAF) og Matteo Pardo, vísindamennsögusamþykki í Ítalíu.

</details>

<details><summary>final_semantic_review #0 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:930

English: Wells in microtitre plates are coated overnight with recommended dilutions of purified immunoglobulin fractions of antibodies of reference quality.

Reference (shown after audit): Bollar í míkrótítrunarplötum eru þaktir næturlangt með ráðlögðum þynningum af hreinsuðum ónæmisglóbúlín- þáttum mótefna sem standast kröfur um viðmiðunargæði.

Review: All eight corrupt microtitre wells/coating overnight and purified immunoglobulin-antibody dilutions.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Vélur á miðlæganum þynni eru mynduð með tilhögunnara þroskunum af eftirlitsgjalds aðferðum til að beita aðferðaskiptum í önd.

Candidate 1: Wells í sprautukorna eru skýtlaðar á næri kvöld með farglæðingu úr þróaþyngjum í gæðisríktu gagnum af immunglibúnum sem náðaðar eru.

Candidate 2: Hruðir í máltrýtpratkammar eru þvott í nátt undir meðferðarþáttum þurrkunnuðra immungólubreytana sem eru valdarefni mótefna með viðmiðunarmögnun.

Candidate 3: Vellir í litlýfjufjölda eru samræmd við fyrrmeðaltaliða þolsum tímabili í nýtt og ekki skilvirkum immungólbijafaliðum úr forðunarmjólkum óþolgjafalegri móttökufarþeganna.

Candidate 4: Vallir í mikrólögækjum eru mynduð með tilgreindri þéttnum af silfurínum í nýta með því að skera úr því að miðað er með því að falla er úr víkturlegri orðnum móttökuglymu.

Candidate 5: Vökufæranir í meirikóptarfræðilegu beinum eru útblönd um fyrirhugaðar þynningu af kvalvíslegum immungólgíbulfrumum í viðmiðunarkvörtum.

Candidate 6: Vælpör um stjórnunartíbrúi eru íródar um nýði með tilgreindri þroskanir af silfri part í ósýfuglu mótefni eða mótefni með viðmiðunarskammt.

Candidate 7: Sprautur í stærðfræðilegum plátum eru úrveglaðar á nótt með tilgreindum þróunaflokka í sviði ósýnum ólíkuruppiðar ósýnum sem eru af viðkomandi gæði.

</details>

<details><summary>final_semantic_review #1 · after · greedy · technical_medium · P</summary>

Source ID: p13official21:test:ema:74

English: ARICLAIM should normally not be used for children and adolescents under 18 years.

Reference (shown after audit): Venjulega ætti ekki að nota ARICLAIM handa börnum og unglingum undir 18 ára aldri.

Review: Normal avoidance for children/adolescents under18 and drug identity preserved.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: ARICLAIM á ekki venjulega að nota handa börnum og unglingum yngri en 18 ára.

</details>

<details><summary>final_semantic_review #2 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eso:716

English: From the gravitational lensing effect, these groups turn out to contain around 30 times more dark than visible matter.

Reference (shown after audit): Þyngdarlinsuhrifin sýna að hóparnir innihalda um 30 sinnum meira hulduefni en sýnilegt efni.

Review: None preserves gravitational lensing and the30-to-one dark-versus-visible-matter inference.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þessi hóp teljast hafa um 30 áfestu morgnaður af dýrrími en lituðu efninu.

Candidate 1: Í ljós þessarri íhljómu fjallar þessi félög yfir 30 sinnum meira svörtu en glænur.

Candidate 2: Í ljós þessarar skugganar í því hve þessar vald eru fyrir þjónustu styrkjaðar 30 sinnum meira af dunkum en litanum.

Candidate 3: Í því skiptingu sem veiruþjálfar fylgja þessa hópa er þau búin að vera meira en í 30 skiptingum þjálf er hvítu en ljósið.

Candidate 4: Íhluta þessara fylgni í vörslu með synjað leiðinni eru stærri um 30 skiptir af dauðum en láttum.

Candidate 5: Í ljósi við grásvikskammtun gengur þessi aðilar til að innihalda um 30 brjóðri mikið eftir litlum efninu.

Candidate 6: Stökkbreytur á serkustungum, sem sérstaklega eru í þessum samanburðum, eru kynntar að þau innihaltu um 30 sinnum meira dýrmjögubreytla en háða.

Candidate 7: Brot af því að áhugnægjandi ljós er llevað veiti þessu samsetningu um 30 sinnum meiri myrkur en lágtunarefni.

</details>

<details><summary>final_semantic_review #3 · after · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:1601

English: I don"t plan on wearing it that long.

Reference (shown after audit): Ég ætla ekki að vera lengi í honum.

Review: Intention not to wear it for long preserved; minor comparative-duration wording.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Ég ætla ekki að vera í því lengi.

</details>

<details><summary>final_semantic_review #4 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:1144

English: Successful participation in interlaboratory studies that assess laboratory proficiency is the best way to prove the competence in specific analyses.

Reference (shown after audit): Árangursrík þátttaka í rannsóknum með öðrum rannsóknarstofum, þar sem frammistaða rannsóknarstofa er metin, er vænlegust til þess að staðfesta hæfni í sértækum efnagreiningum.

Review: No candidate retains successful interlaboratory participation assessing laboratory proficiency.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Viðskipti í vettvangi í milli aðildarríkja sem skoða kaupa eftir rannsóknarstærðið er besta aðferð til að sýna fram á skilun á sérstökum greinum.

Candidate 1: Viðbót í alræðum rannsóknum sem matast á hagvægunum í vettvangi er besta aðferðinni til að sýna fram á þá þekkingu sem er einstaklingur.

Candidate 2: Reykendur sem taka að röskun á öryggisstöðum og taka besta leiðina til að sýna fram á menntun þeirra í sérstökri greiningu.

Candidate 3: Rekstrarhöndun í rannsóknir á varðandi eftirlitsrannsóknir, þar sem færi að því hvort rannsóknir eru farið ráðstafanir, er besta aðferðinni til að sannprófa fagleg hæfi í sérstöku greiningunum.

Candidate 4: Viðbótur á innanfélagslegum rannsóknum sem mæla um skynsæti rannsóknarstofu er bestan leiðin til að sýna fram á störfþekkingu í sérstöku greiningu.

Candidate 5: Aðlöngt meðtæknilega rannsóknir með í fyrirtækjum sem meta hagnað á rannsóknirmálum er besta aðferðin til að sýna fram á nákvæmni í sérstökum greiningum.

Candidate 6: Bestur að yfirliti í innanstofum til að meta skilfullleik fyrir rannsóknir og ná þangað að sýna fram á vitneskju um nokkur menntun.

Candidate 7: Reynsla við rannsóknir á annarri starfsmálum sem mæla fyrir hæfni í vettvangi er besta leiður til að sýna fram á nákvæmni í sérstökri greiningi.

</details>

<details><summary>final_semantic_review #5 · after · greedy · technical_short · F</summary>

Source ID: p13official21:test:ema:2490

English: If you are left-handed, do what comes naturally to you.

Reference (shown after audit): Þeir sem eru örvhentir eiga að gera það sem þeim finnst eðlilegast.

Review: Left-handed condition is lost in an unrelated hand adjective.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef þú ert höndlegra skaltu gera það sem kemur fyrir þér eðlilega.

</details>

<details><summary>final_semantic_review #6 · before · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:825

English: The process of dust trapping is explained in an earlier release (eso1325).

Reference (shown after audit): Þetta ferli, þegar ryk festist, er útskýrt í eldri fréttatilkynningu (eso1325).

Review: All corrupt dust-trapping process; release number alone is retained.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Sjá skal framleika þess að snertja ugnaðarmiðju (eso1325).

Candidate 1: Í forsendu meðan áður er lýst má liðun með flítunni til greininga (eso1325).

Candidate 2: Efnið við úrbóta steldri lausa er greint fram í fyrri skírteini (eso1325).

Candidate 3: Nákvæmlega er tíðnotkun dýrsamfs í einu tilgreind í unntu skjölum (eso1325).

Candidate 4: Verklagsbundin skjalfstýring er greint í áður (esó1325).

Candidate 5: Hlutfallur í þynnist í körfunni eru lýst í fyrri útgáfu (eso1325).

Candidate 6: Lífshættufangahlut er lýst í ófræðingu frá fyrri (eso1325).

Candidate 7: Rakkaður vísnar með dusti er lýst í fyrri frásæði (eso1325).

</details>

<details><summary>final_semantic_review #7 · before · greedy · technical_short · P</summary>

Source ID: p13official21:test:eea:1965

English: After paragraph 97B, paragraph 97C is added.

Reference (shown after audit): Lið 97C er bætt við á eftir lið 97B.

Review: Both paragraph identifiers and insertion-after relation preserved.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Eftir lið 97B bætist við lið 97C.

</details>

<details><summary>final_semantic_review #8 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:ema:709

English: The other ingredients are sodium chloride, succinic acid, polysorbate 80, 2- phenoxyethanol and water for injections.

Reference (shown after audit): Önnur innihaldsefni eru natríumklóríð, succinic sýra, polysorbat 80, 2-fenoxýetanól og vatn fyrir stungulyf.

Review: Polysorbate80 becomes an unrelated invented ingredient.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Aðrar innihaldsefni eru natríumklóríð, suksínsýru, flókisbólusetur 80, 2- fenóxýetanol og vatn fyrir stungulyf.

</details>

<details><summary>final_semantic_review #9 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:ema:970

English: In patients with mild hepatic impairment (Child-Pugh A), there was no significant changes in pharmacokinetics compared with normal healthy volunteers.

Reference (shown after audit): Hjá sjúklingum með væga skerðingu á lifrarstarfsemi (Child-Pugh A) voru engar marktækar breytingar á lyfjahvörfum samanborið við heilbrigða sjálfboðaliða.

Review: Healthy-volunteer comparator becomes severely ill patients; hepatic-impairment wording also corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Í sjúklingum með vægri lifrarverndareinkenna (Child-Pugh A) var engin marktæk breytingar á lyfjahvörfið samanborið við eðlilega heilbrigðu hjá alvarlegum sjúklingum.

</details>

<details><summary>final_semantic_review #10 · after · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:1803

English: What are you planning on telling her?

Reference (shown after audit): Hvað ætlarðu að segja henni?

Review: Question about planned statement to her fully preserved.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Hvað ætlarðu að segja henni?

</details>

<details><summary>final_semantic_review #11 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:ema:74

English: ARICLAIM should normally not be used for children and adolescents under 18 years.

Reference (shown after audit): Venjulega ætti ekki að nota ARICLAIM handa börnum og unglingum undir 18 ára aldri.

Review: Normally-not-used recommendation becomes an unconditional prohibition; the limiting qualifier is omitted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: ARICLAIM skal ekki nota hjá börnum og unglingum yngri en 18 ára.

</details>

<details><summary>final_semantic_review #12 · before · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:2209

English: Much has been made of the hostility between our countries.

Reference (shown after audit): Mikið hefur verið gert úr fjandskapnum milli ríkja okkar.

Review: Hostility becomes uncleanness.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Miklu hefur verið sagt um óhreinleika milli landanna okkar.

</details>

<details><summary>final_semantic_review #13 · after · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:1088

English: Weather statistics are available here.

Reference (shown after audit): Upplýsingar um veður má finna hér.

Review: Weather statistics becomes winter research, radio data or unrelated records in every candidate.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Vetrarannsóknir eru hér.

Candidate 1: Útvarps-íslendingarnám birtaðar eru hér.

Candidate 2: Útabréf yfir vakt er hér.

Candidate 3: Vetrarannsóknarupplýsingar eru hér.

Candidate 4: Vetnaskýrslur eru hér fyrir hendi.

Candidate 5: Útvarpsgögur eru hér fyrir.

Candidate 6: Vetrarannsóknarupplýsingar eru hér fyrir.

Candidate 7: Útvarps-eyðubúnað er hér fyrir.

</details>

<details><summary>final_semantic_review #14 · after · G8 · technical_short · P</summary>

Source ID: p13official21:test:eso:514

English: This star formation region is forming many stars.

Reference (shown after audit): Þetta stjörnumyndunarsvæði er að mynda margar stjörnur.

Review: Candidate5 retains star-forming region forming many stars; case/voice agreement is rough but entities and process clear.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [5]

Candidate 0: Þessi vetrarbraut verður fjöldi stjarna.

Candidate 1: Við skýrfjöldinum eru enn mörg stjörnur búin til að mynda.

Candidate 2: Þessi stjörnumyndunarféluga myndast mörg stjörnur.

Candidate 3: Þessi stjörnumyndunarsvæði myndast marga stjörnur.

Candidate 4: Þennan stjörnufrumuhópi myndast margir stjörnur.

Candidate 5: Þetta stjörnumyndunar svæði myndast mörg stjörnur.

Candidate 6: Einnig eru mörg stjörnur úr þessum myndunarlaga.

Candidate 7: Þessi stjörnumyndunarsvæði myndast mörg stjörnur.

</details>

<details><summary>final_semantic_review #15 · after · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:349

English: The results described here use some of these Science Verification data.

Reference (shown after audit): Gögnin sem notuð voru fyrir þessa rannsókn var að hluta til aflað við þessar prófanir.

Review: Results using verification data becomes results being used; source/data roles reverse.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Niðurstöðurnar sem koma fram hér eru notaðar sumar af þessum gögn um sannprófun á vísindum.

</details>

<details><summary>final_semantic_review #16 · after · G8 · technical_medium · P</summary>

Source ID: p13official21:test:ema:1495

English: Check again to make sure the correct dose of Tevagrastim is in the syringe.

Reference (shown after audit): Athugaðu aftur hvort rétt magn Tevagrastim er í sprautunni.

Review: Candidates2/3 preserve rechecking correct Tevagrastim dose in syringe.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [2, 3]

Candidate 0: Athugaðu á ný og sjá að réttur skammtur af Tevagrastim sé til staðar í sprautunni.

Candidate 1: Athugaðu aftur að vísa á að réttur skammtur af Tevagrastim sé fyrir hendi í sprautunni.

Candidate 2: Athugaðu aftur til þess að tryggja að réttur skammtur af Tevagrastim sé í sprautunni.

Candidate 3: Athugaðu aftur til að tryggja að réttur skammtur af Tevagrastim sé í sprautunni.

Candidate 4: Skoðaðu aftur til að tryggja að rétta skammtur af Tevagrastim sé í sprautunni.

Candidate 5: Skoðið aftur að talin sé réttur skammtur af Tevagrastim í sprautunni.

Candidate 6: Athugaðu aftur til að sjá að réttur skammtur af Tevagrastim sé í sprautunni.

Candidate 7: Komið aftur og gætið úr skugga um að réttur skammtur af Tevagrastim sé í sprautunni.

</details>

<details><summary>final_semantic_review #17 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:382

English: In the controlled clinical studies in chronic ITP with eltrombopag, increases in serum alanine aminotransferase (ALT), aspartate aminotransferase (AST) and bilirubin were observed (see section 4.8).

Reference (shown after audit): Í klínískum samanburðarrannsóknum á eltrombópagi hjá ITP-sjúklingum kom fram hækkun á alanínamínótransferasa (ALAT), aspartatamínótransferasa (ASAT) og bílírúbíní í sermi (sjá kafla 4.8).

Review: All alter controlled-study/chronicITP identity or the enzyme/serum terms; candidate5 makes controlled studies familiar studies.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Í samkeppnishæfðum klínískum rannsóknum á langvinnri nýstöðubólgu með eltraðrupaflíði með eltrombopagi komu fram aukningu í alanínásíntransféraasum (ALT) og asparátásíntransféraasum (AST) í sykursýni og bilirúbínum (sjá kafla 4.8).

Candidate 1: Í samkeppnishæfðum klínískum rannsóknum á langtíma sjúkdómi af blóðflókinu hjá þau með því að nota eltrombopag komst fram aukning á alanínaminótrensa í sermuið (ALT) (alanínaminótrensa í sermum), frumínótrensa í sermuið (AST) og bilírubína (sjá kafla 4.8).

Candidate 2: Í samkeppnishæfðum klínískum rannsóknum á langvinnri blæðingu af því er var ákvarðað aukningu í serumalanínaminotransférasýni (ALT), aspartataminotransférasýni (AST) og bilírubíni (sjá kafla 4.8).

Candidate 3: Í samkeppnishopaðum klínískum rannsóknum á langvinna blóðflæðisútverkum virkaði altídúrennsýni (ALT), aspartatúrennsýni (AST) og bilírubín (sæ 4.8).

Candidate 4: Í samfylkingu þar af fáanlegri klínískri rannsóknir um langvinnar blóðflagnatíðendisbólgu með eltrombopag komst fram aukningu alanínamínótranfræðis í sermi (ALT), aspartatamínótranfræðis (AST) og bilírubina (sjá kafla 4.8).

Candidate 5: Í kunningslegri klínískri rannsóknum á langtíma ITP með eltrómbópag komu í ljós aukning af alanínaminótrasférmi í sermissýni (ALT), aspartataminótrasférmi (AST) og bilírubíni (sjá kafla 4.8).

Candidate 6: Í takmarkaðum klínískum rannsóknum á langvinnri blóðflæðismyndun með eltrómbópag komu fram aukningar á alanínamínótrensa í sermi (ALT), aspartatamínótrensa í sermi (AST) og bilírubín (sjá kafla 4.8).

Candidate 7: Í samkeppnishafið klínískum rannsóknum á langtíðnið með ónæmi í blóði með eltrómbópag var tilgreind aukningu á alanín-aminótransféras í sérumi (ALT), aspartat-aminótransféras (AST) og bilírubín (sjá kafla 4.8).

</details>

<details><summary>final_semantic_review #18 · before · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:1596

English: I stuffed it in my pocket.

Reference (shown after audit): Ég setti hana í vasann.

Review: Pocket and stuffing action replaced by package/unrelated verb.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ég skrúddi það í pakkinn.

</details>

<details><summary>final_semantic_review #19 · after · G8 · technical_short · F</summary>

Source ID: p13official21:test:eea:679

English: This relates to the gross earnings paid during the reference year.

Reference (shown after audit): Þetta lýtur að vergum tekjum sem eru greiddar á viðmiðunarárinu.

Review: No candidate preserves gross earnings paid in reference year; gross earnings becomes base payments/tax/unrelated invented terms.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þetta varðar hryggjaríkur sem gefinn eru á í viðmiðunarefni.

Candidate 1: Þetta varðar hagskattin á því sem greidd er á viðmiðunarári.

Candidate 2: Þetta varðar fyrirbærin laun, sem er greitt meðan á viðmiðunarliðinu stendur.

Candidate 3: Það varðar heildarnafnaráðgengi sem er gefin í viðmiðunar árinu.

Candidate 4: Þetta varðar grunngreiðslurnar í samkvæmta ári.

Candidate 5: Þetta varðar heildarnafn fyrir áletra á viðmiðunaröldinni.

Candidate 6: Þetta varðar grunngreiðslur sem teknum eru út ásamt ákvörðunarsjóði.

Candidate 7: Það tengist fjárhæðum sem stöðvar eru fram á viðmiðunar árinu.

</details>

<details><summary>final_semantic_review #20 · before · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:3337

English: But maybe, if we got away from here, if we went somewhere safe, it could be different.

Reference (shown after audit): En kannski ef við kæmumst burt héðan, ef við færum á öruggan stað, gæti það breyst.

Review: Getting away from here and going somewhere safe are omitted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: En kannski, ef við fariðum til hæfis, getur það verið annars.

</details>

<details><summary>final_semantic_review #21 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:2125

English: In addition, the sub-processing should only consist of the operations agreed in the contract between the data exporter and the data importer incorporating the standard contractual clauses provided for in this Decision and should not refer to different processing operations or purposes so that the purpose limitation principle set out by Directive 95/46/EC is respected.

Reference (shown after audit): Þá skal ráðstöfun til undirverktaka aðeins fela í sér þær aðgerðir sem samþykktar eru í samningnum milli gagnaútflytjanda og gagnainnflytjanda og sem inniheldur föstu samningsákvæðin sem kveðið er á um í þessari ákvörðun og þessi ráðstöfun skal ekki ná yfir annars konar gagnavinnslu eða hafa annan tilgang svo að meginreglan um takmörkun vegna tilgangs, sem sett er fram í tilskipun 95/46/EB, sé virt.

Review: Every candidate corrupts sub-processing/data-agent/contract or purpose-limitation relationships; correct directive number alone insufficient.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Auk þess skal undirfjölfunina einungis gilda rekstri sem samkvæmt samningnum milli gagnaflutnings- og gagnainnflutningsins þar sem undirfylltar samningargreinar eru gert samkvæmt þessari ákvörðun og hún skal ekki vísa til mismikla rekstri eða tilskusviða til þess að meginreglunni um takmarkaða markmiði sem sett er fram í tilskipun 95/46/EB sé fylgt.

Candidate 1: Að auki skulu undirrekandi forritinu einungis innihalda það sama aðgerðir sem samningin um dreifingu gögnum inni og út gerðir innihalda staðla samningsaðgerðirnar sem kveðið er á um í þessari ákvörðun og skulu ekki beita aðrar rekstrarafurðir eða tilgangi svo að þetta reglur um takmarkaða meginmarkmiði, sem kveðið er á um í tilskipun 95/46/EB, sé uppfyllt.

Candidate 2: Að auki ætti að undirprentunin sé eingöngu skipulaginn sem samið er í samninginu um gagnamögnunaraðlun og -skráningu, þar sem uppáhaldar samningarlögum er fylgjað sem kveðið er á um í þessari ákvörðun og ekki má vísa til annars aðrar starfseininga eða til að skilgreina mismunandi upplýsingaverndar, svo að meginreglur sem kveðið er á um um að ræða með tilskipun 95/46/EB séu uppfylltar.

Candidate 3: Auk þess skulu niðri verkefnið aðeins vera aðgerðir sem samþykkt var um í samninginum um gagnamögnunaraðskriftar í niðurverkefni, sem samhliða staðla samningsaðgerðirnar sem kveðið er á um í þessari ákvörðun, og það skal ekki vísa til annarra verkefna eða aðskildra þeirra markaðsins fyrir að viðeigandi meginreglun fyrir markaðssetningu, sem kveðið er á um í tilskipun 95/46/EB, sé nýtt.

Candidate 4: Í aukinni skipti skal undirkerfið aðeins vera upptöku sem samkvæmt samningi hansinni milli gögnumfæra og gögnuminnna, þar sem fylgjast er með staðla samningsmála sem kveðið er á um í þessari ákvörðun, og upptöku skal ekki vísa við mismunandi rekstrarferli eða aðstæður svo að meginreglunin um takmörkuð viðmiðanir, sem til komið er í tilskipun 95/46/EB, sé uppfyllt.

Candidate 5: Að auki skal undirprentunin einungis vera í samræmnum rekstri sem samþykkt er milli gagnaútgefanda og gagnainnöfnunar eftir fyrirbyggjandi samningslögum sem kveðið er á um í þessari ákvörðun og leið og ekki verða um annað fyrirkomulag eða tilgangar til að fylgja því að bólguskeiðisreglunni sem kveðið er á um í tilskipun 95/46/EB sé fylgt eftir.

Candidate 6: Auk þess skulu undirbúningarnar aðeins vera réttar þeir starfsemi, sem samningin um geymslu gögnum innleiðir, sem samþykktar eru samkvæmt þessum ákvörðun og geta ekki tekist til annarra starfsemi eða hagsmuna svo að meginreglurnar um takmarkaðina aðferð, sem kveðið er á um í tilskipun 95/46/EB, sé uppfylltar.

Candidate 7: Að auki skal undirbreiði það líka aðeins vera aðgerðir sem samið eru samkvæmt samningi um gagnaútgjöf og gagnainnflytjendustarfsemi, þar sem eftirfarandi kostir til skipulags er kveðið á um, og skal ekki vísa til annarra aðgerða eða ástæða sem birta þann reglunni um takmarkaða markmið í tilskipun 95/46/EB.

</details>

<details><summary>final_semantic_review #22 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:512

English: Another team member, Ana Duarte Cabral from the Laboratoire d'Astrophysique de Bordeaux, France, emphasises that "the ALMA observations reveal the spectacular details of the motions of the filamentary network of dust and gas, and show that a huge amount of gas is flowing into a central compact region".

Reference (shown after audit): Annar meðlimur í rannsóknarhópnum, Ana Duarte Cabral við Laboratoire dAstrophysique de Bordeaux í Frakklandi, undirstrikar að „mælingar ALMA leiða í ljós stórkostleg smáatriði í hreyfingu gas- og rykslæðanna og sýna að geysimikið magn af gasi streymir inn að þéttasta svæðinu í miðjunni.“.

Review: Filamentary dust/gas network and its motions are corrupted or absent.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Önnur liðmanni í hópnum, Ana Duarte Cabral frá Laboratoire d'Astrophysique de Bordeaux í Frakklandi, kemur fram á það að „sýnir ALMA mælingarinnar skýrslu um snertingu vetrarbrauta og gasins í sér, og sýna að mikil magn af gasi flæðist inn í miðvettanum“.

</details>

<details><summary>final_semantic_review #23 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:1069

English: By using the SPHERE instrument on ESOs Very Large Telescope (VLT) - one of the most powerful planet-hunting instruments in existence - the international team has made the first robust detection of a young planet, named PDS 70b, cleaving a path through the planet-forming material surrounding the young star.

Reference (shown after audit): Með SPHERE mælitækinu á Very Large Telescope (VLT) ESO - sem er eitt öflugasta reikistjörnuleitartæki heims - sáu stjörnufræðingarnir hvernig reikistjarnan unga, PDS 70b, plægir sig í gegnum efnisskífuna sem umlykur stjörnuna.

Review: All corrupt SPHERE/VLT instrument, planet detection and path through planet-forming material.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Við notkun SPHERE mannleysu á V-Irgamagskotunum (VLT) á ESO, sem er viðeigandi aðalinn lífleyfinu til að leita úr köllunum, hefur alþjóðasamstöðurinn komið fram fyrsta sterkri eftirlit með ungum köllunum, nýttanum PDS 70b, sem hreinir í lýsingu úr þeim efni sem mundur er til að gera nýja gegn stjarnina.

Candidate 1: Með notkun SPHERE eftirferðarhenda á Veltýltingunni ESO (ESO Very Large Telescope) - einhverjar versta hamingjuhlökkuna til að leita til ára heimsíða - hefur sýnt í fyrsta augnablikinu að yngri heimurinn, nýtt á númer PDS 70b, fljúga út í það fæðingu þar sem nýja stjórinn er verið búinn.

Candidate 2: Með notkun SPHERE tímabilsins á Vísuðum miklu æðisunni í ESO (ESO Very Large Telescope) - einu af þeim meist virkum áhersluafurðum sem hafa verið gert fyrir þjóðann hefur gert fyrsta sterkri áherslu á unglögum, náttúruna PDS 70b, sem er að leiðri um umhverfið sem leyst er við nýju stjarnann.

Candidate 3: Með notkun SPHERE-gefna málsmeðferðar á verjasta stórum teins (VLT) í ESO hefur hagsmunaleikrásan tveimur tegundir mínustuðlaða insöngur, PDS 70b, sýnt sýni í einstökum vopnum í umhverfið um jöfnu úr teimum yngri staurinnar.

Candidate 4: Með notkun SPHERE-venjuna á VLT-veljastjórnunarmagnslitinum ESO hafi alþjóðalegar fólkið gert fyrsta styrkir á júnnarstarfsemi, nýttu PDS 70b, sem hefur fatta leið í hliði af vefjum, sem eru í vefjum um andaði júnnarstara.

Candidate 5: Með notkun SPHERE-fermlinu á storku loftforskvæði ESO (ESO Very Large Telescope) (VLT) - einu af sterkustu stjórnunarfermlinum fyrir stórjúkja - hefurðarfræðileg hópið gert fyrsta sterkri greiningu á ungum jórði, nýtt kallað PDS 70b, sem hækkaðar hefur störf í loftmatsverði, sem um hún haldið er um, um kynningsstærðina sem eru í nýju stjórnu.

Candidate 6: Í kostun SPHERE-ferlísins á stöðugum, stórum teklunni ESOs Vélarstorkunarfyrirtækis (VLT)-eins af stóra og sterkasta véllyfjarmiðunaraðferðum sem til hætti er hafa lögbær hópur í umglæði annars ammis, llamátt PDS 70b, stýrt yngriuðu Vél úr því föst efni sem snertir umhverfið, sem eldri stjarnaðinn er um rúðað.

Candidate 7: Með notkun SPHERE-ferðarhjálpuna á VÍRUR-teknarstarfsemi ESOs (Very Large Telescope) - einnar af stærsta hækkufjárhjálpununum sem vera í gegnum - hefur alþjóða starfsmenn það fyrsta tær rýmum sem gefur upp líkur af unga heimsóknar við PDS 70b, sem endar á umhverfislega niðri í umhverfið sem tekið er úr því að geira það hvar fyrir eldri stjarnanum.

</details>

<details><summary>final_semantic_review #24 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eso:554

English: In the lower part of the image a big chunk of the molecular cloud that gave birth to these stellar youngsters still can be seen.

Reference (shown after audit): Á neðri helmingi myndarinnar sést stór hluti af sameindaskýinu sem gat af sér stjörnurnar ungu.

Review: Molecular cloud is replaced by an unrelated material expression.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Í lágsta hluti myndarinnar er stóra hlut af líkamalefnið sem fengið þessum stjarnakrökkum á upphafi enn í sér.

</details>

<details><summary>final_semantic_review #25 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:2120

English: In order to facilitate data flows from the European Union, it is desirable for processors providing data-processing services to several data controllers in the European Union to be allowed to apply the same technical and organisational security measures irrespective of the Member State from which the data transfer originates, in particular in those cases where the data importer receives data for further processing from different establishments of the data exporter in the European Union, in which case the law of the designated Member State of establishment should apply.

Reference (shown after audit): Til að auðvelda gagnaflæði frá Evrópusambandinu er æskilegt að vinnsluaðilar, sem veita mörgum ábyrgðaraðilum gagna í Evrópusambandinu gagnavinnsluþjónustu, fái leyfi til að beita sömu tæknilegu og skipulagslegu öryggisráðstöfunum, óháð því frá hvaða aðildarríki gögnin eru flutt, einkum í þeim tilvikum þar sem gagnainnflytjandinn tekur við gögnum til frekari vinnslu frá mismunandi starfsstöðvum útflutningsaðila í Evrópusambandinu, en þá gilda lög þess aðildarríkis þar sem starfsstöðin er staðsett.

Review: All corrupt processor/controller/importer/exporter roles or the establishment-law conditions.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Til þess að draga úr flutningum gögn frá Evrópusambandi er réttlegt að meðferðarþegar fá gögn (processors) sem veita gagnagjaferaðlun þátttakendur í Evrópusambandinu séu heimilt að gera sömu tæknilega og stjórnsýslu- öryggisvörunir án tillits til aðildarríkis þar sem gögnin bori fram samkvæmt, einkum þegar gagnasamfærðarið bahar gögn sem öðrum stöðum útflutningsþegara í Evrópusambandinu gefa nýtt gagnafrumskerfið, þar sem skal beita löggjöf tilnefndrar aðildarríkisins.

Candidate 1: Til þess að gera gagnagjaf frá Evrópusambandinu auðvelt er æskilegt að vinnuveitendur, sem veitir gagna- rekstrarþjónustu til meira endurspeglinga gagna-/innprófunaryfirvalda í Evrópusambandinu, séu heimilt að beita sömu tæknilegum og stjórnsýsluefnislegum öryggismeðferðum án tillits til aðildarríkis af því frá sem gagna- rekstrarflytjan er hér fyrir fram á, einkum þegar gagna- innflytjandan næst gagna frá annarra stofnanum fyrir gagna- úflings í Evrópusambandininu, þá skal þá beita löggjöf landsins þar sem stofnunin er tilnefnd.

Candidate 2: Til þess að auðvelda gagnagjöf frá Evrópu- samræðunni ætti því að hægt sé að aðildarríkinu á að veita gagna- útvarpsfyrirtækinum sem fá gögn, sem eru útvarpaðir, samanborið við fleiri gagna- megi í Evrópu- samræðunni, sambærilegar tæknilegar og stjórnsýslu- kerfi, án tillits til aðildarríkisins þar sem gagnirnir eru sendar úr, einkum þegar gagna- innameðaerðin fær gögn til frekari gagna- útvarps frá mismunandi stofnunum sem senda gagna í Evrópu- samræðunni, og án tillits til hvers aðildarríkis sem stofnun sendir gagna í Evrópu- samræðunni.

Candidate 3: Til þess að auðvelda gagnamöguleika frá Evrópusambandinu ber, í tengslum við þau stjórnendur gagnasjóða sem fá gagnagjaf, að heimila vera að þau ekki skuli fá að gera sami tæknilega og stjórnunarheimildir án tillits til þess aðildarríkis, sem gagnamálastarfsemi er hnefil frá, einkum þegar gagnamálastarfsemi hefur viðkomist frá mismunandi stofnunum gagnamálastarfsemi í Evrópusambandininu, þá skal beita lögum þeirra aðildarríkis, sem tilnefnt er til staðfestu.

Candidate 4: Til þess að skipti gögn fari greinilega um evrópubandalaginu er krafist að tæknifyrirtækjum sem leggja út gögn í fjölda í umfangi tilskipana evrópubandalagsins að vera heimilt að beita sömu tæknilegar og stjórnsýslustöfunar- kerfin, óháð því hvaða aðildarríki gögnin koma frá, einkum þegar innfylgjandi er fjármálagjafa gefi gögn til frekari gjafar úr annarrum stofnanum úr evrópubandalagsins sem sendir gögnum, þá skal beita löggjöf staðfestu aðildarríkisins.

Candidate 5: Til þess að auðvelda gagnamögnun frá Evrópusambandinu er það bein til að heimila rekstillum sem veita gagnagjafarþjónustu fyrir nokkrum gagna- skipum í Evrópusambandinu að beita sömu tæknilegum og stjórnsýsluverkunum að því er varðar aðildarríkið sem gagnaferðin hefur upprunalegt, einkum þegar gagna- innflytjendurinn fær gagna frá annarra stöðvum skýrimþáttanna, sem skýrsluþéttur evrópska aðilinn er sendur úr, og ætti þá að beita lagi tilnefnda aðilsins.

Candidate 6: Til þess að auðvelda gagnagjöf frá Evrópusambandinu er hægt að heimila vinnu- stofum, sem veita gagna- reikningssér, einstaka gagnaarkar til vísindaábyrgja í Evrópusambandinu, að beita sama tæknilega og stjórnsýslufyrirbyggjandi ráðstöfunum óháð því hvaða aðildarríki gagnaflutningin hefur upphaf, einkum þegar gagna- innflytjandi fær gagna til fyrirframreikninga frá annarri stofa útflutningsdómara í Evrópusambandinu, þá skal beita lögum tilnefnda aðildarríkisins.

Candidate 7: Til þess að auðvelda flutninga gögn frá Evrópusambandinu, er þá þarf að leyfa gjafara, sem veita gagnavinnuþjónustu fyrir nokkrum gagnavinnu- tilhöndlumannir í Evrópusambandininu, að beita sömu tæknilegum og stjórnunarlögum um öryggi án tillits til hvaða aðildarríkis flutningin komur frá, einkum þegar gagnasjóandi fær gagna frá öðrum stöðum gagnasjóandi í Evrópusambandininu við að slík gagna verði fara út til frekari gagnavinnu, þá skal beita lögum þeirra aðildarríkis sem verið er í því skyni.

</details>

<details><summary>final_semantic_review #26 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:ema:607

English: Since the possibility of increased risk of cancer development in patients with newly diagnosed dysplasia treated with infliximab is not established, the risk and benefits to the individual patients must be carefully reviewed and consideration should be given to discontinuation of therapy.

Reference (shown after audit): Þar sem ekki hefur verið gengið úr skugga um hugsanlega aukna hættu á krabbameinsmyndun hjá sjúklingum með nýgreindan misvöxt sem fá infliximab, verður að endurskoða gaumgæfilega áhættu og ávinning fyrir hvern sjúkling um sig og íhuga á að stöðva meðferð.

Review: Unestablished risk premise and newly diagnosed dysplasia are corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þar eð aðildarráðstöfunin hefur ekki verið áfram til að hægt sé að greina áhættu af aukinni áhættu á því að krabbameini kemur fram hjá sjúklingum með nýlega klínískt greint skurðbreyting í meðferð með infliximabi skal meta mikilvægi áhættu og ávinning fyrir hverja sjúkling og taka tillit til þess að hætta meðferð.

</details>

<details><summary>final_semantic_review #27 · after · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:3265

English: There's a police convention out there.

Reference (shown after audit): Það er lögregluráðstefna þarna úti.

Review: Police convention is not expressed by the invented compound.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það er lögreglukonar úti.

</details>

<details><summary>final_semantic_review #28 · before · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:434

English: The guest of honour was the President of Chile, Sebastián Piñera.

Reference (shown after audit): Sebastián Piñera, forseti Chile, var heiðursgestur.

Review: None preserves guest of honour being President of Chile; name copied without correct role.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Dælubláin og viðbótarbláin var hjá Prósótt í Chile, Sebastián Piñera.

Candidate 1: Jafiðið í þátti var hugarðarminn Chile, Sebastián Piñera.

Candidate 2: Gjásturinn í kvenjófinu var hryggjufyrirtæki Chile, Sebastián Piñera.

Candidate 3: Dýrilögðurnirinn var flankamenni lífveitanda Hílens, Sebastián Piñera.

Candidate 4: Ótrúður hissaði var vicekonungur Chile, Sebastián Piñera.

Candidate 5: Þjófaþóttinn var hreiðarmannur Chile, Sebastián Piñera.

Candidate 6: Mjögþættið var hrengispresenda í Chile, Sebastián Piñera.

Candidate 7: Hefndarheitið var Préstur Chile, Sebastián Piñera.

</details>

<details><summary>final_semantic_review #29 · after · greedy · technical_short · F</summary>

Source ID: p13official21:test:ema:2124

English: If in doubt, talk to your doctor or pharmacist.

Reference (shown after audit): Ef þú ert í vafa, skaltu leita ráða hjá lækninum eða lyfjafræðingi.

Review: In doubt becomes in trouble, changing the consultation condition.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef þú ert í vanda skaltu tala við lækninn eða lyfjafræðing.

</details>

<details><summary>final_semantic_review #30 · before · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:2128

English: Don't you worry about those dope smokers and nudists down below there?

Reference (shown after audit): Hefurðu ekki áhyggjur af dóphausunum og striplingunum þarna?

Review: Dope smokers/nudists and location are not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Viltu ekki hafa áhyggjur af þessum döpum og náttúruþjálfum?

</details>

<details><summary>final_semantic_review #31 · after · G8 · technical_long · U</summary>

Source ID: p13official21:test:eea:43

English: Where plant protection products containing the active substance are intended to be used in cold climatic conditions, the tests have to be conducted where DT50lab, determined at 10 °C and at a moisture content of the soil related to a pF value of 2 to 2,5 (suction pressure) is greater than 90 days.

Reference (shown after audit): Þegar nota á plöntuvarnarefni, sem innihalda virka efnið, í köldu loftslagi verða prófanirnar að fara fram þar sem DT50lab er meira en 90 dagar, ákvarðað við 10°C og í jarðvegi með rakainnihaldi sem miðast við pF-gildi 2 til 2,5 (sogþrýstingur).

Review: Candidate2 retains most conditions/numbers but suction pressure becomes a nonstandard collection-pressure term; cannot certify the technical condition. Others clearly corrupted.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Ef lyf sem vernda plöntu innihaldu virka efnisins eru ætlað til notkunar í kaltum umhverfismatsstöðum, skulu prófanir fara fram í kópum þar sem DT50lab, ákvarðað í 10°C og í mjóðinni í yfirborði til 2-2,5 sýrum (sýrueðli) er meiri en 90 dagar.

Candidate 1: Ef notkun á plöntuhemlum sem innihalda virka efni er áhugað fyrir hjálagtum líghraðum aðstæðum, þarf að framkvæma prófunnar þar sem DT50lab, sem ákvörðuð er í 10°C og víðmyndastigi í jarði sem tengist pF gildi 2 til 2,5 (lengingssvefi), er meiri en 90 daga.

Candidate 2: Ef um er að ræða notkun plöntuvarnarefna sem innihalda virka efni í kaltum loftsskilyrðum þarf að framkvæma prófanir þar sem DT50lab, sem er ákvarðaður við 10°C og vökvastigi í jörðu sem tengist pF-gildi 2 til 2,5 (safniþrýstingi) er stærri en 90 dagar.

Candidate 3: Ef um er að ræða notkun plöntuvarnarefna sem innihalda virka efnin með fyrirvaranum með hárna líffæri á að prófa þau ef DT50lab, á vísanlega 10°C og á vökvaþéttni yfir í jarðæðin sem tengist pF gildi 2 til 2,5 (þrýsting) er að vera meiri en 90 daga.

Candidate 4: Ef vörn völdum á plöntum er áhugað til notkunar við kaltikvarða skal framkvæma prófanir þar sem DT50, á 10°C og vökvasityrningu sem tengist pF gildi 2 til 2,5 (sýruþrýstingur), er stærri en 90 daga.

Candidate 5: Ef hægt hefur verið að nota plöntuhemjandi vörur sem innihalda virka efnin þar sem það er notað við kalt skýra, skulu mælingar gefnar ásamt þeim þar sem DT50lab, á 10 °C og á rýmubroti sem tengist 2-2,5 (sirkvöðubroti) er meiri en 90 dagar.

Candidate 6: Ef flöguðar varnarefni, sem innihalda virka efnið, eru ætlaðir notuð við kæli varnirinnar skal gera prófanir þar sem DT50lab, sem ákvarðað er við 10° C og í vökvalegu þurrði sem tengd er pF gildinum 2-2,5 (útsæðisþrýstingi), er meiri en 90 daga.

Candidate 7: Ef lyf, sem innihalda virku efnin, ætlað er að nota við kaltum loftstengdum ástandi, skulu tilraunir gefnar upp ef DT50lab, á 10 °C og með 2 til 2,5 (sýrufjölgunarhlutfall), er meiri en 90 daga.

</details>

<details><summary>final_semantic_review #32 · after · greedy · technical_medium · F</summary>

Source ID: p13official21:test:ema:1458

English: This is important to make the medicine easier and more comfortable to inject.

Reference (shown after audit): Þetta er mikilvægt til þess að auðveldara og þægilegra sé að sprauta lyfinu.

Review: More comfortable becomes old.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þetta er mikilvægt að gera lyfið auðveldari og gamall til inndælingar.

</details>

<details><summary>final_semantic_review #33 · before · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:825

English: The process of dust trapping is explained in an earlier release (eso1325).

Reference (shown after audit): Þetta ferli, þegar ryk festist, er útskýrt í eldri fréttatilkynningu (eso1325).

Review: Dust-trapping process remains corrupted/untranslated English rather than an intelligible Icelandic concept.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Verkefnið með því að trapa dust er lýst í fyrri útgáfu (eso1325).

</details>

<details><summary>final_semantic_review #34 · after · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:434

English: The guest of honour was the President of Chile, Sebastián Piñera.

Reference (shown after audit): Sebastián Piñera, forseti Chile, var heiðursgestur.

Review: Candidate3 gives a guest but omits honour status; all others corrupt guest/president roles.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Drottningurinn var Sebastían Piñera, forseti Chile.

Candidate 1: Jafiðið sýnitsýna var Sebastián Piñera, forseti Chile.

Candidate 2: Vinuvaldandi var Sebastián Piñera, forseti Chile.

Candidate 3: Gesturinn var Piñera Sebastián, forseti Chile.

Candidate 4: Stórarfélagið var hér með forsetanum, Sebastián Piñera, forsetanum Chile.

Candidate 5: Höfuðsmanur Chile, Sebastián Piñera var beinmannið.

Candidate 6: Gassögumennin var Sebastián Piñera, forseti Chile.

Candidate 7: Kveikningsborgarni var Próprésident Chile, Sebastián Piñera.

</details>

<details><summary>final_semantic_review #35 · after · G8 · technical_medium · U</summary>

Source ID: p13official21:test:ema:1610

English: The true extent of CNS penetration of lamivudine and its relationship with any clinical efficacy is unknown.

Reference (shown after audit): Í hve miklum mæli lamivúdín kemst raunverulega inn í miðtaugakerfið og samband þessa við klíníska verkun er ekki þekkt.

Review: CNS entry and unknown efficacy relationship partly recognizable in1/3, but true extent/penetration wording is too uncertain to confirm.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Líklegur upplýsingar um útferð áhöfnun lamivúdíns í miðtaugakerfi og tengsl við klíníska verkun eru ekki til staðar.

Candidate 1: Hluti innferðar lamivúdíns í miðtaugakerfið og tengingin við klíníska verkun er ekki þekkt.

Candidate 2: Reyndar útsetning á höfuðvöðva og myndun lamivúdíns á við áhrif í klínískum tilvikum er ekki þekkt.

Candidate 3: Vitað er ekki að vera hversu mikil bera lamivúdín eykur til miðtaugakerfisins og hvaða tengsl með klínískri verkun er.

Candidate 4: Ráðstæði endurtekis lamivúdíns til útbrotar í heilaheilabúanefni og tengsl þess við klíníska virkni eru ekki þekktir.

Candidate 5: Hjáhlutin lamivúdín í heilaæðum og tengsl þess við klíníska verkun eru ekki þekkt.

Candidate 6: Verulegri hátti lamivudíns innrennslis í lifrar- og heilaætlun er ekki þekkt, né tengsl þess við lyfjaformi fyrir klínískri verkun.

Candidate 7: Nákvæmar mælingar á inntaki lamivúdíns í miðtaugakerfið og tengsl með klínísku verkun, staðfest ekki í tengslum við nýrnastarfsemi.

</details>

<details><summary>final_semantic_review #36 · before · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:839

English: The Caisey Harlingten and ASH2 telescopes.

Reference (shown after audit): Caise Harlingten og ASH2 sjónaukarnir.

Review: None preserves telescopes, although names are copied.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Caisey Harlingten og ASH2 stjórnunargrein.

Candidate 1: Caisey Harlingten og ASH2 átæmi.

Candidate 2: Caisey Harlingten og ASH2 skapi.

Candidate 3: Caisey Harlingten og ASH2 tappa.

Candidate 4: Caisey Harlingten og ASH2 skotbólur.

Candidate 5: Caisey Harlingten og ASH2 stjörnuótta.

Candidate 6: Ljósfarandi Caisey Harlingten og ASH2.

Candidate 7: Caisey Harlingten og ASH2 skjólum.

</details>

<details><summary>final_semantic_review #37 · after · G8 · technical_short · P</summary>

Source ID: p13official21:test:eso:1198

English: The new observations are thus the first direct confirmation of such models.

Reference (shown after audit): Niðurstöður mælinganna eru þar af leiðandi fyrsta beina staðfestingin á útreikningunum.

Review: Candidate4 preserves new observations as first direct confirmation of these models.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [4]

Candidate 0: Nýja mælingarnar eru því fyrsta beinu staðfestir á slíkum líkamum.

Candidate 1: Nýjar mælingarnar eru því fyrsta beinu staðfestur á slíkum líkani.

Candidate 2: Nýjar upplýsingarnar eru það í þessu samhengi fyrstu beina staðfestir á sva tíma líkam.

Candidate 3: Nýir mælingarnar eru því fyrsta beinu staðfestingin á slíkum líkani.

Candidate 4: Nýjar mælingarnar eru því fyrsta beinu staðfestingu þessara líkönanna.

Candidate 5: Nýir mælingarnar eru því fyrstu beinu staðfestingar á slíkum skipum.

Candidate 6: Nýja mælingarnar eru þannig fyrsta beinkoll á slíkum líkamerjum.

Candidate 7: Nú skulu nýjar mælingarnar höfðast í fyrsta sinn að draga beint í ljósi samræmingu um svona líkennur.

</details>

<details><summary>final_semantic_review #38 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:409

English: Purpose: to determine whether the test facility, if engaged in studies using animals or other biological test systems, has support facilities and conditions for their care, housing and containment, adequate to prevent stress and other problems which could affect the test system and hence the quality of data.

Reference (shown after audit): Markmið: að ákvarða hvort prófunarstöðin, ef þar eru stundaðar rannsóknir með dýr eða önnur líffræðileg prófunarkerfi, hefur yfir að ráða búnaði og aðstöðu þar sem hægt er að hirða um þau, koma þeim fyrir og einangra þau á annan viðeigandi hátt þannig að koma megi í veg fyrir streitu og önnur vandamál sem gætu haft áhrif á prófunarkerfið og þar af leiðandi á gæði gagnanna.

Review: Care, housing, containment and preventing stress are corrupted, losing the inspection purpose.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Markmiðið: til að ákvarða hvort prófunarstöður, ef þær eru í notkun rannsóknanna með dýrum eða öðrum lífverulegra prófunarkerfum, hafa stjórnsýslustöðu og skilyrði til að hafa ábyrgð á því að hún verði áhugað, búast við og fylgja, svo að tryggja að það sé ótæm og annað sem geti haft áhrif á prófunarkerfið og þannig gæti verið ákvörðun á gæði gagna.

</details>

<details><summary>final_semantic_review #39 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:1138

English: “Terrestrial planets similar to our Earth are obvious targets for the search for life outside the Solar System, while comets are suspected to have played an important role in the appearance and development of life on our planet,” adds his colleague Emmanuël Jehin, who leads the cometary part of the project.

Reference (shown after audit): „Bergreikistjörnur sem líkjast jörðinni eru augljós skotmörk fyrir leitina að lífi utan sólkerfisins en halastjörnurnar eru taldar hafa leikið mikilvægt hlutverk í uppruna og þróun lífs á reikistjörnunni okkar“ bætir Emmanuël Jehin við en hann leiðir halastjörnuþátt verkefnisins.

Review: All corrupt terrestrial planets, extrasolar life search, comet role and/or project attribution.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: „Terísskur áfæðir sem eru svipir út úr Þjóðvélinsjörða eru skýr og ávallt markmiðið að leitinni í lífi útsjáðu að utan jörðsveðara, þar sem komjum er fyrir föt og frammistæði lífið á þessari aðila á sér,“ bætir í þáttu samanbær samfélagsins Emmanuél Jehín, sem leiddur komjumarskaupaða áætlunarinnar.

Candidate 1: „Hjá landþjóðu föstu sem eru svona líklega marktakaðar til leitunar lífs í líkaðra þjóði en okkur á Eyjum, þar sem kjarnufljósir eru ástandarlega orkunir við það,“ bætir samankvæmti hans, Emmanuël Jehin, og hinn vefþjónarstjórnandi, sem leitar á áætlanum í kjarnufljósirveru.

Candidate 2: „Tókalmæli utvarpið af réttum altíðum um græn í reynslu þar sem lífverið tekin er úr hálfu Solhreyminu, svo einhrar hreyfjar hafa hafa verið ekki of lítið tilhlýðingu við neiningu í reynslu þar sem lífverið alvarlega tekið er upp og það verður á skipti við réttar lífverið úr réttar lífverið,” að auki viðkomandi Efmanáúss Jehin, sem stjórnaður er við hreyfisstöðunum í samstarfsemiðinni.

Candidate 3: „Ég vil líklegt að þessi afvöxtarjörðar, sem eru bein og heilin á ökutækjum okkar, séu mikilvægi verkmiða að leita fram lífi úti í andrásögu, þó að í óvitaðum hætti við þannig að kömubláðir hafi viði mikilvægan hóp í uppáhald og þróun lífs á ökutækinu okkar.“ Skemmtileiki hans er Emmanuél Jehin, sem hefur fylgistr í fyrirhvarf í afvöxtumhljóðriði í vísindanefndinni.

Candidate 4: „Umbóðarnar til návangar út frá Jörði eru fljótlega markmiðarmyndir fyrir leit á líf í yfirhliða Sunsólarhópanna, og orkumar ásamt því að þær hafa komið í vandamál af því að flutningurinn hefur verið mikilvægt hverjarkost og þróun lífa á Jörðu okkar,” bætir það til við ekkiannir Emmanuél Jehin, sem er viðkomandi í skýrsluna á orkumar og leitar fyrir það.

Candidate 5: „Tilundir af einrædda heimur, sem eru liðarlega sambærilegir áréttu þegar, eru skýrsla og liður að leita að lífu út úr Solssjólinu, þar sem vanir eru skynskeðir að hafi ákveðið mikilvægt viðmiðanlegu áhrif í þegar og á undanleika lífs á hins evrópsu,“ björguíðar samanræddur hans, Émmanuél Jehin, sem leitar fyrir þeirri hlutverki í samstarfsemi á rannsókninni.

Candidate 6: „Heimaverantar sem eru líkefni heiminni hafa þóðar komið í hjá háttumastatandi markmiðum fyrir leitina á líf í utan jörðu Jörðu.“ Útreikningssamræmisnarlagi hans Emmanuël Jehin segir, sem fylgir á drögum eftir sérstaka hluta í verkefninu.

Candidate 7: „Hveður um landlætum föstum sem líka eru þessum Jörðu eru skýrðir markstöður fyrir rannsóknina um líf úti í solhlið. Þar sem nema, eru kúlið að hafa gert mikilvægt áhrif í viðkomandi úturslið og frumdu lífanna á Jörðunni,” bætir inni samfélöginn Emmanuël Jehin sem á ökumennuleika frá ökumennunni.

</details>

<details><summary>final_semantic_review #40 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:1385

English: Lynparza is indicated as monotherapy for the maintenance treatment of adult patients with platinum-sensitive relapsed BRCA-mutated (germline and/or somatic) high grade serous epithelial ovarian, fallopian tube, or primary peritoneal cancer who are in response (complete response or partial response) to platinum-based chemotherapy.

Reference (shown after audit): Lynparza er ætlað til einlyfjaviðhaldsmeðferðar hjá fullorðnum sjúklingum eftir bakslag platínunæms þekjufrumukrabbameins með stökkbreytt BRCA (kímlínu og/eða líkamsfrumu) með miklum vefjabreytingum (HGS [high grade serous]) í eggjastokkum, eggjaleiðara eða lífhimnu (frumkrabbamein) sem svara (algjör svörun eða svörun að hluta til) krabbameinslyfjameðferð sem byggist á platínu.

Review: All corrupt clinical cancer subtype, mutation/platinum-sensitivity/relapse conditions or response qualifications.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Lynparza er ætlað til einlyfjameðferðar til viðhaldsmeðferðar hjá fullorðnum sjúklingum með hægtengd endurheimt af völdum BRCA-þroska (germlingsþroska og/eða líffærasþroska) sem eru í hæstu líffærasýkingu í eggjastokki, hárgangabreiddan eggjastokk, fæðubrunni eða frumhöfn og berinni svörun (heildarfullan svörun eða hlutfallslegan svörun) við krabbameinslyfjameðferð með platínum.

Candidate 1: Lynparza er ætlað til einlyfjameðferðar við hvarfefnum aðgerðir hjá fullorðnum sjúklingum með BRCA-skurðsmit sem eru með hægri gráðu gráðuöðraudalaugakrabbamein í eitrunarvegum, fallopianvegi eða fyrirbyggðum krabbameini í kæli og svara meðferð með járnplatinum (platinum-based chemotherapy) í öðru lagi (fullanleg meðferð eða aðlagað meðferð).

Candidate 2: Lynparza er ætlað til einlyfjameðferðar til viðhaldsmeðferðar hjá fullorðnum sjúklingum með BRCA-affnslag sem stuttir er fyrir platín og með hæga sérþekkingu í kyrningafjölli, kyrklaga eða frumskýja (serous epithelial ovarian, fallopian tube, or primary peritoneal cancer), sem fá svörun (heildarsvörun eða hlutaþéttnisvörun) af lyfjameðferð með platín (platinum-based chemotherapy).

Candidate 3: Lynparza er ætlað til einlyfjameðferðar til viðhaldsmeðferðar hjá fullorðnum sjúklingum með BRCA-stökkbreyt sem verður aldrei sjúkur af nýgengi (germlíngefni eða líffæri) á hægri skali serusföng í eggjastokki, getnaflabúð eða frumuð eggjastokka (ovík, kílirháttar og eða víðmál) sem eru í svörun (fullan svörun eða hlutlaus svörun) af gegnum lyfjafræðilegan platinum meðferð.

Candidate 4: Lynparza er ætlað til einlyfja meðferðar við viðhaldslifur hjá fullorðnum sjúklingum með BRCA-skiltið (germlin- og/eða líffæra) hæga gráðu serusæju eggjastokk, fallopian-tunga eða grunnkjaftari- krabbamein sem tilvikið er við lyfjameðferð með platíníu en sjúklingurinn sýnir svörun (fullanleg svörun eða hlutfallsleg svörun).

Candidate 5: Lynparza er ætlað til einlyfja meðferðar til viðhaldsmeðferðar hjá fullorðnum sjúklingum með Brca-háþrýstingsertæka (germline and/or somatic) hægðaháttar, sérþekkingar (serous epithelial) eggjastokka, fallopian-tappa (fallopian-tapastokka) eða hægðaháttar sjálfkrafa frumuhúð (primary peritoneal cancer) sem svara (heildar- eða hluta- svar) á meðferð með platínum í bakgrunni.

Candidate 6: Lynparza er ætlað til einlyfjameðferðar við viðhaldsmeðferð hjá fullorðnum sjúklingum með BRCA-germlínnum, krabbamein í seröuml;uphafa eggjastokku, fallopian- túpu eða gríneftir í rúmmælum sem eru hækkar af völdum platinum og tengist platinumbundinni krabbameinslyfjum (platinum-based chemotherapy) við óvikaðar (fullkominni svörun eða hluta af svörun) eða óvikaðar svörun.

Candidate 7: Lynparza er ætlað til einlyfjameðferðar við viðhaldsmeðferð hjá fullorðnum sjúklingum með brísna BRCA, (germlin- eða eða líffæra) segnaþéttnis ægileg eitilkrabbamein í eggjastokki, háheilablöðru eða grunnbrjóst, með svörun (heiluhliði eða hlutverk heiluhliðar) við eitlaferlifæra meðferð með platinum.

</details>

<details><summary>final_semantic_review #41 · before · greedy · technical_short · F</summary>

Source ID: p13official21:test:ema:2722

English: See also ‘Bleeding or bruising after you stop treatment in section 4.

Reference (shown after audit): Sjá einnig „Blæðingar eða mar eftir að meðferð er hætt“ í kafla 4.

Review: Bruising becomes mixtures.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Sjá þó „Blæðing eða blöndur eftir að meðferð er hætt í kafla 4“.

</details>

<details><summary>final_semantic_review #42 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:970

English: In patients with mild hepatic impairment (Child-Pugh A), there was no significant changes in pharmacokinetics compared with normal healthy volunteers.

Reference (shown after audit): Hjá sjúklingum með væga skerðingu á lifrarstarfsemi (Child-Pugh A) voru engar marktækar breytingar á lyfjahvörfum samanborið við heilbrigða sjálfboðaliða.

Review: None preserves all mild hepatic impairment, no significant PK change and healthy-volunteer comparator; several change volunteers or impairment severity.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Í sjúklingum með mildan skerta lifrarstarfsemi (Child-Pugh A) var engin mikilvægar breytingar á lyfjahvörfiði við sér samanborið við óneigandi, heilbrigðið starfsmenn.

Candidate 1: Í sjúklingum með vægari lifraskort (Child-Pugh A) komu engin mikilvægum breytingum á lyfjahvörf samanborið við almennum, heilbrigðum heimanlegum mannmenn.

Candidate 2: Þegar um var að ræða mjög slæma lifrarvirkrar (Child-Pugh A) voru hjá sjúklingum varðaðu ekki óhlut deyti í lyfjahvörf hjá þeim samanborið við ósýnt heilbrigðu sjálfboðum.

Candidate 3: Í sjúklingum með væga lifrarverkun (Child-Pugh A) var viðkomandi í meinvart tíðni lyfjahvörf og mótefna hjá öðrum, óvikna heilbrigðum sjálfboðnum.

Candidate 4: Í sjúklingum með þrjústofna vandamál með lítill áhættu (Child-Pugh A) var engin háttar aukunar á lyfjahvörfiðar hafið samanborið við reglulega heilbrigðu heilsufólksþéttni.

Candidate 5: Í sjúklingum með lækk tækni á fögðri lifrar (Child-Pugh A) voru engin miklu áhrif á lyfjahvörf hjá þeim samanborið við meðalgjöf við heilbrigðu.

Candidate 6: Í sjúklingum með vægri lifrarstarfsemi (Child-Pugh A) var engar óhlutið skipt á lyfjahvörfið skipt í samanborið við áreiðanlega heilbrigðu almennum sjálfboðum.

Candidate 7: Hjá sjúklingum með milda lifrarverkunir (Child-Pugh A) var ekki yfir mikilvægum brotn á lyfjahvörfi, samanborið við sjúklingum með alvöru.

</details>

<details><summary>final_semantic_review #43 · before · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:20

English: These galaxies span a vast range of distances from us.

Reference (shown after audit): Allar eru þessar vetrarbrautir í mismikilli fjarlægð frá okkur.

Review: Galaxies and range of distances are not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þessar galæsir eru í miklu málsgrein af okkur.

</details>

<details><summary>final_semantic_review #44 · before · greedy · general · U</summary>

Source ID: p13official21:test:opensubtitles:1601

English: I don"t plan on wearing it that long.

Reference (shown after audit): Ég ætla ekki að vera lengi í honum.

Review: Not wearing for long is only approximately recognizable; vera med thvi may mean having it rather than wearing it.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ég ætla ekki að vera með því í lengi.

</details>

<details><summary>final_semantic_review #45 · before · greedy · technical_short · F</summary>

Source ID: p13official21:test:ema:2323

English: It is important to drink plenty of water to avoid dehydration.

Reference (shown after audit): Mikilvægt er að drekka mikið af vatni til að koma í veg fyrir ofþornun.

Review: Dehydration becomes dilution.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það er mikilvægt að drekka mikið af vatni til að koma í veg fyrir þynningu.

</details>

<details><summary>final_semantic_review #46 · after · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eso:1181

English: By combining light from three of the VLTIs 1.8-metre Auxiliary Telescopes with the AMBER instrument, this facility allows astronomers to see details equivalent to those a telescope with a mirror of 85 metres in diameter would see.

Reference (shown after audit): Með því að sameina ljós frá þremur 1,8 metra aukasjónaukum VLTI við AMBER mælitækið gátu stjörnufræðingar greint smáatriði sem væri aðeins gerlegt með sjónauka með 85 metra spegilþvermál.

Review: Mirror85metres in diameter becomes85metres in surface; auxiliary-telescope identity also drops.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Með því að setja ljósi úr þremur VLT-1,8 m sjónaukum ásamt AMBER mælitækinu geta stjörnufræðingar sést nákvæmar upplýsingar eins og sjónauki með 85 metra í yfirborði myndi sjá.

</details>

<details><summary>final_semantic_review #47 · before · G8 · technical_short · U</summary>

Source ID: p13official21:test:ema:2323

English: It is important to drink plenty of water to avoid dehydration.

Reference (shown after audit): Mikilvægt er að drekka mikið af vatni til að koma í veg fyrir ofþornun.

Review: Candidate3 paraphrases dehydration as drying; context is close but nonstandard medical wording prevents confident certification.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Það er mikilvægt að drekka of mikið vatn til að koma í veg fyrir það að drifur verður.

Candidate 1: Það er mikill þarf að drekka mikla vatn til að koma í veg fyrir vatnsskiptun.

Candidate 2: Það er mikilvæg að drekka margt vatn til að koma í veg fyrir vatnsþrýstingu.

Candidate 3: Það er mikilvægt að drekka mikið af vatni til að koma í veg fyrir þurrkunnunni.

Candidate 4: Það er mikilvægt að drekka mikið af vatni til að koma í veg fyrir vatnsþyngd.

Candidate 5: Það er mikilvægt að drekka víðt vatn til að koma í veg fyrir úthreinsun.

Candidate 6: Það er mikilvægt að drekka mikið vitna til að forðast útþyrftun.

Candidate 7: Það er mikilvægt að drekka mikið af vatni til að hafa aðgang að þvagræsni.

</details>

<details><summary>final_semantic_review #48 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:611

English: “With Mars losing that much water, the planet was very likely wet for a longer period of time than previously thought, suggesting the planet might have been habitable for longer,” said Michael Mumma, a senior scientist at Goddard and the second author on the paper.

Reference (shown after audit): „Þar sem Mars hefur glatað svo miklu vatni var reikistjarnan líklega blaut í lengri tíma en áður var talið, sem bendir til að Mars gæti hafa verið lífvænleg í lengri tíma,“ sagði Michael Mumma, vísindamaður við Goddard og annar höfundur greinarinnar.

Review: No candidate preserves both wet-longer and habitable-longer inference with the attribution.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: „Þegar Mars tapaði svona mikið vatni var reykjalegur lítið lígrótt lengri tíma en áður hafi tilkynnt um, sem gefur til kynna að reynslugrein leyfilegt hafi verið á reynslum á réttum stigi um lengri tíma“ sagði Michael Mumma, fyrirfræðingur í Goddard og annar aðalhöfundur greinarinnar.

Candidate 1: „Þegar Mars missti svona vökvi, var jörðin það líklegast húðann í lengri tíma en áður hefur verið heldur, sem bendir til þess að húðin hafi verið búsettarflugu í lengri tíma,“ sagði Michael Mumma, hæstur rannsóknarmannur við Goddard og aðra aðalhöfundur á greininni.

Candidate 2: „Þegar Mars mislist svo mikt vökvi, var reikistjörnin hægt á lengri tíma en áður hefur verið talið og er hugsanleg að reikistjörnin hafi verið hálegri lengur,“ sagði Michael Mumma, hæfilegur vísindamannur í Goddard og annar aðalhöfundur greinarinnar.

Candidate 3: „Þegar Mars tapar svona mikið af vatni, var líklega hágægt af vatn á langri tíma en áður hefur verið tilkynnt, sem bendir til að hún væri í lagi fyrirhugaðar,“ sagði Michael Mumma, hæsta vísindamannur í Goddard- viðbótarins.

Candidate 4: „Við því að Mars losar svona mikið vatn, er líklegt að jörðinni væri langtíma vatnslagur en um kom í fyrri tíma, sem hugsanlega gefur til kynna að hún séið í trúnaði lengur“ sagði Michael Mumma, frægur vísindamaður í Goddard og annar aðalhöfundur greinarins.

Candidate 5: „Þegar Mars tekur úr sig svona mikið af vatni, var reikistjörnin víðtaklega vatn til lengri tíma en við ávartum áður, sem sugir að reikistjörnin hafi verið ferskja í lengri tíma,“ sagði Michael Mumma, aðalhæfilegur vísindamannur í Goddard og annar í greininni.

Candidate 6: „Við því að Mars missti svona mikið vatn, var líklegt að jörðin væri líka vapastofugt í lengri tíma en áður hafi verið leitt til, sem bendir til þess að það væri hægt að vera í stað sinni lengra,“ sagði Michael Mumma, hæfilegur vísindamann í Goddard og annar rannsóknaraðili á greininni.

Candidate 7: „Þegar Mars tapaði svæði sem er svæðið með það miklu af vatni, er líklegt til að jörðin væri umfanglega vökvað í lengri tíma en greint hefur verið frá, sem getur gert til kynna að jörðin væri húðu að vera fyrir undirbúning lengur“ sagði Michael Mumma, meistararannsóknari í Goddard og annar erlendur á greininni.

</details>

<details><summary>final_semantic_review #49 · after · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:1121

English: Of course you're right, Starling... but it doesn't change anything.

Reference (shown after audit): Auðvitað er það rétt, Starling... en það breytir engu.

Review: You are right and it changes nothing retained; malformed opening is grammatical/style noise.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Að mikið er þú rétt, Starling... en það breytir ekkert.

</details>

<details><summary>final_semantic_review #50 · after · G8 · technical_long · U</summary>

Source ID: p13official21:test:ema:3025

English: Based on individual patient response and tolerability, the dose may be increased to 300 mg (15 ml) per day after an interval of 3 to 7 days, and if needed, to a maximum dose of 600 mg (30 ml) per day after an additional 7-day interval.

Reference (shown after audit): Eftir svörun og þoli hvers sjúklings má auka skammtinn í 300 mg (15 ml) á sólarhring eftir 3-7 daga og ef þörf krefur í hámarksskammt, 600 mg (30 ml) á sólarhring, eftir 7 daga til viðbótar.

Review: Most omit maximum/additional interval. Candidate7 has maximum600mg but patient-response/tolerance and interval syntax remain uncertain.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Með tilliti til þeirra svörun og þoli sjúklings er hægt að auka skammtinn í 300 mg (15 ml) á sólarhring eftir 3 til 7 daga tímabili og ef þörf er að vera að auka skammtinn í 600 mg (30 ml) á sólarhring eftir 7 daga tímabili.

Candidate 1: Bundinu svörun og þróun hjá hverjum sjúklingi má aukast skammturinn í 300 mg (15 ml) á dag eftir 3 til 7 daga fresti og ef þörf er ráðlaggt að aukast í 7 daga fresti í 600 mg (30 ml) á dag.

Candidate 2: Býð að skammtinum 300 mg (15 ml) á dag, eftir 3 til 7 daga tímabili, og ef þörf er á 600 mg (30 ml) á dag, eftir 7 daga tímabili.

Candidate 3: Bundinn á svið sjúklingsvarðar og þol mætti, má auka skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga fresti, ef þörf krefur skammtinn í 600 mg (30 ml) á dag eftir einkennum 7 daga.

Candidate 4: Hjá sjúklingum sem svara bæði meðferðinni og geta næstum 300 mg (15 ml) á dag áfram í 3 til 7 daga, en ef þörf er á að bæta skammtinn í 600 mg (30 ml) á dag að viðbótarmörkum 7 daga.

Candidate 5: Bundið á því að það sé 300 mg (15 ml) skammturinn er aukinn til 3 x 7 daga meðferðarinnar og ef þörf er einnig upptekinn í 600 mg (30 ml) skammturinn á 7 daga fresti.

Candidate 6: Byggt á svörun hjá einstaklingum og þolanleika getur skammtinn vers hæft í 300 mg (15 ml) á dag eftir 3 til 7 daga gáfa og, ef þörf er, í helstu skammti 600 mg (30 ml) á dag eftir 7 daga aukka.

Candidate 7: Sérfræðilega síðan sem fyrir sér stendur virkni og þol ágera má aukast skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga tímabili og ef þörf er á að auka síðan í 7 daga að hámarksskammtinum 600 mg (30 ml) á dag.

</details>

<details><summary>final_semantic_review #51 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:1323

English: If refills are not provided, the weight of the total primary packaging shall not exceed 3,7 g per wash for tablets and 1,7 g per wash for all other products.

Reference (shown after audit): Ef áfyllingar eru ekki í boði skal þyngd grunnumbúðanna í heild ekki vera meiri en 3,7 grömm á þvott ef um er að ræða töflur og 1,7 grömm á þvott fyrir allar aðrar vörur.

Review: Primary packaging and per-wash meaning are corrupted; thvag denotes urine, not washing.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef ekki er veitt endurfyllingu skal það líkamavikt heildarfrásætisins ekki vera meira en 3,7 g fyrir hverja þvag við töflur og 1,7 g fyrir hverja þvag við öll öðru afurði.

</details>

<details><summary>final_semantic_review #52 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:2183

English: For intravenous use, infusion systems with Actrapid at concentrations from 0.05 international unit/ml to 1.0 international unit/ml human insulin in the infusion fluids 0.9% sodium chloride, 5% dextrose and 10% dextrose inclusive 40 mmol/l potassium chloride using polypropylene infusion bags, are stable at room temperature for 24 hours.

Reference (shown after audit): Fyrir gjöf í bláæð er Actrapid stöðugt við stofuhita í 24 klst., í styrkleikum 0,05 alþjóðlegar einingar/ml til 1,0 alþjóðlegar einingar/ml af mannainsúlíni í eftirfarandi innrennslisvökvum; 0,9% natríumklóríði, 5% glúkósa og 10% glúkósa með 40 mmól/l af kalíumklóríði, þegar notaðaðir eru pólýprópýlen innrennslispokar.

Review: Every candidate changes potassium chloride to sodium chloride or invented salt, or loses critical solution/stability details.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Fyrir innrennslisnotkun eru innrennslisfyrirtæki með Actrapid á styrk frá 0,05 alþjóðlegu eining/ml til 1,0 alþjóðlegu eining/ml af mannainsúlíni í innrennslisvökva 0,9% natríumklóríð, 5% drexsúlósi og 10% drexsúlósi, þar með talið 40 mmól/l kórtilklóríð í innrennslisflögunum með pólýprópýlen innrennslisútblöðum, stöðug fyrir 24 klst.

Candidate 1: Fyrir gjöf í bláæð, innrennsliskerfi sem innihalda Actrapid með styrk frá 0,05 evrópsk/ílínúmsvörun/ml til 1,0 evrópsk/ílínúmsvörun/ml manna insúlíns á innrennslisrás 0,9% natríumklóríð, 5% dextros og 10% dextros, að meðtöldu 40 mmol/l natríumklóríð með pólýprópýlen innrennslibösur, eru stöðug á stofuhita í 24 klst.

Candidate 2: Fyrir notkun í bláæð, innrennslissjónavélar með Actrapid með styrk frá 0,05 alþjóðlegum einingum/ml til 1,0 alþjóðlegum einingum/ml af manna insúlíni í innrennslisvatni 0,9% natríumklóríð, 5% dextrosi og 10% dextrosi, í samhliða 40 mmol/l natríumklóríð, með pólýprópýlen innrennslisúrnautum, eru stöðugar við hemilstig í 24 klukkustundir.

Candidate 3: Fyrir notkun með innrennslisverkju, geymslurör um Actrapid með styrk frá 0,05 evrópskum einingum/ml til 1,0 evrópskum einingum/ml af insúlíni úr mönnu í innrennslitengdum vökva 0,9% natríumklóríð, 5% dextros og 10% dextros, með hugsanlega 40 mmól/l natríumklóríð, á 24 klst. stað við stofuhita.

Candidate 4: Fyrir innrennslisnot: innrennsliskerfi með Actrapid í styrk frá 0,05 alríkis eining/ml til 1,0 alríkis eining/ml af mannainsúlíni í innrennslisinu 0,9% natríumklóríð, 5% dextros og 10% dextros, þar með talið 40 mmól/l natríumklóríð, í pólýprópýlens innrennslispakkningum, eru stöðugir við stofuhita í 24 klukkustundir.

Candidate 5: Til notkunar í æð, innrennslistengd með Actrapid í þéttni frá 0,05 evrópskum einingum/ml til 1,0 evrópskum einingum/ml af mannainsúlíni í innrennslisvökva 0,9% natríumklóríð, 5% dextrosa og 10% dextrosa, með 40 mmol/l kútríumklóríð, á 24 klukkustundum við stofuhita, er stöðugur.

Candidate 6: Fyrir notkun í bláæð, innrennsliskerfi með Actrapid í þéttni frá 0,05 evrópskri eining/ml til 1,0 evrópskri eining/ml af mansinsúlíni í innrennslisfluðunum 0,9% natríumklóríð, 5% dextros og 10% dextros, þar með talið 40 mmól/l natríumklóríð, sem nota á pólýprópýlen innrennslislögunum, eru stöðug á stofuhita í 24 klukkustundir.

Candidate 7: Fyrir gjaf í bláæð notuðar innrennslisstykki með Actrapid með styrkleika frá 0,05 einstök eining/ml til 1,0 einstök eining/ml af mannainsúlíni í innrennslisflókinu 0,9% natríumklóríð, 5% dextros og 10% dextros, tæknilegur, 40 mmól/l natríumklóríð, með pólýprópýleninnrennsliskörfum, eru stöðugir við stofuhita í 24 klukkustundir.

</details>

<details><summary>final_semantic_review #53 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:850

English: When implementing this strand the Commission will in particular ensure consistency and complementarity with the activities conducted by other Commission services or by European agencies; in particular, the European Foundation for the Improvement of Living and Working Conditions and the Community RTD Framework programme and the European Centre for the Development of Vocational Training (Cedefop).

Reference (shown after audit): Við framkvæmd aðgerða í þessum flokki mun framkvæmdastjórnin sérstaklega sjá til þess að þær séu í samræmi við og komi til fyllingar starfsemi sem aðrar þjónustugreinar framkvæmdastjórnarinnar eða evrópskar stofnanir stýra, einkum Evrópustofnun um bætt lífskjör og starfsskilyrði, rammaáætlunbandalagsins um rannsóknir og tækniþróun og Evrópumiðstöð um þróun starfsmenntunar (CEDEFOP).

Review: Complementarity and the named institutions/programmes are materially corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þegar framkvæmd þessarar hóps er gerð mun framkvæmdastjórnin sérstaklega tryggja samræmi og aukabill við starfsemi annarra þjónustu framkvæmdastjórnarinnar eða evrópskra stofnana; sérstaklega Evrópuð stofnun fyrir bætur á aðgerðum til að bæta lífsgjafar- og vinnuþáttum og rannsóknaráætlun evrópska samanburðarríkisins um rannsóknir á tæknilegri og tæknilega sviði og Evrópuskrána fyrir þjálfun í sviði starfsþjálfunar (Cedefop).

</details>

<details><summary>final_semantic_review #54 · before · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:1073

English: Analysis of this spectrum indicated that its atmosphere is cloudy.

Reference (shown after audit): Greining á litrófinu sýnir að lofthjúpurinn er skýjaður.

Review: Spectrum and cloudy atmosphere are not intelligibly preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Í greiningu á þessum röð var tilgreint að loftið hennar sé skúlur.

</details>

<details><summary>final_semantic_review #55 · after · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:3404

English: A mother never gives up on her child.

Reference (shown after audit): Móðir snýr aldrei baki við barni sínu.

Review: Mother never giving up on her child retained despite imperfect idiom.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Mamma gefur aldrei upp á barni sínu.

</details>

<details><summary>final_semantic_review #56 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:2652

English: Put the needle fully into the skin as shown by your nurse or doctor (see picture 6).

Reference (shown after audit): Stingdu nálinni í húðina eins og læknirinn eða hjúkrunarfræðingur sýna þér (sjá mynd 6).

Review: No candidate correctly preserves needle plus full insertion and nurse/doctor demonstration; nituna is not needle.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Settu snivaslniðið til að því er leiði í hófnina eins og sjúklingarfræðingur eða lækni sagt( sjá mynd 6).

Candidate 1: Billaðu nituna fullt í húðina eins og þú færð með hjá sjúklingseinkenni eða hjúkrunaraðila (sjá mynd 6).

Candidate 2: Settu stólaðan nálli í húðina eins og sjúklingablandan eða læknirinn sýnir (sjá mynd 6).

Candidate 3: Settu hæglega níðinguna í húðina, eins og sjúklingsskólan þú eða læknirinn sýnir (sjá mynd 6).

Candidate 4: Settu peynn til fullt inn í húðina eins og sjúklingaskjölinn eða læknirinn sýnit (sjá mynd 6).

Candidate 5: Gefðu nínni hundrun í fullu í húðina eins og sjúklingakennarinn eða læknirinn sýnir (sjá mynd 6).

Candidate 6: Settu nituna á fullu inn í húðina eins og þú hefur farið fram hjá hjúkrunarfræðingnum eða lækninu (sjá mynd 6).

Candidate 7: Settu stefnuna í hliðar í húð við þig eins og sjúklingan þín eða læknin sé að viðhafa (sjá mynd 6).

</details>

<details><summary>final_semantic_review #57 · before · greedy · technical_short · P</summary>

Source ID: p13official21:test:ema:2175

English: Breast-feeding must be stopped on initiation of treatment with Voriconazole Accord.

Reference (shown after audit): Hætta verður brjóstagjöf þegar meðferð með Voriconazole Accord hefst.

Review: Stopping breastfeeding when Voriconazole Accord treatment starts retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Þegar meðferð með Voriconazole Accord hefst skal hætta á brjóstagjöf.

</details>

<details><summary>final_semantic_review #58 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:908

English: This bridge, which has not been seen before (and is too faint to show up in this picture), is somewhat bluer than either galaxy, indicating that it consists of stars created in gas that was drawn away from NGC 1387 by the gravitational pull of NGC 1399.

Reference (shown after audit): Þessi brú hafði ekki sést áður (og er of dauf til að koma fram á myndinni) en hún er nokkuð blárri en hin vetrarbrautin sem bendir til þess að hún samanstandi af stjörnum sem mynduðust úr gasi sem NGC 1399 hrifsaði úr NGC 1387.

Review: Bluer becomes greener, alongside other clause corruption.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þessi brú, sem hefur ekki séð fyrir fyrst og er of litla til að hafa sýnt fram í þessari mynd, er meira græn en öllum galáxjum og tekur til þess að hún verði úr stjörnum sem eru skapnaðar í loftsvíti sem var dragað úr NGC 1387 vegna gildisverkunar NGC 1399.

</details>

<details><summary>final_semantic_review #59 · before · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:3454

English: And I work for Danny.

Reference (shown after audit): Og ég vinn hjá Danny.

Review: Working for Danny retained; initial conjunction omitted only.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Ég vinn fyrir Danny.

</details>

<details><summary>final_semantic_review #60 · after · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:705

English: Normal long-duration GRBs last between 2 and 2000 seconds.

Reference (shown after audit): Venjulegir langir gammablossar standa yfir í 2 til 2000 sekúndur.

Review: GRB is replaced by a corrupted red-radiation/cancer term; numbers alone do not preserve the claim.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Lengd eðlilegra rauðum geislameinsbrotna er á bilinu 2 til 2000 sekúndur.

</details>

<details><summary>final_semantic_review #61 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:611

English: “With Mars losing that much water, the planet was very likely wet for a longer period of time than previously thought, suggesting the planet might have been habitable for longer,” said Michael Mumma, a senior scientist at Goddard and the second author on the paper.

Reference (shown after audit): „Þar sem Mars hefur glatað svo miklu vatni var reikistjarnan líklega blaut í lengri tíma en áður var talið, sem bendir til að Mars gæti hafa verið lífvænleg í lengri tíma,“ sagði Michael Mumma, vísindamaður við Goddard og annar höfundur greinarinnar.

Review: Wet/habitable longer inference and scientist attribution are corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: „Þar sem Mars missti svo mikið vatn var líklega lítilt út í langri tíma en áður hefði verið hugtakandi, því að hafa sýnt til að landið væri fyrirhuguður fyrir lengri tíma.“, sagði Michael Mumma, stórfjármannur í Góddart og annar aðilur á greininni.

</details>

<details><summary>final_semantic_review #62 · after · greedy · technical_medium · P</summary>

Source ID: p13official21:test:ema:772

English: These effects are called interactions, and can lead to serious side effects, or prevent proper control of other conditions you may have.

Reference (shown after audit): Þessi áhrif eru kölluð milliverkanir og geta valdið alvarlegum aukaverkunum, eða komið í veg fyrir viðeigandi meðferð annarra sjúkdóma hjá þér.

Review: Interactions, serious adverse effects and interference with control of other conditions retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Þessar áhrif eru nefndar milliverkanir og geta leitt til alvarlegra aukaverkana eða hindraði viðeigandi eftirliti með öðrum sjúkdómsstöðum sem þú getur haft.

</details>

<details><summary>final_semantic_review #63 · before · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:1086

English: Media representatives and other outreach groups will also be attending the event.

Reference (shown after audit): Fjölmiðlar og fræðsluhópar munu einnig sækja atburðinn.

Review: Media/outreach representatives attending an event not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Tilvísunarmenn og önnur áhersluverum fá einnig aðstoð á hins sviðs.

</details>

<details><summary>final_semantic_review #64 · after · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eso:502

English: The first five signals are very confident, while the sixth is tentative, and seventh more tentative still.

Reference (shown after audit): Fyrstu fimm merkin voru mjög sannfærandi en meiri óvissa ríkir um það sjötta og enn meiri óvissa um hið sjöunda.

Review: All corrupt signals and ordered sixth/seventh increasing uncertainty.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Fyrstu fimm öryggisöryggisverk eru mjög tunglavíkar en sjötthundraði er tilbún þess og sjötthundrunum er tilbún enn enn.

Candidate 1: Fyrstu fimm hættarinnar eru mjög áreiðanir, en sexútt er í betru tilviki og sjötútt enn fremur.

Candidate 2: Fyrstu fimm merkingarnir eru mjög þekkju, þar sem sjöttháttinu er fyrstu enda, síðsta ein hagalega enn.

Candidate 3: Fyrstu fimm yfirburðarnar eru mjög vissar en sexu yfirburðurinn er tækur og sjönu yfirburðurinn er enn tækrari.

Candidate 4: Fyrstu fimm mörk eru mjög róleg, en síðustu er í fjögurri sinn vottinn, og sjönum liggur sinn í fyrirsvörun.

Candidate 5: Fyrstu fimm útgefinu eru mjög tunglæga, en sjötthunni er næmið, en sjötthunni sína er engin næmið.

Candidate 6: Eftirfarandi fimm merkimiði eru mjög vissar en sjötthundurför varðandi sjötthundurför.

Candidate 7: Fyrstu fimm verkaðar eru til birta, en síðasti er þannig tilbúin.

</details>

<details><summary>final_semantic_review #65 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:1557

English: The Commission Communication ‘i2010 - A European Information Society for growth and employment (COM(), developing the Lisbon strategy, seeks to ensure coherence across the Commission's information society and media policies in order to reinforce the significant contribution of information and communication technologies to the performance of the economies of Member States.

Reference (shown after audit): Í orðsendingu framkvæmdastjórnarinnar „i2010 – upplýsingasamfélagið í Evrópu í þágu hagvaxtar og atvinnu“(COM (), þar sem Lissabon-áætlunin er útfærð, er leitast við að tryggja samræmi innan stefnu framkvæmdarstjórnarinnar um upplýsingasamfélagið og fjölmiðla í því skyni að styrkja mikilvægt framlag upplýsinga- og samskiptatækni til efnahagslegrar afkomu aðildarríkjanna.

Review: Invents a COM identifier and corrupts Lisbon strategy/policy-coherence relationships.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Í framkvæmdaðri sendunum frá framkvæmdastjórninni „i2010 – Evrópska upplýsingasamfélög til þróunar og starfs( COM(2009) 478), sem er að því erfiðu að þróa lán í Lissabón, reyndar fram á að tryggja samhliða hagsmuna um upplýsingasamfélög og fjarskiptatilvísun í ramma framkvæmdastjórnarinnar til að styrkja mikilvægan þáttur upplýsingakerfa og fjarskiptaferla í þróun aðildarríkjanna.

</details>

<details><summary>final_semantic_review #66 · after · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:2721

English: No, but one day, I'll take that cane away...

Reference (shown after audit): Nei, en einn góðan veðurdag á ég eftir að taka stafinn...

Review: Taking away a cane is not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Nei, en eitt dagur, færi ég þessu stóðinn...

</details>

<details><summary>final_semantic_review #67 · after · G8 · technical_medium · U</summary>

Source ID: p13official21:test:eea:2090

English: Member States shall require the competent authorities to monitor compliance with this Regulation effectively and take all necessary measures to ensure such compliance.

Reference (shown after audit): Aðildarríki skulu skylda lögbær yfirvöld til að hafa eftirlit með því að farið sé með virkum hætti eftir þessari reglugerð og gera allar nauðsynlegar ráðstafanir til að tryggja að farið sé að ákvæðum hennar.

Review: Candidate2 has most required actions but makes monitored compliance explicitly their own; broad regulatory oversight relation uncertain. Others materially corrupted.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Aðildarríki skulu krefjast lögbærra yfirvalda til að fylgjast með því að þessi reglugerð sé fullgilt og gera allar nauðsynlegar ráðstafanir til að tryggja það.

Candidate 1: Aðildarríkin skulu kveða á um það að lögbær yfirvöld eigi að fylgja til þess að þetta reglugerð sé fullgilt og geta allar nauðsynlegar ráðstafanir til að tryggja það.

Candidate 2: Aðildarríkin skulu krafast lögbærum yfirvöldum að fylgjast vel með því að þau uppfylli þessari reglugerð og gera allar nauðsynlegar ráðstafanir til að tryggja það.

Candidate 3: Aðildarríkin skulu kveða á reikfærni á það að lögbær yfirvöld eigi fylgjast með því að þau uppfylli þessa reglugerð eigi stuðullega og geri allar nauðsynlegar ráðstafanir til að tryggja það.

Candidate 4: Aðildarríkin skulu kveða á um það í skjal til lögbærra yfirvalda að þau fylgi áfram þessar reglugerðar með skilvirkan áhættueftirliti og gera allar nauðsynlegar ráðstafanir til að tryggja það.

Candidate 5: Aðildarríkin skulu kveða á um að lögbæra yfirvaldar hafi verið fylgt eftir skilvirku sannprófuninni að gera sinni til að fylgja skilyrðum þessarar reglugerðar og tekni allar nauðsynlegar ráðstafanir til að tryggja slíka sannprófun.

Candidate 6: Aðildarríkin skulu kveða á um það í þátttakendum, þar sem um er að ræða, að þau fylgi áfram þessari reglugerð með skilvirku hætti og aðeins þær aðgerðir sem nauðsynleg eru taka til að tryggja það.

Candidate 7: Aðildarríki skulu krefjast þess að lögbær yfirvöldi hafi skilvirkum eftirliti þannig að þau munu vera að fylgja reglugerðinni vel og gera allar nauðsynlegar ráðstafanir til að tryggja það.

</details>

<details><summary>final_semantic_review #68 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eso:1181

English: By combining light from three of the VLTIs 1.8-metre Auxiliary Telescopes with the AMBER instrument, this facility allows astronomers to see details equivalent to those a telescope with a mirror of 85 metres in diameter would see.

Reference (shown after audit): Með því að sameina ljós frá þremur 1,8 metra aukasjónaukum VLTI við AMBER mælitækið gátu stjörnufræðingar greint smáatriði sem væri aðeins gerlegt með sjónauka með 85 metra spegilþvermál.

Review: Auxiliary telescopes, astronomers and mirror-diameter comparison are corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þessi búnað er hægt að nota til að samfylgja ljósi frá þremur viðbótartengslum á 1,8 m í lengd sem eru fyrirhugaðar við VLT-tekni og AMBER-gerðina og því er hægt að gera stjórnunarmenn sér út í hlutum sem tekið er í tengslum við tegundinni sem hefur 85 metra diametr í myndi.

</details>

<details><summary>final_semantic_review #69 · after · greedy · technical_medium · P</summary>

Source ID: p13official21:test:ema:970

English: In patients with mild hepatic impairment (Child-Pugh A), there was no significant changes in pharmacokinetics compared with normal healthy volunteers.

Reference (shown after audit): Hjá sjúklingum með væga skerðingu á lifrarstarfsemi (Child-Pugh A) voru engar marktækar breytingar á lyfjahvörfum samanborið við heilbrigða sjálfboðaliða.

Review: Hepatic impairment, Child-PughA, no significant PK change and healthy-volunteer comparison all retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Hjá sjúklingum með vægt skerta lifrarstarfsemi (Child-Pugh A) var engin marktæk breytingar á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.

</details>

<details><summary>final_semantic_review #70 · after · greedy · technical_short · P</summary>

Source ID: p13official21:test:eso:278

English: Centaurus A has therefore been observed with many different telescopes.

Reference (shown after audit): Vetrarbrautin hefur þess vegna verið viðfangsefni fjölmargra ólíkra sjónauka.

Review: CentaurusA observed/measured with many different telescopes retained; duplicated preposition only.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Því hefur Centaurus A verið mælt með með margum mismunandi sjónaukum.

</details>

<details><summary>final_semantic_review #71 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:908

English: This bridge, which has not been seen before (and is too faint to show up in this picture), is somewhat bluer than either galaxy, indicating that it consists of stars created in gas that was drawn away from NGC 1387 by the gravitational pull of NGC 1399.

Reference (shown after audit): Þessi brú hafði ekki sést áður (og er of dauf til að koma fram á myndinni) en hún er nokkuð blárri en hin vetrarbrautin sem bendir til þess að hún samanstandi af stjörnum sem mynduðust úr gasi sem NGC 1399 hrifsaði úr NGC 1387.

Review: All corrupt bridge colour, faintness, stellar-gas origin or gravitational-pull relationship.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Hræðileg handlan, sem hafa ekki verið séð áður og er alveg hræðilegur til að líta á í myndin, er ánægilegari en bænum stjarnakornum, og því semgerðir að hann inniheldist stjörnur sem eru fengnar úr gjöf sem hefði verið ábreytt úr því lyfninu sem þótt í NGC 1387 og sem hverfið haft á bænum stjörnunum með því að hættanir fjallega áhættugjöf NGC 1399 hafði fengið áhætta.

Candidate 1: Þessi brú, sem hefur ekki hittð áður og verður langt í fyrirhluta að komi í ljósi í þessari mynd, er annað hvíli undir hvílið en hverri galáxja og tilheyrt að hún sé stjórnafla sem eru uppknötur í af loftríssmáli sem fór á úr NGC 1387 vegna grettisstöðvunar í NGC 1399.

Candidate 2: Þetta brú, sem hefur ekki séðð áður (og er ekki láttandi til að sýna upp í þessari mynd), er algengur borður en öllum galmu, það heimsækir að það séu stjörnur sem eru skapaðar úr lofthæi sem verður tekin úr NGC 1387 vegna gúta áhuga NGC 1399.

Candidate 3: Þetta bráður, sem er ekki séð áður og er of langt röndaskilinn til að horfa upp í þessari mynd, er blotuðhraðari en öllum galáksunum og tekur til þess að henni verði staðað af stjörnunum sem verða fram í gasi sem var skrúfan úr NGC 1387 með því aðeins því að hún var í árásinn við NGC 1399.

Candidate 4: Þetta bráður, sem hefur ekki séðð áður og er skemmta langt að leysast í þessari mynd, er svona graunari en bælið, til að gefa tilliti til að hann verði úr stjörnu sem eru skapnaðir í loftlegri lausn sem var dragið frá NGC 1387 við gegn áhættugreiningu NGC 1399.

Candidate 5: Þetta brú, sem hafa verið ekki séð áður og er ekki fyrir gagn í skýrunni, er fjarlægilegur hvítrari en öðru galaxjum, og endurspeglar það að þessa brú sé tekið úr stjörnunum sem eru uppþátt í loftsvæði, sem áður var dragið úr NGC 1387 með skrítunni NGC 1399.

Candidate 6: Þessi brú, sem hefur aldrei komið í ljós (og er öfugt langt að hún sé í myndnum) er seinni grára en hvert galásk, til þess að hanna að hún haldi af stjörnunum sem eru skapaðar úr gæði sem ástæðuna NGC 1399 hafði í sölum í gás sem wasstu af NGC 1387 með því að dræna var á því.

Candidate 7: Þessi bráður, sem hefur ekki séðð áður og til stúla migurgirnirnar, er stuttri hvítt en öðrum galákjur, til þess að hún er þá þátttöku úr stjarnum sem eru criaðir í stofunn, sem var myndast úr NGC 1387 vegna þar áhættugreinis NGC 1399.

</details>

<details><summary>final_semantic_review #72 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:571

English: To check power-operated windows/roof-panel systems/partition systems with reversing devices, a measuring instrument/test rod shall be placed through the opening from the inside of the vehicle or, in the case of a partition system, from the rear part of the passenger compartment in such a way that the cylindrical surface of the rod contacts any part of the vehicle structure which forms the boundary of the window/roof-panel aperture/partition.

Reference (shown after audit): Ef gera á athugun á rafstýrðum rúðum/þaklúgukerfum/skilrúmskerfum með enduropnunarbúnaði er mælitæki/prófunarstöng sett í gegnum opið innan frá úr ökutækinu eða, þegar um er að ræða skilrúmskerfi, frá aftari hluta farþegarýmis með þeim hætti að sívalt yfirborð stangarinnar snertir einhvern þann hluta ökutækisins sem afmarkar gluggann/þaklúguopið/skilrúmið.

Review: Powered systems, reversing devices, test rod and required contact geometry are corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Til að greina vopnlega styrkur í gluggi/rúttarhlutir/kerfi og því sem hægt er að endurheimta þær skal setja mælitækia/eftirlitsstöðu í útfluginn innan ökutækisins eða, ef um er að ræða kerfi, í bakhlið á borðsakafnið slíkt að yfirborði stöðvunarkerfisins skuli snertingin hafa snertingu á einhverri hluta stöðvunar ökutækisins sem eru líkur við gluggi/rúttarhlutir/kerfi.

</details>

<details><summary>final_semantic_review #73 · before · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:2130

English: Because Mr. Doyle called and said you have not been there all week.

Reference (shown after audit): Því að herra Doyle hringdi og sagði að þú hafir ekki mætt alla vikuna.

Review: There changes to here, altering the stated location.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Því Doyle hringdi og sagði að þú hefur ekki verið hér í viku.

</details>

<details><summary>final_semantic_review #74 · after · G8 · technical_medium · U</summary>

Source ID: p13official21:test:eso:356

English: The nebula lies more than four hundred times further away than the famous star.

Reference (shown after audit): Þokan er þó meira en fjögur hundruð sinnum lengra í burtu en stjarnan fræga.

Review: Candidate5 preserves >400times distance and famous-star comparison, but nebula is an uncertain nonstandard loan form; no confidently Icelandic full rendering.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Nebuðið er meira en fjórar hundraðsinna fjarlægð frá fyrsta stjörnunni.

Candidate 1: Nebúnaðurinn er meira en fjórum hundraðum sinnum fjarri en frægasta stjörnin.

Candidate 2: Neifarfarina er meira en fjögur hundraðsin tíð ekki fyrir stjörnuna.

Candidate 3: Nebulónið er meira en fjórir hunda sinnum fjarlægri en fyrirvistasta stjarnan.

Candidate 4: Nebúanum er meira en fjórum hundrað tímann fjarri en frægum stjörnunum.

Candidate 5: Nebularann er meira en fjögur hundruð sinnum fjarlægri en þeirri frægri stjörnunni.

Candidate 6: Nebulann er meira en fjórhundrað sinnum fjarlægri en uppsprettastjörnurinn.

Candidate 7: Nebulinn er meira en fjórhundraðsinna fjarlægir en frægast stjarnan.

</details>

<details><summary>final_semantic_review #75 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:918

English: "With such short orbital periods, the planets are between 20 and 100 times closer to their star than the Earth to the Sun. The structure of this planetary system is much more similar in scale to the system of Jupiters moons than to that of the Solar System," explains Michaël Gillon.

Reference (shown after audit): „Umferðartímarnir eru svo stuttir að reikistjörnurnar eru 20 til 100 sinnum nær móðurstjörnunni en Jörðin frá sólinni. Uppbygging þessa sólkerfis svipar því meira til Júpíters og tungla hans en sólkerfinu okkar,“ segir Michaël Gillon.

Review: Orbital-period, Earth/Sun and Jupiter-moon system comparison corrupted; speaker attribution missing.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: „Með svona skmælum umferðarfrámi eru þær planetarnir í milli 20 og 100 sinnum nálægri frá stjórni en Þjóðor frá Solu.“ „Stökkbreytingur þessarar hreyfla er mjög líklegari en áhliða Júpítra frá stjórnu en áhliða Solhreyfla.“

</details>

<details><summary>final_semantic_review #76 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:538

English: Previous observations had shown hotter, but much less dense, gas streaming away from NGC 253s star-forming regions, but alone this would have little, if any, impact on the fate of the galaxy and its ability to form future generations of stars.

Reference (shown after audit): Eldri rannsóknir höfðu sýnt að heitara en ekki jafn þétt gas streymdi burt frá stjörnumyndunarsvæðum NGC 253 en að það eitt hefði lítil eða ekki nokkur áhrif á örlög vetrarbrautarinnar og getu hennar til að mynda nýjar kynslóðir stjarna.

Review: Less dense becomes heavier; gas outflow and impact/future star-formation clauses corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Fyrri athugasemdir hafa sýnt að það var heitari og mjög þyngdarlegari stofnun áhættufrumur í stjarnafæðarhópum NGC 253 en það hefði ekki náð nokkru eða neinn áhrif á endurheimt galdranna og hvernig hún getur framkvæmt nýja stjarnafrumur.

</details>

<details><summary>final_semantic_review #77 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:611

English: “With Mars losing that much water, the planet was very likely wet for a longer period of time than previously thought, suggesting the planet might have been habitable for longer,” said Michael Mumma, a senior scientist at Goddard and the second author on the paper.

Reference (shown after audit): „Þar sem Mars hefur glatað svo miklu vatni var reikistjarnan líklega blaut í lengri tíma en áður var talið, sem bendir til að Mars gæti hafa verið lífvænleg í lengri tíma,“ sagði Michael Mumma, vísindamaður við Goddard og annar höfundur greinarinnar.

Review: All corrupt wetness/habitability duration inference and/or attribution.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: „Þegar Mars förgi svo mikið í vatni var átta lítil of litla líklegt að landin var næstunlega vatnað til lengra tíma en áður teljast, því að hafa sýnt því að landið væri líta tilhlýðilega húðbúður“ sagði Michael Mumma, vitneskandi í frumum almenningsráðherra frá Goddard og annar hluthafa aðyfnaðar í skýslunni.

Candidate 1: "Fyrir að Mars missti svölssvorni var það líklegast vandað í lengri tíma en það sem áður hefði verið líklega gert þá til að taka til þess að það gæti vera ávísulegt í lengri tíma," sagði Michael Mumma, hófóður eftirfengara nefndar í núám þar á.

Candidate 2: „Þar sem Mars misst svo mikt vatn var líklega merkt því að erust var lengri en skal áður hefði verið til staðar að átt fyrir að aðstandið væri dýralistið lengri en hún var á því tiltakandi,” sagði Michael Mumma, lífverafræðingur í Giddarwardi og annar aðilur í tekjunni.

Candidate 3: „Þar sem Mars hafði misvinn svona mikið vatn var líklegast þokur lengra en áður heyrði og björgnar til að við áttum að gæti fengist hafa venjuðarum færri tímabili í réttu,“ sagði Michael Mumma, æktur vísindanefndar í Göttingum og annar aðilinn á greinunni á kaupinni.

Candidate 4: „Við Mars skilfornu vatni hefur líklegt verið hægt að vera kláru fyrir langara tíma en áður hafði verið líkt, til að ræða að hægt væri að vera bærskrúða hæfir lengur,” sagði Michael Mumma, lifrarfræðingur sem er í háa stöðugur lífræðingur á Goddard og annar aðili á greininu.

Candidate 5: „Þegar Mars losir svo miklu vatni var það líklega mikilvæglegt vatnleg í lengri tíma en áður teljast, sem tilheyrir að það gæti verið húðlega færa fyrir lengri.“, sagði Michael Mumma, ónæmisstúlur sérfræðing í Góðard og annar aukst íðir að skrifnum.

Candidate 6: „Með Mars að lofa svona miklum vatni var líklegt að höfðið væggjandi lengra í lengri tíma en áður hefur verið metað, því að besti hlutir niður víði að hlutaðeigandi lífverandi hafi vossa á milli“ segir Michael Mumma, hæfir rannsóknarfræðingur í Goddard og annar aðili á greinum.

Candidate 7: „Þar sem Mars tók úr eftir þessu miklum vatni var lítil líka líktur sæ, nálægt til lengri tíma en áður meðtækar velt að Barðarhús var hljóðleg og ætt að geta gert ílifandi fyrir lengri tíma.“, sagði Michael Mumma, frumköstur rannsóknarnar í Goddard og annar aðili á skrifann.

</details>

<details><summary>final_semantic_review #78 · after · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:1878

English: That's not what Optimus would want.

Reference (shown after audit): Optimus hefði ekki viljað það.

Review: Negated claim about what Optimus would want retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Það er ekki það sem Optimus vildi.

</details>

<details><summary>final_semantic_review #79 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:329

English: The experiment marks the first time that APEX has taken part in VLBI observations, and is the culmination of three years hard work at APEXs high altitude site on the 5000-metre plateau of Chajnantor in the Chilean Andes, where the atmospheric pressure is only about half that at sea level.

Reference (shown after audit): Með tilrauninni er APEX í fyrsta sinn notaður í VLBI mælingum og er hápunkturinn á þriggja ára erfiðisvinnu við APEX sjónaukann sem er í 5.000 metra hæð yfir sjávarmáli á Chajnantor sléttunni í Andesfjöllum Chile, þar sem loftþrýstingur er helmingi minni en við sjávarmál.

Review: VLBI observations and culmination of three years hard work are corrupted; sea-level pressure comparison also unclear.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Rannsóknin er fyrsta sinn sem APEX hefur taktu þátt í miðlunum áhættugjöf og er endurtekningi þriggja árarskírteins á hæðri staðsetningu APEX á 5000 metri hæðar á Chajnantorsplata í Chile-Andes, þar sem loftþyngd er bara um hálft þá sem á landvöknum.

</details>

<details><summary>final_semantic_review #80 · after · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:504

English: The precise extent of the habitable zone depends on many factors.

Reference (shown after audit): Umfang lífbeltisins veltur á ýmsum þáttum.

Review: Habitable zone is replaced by unrelated invented terms in every candidate.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Mikilvægur smásvæði heimskara svæðis er háð margri fyrirliggjandi færibreyttra.

Candidate 1: Nákvæmri fæðingarvettirinninn til stjórnar á margum þætti.

Candidate 2: Nákvæmur fjarlægð trúheimilsins er háð margra þáttanna.

Candidate 3: Nákvæmar tíðni sævægar svæðisins tekur til mörga aðstæðna.

Candidate 4: Vissan styrkur sömu ramma sé stjórnun margrar aðstæðna.

Candidate 5: Nákvæmur umfang sætþjálanda varar til mörgu fyrirbæra.

Candidate 6: Nákvæm fjarlægð sæfisvettilsins er háð margra aðstæðna.

Candidate 7: Mikilvægar vinnsluáætlunin hægt er hálfátti hjástuðunarbanna.

</details>

<details><summary>final_semantic_review #81 · before · G8 · technical_short · F</summary>

Source ID: p13official21:test:eea:679

English: This relates to the gross earnings paid during the reference year.

Reference (shown after audit): Þetta lýtur að vergum tekjum sem eru greiddar á viðmiðunarárinu.

Review: Gross earnings not retained; candidate7 only says work amounts paid in reference year, losing gross-earnings scope.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þetta varðar haldskujuður áhættudauði í viðmiðunarrökunarsjóðinu.

Candidate 1: Þetta varðar alvöruð útgáfu sem greiðið var í viðmiðunarrök.

Candidate 2: Þetta varðar fyrirliggjandi úttegða frá áföngum.

Candidate 3: Það varðar alvöruðaránnin sem greitt var á ákvörðunarsálinnum.

Candidate 4: Þetta varðar grunnum áhættusækinu sem greiðið á á viðmiðunarságinn.

Candidate 5: Þetta varðar allt reiknuð fenginn útbúnaðar.

Candidate 6: Þetta varðar grunnaðgang sem veitt var í viðmiðunargreiningargjöldinu.

Candidate 7: Það er um fjárhæð frá störfum sem gefin var í viðmiðunarárinu.

</details>

<details><summary>final_semantic_review #82 · after · greedy · technical_short · P</summary>

Source ID: p13official21:test:eea:1965

English: After paragraph 97B, paragraph 97C is added.

Reference (shown after audit): Lið 97C er bætt við á eftir lið 97B.

Review: 97C added after97B retained exactly.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Eftir 97B-lið bætist við 97C-lið.

</details>

<details><summary>final_semantic_review #83 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:1190

English: In these cases it is therefore recommended that the Zonegran total dose should be rounded up or down to the nearest available dose that can be achieved with commercially available capsule strengths of Zonegran (25 mg, 50 mg and 100 mg).

Reference (shown after audit): Í slíkum tilfellum er því mælt með því að heildarskammturinn af Zonegran sé minnkaður eða stækkaður í næsta skammt sem hægt er að gefa með hylkjum af þeim styrkleika af Zonegran sem fáanleg eru (25 mg, 50 mg og 100 mg).

Review: All omit/corrupt rounding or commercially available capsule-strength constraint; candidate6 lacks capsule form and reliable rounding verb.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þess vegna er ráðlagt að hefðun tölfrámið Zonegran skuli jafnað við næsta fáarlega skammta, sem er fáanleg og má ná með hjá pöptugalistu tæki við hagrar styrk við Zonegran (25 mg, 50 mg og 100 mg).

Candidate 1: Því er ráðlagt að þegar um er að ræða þá skal umbláðin fylgja fram eða niðri einungis að næsta, færa fali sem er farið að með skjalfestum hárðgjafum af frumum í sér við færi með afhendulegum kúpum með fali (25 mg, 50 mg og 100 mg) af Zonegran.

Candidate 2: Því er ráðlagt þess að skugga málið sem varðar allt skammtur af Zonegran í upprunnalagi einstökum skammtum sem fáanlegu er og sem geta loksæið við lyfjun með gagnvart 25 mg, 50 mg og 100 mg.

Candidate 3: Í þessum tilfellum er því ráðlagð að hefja eða loka skammtinn af Zonegran til næsta uppfært skammt sem er farið að með hygda gegn með 25 mg, 50 mg og 100 mg skammt sem eru fáanlegar í lyfinu við Zonegran.

Candidate 4: Í slíkum tilfellum er þess vegna ráðlögð að þess að lausn var sú upphæð af Zonegran sem er háttum húðað eða minni til næsta uppgjör sem gert er komið með meðgönguðum lyfiþætti Zonegran (25 mg, 50 mg og 100 mg).

Candidate 5: Því er mælt með að umfang alls skammta Zonegran skildist að því er varðar næstum viðbótarskammta sem getur verið við sér þegar fjölbrautastærðir Zonegran (25 mg, 50 mg og 100 mg) eru fyrir fangi.

Candidate 6: Í samanburði með þetta er þó þörf á að haldi reikningsskammtinn af Zonegran upp eða niður að næsta fáanlegri skammti sem er búin til að ná með lyfjagreinanlegum skammtum af Zonegran (25 mg, 50 mg og 100 mg).

Candidate 7: Því er ráðlagt að um rúminu eða uppflutningu samsvarandi haldslitum í Zonegran skulu þolast þegar um er að ræða þetta tilvik. Þegar um er að ræða sér stöðu skal þolast þegar um er að ræða þetta tilvik. Þegar um er að ræða stöðu skal þolast þegar um er að ræða þetta tilvik og skal þegar um er að ræða stöðu skal þolast þegar um er að ræða þetta tilvik.

</details>

<details><summary>final_semantic_review #84 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:ema:3025

English: Based on individual patient response and tolerability, the dose may be increased to 300 mg (15 ml) per day after an interval of 3 to 7 days, and if needed, to a maximum dose of 600 mg (30 ml) per day after an additional 7-day interval.

Reference (shown after audit): Eftir svörun og þoli hvers sjúklings má auka skammtinn í 300 mg (15 ml) á sólarhring eftir 3-7 daga og ef þörf krefur í hámarksskammt, 600 mg (30 ml) á sólarhring, eftir 7 daga til viðbótar.

Review: Individual response/tolerability, dose increase and maximum-dose constraint omitted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Með hliðsjón af sviði sjúklinga og þess að meðhöndluð sé um 300 mg (15 ml) á dag eftir 3 til 7 daga millibili og ef þörf krefur 600 mg (30 ml) á dag eftir 7 daga millibili.

</details>

<details><summary>final_semantic_review #85 · before · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:1803

English: What are you planning on telling her?

Reference (shown after audit): Hvað ætlarðu að segja henni?

Review: Question about what to tell her preserved.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Hvað ætlarðu að segja henni?

</details>

<details><summary>final_semantic_review #86 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eso:714

English: By studying this effect it is possible to map out the places where gravity is strongest, and hence where the matter, including dark matter, resides.

Reference (shown after audit): Með því að rannsaka áhrifin er hægt að kortleggja hvar þyngdarkrafturinn er mestur og þar af leiðandi hvar efnið, þar á meðal hulduefnið, er.

Review: Gravity mapping and dark-matter terminology corrupted; black material is not a reliable rendering of dark matter.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þegar við rannsaka áhrif þess er hægt að myndast staðnum þar sem gildi gráttíu er stærsta og því þar sem efnið, þ.m.t. svart efnið, er.

</details>

<details><summary>final_semantic_review #87 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:538

English: Previous observations had shown hotter, but much less dense, gas streaming away from NGC 253s star-forming regions, but alone this would have little, if any, impact on the fate of the galaxy and its ability to form future generations of stars.

Reference (shown after audit): Eldri rannsóknir höfðu sýnt að heitara en ekki jafn þétt gas streymdi burt frá stjörnumyndunarsvæðum NGC 253 en að það eitt hefði lítil eða ekki nokkur áhrif á örlög vetrarbrautarinnar og getu hennar til að mynda nýjar kynslóðir stjarna.

Review: Much less dense becomes very dense; changes the gas property.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Fyrri mælingar hafa sýnt að gasið var heitt en mjög þykktur, á umferð frá stjörnumyndunarsvæðum NGC 253, en einnig ekki hafi það miklu áhrif á lífinu stjörnuþyrpingarins og hæfni til að mynda fjölda nýja stjarna í framtíðinni.

</details>

<details><summary>final_semantic_review #88 · after · greedy · technical_short · F</summary>

Source ID: p13official21:test:eea:1471

English: Prices including all taxes, levies and VAT.

Reference (shown after audit): Verð með öllum sköttum, álögðum gjöldum og VSK.

Review: Levies become tax tables and VAT is corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Verð þar sem tilgreind er allar skattir, skattatöflur og gildaaukaverði.

</details>

<details><summary>final_semantic_review #89 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:43

English: Where plant protection products containing the active substance are intended to be used in cold climatic conditions, the tests have to be conducted where DT50lab, determined at 10 °C and at a moisture content of the soil related to a pF value of 2 to 2,5 (suction pressure) is greater than 90 days.

Reference (shown after audit): Þegar nota á plöntuvarnarefni, sem innihalda virka efnið, í köldu loftslagi verða prófanirnar að fara fram þar sem DT50lab er meira en 90 dagar, ákvarðað við 10°C og í jarðvegi með rakainnihaldi sem miðast við pF-gildi 2 til 2,5 (sogþrýstingur).

Review: Every candidate corrupts climate/soil-moisture/pF/suction conditions or the90day inequality.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Ef efnaöryggisvörur með virka efna eru ætlaðar að nota í kæfuríkum skal prófanir framkvæmdar á stað sem ettikursdreifingur í kæfuríkum, á 10 °C og við 2 til 2,5 (súkkaþrýsting) umbrotu af jörðkvæði sem tengist pF-gildi 2 til 2,5 (súkkaþrýsting), er meiri en 90 daga.

Candidate 1: Ef plöntuverndarvörur með virka efni eru að marktaka til notkunar í kaltum landfræðilegum aðstæðum skal prófunin fram á staðnum þar sem DT50lab, sem ákvarðað er á 10 °C og við váðnandi næð endurtrúa er 2 til 2,5 (stengingur) og er meiri en 90 dagar.

Candidate 2: Ef átt er að nota plöntuvarnarefnum, sem innihalda virka efnið, í kaltum sjaldgæfum aðstæðum skal prófunin rækta þegar DT50lab, sem áður hægt er að ákvarða með 10 °C og með þynningarþéttni á jörðu sem tengjast pF-gildið 2-2,5 (nefndur við meðfanga) er meira en 90 daga.

Candidate 3: Ef nær með smitfreyrleifar sem innihalda virka efni í gegnum fyrrveldi með kalt vist sem notuð verður, verður að prófa á því að DT50láb, sem ákvarðað er í 10 °C og í því þreyttu úrsoðu, sem tengist pF-gildi 2–2,5 (skipþrýstingarmask) jafnframt 90 daga.

Candidate 4: Ef áhættuhemliframleiðsöguvarnarefni með virkum efnum eru ætlaðir að nota í kaltum landshafsgildum skal greina við úr rannsókninni þess og þegar DT50lab, sem telst við 10 °C og með eðlilega hreinsun á jörðun, er 2–2,5 (sykrunamörk) áhrif (súkkulustenging), er hámarkssýnið meiri en 90 dagar.

Candidate 5: Ef áætlanir vegna plöntunarkerfis, sem innihalda virka efni, ætla að vera notaðir í kaltum landamæli stöðu skal prófunin mæla að DT50lab, sem ákvarðað er við 10 °C og við 2–2,5 (súkkaþrýsting) pF veldi vél undir 90 dagi.

Candidate 6: Meðan kemur að því að nota plöntuvarnarefni sem innihalda virku efni í kaltum hættulegum aðstæðum skal greina með því að nota prófunir þar sem DT50lab, ákvarðin í 10°C og með 2-2,5 (sáðaður stöðluður spenni) veldi á ræktum yfirráðasviði, hefur verði meira en 90 dagar.

Candidate 7: Ef lyf, sem innihalda virku efni og eru ætlaðir að nota í kasa aðstæðu, á að gera prófanir á því að virktímot tíðni, sem er ákveðin í 10 °C og með því að þyngdarstigi yfirhúsa, sem er tengd pF-gildi 2 til 2,5 (stökkþrýsturfjölda) sé stærri en 90 daga.

</details>

<details><summary>final_semantic_review #90 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:ema:2690

English: Adverse effects not observed in clinical studies but seen in the rat and to a lesser extent in the mouse at exposure levels similar to human exposure levels and with possible relevance for clinical use were liver changes, indicating an adaptive response such as increased weight and centrilobular hypertrophy, fatty infiltration and increased liver enzymes in plasma.

Reference (shown after audit): Aukaverkanir, sem komu ekki fram í klínískum rannsóknum, en sáust hjá rottum og hjá músum þó í minna mæli, við skammta sem eru svipaðir meðferðarskömmtum hjá mönnum og skipta hugsanlega máli við klíníska notkun, voru lifrarbreytingar sem gefa til kynna aðlögunarsvörun eins og aukna þyngd og stækkun í miðju lifrarblaða, fituíferð og aukningu á lifrarensímum í plasma.

Review: Centrilobular hypertrophy becomes pressure and fatty infiltration becomes fat reduction; plasma also generalized to blood.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Aukaverkanir sem ekki sást í klínískum rannsóknum en sáust hjá rottum og mjög minni marki hjá músum við útsetningu sem jafngildir útsetningu fyrir menn og geta haft áhrif á klínískan notkun voru breytingar á lifur sem benda til þess að það sé að því er varðar aðlagaða svörun eins og aukin þyngd og þrýsting í miðlókum, fituskerðingu og aukin lifrarensím í blóði.

</details>

<details><summary>final_semantic_review #91 · after · greedy · technical_short · F</summary>

Source ID: p13official21:test:eea:1503

English: If this kind of costs exists, they will be reported separately.

Reference (shown after audit): Ef þess háttar kostnaður er fyrir hendi skal tilgreina hann sérstaklega.

Review: Separately reported becomes reporting under special conditions.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef slík kosti eru til koma þeir til skýrslu í sérstökum skilyrðum.

</details>

<details><summary>final_semantic_review #92 · after · greedy · technical_short · F</summary>

Source ID: p13official21:test:eea:1855

English: The product must be easily recyclable.

Reference (shown after audit): Það verður að vera auðvelt að endurvinna vöruna.

Review: Product changes to medicine and recyclable to renewable/renewable action.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Lyfið verður að vera auðvelt að endurnýja.

</details>

<details><summary>final_semantic_review #93 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:ema:1152

English: Change from baseline in body weight was similar for patients treated with sitagliptin relative to placebo.

Reference (shown after audit): Breytingar á þyngd frá grunnlínu voru svipaðar fyrir sjúklinga sem meðhöndlaðir voru með sitagliptíni miðað við þá sem fengu lyfleysu.

Review: Body-weight change is replaced by weight dose.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þyngdarskammtur frá upphafsgildi var svipað fyrir sjúklinga sem fengu sitagliptín samanborið við lyfleysu.

</details>

<details><summary>final_semantic_review #94 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:409

English: Purpose: to determine whether the test facility, if engaged in studies using animals or other biological test systems, has support facilities and conditions for their care, housing and containment, adequate to prevent stress and other problems which could affect the test system and hence the quality of data.

Reference (shown after audit): Markmið: að ákvarða hvort prófunarstöðin, ef þar eru stundaðar rannsóknir með dýr eða önnur líffræðileg prófunarkerfi, hefur yfir að ráða búnaði og aðstöðu þar sem hægt er að hirða um þau, koma þeim fyrir og einangra þau á annan viðeigandi hátt þannig að koma megi í veg fyrir streitu og önnur vandamál sem gætu haft áhrif á prófunarkerfið og þar af leiðandi á gæði gagnanna.

Review: Animal care/housing/containment omitted and stress becomes development.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Tilgangur: til að ákvarða hvort prófunarstöð varði stofnun og skilyrði til að hafa áhættuvernd fyrir dýrum eða öðrum líffræðilegum prófunarkerfum, svo að það geti komið í veg fyrir þróun og annað vandamál sem geta haft áhrif á prófunarkerfinu og þannig gagnasmiði.

</details>

<details><summary>final_semantic_review #95 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:908

English: This bridge, which has not been seen before (and is too faint to show up in this picture), is somewhat bluer than either galaxy, indicating that it consists of stars created in gas that was drawn away from NGC 1387 by the gravitational pull of NGC 1399.

Reference (shown after audit): Þessi brú hafði ekki sést áður (og er of dauf til að koma fram á myndinni) en hún er nokkuð blárri en hin vetrarbrautin sem bendir til þess að hún samanstandi af stjörnum sem mynduðust úr gasi sem NGC 1399 hrifsaði úr NGC 1387.

Review: Too faint becomes light-giving; galaxy/gravity terms also corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þessi brú, sem hefur ekki séð áður (og er of ljósgæf til að sýna í myndinni) er einhverskju blárri en annar galdrar, sem benda til þess að hún er úr stjörnum sem eru myndar úr gasi sem var dragað út frá NGC 1387 af gildislagi NGC 1399.

</details>

<details><summary>final_semantic_review #96 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:386

English: Purpose: to inform the management and staff of the facility of the reason for the test facility inspection or study audit that is about to take place, and to identify the facility areas, study(ies) selected for audit, documents and personnel likely to be involved.

Reference (shown after audit): Markmið: að tilkynna stjórn og starfsliði prófunarstöðvarinnar um ástæðuna fyrir því að skoða á prófunarstöðina eða gera úttekt á rannsóknum og nefna þá hluta prófunarstöðvarinnar, rannsókn(ir), skjöl og starfsmenn sem líklegt er að komi við sögu við skoðunina eða úttektina.

Review: All corrupt reason for forthcoming inspection/audit and the selected facility areas/studies/personnel relation.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Framlengi: til að bæta stjórnvöld og starfsmenn á störfum frá því að það er að gera úttekt á annarrar störf og að tekja fram á byggingu störfar og tilteknum starfsmenn og skjöl sem líka eru líklega tækivélar til að taka tillit til.

Candidate 1: Markmiðið: til að upplýsa rekstraraðila og starfsmenn á störfum eftir sannprófun á prófunastofnunni eða notkunareftirlitið sem komi að gengi og til að koma fram það hvar aðstöðuð er, þau rannsóknir sem valin eru við notkunareftirliti, skjöl og starfræðingar sem líklega verða þegar að tekur á.

Candidate 2: Tilgangur: til að tilkynna stjórnvöld og starfsmenn á viðkomandi aðila varðandi ákvarðanir varðandi eftirlit með prófunarfélagsið eða prófunarviðurkenningu og til að greina íhugað staðir viðkomandi aðila, viðkomandi prófunum, skjöl og starfsmenn sem líklega eru í tengslum við prófunarviðurkenninguna.

Candidate 3: Skáldsögn: til að upplýsa stjórnun og starfsfólki um kerfisvaranir við eftirlitsins á prófunarstofu eða prófunarætlunar eða tilkynningar sem þær gerir og til að greina yfir hennar stofunarkvæði, smásvæði, tilkynntir prófanir sem verða að gera prófunarætlunar, skjöl og starfsmenn sem líkur eru.

Candidate 4: Tilgang: til að upplýsa stjórnviður og starfsmenn viðskiptastæðisins um rökprófunarstofnunar eða rökprófunarstofnungarkerfið sem verður að greiða og til að koma í ljós yfir stöðvegur, röku sem taldir eru í rökprófunarhagskerfið, skjöl og starfsmenn sem líklegt er að taka þátt í því.

Candidate 5: Viðmiðun: til að upplýsa stjórnvöld og starfsfólki viðskiptastöðva um ástæðu þess að prófsýni á viðskiptastöðvinu eða rannsóknarfjármönun og til að því er varðar, og til að tekja fram áhrif af stöðvunarmiðum, rannsóknir, skjölum og starfsfólki sem líklegt er til að hafa áhættugrun.

Candidate 6: Tilgang: til að upplýsa stjórnun og starfsfólki viðskiptastæðisins um skoðun eða rannsóknastjórnunar, sem nær stað, og til að koma fram áraðagangum viðskiptastæðisins, ásamt viðskiptavísindunum, sem ákvarðaður hefur verið, upplýsingum og starfsfólki sem líklegt er að sé að taka þátt í rannsóknastjórnun.

Candidate 7: Ráðstafanir: til að upplýsa stjórnandi og starfsfólk á sviði staðnarstarfsemi og að tekja grein í þessarar yfirráðasvæði, prófum, gagnvart fariði að því að meta fyrir eftir, og tiltekið fyrirkomulag, próf og starfsmenn sem líklega geta stundað.

</details>

<details><summary>final_semantic_review #97 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:136

English: Member State shall recognize the documents of compliance and safety management certificates issued by, or on behalf of, the administrations of third countries if it is satisfied that they demonstrate compliance with the provisions of this Regulation.

Reference (shown after audit): Aðildarríki skal viðurkenna þau samræmingarskjöl og öryggisstjórnunarskírteini sem stjórnvöld í þriðju löndum, eða annar fyrir þeirra hönd, hefur gefið út ef það er sannfært um að með þeim sé farið að ákvæðum þessarar reglugerðar.

Review: Compliance documents/safety-management certificates and issuance/recognition relations are not retained.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Aðildarríki skulu viðurkenningu fyrir samræmi og öryggisstjórnun í þriðju löndum, sem eru gefin út eða hafa verið gefin út fyrir stjórnvöld þriðju löndanna, þegar þau sýna fram á að þau uppfylli ákvæði þessarar reglugerðar.

</details>

<details><summary>final_semantic_review #98 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:437

English: Lenvatinib should not be started in patients with fistula to avoid worsening and lenvatinib should be permanently discontinued in patients with oesophageal or tracheobronchial tract involvement and any Grade 4 fistula (see section 4.2); limited information is available on the use of dose interruption or reduction in management of other events, but worsening was observed in some cases and caution should be taken.

Reference (shown after audit): Ekki skal hefja meðferð með lenvatinibi hjá sjúklingum með fistil til að forðast versnun og hætta skal meðferð með lenvatinibi til frambúðar hjá sjúklingum þar sem vélinda eða barki og berkjur eiga í hlut og í tilfellum allra 4. stigs fistla (sjá kafla 4.2), takmarkaðar upplýsingar liggja fyrir um skammtahlé eða skammtaminnkun við meðferð á öðrum atvikum, en versnun varð í sumum tilvikum og því skal gæta varúðar.

Review: All corrupt fistula sites/grades and starting/permanent-discontinuation instructions; some reverse stop/start.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Ekki skal stöðva lenvatinib á upphaf við sjúklinga með þá þrýstingu til að koma í veg fyrir orðun og lenvatinib skal ótrúað í mótefni við sjúklinga með tæknileg áhætta í fæðra eða víðhjálmafyrirleitinni og allar 4. grad íhækkun (sjá kafla 4.2); aðgerðir með því að hætta eða minnka skammti eru algjörulagið í nota við öðrum aukaverkanum en nýtt í tillit til að hætta aukaverkuna. Nútæki var stærðfræðilega til þess að miklu máli var í treyst á aukaverkunum en aðgerðir með því að hætta eða minnka skammti voru þráðir í tilvísunum.

Candidate 1: Lenvatinib má ekki ábyrga við notkun hjá sjúklingum með fræðs. Til að koma í veg fyrir hækkun skal hætta að notkun lenvatinbis og hún skal hætta að því í beinni lagi hjá sjúklingum með áhættu á greiningum á öskju eða að lækka þrýstingum frá tráhjóði og í öðru hluta eða varðandi fræði (sjá kafla 4.2). Að því er varðar annarra ákvæði hefur ekki verið fyrir ráðstafanir um notkun talið í tímabili sem stöðvar eru hækkunin er hægt að hætta og við hættu skal koma í veg.

Candidate 2: Nýtja skal notkun lenvatíníbs ekki hjá sjúklingum með orðmörk til þess að koma í veg fyrir aukun og hann skal áframblandt meðan sjúkling hjá ónæmi á hrygg eða í þjófhylfinu og annað hvort í 4. gradu (sjá kafla 4.2); aðgerðir með beitingu styrks eða styrkun áhættuhæfis hafa ekki notaðarum, en aukun var sýnt fram fyrir til að rangarannsóknar var gert og skal varúðar verða.

Candidate 3: Eftirlit með lyfjunum með lenvatiníb á því að leiðast misvirki og lyfjameðhöndlun áfram í þeim tilfellum sem eru með vaxingu í og eða hreinsluverð í öðrum tilfellum og þeim tilfellum sem eru með vaxingu í öðrum vaxingunum meira en 4. stigs (sjá kafla 4.2). Velkomið upplýsingar um notkun á tímabundnum hætta á skammta eða minnkingrið í notkun á annarra aukaverkanum eru fyrir hendi en mikill virkni var sýnt í nokkrum tilvikum og á beitingu var að gera varðandi áhættu.

Candidate 4: Læraðaður skal ekki lenvatinib viðkomandi hjá sjúklingum með lausi til að koma í veg fyrir það að lausinn skammtir verði lítillega. Læraðaður skal niðurstöðugt stöðva lenvatinib við sjúklinga með lífeyriskrá eða krökur í tráhálf í íhluta og einhverjar 4. gradu lausna (sjá kafla 4.2); auki getur varandi upplýsingar verið um notkun á lokbraka undanþáða skammta eða minnkaðri skammta við aðstoðarferli annarra ástanda en að hafa verið þýdd að bætt væri í nokkrum tilviki.

Candidate 5: Hvaðandi er varðar að koma fyrir upptök eftir hætta skal ekki með lenvatinib hjá sjúklingum með hættulegri blöndu til að koma fyrir upptök og lenvatinib skal hætta meðan á sviði á meðferð stendur hjá sjúklingum með þrýsting í geymissvæðum eða þýssvæðum og í öllum Fall 4 hættulegri blöndu (sjá kafla 4.2). Notkun á að því er varðar magnarskörtingu eða lækkaður magn í meðferð með öðrum ákvæðum en að því er varðar að störfið hafi í stað gengið og skal beita varúð.

Candidate 6: Lenvatinib skal ekki byrja á hjá sjúklingum með stungustöfun til að koma í veg fyrir vanda af og ber að loka lenvatinib á lengi búnaði hjá sjúklingum með þróun í sykla eða stungustaði og öðrum síkkingum, og hverju stungustöfun (sjá kafla 4.2) með atriða 4; tilgreind er einungis hvort úrgang og minnkingur á skammtum hafa verið notuð að ræða annað ástand og hafa verið þó sýnt breytingar í tilteknum tilvikum, en varða skal við áherslu.

Candidate 7: Læt ekki fara á með útsetingu af lenvatinibi við sjúklingar með flýta til að koma í veg fyrir þess að lífrýminn þreyti og skal hægt að hætta gildisskammtinni lenvatinib á tíma, ef sjúklingur með váhrifum á gólfinu eða hvíslu og hvíslabroður, innihaldi og ekki meira en 4. grad; fyrir hönd skulu fá nauðsynleg atriði um notkun barnaútkomunar eða þróunar í óhæðum áhættuvirkjum en það var prófun, en þrátt var í nokkrum tilvikum og vart skal varúð.

</details>

<details><summary>final_semantic_review #99 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:1059

English: The domestic output price index for an economic activity measures the average price development of all goods and related services resulting from that activity and sold on the domestic market.

Reference (shown after audit): Vísitala innlends framleiðsluverðs vegna atvinnustarfsemi mælir meðalverðþróun á öllum vörum og tengdri þjónustu vegna þeirrar starfsemi sem eru seldar á innanlandsmarkaði.

Review: All corrupt domestic output-price index and average price-development concept, despite fragments about goods/services.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Innlíknið verðsins fyrir innlán er víðvart verðsáætlun á öllum verkum og tengslum þjónustu sem beitað er af þessari starfsemi og verði seljandi á innri markaðinum.

Candidate 1: Ístandarlegur verðsáætlun í innri ríki fyrir starfsemi mælt er frammi verðaðar allra verkja og tengda þjónustu sem útgefur þessi starfi og sem verðað eru á innri markaðinu.

Candidate 2: Hogt verðuður fyrirsættur fyrir innlendur rekstrarhæfni fyrir rekstrarhlutvinnslu mælt er að því hversu mikil verði allir vörur og tengda þjónustur, sem frá þessu rekstrarhæfi komu í ljós og var seldar á innlendum markaðum, og mælt er að hún sé hins meðaltals og hún er skiptið við rekstrarhæfni.

Candidate 3: Þjóðverðlega verðþáða þegar vinnuferliðar eru að því er virði allra vörur og tengda þjónustu sem eru mynduð af vinnuna og söluð á innlandsmarkaðinum.

Candidate 4: Hagseldustyrkakostnaður til heimili til rekstrarvirkra starfsemi mætir meðalverandi verðaðli alla vöru og tengdar þjónustu sem er afkostn hennar starfsemi og skiptir á raunhrifum aðilinni.

Candidate 5: Inndælslaprófanum fyrir efnahagsgerð með innri hætti metir tíðni meðalverðar allra vörur og tengda þjónustu sem afkastar af þessari starfsemi og hefur verið selt á innri markaðinum.

Candidate 6: Ætlanir innleiðinnar verðaðar í innlendu bandastöðu tölvanir til að meta meðalverðu verðaðar af öllum vörum og tengdum þjónustum sem farið er fram af þeim starfsemi og sem er seljandi á innlendu markaðinu.

Candidate 7: Hagspeðleiðslutöfluninn sem mælt er með innra verkunum mælt er fram ásamt því hverju tæki og þær starfsmæli sem tengjast þess viðskipta hefur verið af þeirri hag og verður upp á innlandsmarkaðinu.

</details>

<details><summary>final_semantic_review #100 · before · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:3484

English: If you do not give me the house you promised I shall be forced to return to England.

Reference (shown after audit): Ef þú lætur mig ekki fá húsið eins og þú lofaðir neyðist ég til að fara aftur til Englands.

Review: The condition loses NOT, reversing the house-giving premise.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef þú gefur mér húsið sem þú lofaðir mér að fá verð ég forvart til Englands.

</details>

<details><summary>final_semantic_review #101 · after · G8 · technical_short · F</summary>

Source ID: p13official21:test:eea:1471

English: Prices including all taxes, levies and VAT.

Reference (shown after audit): Verð með öllum sköttum, álögðum gjöldum og VSK.

Review: No candidate preserves the full taxes/levies/VAT list; closest6 substitutes obligations and non-VAT value tax.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Verð, þar með talið alla styrk, skatt og gilda skattatiltekni.

Candidate 1: Verð sem takmörkuð er allarum skattum og skattaraðskrafa, skuldum og markaðsskatta.

Candidate 2: Verðið skal inntaka allar skálds og skattatöflur.

Candidate 3: Verð þar sem tilgreind eru allar skálds eftir tilskildir og gilda skattaárekströr.

Candidate 4: Verðin með inntöku öllum skáls, skrifstofum og auðskilnaðarsskattinum.

Candidate 5: Verð þar sem tilgreindir eru allar skattir og skattrík og markaðsskipulag.

Candidate 6: Verð þar sem fela upp allar skatta, skuldbindingar og gildisskatt.

Candidate 7: Verð þar sem tilgreind eru allar skattir, tilbótir og töldeysakerfi.

</details>

<details><summary>final_semantic_review #102 · before · greedy · technical_medium · U</summary>

Source ID: p13official21:test:ema:772

English: These effects are called interactions, and can lead to serious side effects, or prevent proper control of other conditions you may have.

Reference (shown after audit): Þessi áhrif eru kölluð milliverkanir og geta valdið alvarlegum aukaverkunum, eða komið í veg fyrir viðeigandi meðferð annarra sjúkdóma hjá þér.

Review: Most interaction/adverse-effect meaning recognizable, but concurrent-effects terminology and proper-control wording are uncertain.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þessi áhrif eru kallarðar samhliðaáhrif og geta leitt til alvarlegra aukaverkana eða hindrað hæfi meðferð á öðrum aðstæðum sem þú getur verið að hafa.

</details>

<details><summary>final_semantic_review #103 · before · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:1317

English: General Barnicke's gone until tomorrow morning.

Reference (shown after audit): Barnicke kemur ekki fyrr en í fyrramálið.

Review: Until tomorrow morning becomes until this morning; military title also absent.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Barnicki hefur farið til í morgun.

</details>

<details><summary>final_semantic_review #104 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:2120

English: In order to facilitate data flows from the European Union, it is desirable for processors providing data-processing services to several data controllers in the European Union to be allowed to apply the same technical and organisational security measures irrespective of the Member State from which the data transfer originates, in particular in those cases where the data importer receives data for further processing from different establishments of the data exporter in the European Union, in which case the law of the designated Member State of establishment should apply.

Reference (shown after audit): Til að auðvelda gagnaflæði frá Evrópusambandinu er æskilegt að vinnsluaðilar, sem veita mörgum ábyrgðaraðilum gagna í Evrópusambandinu gagnavinnsluþjónustu, fái leyfi til að beita sömu tæknilegu og skipulagslegu öryggisráðstöfunum, óháð því frá hvaða aðildarríki gögnin eru flutt, einkum í þeim tilvikum þar sem gagnainnflytjandinn tekur við gögnum til frekari vinnslu frá mismunandi starfsstöðvum útflutningsaðila í Evrópusambandinu, en þá gilda lög þess aðildarríkis þar sem starfsstöðin er staðsett.

Review: All corrupt data processor/controller/exporter/importer roles or establishment-law/security conditions.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Til að auðvelda gagnafélög frá Evrópusambandið ætti að þeim giguð er varðandi gögnum sem geymi gagna, sem geytir til annarra gagnaframleiðendum í Evrópusambandinu, heimilað að gera sama tæknilega og stjórnsýsluefni öryggisstanda án þess hátt með aðildarríkisins sem gagnabréf stofnaður samkvæmt, einkum þegar gagnabreiddarkerfantin får gagna sem geytir til annarra rekstraraðila af gagnabreiðandi í Evrópusambandinu til frekari framleiðslu, þá skal lög staðfestu aðildarríkisins til staðar.

Candidate 1: Til þess að auðvelda gagnamæli milli Evrópusambandsins skal því ráðlega gert heimilt gagnaendur sem tilbyggja gagnaþjónustu fyrir fleiri gagnaþjónustuvarnir í Evrópusambandinu að nota þeirra sömu tæknilegar og stjórnsýslustöku varnarkerfiss án þess hvaða aðildarríki gagnaðstillanum kemur frá, einkum þegar gagnaðstillanin fær gagna frá öðrum starfsmælum útsettingarinnar í Evrópusambandinu og þær eru til að endurskoða, þá skal löggjöf í tilnefnt aðildarríki mesta stöðu synja við.

Candidate 2: Til að auðleika gagnagjafarnar og gagnafrumnum í Evrópusambandinu ætti viðurkennd að sameiginlega tækni og stjórnsýsluefni var skuli beitt öll tækni og stjórnsýsluefni í sama stigi, án þess að farið sé fyrir framkomulagi aðildarríkis, einkum þegar gagnaðkutamuraður fær gagna sem eiga við um að fara í nýju gagnafrumni úr annarri störfstað gagnaframsækjandans í Evrópusambandinu, þar sem ákvarðaði aðildarríkið gerist rétt á að gagnaþátturinn í því aðildarríki sé þjáð.

Candidate 3: Til að auðsökja gagnsýslur milli Evrópusambandsins getur verið ráðandi að því að reiknaðarverkur, sem veita gagnaþýðingu við þjónustu með gagnaþýðingu til nokkrar gagnaöryggishandlager í Evrópusambandinu, sé sýkt heimild til að nota samanlegri tæknilegar og stjórnsýslufyrirkomulagsgæði í þeim tilvikum, hvort það sé úr þeirri aðildarríki sem gagnaþýðingurinn hefur fengið gagna fyrir nýju gagnaþýðingu frá drepum stofnum af gagnaþýðingu í Evrópusambandinu, eigi hvers konar aðildarríki, einkum þegar innflytjanir hafa fengið gagna frá drögum stofnu af gagnaþýðingu í Evrópusambandinu til að aðlaga þeim, þar sem lög tilnefndrar aðili að stofnun hennar skuli gilda.

Candidate 4: Til að auðvelda gagnaflokk í Evrópusambandinu er það hæfilegt að reynsluþjónustuverum, sem veita gagnagjafarþjónustu fyrir margir gagnafangamannir í Evrópusambandinu, sé heimilt að nota samsvarandi tækni og stjórnsýsluefnið vernda á öðrum stöðum, hvort sem um er að ræða Evrópusambandsstaðla, einkum þegar gagnaafhendingið fær gagna og er að gagnaafursturinn telur þau til næstu gagnafrumur, sem gagnaafursturinn í Evrópusambandinu á, þá skal laugir í tilnefnt stöðum til að finna á.

Candidate 5: Til þess að auðvelda gagnabréf frá Evrópu að tryggja að tryggingar hafa verið fengin og hægt sé að gera framkvæmdastarfsemi aðila, sem veita gagnakerfi fyrir nokkrum gagnastjórnenda í Evrópu, að beita sömu tækni og stjórnunarskyggðum ráðstafanum, án þess að það skipti sig fyrir því hvort ákvarðað er að koma frá evrópskri aðildarríki og, einkum því til að gagnafrumur skuli fá gagna frá annarra starfsstöðvum æða gagnaflutningsaðilanna í Evrópu, þar sem skal gilda lög fyrir tilnefndri aðildarríki fyrirtækis.

Candidate 6: Til að auðvelda gagnalentröndur milli Evrópusambandsins ætti því tilægt að aðlaga krafanir fyrir framleiðendum sem veita gagnaþjónustu fyrir fleiri gagnaábyggjandur í Evrópusambandið um sameiginlega öryggisstöfun og samstæðustöfun, án þess háva að þessi stöfun sé frá hverju Evrópusambandsins, einkum þegar gagnaþörfjárhæður fær og fjarlæga gögnum gagna fyrir foreldreiningu frá aðskilinni starfsstöðum gagnaþjónustuðs í Evrópusambandið, þar sem gæði staðfestu evrópskra landsbundna stóðu skal tiltekin framleiðsluðstaðaðildarríkið koma í gildi.

Candidate 7: Til þess að auðlindast gert sé inntökur úr Evrópsu, er þá þætt að leiðbeiningar fyrir viðkomandi gagnafrumur, sem veita gagnafrumudæmi fyrir nokkrum gagnaendursökum í Evrópusambandinu, sé heimilt að beita sama tækni og stjórnsýsluefnið öryggismáknaða án þess að það skipti sig frá því hvaða aðildarríki gerningurinn er komin frá, einkum þegar gagnaðfæddur fær gagna úr viðkomandi gagnaðfjármörkum af gagnaðgangandi í Evrópusambandinu, þar eiga þá lög gildandi í tilnefndri aðildarríkinu.

</details>

<details><summary>final_semantic_review #105 · before · greedy · technical_short · P</summary>

Source ID: p13official21:test:eea:1503

English: If this kind of costs exists, they will be reported separately.

Reference (shown after audit): Ef þess háttar kostnaður er fyrir hendi skal tilgreina hann sérstaklega.

Review: Conditional existence of costs and separate reporting retained despite inflection.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Ef slík kostnað er til stöður verða þær greint í sér.

</details>

<details><summary>final_semantic_review #106 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:1831

English: However fibreboards classified as class A will be accepted if they do not represent more than 50 % of the total wood and wood-based materials used in the product.

Reference (shown after audit): Trefjaplötur sem flokkaðar eru sem E1 munu þó samþykktar ef þær eru ekki meira en 50% af samanlögðu innihaldi viðar og efna úr viði sem notuð eru í vöruna.

Review: Fibreboard and wood-based materials become unrelated fibres/cells.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þó má taka við fíbraröð sem eru skráð í flokki A ef þeir eru ekki meira en 50% af heildarfrumur og frumur sem eru búin úr frumum í vörunni.

</details>

<details><summary>final_semantic_review #107 · after · greedy · technical_medium · P</summary>

Source ID: p13official21:test:ema:1152

English: Change from baseline in body weight was similar for patients treated with sitagliptin relative to placebo.

Reference (shown after audit): Breytingar á þyngd frá grunnlínu voru svipaðar fyrir sjúklinga sem meðhöndlaðir voru með sitagliptíni miðað við þá sem fengu lyfleysu.

Review: Body-weight change from baseline similar for sitagliptin versus placebo retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Breyting frá grunngildi á líkamsþyngd var svipuð hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.

</details>

<details><summary>final_semantic_review #108 · after · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:1059

English: The domestic output price index for an economic activity measures the average price development of all goods and related services resulting from that activity and sold on the domestic market.

Reference (shown after audit): Vísitala innlends framleiðsluverðs vegna atvinnustarfsemi mælir meðalverðþróun á öllum vörum og tengdri þjónustu vegna þeirrar starfsemi sem eru seldar á innanlandsmarkaði.

Review: No intelligible domestic output-price index measuring average price development; multiple scope/quantity relations corrupted.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Innri verðsinsleifur fyrir efnahagsaðstöðu mæla með sér miðgildi verðsverkis allra vörum og tengda þjónustu sem kemur fram af ákvörðun sjálfri þess og seljast á innlanum markaði.

Candidate 1: Í innlendri veruverðskrá fyrir efnahagsaðgerð er mælt fyrir um miðgildi verufram- vikranna allra vörva og tilheyrandi þjónustu sem komist er fram af þessari starfsemi og er selgt á innlands- markaðinum.

Candidate 2: Staðbundinn merkmið um útgjöld fyrir efnahagsaðgerð mælið verði arsmerki á vísitölu hinra vörus og tengda þjónustu sem er afkvæmat fyrir það aðgerð og selis á innlöginu.

Candidate 3: Þjóðlega verðþýðisstykkin fyrir vinnu- hag, að því er varðar kostnaðarbúning, miðar tíðni á meðaltali verðs fyrir öll vörur og tilheyrandi búningi, sem leiðir af þessari hag og seldur á innlandsmarkaðinu.

Candidate 4: Haglegur vísitilraun um útbreiðslu verð við efnahagsaðgerð metir með hlutföllu ástaþroska af öllu efninu og tengdum þjónustum sem það fer fram og selstu á innlendu markaðinum.

Candidate 5: Innri verðaðiðaþáttur fyrir efnahagsaðstoður miðir það þá verðbreytingu samkvæmt þeirri aðstæðum sem hafa í sér eða tengjast þeirri sjálfri aðstöðu og selskoðaðir á innri markaðinum.

Candidate 6: Ættarverðleið seði fyrir innri verð (domestic output price index) fyrir rekstrarhóf tilkynnt er með því að meta meðalverðaráhrif gögnum og þeirra þjónustu sem þeir eru fyrir framleiðslu og seljast á innlandsmarkaðinu af komið út úr þeirri rekstrarhófi.

Candidate 7: Hagverðin fyrir innri útgjöf efnahagsaðstæðu eru miðað um meðal verðskipti allra vörna og tengda þjónustu úr sér sér í þessari aðstæði og seljandi á innri markaðinum.

</details>

<details><summary>final_semantic_review #109 · before · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:1121

English: Of course you're right, Starling... but it doesn't change anything.

Reference (shown after audit): Auðvitað er það rétt, Starling... en það breytir engu.

Review: You are right and nothing changes retained; discourse marker omitted only.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Þú ert rétt, Starling, en það breytir ekkert.

</details>

<details><summary>final_semantic_review #110 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:2090

English: Member States shall require the competent authorities to monitor compliance with this Regulation effectively and take all necessary measures to ensure such compliance.

Reference (shown after audit): Aðildarríki skulu skylda lögbær yfirvöld til að hafa eftirlit með því að farið sé með virkum hætti eftir þessari reglugerð og gera allar nauðsynlegar ráðstafanir til að tryggja að farið sé að ákvæðum hennar.

Review: Effective compliance monitoring and who must take measures are corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Aðildarríkin skulu krefjast lögbæru yfirvölda um að eftirlit með því sé framkvæmd á þessari reglugerði sé ráðstafanleg og að þeim gerist allar nauðsynlegar ráðstafanir til að tryggja það.

</details>

<details><summary>final_semantic_review #111 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:80

English: But the new study using the VLT has found that much of the stars energy is being absorbed and scattered by dust clouds before it gets to Earth - it is actually more luminous than previously thought and among the brightest stars known.

Reference (shown after audit): Nýja rannsóknin með VLT hefur hins vegar sýnt fram á að rykský gleypa og dreifa stórum hluta orkunnar sem stjarnan gefur frá sér áður en hún berst til jarðar - hún er því í raun miklu bjartari en áður var talið og er meðal skærustu stjarna sem vitað er um.

Review: All corrupt stellar energy absorption/scattering by dust and luminosity inference.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Nýr rannsókn með þessari mikilvægtar skynstu gönguna hefur fundið að meira en það af fyrirbarði stjarnafræðis er svo undanfært og úranslengtur til að mikilvægt stjarnanum íði til Jörð og svo er það hvarflega ljúmennari en áður telst og er meðal bláusta stjarna sem vitað er.

Candidate 1: Nýr rannsókn sem notaði hreyfingarstjórnunarkassins fái að mjög er af ljós kertið rafþjóða sem myndar innyum og sprengir hann áður en hann krefur að Eðrun. Það er virkilega ljólamæri háman eða ljósa en áður heyrðist og sumur af hinnum blára stjörnunum.

Candidate 2: Nýttan rannsókn með VLT færði það að mikið af verksmyndismyndis er gefið út og flókt af svæðið áður en það kemur til jörðu - það er virkilega ljóðari en áður hefði verið þolst og það er í sér meist ljóðilegir stjarnur sem þekktir eru.

Candidate 3: Nýr rannsókn með VLT hafði fundið að mikill af glósakrafti hafa verið nefnd inn í myndandi svæði og því að hægðu áður en hún komin leitið á jörð - það er svona leeri og víðmæri en það var þó öðrum tímanum og með því hvetstirri lögum sem það var þurftlega til að leita.

Candidate 4: En nýi rannsókn með VLT hefur fundið að myndavaxið elskaði upp og beinu af stjarnanum fyrir því að þær ná yfir á Jörð - það er í raun meiri ursauti en það var í talið og þjálfast mikið er þar til.

Candidate 5: Nýr rannsókn með því að nota VLT hefur fundið að það væri mikið af ljósmyndanum stjárnar sem samgjaldast og skarrið við dýrarkrænurnar áður en þeir komi á Þjóð eftir það er frá þessu hækkur. Gefur það bara líft en áttaðu ljómur en í því er mikið hinnst fyrir upphafi.

Candidate 6: Nýr rannsókn með VLT-hlutunni hafi fundið að flestarinn stjórnandi er tekið af út og skjótinn af durustykkum fyrir áður en hann fær í jörðan, það er á sérstaklega ljusaraðgerður enn enn það sem gildið var og innan mestu litmenn og hægri stjórni sem þekkt er.

Candidate 7: Nýr rannsókn með VLT hefur fundið að margt ljósi stjórnuði varraða er borist og flokkur af stærðfræðilegum afdalum áður en stjórnið ná einhverjum fram á Þjóðverjum. Það er í raun lengur glæðilegari en áður heyrðu og á meðal fyrrvirkra stjórni.

</details>

<details><summary>final_semantic_review #112 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:2944

English: Chemical, physical and microbiological in-use stability has been demonstrated for 28 days at 2-8°C. Once opened, the product may be stored for a maximum of 28 days at 2°C to 8°C. Other in-use storage times and conditions are the responsibility of the user.

Reference (shown after audit): Sýnt hefur verið fram á efnafræðilegan, eðlisfræðilegan og örverufræðilegan stöðugleika við notkun í 28 daga við 2-8°C. Eftir að penninn hefur verið notaður einu sinni, má nota hann í allt að 28 daga ef hann er geymdur við 2° til 8°C. Notkun og geymsla umfram þennan tíma eða við önnur geymsluskilyrði er á ábyrgð notanda.

Review: No candidate preserves chemical/physical/microbiological stability plus maximum storage and user responsibility; chemical often becomes genetic.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Sýnt hefur verið fram á efnafræðilega, eðlisfræðilega og örveruefnafræðilega stöðugleika lyfsins á 28 daga við 2-8°C. Ef lyfið hefur verið opnað er geyma að eftirlits gætu verið lauk í aukastöðu 28 daga við 2°C til 8°C. Annar geymsleiðslutími og -setningskvarðar eru ábyrgð ásjónavélar.

Candidate 1: Erfðabundin, eðlisfræðileg og sýlisfræðileg stöðugleiki í notkun hefur verið sýnt fram á 28 daga við 2-8° C. Eftir að lyfið er opnað má geyma það í hámarki 28 daga við 2° C til 8° C. Aðra geymslutíma og skilyrði er ábyrgð notanda.

Candidate 2: Eðli á meðferð eftir myndunar sést í efna-, eðlis- og líffræðilegar viðbrögð í 28 daga við 2-8°C. Eftir opnun er má geyma lyfið í hámarkstímabili 28 daga við 2°C til 8°C. Hjá notendur er ábyrgð á öðrum geymslu- og staðbendingum.

Candidate 3: Stöðugleiki efnisins, efna- og sýkluháttar in- ú notkun, hefur verið sýnt fram fyrir í 28 dagar við 2-8°C. Eftir að lyfið er opnað má geyma það í 28 dagana við 2°C til 8°C. Annars máli notendur ábyrgð á geymslutíma og kvarðargildum.

Candidate 4: Erfildan stöðugleiki af völdum efna, vefja og örvahefða er sýnt fram á 28 daga við 2-8°C. Eftir að lyfið er opnað getur það geymt í hámarki 28 daga við 2°C til 8°C. Annar stjórnunarmat og skilyrði fyrir lyfjagjöfina er ábyrgð notanda.

Candidate 5: Eru sýnt fram á efnafræðilegur, eðlisfræðilegur og líffræðilegur tíðni í notkun í 28 daga við 2-8°C. Eftir opnun má geyma lyfið í 28 daga við 2°C til 8°C. Þar til er hvers konar geymsluþol og skilyrði er ábyrgð notanda.

Candidate 6: Sýnt hefur verið fram á efnisfræðilega, orkugreinilega og sýklaskapamálgæði í notkun fyrir 28 daga við 2-8°C. Eftir að lyfið er opnað má geyma það í hámarksgildi 28 daga við 2°C til 8°C. Áður en notanda sýnir það fyrir sér er ákvæði notanda fyrir önnur gilda- og stillingartíma.

Candidate 7: Eintakaástandið fyrir efnisfræðilega, eðlisfræðilega og sýlumótefnaheilkenni hafa verið sýnt fram á 28 daga á 2-8°C. Eftir að lyfið hefur verið opnuð má geyma það í hámarki 28 daga á 2°C til 8°C. Annars gagnstöðvar við geymslu eftir notkun bera ábyrgð notanda.

</details>

<details><summary>final_semantic_review #113 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:63

English: “Studying afterglows is vital to further our understanding of the objects that become gamma-ray bursts and what they tell us about star formation in the early Universe,” says the studys lead author Jochen Greiner from the Max-Planck Institute for Extraterrestrial Physics in Garching bei München, Germany.

Reference (shown after audit): „Það er nauðsynlegt að rannsaka glæður blossanna svo auka megi skilning okkar á þeim fyrirbærum sem mynda gammablossa og hvað þau segja okkur um myndun stjarna snemma í sögu alheimsins“ segir Jochen Greiner, aðalhöfundur greinar um rannsóknina, og stjarneðlisfræðingur við Max-Planck-Institut für extraterrestrische Physik í Garching við München í Þýskalandi.

Review: All corrupt afterglows, gamma-ray bursts, early-universe star formation and/or institutional attribution.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: "Að grofum er kostur til að æða við líka að gætu nátumaður einnig í sér um hvaða stjörnuhlutir sem sem hvetjaröðar eru verðaðir og hvað þær segja okkur um stjörnufrumun í börnum alþjóðinu," segir leiðursýfandi fyrir rannsóknina Jochen Greiner úr Max-Planck stofnum fyrir fjöldafræn þjóðlega fjöldebyggingu í Garching í München í Þýskaland.

Candidate 1: „Nauðsynlegt er að sýna fram á nýtingu afrausa við áhættuð getingu til að fylgjast með því sem leitið hefur verið að okkur vísa að stjórnamenn eru frá veiki dýrka og hvort þeir segja okkur frá því hvað stjórnamenn fást upp í alþjóðið fyrir hendi.“„, myndar leikartari aðgestu Jöchons Greiner frá framseldar hlutaðeigandi grein í viðskiptastofnuninni fyrir þurrfjórafni í Glómarshúsið í Garching í Münchens, Þýskaland.

Candidate 2: „Viðgangsgefni er mikilvægt að því að við ætlum að því að skilja lengur um gerningar sem eru hraðir á lofti og þau sem makið er, sem við komum í höndum um stjörnuöryggi í yngri Hvernig í Heiminnu“, segir aðilinn Jochen Greiner frá aðilun á flokkinum “studið á viðgangsgefni“ frá Max-Planck-ið fyrir loftræfluaðferðir í Garching, bei München í Þýskalandi.

Candidate 3: "Íhug að eftirlit með endskilinum er krafis að því að frekari skilja við um verulegan lítkolli og hvað þær segja okkur um stjórnun á stjörnúhliðinu í frjálsari geimsvæði," segir Jochen Greiner, aðilabókstöttur okkar þessra rannsóknarar, frá fræðismálarannsóknins Max Planck í þjóðtryggingarafurðir í Garching í Münchener yfirráðasvæði í Noreg.

Candidate 4: "Að taka á meðferð eftir hreinnihluta er mikilvægt til að draga úr okkar skyn í frekari skilningu á efni sem verða með áhrif af gama-gamma-gangir og hvað þeir segja okkur um stjórnsýslu á röð úr óhófninu," segir Jochen Greiner, aðilinaframarásaðilar í tafarlega einingunni fyrir útvara fjórafræði í Garching í München í Þýskaland.

Candidate 5: „Atvinnugreiningar eftirgengjum eru mikilvægt til að bæta unntun okkar um efni sem verða umferðmeð greiamjóð og hvað þeir segja okkar um stjálfsvirkun stjórnsyns í frumurðið,” segir framsæðisforritaðil við greininguna Jochen Greiner af Max-Planck-instituttinu fyrir útirfarandi fysiskið í Garching í Münchener, Þýskaland.

Candidate 6: „Með því að rannsaka eftirvinkjufullabrekta er mikilvægt til að drepið viðtæka unnt að skilja hvaða gnitaði verða og hvað þeir segja okkur um stjórnun stjórnsaka á ófríðu sjóðinu“ segir frásigrifandi aðilur í rannsókninni sem Jochen Greiner frá Max-Plank stofnuninu fyrir uppfinnunarfyrirtækjum í Garching með München, í Þýskaland.

Candidate 7: „Vita frá skuggafæði er verulegt og skyldir til að ætla okkur hversu síðan veira orðið sem verður reynslu í gama-gjarni og af hverju þetta er vituð um stjarnaklukkun í frumfjölda,” segir Jochen Greiner, aðalforverndi þessarar rannsóknar frumhæfisforsvarasafnarinnar í kúsa, algarðarfarðarforsenalaginu í Garching í München í Reykjavík, Heimurinn.

</details>

<details><summary>final_semantic_review #114 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:1524

English: In the case of bulk liquid products the lot or sublot shall be thoroughly mixed in so far as possible and in so far it does not affect the quality of the product, by either manual or mechanical means immediately prior to sampling.

Reference (shown after audit): Þegar um er að ræða fljótandi farm í lausu máli skal blanda framleiðslueininguna eða framleiðsluhlutann eins vandlega og unnt er, annaðhvort handvirkt eða vélvirkt, rétt áður en sýni er tekið.

Review: All corrupt bulk liquid lot mixing, manual/mechanical means or immediate pre-sampling timing.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Ef um er að ræða eitthvað sem er á fljótina skal allt fljót og svifin sig í helming eða undirhjálp viðhöfn, meðan það haldi stöðugt gæði lyfjanna og eigi það á hættu á gæði lyfjanna, fyrir að það sé laus við sýnatök.

Candidate 1: Ef um er að ræða magnlega vatnslega umbúði skal lottið eða undirlokutakið þegar mögulegast er að smíðað vera í skemmtilegu hætti þannig að gæði umbúðsins verði ekki stuttur í því skipti sem hefur áhrif á gæða umbúðsins, með annaðhvort mannsstæðu eða virkni, meðan á því er varða að teita í sýnatök.

Candidate 2: Þegar um er að ræða blandað vökva af húð skal íhlutið eða undirhlutið leysað í fullu að því marki sem unnt er og þegar það hefur ekki áhrif á gæða vöru, með beinu og vélreiknu aðferð áður en sýnilegt er gert.

Candidate 3: Ef um er að ræða magnlega vatnsleiðir skal lotin eða undirlotin, að því marki sem unnt er, vera í fullt samhliða þróun meðan það hægir og að því marki sem það hefur ekki áhrif á gæði vöru, með annaðhvort handverki eða vél, eigi síðar en áður en eftirlit með vörunum er gerð.

Candidate 4: Í öryggi fyrir greinilegar leysir er hlutaðeigandi hluta eða undirhluta liðinni þurft að fengja það í fullt grátt miðað við annaðhvort í eldsnefnum eða tæku leynd eftir fyrirlikvendum og að því tilskildu að það hafi ekki áhrif á gæðaleika leysanna.

Candidate 5: Ef um er að ræða vatnsmyndir sem eru að blöndu skal hlutlausnina eða undirhlutlausnina vera fyrirhuguð í þann hátt sem unnt er og að því marki að það hafi ekki áhrif á gæði vörninnar, með annaðhvort mögulegum handhafi eða með virkum tæknilegum aðferðum áður en elsk er taldur í sýnatökum.

Candidate 6: Ef um er að ræða vökvi efnisleiðna skal lóta eða undirlóta í fullt gagni með öll þannig að hún án þess að hægt sé að viðurkenna gæði lyfsins, með máli að meðhöndla hana með handvissu eða vél, loklega fyrir að samanburði er tekin.

Candidate 7: Ef um er að ræða leitli og leitliþáttir skal skammtan auðvitað með tilteknum leiðum, hvar sem mögulegt er, og meðan því er að gera og það hafa ekki áhrif á gæðu lyfsins meðan það er í nýtingu, með eitthvað mögulegum handhafi eða með vél.

</details>

<details><summary>final_semantic_review #115 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:1385

English: Lynparza is indicated as monotherapy for the maintenance treatment of adult patients with platinum-sensitive relapsed BRCA-mutated (germline and/or somatic) high grade serous epithelial ovarian, fallopian tube, or primary peritoneal cancer who are in response (complete response or partial response) to platinum-based chemotherapy.

Reference (shown after audit): Lynparza er ætlað til einlyfjaviðhaldsmeðferðar hjá fullorðnum sjúklingum eftir bakslag platínunæms þekjufrumukrabbameins með stökkbreytt BRCA (kímlínu og/eða líkamsfrumu) með miklum vefjabreytingum (HGS [high grade serous]) í eggjastokkum, eggjaleiðara eða lífhimnu (frumkrabbamein) sem svara (algjör svörun eða svörun að hluta til) krabbameinslyfjameðferð sem byggist á platínu.

Review: All corrupt maintenance-monotherapy cancer indication, mutation/relapse/platinum-response qualifications.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Lynparza er tilgreind sem einnifæri úr efnahæfi við viðhald sjúklinga, fullorðna, með BRCA-skýrslugreiðslu (germline-skýrslugreiðslu eða skýrslugreiðslu í lífverkunum) í hágradi seruskjúkjúkju, fallopian-tblúðvörpi eða frumur í umferð, með sérfræðilegum slysi og ber að uppfylla skilyrði við efnahæfi með lyf sem innihalda platin.

Candidate 1: Lynparza er ætlað sem einnifæri við hemla meðgönguhjá alþekjunum sjúklingum með BRCA-skv. viðtökum (græðsleg eða græðslegur samanstöndur í frumfjöldi eða í mótteki) með sturtar lágre svipunarsvöng í rúðlókkurín, fallopíntuð eða frumhæfir krabbameini sem er í bori (fullu bori eða hlutbær bori) við lyfjagjöf með platin.

Candidate 2: Lynparza er ætlað til einungisnotkunar til að halda í gegnum meðferð með fullt nítra sem gjaldar platin og eru BRCA-mutatir (beinlegar og/eða líkamlegar) langreiðsluskemmir, hækkuð, serusýrði í kjólum, fallopíntegunda, eða upphaflega kjólun í umbúðinu hjá fullorðnum sjúklingum sem hafa svar við nítra efnahaglega krabbameðhöndlun.

Candidate 3: Lynparza er ætlað til einar meðferðar með útlentur hjá fullorðnum sjúklingum með brótplatínssjónarettu endurfæddu BRCA-motífa (brátt ígræðsla og/eða fyrirgræðsla) í höfuðvægi serúlgar skjólulaga í stungukviðum, fallopian-vöðva eða fyrstu húðdauða á óþekktum (complete response eða partial response), sem hafa svarið við brótplatínþættum lyfjafrumur.

Candidate 4: Lynparza er ætlað til einar meðferðar við viðhaldi meðal meðal feldis í fulla eða hlutlausu svifagreiningu vegna braktífa við platinur og við BRCA-gerða (slæmi frumum og/eða súþu frumum) ónæðalegri serússjúkdóm í kopulýsins, fallopsfyrirkomnuna eða upphaflega kynkammri, hjá fullorðnum sjúklingum sem hafa svifagreining á platinur meðvottana (platinu base-) meðhöndluð.

Candidate 5: Lynparza er ætlað til eintækla meðferðar við viðhald hjá fullorðnum sjúklingum með gerð BRCA-dynni (germline og/eða sjúkdómheimildir) sem eru með alvarlega serúlíuþjónustuaðli, hægri stigs, í útsetningu úr húð, í fyrrvirktum fallopian tubu eða algengar sjúkdóm húðfæðis (bólgu í rúmum), sem hafa svörun við platinþýðu lyfjafrumnanngur.

Candidate 6: Lynparza er ætlað til einvikrar meðferðar við viðhald hjá fullorðnum sjúklingum með BRCA-hlutaðferðuuppkomu, sem eru með alvarlegri, sagaþyggjandi, serusþykki í húð í kviðamjólkum, fallopian-tungi, eða frumaburdýra í frumaskjölinu, sem hafa svar við palladínsmynduð óvirkjameðferð, í hreinu (heilbrigði eða hlutgeýi) eða óhreinu (heilbrigði).

Candidate 7: Lynparza er ætlað til einnigjögnunar meðferðar hjá fullorðnum sjúklingum með brúktínglaus sjúkdóm með grein í BRCA-fræksunum (fræksun í frumkvæðingu eða eruði) í hágreiðsastýrjulegar, serúla-, valda, óvalda grátt, skerta eða frumkuð ökutækjum í fallopian-túli eða frumruðu eða frumruðu með uppkomu í frumruðu með lyfjafræksun (platinum-bundnum lyfjafræksunum) með viðbótarviðbrögð í (heildarviðbrögð eða hlutaðeigandi).

</details>

<details><summary>final_semantic_review #116 · after · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eso:710

English: The VST KiDS survey will allow astronomers to make precise measurements of dark matter, the structure of galaxy halos, and the evolution of galaxies and clusters.

Reference (shown after audit): Kortlagningin nefnist VST KIDS og gerir stjörnufræðingum kleift að mæla nákvæmlega staðsetningu hulduefnis, uppbyggingu vetrarbrautahjúpa og þróun vetrarbrauta og þyrpinga.

Review: Structure of galactic halos becomes formation of rings in galaxies.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: VST KiDS rannsóknin mun gera stjörnufræðingum kleift að gera nákvæmar mælingar á dökku efninu, myndun hringjar í vetrarbrautum og þróun vetrarbrauta og vetrarbrautahópa.

</details>

<details><summary>final_semantic_review #117 · after · G8 · technical_medium · P</summary>

Source ID: p13official21:test:ema:970

English: In patients with mild hepatic impairment (Child-Pugh A), there was no significant changes in pharmacokinetics compared with normal healthy volunteers.

Reference (shown after audit): Hjá sjúklingum með væga skerðingu á lifrarstarfsemi (Child-Pugh A) voru engar marktækar breytingar á lyfjahvörfum samanborið við heilbrigða sjálfboðaliða.

Review: Candidates0/1/2/3/6 retain mild impairment, no significant PK change, Child-PughA and healthy volunteers.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [0, 1, 2, 3, 6]

Candidate 0: Hjá sjúklingum með vægt skerta lifrarstarfsemi (Child-Pugh A) voru engin marktæk breytingar á lyfjahvörfum borið saman við eðlilega heilbrigða sjálfboðaliða.

Candidate 1: Hjá sjúklingum með vægt skerðingu á lifrarstarfsemi (Child-Pugh A) komu engin marktæk breytingar fram á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.

Candidate 2: Hjá sjúklingum með væga skerðingu á lifrarstarfsemi (Child-Pugh A) varð ekki marktæk breytingar á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.

Candidate 3: Hjá sjúklingum með vægt skerta lifrarstarfsemi (Child-Pugh A) var engin marktæk breytingar í lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.

Candidate 4: Hjá sjúklingum með vægari lifrarstarfsemi (Child-Pugh A) voru ekki marktæk breytingar á lyfjahvörfum samanborið við eðlilega, heilbrigða sjálfboðaliða.

Candidate 5: Hjá sjúklingum með vægan lifrarbilun (Child-Pugh A) varð ekki marktækt breytingar á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.

Candidate 6: Hjá sjúklingum með vægt skerta lifrarstarfsemi (Child-Pugh A) var enginn marktæk breytingar á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.

Candidate 7: Hjá sjúklingum með vægt skerðingu á lifrarstarfsemi (Child-Pugh A) var ekki marktækt breytingar á lyfjahvörfum samanborið við heilbrigðan heilbrigði hjá sjálfboðaliðum.

</details>

<details><summary>final_semantic_review #118 · after · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:2621

English: I'm glad you found one another."

Reference (shown after audit): Ég er svo ánægð að þið funduð hvort annað."

Review: Finding one another becomes finding either one.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Mér gleður að þú hafir fundið annað hvort."

</details>

<details><summary>final_semantic_review #119 · after · greedy · technical_medium · F</summary>

Source ID: p13official21:test:ema:2650

English: Patients should be advised that in the event of any sudden visual defect, they should stop taking Sildenafil Actavis and consult a physician immediately (see section 4.3).

Reference (shown after audit): Ráðleggja á sjúklingum að hætta töku Sildenafil Actavis og hafa strax samband við lækni ef þeir finna fyrir skyndilegri sjónskerðingu (sjá kafla 4.3).

Review: Sudden visual defect becomes a different visual impairment; sudden-onset condition is lost.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Sjúklingum skal ráðlagt að hætta tafarlaust meðferð með Sildenafil Actavis ef þeir fá sér ólíka sjónskerðingu og leita læknis tafarlaust (sjá kafla 4.3).

</details>

<details><summary>final_semantic_review #120 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:63

English: The placement of these devices in the soil should not result in preferential flow paths.

Reference (shown after audit): Staðsetning þessara tækja í jarðveginum má ekki breyta farvegi vatnsins.

Review: Preferential flow paths are not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Setning þessara búnaðar í jörð skal ekki leysa til að þeirri áhættu að þær skipti með sér áhættuflutningslega.

</details>

<details><summary>final_semantic_review #121 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:568

English: This device shall reverse the window/roof panel/partition before it exerts a pinch force of more than 100 N within the opening of 200 mm to 4 mm above the top edge of a power-operated window/partition or in front of the leading edge of a sliding roof panel and at the trailing edge of a tilting roof panel.

Reference (shown after audit): Þessi búnaður skal enduropna gluggann/þaklúguna/skilrúmið áður en klemmuaflið nær gildinu 100 N, innan ops sem er 200 mm til 4 mm yfir efri brún rafstýrðrar rúðu/skilrúms eða framan við leiðandi brún rennandi þaklúgu og við aftari brún þaklúgu sem er hnikað til.

Review: Reversing operation, pinch force and positional geometry are corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þessi búnaður skal endurnýja glugga/rúði/fjölskyldu fyrir því að hún stendur í því skipti að meira en 100 N á 200 mm til 4 mm yfir hátræti loftkraftsnotuðra glugga/fjölskylds eða í fyrirhliði á fyrstu hátræti loftkraftsnotuðra rúðis og á bakstæðri hátræti loftkraftsnotuðra fjölsluðra rúðis.

</details>

<details><summary>final_semantic_review #122 · before · G8 · technical_medium · P</summary>

Source ID: p13official21:test:eea:2090

English: Member States shall require the competent authorities to monitor compliance with this Regulation effectively and take all necessary measures to ensure such compliance.

Reference (shown after audit): Aðildarríki skulu skylda lögbær yfirvöld til að hafa eftirlit með því að farið sé með virkum hætti eftir þessari reglugerð og gera allar nauðsynlegar ráðstafanir til að tryggja að farið sé að ákvæðum hennar.

Review: Candidate7 retains MemberStates requiring competent authorities effective monitoring of fulfilled regulatory requirements and all necessary measures.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [7]

Candidate 0: Aðildarríkin skulu krefjast lögbæru yfirvölda um að tryggja að þessari reglugerð sé brotlaus og því að þau geri allar nauðsynlegar ráðstafanir til að tryggja þá samræmi.

Candidate 1: Aðildarríkin skulu krefjast lögbæru yfirvölda að eftirliti á að þessi reglugerð sé fylgt í því skyni að það sé virklega og að því að þau gerðu allar nauðsynlegar ráðstafanir til þess að tryggja það.

Candidate 2: Aðildarríkin skulu krefjast lögbæru yfirvölda um að fylgi þessari reglugerði sé umhverfislega og geri allar nauðsynlegar ráðstafanir til að tryggja hvernig það sé.

Candidate 3: Aðildarríkin skulu krefjast lögbæru yfirvölda um að eftirliti sé gerð áfram fyrir að þessi reglugerð sé beitt og sérstaklega gera allar nauðsynlegar ráðstafanir til að tryggja það.

Candidate 4: Aðildarríkin skulu krefjast þess að lögbær yfirvöld eigi að staðfesta áfram að þessari reglugerð sé fullnægjandi og gera viðeigandi ráðstafanir til að tryggja það.

Candidate 5: Aðildarríkin skulu krefjast lögbæru yfirvölda til að eftirliti með hæfir hætti á að þau uppfylli þessa reglugerð og taka allar nauðsynlegar ráðstafanir til að tryggja slíka samræmi.

Candidate 6: Aðildarríkin skulu krefjast lögbærri yfirvöld að ráða hvers konar reglu þessari með því að starfsskilum þeirra sé til staðarhæfis og taka öll nauðsynlegar ráðstafanir til að tryggja það.

Candidate 7: Aðildarríki skulu krefjast lögbæru yfirvölda um að hafa skilvirkri eftirlit með því að kröfurnar í þessari reglugerð verði uppfylltar og taka allar nauðsynlegar ráðstafanir til að tryggja það.

</details>

<details><summary>final_semantic_review #123 · before · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:2621

English: I'm glad you found one another."

Reference (shown after audit): Ég er svo ánægð að þið funduð hvort annað."

Review: One another becomes either one.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ég er hrifinn af því að þið hafðir fundið annaðhvort."

</details>

<details><summary>final_semantic_review #124 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:1323

English: If refills are not provided, the weight of the total primary packaging shall not exceed 3,7 g per wash for tablets and 1,7 g per wash for all other products.

Reference (shown after audit): Ef áfyllingar eru ekki í boði skal þyngd grunnumbúðanna í heild ekki vera meiri en 3,7 grömm á þvott ef um er að ræða töflur og 1,7 grömm á þvott fyrir allar aðrar vörur.

Review: No candidate preserves refills/total primary packaging/per-wash constraint together.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Ef ekki er tilfylgt að endurtekinum skal þyngd heildaraðfæðs fyrir varðandi þágu, hafa ekki meiri en 3,7 g, þegar um er að ræða töflur, og 1,7 g, þegar um er að ræða önnur vörur.

Candidate 1: Ef fyllinguþoli er ekki tilhöfður skal takmarka eigi vigt öllum fyrirhuguðu umbúðinum sem er smíðað í 3,7 g fyrir handhandamjöðu fyrir töflur og 1,7 g fyrir handhandamjöðu fyrir öllu öðru íhlutar.

Candidate 2: Ef ekki er veitt endurtekin skal þessi hlutverk eyna áburðarblöndu ekki vera meira en 3,7 gr. fyrir hverja þvott með töflum og 1,7 gr. fyrir öðru vörusýni.

Candidate 3: Ef ekki er veitt endurtekin skal líkamadæmi heildarfrásæðislífrar eigi að megi líta fram 3,7 g fyrir hverja þvöfur með töflum og 1,7 g fyrir alla öðru vörur.

Candidate 4: Ef ekki er til greiðslu skal þýði heildargrundvelliðum, sem eru fargar samkvæmt afurðum, að vera ekki meira en 3,7 g á hverri þurrun fyrir töflur og 1,7 g á hverri þurrun fyrir öllum öðrum vélum.

Candidate 5: Ef ekki er í fót uppfyllingar skal þjóðhámarksgildi heildarfrsæðilegra pakkningarins meiri en 3,7 g hvert fullung með þvo smíða fyrir töflur og 1,7 g hvert fullung með þjóðanum fyrir öll aðra vörur.

Candidate 6: Ef tilbætur eru ekki veittir skal hreyfillnæmi heildarskörnunar, sem er látinn í hendi fyrir hverri rödd, vera ekki meiri en 3,7 g hver rödd að því er varðar töflur og 1,7 g hver rödd að því er varða öll önnur vörur.

Candidate 7: Ef ekki er fenginn viðbættu skal þyngd heildarfrumduð afburðarfræðis ekki vera meira en 3,7 g fyrir hverja þurfu með töflum og 1,7 g fyrir allar öðru afurðir.

</details>

<details><summary>final_semantic_review #125 · after · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:400

English: ESPRESSO will feature radial velocity precision of 0.35 km/hour or less.

Reference (shown after audit): ESPRESSO mun ná að greina sjónstefnuhraða niður í 0,35 km/klst eða minna.

Review: Radial component of velocity precision is omitted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: ESPRESSO mun koma fram með nákvæmni á hraða sem er 0,35 km/klst. eða minna.

</details>

<details><summary>final_semantic_review #126 · after · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:20

English: These galaxies span a vast range of distances from us.

Reference (shown after audit): Allar eru þessar vetrarbrautir í mismikilli fjarlægð frá okkur.

Review: Vast range of distances becomes much farther boundaries; diversity of distances not retained.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þessi vetrarbraut eru í miklu fjarlægri mörkum frá okkur.

</details>

<details><summary>final_semantic_review #127 · before · greedy · technical_short · U</summary>

Source ID: p13official21:test:eso:349

English: The results described here use some of these Science Verification data.

Reference (shown after audit): Gögnin sem notuð voru fyrir þessa rannsókn var að hluta til aflað við þessar prófanir.

Review: Science-verification data and results using them recognizable, but extra reports and malformed syntax make the relation uncertain.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Niðurstöðurnar sem eru lýst hér nota í þeim skýrslum einhverja af þessum vísindalegum sannprófunardatni.

</details>

<details><summary>final_semantic_review #128 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:1751

English: On the basis of the common criteria, and in view of the fact that, to date, ICAO has not agreed to the closure of any of the findings raised during its audits, it is assessed that, at present, the competent authorities of Indonesia have failed to demonstrate that they have performed their regulatory and oversight responsibilities in compliance with ICAO standards with respect to all the carriers they certify.

Reference (shown after audit): Á grundvelli sameiginlegu viðmiðananna og í ljósi þess að enn sem komið er hefur Alþjóðaflugmálastofnunin ekki samþykkt lyktir neinna þeirra mála sem komu í ljós við úttektir hennar er það metið svo að eins og sakir standa hafi lögbær yfirvöld í Indónesíu ekki getað sýnt fram á að þau hafi gætt ábyrgðar sinnar á sviði reglusetningar og eftirlits í samræmi við staðla Alþjóðaflugmálastofnunarinnar með tilliti til allra flugrekenda sem þau votta.

Review: All corrupt Indonesia/certifying-carrier scope, audit-findings closure or regulatory oversight duties.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Í því skyni að neyðarmarkaðirnar hafi samræmt við hlutaðeigandi ástandi og til að tekja tillit til þess að, þegar viðritað er, ICAO hefur ekki samþykkt lokið á einhverjum svæðum sem hætti voru fram á með rannsóknirnar sinnar, er greint að núna, að því er varðar úrræði í Indíó, höfðu lögbær yfirvöld skildu ekki fram á að þeir hafi framkvæmt reglukaupa og afhendingaheimild sína í samræmi við stöðlum ICAO með tilliti til öllum fluttanna sem þeir staðfesta.

Candidate 1: Býðan af sameiginlegum viðmiðunum og í ljósi þess að ICAO hafi ekki samþykkt því að lokast allar ávik sem fengu að fá á með úttektastundum þá er metað að þau lögbæru yfirvöld í Indíó hafðu ekki sýnt fram á að þau hafi grípt þá reglur og eftirliti sem þeir eru skyldur fyrir og geri það í samræmi við ákvæði ICAO að því er varðar öllum flugrekandi sem þau kveða fram.

Candidate 2: Að grundvelli sameiginlegra viðmiðananna og með hliðsjón af því að um þá allt sem þó eftir staðar hafa verið aflótur í sannprófi um útburð þjónustu, er matið þriðju að þeirra lögbær yfirvöld í Indó, hafi aðildarríki verið fyrirtæki um að fullnægja að þau hafi framkvæmt lögbær og í yfirvöldvarárekjastjórnunarbundnum skyldum sínar í samræmi við staða ICAO með tilliti til öllum fluttana sem þeir staðfesta.

Candidate 3: Að grundvallar samrita viðsamegileika og með hliðsjón af því að þar til augnaböndu er flugvöld ICAO ekki samþykkt að loka neinu af þeim niðurstöðum sem voru sett í ljós með skoðunaraðgerðum þeirra, er matið að núverandi lögbær yfirvöld í Indíu hafi missið við að sýna fram á að þau hafi fullnægt reglueigð og eftirlitsbundnu skyldu sín í samræmi við gildandi ICAO-stöðlum í þeim felldum sem viðurkenndar eru.

Candidate 4: Að grundvelli sameiginlega viðmiðana og með tilliti til þess að þegar tilskildu hafa verið ekki samþykkt í samræmi við almenningarsviði ICAO um það að þær gagna sem borðað voru í úrskurða í tengslum við henni hafi verið matin gert að lögbært yfirvald Indóka hefur ekki sýndir fram á því að þau hafi greitt ákvæði fyrirskipunar og eftirlits í samræmi við ákvæði ICAO við allar flugrekendum sem þau unnið.

Candidate 5: Á grundvöldum sameilda viðmiðana og með hliðsjón af því að í fyrra félagi hefur Flugmálastofnun í Bandaríkjum verið samþykkt um lokið tiltekna niðurstöðva þegar flugrekandinn hefur gangið fram í skoðunum sinni er meti að lögbær yfirvöld í Indíen hafi hins vegar missað fram á að sýna fram á að þau hefðu stytt gagna og eftirlit þeirra í samræmi við stöðlum Flugmálastofnunar í Bandaríkjum við öll flugrekand sem þau gjöfðu vottorð fyrir.

Candidate 6: Með tilliti til þess að ÍSAA hefur ekki samþykkt lok á allar ályktunum sem var gefin fram í skoðunum og á grundvelli sameiginlega viðmiðana er matið þannig að núna hafa lögbærum yfirvöldum í Indó ekki sýnt fram á að þær hafi fullnægt stuðningaraðila og eftirlitsbundin ábyrgð þeirra í samræmi við reglubreiðslur ÍSAA um öllum flutningsfélög þeir handkveða.

Candidate 7: Á grundvelli sameiginlegra viðmiðana og með hliðsjón af því að, þegar hæfileika er, ICAO hefur ekki samþykkist að lokandi sé um nokkur af niðurstöðum sem koma fram í skoðunum eiga lögbær yfirvöld í Indíía ekki þegar sýnt fram á því að þau hafi farið fram á ábyrgð sín sem reglur og skoðunarkerfis með tilliti til ICAO-stöðlanna sem hafa verið samþykkt allra flugrekandanum sem þau skyltu.

</details>

<details><summary>final_semantic_review #129 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eso:871

English: A team of astronomers led by Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) first used the ULTRACAM system on ESOs New Technology Telescope to measure these brightness changes very precisely.

Reference (shown after audit): Hópur stjörnufræðinga undir forystu Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) notaði fyrst ULTRACAM mælitækið á New Technology Telescope ESO til að mæla birtubreytingarnar með mikilli nákvæmni.

Review: Every candidate corrupts astronomer-team leadership, telescope or precise brightness-change measurement.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Fjöllaborð af æðarfræðinga, sömu Adam Hardy (Universidad Valparaíso, Valparaíso, Chile), fyrst notuðu ULTRACAM-verkmála í viðtak við neytinu ESO á nýju tækni herbergjuna og mælðu þessum skemmtaleiki á viðbætt hátt.

Candidate 1: Tveggja tilsta fylgjarnir astríðanna, Adam Hardy (Universidad Valparaíso, Valparaíso, Chile), fyrst notaðu ULTRACAM kerfið á nýjum tækni-tekníkum ESO-tengilegri tekníkuastæðinni til að mæla breytingum á svipaðni við þá vegi.

Candidate 2: Fjölskyldubótarfær, Adam Hardy (Universidad Valparaíso, Valparaíso, Chile), fyrst notaðu ULTRACAM kerfisynsleyfið á nýju tækninu á nýju teknunni sem ESO (European Southern Observatory) var að búast undir.

Candidate 3: Hjópskynlæiðarrétta, leit upp af Adam Hardy (Universidad Valparaíso, Valparaíso, Chile), fyrst notaði ULTRACAM-kerfið á nýju tæknilegri rannsóknartegundum í ESO-tekjum til að mæla um litandi breytinga.

Candidate 4: Höfundur Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) hópið að notkun ULTRACAM-starfsettakerfi í nýja tækni teinni til miðlun hversu álit styrktist fyrir um ESO-tekni-teinni.

Candidate 5: Fyrst átt Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) með stjórnsýni á skemmtinum notuð ULTRACAM kerfisins á nýju tækni hreyfilinn ESO til að metast þessi ljóssfjöldaábrunum mjög hugsanleg.

Candidate 6: Fjölskyldu ókólna, leitaður Adam Haryds (Universidad Valparaíso, Valparaíso, Chile), ástgjafarinn Béla Kucke (Universidad Valparaíso, Valparaíso, Chile) fyrst notuð þessu ULTRACAM kerfi á nykkjafyrra tækniræktunni ESO til að metast þessi ljóskaðna breytir mjög nákvæmlega.

Candidate 7: Fyrst var stjórnsýnaskemmti Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) að nota ULTRACAM kerfisins á nýjum tækjum á neytisölunni ESO til að mæla á littryggingum með verulega nákvæmni.

</details>

<details><summary>final_semantic_review #130 · after · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eso:554

English: In the lower part of the image a big chunk of the molecular cloud that gave birth to these stellar youngsters still can be seen.

Reference (shown after audit): Á neðri helmingi myndarinnar sést stór hluti af sameindaskýinu sem gat af sér stjörnurnar ungu.

Review: Molecular cloud and still visible become physical fog and still okay.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Í lágri hluta myndarinnar er stór flögu af líkamlegu loftþokunni sem fæddi þessar stjörnuunglingar enn í lagi.

</details>

<details><summary>final_semantic_review #131 · before · G8 · technical_medium · P</summary>

Source ID: p13official21:test:ema:1495

English: Check again to make sure the correct dose of Tevagrastim is in the syringe.

Reference (shown after audit): Athugaðu aftur hvort rétt magn Tevagrastim er í sprautunni.

Review: Candidates1/4 preserve rechecking correct Tevagrastim dose in syringe.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [1, 4]

Candidate 0: Skoðaðu á sviði að fullnægja að rólega skammtur Tevagrastims sé í sprautunni.

Candidate 1: Gernu að kanna aftur til að tryggja að réttur skammtur af Tevagrastim sé í sprautunni.

Candidate 2: Gerau skoðun aftur til að sjá tilskild efni Tevagrastims í sprautunni.

Candidate 3: Reyndu um aftur til að sjá að rétt skammtur af Tevagrastim sé í sprautunni.

Candidate 4: Skoðuðu aftur til að tryggja að réttur skammtur af Tevagrastim sé í sprautunni.

Candidate 5: Sjáðu aftur að talin verði í rörinn í ljós.

Candidate 6: Skoðaðu slíkt aftur til að tryggja að lyfið innihaldi réttina skammta.

Candidate 7: Komið að henda á endur að tryggja að réttur skammtur af Tevagrastim er í sprautunni.

</details>

<details><summary>final_semantic_review #132 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:ema:978

English: Similarly, the geometric mean AUC (CV%) values at Cycle 6 were higher among the subcutaneous group than the intravenous group; 4088 μg day/mL (34.2) versus 3630 μg day/mL (32.8) respectively) with a resulting adjusted geometric mean ratio [90% CI] of 1.10 [0.98-1.24].

Reference (shown after audit): Sömuleiðis var margfeldismeðaltal AUC (flatarmál undir þéttniferli) (fráviksstuðull) í meðferðarlotu 6 hærra hjá hópnum sem fékk MabThera undir húð en hjá hópnum sem fékk MabThera í æð; 4.088 μg dag/ml (34,2) borið saman við 3.630 μg dag/ml (32,8) respectively og leiðrétt hlutfall margfeldismeðaltala [90% öryggismörk] var því 1,10 [0,98-1,24].

Review: Subcutaneous group, geometric means/ratio and confidence interval corrupted despite retained numbers.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Sambærilega var meðalgeinar AUC-gildi (CV%) í 6. róma hækkur hjá undirhúsnýtingu en í innrennsli: 4088 μg dag/mL (34,2)% við 3630 μg dag/mL (32,8)% samfellt, með því að framkvæmdastjórnandi meðalgeinar gildi [90% viknaframfærð] fyrir 1,10 [0,98-1,24].

</details>

<details><summary>final_semantic_review #133 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:179

English: These violent explosions rip through the molecular gas clouds in their immediate surroundings, but after the shockwaves have travelled more than about ten light-years they are weaker, and may instead compress clouds that are a little further away, triggering the formation of new generations of stars.

Reference (shown after audit): Höggbylgjur þessara orkuríku sprenginga tæta sundur sameindagasskýin í kring en eftir að þær hafa ferðast meira en tíu ljósár eða svo, hafa þær veikst en geta þjappað fjarlægari skýjum saman og þannig hrundið af stað myndun nýrra kynslóða stjarna.

Review: All corrupt molecular clouds/shockwave weakening or farther-cloud compression triggering stars.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þessi rauði sprengingar brjóta í rauði geimvökum í nálægt umhverfi, en eftir að hryggjaröndum hafa flutt þær meira en um tíu ljósára breytir eru þær vægar og geta þess vegna þá rauði geimvökum sem eru stutt fyrir, hlauparaðar á nýju ævindrömur úr stjörnum.

Candidate 1: Þessi ömurlegar sprengingar sérstaklega beinu þéttum gaskúlum í nálægri umhverfi þeirra, en eftir að skjálftabláinum hefur fara meira en um tíu ljósára færrar eru þær vægari, og geta þá þess að þrýsti það í slíkir hófar sem eru stuttar fyrir er, olli þau að myndi framleika nýrrar ævi stjarna.

Candidate 2: Þessi erfiðir sprengingar skola fyrir efnisgaslegar loftniður í nálægum umhverfi sínu, en eftir það að skjölmálum hafa farið í meira en um tíu ljósára er þær stærri og geta þar af leiðandi styttri loftnámi sem eru næstum lengur en það, sem hefur það hvarfefni myndun nýrra ástanda stjarna.

Candidate 3: Þessi veruleg afblæðing hlaup hraða alls undir þær stunguhringar sem eru í umkringlum svæðum en eftir að þær hlaupar hraðir hafa komið fram yfir um árum eru þær eins styttri og geta þó því komið til þess að þrýstir einhverjar skýir sem eru í frikum, og því geta þau indráttar nýra fæðuna stjörnur.

Candidate 4: Þessi sáramjögnur leggja undir kúnaþokum og eru því að vinna eftir að skerðingar hafa farið meira en um tíu ljósára, ættar þeir því að skrýða hliðsjónsskaða sem eru fyrir um um það bil þar sem þeim verður að hraða upp nýjar starfi.

Candidate 5: Þessar rauða sprengingar skapa skímmur um umhverfisglæði í nálægt svæði, en eftir að skjaldnir eru mikið langt um tíð sem vísi um eina títandi ljósáranum eru þær værir öðruvísi kræftar og geta gera það hryðjá á um umhverfisglæði sem eru lítið færri burt, að hlaupi úr því myndun nýjar æðagrennna.

Candidate 6: Þessir alvarlegar sprengingar koma í gegnum mótvega gasglönn og þær komna þá að strax en skeljum þeirri stjörnum tíðbreytingum en þegar skeljungur hefur farið frekar en um tíu ljósára þá eru þær styttr og geta í stað bittið nýgátir af lofti sem eru stuttar til staðar og hefur þá hátt áhrif á myndun nýu árafjölda stjarna.

Candidate 7: Við þessi kraftaverk eru þess arðbergir gert í það gáttu í líkamlega gasmyndum í íbúgildi þeirra en eftir að óhömmunarkræfir hafa farið yfir í meira en um tíu ljósára er þeir vægar og hægt er í stað að þrýstir þeim sem eru í nærri þátt og löguðu þeim, að því er varðar myndun nýrra æxlisflokka.

</details>

<details><summary>final_semantic_review #134 · after · G8 · technical_medium · P</summary>

Source ID: p13official21:test:eso:871

English: A team of astronomers led by Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) first used the ULTRACAM system on ESOs New Technology Telescope to measure these brightness changes very precisely.

Reference (shown after audit): Hópur stjörnufræðinga undir forystu Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) notaði fyrst ULTRACAM mælitækið á New Technology Telescope ESO til að mæla birtubreytingarnar með mikilli nákvæmni.

Review: Candidate1 preserves AdamHardy-led astronomy team, ULTRACAM/NewTechnologyTelescope and precise brightness-change measurements.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [1]

Candidate 0: Hópur stjörnufræðinga, gefinn á byrjun Adam Hardy (Universidad Valparaíso, Valparaíso í Chile), notuði fyrst þann ILTRACAM kerfi við New Technology Telescope ESO til að mæla venjulega breytir á svæðum.

Candidate 1: Hópur stjörnufræðinga, leitt af Adam Hardy (Università Valparaiso, Valparaiso í Chile), fyrst notaði ULTRACAM kerfið á New Technology Telescope ESO til þess að mæla fyrir ljósstigsbreytingunum mjög nákvæmlega.

Candidate 2: Hópur stjörnufræðinga, gefinn gefið leitil til Adam Hardy (Universidad Valparaíso, Valparaíso, Chile), notuði ULTRACAM kerfið á New Technology Telescope ESO til að mæla skýrlega á birtum breytum á stjörnunum.

Candidate 3: Hópur stjarnvísindamanna, á borð Adam Hardy (Universidad Valparaíso, Valparaíso í Chile) fyrst notuði ULTRACAM kerfið á New Technology Telescope ESO til að mæla ljósverkni í þessum skiptum.

Candidate 4: Hópur stjarnvísinda, yfirskipað Adam Hardy (Universidad Valparaíso í Chile), notuði fyrst ULTRACAM kerfinu á New Technology Telescope ESO til að mæla bæði áhrif á ljósstyrkurinni svo nákvæmlega sem mögulegt er.

Candidate 5: Hópur stjörnufræðinga, yfirskipuð Adam Hardy (Universidad Valparaíso í Chile), nýtti ULTRACAM kerfið á New Technology tealli ESO til að mæla skýrlega úr breytni á ljósstyrkum.

Candidate 6: Fjölskylda stjörnufræðinga, leitt af Adam Hardy (Universidad Valparaíso í Valparaíso í Chile), fyrst notuð hefur ULTRACAM kerfið á New Technology Telescope ESO til að mæla í mjög nákvæmri hætti um breytanir ljósafmagns.

Candidate 7: Starfsfélög stjörnufræðinga, leitt á forysti Adam Hardy (Universidad Valparaíso, Valparaíso í Chile), fannst fyrst og fyrst með ULTRACAM kerfinu á New Technology Telescope ESO til að mæla ljósmagna breytina mjög nákvæmlega.

</details>

<details><summary>final_semantic_review #135 · after · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:936

English: Ma'am, I need the gentleman's signature so we can begin.

Reference (shown after audit): Ég þarf að fá undirskrift hans svo við getum byrjað.

Review: Need the gentleman signature to begin retained; inflection errors only.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Frú, ég þarf undirskriftur herra til að byrja.

</details>

<details><summary>final_semantic_review #136 · after · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:2130

English: Because Mr. Doyle called and said you have not been there all week.

Reference (shown after audit): Því að herra Doyle hringdi og sagði að þú hafir ekki mætt alla vikuna.

Review: Doyle called, saying you were not there during the week retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Því að Doyle hringdi og sagði að þú hefur ekki verið þar í viku.

</details>

<details><summary>final_semantic_review #137 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eso:502

English: The first five signals are very confident, while the sixth is tentative, and seventh more tentative still.

Reference (shown after audit): Fyrstu fimm merkin voru mjög sannfærandi en meiri óvissa ríkir um það sjötta og enn meiri óvissa um hið sjöunda.

Review: No candidate preserves first-five confident versus sixth tentative and seventh more tentative.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Fyrsta fimm merkir eru of algaðar, þar sem sjötta er þremur eftir undirbúin og sem sjötta í tönum, og sjötta þriggja eftir undirbúin.

Candidate 1: Fyrstu fimm hættulla eru mjög tækt en sjöttháttar og sjöttháttis hennar er stökkbreytt.

Candidate 2: Fyrsta fimm merkingarnir eru mjög þekkilegar en sjöðuður, en sá sem stendur á sigstæðu hagalega þakkom.

Candidate 3: Fyrstu fimm síma eru mjög vicandi og syfandi þriðja síma er hæðar sem þá.

Candidate 4: Fyrsta fimm mörk eru mjög treyjaðra en sjöunduðum mörkum er fóstra, og sjöunda mörkum er þær enn fóstra.

Candidate 5: Fyrstu fimm útgefið vissa, þar sem sjöunduður er ósíðaður.

Candidate 6: Eftirfarandi fimm merkja eru verulega treyst, þar sem sjóðust er öðrum tíma og svona.

Candidate 7: Fyrstu fimm verkaður, þrjú þannig varjara og þegar þrjú er þríðju varjara enn.

</details>

<details><summary>final_semantic_review #138 · after · G8 · technical_short · U</summary>

Source ID: p13official21:test:eso:136

English: ALMA is radically different from visible-light and infrared telescopes.

Reference (shown after audit): ALMA er gerólík sjónaukum sem sjá sýnilegt og innrautt ljós.

Review: Candidate6 approximates visible/infrared light but phrase says telescopes coming into light; exact spectral comparison uncertain. Others omit visible-light restriction.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: ALMA er skömmu ólík af skyni geymslu og infrarámetru sjónauka.

Candidate 1: ALMA er til mikilvægu mismunandi frá sjónauki og innrauðu sjónauki.

Candidate 2: ALMA er umfangsmikil mismunandi en sjónauka og innrauða sjónauka.

Candidate 3: ALMA er svo alvarlega mismunandi á móti sjónauða og infráleifiskortferli.

Candidate 4: ALMA er aðallega skipt úr sjónauki og in-fræðilegu sjónauki.

Candidate 5: ALMA er hátt mismunur burt af sjónaukum og innrauða sjónaukum.

Candidate 6: ALMA er framangreint mismunandi frá sjónaukum sem koma í ljósi og innrauða ljósi.

Candidate 7: ALMA er umfangsmikill mismunandi frá sjónaukum og innrauðu sjónaukum.

</details>

<details><summary>final_semantic_review #139 · after · G8 · technical_short · U</summary>

Source ID: p13official21:test:ema:1788

English: Magnetic resonance imaging is necessary to confirm the diagnosis of PRES.

Reference (shown after audit): Segulómun er nauðsynleg til að staðfesta greiningu PRES.

Review: Candidate2 retains correct English MRI expansion and PRES diagnosis but supplies a contradictory/corrupt Icelandic term; cannot count a fully correct Icelandic candidate.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Gagnvirk skýrslugreiðslu er nauðsynleg til að statra vísbendingu um PRES.

Candidate 1: Vera nauðsynlegt að skoða PRES með skynhleði.

Candidate 2: Takmörkuðtakmörkuðhvarf (magnetic resonance imaging, MRI) er nauðsynlegt til að staðfesta sjúkdómukvarðanina (PRES).

Candidate 3: Magnæskímyndun er nauðsynleg til að staðfesta sjúkdómurinn með sérfæranlif.

Candidate 4: Magnsöfnun eru nauðsynleg til að staðfesta sjúkdómssýkingu áfram á PAT- hópum.

Candidate 5: Magneðaæðatæknin er nauðsynlegt til að staðfesta sjúkdómssýnina á vegum PRES.

Candidate 6: Magnaheilkenni- myndmyndun er nauðsynleg til að staðfesta sýnun á PRES.

Candidate 7: Magneðsensíslimm bláæðmyndin er nauðsynlegt til að staðfesta sjúkdómsskýringu á PRES.

</details>

<details><summary>final_semantic_review #140 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:1190

English: Indeed, there is a need for technical and scientific support and a high level of stable expertise to properly apply the Community legislation in the fields of maritime safety and ship pollution prevention, to monitor its implementation and to evaluate the effectiveness of the measures in place.

Reference (shown after audit): Raunar er þörf á tækni- og vísindalegri aðstoð og öflugri og yfirgripsmikilli sérfræðiþekkingu til að beita með réttum hætti löggjöf Bandalagsins á sviði siglingaöryggis og varna gegn mengun frá skipum, fylgjast með framkvæmd hennar og meta skilvirkni þeirra ráðstafana sem eru fyrir hendi.

Review: Stable expertise and ship-pollution prevention omitted/corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það er þörf á tæknilegri og vísindalegri stjórnun og mikla staðbundinnar menntarverk við að beita framkvæmd samkvæmt löggjöf Bandalagsins í sviði öryggis á sjó og að koma með hliðsjón af framkvæmdum og meta árangur ráðstafana sem eru í gildi.

</details>

<details><summary>final_semantic_review #141 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:2944

English: Chemical, physical and microbiological in-use stability has been demonstrated for 28 days at 2-8°C. Once opened, the product may be stored for a maximum of 28 days at 2°C to 8°C. Other in-use storage times and conditions are the responsibility of the user.

Reference (shown after audit): Sýnt hefur verið fram á efnafræðilegan, eðlisfræðilegan og örverufræðilegan stöðugleika við notkun í 28 daga við 2-8°C. Eftir að penninn hefur verið notaður einu sinni, má nota hann í allt að 28 daga ef hann er geymdur við 2° til 8°C. Notkun og geymsla umfram þennan tíma eða við önnur geymsluskilyrði er á ábyrgð notanda.

Review: All corrupt chemical/physical/microbiological stability or user responsibility; some change maximum28days to more than28days.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Hæfi undirhaldandi stöðlun á efnisfræðilega, eða líkamsfræðilega, og mikrobiðskjöfanlega samkvæmt notkun hefur verið sýnt fyrir 28 dagar á 2-8° C. Þegar lyfið er opnum má geyma það að hámarki 28 dagum á 2°C til 8°C. Aðra geymaþorð og skilyrði fyrir notkun eru á miðlun notanda.

Candidate 1: Þörfsslysir hafa verið sýndir með þvottír og nýtingargreiningu í 28 daga á 2-8°C. Við uppteka skal geyma lyfið í smásæti í aukastöðu af 2-8°C á móti að því er varðar að lyfið er einnig notaður. Á öðru aukastöðu og ástæðu fyrir notkun eru ábyrgir notanda.

Candidate 2: Rannsókn á stöðugleika efnisvexna, efnaefnis eftir pris og mikrobiálalíka í notkun hefur verið fram á 28 daga á 2-8°C. Ef lyfið hefur verið opnað skal geyma honum að mesteru 28 daga á 2°C til 8°C. Einnig á að notendur bættu að því hvaða stöðugleika og hvernig skráð er lyfið við notkun.

Candidate 3: Stöðugur, efnahagur og mikrobiólegur aðgengi hefur verið sýnt fyrir 28 daga á 2-8°C. Ef lyfið er opnavið má geyma það í staðbundinum gengi eftir 28 dagum á 2°C til 8°C. Aðra gengi til geyminningar og skilyrði er ábyrgð notanda.

Candidate 4: Erfildan stöðugleika af efnablöndun, efnahæfileika og lífveruleika hefur verið sýnt fram á 28 daga á 2-8°C. Hvetur hefur verið um að lykil verði geymd á 2-8°C hámarkstímabil 28 dagar eftir að lykil er opinn. Annar uppfærslustundar og skilyrði fyrir geymingu er ábyrgi notanda.

Candidate 5: Það hefur verið sýnt fram á að efnið standi stöðugt, með tilliti til beinra, með tilliti til efnisfrumur og með tilliti til mikroskófla í notkun á 28 daga að 2-8°C. Eftir að það hefur verið opnað er hægt að geyma efnið á 2°C til 8°C að hámarksverðu 28 daga. Afhvarnir og skilyrði um geymun öðru innan notkunar er ábyrgðaður frá notendunum.

Candidate 6: Hlutfallir, þættir og lífufljóðaðir áhrif í notu hafa verið sýndar fyrir 28 dagar að 2-8°C. Sér um er að gera lyfið geymd í 2-8°C með hámarksgildi 28 dagar eftir að lyfið hefur verið opnað. Aðrar geymdar tíma og skilyrði hafa semjaður viðanallir.

Candidate 7: Erfitt er í sérhæfilegum, efni og gerðum og mikrobiílagtum vegum í notu fyrir 28 daga á 2-8°C. Eftir að henni er opnað er trúnaður gerðarinnar heimilt að vera á 2° C til 8°C á meira en 28 daga. Hjá önnur notendur er handa að ákvarða annan tíma og skilyrði fyrir hugtakandi lausn.

</details>

<details><summary>final_semantic_review #142 · after · G8 · technical_medium · U</summary>

Source ID: p13official21:test:eso:45

English: This would make the system similar to our Solar System in terms of the number of planets (seven as compared to the Solar Systems eight planets).

Reference (shown after audit): Þetta sólkerfi geymir því svipaðan fjölda reikistjarna og sólkerfið okkar (sjö reikistjörnur í samanburði við átta í sólkerfinu okkar).

Review: Candidate6 retains seven-versus-eight and near-similarity relation, but invented similarity wording prevents confident confirmation; others corrupt equality/objects.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þetta myndar á kerfinu jafnvægi sólarkerfinu í því skyni að aðfærðirnir eru sá fær og sólarkerfinu tveggja mánaðarins.

Candidate 1: Það myndi gera kerfið sambærilegt úr sólarkerfinu, í þáttum fjarstæða (sjö geimfara í samanburði við átta fjarstæðum úr sólarkerfinu).

Candidate 2: Þetta myndar kerfið svipað á sólkerfinu okkar í skömmtum fyrir fyrirbæri fyrir fjölda reikistjarna (sjö miðað við átta reikistjörnurnar í sólkerfinu).

Candidate 3: Þetta myndi skaðað kerfið eins og sólarkerfið okkar í því skyni að fjölda reikistjarna (símað við aðalrök stóra sólarkerfisins).

Candidate 4: Þetta myndi gera kerfið svipaði á sólkerfinu og hefur sama fjölda reikistjarna (sjö af miðjunum við eights reikistjörnur í sólaæðinu).

Candidate 5: Þetta myndi benda stöðina til sólarkerfinu í skyninu hvað varðar fjölda reikistjarna (sjö fyrir sig samanborið við fyrir sig eigndreifin af sólarkerfinu).

Candidate 6: Það myndi geri kerfið svipufram á sólkerfinu okkar í þeim þáttum sem um getur um fjölda reikistjarna (sjö þegar samanborið við átta reikistjarna í sólarkerfinu).

Candidate 7: Það myndar saman kerfinum við sólarkerfið í skömmtum fjölda reikistjarna (sjö, samanborið við átta reikistjörnurnar í sólarkerfinu).

</details>

<details><summary>final_semantic_review #143 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:ema:2690

English: Adverse effects not observed in clinical studies but seen in the rat and to a lesser extent in the mouse at exposure levels similar to human exposure levels and with possible relevance for clinical use were liver changes, indicating an adaptive response such as increased weight and centrilobular hypertrophy, fatty infiltration and increased liver enzymes in plasma.

Reference (shown after audit): Aukaverkanir, sem komu ekki fram í klínískum rannsóknum, en sáust hjá rottum og hjá músum þó í minna mæli, við skammta sem eru svipaðir meðferðarskömmtum hjá mönnum og skipta hugsanlega máli við klíníska notkun, voru lifrarbreytingar sem gefa til kynna aðlögunarsvörun eins og aukna þyngd og stækkun í miðju lifrarblaða, fituíferð og aukningu á lifrarensímum í plasma.

Review: Truncated repetitive continuation replaces the named liver effects.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0 [TRUNCATED]: Óhvördur áhrif sem ekki voru sýnt í klínískum rannsóknum en sýndir í rott og mjög minni í húsinu við útsetningargildi sem eru svipaðar útsetningargildi fyrir manns og með möguleika um eftirlit með klínísku notkun komu fram í skjöl, þ.e. breytingar á lifrar, sem benda til aðgerða sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin sem er að gera við aðgerðin

</details>

<details><summary>final_semantic_review #144 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:1433

English: Aseptically add sodium pertechnetate (Tc 99m) solution (from step d above) to the tilmanocept powder vial.

Reference (shown after audit): Bætið með smitgátuðum hætti natríum pertechnetate (Tc 99m) lausn (úr skrefi d hér á undan) í hettuglasið með tilmanocept stofninum.

Review: All corrupt aseptic addition, sodium pertechnetate or powder-vial instruction.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Uðfyllið aefjumína pertechnetat (Tc 99m) lausn (frá lið d á þessari lið) í tilmanóceptið iðgjöf.

Candidate 1: Blöndinn með natriumpertechnetati (Tc 99m) (frá lið d að fyrri) er þegar blönd inn í vellurinn með tilmanocept.

Candidate 2: Anhaldið skal ósrænn liðið af natríum-pertektínetat (Tc 99m) (frá lið d hér að framan) í tilmanócept með húðið (frá lífsvörunum).

Candidate 3: Þykkjastofnun af natríum petrýntektat (Tc 99m) (þegar á er að koma að d-stiginn hér að framan) skal gera í tilmanópekptuða fasvös.

Candidate 4: Uðvinnu niður náttúrulegri einkatið (Tc 99m) í nýtnatferumlífi (frá lið d hér að framan) í röð tilmanóceptiðíð á uðblöndu.

Candidate 5: Hreinsað út af eftirfarandi áeiningu: Tc 99m (náttúruhjónabréfa pertechnetat) lausn (frá þeim áætlanum sem komið er fyrir á sig) og látu því stökkbúa tilmanóceptarad (frá d-stiginn innihaldi) þegar í lyfið.

Candidate 6: Vitrósinuðuð súnnatretmetat (Tc 99m) lausn (frá d-stungu yfir) skal þrátt í áhrif tilmanóceptið löngurvökull.

Candidate 7: Samsænlega bætum við óþynnt naustópsféðis (Tc 99m) lausn (út frá d-steppan í þessum lið) í tilmanóceptu fyrir pótra (vítur).

</details>

<details><summary>final_semantic_review #145 · after · G8 · technical_medium · U</summary>

Source ID: p13official21:test:ema:2652

English: Put the needle fully into the skin as shown by your nurse or doctor (see picture 6).

Reference (shown after audit): Stingdu nálinni í húðina eins og læknirinn eða hjúkrunarfræðingur sýna þér (sjá mynd 6).

Review: Closest5 retains needle/nurse/doctor but fully becomes for all; full-insertion modifier/syntax uncertain. Other candidates change nurse or action.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Settu nálina laus til í húðina eins og hjá svefnfóðurinn eða lækninum sýnist (sjá mynd 6).

Candidate 1: Setjið nálina fullt í húðina eins og náin eða læknirinn sýnir eftir (sjá mynd 6).

Candidate 2: Settu nálinni full komið í húðina eins og nálsa sjúklinga er sjá kjölfar hjá hjúkrunarfræðingi eða lækninum (sjá mynd 6).

Candidate 3: Settu nálinni á fullu í húðina eins og meðferðarlæknirinn eða meðferðaráeinandi sýnir (sjá mynd 6).

Candidate 4: Settu nálinni fullt inn í húðina eins og fræðandi eða hjúkrunarfræðingurinn sýnir (sjá mynd 6).

Candidate 5: Settu nálinni fyrir öll í húðina eins og sýnist fyrir hjá hjúkrunarfræðinginn eða lækninum (sjá mynd 6).

Candidate 6: Settu nálina allt inn í húðina eins og verið er sýnt frá hjá hjúkrunartækinni eða lækninum (sjá mynd 6).

Candidate 7: Settu nálinni í sækni í húðina eins og vefjakerdin eða læknirinn sýnir (sjá mynd 6).

</details>

<details><summary>final_semantic_review #146 · after · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:1433

English: Aseptically add sodium pertechnetate (Tc 99m) solution (from step d above) to the tilmanocept powder vial.

Reference (shown after audit): Bætið með smitgátuðum hætti natríum pertechnetate (Tc 99m) lausn (úr skrefi d hér á undan) í hettuglasið með tilmanocept stofninum.

Review: None preserves aseptic addition plus complete solution/powder-vial identity; sterile solution alone is not aseptic addition.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Aefnid mixtúru safa skiptið úr flösku (frá fyrirlið d hér að framan) í hettuglasinu með tilmanocept dufti.

Candidate 1: Aðruflæsingi skal gefa natríum perteknetat (Tc 99m) lausn (frá d-stigi hér að ofan) í hettuglasinu með tilmanocept dufti.

Candidate 2: Aflsa evicóðuð lausn (Np 99m) (frá d-stignum hér að ofan) til geymsluspýru með tilmanócepti í hettuglasi.

Candidate 3: Að og á ekki sterra afhældu sodium pertechnetat (Tc 99m) lausn (frá d-stiginn hér að framan) til tilmanocept stungulyfsins í hettuglasinu.

Candidate 4: Aðkúmu niður natríum pertechnetat (Tc 99m) lausn (frá d liði hér á ofan) í hettuglasinu sem inniheldur tilmanocept duft.

Candidate 5: Nota skal sæfða natríum pertechnetat (Tc 99m) lausn (fra d stig hér á ofan) til tilmanocept duftfylgiseðils í hettuglasi.

Candidate 6: Aa skammtinu af natriumpertechnetat (Tc 99m) lausn (frá d-stignum hér að framan) á tilmanocept duftaflöskuna í hettuglasinu.

Candidate 7: Samsænka aðeins naútupsertechnetat (Tc 99m) lausn (frá d-stigi fyrir aftur hér) í hettuglasinu með tilmanocept innihaldi.

</details>

<details><summary>final_semantic_review #147 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:ema:3025

English: Based on individual patient response and tolerability, the dose may be increased to 300 mg (15 ml) per day after an interval of 3 to 7 days, and if needed, to a maximum dose of 600 mg (30 ml) per day after an additional 7-day interval.

Reference (shown after audit): Eftir svörun og þoli hvers sjúklings má auka skammtinn í 300 mg (15 ml) á sólarhring eftir 3-7 daga og ef þörf krefur í hámarksskammt, 600 mg (30 ml) á sólarhring, eftir 7 daga til viðbótar.

Review: Maximum600mg constraint omitted; additional-interval qualification not explicit.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Bundin þar sem tilgreind er svörun og þol sjúklings er metið má auka skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga fresti og ef nauðsyn krefur í 600 mg (30 ml) á dag eftir 7 daga fresti.

</details>

<details><summary>final_semantic_review #148 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:1069

English: By using the SPHERE instrument on ESOs Very Large Telescope (VLT) - one of the most powerful planet-hunting instruments in existence - the international team has made the first robust detection of a young planet, named PDS 70b, cleaving a path through the planet-forming material surrounding the young star.

Reference (shown after audit): Með SPHERE mælitækinu á Very Large Telescope (VLT) ESO - sem er eitt öflugasta reikistjörnuleitartæki heims - sáu stjörnufræðingarnir hvernig reikistjarnan unga, PDS 70b, plægir sig í gegnum efnisskífuna sem umlykur stjörnuna.

Review: All corrupt robust detection, powerful planet-hunting qualification or path through planet-forming material.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Með notkun SPHERE mælitæknisins á Very Large Telescope (VLT) ESO, sem er einn af öflugustu mælitækninum til að finna reikistjörnur, hafnar alþjóðlegur hópurinn fyrstu koma fram þjóðarafurðir að fara í gegnum hringringar sem reikistjörnur eru með fyrirbyggjandi efni í kringum þessa ungasta stjörnu.

Candidate 1: Samkvæmt notkun SPHERE mælitækisins á Very Large Telescope ESO (VLT) - einni af þeim mesti kröftugu mælitækjum sem liggja á milli í alheimsins - hefur alþjóða hópurinn gert fyrstu rannsókn á ungbirtu jörðu, nétt nöfnun PDS 70b, í gangi um jörðu- myndunarmat sem snýst um unnu stjörnu.

Candidate 2: Með notkun SPHERE tækninu á Very Large Telescope (VLT) ESO - einkennistæklisins eftir fyrstu sterkustu greiningu á unga reikistjörnu, PDS 70b, hefur alþjóðlegur hópur gert fyrstu álykt á hana.

Candidate 3: Með notkun SPHERE mælitækisins á Very Large Telescope (VLT) ESO, sem er einn af blönduðum mælitæki sem notuð er til að reyna á reikistjörnum - hefur alþjóðalegt hópurin gert fyrstu skallega grein fyrir unga reikistjörnuðann PDS 70b og hafði að skugga um efnið sem umhverfur og byggir á um á unnu stjörnuna.

Candidate 4: Með notkun SPHERE mælitækisins á Very Large Telescope (VLT) ESO hefur alþjóðlegur hópurinn gert fyrsta þyngra undirgreinanlegan greiningu á ungar aðfeldi, númer PDS 70b, og koma í gegnum fyrirhlið aðfeldisins í kringum unga stjörnuna.

Candidate 5: Með notkun SPHERE tækninu á Very Large Telescope ESO (VLT) - einar hæst vetrarbrautaskoti vetrarbrautanna sem liggja á sér - hefur Alþjóðasamfélkið kjaftð aðalfélagið áður á unga veg í barnartraustu PDS 70b sem berst um kringum unna stjörnuna.

Candidate 6: Með notkun SPHERE mælitækisins á Very Large Telescope (VLT) ESO - sem er einn af stærstu sártibúnaði til að taka sjón fyrir heimsjóða - hefur alþjóðalegur hópurin gert fyrstu þræðilega greiningu á ungar heimsjóð, núnan PDS 70b, sem snúaði á gangi úr sviði mörkuðu fyrirbyggjandi efnisins kring umhverfið um rjótt stjörnunni.

Candidate 7: Með notkun SPHERE mælitækisins á Very Large Telescope (VLT) ESO - annarri sætasta mælitækisins til að finna reikistjörnur - hefur alþjóða hópurinn, nýtt fyrstu áhrifar á það yngri reikistjörnu, nýtt neinu, nöfnuð PDS 70b, í korninu um um um borgun af byggjandi efninu af reikistjörnunni.

</details>

<details><summary>final_semantic_review #149 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:568

English: This device shall reverse the window/roof panel/partition before it exerts a pinch force of more than 100 N within the opening of 200 mm to 4 mm above the top edge of a power-operated window/partition or in front of the leading edge of a sliding roof panel and at the trailing edge of a tilting roof panel.

Reference (shown after audit): Þessi búnaður skal enduropna gluggann/þaklúguna/skilrúmið áður en klemmuaflið nær gildinu 100 N, innan ops sem er 200 mm til 4 mm yfir efri brún rafstýrðrar rúðu/skilrúms eða framan við leiðandi brún rennandi þaklúgu og við aftari brún þaklúgu sem er hnikað til.

Review: Vehicle controls become anatomical/unrelated terms and geometry is corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þetta tæki skal snúa glugga/þörmu/teppi fyrir fram á þann tíma sem það skuli stunda meira en 100 N á 200 mm til 4 mm yfir háttar brún í glugga/þörmu/teppi eða fyrir framan háttar brún í slímhlaupi þörmunnar eða yfir háttar brún í hlaupi þörmunnar.

</details>

<details><summary>final_semantic_review #150 · after · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:3044

English: Isn't there someone in some league, who's left- footed?

Reference (shown after audit): Er ekki einhver í einhverri svona deild sem er örfættur?

Review: Left-footed changes to left-handed.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Er ekki einhver í einhverri hópi sem er höfður höndinni til vinstri?

</details>

<details><summary>final_semantic_review #151 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:ema:129

English: Clinical studies have demonstrated that ProQuad can be given simultaneously (but at separate injection sites) with Prevenar and/or hepatitis A vaccine, or with monovalent or combination vaccines comprised of diphtheria, tetanus, acellular pertussis, Haemophilus influenzae type b, inactivated poliomyelitis, or hepatitis B antigen.

Reference (shown after audit): Klínískar rannsóknir hafa sýnt fram á að hægt er að gefa ProQuad á sama tíma (en á öðrum stungu- stað) og Prevenar og/eða lifrarbólgu A bóluefni eða með eingildu eða samsettum bóluefnum með barnaveiki, stífkrampa, frumulausan kíghósta, Haemophilus influenzae af gerð b, deyddum mænu- sóttar eða lifrarbólgu B mótefnavökum.

Review: Vaccines and antigen list extensively corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Læknisk rannsóknir hafa sýnt fram á að ProQuad getur verið gefið samhliða (en í mismunandi stungustöðum) með Prevenar og/eða heilbrigðisvaxmi gegn sýktu A-klínísku sjúkdómum eða með einbúnum vaxmi sem innihalda dýprýng, tétanúsýr, óhyltur af pértrú, H. influenzae b-tengdra, ólifuglaða mótaflutninga, eða vaxmi sem innihalda B-klínísku heilbrigðisvaxmi.

</details>

<details><summary>final_semantic_review #152 · after · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:349

English: The results described here use some of these Science Verification data.

Reference (shown after audit): Gögnin sem notuð voru fyrir þessa rannsókn var að hluta til aflað við þessar prófanir.

Review: No candidate preserves results using ScienceVerification data; outputs reverse use relation or substitute unrelated reports.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Niðurstöðurnar sem merktar eru hér notuð sumar af þessum skýringabákmiðum.

Candidate 1: Niðurstöðurnar sem gefin eru upp eru notaðar af þessum gagnum um vísindalega sannprófun.

Candidate 2: Niðurstöðurnar hér á eftir vega nauðsynlegt af þessum vísindatökum.

Candidate 3: Niðurstöðurnar sem lýsað er hér byggja á sumum upplýsingum um vísindaleikaupplýsingar.

Candidate 4: Niðurstöðurnar sem lýst er hérinnar eru notaðar á sumum þessara upplýsinga um sannprófun á vísindum.

Candidate 5: Niðurstöðurnar sem lýst er hér eru notaðar nokkrar af þessum skýrslugjöfum um vísindalegan sannprófun.

Candidate 6: Niðurstöðurnar, sem er lýst hér, ná að sumum þessara Skýrslugjafar.

Candidate 7: Niðurstöðurnar sem lýst er hér, skipta séríð af þessum rannsóknarupplýsingum.

</details>

<details><summary>final_semantic_review #153 · before · G8 · technical_medium · U</summary>

Source ID: p13official21:test:eea:1509

English: Therefore, in the interest of clarity of legislation, it is appropriate to merge those provisions in one single legislative act.

Reference (shown after audit): Til að tryggja gagnsæi í löggjöf er því rétt að sameina þessi ákvæði í einni lagagerð.

Review: Candidate6 roughly combines provisions for clearer law, but a single legislative-act object is uncertain; other versions corrupt clarity/merging/act.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Því, í þeim þáttum sem hæfar skýrslu, er rétt að hæfa þessar ákvæði í ein sama lagalegan gerð.

Candidate 1: Því í þeim tilvikum þar sem skilgreiningur gerðar er mikilvægt er rétthæf eð að samfylgja þessar ákvæði í einn heildarlega leggja.

Candidate 2: Því er rétt að þessari ákvörðun skuli samið í einum samkvæmt því að sem láti grípið í ljós fyrir skili lög.

Candidate 3: Þar að teknu tilliti til skýrsta lög þarf að blanda þessar ákvæði í einn samkvæmt lögum.

Candidate 4: Því er örugg að samfylgja þessi ákvæði í einum samkvæmt atvinnugleðið af reglugerðum.

Candidate 5: Því, í þróun svagræsrar löganna, er rétt að skipta þessa ákvæði í einn samning.

Candidate 6: Því er rétt að eina saman hafa þá ákvæði í einum ríkisákvæði í því skyni að ná að skýrsli löganna.

Candidate 7: Því eru þessi ákvæði, í þá þyngjandi við þátt í glæðilegri lögum, við á að samanfylgja þá ákvæði í einum röðlegum löggjöf.

</details>

<details><summary>final_semantic_review #154 · after · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:1323

English: If refills are not provided, the weight of the total primary packaging shall not exceed 3,7 g per wash for tablets and 1,7 g per wash for all other products.

Reference (shown after audit): Ef áfyllingar eru ekki í boði skal þyngd grunnumbúðanna í heild ekki vera meiri en 3,7 grömm á þvott ef um er að ræða töflur og 1,7 grömm á þvott fyrir allar aðrar vörur.

Review: Refills, primary packaging and per-wash units corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef ekki er veitt endurtekningar skal þyngd heildarfráseldsins ekki vera meira en 3,7 g fyrir hverja þvag fyrir töflur og 1,7 g fyrir hverja þvag fyrir öll önnur vörur.

</details>

<details><summary>final_semantic_review #155 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eso:45

English: This would make the system similar to our Solar System in terms of the number of planets (seven as compared to the Solar Systems eight planets).

Reference (shown after audit): Þetta sólkerfi geymir því svipaðan fjölda reikistjarna og sólkerfið okkar (sjö reikistjörnur í samanburði við átta í sólkerfinu okkar).

Review: All corrupt planets/SolarSystem and seven-versus-eight comparison.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þetta myndar að tryggingin sé svipað er svo að áætlunarnar verða fyrir óháð með henni og stjórnmálans við hliði og verða fyrir óháð með henni og stjórnmálans á tví.

Candidate 1: Þetta skal gera kerfaði líkt sólarhreyflunum í skiptum fjölda geða (sjö í ljósi sólarhreyflunnar á nafnið eig.)

Candidate 2: Þetta bregðir kerfisins saman heimsins eins og sænheimsin, á teknum fyrir fjöldi planets (septi fyrir samanborið við ótta plöntur sænheimsins).

Candidate 3: Þetta myndi skaðað kerfinu eins og þjállarátin þar sem við erum að ræða og hvorki annar rúmið hefur sínri stórfjölda þjállanna.

Candidate 4: Þetta myndar líkur að þér á því að við erjum heilagið Heimsýslu í þær fjölda geða sem Sólarhvarfinn á við fyrir (sjö geða, komin til áttar sátt fyrir Sólarhvarfinni).

Candidate 5: Þetta myndi gera kerfið líka áhersla síður á þá hvaða fjölda þjóna um um um um hliðarins og umður dýrlaga fyrir síður, þar sem síður áhersli stendur á óhæðinum umðarhlutfjölda.

Candidate 6: Þetta gæti litið þessari kerfi æða mjög saman og útlætið í því skipti þar sem fyrirborðið er í skógunni milli sölutækar að öðrum þótt það er fyrrum.

Candidate 7: Þetta myndi læta lífæðina líkt út á óstarasölunni í því skipti að fylgnir (sjö í tengslum við þau á óstarasölunni).

</details>

<details><summary>final_semantic_review #156 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:79

English: Justified estimates must be made of the expected concentrations of the active substance and relevant metabolites, degradation and reaction products, in soil, groundwater, surface water and air, following use as proposed or already occurring.

Reference (shown after audit): Rökstutt mat verður að koma fram á áætluðum styrk virka efnisins, og viðkomandi umbrots-, niðurbrots- og hvarfaefna, í jarðvegi, grunnvatni, yfirborðsvatni og lofti, eftir núverandi notkun eða ráðgerða notkun.

Review: All corrupt justified expected concentrations, metabolite/degradation/reaction products or environmental compartments.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Rekstrar fáanleiki til að meta viðeigandi hætti virka efnisins og tengdra umbrotsefnis og útbrotsefnis í jarðvökum, grundvöknum, yfirvöknum og lofti, eftir notkun eins og hún er ákveðin eða þar hætur.

Candidate 1: Við úttektum skal taka við gildandi magn gildandi störf á virka efna og tengjast efni og sem verður í grundvelli, grunnvatni, vatnsbólgu og lofti, eftir notkun eins og um er að ræða eða þó aldrig gerð.

Candidate 2: Hægt er að meta áfram að því að viðkomandi efni og efnin eða umbrotin, sem eru tengd efni efni, verði í tilteknum stöðlum í soði, grundvatni, jörðvog og lofti ef meðferð er stundað eða tilgreind eða tiltekin hefur tiltekin.

Candidate 3: Stýrt útreikningar hljóðað á nægilegri hámarki virka efna og tengjutegunda umbrotsefna og leifa í jörð, grundvökjuvatni, vatnsfljótum og lofti skulu gert eftir notkun og með tilliti til fyrirhugaðrar eða fyrirhugaðra.

Candidate 4: Gilda má útbreyta tilgreiningu á því hvort tiltekinn efnisþyngd eldsneytisleysins og viðkomandi úthreinsunaraðferðir, í vatn, grunnvatn, yfirloftsefni og æði, eftir notkun sem kveðið er á um eða þó lögð á, og þeim sem hafa þegar verið.

Candidate 5: Rekstrarþoli skal rætt með tilteknum búnaði efnisfræðilega lyfjaefnisins og viðkomandi efni, útburða og í bæði jafngildi í jörð, grunnvatni, vatni og lofti, að lok af notkun sem er greind fyrir eða tiltekin hafa áður verið.

Candidate 6: Reiknu skal rétt við því hvað virka efnið og viðkomandi umburdæmigifni, leitunum og efni sem lagðar eru í grunnvökva, grunnvatn, vatn á yfirborði og lofti, meðan á notkuninni, eins og tilgreind er, stendur eða hafa þegar verið.

Candidate 7: Kríma má framkvæma viðmiðunarmat á hugsanlegum styrkum virka efna og meginfræðilegum umbrotsefni, mótefni og afleiðingar í jólum, grundvelli, grunnvatni, fjarviðvatni og andrúðum, að lokinni notkun sem er tilgreindur eða hefur saman.

</details>

<details><summary>final_semantic_review #157 · before · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:514

English: This star formation region is forming many stars.

Reference (shown after audit): Þetta stjörnumyndunarsvæði er að mynda margar stjörnur.

Review: No candidate preserves star-formation region forming many stars.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þessi stjarnaherli er upphafandi mikið fyrir stjörnur.

Candidate 1: Þetta stjarnafassirskrá eru í stökk við margar stjörnur.

Candidate 2: Þessi stjórnsýrumsetningarhópi er að forma margar stjórns.

Candidate 3: Þessi staðreyðirfraðistilum er staðreyndum hún svo margar stjörnur.

Candidate 4: Þennan stjórnunarhlið hefur gegn morgun verið stjórnuð með margum stjörnum.

Candidate 5: Þetta stiguppsælið varar mikið stjörn.

Candidate 6: Einnig eru morgunverulegar stjarnar við þetta starfshraður.

Candidate 7: Hér verður mikið um stjörnufæri.

</details>

<details><summary>final_semantic_review #158 · before · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:939

English: Put it in the envelope, Mrs. Rochon.

Reference (shown after audit): Settu hann í umslagið, frú Rochon.

Review: Envelope becomes papers.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Settu það í pappírunum, frú Rochon.

</details>

<details><summary>final_semantic_review #159 · before · G8 · technical_medium · P</summary>

Source ID: p13official21:test:eea:1354

English: Testing at low dosages may be performed by use of OECD 308 (August 2000) or an equivalent method.

Reference (shown after audit): Ef prófanir eru gerðar með litlum skömmtum má nota OECD 308 (frá ágúst 2000) eða jafngilda aðferð.

Review: Candidate3 retains low-dose testing by OECD308(August2000) or equivalent method.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [3]

Candidate 0: Gögninn á lágum skammtum má framkvæma með notkun á samræmdri aðferð sem tilheyrir OECD 308 (august 2000).

Candidate 1: Prófun á lágum skammtum má gerast með notkun OECD 308 (ári 2000) eða jafngildri aðferð.

Candidate 2: Prófun í lágri magni er hægt að gerast með notkun OECD 308 (á augnst 2000) eða sambærilegu aðferð.

Candidate 3: Próf á lágum skammtum má framkvæma með notkun OECD 308 (August 2000) eða sambærilegra aðferðar.

Candidate 4: Greiðslur með lágum skammta má gerð með þeim aðferðum sem er í samræmismál samkvæmt eftirlitsfélaga fyrir evrópu 308 (ári august 2000) eða jafngildri aðferð.

Candidate 5: Gildi má prófa í lágum skammtum með því að nota OECD 308 (ári 2000) eða jafngildri aðferð.

Candidate 6: Prófun í lágum skammtum má framkvæma með notkun OECD 308 (ári 2000) eða sambærilegri aðferð.

Candidate 7: Rannsóknir með lágum skammtum geta verið framkvæmd með notkun OECD 308 (árið 2000) eða jafngildri aðferð.

</details>

<details><summary>final_semantic_review #160 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:852

English: These actions may include comparison of the effectiveness of processes, methods and tools related to the chosen themes, mutual transfer and application of good practice, exchanges of personnel, joint development of products, processes, strategy and methodology, adaptation to different contexts of methods, tools and processes identified as good practice, and/or dissemination of results, profile-raising materials and events.

Reference (shown after audit): Aðgerðirnar geta falist í því að bera saman skilvirkni vinnsluferla, aðferða og tóla, sem tengjast þeim þemum sem eru valin, í gagnkvæmri miðlun og ástundun góðra starfsvenja, í starfsmannaskiptum, sameiginlegri þróun vara, vinnsluferla, skipulags og aðferðafræði, í því að aðlaga að ólíku samhengi aðferðir, tól og vinnsluferli, sem eru skilgreind sem góðar starfsvenjur, og/eða í útbreiðslu niðurstaðna og kynningarefnis og skipulagningu viðburða.

Review: All omit/corrupt several list elements, such as adaptation to contexts, personnel exchange and dissemination/profile raising.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þessir aðgerðir geti varjast samanþágu þeirra verkun, aðferða og aðferðir sem tengjast tilbúinum framlögum, hins vegar að sameiginlega greiða og beita góðu aðferð, skiptum í stjórn fólks, samvinnu í þróun af vörur, verkjum, áætlanum og tæknilegri aðferð, aðgerðir og aðferðir sem eru tilgreindar sem góða aðferð og/eða meðferð með áhrifum í vorum, greiningarprófi og tiltekin ástand.

Candidate 1: Síðast komi þessar störfir að líta saman á verkun, aðferðir og verkunarkerfissamfylki sem tiltækar eru framkvæmd, samanburð í vinnu og beitingu góðra aðferða, flestru samanburði af starfsmanna, sameiginlega þróun af framleiðslu, verkunum, áætlanum og aðferðum, samræmingi á sameiginlegum aðferðum, verkunarkerfisamfylki og verkunum sem tilgreind eru sem góða aðferð, og/seiða að útsetningi niðurstöðum, framleikasýni og segferðum.

Candidate 2: Þessi ráðstafanir gætu í tengslum við samanburð á verkunum, aðferðum og verkfæranir sem tengja þau vísanir sem valin eru, að því er varðar sama rekstur og beitingu góðra aðferða, samstillun manna, sameiginlega þróun vöru, meðferðar, stjórnunarhófs og aðferðar, aðferðirnir og verkfæranir sem teknum verið að góðu aðferði, og/eða útsendingu útgáfu, vöru, hagskýrslu og fars.

Candidate 3: Tilgangirnar geta í þessum ökutæki verið að tekið saman áhættureikning efnisskerfis, aðferða og kerfin, sem tengjast valinum umhverfi, hvort í gegnum það heim að þéla saman, að ná meðal með annað, að úthlutunum hagbærisgerða, að skipti með starfsmenn, að samhliða þróun afurða, ferðar og áætlunar, að nýta aðferðir og kerfin sem eru viðurkenndu hagbærargerð, og/eða þegar meðferður er farið fram, lífi í líf eða tilfiningar.

Candidate 4: Þessi aðgerðir geta náð með samanburði á skilun á verkun, aðferðum og vörslum sem tengjast valinum þætti, samræmingu af haglegum aðgerðum og beitingu þeirra, samfylkingu starfaðila, samvinnu á framleiðslu vöru, vörslu og áætlunar, samræmingu aðferða, vörslu og vörslu í aðskilinnum stöðvar í samræmingu í samræmi við haglega aðgerðir og vörslu sem hafa verið tilgreindar og/að samsvarandi mistöku á niðurstöðum, eðlisbælingarmálum og hækku.

Candidate 5: Þessi aðgerðir geta mengt í sameiginlegri þróun og notkun á líftækinum, meðalhæfingu aðgerða og aðferða sem tengjast valdina þjónustu, samanburði á aðgangi að aðstæðu og notkun á góðum aðferðum, aðgang að starfsmenn, sameiginlegri framleiðslu gerða, aðferða og aðferða sem tengjast með sér sérstaða, samhliða, aðferðun til að bjarga á skiptum gagnkvæma aðferðum og aðferðum sem tengjast tekið verði á góðum aðferðum, og/svo framboð þekkingara, handvaða og sérstöðu.

Candidate 6: Þessar aðgerðir gætu t.d. þessarar náð þess að meðhöndla sameiginlega samanburði vegna hvers þáttar og meðhöndla hlutverk, aðferðir og vörur sem vera í tengslum við þáttir sem valið eru, meðhöndlað samanburði og beitingu góðra aðferða, meðhöndlað saman starfsmenn, samhliða framsetningu vöru, starfsemi, áætlun og aðferð og aðrekja aðferðir, vörumeðferð og vinnuhæfðar aðferðir til að athugasemat er fenginn, að því er varðar aðgerðir og aðferðir sem eru tilgreind sem góðar aðferðir og því er varðar þróun á vísindum og umbótum.

Candidate 7: Þessi aðgerðir geta varðar samanburð við því hvenær verktækir, þjálfunarvæktir og vettvangir sem tilvísun er um tilvísunarkerfi, samantekt og notkun góðra starfsvenja, úttekt fólks, samhliða þætt og tækni, sameiginlega þróun í vöru, virkju, stefnu og vangaða, aðgerðir og vettvangir sem tilvísun er um góðu starfsvenja, aðferðir og vettvangir, aðgerðir sem aðraðast til mismunandi aðstæðu, hæfingu á meginfylgjum og ákvarðanir og hópum.

</details>

<details><summary>final_semantic_review #161 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:1144

English: Successful participation in interlaboratory studies that assess laboratory proficiency is the best way to prove the competence in specific analyses.

Reference (shown after audit): Árangursrík þátttaka í rannsóknum með öðrum rannsóknarstofum, þar sem frammistaða rannsóknarstofa er metin, er vænlegust til þess að staðfesta hæfni í sértækum efnagreiningum.

Review: Successful participation becomes recognition and analytical competence becomes efficiency.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Viðurkenning í samanburðum milli rannsóknarstofa sem meta hæfni rannsóknarstofa er besta aðferð til að sýna fram á skilvirkleika í sérstökri greiningu.

</details>

<details><summary>final_semantic_review #162 · after · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:1596

English: I stuffed it in my pocket.

Reference (shown after audit): Ég setti hana í vasann.

Review: Stuffing into a pocket becomes screwing into a watch/shift.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ég skrúfaði það í vaktina.

</details>

<details><summary>final_semantic_review #163 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:1610

English: The true extent of CNS penetration of lamivudine and its relationship with any clinical efficacy is unknown.

Reference (shown after audit): Í hve miklum mæli lamivúdín kemst raunverulega inn í miðtaugakerfið og samband þessa við klíníska verkun er ekki þekkt.

Review: None preserves CNS penetration/extent and relationship to clinical efficacy.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Löngu rými lyfinu í hlutfalli meðhöndluð á rannsóknarhrifum er óþekkt og tengd er ekki meðhöndluðu læknisviðkomandi verkun.

Candidate 1: Vart kenna er hvernig lamivudín hefur snertingu á hemlum og lifraríkis eða hvort það hafi nokkru áhrif á klíníska áhrif.

Candidate 2: Viðkun á fráhóður á innrykingu lamivudíns í mótefnalífi og hvernig hún tengist klínískri árangri er óþekkinn.

Candidate 3: Vélarlegur undirvikusviðbragð lámívúdínar á skemmtilegrum hlutum er óþekkt og láninn fyrir klínískar verkun er óþekkt.

Candidate 4: Tíðni, sem lamivudín færir í lifrarstjórn, og hvernig það tengist meðferðarvirkni, er ekki þekkt.

Candidate 5: Ráðstafanir hjá klínískri áhrifum lamivudíns og viðkomandi krafni í aðlaga er enn óþekkt.

Candidate 6: Verulegri háttum þess að lamívúdín haldi breytingum á neyðarsviðinu er engin skýring frá.

Candidate 7: Gjöf og samræmi lyfsins á krabbameinskrabbameinanna er óþekk.

</details>

<details><summary>final_semantic_review #164 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:850

English: When implementing this strand the Commission will in particular ensure consistency and complementarity with the activities conducted by other Commission services or by European agencies; in particular, the European Foundation for the Improvement of Living and Working Conditions and the Community RTD Framework programme and the European Centre for the Development of Vocational Training (Cedefop).

Reference (shown after audit): Við framkvæmd aðgerða í þessum flokki mun framkvæmdastjórnin sérstaklega sjá til þess að þær séu í samræmi við og komi til fyllingar starfsemi sem aðrar þjónustugreinar framkvæmdastjórnarinnar eða evrópskar stofnanir stýra, einkum Evrópustofnun um bætt lífskjör og starfsskilyrði, rammaáætlunbandalagsins um rannsóknir og tækniþróun og Evrópumiðstöð um þróun starfsmenntunar (CEDEFOP).

Review: All corrupt named institutions/programme and complementarity; living conditions often becomes liver conditions.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þegar framkvæmdastjórnin beitt þessum flokknum mun hún sérstaklega tryggja samræmi og aukabils við starfsemi annarra stofnana framkvæmdastjórnarinnar eða evrópsku stofnana; sérstaklega evrópska stofnuninni fyrir bætur á aðstoðar- og vinnuskilyrði og evrópsku stofnuninni fyrir inntöku og svæði um rannsóknir og þjálfun í sviði starfsfæranotkunar (Cedefop).

Candidate 1: Þegar framkvæmd þessa ísla kemur til stunda skal framkvæmdastjórnin sérstaklega tryggja samræmi og aðstoð sem notið er af starfsemi annarra þjónustu framkvæmdastjórnarinnar eða Evrópuþjónustuverkefna; sérstaklega Evrópuþjónustuáðeigandi stofnuninni vegna aðlögunar á viðskiptum á lifrar- og verkunarskilyrði, evrópskra rannsóknar- og þjálfnauðlögum (R&T-D) og evrópsku stofnun vegna þjálfunar á sviði rekjafræðilegrar hæfis (Cedefop).

Candidate 2: Þegar framkvæmdað er þetta slegið mun framkvæmdastjórnin sérstaklega tryggja samræmi og aðstoð með starfsemi annarra þjónustu framkvæmdastjórnarinnar eða Evrópuðra stofnana; sérstaklega evrópskeru stofnuninni til bæjar ástæðna um að uppruna og vinna á aðstæðum fyrir lifun og vinnu og Evrópukerfiðum um vöktun og uppbyggingu á tækifærslu og starfsmen (RTD) að því er varðar evrópska stofnuninni til framhalds að þjálfa (Cedefop).

Candidate 3: Þegar framkvæmdað er þetta markvegi mun framkvæmdastjórnin, einkum, tryggja samvirkni og auðmat með starfsemi annarra framkvæmda aðila framkvæmdastjórnarinnar eða evrópubóta; einkum með hjálp Evrópubandalsins fyrir aukningu á aðstæðum í atvikum og launirmiða ESB og Evrópulánastofnunarinnar fyrir þjálfun í starfsemi (Cedefop).

Candidate 4: Þegar framkvæmd þess fyrirhvarfs er gerð gerir framkvæmdastjórnin sérstaklega með íhaldanleið og aðstoðanleið við starfsemi annarra búðanna framkvæmdastjórnarinnar eða Evrópuþjónustufundanna; sérstaklega, Evrópu stofnuninni fyrir aukningu á lifun og vinnumiðlun og Evrópu rannsóknasviðið á rannsóknir á tæknifestum hætti (fyrir schnell herferð (Rafend) og Evrópu stofnuninni fyrir þjálfun og þjálfun hugbúnaðar (Cedefop)).

Candidate 5: Við framkvæmd þessara þærms skal framkvæmdastjórnin sérstaklega tryggja samræmi og aukin starfsemi yfirleitt í þeim stofnunum sem framkvæma starfsemi áframhaldandi framkvæmda- stjórnarinnar eða áframhaldandi ESB-stofnunum, einkum Evrópuríkimannastofnuninni fyrir aðlögun lífsmálayfirvalda og atvinnu- og skuldbindingabundinni rannsóknar- og fjármála- áætlun Sambandsins og Evrópasviðið fyrir þjálfun í hæfis (Cedefop).

Candidate 6: Þegar framkvæmd þessarar skipar gerist mun framkvæmdastjórnin sérstaklega tryggja sam síni og til æxlis með starfsemi annarra þjónustuveitana fram völdum framkvæmdastjórnarinnar eða Evrópuþjónustudeyminu; sérstaklega evrópska stofnuninni fyrir hæfi og sviði við að auka sjóði og vinnu ástand og aðila EES yfirráðasamfelti um rannsóknir á tækninum og vinnuskyldur (RTD) og evrópsku stofnuninni fyrir þjálfun í sviði vinnsluaðstæðna (Cedefop).

Candidate 7: Þegar framkvæmdastjórnin fari fram í þessum marki skal hún, sérstaklega, tryggja samræmi og viðbótarmeðferð við starfsemi annarra þjónustu framkvæmdastjórnarinnar eða Evrópubótagernjana; sérstaklega með evrópsku stofnuninni fyrir aðgerðir við bælingu á lifrar- og vinnumörkuðum skilyrðum og með evrópsku tveggja stofnun fyrir tækifæringar í sviði starfsemi (RTD) og evrópsku stofnun fyrir hæfni á launamarkaði (Cedefop).

</details>

<details><summary>final_semantic_review #165 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:881

English: Using standard candles - such as the variable stars within IC 1613 and the less-common Type Ia supernova explosions, which can seen across far greater cosmic distances - astronomers have pieced together a cosmic distance ladder, reaching deeper and deeper into space.

Reference (shown after audit): Með hjálp staðalkerta eins og breytistjörnunum í IC 1613 og sprengistjörnum af gerð Ia, sem sjást úr mikilli fjarlægð í geimnum, hafa stjörnufræðingar smíðað fjarlægðarstiga sem nær lengra og lengra út í geiminn.

Review: All corrupt standard candles, variable stars/TypeIa supernovae or cosmic-distance ladder.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Við notkun stöðugra bula - svo sem ótursvæði stjórnstjarna í IC-1613 og stjórnmálareikna Ia-afla, sem birtast yfir bunnu fyrir erfittum kosmískum sólarhringum - hefja starflagslegar aðferðir fyrir skyna um kosmísku þyngdarlega hreinlaga liggjandi stig í rafum.

Candidate 1: Að nota fyrirliggjandi stjarnar - s.s. stjarna í IC 1613 og stjarna sem eru algengari en stjarna af tegund Ia, sem þeir eru með fyrir sig og sem sérstaka eru í alvöru - hafa aðstandisfræðingar sérstakar þátttöku og tafarlaust til að sérstökast í gögn eftir numri.

Candidate 2: Til að nota viðkomandi aðföng, eins og breytulegar stjarnarnir í IC 1613 og lægri sú af alíðum, Ia, supenovakökunir sem séu fyrir sér á frekar lengri umferð í sviði kökuna, hafa aðferðarfræðingar hannað þunguð læknisstig í umferð, sem stengst í dýrarðri af umferði.

Candidate 3: Með því að nota stöðugar stjörnur, eins og hreyflinu í IC 1613 sem hreyfir neiðlega og lítilt frekari hreyfi stjórnsýnu Ia sem sétt er í ljós á mjög hári vatnsmyndum hefur látaustar hafi létast upp áhersli tilkynningum um gæði vatnsmyndanna, að því skipti að lægri og lægri í þungumyndin.

Candidate 4: Tilskipanir hafa notað staðlaðir stjörnuvarnir, svo sem stjörnunum í IC 1613 sem eru særuendurskilana og staurnir í smáhlagi sem eru mjög sjaldsvarir. Þær hafa kopnað eiginliðskynislið í göngunum, sem nýtjast aðri og aðri í úthugun.

Candidate 5: Hjá stöðugum orðnum, eins og hvitstuórarnir í IC 1613, og stökkaða fljótarefni af Ia-tökun, sem fyrirhugaðir eru miðað með, hafa aðraðarlegar aðferðafræðingar gert sérhæfða fjölgunarsöngu í farársprautana sem reyndar að sníða í fjarlægri röð með útstöðum til þess.

Candidate 6: Með staðlafurðum - s.s. þótt sem óhlutdedur stjarnarnar í IC 1613 og það lýkur í smittyföngum í Ia-tökum sem hafa verið sérhæfðra - hafa fjórðingaðar dýraflur og hittað út í með fjarlægri veruþyngdar.

Candidate 7: Notandi við staðlverkir, svo sem breytnar stjörnur í IC 1613 og ýmsu Ia-stjörnvöðulíkamar, sem eru háttast og unntar að sjái, eru ókunnar voru áhættuvistu svörunarlérð. Astrómenn hafa settar fyrirfram lérðina sem leiðir í okkur.

</details>

<details><summary>final_semantic_review #166 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:1524

English: In the case of bulk liquid products the lot or sublot shall be thoroughly mixed in so far as possible and in so far it does not affect the quality of the product, by either manual or mechanical means immediately prior to sampling.

Reference (shown after audit): Þegar um er að ræða fljótandi farm í lausu máli skal blanda framleiðslueininguna eða framleiðsluhlutann eins vandlega og unnt er, annaðhvort handvirkt eða vélvirkt, rétt áður en sýni er tekið.

Review: No candidate preserves bulk-liquid/manual-or-mechanical/thorough mixing and immediate-before-sampling constraint together.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Ef um er að ræða vökvafræðilega vörur skal lotinu eða undirlotinu að blanda þau vel og eftir það sem er mögulegt, að því tilskildu sem það hefur ekki áhrif á gæði vörunnar með beinum eða tæknilegum aðferðum áður en sýnatöku er gerð.

Candidate 1: Ef um er að ræða magnafæð blender hóðinu eða undirhóðunni í allt að fyrir hendi, þar sem það hefur ekki áhrif á gæði lyfsins, með beintilvirkjum eða með virkju, innan þeirra sér sem er, fyrir að sýna eðlilegt.

Candidate 2: Ef um er að ræða vatnsþætti skal lotur eða undirlotur mergið vel eftir því sem unnt er og það skalt ekki hafa áhrif á gæði vörunnar, með annaðhvort tæknilegri eða tæknilegri aðferð í tafarlaust fyrir vali sýnu.

Candidate 3: Fyrir vökvi öryggismerkjum fyrir vökva í umfjöllum skal lauseða blanda lot eða undirlot í hvorki dæmigerðum máli né með séslæknum taka til að það hafi ekki áhrif á gæðisvörv vörunnar, fyrir það sem getur að verja.

Candidate 4: Í örsýnum vökva tilgreiningar skal hitti í eðlilega fullkomlega hætti, að liðnum eða undirliðum, svo fremst sem unnt er og eftir það ekki skipti á gæði vörunnar, með annaðhvort manna eða tæknilegum hætti áður en sýnatæking er gerð.

Candidate 5: Ef um er að ræða ígrunalegar vörur skal blanda loti eða undirlotu í sérhverju hæfileikum sem unnt er og í sérhverju hæfileikum sem hún hefur málefni við gæði vörunnar, með beina eða tæknilegum aðstæðum, innan við sýnatök.

Candidate 6: Ef um er að ræða vökva í þynnu skal lotið eða undirlotið tekið fullt blandað með öllum fyrir sitt hæfilegum leyti sem einnig má er við og það gerir ekki nein áhrif á gæði lyfsins, með annaðhvort tæknilegum eða mannaþætti að lokum á forstöðu ísambendingar.

Candidate 7: Hjá þeim vörum sem eru lífverudreifingar skal lotur eða undirlotur lagað til að blanda vel upp, að því marki sem unnt er og á kosti fyrir gæðavinningu, með annaðhvort fyrirhæfilegum eða tæknilegum hátt, áður en sýna er gerð.

</details>

<details><summary>final_semantic_review #167 · after · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eso:714

English: By studying this effect it is possible to map out the places where gravity is strongest, and hence where the matter, including dark matter, resides.

Reference (shown after audit): Með því að rannsaka áhrifin er hægt að kortleggja hvar þyngdarkrafturinn er mestur og þar af leiðandi hvar efnið, þar á meðal hulduefnið, er.

Review: Strongest gravity becomes largest area; mapping relation corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Með þessari rannsókn er hægt að mynda út staðir þar sem svæðið er stærsti og því þar sem efnið, þar með talið dökk efni, er.

</details>

<details><summary>final_semantic_review #168 · after · greedy · technical_short · U</summary>

Source ID: p13official21:test:eso:825

English: The process of dust trapping is explained in an earlier release (eso1325).

Reference (shown after audit): Þetta ferli, þegar ryk festist, er útskýrt í eldri fréttatilkynningu (eso1325).

Review: Dust accumulation is approximately related to trapping, but powder/release terminology is not confidently correct.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Framkvæmdarferlið um uppsöfnun duftar er skýrt í fyrri útleiðingu (eso1325).

</details>

<details><summary>final_semantic_review #169 · before · G8 · technical_short · F</summary>

Source ID: p13official21:test:eea:1814

English: The producer must ensure that all wood originate from legal sources.

Reference (shown after audit): Framleiðandi skal tryggja að allur viður komi frá löglegum aðilum.

Review: Wood/legal-source/producer relation not all retained in any candidate;6 substitutes trees and corrupts producer.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Útgeilen skal tryggja að allt dýr úði úr löggiltum orsókum.

Candidate 1: Framleiðandinn skal tryggja að allt vökvi úrurðið hafi ákveðin vald.

Candidate 2: Lýfiserfandi verður að tryggja að allt tær vera af lögvarðaðrum fyrirkomulag.

Candidate 3: Útbúinn verður að tryggja að allt æxlir gangja úr lögvirðu.

Candidate 4: Framleiðandi verður að tryggja að öll tyllur hafa löglega komin af.

Candidate 5: Útgeyrifreyja verður að tryggja að allt eignur aukið í vökki frá löglegum aðstöðum.

Candidate 6: Uðlendin hefur verkið að tryggja að öll tré sé úr lögbærum framleiðsluheimildum.

Candidate 7: Framleiðandinn skal sjá til þess að allt eigni sé af löggiltum orðustöðum.

</details>

<details><summary>final_semantic_review #170 · after · greedy · technical_medium · P</summary>

Source ID: p13official21:test:ema:992

English: Animal studies have shown excretion of retagabine and/or its metabolites in breast milk.

Reference (shown after audit): Dýrarannsóknir hafa sýnt útskilnað retigabíns og/eða umbrotsefna þess í mjólk.

Review: Animal studies, excretion, drug/metabolites and breast milk all retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Dýrarannsóknir hafa sýnt fram á útskilnaður retagabíns og/eða umbrotsefna þess í brjóstamjólk.

</details>

<details><summary>final_semantic_review #171 · before · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:1878

English: That's not what Optimus would want.

Reference (shown after audit): Optimus hefði ekki viljað það.

Review: Exact source/hypothesis semantic reuse from card78: Negated claim about what Optimus would want retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Það er ekki það sem Optimus vildi.

</details>

<details><summary>final_semantic_review #172 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:80

English: But the new study using the VLT has found that much of the stars energy is being absorbed and scattered by dust clouds before it gets to Earth - it is actually more luminous than previously thought and among the brightest stars known.

Reference (shown after audit): Nýja rannsóknin með VLT hefur hins vegar sýnt fram á að rykský gleypa og dreifa stórum hluta orkunnar sem stjarnan gefur frá sér áður en hún berst til jarðar - hún er því í raun miklu bjartari en áður var talið og er meðal skærustu stjarna sem vitað er um.

Review: All corrupt absorption/scattering by dust or stellar luminosity inference; some make the star itself reachEarth.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: En ný rannsóknin sem notuð var VLT hefur fundið að margi áburts er fenguð og slembið af rykiklónu fyrir geimnum en áður var tekið með - geðs er enn á eða bjánlegri en ætluð og er meðal bjóðsastjarna sem vitað er um.

Candidate 1: En nýr rannsóknin með VLT hefur leitt í ljós að mjög fyrirvirkni stjarnanna koma úr fyrirvirkni rykskæðlanna áður en stjarnan fæst til Ørðis - það er í raun sveigja stjörnurnar lengur en áður var talið og það er einn af björtustu stjörnunum sem vitað er um.

Candidate 2: En þessan nýja rannsókn með VLT hefur fundið að mikið af orku stjarnaðs er gefið til útsunnar og sprengtedins af rykskýum fyrir áður en það nær jörðinni - sem hefur í raun víst mikla ljós en virðist áður þegar það var talið og við um björtustu stjarna sem vitað er um.

Candidate 3: En í nýju rannsókninni með VLT hefurðið fundið að mikill orku stjörnurnar er samtans meðferðu og dreifður af rykskúum fyrir ásamt jörð, sem er í raun leysi magar en voru einungis hugtakandi og er meðal bjartasta stjörnunum sem vitað er um.

Candidate 4: En ný rannsóknin með VLT hefur fundið að fyrirrosturinn er að vera upp og út í stjörnumyndun, á móti eru stjörnurinn sýnilegri en áður taldist og innan þeirra er einnig ljóslegri.

Candidate 5: En nýtt rannsókn með VLT hefur fundið að tilfelli um það að mikið af orku stjarnaðs er seyptur og skilgreitt út af rykskyni áður en hann kemur til Jörðar - það er í raun mikil Útlitari en áður var talin og í samanburðarlistinni.

Candidate 6: En nýtt rannsókn með VLT hefur fundið að mikið af orku stjarna er borist og dreifist út af rykkykju áður en stjarnan ná yfir til Jörðar - hún er í raun fyrrandi ljósriðar en til þess var talið og von sérstaklega ljóslegasti stjarnan sem það er þekkt.

Candidate 7: Nýtt rannsókn á VLT talið það að mikið af orku stjarna sé tekið til holtar og dreifinn af duftamóta fyrir áður en það kemur til Jörðar, - orkuð er það hjá stjörnum nánari en gegn áður vart var að rasa og það er aðeins eins bjart og það er þess jákvætt.

</details>

<details><summary>final_semantic_review #173 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:1751

English: On the basis of the common criteria, and in view of the fact that, to date, ICAO has not agreed to the closure of any of the findings raised during its audits, it is assessed that, at present, the competent authorities of Indonesia have failed to demonstrate that they have performed their regulatory and oversight responsibilities in compliance with ICAO standards with respect to all the carriers they certify.

Reference (shown after audit): Á grundvelli sameiginlegu viðmiðananna og í ljósi þess að enn sem komið er hefur Alþjóðaflugmálastofnunin ekki samþykkt lyktir neinna þeirra mála sem komu í ljós við úttektir hennar er það metið svo að eins og sakir standa hafi lögbær yfirvöld í Indónesíu ekki getað sýnt fram á að þau hafi gætt ábyrgðar sinnar á sviði reglusetningar og eftirlits í samræmi við staðla Alþjóðaflugmálastofnunarinnar með tilliti til allra flugrekenda sem þau votta.

Review: All corrupt country, closure-of-findings, regulatory/oversight duties or certified-carrier scope; correct Indonesia in7 does not fix remaining clauses.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Á grundvelli sameiginlegra viðmiðanna og miðað við það að ICAO hefur ekki þegar samþykkist gagnvart lokun af mörgum niðurstöðum sem upprunandi skoðanir hafa leitt fram, er greint að lögbæra yfirvöld Indíans hafi ekki komið fram á því að þau hafi lögð fram eftirlits- og regluminniverk fyrir sér í samræmi við staðla ICAO að því er varðar allir flutningsfélög sem þau staðfesta.

Candidate 1: Béðið ánægjandi viðmiðunum og með tilliti til þess að ICAO hefur ekki samþykkist skal ekki taka til greina, til þess að þeir hafa sýnt fram á að lögbær yfirvald í Indónesía hafi ekki sýnt fram að þeir hafi komið á fót reglum og eftirlitsþörfum sínum í samræmi við ICAO-rúmmál um allt flugum sem þau sannfæra.

Candidate 2: Á grundvelli sameiginlegra viðmiðanna og með tilliti til þess að ICAO hefur ekki samþykkist leyfis nema á einhverjum niðurstöðum sem stofnaði á með skoðunum, er gert útreikning á því að núverandi lögbæra yfirvöld Indóneisinni hafi ekki sýnt fram á að þau hafi fullnægt yfirmiðilum sínum um reglufyrirkomulag og eftirlit með öllum flutningameðallögum sem þau staðfesta.

Candidate 3: Á grundvelli sameiginlegra viðmiðana og í þeim tilviki að ICAO hefur ekki komið á samkomulagi um lokuð af niðurstöðum sem komu fram í endurskoðuninni, er talið að lögbæra yfirvöld Indíans hafi ekki snýið fram að þeir hafi uppfyllt ræðubærar og eftirlitsbærar skyldur sína í samræmi við stöður ICAO að því er varðar öll flutningafélög sem þau samþykkja.

Candidate 4: Af grundvelli sameiginlegra viðmiðana og með tilliti til þess að ICAO hefur ekki samþykkt fyrir hendi skoðunaraðgerðirnar í beinu um hvern af skynsöguðum niðurstöðum sem þeir voru að ræða, er ákvarðanir gerðar á því að gagnvart útgáfu ICAO hefur lögbær yfirvald í Indóleni ekki sýnt fram á að þau hafi uppfyllt ákvæði um skuldbindingar og eftirlit með flugmálum í samræmi við stöðu ICAO að teknu tilliti til öllum flugfélöganna sem þau staðfesta.

Candidate 5: Á grundvöllum sameiginlegra viðmiðana og með tilliti til þess að ICAO hefur ekki samþykkt að loka ákvarðanann sem upp komu í sannprófunins sína til auglá, er metin þýði lögbær yfirvöld í Indókanum hafa ekki sýnt fram á að þau hafi framfylgt ábyrgð sín með reglur og eftirliti í samræmi við stöðlu ICAO að því er varðar alla flutningsfélög sem þau sannreyna.

Candidate 6: Með tilliti til þess að ICAO hefur ekki samþykkist að loka neinu af niðurstöðunum sem hafa verið tekið fram í endurskoðun, er ákvarðað að, þegar í tímanum, hafi lögbær yfirvald í Indónenía ekki sýnt fram á að þau hafi stuðlað yfirvalda- og eftirlitsaldila sína í samræmi við verklagsstaðla ICAO við aðgerðir til allra flugfara sem þau sannfæra.

Candidate 7: Á grundvelli sameiginlegra viðmiðana og miðað við það að ICAO hafi ekki samþykktur að slökkva á neinum niðurstöðum sem koma fram í eftirliti sín með þá tilskildum aðstöðu, er matin liðin að lögbær yfirvöld Indónesíu hafi ekki sýnt fram á að þau hafi uppfyllt fulltrúa skuldbindingar sínar um reglulegu og eftirlits- mannkun í samræmi við stöðu ICAO að því er varðar öll flutningsfélög sem þau bindir undir.

</details>

<details><summary>final_semantic_review #174 · after · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:825

English: The process of dust trapping is explained in an earlier release (eso1325).

Reference (shown after audit): Þetta ferli, þegar ryk festist, er útskýrt í eldri fréttatilkynningu (eso1325).

Review: No candidate preserves dust trapping; closest2 says an unclear outing of dust.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Undirstuðuð er ferlið um ávestingslag og það er lýst í fyrri losun (eso1325).

Candidate 1: Í forföllum losunarinni er leiðbeinin greint fyrir (eso1325).

Candidate 2: Efnið við útingu ryksins er útskráð í fyrri útgáfu (eso1325).

Candidate 3: Neytisfer glösumstíðni er útskýrt í fyrri útvegð (eso1325).

Candidate 4: Verklagskeðjunin er skýrt í fyrri losun (eso1325).

Candidate 5: Hreyfanefndur þess sem dorunnir eru er útskýrt í fyrri útgáfu (eso1325).

Candidate 6: Fyrirmyndin um aðskilnað dagssvæða er gefin upp í fyrri losunarmynd (eso1325).

Candidate 7: Afurðin um skrúfaskipti er lýst í fyrri rannsóknum (eso1325).

</details>

<details><summary>final_semantic_review #175 · after · greedy · technical_short · F</summary>

Source ID: p13official21:test:eea:607

English: Years of career break in the current enterprise (optional).

Reference (shown after audit): Hve mörg ár hafa fallið úr í starfi hjá núverandi fyrirtæki (valkvætt).

Review: Career break becomes unrelated career changes.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ár af skipti í starfsáttamönnum í núverandi fyrirtæki (valfrjáls).

</details>

<details><summary>final_semantic_review #176 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:1190

English: In these cases it is therefore recommended that the Zonegran total dose should be rounded up or down to the nearest available dose that can be achieved with commercially available capsule strengths of Zonegran (25 mg, 50 mg and 100 mg).

Reference (shown after audit): Í slíkum tilfellum er því mælt með því að heildarskammturinn af Zonegran sé minnkaður eða stækkaður í næsta skammt sem hægt er að gefa með hylkjum af þeim styrkleika af Zonegran sem fáanleg eru (25 mg, 50 mg og 100 mg).

Review: All corrupt rounding/nearest available dose or commercially available capsule-strength requirement.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Í þeim tilfellum er því mælt með að heildarskammtur Zonegran sé snúin upp eða niður til næstum fyrirbærrar skammtsins sem er hægt að ná með skammtastyrku Zonegran innleiðisbúnaðar (25 mg, 50 mg og 100 mg).

Candidate 1: Í þessum tilfellum er því ráðlagt að kenna við að ná nálægri þéttni frá toölum af Zonegran í að minnsta kosti eða að hásta þann stærri nálægri þéttni sem getur náð með sárið fyrir handa capsúlum af Zonegran (25 mg, 50 mg og 100 mg).

Candidate 2: Í slíkum tilvikum er því mælt með að nýta allra talna skammta Zonegran sem er fáanlegt og reyna má með skammtokynnum af Zonegran sem eru fáanleg í markaðsleyfi (25 mg, 50 mg og 100 mg).

Candidate 3: Í þessum tilfellum er því mælt með að þann heildarlyfjagjöf sem gefast er með Zonegran sé kviðupanleg eða kviðinn niður, að nægri frá fyrirbæri lyfsstyrkurinu sem er að komast á með öflugum, aðgengi Zonegran (25 mg, 50 mg og 100 mg).

Candidate 4: Í slíkum tilvikum er því ráðlagt að enduruppið þéttni skammta með Zonegran, að lokinni nálægri skammti sem má ná með kílum styrk Zonegran (25 mg, 50 mg og 100 mg) sem eru fyrir handa markaðsleyfis.

Candidate 5: Í þessum tilvikum er því ráðlagt að hefja viðbótareinkennum af heildarskammtinum af Zonegran upp eða niður í næstu færanlega skammt sem er hægt að ná við af lyfjagigt fyrir skammta af Zonegran (25 mg, 50 mg og 100 mg).

Candidate 6: Í þessum tilfellum er því mælt með því að ná skuggaðan, nálægri skammti sem færi að ná með útsækjandi skammti úr kapslerum með virðingu til nálægri skammts af Zonegran (25 mg, 50 mg og 100 mg).

Candidate 7: Í þessum tilfellum er því ráðlagt að aðlaga umsóknina eða niðri í nálægri fyrirbæri skammtinum, sem hægt er að ná með vörnum af breytilegu fæðu (25 mg, 50 mg og 100 mg) sem eru fyrir handelsráð.

</details>

<details><summary>final_semantic_review #177 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eso:760

English: Extreme stars like the two components of VFTS 352, play a key role in the evolution of galaxies and are thought to be the main producers of elements such as oxygen.

Reference (shown after audit): Ofsafengnar stjörnur eins og í VFTS 352 leika lykilhlutverk í þróun vetrarbrauta og eru taldar meginuppspretta frumefna á borð við súrefni.

Review: Galaxy evolution and oxygen-production claim corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Háskillegar stjörnur eins og tvö hluta VFTS 352 spila mikilvægum þátt í frumunni galdranna og eru hugtakandi framleiðendur efnisins eins og ókólna.

</details>

<details><summary>final_semantic_review #178 · after · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:136

English: Member State shall recognize the documents of compliance and safety management certificates issued by, or on behalf of, the administrations of third countries if it is satisfied that they demonstrate compliance with the provisions of this Regulation.

Reference (shown after audit): Aðildarríki skal viðurkenna þau samræmingarskjöl og öryggisstjórnunarskírteini sem stjórnvöld í þriðju löndum, eða annar fyrir þeirra hönd, hefur gefið út ef það er sannfært um að með þeim sé farið að ákvæðum þessarar reglugerðar.

Review: Certificates and issuance/on-behalf-of relationship not preserved; directives substituted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Aðildarríki skal viðurkenna skjöl um samræmi við og öryggisstýringu sem tilskipanir eru af stjórnunum þriðju landa eða fyrir henni ef það er fullgengi að þeir sýni fram á samræmi við ákvæði þessarar reglugerðar.

</details>

<details><summary>final_semantic_review #179 · after · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:2209

English: Much has been made of the hostility between our countries.

Reference (shown after audit): Mikið hefur verið gert úr fjandskapnum milli ríkja okkar.

Review: Much being made of discord/hostility between our countries retained despite rough grammar.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Miklum hefur verið gerð af ósáttinu milli landa okkar.

</details>

<details><summary>final_semantic_review #180 · before · greedy · technical_short · F</summary>

Source ID: p13official21:test:ema:2124

English: If in doubt, talk to your doctor or pharmacist.

Reference (shown after audit): Ef þú ert í vafa, skaltu leita ráða hjá lækninum eða lyfjafræðingi.

Review: In doubt becomes having certainty, reversing the condition.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef þú hefur vissleika mátt tala við lækninn eða lyfjafræðingina.

</details>

<details><summary>final_semantic_review #181 · after · G8 · technical_long · U</summary>

Source ID: p13official21:test:eea:386

English: Purpose: to inform the management and staff of the facility of the reason for the test facility inspection or study audit that is about to take place, and to identify the facility areas, study(ies) selected for audit, documents and personnel likely to be involved.

Reference (shown after audit): Markmið: að tilkynna stjórn og starfsliði prófunarstöðvarinnar um ástæðuna fyrir því að skoða á prófunarstöðina eða gera úttekt á rannsóknum og nefna þá hluta prófunarstöðvarinnar, rannsókn(ir), skjöl og starfsmenn sem líklegt er að komi við sögu við skoðunina eða úttektina.

Review: Candidate2 retains many inspection-purpose elements but forthcoming audit/inspection syntax is unclear; cannot confirm complete procedural meaning.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Tilgangur: til að bæta með fyrirhugaðri fyrirumsar eða verkefni fyrir rannsóknir á sviði afurðasviðs, sem er aðstoðar- eða í náum til rannsóknar, og til að tilgreina svið afurðasviðs, sem verkefnið er afveldi fyrir rannsóknarna, skjálftir og starfsfólki sem líklegt er að taka þátt í rannsóknum.

Candidate 1: Markmið: til að tilkynna stjórnun og starfsfólki stöðvarinnar um ástæðu til að framkvæma eftirlit með notkun eftirlitsstöðvarar eða rannsóknar eftirlits og til að koma á áhrif stöðvarins, rannsóknar(annað) sem valnumurinn var settur, skjala og starfsfólki sem líklega verður að taka þátt í.

Candidate 2: Tilgangur: til að upplýsa stjórnun og starfsfólki viðkomandi stofunnar um ástæður prófunar á eða rannsókn á eða í nálsið aðgerð þar sem prófunarstofanum er skoðuð eða rannsakað, og til að greina svið stofunnar, rannsóknirnar sem valin eru til skoðunar, skjöl og starfsmenn sem líklegt er að sé í tali við sem stofuð er.

Candidate 3: Tilgangur: til að tilkynna framkvæmdarstjóra og starfsfólki viðkomandi stofnunar um ástæðan af eftirliti með prófunarstofu eða rannsóknarupptaka sem tekst er til, og til að sýna fram á svæði stofnunar, rannsóknir sem jafnað er á fyrir upptaka, skjöl og starfsmenn sem líklegt er að taka þátt í.

Candidate 4: Tilgangur: til að koma fram árað fyrir stjórnun og starfsfólki stofnunarinnar um ástæður til að framkvæma eftirlit með stofnunni eða rannsókn eftirlit með rannsóknum (rannsóknir) sem verða að koma fram og til að greina sér stofnisvettindir, útgáfu rannsókna (rannsókna) sem verða að valað, skjaldir og starfsfólki sem líklega verða að taka þátt í rannsókninni.

Candidate 5: Tilgangur: til að upplýsa stjórn- og starfsfólki í stofunni ástæðan fyrir athuganir á rannsóknarstaðnum eða rannsóknar í samhæfi sem er að komast fyrir og til að þýða svið í staðnum, rannsóknirnar sem valin eru fyrir athuganir, skjöl og starfsfólk sem gæti komið fyrir í athuganir.

Candidate 6: Tilgangur: til að upplýsa stjórnun og starfsmenn stöðvarinnar um sönnun í eftirlit með aðstæðum á prófunarstöðunum, stöðu eða rannsóknum, sem er að fara fram, til að tilgreina svæði stöðvarinnar, rannsókn eða rannsóknir sem verða til að vera í eftirlitinu, upplýsinga og starfsfólks sem líklega gerir mismunur í meðan á eftirlitið stendur.

Candidate 7: Tilgangur: til að upplýsa stjórnun og starfsfólk stöðuins um ástæðu eftirlits á rannsóknastöðnum eða rannsóknir á fyrirhugaði sem verður til að taka sér til, og til að kanna um sjálfkrafa stöðunnar, rannsóknir (raunir) sem velkomið eru til eftirlits, skjöl og starfsmenn sem líklega munu taka þátt í.

</details>

<details><summary>final_semantic_review #182 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:611

English: “With Mars losing that much water, the planet was very likely wet for a longer period of time than previously thought, suggesting the planet might have been habitable for longer,” said Michael Mumma, a senior scientist at Goddard and the second author on the paper.

Reference (shown after audit): „Þar sem Mars hefur glatað svo miklu vatni var reikistjarnan líklega blaut í lengri tíma en áður var talið, sem bendir til að Mars gæti hafa verið lífvænleg í lengri tíma,“ sagði Michael Mumma, vísindamaður við Goddard og annar höfundur greinarinnar.

Review: Habitable becomes intended/planned; the central inference is lost.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: „Þegar Mars missti svona mikið vatn var jörðin líklega vökvað lengur en áður hefur verið talið og það bendir til þess að hún hafi verið fyrirhuguð fyrir lengri tíma,“ sagði Michael Mumma, hæsta vísindamannur í Goddard og annar aðalhöfundur greinarinnar.

</details>

<details><summary>final_semantic_review #183 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:430

English: Keep the needle in your skin after the dose counter has returned to 0 and count slowly to 6.

Reference (shown after audit): Haltu nálinni í húðinni eftir að skammtateljarinn sýnir aftur 0 og teldu hægt upp að 6.

Review: No candidate preserves needle kept in skin after counter returns0 and slow counting6; some reverse slow to fast.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Geymið níðingunum á húð þitt eftir að töflunin hafi komið aftur að 0 og hættu á milljónu og tölfaður 6.

Candidate 1: Haltu nálinni á húð þín eftir að töluð er lifur öðrum og taka skammtum þig vel út í 6.

Candidate 2: Haltu nálin í húð við þeim skiptum sem rafþíðnirnafn endar í 0 og taka þá hratt í 6.

Candidate 3: Haldið níðurinn á húð í viðmiðun við skammtavirkjuna komin til 0 og talaðu slæmt út á 6.

Candidate 4: Haltu námið í húð þinni eftir að töflun þýðir 0 og hraðaðu þig að 6.

Candidate 5: Haltu nýlið vísi í húð þín eftir að skammtartúllurinn hefur komið til 0 og talaðu þá hlutum 6.

Candidate 6: Haltu nýljanum í húðinni eftir að skömmtunarmörkin hafi komið aftur saman og tölutöku að 6.

Candidate 7: Haldið stöðugt á meðni þegar töflu upphaflega er að 0 og tölfa þig af 0 til 6.

</details>

<details><summary>final_semantic_review #184 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:1138

English: “Terrestrial planets similar to our Earth are obvious targets for the search for life outside the Solar System, while comets are suspected to have played an important role in the appearance and development of life on our planet,” adds his colleague Emmanuël Jehin, who leads the cometary part of the project.

Reference (shown after audit): „Bergreikistjörnur sem líkjast jörðinni eru augljós skotmörk fyrir leitina að lífi utan sólkerfisins en halastjörnurnar eru taldar hafa leikið mikilvægt hlutverk í uppruna og þróun lífs á reikistjörnunni okkar“ bætir Emmanuël Jehin við en hann leiðir halastjörnuþátt verkefnisins.

Review: All corrupt terrestrial planets, comets and origin/development-of-life inference or attribution.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: „Terrosplanets sem líka eru við okkur á Jörðina eru greinilegar markmiði fyrir leikfega lif og áður um rafmjaðarflugum,“ sagði Emmannuel Jehin, aðilarinn hjá sér, sem stjórnar rafmjaðarflugum í verkefnið, „veitir stutt að þær hafi leitt verið til mikilvægs hlutleysins í fækkun og þróun lífs á Jörðinni.“

Candidate 1: „Já, viðum er neikvæðan áhuga að leitir til lífs eru mælt með sem áttur að leitir frá lífi á utan sólarkerfisins, en við erum búin til að bjóða til komna sér í ljós að þeir hafi verið mikilvægar fyrir birtustu og þróun lífs á Eristuverjum okkar.“ Emmanuël Jehin, samstarfsmaðurinn, er aðeins að segja að rýmurinn hefur baik áhrif á birtun og þróun lífs á Eristuverjum okkar.

Candidate 2: „Sýna fyrir er að jörðulykur, sem er svipuð út í Miðjan, séu aðeins markmiði í leitinni að lifi út um sólkerfinu en á sjálfu sér eru ekki tilfinnt að kettilunum séu hafa mikilvægar þátttöku í mælikerfinu á jörðinni okkar,“ sagði Emmanuël Jehin samfélagsið hans, sem fylgir hjá meðferðina með kettilum.

Candidate 3: „Jafnvægar jarðverur, og líkin, eru skýrðar markmið fyrir leit á lifi utan sólarbardar, en erfðaköstunum er gert vísbending um að þær hafi verið mikilvægar fyrir dýrum á jarðverönum okkar við uppjöfnun og þróun lífs,“ sagði samtímis Emmanuël Jehin, fylgjara hjá framkvæmdarmeðluninni, sem stjórnera aðferðarinnar um erfðaköstur.

Candidate 4: „Umbóðir til að leita lífs fyrir utan sólarveranda, en fyrirhuguð er að flóttir hafi haft mikilvægar þátt í sýnileginu og þróun lífs á Jörðinni,“ bætir Emmanuël Jehin samfélagið til að segja með um um flóttirnir sem skipuleggja sérstaklega þátt í umferð og þróun lífs á Jörðinni.

Candidate 5: „Tilundin af völdum er að hraðarjörðir, sem eru svipaðir áréttu heiminn okkar, séu tilbúnar til að leita á lifi utan sólarvettisins, en sást að kornir hafi hafa mikilvæg árangur á komunnann á sér stað við útbreitt og þróun lífis á heiminn okkar,“ bætir Emmanuël Jehin, samtaktanefndur hans, til þess.

Candidate 6: „Lokafrjálsir, er einnig í svæðinu, sem nemur fyrir svæðið við að leita lífs utan sólarverksins, en áfanga er gert ráð fyrir að reykisverkur hafi haft mikilvægar áhrif á það sem barfur á lífi á ökutísinu okkar,“ sagði Emmanuël Jehin, samstarfsmaður hans, sem stjórnar hópnum sem styrkir reykisverkina.

Candidate 7: „Hljóðandi markmiðið við leitina á líf til herjalds í reikistjörnunum er jörðin okkar, sem eru eins og verið getað og úr námi, en fyrirbærið er á að flátar hafi haft mikilvægar hætti á upprunum og þróun lífs á jörðinni,“ sagði Emmanuël Jehin, samstarfsmaður hans, sem stjórnar draparinnar.

</details>

<details><summary>final_semantic_review #185 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:ema:992

English: Animal studies have shown excretion of retagabine and/or its metabolites in breast milk.

Reference (shown after audit): Dýrarannsóknir hafa sýnt útskilnað retigabíns og/eða umbrotsefna þess í mjólk.

Review: Animal studies becomes veterinary competition and excretion is omitted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Dýralyfjakeppni hafa sýnt að retagabin og/eða umbrotsefni þess eru í brjóstamjólk.

</details>

<details><summary>final_semantic_review #186 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:1716

English: In addition, the competent authorities of Gabon provided evidence to the Commission of the adoption of a new civil aviation code in May 2008, of the development of specific operating regulations for airworthiness and operations, and informed that the decision to establish an independent civil aviation agency (ANAC) was taken and should be promulgated in July 2008.

Reference (shown after audit): Þar að auki létu lögbær yfirvöld í Gabon framkvæmdastjórninni í té sönnun þess efnis að samþykktar hefðu verið nýjar reglur um almenningsflug í maí 2008 og að í undirbúningi væru sérstakar rekstrarreglur um lofthæfi og rekstur og tilkynntu þau að ákvörðun hefði verið tekin um að koma á fót sjálfstæðri stofnun á sviði almenningsflugs (ANAC) sem vænst er að verði tilkynnt um í júlí 2008.

Review: Airworthiness becomes aviation knowledge; civil-aviation and promulgation relations also corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Einnig lagði lögbær yfirvöld í Gabón fram sannanir um samþykki fyrir framkvæmda- stjórnina um nýja flugregla fyrir ríkisflugina í maí 2008, um þróun sértækra rekstri reglur um flugþekkingu og rekstur og tilkynnti um það að ákvörðunin um að setja stofnun sem er óháð flugmálastofnunum (ANAC) var tekin og ber að framkvæma hana í júlí 2008.

</details>

<details><summary>final_semantic_review #187 · before · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:278

English: Centaurus A has therefore been observed with many different telescopes.

Reference (shown after audit): Vetrarbrautin hefur þess vegna verið viðfangsefni fjölmargra ólíkra sjónauka.

Review: Telescopes become drawing materials.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Því hefur Centaurus A verið horfbúin með margum mismunandi teiknarefnum.

</details>

<details><summary>final_semantic_review #188 · after · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:1073

English: Analysis of this spectrum indicated that its atmosphere is cloudy.

Reference (shown after audit): Greining á litrófinu sýnir að lofthjúpurinn er skýjaður.

Review: Spectrum becomes sequence and cloudy is not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Greining á þessari röð sýndi að lofthjúpurinn sé skúttur.

</details>

<details><summary>final_semantic_review #189 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eso:356

English: The nebula lies more than four hundred times further away than the famous star.

Reference (shown after audit): Þokan er þó meira en fjögur hundruð sinnum lengra í burtu en stjarnan fræga.

Review: No candidate preserves nebula >400times farther than famous star; numeric/object/comparison errors remain.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Haldar Þarfið of mikið fyrir frá kvenfræðilegu stjarnanum.

Candidate 1: Sökkunarnar eru fyrrkvæði móttökum stjórnu.

Candidate 2: Neimsliðurinn er mikið of langt fyrir auðan fyrsta stjarninnar.

Candidate 3: Nebulaðið er fjarlægt fjarlægt en fánevurast hvítastjarnan.

Candidate 4: Flugvögnuðin er frekari fjórhundrað tímann frá þeim vikumhjálmar gesti.

Candidate 5: Nebulaðið er ofnar en fjórhundrað tíu miðla langt frá þeim óttaðri stjarnanum.

Candidate 6: Nebulann er meira en fjörmilli fjórar fyrir hámarksstefnu stjarnanum.

Candidate 7: Hryðjallinn er meira en fjögur hundrað tíma færri áfram en upprtækkin stjarnan.

</details>

<details><summary>final_semantic_review #190 · after · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eso:710

English: The VST KiDS survey will allow astronomers to make precise measurements of dark matter, the structure of galaxy halos, and the evolution of galaxies and clusters.

Reference (shown after audit): Kortlagningin nefnist VST KIDS og gerir stjörnufræðingum kleift að mæla nákvæmlega staðsetningu hulduefnis, uppbyggingu vetrarbrautahjúpa og þróun vetrarbrauta og þyrpinga.

Review: All corrupt dark matter/halo structure or evolution/cluster measurement list.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: VST KiDS verndir sér með skilverskum mælingum á dökkum rafum, myndun um sertleyfi stjörnuvöldanna og skiptingu stjörnuvöxta og knotta.

Candidate 1: VST KiDS rannsóknin mun gera stjörnufræðingum kleift að gera nákvæmar mælingar á dýrkaríki, rými úr galdrarum og myndun þeirra og þróunar sjónbergja.

Candidate 2: VST KiDS rannsóknin hefur áhrif á rannsóknarstjórnar á nákvæmar mælingum á djöfulu, stökkbreytingu í hela vetrarbrauta og þróun vetrarbrauta og vetrarbrautahluta.

Candidate 3: VST KiDS rannsókninni er grunin til stærðfræðinga til að gera nákvæmar mælingar á dæmunni, stökkbreytingunni hringjum stjörnuverða og vörnunum stjörnuverða og fjölmagnsins.

Candidate 4: VST KiDS mælingarinn mun láta stjörnufræðingum gera nákvæmar mælingar á doku, myndun haldar gegna í vetrarbrautum og þróun vetrarbrauta og vetrarbrautahópa.

Candidate 5: VST KiDS rannsóknin tekur stærðfræðingum tæknilega getu að gera nákvæmar mælingar á duskaeði, myndun helu í vetrarbrautum og sjónbæruþroska vetrarbrautar og vetrarbrautaklúða.

Candidate 6: VST KiDS skoðunin gerir stjörnufræðingum kleift að gera nákvæmar mælingar á dökktu efni, structúrunni á kringum gegnum snotta hjá vetrarbrautum og sjónukerfi og þróun vetrarbrauta og býla.

Candidate 7: VST KiDS tæki verður stærðfræðingum að mæla nákvæmlega um dökk efni, bylgjuloki vetrarbrauta og þróun vetrarbrautta og hóptar.

</details>

<details><summary>final_semantic_review #191 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:918

English: "With such short orbital periods, the planets are between 20 and 100 times closer to their star than the Earth to the Sun. The structure of this planetary system is much more similar in scale to the system of Jupiters moons than to that of the Solar System," explains Michaël Gillon.

Reference (shown after audit): „Umferðartímarnir eru svo stuttir að reikistjörnurnar eru 20 til 100 sinnum nær móðurstjörnunni en Jörðin frá sólinni. Uppbygging þessa sólkerfis svipar því meira til Júpíters og tungla hans en sólkerfinu okkar,“ segir Michaël Gillon.

Review: Jupiter moons becomes planets; scale comparison is corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: „Með slæma umferðarfráhringum eru plönturnir í 20 til 100 sinnum nálægri fjarlægð frá stjörnunni en jörðin frá sólinni,“ segir Michaël Gillon. „Staðsetningur þessarar reikistjarna er mjög lítiltar sambærilegur við reikistjarnanir Júpíters en reikistjarnanir á sólkerfinu,“ segir Michaël Gillon.

</details>

<details><summary>final_semantic_review #192 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:2125

English: In addition, the sub-processing should only consist of the operations agreed in the contract between the data exporter and the data importer incorporating the standard contractual clauses provided for in this Decision and should not refer to different processing operations or purposes so that the purpose limitation principle set out by Directive 95/46/EC is respected.

Reference (shown after audit): Þá skal ráðstöfun til undirverktaka aðeins fela í sér þær aðgerðir sem samþykktar eru í samningnum milli gagnaútflytjanda og gagnainnflytjanda og sem inniheldur föstu samningsákvæðin sem kveðið er á um í þessari ákvörðun og þessi ráðstöfun skal ekki ná yfir annars konar gagnavinnslu eða hafa annan tilgang svo að meginreglan um takmörkun vegna tilgangs, sem sett er fram í tilskipun 95/46/EB, sé virt.

Review: All corrupt sub-processing and data-agent/contract/purpose-limitation conditions.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Auk þess skal undirlag þær skiptir þar sem samkvæmt samningunni um gagnagjafavakst er staðfestuð að gera og þar sem undirbúningar eiga að gera og samkvæmt þessum samningum, með því að gera undirlag þær samkvæmt staðfestuðum samningartákn sem kveðið er á um í þessari ákvörðun, að þær skiptar ekki í öðrum unntfreyrslustarf eða tilteknum tilgangi svo að því að setja viðeigandi reglur um takmarkanir á markmiðum í tilskipun 95/46/EB verði haldið.

Candidate 1: Auk þess skulu undirrekandi forsendu aðeins hafa samræmda starfsemi meðal hluta í samningnum milli gögnafæringsdeyja og gögnfréttaþáttans, þar sem viðkomandi samningsreglur er í gildi í þessari ákvörðun, og skal henni ekki viðkomandi annars rekstraraðgerðir eða þær aðstoðarverk, þannig að viðkomandi samkvæmtvörð, sem sett er fram í tilskipun 95/46/EB, skal beitt.

Candidate 2: Auk þess skulu aðra prófunarstofnanir einungis hafa þau starfsemi sem samdisvarðaðar voru í samningunni milli gögnfjáris og gögnfrumar, þar sem staðfest samningslögirnar, sem kveðið er á um í þessari ákvörðun, seiðu þær til og miklu ekki við annarri prófunarstofnun eða tilgang, svo að þessi reglur um takmarkanir á þekkingu heyra í því skyni að skv. tilskipun 95/46/EB.

Candidate 3: Auk þess skulu auðborðsreikningar einkenni aðeins þær starfsemi sem samþykkt er í samningnum milli gögnuríkja og gögnuríkjna, þar sem staðfestar samningsreglur, sem mælt er fyrir um í þessari ákvæði, eru viðurkenndar. Með því skal ekki trefa að öðrum hætti að rekstri einkenna eða því þegar hægt er að koma í tæki við að þjónustu er veitt að öðrum tilgangi eða við því að þjónustu er veitt í öðrum tilgangi og því skal takmarka markmiðið sem sett er fram í tilskipun 95/46/EB.

Candidate 4: Í aukningu skal verði undirhaldandi aðgerðirnar einungis þá aðgerðir sem samþykktar eru í samningunni um gagnaflutningu og gagnaflutningu og innflutningina, sem samræmt er við viðmiðunarmörkin í samningunni sem kveðið er á um í þessari ákvörðun, og þær skal ekki viðtaka annarri aðgerðir eða tilgangi, svo að regluna um að setja takmarkanir á markmiðum sé fengið.

Candidate 5: Auk þess skal samsvarandi upplýsingakerfið aðeins innifæra starfsemi sem samningin með útgefandi og innfjölda um gagnvirkni inniheldur viðmiðunarfrumur sem kveðið er á um í þessari ákvörðun. Því skal það ekki víxla yfir annað starfsemi eða ástæður sem því að tryggja heimilað að meðal er af því að þar til hennar er mælt með í 95/46/EB.

Candidate 6: Auk þess skulu þrífræðið skiptast að því að það sé eina aðgerðirnar sem samðerðin milli gagnaútfarandi og gagnaöfguðs er samþykkt og meðhöndlað samkvæmt viðurkenndum samningsreglum og séu ekki fyrir hendi annarri aðgerðir eða tilgangur í dreifingu þannig að þessi reglur í tilskipun 95/46/EB verði uppfylltar.

Candidate 7: Að auki skal hæfi varinn þannig að það sé að því er varðar þær starfsemi sem samningin með skrána sendandi og skrána innhaldi hefur samþykkt og skilgreindar staðallegar samningsreglur í þessari ákvörðun og skal í þeim ekki taka til annarra starfseininga eða þætta að því er varðar að það geri reglna um því að mæla má ekki að frá um öðrum markmiði eða meðferðarstarfsemi.

</details>

<details><summary>final_semantic_review #193 · after · G8 · technical_medium · P</summary>

Source ID: p13official21:test:eea:1509

English: Therefore, in the interest of clarity of legislation, it is appropriate to merge those provisions in one single legislative act.

Reference (shown after audit): Til að tryggja gagnsæi í löggjöf er því rétt að sameina þessi ákvæði í einni lagagerð.

Review: Candidate0 combines provisions in one legislative act for clarity of legislation; minor spelling/grammar.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [0]

Candidate 0: Því er rétt að samfleyta þessar ákvæði í einni laggjöf til að gera skýrleika á löggjöfina.

Candidate 1: Því er rétt að flagna þessi ákvæði í einn skipuð löggjaf.

Candidate 2: Því er rétt að samþykkja þá ákvæði í eina einsti löggjaf.

Candidate 3: Þar af leiðandi er rétt að gera saman þessar ákvæði í einni lag-gerð.

Candidate 4: Því er rétt að samfleytu þessum ákvæðum í einni sameiginlegu löggjöf.

Candidate 5: Því er rétt að samgöf þessara ákvæða í einni lagagjaldeyti til að býða til skýramiklunar.

Candidate 6: Því er rétt að eftirbyggja það í þeim ástandi sem gerir skýrleika löggjafar á eitt slegið löggjaf.

Candidate 7: Því eru rétt að samruna þessum ákvæðum í einni mengandi laggjöf til að gera lögunina auðveldara.

</details>

<details><summary>final_semantic_review #194 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:179

English: These violent explosions rip through the molecular gas clouds in their immediate surroundings, but after the shockwaves have travelled more than about ten light-years they are weaker, and may instead compress clouds that are a little further away, triggering the formation of new generations of stars.

Reference (shown after audit): Höggbylgjur þessara orkuríku sprenginga tæta sundur sameindagasskýin í kring en eftir að þær hafa ferðast meira en tíu ljósár eða svo, hafa þær veikst en geta þjappað fjarlægari skýjum saman og þannig hrundið af stað myndun nýrra kynslóða stjarna.

Review: Molecular gas clouds and compression of farther clouds triggering stars are corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þessi rauðar sprengingar skipta um milli líkamsgasvefnanna í nálægum umhverfi þeirra en eftir að skjálftan hefur farið meira en um tíu ljósára er þær vægar og geta þó styrkt það úr því að þeim verði það hægra veður og myndi þau koma upp í nýjar ævihóp stjarna.

</details>

<details><summary>final_semantic_review #195 · before · greedy · technical_short · F</summary>

Source ID: p13official21:test:eea:21

English: Soils used must, wherever possible, be freshly sampled.

Reference (shown after audit): Jarðvegssýni verða ætíð að vera nýtekin sé þess nokkur kostur.

Review: Fresh sampling becomes exposure.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þar sem notuð eru jörðir verður, hvenær sem mögulegt er, að útsetja þá fyrir sér.

</details>

<details><summary>final_semantic_review #196 · after · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:1317

English: General Barnicke's gone until tomorrow morning.

Reference (shown after audit): Barnicke kemur ekki fyrr en í fyrramálið.

Review: Absence until tomorrow morning replaced by going back.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Barnicke hefur farið til baka.

</details>

<details><summary>final_semantic_review #197 · after · G8 · technical_short · F</summary>

Source ID: p13official21:test:eea:1814

English: The producer must ensure that all wood originate from legal sources.

Reference (shown after audit): Framleiðandi skal tryggja að allur viður komi frá löglegum aðilum.

Review: No candidate retains wood from legal sources with producer obligation.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Framleiðandi skal tryggja að verður allir frá lögboðum.

Candidate 1: Framleiðandinn skal tryggja að allt vökvi úr skuldum.

Candidate 2: Vinnaraðilið þarf að tryggja að allt eystur vera úr lögboðum ásamt.

Candidate 3: framleiðandinn skal tryggja að allir stiga úr lögboðum.

Candidate 4: Framleiðandi verður að tryggja að öll stæði úr varð leyfðum.

Candidate 5: Varandahöfundur verður að tryggja að öll stærðbergur séu frá löglegum upprætingum.

Candidate 6: Umsækjandinn verður að tryggja að allt dyr er úr lögboðum.

Candidate 7: Framleiðandinn skal sjá til þess að allt skerthorni hafi orðið úr lögbeina upprunum.

</details>

<details><summary>final_semantic_review #198 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:ema:978

English: Similarly, the geometric mean AUC (CV%) values at Cycle 6 were higher among the subcutaneous group than the intravenous group; 4088 μg day/mL (34.2) versus 3630 μg day/mL (32.8) respectively) with a resulting adjusted geometric mean ratio [90% CI] of 1.10 [0.98-1.24].

Reference (shown after audit): Sömuleiðis var margfeldismeðaltal AUC (flatarmál undir þéttniferli) (fráviksstuðull) í meðferðarlotu 6 hærra hjá hópnum sem fékk MabThera undir húð en hjá hópnum sem fékk MabThera í æð; 4.088 μg dag/ml (34,2) borið saman við 3.630 μg dag/ml (32,8) respectively og leiðrétt hlutfall margfeldismeðaltala [90% öryggismörk] var því 1,10 [0,98-1,24].

Review: Adjusted geometric mean ratio is corrupted, despite most numeric values being copied.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Eins og áður var meðalgeðið AUC (CV%) gildi í 6. lotu hærri hjá undirhúða hópnum en hjá hópnum sem fengu inndælingu í bláæð; 4088 μg dag/ml (34,2) samanborið við 3630 μg dag/ml (32,8) í skiptum röðum, sem leiddi til að jafnframt með bilun á meðalgeðið [90% CI] 1,10 [0,98-1,24].

</details>

<details><summary>final_semantic_review #199 · after · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:3454

English: And I work for Danny.

Reference (shown after audit): Og ég vinn hjá Danny.

Review: And I work for Danny preserved.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Og ég vinn fyrir Danny.

</details>

<details><summary>final_semantic_review #200 · before · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:1198

English: The new observations are thus the first direct confirmation of such models.

Reference (shown after audit): Niðurstöður mælinganna eru þar af leiðandi fyrsta beina staðfestingin á útreikningunum.

Review: First direct confirmation of models is not retained in any candidate.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Nýja tilgreiningarnar eru því fyrsta beikingu í sér um þá líkam.

Candidate 1: Nýjar sýnin eru því fyrsta beinlegri bestu kannski fyrir þessa leynd.

Candidate 2: Nýjar upplýsingarnar eru það fyrsta leiðréttar staðfestingar vegna slíkrar leiðræðanna.

Candidate 3: Útgefnir niðurstöðurnar eru þannig fyrsta beðin viðbót við slíka líkani.

Candidate 4: Nýjar sýnirnar eru því fyrsta aðra beðan viðbót í ljósi slíkra líkana.

Candidate 5: Nýjar sérstökum upplýsingum eru því liðið nýjum staðfestingu um slíkar líkam.

Candidate 6: Nýja upplýsingarnar eru því fyrsta rannsóknarframboð um slíka líkanna.

Candidate 7: Nýja sýnir eru svo fyrstarðar framleiðsluferliðar í þessa tilteknum líkunum.

</details>

<details><summary>final_semantic_review #201 · after · G8 · technical_medium · P</summary>

Source ID: p13official21:test:eea:1354

English: Testing at low dosages may be performed by use of OECD 308 (August 2000) or an equivalent method.

Reference (shown after audit): Ef prófanir eru gerðar með litlum skömmtum má nota OECD 308 (frá ágúst 2000) eða jafngilda aðferð.

Review: Candidates2/6 retain low-dose testing, OECD308August2000 and equivalent-method alternative.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [2, 6]

Candidate 0: Gera má rannsókn á lágum skömmtum með tilvísun á OECD 308 (á august 2000) eða jafngildri aðferð.

Candidate 1: Gera má rannsóknir á litlum skömmtum með að nota OECD 308 (á augustus 2000) eða samsvarandi aðferð.

Candidate 2: Prófun í lágum skömmtum má framkvæma með nota OECD 308 (á augustus 2000) eða sambærilegri aðferð.

Candidate 3: Hægt er að nota OECD 308 (á augustus 2000) eða jafngildan aðferð til að mæla úr líkamsrannsóknum við lítinn skammtar.

Candidate 4: Gera má rannsóknir á lágum skömmtum með þeim aðferðum sem gerðar eru með OECD 308 (á augustus 2000) eða sambærilegri aðferð.

Candidate 5: Reyndar má prófa á lágum skömmtum með sérhæfðum aðferðum, sem samkvæmt OECD 308 (August 2000) eru komin í ljós eða samsvarandi aðferð.

Candidate 6: Prófun í lágum skömmtum má framkvæma með notkun OECD 308 (á august 2000) eða sambærilegrar aðferða.

Candidate 7: Rannsóknir á lítilum skömmtum má gerð með rannsóknarmskerfi OECD 308 (á augustus 2000) eða jafngildri.

</details>

<details><summary>final_semantic_review #202 · after · G8 · technical_medium · U</summary>

Source ID: p13official21:test:ema:1414

English: Invokana has no or negligible influence on the ability to drive, cycle, and use tools or machines.

Reference (shown after audit): Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, hjólreiða og notkunar tækja eða véla.

Review: Candidate6 has correct driving/tools/machines but cycling is an uncertain foreign loan; others change cycling or effects.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, vélræðna og notkunar vélj átta eða vél.

Candidate 1: Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, kringgjafar og notkunar tækja eða véla.

Candidate 2: Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, vélar og notkunar vélana eða véla.

Candidate 3: Invokana hefur engin áhrif eða óveruleg áhrif á hæfni til aksturs, byssu og notkunar verkja eða vél.

Candidate 4: Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, kringgöngu og notkunar tæki eða vél.

Candidate 5: Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, kíklans og notkunar vélka eða véla.

Candidate 6: Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, cíklings eða notkunar tækja eða véla.

Candidate 7: Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, ciklingu og notkunar vélaga eða véla.

</details>

<details><summary>final_semantic_review #203 · after · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:1831

English: However fibreboards classified as class A will be accepted if they do not represent more than 50 % of the total wood and wood-based materials used in the product.

Reference (shown after audit): Trefjaplötur sem flokkaðar eru sem E1 munu þó samþykktar ef þær eru ekki meira en 50% af samanlögðu innihaldi viðar og efna úr viði sem notuð eru í vöruna.

Review: Wood/materials become galaxies; fibreboards omitted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Hins vegar munu þeir sem eru flokkaðir sem A flokkur vera viðkomandi ef þeir eru ekki meira en 50% af heildarstærði vetrarbrauta og vetrarbrautafundna í vörunni.

</details>

<details><summary>final_semantic_review #204 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:1409

English: The port security assessment is the basis for the port security plan and its implementation.

Reference (shown after audit): Áhættumat fyrir höfn er undirstaða verndaráætlunar hafnar og framkvæmdar hennar.

Review: Assessment-as-basis of port-security plan not correctly expressed; updated port security is not a security assessment.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Portvæðaleika er grundvöl fyrir portvæðakvörðuninni og framkvæmd hennar.

Candidate 1: Portótursögnun náðar varðandi portótursáætlunina og framkvæmd hennar.

Candidate 2: Portverndasannstandard er grunur fyrir portverndaáætlunina og framkvæmd hennar.

Candidate 3: Væryttaárangurinn er grundvallur fyrir væryttaáætlunina og framkvæmd hennar.

Candidate 4: Væðlaus málstæði varðandi portvirkjafyrirsýslu er verndarmál fyrir portvarnaráætlun og beitingu þess.

Candidate 5: Portaðferðirmál um öryggismál í bænum er stofnun við umræddum meðferðaráætlunina á portiins og framkvæmd þeirra.

Candidate 6: Uppfærtur öryggi hafnarinnar er grunur á áætlun og framkvæmd öryggi hafnarinnar.

Candidate 7: Ráðning um vernd hafnanna telst eftirfarandi grundvöll fyrir hafnargoldaáætlunina og framkvæmd.

</details>

<details><summary>final_semantic_review #205 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:1414

English: Invokana has no or negligible influence on the ability to drive, cycle, and use tools or machines.

Reference (shown after audit): Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, hjólreiða og notkunar tækja eða véla.

Review: All corrupt drug effects, driving/cycling or tools/machines list.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Hjálpefnið hittur engan eða óverulegt áhrif á hagsmuni að veikja, kikka og nota vél eða vél.

Candidate 1: Útborðslega eða óhrifandi er útborðslega sem invokana þráðir.

Candidate 2: Invikanakemi hefur engan eða líkamlega málsleika á hæfni að keyra, hlaupa og nota verkfæra eða verkvara.

Candidate 3: Invokana hefur ekki áhrif eða skemmtileg áhrif á hæfni að keyra, kíkka og nota verk þjálf eða vél.

Candidate 4: Næmkað eða utan áhrif hráttu hans á hæfni til að fljúga, kyla og nota vél eða vél.

Candidate 5: Áhugavara æxla hafa ekki eða undantekinn áhrif á hæfni til að stofna, kæmu og nota hönd eða stjórn á tæki eða vél.

Candidate 6: Invokana hefur engin eða neikvæð áhrif á hæfni og hæfni leiðja, kælka og notkun vélja eða virkja.

Candidate 7: Áhrif uppleyska, fyrirframstöfun, erkona eða eldsneytis er óverulegt eða óskiljanleg.

</details>

<details><summary>final_semantic_review #206 · after · greedy · technical_short · P</summary>

Source ID: p13official21:test:ema:2175

English: Breast-feeding must be stopped on initiation of treatment with Voriconazole Accord.

Reference (shown after audit): Hætta verður brjóstagjöf þegar meðferð með Voriconazole Accord hefst.

Review: Breastfeeding must stop at treatment initiation retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Hætta verður brjóstagjöf við upphaf meðferðar með Voriconazole Accord.

</details>

<details><summary>final_semantic_review #207 · after · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:1086

English: Media representatives and other outreach groups will also be attending the event.

Reference (shown after audit): Fjölmiðlar og fræðsluhópar munu einnig sækja atburðinn.

Review: Media/outreach groups attending an event not intelligibly conveyed.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Tilskipendum fjölmi og öðrum hópum sem hafa áhersla til að taka til bæjar í sér verða einnig aðstoðar.

</details>

<details><summary>final_semantic_review #208 · before · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:2164

English: You didn't have the guts to do it yourself.

Reference (shown after audit): Þú hafðir ekki kjark til þess sjálfur.

Review: Lacking guts becomes not refusing, changing the assertion.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þú hefðir ekki hafnað til að gera það sjálfur.

</details>

<details><summary>final_semantic_review #209 · after · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:1144

English: Successful participation in interlaboratory studies that assess laboratory proficiency is the best way to prove the competence in specific analyses.

Reference (shown after audit): Árangursrík þátttaka í rannsóknum með öðrum rannsóknarstofum, þar sem frammistaða rannsóknarstofa er metin, er vænlegust til þess að staðfesta hæfni í sértækum efnagreiningum.

Review: No candidate retains successful interlaboratory proficiency participation; experience/precision/opportunity substitutes change the proposition.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Reynsla í rannsóknir á milli stofna, sem meta færni rannsóknaraðstæðna, er besta leiðinni til að sannfæra færni í tilteknum greiningum.

Candidate 1: Viðrekta þátttöku í rannsóknum milli rannsóknarstofa sem mati á nákvæmni rannsóknarstofa er besta leiðin til að sannfæra nákvæmni í sérstökum greiningum.

Candidate 2: Reynsla í samstarfsrannsóknum á rannsóknarkerfi sem meta nákvæmni rannsóknarstofu er besta leiðin til að sýna fram á nákvæmni í sérstakri greiningum.

Candidate 3: Fullnægjandi tækifæri í samstarf um rannsóknir á rannsóknarstofum, þar sem mat er breyttri staðfestu, er besta leiðin til að sýna fram á tengd reynslu.

Candidate 4: Við fullnægjandi þátttöku á samstarfi írannstu stofnunar sem meta stærðfræðilegum hæfni er besta ways til að sýna fram á hæfni í sérstakri greiningu.

Candidate 5: Aðlögun í samstarf sem mæli er mat yfir nytjalegu fyrirskiptum í rannsóknir á nytjalegu fyrirhæfni er besta leiðin til að sýna fram á færni í tilteknum greiningum.

Candidate 6: Reynsla í yfirvöldum rannsóknir, sem meta kröfur fyrir rannsóknarstjórnar, er besta leiðin til að sýna fram á menntun- kunninu í sérstökum greiningum.

Candidate 7: Reynsla við þátttöku í samstarfsrannsóknum á verkefni, þar sem nákvæmni í rannsóknastofum er metin, er besta leiðin til að sýna fram á náið í sérstökum greiningum.

</details>

<details><summary>final_semantic_review #210 · after · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:79

English: Justified estimates must be made of the expected concentrations of the active substance and relevant metabolites, degradation and reaction products, in soil, groundwater, surface water and air, following use as proposed or already occurring.

Reference (shown after audit): Rökstutt mat verður að koma fram á áætluðum styrk virka efnisins, og viðkomandi umbrots-, niðurbrots- og hvarfaefna, í jarðvegi, grunnvatni, yfirborðsvatni og lofti, eftir núverandi notkun eða ráðgerða notkun.

Review: All corrupt degradation/reaction products or soil/groundwater/surface-water/air compartments and justified-estimation scope.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Vottun skal gera grunngottar áætlanir um hliðstæðan þéttni virka efnisins og viðkomandi umbrotsefna, umbrotsefnaþekkingar og efni sem eru afleidd úr umbroti í jarðvökunni, grunnvatni, yfirborðsvökunni og lofthvöði, eftir notkun eins og mælt er fyrir um eða þegar það hefur verið að sé.

Candidate 1: Gera verður réttar áætlanir um búist við styrk virka efnisins og viðkomandi umbrotsefna, umbrotsefnafræðilegum afleiðingum og lyfjagöfum í jarðabúði, grundvökva, yfirborðawatni og lofthjóði eftir notkun sem mælt var fyrir um eða sem þegar eru til.

Candidate 2: Gera verður réttar mat á búistæðum þéttni virka efnisins og viðkomandi umbrotsefna og framleiðslu- og hlutverkafæra í jarðinu, grunnvatni, yfirlokvatni og loysi eftir notkun eins og pú er ráðið eða hafa orðið til.

Candidate 3: Gera skal réttar mataríki um hugsanlegu styrk virka efnisins og viðeigandi umbrotsefna, umbrotsefni og framleiðsluafurða í jarðverri, grundvöllvöru, vöðva, baksvöru, yfirborðsvöru og lofti, eftir notkun eins og mælt er fyrir um eða þegar það er gerð.

Candidate 4: Gera verður réttleggrekninga um búnaður og fyrirhuguðum styrk virka efnisins og áhrifalega umbrotsefnis og umbrotsefnifæri í jarðvatni, grunnvatni, yfirbólguvatni og lofthjóði, eftir notkun eins og mælt er fyrir um eða sem hefur þegar orðið.

Candidate 5: Gera skal réttan mat á viðfangseðlandi styrk virka efnisins og viðkomandi umbrotsefna, umbrotsefnisstofna ogafbrotu í jarðverri, grunnvatni, yfirborðsvatni og lofthvötu eftir notkun eins og hún hefur komið fyrir eða á bilinu.

Candidate 6: Sjálfkærar mat skal gera á virku efninu og viðkomandi umbrotsefnum og framleiðsluefnum í jarðvökju, grunnvatni, yfirborðsvökju og lofthjálp, eftir notkun eins og mælt er fyrir um eða þar sem það hefur orðið.

Candidate 7: Komi réttlætt mat á búist við á því að áætlaðir þéttni virka efnisins og viðkomandi umbrotsefnis, umbrotsefna- og framleiðsluefnis, í jarðvökva, jarðvatn, yfirborðsvökva og lofti eigi að fylgja, eftir notkun sem leið og til kynna kemur fram eða það er hafa orðið til komið.

</details>

<details><summary>final_semantic_review #211 · after · G8 · technical_short · P</summary>

Source ID: p13official21:test:ema:635

English: Table 4 provides dose modification guidance for dinutuximab, GM-CSF and IL-2.

Reference (shown after audit): Tafla 4 veitir leiðbeiningar um skammtaaðlögun dínútúxímabs, GM-CSF og IL-2.

Review: Candidates4/7 preserve Table4 providing dose-modification guidance for all three named treatments.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 7]; confirmed correct indices: [4, 7]

Candidate 0: Tafla 4 fylgir fyrirmælum um skammtaaðlögun fyrir dinútúximab, GM-CSF og IL-2.

Candidate 1: Í töflu 4 fyrirfylgja eru leiðbeiningar um skammtaaðlögun fyrir dinútúxímab, GM-CSF og IL-2.

Candidate 2: Í töflu 4 fyrirboði breytilegum skömmtum af dinutuximabi, GM-CSF og IL-2.

Candidate 3: Í töflu 4 er kveðið á um leiðbeiningar um skammtahönnun af dinutuximabi, GM-CSF og IL-2.

Candidate 4: Tafla 4 gefur leiðbeiningar um skammtaaðlögun fyrir dinutuximab, GM-CSF og IL-2.

Candidate 5: Í töflu 4 er gerð leiðbeiningar um skammtahöfnun fyrir dinutuxímab, GM-CSF og IL-2.

Candidate 7: Í töflu 4 er gefin leiðbeiningar um aðlögun skammta af dinutuximabi, GM-CSF og IL-2.

</details>

<details><summary>final_semantic_review #212 · after · greedy · technical_short · F</summary>

Source ID: p13official21:test:eea:21

English: Soils used must, wherever possible, be freshly sampled.

Reference (shown after audit): Jarðvegssýni verða ætíð að vera nýtekin sé þess nokkur kostur.

Review: Soil is rendered as suns; required object of fresh sampling corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Sólar sem notaðir verða, hvenær sem mögulegt er, að taka nýtt sýni úr.

</details>

<details><summary>final_semantic_review #213 · after · G8 · technical_medium · P</summary>

Source ID: p13official21:test:ema:382

English: In the controlled clinical studies in chronic ITP with eltrombopag, increases in serum alanine aminotransferase (ALT), aspartate aminotransferase (AST) and bilirubin were observed (see section 4.8).

Reference (shown after audit): Í klínískum samanburðarrannsóknum á eltrombópagi hjá ITP-sjúklingum kom fram hækkun á alanínamínótransferasa (ALAT), aspartatamínótransferasa (ASAT) og bílírúbíní í sermi (sjá kafla 4.8).

Review: Candidates0/7 preserve controlled chronicITP studies with eltrombopag and increased serum ALT/AST/bilirubin plus section4.8.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [0, 7]

Candidate 0: Í klínískum, samanburðarrannsóknum á langvinnri ITP með eltrombópagi komu fram aukningu á alanínamínótransferasa í sermi (ALT), aspartatamínótransferasa í sermi (AST) og bilirubin (sjá kafla 4.8).

Candidate 1: Í klínískum, samanburðarrannsóknum á langvinnt blóðfall með eltrombópagi höfðu orðið til aukningu á alanínamínótransferasi (ALT), aspartatamínótransferasi (AST) og bilirúbíni í sermi (sjá kafla 4.8).

Candidate 2: Í klínískum samanburðarrannsóknum á langvarandi ITP með eltrombópagi komu fram hækkun á alanín aminótrentrasíði (ALT), aspartat aminótrentrasíði (AST) og bilirúbíni (sjá kafla 4.8).

Candidate 3: Í klínískum samanburðarrannsóknum á langvinna blóðflæðisbólgu með eltrombópagi komu fram hækkaðir gildi alaninamínótransferasa í sermi (ALT), aspartatamínótransferasa (AST) og bilirúbíns (sjá kafla 4.8).

Candidate 4: Í klínískum samanburðarrannsóknum á langvinnri ITP með eltrombópagi komu fram aukningu á alanínamínótransferasa (ALT), aspartatamínótransferasa (AST) og blóðrúrubíni í sermi (sjá kafla 4.8).

Candidate 5: Í klínískum samanburðarrannsóknum á langvinnum blóðflæðismyndun (chronic ITP) með eltrombópagi komu fram aukningu á alanín amínótransfereiníði (ALT), aspartat amínótransfereiníði (AST) og bilirúbíni í sermi (sjá kafla 4.8).

Candidate 6: Í klínískum samanburðarrannsóknum á langvarandi æðasjúkdómi, sem meðferð var stundað með eltrombópagi, komu fram hækkanir á alanín amínótransferasi í sermi (ALT), aspartat amínótransferasi (AST) og bilirubini (sjá kafla 4.8).

Candidate 7: Í klínískum samanburðarrannsóknum á langvinnri ITP með eltrombópagi kom fram aukning á alanínamínótransferasa í sermi (ALT), aspartatamínótransferasa (AST) og bilirubíni (sjá kafla 4.8).

</details>

<details><summary>final_semantic_review #214 · before · greedy · technical_short · F</summary>

Source ID: p13official21:test:eea:607

English: Years of career break in the current enterprise (optional).

Reference (shown after audit): Hve mörg ár hafa fallið úr í starfi hjá núverandi fyrirtæki (valkvætt).

Review: Career break becomes an unrelated jump-work expression.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ár af stökkvinni í núverandi fyrirtæki (valinlegt).

</details>

<details><summary>final_semantic_review #215 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:409

English: Purpose: to determine whether the test facility, if engaged in studies using animals or other biological test systems, has support facilities and conditions for their care, housing and containment, adequate to prevent stress and other problems which could affect the test system and hence the quality of data.

Reference (shown after audit): Markmið: að ákvarða hvort prófunarstöðin, ef þar eru stundaðar rannsóknir með dýr eða önnur líffræðileg prófunarkerfi, hefur yfir að ráða búnaði og aðstöðu þar sem hægt er að hirða um þau, koma þeim fyrir og einangra þau á annan viðeigandi hátt þannig að koma megi í veg fyrir streitu og önnur vandamál sem gætu haft áhrif á prófunarkerfið og þar af leiðandi á gæði gagnanna.

Review: All corrupt animal/biological-system care, housing, containment or stress-prevention requirements.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Aim: til að geta ákveðið hvort prófunarsviðin, ef það er meðtakandi á rannsóknir með dýrum eða annarra lífverulegar prófunarkerfja, hafi ábyrgðarviðmiðunarsvið og skilyrði til að tryggja ráðstafanir, háður og sjúklingarmun til, að því er varðar að æskileika og öðrum vandamálum sem gætu íhlutar rekstrarkerfisins og því að gæti verið hættuleg viðgöngu reknislega.

Candidate 1: Að því er varðar: að ákvarða hvort prófunarkerfið, ef það er í sérhæfðum rannsóknum með dýrum eða annarri lífverulegan prófunaraðferð, hafi fylgtfjárhæð og skilyrði til að viðhalda þau, eftirhugað til að koma í veg fyrir ástværingu og aðrar máli sem geta haft áhrif á prófunaraðferðina og þannig á gæði gagnanna.

Candidate 2: Tilgangur: til að ákvarða hvort prófunarkviðburði, ef það er að ræða með rannsóknir með dýrum eða annarri lífverulegs prófunarkerfum, hafi aðann starfsvæði og skilyrði til að fá aðstoð vegna viðbrögðar og háðar meðferðar, nákvæmar til þess að koma í veg fyrir stungustörf og öðrum vandamálum sem geta hafa áhrif á prófunakerfinu og þessu til að gera tillögur á gæði gagna.

Candidate 3: Aim: að ákvarða hvort prófunarkerfi, hvort það er með þvagaðar meðan það er í rannsóknir með dýrum eða öðrum lífverulegan prófunaraðferð, sé með tilhögunarviðmiðanir og skilyrði til hins vegar að hafa og beita meðhöndla og því að fella við hendi og taka að lokuð því að þau skipti í veksli og að öðrum málsmeðferðum sem geta ákveðið áhrif á prófunaraðferðina og þannig á gæði gagnanna.

Candidate 4: Markmiðið: að ákvarða hvort prófunaráætlun í prófunarmiðstöðum, ef hún er að ræða prófanir með dýrum eða annarri lífverulegu prófunarstöðum, er með aðstoðarstöðum og skilyrðum til að bæta aðstoð, hleðslu og fersking á því og það er nauðsynleg til að koma í veg fyrir þjóðþreyti og önnur vandamál sem geti haft áhrif á prófunarstöðuna og þannig á gæði gagna.

Candidate 5: Markmiðið: að ákvarða hvort rannsóknarstofan, ef hún er í rannsóknir með dýrum eða aðrar líffræðilegar prófunarkerfum, hafi ráðstafanir og skilyrði til að hafa ábyrgð á hana, með hliðsjón af því að hún sé í skilvirkum ástandum, svo að velti út á áskrefi og öðru vandamálum sem gætu haft áhrif á prófunarkerfið og þannig gætu áhrif á gæðu gagna.

Candidate 6: Markmiðið: til að ákvarða hvort prófunarstöðvenna, ef þær eru með þátttöku sem nota lifrar eða ólík lífverulegan prófunarkerfum, hafi áætlana og skilyrði til að fylgi að hlutaðeigandi prófunarkerfi og er varða þeim, í því skyni að þeim sé unnt að koma í veg fyrir ónæmiskvyrðing og einhverri vandamál sem gæti haft áhrif á prófunarkerfið og því gæði niðurstöðu.

Candidate 7: Aðstoðvald og skilyrði með því að því marki að tilkynnt sé um rannsóknir með dýrum eða aðra lífverulegan prófunaferli farið á með sér, skal tilgreina hvort prófunarfjöðurin að vera aðstoðvaldi og skilyrði til að hjálpa með reynslu, ökutæki og fylgni, með því að þær hafi nægilega félags til að koma í veg fyrir vopnun og aðra vandamál sem gætu haft áhrif á prófunafyrirtækið og þannig á gæði gagna.

</details>

<details><summary>final_semantic_review #216 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:179

English: These violent explosions rip through the molecular gas clouds in their immediate surroundings, but after the shockwaves have travelled more than about ten light-years they are weaker, and may instead compress clouds that are a little further away, triggering the formation of new generations of stars.

Reference (shown after audit): Höggbylgjur þessara orkuríku sprenginga tæta sundur sameindagasskýin í kring en eftir að þær hafa ferðast meira en tíu ljósár eða svo, hafa þær veikst en geta þjappað fjarlægari skýjum saman og þannig hrundið af stað myndun nýrra kynslóða stjarna.

Review: All corrupt explosions, molecular clouds, shockwave distance/weakening or triggered star formation.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þessi sprautunir ristir hringtum í líkmyndandi losa og eru stærri en eftir að volupurnar hafa hreinsið sér lengur en ljósgreiðslu í tíu ljósgreiðsluleni eru þær líklega öllu þessu lægri og geta þó í staðið stökkbólgið það sem er næstum færri og því útskiptir nýjar frálendir stjórnað.

Candidate 1: Þessi veiki sviðarrennur gripi í rafíauhljóðið sem liggur í nálægt umhverfi þeirra, en meðan úrdjölen reiðaði fið innan og munnandi um ljóslið í meira en tíu ljósriði er þau þrýstir en þó gætu þeir konar slottir, sem eru stjórnaðrar, og hættu þannig á nýjum saga stjórnsýns.

Candidate 2: Þessi voklareisir safna í fyrirliggjandi umhverfi og hægir í snertugjöld þeirra en þegar áflæðið hafði farið lengur en um tíu ljósgeymi er þau væga og gæta því að þeir verði lausnir á sjálfri umhverfi sem er nægjandi, og þeir orðaðu nýju fráningu stjórna.

Candidate 3: Þessi verklæði rypa sig í lífveru, sem er í náttúrunarumhverfiði í náttúrunum, en eftir að bráðauslóð hausuðu frá því hvarf meira en um tíu ljósgangar eru þau smitlagar, og geta þau stökk og lífveru sem er lítið frekari fara úr, og því býr til nýju frumur stjarnanna.

Candidate 4: Þessir sára vantrákuna hreyfiðu um teymið og lítila útvarpi eftir, en eftir að þeir hreyfðu merki en nóg um tít ættar þeir að verka vægari og gæja útvaldum sem eru fyrir um um um, þannig að þeir stöðva útvarpum sem eru fyrir um, þ.e. þeir drapast nýtt generaða hvítra stjórna.

Candidate 5: Þessar rauðu fyrirskipti rífa um miðalafþurrkunina, en ef skömmugjarnir hafa farið um fyrir hogtum félögum er þær líklega værar ætti en geta fyrir að drapa leið og öðru dýru sem er mjög frekari og stóð til að auka nýju stungustungum stjórna.

Candidate 6: Þessir alvarlegar losun eru áfram í einungis mótvega kvikvatnslytta í þá smíðandi umhverfi, en eftir að losunarmýnkunum hefur farið meira en nánast tíu ljósstigorða er þeir þreyttar og geta snjallað lytta í neikvæðum umhverfi sem eru bara nægilega vefri, og því laga þau nýjum æðir á nýjar stjarnanir.

Candidate 7: Við þessar háheppublýnir skjúkar hettugásins í íbúðarhópum og eyk við því að þau séu stærri eftir að óhömmluflæðið hefur reitð yfir við um tíu ljósgangir en þeim hugsanlega hækkur og því getur þeir tilvikað hópa í nærri því aðild að komast úr nýrri rökstöðvum og því er hægt að leggja úr nýrum dauðrétta stjarna.

</details>

<details><summary>final_semantic_review #217 · before · G8 · technical_short · U</summary>

Source ID: p13official21:test:ema:1918

English: The presented safety information is derived principally from paediatric patients.

Reference (shown after audit): Fyrirliggjandi öryggisupplýsingar eru einkum til komnar út frá börnum.

Review: Candidate2 approximates safety information mainly from children but principal derivation/patient wording is not confidently grammatical; no confirmed full translation.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Varanaleiðbeiningarnar sem lögð eru fram er gruninlegt frá sjúklingum sjúkdómsleyskra.

Candidate 1: Tilgreins öryggisupplýsingar eru lítilst þannig myndar af sjúklingum með lækkum alifæð.

Candidate 2: Fyrirliggjandi öryggisupplýsingar eru eigandi í algengu ræði frá hjá börnum.

Candidate 3: Ráðstafanir um öryggi, sem liggja fram, eru í yfirleitt frá sjúklingum með þágerð.

Candidate 4: Umskýrt öryggiskennum er aðallega fengin úr kröfu hjá börnum.

Candidate 5: Sjálfkostlegar öryggisupplýsingar eru grunlæga úr sjúklingum þátttakum.

Candidate 6: Tilgreindar öryggishæfðnemaður sé fráhlífisverkanir hjá krabbameinum.

Candidate 7: Tilgreindar öryggisupplýsingar eru beint frá sjúklingum þrírásdeildar.

</details>

<details><summary>final_semantic_review #218 · after · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:2090

English: Member States shall require the competent authorities to monitor compliance with this Regulation effectively and take all necessary measures to ensure such compliance.

Reference (shown after audit): Aðildarríki skulu skylda lögbær yfirvöld til að hafa eftirlit með því að farið sé með virkum hætti eftir þessari reglugerð og gera allar nauðsynlegar ráðstafanir til að tryggja að farið sé að ákvæðum hennar.

Review: Member-State requirement for competent authorities to monitor compliance becomes participants following regulation; monitoring relation missing.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Aðildarríkin skulu kveða á um það í þátttakendur lögbæra yfirvalda til að fylgja með skilvirkum hætti reglugerðinni og gera allar nauðsynlegar ráðstafanir til að tryggja það.

</details>

<details><summary>final_semantic_review #219 · after · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:1144

English: Successful participation in interlaboratory studies that assess laboratory proficiency is the best way to prove the competence in specific analyses.

Reference (shown after audit): Árangursrík þátttaka í rannsóknum með öðrum rannsóknarstofum, þar sem frammistaða rannsóknarstofa er metin, er vænlegust til þess að staðfesta hæfni í sértækum efnagreiningum.

Review: Successful interlaboratory participation becomes experience; laboratory-proficiency relation corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Reynsla í samstarfsrannsóknum á rannsóknarþjálfun sem meta þjálfa rannsóknarstofa er besta leiðin til að sýna fram á færni í sérstökum greiningum.

</details>

<details><summary>final_semantic_review #220 · before · greedy · technical_short · F</summary>

Source ID: p13official21:test:eea:1471

English: Prices including all taxes, levies and VAT.

Reference (shown after audit): Verð með öllum sköttum, álögðum gjöldum og VSK.

Review: Levies and VAT not retained in the tax list.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Verð sem tölur innlendum skatta og skattatöflu og viðskiptavirkjuskatta.

</details>

<details><summary>final_semantic_review #221 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:1557

English: The Commission Communication ‘i2010 - A European Information Society for growth and employment (COM(), developing the Lisbon strategy, seeks to ensure coherence across the Commission's information society and media policies in order to reinforce the significant contribution of information and communication technologies to the performance of the economies of Member States.

Reference (shown after audit): Í orðsendingu framkvæmdastjórnarinnar „i2010 – upplýsingasamfélagið í Evrópu í þágu hagvaxtar og atvinnu“(COM (), þar sem Lissabon-áætlunin er útfærð, er leitast við að tryggja samræmi innan stefnu framkvæmdarstjórnarinnar um upplýsingasamfélagið og fjölmiðla í því skyni að styrkja mikilvægt framlag upplýsinga- og samskiptatækni til efnahagslegrar afkomu aðildarríkjanna.

Review: Invented COM identifier and corrupted Lisbon/policy/ICT-economic relations.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Í orðsendingu framkvæmdastjórnarinnar „i2010 – Evrópska upplýsingahópi til vaxtar og launþátta (COM(2009) 478, þjálfun í lögum um stefnumarkmið í Lissabon, er aðstoða að tryggja samhliða meðferð í ramma- og fjarskiptalögunum framkvæmdastjórnarinnar til að veita verulega þátttöku upplýsingakerfa og fjarskipta- kerfa í hagstöðum aðildarríkjanna.

</details>

<details><summary>final_semantic_review #222 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:1716

English: In addition, the competent authorities of Gabon provided evidence to the Commission of the adoption of a new civil aviation code in May 2008, of the development of specific operating regulations for airworthiness and operations, and informed that the decision to establish an independent civil aviation agency (ANAC) was taken and should be promulgated in July 2008.

Reference (shown after audit): Þar að auki létu lögbær yfirvöld í Gabon framkvæmdastjórninni í té sönnun þess efnis að samþykktar hefðu verið nýjar reglur um almenningsflug í maí 2008 og að í undirbúningi væru sérstakar rekstrarreglur um lofthæfi og rekstur og tilkynntu þau að ákvörðun hefði verið tekin um að koma á fót sjálfstæðri stofnun á sviði almenningsflugs (ANAC) sem vænst er að verði tilkynnt um í júlí 2008.

Review: Airworthiness term and independent-agency decision relationship corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Að auki voru lögbær yfirvöld í Gabón að sýna framkvæmdastjórninni fram á því að nýtt flugreglurháskil hafi verið samþykkt í maí 2008, um þróun sértækra rekstraraðferðir vegna flugþéttar og rekstrar og tilkynnti að ákvörðunin um að stofnun viðkomandi flugrekstur (ANAC) var tekin og ætlað að gera hana óháða og birta hana í júlí 2008.

</details>

<details><summary>final_semantic_review #223 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:512

English: Another team member, Ana Duarte Cabral from the Laboratoire d'Astrophysique de Bordeaux, France, emphasises that "the ALMA observations reveal the spectacular details of the motions of the filamentary network of dust and gas, and show that a huge amount of gas is flowing into a central compact region".

Reference (shown after audit): Annar meðlimur í rannsóknarhópnum, Ana Duarte Cabral við Laboratoire dAstrophysique de Bordeaux í Frakklandi, undirstrikar að „mælingar ALMA leiða í ljós stórkostleg smáatriði í hreyfingu gas- og rykslæðanna og sýna að geysimikið magn af gasi streymir inn að þéttasta svæðinu í miðjunni.“.

Review: Gas becomes radiation and filament motions/compact region are corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Aðra starfsfólkið, Ana Duarte Cabral frá Laboratoire d'Astrophysique de Bordeaux í Frakklandi, virðir því að „viðmiðanir úr ALMA-venjunum eru ótrúlegar og sýna fram áherslulegu hlutverk á flugnetið sem er í stöðuður netið af stofnun og geisli og sýna fram að mikla magn geisls sé í fljóttu í miðaðri, komiðum hópi“.

</details>

<details><summary>final_semantic_review #224 · after · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:879

English: If more than one water source is utilised for fish production, fish representing all water sources must be included for sampling.

Reference (shown after audit): Ef vatn úr fleiri en einni lind er notað við fiskframleiðslu skal velja fisk úr öllum vatnslindum til sýnatöku.

Review: Fish representing all water sources becomes fish being all water sources; source term also malformed.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef fleiri en einn vatnsorð er notað til fiskaræktar verður að taka til sýnatöku fisk sem eru allir vatnsorðin.

</details>

<details><summary>final_semantic_review #225 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:ema:607

English: Since the possibility of increased risk of cancer development in patients with newly diagnosed dysplasia treated with infliximab is not established, the risk and benefits to the individual patients must be carefully reviewed and consideration should be given to discontinuation of therapy.

Reference (shown after audit): Þar sem ekki hefur verið gengið úr skugga um hugsanlega aukna hættu á krabbameinsmyndun hjá sjúklingum með nýgreindan misvöxt sem fá infliximab, verður að endurskoða gaumgæfilega áhættu og ávinning fyrir hvern sjúkling um sig og íhuga á að stöðva meðferð.

Review: Newly diagnosed dysplasia is replaced by tissue-change/metabolism wording, losing the specified diagnosis.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þar sem ekki hefur verið sýnt fram á möguleika á aukinni hættu á krabbameinsuppkomu hjá sjúklingum með nýtt greiningu á vefjaskipta og sem fá infliximab, er nauðsynlegt að endurskoða áhættu og ávinning fyrir hverju sjúklingi og íhuga skal hvort þessi meðferð sé hætt.

</details>

<details><summary>final_semantic_review #226 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:1100

English: The combination of images taken by three exceptional telescopes, the ESO Very Large Telescope on Cerro Paranal , the MPG/ESO 2.2-metre telescope at ESOs La Silla observatory and the NASA/ESA Hubble Space Telescope, has allowed the stunning Jewel Box star cluster to be seen in a whole new light.

Reference (shown after audit): Myndir teknar með þremur sjónaukum, Very Large Telescope ESO á Cerro Paranal, 2,2 metra MPG/ESO sjónaukanum í La Silla stjörnustöðinni og Hubble geimsjónauka NASA og ESA, sýna hina glæsilegu lausþyrpingu Skartgripaskrínið í glænýju ljósi.

Review: Every candidate changes telescope number, JewelBox identity, instrument/site details or seeing-in-new-light relation;5 introduces denial.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Samsetningu myndanna sem tveggja skilgreindir sjónaukar gefa til, Very Large Telescope (ESO) í Cerro Paranal, MPG/ESO 2,2 metra sjónaukann í La Silla stjörnustöð ESO og Hubble geimsjónaukinn NASA/ESO, hefur leitt til sérstakrar litningar onnir.

Candidate 1: Samsetningu myndirnar, sem tveggja sjónauka ESO Very Large Telescope á Cerro Paranal, MPG/ESO 2,2-metrar sjónauka í La Silla stjörnustöð ESO og NASA/ESA Hubble geimflutningssjónauka hafa lauk í stórum þáttum að sjá svona kyrrt og fetu bæjar stjörnuþyrpingu sem er nýtt hjá ný.

Candidate 2: Þessi samsetta myndir úr fjörum óvenjulegum sjónauka, Very Large Telescope ESO á Cerro Paranal, MPG/ESO 2,2 metra sjónauka í La Silla stjörnustöð ESO og NASA/ESA Hubble geimstjörnu, hafa gert kleift að sjá stútt í nýju ljósi rauðbyssavirkja stjörnuþyrpingunni.

Candidate 3: Samsetning ámyndanna, sem tveggja stökkbreyta sjónauka tóku afkerða, Very Large Telescope ESO í Cerro Paranal, MPG/ESO 2,2 metra sjónauka á La Silla stjörnustöð ESO og Hubble geimstjörnustjórnunarstofnunar NASA og ESA, hefur gert kleift að sjá hvarfefna stjörnueyðið Jewel Box.

Candidate 4: Sjónaukorna sem lokuð hafa sú glæsilega Jewel Box stjörnuþyrpingin, sem ESO Very Large Telescope á Cerro Paranal, MPG/ESO 2,2-metrar sjónaukanin á La Silla stjörnustöð ESO og NASA/ESA Hubble geimfarsjónaukanin, hefur leitt í ljós að ný.

Candidate 5: Sjónauka á þremur skilgreindum sjónauka, Very Large Telescope ESO á Cerro Paranal, MPG/ESO 2,2 metra sjónauka í La Silla stjörnustöð ESO og Hubble geimfarsrétta NASA/ESAs, hafa hafnað því að sjónaukinn í Jewel Box stjörnufalinn séð í öllu nýjum ljósi.

Candidate 6: Samsetningu myndirnar sem fyrirhugaðar sjónaukar borið hafa reið á, Vélaráktengið ESO í Cerro Paranal, MPG/ESO 2,2 mítna sjónaukanum í La Silla stjörnustöð ESO og NASA/ESO Hubble geimsjónaukanum hafði gert kleift að sjá Stíkuríkju stjörnuþyrpinguna í nýju ljósi.

Candidate 7: Samhliða myndir úr þremur undanteknum stjörnustofnum ESO Very Large Telescope á Cerro Paranal, MPG/ESO 2,2-metra stjörnustjörnin í La Silla stjörnustöð ESO og NASA/ESA Hubble geimsjónaukinni, hafa leitt til þess að sýna stjörnulokaðartýrunin inntöku í nýju ljósi.

</details>

<details><summary>final_semantic_review #227 · after · greedy · technical_short · F</summary>

Source ID: p13official21:test:ema:2722

English: See also ‘Bleeding or bruising after you stop treatment in section 4.

Reference (shown after audit): Sjá einnig „Blæðingar eða mar eftir að meðferð er hætt“ í kafla 4.

Review: Bruising not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Sjá einnig „Blæðingar eða sláður eftir að meðferð er hætt í kafla 4.

</details>

<details><summary>final_semantic_review #228 · before · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:3044

English: Isn't there someone in some league, who's left- footed?

Reference (shown after audit): Er ekki einhver í einhverri svona deild sem er örfættur?

Review: Left-footed player/league relation not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Er ekki einhver í einriði sem er höfugur á hliða?

</details>

<details><summary>final_semantic_review #229 · before · G8 · technical_short · F</summary>

Source ID: p13official21:test:ema:1788

English: Magnetic resonance imaging is necessary to confirm the diagnosis of PRES.

Reference (shown after audit): Segulómun er nauðsynleg til að staðfesta greiningu PRES.

Review: No candidate preserves MRI confirming PRES diagnosis.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Gagnkvæma mánurmyndun er nauðsynlegt til að staðfesta lyfsáritandi PRES.

Candidate 1: Tilvísun með einhvern annar merkismyndun sem ljós hafir á sviði PRES er nauðsynleg.

Candidate 2: Tilkynning á hendi með loftþyngdaskiptalegra myndun þarf til að staðfesta PRES-klínískuðferð.

Candidate 3: Magnífertíðsnúming er nauðsynleg til að staðfesta sýkingina yfir PRES.

Candidate 4: Tökunarheiningu er nauðsynleg að staðfesta sak á PRES.

Candidate 5: Magnétfrjöskja myndun er nauðsynleg til að staðfesta PRI.

Candidate 6: Tilgreining með líkurnarvíslíða er nauðsynlegur til staðfestingar á PRES.

Candidate 7: Skrár úr magnaruppskiptum eru nauðsynleg til að staðfesta PRES-græðu.

</details>

<details><summary>final_semantic_review #230 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:852

English: These actions may include comparison of the effectiveness of processes, methods and tools related to the chosen themes, mutual transfer and application of good practice, exchanges of personnel, joint development of products, processes, strategy and methodology, adaptation to different contexts of methods, tools and processes identified as good practice, and/or dissemination of results, profile-raising materials and events.

Reference (shown after audit): Aðgerðirnar geta falist í því að bera saman skilvirkni vinnsluferla, aðferða og tóla, sem tengjast þeim þemum sem eru valin, í gagnkvæmri miðlun og ástundun góðra starfsvenja, í starfsmannaskiptum, sameiginlegri þróun vara, vinnsluferla, skipulags og aðferðafræði, í því að aðlaga að ólíku samhengi aðferðir, tól og vinnsluferli, sem eru skilgreind sem góðar starfsvenjur, og/eða í útbreiðslu niðurstaðna og kynningarefnis og skipulagningu viðburða.

Review: All omit/corrupt several process-comparison, good-practice, personnel, adaptation or dissemination list elements.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þessir aðgerðir geta samanstendur samanburði á verkun, aðferðum og verkefnum sem tengjast úrskurðum, meðskipti á starfsmenn, samstarfi í vörum, ferli og aðferðum, samstarfi í þátttöku, aðferðir og ferli sem er til þess að verða góðar starfsvenjur, aðferðir og ferli sem tengjast uppruna, aðgerðir og hæfisreglur, aðferðir, verkefni og ferli sem eru til þess að verða góðar starfsvenjur, aðgerðir um aðupun á aðgerðir og vörum, vörum og tilvikum, aðgerðir um hægðatrifari, vörum og tilvikum, og aðgreining á niðurstöðum, aðgerðum um aðupun á vörum og tilvikum og sýningu á hæfisreglum, verkefnum og tilvikum.

Candidate 1: Síðan má taka til greina þess að þessi aðgerðir hvað varðar samanburð yfir skilvirkni ferlanna, getnaðarferla og vörn sem tengist ákveðnu kerfinu, viðbótarhreyfingum og notkun góðra færni, skilbreytingu umsjóna, sameiginlegri vörnumyndun, sameiginlegri vinnslu ferla, áætlunar og aðferða-, vörnarmeðferðar og aðrar aðferða inntöku sem greind eru hvaða fyrirbæris, og/eða að auka, að því er varðar, niðurstaður, úrræði og tilfinningar.

Candidate 2: Þessi aðgerð geta felldir í samanburð á verkun, aðferðir og búnaður sem tengjast valinu þóknunum, aðskilinn skipti um manna, samstarfsverkun á vörum, ferli og aðferðum, hefðbundin þróun varanir, ferla og aðferða, aðlögun á samhengi við mismunandi kringumastilslu, búnað og ferli, sem auðveldar er kallað slík, og/eða dreifingu á niðurstöðum, af völdum hentugleika og tilvikum.

Candidate 3: Í þessum aðgerðum geta komið fyrir samanburður á virkni vinnu- aðferða, aðferða og búnaðar, sem tengist ákveðnum umbreykjunum, hvort samanburður á heimildum, samþætun eftir dagskilyrðum, skipti þeirra í hand, starfsgreiðslu aðferða, vinnu og áætlana, aðgerðir og aðferðir á tengslum við mismunandi skilyrði og skipti skiptir í hand, eða framlaggingu niðurstöðva, þungaði- og aðskiljandi hlutum og tilvikum.

Candidate 4: Þessi aðgerðir geta náð meðferð, aðferðir og tækni, sem tengjast tilgreindu þrengslum, samanburði um virkni á þeim, einangra flutningu og beitingu góðra aðgerða, millifyrirbréfum um starfsmenn, sameiginlegri þróun afurða, aðferða og aðferðar, stjórnun á vegum til að ná að mismunandi þætti aðferða, tækja og aðferða sem gefnu til góða aðgerða og/eða blettur niðurstöður, aðgreiningar og tilfinningar.

Candidate 5: Þessi aðgerðir geta tengst samanburð á verkun, aðferðum og hlutum sem tengjast tilvistið þema, mismunandi dreifingu og beitingu góðrar aðferða, skipti í aðila, sameiginlega þróun vöru, aðferða og áætlana, aðlögun á aðferðum, hlutum og aðferðum sem tengjast góðar aðferðir, og/eða raunabreyting á niðurstöðum, meðalhæðarvinnslu og tilvikum.

Candidate 6: Þessar aðgerðir geta verið í samanburði á virkjunum, aðferðum og tækjum sem tengjast valinum þóknunum, bæði sjálfsmæli og notkun góðra starfsmála, skipti í hlutum, sameiginlega þátttöku, samstarfs á vörum, aðgerðum, stefnumála og aðferðum, samræmingar á mismunandi tæknilegum ráðstöfunum, tækjum og aðferðum sem gefin eru upp sem góða starfsmálaráðstöfun, og/eða framlags útlits, trefu- og tæknivísi og tilfella.

Candidate 7: Þessi aðgerðir geta innihaldið samanburð á verkun skiptislegra kerfanna, þjóðaferða og tækja sem tengjast vökvunni, aðstoð og beiting á góðum starfsmönnum, skipti í einstöku í móti um leiðbeiningar, samvirkan tækning eftir vöru, kerfum, áætlun og aðferða-, samhliða þróun vörum, kerfanna, áætlunar eða aðferða og aðferða sem ólíkun sjálfkvæmum aðstæðum er greind að vera góðum starfsemi, tækjum og kerfum, og/eða miðlun á niðurstöðum, vísitækum efninum og tilheyri fyrirkomulagum.

</details>

<details><summary>final_semantic_review #231 · before · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:936

English: Ma'am, I need the gentleman's signature so we can begin.

Reference (shown after audit): Ég þarf að fá undirskrift hans svo við getum byrjað.

Review: Signature replaced by unclear handwriting-like invented term; required object not confidently conveyed.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ég þarf að fá handskrínn hans til að við getum byrjað.

</details>

<details><summary>final_semantic_review #232 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:850

English: When implementing this strand the Commission will in particular ensure consistency and complementarity with the activities conducted by other Commission services or by European agencies; in particular, the European Foundation for the Improvement of Living and Working Conditions and the Community RTD Framework programme and the European Centre for the Development of Vocational Training (Cedefop).

Reference (shown after audit): Við framkvæmd aðgerða í þessum flokki mun framkvæmdastjórnin sérstaklega sjá til þess að þær séu í samræmi við og komi til fyllingar starfsemi sem aðrar þjónustugreinar framkvæmdastjórnarinnar eða evrópskar stofnanir stýra, einkum Evrópustofnun um bætt lífskjör og starfsskilyrði, rammaáætlunbandalagsins um rannsóknir og tækniþróun og Evrópumiðstöð um þróun starfsmenntunar (CEDEFOP).

Review: Named institutions, complementarity and programme roles corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þegar framkvæmd þessarar áætlunar gerist skal framkvæmdastjórnin í einkum tryggja samræmi og aukabundning við starfsemi annarra þjónustu framkvæmdastjórnarinnar eða Evrópusamanna; einkum Evrópsk fundinn til bænanna um að þróa fyrirhugaðstæður fyrir aðstoð og starfsemi og rannsóknarsviðbótarréttind Bandalagsins sem varðar rannsóknir innan ríkis og Evrópska stofnunin til þróunar vinnsluefnagernings (Cedefop).

</details>

<details><summary>final_semantic_review #233 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:179

English: These violent explosions rip through the molecular gas clouds in their immediate surroundings, but after the shockwaves have travelled more than about ten light-years they are weaker, and may instead compress clouds that are a little further away, triggering the formation of new generations of stars.

Reference (shown after audit): Höggbylgjur þessara orkuríku sprenginga tæta sundur sameindagasskýin í kring en eftir að þær hafa ferðast meira en tíu ljósár eða svo, hafa þær veikst en geta þjappað fjarlægari skýjum saman og þannig hrundið af stað myndun nýrra kynslóða stjarna.

Review: Weaker shockwaves becomes larger; cloud compression/star formation corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þessi bráða brennslur hreyfa í líkamlegum flugiðu í umhverfið þeirra en eftir að skömmur hafa farið meira en um tíu ljósgangar er þær stærri og geta þó einnig þegar þær eru þrýstir í flugvél sem eru nokkuð frábært til að koma út í nýja áfökum stjórna.

</details>

<details><summary>final_semantic_review #234 · before · G8 · technical_short · F</summary>

Source ID: p13official21:test:eea:1471

English: Prices including all taxes, levies and VAT.

Reference (shown after audit): Verð með öllum sköttum, álögðum gjöldum og VSK.

Review: No complete taxes/levies/VAT list retained.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Verð, þar sem allar skattir, skuldbindingar og gagnaþrengisverð er tilfylt.

Candidate 1: Verðir meðhöndluð allar tækja og skattaraðstöfun.

Candidate 2: Verðir þar sem allar skatta, ámót og gagnaáfengisbót.

Candidate 3: Verðir með íbúiðum skálds eftir, bótakost og viðskiptastöðuaðlengd.

Candidate 4: Verðin með allt tækjum, skattum og aðlögum skatta.

Candidate 5: Verðir, sem þurfa að opna til skuldbindinga, gagna, skrár og gjaldbreiðsluverði.

Candidate 6: Verð þar sem allar skatta, skalföldur og efri skattarverð er takmörkuð.

Candidate 7: Verðir með allan skatta, skóðunum og bótakassa.

</details>

<details><summary>final_semantic_review #235 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eso:710

English: The VST KiDS survey will allow astronomers to make precise measurements of dark matter, the structure of galaxy halos, and the evolution of galaxies and clusters.

Reference (shown after audit): Kortlagningin nefnist VST KIDS og gerir stjörnufræðingum kleift að mæla nákvæmlega staðsetningu hulduefnis, uppbyggingu vetrarbrautahjúpa og þróun vetrarbrauta og þyrpinga.

Review: All corrupt dark matter, halo structure and galaxy/cluster evolution.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Skoðunin VST KiDS leyfir ljósfræðingum að gera nákvæm mælingar á dunkulettu, störfu galælillar og frammistöðu galæla og hlutflokka.

Candidate 1: VST KiDS-venndunin hefur í sérstökum tillögum fyrir stjörnunarkomulagum til að meta drakkum efni, þá ristir úr galáxur, og ævinni galáxur og galáxurklínu.

Candidate 2: VST KiDS ferleiðsluðan skoðun hefur í lokuðri mikinn tækifæri fyrir hvílakrafna, alþjóðhreinni þrýstingar og þróun þrýstings og kújetta.

Candidate 3: VST KiDS-ferlinu heimur úr því að starfsmenn geti gerið áhættugjarnar mælingar á dýraríki, þróun galáxjur og knúna.

Candidate 4: Viðtagan VST KiDS-ferð lýst víkumstjarna og arkimíði og tilgreinir rými hreyfilsrétta, útburð hreyfla og samfylgjandi hreyfla.

Candidate 5: VST KiDS-ferlisendinni er heimilt að taka skilvirkri mælinga á dýrtfeldi, stöðlun gegn skyni í galáxjum og æviningu galáxjanna og svæðisþolanna.

Candidate 6: VST KiDS-aðskilningin hefur í tengslum við miðlun þynna efna, þróun gildis og þróun glóssar og gegnis.

Candidate 7: Forsamlagin með VST KiDS-tekningum hefur gert meðhöndlan fyrir astríðarstjórnendum um nákvæm mælingu á dyrgáfu, gjöf hálim meðal galdranna og þróun galdranna og meðalhópna.

</details>

<details><summary>final_semantic_review #236 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:409

English: Purpose: to determine whether the test facility, if engaged in studies using animals or other biological test systems, has support facilities and conditions for their care, housing and containment, adequate to prevent stress and other problems which could affect the test system and hence the quality of data.

Reference (shown after audit): Markmið: að ákvarða hvort prófunarstöðin, ef þar eru stundaðar rannsóknir með dýr eða önnur líffræðileg prófunarkerfi, hefur yfir að ráða búnaði og aðstöðu þar sem hægt er að hirða um þau, koma þeim fyrir og einangra þau á annan viðeigandi hátt þannig að koma megi í veg fyrir streitu og önnur vandamál sem gætu haft áhrif á prófunarkerfið og þar af leiðandi á gæði gagnanna.

Review: No candidate preserves all support facilities for care/housing/containment and prevention of stress; repeated housing/monitoring substitutes lose concepts.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Tilgangur: til að ákvarða hvort prófunarfyrirkomulag, ef það er í rannsóknáða með dýrum eða öðrum líffræðilegum prófunarkerfum, ábyrg í því að fá til að stuðla að því til þess að fá aðstoð, háfestur og sjálfsvæði, að fullnægjandi leyti, til að koma í veg fyrir þrýsting og aðra vandamál sem geta haft áhrif á prófunarfyrirkomulag og þannig á gæði gagna.

Candidate 1: Tilgangur: til að ákvarða hvort prófunarstöð varðandi dýraeiningu eða annað líffræðilegt prófunarkerfi, ef um rannsóknir er að ræða, ná til stofnana og skilyrða fyrir að hafa stöðu og stjórn fyrir þeim til að verja, ræða og felgi henni, að fullnægi og takmarka að því að það stóð á því að það hvaldi því að það komi í veg fyrir þol og aðrar vandamálur, sem geta haft áhrif á prófunarkerfið og þar af leið og gagnasamþykki.

Candidate 2: Tilgangur: til að ákvarða hvort prófunarstöð, ef tilheyrir rannsóknum á dýrum eða annarri líffræðilegri prófunarkerfi, ásamt tilhlýðilegu aðstoðann og skilyrðum til að sjást, veita og fylgja þeim, séu nægilegur til þess að koma í veg fyrir stress og aðra vandamál sem geta haft áhrif á prófunarkerfið og þannig á gæði gagnanna.

Candidate 3: Tilgangur: til að ákvarða hvort prófunaraðstöður, ef þar hafa verið gerðar prófanir á dýrum eða annarra líffræðilegra prófunarkerfum, hafa stuðningsaðstöðu til að fylgjast með þeim og handhafa þær og tekja til innrennslisvörn, nóg til að koma í veg fyrir þrýsting og önnur vandamál sem geta haft áhrif á prófunarkerfinu og þannig gætu ákvæði.

Candidate 4: Tilgangur: til að ákvarða hvort prófunarásetning, í sambandi við rannsóknir á dýrum eða öðrum líffræðilegum prófunarstöðum, hafi stuðningaraðstöðvar og skilyrði fyrir meðhöndlun, heimilis- og skilferlun, viðkvæmar til að koma í veg fyrir þunglyndi og aðra vandamál sem geta haft áhrif á prófunarstöðuna og þannig gagnkvæmni gagna.

Candidate 5: Markmiðið: að ákvarða hvort rannsóknarstofan, ef hún taki þátt í rannsóknum með dýrum eða öðrum líffræðilegum prófunarkerfum, fylgir staða og fyrirkomulag til að fylgjast með henni, fyrirhuga og inngjaf, nákvæmt til að koma í veg fyrir árás og aðrar vandamál sem geta haft áhrif á prófunarkerfinu og þannig á gæði gagna.

Candidate 6: Tilgangur: til að ákveða hvort prófunarfyrirtæki, ef það gengur í rannsóknir á dýrum eða annarra líffræðilegrar prófunarkerfum, ábyrgjast í sambandi með ábyrgjastarfsemi og skilyrðum fyrir meðhöndslu, húða og innrennslisreglur, sem nægir það að hafa áhrif á hóli prófunarkerfisins og þannig gætu á lagi gagnasammanstæðið.

Candidate 7: Tilgangur: að ákvarða hvort prófunarstöðvar, ef þar til rannsóknir eru gerðar með dýrum eða öðrum líffræðilegum prófunarkerfinni, hafa stuðningarstöðvar og skilyrði til að fylgjast með þær, hýsja þær og fylgjast með þær, að fullnægjandi leyti til að koma í veg fyrir þróun og aðra vandamál sem gætu haft áhrif á prófunarkerfinu og þar afleiðandi gæði gagna.

</details>

<details><summary>final_semantic_review #237 · before · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:504

English: The precise extent of the habitable zone depends on many factors.

Reference (shown after audit): Umfang lífbeltisins veltur á ýmsum þáttum.

Review: No candidate preserves precise extent of the habitable zone and dependence on many factors.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Mikilvægur háttur uppbyggðuð er að því erlendir tíðni.

Candidate 1: Staðbundin umfang bújörðsins er háður þannig margra þátta.

Candidate 2: Prófunartæka þætti réttarskápinn fyrir sæfisáttandið er hátt með því að mörgum þróunarmjögum.

Candidate 3: Prófið yfir inntökuáætlunina er hálfu fjölda fyrirliggjandi aðstæðna.

Candidate 4: Vágaraleikur hlutabréfsamtílsaðar skiptir saman við mikill þátttöku.

Candidate 5: Hlutfall hvaða horfandi hverjans stöðu veita þórverðan sérstökra ekki hennar.

Candidate 6: Ráðstafanir sem aukið gegn umhverfisáæðið eru í miklu mikið.

Candidate 7: Mikið er umfang samtækinu húðinu hins sviðs.

</details>

<details><summary>final_semantic_review #238 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:571

English: To check power-operated windows/roof-panel systems/partition systems with reversing devices, a measuring instrument/test rod shall be placed through the opening from the inside of the vehicle or, in the case of a partition system, from the rear part of the passenger compartment in such a way that the cylindrical surface of the rod contacts any part of the vehicle structure which forms the boundary of the window/roof-panel aperture/partition.

Reference (shown after audit): Ef gera á athugun á rafstýrðum rúðum/þaklúgukerfum/skilrúmskerfum með enduropnunarbúnaði er mælitæki/prófunarstöng sett í gegnum opið innan frá úr ökutækinu eða, þegar um er að ræða skilrúmskerfi, frá aftari hluta farþegarýmis með þeim hætti að sívalt yfirborð stangarinnar snertir einhvern þann hluta ökutækisins sem afmarkar gluggann/þaklúguopið/skilrúmið.

Review: Powered/reversing systems and cylindrical contact geometry corrupted; any part becomes all surface.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Til að athuga verkstæða-gerðir glugga/þekjuflagna/fyrirhluta með bakslögunartækni skal setja mælitæki/prófunarrod út í skýrinu frá inni á ökutækinu eða, ef um fyrirhluta er að ræða, frá enda hluta sjónsykisins og þannig að hringræn yfirborð prófunarroðsinnar snertir allt yfirborð ökutæknisins sem myndar skýrinu/þekjuflagna/fyrirhluta.

</details>

<details><summary>final_semantic_review #239 · before · greedy · technical_short · F</summary>

Source ID: p13official21:test:ema:2490

English: If you are left-handed, do what comes naturally to you.

Reference (shown after audit): Þeir sem eru örvhentir eiga að gera það sem þeim finnst eðlilegast.

Review: Left-handed condition not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef þú ert höflugur, gertu það sem er eftir þér.

</details>

<details><summary>final_semantic_review #240 · after · greedy · technical_short · F</summary>

Source ID: p13official21:test:ema:2323

English: It is important to drink plenty of water to avoid dehydration.

Reference (shown after audit): Mikilvægt er að drekka mikið af vatni til að koma í veg fyrir ofþornun.

Review: Dehydration becomes urine formation.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Mikilvægt er að drekka mikið af vatni til að forðast þvagmyndun.

</details>

<details><summary>final_semantic_review #241 · before · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:2721

English: No, but one day, I'll take that cane away...

Reference (shown after audit): Nei, en einn góðan veðurdag á ég eftir að taka stafinn...

Review: Cane becomes girl; future one-day removal omitted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Nei, en ég færi þetta stúlku úr hendi.

</details>

<details><summary>final_semantic_review #242 · before · greedy · technical_short · F</summary>

Source ID: p13official21:test:eea:1855

English: The product must be easily recyclable.

Reference (shown after audit): Það verður að vera auðvelt að endurvinna vöruna.

Review: Recyclable becomes repeatable.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Vörullin skal vera auðvelt að endurtekið.

</details>

<details><summary>final_semantic_review #243 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:879

English: If more than one water source is utilised for fish production, fish representing all water sources must be included for sampling.

Reference (shown after audit): Ef vatn úr fleiri en einni lind er notað við fiskframleiðslu skal velja fisk úr öllum vatnslindum til sýnatöku.

Review: Water-source and fish-representing-all-sources relation corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef fleiri en einn vatnsorð er notað til fiskarannsóknar verður að taka til sýnatöku fisk sem eru í allt vatnsorði.

</details>

<details><summary>final_semantic_review #244 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:1190

English: Indeed, there is a need for technical and scientific support and a high level of stable expertise to properly apply the Community legislation in the fields of maritime safety and ship pollution prevention, to monitor its implementation and to evaluate the effectiveness of the measures in place.

Reference (shown after audit): Raunar er þörf á tækni- og vísindalegri aðstoð og öflugri og yfirgripsmikilli sérfræðiþekkingu til að beita með réttum hætti löggjöf Bandalagsins á sviði siglingaöryggis og varna gegn mengun frá skipum, fylgjast með framkvæmd hennar og meta skilvirkni þeirra ráðstafana sem eru fyrir hendi.

Review: Ship-pollution prevention becomes preventing improvement of an unexplained impact; stable expertise also corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það er þörf á tæknilegri og vísindalegu stuðningu og mikil stöðugt sérfræðileg mat til að beita rétt fyrir löggjöf bandalagsins um öryggi á sjó og að koma í veg fyrir að hægt sé að bæta úr skellunni af skipum, til að fylgjast með framkvæmdi hennar og meta árangur ráðstafana sem eru í gildi.

</details>

<details><summary>final_semantic_review #245 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:850

English: When implementing this strand the Commission will in particular ensure consistency and complementarity with the activities conducted by other Commission services or by European agencies; in particular, the European Foundation for the Improvement of Living and Working Conditions and the Community RTD Framework programme and the European Centre for the Development of Vocational Training (Cedefop).

Reference (shown after audit): Við framkvæmd aðgerða í þessum flokki mun framkvæmdastjórnin sérstaklega sjá til þess að þær séu í samræmi við og komi til fyllingar starfsemi sem aðrar þjónustugreinar framkvæmdastjórnarinnar eða evrópskar stofnanir stýra, einkum Evrópustofnun um bætt lífskjör og starfsskilyrði, rammaáætlunbandalagsins um rannsóknir og tækniþróun og Evrópumiðstöð um þróun starfsmenntunar (CEDEFOP).

Review: All corrupt complementarity and named institutions/programmes; some invent identifiers.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þegar framkvæmdastjórnin beitt þessar far til að gera að talin í samræmi með hreyfingunum í annarri aðila framkvæmdastjórnarinnar eða um rammaáhöfundum Evrópu eða að hlutaðeigandi ráðstafanir hjá Evrópu svæði, að framan Evrópusmiðjuna um aðstæður fyrir rekstraraðgerðir inntækis og svæði Evrópusmiðjuna um þróun vinnu og starfsemi (Cedefop).

Candidate 1: Þegar framkvæmd þessarar vegna stendur á aðildarríkjunum skal framkvæmdastjórnin í sambandi við aðra viðskiptasviði framkvæmda þessarar stofnunar með því að tryggja samræmi og aukabirgða við þær starfsemi sem annarir aðila framkvæma í framkvæmdastjórninni eða starfsemi Evrópusamningsins sem einnig veitir Evrópusamningsins fyrir rannsóknir og áðurhvernvaldi og Evrópusamningsins fyrir mælinga um þátttakaðan þjálfun (Cedefop).

Candidate 2: Með framkvæmd þessarar hleðsla skal framkvæmdastjórnin í sér tryggja í sér samræmi og samhliða þá starfsemi sem annarra þjónustu framkvæmdastjórnarinnar eða starf sem ESB-hlutaðeigandi stofnanir framkvæma. Í sérstökum tilvikum skulu það um ESB-fundinn til bælingu á aðstæður áhættueðlunar og starfsemi til að endurheimta lifun og vinnslu, og áætlanir um rannsóknarskilyrði í evrópskum ríkum og ESB-svæðið fyrir rekstraraðlun í lagskírteini (Cedefop).

Candidate 3: Þegar framkvæmd þessa megin er að huga að því að framkvæmdastjórnin tryggja sér að hvaða kosti varðar samræmi og staðbundinn haus við starfsemi þátttækra aðila í framkvæmdastjórninni eða evrópskrar stofnanir, sérstaklega, Framstöð við bælingu og fullvísindri ákvæði um heimild fyrir vinnslu og starfsemi (European Foundation for the Improvement of Living and Working Conditions) og Evrópusambandskerfi til að lokunarsjóða um reynslu og tækniforsætum og Evrópusamstofnun um framhlutverk í vinnslu og starfsemi (Cedefop).

Candidate 4: Í staðun niðurstaðnaaráttarinnar mun framkvæmdastjórnin, einkum, sjá til þess að íhuga samræmi og aðstoðarátt við starfsemi annarra búðanna framkvæmdastjórnarinnar eða Evrópusamningsins, einkum náttúruframfara Evrópu til að auka gæði í hópum og starfsemi (talinn 41/1998), Evrópu milliða rannsóknarstofu á rannsóknir í þjónustu (Community RTD Framework programme) og Evrópuð þjóðhagsfræðilegs stofa til þróunar verkefna og starfsemi (Cedefop).

Candidate 5: Við framkvæmd þessarar strandar skal framkvæmdastjórnin sérstaklega tryggja samræmi og aukunleika við þær starfsemi sem annarra þjónustu framkvæmdastjórnarinnar eða aðildarríkisstofnunanna eru að starfa með; sérstaklega: Evrópuefingin fyrir bætt glæp og vinnslu aðgerð og Stjórn Evrópu fyrir rannsóknarsviðbót innan ríkisins (RTD) og Evrópustofnunin fyrir frammistöðu starfsemi í vísindum til hæfis (Cedefop).

Candidate 6: Í framkvæmd þessarar starfsgreinar skal framkvæmdastjórnin viðeigandi til þess tryggja síðurkerfi og umsökunarviðurkenningu við starfsemi annars stofnunarinnar sem er með sérstaklega aðil fyrir framkvæmdastjórnina eða aðilans í Evrópusambandi; við umsóknir Bandalagsins um rannsóknarvísindamáta og annar aðila innan Bandalagsins sem telur með sjálfbærum tegundum (Cedefop).

Candidate 7: Með framkvæmd þessarar kerfi verður framkvæmdastjórnin einnig aðstoðara míðvörnu og fylgvirka þeim starfsemi sem þátttöfin í aðra framkvæmdastjórnar eða aðildarríkisstofnunum eru framkvæmdar, einkum Efndin fyrir að greiðslu og vinnslu í Bandalagi Evrópu og ramma þátttöflu Evrópu um rekstraraðferðir til að haft paytu aðskilningarskírteini (Community RTD Framework programme) og Evrópu-kerfi fyrir þróun í hagskírteini (Cedefop) fyrir starfsmenningu.

</details>

<details><summary>final_semantic_review #246 · after · G8 · technical_medium · P</summary>

Source ID: p13official21:test:ema:1152

English: Change from baseline in body weight was similar for patients treated with sitagliptin relative to placebo.

Reference (shown after audit): Breytingar á þyngd frá grunnlínu voru svipaðar fyrir sjúklinga sem meðhöndlaðir voru með sitagliptíni miðað við þá sem fengu lyfleysu.

Review: Candidates1/3/4/5/6 preserve body-weight change from baseline, similar sitagliptin-versus-placebo comparison.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [1, 3, 4, 5, 6]

Candidate 0: Breyta á líkamsþyngd frá upphafsgildi var svipuð hjá sjúklingum sem fengu sitagliptin í samanburði við lyfleysu.

Candidate 1: Breyting á líkamsþyngd frá grunngildi var svipað fyrir sjúklinga sem fengu sitagliptín samanborið við lyfleysu.

Candidate 2: Áhrif á líkamsþyngd frá upphafsskammti voru svipuð hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.

Candidate 3: Breyting á líkamsþyngd frá upphafsgildi var svipuð hjá sjúklingum sem fengu sitagliptin samanborið við lyfleysu.

Candidate 4: Breyting á líkamsþyngd frá upphafsgildi var sambærileg hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.

Candidate 5: Breyting frá upphafsgildi á líkamsþyngd var svipuð hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.

Candidate 6: Breyting í líkamsþyngd frá upphafi var svipuð hjá sjúklingum sem fengu sitagliptin samanborið við sjúklinga sem fengu lyfleysu.

Candidate 7: Breyting frá grunngildi á líkamsþyngd hjá sjúklingum sem fengu sitagliptin samanborið við lyfleysu.

</details>

<details><summary>final_semantic_review #247 · before · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:136

English: ALMA is radically different from visible-light and infrared telescopes.

Reference (shown after audit): ALMA er gerólík sjónaukum sem sjá sýnilegt og innrautt ljós.

Review: No candidate preserves visible-light and infrared telescope distinction.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: ALMA er í grundvelli að öðrum öndulegrum og infraráðiðum töflum.

Candidate 1: ALMA er hræðilega rangriður frá ljóskopogáfæði og infraráglugáfæði.

Candidate 2: ALMA er umtalsverulega aðra en litlega og ir-ótlega stjórnsýsluvélum.

Candidate 3: ALMA er svo alvarlega mismunandi áherslnarleðingi og innreikjulæti.

Candidate 4: ALMA er að því miklu sem er alvarlega mismunandi leysingarhjálpum sem eru hálfarmiðlega og í reyni.

Candidate 5: ALMA er háðar mismunandi hjá útreikningarkemjum sem sýsa ljósi og geislagjófa.

Candidate 6: ALMA er í alvarlega aðallega mismunandi áhersla og skúlunarhislum.

Candidate 7: ALMA er glöfulslega mismunandi hverju líkamlegum og infraráðlegum teletúlum.

</details>

<details><summary>final_semantic_review #248 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:ema:129

English: Clinical studies have demonstrated that ProQuad can be given simultaneously (but at separate injection sites) with Prevenar and/or hepatitis A vaccine, or with monovalent or combination vaccines comprised of diphtheria, tetanus, acellular pertussis, Haemophilus influenzae type b, inactivated poliomyelitis, or hepatitis B antigen.

Reference (shown after audit): Klínískar rannsóknir hafa sýnt fram á að hægt er að gefa ProQuad á sama tíma (en á öðrum stungu- stað) og Prevenar og/eða lifrarbólgu A bóluefni eða með eingildu eða samsettum bóluefnum með barnaveiki, stífkrampa, frumulausan kíghósta, Haemophilus influenzae af gerð b, deyddum mænu- sóttar eða lifrarbólgu B mótefnavökum.

Review: Several vaccine antigens, including diphtheria/pertussis/polio, are invented or corrupted terms.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Klínískar rannsóknir hafa sýnt fram á að ProQuad má gefa samhliða (en í mismunandi stungustöðum) með Prevenar og/eða lifrarbóluefni gegn lifrarbólgu A eða einstök eða samsetta bóluefni sem innihalda dýpkransa, tétanus, ófrumna kútusótt, Haemophilus influenzae tegund b, óvirkjaða mænirétta eða lifrarbólgu B mótefni.

</details>

<details><summary>final_semantic_review #249 · after · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:3337

English: But maybe, if we got away from here, if we went somewhere safe, it could be different.

Reference (shown after audit): En kannski ef við kæmumst burt héðan, ef við færum á öruggan stað, gæti það breyst.

Review: Getting away from here, safe destination and possible different outcome all retained despite inflection.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: En kannski, ef við farið úr hér, ef við farið til öruggs staðar, gæti það verið annars konar.

</details>

<details><summary>final_semantic_review #250 · after · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:2164

English: You didn't have the guts to do it yourself.

Reference (shown after audit): Þú hafðir ekki kjark til þess sjálfur.

Review: Lack of courage becomes lack of ability, changing the psychological assertion.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þú hefur ekki hægt til að gera það sjálfur.

</details>

<details><summary>final_semantic_review #251 · after · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:939

English: Put it in the envelope, Mrs. Rochon.

Reference (shown after audit): Settu hann í umslagið, frú Rochon.

Review: Envelope becomes package.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Settu það í pakkanum, frú Rochon.

</details>

<details><summary>final_semantic_review #252 · after · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:63

English: The placement of these devices in the soil should not result in preferential flow paths.

Reference (shown after audit): Staðsetning þessara tækja í jarðveginum má ekki breyta farvegi vatnsins.

Review: Preferential flow paths becomes indication-like flow paths, losing the hydraulic concept.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Setning þessara tækjanna í jarði ætti ekki að leysa til ábendingar flæðislega leiða.

</details>

<details><summary>final_semantic_review #253 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:63

English: “Studying afterglows is vital to further our understanding of the objects that become gamma-ray bursts and what they tell us about star formation in the early Universe,” says the studys lead author Jochen Greiner from the Max-Planck Institute for Extraterrestrial Physics in Garching bei München, Germany.

Reference (shown after audit): „Það er nauðsynlegt að rannsaka glæður blossanna svo auka megi skilning okkar á þeim fyrirbærum sem mynda gammablossa og hvað þau segja okkur um myndun stjarna snemma í sögu alheimsins“ segir Jochen Greiner, aðalhöfundur greinar um rannsóknina, og stjarneðlisfræðingur við Max-Planck-Institut für extraterrestrische Physik í Garching við München í Þýskalandi.

Review: All corrupt afterglows/gamma-ray bursts or scientific/institutional attribution.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: "Að rannsaka eftirgláðurnar er mikilvægt til þess að við sýnir meira af stjörnunum sem verða geimstorkur og sem segja við um stjörnumyndun fyrirheimisins", segir Jochen Greiner, hópyfni greinar um rannsóknina frá Max-Planck institúturinni fyrir geimfræði í Garching bei München í Þýskalandi.

Candidate 1: „Nauðsynlegt er að fá nánari nátmetun af stjörnum sem verða gamma-geislir og hve þau segja okkur um stjörnuformiðið í börnum alheiminu,“ sagði Jochen Greiner, forritandi greinarinnar, frá Max-Planck stofnuninni fyrir forraði-geðsniði í Garching við München í Þýskalandi.

Candidate 2: „Viðgangsprófanir skipta málið í frekari námi við skilningu á einingunum sem fleygja gammatillögun og hvað þær segja okkur um stjörnumyndun á fyrsta lagi alheimsins“, sagði Jochen Greiner, aðalhöfundur rannsóknarinnar frá Max-Planck stofnuninni fyrir fjölafurðatengda vísindanir í Garching í München í Þýskalandi.

Candidate 3: „Mannnmælingar á eftirglænum eru mikilvægar að því að því að framlengja skilning okkar um efnablöndur sem verða og hvað þeir segja okkur um stjörnumyndun á frumumjórninu,“ sagði Jochen Greiner, aðalhöfundur greiningarannsóknarinnar, frá Max-Planck stofnuninu fyrir geimfræði í Garching í München, Þýskalandi.

Candidate 4: "Að taka átöllu á eftirglæðum er mikilvægra þar sem það lætur okkur frekar skilja hvaða fyrirbæri gama-grásskjálftan eru og hvað þær segja okkur um stjörnumyndun í fyrstu evíni heims", sagði Jochen Greiner, leiðsöguhólls greinar í frambúrsjónunar-stofu í Garching í München í Þýskalandi.

Candidate 5: „Atprýma áfangan er mikilvægt því að auka skilning á lagi sem verða gymlaugabrot og hvað þeir segja okkur um stjörnumyndun í fyrstu alheiminum,“ sagði Jochen Greiner, leiðsöguherra rannsóknarinnar í Max-Planck stofnun um geimfluttni í Garching í München í Þýskalandi.

Candidate 6: „Með það sem varðar að æðast eftirglæði er mikilvægt til að drepið skilningu okkar um fyrirbæri sem verið er og hvað þau sega okkur um stjörnumyndun á fundinu fyrir Burtuðu Vetrarbrautana,“ sagði Jochen Greiner, aðalhöfundur rannsóknarinnar, frá Max-Planck stofnuninu fyrir raffræn fjölgaða í Garching bei München í Þýskalandi.

Candidate 7: „Vera með þátttöku á eftirlitusbolunum er háttfalt til að hafa frekari skilningu um fyrirbjóða sem verða gamma-geislur og veita okkur þáttar á stjörnumyndun á fyrri alheiminu,“ sagði Jochen Greiner, leiðsögnarstjóri rannsóknarinnar, frá Max-Planck stofnuninu fyrir geimfræði í Garching í Nemöđunum.

</details>

<details><summary>final_semantic_review #254 · before · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:1168

English: R Coronae Australis itself is not visible to the unaided eye, but the tiny, tiara-shaped constellation in which it lies is easily spotted from dark sites due to its proximity on the sky to the larger constellation of Sagittarius and the rich star clouds towards the centre of our own galaxy, the Milky Way.

Reference (shown after audit): R Coronae Australis sést ekki með berum augum en litla kórónulaga stjörnumerkið sem hún tilheyrir sést auðveldlega við góðar aðstæður sökum nálægðar þess á himninum við stjörnumerkið Bogmanninn og stjörnumprýtt svæðið við miðju okkar Vetrarbrautar.

Review: Constellation shape, Sagittarius, star clouds and MilkyWay extensively corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: R Coronae Australis sjálfur er ekki sýnt á óhjálma augun en stuttur, tókshúður stökkbreyturinn sem hún liggur í er einfaldlega sýndur frá svartum staðnum vegna nærþættar hennar á himni við stærri stökkbreyturinn Ségíttíusar og þrýstingar stjórnsýsanna í miði heimsins, Mjólkurvindans.

</details>

<details><summary>final_semantic_review #255 · after · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:430

English: Keep the needle in your skin after the dose counter has returned to 0 and count slowly to 6.

Reference (shown after audit): Haltu nálinni í húðinni eftir að skammtateljarinn sýnir aftur 0 og teldu hægt upp að 6.

Review: Each candidate changes in-skin to on-skin, slow to fast, dose counter or the complete ordered instruction.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Geymið nálina á húðinni eftir að skammtahlutarinnur hefur náð 0 og rannsakaði hratt að 6.

Candidate 1: Haldið nálinni á húðinni eftir að skammtaríkið hefur náð 0 og tölutakaðst fljótlega til 6.

Candidate 2: Geymið nálina í húðinni eftir að gömlunarkílurinn hefur orðið 0 og tölulastu hraðar til 6.

Candidate 3: Haldið nálinni á húðinni eftir að skammtaalitinn hefur farið til 0 og tölur hægt langt saman til 6.

Candidate 4: Haltu nálina í húðinni á eftir að skammtaleyfið hefur náð 0 og töljaði slæmar til 6.

Candidate 5: Haltu nálinni á húðina í lok 0 og tölutakkaðu hægt til 6.

Candidate 6: Haltu nálina lengi í húðinni eftir að skammtalistið er aðeins 0 og rannsakaðu hana að 6.

Candidate 7: Haldið nálina í húðinni þegar töflu upphaflega hefur orðið að 0 og tölutöluðið slönguð eftir að getið er 6.

</details>

<details><summary>final_semantic_review #256 · after · greedy · technical_medium · U</summary>

Source ID: p13official21:test:ema:709

English: The other ingredients are sodium chloride, succinic acid, polysorbate 80, 2- phenoxyethanol and water for injections.

Reference (shown after audit): Önnur innihaldsefni eru natríumklóríð, succinic sýra, polysorbat 80, 2-fenoxýetanól og vatn fyrir stungulyf.

Review: Ingredient list largely recognizable, but succinic-acid rendering is nonstandard and cannot confidently certify chemical identity.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Önnur innihaldsefni eru natríumklóríð, súkfinýlsýra, pólýsorbat 80, 2-fenóxýlethanól og vatn fyrir stungulyf.

</details>

<details><summary>final_semantic_review #257 · after · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eso:716

English: From the gravitational lensing effect, these groups turn out to contain around 30 times more dark than visible matter.

Reference (shown after audit): Þyngdarlinsuhrifin sýna að hóparnir innihalda um 30 sinnum meira hulduefni en sýnilegt efni.

Review: No candidate preserves gravitational lensing and dark/visible-matter30-to-one comparison.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Frá slæmu merginormsins færa þessar hópar um 30 sinnum gömul en myndarbúið.

Candidate 1: Af rafþekjum í silíðum fjallar þessi hópar um 30 sinnum mikið skemmt á dökkum fyrirritum en réttum.

Candidate 2: Í gegnsviknumagalausningu, skal þessi hópar innihalda um 30 sinnum mikið skemmta en myndarvænni efni.

Candidate 3: Frá andstræna skýlun er sáttmálum þessi til að koma fram að þeir innihaldi um 30 sinnum fleiri dýraríki en sýnilegt (dark matter).

Candidate 4: Framkvæmd grátrumýlunar gefur þessi hópar yfirleitt 30 sinnum meiri skertu en sýnilegt.

Candidate 5: Í ljósmyndunartruflunum urðu þessi hópar aðeins í um 30 sinnum miklar djúpt en sýnilegar efnis.

Candidate 6: Stöurnáingurinn ser yfir þessi hópar í aldur 30-faldi mikið skemmta en myndi.

Candidate 7: Af geimfræðilegri myndun þess, upphafstækur þessi hópar eru um það bil 30 sinnum mikið skerðri en litlaður vatn.

</details>

<details><summary>final_semantic_review #258 · before · greedy · technical_short · U</summary>

Source ID: p13official21:test:eso:705

English: Normal long-duration GRBs last between 2 and 2000 seconds.

Reference (shown after audit): Venjulegir langir gammablossar standa yfir í 2 til 2000 sekúndur.

Review: Long-duration GRB and2-2000seconds retained; normality modifier is unclear/invented.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Staðgengi langt í tíma GRB eru áfram í 2 til 2000 sekúndur.

</details>

<details><summary>final_semantic_review #259 · before · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:3404

English: A mother never gives up on her child.

Reference (shown after audit): Móðir snýr aldrei baki við barni sínu.

Review: Giving up becomes storing; idiom meaning not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Mamma geymir aldrei upp á barnið sinni.

</details>

<details><summary>final_semantic_review #260 · before · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:349

English: The results described here use some of these Science Verification data.

Reference (shown after audit): Gögnin sem notuð voru fyrir þessa rannsókn var að hluta til aflað við þessar prófanir.

Review: ScienceVerification data/usage relationship corrupted in every candidate.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Niðurstöðurnar sem eru lýst hér eru notuð sumu af þessum skjölunarmatvottunardati.

Candidate 1: Tilkynntir niðurstöðurnar eru í þessum texti að nota nokkra af þessum skjölun.

Candidate 2: Efninu, sem lýst er hér, eru visslur með þessari rannsóknaraupplýsingum.

Candidate 3: Niðurstöðurnar sem komið er fyrir hér eru að útfræðilegum upplýsingum fyrir gagnagrunni.

Candidate 4: Niðurstöðurnar sem eru lýst hér nota að því er varðar nokkra af þessum skynsamlan um sannprófun.

Candidate 5: Niðurstöðurnir sem eru lýst hér eru notaðrar þessara framleiðslubréfsins.

Candidate 6: Í þessum niðurstöðum eru notuð sum þessara verkunaraðferðardatatana.

Candidate 7: Sértryggingarnar sem eru lýst hér, skipta með nokkrum þessara rannsóknsfrákvæða.

</details>

<details><summary>final_semantic_review #261 · after · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:1409

English: The port security assessment is the basis for the port security plan and its implementation.

Reference (shown after audit): Áhættumat fyrir höfn er undirstaða verndaráætlunar hafnar og framkvæmdar hennar.

Review: No correct port-security-assessment-as-basis-for-plan relation; several reverse assessment/plan or change port.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Portvænslarasmat er grunn úr áætlun um portvænslu og framkvæmd þeirrar.

Candidate 1: Portvæsnarænsla er grundvöllur við áætlunina um vænskun á hafðum og framkvæmd hennar.

Candidate 2: Portverndarúttekkningin er grunnur á portverndarefni og framkvæmdi þess.

Candidate 3: Vaktarúttekkandi mat á vörðunartökum er grunnur fyrir vaktarútgáfu aðurstofunnar og framkvæmd hennar.

Candidate 4: Portvættaráætlunin er grunnur fyrir mat á portvættamál og beitingu þess.

Candidate 5: Portaðbelti mat er grunnur fyrir portaðbeltakerfið og framkvæmd þess.

Candidate 6: Upprétting á öryggi borgarinnar er grunur fyrir áætlun á öryggis borgarins og framkvæmd hennar.

Candidate 7: Rörverndarskyldur í vikilund eiga að vera grundvöll fyrir rörverndarplofið og framkvæmd þess.

</details>

<details><summary>final_semantic_review #262 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:1100

English: The combination of images taken by three exceptional telescopes, the ESO Very Large Telescope on Cerro Paranal , the MPG/ESO 2.2-metre telescope at ESOs La Silla observatory and the NASA/ESA Hubble Space Telescope, has allowed the stunning Jewel Box star cluster to be seen in a whole new light.

Reference (shown after audit): Myndir teknar með þremur sjónaukum, Very Large Telescope ESO á Cerro Paranal, 2,2 metra MPG/ESO sjónaukanum í La Silla stjörnustöðinni og Hubble geimsjónauka NASA og ESA, sýna hina glæsilegu lausþyrpingu Skartgripaskrínið í glænýju ljósi.

Review: All corrupt telescope count/instruments/JewelBox identity or combination/new-light relationship.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Samsetningu myndanna sem tveimur óttaðum teiknareikningum, ESO-velkominu stöðugum teiknareiknings í Paranal, ESO 2,2 metrið teiknareiknings í MPG/ESO í La Silla og NASA/ESO Hubble teiknareiknings, hefur leitt í ljós minn að upplýsingu varjalandi stjórnungarstjórna með svínignaði.

Candidate 1: Samsetningar af myndunum sem tveimur óháðum teklum útburðast, Veltakilvirkni-teklinn á Paranal-kopulann í ESO-stofnun, 2,2-métriktöluninn fyrir ESO af MPG/ESO og NASA/ESA-teklinn Hubble sem haldar á svona þrótt og snemma néttið er unnt að horfa á stórlíkt stjórnjafnrök.

Candidate 2: Þessi samsetningu af myndum sem tveggja óhæðlegum stjórnsýslustjórnunarmiðum, ESO-öndunaryrkjuna í Vélustaður á Paranal hleðinu, MPG/ESO 2,2 m trjáma stjórnsýslustjórnunarmiðuna í ESO-stjórnvaldins La Silla og NASA/ESO Hubble stjórnsýslustjórnunarhvarfinnar hefur unntað að fá út í ný rýmur fjöri stefnu.

Candidate 3: Samsetning á myndum, sem eru tekin með þrjú óvart fáenlegum teker, ESO-ótungum stelpriftum á Paranal-bergunni, 2,2-metri stelpriftum á ESO-umbralíðnum í Lasa Silla og NASA/ESO Hubble stelpriftum, hefur launð snúnin Jonatan starhrein.

Candidate 4: Samsetning ímyndanna sem þrjár sérstök útbúnaðarhúsin hafa tekið af, ESO-útbúnaðinn á Paranal-bergunni í Vesturland, 2,2-míði útbúnað innan ESO-fara í La Silla-teknarstofu og NASA/ESO Hubble-geimsusýni, hefur hafa leyfi í því að þolast rofari ástefnun af starnæstingi Nesturblöndinu í nýtt ljósi.

Candidate 5: Samsetningu af myndum sem tveggja óttaflaglega týningar síða ESO-Very Large Telescope á Cerro Paranal, MPG/ESO 2,2 m týningu á ESO-loskutunarstöðinni La Silla og NASA/ESA Hubble Space Telescope hefur leitt til að sjá úrskólinu sérhæfis stjarnaeiningarinnar í nýju ljós.

Candidate 6: Samsetning á myndum sem tveimur meginhlésvikusjóna borið, ESO-veltaanleggi í Paranalskýrinu, 2,2 metra veltaanleggi ESO/MPG í Sjálfstæðisvæði Lassíla og NASA/ESO Hubblehugnaðarhvernifarið, hefur leitt til gagnvartíma að því að starran stjórnstýringi málsastarfarinnar sé horfður í óvartum ljósum.

Candidate 7: Samsett af myndum sem fórstum tveimur sjálftendum skynskegðum stjórnutennum, ESOvíðmæðastjórnutenni í Paranalberði, MPG/ESO 2,2 m stjórnutenn á Skaðaviklæði-tekníkastöðvinni af ESO og NASA/ESE 20 m stjórnutenn í Húllu, hefur hefjaða að hitta stökkbólgaða stjórnhliðastjórnað á nýjum ljósi.

</details>

<details><summary>final_semantic_review #263 · after · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:930

English: Wells in microtitre plates are coated overnight with recommended dilutions of purified immunoglobulin fractions of antibodies of reference quality.

Reference (shown after audit): Bollar í míkrótítrunarplötum eru þaktir næturlangt með ráðlögðum þynningum af hreinsuðum ónæmisglóbúlín- þáttum mótefna sem standast kröfur um viðmiðunargæði.

Review: All corrupt microtitre wells/coating overnight or purified immunoglobulin/reference-quality dilutions.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Vélur á miðlæga hettuglasum eru lausn undir einn sólarhring með tilgreindri þynningu úr því að þynna ónæmisglóbúlíni fyrir öryggishæfðum mótefni.

Candidate 1: Wells á milliglaðutækinu eru klavaðir eftir kvöld með ráðlögðum þynningu af gilduðum ónæmisglóbúlínfráhófum mótefna, sem eru til staðar.

Candidate 2: Hettuglöfur í mikið gluggu eru úða út í nálægt tíma með ráðlögðum þynningum af hreinsuðri immunglóbúlín frumum mótefna miðað við viðmiðunarmeðferð.

Candidate 3: Vellir í bilsuflöginna eru klúftir til baka með tilmeðræði þolsum tómörum af gerðarimmúnóglóbúlíni frahófum mótefna með viðmiðunarmikilli gildum.

Candidate 4: Vell í lyfjaplatti eru klúft í nálægt tíma með skammta (recommended dilutions) úr gerð nýrnaefnum í samræmi við staðbundna gildi.

Candidate 5: Wells í mífretturplaðum eru útfellt í svolíti smá tímar sem ráðlögða þynningu af hreinsuðu immunglóbúlín-skilum mótefna af gæða við viðmiðunarmál.

Candidate 6: Vellir á milliseðlunarplátum eru klippið með ráðlagðum þynningum úr gerðnum immungólóbínlíffrásundum mótefna með viðmiðunarmikilli gæði.

Candidate 7: Vell í mífurýrfræðum æsast á næurnum með viðeigandi þynningum úr hreinsuðum immunglóbúlni í sérstökum stigi mótefna af gertgöngu stærðfræðilegu gæfni.

</details>

<details><summary>final_semantic_review #264 · before · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:1152

English: Change from baseline in body weight was similar for patients treated with sitagliptin relative to placebo.

Reference (shown after audit): Breytingar á þyngd frá grunnlínu voru svipaðar fyrir sjúklinga sem meðhöndlaðir voru með sitagliptíni miðað við þá sem fengu lyfleysu.

Review: No candidate preserves body-weight CHANGE FROM BASELINE; words become letter arrangement/frequency/tiredness or omit baseline.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Tíðni skipti úr byrjunverandi líkamsþyngd hafði jafnaðar þegar sjúklinga var á meðferð með sitagliptínum í tengslum við lyfleysu.

Candidate 1: Kvarstæðan breytur á líkamsþyngd var svipufull fyrir sjúklinga sem fengu sitagliptín samanborið við lyfleysu.

Candidate 2: Ákvæði um breytingu á líkamsþyngd komu til saman hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.

Candidate 3: Tilgangur á líkamsþyngd hafði sömu í sameiginlegu hlið eftir upphafsgildi hjá sjúklingum sem fengu sitagliptín í samanburði við lyfleysu.

Candidate 4: Verður á líkamsþyngd undanskils fyrir sjúklinga sem fengu sitagliptín samanborið við lyfleysu.

Candidate 5: Þreyttur á líkamsþyngd var nákvæmlega sami hjá sjúklingum, sem fengu sitagliptín, í því mæli að lyfjagjöf veldeyði.

Candidate 6: Bréfskipan frá grunnþéttni í líkamsþyngd er sambærilegt hjá sjúklingum sem fengu sitagliptín í samanburði við lyfleysu.

Candidate 7: Þreyttur úr grundvelli á líkamsþyngd var líka hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.

</details>

<details><summary>final_semantic_review #265 · after · G8 · technical_short · P</summary>

Source ID: p13official21:test:eso:839

English: The Caisey Harlingten and ASH2 telescopes.

Reference (shown after audit): Caise Harlingten og ASH2 sjónaukarnir.

Review: Candidate1 preserves both named telescopes with correct Icelandic telescope noun.

Inspected original candidate indices: [0, 1, 3, 4, 6]; confirmed correct indices: [1]

Candidate 0: Caisey Harlingten og ASH2 stjörnustjörnunum.

Candidate 1: Caisey Harlingten og ASH2 sjónaukarnir.

Candidate 3: Caisey Harlingten og ASH2 sjónaukann.

Candidate 4: Caisey Harlingten og ASH2 sjónauki.

Candidate 6: Caisey Harlingten og ASH2 sjónaukarnar.

</details>

<details><summary>final_semantic_review #266 · after · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:1323

English: If refills are not provided, the weight of the total primary packaging shall not exceed 3,7 g per wash for tablets and 1,7 g per wash for all other products.

Reference (shown after audit): Ef áfyllingar eru ekki í boði skal þyngd grunnumbúðanna í heild ekki vera meiri en 3,7 grömm á þvott ef um er að ræða töflur og 1,7 grömm á þvott fyrir allar aðrar vörur.

Review: All corrupt refills/primary packaging or per-wash quantity units.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Ef ekki er tilfullt að gefa endurnýjunum skal þyngd heildarfræðilegra umbúða ekki vera meiri en 3,7 g til úthreinsunar, handa töflum og 1,7 gr/ úthreinsun handa öðrum lyfjum.

Candidate 1: Ef fylgikerfi ekki eru til boði skal ekki vera meira en 3,7 g á heildarförun í hreinun fyrir töflur og 1,7 g á hreinun fyrir öll önnur afurð.

Candidate 2: Ef ekki er veitt uppsetningar skal þyngd heildarfylgsins ekki fara yfir 3,7 g til útbrotunar á hverri lykja af töflum og 1,7 g til útbrotunar á öllum öðrum lyfjum.

Candidate 3: Ef endurtekinn skammtur er ekki veitt skulu þyngdar hluti öllra hefðbundna umbúða ekki vera stærri en 3,7 gr/þvag fyrir töflur og 1,7 gr/þvag fyrir öllu öðrum vörum.

Candidate 4: Ef ekki er útgefandi endursetningar skal hægður heildarfyrirbærlisums pakkningar ekki vera meiri en 3,7 g í hverjum þvagrindi fyrir töflur og 1,7 g í hverjum þvagrindi fyrir allar önnur lyf.

Candidate 5: Ef meir tilbúinum afbúnum er ekki tilfyltur, má ekki vera meira en 3,7 gr/ryk fyrir töflur og 1,7 gr/fjölda gráðu fyrir önnur vörur.

Candidate 6: Ef tilbætur eru ekki veittar skal vigt heildarfræðilegra umbúða ekki vera meira en 3,7 g í hverjum þurrfæðu fyrir töflur og 1,7 g í hverjum þurrfæðu fyrir öll aðra vara.

Candidate 7: Ef ekki er fylgt við endurtekna af lyfjagjöfum, skal þyngdar hluta heildarfráselds ekki vera meiri en 3,7 g hver ríma með töflum og 1,7 g hver ríma með öðrum lyfjum.

</details>

<details><summary>final_semantic_review #267 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:437

English: Lenvatinib should not be started in patients with fistula to avoid worsening and lenvatinib should be permanently discontinued in patients with oesophageal or tracheobronchial tract involvement and any Grade 4 fistula (see section 4.2); limited information is available on the use of dose interruption or reduction in management of other events, but worsening was observed in some cases and caution should be taken.

Reference (shown after audit): Ekki skal hefja meðferð með lenvatinibi hjá sjúklingum með fistil til að forðast versnun og hætta skal meðferð með lenvatinibi til frambúðar hjá sjúklingum þar sem vélinda eða barki og berkjur eiga í hlut og í tilfellum allra 4. stigs fistla (sjá kafla 4.2), takmarkaðar upplýsingar liggja fyrir um skammtahlé eða skammtaminnkun við meðferð á öðrum atvikum, en versnun varð í sumum tilvikum og því skal gæta varúðar.

Review: All corrupt fistula/site/grade or permanent-discontinuation instructions; some invert stopping.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Ekki skal hefja meðferð með lenvatinibi hjá sjúklingum með liðverða til að koma í veg fyrir versnun og ekki skal hætta meðferð með lenvatinibi hjá sjúklingum með fæðu í munni eða fyrir öndunarfæraneti og eftir sem jöfn (aðeins fyrir í 4. gráðu) og að ráðlagðar upplýsingar liggja fyrir um notkun skilyrða, skorts eða minnkaða skammts í meðferð þar sem ekki varðar aðra aukaverkanir og versnun kom fram hjá sumum tilvikum.

Candidate 1: Ekki skal hefja meðferð með lenvatinibi hjá sjúklingum með glötu til að koma í veg fyrir aukningu á sjúkdóminn og skal stöðva meðferð með lenvatinibi hjá sjúklingum með raðavatnshvati eða enda- og skógræði og þeim sjúklingum sem fá 4. stigs glós (sjá kafla 4.2); takmarkaðar upplýsingar liggja fyrir um notkun skammtsins stuttra eða minnkaðs til að hefja meðferð á öðrum tilvikum, en versnun séð í nokkrum tilvikum og þá skal gæta varúðar.

Candidate 2: Ekki ætti að hefja meðferð með lenvatinibi hjá sjúklingum með glæs to ofnæmi til að koma í veg fyrir versnun lenvatinibs og skal stöðvulega hætta meðferð með lenvatinibi hjá sjúklingum með svæði sem tengist mergkviðum eða brota og einhverri miðað við fargi 4 glæs (sjá kafla 4.2); takmörkuð upplýsingar liggja fyrir um notkun skrefaframsýklunar eða minnkaða skammta í öðrum tilvikum, en versnið fylgdi eftir í sumum tilviki og mikilvægar kröfur skulu tekið.

Candidate 3: Ekki á að hefja meðferð með lenvatinibi hjá sjúklingum með liðskur og utan að varta þegar meðferðin er hætt í lengi og hægt er að halda meðferð með lenvatinibi hjá sjúklingum með sýringu í rásaræði eða öndunarfæra og sjúklingum með 4. stigs liðskur (sjá kafla 4.2); takmörkuð upplýsingar liggja fyrir um notkun skiptis á skammti eða minnkað skammtar í meðferð hjá sjúklingum fyrir önnur aukaverkanir, en versnun kom fram í einstakum tilfellum og ráð gegn því skal gæta varúðar.

Candidate 4: Ekki skal hefja meðferð með lenvatinibi hjá sjúklingum með gáta vegna þess að hún getur versnað og hægt ætti að hætta notkun lenvatinibs tilvara hjá sjúklingum með ítar í þroti eða hrygglofshrygg og hvaða kostar 4. stigs gáta (sjá kafla 4.2); fyrirbæri er að komi fram um takmarkaðar upplýsingar um því hvort stöðuga stöðugleika eða minnkaður skammtur sé notað við meðferð annarra ástanda og því að breytingar á skömmtum hafa orðið til bata komu fram hjá sumum tilvikum, þá skal gæta varúðar.

Candidate 5: Hefja skal ekki meðferð með lenvatinibi hjá sjúklingum með fiðlun til að koma í veg fyrir versnun sjúkdómsins og stöðvarenda skal meðferð með lenvatinibi af loknum hjá sjúklingum með svæði á áxli eða tunguhraði þar sem svæðið verður með höndum og í sumum tilvikum sem verður miðað við 4. stigs, að því tilskildu að það er einungis skýrt um að gefa að stöðva skammtatíma, að minnka skammta eða breyta meðferð í innan sér við aðgerðir annarra tilbreytinga og að breyta meðferðinni, en versnun átti fyrir hendi í sumum tilvikum og skal gæta varúðar.

Candidate 6: Lenvatinib skal ekki hefja hjá sjúklingum með glæsi til að koma í veg fyrir versnun og hætta skal meðferð með lenvatinibi á lengi þegar um sjúklinga er að ræða smút í sársaka eða asta og tréða eða þrúða og einhverjar smút í 4. stigs (sjá kafla 4.2); takmörkuð upplýsingar eru fyrirliggjandi um notkun skrefa tímabundið eða minnkaðs á meðferð á öðrum tilvikum, en versnun kom fram í sumum tilvikum og vart ber að gæta varúðar.

Candidate 7: Ekki á að byrja meðferð með lenvatinibi hjá sjúklingum með glæi til að forðast að það væri að versna, og lyfjagjöf á lenvatinibi skal hægt gauð til að hjá sjúklingum með uppsvæði í lagsmíði eða öndulifshorni og lyfja sem liggja í 4. stigs (sjá kafla 4.2); fyrirbæri á upplýsingum um að hamla meðferð eða minnka skammta við meðferð fyrir annað sjúkdómur er takmörkuð, en versnun varst fyrir tilteknum tilvikum og þá á að gæta varúðar.

</details>

<details><summary>final_semantic_review #268 · before · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:400

English: ESPRESSO will feature radial velocity precision of 0.35 km/hour or less.

Reference (shown after audit): ESPRESSO mun ná að greina sjónstefnuhraða niður í 0,35 km/klst eða minna.

Review: Radial-velocity precision not intelligibly conveyed despite numeric value.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: ESPRESSO skal hafa radalegri sniðaðri hreyfingaráknun í 0,35 km/h eða minna.

</details>

<details><summary>final_semantic_review #269 · before · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:1088

English: Weather statistics are available here.

Reference (shown after audit): Upplýsingar um veður má finna hér.

Review: No candidate preserves weather STATISTICS available here; closest4 substitutes physical weather data with unrelated prefix.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Vegna heitt og vatnslyfja þykir tilbirgir.

Candidate 1: Vegna er búist gögn fyrir veður.

Candidate 2: Í þessum heimilis er staðfest yfir þátttöku.

Candidate 3: Vegnavarðskilaboð eru fyrir hér.

Candidate 4: Vegna líkamslega gögn fyrir veður er hér aðgengileg.

Candidate 5: Í metum hefur varður verður til dæmis.

Candidate 6: Vegna áhrifanna er búnaður fært.

Candidate 7: Vegna kvenntíma hér er það fyrir.

</details>

<details><summary>final_semantic_review #270 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:329

English: The experiment marks the first time that APEX has taken part in VLBI observations, and is the culmination of three years hard work at APEXs high altitude site on the 5000-metre plateau of Chajnantor in the Chilean Andes, where the atmospheric pressure is only about half that at sea level.

Reference (shown after audit): Með tilrauninni er APEX í fyrsta sinn notaður í VLBI mælingum og er hápunkturinn á þriggja ára erfiðisvinnu við APEX sjónaukann sem er í 5.000 metra hæð yfir sjávarmáli á Chajnantor sléttunni í Andesfjöllum Chile, þar sem loftþrýstingur er helmingi minni en við sjávarmál.

Review: Culmination becomes repetition, and atmospheric pressure becomes an invented air-whiteness term.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Framkvæmdin er fyrsta sinn sem APEX hefur taka þátt í VLBI mælingum og endurtekið þriggja ára vinnu á hægri stöðu APEX á 5000 metra hæði Chajnantors á Andes fjallunni í Chile, þar sem lofthvítur er aðeins um hálftil þess sem á hafihæði.

</details>

<details><summary>final_semantic_review #271 · before · G8 · technical_short · P</summary>

Source ID: p13official21:test:ema:635

English: Table 4 provides dose modification guidance for dinutuximab, GM-CSF and IL-2.

Reference (shown after audit): Tafla 4 veitir leiðbeiningar um skammtaaðlögun dínútúxímabs, GM-CSF og IL-2.

Review: Candidates5/7 retain Table4 giving dose-change guidance for dinutuximab,GM-CSF,IL-2.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [5, 7]

Candidate 0: Í töflu 4 koma fyrir leiðbeiningar um breytingu á skammti við einstök notkun dinutuximesíða, GM-CSF og IL-2.

Candidate 1: Í töflu 4 er veitt ráðstafanir fyrir breytingu á skammti fyrir dinútuxímab, GM-CSF og IL-2.

Candidate 2: Í töflu 4 fyrirboð er um breytingu á skammti fyrir dinutuximab, GM-CSF og IL-2.

Candidate 3: Tölfræðilegar gögn í töflu 4 gefa ábyrgð á að breyta skammta af dinutuxímabi, GM-CSF og IL-2.

Candidate 4: Í töflu 4 færast aðstoðarverkun á skammtabreytingum fyrir dinutuximab, GM-CSF og IL-2.

Candidate 5: Í töflu 4 er tilgreind leiðbeiningar um breytingar á skammtum fyrir dinutuximabi, GM-CSF og IL-2.

Candidate 6: Í töflu 4 er fært ráðhendingar fyrir breytingu á skammti til íðbúnaðar með dinutuxímabi, GM-CSF og IL-2.

Candidate 7: Í töflu 4 er gefið ráðgjöf um breytingu á skammta fyrir dinutuximab, GM-CSF og IL-2.

</details>

<details><summary>final_semantic_review #272 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:ema:2650

English: Patients should be advised that in the event of any sudden visual defect, they should stop taking Sildenafil Actavis and consult a physician immediately (see section 4.3).

Reference (shown after audit): Ráðleggja á sjúklingum að hætta töku Sildenafil Actavis og hafa strax samband við lækni ef þeir finna fyrir skyndilegri sjónskerðingu (sjá kafla 4.3).

Review: Sudden visual defect and immediate consultation are not retained.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Sjúklingar skulu vera ráðlagir um að hætta að taka Sildenafil Actavis ef áhættuleg álit í augum koma fram og takið ráðstafanir hjá lækninum tilvísu (sjá kafla 4.3).

</details>

<details><summary>final_semantic_review #273 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:908

English: This bridge, which has not been seen before (and is too faint to show up in this picture), is somewhat bluer than either galaxy, indicating that it consists of stars created in gas that was drawn away from NGC 1387 by the gravitational pull of NGC 1399.

Reference (shown after audit): Þessi brú hafði ekki sést áður (og er of dauf til að koma fram á myndinni) en hún er nokkuð blárri en hin vetrarbrautin sem bendir til þess að hún samanstandi af stjörnum sem mynduðust úr gasi sem NGC 1399 hrifsaði úr NGC 1387.

Review: All corrupt bridge faintness/colour or gravitational-pull origin, despite copied NGC numbers.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þessi brú, sem hefur ekki séðð áður (og er of seyðið til að vera sem séður á myndinni), er blár en oss annan vetrarbraut, sem benda til að henni fái upp stjörnur sem eru myndar úr gasi sem lítið var drag teir úr NGC 1387 af völdum gærhlaustur á NGC 1399.

Candidate 1: Þessi brú, sem hefur ekki séð áður (og sést ekki vel í myndinni) er merkurblár en annar galni, sem bendir til að það er stjörnur sem eru búin úr gasið sem var tekin úr NGC 1387 vegna þá þrálags sem NGC 1399 hefur á höndinni.

Candidate 2: Þetta brú, sem hefur ekki séðð áður (og er of þungur til að sýna í myndinni), er örlítið fjarlægari en annar útflugan og bendir til þess að hann séu stjörnur sem eru myndaðar úr gasi sem komið var mæði af NGC 1387 vegna gagnsemi NGC 1399.

Candidate 3: Þetta brú, sem hafa ekki séð þar fyrir (og er of lágt til að lítur upp í þessari mynd), er fargari en hvert stjarnafugli einu sér, sem gefur til kynna að það samanstendur af stjörnum sem byggðuðu út úr gassins sem tókst úr NGC 1387 vegna áhættuhvítanums NGC 1399.

Candidate 4: Þetta brú, sem hefur ekki séð áður (og er yfirveldur til að sýna í myndinni) er mikið grátt en annar galdrirnar, til að gefa til áherslu á að það er stjörnur sem eru unnið úr gasi sem leidstyrkir NGC 1399 gleypt úr NGC 1387.

Candidate 5: Þessi brú, sem hefur ekki séð áður (og er of dýr hvolið til að koma fram í myndinni), er hvolfri en öllum vetrarbrautum, sem benda til þess að hann séu þyrpingar sem eru created í gasi sem gefinn verið frá NGC 1387 af gegnum sjón á NGC 1399.

Candidate 6: Þessari brú, sem hefur aldrei komið fram (og er of svart til að koma fram í þessari mynd), er bær seinni en annar galnur og gefur til kynna að hann sést af stjörnum sem birtust úr gasi sem var kallað úr NGC 1387 af því að það leggast við áhrif þráðs NGC 1399.

Candidate 7: Þessi brú, sem hefur ekki séð áður og er ekki til stæðara til að sjá upp í myndinni, er aðeins viðbriggrein en annarra vetrarbrauta, sem bendir til þess að það séu stjörnur sem eru framleiddar úr gasi sem var dragið út frá NGC 1387 af gegnþrýstingi NGC 1399.

</details>

<details><summary>final_semantic_review #274 · before · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:3265

English: There's a police convention out there.

Reference (shown after audit): Það er lögregluráðstefna þarna úti.

Review: Police convention and location not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það er lögreglurinn í þessu.

</details>

<details><summary>final_semantic_review #275 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:2183

English: For intravenous use, infusion systems with Actrapid at concentrations from 0.05 international unit/ml to 1.0 international unit/ml human insulin in the infusion fluids 0.9% sodium chloride, 5% dextrose and 10% dextrose inclusive 40 mmol/l potassium chloride using polypropylene infusion bags, are stable at room temperature for 24 hours.

Reference (shown after audit): Fyrir gjöf í bláæð er Actrapid stöðugt við stofuhita í 24 klst., í styrkleikum 0,05 alþjóðlegar einingar/ml til 1,0 alþjóðlegar einingar/ml af mannainsúlíni í eftirfarandi innrennslisvökvum; 0,9% natríumklóríði, 5% glúkósa og 10% glúkósa með 40 mmól/l af kalíumklóríði, þegar notaðaðir eru pólýprópýlen innrennslispokar.

Review: All corrupt potassium chloride, international-unit concentration, container or stability conditions.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Fyrir innrennslit, innrennsli yfir valdið með Actrapid í þéttni frá 0,05 heimildarhópur/ml til 1,0 heimildarhópur/ml af mannisku insúlín í innrennslihettanum 0,9% natríumklóríð, 5% dektrosi og 10% dektrosi, íhvernfalli 40 mmól/l klóríðkloríð, í pólýprópílynnum innrennsliþjáli, er þetta stöðugt í herbergistengsl 24 klukkustund.

Candidate 1: Til notkunar inntækis eru endurvaranir inndælingartækjum með Actrapid í styrkurum frá 0,05 stóð/í mílílínúmi til 1,0 stóð/í mílílínúmi, óþekktur óbundinn insúlíni, í inndælinguflussi 0,9% natríumklóríð, 5% dextros og 10% dextros, með 40 mmól/l knúkóríð, með pölpópúlypum, þegar í hita 24 klukkustundar.

Candidate 2: Ef til handhafurstu, bein eru stöðugt 24 klst. þegar innrennvæpnum með Actrapid í meðhöndlunum, með styrk frá 0,05 í.st. í ml. til 1,0 í.st. í ml. líkamsinsúlín í beinunarmjólkum sem innrennvæpnum menga 0,9% natríumklóríð, 5% dextros og 10% dextros sér 40 mmol/l natríumklóríð í 24 klst.+ í vökuvægi í plópum af polypropýl.

Candidate 3: Þar að gegnum inntöku eru innrennsli efnahogur með Actrapid í styrk frá 0,05 ínst. eining/mlíkvið til 1,0 ínst. eining/mlíkvið með insúlíni í sviðinu fyrir menn í innrennsliölum, 0,9% natríumsaltr, 5% dáxtósa og 10% dáxtósa, inl. 40 mmol/l natríumsaltr, með pólýprópílynninni innrennslisbolla, leyfileg nálægt í 24 klst. á hita.

Candidate 4: Fyrir innrennsli skal nota blóðleysi með Actrapid í þéttni frá 0,05 aðstæðu alþjóðalegu einingar/ml til 1 alþjóðalegu einingar/ml af sprautuinsúli í blóðleysinum 0,9% natríumklóríð, 5% dextros og 10% dextros íþætta 40 mmol/l natríumklóríð, með blóðleysi af pólýprópýleni, sem er stöðug við 24 h notað við hitarglosi.

Candidate 5: Tilkynnt er að lyfjakerfi sem notað er innar bláæð með Actrapid í styrk frá 0, 05 heimildarviðmiðun/jml til 1, 0 heimildarviðmiðun/jml fyrir mennins insúlíns þar sem insúlínið er í bláæðinni 0, 9% natríumklóríð, 5% dextrosi og 10% dextrosi í þætti og 40 mmol/l kópríklóríð, eru stöðugt með 24 klst. við 0, 05, 1, 0 heimildarviðmiðun/jml í bláæðinni, til 24 klst. með betur styrk, við 2, 0 heimildarviðmiðun/jml í bláæðinni, til 24 klst. með betra styrk, við 3, 0 heimildarviðmiðun/jml í bláæðinni, til 24 klst. með betri styrk, við 4, 0 heimildarviðmiðun/jml í bláæðinni, til 24 klst. með betri styrk.

Candidate 6: Fyrir notkun í bláæðu eru þáhlutabúnaður með Actrapid í þéttni 0,05 aðina einninga/ml til 1,0 aðina einninga/ml af mannsinsulín í bláæðunum með 0,9% natríumklóríð, 5% dextros og 10% dextros, inl. 40 mmol/l klorít kíníums, í bláæðunum í bólusetningu í pólýprópýlýni, staflægan við háður hitastigi í 24 klst.

Candidate 7: Fjörgurvæli með Actrapid við blóðflösi eru þarflega til notkunar, með insúlín frá mannvaxlum sem eru í þéttni 0,05 stigi milljónunni/ml til 1,0 stigi milljónunni/ml í fjörgunatrúunum með 0,9% natríumklóríð, 5% dextros og 10% dextros sem inlend 40 mmol/l natríumklóríð, með fyrirhuguðum pólýproprílynír, stöðugu í rúmkamræði að 24 klst.

</details>

<details><summary>final_semantic_review #276 · after · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:881

English: Using standard candles - such as the variable stars within IC 1613 and the less-common Type Ia supernova explosions, which can seen across far greater cosmic distances - astronomers have pieced together a cosmic distance ladder, reaching deeper and deeper into space.

Reference (shown after audit): Með hjálp staðalkerta eins og breytistjörnunum í IC 1613 og sprengistjörnum af gerð Ia, sem sjást úr mikilli fjarlægð í geimnum, hafa stjörnufræðingar smíðað fjarlægðarstiga sem nær lengra og lengra út í geiminn.

Review: No correct standard-candle/variable-star/TypeIa/cosmic-distance-ladder explanation.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Með stöðugum bannlar - svo sem breytilegir stjörnur innan IC 1613 og lítilegir af tegund Ia ræktarstyrkur, sem sjá má yfir miklu stjörnuferil - hafa stjörnufræðingar samið raflínu sem náir skýrri stjörnuferill- með það að koma öðru og öðru að misna í geimnum.

Candidate 1: Nauðsynlegir býli - sem eru ávísu sjónbúnaður, eins og breytilegir stjörnur í IC 1613 og lítill en vanfreyi af tegund Ia eftirlitsbrotum - hefur stjörnufræðingar samið sternur til sér og hentar lengri og lengri í geimnum.

Candidate 2: Stjörnufræðingar hafa laust saman stjörnumælanæri skipti sem reynir öðrum styrkurstjörnuríkum í IC 1613 og fleira sárstjörnur af tegund Ia sem er um leiðir í smástirri stjörnustig í geiminn.

Candidate 3: Með stöðugum myndunni - svo sem þessu umlægðu stjörnu fyrir alíkunum í IC 1613 og umlægðu stjörnuflæði af tegund Ia, sem má sjá í hári langri geimfræðilegri sjálfbrundi -, hafa stjörnufræðingar gengið saman sjálfbrundi frá sjálfbrundi í geimnum og náði sjálfbrundi sem náði djúpu og djúpu til geimsins.

Candidate 4: Með hjálp staðla kérna, svo sem breyttra stjörnurnar í IC 1613 og lágsvægar breyttra stjörnuþjónusturar af tegund Ia, sem sjáist á mjög langa fjarlægð, hafa stjörnufræðingar reynst saman stjörnuþjálfan sem nánast í djúpu og djúpu í geimnum.

Candidate 5: Hjá stjörnufræðingum hefur verið haft þróun á litunum - eins og breytandi stjörnur í IC 1613 og minnkunar fyrir gerð Ia af æxlun í himnu, sem sjár er um örlítið lengri rúm - og hefur þeir lagt saman lítilt stjarnrúmmál í far seinnum inni í geiminn.

Candidate 6: Með staðallum baka- og burtkirkja - svo sem breytilegir stjörnur í IC 1613 og minnkunar Ia geislaskipti, sem sjáðar á lengra himnir - hefur stjörnufræðingar komið saman stjarnvagnsvallann, sem nærster og síðar til umfangsgerðar.

Candidate 7: Með viðbúnum ljósinum, eins og breytilegir stjörnur í IC 1613 og minnkri úrferri af tegund Ia sem sjást í langa stjörnumál, hafa stjörnufræðingar reiknað út svörunarladd á geimnum, sem lægri og lægri kemur í geiminn.

</details>

<details><summary>final_semantic_review #277 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:ema:1458

English: This is important to make the medicine easier and more comfortable to inject.

Reference (shown after audit): Þetta er mikilvægt til þess að auðveldara og þægilegra sé að sprauta lyfinu.

Review: Comfortable becomes enjoyable/fun, changing injection comfort claim.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þetta er mikilvægt að gera lyfið einfaldari og gamanlegt að innspruða.

</details>

<details><summary>final_semantic_review #278 · before · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:3025

English: Based on individual patient response and tolerability, the dose may be increased to 300 mg (15 ml) per day after an interval of 3 to 7 days, and if needed, to a maximum dose of 600 mg (30 ml) per day after an additional 7-day interval.

Reference (shown after audit): Eftir svörun og þoli hvers sjúklings má auka skammtinn í 300 mg (15 ml) á sólarhring eftir 3-7 daga og ef þörf krefur í hámarksskammt, 600 mg (30 ml) á sólarhring, eftir 7 daga til viðbótar.

Review: No candidate preserves individual response/tolerability and full staged maximum-dose instruction.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Á grundvelli ákvæða sjúklinga og meðferðarlækna er má auka skammtinn við 300 mg (15 ml) á daga á hverju degi eftir 3 til 7 daga tíma og, ef þörf krefur, á 600 mg (30 ml) á degi á 7 daga tíma.

Candidate 1: Bundinu upplýsingu um hvers konan sjúklingur tafar og greiðsluþoli varðandi samanburði er styrkt að skammti sé aukinn upp að 300 mg (15 ml) á dag eftir 3 til 7 daga millibili og ef þörf kemur að 600 mg (30 ml) á dag.

Candidate 2: Býrðu á það að lækni fær 300 mg (15 ml) meðan á voru 3 til 7 daga, og ef þörf á verið er 600 mg (30 ml) meðan á voru 7 daga.

Candidate 3: Bæði og viðkomandi hjálpar og íhlæðissvið fyrir birtur er hægt að auka skammtinn meðan að 300 mg (15 ml) á dag eftir 3 til 7 dagar fresti og, ef nauðsyn krefur, að 600 mg (30 ml) á dag eftir 7 dagar fresti til hámarksþátta.

Candidate 4: Hækkun yfir lyfjagjöf er hægt þó að 300 mg (15 ml) á dag, áfram 7 dag á milli, og ef nauðsyn krefur er 600 mg (30 ml) á dag áfram 7 dag á milli.

Candidate 5: Bundin ákvæði sjúklinganna og þeirra umræddar nota má stækka skammtinn að 300 mg (15 ml) á dag eftir 3 til 7 dagar í milli og, ef þörf krefur, að 600 mg (30 ml) á dag eftir 7 dagar okkur.

Candidate 6: Byggð á leiðréttun og þátttökum hverja sjúklinga er hækkun lyfsins heimilt að stakka til 300 mg (15 ml) á dag eftir 3 til 7 daga tíma og ef þörf kemur að 600 mg (30 ml) á dag eftir 7 daga tíma.

Candidate 7: Voxir má aukið síðar í 300 mg (15 ml) á sólarhring, með íhlutum sem sá sjúklingur veitir, ef það teljist nauðsynlegt, að því er varðar 600 mg (30 ml) sáðið mátlægt í 7 dagar eftir stöðgjöf.

</details>

<details><summary>final_semantic_review #279 · after · G8 · technical_short · U</summary>

Source ID: p13official21:test:ema:2323

English: It is important to drink plenty of water to avoid dehydration.

Reference (shown after audit): Mikilvægt er að drekka mikið af vatni til að koma í veg fyrir ofþornun.

Review: Candidate0 approximates drinking fluids to avoid drying out, but dehydration term and water-specific object uncertain; no confirmed fully correct rendering.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Mikilvægt er að drekka miklu vökva til að forðast útþurrkun.

Candidate 1: Mikilvægt er að drekka marga vatni til að forðast þurrka.

Candidate 2: Mikilvægt er að drukkja mikið vatn til að koma í veg fyrir vatnsþurrkun.

Candidate 3: Mikilvægt er að drekka munur af vatni til að forðast þvagræsingu.

Candidate 4: Mikillvigt er að drekka mikið vatn til að falið úr þvagi.

Candidate 5: Mikilvægt er að drekka mjög víðtækt vatn til að forðast þurrkun.

Candidate 6: Mikilvægt er að drekka mikið af vatni til að koma í veg fyrir útbrot á vatnsþurrku.

Candidate 7: Mikilvægt er að drekka mikið af vatni til að forðast þráþykki.

</details>

<details><summary>final_semantic_review #280 · after · greedy · technical_short · F</summary>

Source ID: p13official21:test:eea:615

English: Annual days of sick leave not paid by the employer (optional).

Reference (shown after audit): Árlegur fjöldi leyfisdaga vegna veikinda sem vinnuveitandi greiðir ekki (valkvætt).

Review: Sick leave and unpaid-by-employer relation corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Árslegar dagir fyrir sjúkdómsframsölu sem vinnuveitandi gefur ekki til (valfræðileg).

</details>

<details><summary>final_semantic_review #281 · before · greedy · technical_short · F</summary>

Source ID: p13official21:test:eea:615

English: Annual days of sick leave not paid by the employer (optional).

Reference (shown after audit): Árlegur fjöldi leyfisdaga vegna veikinda sem vinnuveitandi greiðir ekki (valkvætt).

Review: Annual days of sick leave becomes dates for weakness; annual count and leave meaning lost.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Dagsetningar fyrir veikleikur sem fyrirtækið borgar ekki (valinlegt).

</details>

<details><summary>final_semantic_review #282 · after · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:2128

English: Don't you worry about those dope smokers and nudists down below there?

Reference (shown after audit): Hefurðu ekki áhyggjur af dóphausunum og striplingunum þarna?

Review: Smokers/nudists and the negative question are not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ekki hafa áhyggjur af þeim doppaheyrum og náttúruhæðum niðri í þessu?

</details>

<details><summary>final_semantic_review #283 · after · G8 · technical_short · P</summary>

Source ID: p13official21:test:ema:1918

English: The presented safety information is derived principally from paediatric patients.

Reference (shown after audit): Fyrirliggjandi öryggisupplýsingar eru einkum til komnar út frá börnum.

Review: Candidate4 retains presented safety information mainly derived from paediatric patients, using a child-stage paraphrase.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [4]

Candidate 0: Sýndar upplýsingar um öryggi liggja aðallega fram fyrir sjúklinga á aldrinum 0-12 ára.

Candidate 1: Tilvist öryggiskenndir eru aðallega úr upplýsingum um sjúklinga fyrir börn.

Candidate 2: Tilkynntu upplýsingar varðandi öryggi eru í algengu rökstuddar frá sjúklingum á aldri.

Candidate 3: Ráðlagðar upplýsingar um öryggi ræðast aðallega frá sjúklingum til handa börnum.

Candidate 4: Tilkynnt upplýsingar um öryggi eru, aðallega, úr upplýsingum um sjúklinga á börnastigi.

Candidate 5: Sjálfkærar öryggisupplýsingar eru, að höfðu sérstaklega grun í hjá börnum.

Candidate 6: Tilkynntum öryggishagana byggist hins vegar áhluti hjá börnum.

Candidate 7: Tilkynntar upplýsingar um öryggi eru meðal sinni frá upplýsingum um sjúklinga börn.

</details>

<details><summary>final_semantic_review #284 · before · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eso:710

English: The VST KiDS survey will allow astronomers to make precise measurements of dark matter, the structure of galaxy halos, and the evolution of galaxies and clusters.

Reference (shown after audit): Kortlagningin nefnist VST KIDS og gerir stjörnufræðingum kleift að mæla nákvæmlega staðsetningu hulduefnis, uppbyggingu vetrarbrautahjúpa og þróun vetrarbrauta og þyrpinga.

Review: Dark matter and galaxy-halo/evolution concepts extensively corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: VST KiDS-ferlið hefur í tengslum við skilgreiningu á dýrfrumum, stökkbreytingu galáxjaskipta og stökkbreytingu galáxjafar og klúðra.

</details>

<details><summary>final_semantic_review #285 · after · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:1168

English: R Coronae Australis itself is not visible to the unaided eye, but the tiny, tiara-shaped constellation in which it lies is easily spotted from dark sites due to its proximity on the sky to the larger constellation of Sagittarius and the rich star clouds towards the centre of our own galaxy, the Milky Way.

Reference (shown after audit): R Coronae Australis sést ekki með berum augum en litla kórónulaga stjörnumerkið sem hún tilheyrir sést auðveldlega við góðar aðstæður sökum nálægðar þess á himninum við stjörnumerkið Bogmanninn og stjörnumprýtt svæðið við miðju okkar Vetrarbrautar.

Review: Constellation shape/Sagittarius/rich star clouds corrupted; rich clouds becomes calm star formation.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: R Coronae Australis sjálfur er ekki sýnt með óhjálpar augu en stuttur, tiara- skipti stjörnumerkin sem það er í er greint frá fyrir svartum staðsetningum vegna nálægri fjarlægðs á himninum við stærri stjörnumerkin Sígítrarinn og rólega stjörnumyndunum í miðju okkar vetrarbrauta, Vetrarbrautarinnar.

</details>

<details><summary>final_semantic_review #286 · after · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:3484

English: If you do not give me the house you promised I shall be forced to return to England.

Reference (shown after audit): Ef þú lætur mig ekki fá húsið eins og þú lofaðir neyðist ég til að fara aftur til Englands.

Review: NOT giving the house becomes giving it, reversing the premise.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef þú gefur mér húsinn sem þú lofaðir mér skal ég vera forðast til England.

</details>

<details><summary>final_semantic_review #287 · after · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eso:760

English: Extreme stars like the two components of VFTS 352, play a key role in the evolution of galaxies and are thought to be the main producers of elements such as oxygen.

Reference (shown after audit): Ofsafengnar stjörnur eins og í VFTS 352 leika lykilhlutverk í þróun vetrarbrauta og eru taldar meginuppspretta frumefna á borð við súrefni.

Review: Oxygen element production becomes an unrelated vehicle-type expression.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Hámarkssjár eins og tvö hlutir VFTS 352 spila mikilvægar hlutverki í þróun vetrarbrauta og eru talin vera aðalmyndandi efni sem eigið er ökutípu.

</details>

<details><summary>final_semantic_review #288 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:ema:992

English: Animal studies have shown excretion of retagabine and/or its metabolites in breast milk.

Reference (shown after audit): Dýrarannsóknir hafa sýnt útskilnað retigabíns og/eða umbrotsefna þess í mjólk.

Review: Animal studies becomes animal descriptions; stated evidential study type changes.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Dýralýsingar hafa sýnt að retagabín og/eða umbrotsefni hans skilst út í brjóstamjólk.

</details>

<details><summary>final_semantic_review #289 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:80

English: But the new study using the VLT has found that much of the stars energy is being absorbed and scattered by dust clouds before it gets to Earth - it is actually more luminous than previously thought and among the brightest stars known.

Reference (shown after audit): Nýja rannsóknin með VLT hefur hins vegar sýnt fram á að rykský gleypa og dreifa stórum hluta orkunnar sem stjarnan gefur frá sér áður en hún berst til jarðar - hún er því í raun miklu bjartari en áður var talið og er meðal skærustu stjarna sem vitað er um.

Review: All corrupt stellar-energy absorption/scattering and luminosity inference; several changeEarth toEurope/USA.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Nýjar rannsóknir sem nota VLT hafa fundið að mikið af stjórniðýni viðfallist og skilur með þegi áður en það kemur til Jörðar - það er alveg meira ljóslegara en þegar áður var hægt að hugsa en í ljós er vænt um flestir stjörnunum.

Candidate 1: Nýjar rannsókna með VLT-ferlinu kemu í ljós að mikið af starhreinun er orðin af þvertkollum áður en við komum til jarðarins, Það er frábærlega ljósari en fyrr áður varð við og með þeim berjast þær best ljósar starur sem þeir kalla.

Candidate 2: Nýjar rannsóknir sem nota VLT-hlutlið hafa fundið að mikið af stjörnuhlýsingu er sæknað og tilraunandi hérum af stynum áður en þetta kemur til Evrópu. Í fyrstu var þetta myrkeðari en áður var fengið að segja og það er einnig heita.

Candidate 3: Nýja rannsóknin sem notuð er VLT-geimluprófunu hefur fundið að einnig hefur þeir sunnan efnis þar sem um fólk er að grunna undan flæðjuflótum áður en þau koma til Jörðar. Þau eru áketlegri en fyrir þennan stund varðandi áhættu og líf í þynggstum stjörnur sem kunnar hefur verið.

Candidate 4: Í nýjum rannsókninni sem notað er með VLT hefur fundist að miklum eldsjálarljósum er safnað og skiljað með þverlausum í þar til það kom til Bandaríkja - það hefur eiginleika sem eru virkilega ljóseftir og núna er vitað að það sé ljósetra en áður varðar.

Candidate 5: Nýja rannsóknin með VLT-hlutfalli hefur fundið að miklar hlutar starfrarinn er afsökunar og sent af kosin færi áður en þetta nær til Jörðinnar. Efra um síðkunnar er þetta meiri ljóstryggingi en í fyrra hugtaðist. Á öðrum stað eru þær besta sjóar sem þjóðin hefur þekkt.

Candidate 6: Nýjan rannsókn sem hefur verið fram á með því að nota VLT hefur sýnt fram á að mikil orkujafur af stjörnunum er reynast að taka við og skjóta í þverhlíðum íður fyrir að hann sé á Jörðinni. Hann er í alvöru sterkari en áður hafði verið hugsað um og er jafnvel stærsti alvarlegur kjarnastjóri.

Candidate 7: Nýji rannsóknin með VLT-ferlinum hafa fundið að mikill hluti starhugans er þróaður og íðraður af grasgöngum áður en hann fær sér í upptökuna á Jörðinni. Það er í raunum meiri ljósgræðingu en fyrr komið var í huga og í myrkri starra sem þeim sem þeim er þekkt.

</details>

<details><summary>final_semantic_review #290 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:63

English: “Studying afterglows is vital to further our understanding of the objects that become gamma-ray bursts and what they tell us about star formation in the early Universe,” says the studys lead author Jochen Greiner from the Max-Planck Institute for Extraterrestrial Physics in Garching bei München, Germany.

Reference (shown after audit): „Það er nauðsynlegt að rannsaka glæður blossanna svo auka megi skilning okkar á þeim fyrirbærum sem mynda gammablossa og hvað þau segja okkur um myndun stjarna snemma í sögu alheimsins“ segir Jochen Greiner, aðalhöfundur greinar um rannsóknina, og stjarneðlisfræðingur við Max-Planck-Institut für extraterrestrische Physik í Garching við München í Þýskalandi.

Review: All corrupt afterglows, gamma-ray bursts, earlyUniverse or scientific affiliation.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: „Þú skilur eftirlit með lengu gömluhaldanir, er mikilvægt að fjárfesta þér að skilningi á hvernig efnin sem verða á gömluhaldanir verða orkugrupp sem ekki eru lengur í gangi, og hvað þeir segja um formaðgerð starfa á fjannaðri alheiminu,” segir Jochen Greiner, leikfólk við M. P. M. íframleiddisþjónustu í Garching bei München, Þýskalandi.

Candidate 1: „Ef útsetningu er að ræða er mikilvægt að frumgreina þekkingu á verkenum sem teljist hjartbroti og hvað sem þær sýna út um starnafnunarþrýsting í upphafur almenningsins“, segir Jochen Greiner, leiðsögnir útskýringarar í Max-Planck Instítu fyrir útræðastofnun í Garching bei München, í Þýskalandi.

Candidate 2: „Vísindaleikur á eftirgöngu hjálpar til að munurka á þeim hlutum sem koma til staðar og veita okkur upplýsingar um framleiðslu stjarna í upphendi Allhymningunnar“, segir Jochen Greiner, fyrirmælið í Mtóplæki fyrir útrýmint um útgifnanir í Pálskefnisins í Garching bei München, Þýskalandi.

Candidate 3: „Það er mikilvægt að læra eftirgæðurnar til að frekara skilgreina lýs og það sem þær segja um formun umhverfisins á áranlegri útstæðum“, segir Jochen Greiner, leiðsögnur við rannsóknina, úr Max-Planck viðskipunaríthópur í Garching bei München, Þýskaland.

Candidate 4: „Mögnun í eftir þegarferli er mikilvægt við að auka skilningi á þeim virkum sem koma í gátrærjarbraut og því hvað þeir veita okkur um skripið upptöku stjarna í upphafi alheimsins“, segir Jochen Greiner, fyrsti launorkur af Max-Planck-Innið fyrir útflutningsfísíki í München, Ráðstöðvaði Garching.

Candidate 5: „Studhæfandi eftirfarunar er mikilvægt til að frekari skilgreina eiginleikar áhlutunanna sem verða gammarbrýslur og hvað þær veita okkur um formið stjörnu í upprunalegum Allsheiminu“, segir Froðamannur Jochen Greiner frá Max-Planckinetmannaríkinu fyrir útflutningaskipti í Garching bei München, Þýskalandi.

Candidate 6: „Þóskistýrðir eru mikilvægir til að koma áfram og þekjast upprunalegar einkenni greinirnar sem verða gammtur, og því hvað þær veita um formun starða á orðinni heitar lýndi,” segir Jochen Greiner, leiðsöguartarfangur af Max-Planck-Innlatinum fyrir útanjörð og heildarfræði í München.

Candidate 7: „Rannsókn eftir frumum er mikilvægt að frekara skilgreina aðgerðir sem verða gátrænum og hvað þær veita okkur um formun á stjórnum á upprunalegrum heimi“ segir Jochen Greiner, fyrstur yfirleitt rannsóknari heimasambandi skáldstjórnarinnar í Garching bei München, þýskalandi.

</details>

<details><summary>final_semantic_review #291 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:ema:607

English: Since the possibility of increased risk of cancer development in patients with newly diagnosed dysplasia treated with infliximab is not established, the risk and benefits to the individual patients must be carefully reviewed and consideration should be given to discontinuation of therapy.

Reference (shown after audit): Þar sem ekki hefur verið gengið úr skugga um hugsanlega aukna hættu á krabbameinsmyndun hjá sjúklingum með nýgreindan misvöxt sem fá infliximab, verður að endurskoða gaumgæfilega áhættu og ávinning fyrir hvern sjúkling um sig og íhuga á að stöðva meðferð.

Review: Dysplasia/risk-benefit premise corrupted and pregnancy introduced.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þar eð líkamað er ekki staðfest að hægt sé að aukna áhættu á krabbamein hjá sjúklingum með nýttu skugga á óþrýstingum sem meðferð með infliximabi hefur verið á meðgöngu, skal taka tillit til þess hve líklegt er að þeir sjúklingar verðið hafa áhættu og áhættu og þægð og þægð og skal taka tillit til þess að hætta meðferðinni.

</details>

<details><summary>final_semantic_review #292 · old08 · G8 · technical_short · F</summary>

Source ID: p13official21:test:eea:1471

English: Prices including all taxes, levies and VAT.

Reference (shown after audit): Verð með öllum sköttum, álögðum gjöldum og VSK.

Review: No taxes/levies/VAT list preserved.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Verð, sem inniheldur allt skatta, sáskatt og alíverði.

Candidate 1: Verðið með öllu inntök, skatt, skipulaga og allan skatta.

Candidate 2: Verðið innihaldsverð, þar með talsverð allra skatta, reiknaðar skattamál og almenningverð.

Candidate 3: Verð í tengslum við öll skatta og skattaásetu og viðskiptavettvang.

Candidate 4: Verðin bæði með allt bruður, þágrétt og VMT.

Candidate 5: Verðið, þ.m.t. öll skatta, fengur og yfirvinnu.

Candidate 6: Verðið innihaldi öll skatt, skattaþjónustu og vatnsgeim.

Candidate 7: Verðið innihalda öll skatta, verðskatt og verðbúnað.

</details>

<details><summary>final_semantic_review #293 · old08 · G8 · technical_short · F</summary>

Source ID: p13official21:test:eea:679

English: This relates to the gross earnings paid during the reference year.

Reference (shown after audit): Þetta lýtur að vergum tekjum sem eru greiddar á viðmiðunarárinu.

Review: Gross earnings/reference-year payment not retained in any candidate.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Það tengist fullgöngugjöfum sem fengir í viðmiðunarárinu.

Candidate 1: Þetta varðar hreinsku greiðslurnar sem lostuð voru á viðmiðunardýrum.

Candidate 2: Það tengist útgjöldum, sem fengðir eru í viðmiðunarárinu.

Candidate 3: Þetta tengist greiðslu greiðslustaddið eftir tímabilinu.

Candidate 4: Það tengist beinni reikningsskilum sem greiddar eru fram á viðmiðunararéttarárinu.

Candidate 5: Þetta tengist hreint gjöldum sem fengnu var í viðmiðunarsveitinni.

Candidate 6: Þetta tengist heildarúðverðum sem fengnar á viðmiðunararéttaríkið.

Candidate 7: Þetta tengist frumsímanum sem gefin eru á tímabili grundvallararársins.

</details>

<details><summary>final_semantic_review #294 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:43

English: Where plant protection products containing the active substance are intended to be used in cold climatic conditions, the tests have to be conducted where DT50lab, determined at 10 °C and at a moisture content of the soil related to a pF value of 2 to 2,5 (suction pressure) is greater than 90 days.

Reference (shown after audit): Þegar nota á plöntuvarnarefni, sem innihalda virka efnið, í köldu loftslagi verða prófanirnar að fara fram þar sem DT50lab er meira en 90 dagar, ákvarðað við 10°C og í jarðvegi með rakainnihaldi sem miðast við pF-gildi 2 til 2,5 (sogþrýstingur).

Review: All corrupt plant-protection/cold climate/soil moisture/pF/suction-pressure test conditions.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Ef óhólfunarvöru, sem inniheldur virka efnið, er ætlað að nota í kolförum skal prófanir gerðar þegar DT50lab, ákvarðað á 10° C og með móðurfjarðum í jarðvelinum sem tengjast 2 til 2,5 (þrýstingstryggi) er meira en 90 daga.

Candidate 1: Vegna þess að búnaður til verndar gegn planata skal nota þau á kjánalegu unntökum skal prófunum gera að lokinni DT50lab þannig að þar sem það er ákvarðað 10°C og þegar máttmæt liðin í-gemningi er 2 til 2,5 (vöðvaþrýsting), er hún 90 daga meiri en 90 daga.

Candidate 2: Við notkun örveraþjónustaefna sem innihalda virka efni í góðu veitandi skyni skal prófunin milli slúðra veðri vera þar sem DT50lab, ákvarðaður málið á hitastig 10 °C og geymslu í magfarum í geðju sem tengist pF-gildi um 2 til 2,5 (slúðunarpísi), er hærri en 90 daga.

Candidate 3: Ef búnaðarverki, sem innihalda virka efni, vilja vera notaðar við kyllumkrona skal prófunin gerð að því að skalræði skýrsluvarnsins DT50lab, á 10 °C og hversu miklu úðulöngum, sem gætu verið í landbæri sem tengist fjölmökum 2 til 2,5 (þrýstingabreytingu), er gert háð 90 dögum.

Candidate 4: Ef búnaðarverki með virka efni er tekið til notkunar í koldyrtum viðkomandi veðri skal prófanir stendur í miðlökum þar sem DT50lab, ákveðið á 10°C og heildarlengd á vefi sem tengist pF-gildi 2 til 2,5 (þrennsligsþrýstingi), er stærra en 90 daga.

Candidate 5: Þegar við á til að nota plöntufóðurofna, sem innihalda virka efninu, í koldólarhæðum skal prófunin gerð á þeim stöðum þar sem vökvahvörf skjæðarins (DT50lab) er ákvarðaður við 10° C og er meira en 90 degi (þækkumörk) að hálfu þjófhræðis (suction pressure) þar sem hvarðina er í 2 til 2,5 (suction pressure) skílagsstofn (moisture content).

Candidate 6: Ef efnahagssýni í plöntuverningavörum er viðeigandi efnið bætt við kærustu hagsmuna skulu prófurnar gerðar þegar DT50lab, ákvarðað við 10°C og þegar þungumæti geislsins, sem tengist pF-gildi 2 til 2,5 (tryggingavörð), er stórvært meira en 90 daga.

Candidate 7: Ef er ætlað að nota pulveraveitakerfi með virka efninu í kolflokkunalegum orkumíðunarkerfi skulu prófanir gerðar þar sem DT50lab, ákveðinn á 10 °C og við þurrkaðni í blöndunarsíma er efnislega 2 til 2,5 (æðingarklæði) meiri en 90 dögur.

</details>

<details><summary>final_semantic_review #295 · old08 · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:514

English: This star formation region is forming many stars.

Reference (shown after audit): Þetta stjörnumyndunarsvæði er að mynda margar stjörnur.

Review: No correct star-formation-region noun/process; closest3 uses star-straightening rather than formation.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þessi starfsleið sem æxlir er er að þeim mætt um margra stjörnu.

Candidate 1: Þessi störverufrum er að frumu margum störrum.

Candidate 2: Þessi starfkraftsjafn hefur smíðað marga starnar.

Candidate 3: Startréttunarsvæðið er að framleiða marga stjörnur.

Candidate 4: Þessi stjörnustöð við formunarmál er að þeirri stigi að hún rækni mörg stjörnu.

Candidate 5: Þessi starfsvatanum eru mörgir stjörnur sýnileg.

Candidate 6: Þessi starfsstofnir eru að þurfa að gera margar stjörnu.

Candidate 7: Þessi stegurðvarðar margir stjörnur.

</details>

<details><summary>final_semantic_review #296 · old08 · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:1198

English: The new observations are thus the first direct confirmation of such models.

Reference (shown after audit): Niðurstöður mælinganna eru þar af leiðandi fyrsta beina staðfestingin á útreikningunum.

Review: No complete new observations as first DIRECT confirmation of models;3 substitutes assessments and particular confirmation.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Nýjum athugunum er svo fyrsta andskipti öryggismálanna sem settu framan í rannsóknir.

Candidate 1: Nýjar sögusvarsið eru þar sem fyrst eru lánstærðar lýðbeinar sannprófun á slíkum líkinum.

Candidate 2: Nýjar útskýringar eru svo fyrsta dreifandi staðsett samræmingar á slíkum líkama.

Candidate 3: Nýju matin eru þannig fyrsta sérstakt staðfestingu slíkra líkana.

Candidate 4: Nýjar upplýsingar eru svo fyrsti orðin að tilgreina slíkar líkin og mælir.

Candidate 5: Nýjar tölur eru svo fyrstu beint samræmdar sannir á slíkum líkum.

Candidate 6: Nýju sannprófunarnar eru sár tveggja að því er varðandi fyrsta, ræktu niðurstöðu uppá slíkum líkur.

Candidate 7: Nýjum athugunum er svo fyrsta bregðisangreindur sannprófun á slíkum líkum.

</details>

<details><summary>final_semantic_review #297 · old08 · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:434

English: The guest of honour was the President of Chile, Sebastián Piñera.

Reference (shown after audit): Sebastián Piñera, forseti Chile, var heiðursgestur.

Review: Guest of honour and President ofChile not preserved; several change country toChina.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Viðgötvini var Predósin í Kaledó, Sebastián Piñera.

Candidate 1: Forskniráðinn Árávelss Konungarinn var Sebastián Piñera.

Candidate 2: Hvelpesska afmælislokkann var forsetur Chile, Sebastián Piñera.

Candidate 3: Götvíninn var Prunksjátnum í Kína, Sebastián Piñera.

Candidate 4: Éginn huldmyrkinn var prýmístur Kína, Sebastián Piñera.

Candidate 5: Eldinn hófst var Cordoba-yfirvaldið, Sebastián Piñera.

Candidate 6: Viðskiptamenninn í farni var Prýsmennin í Kína, Sebastián Piñera.

Candidate 7: Vörsluhöfundurinn var Sebastián Piñera, prefánur í Kallí.

</details>

<details><summary>final_semantic_review #298 · old08 · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:349

English: The results described here use some of these Science Verification data.

Reference (shown after audit): Gögnin sem notuð voru fyrir þessa rannsókn var að hluta til aflað við þessar prófanir.

Review: No ScienceVerification-data use relation; monitoring/evidence/necessity substitutes do not preserve data identity.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Nákvæmnið sem hér ræðir hefur viðeigandi útgáfum vísindalegu staðreyndar.

Candidate 1: Það hlutverk sem hér eru lýst er fram í vottunum sem hér eru sýnt.

Candidate 2: Þar sem lýs eru niðri vörsluð áframhaldandi upplýsingarnar sem eru öðruvísi fyrir verndasjákvæmd.

Candidate 3: Niðurstöðurnar sem hér eru lýst nota nokkurum þessum sönnunargögnum frá vöktunni.

Candidate 4: Niðurstaðin sem hingað er lýst þar nota einhvern af þessum gagnanum sem gefnar eru til að sannprófa nauðsyn.

Candidate 5: Þar sem lýst er hér gildir að þessar Cellular Data geti nýtt þátt i þær útreikningar.

Candidate 6: Niðurstaðin, sem hér er lýst, notar einhverjar þessar vitsunarstilliliðar.

Candidate 7: Námartarfagnirnar sem hingað er lýst eru notaðir fyrir tilvísunarskammdar.

</details>

<details><summary>final_semantic_review #299 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:ema:970

English: In patients with mild hepatic impairment (Child-Pugh A), there was no significant changes in pharmacokinetics compared with normal healthy volunteers.

Reference (shown after audit): Hjá sjúklingum með væga skerðingu á lifrarstarfsemi (Child-Pugh A) voru engar marktækar breytingar á lyfjahvörfum samanborið við heilbrigða sjálfboðaliða.

Review: Mild impairment and healthy-volunteer comparator changed to unclear function and healthy patients.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Í sjúklingum með mjög leifa lifrarstarfsemi (Child-Pugh A) var engin merkileg breytingar á lyfjahvörfum samanborið við heilbrigðum heilbrigðum sjúklingum.

</details>

<details><summary>final_semantic_review #300 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eso:1181

English: By combining light from three of the VLTIs 1.8-metre Auxiliary Telescopes with the AMBER instrument, this facility allows astronomers to see details equivalent to those a telescope with a mirror of 85 metres in diameter would see.

Reference (shown after audit): Með því að sameina ljós frá þremur 1,8 metra aukasjónaukum VLTI við AMBER mælitækið gátu stjörnufræðingar greint smáatriði sem væri aðeins gerlegt með sjónauka með 85 metra spegilþvermál.

Review: Auxiliary telescopes, astronomy observers and mirror-diameter comparison corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þegar ljós frá þrjú VLTIs 1,8 m stórum aðstoðarþrýstingum er samsettur og AMBER-ökurinn er notað getur stjórnendur leynslu til að sjá þá upplýsingar sem þeir sjá með 85 m stærð ámiðsliðsleysis.

</details>

<details><summary>final_semantic_review #301 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:eea:1855

English: The product must be easily recyclable.

Reference (shown after audit): Það verður að vera auðvelt að endurvinna vöruna.

Review: Product becomes action and recyclable becomes repeatable.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Aðgerðin skal vera auðvelt að endurtekja.

</details>

<details><summary>final_semantic_review #302 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:eea:21

English: Soils used must, wherever possible, be freshly sampled.

Reference (shown after audit): Jarðvegssýni verða ætíð að vera nýtekin sé þess nokkur kostur.

Review: Soils/fresh sampling replaced by acidified air/new display.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Sýruður loft er þarf, þar sem það er hægt, að nota nýja sýningu.

</details>

<details><summary>final_semantic_review #303 · old08 · G8 · technical_medium · P</summary>

Source ID: p13official21:test:ema:1495

English: Check again to make sure the correct dose of Tevagrastim is in the syringe.

Reference (shown after audit): Athugaðu aftur hvort rétt magn Tevagrastim er í sprautunni.

Review: Candidates2/6 preserve rechecking correct Tevagrastim dose in syringe.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [2, 6]

Candidate 0: Kanna þetta aftur til að vissu hvort eftirfarandi skammtur af Tevagrastim er í sprautunni:

Candidate 1: Kannski er ekki rétt sýringjan sem er í undirhaldi. Rekstu þá eftir.

Candidate 2: Kannaðu aftur að það sé réttur skammtur af Tevagrastim í sprautunni.

Candidate 3: Kannski skortir stuðninginn eftir það að Tevagrastim hafi ekki verið skammturinn í sprautunni.

Candidate 4: Kannski er ekki rétt sýruþyppslegur skammtur í sprautunni.

Candidate 5: Kannaðu aftur til að ekkert séð er annað en réttur skammtur af Tevagrastim í sprautunni.

Candidate 6: Kannaðu aftur til að vissulega sé réttur skammtur af Tevagrastim í sprautunni.

Candidate 7: Kannið aftur til að staðfesta að rétt áföng Tevagrastim sé í sprautunni.

</details>

<details><summary>final_semantic_review #304 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:1323

English: If refills are not provided, the weight of the total primary packaging shall not exceed 3,7 g per wash for tablets and 1,7 g per wash for all other products.

Reference (shown after audit): Ef áfyllingar eru ekki í boði skal þyngd grunnumbúðanna í heild ekki vera meiri en 3,7 grömm á þvott ef um er að ræða töflur og 1,7 grömm á þvott fyrir allar aðrar vörur.

Review: All corrupt refill/primary-packaging/per-wash constraints; one mixes Chinese text.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Ef ekki er veitt yfirþynningar er þvermæri heildarpakkans hætta ekki af 3,7 g á þynningu fyrir töflur og 1,7 g á þynningu fyrir önnur vörur.

Candidate 1: Ef viðbótarnotaður er ekki fyrir hendi skal þétta allra fyrsta pakkanaðana nemur ekki lengur en 3,7 g á þrétt og 1,7 g á þrétt fyrir öll annar vörur.

Candidate 2: Ef ekki er veitt viðbótarefni skal heita heildarfjarð innihaldsefnisins, þar með talið lægsta hlutfallsleysatabla og 3,7 g á hvatningu fyrir töflur, og 1,7 g á hvatningu fyrir hinu önnur afurðir.

Candidate 3: Ef ekki er gefið inn nýja uppfærslu skal hægt er að hægt verður að hafa þann háðagni heildarinnar fjölda íbúðarinnar sem er hægt að hafa 3,7 g fyrir hleðslu á töflum og 1,7 g fyrir hleðslu á öllum öðrum afurðum.

Candidate 4: Ef innihaldsskiptun er ekki veitt skal hæð almennum upptökuflokks stöðva ekki áfram en 3,7 g fyrir smák表和 1,7 g fyrir öll annars líftrygginga.

Candidate 5: Ef ekki er veitt þær endurfarar eru hægt ekki að hafa hærri þyngd heildarprjónarinnar en 3,7 g á hreinsun fyrir töflur og 1,7 g á hreinsun fyrir öll annar vörur.

Candidate 6: Ef innihaldsmeðferð er ekki veitt skal hverja almindlausar pakkninga 3,7 g á slys fyrir töflur og 1,7 g á slys fyrir öll aðrar vöru.

Candidate 7: Ef ekki er veitt neðan endurboð skal hægt ekki að þyngd tölfræðilegra pakkningarins sé meiri en 3,7 g á þynningu fyrir töflur og 1,7 g á þynningu fyrir öll aðrar vöruvarnir.

</details>

<details><summary>final_semantic_review #305 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:1059

English: The domestic output price index for an economic activity measures the average price development of all goods and related services resulting from that activity and sold on the domestic market.

Reference (shown after audit): Vísitala innlends framleiðsluverðs vegna atvinnustarfsemi mælir meðalverðþróun á öllum vörum og tengdri þjónustu vegna þeirrar starfsemi sem eru seldar á innanlandsmarkaði.

Review: No correct domestic output-price-index/average-price-development definition.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Í innbyggðum verðferðarstöðu fyrir eigin tryggingakerfi merki það ásthægt fjárfestingsþróun allar vörur og hamingjaða þjónustu, sem er afblönduð af tryggingakerfinu, og er söluð á landamáta.

Candidate 1: Efnahagssiglinginn fyrir heimila þá vegna efnahagslega starfsemi talar um meðaltali útgjöld frá öllum varða og tengd þeim aðstoðarverjunum sem er afleiðt af starfsemi hennar og deild um heimilargörðinn.

Candidate 2: Verkþáttastýringarverðmæt á innlandri markaði mæli meðaltali verðvörnaraðræði öllu vörja og tengdra þjónustu af því veikun og sem seld er á innlandri markaði.

Candidate 3: Innihaldsverðsforðakeðju fyrir heimilisstofnun mestar verða um áhættuþurrðir frumsóknir og viðbætur sem tækja af henni og er selðar á heimilismarkaðinni.

Candidate 4: Ístaútpronsleikarefnumarkti fyrir efnahagsskruttu metur meðall verðþráttir á öllum vörum og tengdum þjónustu sem af þeirri krutta verða og einfaldaðir á innri markaðinn.

Candidate 5: Innimatið fyrir innflutur á markaðarverkir fyrir eðlilega starfsemi metur meðaltal breytur á verðbúnaði alla vörur og tengdar þjónustu sem tilvísanlegt starfsmáli gerir og er sátt við sal á innlandri markaði.

Candidate 6: Innihaldsgildi útsettur markaðsgreiningar fyrir efnahagslegri starfsemi mægir meðaltal markaðsgöngu yfir allar vörur og tengdar þjónustu sem tiltekinn starfsemi þykir og er seldur á innlandetur markað.

Candidate 7: Innhaldsverðindurinn fyrir innlend útgáfa við skilvirðisstöðva, einkums, metur meðferð á meðaltali verða þegar allar búnaðurir og tengdar þjónustu, sem af þeirri starfsemi er eigað, eru saldar á innlendum markaðinni.

</details>

<details><summary>final_semantic_review #306 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:1190

English: In these cases it is therefore recommended that the Zonegran total dose should be rounded up or down to the nearest available dose that can be achieved with commercially available capsule strengths of Zonegran (25 mg, 50 mg and 100 mg).

Reference (shown after audit): Í slíkum tilfellum er því mælt með því að heildarskammturinn af Zonegran sé minnkaður eða stækkaður í næsta skammt sem hægt er að gefa með hylkjum af þeim styrkleika af Zonegran sem fáanleg eru (25 mg, 50 mg og 100 mg).

Review: All corrupt rounding/nearest capsule dose; some change drug name or invent doses.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Í þessum tilvikum er þannig mælt fyrir um að Vissfold hliðarleysi sé nr. aukin eða minnukun við fjarlægan skammt sem er með hæfilegum styrk í skopula af Vissfold (25 mg, 50 mg og 100 mg).

Candidate 1: Í þessum tilvikum er til að mæta upp eða neina upp staðlið 100% af tölfræðilegum háttastærðum ampullanna af Zonegran (25 mg, 50 mg og 100 mg) sem eru flestar og fágar sem eru til að nota.

Candidate 2: Í þessum tilvikum má ákveða að hún sé öðruþáttuð út eða inni í næstu aðgengi sem ekki eru fyrir裱aðanhaldar styrk í裱upósum Zonegran (25 mg, 50 mg og 100 mg) sem kröfuð er til.

Candidate 3: Þegar um þetta komið er má því kveðið á um að hvarða geislaskammta af Zonegran öllum skammtum sem eru til gömlu, þ.e. 25 mg, 50 mg og 100 mg, eða 12,5 mg, 25 mg og 50 mg, annars af stað.

Candidate 4: Þegar um þetta stendur er því mælt fyrir um að klára að allt skammtið af Zónegran ætti að vera næstum nægilegt – eða minni – til að ná að hægt sé að nota yfir 25 mg, 50 mg og 100 mg af Zónegran í töfluspöllum sem eru haft samvinnu á.

Candidate 5: Í þessum tilvikum má því mælt fyrir um að flugmóður hafi að 25 mg, 50 mg og 100 mg sem er næstum hægt að fá, með notkun hópna-flugmanna af völdum Flugmóðar (25 mg, 50 mg og 100 mg), flugmóður innihaldaðar í hópnum.

Candidate 6: Í þessum tilfellum má því mæla upp eða neyta nærummi í að úthreinstu með nýttu, auðlinduðu þar með að 25 mg, 50 mg og 100 mg, með áfengd meðvælaðum hylkum úr Zonegran.

Candidate 7: Mælt er þannig með því að endurhæfa eða draga úr stærðli Zonegran (25 mg, 50 mg og 100 mg) að því er varðar heildarstofnar sem rekstrarverkun er að höfða og fá í allt að aðstæðum.

</details>

<details><summary>final_semantic_review #307 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:63

English: The placement of these devices in the soil should not result in preferential flow paths.

Reference (shown after audit): Staðsetning þessara tækja í jarðveginum má ekki breyta farvegi vatnsins.

Review: Device placement in soil and preferential flow paths not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það ætti ekki að þessu að fljótun á þessum stöðum sé afleiðing á þar til þeirra.

</details>

<details><summary>final_semantic_review #308 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eso:760

English: Extreme stars like the two components of VFTS 352, play a key role in the evolution of galaxies and are thought to be the main producers of elements such as oxygen.

Reference (shown after audit): Ofsafengnar stjörnur eins og í VFTS 352 leika lykilhlutverk í þróun vetrarbrauta og eru taldar meginuppspretta frumefna á borð við súrefni.

Review: Oxygen becomes fear; extreme-star/element-production relation corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Hvorkar starströndir eru eins og tvo hlutir í VFTS 352, eru mikilvægir í þróun galaxanna og eru hugsanlega að verða að verða að framleiða efnin eins og óttan.

</details>

<details><summary>final_semantic_review #309 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:400

English: ESPRESSO will feature radial velocity precision of 0.35 km/hour or less.

Reference (shown after audit): ESPRESSO mun ná að greina sjónstefnuhraða niður í 0,35 km/klst eða minna.

Review: Radial velocity not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: ESPRESSO mun vera með 0,35 km/hora eða minni nákvæmni á hjálpstæðingu.

</details>

<details><summary>final_semantic_review #310 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:611

English: “With Mars losing that much water, the planet was very likely wet for a longer period of time than previously thought, suggesting the planet might have been habitable for longer,” said Michael Mumma, a senior scientist at Goddard and the second author on the paper.

Reference (shown after audit): „Þar sem Mars hefur glatað svo miklu vatni var reikistjarnan líklega blaut í lengri tíma en áður var talið, sem bendir til að Mars gæti hafa verið lífvænleg í lengri tíma,“ sagði Michael Mumma, vísindamaður við Goddard og annar höfundur greinarinnar.

Review: All corrupt wetness/habitability inference or author role/location.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: „Með því að Mars ótti hat annars vegna vatns sólust planetinn miklu lítilu lengi og ekki seinna, og tæki að hann hefði verið ígengibundinn yfir lengur,” sagði Michael Mumma, stórsambandseðilur á Goddard og annar gögnunni í þessari grein.

Candidate 1: “Þegar Mars hefur mislitið svo miklu vatni þá var planetið mjög líklegt að vera vatnslökur lengra tíma en fyrr áður hefði verið hugsað, og leiðartækið mætti því hefja líf fyrir lengur,” segir Michael Mumma, þriðju starfsmann í Goddard og annarum athafnanum á þessari rannsókninni.

Candidate 2: „Með því að Mars margt vandnar vandarsvæði var úr lofti var planeturinn mjög líklegt að vera þynnt í lengra tíma en var fyrst leitt að því, mælt með af Michael Mumma, nýttu nákvæmni, stjórnandi fyrirsæi og þriðja skrána af rannsóknarheimnum.

Candidate 3: „Fyrir marsins aðlaðan vitnin er verður örugglega útbrotið af vatni, planeturinn var líklegt að vera vatnsskurt í lengri tíma en áður var hugsaður að því að það væri fyrir hálfu setuð.“, sýndi Michael Mumma, góðar líkinu í Goldvidar og annar umræðastofnir í greininni.

Candidate 4: „Vöðvaði Mars ofan svo mikið úðar, var planetinn líklegt að vera úður lengur en fyrr og til og þar til þeir voru að finna, sem mælir um möguleika á stjórnvöxtu fyrir lengur.“, sagði Michael Mumma, stjórnandi starfræknar kennarainnu á Goddard og annar aðritur í þeirri bóka.

Candidate 5: „Með því að Mars lári í þessu mikið vatni var planetinn líklega úti sýntur lengur en fyrr átti að hugsa var það líklegt að hann hefði verið íjafanlegur lengur í mögulegum tilvikum“, sagði Michael Mumma, stöðugur rannsóknarfræðingur í Goddard, og annar framkvæmdastjórnand í þessari rannsókn.

Candidate 6: „Með því að Mars hafi misstuðlað svo mikið af vatni, var planetinn líklega reyndar vatninn lengur en við öðru högg og enda valdaði að planeturinn hefði verið æxulegur lengur en varðandi tækið.“, sagði Michael Mumma, stórfræðingi á Goddard og annar skráningaraðilinn á papierinu.

Candidate 7: „Með því að Mars hafi misstuðlað svo mikið af vatni komið planetið í ljós að því er staðfestur að hann væri um lengra tíma þungur en áður varðið var, til að sýna að hún hefði getið verið íhlutandi um lengra tíma.“, sagði Michael Mumma, fyrsta starfsmeiri að Goldberg og sömu skráningaraðila fyrir rannsóknarpaperina.

</details>

<details><summary>final_semantic_review #311 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:850

English: When implementing this strand the Commission will in particular ensure consistency and complementarity with the activities conducted by other Commission services or by European agencies; in particular, the European Foundation for the Improvement of Living and Working Conditions and the Community RTD Framework programme and the European Centre for the Development of Vocational Training (Cedefop).

Reference (shown after audit): Við framkvæmd aðgerða í þessum flokki mun framkvæmdastjórnin sérstaklega sjá til þess að þær séu í samræmi við og komi til fyllingar starfsemi sem aðrar þjónustugreinar framkvæmdastjórnarinnar eða evrópskar stofnanir stýra, einkum Evrópustofnun um bætt lífskjör og starfsskilyrði, rammaáætlunbandalagsins um rannsóknir og tækniþróun og Evrópumiðstöð um þróun starfsmenntunar (CEDEFOP).

Review: All corrupt institutions/complementarity; candidates0/2 repeat and truncate.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0 [TRUNCATED]: Þegar framkvæmdastjórnin reiknið þessa rúðar verður skulu, einkum, tryggja samræmi og samræmi við starfsemi annarra aðila framkvæmdastjórnarinnar eða evrópskra fyrirtækja og einkum, Evrópuaðilinn fyrir að auka lífshússun og starfshússun og ráðgögn Störfsbandalags Bandalag Bandalag Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags Bandalags B

Candidate 1: Svo framkvæmdarstjórnin mun einkum tryggja samræmi og næmi menntun. Meðal þess skulu vera þýðing eðlisbúnaðsins fyrir þjónustu og virkunarstofnanefndar ESB og ráðstöfunaráætlun Evrópu fyrir bærum áætlunir og Evrópuforðin fyrir þjónustu þjónustu og virkunarstofnanefndar ESB.

Candidate 2 [TRUNCATED]: Þegar framkvæmdaráðið framkvæmdir þessi strönd skal einkum tryggja sjálfstættar og samræmistykjur við Starfsemi annara þjónustu við framkvæmdaráðstæður eða evrópskrum stjórnvöldum, einkum EFB-stöðvarinn „Eftirfarandi yfirborð fyrir gagnvart líf og starfsmál“ og fylgjandi eldsta skrifstofu Bandalagsins „Ráðstöfunarvettvangur til ráðstöfunar fyrir framkvæmd launþjónustu“ og „Eftirfarandi fyrirbæri fyrir starfsmál“ og „Eftirfarandi eldsta skrifstofu Bandalagsins „Eftirfarandi fyrirbæri fyrir starfsmál“ og „Eftirfarandi eldsta skrifstofu Bandalagsins „Eftirfarandi fyrirbæri fyrir starfsmál“ og „Eftirfarandi eldsta skrifstofu Bandalagsins „Eftirfarandi fyrirbæri fyrir starfsmál“ og „Eftirfarandi eldsta skrifstofu Bandalagsins „Eftirfarandi fyrirbæri fyrir starfsmál“ og „Eftirfarandi eldsta skrifstofu Bandalagsins „Eftirfarandi fyrirbæri fyrir starfsmál“ og „Eftirfarandi eldsta skrifstofu Bandalagsins „Eftirfarandi fyrirbæri fyrir starfsmál“ og „Eftirfarandi eldsta skrifstofu Bandalagsins „Eftirfarandi fyrirbæri fyrir starfsmál“ og „Eftirfarandi eldsta skrifstofu Bandalagsins „Eftirfarandi fyrirbæri fyrir starfsmál“ og „Eftirfarandi eldsta skrifstofu Bandalagsins „Eftirfarandi fyrirbæri fyrir starfsmál“ og „Eftirfarandi eldsta skrifstofu Bandalagsins „Eftirfarandi fyrirbæri fyrir starfsmál“ og „Eft

Candidate 3: Þegar framkvæmdarmálastjórnin framkvæmdir þessa strandi munar m.a. á að úr skyni sé að tryggja samræmi og samanburð með hlutverkum annarra framkvæmdastjórnarinnar eða Evrópusambandskabannar, einkum Efanya Evrópu fyrir bregðslu á lífargilda og starfsemi og ráðstöfunaráætlun samkvæmt framkvæmdastjórnaráætlun Evrópu fyrir þróun læknarferlis (Cedefop).

Candidate 4: Þegar framkvæmdastjórnin framkvæmist þessa þróa er sérstaklega tryggja þann hátt að ástandi sé eðlilegur og viðbótarstætt við starfsemi aðra aðila framkvæmdastjórnarinnar eða ESB stöðvar, einkum Efabelaginu fyrir bæring á lífsháttum og starfsháttum og ráðstöfun fyrir almennu markaðsmálastjórnun milli Bandalagsins og Evrópu (RTD-Framkvæmdastjórnaráætlunin) og Evrópuðirkónunin fyrir næmingarþjálfun (Cedefop).

Candidate 5: Þegar framkvæmdastjórnin starfar á þessari þjónustu skulu meindra en að stöðugt og samrýmist starfsemi annarra þjónustureiðja af framkvæmdastjórninni eða evrópsku starfsstofnunum, einkum að Guðbúnarstöðin fyrir bregðabreytendum loftstaðar og fjarskipulag ESB og bærum á Evrópu fyrir þróun starfsmótnáms (Cedefop).

Candidate 6: Þegar framkvæmdastjórnin framkvæmdir þessa strandur skal einkum tryggja samræmi og samræmi við hríðir sem其他地区 framkvæmdastjórnar eða Evrópusambandsherja, sérstaklega Evrópuferðina um blöndun á starfshélfum og atvinnulega starfshálfum og ráðstöfun Evrópubandalagarinnar til þróunar starfsmanna (RTD) og Evrópuferðinni fyrir þróun starfsþjónustu (Cedefop).

Candidate 7: Þegar framkvæmdastjórnin útbúa þennan sætur muni hún einkum tryggja samræmi og skyndingu við starfsemi annarra framkvæmdastjórnarþjónustu eða við hóp evrópuflugverkafélaganna, einkum aðgerðir Evrópuþjóðarinnar fyrir að lækka lífshúðræði og starfshúðræði og framkvæmdaráætlun Evrópusambandsins, og Evrópuþjóðahús fyrir þróun rekstrangreindra starfs (evrópuþjónustuhúsið).

</details>

<details><summary>final_semantic_review #312 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:ema:2722

English: See also ‘Bleeding or bruising after you stop treatment in section 4.

Reference (shown after audit): Sjá einnig „Blæðingar eða mar eftir að meðferð er hætt“ í kafla 4.

Review: Bruising becomes a second bleeding item.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Sjá einnig „Blæðing eða blæðing eftir að meðferð stöðvast í kafla 4.“

</details>

<details><summary>final_semantic_review #313 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:1323

English: If refills are not provided, the weight of the total primary packaging shall not exceed 3,7 g per wash for tablets and 1,7 g per wash for all other products.

Reference (shown after audit): Ef áfyllingar eru ekki í boði skal þyngd grunnumbúðanna í heild ekki vera meiri en 3,7 grömm á þvott ef um er að ræða töflur og 1,7 grömm á þvott fyrir allar aðrar vörur.

Review: Refills/primary packaging/per-wash units corrupted; wash becomes dilution.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef ekki er veitt nýja innihaldseiningar skal þyngd almennta fyrsta pakkninga ekki vera meiri en 3,7 g á þynningu fyrir töflur og 1,7 g á þynningu fyrir önnur vöru.

</details>

<details><summary>final_semantic_review #314 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:512

English: Another team member, Ana Duarte Cabral from the Laboratoire d'Astrophysique de Bordeaux, France, emphasises that "the ALMA observations reveal the spectacular details of the motions of the filamentary network of dust and gas, and show that a huge amount of gas is flowing into a central compact region".

Reference (shown after audit): Annar meðlimur í rannsóknarhópnum, Ana Duarte Cabral við Laboratoire dAstrophysique de Bordeaux í Frakklandi, undirstrikar að „mælingar ALMA leiða í ljós stórkostleg smáatriði í hreyfingu gas- og rykslæðanna og sýna að geysimikið magn af gasi streymir inn að þéttasta svæðinu í miðjunni.“.

Review: Filamentary dust/gas network motions and compact-region inflow corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Aðra starfsfólkinnar, Ana Duarte Cabral frá Laboratóreynið Astarfræðilegra starfsskóla í Bordeaux, Frakkland, er að ræða að "ALMA-kröfunum sýna út frábærar upplýsingar um hreyfingarmörkum í þvafjöldum og gasi og sýna út að mikil fjölda gases fljúgi inn í miðbæjarbæjarbúnað".

</details>

<details><summary>final_semantic_review #315 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:ema:2690

English: Adverse effects not observed in clinical studies but seen in the rat and to a lesser extent in the mouse at exposure levels similar to human exposure levels and with possible relevance for clinical use were liver changes, indicating an adaptive response such as increased weight and centrilobular hypertrophy, fatty infiltration and increased liver enzymes in plasma.

Reference (shown after audit): Aukaverkanir, sem komu ekki fram í klínískum rannsóknum, en sáust hjá rottum og hjá músum þó í minna mæli, við skammta sem eru svipaðir meðferðarskömmtum hjá mönnum og skipta hugsanlega máli við klíníska notkun, voru lifrarbreytingar sem gefa til kynna aðlögunarsvörun eins og aukna þyngd og stækkun í miðju lifrarblaða, fituíferð og aukningu á lifrarensímum í plasma.

Review: Mouse/exposure and centrilobular hypertrophy/fatty infiltration corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Aukaverkanir komu ekki fram í klínískum rannsóknum en eru sýndar hjá rottum og í smíðum við minna hlutaðar staðbundna útbreiðslu og við útbreiðslu þannig sem hjá mönnum og með mögulega viðkomandi áhrif á klínísku notkun varu lifrarbreytingar sem sýna á viðbótarsvörun sem varðar aukningu þyngdar og þvöðruþrýsting á miðlæga hlutfalli, fæðingafyllingu og aukningu lifrarensíma í blóði.

</details>

<details><summary>final_semantic_review #316 · old08 · G8 · technical_short · F</summary>

Source ID: p13official21:test:ema:2323

English: It is important to drink plenty of water to avoid dehydration.

Reference (shown after audit): Mikilvægt er að drekka mikið af vatni til að koma í veg fyrir ofþornun.

Review: No correct plenty-of-water/dehydration prevention; outputs say avoid pregnancy/fluid/hydration or corrupt water amount.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Það er mikilvægt að drekka mikið af vatni til að forðast þungunar.

Candidate 1: Það er mikilvægt að drekka fíngustu vatns til að forðast vökva.

Candidate 2: Mikilvægt er að drekka mikið af vatni til að forðast vökvun.

Candidate 3: Það er mikilvægt að drekka fángnir vatn til að forðast vatnsþorn.

Candidate 4: Það er mikilvægt að drekka ofanlegan vatn til að forðast vökvanleg.

Candidate 5: Mikilvægt er að drekka fínt vatn til að forðast vatnshlýtingu.

Candidate 6: Það er mikilvægt að drekka nógu vatns til að unna vatnslausn.

Candidate 7: Mikilvægt er að drekk samkvæmt þessu í fullu vatni til að forðast vökva.

</details>

<details><summary>final_semantic_review #317 · old08 · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:1601

English: I don"t plan on wearing it that long.

Reference (shown after audit): Ég ætla ekki að vera lengi í honum.

Review: Not planning to wear it becomes not being worried.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ég er ekki með áhyggjur af þessu lengi.

</details>

<details><summary>final_semantic_review #318 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:908

English: This bridge, which has not been seen before (and is too faint to show up in this picture), is somewhat bluer than either galaxy, indicating that it consists of stars created in gas that was drawn away from NGC 1387 by the gravitational pull of NGC 1399.

Reference (shown after audit): Þessi brú hafði ekki sést áður (og er of dauf til að koma fram á myndinni) en hún er nokkuð blárri en hin vetrarbrautin sem bendir til þess að hún samanstandi af stjörnum sem mynduðust úr gasi sem NGC 1399 hrifsaði úr NGC 1387.

Review: Bridge colour, faintness and gravitational origin corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þessi brúð, sem er ekki séð áður (og er of fátætt til að sjá fram í þessari mynd) er smágrúður en annar eitt galáx, sem tekin er til að sýna að hún tekur upp af stjörnum sem eru skiptir í lofti sem eru hreint frá NGC 1387 af geðsýni NGC 1399.

</details>

<details><summary>final_semantic_review #319 · old08 · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:939

English: Put it in the envelope, Mrs. Rochon.

Reference (shown after audit): Settu hann í umslagið, frú Rochon.

Review: Envelope becomes traffic.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Settu hana í umferðina, frú Rochon.

</details>

<details><summary>final_semantic_review #320 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:136

English: Member State shall recognize the documents of compliance and safety management certificates issued by, or on behalf of, the administrations of third countries if it is satisfied that they demonstrate compliance with the provisions of this Regulation.

Reference (shown after audit): Aðildarríki skal viðurkenna þau samræmingarskjöl og öryggisstjórnunarskírteini sem stjórnvöld í þriðju löndum, eða annar fyrir þeirra hönd, hefur gefið út ef það er sannfært um að með þeim sé farið að ákvæðum þessarar reglugerðar.

Review: Safety-management certificates reduced to safety certificates and satisfied-condition omitted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Aðildarríki skal viðurkenna skýrslur um samræmi og öryggisvottorð sem stjórnvöld þriðja landa hafa gefið út eða út fyrir þau ef þau sýna fram á samræmi við ákvæði þessarar reglugerðar.

</details>

<details><summary>final_semantic_review #321 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:1716

English: In addition, the competent authorities of Gabon provided evidence to the Commission of the adoption of a new civil aviation code in May 2008, of the development of specific operating regulations for airworthiness and operations, and informed that the decision to establish an independent civil aviation agency (ANAC) was taken and should be promulgated in July 2008.

Reference (shown after audit): Þar að auki létu lögbær yfirvöld í Gabon framkvæmdastjórninni í té sönnun þess efnis að samþykktar hefðu verið nýjar reglur um almenningsflug í maí 2008 og að í undirbúningi væru sérstakar rekstrarreglur um lofthæfi og rekstur og tilkynntu þau að ákvörðun hefði verið tekin um að koma á fót sjálfstæðri stofnun á sviði almenningsflugs (ANAC) sem vænst er að verði tilkynnt um í júlí 2008.

Review: May2008 adoption timing omitted and civil-code/airworthiness terms corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Að því er varðar, veittu lögbær yfirvöld í Gabonu sönnunarskrá til framkvæmdastjórnarinnar um samþykkt nýrra ríkiflugsskilyrðis og sýndu þeim að þegar áttu sérstaklega reglur um flugvörslu og flugrekningar og veittu þeim að ákveðið hafi verið að skapa óháðri flugrekningastofnun (flugrekningastofnun) og að þetta ákveðið sé framkvæmd í júlí 2008.

</details>

<details><summary>final_semantic_review #322 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:571

English: To check power-operated windows/roof-panel systems/partition systems with reversing devices, a measuring instrument/test rod shall be placed through the opening from the inside of the vehicle or, in the case of a partition system, from the rear part of the passenger compartment in such a way that the cylindrical surface of the rod contacts any part of the vehicle structure which forms the boundary of the window/roof-panel aperture/partition.

Reference (shown after audit): Ef gera á athugun á rafstýrðum rúðum/þaklúgukerfum/skilrúmskerfum með enduropnunarbúnaði er mælitæki/prófunarstöng sett í gegnum opið innan frá úr ökutækinu eða, þegar um er að ræða skilrúmskerfi, frá aftari hluta farþegarýmis með þeim hætti að sívalt yfirborð stangarinnar snertir einhvern þann hluta ökutækisins sem afmarkar gluggann/þaklúguopið/skilrúmið.

Review: Vehicle controls, reversing devices and rod-contact geometry corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Til að meta hættuþjónustu, glugga/þjónustu, þjónustu með þróaðum þjónustuefni og þjónustu með endurnýjunum skal setja mælingaraðferð eða prófunarstjórnarmál í gegnum opinnum hlutaðeigingu frá innri ökutækinu eða, ef um er að ræða þjónustu með endurnýjunum, frá ytra hluta ökutækinu, þannig að hyljulegur yfirborð stjórnarinnar snýst um einhverja hluta ökutækinu sem eru að þróaðum þjónustuefnum, þ.e. þróaðum þjónustu með endurnýjunum, þar sem glugga/þjónustu, þjónustu með endurnýjunum og þjónustu með endurnýjunum eru að þróaðum þjónustuefnum.

</details>

<details><summary>final_semantic_review #323 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:eea:607

English: Years of career break in the current enterprise (optional).

Reference (shown after audit): Hve mörg ár hafa fallið úr í starfi hjá núverandi fyrirtæki (valkvætt).

Review: Career break becomes changes in career journey.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Árin sem eru í skipti í starfsferð í núverandi fyrirtækinu (valkostur).

</details>

<details><summary>final_semantic_review #324 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:430

English: Keep the needle in your skin after the dose counter has returned to 0 and count slowly to 6.

Reference (shown after audit): Haltu nálinni í húðinni eftir að skammtateljarinn sýnir aftur 0 og teldu hægt upp að 6.

Review: No candidate preserves complete needle-in-skin/counter0/slow counting6 sequence; several say talk instead of count.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Geymið nálinni í húðinni eftir að skammtatímabilinn er í 0 og haldið áfram að minnka tölina upp á 6.

Candidate 1: Geymið nálinni í húðinni eftir að skammtaleitinn hefur verið lokaður og talaðu hægt er að tala hingað til 6.

Candidate 2: Haltu hálið á þér eftir skammtaþolinn hefur komið í 0 og teljið það hægri til 6.

Candidate 3: Haltið núna nálinni eftir skilurinn og talaðu niður við 0 og talaðu stakkurt til 6.

Candidate 4: Haltu nálinni í húðinni eftir að skammtastortinn hefur komið að 0 og talaðu svo leið að 6.

Candidate 5: Haltu nálinni í húðinni eftir að skammtaskiptinn hefur stoppað og taktu nálinni hingað á hætrandi hátt til 6.

Candidate 6: Haltu nyléann á húð þinni eftir að skammtaskilinn hefur komið í 0 og talaðu með hættu til 6.

Candidate 7: Haltu nálinn í húðinni eftir þann skammt sem sett hefur verið og talaðu hún hægt og lyktlega til 6.

</details>

<details><summary>final_semantic_review #325 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:1610

English: The true extent of CNS penetration of lamivudine and its relationship with any clinical efficacy is unknown.

Reference (shown after audit): Í hve miklum mæli lamivúdín kemst raunverulega inn í miðtaugakerfið og samband þessa við klíníska verkun er ekki þekkt.

Review: CNS penetration/extent and clinical-efficacy relationship not retained.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Reyndar eftirlit með innrennslífi lamivudíns í móteiningu hefur ekki verið gerður.

Candidate 1: Sjálftæki sterfuvirkni lamívídüns og tengsl hans við klínísk árangur er ekki þekkt.

Candidate 2: Sgan þrír háttur á innflutning lamivúdins í neurluft og tengsl hans við klínísk starfsemi er ekki þekkt.

Candidate 3: Það er ekki þekkt hvoru langt lamivudín fer inn í móteiningu umhverfis og hvers vegna það er almennilega búin til að færa úr því.

Candidate 4: Sannar lengd breyingar lamivúdíns inn í blóðkornatæki er ekki vitað og ekki er greint út um samband við klínískar áhrifir.

Candidate 5: Þúsá hátti hlutfallið milli vísindi andlægis í móteiturliðinu greiðslusjúklinga frá lamivúdíni og tengslum þess við klínískar áhrif er þekkt ekki.

Candidate 6: Kannski hvar læknir nafna lamivudins inn í nálgunarhár er ekki þekkt.

Candidate 7: Heilbrigðis takmark fyrir innflutning lámvudíns í skilvirkni tilraunaraðilanna er ekki þekkt.

</details>

<details><summary>final_semantic_review #326 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:705

English: Normal long-duration GRBs last between 2 and 2000 seconds.

Reference (shown after audit): Venjulegir langir gammablossar standa yfir í 2 til 2000 sekúndur.

Review: GRB becomes an invented plant-blood-bleeding term.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Normið langvinnir gróðurblóðblæðir eru á 2 til 2000 sekúndum.

</details>

<details><summary>final_semantic_review #327 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eso:356

English: The nebula lies more than four hundred times further away than the famous star.

Reference (shown after audit): Þokan er þó meira en fjögur hundruð sinnum lengra í burtu en stjarnan fræga.

Review: No correct nebula >400times farther than famous star comparison.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Hraðarbragðin liggur meira en fjögur hundraðsin erra undir en þekktur stjarnan.

Candidate 1: Hjángirins er meira en fjórðungur sinn áfram.

Candidate 2: Hornuplanandið liggur meira en fjórðu hundraðsinn rúnnar frekar en frábær staðurinn.

Candidate 3: Draugurinn verður lengra en fjögur hundruð af stað en fræin starnarinn.

Candidate 4: Hölunin liggur meira en fjörtíu hundraðum sinnum lengur en frægasta starnið.

Candidate 5: Bifölunni er miðlengri en fjórða hundruða árið framan auðkynlaust stérunni.

Candidate 6: Hlæðurnar eru meira en fjögur hundruð verðar jartangs lengur en frægur starfarnir.

Candidate 7: Bílublu er meira en fjögur hundrar sinnum farar en frægur sterkarnar.

</details>

<details><summary>final_semantic_review #328 · old08 · greedy · technical_short · P</summary>

Source ID: p13official21:test:ema:2175

English: Breast-feeding must be stopped on initiation of treatment with Voriconazole Accord.

Reference (shown after audit): Hætta verður brjóstagjöf þegar meðferð með Voriconazole Accord hefst.

Review: Breastfeeding must stop on Voriconazole Accord treatment initiation retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Hætta verður með brjóstagjöf við byrjuð meðferð með Voriconazole Accord.

</details>

<details><summary>final_semantic_review #329 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:ema:2490

English: If you are left-handed, do what comes naturally to you.

Reference (shown after audit): Þeir sem eru örvhentir eiga að gera það sem þeim finnst eðlilegast.

Review: Left-handed becomes running-capable.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef þú ert hlaupanhæfur, gerðu það sem er þér nautnlegt.

</details>

<details><summary>final_semantic_review #330 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:ema:1458

English: This is important to make the medicine easier and more comfortable to inject.

Reference (shown after audit): Þetta er mikilvægt til þess að auðveldara og þægilegra sé að sprauta lyfinu.

Review: Comfortable becomes pregnant/heavy.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þetta er mikilvægt að láta lyfið vera auðvelt og þunguðar að sprauta.

</details>

<details><summary>final_semantic_review #331 · old08 · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:3337

English: But maybe, if we got away from here, if we went somewhere safe, it could be different.

Reference (shown after audit): En kannski ef við kæmumst burt héðan, ef við færum á öruggan stað, gæti það breyst.

Review: Escape from here, safe destination and possibly different outcome retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: En kannski, ef við færum okkur frá hér, ef við færum okkur í einhverju öruggi, gæti það verið annað.

</details>

<details><summary>final_semantic_review #332 · old08 · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:2209

English: Much has been made of the hostility between our countries.

Reference (shown after audit): Mikið hefur verið gert úr fjandskapnum milli ríkja okkar.

Review: Hostility between countries becomes wars at our border.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það hefur verið mikilvægt að ræða stríðina á landamæri okkar.

</details>

<details><summary>final_semantic_review #333 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:825

English: The process of dust trapping is explained in an earlier release (eso1325).

Reference (shown after audit): Þetta ferli, þegar ryk festist, er útskýrt í eldri fréttatilkynningu (eso1325).

Review: Dust trapping becomes pressure research.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Rannsókn á þrýstingum er útskýrt í fyrra (eso1325).

</details>

<details><summary>final_semantic_review #334 · old08 · G8 · technical_short · F</summary>

Source ID: p13official21:test:eea:1814

English: The producer must ensure that all wood originate from legal sources.

Reference (shown after audit): Framleiðandi skal tryggja að allur viður komi frá löglegum aðilum.

Review: Wood from legal sources not retained in any candidate.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Fyrirtækið aðgengi þess að allir vöðir séu aðalgerðir á lögunæmi.

Candidate 1: Búnaðurinn á að tryggja að allar bitar séu tilboðsýtar að lögbærum ástæðum.

Candidate 2: Að framleiðanda skal tryggja að allar bitar eru urðu frá lögaðlun.

Candidate 3: Aðurstöðullendingurinn verður að tryggja að allir vöður séu að feðrum lögbærum.

Candidate 4: Aðurstöðvunarfélagið skal sjá til þess að allar skeiðið koma úr lögbærum vörslum.

Candidate 5: Aðlagið skal tryggja að öll bóður komi frá löggjöfum.

Candidate 6: Að skipunartæki verður að sjá til að allar vöðir upplifna frá lögaðlun.

Candidate 7: Færan verður að sjá til þess að alla eldhópur séu frá löglegri ávörnu.

</details>

<details><summary>final_semantic_review #335 · old08 · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:3265

English: There's a police convention out there.

Reference (shown after audit): Það er lögregluráðstefna þarna úti.

Review: Police convention becomes police order/line rather than convention.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það er lögreglufyriröðin þarna.

</details>

<details><summary>final_semantic_review #336 · old08 · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:1596

English: I stuffed it in my pocket.

Reference (shown after audit): Ég setti hana í vasann.

Review: Pocket becomes packages.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ég setti það í pakkana.

</details>

<details><summary>final_semantic_review #337 · old08 · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:3454

English: And I work for Danny.

Reference (shown after audit): Og ég vinn hjá Danny.

Review: Exact source/hypothesis semantic reuse from card59: Working for Danny retained; initial conjunction omitted only.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Ég vinn fyrir Danny.

</details>

<details><summary>final_semantic_review #338 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eso:45

English: This would make the system similar to our Solar System in terms of the number of planets (seven as compared to the Solar Systems eight planets).

Reference (shown after audit): Þetta sólkerfi geymir því svipaðan fjölda reikistjarna og sólkerfið okkar (sjö reikistjörnur í samanburði við átta í sólkerfinu okkar).

Review: All corrupt SolarSystem/planet identity or seven-versus-eight numerical comparison.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þetta gæti gerst kerfið sjálfu sátt saman við Geimverksmiðunni okkar, að því er varðar fjölda planetanna (sjöfirarnar eru fleiri en geimverksmiðuninni á sjöplannum).

Candidate 1: Þetta gæti verið sýnt samkvæmt helvítismörkum í gegnum fjölskyldunnar (sjögri fjölskyldurnar eru sjö og helvítismörkarnar sjö fjölskyldur).

Candidate 2: Það myndi líka geirast eiginleika okkar um jörðastafa í gegn sjöjarð og sjöjarð í geirismörkum okkar.

Candidate 3: Það myndi samræma kerfið við Sjúrinu á sama hátt sem í fjölgæðum er að tala um nokkrum geðir (sjögu fjögur, í gegnndi við aðtalaðan sjö geðir í Sjúrunni).

Candidate 4: Þessi tilviki gerir kerfinu sömu við ljósvegssyni og okkar í tengslum við fjölda plánera (sjöllum í ljósvegssyni og sjö plánerum í ljósvegssyni).

Candidate 5: Það gerir kerfinu sýnt eins og solarhráðinn okkar, í því skipti, að hlutfallið á sjö úteræðum í gegn átta úteræðum í solarkránum.

Candidate 6: Þetta gæti orðið samanburðarlegt við jörðleysisljóskuna í því skyni að fleiri sýnum (sjögurðin eru sjötugur samanburður við sjötugurjörðleysisleysinu sjóðsýnum sjóðsýnum).

Candidate 7: Þetta myndi geta lýst kerfið eins og systemur sýnhólfa okkar á þeim margfalda, sem sýni hefur átt sjö hvarfingar samanborið við sýnhólfið þitt sem hefur hafa átt náttúrulega hvarfing.

</details>

<details><summary>final_semantic_review #339 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:930

English: Wells in microtitre plates are coated overnight with recommended dilutions of purified immunoglobulin fractions of antibodies of reference quality.

Reference (shown after audit): Bollar í míkrótítrunarplötum eru þaktir næturlangt með ráðlögðum þynningum af hreinsuðum ónæmisglóbúlín- þáttum mótefna sem standast kröfur um viðmiðunargæði.

Review: All corrupt microtitre wells, overnight coating and immunoglobulin/reference-antibody dilution.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Skýlin í mikrortíðumplötrum eru málað með fyrirbyggðum skammta úr jarðmyntu skilvísindarefni á hávinnum.

Candidate 1: Í mikrotitripplötnum er meðferð með bætur í fullnægjandi mæðum af þynntu ónæmingjafra af ónæmingum, sem eru í rannsóknum, og síðan lokað í eiturítt.

Candidate 2: Málvörðum í mikrolitri töflum er sett í kvöldinn með ráðlagðri þynningu af tæknilegu, þurfuðum, óþrýstingum frá lífblómum í tæknilegri gildi.

Candidate 3: Það skal efna skammtamíðunarmjólöðumbúnaðarinnar um víkumíðum í tegundum með tilliti til viðmiðunarþéttra útblástu.

Candidate 4: Það er meðhöndlað loksnefni í mikrotitillum með ráðlögðu þynningu af lyfjastak af þynkjum sem eru sýnd í rannsóknum.

Candidate 5: Breytingar á veggum í mikrotítuplöturnum eru með tilkynntum þynningum af þynntu alþjóðlegu vöðvargreiningu úr efnislíkunum sem veita gæði við endurtekinuþætti.

Candidate 6: Það er ráðlagt að blönduðu óþrýstaþvörun, þrýstingsfrumum úr óþrýstingum á þrýstingarhrifum í néalögreglu, sé meðhöndlað helgina í þvöðum á grundvelli þrýstingarhrifa í milli-þvöðum.

Candidate 7: Óþegarvelli á mótefnaflokka eru settar um helgina með ráðlagtum efniþyngdum óþreyttra óhítjafra í þyngdistjungum af óhítjuförum sem eru með viðmiðunarlögum.

</details>

<details><summary>final_semantic_review #340 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:538

English: Previous observations had shown hotter, but much less dense, gas streaming away from NGC 253s star-forming regions, but alone this would have little, if any, impact on the fate of the galaxy and its ability to form future generations of stars.

Reference (shown after audit): Eldri rannsóknir höfðu sýnt að heitara en ekki jafn þétt gas streymdi burt frá stjörnumyndunarsvæðum NGC 253 en að það eitt hefði lítil eða ekki nokkur áhrif á örlög vetrarbrautarinnar og getu hennar til að mynda nýjar kynslóðir stjarna.

Review: Galaxy fate becomes circumstances of administration; density wording also changes.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Í fyrra rannsóknir hafa verið sýnt heitt, en mjög lægri þynning, gasið fljótandi frá starfræðisvöllum NGC 253, en einnig þá hefði það lítið, ef neitt, áhrif á ástæðum stjórnsýnið og hæfni til að forma framtíðar sjálfstæðir stjörnu.

</details>

<details><summary>final_semantic_review #341 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:3025

English: Based on individual patient response and tolerability, the dose may be increased to 300 mg (15 ml) per day after an interval of 3 to 7 days, and if needed, to a maximum dose of 600 mg (30 ml) per day after an additional 7-day interval.

Reference (shown after audit): Eftir svörun og þoli hvers sjúklings má auka skammtinn í 300 mg (15 ml) á sólarhring eftir 3-7 daga og ef þörf krefur í hámarksskammt, 600 mg (30 ml) á sólarhring, eftir 7 daga til viðbótar.

Review: No candidate retains response/tolerance and complete staged maximum-dose constraints;3 hallucinates escalating doses and truncates.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Á grundvelli einstaklingssvörunar og einfaldars varðandi notkun má auka skammtinn í samræmi við þá einkenni sem þegar hafa verið, í 300 mg (15 ml) daglega eftir 3 til 7 daga staðfestingar, og ef þörf krefur, í hámarksgrammshófi 600 mg (30 ml) daglega eftir 7 daga staðfestingar.

Candidate 1: Í Grundvöllunum er hægt að auka skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga tímamörkum og ef þörf krefur, að hámarksskammti 600 mg (30 ml) á dag er hægt eftir 7 daga tímamörkum.

Candidate 2: Að því er varðar einstaklingssvefnisbrun og lyfjastöðu getur dosin einnig verið aukin til 300 mg (15 ml) á dag eftir 3 til 7 daga tímabundiðs hvarðferðar, og ef þörf er á, í hámarksskili 600 mg (30 ml) á dag eftir 7-dagis tímabundiðs hvarðferðar.

Candidate 3 [TRUNCATED]: Þrátt fyrir jafnan sýnilegan svörun og umæðahópsömu á að skammturinn sé hægt að aukast upp á 300 mg (15 ml) daglega eftir 3 til 7 daga tíðni og ef nauðsyn krefur, hægt er að stöðva með hámarksskamti 600 mg (30 ml) daglega eftir 7 daga afturtil 360 mg (18 ml) daglega eftir 7 daga afturtil 720 mg (36 ml) daglega eftir 7 daga afturtil 840 mg (42 ml) daglega eftir 7 daga afturtil 960 mg (48 ml) daglega eftir 7 daga afturtil 1080 mg (54 ml) daglega eftir 7 daga afturtil 1200 mg (60 ml) daglega eftir 7 daga afturtil 1320 mg (66 ml) daglega eftir 7 daga afturtil 1440 mg (72 ml) daglega eftir 7 daga afturtil 1680 mg (84 ml) daglega eftir 7 daga afturtil 1800 mg (90 ml) daglega eftir 7 daga afturtil 2040 mg (102 ml) daglega eftir 7 daga afturtil 2160 mg (108 ml) daglega eftir 7 daga afturtil 2280 mg (114 ml) daglega eftir 7 daga afturtil 2400 mg (120 ml) daglega eftir 7 daga afturtil 2520 mg (126 ml) daglega eftir 7 daga afturtil 2640 mg (132 ml) daglega eftir 7 daga afturtil 2760 mg (138 ml) daglega eftir 7 daga afturtil 2880 mg (144 ml) daglega eftir 7 daga afturtil 3000 mg

Candidate 4: Bólt 300 mg (15 ml) á dag á basisi einstaklingssegundar og öryggi, eftir 3 til 7 daga skipti, og ef þörf krefur, 600 mg (30 ml) á dag á basisi eftir þremur árum skipti.

Candidate 5: Þar eð sérhæfð beinlæði sjúklinganna og möguleiki viðkomunar getur sýnt á því að skammtið sé auðveldað út til 300 mg (15 ml) dagsликаð eftir 3 til 7 daga skipti og ef þörf krefur, aftur í 7 daga skipti.

Candidate 6: Við notkun á þessum lyfi má aukast skammtinn, að því er varðar einstaklingsveit og ekki hægt, að 300 mg (15 ml) einu sinni á dag eftir 3 til 7 daga aðferðardagur og ef þörf er á, að hámarksskammti 600 mg (30 ml) á dag eftir 7 dag meðferðardagur.

Candidate 7: Að því er varðar einstaklingarens svörun og ekki möguleik meðferðar varanlega er hægt að auka skammtið af 300 mg (15 ml) daglega eftir 3 til 7 daga hagkvæðis og ef þörf kemur til er hægt að auka stungulyfjaðanum á hámarksgildi 600 mg (30 ml) daglega eftir 7 daga hagkvæðis.

</details>

<details><summary>final_semantic_review #342 · old08 · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:2164

English: You didn't have the guts to do it yourself.

Reference (shown after audit): Þú hafðir ekki kjark til þess sjálfur.

Review: Lack of courage becomes not having the temper/mood for doing it.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þú hafðir ekki skapið til að gera það sjálfur.

</details>

<details><summary>final_semantic_review #343 · old08 · greedy · technical_short · P</summary>

Source ID: p13official21:test:eea:1965

English: After paragraph 97B, paragraph 97C is added.

Reference (shown after audit): Lið 97C er bætt við á eftir lið 97B.

Review: Paragraph97C added after97B retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Eftir 97B. lið bætist 97C lið til.

</details>

<details><summary>final_semantic_review #344 · old08 · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:1088

English: Weather statistics are available here.

Reference (shown after audit): Upplýsingar um veður má finna hér.

Review: Closest0 gives weather information rather than statistics; other candidates also lose the statistical subject.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Veðriupplýsingar eru heimilt að finna hérna.

Candidate 1: Vegnaþjónusta er hér að frjósemi.

Candidate 2: Væðiupplýsingar eru hér að frábært.

Candidate 3: Vegnaþætti eru hér að neðum.

Candidate 4: Veðrið er fengið hérna.

Candidate 5: Vonvirkunarupplýsingar eru fáanleg hér.

Candidate 6: Loftsöfnun er hér að góp.

Candidate 7: Veðurlög og sýnir eru hér.

</details>

<details><summary>final_semantic_review #345 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:2183

English: For intravenous use, infusion systems with Actrapid at concentrations from 0.05 international unit/ml to 1.0 international unit/ml human insulin in the infusion fluids 0.9% sodium chloride, 5% dextrose and 10% dextrose inclusive 40 mmol/l potassium chloride using polypropylene infusion bags, are stable at room temperature for 24 hours.

Reference (shown after audit): Fyrir gjöf í bláæð er Actrapid stöðugt við stofuhita í 24 klst., í styrkleikum 0,05 alþjóðlegar einingar/ml til 1,0 alþjóðlegar einingar/ml af mannainsúlíni í eftirfarandi innrennslisvökvum; 0,9% natríumklóríði, 5% glúkósa og 10% glúkósa með 40 mmól/l af kalíumklóríði, þegar notaðaðir eru pólýprópýlen innrennslispokar.

Review: All corrupt concentration units, solution composition, container or room-temperature stability;5 repeats/truncates.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Með inndælingu á meðferð með Actrapid er framleiðsla óhvarfsemi verðandi, sem er hægt að taka tillit til þess að hún sé stöðug í 24 klst. hitastigi, haldið vegna 40 mmól/l í potassiklórítriði með brúðslóðskólafílmíni (polypropylene) í innrennslaskjót, annars en 0,9% natriumkloríð, 5% dextrosa og 10% dextrosa hliðar 40 mmól/l í potassiklórítriði.

Candidate 1: Tilkynnt er um að innrennslisýrsluhúsi sem innrennir er Actrapid í innrennslisflúði, með innrennslisflúðum sem eru 0,05-1,0 reikningsskil e.f.m. hjá mönnum, stöðugt í 24 klst. heitt klár þegar innrennsla er hægt er innrennslisflúðin sem eru 0,9% natríumklóríð, 5% déstrosa og 10% déstrosa, í innrennslispylstökum sem eru upp að 40 mmól/l af saltklóríð, sem eru upp sem er upprunalegt, með góðum efnaheldsiðum innrennslispappíusamla.

Candidate 2: Samkvæmt tilvísun í blástök brennstjóla, sem meðferð með Actrapid er hæfilegt, eru blöndurinn með innrennslisdríum sem eru í 0,05-1,0 internationaluþætti/ml af vanalinsílinum, sem eru í innrennslisvöðvum, 0,9% nátríumkloríð, 5% dexþyrri og 10% dexþyrri, 40 mmól/l af jártríumkloríð, með fljóttlinnu, hugsanlegri stígum stikkum og hættulegum sáttkvæðum, stöðguð á 24 klst. með þynnum.

Candidate 3: Geymsluþolinnverk sem eru notuð sem innrennslyf eru í innrennslífu með Actrapid í innrennslyfjafærni frá 0,05 að 1,0 alþjóðlegar shtöðugr. /ml hjá mönnum í innrennsliðinu 0,9% natriumkloríð í öðrum innrennsliðinu, 5% dextrosa og 10% dextrosa (40 mmól/l) með staðalbröðulífum í innrennsberðum, eru í stað við 24 klst. heitvirkni komin upp á krefjandi hitastig.

Candidate 4: Við notkun á 10% dextrosa og 10% dextrosa innihaldi 40 mmol/l potassíumklóríð eru innrennslyfja með 1,0% dextrosa og 10% dextrosa innihaldi stöðguð við 24 klst. hlutfallið samtímis 0,9% salíumkloríð og 5% dextrosa og 10% dextrosa innihaldi 40 mmol/l potassíumklóríð. þar með skorti hreyfingaflokkur með 1,0% dextrosa og 10% dextrosa innihaldi natríumklóríð.

Candidate 5 [TRUNCATED]: Heildarverkin sem notuð eru í innrennsnotkun með Actrapid í innrennslífum með innrennsliðum, sem eru í innrennslínum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með innrennsliðum, sem eru í innrennsliðum, með

Candidate 6: Í tetraðómuskílflæði geta litra í Actrapid (0,05~1,0 international unit/ml) í blóðsyklum, 0,9% natriumklóríð, 5% dextrosa og 10% dextrosa, 40 mmólm/l potassíumklóríð, sem eru 24 klukkustundir ár stórir, sem eru stablar í 24 klukkustundum.

Candidate 7: Nema innrennslisstarfsemi, sem eru með Actrapid í innrennslisblöndum, með innrennslyfjafjölda frá 0,05 alþjóðlegar millilitrí (ml) til 1,0 alþjóðlegar millilitrí (ml), hjá manneskjunum í innrennslisblöndum 0,9% natriumklóríð, 5% déxtrós og 10% déxtrós (dextrose), 40 millólítr í sárslið, sem eru í innrennslisöfnum, eru stöðugir við heildarmörk í 24 klst. tímabili.

</details>

<details><summary>final_semantic_review #346 · old08 · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:825

English: The process of dust trapping is explained in an earlier release (eso1325).

Reference (shown after audit): Þetta ferli, þegar ryk festist, er útskýrt í eldri fréttatilkynningu (eso1325).

Review: Dust trapping becomes unrelated pressure/growth/washing research in all outputs.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Sjármál um sátaöskun er útskýrt í forðan (eso1325).

Candidate 1: Breytingarnar á græðslu eru skilgreindir í fjölgun (eso1325).

Candidate 2: Logan um þurráknaðarþrýstingu er aðrar frestru (eso1325).

Candidate 3: Rannsókn um drángun er skýrt í fyrra lesu (eso1325).

Candidate 4: Rannsókn á þrúðunarkerfi er útskýrt í fyrstu greiningu (eso1325).

Candidate 5: Rannsókn "dýristöðunarsviðs" er útskýrt í fyrra íbúð (eso1325).

Candidate 6: Lýsingu að gróðvegi séndar er skýrt í áföngum (eso1325).

Candidate 7: Rannsóknarlegt aðgerð að þvottir séu aðgengileg eru þýðir í öðrum greiningum (eso1325).

</details>

<details><summary>final_semantic_review #347 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:852

English: These actions may include comparison of the effectiveness of processes, methods and tools related to the chosen themes, mutual transfer and application of good practice, exchanges of personnel, joint development of products, processes, strategy and methodology, adaptation to different contexts of methods, tools and processes identified as good practice, and/or dissemination of results, profile-raising materials and events.

Reference (shown after audit): Aðgerðirnar geta falist í því að bera saman skilvirkni vinnsluferla, aðferða og tóla, sem tengjast þeim þemum sem eru valin, í gagnkvæmri miðlun og ástundun góðra starfsvenja, í starfsmannaskiptum, sameiginlegri þróun vara, vinnsluferla, skipulags og aðferðafræði, í því að aðlaga að ólíku samhengi aðferðir, tól og vinnsluferli, sem eru skilgreind sem góðar starfsvenjur, og/eða í útbreiðslu niðurstaðna og kynningarefnis og skipulagningu viðburða.

Review: All corrupt or omit multiple good-practice/personnel/adaptation/dissemination list elements.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Slík meðferð getur komið í ljós samanburð á yrki aðferða, aðferða, áætlaða tækni sem tengjast valdum efnisins, móteindu umferð og notkun góðrar starfsemi, samanburðarhafa starfsmanna, samstarfsþróun á vinnslu, vinnslu, starfsemi og aðferðir, aðlögun við mismunandi skilmála um aðferðir, tæknifíknir og vinnslu og / eða mismunandi útgáfan af niðurstöðum, fólkframhaldssviðum og tilkynningum.

Candidate 1: Þessar álag geta komið með samanburði á árangri aðgerða, aðferða og verkfrialfa sem tengjast valdu málsfélögum, samvinnu á góða aðgerða, samkeppni á starfsfólki, samstarfið að ræða vöru, aðgerðir, áætlun og aðferðir, aðhæfingu að tilteknum umferðum, verkfirlögunum og vörubrögðum og/eða meðferðar við útbreiðslu af úrtækum niðurstöðum og semjurtölu til að upprúnastuðla starfsmenn.

Candidate 2: Staðfestar árangri á þessum starfsemi getur þó haft tengningi við samræmingu á árangur starfsmanna, aðferða og vopna, sem tengjast valinni málunum, milliþáttunum og notkun þeirrar starfsemi, varða viðmiðunarskerðingar, samskiptið á starfsmönnum, samverkkunnar á viðkomandi framleiðslunum, starfsem, stýringaráætlun og ákvarðanlegra aðferðalegra, aðgerðir, að uppfylla mismunandi umhverfi og, eða, að sýna út úturu, æviseðjur og aðgerðir.

Candidate 3: Lífrænni ástæðurnar geta verið að sýna fram á auknum árangri að því er varðar að höfuðverum verði lýs að framkvæmdur, aðferðir og tækni sem tengjast þeim valdaðum málinu, samþykki og notkun góðrar háttarvarða, tengslum starfsfólks, sameiginlegri þróun nefndar, í ljósframleiðslu, framkvæmda, áætlunargreiningar og framkvæmdarhagsmál, aðætlað á starfsnæmi, tækni og framkvæmda í tilviki fjölskyldu, tækna og framkvæmda sem teljast góðar háttarvarur og/a, og/hálfræðilega þar til að sýna fram á niðurskrá, skýrslugjöf og eitrun.

Candidate 4: Þetta getur verið að ræða samanburði á Fullnæmi verkunar, aðferða og tækja sem tengjast valduðum málinum, móteiningu og notkun góðra aðgerða, skilningra arcsamninga, sameiginlegri þróun vöru, verkanna, stýrnar og tækniforskrifta, viðætti aðferðanna til að undirbúa aðferðir til tilvísunar til þess að tækniforskrifti séu tilgreindir og/eða smíðun á úrtökum, tengsla og upplýsingum um staðfestingu og útlýsingum.

Candidate 5: Áritækið getur hafa haft samanburði á notkun áframhaldsefna, aðferða og tækja sem tengjast valandi málinum, samþykkið ferð og notkun góðar starfsmanna, samstarfssamvinnu afurða, samstarfssamvinnu afurðanna, áframhaldsefna, stuttra og ræktunarhugsa, samræmingu á aðferðum, tækjum og áframhaldið eða/koma, og/samkvæmdi af niðurstöðum, íbúðum og aðgerðum í tilkynningum og/símunverum og stöðum.

Candidate 6: Sjálfboðin geta náð til þess að bæta þessu aukagert með samræmingu á þróun, aðferðum og veitum, sem tengjast valdið almenningsmálum, samneytingu og beitingu góða starfsmanna, samvinnu á framleiðsluvarum, ströngum, ráðstöfunum og ráðstafanum, ánndun á aðferðum, veitum og ströngum í viðkomandi tengildum tilteknum tilviki, og/eða þrýsting á niðurstöðum, starfsráðum og athafnir.

Candidate 7: Þessi áætlun getur að þegar aðrari þá keyrðum á efni aðgerða, aðferða og tækna flestur, hófi og notkun góða reglna, skipti við starfsmannir, sameiginlegar framkvæmdar á vinnsluvaranum, og aðgerðir, aðferðir og rannsóknartækja og/aða umboðarskoðun um raunverulegri tækni, ættbrauti og/óra samtrúð sem uppgjörra markmið, eða/óða umboðarskoðun um lækni og/hægt að senda niðurstöður, framkvæmdarvörur og aðgerðir.

</details>

<details><summary>final_semantic_review #348 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eso:710

English: The VST KiDS survey will allow astronomers to make precise measurements of dark matter, the structure of galaxy halos, and the evolution of galaxies and clusters.

Reference (shown after audit): Kortlagningin nefnist VST KIDS og gerir stjörnufræðingum kleift að mæla nákvæmlega staðsetningu hulduefnis, uppbyggingu vetrarbrautahjúpa og þróun vetrarbrauta og þyrpinga.

Review: All corrupt dark matter, galactic halo structure or galaxy/cluster evolution.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Sjánmál í VST-fræðilega skrá um hjálfahúsið geta leitt himnskóla til að mæla snjall ár efnisins (dark matter), hundraðarkefnistengir í galáxum og að hvernig gegnumhættu galáxur og eiðubúar úrbær eiga sig að blása.

Candidate 1: Skálaríkar geta tekið nákvæm mat á svörtum kefi, af afurðum herra, og um hreinlestu og skipulestu röðir.

Candidate 2: Verleikarskíði til að KíDSnotkunarstarfsemi verður gerir í starfsemi stjórnpásskeri fyrir því að gerja nákvæmar mælingar á svörtum germum, í vörðunum á gálaðómum og samstundum verðbroti á gálaðómum og fjölgum.

Candidate 3: Með því að VST KiDS-tekjur er gömluþólfarökurur til að geta náð nákvæmum mælingum á myrkur, byggingu afurða í alþekjunum og aðferðinni á alþekjunum og klústurnum.

Candidate 4: Kjötumur með VST-kröfu til lækningar í eðli þróaðar áhrifar geta leitt ísögumum að tæka mælingum á svörtum efninu, struktuðu sýraraflið og þróun sýrarafliða og klústera.

Candidate 5: Sjálfkröfuvöruþopparnar geta endurskoðað hreint starfsemi í ljós, valdandi þakklæði, væri samræmt og málaður, þrýstingartækniflokkun í hjólum galaxa og breytingu á galaxum og vonunum.

Candidate 6: VST KiDS-endurmatningarnar geta leitt stjórnmenn til að mæla slæmu mataræðju með nýrnarlegri nákvæmni, skipti á höfðum lífthraða lífsfyrirtækja og hvort blóðrannsóknarverkir verða að fara frá.

Candidate 7: Haggljóslamtöku til rannsóknar á slíkríki fyrir hreyfilsþrýstingi mun leggja fjár til að ráðstafanir geti gert nægilega nákvæmar mælingar á myrkurum, kerfi gildihlóðanna og einfaldri meðferð gegn gildihlóðum og klústrum.

</details>

<details><summary>final_semantic_review #349 · old08 · greedy · technical_medium · U</summary>

Source ID: p13official21:test:eea:2090

English: Member States shall require the competent authorities to monitor compliance with this Regulation effectively and take all necessary measures to ensure such compliance.

Reference (shown after audit): Aðildarríki skulu skylda lögbær yfirvöld til að hafa eftirlit með því að farið sé með virkum hætti eftir þessari reglugerð og gera allar nauðsynlegar ráðstafanir til að tryggja að farið sé að ákvæðum hennar.

Review: Authority requirement and necessary measures retained, but effective compliance monitoring becomes satisfactory compliance-affairs wording; cannot confidently certify exact legal scope.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Aðildarríkin skulu krefjast frá lögbærum yfirvöldum að fylgjast með fullnægjandi framfylgismálum við þessa reglugerð og gera allar nauðsynlegar ráðstafanir til að tryggja þá fullnægjandi framfylgismál.

</details>

<details><summary>final_semantic_review #350 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:ema:129

English: Clinical studies have demonstrated that ProQuad can be given simultaneously (but at separate injection sites) with Prevenar and/or hepatitis A vaccine, or with monovalent or combination vaccines comprised of diphtheria, tetanus, acellular pertussis, Haemophilus influenzae type b, inactivated poliomyelitis, or hepatitis B antigen.

Reference (shown after audit): Klínískar rannsóknir hafa sýnt fram á að hægt er að gefa ProQuad á sama tíma (en á öðrum stungu- stað) og Prevenar og/eða lifrarbólgu A bóluefni eða með eingildu eða samsettum bóluefnum með barnaveiki, stífkrampa, frumulausan kíghósta, Haemophilus influenzae af gerð b, deyddum mænu- sóttar eða lifrarbólgu B mótefnavökum.

Review: Vaccine/antigen list extensively corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Klínísk rannsóknum hefur sýnt fram á að ProQuad má gefa samtals (en á sérstökum inndælingarstaðum) með Prevenar og/eða heittar A-álföng, eða með einmálvaktandi eða sambundvaktandi bólusetningu sem inniheldur dýræðisvöxt, tetanusvöxt, óvöxta persúðun, b-tíðunshemilbrotta, inndælt poliýmýlýslu eða heittar B-álföng.

</details>

<details><summary>final_semantic_review #351 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:437

English: Lenvatinib should not be started in patients with fistula to avoid worsening and lenvatinib should be permanently discontinued in patients with oesophageal or tracheobronchial tract involvement and any Grade 4 fistula (see section 4.2); limited information is available on the use of dose interruption or reduction in management of other events, but worsening was observed in some cases and caution should be taken.

Reference (shown after audit): Ekki skal hefja meðferð með lenvatinibi hjá sjúklingum með fistil til að forðast versnun og hætta skal meðferð með lenvatinibi til frambúðar hjá sjúklingum þar sem vélinda eða barki og berkjur eiga í hlut og í tilfellum allra 4. stigs fistla (sjá kafla 4.2), takmarkaðar upplýsingar liggja fyrir um skammtahlé eða skammtaminnkun við meðferð á öðrum atvikum, en versnun varð í sumum tilvikum og því skal gæta varúðar.

Review: All corrupt fistula anatomy/grade, starting/permanent stopping or management-warning clauses.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Lenvatinib skal ekki hafa verið hætt til viðbótar hjá sjúklingum með sýrubreyti til að koma áfram og Lenvatinib skal hætt við hald áfram hjá sjúklingum með orðbundni eða slitthæfta sýrubreyti og sýrubreyti um hlutir sem eru í gegnum lenti og brjósti til að koma áfram, og má hætta fyrir Lenvatinib ef sýrubreyti er 4. áfengin (sjá kafla 4.2). Með lokaðum upplýsingum er hafa fengið fram um notkun hlutbreytingar eða fjarlægðar á skammti eða minnkunar meðan við á að það er að meðhöndla önnur ástand en í einnum tilvikum var sýrabreyti svörunin og skal þó halda á breytingu.

Candidate 1: Lenvatinib skal ekki hætta við notkun hjá sjúklingum með sýrð í æð, til að forðast þess að þær verði breytileg, og skal hægt vera að hættast við notkun lengvatinib við sjúklingum með sýrð í æð eða æð og vefssen í svæði eða vefssen í svæði vefssen, og hjá sjúklingum með hvettingu í vefssen eða vefssen í svæði vefssens, en þó var einhverjar sýrðar á öðrum eigi og ábyrgð vegna þess skal vera um það.

Candidate 2: Lenvatiníbi ætti ekki að færa hjá sjúklingum með þróun á fístu til að forðast þessu og lenvatiníbi skal hættu á efri stað hjá sjúklingum með þróun á tengsla við magi, tengsl við trákta og húð og tímabundinn físt (sjá kafla 4.2); viðeigandi (4. gr.) físt eru ekki tilvísun til nema sýni séu tilnefndar, en framkvæmdstætti fyrir að viðkomandi sjúklingi séu leynin á því að breyta skammti eða minnka skammti meðan meðferð á öðrum aðgerðum er í lagi, en það er greint fram um að þróað væri í tilvísun við sumum tilvikum og að gæta skal.

Candidate 3: Lenvatinib skal ekki hafa verið hætt við sjúklinga með fistúru til að forðast að þær væri vart og lenvatinib skal hætt við sjúklinga með þurrar á flæði í eðlumið eða tengjum við rekkju eða æð í gegnum slæm eða æð eða æð eða æð og þegar tilfalið á að lenvatinib er hætt við sjúklinga með þurrar á flæði í eðlumið eða tengjum við rekkju eða æð eða æð eða æð en aðeins einn hálfurinn er gefinn um að notkun dreifunar eða afturtekunar á skammti eða minnkun á næringarvöru meðferðar með annarra aðgerða er erfið en þegar þó var einhverju aðgerðum við þær þar sem þurra á flæði í eðlumið eða tengjum við rekkju eða æð eða æð eða æð var sjá um að dreifun og var þó að halda að gæta.

Candidate 4: Lenvatinib ætti ekki að vera hægt að nota hjá sjúklingum með kveikjanlegi umbrot vegna þess að það getur haft heilkun og lenvatinib skal hættast áfram á langvun á meðan sjúklingum með þátttöku í brýni í svæði úti í aðhonnum og í fjölgjafli eða í fjölgjafli í sviði 4 (sjá kafla 4.2); kleift að taka tillit til máls sem er tilgreindur í 4.2, en má skipuleggja meðferð með öðrum aðgerðum, og það var sjálfur sett í höfð eða óþægð fyrir notkun þessara verða meðferðar, en það var sett í höfð eða óþægð fyrir notkun þessara verða meðferðar og klára má um þá aðgerð sem er tilgreind.

Candidate 5: Ekki skal byrja með lenvatínib hjá sjúklingum með skítbeinung, til að forðast að skítbeinunni væri aukin, og lenvatínib skal fylgja slöðlega fyrirkomulag hjá sjúklingum með eiginleika og traktir í gegnum mag og kvik í meðhöndlu og hverra bráðar skítbeinun (sjá kafla 4.2). Fjármögnun er mennt um notkun viðbótastarfsemi eða þynningar viðhalda fyrir hluta, en það kemur í ljóst að aukningur væri um einhverjar tilfelli og að tækja aðgerðir til varnar.

Candidate 6: Að notkum á læganvinnslöngvinib ekki fyrir sjúklingum með fistula til að forðast því að þau missi þessari einkennum og læganvinib skaltur hætta algerlega fyrir sjúklinga með þóttarþol eða trakt í tengslum við hálfa eða hólfa og hljóða til 4. flokki. Með skýringuna 4.2 er gert tilkynnt um að gerðar er hægt að nota lækur eða minnka á skammti eða meðferð hjá öðrum aðgerðum en mjög dregið úr verulegu vinnslu er komin til staðar en hægt er að tæka varða sjúklinga og skal því gætt við.

Candidate 7: Lenvatinib skal ekki hleið að hætta með sjúklingum með vífur til að forðast að þær væri að úr hópinni en lenvatinib skal vera hættuð aðeins ef lífsvigt er einnig í vífur eða vífur með íttuðri vinkurum og um 4 gráðu vífur (sjá kafla 4.2), viðeigandi upplýsingar um notkun þess og hléðra skammta eða verkunarflugs í meðferð við önnur ástand eru hæfar en þær væru að úr hópinni og þó er ekki að segja að þær væru breytir og að tekið sé eftirlit við henni.

</details>

<details><summary>final_semantic_review #352 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:1168

English: R Coronae Australis itself is not visible to the unaided eye, but the tiny, tiara-shaped constellation in which it lies is easily spotted from dark sites due to its proximity on the sky to the larger constellation of Sagittarius and the rich star clouds towards the centre of our own galaxy, the Milky Way.

Reference (shown after audit): R Coronae Australis sést ekki með berum augum en litla kórónulaga stjörnumerkið sem hún tilheyrir sést auðveldlega við góðar aðstæður sökum nálægðar þess á himninum við stjörnumerkið Bogmanninn og stjörnumprýtt svæðið við miðju okkar Vetrarbrautar.

Review: Constellation identity/shape, Sagittarius, unaided visibility and stellar-cloud relation corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: R Coronae Australis er sjáanleg ekki án þess að það liggur í smáum, þrúgulegum stjórnum sem eru sjáanlegir af þeim þrúgulegum stjórnum sem eru í gegnum loftið og eru í miðjunni á sjálfu sjálfu galaksiðinu, Sýru-ávið.

</details>

<details><summary>final_semantic_review #353 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:1831

English: However fibreboards classified as class A will be accepted if they do not represent more than 50 % of the total wood and wood-based materials used in the product.

Reference (shown after audit): Trefjaplötur sem flokkaðar eru sem E1 munu þó samþykktar ef þær eru ekki meira en 50% af samanlögðu innihaldi viðar og efna úr viði sem notuð eru í vöruna.

Review: Wood becomes muscles; fibreboard/product terms corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þó mælt er fyrir um að fírbönd sem flokknaðir eru sem A-klópa séu samþykkt ef þau eru ekki meira en 50% af heildarvöðvum og vöðvabærum efni sem notaðir eru í lyfið.

</details>

<details><summary>final_semantic_review #354 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:179

English: These violent explosions rip through the molecular gas clouds in their immediate surroundings, but after the shockwaves have travelled more than about ten light-years they are weaker, and may instead compress clouds that are a little further away, triggering the formation of new generations of stars.

Reference (shown after audit): Höggbylgjur þessara orkuríku sprenginga tæta sundur sameindagasskýin í kring en eftir að þær hafa ferðast meira en tíu ljósár eða svo, hafa þær veikst en geta þjappað fjarlægari skýjum saman og þannig hrundið af stað myndun nýrra kynslóða stjarna.

Review: Weaker shockwaves becomes stronger, with remaining physical terms corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þessar brjálar eru ríkur í gegnum límdýr í loftbreytunum, en eftir að þær hafa farið lengra en tíu ljósjaríðum þar sem þær verða sterkari og geta í stað þeirra þróað loftbreytunum sem eru einnig nálægt og þeim hafa í stað þeirra íbúnaðar nýja jöfnu startra.

</details>

<details><summary>final_semantic_review #355 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:1138

English: “Terrestrial planets similar to our Earth are obvious targets for the search for life outside the Solar System, while comets are suspected to have played an important role in the appearance and development of life on our planet,” adds his colleague Emmanuël Jehin, who leads the cometary part of the project.

Reference (shown after audit): „Bergreikistjörnur sem líkjast jörðinni eru augljós skotmörk fyrir leitina að lífi utan sólkerfisins en halastjörnurnar eru taldar hafa leikið mikilvægt hlutverk í uppruna og þróun lífs á reikistjörnunni okkar“ bætir Emmanuël Jehin við en hann leiðir halastjörnuþátt verkefnisins.

Review: All corrupt terrestrial planets, comets, extrasolar life or colleague/project attribution.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: „Jafnvægilegir stjórnarheimjar, sýndir á landi, eru mikilvægir markstæður til að leita til lífs úti um í ljós herbergið, en hurðar eru óþolandi til að hafa haft mikilvægi í að útsiglingu og þýðingu lífs á jörðu okkar“, er Emmanuël Jehin, viðskiptavini hans sem stendur framhjá hurðabyrgum kerfisins, til að taka uppi með það.

Candidate 1: „Terstærjaprófnir sem eru svipaðir jörðu eru áknæmar vandamál til að leita á heimilum fyrir utan sviðsjöa sinni, þótt það sé óeðlilegt að eyðirur hafi haft mikilvægt hlutverk í fyrirkomu og þróun heimilsins á milli mínar, og að þeir eru möguleg að hafa verið að eðlilegum kosti í andlíndum verjum sem vaka að verja lífina á milli mínar“, er Emmanuël Jehin, aðila þeirra hagsmuna sem stjórna hluti úr eyðirunum, sem er aðstoðari í því.

Candidate 2: „Allt eins á jörðu, eins og jarð, eru ótrúlegar aðstæður fyrir söguna á ósláuræðinum þegar í gjöld er að finna líf utan helvítisfelldar einingsins, aðeins meðan eggjar fylla illa á að hafa haft mikilvæg áhrif á því að lifur séu hafa virði upp í eðlisþættun á jarðinni,“ útbúa Emmanúl Jehin, eiginmann sem leitar í gegnum eighjara, mælt með það.

Candidate 3: „Jafnvægið milli jörðarinnar og eimanns innihaldi er ógandi markmiði til að leita til lifar utan kjallsvæðisins en aflöngur eru óvæntir að hafa haft mikilvægt hlutverki í aðkomu og aðraðferðingum lifar á jörðinni“, er Emmanúël Jehin, viðtakinn í aflönga hluta verkefnisins, í mikilvægustu lagi.

Candidate 4: „Stjörmyrjarar, sem eru sömu og Jörðin, eru ályktar atburðir fyrir að finna lifi utan sýrustarfelldar og, með ávinningi úr því að flestar sýrjar hafi gert mikilvægt hluti af því að lifi á jörðinni,“ talar Jehin, aðli þeirra, sem stendur með sýrjaheimsbólgu.

Candidate 5: „Jörðar, sem eru svipaðar jörðum okkar, eru ósorðar vörur fyrir að finna fólk úti hjá síðlum sjóðarhæðirnar, og meginþurrðir eru taldar að hafa haft mikilvægu hlutverki í þeim sviði að fólk séu útbrednuð út úr jörðinni.“ Talar við Einnu Jehin, samfélaga, sem hefur stjórn á þeim hluta vefjarhópsins sem gerir fólk úti hjá síðlum sjóðum.

Candidate 6: „Gemstæðir planeter sem eru líklegir á jörðinni eru ótrúlegar markstæður fyrir sáning á að fundast á lifi fyrir utan helvítismál, sem við höfum hefur í huga vegna hve mikil vefur getur verið í þessu ákvörðun, þótt mynst við að gangur hafi haft mikilvægt hlutverki í þeim tíma sem lifur í vegum til baka lifi í geymslu jörðarins og þeim þar sem hún er meðgengin,” talar stefnufræðinginn Jehin, sem hefur stærðfræðingaforsamning um ganga í gangvöru, sem leiðir í gegnum ákvörðun um gangvörunir í gegnum gangvöru.

Candidate 7: „Útræðirurjarðir sem eru samskipti með jörðinni eru kynnulegur markað fyrir leit að því að finna líf utan hjárlaflokkins, en munnar eru taldar að hafa haft mikilvægar hlutverki í þeim að því sem lifið var að búa á jörðinni okkar og í þeim að því sem lifið var að rísta í jörðinni,” tilkynnist Emmanuël Jehin, samleiðandi í leiðirum um munnar, sem leiga lífið í munnarmálaríkinum.

</details>

<details><summary>final_semantic_review #356 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:970

English: In patients with mild hepatic impairment (Child-Pugh A), there was no significant changes in pharmacokinetics compared with normal healthy volunteers.

Reference (shown after audit): Hjá sjúklingum með væga skerðingu á lifrarstarfsemi (Child-Pugh A) voru engar marktækar breytingar á lyfjahvörfum samanborið við heilbrigða sjálfboðaliða.

Review: All corrupt mild hepatic impairment and/or healthy-volunteer comparator; most substitute healthy patients.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Hjá sjúklingum með mjöglega aukningu lifrarverkunar (Child-Pugh A) var engin merkilegur breytingar á lyfjahvörfunum samanborið við heilbrigðum heilbrigðum sjúklingum.

Candidate 1: Hér átti ekki markmiðandi breytingar á lyfjaplöntun í sjúklingum með mjög svona fínum lifrarfræðilegum áhyggjum (Kind-Pugh A) en hjá heilbrigðum heilbrigðum sjúklingum.

Candidate 2: Í sjúklingum með mjög lítila lifrarfrakkna (Child-Pugh A-tíðna) var engin merkilegt breytingar á lyfjahvörfum samanburðandi við venjulega heilbrigðan sjúklinga.

Candidate 3: Hjá sjúklingum með mjög leitt lifrarverkun (Kind-Pugh A) var engin markvægir breytingar á lyfjahvörfum samanborið við heilbrigðan heilbrigðan heilbrigðir sjúklinga.

Candidate 4: Hjá sjúklingum með mjög óþægilega lifrarþrýsting (k. á Child-Pugh skilyrði) var engin merkileg breytingar á lyfjahvörfunum samanborið við heilbrigðum heilkynjuna.

Candidate 5: Í sjúkdömmum með mjög leifa lifrarverkun (Child-Pugh A.) var engin merkilegur breytingar á lyfjahvörfum samanborið við heilbrigðan heilaverkin úr ljósi.

Candidate 6: Í sjúklingum með mjög lítila lifrarþurrð (Child-Pugh A), var engin merkileg breytingar á lyfjahvörfum samanborið við heilbrigðum heilbrigðum sjúklinga.

Candidate 7: Hraða lyfsreinnsins var ekki breytt mjög fyrir akvörðunarklíníkuna (C-Pugh A) við sjúklinga með smila vá á lifrarstarfsemi.

</details>

<details><summary>final_semantic_review #357 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:918

English: "With such short orbital periods, the planets are between 20 and 100 times closer to their star than the Earth to the Sun. The structure of this planetary system is much more similar in scale to the system of Jupiters moons than to that of the Solar System," explains Michaël Gillon.

Reference (shown after audit): „Umferðartímarnir eru svo stuttir að reikistjörnurnar eru 20 til 100 sinnum nær móðurstjörnunni en Jörðin frá sólinni. Uppbygging þessa sólkerfis svipar því meira til Júpíters og tungla hans en sólkerfinu okkar,“ segir Michaël Gillon.

Review: Sun/orbital periods and Jupiter-moon scale comparison corrupted; attribution omitted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: „Með slíku mikilvægri umferðarfrímiðna skipta eru jörðirnar á 20 til 100 sinnum nærri stjörnu sínum en Jörðin er til Sýruins. Stjórnun þess jörðarinsins er miklu nægilegari í tengslum við Júpiter-muna og Jörðinni en Jörðinni og Sýruins. „“

</details>

<details><summary>final_semantic_review #358 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:409

English: Purpose: to determine whether the test facility, if engaged in studies using animals or other biological test systems, has support facilities and conditions for their care, housing and containment, adequate to prevent stress and other problems which could affect the test system and hence the quality of data.

Reference (shown after audit): Markmið: að ákvarða hvort prófunarstöðin, ef þar eru stundaðar rannsóknir með dýr eða önnur líffræðileg prófunarkerfi, hefur yfir að ráða búnaði og aðstöðu þar sem hægt er að hirða um þau, koma þeim fyrir og einangra þau á annan viðeigandi hátt þannig að koma megi í veg fyrir streitu og önnur vandamál sem gætu haft áhrif á prófunarkerfið og þar af leiðandi á gæði gagnanna.

Review: All corrupt care/housing/containment or stress-prevention requirements.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Tilgangur: að ákvarða hvort prófunarstöð varðar prófunarskyni, ef hún er í rannsókn sem notaðir eru til prófunar á dýrum eða öðrum lífsvísindatækjum, hafi stöð og skilyrði til þeirra að rannsóknum og eðlilegum og til þess að tryggja að skemmtun og önnur vandamál sem geta haft áhrif á prófunartækifa og þannig aðgengt yfirvöld upplýsinganna.

Candidate 1: Tilvandareign: að ákvarða hvort prófunarstöðin, ef hún er í starfsemi með rannsóknum á dýrum eða annarri lífleysilegu prófunarsystum, sé með aðstoðarstöðu og skilyrðum fyrir umsókn, búnað og geymslu með fullnægjandi hætti til að koma í veg fyrir vöðv og önnur vanda sem gætu haft áhrif á prófunarsystuna og því hlýti að vera í lagi við gæði upplýsinganna.

Candidate 2: Tilvinnisatriði: að koma ákvörðun um hvort prófunarstöðin, ef hún er áfram í rannsóknir sem nota hafa verið með dýrum eða annarri lífleysilegu prófunarstarfsemi, hefði geymsluþættum og skilyrðanum fyrir viðhald, búnað og öskjandi hlíðun fyrir það, sem auk þess eru nægilegt til að fjarlægja stökkbreytingar og aðra vandamál sem geta haft áhrif á prófunarstarfsemi og hve góð verður grein半.

Candidate 3: Tilvísun: að ákvarða hvort prófunarfélag, ef það er notuð í rannsóknum með dýrum eða öðrum lífleiðis prófunarfólki, hafi gæðatæki og skilyrði fyrir meðhöndlun, heimsókn og uppfylltu, til þess að forðast þræðingu eða öðrum vandamálið sem gætu haft áhrif á prófunaflokkin og svo hafi áhrif á gildi gögn.

Candidate 4: Markmið: að koma á umholsfræðilega fundið hvort prófunaraðilið, ef það stendur við rannsóknir sem notaðar eru á dýrum eða öðrum lífssýslum, sé meðhöndlarstofa og gögn fyrir þau og búnað til að veita þeim tækifæri til að veita og veita þeim þá aðstæður sem tryggja að þau séu búin og búin í huga, fá fíknandi aðstoð til að örugglega veita fullnægjandi upplýsingum til að gæta áhættu og annars slíks og mæla hvernig prófunarseldurinn er.

Candidate 5: Tilvísun: að ákvarða hvort prófunarstöðin, ef hún er í staðgjöf til rannsókna sem notað er við dýr eða önnur líffræðileg prófunarefni, hafi rækt þáttkvæmi og skilyrði fyrir fjölskyldunirnar og hópna fyrir þeim, sem eru nægileg til að forðast strósinu og önnur vandamál sem gætu haft áhrif á prófunarefnið og hér að framan ákvarða gildi gagna.

Candidate 6: Tilvísun: að ákvarða hvort prófunarstöðin, ef hún er að ræða, með notkun dýra eða öðru líflegeðra prófunaraðferða, hafi stjórnvörn og stöðugleika fyrir hugsanlegri veitingu, heimili og búnaðskipti, sem nægilega er til að koma í veg fyrir stofnunarþrýsting og önnur vandamál, sem geta haft áhrif á prófunarstarfsemi og háðar gildi upplýsinganna.

Candidate 7: Tilvindi: að koma ákvörðun um hvort prófunarstöðin, ef hún er í aðferðir með dýrum eða annara líffræðilegum prófunarstöðum, hefðir viðmiðunarréttindi og veita skilyrði til hjálp, búnaðar og bælingar, sem fylgjast með fullnægjandi fyrirfram við að stöðva þróun og aðra áhættu sem gætu haft áhrif á prófunarstöðina og sem eiga áhrif á gildi gögnanna.

</details>

<details><summary>final_semantic_review #359 · old08 · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:1121

English: Of course you're right, Starling... but it doesn't change anything.

Reference (shown after audit): Auðvitað er það rétt, Starling... en það breytir engu.

Review: You are right and nothing changes retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Þú hefur rétt fyrir þér, Starling, en það breytir ekki neitt.

</details>

<details><summary>final_semantic_review #360 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:879

English: If more than one water source is utilised for fish production, fish representing all water sources must be included for sampling.

Reference (shown after audit): Ef vatn úr fleiri en einni lind er notað við fiskframleiðslu skal velja fisk úr öllum vatnslindum til sýnatöku.

Review: Fish representing each water source and sampling requirement not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef meira en einn vatnsstöð var notað til fiskeiðar skal taka í samræmi við öll vatnsstöð sem notaðar eru til fiskeiðar.

</details>

<details><summary>final_semantic_review #361 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:568

English: This device shall reverse the window/roof panel/partition before it exerts a pinch force of more than 100 N within the opening of 200 mm to 4 mm above the top edge of a power-operated window/partition or in front of the leading edge of a sliding roof panel and at the trailing edge of a tilting roof panel.

Reference (shown after audit): Þessi búnaður skal enduropna gluggann/þaklúguna/skilrúmið áður en klemmuaflið nær gildinu 100 N, innan ops sem er 200 mm til 4 mm yfir efri brún rafstýrðrar rúðu/skilrúms eða framan við leiðandi brún rennandi þaklúgu og við aftari brún þaklúgu sem er hnikað til.

Review: Powered-window/roof/partition pinch-force geometry corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þessi tæki skal endurleiða glugganefndina/þrýstuglugganefndina/þátturinn/þátturinn áður en hún virkar með meira en 100 N á þynningi innan opningsins 200 mm til 4 mm yfir ytri hlið þeirra styrklegra glugganefndar/þáttanna eða á foran ytri hlið þeirra styrklegra glugganefndar/þáttanna og á eftir ytri hlið þeirra styrklegra glugganefndar/þáttanna.

</details>

<details><summary>final_semantic_review #362 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:1557

English: The Commission Communication ‘i2010 - A European Information Society for growth and employment (COM(), developing the Lisbon strategy, seeks to ensure coherence across the Commission's information society and media policies in order to reinforce the significant contribution of information and communication technologies to the performance of the economies of Member States.

Reference (shown after audit): Í orðsendingu framkvæmdastjórnarinnar „i2010 – upplýsingasamfélagið í Evrópu í þágu hagvaxtar og atvinnu“(COM (), þar sem Lissabon-áætlunin er útfærð, er leitast við að tryggja samræmi innan stefnu framkvæmdarstjórnarinnar um upplýsingasamfélagið og fjölmiðla í því skyni að styrkja mikilvægt framlag upplýsinga- og samskiptatækni til efnahagslegrar afkomu aðildarríkjanna.

Review: Lisbon/ICT/media-policy and economic-performance relations replaced by repetitive agreement text.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Framkvæmdastjórninni er búin að gera þátttöku í þeirri samningu „i2010 - Evrópskri upplýsingasölu fyrir þróun og starfsemi“ (COM), sem er í þeim skýrslum sem eru í þeim tilviki sem þátttöku í þeim samningi er búin að gera, að tryggja samræmi á upplýsingasölu og viðkomandi þátttöku í þeim samningi sem þátttöku í þeim samningi er búin að gera, til að styrkja mikilvægu þátttöku upplýsinga og tölfræðis sem er búin að gera, í starfsemi aðildarríkja.

</details>

<details><summary>final_semantic_review #363 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:eea:615

English: Annual days of sick leave not paid by the employer (optional).

Reference (shown after audit): Árlegur fjöldi leyfisdaga vegna veikinda sem vinnuveitandi greiðir ekki (valkvætt).

Review: Not paid by employer becomes shall be paid, reversing polarity.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Árslegur sjúklastarfag sem fyrirtæki skulu greiða (ákveðið).

</details>

<details><summary>final_semantic_review #364 · old08 · G8 · technical_medium · U</summary>

Source ID: p13official21:test:ema:1433

English: Aseptically add sodium pertechnetate (Tc 99m) solution (from step d above) to the tilmanocept powder vial.

Reference (shown after audit): Bætið með smitgátuðum hætti natríum pertechnetate (Tc 99m) lausn (úr skrefi d hér á undan) í hettuglasið með tilmanocept stofninum.

Review: Candidate0 roughly retains aseptic addition/solution/vial, but pertechnetate and powder wording uncertain; others lose asepsis or objects.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Aseptísku bætið nátríumsertektanat (Tc 99m) lausn (breytt úr d áðan) með tilmanocept puffínum hettuglasi.

Candidate 1: Flettað samsetjinga natríum pertektænati (Tc 99m) (lísning úr blaði að hlið d hér á öðrum) á töfluna tilmanócceptor í hettuglasinu.

Candidate 2: Aseptíska efnisbundna blöndun skal verða svo:

Candidate 3: Vökvaðu nátrium pertektanat (Tc 99m) lausn (eitt úr d ryðju hér fyrir F) í tilmanocept hettuglas.

Candidate 4: D), á Natriumpertektanat (Tc 99m) lausn (fram í d-stigi hér á voru) með tilmanocept puffið.

Candidate 5: Þaðarlega aukið nátrýn pertaktént (Tc 99m) lausn (e. from step d) í hettuglasinu með tilmanocept pulveri.

Candidate 6: Breytja skal natríum pertektanat (Tc 99m) lausn (fræinn úr d lið í höfðinni) á púðri tilmanócept.

Candidate 7: Takað á prófuni skal nota natríumertektanat (Tc 99m) lausn (fjárhættu úr d. - stigi hér á öðru viðbótarlið) í tilmanocepti puffi.

</details>

<details><summary>final_semantic_review #365 · old08 · G8 · technical_short · P</summary>

Source ID: p13official21:test:ema:635

English: Table 4 provides dose modification guidance for dinutuximab, GM-CSF and IL-2.

Reference (shown after audit): Tafla 4 veitir leiðbeiningar um skammtaaðlögun dínútúxímabs, GM-CSF og IL-2.

Review: Candidate3 retains Table4 recommendations for dose changes of all three named treatments.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [3]

Candidate 0: Í töflu 4 eru búnaðurstefnir til að veita leiðbeiningar um skammtamögnun fyrir dinutuximab, GM-CSF og IL-2.

Candidate 1: Í töflu 4 eru leittar ráðlegar fyrir skammtaleiðbeiningar fyrir dinutuximab, GM-CSF og IL-2.

Candidate 2: Í töflu 4 er ákvarðaður skýrslu um skammtamögbundin efnasýringu fyrir dinutuximab, GM-CSF og IL-2.

Candidate 3: Í töflu 4 eru tilmæli gefin um breytingar á skammti fyrir dinutuximab, GM-CSF og IL-2.

Candidate 4: Í töflu 4 eru heimiltarkönnunargreinir fyrir dinutuximab, GM-CSF og IL-2.

Candidate 5: Í töflu 4 eru búnaðarlegar leiðbeiningar fyrir skammtabreytingar fyrir dinutuximab, GM-CSF og IL-2.

Candidate 6: Í töflu 4 eru leyfðir til að þrýstingarnar á dinutuximab, GM-CSF og IL-2 verði breytt.

Candidate 7: Í töflu 4 eru veittar leiðbeiningar um ávörslu við skammtahækkun innrennslisvörnssýklunarins, rýmisfýrlýslustimansins og IL-2.

</details>

<details><summary>final_semantic_review #366 · old08 · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:3404

English: A mother never gives up on her child.

Reference (shown after audit): Móðir snýr aldrei baki við barni sínu.

Review: Never giving up on child idiom becomes laying up, changing meaning.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Móðir leggur aldrei upp á barn sitt.

</details>

<details><summary>final_semantic_review #367 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:179

English: These violent explosions rip through the molecular gas clouds in their immediate surroundings, but after the shockwaves have travelled more than about ten light-years they are weaker, and may instead compress clouds that are a little further away, triggering the formation of new generations of stars.

Reference (shown after audit): Höggbylgjur þessara orkuríku sprenginga tæta sundur sameindagasskýin í kring en eftir að þær hafa ferðast meira en tíu ljósár eða svo, hafa þær veikst en geta þjappað fjarlægari skýjum saman og þannig hrundið af stað myndun nýrra kynslóða stjarna.

Review: All corrupt explosions/molecular gas/shockwave weakening/farther-cloud compression and star formation.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Í urðum skrífas verðum verða það sem rífa um á meðan fljótt eða í viðmiðunum á meðan ofan á þeim fljóta hafa fullnægt tæki. En ef um benti eru lengi lengra en tíu einn ljósjarðarþúsundra, komið stjórnandi þau eigi síðan gegnum þar og þeir gerast stærri og hafa annað leið farið í samræmi með þeim fljóta sem varnað eru einnig um mikla frekar en þessu, og þessa til þess að þau geti verið sátt í nýttu þroska starhafa.

Candidate 1: Þessi jarðræðingar eyða skilja um í uppþrosku í loftlausnaðum sem eru fyrir sig, en eftir um fljóttarannskotirnar kannu hafa flutuð meira en tana ljósjungrjóða þá þeir eru minni, og gæti í stað þeirra fyllt upp á loftlausnurnar sem eru aðeins háttar framar, og skilju að upphafu nýjum gera af starjarnar skjöl.

Candidate 2: Þessar orvísandi brýnin rískar aftur í gegnum diðnaðarþjárhitaum á närðargreinum þeirra, en eftir að skrýðunarmörkurnar hafa farast lengra en tíu ljósjar á milli hafa þau verið svæfari, og gætu eitthvað í stað þeirra þróaðir tæthapsa sem eru aðeins langt fyrirfram og í skapunum núgetur nýr háðúðir.

Candidate 3: Þessar hræðileg erubrulur brjáða í vísindagæsu þjónustu í viðkomandi stað mennta en þau fljóta mátt eftir þeim aðraðskipti, sem fást um fleiri en tíu ljósgjarna, verða sterkari og geta því, í stöðugum tilviki, þróaðu upptek og þróaðu nýjum tímannum á starð.

Candidate 4: Þessi stríðar upprúngir í gegnum líffraðar viðskiptavörunarblað þegar þeir eru í viðhaldi, en þegar hreyflana hafa farið út í lengra en tíu ljósjarásárs tekur þau sterkni og muni því svo aðum, og gæti í staðinni er hafnað um loft í langt af stað sem stöðvur að neytja til þess að tekja fram nýttu sjálfu andlausrannir starfsemi.

Candidate 5: Þessi brjálagræða blöðúðum rífa koma í samræmi við mikill í næstu æðum, en eftir að þau hafa farið lengri en tíu ljósjarbæjar eru þeim þykilega vart, og þó geta þau þótt smá þögun blöðum sem eru nema þær mjög langt, sem íbúna starfsmenn.

Candidate 6: Þessar spælarbrjálar riggja þroska á loftra loftdæmi í öðrum hlutaðeigandi þáttum en eftir hreyflarnir hafa flaug lengra en að tíu þáttum litla þar eru þeim sterkari og má í stað þeirra flýja loftdæmi sem eru mjög frekar þangaðar en það, og þar geti komið fram nýjar ájörnum stjörnu.

Candidate 7: Þessar alvarlegar auðskotti ríðast um í gegnum molekúluspaltirnar í næsta umhverfi þeirra en þar eftir þeim er fljóttþrjósað og hafa lengra en tíu ljósmyndahraða í lengi slysust og mæta þá er hægt að þótti þá klúddirnar að hafa frekar nærri og þeim ístindar starðhópur sem hafa nýtt veru.

</details>

<details><summary>final_semantic_review #368 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:2652

English: Put the needle fully into the skin as shown by your nurse or doctor (see picture 6).

Reference (shown after audit): Stingdu nálinni í húðina eins og læknirinn eða hjúkrunarfræðingur sýna þér (sjá mynd 6).

Review: No candidate preserves needle/full insertion plus nurse-or-doctor demonstration; nurse or needle terms are corrupted.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Settu nálinni fullu í húðina eins og hjá lífmeðferðarfélögum sem sjá á henni (sjá myndin 6).

Candidate 1: Nálinni setja fullt inni í húðina eins og varðandi eða lyfjameðanda (sjá mynd 6).

Candidate 2: Settu nálinni fullkomlega inni í húðina eins og lyfjaheimila eða læknir kenna í mynd 6.

Candidate 3: Settu þannig strakið fullu inn í húðina eins og venjúð eða lækni sýnir (sjá mynd 6).

Candidate 4: Settu nálinni þannig yfir sig sem vögðinn eða læknirinn sýnir í mynd 6.

Candidate 5: Settu nyðina fullsækilega inn í húðina eins og hjúkrunarfræðingur eða læknir sillust á (sjá mynd 6).

Candidate 6: Settu nálinn vel inn í húðina eins og að=minn staðallinn sýnir (sjá mynd 6).

Candidate 7: Taktu nálinni fulla inn ið húðina, eins og hjá þér eða lækninum er sýnt (sjá mynd 6).

</details>

<details><summary>final_semantic_review #369 · old08 · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:936

English: Ma'am, I need the gentleman's signature so we can begin.

Reference (shown after audit): Ég þarf að fá undirskrift hans svo við getum byrjað.

Review: Signature becomes unspecified written material; request object not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ég þarf að fá skriflegu þessu góðarmanns svo við getum byrjað.

</details>

<details><summary>final_semantic_review #370 · old08 · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:2721

English: No, but one day, I'll take that cane away...

Reference (shown after audit): Nei, en einn góðan veðurdag á ég eftir að taka stafinn...

Review: Cane and taking it away not retained.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Nei, en einn daginn, fá ég þennan handvökin...

</details>

<details><summary>final_semantic_review #371 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:881

English: Using standard candles - such as the variable stars within IC 1613 and the less-common Type Ia supernova explosions, which can seen across far greater cosmic distances - astronomers have pieced together a cosmic distance ladder, reaching deeper and deeper into space.

Reference (shown after audit): Með hjálp staðalkerta eins og breytistjörnunum í IC 1613 og sprengistjörnum af gerð Ia, sem sjást úr mikilli fjarlægð í geimnum, hafa stjörnufræðingar smíðað fjarlægðarstiga sem nær lengra og lengra út í geiminn.

Review: All corrupt standard candles, variable stars/TypeIa supernovae or cosmic-distance ladder.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Heimstólpar, eins og hlutfallslega stígur í IC 1613 og áttara vel sjaldgæfur Ic Ia supernova eru þeir sem leiðrétta áfram í mikilvægur kosmosfarvæla á út frá langt hámarki út fyrir mikilvægur kosmosfarvi.

Candidate 1: Absamræðaraðferðir með staðlínum - eins og móðkyltur heta í IC 1613 og meiri sjónþóga eru á vopnumhliðum með því að sjá yfir fjarlægðarmennislegt rými - soúrinfræðingar hafa fyllt upp nýleg skilvirkni rýmstuðurs í mikilvægri farannar, síðar í rými.

Candidate 2: Óstöðgul körlur, eins og tilgreindur stjörnur í staðbók 1613 og tvímunar alþjóðlegamjaldarvilla að hámarki sem eru sjálfsögðir yfir langt, hafa ífangalegur stjórnmenn ísett upp sumastig framan í himnið sem fjallar yfir lengri stöðurnar í heimi.

Candidate 3: Nefndar hljóða af staðbundna sólum eins og viðurkenndum staðundum í IC 1613 og hljóðum sem rísa í meiri og meiri kosinormið, sem eru færari en sjaldgæfir, að því er varðar stöðvunarboð sem gerist upp á kosinormið með miklum þynningu.

Candidate 4: Hér er hreint gefinn frá þessu: Vesturlitarnir, eins og rýmarnir sem eru í IC 1613 og mjög sjaldgæfar alþótt ódýrskar stregaýjur, sem eru tilkynntir á frábært skipti á fjárlegri hátt, hafa fengst með grípa á áfenginni tíandýra skilni í kosmikiðri áfæri.

Candidate 5: Nefndarhlíð undir sjó stundmálssviðs, eins og gefnanefndar í tækniflokkinni 1613 og mjög sjaldgæfandi jörðavörf sýndingar í Type Ia fjararóðvirðingum, sem sjáum svo miklu langt af stað til að lesa, eru stjörnuburðar að falla þar til þau nærast í yfirleitt fararíki.

Candidate 6: Hins vegar hafa Strangerum fengið að sækja kosinísstigið af stóðum sáttbærum - sem stórtar stierar eru í náttúruhlutinu í IC 1613 og mikið aðrar sturtar eru, sem eru mörgu miklu hámarks að munu, sem eru sýnir út frá mikla kosiníðsstað.

Candidate 7: Með því að nota staðfestar kólnur, eins og breytilegir stjörnur innan IC 1613 og lækna sjávarunaldra eyðubola sem hafa leitt eftir langt aukargrafa, hefur stjórnaðirnir samstælt í starfsemi kosin fyrir lengi lengra rökstaða, þar sem eðlir og rökstaðar inni í himnið.

</details>

<details><summary>final_semantic_review #372 · old08 · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:1803

English: What are you planning on telling her?

Reference (shown after audit): Hvað ætlarðu að segja henni?

Review: Exact source/hypothesis semantic reuse from card85: Question about what to tell her preserved.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Hvað ætlarðu að segja henni?

</details>

<details><summary>final_semantic_review #373 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:ema:3025

English: Based on individual patient response and tolerability, the dose may be increased to 300 mg (15 ml) per day after an interval of 3 to 7 days, and if needed, to a maximum dose of 600 mg (30 ml) per day after an additional 7-day interval.

Reference (shown after audit): Eftir svörun og þoli hvers sjúklings má auka skammtinn í 300 mg (15 ml) á sólarhring eftir 3-7 daga og ef þörf krefur í hámarksskammt, 600 mg (30 ml) á sólarhring, eftir 7 daga til viðbótar.

Review: Individual response/tolerance and maximum/additional-interval constraints lost.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þar með skýtur sjálfstæður sýni sjúklinga og ekki hægt er að draga úr þessu má aukast skammturinn í 300 mg (15 ml) á sólarhring eftir 3 til 7 daga skipti og ef þörf krefur er má hægt að aukast skammtinn í 600 mg (30 ml) á sólarhring eftir 7 daga skipti.

</details>

<details><summary>final_semantic_review #374 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:ema:1152

English: Change from baseline in body weight was similar for patients treated with sitagliptin relative to placebo.

Reference (shown after audit): Breytingar á þyngd frá grunnlínu voru svipaðar fyrir sjúklinga sem meðhöndlaðir voru með sitagliptíni miðað við þá sem fengu lyfleysu.

Review: Change from baseline omitted; similar body-weight value is not similar change.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það var sama hvort sjúklingar með sitagliptin og lyfleysu varðar líkamsþyngd í staðbúnaði.

</details>

<details><summary>final_semantic_review #375 · old08 · G8 · technical_medium · P</summary>

Source ID: p13official21:test:eea:1509

English: Therefore, in the interest of clarity of legislation, it is appropriate to merge those provisions in one single legislative act.

Reference (shown after audit): Til að tryggja gagnsæi í löggjöf er því rétt að sameina þessi ákvæði í einni lagagerð.

Review: Candidate4 retains combining provisions into one legislative instrument for clearer legislation, rendered regulation.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [4]

Candidate 0: Því er rétt að blanda þessar ákvæði í eina reglugerð.

Candidate 1: Því er rétt að samsetja þessar ákvæði í einn frumreglugerð í þjónustuna á klárnu frumreglinu.

Candidate 2: Því er rétt að samlaga þau ákvæði í einn aðgerða reglugerð við hættu á skýrleika á löggjöf.

Candidate 3: Því er rétt að samsetja þessar ákvæði í öðru leyfi.

Candidate 4: Til að skýra löggjöf er rétt að samsetja þessar ákvæði í eina reglugerð.

Candidate 5: Því, að varðar skilvirkleika lögaðgerðanna, er rétt að flutti þessi ákvæði í einu löggjöf.

Candidate 6: Því, í þátttaka áfanga krefjandi, er rétt að samsetja þessa ákvæði í öðlu skuldbindingu.

Candidate 7: Ef við miðlun á skýrleika reglna er rétt að samsetja þessu ákvæði í einum löggjöf.

</details>

<details><summary>final_semantic_review #376 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eso:716

English: From the gravitational lensing effect, these groups turn out to contain around 30 times more dark than visible matter.

Reference (shown after audit): Þyngdarlinsuhrifin sýna að hóparnir innihalda um 30 sinnum meira hulduefni en sýnilegt efni.

Review: No gravitational-lensing/dark-versus-visible-matter30times inference retained.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Í fjármagnshraustunum eru þessi hópa í um 30-faldum mikið muffið en sjáanlegur efn.

Candidate 1: Samkvæmt þróun bókurarinnar eru þeir flokka sem eru göngubúin í spjalli að 30-þar af þrýstingum og tyggjum.

Candidate 2: Af geðretningslæðingu eru þessi flokkar um 30 sinnum融入ra en sjáanlegi eitur.

Candidate 3: Í gegnum þarnaskiptaspektinum er þessi flokki til að innihalda um 30 sinnum fleiri vérlegra en skjaldar efnis.

Candidate 4: Af vökvuföngum stendur þessi flokk við um 30-faldur lengd sem ljóslegur efn.

Candidate 5: Af krabbaplásturskráðuntekja þeirra, sem eru stofnunin í mótaðri, verður í tengslum að það hafa um 30-faldur fleiri þyngdarlega skjald en sjáanlegi efla.

Candidate 6: Með þeim varðargræðisgreiningu gáfa þessi flokka um 30-svarðar fleiri dimmt og sjáanlegur efn.

Candidate 7: Af geðræðisbúlingu sækja þessi flokka innihalda um 30 sinnum mikið þótt þau séu orðin óhætt.

</details>

<details><summary>final_semantic_review #377 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:2125

English: In addition, the sub-processing should only consist of the operations agreed in the contract between the data exporter and the data importer incorporating the standard contractual clauses provided for in this Decision and should not refer to different processing operations or purposes so that the purpose limitation principle set out by Directive 95/46/EC is respected.

Reference (shown after audit): Þá skal ráðstöfun til undirverktaka aðeins fela í sér þær aðgerðir sem samþykktar eru í samningnum milli gagnaútflytjanda og gagnainnflytjanda og sem inniheldur föstu samningsákvæðin sem kveðið er á um í þessari ákvörðun og þessi ráðstöfun skal ekki ná yfir annars konar gagnavinnslu eða hafa annan tilgang svo að meginreglan um takmörkun vegna tilgangs, sem sett er fram í tilskipun 95/46/EB, sé virt.

Review: All corrupt sub-processing, data export/import contract or purpose-limitation relationship.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Einnig skal aðstæður að aðgerðir þeirra, sem samþykktar eru í söluáætluninni milli djúpupplýsingusendur og upplýsingasendur, innehalda stöðluðum samningsreglum, sem kveðið er á um í þessari ákvörðun, en ekki til neinn aðferðir sem eru í framanum, svo að mörk á því að því sem áður hefur verið í tilskipun 95/46/EB verði búið við.

Candidate 1: Einungis þarf að gera undirréfningu að því að framkvæmdarfyrirtæki hafi sameiginlega samþykkt að því að bæta styrk í hönnuninni úr röðnilegu samningsskilyrðum sem mælt er fyrir um í þessari ákvörðun og til að hafa ekki að telja að einhverri reikningaþróunum sé veitt aðmið til þess að mæla áttir eða undirgreinir við þegar um það segið sé í þessari ákvörðun þannig að meginreglur, sem mælt er fyrir um í tilskipun 95/46/EB, sé gert við.

Candidate 2: Einnig skulu aðrar aðferðir samþykktar samningsinnar milli datahleðslunarökurákvörðunar og datahöndsluökurákvörðunar varða aðgerðir og staðfestingar sem eru í staðbundinni samningsákvörðuninni sem kveðið er á um í þessari ákvörðun og skulu ekki megra aðgerðir samanburðar þar sem er tekin á meðferð í staðbundinni samningsákvörðuninni sem gerð er í tilskipun 95/46/EB.

Candidate 3: Aðrar en aðeins skal skipta aðferðirnar um aðgerðir sem samþykkt er á í samninginu, sem þjónustuaðilaðila með aðgerðahópnum og aðgerðahópnum aðila, skulu innihaldi andlitið verslunarsamningsskildu, sem kveðið er á um í þessari ákvörðun, og hún á að ekki taka til tiltekna aðgerða eða áætlaðanna, svo þessari aðgerðarskrá, sem um getur í tilskipun 95/46/EB, sé gert.

Candidate 4: Að því er varðar aðrar aðferðir, skal einkum aðferðirnar aðeins taka upp þær gerðar sem samþykktir eru á um í samninginu milli yfirborðarinnar á grein síðar en innflutningarsvæði sinnar og innflutningarinnar og viðkomandi stöðluð samningsklúður skv. ákvæði þessarar ákvörðunar og skal hvarfingurinn ekki tilgreina mismunandi aðferðir eða viðmiðun þeirra, svo að meginreglurinn, sem í tilskipun 95/46/EB stýrir að ámólinu, sýnar upp á, versti.

Candidate 5: Einmitt skal ekki gera greiðsluna með sér aðferðir sem samþykktar eru á í samninginu milli datadómaverðsins og datadómamannsins, sem innihalda staðallan samningsreglur sem kveðið er á um í þessari ákvörðun, og ekki skýra í öðru verði og ástæðum það efni að því er varðar þá markmið sem mælt er fyrir um í tilskipun 95/46/EB.

Candidate 6: Að því er varðar aðferðirnar skulu einnig ekki slíkt endurbreyti sem ákveðið er á um í samninginu milli döllum sem slátó skipta upprunalegar upplýsingar í gegn aðgengisveitinni og þeir skulu ekki taka tillit til þessarar endurbreyti sem tekur til þess að mæla reglu um ákveðin mælingarskilyrði sem sett er fram í tilskipun 95/46/EB.

Candidate 7: Einmitt skal ekki gera sérstakaraðferðir, en aðgerðir sem eru samþykktar í skipti milli inntökumálastofnunarinnar og inntökumálastofnunarinnar og innihalda staðlað skuldbindingar sem kveðið er á um í þessari ákvörðunarþætti og ekki skal taka til ótryggt eins og varðar tiltekin áhættuþáð, svo að mæla einfaldlega yfir verkefnið sem hefur verið sett upp í tilskipun 95/46/EB.

</details>

<details><summary>final_semantic_review #378 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:1409

English: The port security assessment is the basis for the port security plan and its implementation.

Reference (shown after audit): Áhættumat fyrir höfn er undirstaða verndaráætlunar hafnar og framkvæmdar hennar.

Review: No complete port-security assessment as plan basis; some change port to airport and5 omits assessment.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Dæmi yfir vernd á liggandanum er grundvöllur fyrir plána um vernd á liggandanum og framkvæmd þess.

Candidate 1: Vegna þess erstaðist er skýrslan um öryggisvottorðið grundvöllur fyrir hagnað á öryggismarkmiðum og framkvæmdar samkvæmt henni.

Candidate 2: Vegna þess er matur á öryggi flugvelli grundvöllinn fyrir plánn um öryggi flugvalla og framkvæmd hennar.

Candidate 3: Íkomin við athugun reyðslustjórnunarinnar er grundvöllur áætluninni um reyðslustjórnunarinnar og framkvæmd hennar.

Candidate 4: Tilgangurinn fyrir öryggisvöttunarmiðstöðina er grundvöllur fyrir plan á öryggismálum og framkvæmd þess.

Candidate 5: Portaröryggiþið er grundvöllur áætluninni um portaröryggi og framkvæmd þess.

Candidate 6: Rannsókn á öryggi við flugvallinn er grundvöllinn til hennar pláns og framkvæmd hans.

Candidate 7: Tilvísun á öryggisvottorðið er grundvöllur til þess hvernig öryggisvottorðið verður að framkvæma.

</details>

<details><summary>final_semantic_review #379 · old08 · G8 · technical_short · P</summary>

Source ID: p13official21:test:ema:1918

English: The presented safety information is derived principally from paediatric patients.

Reference (shown after audit): Fyrirliggjandi öryggisupplýsingar eru einkum til komnar út frá börnum.

Review: Candidate7 conveys presented safety information principally from children, with patient context implicit.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: [7]

Candidate 0: Öryggisupplýsingarnar sem sýndar eru eru aðallega frá børnum með eiginleika.

Candidate 1: Öryggisupplýsingarnar sem tilnefndar eru eru aðallega fundnar frá börnum.

Candidate 2: Matin um öryggi sem er sýnd er aðallega úr bólgu börna.

Candidate 3: Þessar öryggisupplýsingar eru algengast aðilið af barnaþætti.

Candidate 4: Eftirtæki upplýsingar um öryggi eru aðallega fundarlegt frá börnum með klóftak.

Candidate 5: Upplýsingar um öryggi sem eru sýnð eru aðallega gagnrýnar um sjúkdóma barna.

Candidate 6: Upplýsingar um öryggi sem eru tilnefndar eru aðallega gagnmætt frá börnum.

Candidate 7: Upplýsingar um öryggi sem eru tilgreindar birtar eru aðallega frá börnum.

</details>

<details><summary>final_semantic_review #380 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eea:1144

English: Successful participation in interlaboratory studies that assess laboratory proficiency is the best way to prove the competence in specific analyses.

Reference (shown after audit): Árangursrík þátttaka í rannsóknum með öðrum rannsóknarstofum, þar sem frammistaða rannsóknarstofa er metin, er vænlegust til þess að staðfesta hæfni í sértækum efnagreiningum.

Review: Successful participation in interlaboratory proficiency work becomes business-science collaboration.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það er besta að sýna fram á hæfni í sérstökum greiningum með framkvæmdum í samstarfi viðskiptafræðilegra rannsókna í samvinnu rannsóknastofnana sem meta hæfni í rannsóknastofnunum.

</details>

<details><summary>final_semantic_review #381 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:278

English: Centaurus A has therefore been observed with many different telescopes.

Reference (shown after audit): Vetrarbrautin hefur þess vegna verið viðfangsefni fjölmargra ólíkra sjónauka.

Review: Telescopes becomes boundaries/limits.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Centaurus A hefur þó verið sjáðan með margt af mörkum.

</details>

<details><summary>final_semantic_review #382 · old08 · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:3044

English: Isn't there someone in some league, who's left- footed?

Reference (shown after audit): Er ekki einhver í einhverri svona deild sem er örfættur?

Review: League/left-footed relation not preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Er ekki einhver í einhverju leigu sem er ekki eftir föt?

</details>

<details><summary>final_semantic_review #383 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:ema:2650

English: Patients should be advised that in the event of any sudden visual defect, they should stop taking Sildenafil Actavis and consult a physician immediately (see section 4.3).

Reference (shown after audit): Ráðleggja á sjúklingum að hætta töku Sildenafil Actavis og hafa strax samband við lækni ef þeir finna fyrir skyndilegri sjónskerðingu (sjá kafla 4.3).

Review: Sudden visual defect and immediate consultation not retained.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Fyrir sjúklinga skal ráðfara að hætta að taka Sildenafil Actavis ef einhver einhverjar augnablikshættir koma fram og hafa samband við lækni (sjá kafla 4.3).

</details>

<details><summary>final_semantic_review #384 · old08 · G8 · technical_short · F</summary>

Source ID: p13official21:test:ema:1788

English: Magnetic resonance imaging is necessary to confirm the diagnosis of PRES.

Reference (shown after audit): Segulómun er nauðsynleg til að staðfesta greiningu PRES.

Review: No MRI confirming PRES; several invent diagnoses including presbyopia.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Gegnarmagnbreytislýsis er nauðsynleg til að staðfesta sjúkdóma alvarlegra blóðflóða.

Candidate 1: Verkileg magnetískar samræmingargerðir eru nauðsynlegar til að staðfesta ákvarðaniningu við sjúkdóma sem tengist húðvöðva í skríma.

Candidate 2: Gegnast er magntispröfung til að staðfesta sérstakara skilyrði vegna Presbyopia.

Candidate 3: Þýðslu með magnvísíum er nauðsynleg til að staðfesta ályktun um presýðun.

Candidate 4: Þurf er prófsýning til að staðfesta skilmæli um blóðflæðisræðisfrum (PRES).

Candidate 5: Magnetískan upprunaleiðbótarþynningu er nauðsynlegt að staðfesta álit um alvarleg farsveikun.

Candidate 6: Magnetísk vístunarmyndun er nauðsynleg til að staðsetja sýnatölu um skurðsjúkdóm.

Candidate 7: Magnetræistefnismyndun er nauðsynlegt til að staðfesta skynræni hjá sjúklingum með presúskun.

</details>

<details><summary>final_semantic_review #385 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:20

English: These galaxies span a vast range of distances from us.

Reference (shown after audit): Allar eru þessar vetrarbrautir í mismikilli fjarlægð frá okkur.

Review: Range of distances becomes anniversary.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þessi galáxir eru í miklu afmæli af framan okkar.

</details>

<details><summary>final_semantic_review #386 · old08 · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:136

English: ALMA is radically different from visible-light and infrared telescopes.

Reference (shown after audit): ALMA er gerólík sjónaukum sem sjá sýnilegt og innrautt ljós.

Review: No visible-light/infrared TELESCOPE comparison;6 omits telescope objects.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: ALMA er algerlega annar en þekkt af skýrheimum og inRéðarmörkum.

Candidate 1: ALMA er aðallega annað en ljósið og innræðandi þjónustueins.

Candidate 2: ALMA er örugglega fjárhættulegt gegnum ísjó og vatnsþyngdarmörk.

Candidate 3: ALMA er bráðastaklega ólíkt við þekkingarferlir sem sækja á ljósi og þurrkaugum.

Candidate 4: ALMA er rannsóknarþrýstingur ótébrislaus.

Candidate 5: ALMA er skiptilega annar en sjáanlegir og þrýstigar stajurnar.

Candidate 6: ALMA er algerlega annað en sýnileg ljósið og infrarauðsvit lið.

Candidate 7: ALMA er aðallega munurlegt við sýniitt og innreindum sýniittum.

</details>

<details><summary>final_semantic_review #387 · old08 · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:1317

English: General Barnicke's gone until tomorrow morning.

Reference (shown after audit): Barnicke kemur ekki fyrr en í fyrramálið.

Review: General title/absence becomes all-together/in storage; tomorrow-morning limit unclear.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Allsamt Barnicke er í geymslu þar til morguninn er kominn.

</details>

<details><summary>final_semantic_review #388 · old08 · greedy · technical_short · U</summary>

Source ID: p13official21:test:eea:1503

English: If this kind of costs exists, they will be reported separately.

Reference (shown after audit): Ef þess háttar kostnaður er fyrir hendi skal tilgreina hann sérstaklega.

Review: Conditional cost existence and separate itemization approximately recognizable, but defined versus reported wording is uncertain.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef þessi gerð kostar er skulu þau skilgreindir að sér.

</details>

<details><summary>final_semantic_review #389 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eso:502

English: The first five signals are very confident, while the sixth is tentative, and seventh more tentative still.

Reference (shown after audit): Fyrstu fimm merkin voru mjög sannfærandi en meiri óvissa ríkir um það sjötta og enn meiri óvissa um hið sjöunda.

Review: All corrupt five/six/seven signal order and confidence/tentativeness.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Fyrri fimm orð er mjög viss og sá sex er mótnýtt og sjötta enn framan mótnýtt.

Candidate 1: Fyrstu fjögurir eru mjög sérstök og sjóðusturðir sérstök, fegin fjögurir eru heldur veislustar, og heimin fjögurir eru heldur veislustar.

Candidate 2: Fyrri fjórðu skilarnir eru mjög áætlunargreindir, þótt sjólfur þeir séu óþægilegar, samt þær sjólfar eru óþægilegar, sjólfur þeir eru óþægilegar með sjólfum að þeim er fullnægjandi skil.

Candidate 3: Fyrri fjögur vörslir eru mjög sérstær og sjólfur, þótt sjólfur sjólfur seinni fjögur er óheimta og sjólfur sjólfur séin fjórðu.

Candidate 4: Fyrst fjögur ferli eru mjög beinólið og sex ferli er óeitt og sex fjarri er enn ofeitt.

Candidate 5: Fyrri fimm svörunar eru mjög sérstakt, sjóða sá hundrað. Það sjóða er hundraðinn og seht er hundraðinn lengur.

Candidate 6: Fyrri fjögur svörunir eru mjög óvissar, sjálfur tveggja fjórða svörun er ætíð og seðri konar svörun hefur verið áfyllt.

Candidate 7: Fyrri fjögur löggil eru mjög ákvarðanleg og fjölur er haft vandamál, hvetjan fjögurinn heldur eigið og fjögurinn fer í vandamál.

</details>

<details><summary>final_semantic_review #390 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eso:554

English: In the lower part of the image a big chunk of the molecular cloud that gave birth to these stellar youngsters still can be seen.

Reference (shown after audit): Á neðri helmingi myndarinnar sést stór hluti af sameindaskýinu sem gat af sér stjörnurnar ungu.

Review: Molecular cloud becomes core boundary; formation/visibility clauses corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Í niðri hluta myndarinnar er stór hluti kjarnamörkunnar sem gerðist þessa stjörnufræna yngri sem varð fram.

</details>

<details><summary>final_semantic_review #391 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:349

English: The results described here use some of these Science Verification data.

Reference (shown after audit): Gögnin sem notuð voru fyrir þessa rannsókn var að hluta til aflað við þessar prófanir.

Review: ScienceVerification data becomes custody of science.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Niðurstöðurnar sem hér eru lýst nota nokkrar þessar vörslur um vörslu vísindanna.

</details>

<details><summary>final_semantic_review #392 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eso:714

English: By studying this effect it is possible to map out the places where gravity is strongest, and hence where the matter, including dark matter, resides.

Reference (shown after audit): Með því að rannsaka áhrifin er hægt að kortleggja hvar þyngdarkrafturinn er mestur og þar af leiðandi hvar efnið, þar á meðal hulduefnið, er.

Review: Gravity becomes weight and dark matter becomes weight pressure.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þegar manum er leitt á þessu áhrif er mögulegt að markaða þar sem þyngd er stærst og þar sem efnið, þ.m.t. þyngdþrýstingi, er.

</details>

<details><summary>final_semantic_review #393 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:382

English: In the controlled clinical studies in chronic ITP with eltrombopag, increases in serum alanine aminotransferase (ALT), aspartate aminotransferase (AST) and bilirubin were observed (see section 4.8).

Reference (shown after audit): Í klínískum samanburðarrannsóknum á eltrombópagi hjá ITP-sjúklingum kom fram hækkun á alanínamínótransferasa (ALAT), aspartatamínótransferasa (ASAT) og bílírúbíní í sermi (sjá kafla 4.8).

Review: All corrupt controlled chronicITP study identity or enzyme/serum details;0 substitutes acute blood disease.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Í klínískum rannsóknum á meðferð með bráðablóssjúkdóma með eltrombopagu var dreifandi aukning á ALT (serum alanínamínotransferasa), AST (serum aspartatamínotransferasa) og bilirubínum (sjá kafla 4.8).

Candidate 1: Í klínískum rannsóknunum um beinleg breyting á ALT, AST og bilirubín í serum, í þroska ITP, sem áframhaldandi, kom fram (sjá kafla 4.8).

Candidate 2: Í kránmeðhöndlunarkerfi með ennsömu blóðþrýstingsleyfju (echimóbrólforag) sem varðar langvandi blóðþrýstingsleyfju (ITP), staðfestu þróun á helgíðjaskiljun (ALT) og þrýstingsleysisljufnum (AST) og bilirubíni (sjái 4.8).

Candidate 3: Í klínískum rannsóknunum á beinverum, á lægri hætti en við ITP, sem varðar eltrombopag, var sett fram þættun á loftþætti á alanínamíntransferasi (ALT), asparatamíntransferasi (AST) og bilirubín (sjá kafla 4.8).

Candidate 4: Í rannsóknunum sem varðar alvarlegan fullvísnaþvörun með eltrombólgi í líkama komu síðan að þörfum á aukningu á ALT (serum alaninamínotransferasa), AST (serum asparatamínotransferasa) og bilirubín (sjá kafla 4.8).

Candidate 5: Í klínískum rannsóknum á meðgöngusjúklingum með týpkó, sem varðar eltrombópaga, komu fram aukningur á ALT (alanínambrotþrýstingi), AST (aspartateambrotþrýstingi) og bilirubín (biliður) (sjá kafla 4.8).

Candidate 6: Í klínískum rannsóknum á meðferð með eltrombólgi hjá fullorðnu blóðþrýsting á meðgengi á ALT (serumalánínamíþerðasýki), AST (serumaspartatamíþerðasýki) og bilirubín (bílurín) (sjá kafla 4.8).

Candidate 7: Í klínískum rannsóknum á blóðvöxt við eilíðlegra blóðblæðislegum blóðræðum með eltrombopag komu til þess að hægt sé að vita að aukning á ALT (alanínamínóþerðasýkingaríð), AST (aspartatamínóþerðasýkingaríð) og bilirubíni (biliðerið) séu á þeim stað (sjá kafla 4.8).

</details>

<details><summary>final_semantic_review #394 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:1385

English: Lynparza is indicated as monotherapy for the maintenance treatment of adult patients with platinum-sensitive relapsed BRCA-mutated (germline and/or somatic) high grade serous epithelial ovarian, fallopian tube, or primary peritoneal cancer who are in response (complete response or partial response) to platinum-based chemotherapy.

Reference (shown after audit): Lynparza er ætlað til einlyfjaviðhaldsmeðferðar hjá fullorðnum sjúklingum eftir bakslag platínunæms þekjufrumukrabbameins með stökkbreytt BRCA (kímlínu og/eða líkamsfrumu) með miklum vefjabreytingum (HGS [high grade serous]) í eggjastokkum, eggjaleiðara eða lífhimnu (frumkrabbamein) sem svara (algjör svörun eða svörun að hluta til) krabbameinslyfjameðferð sem byggist á platínu.

Review: All corrupt cancer subtype/mutation/platinum-sensitivity/relapse/response indication.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Lynparza er ætlað sem eineigandi meðferð til að halda áfram meðferð hjá fullorðnum sjúklingum með víkjaþrýsting á BRCA-hafni (gerðasæi og/eða eftirgengusæi) með hagvirkum víku föt, æð, katvisspá eða eðlisvöxtmáli sem hafa orðið í svæði (breyttur eða hlutvöxtur) avísanlegri platinabasisamtök.

Candidate 1: Lynparza er ætlað sem einhvers kyns stjórnunarráð fyrir starfshópsþjónustuna hjá fullorðnum sjúklingum með platinatengðu ofnæmisjúkdóm með bretna eða/hvað eða móðraður (gerð og/samskipti) og sérhæfðum (gerð og/samskipti) óþjónusturemslun (fullnægjandi eða hlutnægjandi) af platinabasiska meðferð.

Candidate 2: Lynparza er ætlað sem einhverjarlið efnaleggjandi meðferð hjá fullorðnum sjúklingum sem líða á brúnvera gerð slíkrannsókna brjóstahvöru (gerðarhluta og/sam/harf í efnasvein) og eiga einkennum á brúnvera gerð slíkrannsókna brjóstahvöru (gerðarhluta og/sam/húfn á efnasveinu) hjá þeim sem eru í svona tilgangi að tækja (fullt svona eða hlutað svona) platinum.

Candidate 3: Lynparza er ætlað eins og einhverjar meðferð með platiníumferð fyrir varúðar meðferð hjá fullorðnum sjúklingum með platiníumþægðan hita af BRCA-móðuglingum (eða/eða lífslinnum) betri breytingar í platónaðlæri (óþrýstingur) í alvöruæf og/óþrýstingur í lífslinnum.

Candidate 4: Lynparza er ætlað sem einhjóna meðferð til haldið meðferð með platinum fyrir fullorðna sjúklinga með platinúthreinsunarsjúkdóma sem er meðferð með platinasamhengd áfæra platinurof eins og platinuréttar eða platinusamhengdar (gerðstætt og/eða sjálfræn). Þau eru í svar (fullsvari eða hlutverkar svari) á platinabasisamhengdu meðferð.

Candidate 5: Lynparza er ætlað með einum lyfjagreiðslum til viðbyggja meðferð hjá fullorðnum sjúklingum sem eru áframhaldandi meðferð með platinusensum brúðkaldufræðingjafnarens (hóð og/eða lífurs) auknum (gróðtæmu) sýrar óhópariska, farapalns, eða alvarlega lífurskekkjum í fót, þeir sem hafa reþað (allur eða hlutaþóru) svörun við platinasambönduð meðferð.

Candidate 6: Lynparza er ætlað sem eituráðferð hjá fullorðnum sjúklingum með brúðskiptunarsjúkdóma sem fyrirtekja platinam (platinum-sensitive) BRCA-móðaður (gerð eða eða lífsemið eðlis) (agengja, gerð eða lífsemið eðlis), sem hafa átt ástand (fullur ástand eða hlutaður ástand) á platinam-basið meðferð.

Candidate 7: Lynparza er ætlað sem einhverjar semjurtæku meðferð fyrir viðhalan á meðferð hjá fullorðnum sjúklingum sem eiga brjóstafleik á platinum, sem hafa endurblöndu af brjóstafleik á BRCA-óhlýðina (gerðalýð og/eða eiginlegri) og eiga á móti platinum fundandi rökverkanleika (jafnfrام fullur eða hluta rökverkanleika) við platinbasið meðferð með rökverkamaskinum.

</details>

<details><summary>final_semantic_review #395 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:ema:978

English: Similarly, the geometric mean AUC (CV%) values at Cycle 6 were higher among the subcutaneous group than the intravenous group; 4088 μg day/mL (34.2) versus 3630 μg day/mL (32.8) respectively) with a resulting adjusted geometric mean ratio [90% CI] of 1.10 [0.98-1.24].

Reference (shown after audit): Sömuleiðis var margfeldismeðaltal AUC (flatarmál undir þéttniferli) (fráviksstuðull) í meðferðarlotu 6 hærra hjá hópnum sem fékk MabThera undir húð en hjá hópnum sem fékk MabThera í æð; 4.088 μg dag/ml (34,2) borið saman við 3.630 μg dag/ml (32,8) respectively og leiðrétt hlutfall margfeldismeðaltala [90% öryggismörk] var því 1,10 [0,98-1,24].

Review: Geometric means, administration groups and adjusted ratio corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Svona varð með líkamanlegri, lítila geimihlutaðum AUC (CV%) verðum á 6. cirklum, sem í skertum (skammta) hjá skammtaðri (intra)hlutinu voru háar en í hjá inntökuhlutinu; 4088 μg/dag/ml (34,2) samanborið við 3630 μg/dag/ml (32,8) í samræmi við þannig að viðmiðunarmörk [90% CI] á geimihlutaðum hlutaðum AUC (CV%) var 1,10 [0,98-1,24].

</details>

<details><summary>final_semantic_review #396 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:2090

English: Member States shall require the competent authorities to monitor compliance with this Regulation effectively and take all necessary measures to ensure such compliance.

Reference (shown after audit): Aðildarríki skulu skylda lögbær yfirvöld til að hafa eftirlit með því að farið sé með virkum hætti eftir þessari reglugerð og gera allar nauðsynlegar ráðstafanir til að tryggja að farið sé að ákvæðum hennar.

Review: No full effective compliance-monitoring obligation;3 says stop monitoring.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Aðildarlög fari að segja lögbærum yfirvöldum að veita eftirlit með því að reglugerð þessarar til staðfestri og að gera allar nauðsynlegar ráðstafanir til að tryggja að slíkt sé framkvæmt.

Candidate 1: Aðildarríkin skulu krefjast þess að lögbær yfirvöld stuðli að stöðu þess að viðkomandi reglugerð sé gert í réttu mæli og eru þeir efni sem nauðsynlegar eru til við því að tryggja þá stöðun.

Candidate 2: Aðildarríkin skulu krefjast að lögbærum yfirvöldum sé framkvæmt að því er varðar að viðkomandi stjórnsýslur skilið saman um að reglugerð þessari sé gjarnþekkt og gera allar nauðsynlegar ráðstafanir til að tryggja að þessi reglugerð sé gjarnþekkð.

Candidate 3: Aðildarríkin skulu kveða fram lögbærum yfirvöldum að stöðva athugun við framkvæmd þessarar reglugerðar og undirbúa alla nauðsynlegar ráðstafanir til að tryggja að slíkt séu þeim.

Candidate 4: Aðildarríkin skulu krefjast sástu að lögbæru yfirvöldum er að halda áfram ef viðtekinn ákvæði er uppfyllt og þær skal taka allar nauðsynlegar ráðstafanir til að tryggja þann tilgang.

Candidate 5: Aðildarríkin skulu krefjast af lögbært yfirvöldum að eðlilegri hætti fylgi viðskiptavirkni þessarar reglugerðar og leggja allar nauðsynlegar ráðstafanir til að tryggja þá.

Candidate 6: Aðildarríkin skulu krefjast frá lögbærum yfirvöldum að efna tækifæri til að fylgjast með þeim að því tilnefndri að þessum reglugerðinni ákvarðist að haldið og gerðu allar nauðsynlegar ráðstafanir til að tryggja að þessari aðgerð niðurstöðvist.

Candidate 7: Aðildarríkin skulu krefjast frá lögbærum yfirvöldum að mæta þessu reglugerð í raun og skila sökulegum ráðstafanum til að tryggja þann samræmi sem hugta verður.

</details>

<details><summary>final_semantic_review #397 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:eso:710

English: The VST KiDS survey will allow astronomers to make precise measurements of dark matter, the structure of galaxy halos, and the evolution of galaxies and clusters.

Reference (shown after audit): Kortlagningin nefnist VST KIDS og gerir stjörnufræðingum kleift að mæla nákvæmlega staðsetningu hulduefnis, uppbyggingu vetrarbrautahjúpa og þróun vetrarbrauta og þyrpinga.

Review: Astronomers/dark matter/galaxy evolution not correctly preserved.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: VST-kiðsgræðisvörunin getur leitt íbúgðum að mæla nákvæmlega þakmáttarfljóti, struktur hálósins í galaxum og aðferðir galaxa og klústra.

</details>

<details><summary>final_semantic_review #398 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:1152

English: Change from baseline in body weight was similar for patients treated with sitagliptin relative to placebo.

Reference (shown after audit): Breytingar á þyngd frá grunnlínu voru svipaðar fyrir sjúklinga sem meðhöndlaðir voru með sitagliptíni miðað við þá sem fengu lyfleysu.

Review: No correct body-weight change-from-baseline comparison;1 changes relative-to-placebo to through-placebo and6 repeats/truncates.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Það var sama hvort sjúklingar með sitagliptin ræktu á váði, sem var breytt frá undirborðsetningu, og hvort sjúklingar með placebo ræktu á váði, sem var breytt af undirborðsetningu.

Candidate 1: Breyting á líkamsþyngd frá grundvallarstaðri var sömu hjá sjúklingum sem voru meðnotuð með sitagliptinu í gegnum lyfleysu og lyfleysuó.

Candidate 2: Áhrif skýrsluþægðar á líkamsþyngd hjá sjúklingum sem fengu sitagliptini samanburður var við óléttarlyf.

Candidate 3: Miðað við ástand heildarþyngdar breytti með sitaglitíni sem setla lið er sá sama og með setla.

Candidate 4: Breyting á líkamarga hjá sjúklingum, sem fengu sitaglitin, var jafn sem viðhaldssýni.

Candidate 5: Markmið bótshæðin sést líklegt hjá sjúklingum sem fengu sitaglitín samanburðar við lyfleysu.

Candidate 6 [TRUNCATED]: Þótt viðtakandi væri svipuð við sitagliptini í þrosku við þugafolk og lyfjagöng með lyfjagreiningu í þrosku við lyfjagöng með lyfjagreiningu og lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjagreiningu með lyfjag

Candidate 7: Miðað við váðann var breytingu frá væntu efnahagsskilum hættu beint sama hjá sjúklingum sem fengu sitagliptini í samanburð með lyfleysum.

</details>

<details><summary>final_semantic_review #399 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:1069

English: By using the SPHERE instrument on ESOs Very Large Telescope (VLT) - one of the most powerful planet-hunting instruments in existence - the international team has made the first robust detection of a young planet, named PDS 70b, cleaving a path through the planet-forming material surrounding the young star.

Reference (shown after audit): Með SPHERE mælitækinu á Very Large Telescope (VLT) ESO - sem er eitt öflugasta reikistjörnuleitartæki heims - sáu stjörnufræðingarnir hvernig reikistjarnan unga, PDS 70b, plægir sig í gegnum efnisskífuna sem umlykur stjörnuna.

Review: All corrupt powerful SPHERE/VLT detection or clearing path in planet-forming material.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Með því að nota SPHERE-geimtalan á mjög lítilum leitum af ESO - mjög kröfulegu leiðréttingaríðinni hjá planetum - hefur alþjóðanna komið fram fyrsta rauðlega kveðjanlegu greinin á ungri plöntu, sem heitir PDS 70b, í fljótið um plöntuefnið sem snýr um unginn stjörnu.

Candidate 1: Með því að nota SPHERE miðlun á ESO-Veltískipti, mjög stórra jörðumíðlunarkerfi í tilviki, hefur alþjóðlegur hópinn fengið fyrsta raunverulega ákvarðanir á yngri plöntu, sem heitir PDS 70b, og hafið skilir leið í plöntunafnerið sem umræðist við plöntufólkið við yngri stjórna.

Candidate 2: Með því að nota SPHERE ít frá ESO-veitendur VLT (Very Large Telescope - mjög kröfulegur planetaréttarvörpu) hefur rannsóknarfélagin áframstækja fyrstu raunverulegri greiningu á frumsigri planeti, sem er nýð, sem heitir PDS 70b, sem hlaupur um leið um þau efni sem flauta um frumsigri starfið.

Candidate 3: Með því að nota SPHERE-héfið á ESO-Virtleiti „Mjög stóra spötuleika“ hafa alþjóðinir fengið fyrstu aðstæður við fundi um ungri planeta sem heyrir námi PDS 70b, sem reynir í gegnum geimferlið um stórjarðinn.

Candidate 4: Með því að nota SPHERE-kaflann á ESO VLT-þyrlinum eiga alþjóðlegri meðferðinistjórnin í fyrsta lagi að koma í ljós mikilvægt sjálfstæður úr yngstu planeti sem telst PDS 70b og hafa ógjófsaðila meðhöndluð í vegri um nógu mikið um fljótandi sturtuna.

Candidate 5: Með því að nota SPHERE-þéttkýrslustöðvinnuna á ESO-þéttKEYTílausvöldnum (VLT) hefur þeir sameiginlega fundið fyrsta verulegt viðkomandi á unga planeti sem heitir PDS 70b og hafa lokuð á leið í vegum um upprunalegar feysleika um neytunarstöðina.

Candidate 6: Með því að nota SPHERE einnnar þeirra sem eruðferðarskýrslustofnunin VLT (Very Large Telescope) hefur unnt að nefna fyrsta rétta fundið á ungri planeti sem kallast PDS 70b, sem krefst um fljóttum leið fljótt að þegar stórkosnir í stöðva flokka um ströndin.

Candidate 7: Með því að nota SPHERE útreikninga á ESO VLT (Very Large Telescope) hefur allsambönd flestra stórkostaðanna haft fyrsta, stórnartæki hittesting á ríkur planeti, heitið PDS 70b, sem athafnað er að reyna að hreinsa yfir jafnt á umgöngu plöntunnar og storkunnar.

</details>

<details><summary>final_semantic_review #400 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:1100

English: The combination of images taken by three exceptional telescopes, the ESO Very Large Telescope on Cerro Paranal , the MPG/ESO 2.2-metre telescope at ESOs La Silla observatory and the NASA/ESA Hubble Space Telescope, has allowed the stunning Jewel Box star cluster to be seen in a whole new light.

Reference (shown after audit): Myndir teknar með þremur sjónaukum, Very Large Telescope ESO á Cerro Paranal, 2,2 metra MPG/ESO sjónaukanum í La Silla stjörnustöðinni og Hubble geimsjónauka NASA og ESA, sýna hina glæsilegu lausþyrpingu Skartgripaskrínið í glænýju ljósi.

Review: All corrupt telescope/site/cluster identity or complete image-combination relation;2/6 repeat and truncate.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Samsetningu myndanna sem eru tekin með þremur afmýra hvítrunum, ESO Very Large Telescope á Cerro Paranal, MPG/ESO 2,2 metrú hvítrun á La Silla-kerfinu, og NASA/ESA Hubble sviði er greitt til að geta fengið göngulega sýningu á starfshafið í ljósi fjölskylduja.

Candidate 1: Samsett hagsmýtin úr þris óvenjulega þrýstugjaldvélum, ESO Veltmætabúin á Cerro Paranal, MPG/ESO-2.2 meteru búinu í La Silla-þjónustunni ESO og Húsbúin frá NASA/ESA, hefur getið séð stóruna á Jewel Box starskipi í nýju ljósi.

Candidate 2 [TRUNCATED]: Samsetningu myndanna sem eru tveggja þrjátíu miklu vígissvæði birtar ESO Viðmiðtakaþjónustu í Cerro Paranal, MPG/ESO 2,2m tvöþurrtað hlutastodmál við La Silla efnahagsraðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðvaðstöðva

Candidate 3: Samsetningu myndanna sem eru talað af þrjú afmælisöngum, ESO Very Large Telescope appaðað á Paranal, MPG/ESO 2,2-metrein öngið á La Silla sjótskiptastofnunarstöðinni og NASA/ESA Hubble-samferðaröngu, hefur leitt fyrir beinum að kjörlum í ljós, þakklæði á sérstakt.

Candidate 4: Samsetning þessara tríðja mörkgræðslustefnana, ESO Very Large Telescope, efnisefnisfrum Helvísmörkstaðarinnar, 2,2 métra af Mískir, SWC-stefnana og NASA/ESA Hubble Space Telescope, hefur ákveðið að gera skotatíðindhulsklöpuðælinu í nýjan ljósi.

Candidate 5: Samræmingu myndna sem eru taldar með þrjú sérstökum himnsleikamálum, ESO-Vammasfótastolið á Cerro Paranal, MPG/ESO 2.2 mórtaslitið á La Silla-ferðastjórnunni ESOs og miðlitið NASA/ESA Hubble úr lofti, er möguleiki til að sjá hana í nýju ljósi.

Candidate 6 [TRUNCATED]: Samsetningu myndanna sem eru myndar af þremur sérstökum stællum, ESO sáttin mikla í Cerro Paranal, MPG/ESO stællinn 2,2 meter í la silla efnahagsþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjónustaþjón

Candidate 7: Samsetningu myndanna sem áttuð voru með þremur ofdóma útgeðslufotvélum, ESO Very Large Telescopes on Cerro Paranal, MPG/ESO 2.2-meter telescope at ESOs La Silla observatory and NASA/ESA Hubble Space Telescope, hefur leitt til að sjá skildan kjarnablöndunina í nýju heitu.

</details>

<details><summary>final_semantic_review #401 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:611

English: “With Mars losing that much water, the planet was very likely wet for a longer period of time than previously thought, suggesting the planet might have been habitable for longer,” said Michael Mumma, a senior scientist at Goddard and the second author on the paper.

Reference (shown after audit): „Þar sem Mars hefur glatað svo miklu vatni var reikistjarnan líklega blaut í lengri tíma en áður var talið, sem bendir til að Mars gæti hafa verið lífvænleg í lengri tíma,“ sagði Michael Mumma, vísindamaður við Goddard og annar höfundur greinarinnar.

Review: Habitable-duration inference and scientist role corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: „Með því að Mars væri að missa svona miklum vatni var planeturinn líklega vatnið lengra tíma en fyrr áður varðar og mælti fyrir um að hann væri íkomið lengra tíma,” sagði Michael Mumma, stórsjálfboðarfræðingur á Goddard og annar skráningaraðilinn á þessari grein.

</details>

<details><summary>final_semantic_review #402 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:ema:2124

English: If in doubt, talk to your doctor or pharmacist.

Reference (shown after audit): Ef þú ert í vafa, skaltu leita ráða hjá lækninum eða lyfjafræðingi.

Review: In doubt becomes by accident/unexpectedly.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef þú ert með óvart skal hafa samband við lækninn eða lyfjafræðing.

</details>

<details><summary>final_semantic_review #403 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:1073

English: Analysis of this spectrum indicated that its atmosphere is cloudy.

Reference (shown after audit): Greining á litrófinu sýnir að lofthjúpurinn er skýjaður.

Review: Spectrum/atmosphere/cloudy terminology corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Álysing á þessum fjölda sýni sýndi að loftjafurinn á þessu er klúddur.

</details>

<details><summary>final_semantic_review #404 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:1354

English: Testing at low dosages may be performed by use of OECD 308 (August 2000) or an equivalent method.

Reference (shown after audit): Ef prófanir eru gerðar með litlum skömmtum má nota OECD 308 (frá ágúst 2000) eða jafngilda aðferð.

Review: No full low-dose OECD308August2000-or-equivalent instruction; months change or low-dose scope omitted.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Verkunarprófunar sem er útbúað með notkun lágnaðrar skammta er hægt að gera samkvæmt OECD 308 (oktur 2000) eða viðeigandi aðferð.

Candidate 1: Í tækforðunum má nota OECD 308 (centrifum 2000), svo sem við á, eða ökutæknarhérilag.

Candidate 2: Prufna má við lítillar skammta með því að nota OECD 308 (október 2000) eða fjármögnun með sjálfu sér.

Candidate 3: Í þeim tilvikum sem eru aðgerðir með minni skammti má nota OECD-308 (júlí 2000) eða samsvarandi aðferð.

Candidate 4: Mælingar með lágri skammta eru gerðar með því að nota 308 frá Norðurlögnum (August 2000) eða eiginlíkri aðferð.

Candidate 5: Mælitæki má fara fram við minnkun skammta með því að nota OECD 308 (August 2000) eða jafngildið meðtænlegan aðferð.

Candidate 6: Tilraun má gera með notkun OECD 308 (ag. 2000. ár) eða sömu raunverulegan aðferð.

Candidate 7: Í efnisgreiningu má nota OECD 308 (August 2000) eða samsvarandi aðferða.

</details>

<details><summary>final_semantic_review #405 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:ema:2944

English: Chemical, physical and microbiological in-use stability has been demonstrated for 28 days at 2-8°C. Once opened, the product may be stored for a maximum of 28 days at 2°C to 8°C. Other in-use storage times and conditions are the responsibility of the user.

Reference (shown after audit): Sýnt hefur verið fram á efnafræðilegan, eðlisfræðilegan og örverufræðilegan stöðugleika við notkun í 28 daga við 2-8°C. Eftir að penninn hefur verið notaður einu sinni, má nota hann í allt að 28 daga ef hann er geymdur við 2° til 8°C. Notkun og geymsla umfram þennan tíma eða við önnur geymsluskilyrði er á ábyrgð notanda.

Review: All corrupt stability types/user responsibility or storage limits;6 changes2-8C to2-2C.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Lyfjafærileik, efniþætti og elektrískar efnisþættir hafa verið sýndar í 28 dag áframhaldandi vegi við notkun á 2-8°C. Ef lyfið er opinrætt má gæta lyfsins eftir að mættu liðum 28 daga áframhaldandi vegi við 2°C til 8°C. Önnur geymsluþol og geymsluþolstímu fyrir notendann eru ábyrgð.

Candidate 1: Réttindi til dæmis í líffæri og líffæraætlun hefur verið sannað fyrir 28 dag á 2-8°C. Ef lyfið er hringjast á má lagða í drykk þess gildi 28 dag á 2°C til 8°C. Íðnaðarreglur fyrir önnur notkunarstundir og stöðuhald er einstaklingsábyrgður.

Candidate 2: Lyfjastærð var útskýrt með tilraunum fyrir 28 daga fyrir notkun þar sem lífstað er 2-8°C. Ef lyf er opnað er ekki hægt að geyma lyfið lengra en 28 daga þar sem lífstað er 2-8°C. Önnur geymsluðir og geymsluþykki fyrir notkun eru að öryggisástandi verkefndarinnar.

Candidate 3: Leggjast hefur verið í ljós að efnaleifar, efni og lífveruflæði í notkun hefur verið við staðfest að 2-8°C í 28 daga. Eftir prutun má leggja vörunni í geymslu lengur en 28 daga við 2°C - 8°C. Arðar notkunarskilgildi og skilyrði fyrir innflutningi er ábyrgð notendurs.

Candidate 4: Hafna á eituríkinu er lýst sem líklega stöðug á 28 dögum, hverju í 2-8°C. Þegar lyfið er opnað er hægt að geyma það í hámarksmiðanum 28 daga, frá 2°C til 8°C. Hinmælt er að einstaklingarinnar ber að ábyrgð um eitthvað annað er varðandi geymingardagsetningu og skilræddi fyrir eitthvað annað.

Candidate 5: Lyfjaflagnastjórnin hefur sýnt fram á 28 daga áframhaldandi styrkstaðar og lífleyfi með 2-8°C þegar lyfið er notað. Stöðuhaldi afurðarinnar, eftir að hún er opnað, er hægt að geyma á hámarki 28 daga við 2°C til 8°C. Heimildir hversu lengi þannig er að gera upphafanum áframhaldandi styrkstaðar og stöðu hefur öryggislyfjastofnanefndin ábyrgð.

Candidate 6: Efmiðni, efnisleg stöðugleiki og lífmeðferðarstöðugleiki, sem verður í viðnotun 28 daga á 2-8°C, hefur verið sýnt. Ef lyfið er opnað hefur haft eftirfarandi staðall fyrir að geyma lyfið í hámarki 28 daga á 2°C-2°C. Lífvernda eftirnotunarstundir og skilyrði eru ábyrgð viðeigandi notendurs.

Candidate 7: Veit er fram liggður um 28 daga staðalstöðu í notkun í 2-8°C varmanverð. Ef lyfið er opnað er fyrir leyti hægt að geyma lyfið í hámarki 28 daga í 2°C til 8°C í innihaldi. Aðrar geymsluþolstíðar og geymsluþolstefni sem notaðar eru eru ábylgjur notanda.

</details>

<details><summary>final_semantic_review #406 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:ema:772

English: These effects are called interactions, and can lead to serious side effects, or prevent proper control of other conditions you may have.

Reference (shown after audit): Þessi áhrif eru kölluð milliverkanir og geta valdið alvarlegum aukaverkunum, eða komið í veg fyrir viðeigandi meðferð annarra sjúkdóma hjá þér.

Review: Interactions becomes comparability and control of other conditions is corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þessi áhrif kallaðar eru sambærileikur og geta leitt til alvarlegra aukaverkana eða til að hindra að viðkomandi aðstæður séu stöðugt stjórnar.

</details>

<details><summary>final_semantic_review #407 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:1524

English: In the case of bulk liquid products the lot or sublot shall be thoroughly mixed in so far as possible and in so far it does not affect the quality of the product, by either manual or mechanical means immediately prior to sampling.

Reference (shown after audit): Þegar um er að ræða fljótandi farm í lausu máli skal blanda framleiðslueininguna eða framleiðsluhlutann eins vandlega og unnt er, annaðhvort handvirkt eða vélvirkt, rétt áður en sýni er tekið.

Review: No complete bulk-liquid thorough mixing/manual-or-mechanical/immediate sampling instruction.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Ef um er að ræða löngum fljótandi afurðum skal kominn eða undirkominn lausn í fullnægjandi mörk fyrir svæðið og þar sem það ekki hefur áhrif á gæði afurðarinnar, annaðhvort með einkennuöryggiseftirliti eða eðlilegu verkefni.

Candidate 1: Í þeim tilvikum þegar um er að ræða fljótandi lyfja skal efnis eða ms. blöndu þessu í því tilviki sem er möguleg og þó ekki hafa áhrif á gæði lyfjans, með því að nota notkun í eða starfsemi fyrst og fremur á mótiðu.

Candidate 2: Ef er varan um blöðleg, fljótandi afurðir að koma í huga skal til að hilja eða skipta örlíftén eða skipta hluta í þann hátt sem er hægt og ég ekki í lífi afurðarinnar vegna þess að þessi er afurðin sem stendur við myndun, í öðru lagi án eða með öðrum aðferðum, að því er varðar kynningu þess.

Candidate 3: Ef um er að ræða fullsölulaufna varða skal þann hluta sem fluttur er eða hluti þessi þannig að á fót að hreinsa og þar sem það er ekki ávaxnt að þannig að koma í veg fyrir að hafa áhrif á gæðu laufnar, með því að nota eða aðrar stjórnvelli, beint fyrir aftur fyrir sýnir.

Candidate 4: Fyrir hálfbætta lyfjafurðir skulu hóp eða undirhóp slíku einnig þynnt blönduð sem hér segir, þar sem undirbúin að því er varðar gæði lyfjans, með eða án lána, áður en aðsvísun er hægt.

Candidate 5: Ef um er að ræða hlaðar lausnifyrri verður ætt að blanda þá fyrirkomulaga eða samsamsjálfstæði í til hvers konar þéttna sem er til tilraunar, svo lögbært. En þá skiptir ekki þáttur á þáttarvarpinu. Það er hægt að gera þetta með aðeins einhvers konar aðgerða, annarri í tengslum við eða með verkfræðilega tilraunina.

Candidate 6: Ef um er að ræða fljótandi eldfræki skal þeirri áskirin eða undiráskirin, svo langt sem til er, blandaðar í fullu tilgangi og þó skýri ekki um gæði eldfræksins, með annað eða einum aðeins með tíðskilningi eða við myntun.

Candidate 7: Einmitt skal blöðri eldli afurða flokka eða hlutaflókasins samsetja þannig að lengst er hægt og það hafi enga áhrif á gæði afurðar með annað en að stöðum eða vélbúum áður en sýnir eru.

</details>

<details><summary>final_semantic_review #408 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:1751

English: On the basis of the common criteria, and in view of the fact that, to date, ICAO has not agreed to the closure of any of the findings raised during its audits, it is assessed that, at present, the competent authorities of Indonesia have failed to demonstrate that they have performed their regulatory and oversight responsibilities in compliance with ICAO standards with respect to all the carriers they certify.

Reference (shown after audit): Á grundvelli sameiginlegu viðmiðananna og í ljósi þess að enn sem komið er hefur Alþjóðaflugmálastofnunin ekki samþykkt lyktir neinna þeirra mála sem komu í ljós við úttektir hennar er það metið svo að eins og sakir standa hafi lögbær yfirvöld í Indónesíu ekki getað sýnt fram á að þau hafi gætt ábyrgðar sinnar á sviði reglusetningar og eftirlits í samræmi við staðla Alþjóðaflugmálastofnunarinnar með tilliti til allra flugrekenda sem þau votta.

Review: All corrupt audit-finding closure, common criteria, regulatory/oversight duties or certified-carrier scope.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Í grundvelli samanburðarreglana og af því að í dag hef ekki ICAO samþykkt að loka öllum ráðfundum sínum, er meta að gildandi yfirvöld í Indónesía hafi ekki sýnt fram á að þeir hafi farið á vegum regluefna og skýringaraðila í samræmi við ICAO-tryggt fyrir allar flutningarnar sem þeir trygga.

Candidate 1: Heimilt er að framkvæmdastjórnin á grundvelli samkvæmdar skilmála sem eru viðkomandi í þeim eftirlitsráðningum sem ICAO hefur ekki samþykkt að loka ekkert af dáann ígræddum ákvarnum og að hafa komið í ljós að í dag hafa lögbær yfirvöld Índóleslands ekki sýnt út að þær hafi haldið frásýslu og eftirlit með reglugerðum og eftirliti sínum í samræmi við ICAO-reglur um öll flugrekendur sem þær veltu.

Candidate 2: Að því er varðar samkvæmt sameiginlegu kerfinu og með tilliti til þess að áður hafi ICAO ekki samþykkt að loka yfirtekna ákvarðana hafi í stað haldist að, í dag, hafi lögbær yfirvöld Indónesíu misfyllt aðstoðar þeim að sanna að þeir hafi verið að reglum og eftirliti sínum í samræmi við staðlin ICAO með viðkomandi flutninga.

Candidate 3: Sá sem í staðverum er í samræmi við samkvæmtáknir, í skyni þess að þau hafa ekki samþykkt tilkynning um nýtingu að því er varðar þær nauðsynlegar niðurstöður sem komu fram í eftirgreiningum, er metið að í dag hafi lögbær yfirvöld í Indónesíu ekki fengið mögulegt sýni um að hafi getið greiði sína á reglunum og eftirliti sínu í samræmi við staðla ICAO, að því er varðar allar flutningarnar sem þeir veita.

Candidate 4: Basið á samkvæmtum þeirra og með því að í tilgangi að taka tillit til endurtekna yfirvöldanna í Indónesíu er það skoðað að þau hafi ekki upplýst að þeir hafi gert reglulega og eftirlitsskapinn efni í samræmi við lofttæki Íslands.

Candidate 5: Hafðar verðið á grundvelli samanburðarreglur og í lagi fyrir þann að, eftir því er komið að tæki, hafi ICAO ekki samþykkt að loka upp ákvarðanir sem í augnablikum var gerð í gagnaögurðarmálum og er reiknuð til að í dag hafi lögbær yfirvöld í Indónesíu fundið ekki fram á að hafi framhaldsþáttin sína, reglusetningu og stjórnsýslu, sem er í samræmi við ICAO-reglur, sem um segir fyrir öllum flutninga sem þau tilskildu.

Candidate 6: Á grundvelli sameiginlegra ákvæða og með tilliti til þess að í dag hafa ekki ICAO samþykkt lokað einhverja uppgötvana sem fengist með rannsóknirnar, er sett fram að ríkjandi yfirvöld í Indónesíu hafi ekki fengið sannprófun á því að þeir hafi gert reglulega aðgengisvinnslu og hafa náð kveðju og eftirlit í samræmi við ICAO-gerðunum, með tilliti til öllu flutnenda sem þeir sjá til.

Candidate 7: að því er varðar að, á sviði samræmisreglum, og með því að talsvert hefur því ekki verið komið á að ICAO hafi samþykkt að loka ekki ákvarðanirnar sem fengd voru í rekstingunum, er í órúðum að lögbærar yfirvöld í Indónesía hafi farið ekki að sýna fram á að þeir hafi farið að reglunarpilstu og eftirlitsstörfum sínum í samræmi við ICAO-stöðla með tilliti til alla flutninga sem þeir samþykka.

</details>

<details><summary>final_semantic_review #409 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:409

English: Purpose: to determine whether the test facility, if engaged in studies using animals or other biological test systems, has support facilities and conditions for their care, housing and containment, adequate to prevent stress and other problems which could affect the test system and hence the quality of data.

Reference (shown after audit): Markmið: að ákvarða hvort prófunarstöðin, ef þar eru stundaðar rannsóknir með dýr eða önnur líffræðileg prófunarkerfi, hefur yfir að ráða búnaði og aðstöðu þar sem hægt er að hirða um þau, koma þeim fyrir og einangra þau á annan viðeigandi hátt þannig að koma megi í veg fyrir streitu og önnur vandamál sem gætu haft áhrif á prófunarkerfið og þar af leiðandi á gæði gagnanna.

Review: Care/housing/containment and stress-prevention conditions not retained.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Tilvísun: að ákvarða hvort prófunarstöðin, ef hún er í rannsóknum með dýrum eða öðrum líflegum prófunarsystum, hafi viðhaldssvæði og skilyrði fyrir þau, hvort þær séu í stað og í hættu, og hafi fullnægjandi hættu til að koma í veg fyrir áhættu og önnur vandamál sem gætu haft áhrif á prófunarsystan og þar með á gæði gögnanna.

</details>

<details><summary>final_semantic_review #410 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:eso:329

English: The experiment marks the first time that APEX has taken part in VLBI observations, and is the culmination of three years hard work at APEXs high altitude site on the 5000-metre plateau of Chajnantor in the Chilean Andes, where the atmospheric pressure is only about half that at sea level.

Reference (shown after audit): Með tilrauninni er APEX í fyrsta sinn notaður í VLBI mælingum og er hápunkturinn á þriggja ára erfiðisvinnu við APEX sjónaukann sem er í 5.000 metra hæð yfir sjávarmáli á Chajnantor sléttunni í Andesfjöllum Chile, þar sem loftþrýstingur er helmingi minni en við sjávarmál.

Review: VLBI observations becomes requirements; culmination/hard work and site description corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Í þessu rannsókn var APEX fyrsta sinni að taka þátt í VLBI-kröfunum og þetta er endurheimt þrjár ára þjónustu á hávaxandi staðnum APEX á 5000 m. stigi á Chajnantor í Chileiðsandsandum þar sem loftþrýstingið er aðeins hálft af þeim sem á sjóþrýsting.

</details>

<details><summary>final_semantic_review #411 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:ema:2323

English: It is important to drink plenty of water to avoid dehydration.

Reference (shown after audit): Mikilvægt er að drekka mikið af vatni til að koma í veg fyrir ofþornun.

Review: Plenty becomes fine water and dehydration becomes fluid, changing the preventive purpose.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það er mikilvægt að drekka fínt vatn til að forðast vökva.

</details>

<details><summary>final_semantic_review #412 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eso:871

English: A team of astronomers led by Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) first used the ULTRACAM system on ESOs New Technology Telescope to measure these brightness changes very precisely.

Reference (shown after audit): Hópur stjörnufræðinga undir forystu Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) notaði fyrst ULTRACAM mælitækið á New Technology Telescope ESO til að mæla birtubreytingarnar með mikilli nákvæmni.

Review: All corrupt astronomer-team/precision/brightness/instrument relationship;0 repeats and truncates.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0 [TRUNCATED]: StarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStarfsskírtepiStar

Candidate 1: Reikningaraðilar stjórnirir af Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) börðu þegar við ULTRACAM tækin með ESO New Technology Teleskop til að mæla þessa ljósfæringurannum á mjög snertilega.

Candidate 2: Samsetningur umagnverðarframfæra með lestinu af Adam Hardy (ev. Valparaíso, Chile, Valparaíso) byrjaði fyrst að nota ULTRACAM-kerfissamsetninguna á útæggingu efnisfrumanna ESOs New Technology Telescope til að mæla þessa ljósbreytingar út af miklum nýtri mörkum.

Candidate 3: Högþjóðasjálfur, samkvæmt Leiðbeiningum frá Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) fannst sér að einungis með ULTRACAM-sætinu í Nefndastjórnin ESO-STAR-geislavediðar færið mælið áþökkunaraukinn þeirra mjög lítilt.

Candidate 4: Reyindjökona með framkvæmdastjórninni áfram í Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) nýttu algjörum mælingarmörkum saman á kunnuginnúðarsjóð ESO's til að mæla þessum miklar sárlega breytingum.

Candidate 5: Fyrsta notkun ULTRACAM-kerfisins á ESO-ni, Nefndarveitislettarinnu, var spearlað af heimsókn haldaðar af Adam Hardy (Universidad Valparaíso, Valparaíso, Chile).

Candidate 6: Samtök jeðsluefna, sem stjórnast af Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) birtist fyrst með ULTRACAM kerfisvísindaviðferðinni á ESO-ni „New Technology Telescope“ til mælinga þessara ljóslagafanarefna.

Candidate 7: Samstarfsskapur starstræðenda, sem leiddi afadam Hardy (Universidad Valparaíso, Valparaíso, Chile), nýtti fljótsmyndunarhlutliðina ESOs New Technology Telescope fyrst til mælingar á þessum ljóshreinsunum með mjög kynnulegri niðurstöðu.

</details>

<details><summary>final_semantic_review #413 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:850

English: When implementing this strand the Commission will in particular ensure consistency and complementarity with the activities conducted by other Commission services or by European agencies; in particular, the European Foundation for the Improvement of Living and Working Conditions and the Community RTD Framework programme and the European Centre for the Development of Vocational Training (Cedefop).

Reference (shown after audit): Við framkvæmd aðgerða í þessum flokki mun framkvæmdastjórnin sérstaklega sjá til þess að þær séu í samræmi við og komi til fyllingar starfsemi sem aðrar þjónustugreinar framkvæmdastjórnarinnar eða evrópskar stofnanir stýra, einkum Evrópustofnun um bætt lífskjör og starfsskilyrði, rammaáætlunbandalagsins um rannsóknir og tækniþróun og Evrópumiðstöð um þróun starfsmenntunar (CEDEFOP).

Review: Complementarity and named organisations/programmes corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Þegar framkvæmdastjórnin framkvæmdir þessa ströndar skal einkum tryggja samræmi og samræmi við starfsemi annarra þeirra þjónustu framkvæmdastjórnarinnar eða evrópsku stofnunanna, einkum Evrópuþjónusta fyrir aðlaga lífsháttar og starfshættir og ráðstöfunaráætlun Evrópusambandsins um framkvæmdaráætlun fyrir starfsþjónustu (RTD) og Evrópuþjónusta fyrir þjónustu fyrir þjónustu fyrir starfsþjónustu (Cedefop).

</details>

<details><summary>final_semantic_review #414 · old08 · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:2128

English: Don't you worry about those dope smokers and nudists down below there?

Reference (shown after audit): Hefurðu ekki áhyggjur af dóphausunum og striplingunum þarna?

Review: Worry question and nudists/location not retained; nudists becomes another smoking clause.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Viltu ekki að þeir sem reykja dope og reykja náðar séu þangað?

</details>

<details><summary>final_semantic_review #415 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:386

English: Purpose: to inform the management and staff of the facility of the reason for the test facility inspection or study audit that is about to take place, and to identify the facility areas, study(ies) selected for audit, documents and personnel likely to be involved.

Reference (shown after audit): Markmið: að tilkynna stjórn og starfsliði prófunarstöðvarinnar um ástæðuna fyrir því að skoða á prófunarstöðina eða gera úttekt á rannsóknum og nefna þá hluta prófunarstöðvarinnar, rannsókn(ir), skjöl og starfsmenn sem líklegt er að komi við sögu við skoðunina eða úttektina.

Review: No complete forthcoming inspection/audit reason plus selected facility/studies/documents/personnel purpose.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Tilvísun: til að koma áhættu fyrir stjórnførum og starfsfólki með því að greina þá eigin ástæðu um prófunarstöðinni eða eftirlit með henni sem er um rannsóknarvöru að verða, og koma áhættu fyrir starfsmenn sína, að finda þá fyrirtækishól sem verða að eiga sér þátt í eftirliti, eftirlitsrannsóknir, skráningar og starfsmenn sínum.

Candidate 1: Tilvísun: til að kanna ástæðurnar fyrir prófunarstöðvar í fjölskyldunum og kalla á að reyna með uppáhaldsri að þeim ástæðum og kalla á að koma fram heimsundir og upplýsingar sem koma inn í umboð og staðfestu, með því að stöðvun leggjast á, sem um er að ræða, og greina um starfsmenn sem geta haft meðhöndlu.

Candidate 2: Tilvísun: til að kanna af hverju á textaætlun fyrir staðvæðið kemur til eftirfarandi eftirlits: að upplýsa starfsmenn og stjórnmálana af hverju eftirlitið og eftirlitið um textaætlunina kemur til fyrir sem stendur og að teljast við á tímanum, eftirlitið, eftirlitið um textaætlunina sem stendur til eftirfarandi markaði: upplýsinga og starfsmenn sem hverju á staðvæðið kemur til eftirfarandi: eftirlitsrannsóknir, upplýsingar og starfsmenn sem hafa mögulega haft skuldbinding á staðvæðið.

Candidate 3: Tilvísun: til að kanna eftirfarandi að því er varðar prófunastofuna: að kynnast stjórnandi og starfsmenn þess sem á að sjúklustofuna, og til að koma fram þau verki, aðgerðir og aðfangabreytingar sem um er að ræða.

Candidate 4: Tilvísun: til að kveða fram ástæðurnar fyrir prófunarstöðvarinnarins prófunar eða rannsókna, sem í vökvunum er við, og til að gilda um þær staðsetningar, rannsókna (eina), sem völdu rannsókna, skírteina og einstaklinga sem þörf krefur.

Candidate 5: Tilvísun: til að kalla á fyrrverandi rannsóknarstöðu og starfsfólki á stöðinni um ástæðu verkefnisstöðvarinnar við rannsókn, eftirkomandi verður að gera, og til að koma í ljós þar sem stöðuhúðverðið er, sem rannsóknaráætlunin upplýsingar um, lögaðilar og starfsfólki sem líklegt er að hefjast.

Candidate 6: Heimild: að veita stjórnvaldi og þjónustuþjónustu að þeim er skýrt af hverju prófunarstöðin getur verið skoðuð eða eftirlit samkvæmt þessu aðgerð verður að fara fram og að koma í veg fyrir að gera eftirlitsrannsókn á reikningarskjal, mál og einungis staðbundið að því að hvaða staðbundnum máttstökum varðar starfsfólki sem munu þurfa að taka þátt í eftirliti.

Candidate 7: Tilvísun: til að kanna og tilkynna stjórnvalda og starfsfólkið vegna rannsókna á verksmiðjunni þar sem veitist eftirlit eða rannsóknarþjónustu fer fram og að kanna verksmiðjunum og aðskildar staðsetningum, rannsóknum og eftirlitsáttirnar og aðgerðir sem líklega eru viðkomandi.

</details>

<details><summary>final_semantic_review #416 · old08 · greedy · general · U</summary>

Source ID: p13official21:test:opensubtitles:3484

English: If you do not give me the house you promised I shall be forced to return to England.

Reference (shown after audit): Ef þú lætur mig ekki fá húsið eins og þú lofaðir neyðist ég til að fara aftur til Englands.

Review: Negated house condition preserved, but skilaEnglandi means returning/handing backEngland rather than clearly returning there; cannot confirm intended motion.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ef þú gefur mér ekki húsinn sem þú lofaðir mér skal ég þurfa að skila Englandi.

</details>

<details><summary>final_semantic_review #417 · old08 · greedy · technical_medium · F</summary>

Source ID: p13official21:test:ema:74

English: ARICLAIM should normally not be used for children and adolescents under 18 years.

Reference (shown after audit): Venjulega ætti ekki að nota ARICLAIM handa börnum og unglingum undir 18 ára aldri.

Review: Normally-not-used recommendation becomes unconditional prohibition; limiting qualifier omitted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: ARICLAIM skal ekki nota fyrir börn og unglinga yngri en 18 ára.

</details>

<details><summary>final_semantic_review #418 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eea:2120

English: In order to facilitate data flows from the European Union, it is desirable for processors providing data-processing services to several data controllers in the European Union to be allowed to apply the same technical and organisational security measures irrespective of the Member State from which the data transfer originates, in particular in those cases where the data importer receives data for further processing from different establishments of the data exporter in the European Union, in which case the law of the designated Member State of establishment should apply.

Reference (shown after audit): Til að auðvelda gagnaflæði frá Evrópusambandinu er æskilegt að vinnsluaðilar, sem veita mörgum ábyrgðaraðilum gagna í Evrópusambandinu gagnavinnsluþjónustu, fái leyfi til að beita sömu tæknilegu og skipulagslegu öryggisráðstöfunum, óháð því frá hvaða aðildarríki gögnin eru flutt, einkum í þeim tilvikum þar sem gagnainnflytjandinn tekur við gögnum til frekari vinnslu frá mismunandi starfsstöðvum útflutningsaðila í Evrópusambandinu, en þá gilda lög þess aðildarríkis þar sem starfsstöðin er staðsett.

Review: All corrupt data-agent roles, origin-independent security measures or establishment-law conditions.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Til að skipta færi um gögn frá Evrópusambandiinni er óhætt að efnahagsmenn sem veita gögnunzið gæti til þriðja gögnabúnaðanna í Evrópusambandiðum lagðar fyrir gildi að samkvæmt þeim tæknilegum og starfsstöðuargjarni tryggjuðum verndarreglum, hvort sem við á, ræsta afurðið frá því að aðildarríkið sem gögnin færa aðferðin á að, einkum þegar um er að ræða, séu gögninleysandi, eigi gögn til frekari vernda frá öðrum fyrirtækjum sem eru í Evrópusambandiðum, þar sem þegar um er að ræða, skuli löggjöf áttanildarríkisins hafa gert.

Candidate 1: Til að þjóna gæðum við upplýsingasmörk frá Evrópusambandinu skal hafa þess hægt að aðila þjónustum fyrir upplýsinga, í nokkrum upplýsingatengnum í Evrópusambandinu, fari að því að búa við sömu tæknilegum og fyrirtækisstöðuáhorfalegum verndarreglum að því er varðar framleiðsluþjónustu þjónustu fyrir upplýsingaskipti, ekki þótt yfirráðastarfurinn sé að tilgreina, einkum þegar innhaldsflutningsmaðurinn veitir innihaldið áfram til að endurspegla áframhaldandi upplýsinga í tilteknum fyrirtækjum í Evrópusambandinu þar sem innhaldsflutningsmaðurinn veitir innihaldið áfram til að endurspegla áframhaldandi upplýsinga í tilteknum fyrirtækjum í Evrópusambandinu þar sem innhaldsflutningsmaðurinn veitir innihaldið áfram til að endurspegla áframhaldandi upplýsinga í tilteknum fyrirtækjum í Evrópusambandinu, þar sem samkvæmt reglum tilgreindra aðildarríkjanna skal beita þeim.

Candidate 2: Þar sem þvert hluti af Evrópskum samningsinu, til að mynda ákvæði um flutningum í gegn, mun óviss að að framleiðendur sem gefa fram áframhaldandi viðtækja, í mörgum aðildarríkjum Evrópusambandsins, séu leyfðir að beita sömu tækniögryðju og starfsstöðu, það eigi ekki að framfylgum, ótt. Jákvæð ráðstöfunaráætlun og ráðstöfunaráætlun, án þess að hafi hagkvæma hagsmuna á viðkomandi aðildarríki, þar sem frávikur tengir aðildarríkið frá þeim viðtökum sem framleiðsögnin færi, þar sem framleiðingurinn færi framleiðsluþekkingu á þeirri sönnun af berandi stöðum í Evrópusambandiinu, þar sem gefur framleiðsluþekkingu á þeim sönnun áframhaldandi viðtaka, í það tilliti hvort á tilteknu aðildarríki, þar sem þegar sameiginlegt rækt er, skal beita lögum á tilteknu aðildarríki.

Candidate 3: Að því er varðar að auka tækifæra fljóti frá Evrópusambandinu er vitundur sem gefa þjálfunarþjónustu til nokkurra tækifæra í Evrópusambandinu heimilt að beita sömu tækni og stöðugleikaþjónustujafnsemi, án þess að móteðli þess sem flutnaðar upplýsingar sjálfu sér sem þáttir í flutningi frá henni, einkum þegar innleiðandi upplýsinga fær upplýsinga fyrir frekari verjaflingu í öðrum starfsstöðum upplýsingareyðanda í Evrópusambandinu þar sem hún er þáttur í upplýsingaskipti í samræmi við tiltekinn fjárfestisland, þ.t.d. þegar innleiðandi upplýsinga fær upplýsingar fyrir frammeldur verjaflingu í öðru starfsstöðu upplýsingareyðanda í Evrópusambandinu, þar sem ákvæði samkvæmt markaðsildandi fjárfestislandi ætti að gilda.

Candidate 4: Til að skaða flutningu gögn úr Evrópusambandinu er mætt að fyrirlestrarleikar sem veita gögnlausnana veitur taldir fyrir fleiri gögnlausnara í Evrópusambandinu gætu beitt sömu tæknilegum og rekstranlegum öryggismálum, án undanþáginnar aðildarríki þar sem gögnflutningin er upphæð, einkum þegar gjöldinn sem upplýsingarnar hafa verið gefin inni til frekari þrýstingum úr öðrum starfsstöðum gafla í Evrópusambandinu, þar sem beið er að þeim reglum sem í tilteknuildistökum ríki ræðir leyfi aðstæðunnar um þrýstingu að hafi gildi.

Candidate 5: Til að stuðla þjónustu við upplýsingarnafn á Evrópu samningnum er óhætt að fleiri upplýsingatengara í Evrópu samningnum fái að ræða að fá samskipulag og tengslaáætlunum um samskipulag gegn öllum skólunum frá þeim aðildarríkjum sem koma á upplýsingunum, einkum þegar innleiðandi upplýsinga innkomin á innhluta til frekari endurspeglunar frá mismunandi fyrirtækjum í Evrópu samningnum þar sem, á því skyni að hafa áhættu á sviði hlýðingafæra, skal eigi stöðullan aðildarríki sem hefur þá eftirlitsstofu sem skal reglulega vera á stöðunni.

Candidate 6: Til að auðvelda greiningum upplýsinga frá Evrópusambandið þarf að því að veita greiningaraðila sem gefa greiningatöku til að viðtöku til nýja tímanna til þeirra plögunara í Evrópusambandið höndluna sömu tæknilegum og fjarskiptalegum varðhaldsmeðferðum, óhólfum aðildarríkinum, einkum þegar innleiðandi upplýsinga, sem gefa inn gruna til frekari greiningar, hafa aðrar fyrirtæki í Evrópusambandið aðgengisgruna til þess að bæta greiningu á sömu fundi, þegar innleiðandi upplýsinga, sem gefa inn gruna til frekari greiningar, hafa aðgengisgruna til þess að bæta greiningu á sömu fundi, þegar innleiðandi upplýsinga, sem gefa inn gruna til frekari greiningar, hafa aðgengisgruna til þess að bæta greiningu á sömu fundi, þegar innleiðandi upplýsinga, sem gefa inn gruna til frekari greiningar, hafa aðgengisgruna til þess að bæta greiningu á sömu fundi.

Candidate 7: Við því til að auðvelda greiningu gögn úr Evrópusambandinu er óvirk til að framleiðendur, sem veita gögnunámiðningarástöðvigur, séu að öðrum aðildarríkjum í Evrópusambandinu leyfi að sama tækniöryggiskerfi og rekstrarstarfsemi, að því er varðar aðildarríki sem gögnþegið kemur frá og um það allra að því er varðar það sem frumstofan aðgerða höfum upplifatöku í frumstofu, þar sem frumstofan umtógur gögn úr í hliðinni sem upplötabúnaðurur í Evrópusambandinu, þar sem skal beita reglum tilkynntu aðildarríkis sem upplötabúnaðurinn býr í.

</details>

<details><summary>final_semantic_review #419 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:1144

English: Successful participation in interlaboratory studies that assess laboratory proficiency is the best way to prove the competence in specific analyses.

Reference (shown after audit): Árangursrík þátttaka í rannsóknum með öðrum rannsóknarstofum, þar sem frammistaða rannsóknarstofa er metin, er vænlegust til þess að staðfesta hæfni í sértækum efnagreiningum.

Review: Successful interlaboratory proficiency participation not preserved in any candidate.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Okkur sem starfsmeðferðir í miðað við eftirlit í rannsóknirum að höfuðstöðva kunnug á prófunarskrafanum er þau störf fyrir bestu lagi til að sanna kunnug á sérstökum greiningum.

Candidate 1: Sjálfsemi starfsamböndu í rannsóknir um prófun á prófinu á gagnsókun í rannsóknum er bestur leiðin til að sanna gæðafærsla að því er varðar sérstök greiningar.

Candidate 2: Stórkun á aðra rannsóknir í þróun á rannsóknarstörfi að skoða læknisfrétt í rannsóknastöðum er hvað besta leiðin er að staðfesta ekki frétthæfi í sérstökum greinfræðslu.

Candidate 3: Þráttarkeppni í þroskunum á þjálfun á prófkröfu ved veitir rökkomulag í þjáldræktum greinsemi.

Candidate 4: Það verður best að sýna réttindi í sérstökum greinunum með þeim hætti að þarf vor á almenntu rannsóknum á þróunarheild aðalborðs til að meta heildarlegri möguleika í sérstökum greinunum.

Candidate 5: Bestan leiðin til sýnis á hæfni í sérstökum greinsemi er að taka þátt í samstarfi sem sett er á samþykktir rannsókna í {frumvísu} og að aðlitinn sé á hæfnið eins og þær aðlit eru sem eru sett á.

Candidate 6: Úhlíkar starfsemi í rannsóknir sem mata á upphaflega þýðingu í prófkrómum er bestur háttur til að sanna þá hagnýta að sér í sérstökum greinunum.

Candidate 7: Aukverðar átak í tækjuraldísprofunum sem meta þjónustu mikils í fólk og kennslu er bestur leiðin að svara fyrir skilvirkni í sérstökum greinsemi.

</details>

<details><summary>final_semantic_review #420 · old08 · greedy · technical_long · F</summary>

Source ID: p13official21:test:eea:1190

English: Indeed, there is a need for technical and scientific support and a high level of stable expertise to properly apply the Community legislation in the fields of maritime safety and ship pollution prevention, to monitor its implementation and to evaluate the effectiveness of the measures in place.

Reference (shown after audit): Raunar er þörf á tækni- og vísindalegri aðstoð og öflugri og yfirgripsmikilli sérfræðiþekkingu til að beita með réttum hætti löggjöf Bandalagsins á sviði siglingaöryggis og varna gegn mengun frá skipum, fylgjast með framkvæmd hennar og meta skilvirkni þeirra ráðstafana sem eru fyrir hendi.

Review: Maritime safety becomes land safety and ship-pollution prevention corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Það er nauðsynlegt að fá tæknilega og vísindalega aðstoð og að hafa hátt á stöðluðu þekkingu til að beita löggjöf Bandalagsins rétt á sviði öryggi á landi og forðunarvöruðstöðvunar, til að fylgjast með framkvæmd þess og meta árangur ráðstafana sem eru í gildi.

</details>

<details><summary>final_semantic_review #421 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:ema:1414

English: Invokana has no or negligible influence on the ability to drive, cycle, and use tools or machines.

Reference (shown after audit): Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, hjólreiða og notkunar tækja eða véla.

Review: No complete drug/no-or-negligible-effect/driving-cycling-tools-machines assertion.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Úfærið hefur engin eða litla áhrif á hæfni til aksturs, vélbíla og notkunar viðökvahenda eða véla.

Candidate 1: Stundvöld hafa engin eða óáhrif á hæfni til aksturs, bilags og notkunar við tækni eða vélar.

Candidate 2: Invokan hefur ekki eða minnkar álag á hæfni til aksturs, vélöskunar og notkunar verkfema eða vélar.

Candidate 3: Bes Joakva hafa engin eða einkum minnkilegan áhrif á hæfni til aksturs og búnaðar, orkunar eða notkun vörna.

Candidate 4: Framkvæmdabundið hefur engin eða minnst hæfileiki á að keyra, kalla og nota vélar eða vél.

Candidate 5: Skráningarnar hafa eða ekki skipti um möguleika á önnun, ökutæki og notkun verkfæra.

Candidate 6: Mögnunina hefur engin eða góðar áhrif á nákvæmni á hæfi til aksturs, kyns, og notkunar verkfjárafna.

Candidate 7: Hefniskerfin yrðir ekki eða er viðkvæm fyrir hæfni til aksturs, ökutækja og notkunar hjálpaþjónustu eða vélna.

</details>

<details><summary>final_semantic_review #422 · old08 · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:839

English: The Caisey Harlingten and ASH2 telescopes.

Reference (shown after audit): Caise Harlingten og ASH2 sjónaukarnir.

Review: No candidate preserves telescope noun despite copied names.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Caisey Harlingten og ASH2 stelpum.

Candidate 1: Caisey Harlingten og ASH2 skáp.

Candidate 2: Tökukjöl Caisey Harlingten og ASH2.

Candidate 3: Caisey Harlingten og ASH2 útseðjur.

Candidate 4: Caisey Harlingten og ASH2 takarstigmur.

Candidate 5: Caisey Harlingten og ASH2 útsetningarnar.

Candidate 6: Caisey Harlingten og ASH2 útsemina.

Candidate 7: Hinsýringar H. Harlingten og ASH2.

</details>

<details><summary>final_semantic_review #423 · old08 · greedy · general · F</summary>

Source ID: p13official21:test:opensubtitles:2621

English: I'm glad you found one another."

Reference (shown after audit): Ég er svo ánægð að þið funduð hvort annað."

Review: Finding one another becomes finding someone else.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Ég er ánægður að þú finnurð einhvern annar."

</details>

<details><summary>final_semantic_review #424 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:eea:1471

English: Prices including all taxes, levies and VAT.

Reference (shown after audit): Verð með öllum sköttum, álögðum gjöldum og VSK.

Review: Levies/VAT corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Verð með öllum skatta, skattaáskipti og verðbúnaði.

</details>

<details><summary>final_semantic_review #425 · old08 · greedy · technical_short · F</summary>

Source ID: p13official21:test:eso:1086

English: Media representatives and other outreach groups will also be attending the event.

Reference (shown after audit): Fjölmiðlar og fræðsluhópar munu einnig sækja atburðinn.

Review: Media representatives becomes notifying persons and outreach/event relation corrupted.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Tilkynningaraðilar og önnur tengslagsbundin stofnanir verða einnig að taka þátt í aðgerðinni.

</details>

<details><summary>final_semantic_review #426 · old08 · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:1878

English: That's not what Optimus would want.

Reference (shown after audit): Optimus hefði ekki viljað það.

Review: Negation and Optimus preference retained; tense/inflection minor.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Það er ekki það sem Optimus vil.

</details>

<details><summary>final_semantic_review #427 · old08 · G8 · technical_medium · F</summary>

Source ID: p13official21:test:eea:79

English: Justified estimates must be made of the expected concentrations of the active substance and relevant metabolites, degradation and reaction products, in soil, groundwater, surface water and air, following use as proposed or already occurring.

Reference (shown after audit): Rökstutt mat verður að koma fram á áætluðum styrk virka efnisins, og viðkomandi umbrots-, niðurbrots- og hvarfaefna, í jarðvegi, grunnvatni, yfirborðsvatni og lofti, eftir núverandi notkun eða ráðgerða notkun.

Review: All corrupt justified expected concentrations, chemical-product categories or environmental compartments.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Umræðingar skal viðurkenna með því að nota vart af lyfið og viðkomandi umbrotsefni, þrýstingsstofna og loftstofna af aðstöðu og meðferð.

Candidate 1: Ákveðið verður er ákveðið hverju áhrifaskammta efnisins og viðeigandi umbrotsefnisins sé átt, auðvelda og verkinu, í landi, dunum jörðar, vefju og lofti, eftir því sem notuð er eftir höndum eða efnis er að vera í notkun.

Candidate 2: Svona skal mæla áhrif lyfs eða lyfahvifa með vilja eða þegar þau ná því, við neyðarmál, þannig að innihaldur lyfs eða lyfahvifa í þeim, eftir notkun, sé þannig aðrúmtæki sem í tilliti er til: efni og leysir sem hafa gert á innihaldsleyfi, vatni í vatnsgeirni og vefi, og efni sem hafa gert á lofti, að því er varðar þau áhrif sem hér segir við.

Candidate 3: Eftirfarandi skal útbreiða á eftirlýsingum fyrir viðunandi þykir sem áætlað er að þykir í vöku og viðkomandi umbrotsefnir, þykir með skipti, efni og innrenndarurðir, í göndum, vafðrum vatni, yfirborðsvatni og lofti, eftir notkun sem rækt er eða er orðin fyrir.

Candidate 4: Eftirfarandi reikningi skal framkvæmd fyrir hyggjanlegar þykirliðir heildarvöðurs og viðeigandi umbrotarefna, þróaðar og svima af afleiðingum aðgerða, í aðskömmtun, í landbúnaði, vefnum í vatni, yfirborði og lofti, eftir notkun eins og tilgreind eða til staðar.

Candidate 5: Kværtar uppskala skal vera á viðeigandi þéttni lyfsins og viðkomandi umbrotsefna í jarðvegi, yfirborðsvatanum og lofti, og aðgar af þrýstingu og viðskiptum, eftir því sem notuð er þetta eða einhverjar eru áfram.

Candidate 6: Athuga skal ætíka þétta virkni efnisins og viðeigandi umbrotasamhengis, aðbyrðingsafurðir og afurðir af rekstraríðum, á landi, í dyrunni, yfirborðið og í lofti, eftir notkun sem tilgreind er eða það er orðið þegar.

Candidate 7: Vísindaleg áætlanir verða að vera á kafla á áætluðum æðisamsetningu virkri efna og viðkomandi umbrotna, efna í þroskinu og efnum af viðbragði, á jarðsvæði, vatni í grundvallarþvöðun, yfirborðsvatni og lofti, eftir notkun, eins og rannsókn hefur verið gerð eða er á vaxi.

</details>

<details><summary>final_semantic_review #428 · old08 · G8 · technical_long · F</summary>

Source ID: p13official21:test:eso:908

English: This bridge, which has not been seen before (and is too faint to show up in this picture), is somewhat bluer than either galaxy, indicating that it consists of stars created in gas that was drawn away from NGC 1387 by the gravitational pull of NGC 1399.

Reference (shown after audit): Þessi brú hafði ekki sést áður (og er of dauf til að koma fram á myndinni) en hún er nokkuð blárri en hin vetrarbrautin sem bendir til þess að hún samanstandi af stjörnum sem mynduðust úr gasi sem NGC 1399 hrifsaði úr NGC 1387.

Review: All corrupt bridge faintness/colour or gravitational stellar-gas origin.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þessi brofið, sem ekki hefur verið horftur á áður (og er of fjarlæg til að sjá upp í þessa mynd) er smágrauður en annar stjórður, sem sýnir að það sé í tengslum við starfsemi í gasi sem var dreifin frá NGC 1387 á grunnkröfur NGC 1399.

Candidate 1: Þessi bjóg, sem hann hefur ekki séð áður (og er of fínt til að sýna upp í þessu mynd) er smágrúinn en annars efnis en jógaskaparinn, sem eigendur staðfestir að það séður stjörnu sem var brennt í gegnumhreinum sem var ígreint eftir námi NGC 1387 og námi NGC 1399.

Candidate 2: Þessi brofur, sem hefur ekki verið horftur á (og er of glat til að sjá upp í þessari mynd), er smágrauð en eitt af þessum gólum og tekin fram vegna þess að það tekur í þeim hreisinu sem stafa á NGC 1399 og 1387 í gegnum tökkstund hreinsa gassins.

Candidate 3: Svæðið sem ekki er sjáðað fyrir (og er-oftar klínka en þann eða önnur heil og er svimað í myndinni) er sumkvæðugt blærr en einhvern heil og dæmir að hann tekist úr heilum sem eru framleidd í loftinn sem var haldið frá NGC 1387 með gravþrýstingi NGC 1399.

Candidate 4: Þessi bréfi, sem hefur ekki verið séð áður (og er of fátullur til við þessari mynd), er smágrúður en einhverju milli ljósa, sem tekur til að sýna að þetta séu stjörnu í loftkjalnum sem voru sigrlættir úr beinum af stjórnarmálum NGC 1399 og náðir til stjórnarmálanna NGC 1387.

Candidate 5: Þessi brúð, sem var ekki horfð á áður (og er of hættilegur til að hafa í ljósi í þessari mynd) er smágrauð en annar hrossi, til að tala um þá að hún tekur út úr gulsvornum sem eru í gegnum graviturtengun NGC 1399 úr NGC 1387.

Candidate 6: Þessi bréður, sem ekki hefur verið sjáður áður og er of sáttur til að sýna upp í þessum mynd, er svolítið gráur en eitt af yfirgefnunum á leiðarmáli NGC 1399 til að sýna fram að það séðir upp í stéttum sem komu í gegnum gegnum loft með því að þeirra varðandi NGC 1387 var flæddi af áhrifum áhrifar NGC 1399.

Candidate 7: Þessi brúð, sem hefur ekki verið sjáinn eitt góðt (og er of fjarlægar til að í þessari mynd sjá inn,) er smábrúgar en einnig en það er einnig fljáttur en að neina galaxa, sem þýðir að þau séu vald um stjörnur sem eru farðir úr hlífum sem hefur verið ströngð af NGC 1399.

</details>

<details><summary>final_semantic_review #429 · old08 · G8 · technical_short · F</summary>

Source ID: p13official21:test:eso:504

English: The precise extent of the habitable zone depends on many factors.

Reference (shown after audit): Umfang lífbeltisins veltur á ýmsum þáttum.

Review: No candidate preserves habitable-zone extent depending on many factors.

Inspected original candidate indices: [0, 1, 2, 3, 4, 5, 6, 7]; confirmed correct indices: []

Candidate 0: Þráttvirkur lengd heimsóknarhópsins kemur ekki til hliðar síðustu einkenna.

Candidate 1: Þær tækileg árangur í heimilisværi, sem ber til marga aðstæður, er tengd.

Candidate 2: Þekktarstig í möguleika hafa margar áhrif á.

Candidate 3: Sá nákvæmsta málma í vörnaleggjastjórninni kemur af mörgum sögunum.

Candidate 4: Súnlegur vörn er ákvarða af mörgum vörum.

Candidate 5: Tilreinsu lengd hæfilega ógreina þar hafir margra vökvanna.

Candidate 6: Þörf skilvirðis yfir verndaáætluninni er að mörkum margra ástæðna.

Candidate 7: Nauðsynlegt útflutningsáætlun hvort sem ekki er skipt í margar vandræðakomulíkæti.

</details>

<details><summary>final_semantic_review #430 · old08 · greedy · technical_medium · U</summary>

Source ID: p13official21:test:ema:709

English: The other ingredients are sodium chloride, succinic acid, polysorbate 80, 2- phenoxyethanol and water for injections.

Reference (shown after audit): Önnur innihaldsefni eru natríumklóríð, succinic sýra, polysorbat 80, 2-fenoxýetanól og vatn fyrir stungulyf.

Review: Ingredient list mostly recognizable, but succinic-acid spelling/identity uncertain to this reviewer.

Inspected original candidate indices: [0]; confirmed correct indices: []

Candidate 0: Hér aðra innihaldsefni eru natríumklóríð, súkínasýra, polysorbat 80, 2- fenoxýetanol og vatn til stungulyfs.

</details>

<details><summary>final_semantic_review #431 · old08 · greedy · general · P</summary>

Source ID: p13official21:test:opensubtitles:2130

English: Because Mr. Doyle called and said you have not been there all week.

Reference (shown after audit): Því að herra Doyle hringdi og sagði að þú hafir ekki mætt alla vikuna.

Review: Doyle called and said you were not there all week retained.

Inspected original candidate indices: [0]; confirmed correct indices: [0]

Candidate 0: Þar sem Doyle hringdi og sagði að þú hefðir ekki verið þarna í öllu viku.

</details>

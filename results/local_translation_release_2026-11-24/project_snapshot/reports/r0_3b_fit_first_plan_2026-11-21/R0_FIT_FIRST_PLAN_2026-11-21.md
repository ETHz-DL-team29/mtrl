# 3B R0：先验证拟合再定向SFT / Verify fit, then targeted SFT

2026-11-21 · Europe/Berlin · PROPOSAL ONLY / 仅方案；未分配GPU、未启动训练。

## 明确决策 / Decision

优先处理SFT的训练拟合和技术中长句正确候选覆盖，暂不重跑DAPO。奖励排序验证是之后恢复RL的独立条件。原P15 R0和本轮负结果端点均保留，正式SFT从DAPO之前的P15开始。

Prioritize SFT trainability and correct-candidate coverage on technical medium/long sources. Pause further DAPO. Reward verification is a separate prerequisite for returning to RL. Preserve both endpoints and start any production SFT from P15, before DAPO.

## 证据与边界 / Evidence and limits

| Evidence | Observed | Interpretation |
| --- | --- | --- |
| P15 known-seen training audit | 7/16 correct before and after; long0/4 | Observed failure to recover some seen meanings; not a tiny-set overfit test or proof of capacity ceiling |
| P16 R0 sampling audit | 6/16 groups contain a confirmed correct candidate; technical medium/long2/8 | Candidate coverage is a concrete bottleneck on this panel |
| P16 matched128 evaluation | chrF++44.007→41.837; BLEU17.943→16.921 | Reject this pilot as an upgrade |
| Reward top1 audit | 5/16 confirmed correct at each endpoint; strict wrong preference in1 good group per endpoint | Reward errors coexist with coverage limitations; counts do not identify the causal contribution to regression |

以上语义判断由同一AI助手完成，含不确定项，不是冰岛语母语专家认证。7/16并不证明模型学不会；上轮句对通常只出现1–2次。原SFT覆盖轮采用继承优化器及1e-5逐步衰减到5e-6的低学习率，因此不原样重复同一配置。

Semantic labels are conditional same-assistant judgments with uncertainty, not native-Icelandic certification. The7/16 result does not prove inability to learn: examples generally had only1–2 exposures. The previous coverage phase inherited optimizer state and decayed LR from1e-5 toward5e-6. Repeating that configuration unchanged is not the proposed action.

## 第一关：小数据拟合 / Gate1: tiny-set fit

从训练侧选64条逐条核查关键语义的真实平行句，32中句、32长句；不加入测试错句或其改写。若无法确认参考准确，替换或标为不确定并排除。先冻结32条训练内审核项，每类16条。

Select64 real training-side parallel pairs,32 medium and32 long, inspecting every reference for key meaning. Do not insert test errors or their paraphrases. Replace uncertain references. Freeze32 in-training audit items,16 per length stratum.

在原P15的诊断副本上重复训练，最多0.25M目标token、最多45分钟有效训练；连同加载和检查，总计约45–60分钟。保持同一分词器、提示、target-only loss和rank16全线性层LoRA；使用fresh AdamW、固定峰值LR3e-5，诊断时关闭dropout。核验label mask/EOS、可训练参数、非零梯度和实际参数变化。

Use a disposable P15 copy, repeated tiny-set exposure, up to0.25M target tokens and45 minutes of actual training, about45–60 minutes including load/checks. Same tokenizer/prompt, target-only loss and rank16 all-linear LoRA; fresh AdamW with fixed peak LR3e-5; dropout disabled for the fit probe. Check masks/EOS, trainable parameters, gradients and real parameter change.

项目预设通过标准：32条中至少26条保留关键语义，且16条长句至少12条通过。必须看自由生成，不能仅凭teacher-forced loss下降。通过只证明能拟合这小组，不是R0质量认证。未通过立即停止扩大训练，归类为当前SFT配置/数据拟合未过关，转查具体失败环节；不自动追加数据、时长、LoRA秩搜索或RL。

Predeclared engineering gate: at least26/32 preserve key meaning, including12/16 long items, assessed by free generation, not teacher-forced loss alone. Passing demonstrates tiny-set fit, not R0 quality. Failure stops scale-up and triggers inspection of the failing SFT configuration/data component; no automatic longer run, rank search or RL.

小数据刻意拟合是训练调试方法；本项目的样本数和阈值是预算内工程选择，并非文献给出的DAPO标准。[Lightning官方调试说明](https://api.lightning.ai/docs/pytorch/stable/debug/debugging_intermediate) / Deliberate tiny-set fitting is a debugging technique. Our sample sizes and thresholds are project choices, not universal DAPO requirements.

## 第二关：有限预算的定向SFT / Gate2: bounded targeted SFT

仅第一关通过后启动。从原P15重新加载，丢弃微型拟合副本。训练数据约1–2万句，以约1M唯一目标token为主尺度，预计两次曝光，实际最多2M目标token；不是预先声称已具备这么多合格数据。按目标token配比：技术中句40%、技术长句40%、通用/技术短句回放20%。

Start only after Gate1. Reload original P15 and discard the fit-probe adapter. Aim for10k–20k pairs, approximately1M unique target tokens and roughly two exposures, capped at2M targets. Availability/quality must be verified first. Target-token mixture:40% technical medium,40% technical long,20% general/technical-short replay.

沿用现有过滤池，额外核查漏译、否定、主体/宾语、数字、药物/法律/天文术语和重复模板；不把MetricX分数当作参考正确的唯一证据。训练集与开发/最终验证按曝光记录排除重合，能取得文档ID时还需文档隔离；缺少文档ID须披露，不能声称文档独立。找不到足够未见验证数据，先停在数据准备阶段。

Reuse the filtered pool with additional checks for omissions, negation, argument roles, numbers, technical terms and template duplication. MetricX alone does not certify references. Exclude overlapping train/development/final sources using exposure records and document IDs where available; disclose missing document IDs. If enough unexposed validation sources cannot be established, stop at data preparation.

正式SFT单一配置：现有rank16 LoRA，不量化、不更换基座；BF16冻结基座+FP32 LoRA；fresh AdamW，峰值LR3e-5、3% warmup、cosine至3e-6、gradclip1、dropout0.05；全局有效target-token均值loss，累积约4096 target tokens/更新，完整样本不截断。该LR为待验证的预设，不宣称最优。

One production configuration: existing rank16 LoRA, same base, no quantization; BF16 frozen base plus FP32 LoRA; fresh AdamW, peak3e-5,3% warmup, cosine to3e-6, gradclip1, dropout0.05; global valid-target-token loss and approximately4096 target tokens/update; no silent truncation. This is a declared setting, not a claim of optimal LR.

0.5M时做低成本开发检查；1M时核查固定开发面板的greedy和G8语义。如果正确候选覆盖及关键语义错误均无改善，不继续到2M；loss下降不能单独解锁续训。通用能力出现明显退步立即检查；连续退步则停止。最多一轮、最多2M目标token，实际GPU训练（含中途开发检查）上限4小时。

Cheap development check at0.5M; fixed greedy/G8 semantic check at1M. If neither correct-candidate coverage nor key semantic errors improve, do not extend to2M. Loss decrease alone cannot unlock continuation. Inspect clear general regression and stop on sustained regression. One round only, at most2M targets and4 hours including in-training development checks.

## R0验收与奖励 / R0 acceptance and reward

使用与训练隔离的新开发面板选一个检查点；封存权重后，仅评估一次新的最终128句greedy和64组技术G8（短16、中24、长24）。前后生成均固定同一FP32精度、提示、G8/T0.7及EOS。最终面板不参与学习率、数据或检查点选择。旧128句只能作为历史锚点，不冒充全新确认集。

Select one checkpoint on separated development data, seal weights, then evaluate a new final panel once:128 greedy sources and64 technical G8 groups(short16/medium24/long24). Match FP32 inference, prompt, G8/T0.7 and EOS. Final sources do not tune LR/data/checkpoints; the old128-source anchor is not a new confirmation set.

沿用之前已提出的项目标准：64组至少39组有确认正确候选，且中句至少12/24、长句至少12/24、短句至少8/16；通用chrF++相对原R0下降不超过1.5，且无新的成片关键语义退步。另报告greedy语义、好坏混合组、U项及配对不确定区间，不能用chrF++单独宣布通过。只有候选覆盖实质改善且最终语义方向一致才提升为新R0；否则保留原R0并如实报告未达标。这些是项目验收线，不是DAPO的理论门槛。

Retain the previous project criteria: at least39/64 groups with a confirmed correct candidate; at least12/24 medium,12/24 long and8/16 short; general chrF++ loss no worse than1.5 and no broad new key-meaning regression. Report greedy semantics, mixed-quality groups, uncertainty and paired intervals. Promote only with substantial candidate improvement and consistent final semantics; otherwise retain original R0. These are project acceptance criteria, not DAPO theory.

本轮不重训MetricX、不搜索多组奖励权重。用训练侧独立来源建立64个固定好坏译文对比，按来源分成校准/验证两半；先锁定当前MetricX与纯chrF++两个诊断候选，参考译文与标签在看到分数前核查。验证要求：关键否定/数字/角色对比至少90%排对，全部对比至少80%排对，并披露小样本不确定性。chrF++也可能不通过，不预先认定它更好；不能用它作为训练奖励后再仅凭chrF++评价成功。

Do not retrain MetricX or search reward mixtures. Build64 fixed good/bad comparisons on independent training-side sources, split by source into calibration/verification. Lock current MetricX and plain chrF++ as two diagnostic candidates before scoring, with references/labels checked first. Require at least90% correct critical negation/number/role rankings and80% overall on verification, disclosing small-sample uncertainty. chrF++ may also fail; it is not assumed superior and cannot be the sole evaluator when used as reward.

只有R0验收和奖励验证均通过，才另排约1.5–2小时的小预算DAPO。任何一关未通过，本轮不再启动RL。奖励问题不会因为SFT通过而自动消失。

Schedule a separate1.5–2 hour DAPO pilot only if both R0 acceptance and reward verification pass. No RL if either fails. Passing SFT does not automatically fix the reward.

## 时间、保存和停止 / Time, preservation and stopping

| Stage / 阶段 | Expected / 预计 | Bound / 边界 |
| --- | --- | --- |
| Data/reference QA and unexposed splits / 数据准备 | 45–60min | Complete before GPU allocation; insufficient data stops preparation |
| Colab setup + tiny fit / 加载及微型拟合 | 45–60min | Failure stops scale-up |
| Targeted SFT including dev / 定向SFT含开发检查 | 3–4h | Up to2M targets; no-benefit stop at1M; timing cap wins |
| Final evaluation + reward check / 最终评估与奖励验证 | 60–90min | Frozen checkpoint; no tuning on final panel |
| Verified export + reports / 核验保存与报告 | 30–45min | Reserve before training; original deadline never resets |

数据就绪时预计总计6–8小时：数据准备最多1小时，之后Colab分配总上限7小时，全部模型运算在Colab，保留最后至少2小时用于最终评估、奖励验证与持久化，主训练截止不得侵占该预留。若时序不足减少训练token，不省略最终核验；无法完成全部验收则报告未完成，不降低标准。上轮实测SFT约2.1M targets/2.16小时，长句占比提高后按更慢速度预算；前10分钟仅测吞吐并冻结可执行token上限，不据质量改预算。

With ready data, expect6–8 hours total: up to1 hour preparation and at most7 hours allocated Colab time. Reserve the final2 hours for evaluation, reward verification and persistence. Reduce training tokens if time is insufficient; do not skip verification or lower criteria. Previous SFT processed about2.1M targets in2.16 hours; budget more slowly for long sources. First10 minutes measure throughput only and freeze a feasible token cap.

微型拟合失败通常约1–2小时内就能结束本次尝试。8小时是支出上限，不是保证能得到强R0的承诺。所有配置、数据SHA、曝光、候选、标签、优化器/RNG检查点及中英MD/HTML保存在D:/deep learning project的独立日期目录；不运行本地模型，不操作前台浏览器，不修改电源设置。

A failed fit probe should end the attempt in about1–2 hours. Eight hours is a spending cap, not a promise of a strong R0. Save configuration/data hashes/exposure/candidates/labels/full optimizer-RNG checkpoints and bilingual MD/HTML under dated D-drive directories. All model work stays on Colab; no local models, foreground-browser or power changes.

Evidence files: D:/deep learning project/experiments/r0_3b_coverage_sft_2026-11-20/training_fit_review/summary.json ; D:/deep learning project/experiments/r0_3b_coverage_sft_2026-11-20/training_fit_reference_spotcheck.json ; D:/deep learning project/reports/dapo_p15_3b_pilot_2026-11-21/DAPO_P15_3B_RESULTS_2026-11-21.html

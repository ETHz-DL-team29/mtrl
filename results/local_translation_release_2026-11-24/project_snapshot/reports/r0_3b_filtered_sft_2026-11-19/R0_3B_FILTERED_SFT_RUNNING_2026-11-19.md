# 3B R0 过滤后 SFT：启动与执行记录 / Filtered-data SFT execution record

2026-11-19 · Updated UTC: 2026-11-19T13:37:06.381194+00:00

当前是正在运行的训练记录，不是训练完成报告。只有真实观测到的更新计数在下表列为结果；最终翻译质量、正确候选率和 DAPO 适用性尚未得出结论。

This is a running record, not a completed-results report. Only observed optimizer updates are reported as facts; final translation quality, correct-candidate coverage and DAPO suitability remain pending.

## 1. 目标和保留基线 / Objective and preserved baseline

从通用 Qwen2.5-3B-Instruct 的现有 A 适配器继续监督微调，改善未见技术中长句的翻译和 G=8 正确候选覆盖率，同时保留一般句能力。原 A 不覆盖，本轮不训练 DAPO，也不调用 MetricX。

Continue supervised fine-tuning the existing A adapter of general-purpose Qwen2.5-3B-Instruct, targeting unseen technical medium/long translation and G=8 correct-candidate coverage while preserving general translation. Original A is unchanged; this phase performs no DAPO or MetricX calls.

Original A: D:\deep learning project\runs\r0_3b_overnight_2026-11-18\final_selected_adapter

A weights SHA256: 9acc23c9595ac0b771bf8f21d125d18f3e993c3f449775377262e7ab73020199

## 2. 已核实进度与预算 / Verified progress and budget

| 项目 / Item | 值 / Value |
| --- | --- |
| GPU | Colab NVIDIA L4, native BF16 |
| Observed optimizer updates | 401 |
| Observed new target tokens | 500990 |
| Timing-locked target | 3000000 |
| Measured trainable parameters | 29933568 |
| Trainable tensors / dtype | 504 / FP32 |
| Effective / microbatch | 32 / 4 (OOM fallback 2/1) |
| Hard GPU deadline Berlin/CET | 2026-11-19T21:41:08.702343+01:00 |
| Maximum allocation wall time | 8 h, includes setup, dev, final evaluation and export |
| Training cutoff | 6 h after first allocation; final 2 h reserved |

用户随后增加时间约束：18:00需关闭电脑、20:00后恢复。已安排17:00冻结和完整备份，校验完成后释放本轮GPU。上表21:41是原连续分配的截止；晚上若重新分配，将按第一段实际已用GPU时间计算剩余预算，两段累计不超过8小时，暂停不算GPU占用。不会在20:00自动申请新运行时。

Subsequent user constraint: computer off by18:00 and resume after20:00. A17:00 freeze/full backup is scheduled, followed by owned-GPU release only after verification. The21:41 entry above is the original continuous-allocation deadline. Any evening allocation must use only the remaining cumulative8h budget after subtracting actual segment1 usage; the released pause is not GPU time. No20:00 allocation is automatic.

Pause/resume plan: D:\deep learning project\experiments\r0_3b_filtered_sft_2026-11-19\USER_PAUSE_AND_RESUME_2026-11-19.md

训练目标由前100步的保守吞吐、剩余评估时间和0.8安全系数锁定为300万新增目标token，不按翻译分数更改预算；EOS计入目标token，提示词与填充不计入。整句边界会令实际数略低于300万。

The first100 updates locked3M new target tokens from conservative measured throughput, remaining evaluation time and a0.8 safety factor, without using quality scores. Counts include EOS and exclude prompt/padding; whole-example boundaries may leave a small shortfall.

## 3. 数据与训练方式 / Data and training recipe

| 项目 / Item | 值 / Value |
| --- | --- |
| Frozen parallel pairs | 100642 |
| Unique-pool target tokens incl EOS | 4748344 |
| Pool SHA256 | ed37570b262f7653f7b9a240c1691753095664a85558c7a6f037f7107b0e3f73 |
| Target-token mix general/technical short/mid/long | 25% /20% /30% /25% |
| 3M prefix distinct sources | 67382 |
| 3M prefix example exposures | 81348 |
| 3M prefix maximum source fraction | 50.74%, documented approximate50% target deviation |
| Loss | Global valid target-token mean causal CE; prompt/pad excluded |
| LoRA | rank16 alpha32 dropout0.05; all7 q/k/v/o/gate/up/down projections |
| Optimizer | Fresh AdamW LR5e-5, betas0.9/0.999, wd0.01, gradclip1 |
| Schedule | 60k target-token warmup; peak until timing lock; cosine to20% |
| Context | prompt≤1024, target≤512, total≤1536; no packing |

使用已完成GPU过滤的ParIce等平行语料池；并非全部数据都来自WMT。冻结顺序按累计目标token配比交错，避免先把一个领域顺序训完。每对最多暴露2次，3M前缀约6.74万独立源文。

Use the GPU-filtered parallel corpus pool, including ParIce sources; this is not an all-WMT training set. Exposure order interleaves strata by cumulative target-token deficit. At most2 visits per pair; the3M prefix has about67.4k distinct sources.

## 4. 训练前核查 / Preflight verification

全量10万条重新分词并核对输入、目标长度；修复模板API返回结构造成的旧提示长度元数据问题后才开训。CPU数学测试3项通过；GPU上逐位确认A加载一致，显式shift与目标loss差值为0，首步参数确实变化且梯度有限。

All100k pairs were retokenized and input/target lengths verified before training, after correcting older prompt-length metadata affected by the chat-template return type. Three meaningful CPU math tests passed. GPU checks confirmed the exact A weights, zero explicit-shift loss difference, finite gradients and a nonzero first-update parameter delta.

First-update evidence: {"parameter_L2_delta": 0.006688808290085558, "finite": true, "grad_norm": 4.554614543914795}

冻结训练协议中保留了祖先方案的几个false草稿标志；它们不是本轮未获授权或未冻结的状态。当前用户授权、数据冻结、CPU准备和真实GPU更新另存有日期的执行账本；为保持检查点绑定的协议哈希，开训后不回写训练协议。

The frozen protocol retains several false draft flags from its ancestor proposal. They do not describe the current execution. Current authorization, data freeze, CPU readiness and real GPU updates are recorded in a dated execution ledger; the checkpoint-bound protocol hash is not rewritten after updates begin.

## 5. 开发集、检查点和最后评估 / Development, checkpoints and final evaluation

开发集128条，每层32条；每50万目标token测greedy和NLL，每100万及末期测固定24条技术句G=8。选择仅用已完成语义审查且满足一般句回退约束的开发检查点；最终测试256条和G=8技术64条在权重封存后生成，不用于选模型。

Development has128 sources,32 per stratum. Greedy/NLL are checked every500k targets; a fixed24-source technical G=8 set at1M intervals and the endpoint. Selection uses reviewed development checkpoints with general-regression safeguards. The256-source final greedy test and64-source technical G=8 are generated only after weights are sealed and never select the model.

这些是官方历史留出集的固定子集，不声称从未被历史评估用过。语义审查按源文判断：P=关键意义正确，F=明确错误，U=不确定；G=8确认至少一个P即可记覆盖，判F须看完所有不同候选。同一助手隐藏检查点名称辅助审查，不冒充外部母语认证。

These are fixed subsets of historical official holdouts, not a never-evaluated new benchmark. Source-based labels are P=key meaning correct, F=clear error, U=uncertain. A G=8 group is covered after confirming at least one P; F requires inspecting all distinct candidates. Checkpoint names are hidden during same-assistant review, without claiming external native certification.

| A开发基线 / A development baseline | 值 / Value |
| --- | --- |
| Overall chrF++ | 36.32325711068724 |
| Technical chrF++ | 36.59669402064523 |
| Technical medium/long chrF++ | 36.61265000576855 |
| Target NLL | 1.5703537802019245 |

这些分数只是在本轮固定开发集上的起点，不应与以前不同样本集的50分或44分直接比较；尚不能用它们推断本轮提升。

These scores identify the starting point on this fixed development set. Do not directly compare them with historical50/44 scores on different samples; they do not yet establish an improvement.

## 6. 保存、断线与费用 / Persistence, interruptions and cost

每100更新或25万目标token保存完整adapter、Adam状态、RNG、游标和协议哈希；逐块SHA和整包SHA校验后镜像到D盘。上传曾在20/27块中断，已在同一运行时恢复且整包校验通过。同步网络问题只修复本地下载助手，训练进程未重启，8小时期限未重置。

Every100 updates or250k targets, save the adapter, Adam state, RNG, data cursor and protocol hashes. D-drive mirrors verify every chunk and whole archive. Input upload resumed from20/27 chunks in the same runtime and passed the final hash. Mirror repairs affected only the local downloader; the training worker and original8h deadline were preserved.

独立后台收尾程序只操作本轮拥有的运行时：校验双份最终导出、在原预算允许时跑预先冻结的历史16句候选面板，随后释放GPU；另有8小时硬上限保护。最终报告需等真实输出和语义审查完成，不能把训练loss下降或文件导出成功写成翻译能力通过。

An independent aftercare helper touches only this phase-owned runtime: verify two final exports, run the pre-frozen historical16-source panel if the original budget allows, then release GPU. A separate hard8h guard remains. The final report requires actual predictions and semantic review; lower training loss or successful export is not a translation-quality qualification.

## 7. 文件索引 / Artifact index

| 内容 / Content | 位置 / Location |
| --- | --- |
| Training/source protocol | D:\deep learning project\experiments\r0_3b_filtered_sft_2026-11-19\source |
| Execution ledger | D:\deep learning project\experiments\r0_3b_filtered_sft_2026-11-19\execution_authorization_and_observations.json |
| Operational repairs | D:\deep learning project\experiments\r0_3b_filtered_sft_2026-11-19\operational_events.json |
| Live updates/evaluation | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\live_mirror |
| Verified full-state checkpoints | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\snapshots |
| Raw preflight proof | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\preflight_verified |
| Development semantic audit | D:\deep learning project\experiments\r0_3b_filtered_sft_2026-11-19\development_review |
| Frozen timing budget | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\live_mirror\frozen_budget.json |
| Aftercare status | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\aftercare.json |
| Final export when complete | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\exported |
| Final analysis when complete | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\analysis |
| Reports | D:\deep learning project\reports\r0_3b_filtered_sft_2026-11-19 |

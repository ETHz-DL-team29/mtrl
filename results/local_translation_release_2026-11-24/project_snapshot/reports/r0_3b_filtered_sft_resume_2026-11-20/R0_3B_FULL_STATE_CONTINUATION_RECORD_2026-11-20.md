# 3B R0完整状态续训：执行记录 / Full-state continuation execution record

2026-11-20 · Updated UTC: 2026-11-20T11:27:24.457310+00:00

用户授权“继续，上限4小时，若仍可改善则接着做”。本文件只记录已经观察到的状态，不把运行中或loss下降写成质量达标。上一段原A、2M开发候选和2.116M恢复点分别保留。

User authorization: continue with a4h ceiling, extending only if useful improvement remains. This file records observations, not a completed-quality claim. Original A, the2M development candidate and the2.116M recovery state remain separate and preserved.

## 1. 当前状态和预算 / State and budget

| 项目 / Item | 值 / Value |
| --- | --- |
| GPU | Colab NVIDIA L4 |
| Restored checkpoint | recovery_001753 |
| Restored updates | 1753 |
| Restored target tokens | 2116552 |
| Observed new segment updates | 8 |
| Latest committed target tokens | 2125953 |
| Observed phase | train_update |
| Original primary target | 3000000 |
| Maximum conditional extension target | 3500000 |
| GPU allocation CET | 2026-11-20T12:09:47.859959+01:00 |
| Training cutoff CET | 2026-11-20T14:46:17.718100+01:00 |
| Hard release deadline CET | 2026-11-20T16:01:17.718100+01:00 |

截止时间包括今天准备、上传、环境恢复、训练、开发选择、最终评估和导出，并为最初只读准备保守扣除5分钟。今天最多4小时，同时不超过前后两段累计8小时GPU分配预算；不会因为断线或重连重新计时。最终75分钟保留给评估和导出。

The absolute wall deadline covers today preparation, upload, environment recovery, training, development selection, final evaluation and export, with a conservative5minute initial-preparation allowance. Today is at most4h and both segments remain within8h cumulative GPU allocation; reconnections do not reset timing. The final75min are reserved for evaluation/export.

## 2. 恢复合同和代码修订 / Continuation contracts and implementation amendments

两份昨晚恢复包、adapter、优化器/RNG、1753步已提交记录及2,116,552目标token重新校验通过。数据、顺序、target-only loss、原训练协议、LoRA结构、Adam状态、随机状态与原学习率进度保持连续；昨晚未持久化的82步从恢复点重新执行，原始日志保留，不冒充已提交进度。

Both prior archives, adapter, optimizer/RNG,1753 committed updates and2,116,552 targets were reverified. Data/order/target-only loss/original protocol/LoRA/Adam/RNG/LR progress remain continuous. The82 previously uncommitted updates are repeated from the saved state; raw logs are preserved without counting them as committed.

新分配的绝对截止需替代昨日单段截止，故以独立segment2修订记录。包内昨日allocation_budget保留备份；启动前将新预算以独立SHA绑定，执行源码清单只去掉被替代的旧预算条目，其余代码、数据、权重逐项哈希仍一致。原协议未回写。首次控制通道握手未完成后改用新控制通道，在同一L4启动，未创建第二个GPU分配。

The new absolute deadline replaces the old continuous deadline through an explicit segment2 amendment. The packaged old allocation budget is retained. Before launch the new budget is bound to its own SHA; the execution source manifest removes only the superseded budget entry, while every code/data/weight hash remains verified. The original protocol is unchanged. A failed control-channel handshake was recovered through a fresh channel on the same L4 without another allocation.

Source amendment diff: D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\resume_code_amendment.diff

Independent budget-manifest proof: D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\control_evidence\allocation_manifest_amendment.json

CPU数学测试在正确源码工作目录3项通过；第一次从错误目录启动仅造成导入收集错误、未训练，已保留记录。GPU新环境也需通过同样核查后才恢复更新。

All3 CPU math tests passed from the correct source directory. An initial wrong-directory launch caused an import collection error before training and is recorded. The new GPU environment also checks these contracts before resumed updates.

## 3. 已锁定的开发语义复核 / Locked development semantic review

| 开发模型 / Model | Confirmed G8 covered/24 | G8 uncertain/24 | Greedy correct/32 | Greedy uncertain/32 |
| --- | --- | --- | --- | --- |
| A | 2 | 5 | 4 | 5 |
| t1001129 | 4 | 5 | 6 | 6 |
| t2000188 | 6 | 8 | 9 | 6 |

全部168张开发卡已逐条审查并锁定，卡片隐藏检查点名称。P=关键意义正确且未截断；F=明确失败，G8判F前检查全部不同候选；U=无法自信确认，单列，不计P，也不假装已经证明全部错误。技术正确候选确认数2→4→6，提供相对进展，但远未证明综合可靠。

All168 development cards were reviewed and locked with checkpoint names hidden. P means key meaning correct and untruncated; G8 F requires inspecting all distinct candidates; U remains uncertain and is neither credited as P nor represented as proven failure. Confirmed technical coverage2→4→6 is relative progress, not broad reliability.

审查由同一AI助手完成，非外部母语专家认证，也不是完全与上下文隔离的盲审。此处24条是开发样本，不能代替权重封存后的最终64条技术G8测试。

Review is by the same AI assistant, not external native-speaker certification or perfect context-blind adjudication. These24 development sources do not replace the64-source final technical G8 test after weight sealing.

## 4. 是否继续到350万 / Conditional extension to3.5M

先完成原定300万目标token。只有3M开发语义复核完成且对前一语义检查点的正确覆盖/greedy正确数均不下降、技术chrF至少+0.5、一般句不低于原A−1.5，并且保守吞吐预测还能留足时间，才追加一次50万。追加阶段保持Adam与数据游标、学习率固定在原计划末端1e−5，不重置warmup、不拉长已执行的余弦退火。

First complete the original3M target. Add a single500k tail only after3M semantic review, nondecreasing confirmed coverage and greedy P versus the previous semantic checkpoint, technical chrF gain≥0.5, general chrF≥originalA−1.5, and sufficient conservative remaining time. Keep Adam/cursor and the original floor LR1e−5, without warmup reset or stretching the already executed cosine schedule.

若条件不满足，就选择已有最优合格开发检查点并完成评估，不为用满4小时强训。选择规则仍是开发集合格候选的覆盖率优先，覆盖相差≤1组时按greedy语义、技术中长chrF和更早检查点依次判断；最终测试不参与选择。

If the gate fails, select the best eligible reviewed development checkpoint and evaluate it without forcing training to fill4h. Selection remains confirmed coverage first; within1 covered source, break ties by greedy semantic P,technical medium/long chrF and earlier checkpoint. Final tests never select weights.

## 5. 3B和0.8B同集比较 / Matched3B and0.8B comparison

最终选择封存后生成旧A和新3B的固定256条greedy及64条G8。在不突破原截止的前提下，再评估预先固定的0.8B历史selected200k技术补强模型，使用相同源文/指令、nativeBF16、greedy batch8和G8采样规则。若时间只够greedy，G8缺失会明确标记。此对比比较实际可用检查点，不是同训练量的参数规模消融。

After selection is sealed, generate fixed256-source greedy and64-source G8 for oldA and selected3B. If the original deadline permits, evaluate the pre-fixed historical0.8B selected200k technical continuation with identical sources/instruction,nativeBF16,greedy batch8 and G8 sampling. If only greedy fits, mark missing G8 explicitly. This compares practical checkpoints, not a matched-exposure size ablation.

最终80条greedy语义抽样在任何最终输出前按源文哈希冻结；最终指标、分层差值和配对bootstrap与G8源文语义审查分别报告。旧历史约50分与本轮不同集合的45.77不能直接比较。

The80-source final greedy semantic sample was hash-frozen before any final outputs. Report final metrics,stratum deltas,paired bootstrap and source-based G8 audit separately. A historical50 and this phase45.77 on different sets are not directly comparable.

## 6. 保存和文件索引 / Persistence and artifact index

| 内容 / Content | 位置 / Location |
| --- | --- |
| Original preservedA | D:\deep learning project\runs\r0_3b_overnight_2026-11-18\final_selected_adapter |
| Segment1 full-state handoff | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\resume_handoff.json |
| Segment2 budget/extension amendment | D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\protocol_amendment.json |
| Frozen original protocol and input source | D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\source |
| CPU test record | D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\local_CPU_test_results.json |
| All development labels | D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\development_review |
| Locked review summaries | D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\review_summaries.json |
| Final semantic freeze | D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\final_semantic_review\pre_generation_freeze.json |
| Historical0.8B comparator | D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\comparison08_protocol.json |
| Live updates/evaluation | D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\live_mirror |
| New verified full states | D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\snapshots |
| Final export when ready | D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\exported |
| Execution tools | D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\execution_tools |

所有新完整检查点以分块和整包SHA校验保存D盘；最终导出需两份校验副本，完成补充GPU工作后释放本轮拥有的运行时。独立硬截止守护仍生效。语义审查和最终双语结论未完成时，不能把文件导出或较低loss当作R0达标。

New full-state checkpoints are mirrored to D with per-chunk and archive SHA verification. Final export needs two verified copies; release only this owned runtime after supplemental GPU work. A separate hard-deadline guard remains. Export or lower loss does not establish R0 qualification before semantic/final reporting is complete.

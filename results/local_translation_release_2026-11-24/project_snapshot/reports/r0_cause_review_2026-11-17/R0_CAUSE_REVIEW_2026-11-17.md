# R0原因复核：尚不能归因于0.8B上限 / R0 causal review: capacity ceiling not established

日期 / Date: 2026-11-17。依据已完成的技术SFT及配对评估。此次仅复核记录；未申请GPU、未开始新训练。 / Record review only; no new GPU allocation or training.

当前能确认的是：这套定向续训配方没有达到扩大技术正确候选覆盖的目标。不能据此认定0.8B已经触及SFT上限，也不能断言唯一原因就是训练token不足。

The observed failure belongs to this continuation recipe and semantic-coverage objective. It does not establish a 0.8B SFT ceiling, nor uniquely prove insufficient training tokens.

## 已确认的事实 / Established facts

| 事实 / Fact | 含义 / Implication |
| --- | --- |
| Frozen base; rank16 LoRA;10,822,656 trainable parameters | This is a constrained adaptation configuration, not a full-capacity ceiling test / 不是全模型容量上限实验 |
| 399,895 target tokens;10,539 unique pairs;selected model at200,770 tokens | Most pairs appeared once within this continuation; earlier training exposure may exist / 本轮大多只见一次，但不能把它当作模型累计只训一遍 |
| LR1e-5→1e-6;one training seed;one configuration | Conservative continuation was tested without learning-rate,adapter-capacity or data-scaling controls / 缺少学习率、可训练容量和数据规模对照 |
| 372 adapter tensors changed;finite gradients;technical NLL1.73553→1.70585 | Weights updated and supervised prediction changed;not proof of adequate optimization or bug-free training / 确实训上，但不证明优化充分或实现完全无误 |
| Selected technical coverage3→3/24;long0→0/10 | Complete-candidate coverage did not expand on this fixed diagnostic subset / 不外推为总体正确率 |
| SFT uses target-token cross entropy;selection uses chrF++/NLL and retention guards | MetricX is auxiliary and cannot cause this SFT learning shortfall / MetricX不参与此轮SFT优化或选模 |

## 最需要纠正的解释 / Interpretation to correct

本轮是保守补强实验，能回答“这一配方是否奏效”，不足以回答“0.8B是否已到上限”。技术NLL下降与自由生成仍错译可以同时发生；它提示需要核查训练样本拟合和生成泛化之间的差距，但尚未定位该差距的唯一原因。

This was a conservative strengthening experiment, not a capacity-limit experiment. Falling teacher-forced NLL can coexist with poor free generation; that motivates a training-fit/generalization diagnosis, not a unique causal conclusion.

40万检查点在记录的最终128条上差于选中20万检查点，不证明所有更大SFT都无效。旧选择集通用能力触发保留护栏，也不能单独证明技术过拟合。

The recorded final400k checkpoint performs worse than selected200k on the final128. This does not establish that every larger SFT run fails. The general-retention guard alone does not prove technical overfitting.

## 定位原因的最小实验 / Minimal discriminating diagnosis — proposed, not executed

先固定一批确实被选中模型见过、经质量复核的文对，分层包含通用、技术短句与技术中长句；在原R0及选中模型上同时检查逐句teacher-forced NLL、greedy译文和关键含义保留。保留集单独报告，不将训练集表现当作泛化质量。

Fix quality-reviewed pairs actually seen by the selected checkpoint. Compare original/selected per-pair NLL,greedy translation and semantic retention across strata. Report held-out results separately; training fit is not generalization.

| 结果 / Result | 支持的定位 / Diagnostic implication |
| --- | --- |
| Training examples translate poorly too / 训练样本也译不好 | Audit loss alignment,prompt/tokenization and optimization,then test fitting a small clean subset / 先查训练链路与优化，再做小集合拟合 |
| Changing LR or adapter capacity enables fitting / 调整学习率或适配容量后能拟合 | The original optimization/adaptation setup was limiting;this is not evidence of the whole0.8B ceiling / 原配方受限，不能说整个0.8B到顶 |
| Training examples fit;held-out examples fail / 训练样本好，保留样本差 | Prioritize coverage,alignment quality and generalization / 优先检查数据覆盖、对齐质量与泛化 |
| Multiple audited configurations still fail on a clean small subset / 多个经核对配置仍无法拟合干净小集合 | Investigate representational/pretraining/adapter restrictions;this alone still does not prove a universal0.8B ceiling / 才进一步怀疑表示、预训练或适配限制，仍不能宣布普遍容量上限 |

仅能记住小集合不等于能达到用户要求的泛化水平；反过来，单一LoRA配置拟合失败也不足以证明基础模型容量不足。 / Memorizing a small subset does not establish target generalization, and one LoRA setup failing does not establish insufficient base-model capacity.

## 证据入口 / Evidence

完整原始结果 / Full completed results: D:/deep learning project/reports/r0_technical_sft_2026-11-17/TECHNICAL_SFT_RESULTS_2026-11-17.html

配置 / Protocol: D:/deep learning project/runs/r0_technical_sft_2026-11-17/exported/protocol.json

结构化结果 / Structured results: D:/deep learning project/runs/r0_technical_sft_2026-11-17/analysis/results.json

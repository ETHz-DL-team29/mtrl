# 八小时3B R0恢复方案与文献依据 / Eight-hour3B R0 recovery and evidence

2026-11-21 · Europe/Berlin · 已授权执行 / Authorized execution; checkpoint quality remains to be measured.

目标是从通用Qwen2.5-3B继续得到可复用的英→冰岛语checkpoint。原P15权重保持原样。本轮研究覆盖12项直接相关论文或第一方资料，不声称穷尽全部文献；不把7B/13B或100亿token训练的结果套用为八小时保证。 / Produce and evaluate a reusable generic-Qwen-derived English→Icelandic checkpoint while preserving P15. This is a targeted12-source review, not exhaustive literature coverage; large-model or10B-token results do not guarantee this8h run.

## 相对上一版的明确修订 / Revisions to the earlier proposal

| Item | Frozen execution decision |
| --- | --- |
| Origin | Same generic Qwen2.5-3B-Instruct + originalP15 adapter; no translation-specialist weights |
| Capacity | rank16/alpha32→rank64/alpha128; preserve scale2 and old blocks; new B columns zero |
| Optimizer | fresh AdamW; old decayed optimizer state not reused |
| Fit probe | 64 source/reference pairs audited;32 free-generation checks;P≥26/32,longP≥12/16;LR1e-4;at most250k targets/45min actual training |
| Production | Discard fit weights;restart expanded original;LR5e-5→5e-6,50k warmup;BF16 base+FP32 LoRA;all-linear;dropout.05 |
| Data | 17,911pairs,991,863unique target tokens,two exposures1,983,726targets;about10/10/40/40% general/short/medium/long |
| QA | 80 reference pairs inspected,16 excluded from fit;103 total production quarantines;not native-certified full-pool audit |
| Evaluation | New selecteddev128/final128,old selected input exclusions;source5gramJaccard≥.85 vs100642pool yielded0hits;not proven document/pretraining independence |
| Selection | Reviewed devG8 coverage→greedyP→technicalCF→earlier;generalCF delta≥−1.5;final test never selects weights |
| Budget | Conservative research-inclusive hard deadline2026-11-22 04:40CET;training must stop≥2h earlier;no reset |
| Allocation | One owned ColabL4;no local neural training/inference;no foreground browser/power changes |
| Priority | This run focuses on SFT and checkpoint acceptance;no DAPO,MetricX retraining or preference-method sweep |

目标token预算上限还受首30步吞吐测量限制；主训练最多4小时。微型拟合不通过则不扩成大训练；到1M目标token候选覆盖和greedy语义均无改善则停止。完整恢复状态在1M及末期保存，中间保存adapter；所有记录和哈希同步到D盘，固定截止不会因修复或断线延后。 / Throughput measured in the first30 production updates can reduce the target budget. Main training is capped at4h. Failure of the fit gate stops scale-up;no semantic improvement at1M stops continuation. Save full recovery state at1M/final and intermediate adapters, with D-drive hashes and a deadline that never resets.

最后交付原R0、开发集选出的新adapter、FP32推理脚本、独立评估和中英MD/HTML。如果未达到预先规定的G8≥39/64、长句≥12/24等项目线，报告必须标为未验收，不能改名字冒称可用。检查点文件可交付与翻译质量已达标是两个不同事实。 / Deliver original R0, the development-selected adapter,FP32 inference,independent evaluation and bilingual reports. If predefined project criteria such asG8≥39/64 andlong≥12/24 fail,the result remains unqualified; a saved checkpoint is not proof of sufficient quality.

## 文献逐项判断 / Source-by-source interpretation

### ALMA · ICLR2024

[ALMA · ICLR2024](https://arxiv.org/abs/2309.11674)

两阶段：单语适应后高质量平行SFT，包含冰岛语；原实验有大规模单语训练，不能把其结果许诺给本轮8小时。

Uses monolingual adaptation followed by high-quality parallel SFT, including Icelandic. Its extensive monolingual stage cannot be reproduced within this8h run.

采用质量优先平行SFT；不载入ALMA权重，不宣称复现其语言能力。 / Adopt quality-focused parallel SFT; no specialist weights or ALMA performance claim.

### AMI WMT25 · 3B英→冰岛语

[AMI WMT25 · 3B英→冰岛语](https://aclanthology.org/2025.wmt-1.46/)

最接近的3B冰岛语系统使用100亿英/冰岛语token预训练及后续SFT、偏好与后处理，仍落后最强系统。

The closely matched3B Icelandic system uses10B English/Icelandic pretraining tokens, SFT and additional stages, and remains behind leading systems.

证明规模障碍真实；不据此说3B做不到，也不承诺短训练达到论文系统。 / Treat as evidence of substantial language adaptation, not proof of a3B ceiling or a short-run guarantee.

### LoRA Learns Less and Forgets Less · TMLR2024

[LoRA Learns Less and Forgets Less · TMLR2024](https://arxiv.org/abs/2405.09673)

在代码和数学等设置中，常见低秩配置学习弱于全参，但遗忘较少；不能直接推广为冰岛语rank16必然不够。

Standard low-rank settings can underperform full tuning while forgetting less in studied programming/math regimes; this does not prove rank16 inadequate for Icelandic.

停止把rank16停滞叫做3B上限；扩大可训练适配空间。 / Avoid conflating low-rank adaptation with model capacity; increase adaptation space.

### LoRA Without Regret · 原作者实验2025

[LoRA Without Regret · 原作者实验2025](https://thinkingmachines.ai/blog/lora/)

研究强调全线性层、足够适配容量、批量与学习率；实验中LoRA往往需要比全参更高LR，但主要使用其他模型/任务。

Finds that layer coverage, adapter capacity, batch size and LR matter; higher LoRA LR is useful in studied settings, not an exact Icelandic hyperparameter prescription.

沿用全线性层；rank64、新优化器与更高但固定的LR先过拟合检查。 / Keep all-linear coverage; test rank64 and fresh higher-LR optimization through a fit gate.

### rsLoRA · 2023

[rsLoRA · 2023](https://arxiv.org/abs/2312.03732)

讨论rank增加时缩放对学习的影响。

Studies the rank-dependent scaling of adapter updates.

本轮不直接切换缩放；alpha16/32→rank64/alpha128，保持alpha/r=2及原适配块，新增B列为0。 / Preserve scale2 through zero-padded rank expansion rather than mixing a new scaling rule into this run.

### QLoRA · NeurIPS2023

[QLoRA · NeurIPS2023](https://arxiv.org/abs/2305.14314)

低比特冻结基座可节省微调内存；文中结果不等于任意模型任意任务无损。

Low-bit frozen bases reduce tuning memory; reported results are not a universal lossless guarantee.

当前L4可容纳BF16基座，避免量化成为新变量。 / Retain BF16 because it fits, avoiding a new quantization variable.

### DoRA · ICML2024

[DoRA · ICML2024](https://arxiv.org/abs/2402.09353)

用幅度/方向分解改进适配，是候选方法，不是本任务已验证收益。

Magnitude/direction decomposition is a candidate alternative, without verified benefit for this task.

本轮不叠加新方法；先建立可用R0。 / Defer additional methods until a useful R0 exists.

### LoRA+ · ICML2024

[LoRA+ · ICML2024](https://arxiv.org/abs/2402.12354)

研究A/B不同学习率对适配效率的作用。

Investigates unequal learning rates for adapter factors.

不同时搜索A/B倍率；本轮固定新AdamW和统一LR。 / Avoid a new factor-LR search; use one declared optimizer setting.

### ALMA-R/CPO · ICML2024

[ALMA-R/CPO · ICML2024](https://arxiv.org/abs/2401.08417)

偏好优化可改进已有翻译模型，也指出人工参考仍可能有质量问题。

Preference optimization improves existing translation models and highlights imperfect human references.

参考逐条抽查并保留U；本轮不改跑CPO/DAPO。 / Inspect references and keep uncertainty; defer preference training.

### Qwen2.5官方SFT示例

[Qwen2.5官方SFT示例](https://qwen.readthedocs.io/en/v2.5/training/SFT/ms_swift.html)

官方示例使用全线性LoRA和1e-4学习率；这是另一规模/数据示例，不是3B冰岛语最优值。

An official example uses all-linear LoRA and1e-4, on a different model/data setting; it is not an optimum for our task.

微型拟合1e-4；主SFT5e-5，固定日程并检查泛化。 / Use1e-4 for the fit probe and5e-5 for bounded production SFT, with generalization checks.

### PEFT官方LoRA文档

[PEFT官方LoRA文档](https://huggingface.co/docs/peft/v0.22.0/package_reference/lora)

r、alpha、目标模块等影响适配定义；本轮实际固定peft0.21.2，已验证的训练环境优先。

Rank, alpha and target modules define the adapter. Execution stays on the already verified peft0.21.2 environment.

扩容检查原块逐值保留、新增B列0，并做模块输出一致性检查。 / Verify copied old blocks, zero new B columns and module-output parity.

### Lightning官方训练调试

[Lightning官方训练调试](https://api.lightning.ai/docs/pytorch/stable/debug/debugging_intermediate)

先拟合少量数据是定位训练能否学习的调试方法。

Deliberately fitting a tiny dataset is a debugging technique for trainability.

64条已审核句对、32条自由生成审核；通过不等于泛化通过。 /64 audited pairs and32 free-generation checks; fitting is distinct from generalization.

## 当前证据与未证明的事项 / Local evidence and unresolved claims

上一轮已见训练样本AI核查7/16、长句0/4；本轮DAPO前G8正确候选6/16，之后仍6/16；同条件chrF++44.007→41.837。它们支持优先修复拟合与候选覆盖，但不能证明3B上限、某个具体学习率最优、或rank扩大必然提高翻译质量。 / Previous known-seen audit7/16,long0/4;DAPO G8 coverage6/16→6/16 andmatchedchrF++44.007→41.837. These motivate fit and coverage work but do not establish a3B ceiling,an optimalLR or guaranteed rank-expansion benefit.

所有语义审核仍是同一助手、有保留U项的条件性判断。后续正式论文结论需独立人工核查、重复种子和可信奖励；本轮不会把AI审核冒充母语专家盲评。 / Same-assistant semantic review retains uncertainty. Formal conclusions require independent human review,replication and a credible reward; AI review is not native-expert blinded certification.

资料与实际代码/数据决定保存在experiments/r0_3b_recovery_sft_2026-11-21；原冻结结果不覆盖。 / Evidence and executed inputs are archived separately without overwriting prior results.

# 下一轮系统性翻译SFT：获得可泛化、能产生正确候选的3B R0 / Systematic translation SFT for a capable 3B R0

2026-11-18 · Europe/Berlin · 状态：仅方案，未启动 / PLAN ONLY — NOT STARTED

核心决定：保留当前3B A，从A新建独立续训分支。起点始终是通用Qwen2.5-3B-Instruct；不以翻译专用模型替代，不从DAPO权重继续。本轮只做一次扩规模SFT与预先定义的验收，0.8B保留为未来对照。

Decision: preserve current 3B A and create a separate continuation branch from it. The origin remains the general-purpose Qwen2.5-3B-Instruct, never a translation specialist or a DAPO checkpoint. This round comprises one larger SFT run and prespecified acceptance; 0.8B is preserved for a later comparison.

目标不是“loss下降”或“chrF++涨一点”，而是未见技术句能产生更多核心含义正确的译文，且不明显牺牲普通翻译。希望得到明显更好的R0，但现有证据不能保证成功或给出成功概率。

The goal is materially better faithful translations and correct-candidate availability on unseen technical sentences while retaining general translation. Lower loss or a small overlap-score gain is insufficient. Improvement is a testable objective, not a guaranteed outcome or quantified probability.

| 固定项 / Fixed | 方案 / Proposal |
| --- | --- |
| Actor lineage | Qwen2.5-3B-Instruct → prior SFT → A → new systematic SFT |
| Parent adapter | D:\deep learning project\runs\r0_3b_overnight_2026-11-18\final_selected_adapter |
| Parent SHA256 | 9acc23c9595ac0b771bf8f21d125d18f3e993c3f449775377262e7ab73020199 |
| Data goal | 50k–100k distinct filtered parallel pairs, with sampled reference QA; not yet prepared |
| Training exposure | Nominal 3.0M NEW target tokens; timing-locked 2.5/3.0/3.5/4.0M, max 2 passes |
| Compute | Original Colab/Edge + official CLI workflow; prefer L4; at most 8h GPU wall |
| Primary outcome | Semantic P coverage of matched G8 on 64 unseen technical sources |
| Current action | Write proposal and evidence only; no data-build/model call/GPU allocation/training |

<details><summary>01 · 已有证据与本轮假设 / Evidence and the hypothesis being tested</summary>

## 已有证据与本轮假设 / Evidence and the hypothesis being tested

| 已观察 / Observed | 能说明 / Supports | 不能说明 / Does not establish |
| --- | --- | --- |
| 0.8B clean32 fitting: both LRs trainchrF100 and32/32exact; heldout35.41→26.20/24.64 | Repeated tiny-set fitting can memorize without generalizing | Universal0.8B capacity ceiling; all broadSFT already overfit |
| 3B parent999,931targets; A adds898,707; selected A chain≈1,898,638targets | Current A is already meaningfully task-adapted, not a zero-shot model | A has received adequate translation-scale supervision |
| A fresh112 chrF44.17 vs parent41.27, paired+2.90[1.17,4.71] | SFT has produced real gains on that set | Every further SFT will improve; score predicts faithful technical outputs |
| B executed1,000,317targets; selectedB at500,620; candidate gains did not improve confirmed coverage | More similar continuation can fail the semantic objective | Any larger/more diverse dataset is futile |
| P10 primary64 chrF32.004→29.753; BLEU7.271→5.263; originalG8 P3/16 | The tested small DAPO did not establish benefit; technical candidate support is weak | RL is universally ineffective; sole cause is SFT; no3B model can learn the task |

本轮工作假设：当前A仍缺少足够广、正确且训练充分的英冰映射，尤其技术语义和中长句关系。以更广覆盖的可靠监督和完整训练改善泛化，是值得进行的一次工程尝试；这不是已经识别的唯一根因。数据、曝光和长度处理构成一个工程方案，本轮不能把收益单独归因于某一项。

Working hypothesis: A still lacks sufficiently broad, faithful and adequately learned English–Icelandic mappings, particularly technical meanings and longer-range relations. Broader reliable supervision with adequate exposure is a justified engineering attempt, not an identified exclusive cause. Data, exposure and length handling form a recipe; gains cannot be causally assigned to one ingredient here.

历史44.17与P10新集合33.44来自不同来源、提示和构造分布，不能相减称为同一个A退化；本轮必须在同一冻结测试上重生成A和新模型。旧P/G/B标签也不能直接混比：本方案的P表示核心语义正确，对应历史G；历史P原本是部分正确且有重大缺损。

Historical44.17 and P10’s new-set33.44 differ in sources,prompt and constructed distribution; they are not a regression of unchanged A. Regenerate A and the new candidate on the same frozen test. This plan’s P means semantically usable, corresponding to historical G, not the older major-defect partial-P label.

</details>

<details><summary>02 · 范围、起点和本轮不做的工作 / Scope, initialization and excluded work</summary>

## 范围、起点和本轮不做的工作 / Scope, initialization and excluded work

| 项 / Item | 固定决定 / Fixed decision |
| --- | --- |
| Task | English→Icelandic, standalone sentence/segment translation; not certified document translation |
| Origin | General-purpose Qwen2.5-3B-Instruct @ aa8e72537993ba99e69dfaafa59ed015b17504d1 |
| Initialization | Load public/local pinned base plus existingA LoRA; preserve nonzero weights; freshAdamW |
| 0.8B | Preserve all prior checkpoints; no second training branch this round |
| Adaptation | Existingrank16,alpha32,seven attention/MLP projection classes; frozenbase |
| Excluded | No DAPO, reward retuning, translation-specialist start, backtranslation, synthetic-teacher distillation, tiny-set refitting, rank search or full-parameter switch in this round |

这是从通用模型出发的下游专门化。使用已训练A续训没有改变这一研究目标，也避免丢弃已验证收益。失败后不自动切换rank、模型、语言或再开一轮训练；任何后续改变须另写预算与对照。

Continuing A remains downstream specialization from a general-purpose model and preserves verified learning. Failure does not automatically authorize another rank/model/language switch or run; such changes need a new bounded comparison.

</details>

<details><summary>03 · 训练数据：规模、覆盖和出处 / Training data: scale, coverage and provenance</summary>

## 训练数据：规模、覆盖和出处 / Training data: scale, coverage and provenance

先在CPU重新扫描已有ParIce/ParIceFiltered、OpenSubtitles与Tatoeba原始归档，目标5万—10万不同句对，不限于上次不足3万的新候选池。原始池大不等于存在同样数量的高质量样本；本文件不声称已准备成功。至少5万不同合格句对才启动“大规模”分支，未达标则先报告数据供给不足。

Rescan existing ParIce/ParIceFiltered,OpenSubtitles and Tatoeba archives onCPU, targeting50k–100k distinct pairs rather than just the previous sub30k fresh pool. Raw size is not clean-data availability. Require50k eligible distinct pairs before this larger-run launch; otherwise report data-supply failure first.

| 分层 / Stratum | 有效目标token占比 / Target-token share | 设计意图 / Intent |
| --- | --- | --- |
| General | 30% | Standalone general statements/questions, retain lexical and sentence translation |
| Technical short | 15% | Terminology in complete sentences, facts/numbers/roles |
| Technical medium | 30% | Conditions, agents/objects, clause relations |
| Technical long | 25% | Complete multi-clause segments without dropping qualifiers |

长度按英文词数统一登记：技术短≤12词，中13–40词，长41–120词；不把包含star或galaxy的普通对白直接标成天文。普通层也覆盖不同长度。医疗、法律、天文/科学各争取占技术目标token的20%–35%，剩余可为其他技术领域；这些是数据构建目标，供给不足时必须在任何模型输出前记录真实比例及偏差，不能靠重复少数样本或猜改标签凑齐。

Register technical length bands using English words:short≤12,medium13–40,long41–120. Ordinary dialogue mentioning stars/galaxies is not automatically scientific. General data also span lengths. Aim for20%–35% of technical target tokens each from medical,legal and astronomy/science,with other technical domains filling the remainder. Record supply-driven deviations before model outputs; do not manufacture quotas by repeating a few pairs or inventing domain labels.

至少70%的本轮计划目标token来自未被A实际训练链见过的源文，其余最多30%允许高质量回放。新增是相对A的实际训练曝光，不是“从未在任何模型预训练出现”；同时分别记录是否在旧0.8B或弃置B中使用过。训练源文在本轮先去重，第二遍才允许一次全池重复，不设小集合过采样。

At least70% of planned new target tokens should come from sources absent from A’s actual training lineage; at most30% may be high-quality replay. Novelty is relative to actual A exposure,not universal pretraining novelty. Also record old0.8B/discardedB exposure. Deduplicate first-pass training; only a second broad pass may repeat each selected pair once,without tiny-set oversampling.

WMT是任务与资源出处语境，不能将所有语料叫成同一WMT官方训练集。现有Tatoeba manifest记录了WMT26 recipe条目，ParIce/OpenSubtitles有自己的归档版本与SHA；逐文件保留真实来源。正式WMT benchmark只有核实年份、split及既往使用记录后才能单独报告，不能把本轮自建256条写成官方WMT分数。

WMT supplies task/resource context,not one interchangeable corpus label. The local Tatoeba manifest references aWMT26 recipe entry; ParIce/OpenSubtitles retain their own archive/version/SHA. Verify year,split and prior use before any separate officialWMT benchmark. The constructed256-source test is not an officialWMT score.

</details>

<details><summary>04 · 监督质量：先准备好再占GPU / Supervision quality before GPU allocation</summary>

## 监督质量：先准备好再占GPU / Supervision quality before GPU allocation

| 检查 / Check | 处理 / Treatment |
| --- | --- |
| Alignment/completeness | Reject obvious missing/extra clauses, adjacent-sentence contamination, dialogue fragments requiring unavailable context |
| Entities and numbers | Flag changed names,drug names,dosages,negation,units,dates and roles; distinguish legitimate number spelling/format changes |
| Encoding/OCR | Quarantine broken words,unrecoverable mojibake and OCR; no guessed repairs |
| Language | Use source/target language checks with short-text uncertainty; do not reject technical terminology simply for ASCII spelling |
| Duplicates/conflicts | Deduplicate normalized sources/pairs; quarantine unresolvable conflicting targets; preserve multilingual characters |
| Length | Tokenize with pinned3B tokenizer; reject full examples over limits; never silently truncate target clauses |
| Reference quality | MetricX,if used diagnostically,is auxiliary only; no reward-score-only acceptance of a reference |

按固定hash分层审查200对候选：通用40、技术短40、中60、长60。先不看模型译文或MetricX分数。启动要求：明显重大监督缺陷≤4/200、不确定≤20/200，且任一层明显缺陷率≤5%。不通过时最多修订一次过滤规则，再抽取完全不同的200对复审；仍不通过则停止，不分配GPU。所有通过、拒绝、不确定及规则修改都留档。抽样通过不等于全量母语认证。

Review200 hash-selected pairs:40general,40short,60medium,60long,without model outputs orMetricX scores. Launch requirements:≤4 clear material defects,≤20 uncertain pairs,and≤5% clear defects in each stratum. Allow at most one filter revision plus a disjoint200-pair re-audit; a second failure stops before GPU allocation. Preserve every decision and rule change. Sampling is not full native certification.

AI可辅助执行审查，但不能同时把自己改写的参考当金标准、再把自己的模型判断当独立人工评测。有冰岛语审查资源时优先复核关键技术事实；没有时明确标签来源与不确定性，不虚构专家或一致性结果。

AI review can assist,but AI-rewritten references and same-assistant judgements are not independent human gold evaluation. Prefer qualified Icelandic checks of critical technical facts when available; otherwise disclose provenance/uncertainty without inventing expert review.

</details>

<details><summary>05 · 划分、去污染和固定最终测试 / Splits, exclusions and a fixed final test</summary>

## 划分、去污染和固定最终测试 / Splits, exclusions and a fixed final test

在选择训练流前，先固定开发和最终测试来源。优先按可用文档/出处组划分；无文档ID时按来源元数据与规范化句群划分并说明限制。最终测试排除A实际训练链、所有已知旧训练/开发/测试/奖励控制与已阅读语义卡的精确和近重复源文/参考。以源文5gram候选检索加Jaccard≥0.85作为启发式近重复检查，保留检索覆盖和漏检风险说明。

Freeze development/final-test sources before selecting the training stream. Prefer document/provenance groups; otherwise use available metadata and normalized sentence groups with caveats. Exclude actual A training,known historical train/dev/test/reward-control and inspected review sources/references,including heuristic near duplicates. Use5gram retrieval andJaccard≥0.85 with documented retrieval coverage/limitations.

不要为了制造“新”，排除整个从未训练的候选池后只从剩余尾部分布取最终测试；那会改变难度和领域。代表性来自预先固定的领域×长度配额，而不是按模型分数挑容易或困难句。历史曝光无法完整追溯时写明“未发现已知重合”，不声称完全未见或预训练去污染。

Do not construct novelty by discarding every untrained candidate pool and sampling only its tail; this shifts difficulty/domain. Use prespecified domain×length quotas,not model-score selection. Incomplete history supports only no-known-overlap,not absolute unseen/pretraining-decontaminated claims.

| 用途 / Use | 规模 / Size | 规则 / Rule |
| --- | --- | --- |
| Dev greedy/NLL | 128 =32 per general/short/medium/long | May guide checkpoint selection; independent from training |
| Dev semantic/G8 | 32greedy (8perstratum),24technicalG8sources (8pertechnicalstratum) | Fixed IDs; no changing failure cases into training references |
| Final matched greedy | 256 =64 per stratum | A and ONEdev-selected candidate; inspect once after weight seal |
| Final technicalG8 | 64sources:16short+24medium+24long | Same sources,seeds,T.7,G8 for A/candidate |
| Final greedy semantics | 80sources:20perstratum | BlindA/candidate; selected before any outputs |
| Historical sets | Keep unchanged | Regression context only; no claim that inspected old sets remain fresh |

最终source/reference可在CPU数据准备时审查，但不得依据任何模型输出修改。优先仅纳入明确可用参考，不确定参考进入独立附录。主测试名单、所有剔除和source/ref SHA在GPU调用前冻结；验收后不能从同一测试再选别的checkpoint。

Source/reference QA precedes outputs; uncertain references enter a separate appendix. Freeze primaryIDs,all exclusions and source/reference hashes before GPU calls. Final outcomes cannot trigger another checkpoint choice on the same test.

</details>

<details><summary>06 · 训练配方与实现约束 / Training recipe and implementation constraints</summary>

## 训练配方与实现约束 / Training recipe and implementation constraints

| 设置 / Setting | 计划 / Planned |
| --- | --- |
| Loss | Target-only causal cross entropy,including correctEOS; global valid-target-token mean across accumulated microbatches |
| LoRA | r16/alpha32/dropout.05;q,k,v,o,gate,up,down; existingA values retained |
| Optimizer | FreshAdamW;LR5e-5;betas(.9,.999);eps1e-8;wd.01;clip1 |
| Schedule | 60k target-token warmup; hold peak until timing lock; then cosine to20% of peak at locked final token |
| Batch | Effective32examples;micro4→2→1 only forOOM; preserve effectivebatch via accumulation |
| Length | Prompt≤1024,targetincludingEOS≤512,total≤1536; preserve whole targets |
| Precision | NativeBF16 frozenbase+FP32LoRA training; matchedFP32 final evaluation;TF32off |
| Padding/packing | Dynamicpadding and lengthbucketing;no cross-example packing this round |
| Exposure | First broad pass preferred; max2new passes; no answer-based sample oversampling |
| Seeds | {"data": 2026111891, "split": 2026111892, "train": 2026111893, "sampling": 2026111894, "bootstrap": 2026111895, "blind": 2026111896} |

复用已有经过核对的训练代码，不因为文档更新就升级整套依赖或切换新trainer。新增路径只做针对性的目标mask/EOS、手算CE、padding与累积梯度分母、A权重逐tensor载入、checkpoint恢复和长度拒绝检查；不再做0.8B式32对反复记忆实验。记录真实trainable参数、各层梯度、有效目标token与更新幅度。

Reuse the audited trainer and pinned dependencies,not an automatic framework upgrade. Check changed paths for targetmask/EOS,manualCE,padding/accumulation denominators,exact A loading,recovery and length rejection. Do not repeat the0.8B32-pair memorization probe. Log actual trainable parameters,layer gradients,valid targets and update magnitude.

学习率按有效目标token而不是可变长度的step计数：前6万token线性预热；预热完成且计时锁定后开始cosine衰减，到固定终点为峰值20%。衰减起点为max(6万,锁定时已训token)；如果100步时还没完成预热，先完成预热，不提前衰减。这样首100步作为正式训练也不需要事后改写预热或重启优化器。

Index the schedule by valid target tokens: warm up linearly through 60k, then start cosine decay at max(60k, tokens seen at timing lock), ending at 20% of the peak. If 100 updates finish before warmup completes, finish warmup first. Retained probe updates need no retrospective schedule change or optimizer restart.

额外保存固定32条实际训练样本在正常训练过程中的NLL和greedy快照，与开发集分开；不额外优化这些句子。它作为低成本训练拟合轨迹，不能单凭训练分数高就晋升R0。

Track32 fixed actual training pairs during the ordinary run,reporting NLL/greedy separately from dev,without extra optimization. This is a low-cost fit trace,not a new memorization experiment or promotion criterion.

</details>

<details><summary>07 · 实际规模与八小时可行性 / Actual scale and the eight-hour feasibility bound</summary>

## 实际规模与八小时可行性 / Actual scale and the eight-hour feasibility bound

| 历史记录 / Historical record | tokens | trainseconds | targettokens/s |
| --- | --- | --- | --- |
| StageA | 898707 | 4317.0 | 208.2 |
| StageB | 1000317 | 4894.4 | 204.4 |

历史训练段约204–208targettoken/s，包含其既定训练实现的计时口径，不是新长度分布的吞吐保证。按205/s粗算，新增300万token仅训练段约4.07小时，500万约6.78小时，1000万约13.55小时；完整任务还需设置、开发评估、最终生成和导出。因此不承诺8小时内完成500万—1000万token和全部验收。

Historical train segments average204–208targettokens/s under their recorded implementation; this is not a forecast guarantee for the new lengths. At205/s,3M/5M/10Mtargets require roughly4.07/6.78/13.55hours of training alone. Setup,development,finalgeneration and exports are additional. Do not promise5M–10M plus acceptance in8hours.

本轮名义目标新增300万、绝对上限400万有效目标token，约为此前A新增90万的3.3–4.4倍；不是语言模型预训练意义上的“大规模”。50k–100k指准备好的唯一句对池，实际读到多少、完整走了几遍必须另报，不得把池大小或计划token当已完成训练量。

Nominal NEW exposure is3M,hardmax4Mtargets,about3.3–4.4times A’s0.9M increment—not pretraining-scale training.50k–100k denotes the prepared unique pool; report actual distinct exposures/passfraction separately,never as if the whole pool was consumed.

| GPU阶段 / Phase | 规划上限 / Planning envelope |
| --- | --- |
| Setup/verification | About30minutes; included in overall480-minute cap |
| Training + scheduleddev + intermediate saving | Up to330minutes from firstallocation; less if setup is slow |
| Final dev decision + matched final generation + durable exports | Reserve120minutes; starts no later than allocation+360minutes |
| Total | Hard480minutes from FIRSTGPUallocation; CPUpreparation/postrelease labels/report outsideGPUcap |

上述时间是分配规划：训练最晚在首次分配+360分钟停止，前30分钟设置并不另加到总额。首100次真实更新就是保留轨迹的开始，用前向/反向实测每步tokens/s的25百分位、未来开发/保存预留和0.8安全系数，从250/300/350/400万网格选择可行的最大目标；只按计时锁定一次，之后不因质量加时或改学习率。无网格目标可行时，保存部分进度并报告预算不可行，不把缩水前缀称为完整大规模训练。

These are planning envelopes,not additive permission beyond480minutes. Training ends by first allocation+360minutes. The first100 real updates remain on the trajectory. Lock once to the largest feasible2.5/3/3.5/4M grid using step-throughput25thpercentile,futuredev/save reserves and0.8safetyfactor. Never extend for quality or changeLR afterward. If no grid fits,preservepartialprogress and report infeasibility rather than calling a reduced prefix a complete larger run.

若token预算只能覆盖池的一部分，采用已冻结、按领域和长度交错的顺序，不从容易句开始截取；如第一遍完成且仍有预算，才以新固定shuffle进行第二遍。第二遍不能使每条在本轮出现超过两次。原方案“至少完整一遍”是目标而非8小时保证；未完成必须明确标记。

A partial budget follows the frozen interleaved domain/length stream,not an easy-first prefix. Only after completing pass1 may a second seededshuffle begin,with atmost2usesperpair. One complete pass is an objective,not an8-hour guarantee; incomplete execution is explicitly flagged.

CPU准备时先计算交错流中前5万不同句对的完整目标token总数；如果它已超过400万绝对上限，则本计划不能承诺完整覆盖这些句对，应在占GPU前报告不匹配并调整书面预算。所有token终点按完整样本边界结束，实际数可略低于目标，不截断译文凑整数。

Before GPU allocation, count full target tokens for the first 50k distinct pairs in the interleaved stream. If this already exceeds the 4M hard cap, report the mismatch and revise the written budget before allocation. Stop at full-example boundaries; actual tokens may be slightly below the target, never truncate translations to hit a round number.

</details>

<details><summary>08 · 开发评估、选模和提前停止 / Development evaluation, selection and early stopping</summary>

## 开发评估、选模和提前停止 / Development evaluation, selection and early stopping

每50万有效targettoken保存完整恢复点并运行固定dev128 NLL/greedy；完整G8与语义开发审查仅在A零步、约100万、约200万和最终目标进行，避免每几十步重做大评估。审查可在训练继续时在CPU并行完成；只看开发集，不读取最终测试输出。

Every0.5Mvalid targets save a fullstate and evaluate fixeddev128 NLL/greedy. FullG8/semanticdev checkpoints are onlyA zero,approximately1M,2M and the final target. CPU review may run while GPU training continues; final-test outputs remain unread.

开发候选先满足普通翻译chrF++相对A下降≤1.5、无新增普遍结构故障；先取技术G8覆盖最多值以内1/24组的合格候选组成并列集合，再依次比较greedy语义P数、技术中长句chrF++和更早checkpoint。这个固定集合定义避免两两“差不足2”产生非传递并列，也避免一个不确定标签决定结果。P/U分歧不能通过看模型身份或分数重新标成P。

Dev eligibility requires general chrF decline≤1.5 from A and no new widespread structural failure. Form a tie set of eligible candidates within one covered source of the maximum technical G8 coverage, then rank by greedy semantic P count, medium/long chrF, and earlier checkpoint. A fixed maximum-based set avoids nontransitive pairwise ties. Identity or scores never justify relabeling U as P.

连续两次50万检查点开发指标停滞，只触发检查，不单独因词面指标平台自动终止：需结合最近两次已完成语义开发审查，若正确候选未增加、greedy语义未增加且技术chrF改善<0.5，才按停滞停止。若语义审查尚未完成，不据缺失值宣称失败；按原预算继续，但不加时。普通chrF下降>3点或反复出现明显语义/输出崩坏时回滚并停止；数值非有限、错权重或恢复状态不一致立即停止。

Two flat0.5Mmetric checks trigger inspection,not an automatic overlap-only stop. Stop for plateau only when the latesttwo completed semanticdev reviews show no coverage/greedysemantic gain and technicalchrF improves<0.5. Missing reviews are not failure evidence; continue only within the fixed cap. General decline>3points or repeated broad semantic/output collapse triggers rollback/stop. Nonfinitevalues,wrongweights or inconsistentrecovery stop immediately.

最终评估前封存唯一所选权重SHA。只在开发证据完成的候选中选择；必要时退回已审查的更早模型或A，不让等待审查耗尽导出预留。若A仍最好，最终结论直接是这轮没有形成更强R0。

Seal exactly one selectedweightSHA before final evaluation. Select only revieweddev candidates;fall back to an earlier reviewedcheckpoint orA rather than exhaust exporttime waiting. IfA remainsbest,report no strongerR0 from this run.

</details>

<details><summary>09 · 正确候选的定义与盲审 / Correct candidates and blinded review</summary>

## 正确候选的定义与盲审 / Correct candidates and blinded review

P：核心意义、参与角色、数字、否定、条件和重要子句保留，允许不改变意思的小语法或屈折问题；F：存在重大错译、漏译、添加、关系反转或不可用输出；U：无法可靠判断。候选必须非空、未被长度上限截断，才可计为正确P。U不算确定正确，另给P+U上界。

P preserves core meaning,roles,numbers,negation,conditions and important clauses,allowing minor nonsemantic grammar/inflection issues. F denotes material mistranslation,omission,addition,inversion or unusableoutput. U is uncertain. Only nonempty,untruncatedP counts as correct. ReportP+U as an uncertainty upperbound,not confirmedaccuracy.

对同源A/新模型的G8候选混排隐藏模型、checkpoint、奖励、chrF及BLEU；审查者可看英文和已核查参考。完全相同的source+hypothesis要求相同标签，冲突保留为U敏感性结果而非择优改标。所有标签先锁定并保存hash，再解盲汇总。关键语义错误逐类计数，不把词面匹配率当语义标签。

Shuffle matchedA/newG8candidates without model,checkpoint,reward or metricidentity;source and checked reference remain visible. Identical source+hypothesis requires consistent labels; disagreements receive a symmetric U sensitivity analysis rather than favorable relabeling. Lock/hashlabels before unblinding. Count critical semantic error types separately from overlap.

| 量 / Quantity | 定义 / Definition |
| --- | --- |
| Coverage@8 | Fraction of sources with at leastoneP among8; source-level paired comparison |
| Correctcandidate rate | Pcount / all8N candidates; not equivalent to sourcecoverage |
| Mixedgroups | Sources containingP andF;descriptive RLopportunity,not a reason to reject all-correctgroups |
| Greedysemantic usability | Pfraction on fixed80source subset |
| Uncertainty | Ucounts andP+Ucoverageupperbound; AIreview notnativegold |

</details>

<details><summary>10 · 项目验收线：什么叫本轮达到目标 / Project acceptance: what counts as reaching the goal</summary>

## 项目验收线：什么叫本轮达到目标 / Project acceptance: what counts as reaching the goal

以下是本轮事前提出的工程目标，不是文献中的DAPO硬门槛，也不意味着低于它的模型不能RL。目标刻意要求实质语义改善，避免再次把一两分chrF当成功；执行前与具体测试名单一并冻结，不按结果调低。

These are proposed exante projecttargets,not publishedDAPOadmissionrules. They require material semantic progress rather than a1–2pointchrFgain. Freeze them with the exacttest before execution and never lower them after results.

| 验收项 / Acceptance | 目标 / Target | 说明 / Interpretation |
| --- | --- | --- |
| Primary technicalCoverage@8 | ≥39/64sources (≥60.9%) | DefiniteP only; short≥8/16,medium≥12/24,long≥12/24 |
| Substantial improvement claim (separate) | At least13/64 additional covered sources net; paired95%coveragegain interval lower>0 | ≥20.3percentagepoint target; not an absolute R0 qualification requirement |
| Greedysemantic usability | Technical≥30/60;general≥14/20 | Coremeaningusable,not perfectnative-style output; smallsampleuncertainty disclosed |
| Overlap/retention guards | GeneralchrFdelta≥−1.5;overall andtechnicaldelta≥0 | Pairedintervals reported; pointguard is not statistical proof of noninferiority |
| Criticalerrors | No broad increase in number/negation/role/condition failures; disclose allcounts | No hiding regressions behind a mean score |
| Integrity | Matchedgeneration,knownleakagechecks,verifiedweights/exports,fullactualexposure | No qualification without auditable artifacts |

分三种结果：①达到工程目标：冻结为本项目下一阶段R0，并明确AI审查与单种子边界；②有可靠进步但未达到目标：保存为改进候选，逐项说明缺口，不能包装成综合强基座；③无实质改善或退化：保留A作为当前历史基线，停止此配方追加。数据或预算不足另记为“未完成”，不能混成能力失败。

Three outcomes:1targetsmet—freeze the next-stage projectR0 withAI/single-seed limitations;2reliablebutinsufficientgain—preserve an improved candidate and list gaps without broad certification;3no material gain/regression—retainA and stop extending thisrecipe. Data/budget infeasibility is incomplete execution,not a demonstrated model capacity failure.

“R0绝对能力达标”与“比A大幅提升”是两张独立成绩单：若达到绝对语义/覆盖目标并保持相对A的质量护栏，但增益不到13组，可称工程目标达标，不能称大幅超过A。若同一新测试显示A本身已达到绝对能力目标，也应承认现有A可用，而不是人为强求新模型必须大幅提升才承认可靠。未经独立语义复核不能作母语级可靠性承诺。

Absolute R0 capability and substantial improvement over A are separate outcomes. Meeting the absolute semantic/coverage targets with retention guards can qualify the project R0 without a13-source gain, but does not support a substantial-gain claim. If matched evidence shows A already meets the absolute targets, acknowledge A as usable rather than demand a large new gain as the definition of reliability. No native-level reliability promise follows without independent semantic review.

Coverage增益按源文配对、按技术长度层分层进行2000次bootstrap；候选不能当作512个独立源句。chrF++/BLEU也按源文配对。区间不含训练种子、文档聚类或语义标注误差；U上下界与领域结果单独报告。只有一条训练链，本轮不能宣称跨种子稳定或达到任何公开排行榜水平。

Use2000 paired source-stratified bootstrap replicates forcoverage,chrF++ andBLEU.512candidates are not512independent sources. Intervals exclude training seed,document clustering andlabel error;reportU bounds/domain results. One chain does not establish cross-seed stability or leaderboard standing.

</details>

<details><summary>11 · 奖励与后续SFT/DAPO比较 / Reward and subsequent SFT/DAPO comparisons</summary>

## 奖励与后续SFT/DAPO比较 / Reward and subsequent SFT/DAPO comparisons

R0质量合格与MetricX奖励校准通过是两个独立状态。此次纯SFT不通过MetricX选训练参考、优化权重或决定R0合格。历史奖励失败对照继续保留；不能因新R0变好就宣布评分器修复，也不要求30步DAPO必须显著涨分才承认R0有翻译能力。

R0quality andMetricXcalibration are independent statuses. This SFT does not optimize/select qualification throughMetricX. Preserve failed reward controls; betterR0 does not repair reward. Conversely,significant gains in a30stepDAPO are not the definition of translation capability.

| 后续支线 / Later branch | 固定与比较 / Controls |
| --- | --- |
| R0 zero update | Exact same frozenR0 andtest |
| R0 continuedSFT | Same eligibletrainingsources;supervisedtargets;log tokens/time/memory |
| R0 standardDAPO | SameR0 andsourcepool;fixed validatedreward/sampling;log allgeneration/scoring/update costs |
| Efficiencyvariants | Compare to fixedstandardDAPO,not a differentR0/data/reward;equalGPUtime andqualityversuscost curves |

继续SFT对照与DAPO不是“完全同样的信息”：SFT直接看到参考，DAPO通过参考奖励间接使用监督。比较应明示信息、数据、实际总算力与预算，不把相同update数叫公平成本。正式SFT/DAPO和效率比较需要另外封存最终评估；本轮已查看的验收集此后只能作开发/历史集。

SFT directly accessesreferences;reference-rewardDAPO accesses supervision differently. Disclose information,data andtotal actual compute rather than equatingupdatecounts. Later formalcomparisons need another sealedfinal evaluation; this round’s inspectedtest becomes historical/development data.

</details>

<details><summary>12 · Colab执行、恢复和成本 / Colab operation, recovery and accounting</summary>

## Colab执行、恢复和成本 / Colab operation, recovery and accounting

沿用Edge登录、官方ColabCLI与本机D盘镜像工作流；数据审核和编码先在CPU完成，确认GPU可用后才分配运行时。优先L4；若只有T4，先测可行性，按同一截止时间自动降低可承诺token，不承诺相同训练量，不购买额度。不要同时打开多个控制运行时把GPU/CPU连错。

Keep the Edge/officialColabCLI/D-drive mirroring workflow. CompleteCPU dataQA/tokenization before allocatingGPU. PreferL4;T4 requires measurement and the same wall deadline with potentially lower achievabletokens,not purchasedquota or equalwork promises. Keep one ownedruntime identity to avoid accidentalCPU/GPU switches.

每100次更新或约25万targettoken（先到者）保存可恢复adapter、AdamW、scheduler、全部RNG、epoch/bucket顺序、cursor和预算状态；至少每50万token保留一份D盘SHA验证的完整状态。服务每15秒心跳，监控只读取已有运行时，不反复创建GPU。

Save recoverablestate every100updates orapproximately0.25Mtargets,whicheverfirst:adapter,AdamW,scheduler,all RNG,epoch/bucket order,cursor andbudget. Mirror at least every0.5M fullstate toD withSHA verification. Send15secondheartbeats and inspect the ownedruntime without repeatedly creatingGPUs.

优先直接可靠回传到D盘，Drive仅作为额外持久化选择，不把一次挂载成功当保存完成。恢复不重置首次分配截止时间；逻辑更新、弃置/重算的物理更新分别记录。接近deadline必须先验证最终adapter及完整状态已落D，再释放GPU；报告上传、等待、评分、恢复和回传全部成本。

Verified directD-drive transfers are primary;Drive is optional redundancy,not proof ofcompleted saving. Recovery never resets the first allocationdeadline. Distinguish retainedlogicalupdates from discarded/recomputedphysicalupdates. Verify finaladapter/fullstate on D before release,and account for setup,waits,scoring,recovery andtransfers.

按历史整段计费观察，L4可能约每小时1.8–2CU；8小时可暂留约15–18CU的预算空间，但这不是现价或额度承诺。启动时读取实际GPU、余额和消费率，日志用实测CU。CPU数据准备与GPU释放后的盲审/报告另需时间，8小时不是保证全部人工审查文档都在8小时内完成。

Historical account observations suggest roughly1.8–2CU/h forL4;reserveabout15–18CU forplanning an8h ceiling,not as a current price/quota promise. Read actualGPU,balance andconsumptionrate atlaunch. CPUpreparation andpostrelease semanticreview/reporting take additionaltime;8hGPU is not an8h endtoendreview guarantee.

</details>

<details><summary>13 · 文件交付与可复现记录 / Deliverables and reproducibility</summary>

## 文件交付与可复现记录 / Deliverables and reproducibility

| 产物 / Artifact | 内容 / Content |
| --- | --- |
| Datasetmanifest | ArchiveURL/version/SHA,eligible/rejectedcounts,actualdomain/lengthmix,exactuniques,targettokens,new-to-Afraction |
| QAandexclusions | Every200paircard,labels,filterversions,heldoutchecks,nearduplicateretrievallimits |
| Frozenexecutionprotocol | Finaldatahashes,seeds,prompt,tokenlimits,exacttargetlock/LR,budgetdeadline,allsoftwareversions |
| Trainingrecords | Loss/NLL/gradnorm,tokenexposure,perpairhistory,devchecks,checkpoints,RNG/optimizer/scheduler,bucketorder |
| Blindreview | Cards,hiddenidentitymap,lockedlabels/hash,duplicateconsistency,uncertainupperbounds |
| Finalcomparison | All256pairedgreedy,all64×8×2candidates,semantics,bootstrap,domain/lengthresults,criticalerrors |
| Model | Selectedadapter plus exactbase/hash andloadinstructions;originalA andalloldweights unchanged |
| Cost/report | GPUminutes/CU/peakmemory,logicalvsphysicalwork,datedbilingualMD/HTML,CSV/JSON,CPUreproduction |

本方案与proposal.json先存experiments/r0_3b_systematic_sft_2026-11-18；真正执行时另建runs同名目录，不能把方案状态冒充已完成实验。所有新文件都在D盘，凭据/代理令牌继续留在私有控制目录而不进入报告包。

This proposal lives underexperiments/r0_3b_systematic_sft_2026-11-18;create the matchingrunsdirectory only for actualexecution. A plan is never an executedexperiment. Newartifacts remainon D;credentials/proxytokens remainprivate and outside deliverybundles.

</details>

<details><summary>14 · 启动顺序与明确停止规则 / Launch order and explicit stop rules</summary>

## 启动顺序与明确停止规则 / Launch order and explicit stop rules

| 顺序 / Step | 动作 / Action | 失败时 / On failure |
| --- | --- | --- |
| 1CPU | Inventoryhistory;rebuildeligiblepool;review200;freeze splits/trainorder | Supply/QA insufficient→noGPU |
| 2CPU | Pin source/dependencies;targetmask/load/recovery checks;hashinputs | Implementation mismatch→fix beforeGPU |
| 3GPU | OwnedL4;firstallocationdeadline;loadA;baseline/dev;first100realupdates | OOM/throughput infeasible→savepartial,do not promisefullrun |
| 4Lock | Freeze timing-onlytarget andschedulerhorizon once | No feasible2.5Mgrid→incompletefeasibility outcome |
| 5Train | Broad interleavedSFT;scheduleddev/semantics;durable states | Collapse/confirmedplateau/deadline→stop,retainbestdevcandidate |
| 6Seal | ChooseONE revieweddevcandidate;sealSHA beforetest | No candidatebetterthanA→A remainsselected;report honestly |
| 7Evaluate | Generate matchedA/candidate test256 andG8;exportall;releaseGPU | Export cannotverify→prioritize save/release withincap,markincomplete |
| 8CPU | Lockblindlabels,unblind,bootstrap,acceptance/status,bilingualreport | Do not lower thresholds,relabel for outcome,or run anotherSFT automatically |

如果本轮没有得到目标R0，结论应是“这套扩规模、质量控制和rank16适配方案未达到目标”。不能写成“Qwen无法翻译”或“3B达到上限”，也不能立即把下一次重复训练称为修复。下一项投入必须针对具体证据只改变一个因素，例如适配容量；不在本轮暗中追加。

If targetsremainunmet,the conclusion is failure of this bounded data/scale/rank16recipe—not thatQwen cannottranslate or3Bhititsceiling. Anotherrepeat is not automatically a fix. Any next investment must targetevidence with onechangedfactor,such as adaptationcapacity,and is not silently addedhere.

</details>

<details><summary>15 · 证据与技术参考 / Evidence and technical references</summary>

## 证据与技术参考 / Evidence and technical references

D:\deep learning project\reports\r0_cause_diagnosis_2026-11-17\R0_CAUSE_DIAGNOSIS_RESULTS_2026-11-17.md · SHA256 e93fccf5c295cc6b78890a65c0ee47bd5a111b4a8213a9478130d014d2ef038a

D:\deep learning project\reports\r0_technical_sft_2026-11-17\TECHNICAL_SFT_RESULTS_2026-11-17.md · SHA256 6309a834be474d8550d2fade06b02b6b306f334157158001c881a955cdf605a6

D:\deep learning project\reports\r0_3b_round1_2026-11-17\R0_3B_ROUND1_RESULTS_2026-11-17.md · SHA256 d318acc84aec0b9953b6c862230f63e8f76c1675f2fc87cac24468659394ca0c

D:\deep learning project\reports\r0_3b_overnight_2026-11-18\R0_3B_OVERNIGHT_RESULTS_2026-11-18.md · SHA256 fd2860c75e0ea09b02225f134733ec10a1f5a6f4a977ce9880fe52cff1bc6a33

D:\deep learning project\runs\r0_3b_overnight_2026-11-18\stage_A\exported\run\summary.json · SHA256 ffd877ff52275a4f5a4f2fb20caf8bee7b4cf74cbc0d5af0006c960e37046401

D:\deep learning project\runs\r0_3b_overnight_2026-11-18\stage_B\exported\run\summary.json · SHA256 d6f0621995b879c3cf3662a12b7565d2f24ec3119897b3eaeba49bf66812d80e

D:\deep learning project\runs\dapo_3b_xl_exploratory_2026-11-18\analysis\results.json · SHA256 c58c5ca721c1515d6feeb78a8a98cc44cdb794ed935d39919b11438e3b223975

D:\deep learning project\data\processed\train.manifest.json · SHA256 acb3afd67879a2c0402ddf6943712694c0705639b48b5d37e7ed24a6bff95b6a

D:\deep learning project\data\raw\r2_2026-11-13\download_manifest.json · SHA256 09ca26f24c1bfaa7b4dc01a9a29c8943ffc87a3b5a0ba217df1d584d1461e55c

[Qwen2.5-3B-Instruct official model card](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct) — General-purpose causal model origin; no claim of certified Icelandic translation quality

[Hugging Face TRL SFT Trainer](https://huggingface.co/docs/trl/en/sft_trainer) — Reference for response-only supervision; existing audited trainer will be reused, not automatically replaced by latest TRL

[Hugging Face PEFT LoRA reference](https://huggingface.co/docs/peft/v0.21.0/package_reference/lora) — Adapter rank,alpha and target-module semantics; no claim that larger rank solves this task

[WMT21 Translation Task](https://www.statmt.org/wmt21/translation-task.html) — English/Icelandic task and supplied training-corpus context; not a claim that all current data are official WMT21 train or test

[ParIce corpus provider](https://parice.arnastofnun.is/) — Source corpus identity, with actual local archive/version hashes recorded separately

技术参考用于核对方法语义；数据规模、学习率、预算、混合比例和验收线均是本项目提出的方案，不冒称来自官方推荐或已证明最优。未来执行时固定版本，不能拿当前网页变化替代历史软件记录。

References verify method semantics. Scale,LR,budget,mixture andacceptance are projectproposals,not officialrecommendations or provenoptima. Pin executionversions rather than replacing historicalrecords with changingdocumentation.

</details>

<details><summary>16 · 当前完成状态 / Current completion status</summary>

## 当前完成状态 / Current completion status

| 状态 / Status | 值 / Value |
| --- | --- |
| Writtenplan | Completed2026-11-18 |
| ParentAhash | Verified unchanged |
| 50k–100kqualitypool | Notyetprepared |
| Exactexecutiondata/schedule | Notyetfrozen |
| Newtrainerimplementation | Notyetimplemented/validated |
| GPUallocation/training | Notstarted |
| Expectedqualification | Objective only;no successprobability promised |

下一项实际工作是CPU数据构建、监督审查和执行代码准备；只有这些通过并封存后才谈启动GPU。这份文件满足“写入下一轮方案”，不代表本轮训练已获启动指令。

The next actual work is CPUdatapreparation,supervisionQA and executioncode. GPUlaunch follows only after those pass andfreeze. This document fulfills the requestedwrittenplan;it is not an instructionalreadyreceived tostarttraining.

</details>

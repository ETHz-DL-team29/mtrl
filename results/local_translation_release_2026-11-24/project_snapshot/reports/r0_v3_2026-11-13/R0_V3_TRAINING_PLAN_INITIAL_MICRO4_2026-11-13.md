# R0-v3 SFT 补强计划 / SFT strengthening protocol

日期 / Date: 2026-11-13. 状态：数据与代码已冻结，训练结果待验证 / Data and code frozen; training outcome pending.

## 目标 / Objective

在 0.8B 不变的前提下，从 R0-v2 接着提升一般词义和句子关系，保留中长专业翻译能力，为后续 DAPO 提供更好的候选分布。原模型保留；本轮独立目录，不覆盖任何旧结果。

Continue R0-v2 on broader general translation data with technical replay. Keep the 0.8B model, preserve prior adapters, and measure whether generated candidates become a sound starting distribution for DAPO. A higher chrF score alone does not establish semantic adequacy.

## 依据 / Rationale

上轮 R0-v2 相比旧 SFT 已有实测改善，但仍出现常用动词义项混淆、专业句关系错误与长句异常。上轮新增语料中 fired 仅有两条不同训练句（一个解雇义、一个开枪义）；这仅说明该轮上下文覆盖薄，不能推断预训练和旧 SFT 完全没见过此词，也不能据此判定 0.8B 的能力上限。

Prior measured improvements coexist with content errors. Thin lexical/context coverage in the added corpus motivates broader data before formal RL comparisons; it does not prove a model-capacity ceiling. Do not handcraft translations of failed held-out sentences into training.

## 冻结数据 / Frozen data

- Training pairs: 38799; new filtered general pairs: 25308; replay pairs: 13491.
- Unique target tokens: 1068396; planned exposure: 1999994 target tokens.
- Token mixture: general 65%, technical short 8%, medium 15%, long 12%.
- Validation: 144 pairs, 64 greedy selection prompts. New independent readiness sample: 32 prompts; prior reserved sample also preserved.
- Original historical held-outs and both official ParIce evaluation releases excluded by normalized source and reference. New official dev/test subsets also exclude every known prior-training source/reference. Near-duplicate and unknown base-pretraining overlap remain possible.
- Full language inventory for language identification; bounded lengths/ratios, numeric and punctuation agreement, foreign-script, metadata and OCR filtering. No target truncation. AI spot screening is not native-speaker certification.
- Training-only auxiliary MetricX QE error≤6 filters the added subtitle pairs after encoding/structural/language screening. No development/test pair is removed by this QE rule. The pinned FP32 scorer and all training-pair scores are recorded; the screening itself uses GPU time. Some valid translations are rejected and some errors can remain. Because the later reward uses the same MetricX, QE gains are not independent evidence of improvement.

新增一般数据来自 OPUS OpenSubtitles v2018；不能把下载的总量称为全部可用高质量训练数据。字幕存在语境依赖和错配，因此经过清洗、去重和源参考抽查。技术回放来自上轮已清洗数据，同时排除本轮新发现的官方留出样本。

The added general data are filtered OPUS subtitles, with remaining context and alignment limitations. Technical replay preserves coverage; all newly protected official evaluation pairs are removed from replay too.

第一次抽查发现大面积疑似编码污染（如冰岛语字母被其他拉丁字母替代），因此在任何 SFT 更新前归档了未审核版本并重建。原始字幕中1,019,209条命中已知字符模式；这是规则命中数，不是人工确认错误率。拒绝受影响样本，没有猜测转码修补。旧 SFT 和上轮 R0-v2 训练数据中该模式命中为0。

The preliminary unreviewed subtitle split was archived and rebuilt before any SFT update. Known character-pattern rules matched1,019,209 raw rows, a heuristic count rather than a human error-rate estimate. Affected targets were rejected rather than guessed/repaired. Earlier SFT/R0-v2 training files had zero matches for the same patterns. Sparse evaluation of the unchanged97-class language identifier matched stock predictions and probabilities on200 checked texts; this speeds preparation without narrowing the language inventory.

## 训练 / Training

Initial adapter SHA256: `806b9857024868131140da43ad3975d7c8653b97e5687420e4499a3769995847`. Pinned base revision: `2fc06364715b967f1860aea9cf38778875588b17`.

LoRA r16/alpha32 unchanged. Fresh optimizer because the data mixture changes. Peak LR 3e-5, 3% warmup, cosine schedule over 2M added target tokens, effective batch32 / microbatch4. BF16 on L4. Target-only token-weighted CE includes EOS; prompt and padding labels ignored. Maximum complete training sequence768, target256 tokens; no silent truncation.

对同一有效批次内的样本按长度分组，减少微批次填充。最多训练200万新增目标token或累计4小时，先到者停；每20万token验证，连续4次验证无改善且达到45万token后早停；约每5分钟保存完整可恢复状态。

Sort within an effective batch to reduce padding without changing its examples or loss weights. Stop at 2M added target tokens or4 accumulated training hours. Validate every200k tokens; early-stop after4 stale validations once450k tokens are consumed. Save adapter, optimizer and RNG about every5min. A stopped run is not automatically a successful new R0.

## 评估与决定 / Evaluation and decision

The expanded greedy development score keeps general and technical domains equally weighted, with equal weighting across technical lengths; NLL breaks ties. Re-evaluate the identical held-out prompts for R0-v2 and the new selected candidate. Inspect content words, negation, numbers and sentence relations, alongside chrF++ and structural failures.

G=8/T=1 matched sampling and pinned MetricX QE diagnose actual candidate utility and ranking. The newly reserved official test subset helps distinguish gains on previously diagnosed prompts from generalization. Reference-based oracle chrF is an upper bound only for that sampled bank and reference metric; it is not a semantic ceiling. Wrong-language gates and high reward are not proof of correct translation.

若候选质量、专业中长句及排序信号都有实证改善，才能讨论小规模 DAPO 试验；若只是字符重合变高而词义继续错，不将其宣称为合格 R0。正式方法比较需固定同一个合格基座及训练/评测协议。本轮不运行 DAPO。

Qualification is conditional on measured candidate quality and meaningful reward signals, with semantic inspection. Do not promote from character overlap alone. Formal method comparisons must share one frozen starting checkpoint and protocol. No DAPO updates in this round.

## 保存与复现 / Preservation and reproducibility

New source/data: `D:/deep learning project/experiments/r2_sft_2026-11-13`. New model/results: `D:/deep learning project/runs/r0_v3_colab_2026-11-13`. Prior R0-v2 remains in its Nov12 directory. Source bundle SHA256: `3427808b038e896deb68f0c8841cd01672be765cbd1c0672d06ae4edcfe2d0f1`.

Remote checkpoints are periodically copied back to the same D-drive workspace; completed artifacts require SHA256 and ZIP integrity verification. Only the runtime allocated for this run is released afterward. Authentication/session secrets are never included in deliverables.

## 数据来源与引用 / Data sources and attribution

- [ParIce official overview](https://parice.arnastofnun.is/) and [Barkarson & Steingrímsson 2019](https://aclanthology.org/W19-6115/).
- [ParIce evaluation sets 21.10](https://hdl.handle.net/20.500.12537/146), [20.05 splits](https://hdl.handle.net/20.500.12537/24), CC BY4.0.
- [OPUS OpenSubtitles v2018](https://opus.nlpl.eu/legacy/OpenSubtitles-v2018.php); [OpenSubtitles provider](https://www.opensubtitles.org/). Cite Lison & Tiedemann2016, OpenSubtitles2016: Extracting Large Parallel Corpora from Movie and TV Subtitles.
- The filtered ParIce package was downloaded for provenance/inspection; the added general training rows in this round come from the separately identified OPUS subtitle archive. Do not misattribute the alignment version to the ParIce authors.

# 3B R0 coverage SFT / 3B R0 覆盖补强续训

日期 / Date: 2026-11-20 · Updated UTC: 2026-11-20T18:00:29.562056+00:00

状态 / Status: PRIMARY_EXPERIMENT_COMPLETE_SEMANTIC_REVIEW_AND_GPU_RELEASE_VERIFIED

已核实新增更新 / Verified new updates: 1476; 新增目标token / Additional target tokens: 2096676.

## 主要结论 / Main finding

本轮有小幅改善，技术长句仍未达到目标；已早停并保留P15与原P14。诊断显示已见长句也未掌握，不能只归咎泛化，更不能据此宣称3B容量已到上限。

Limited gains, persistent long-technical weakness; training stopped and both P15/P14 retained. Errors on known-seen long cases rule out a purely unseen-data account, without establishing a 3B capacity ceiling.

GPU已释放 / GPU released: True.

原P14最佳R0始终保留。本轮是否改善，以实际开发集、既有评估和已完成语义审核分别报告；没有审核的数据不计作失败，也不计作正确。 / The preserved P14 R0 remains available. Automatic scores and completed semantic reviews are reported separately. Unreviewed outputs are neither failures nor successes.

## 固定开发集 / Fixed development set

| Checkpoint | New targets | chrF++ | Tech chrF++ | Mid/long chrF++ | General chrF++ | Tech NLL | G8 P/24 | Greedy P/32 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 0 | 46.490 | 47.100 | 47.614 | 38.615 | 1.11344 | 8 | 8 |
| t0500795 | 500,795 | 47.782 | 48.312 | 48.598 | 40.925 | 1.09210 | 8 | 8 |
| t1000902 | 1,000,902 | 48.235 | 48.816 | 48.971 | 40.689 | 1.08381 | 9 | 7 |
| t1500729 | 1,500,729 | 48.175 | 48.603 | 48.604 | 42.572 | 1.06822 | 8 | 8 |
| t2000728 | 2,000,728 | 48.283 | 48.693 | 49.044 | 42.828 | 1.05905 | 9 | 9 |

### 语义分层 / Semantic strata

P=已确认关键含义保留，U=无法确认，F=已确认关键含义错误。G8的F要求检查全部不同候选。AI审核不等同母语专家认证。 / P=key meaning retained; U=uncertain; F=key meaning wrong. A G8 group is F only after all distinct candidates are inspected.

| Checkpoint | Role | Stratum | N | P | U | F |
|---|---|---|---:|---:|---:|---:|
| A | greedy | general | 8 | 4 | 1 | 3 |
| A | greedy | technical_short | 8 | 3 | 1 | 4 |
| A | greedy | technical_medium | 8 | 1 | 1 | 6 |
| A | greedy | technical_long | 8 | 0 | 0 | 8 |
| A | G8 | technical_short | 8 | 2 | 4 | 2 |
| A | G8 | technical_medium | 8 | 6 | 0 | 2 |
| A | G8 | technical_long | 8 | 0 | 1 | 7 |
| t0500795 | greedy | general | 8 | 3 | 2 | 3 |
| t0500795 | greedy | technical_short | 8 | 4 | 0 | 4 |
| t0500795 | greedy | technical_medium | 8 | 1 | 4 | 3 |
| t0500795 | greedy | technical_long | 8 | 0 | 0 | 8 |
| t0500795 | G8 | technical_short | 8 | 2 | 4 | 2 |
| t0500795 | G8 | technical_medium | 8 | 6 | 1 | 1 |
| t0500795 | G8 | technical_long | 8 | 0 | 1 | 7 |
| t1000902 | greedy | general | 8 | 2 | 3 | 3 |
| t1000902 | greedy | technical_short | 8 | 4 | 0 | 4 |
| t1000902 | greedy | technical_medium | 8 | 1 | 4 | 3 |
| t1000902 | greedy | technical_long | 8 | 0 | 0 | 8 |
| t1000902 | G8 | technical_short | 8 | 3 | 3 | 2 |
| t1000902 | G8 | technical_medium | 8 | 6 | 1 | 1 |
| t1000902 | G8 | technical_long | 8 | 0 | 2 | 6 |
| t1500729 | greedy | general | 8 | 4 | 0 | 4 |
| t1500729 | greedy | technical_short | 8 | 4 | 0 | 4 |
| t1500729 | greedy | technical_medium | 8 | 0 | 7 | 1 |
| t1500729 | greedy | technical_long | 8 | 0 | 0 | 8 |
| t1500729 | G8 | technical_short | 8 | 2 | 3 | 3 |
| t1500729 | G8 | technical_medium | 8 | 6 | 1 | 1 |
| t1500729 | G8 | technical_long | 8 | 0 | 1 | 7 |
| t2000728 | greedy | general | 8 | 4 | 1 | 3 |
| t2000728 | greedy | technical_short | 8 | 4 | 1 | 3 |
| t2000728 | greedy | technical_medium | 8 | 1 | 3 | 4 |
| t2000728 | greedy | technical_long | 8 | 0 | 0 | 8 |
| t2000728 | G8 | technical_short | 8 | 3 | 3 | 2 |
| t2000728 | G8 | technical_medium | 8 | 6 | 2 | 0 |
| t2000728 | G8 | technical_long | 8 | 0 | 2 | 6 |

## 停止与选模 / Stopping and selection

停止原因 / Stop reason: manual_primary_semantic_gain_gate_after_2M.

已封存选中版本 / Sealed selected checkpoint: t2000728.

选择只依赖开发集。每500k目标token检查；最初的自动早停联合考察近期chrF、NLL及已审核语义，本轮另有下述适应性操作性早停。硬截止为2026-11-20 22:56:56 CET。固定评估集已在P14观察，属于继续开发用的anchor比较，不能宣称是新的独立盲测。 / Selection uses development data only. Original automatic stopping jointly checks recent chrF, NLL and reviewed semantics; this run also uses the explicitly documented adaptive operational gate below. The reused P14 anchor is not a new independent confirmatory test.

## 实际训练 / Actual training

起点为通用 Qwen2.5-3B-Instruct + P14最佳LoRA，继承AdamW动量与RNG，新的数据游标和目标token计数；冻结BF16基座、FP32 LoRA、target-only含EOS损失。LR从1e-5按新阶段4M目标token退火至5e-6。 / General-purpose Qwen initialization, preserved AdamW moments and RNG, explicitly new phase cursor, tested target-only loss, and no high-LR restart.

同一100,642句对过滤池；优先使用上轮调度未暴露句对，技术来源内短/中/长目标token请求配比10/55/35，通用句约20%；库存耗尽可改变实际比例。医学、法律与科学均保留，科学语料依旧稀缺。 / Use the same audited pool with unused-first source queues and explicit length balance. Inventory limits alter actual shares; science remains scarce.

训练池的已保存来源包含ParIce21医学EMA、法规EEA、天文ESO及Tatoeba等通用句对，也包含OpenSubtitles18通用句对；本轮没有追加新的原始语料。开发与既有anchor沿用ParIce21官方dev/test构建，保护分割不变。完整行级来源由保存的训练JSONL与过滤记录给出。 / Saved training sources include ParIce21 EMA medicine, EEA regulations, ESO astronomy and general pairs such as Tatoeba, together with OpenSubtitles18 general pairs. No new raw corpus was added in this continuation. Development and reused anchors retain the protected official ParIce21 dev/test construction; row-level provenance and filtering records are preserved.

### 执行预算与继承字段 / Executed budget and inherited fields

LR退火的4M是调度参考长度；本轮按吞吐量锁定的目标预算为3.5M新增目标token，随后按语义操作性条件提前停止。protocol中继承的dataset.token_mixture与training.nominal_new_target_tokens不是本轮实际数据调度/预算的依据，实际以coverage amendment、调度文件和frozen_budget为准。 / The4M LR schedule length is not the executed token budget. Throughput locked a3.5M target, superseded by the documented semantic stop. Inherited dataset.token_mixture and training.nominal_new_target_tokens fields are inactive for P15; the coverage amendment, actual order and frozen budget determine execution.

```json
{
  "target_tokens": 3500000,
  "p25_step_tokens_per_second": 250.31781314047265,
  "projected_safe_token_cap": 3704655.9242773554,
  "remaining_train_seconds": 17797.444574376495,
  "safety_factor": 0.8,
  "quality_used": false,
  "lock_seen_tokens": 140642,
  "lock_step": 100,
  "unix": 1795185401.8929203,
  "forecast_remaining_dev_seconds": 2616.6697141919994,
  "training_deadline": 1795206416,
  "first_allocation_deadline": 1795211816
}
```

### 主语义决策 / Primary semantic decision

在150万token检查后、200万token输出出现前，另行登记了人工操作性早停条件：200万检查后，若所有检查点的G8和greedy均未达到相对起点净增2条，且技术长句无确认正确数增长，则停止。此为适应性探索决策，不能称为最初预注册的联合NLL/chrF平台期规则已触发。 / An additional operational gate was registered after1.5M and before2M outputs. Stop after2M if no checkpoint gains at least2confirmed G8 or greedy sources over the parent and no confirmed long-source gain. This adaptive exploratory decision is distinct from the original joint NLL/CHRF rule.

```json
{
  "UTC": "2026-11-20T17:03:42.097014+00:00",
  "latest_checkpoint": "t2000728",
  "latest_target_tokens": 2000728,
  "stop_requested": true,
  "material_confirmed_gain": false,
  "technical_long_gain": false,
  "long_confirmed_P": {
    "A": {
      "greedy": 0,
      "G8": 0
    },
    "t0500795": {
      "greedy": 0,
      "G8": 0
    },
    "t1000902": {
      "greedy": 0,
      "G8": 0
    },
    "t1500729": {
      "greedy": 0,
      "G8": 0
    },
    "t2000728": {
      "greedy": 0,
      "G8": 0
    }
  },
  "baseline": {
    "labels_locked": true,
    "adapter_sha256": "8eb880545d238f4af2695d08d6aba4f8f2f6f7a204b411d77d19539936b01ce0",
    "technical_sources": 24,
    "greedy_sources": 32,
    "coverage_P": 8,
    "coverage_U": 5,
    "greedy_P": 8,
    "greedy_U": 3,
    "labels_sha256": "5cda2db0fba0f85338637ffe821ecb2bd79d85452fe123a67ea90a2ab7ffe9dc"
  },
  "reviews": {
    "A": {
      "labels_locked": true,
      "adapter_sha256": "8eb880545d238f4af2695d08d6aba4f8f2f6f7a204b411d77d19539936b01ce0",
      "technical_sources": 24,
      "greedy_sources": 32,
      "coverage_P": 8,
      "coverage_U": 5,
      "greedy_P": 8,
      "greedy_U": 3,
      "labels_sha256": "5cda2db0fba0f85338637ffe821ecb2bd79d85452fe123a67ea90a2ab7ffe9dc"
    },
    "t0500795": {
      "labels_locked": true,
      "adapter_sha256": "b0dcd062c5027fe4a3dddc5d460544473c2202dcb50bda1b5422d5c0bf1c3b5d",
      "technical_sources": 24,
      "greedy_sources": 32,
      "coverage_P": 8,
      "coverage_U": 6,
      "greedy_P": 8,
      "greedy_U": 6,
      "labels_sha256": "5cda2db0fba0f85338637ffe821ecb2bd79d85452fe123a67ea90a2ab7ffe9dc"
    },
    "t1000902": {
      "labels_locked": true,
      "adapter_sha256": "886b7db45871ec1a06d53f0a7418e1d4ae2cb07349f7d703d9300a5f3842e6db",
      "technical_sources": 24,
      "greedy_sources": 32,
      "coverage_P": 9,
      "coverage_U": 6,
      "greedy_P": 7,
      "greedy_U": 7,
      "labels_sha256": "5cda2db0fba0f85338637ffe821ecb2bd79d85452fe123a67ea90a2ab7ffe9dc"
    },
    "t1500729": {
      "labels_locked": true,
      "adapter_sha256": "3c1db5ab3eff1693686ee9a3ba695160147d94b58e9f4af6fee7bd79477c0f3d",
      "technical_sources": 24,
      "greedy_sources": 32,
      "coverage_P": 8,
      "coverage_U": 5,
      "greedy_P": 8,
      "greedy_U": 7,
      "labels_sha256": "5cda2db0fba0f85338637ffe821ecb2bd79d85452fe123a67ea90a2ab7ffe9dc"
    },
    "t2000728": {
      "labels_locked": true,
      "adapter_sha256": "54cee7d5f8e3898281d20b70019a6a47088890f89c324445b8a72e652568b858",
      "technical_sources": 24,
      "greedy_sources": 32,
      "coverage_P": 9,
      "coverage_U": 7,
      "greedy_P": 9,
      "greedy_U": 5,
      "labels_sha256": "5cda2db0fba0f85338637ffe821ecb2bd79d85452fe123a67ea90a2ab7ffe9dc"
    }
  },
  "reason": "No stable/material primary semantic gain demonstrated across four fixed checks; preserve reviewed best and finalize. Automatic NLL/CHRF joint rule need not have fired.",
  "adaptive_gate_registration_sha256": "2edb13e922a996421e9b693a52f9c6a83f2fd15bdeedda7dedf619190968362f",
  "actual_training_code_unchanged": true
}
```

人工停止后，原worker的停止标志也阻止了内部评估；其错误与中断导出信息已保留在attempts/intentional_primary_semantic_stop。随后从完整检查点、使用同一选模规则和精度独立完成最终评估，没有恢复训练。所有已完成更新计入计算成本，未保存的尾部更新不用于交付模型。 / The original stop flag also blocked its internal evaluation; interruption records remain archived. Read-only finalization from full checkpoints completed the same selection and evaluation, with no resumed training. All completed compute is counted; an unsaved tail is never used for a delivered model.
未保存尾部更新 / Uncheckpointed tail updates: 66.

最终归档的校验与成功状态以runs目录下verified_export.json和completion_manifest.json为准。压缩包内部根目录的final_export.json可能是打包前保留的中断轮次元数据，不应误认为当前归档的状态。 / The authoritative final archive verification is runs/…/verified_export.json plus completion_manifest.json. A root final_export.json inside the archive can be the preserved preceding interruption metadata, captured before the new archive is completed.

精度核查 / Precision check: 独立最终评估进程未调用训练main中的显式后端设置；同环境新进程实测matmul TF32=False、FP32 matmul precision=highest，cuDNN TF32默认True。该Transformer没有卷积层，基座仍为BF16、LoRA为FP32。不能把所有后端开关均显式关闭作为已执行事实。 / The standalone finalizer does not execute the training main function’s explicit backend assignments. Fresh-process defaults in the same environment were matmul TF32=False, highest FP32 matmul precision, and cuDNN TF32=True. This Transformer has no convolution layers; frozen BF16 base and FP32 LoRA remain unchanged.

```json
{
  "matmul_allow_tf32": false,
  "cudnn_allow_tf32": true,
  "float32_matmul_precision": "highest",
  "observation": "Fresh process default flags; finalizer imports train without calling main; frozen base inference is BF16, LoRA FP32. Transformers have no convolution layers.",
  "no_model_loaded": true
}
```

```json
{
  "unix": 1795194375.9813323,
  "new_phase_updates": 1476,
  "actual_new_target_tokens": 2096676,
  "unique_pairs": 45218,
  "unique_target_tokens": 1957504,
  "source_target_tokens": {
    "eea": 838655,
    "OpenSubtitles18": 335958,
    "ema": 733824,
    "tatoeba": 55948,
    "ted2020": 12284,
    "eso": 104861,
    "statisl": 15146
  },
  "stratum_target_tokens": {
    "technical_medium": 939549,
    "general": 419336,
    "technical_long": 598052,
    "technical_short": 139739
  },
  "previously_unused_pairs_exposed": 12750,
  "previously_unused_unique_target_tokens": 822024,
  "novelty_relative_to_P14_schedule_only": true,
  "all_training_updates_finished_before_audit": true
}
```

选中模型与最后训练状态必须区分；下表述为真正进入选中权重的新增暴露，前面的全阶段数据用于计算成本。 / Selected weights can precede the final training state. This exposure belongs to the selected checkpoint; whole-phase exposure above describes total cost.

```json
{
  "selected_tag": "t2000728",
  "selected_new_step": 1410,
  "selected_additional_target_tokens": 2000728,
  "selected_phase_distinct_pairs": 43244,
  "selected_pairs_not_in_parent_P14_schedule": 12363,
  "selected_stratum_target_tokens": {
    "general": 400097,
    "technical_short": 135872,
    "technical_medium": 894955,
    "technical_long": 569804
  },
  "entire_phase_additional_target_tokens": 2096676,
  "model_selection_can_prefer_an_earlier_checkpoint": true,
  "novelty_relative_to_immediate_parent_schedule_only": true
}
```

### 原R0复现核查 / Parent reproduction

本次原R0的256条greedy与64组G8，与P14保存的对应原R0输出逐条一致，包括生成token IDs、译文和截断标志。这支持前后比较的推理设置一致性。 / Parent decoding exactly reproduces the saved P14 outputs: all256greedy sources and all64G8groups match completion token IDs, text and truncation flags.

```json
{
  "UTC": "2026-11-20T17:21:56.558138+00:00",
  "purpose": "Check parent native decoding reproduction; no model inference",
  "banks": {
    "greedy": {
      "n": 256,
      "exact_matching_sources": 256,
      "all_completion_token_ids_text_and_truncation_identical": true,
      "differing_ids": []
    },
    "g8": {
      "n": 64,
      "exact_matching_sources": 64,
      "all_completion_token_ids_text_and_truncation_identical": true,
      "differing_ids": []
    }
  }
}
```

## 既有256句评估 / Reused 256-source anchor

| Stratum | N | Before chrF++ | After chrF++ | Delta | Before BLEU | After BLEU |
|---|---:|---:|---:|---:|---:|---:|
| all | 256 | 43.670 | 44.140 | +0.470 | 19.662 | 19.598 |
| general | 64 | 42.635 | 44.448 | +1.813 | 22.696 | 23.659 |
| technical_short | 64 | 38.615 | 40.887 | +2.272 | 17.091 | 19.876 |
| technical_medium | 64 | 43.970 | 43.415 | -0.556 | 18.905 | 17.211 |
| technical_long | 64 | 44.623 | 45.004 | +0.381 | 19.634 | 19.995 |

完整逐句greedy和G8采样保存在evaluation文件；自动分数不能证明语义正确。 / Full greedy and G8 outputs are saved. Automatic scores do not certify semantic fidelity.

输出健全性与采样统计 / Output health and sampling statistics:

```json
{
  "failures": {
    "before": {
      "gate": 1,
      "repetition": 1,
      "truncated": 1
    },
    "after": {
      "gate": 2,
      "repetition": 2,
      "truncated": 2
    }
  },
  "sampling": {
    "before": {
      "sources": 64,
      "candidates": 512,
      "mean_unique_texts": 7.9375,
      "truncated_candidates": 0,
      "mean_completion_tokens": 83.736328125,
      "not_a_semantic_accuracy_measure": true
    },
    "after": {
      "sources": 64,
      "candidates": 512,
      "mean_unique_texts": 7.9375,
      "truncated_candidates": 0,
      "mean_completion_tokens": 85.0234375,
      "not_a_semantic_accuracy_measure": true
    }
  }
}
```

重复、截断与gate失败可能重叠，不能相加为独立失败数；候选多样性不等同于语义正确。 / Repetition, truncation and gate failures may overlap and must not be summed as independent cases. Candidate diversity does not establish semantic correctness.

### 同一256句的历史位置 / Historical models on the same256sources

| Model | chrF++ | BLEU |
|---|---:|---:|
| Earlier0.8B | 33.774 | 11.654 |
| Earlier3B before P14 | 35.402 | 12.725 |
| P14 preserved parent | 43.670 | 19.662 |
| P15 selected continuation | 44.140 | 19.598 |

训练量和数据历史不同，该表描述已有模型，不隔离参数规模的因果作用。历史分数沿用P14已完成的同源比较，本轮没有重跑0.8B。 / Training histories differ; this table describes saved models and does not isolate a model-size effect. Historical results are reused from the completed P14 matched comparison;0.8B was not rerun.
Historical metrics: D:\deep learning project\runs\r0_3b_filtered_sft_resume_2026-11-20\analysis\matched_08b_3b_metrics.json; SHA256: a77494f32acc72cbe9877bc5e1d7cd80928b74a1355d050f9c772c87b6281b9c.

### 配对区间 / Paired intervals

| Subset | chrF++ delta | 95% interval | BLEU delta | 95% interval |
|---|---:|---|---:|---|
| overall | +0.470 | [-0.9673516309847132, 1.8937668079368017] | -0.065 | [-1.857187619919748, 1.70848473015027] |
| general | +1.813 | [-0.08128467023384686, 3.7732454650478116] | +0.963 | [-1.3977995927147868, 3.4063590334297493] |
| technical_short | +2.272 | [0.7978604062262841, 4.0127608876525] | +2.785 | [0.1532376631080887, 6.06162479423798] |
| technical_medium | -0.556 | [-4.732896792789142, 2.5340584798651755] | -1.694 | [-5.811624326275605, 2.2442886828735267] |
| technical_long | +0.381 | [-1.2564419723585676, 2.2910688568764397] | +0.361 | [-1.3974164685653454, 2.6489435054164736] |
| technical | +0.352 | [-1.1739006199995348, 1.760570589611209] | -0.160 | [-1.900631519083124, 1.726806856480279] |
| technical_medium_long | +0.083 | [-1.612013255592015, 1.7955416103018125] | -0.549 | [-2.4398056028249884, 1.597009251361771] |

按相同source成对抽样的corpus充分统计量bootstrap，2000次；并非句分数均值。区间不包含训练种子、语义标注和原文档聚类的不确定性。既有anchor已观察，不是独立确认性证据。 / Paired-source bootstrap of corpus sufficient statistics,2000replicates. Intervals omit training-seed, annotation and document-cluster uncertainty; the reused anchor is not independent confirmation.

## 最终anchor语义审核 / Final anchor semantic audit

| Model | Reviewed / Expected | Complete | G8 P/64 | G8 U | Greedy P/80 |
|---|---:|---|---:|---:|---:|
| before | 144/144 | True | 13 | 11 | 18 |
| after | 144/144 | True | 18 | 8 | 20 |

P是已确认语义完整的下界；U不能视作错误。未完成审核时表中数目不是完整覆盖率。 / P is confirmed semantic coverage; U is not counted as wrong. Counts from an incomplete review are not complete coverage rates.

| Model | Role/Stratum | N | P | U | F |
|---|---|---:|---:|---:|---:|
| before | greedy_general | 20 | 10 | 0 | 10 |
| before | greedy_technical_short | 20 | 3 | 1 | 16 |
| before | greedy_technical_medium | 20 | 5 | 1 | 14 |
| before | greedy_technical_long | 20 | 0 | 0 | 20 |
| before | G8_technical_short | 16 | 5 | 3 | 8 |
| before | G8_technical_medium | 24 | 8 | 5 | 11 |
| before | G8_technical_long | 24 | 0 | 3 | 21 |
| after | greedy_general | 20 | 9 | 2 | 9 |
| after | greedy_technical_short | 20 | 5 | 4 | 11 |
| after | greedy_technical_medium | 20 | 6 | 2 | 12 |
| after | greedy_technical_long | 20 | 0 | 1 | 19 |
| after | G8_technical_short | 16 | 6 | 2 | 8 |
| after | G8_technical_medium | 24 | 11 | 3 | 10 |
| after | G8_technical_long | 24 | 1 | 3 | 20 |

### 审核一致性修订 / Annotation consistency correction

对全部前后P状态变化做双向一致性复核：8条G8来源和4条greedy来源。旧R0有一条几乎相同的太阳系比较句先前被判U，而新R0按语义相同且允许语法瑕疵被判P；统一后两者均P。故本报告的原R0为13/64，而历史P14报告和本轮初审为12/64。修订不是模型变化；原标注、理由和时间保留，权重与选模不变。 / All initial paired P-status changes were checked symmetrically:8G8and4greedy sources. A nearly equivalent parent Solar-System candidate had been graded U more strictly than its after counterpart. Applying the same grammar tolerance gives both P. The harmonised parent is13/64 rather than the historical/initial12/64. Original labels and correction provenance remain archived; model weights and selection are unchanged.

```json
{
  "UTC": "2026-11-20T17:50:50.393062+00:00",
  "symmetric_scope": {
    "G8_sources": 8,
    "greedy_sources": 4
  },
  "all_initial_paired_P_changes_inspected_in_both_directions": true,
  "corrections": 1,
  "correction_cards": [
    39
  ],
  "historical_P14_cached_G8_confirmed_P": 12,
  "harmonised_current_parent_G8_confirmed_P": 13,
  "after_G8_confirmed_P": 18,
  "explanation": "Before card39 candidate6 and after card178 candidate6 have the same key meaning and nearly identical malformed similarity wording; both are P under the same grammar tolerance. Historical P14 labels/models remain unchanged. All other changed P statuses retained after paired inspection.",
  "labels_sha256": "aefb18ee0bc3b8d306e62fb5ab791940d05b3c1fb4b59ca9bfed72c225128619",
  "weights_and_selection_unchanged": true,
  "not_external_or_native_expert_review": true
}
```

```json
{
  "before": 13,
  "after": 18,
  "net_source_gain": 5,
  "gain95CI_sources": [
    0.0,
    10.0
  ],
  "replicates": 2000,
  "interpretation": "Confirmed-positive audit coverage only;U is not called incorrect. Interval conditions on this AI-assisted annotation and source sample,not native truth/training seeds."
}
```

项目综合目标的筛查不构成通用DAPO门槛；本轮没有训练或验证DAPO效果。 / Project screening is not a universal DAPO gate. This round does not demonstrate DAPO efficacy.

## 已训练样本拟合诊断 / Known-seen fitting diagnostic

该诊断在权重封存后执行，不参与选模、不增加任何训练更新。128条已知训练样本匹配开发集领域与句长配比，并尽量匹配source词数及target token数；16条greedy按四个句长/领域层各4条。 / Post-sealing evaluation only.128known-seen sources match development domain/length quotas and approximate source-word/target-token lengths;16greedy cases are balanced across four strata.

| Model | Known-seen128 NLL | Known-seen technical NLL | Corresponding dev NLL | Seen greedy P/16 | Seen greedy U |
|---|---:|---:|---:|---:|---:|
| before | 0.92804 | 0.92578 | 1.13064 | 7 | 待审核 / Pending |
| after | 0.82802 | 0.81955 | 1.07987 | 7 | 待审核 / Pending |

已知被训练不等于已学会。NLL差距本身不能区分全部原因，也不能证明模型容量上限；结合生成语义、样本曝光次数和残留数据噪声解释。 / Known exposure is not mastery. An NLL gap alone does not establish all causes or a capacity ceiling; interpret it with generated semantics, exposure and possible residual data noise.
完整采样与长度匹配清单 / Sample and matching plan: D:\deep learning project\runs\r0_3b_coverage_sft_2026-11-20\training_fit_audit\files\sample_plan.json

128条以最终所选模型的训练轨迹界定known-seen：其中121条出现在P14直接父模型调度，另7条只在本轮所选前缀中出现。后者对于before不能称为已知训练样本；这也不证明基座预训练或更早轮次从未见过。 / Known-seen is defined relative to the selected model: 121sources occur in the immediate P14 schedule and 7only in the selected P15 prefix. The latter are not confirmed-seen for the before model. This does not establish novelty to base pretraining or older runs.

| Fixed sample subgroup | N | Before NLL | After NLL |
|---|---:|---:|---:|
| parent_seen | 121 | 0.94428 | 0.84251 |
| new_phase_only_seen | 7 | 0.72321 | 0.64522 |

本轮所选前缀的样本曝光次数分布 / Sample exposures in selected P15 prefix: {"1": 63, "0": 26, "2": 24, "3": 6, "4": 9}.

### 四条已见长句的参考核查 / Four known-seen long reference spot-checks

参考译文包含这些关键术语的正确监督答案，生成仍错误；不能仅把这四例归咎于未见样本泛化或参考把这些术语翻错。该核查不证明整个池无噪声，也不是母语专家认证。 / Critical terms are present in these references while generation fails; these four errors are not explained solely by unseen-data generalisation or those particular reference terms being wrong. This is not a pool-wide clean-data certificate or native-expert audit.

| Source ID | P14 schedule seen | P15 selected exposures | Critical reference/generation comparison |
|---|---|---:|---|
| ParIce21:eso:821 | True | 2 | Reference explicitly uses systur (sisters/siblings). Generation uses fulltrúar/fulltrúi (representatives), losing the common-origin premise. |
| ParIce21:ema:185234 | False | 1 | Reference explicitly gives hármissir (hair loss). Generation uses blóðkúpu, not alopecia. |
| ParIce21:eea:3205170 | True | 1 | Reference explicitly gives authors/listflytjendur, creative/artistic work and adequate income. Generated text changes these to registered persons/telescopes and loses the income relation. |
| ParIce21:eea:1150937 | True | 1 | Reference explicitly contains umfermingu and skoðunarstöð á landamærum (transhipment/border inspection post). Generation corrupts these operational terms. |

## 资源与截止 / Resources and deadline

实际GPU分配 / GPU allocation: 229.36 min; 观察到账户计算单元减少 / Observed account CU drop: 7.3721; 截止满足 / Deadline met: True.

计算单元差额是账户余额观测，不是精确账单；包含设置、训练、评估、诊断和保存。 / CU drop is an account-balance observation, not an exact invoice; allocation includes setup, training, evaluation, diagnostic and persistence.

## 结论 / Conclusion

本轮续训有局部学习与候选覆盖增益，综合大幅提升未获支持。同一256句chrF++为43.67→44.14（差值95%区间−0.97至+1.89），BLEU19.66→19.60；统一审核口径后的G=8已确认正确候选覆盖13/64→18/64（净增5，配对区间0至10条），greedy18/80→20/80。技术长句G=8仅0/24→1/24，greedy仍0/20。U表示无法确认，不能当成错误；这些是AI辅助审核，未获母语专家认证。

拟合诊断表明并非完全没有学习：所选模型已见128句的NLL从0.928降至0.828，开发集NLL从1.131降至1.080。但16条已知训练样本的greedy语义通过数仍是7/16，4条技术长句均未通过。对这4条参考译文的关键错误点检查发现，参考中包含正确的脱发、共同起源、作者/表演者及边境转运术语，生成端却仍译错。这4条在本轮所选训练前缀中均实际曝光1–2次，其中1条是相对P14调度的新样本；不是只把父模型见过误称为本轮已训练。但1–2次曝光并不证明已经充分收敛。因此至少这些例子包含“已暴露但未掌握正确生成”的问题，不能单独归咎于未见数据的泛化；这也不是对整个训练池噪声率的估计。

本次只检验了冻结3B基座、rank16 LoRA、当前数据/顺序/学习率的续训配方。它不能证明达到3B模型容量或全部SFT方法的上限，也不能把残留数据问题、术语监督、曝光深度与可更新参数范围的影响逐一分离。继续相同配方加时的综合收益缺乏充分证据；同样不能断言未来SFT完全无效。

已按训练期间开发集的操作性语义条件早停，保留开发集选出的200万目标token版本及原P14。最终更大的候选审核显示有限增益，不改写当时的停止依据，也不用于事后换选检查点。目前应把P15作为“较有希望、但技术长句仍弱的候选基线”保留，不能宣布已得到综合很强的正式效率对照R0。后续若继续补强，需先提高已见技术长句的有效训练深度，并检查学习率与可更新参数配方；用关键术语/论元的实际生成保真度检验是否学会，再投入长时间扩大训练。受限DAPO试验仍可能进行，但需要独立通过奖励排序校准；本轮没有验证DAPO效果，没有普遍chrF++或正确候选数量的硬门槛。

The continuation shows local learning and increased candidate coverage, without evidence of a large overall quality gain. On the same 256 sources, chrF++ changes from 43.67→44.14 (delta 95% interval −0.97to +1.89) and BLEU 19.66→19.60. After symmetric annotation-consistency correction, confirmed G=8 coverage is 13/64→18/64 (net +5 sources; paired interval 0 to 10), and greedy fidelity 18/80→20/80. Long technical G=8 coverage is only 0/24→1/24, with greedy 0/20 in both times. U denotes genuine uncertainty, not failure. Reviews are AI-assisted, not native-certified.

Learning is occurring: NLL on 128 known-seen sources falls from 0.928→0.828 and development NLL from 1.131→1.080. Yet confirmed greedy fidelity on 16 known-seen cases remains 7/16, including 0/4 long cases. A spot-check of those four references finds the critical correct hair-loss, shared-origin, author/performer and border-transhipment terms, while generation still mistranslates them. All four were actually exposed one or two times in the selected P15 prefix, including one new relative to the P14 schedule. This is not merely inherited parent exposure; one or two passes do not establish convergence. At least these cases therefore exhibit exposure without correct generated mastery, rather than an exclusively unseen-data generalisation problem. This is not a pool-wide noise estimate.

The experiment tests this frozen 3B base, rank 16 LoRA, data, order and learning-rate continuation recipe. It does not establish a 3B capacity ceiling or the limit of all SFT methods, and does not isolate residual data issues, terminology supervision, exposure depth and trainable-parameter capacity. Large benefits from more hours of the unchanged recipe are not demonstrated; universal SFT ineffectiveness is not demonstrated either.

Training stopped under the documented development-only operational semantic gate. The 2M-target checkpoint was selected on development data and the parent remains preserved. The larger final audit reveals limited gains without retroactively changing selection or the recorded stopping rationale. Preserve P15 as a promising candidate with weak long-technical translation, rather than claiming a strong comprehensive R0 for formal efficiency comparisons. Further substantial training should first address effective training depth on known-seen long texts, the learning rate and trainable-parameter recipe. Verify generated key-term/argument fidelity before scaling training time. A restricted DAPO pilot may remain possible after independent reward-ranking calibration. No DAPO effect was tested here, and there is no universal chrF++ or correct-candidate-count admission threshold.

## 本地与持久化 / Local use and persistence

所有模型运算均在Colab。本地仅后台低优先级控制；上传已结束，后续单线程下载限至512KiB/s；无本地GPU、无浏览器前台操作、无电源设置修改。仍有少量CPU/RAM/磁盘和网络占用。正式评估检查点均校验保存，冗余100步临时恢复点不全部下载。 / Model computation is on Colab. Local work is lightweight background control and one-worker downloads capped at512KiB/s, with no GPU use or power changes. Every formal evaluation checkpoint is retained; redundant scratch recoveries are not all downloaded.

云端独立硬截止守护已安装。本地休眠可中断同步，未同步的临时检查点不保证持久化；保留的P14与已验证D盘检查点仍可用。 / The cloud deadline guard is independent, but unsynced temporary checkpoints are not guaranteed durable if local synchronization stops.

## 复现文件 / Reproduction files

- Protocol/source: D:\deep learning project\experiments\r0_3b_coverage_sft_2026-11-20\source
- Logs/checkpoints: D:\deep learning project\runs\r0_3b_coverage_sft_2026-11-20
- Reviews: D:\deep learning project\experiments\r0_3b_coverage_sft_2026-11-20\development_review
- Reports: D:\deep learning project\reports\r0_3b_coverage_sft_2026-11-20

source_bundle.zip为原冻结包；训练前长度配比修订另存coverage_amendment.zip，保留原与实际执行清单。恢复必须使用匹配的优化器、数据顺序、RNG、协议和完整检查点，不能仅据最后一行日志重启。 / The initial source bundle and pretraining amendment are both preserved. Exact recovery requires matching optimizer, order, RNG, protocol and a full checkpoint.

AI语义审核不等同于冰岛语母语专家认证。本轮没有DAPO更新，也没有MetricX调用。 / AI review is not native-expert certification. No DAPO updates or MetricX calls in this round.

## 开发集逐条语义审核 / Development semantic audit

## 开发集分数与语义覆盖 / Development scores and confirmed semantics

![开发集分数与语义覆盖 / Development scores and confirmed semantics](<D:/deep learning project/reports/r0_3b_coverage_sft_2026-11-20/development_scores_and_semantics.png>)


## 同条件最终比较 / Matched anchor comparison

![同条件最终比较 / Matched anchor comparison](<D:/deep learning project/reports/r0_3b_coverage_sft_2026-11-20/matched_anchor_quality_and_coverage.png>)


<details><summary>A · G8 · p13official21:dev:eso:491 · U</summary>

**Source:** ALMA can observe in different frequency bands.
**Semantic decision:** U — Candidate0 mentions observing between different frequencies but omits/changes band relation; remaining candidates clearly corrupt it. Cannot confirm full correctness.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** ALMA getur athugað á milli mismunandi tíðni.
**Candidate 1:** ALMA getur fylgst með framkallargreindum að skugga sem eru í mismunandi fjölbreyttingarbundnum geimsjónum.
**Candidate 2:** ALMA getur fylgst með öðrum frumunarhliðum.
**Candidate 3:** ALMA getur fylgst með segðu upp hægða fyrir tilgreiningu.
**Candidate 4:** ALMA má fara beina í mismunandi framsöfnum.
**Candidate 5:** ALMA getur mælt í mismunandi fjölda ár.
**Candidate 6:** ALMA getur fylgt eftir á milli varir í samhliða öryggismæli.
**Candidate 7:** ALMA getur fylgst með tjörnunum á mismunandi fyrningum.

</details>

<details><summary>A · greedy · p13official21:dev:opensubtitles:996 · P</summary>

**Source:** What kind of man would that make me?
**Semantic decision:** P — Exact source/hypothesis semantic reuse from card127: What kind of man would that make me retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Hvers konar maður myndi það gera mig?

</details>

<details><summary>A · G8 · p13official21:dev:eso:775 · F</summary>

**Source:** A team of astronomers, led by Istvan Dékány of the Pontificia Universidad Católica de Chile, has now used data from this survey, taken between 2010 and 2014, to make a remarkable discovery - a previously unknown component of our home galaxy, the Milky Way.
**Semantic decision:** F — All candidates corrupt discovery/component/MilkyWay or leading/survey relation; none preserves the whole claim.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Hópur stjörnufræðinga, lögð undir Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notuð gögnum frá þessari yfirríki, sem komu frá 2010 til 2014, til stuttu uppgötvunar - hinn fyrir sig óþekkti hlutur við sjóðinni Vetrarbraut.
**Candidate 1:** Hópur stjarnvísindamanna, hjá stjörnufræðingum Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notuð gögnum af þessari rannsókn, sem gerðar voru á bilinu 2010 til 2014, til bæði innánlega vörusöfnun og bæði til bæði sérhæfis uppgöngu í heimsstjörnu okkar, Galldrekkjunni.
**Candidate 2:** Hópur stjörnufræðinga, gefnu félagi Istvan Dékány hjá Pontificia Universidad Católica de Chile, hefur nýlega notið gögnum úr þessari rannsókn, sem gerð var á bilinu 2010 til 2014, til sérstakrar uppgötvunar - aðgang að sér, sem var ekki tilgreint áður, að borginni vetrarbraut, Vetrarbrautinni.
**Candidate 3:** Hópur stjörnufræðinga, leitt frá Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nýlega notað gögnum úr þessum mælingum, sem gerðar voru á bilinu 2010 til 2014 til að gera mikilvægi upplýsingu - nýtt eining af heimilinu vetrarbrautarinnar, Vetrarbrautinu.
**Candidate 4:** Hópur stjörnufræðinga, yfirhugaður Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notað gögn úr þessari rannsókn, sem gerður var á tímabilið 2010-2014, til að ná til mikiðar uppáhaldsins - einn áletrunarmiði víðtæku Vetrarbrautarinnar.
**Candidate 5:** Hópur stjörnufræðinga, leitur eftir Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur notuð gögn úr slíku losunar, sem gerðar voru á bilinu 2010-2014, til að koma að frábendingi sem við höfum ekki sést áður - aðrar hluti um heimaliku svæðisins, Vetrarbrautar.
**Candidate 6:** Hópur stjörnufræðinga, gefinn um stjörnustarfsemi af István Dékány, Pontificia Universidad Católica de Chile, hefur nýlega notað gögn úr þessu skoðun, sem tekin voru á bilinu 2010-2014, til þess að ná undir mikill uppgötvun - aðgang til þess fyrirleitt þols sem er á móti viðfundi.
**Candidate 7:** Hópur stjörnufræðinga, leitt af István Dékány við Pontificia Universidad Católica de Chile, hefur nú notuð niðurstöður úr mælikvarðanum, sem tókjast milli 2010 og 2014, til að gera ósæmu uppgötvun - aðra, fyrir hliðsjónu, hlutu vetrarbrautarnar okkar.

</details>

<details><summary>A · G8 · p13official21:dev:ema:767 · U</summary>

**Source:** Therefore, docetaxel must not be used during pregnancy unless clearly indicated.
**Semantic decision:** U — Drug/pregnancy prohibition preserved in several, but clearly-indicated exception is ambiguous; candidate7 indication wording is closest but not confidently correct.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Því má ekki nota docetaxel á meðgöngu nema ákvarðanir séu klárar.
**Candidate 1:** Því má ekki nota docetaxel á meðgöngu nema sprauta sé tilkynnt á tæka hátt.
**Candidate 2:** Því má ekki nota doketaxel á meðgöngu nema tilkynnt sé greinilega til þess.
**Candidate 3:** Því má ekki nota docetaxel á meðgöngu nema greinilega áður sé til.
**Candidate 4:** Því má ekki nota docetaxel á meðgöngu nema greinilega megi gefa það.
**Candidate 5:** Því verður ekki að nota docetaxel á meðgöngu nema brýna markmiði sé fylgt.
**Candidate 6:** Því má ekki nota dócetaxel á meðgöngu nema greinilega fylgjast með því.
**Candidate 7:** Því má ekki nota dócetaxel á meðgöngu nema algjörlegar ábendingar fylgi.

</details>

<details><summary>A · greedy · p13official21:dev:ema:704 · F</summary>

**Source:** The most frequently reported adverse reaction was acne, which was generally mild.
**Semantic decision:** F — Acne is replaced by kúu; the named adverse reaction is not preserved.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Algengasta aukaverkunin sem greint var frá var kúu, sem var yfirleitt væg.

</details>

<details><summary>A · G8 · p13official21:dev:ema:1394 · F</summary>

**Source:** The most commonly reported adverse reactions (≥ 20%) among patients treated with both belatacept- based regimens (MI and LI) up to Year 3 are diarrhoea, anaemia, urinary tract infection, peripheral oedema, constipation, hypertension, pyrexia, nausea, graft dysfunction, cough, vomiting, leukopenia, hypophosphataemia, and headache.
**Semantic decision:** F — Every candidate changes several named adverse reactions, including graft dysfunction, peripheral oedema, leukopenia or hypophosphataemia.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Algengustu aukaverkanirnar sem greint hefur verið frá (≥ 20%) hjá sjúklingum sem fengu bæði belatacept-bundna meðferðir (MI- og LI-) allt til ári 3 eru niðurgangur, blóðleysi, bakterýatrygging í þvagmálum, bólgu í burtíkjum, lálægða, háþrýstingur, hiti, ógleði, grunnvirkjunarskerðingar, hósti, uppköst, hvítblöðrufæð, lágkornamyndun, ofkornamyndun og höfuðverkur.
**Candidate 1:** Algengustu aukaverkanirnar sem greinst eru hjá sjúklingum sem fá bæði meðferð með belatacepti (MI) og meðferð með belatacepti í samsettri meðferð (LI) og eru fjöldi þess í algeru árinu 3 (≥ 20%) eru niðurgangur, blóðleysi, sýking í þvagvegasjónar, þynnu, trægð, háþrýstingur, hiti, ógleði, vansköpun æða, hósti, uppköst, blóðflagnafæð, blóðfosfatslækkun og höfuðverkur.
**Candidate 2:** Yfirleitt tilkynntar aukaverkanir (≥ 20%) hjá sjúklingum sem fá bæði reglan með belatacept (MI- og LI) allt að 3 árs, eru niðurgangur, blóðleysi, sýking í þvagvegnum, bólgu í hluta af kviði, hægðatregða, háþrýstingur, hiti, uppköst, stofnunarbilun á græðslu, hósta, uppköst, hvítblóðfall, jafngildisblóðfalls, og höfuðverkur.
**Candidate 3:** Algengustu aukaverkanirnar sem fram koma (≥ 20%) hjá sjúklingum sem fá bæði meðferð með belatacept-bundnum meðferðum (MI og LI) til ára 3 eru niðurgangur, blóðleysi, kveikjun í þvagvegin, bólga í utan blóðvegar, truflun í geymslu, háþrýstingur, hiti, ógleði, ónæmingur, hósti, uppköst, blóðleysi, blóðsólarhægðatap, og höfuðverkur.
**Candidate 4:** Algengustu aukaverkanirnar sem fram komu hjá sjúklingum sem fengu bæði reglur sem byggðar voru á belatacepti (MI og LI) til árs 3 (≥ 20%) eru niðurgangur, blóðleysi, sýking í þvagmyndun, þyngdar bólga í útlöndum, trægæði, háþrýstingur, hiti, ógleði, skerta vegna stofnun, hósti, uppköst, blóðflagnafæð, blóðódsýraskort og höfuðverkur.
**Candidate 5:** Algengustu aukaverkanirnar sem greint var frá (≥20%) hjá sjúklingum sem fengu bæði meðferð með belataceptu-bundnum meðferðaráætlunum (MI og LI) fram í 3. ári eru niðurgangi, blóðleysi, ofnæmisbólga í niðurbolti, hvíldrofi í kringum taugahlaup, tráháðir þyngdarleysi, háþrýstingur, hiti, ógleði, skertferli í græðli, hósta, uppköst, blóðfall, blóðfosfatófsvildi, og höfuðverkur.
**Candidate 6:** Algengustu aukaverkanirnar (≥ 20%) sem greindust hjá sjúklingum sem fengu bæði belatacept-bundna meðferð (MI og LI) allt að ári 3 eru niðurgangur, blóðleysi, nýrnasjúkdóm í nýrnaræði, bólga í ljósi, trægðleysi, háþrýstingur, hiti, ógleði, vanskuldaður nýrna, hósti, uppköst, blóðflagnafæð, blóðfosfatsþéttni lág og höfuðverkur.
**Candidate 7:** Algengustu aukaverkanirnar sem greindust hjá sjúklingum sem fengu meðferð með bæði belatacept-bundið meðferð (MI og LI) allt að 3 árs (≥ 20%) eru niðurgangi, blóðleysi, sýking í þvagrann, bólga í umhverfi, hægðatregða, háþrýstingur, hiti, uppköst, truflun í veirum, hósti, uppköst, blóðflagnafæð, blóðfosfatarmilti og höfuðverkur.

</details>

<details><summary>A · greedy · p13official21:dev:eso:919 · F</summary>

**Source:** "Thanks to several giant telescopes currently under construction, including ESOs E-ELT and the NASA/ESA/CSA James Webb Space Telescope due to launch for 2018, we will soon be able to study the atmospheric composition of these planets and to explore them first for water, then for traces of biological activity.
**Semantic decision:** F — Opening construction/launch and atmospheric-composition clauses are corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** „Takinn hefur nokkrar stóra sjónaukar sem eru í framhaldshús, þar með talið ESOs E-ELT og James Webb Space Telescope NASA/ESA/CSA sem er til að fara í reynd árið 2018, munum við náið nánar á geimkemmdi þessara planeta og rannsaka þær fyrst með vatni, síðan með einkennum líffræðilegra virkni.

</details>

<details><summary>A · greedy · p13official21:dev:eso:491 · F</summary>

**Source:** ALMA can observe in different frequency bands.
**Semantic decision:** F — Frequency bands becomes concerts/different numbers of bands.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** ALMA getur fylgst með tónleikum á mismunandi fjölda banda.

</details>

<details><summary>A · greedy · p13official21:dev:opensubtitles:480 · U</summary>

**Source:** Now we have enough evidence to charge you with murder.
**Semantic decision:** U — Evidence/murder retained; skrá fyrir does not confidently establish the intended charge-with relation.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Nú hafa við nægilega sönnunargögn til að skrá þig fyrir morði.

</details>

<details><summary>A · greedy · p13official21:dev:opensubtitles:1169 · P</summary>

**Source:** They're pretty as can be, aren't they?
**Semantic decision:** P — Pretty/cute and the confirmation question retained; inflection is imperfect.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Þau eru mjög sætir, ekki satt?

</details>

<details><summary>A · greedy · p13official21:dev:eea:1716 · F</summary>

**Source:** The competent authorities of Gabon have reacted promptly to these concerns, indicating their commitment to take all measures necessary to implement applicable ICAO standards and enforce compliance with these standards as soon as possible.
**Semantic decision:** F — Enforcing compliance with ICAO standards becomes following reactions.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Lögbær yfirvöld í Gabón hafa svarað þessum ábendingum tafarlaust og benda til þess að þau séu bundnar til að gera allar nauðsynlegar ráðstafanir til að framfylgja gildandi staðli ICAO og fylgja þeim viðbrögðum eins fljótt og unnt er.

</details>

<details><summary>A · greedy · p13official21:dev:eso:924 · F</summary>

**Source:** ESO was delighted to welcome Italys Minister of Education, Universities and Research, H.E. Stefania Giannini, to the ceremony, which was also attended by the Italian Consul General in Munich, Renato Cianfarani, the ESO Council President, Patrick Roche, and the Italian ESO Council Delegates, Nicolò DAmico (who is also President of INAF) and Matteo Pardo, Scientific Attaché at the Italian Embassy in Berlin.
**Semantic decision:** F — Ministerial position, countries, event attendance and named roles are extensively corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** ESO var ánægð af því að viðtaka Stefania Giannini, íslandsskonar menntamaður yfir höndir, í sérstökum sérhæfis, sem var einnig áttur í sérstökum sérhæfis í Ítalíu, Renato Cianfarani, forseta- og stjórnmann ESO, Patrick Roche, og tilskipunaraðilar ESO frá Ítalíu, Nicolò DAmico (sem er líka forseta- og stjórnmann INAF) og Matteo Pardo, vísindamennsögusamþykki í Ítalíu.

</details>

<details><summary>A · greedy · p13official21:dev:eso:768 · U</summary>

**Source:** Both components are classed as O-type stars.
**Semantic decision:** U — Both objects classified as O stars is recognizable, but component is rendered ingredient and the technical relation is uncertain.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Bæði innihaldsefnið er flokkt sem O- stjörnur.

</details>

<details><summary>A · G8 · p13official21:dev:eea:1585 · P</summary>

**Source:** The Commission shall submit a final evaluation report at the end of the Programme.
**Semantic decision:** P — Candidates0/2/5 retain Commission submitting final evaluation report at programme end.
**Inspected / Correct indices:** [0, 1, 2, 3, 5, 6, 7] / [0, 2, 5]
**Candidate 0:** Framkvæmdastjórnin skal leggja fram endanleg matsskýrslu að lokum áætlunarinnar.
**Candidate 1:** Framkvæmdastjórnin skal leggja fram endanleg mataráðgerð eftir að áætlunin er lokið.
**Candidate 2:** Framkvæmdastjórnin skal leggja fram endanlega matsskýrslu eftir að áætlunin er lokið.
**Candidate 3:** Framkvæmdastjórnin skal leggja fram endanlega matsskil á lokum áætluninnar.
**Candidate 5:** Framkvæmdastjórnin skal leggja fram endanlega matsskýrslu eftir áætlunin er lokið.
**Candidate 6:** Framkvæmdastjórnin skal leggja fram endanlega ávísað skýrslu að lokum áætlunarinnar.
**Candidate 7:** Framkvæmdastjórnin skal leggja fram endanlegar matarannsóknarskýrslu eftir lok áætlunarinnar.

</details>

<details><summary>A · greedy · p13official21:dev:eea:281 · F</summary>

**Source:** The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.
**Semantic decision:** F — Maturity band, former/latter relation and residual position are mistranslated.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Hlutfall fyrri (sáttmálans) sem samsvarar sáttamálum sínum í tilteknu vinnuþætti skal vera samsvarandi stöður í þeirri vinnuþætti, en hlutabúnaður á lengi eða stuttu tíma skal vera ósamsvarandi stöður í sama vinnuþætti.

</details>

<details><summary>A · greedy · p13official21:dev:eea:1552 · F</summary>

**Source:** The analytical result shall be reported as x +/– U whereby x is the analytical result and U is the expanded measurement uncertainty, using a coverage factor of 2 which gives a level of confidence of approximately 95 % (U = 2u).
**Semantic decision:** F — Expanded measurement uncertainty and coverage/confidence concepts are corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Greina skal niðurstöður greiningar sem x +/– U þar sem x er niðurstöður greiningar og U er útþekktur málstöfunartími, með því að nota 2 gildi fyrir umfrymisstig sem gefur umframvísitengingu um 95% (U = 2u).

</details>

<details><summary>A · G8 · p13official21:dev:ema:1582 · P</summary>

**Source:** The treatment-free period, however, should take into account the pharmacological properties of the products used previously.
**Semantic decision:** P — Candidate6 conveys period without treatment and consideration of pharmacological properties of previously used drugs despite rough case/word order.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [6]
**Candidate 0:** Meðan á meðferðarfrasluminni stendur skal íhuga lyfjafræðilega eiginleika lyfju sem notað er áður.
**Candidate 1:** Meðferðarframanstundin skal þó taka tillit til lyfjafræðilegra eiginleikanna tilneyttu lyfja.
**Candidate 2:** Meðferðarframtíminn skal þó taka tillit til lyfjafræðilegra eiginleika lyfja sem notaðir hafa verið áður.
**Candidate 3:** Meðferðarfjöldaði skal þó hafa í huga lyfjafræðileg eiginleikar lyfjanna sem notaðir hafa verið áður.
**Candidate 4:** Meðferðarframanum skal því athugasemdir til hvað varðar lyfjafræðilega eiginleikar lyfinna sem notaðir voru áður.
**Candidate 5:** Meðferðarframsýni þótt skal íhuga lyfjamengun lyfja sem notaðir voru áður.
**Candidate 6:** Meðan án meðferðar tímann skal hafa í huga lyfjafræðileg eiginleikar lyfjanna sem notað voru áður.
**Candidate 7:** Meðferðarfraslengdinni skal þó íhuga lyfjafræðilegar eiginleikar lyfinna sem notuð hefur verið áður.

</details>

<details><summary>A · G8 · p13official21:dev:eso:206 · F</summary>

**Source:** The survey was sensitive to planets between 75 million kilometres and 1.5 billion kilometres from their stars (in the Solar System this range would include all the planets from Venus to Saturn) and with masses ranging from five times the Earth up to ten times Jupiter.
**Semantic decision:** F — All candidates corrupt billion scale and/or mass bounds and objects.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Skoðunin hefur verið sérfræðilega til stjörnum á milli 75 milljón km og 1,5 milljón km frá stjörnunum (í Jörðavetrarbrautinni umfarið allar stjörnurinnar frá Vensu yfir í Saturn) með massamagni á bilinu frá fimm sinnum jörðunum til tíu sinnum Júpíturnum.
**Candidate 1:** Skýrslan var næmur fyrir plöntum á bilinu 75 milljón km til 1,5 milljón milljón km frá stjörnunum (í sólkerfinu birta allar plönturnar frá Venus til Saturn) og massaverk fyrir allar plönturnar var á bilinu fyrir fimm sinnum jörðina upp á tíu sinnum Júpíturni.
**Candidate 2:** Skoðunin var næmur til reikistjarna milli 75 milljón km og 1,5 milljón km frá stjörnunum (í sólarkerfinu fingi hún öll reikistjörnurnar frá Venus til Saturns) og massahófur sem fengur var fyrir sig fimm sinnum gildi Bergsins og títtinga í tíu sinnum gildi Júpítrs.
**Candidate 3:** Til greiningar var næm við reikistjörnur sem eru á bilinu 75 milljón km til 1,5 milljón km frá stjörnunum (í sólkerfinu catches tilvísunin við öll reikistjörnurnar frá Venus til Saturn) og massakvörðun var á bilinu fimm sinnum jörði til tennum Júpítr.
**Candidate 4:** Skoðuninni var næm við reikistjörnur sem eru á bilinu 75 milljón km til 1,5 milljón króna frá stjörnunum (í sólarbrautinni í þessa bil er allan reikistjörnin frá Venus til Saturn) og með þyngd á bilinu fyrir fjögurra gildi jörðar til tíu gildum Júpítra.
**Candidate 5:** Skoðanirnar höfðu nákvæmni við reikistjörnu sem eru á milli 75 milljón km og 1,5 milljón km frá stjörnunum (í Jörðareikjunni gætu nar einnig reikistjörnin af Venus til Saturn) og eru með massa á milli fimm sinna jörða og tíu jörða.
**Candidate 6:** Rannsóknin var nægileg fyrir reikistjörnur á bilinu 75 milljón kílómetra og 1,5 milljón milljón kílómetra frá stjörnunum (í sólarráðinu nefnar allar reikistjörnurnar frá Vensu til Saturn) og með massar á bilinu frá fimm sinnum þjóðinu í Júpíturnum til upp í tíu sinnum.
**Candidate 7:** Skoðunin var meðvæn fyrir reikistjörnur á bilinu 75 milljón km til 1,5 milljón km frá stjörnunum (ég hafi í sólkerfinu fengið allar reikistjörnurnar frá Vensu til Sáterni), með vettvangi úr fimm til tíu gildum jörðu.

</details>

<details><summary>A · greedy · p13official21:dev:eea:1194 · F</summary>

**Source:** It should provide the Commission and the Member States with objective, reliable and comparable information and data on maritime safety and on ship pollution prevention to enable them to take any necessary initiatives to enhance the measures in place and to evaluate their effectiveness.
**Semantic decision:** F — Objective/reliable/comparable information and ship-pollution-prevention concepts are corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Hún skal veita framkvæmdastjórninni og aðildarríkjunum vísanir og upplýsingar sem eru áframhaldandi, öruggar og jafngiltar um öryggi á sjávarbærum og um að forðast losun í skipum til þess að hún geti tekið nauðsynlegar aðgerðir til að auka ráðstafanir sem eru í gildi og meti árangur þeirra.

</details>

<details><summary>A · greedy · p13official21:dev:eso:464 · U</summary>

**Source:** With an estimated mass of four to five times that of Jupiter, it would be the least massive planet to be directly observed outside the Solar System.
**Semantic decision:** U — Mass comparison and observation claim mostly recognizable, but invented mass/superlative wording prevents confident confirmation.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Ef það er með fjögur til fimm sinnum stærri massafjölda en Júpíter væri það minnst massaverulegur reikistjarnan sem hefur verið tekið beinu sjón af utan sólkerfinu.

</details>

<details><summary>A · G8 · p13official21:dev:ema:1406 · F</summary>

**Source:** Concomitant use with yellow fever vaccine and with live virus and bacterial vaccines (see section 4.5).
**Semantic decision:** F — None preserves yellow-fever vaccine and the entire concomitant vaccine-use list.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Rannsókn með geislunir á bóluefnum gegn gulþjálfandi eitilvöxti og lifandi veiru- og bakteríu+bóluefnum (sjá kafla 4.5).
**Candidate 1:** Samhliða notkun með llúpurfíkninu og lifandi veiru- og bakteríufíkninu (sjá kafla 4.5).
**Candidate 2:** Samhliða meðferð með brúðu-æxlisbóluefni og með lifandi veiru- og bakteríubóluefni (sjá kafla 4.5).
**Candidate 3:** Samhliða notkun með fasafræðiseftirlyfjum og lifandi veiru- og bakteríufyrirbyggjandi bóluefnum (sjá kafla 4.5).
**Candidate 4:** Samhliða notkun á geislalyfsfleiri og lifandi veiru- og bakteríuhvata (sjá kafla 4.5).
**Candidate 5:** Samhliða notkun millivefja fyrir gulvind og lifandi veirusjúkdóm og bakteríusjúkdóm (sjá kafla 4.5).
**Candidate 6:** Samhliða notkun gegnsæðis gegn gultsótt og lifandi veirus- og bakteríusótt (sjá kafla 4.5).
**Candidate 7:** Notkun samhliða eitlafræðisefna og lifandi veirusjónum og sýklum, fyrir lifur (sjá kafla 4.5).

</details>

<details><summary>A · G8 · p13official21:dev:eea:922 · P</summary>

**Source:** Development of CPE is checked as described in Part I.III.4.
**Semantic decision:** P — Candidate0 retains checking development of CPE and the I.III.4 cross-reference; duplicated preposition only.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [0]
**Candidate 0:** Tilvik um þróun CPE er rannsakað eins og lýst er í í I.III.4.
**Candidate 1:** Rannsókn á þróun CPE er farið fram samkvæmt grein 4 í III.4. I.h.
**Candidate 2:** Frekari þroska CPE er lokið eftir þeirri rök sem lýst er í IV. 4. hlið I. hliðar III. þáttar.
**Candidate 3:** Fylgjar er eftirliti með þróun CPE eins og lýst er í 4. horn I. III. þáttar.
**Candidate 4:** Framdæmi CPE (continuing parental education) er rannsakað eins og lýst er í III.4. hlið í I. hluta greinar.
**Candidate 5:** Meðhöndlun á þróun á CPE er gerð samkvæmt grein 4 í III.4. bönd I. hliðar.
**Candidate 6:** Skoðað er þróun CPE eins og lýst er í III.4. hloð I. lyklans.
**Candidate 7:** Verið er viss um þróun CPE eins og lýst er í I.III.4.

</details>

<details><summary>A · G8 · p13official21:dev:eea:609 · U</summary>

**Source:** Special payments for shift work.
**Semantic decision:** U — Payments retained in several; shift-work wording is nonstandard and cannot confidently confirm a fully correct candidate.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 6, 7] / []
**Candidate 0:** Sérstök greiðslur við skiptatíma.
**Candidate 1:** Sérstök greiðslur fyrir skiptaríki.
**Candidate 2:** Sérstakt greiðslur í starfsmeðaltali.
**Candidate 3:** Sérstök borgun vegna skipti í vinnu.
**Candidate 4:** Sérstök greiðslur fyrir starfsstöðum.
**Candidate 6:** Sérstakar greiðslur fyrir stöðugir verk.
**Candidate 7:** Sérstakar greiðslur fyrir skipta verki.

</details>

<details><summary>A · greedy · p13official21:dev:opensubtitles:3607 · F</summary>

**Source:** Well, that makes you ugly and stupid.
**Semantic decision:** F — Ugly becomes strange; singular you also changes.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Jæja, það gerir ykkur skríti og heimskur.

</details>

<details><summary>A · G8 · p13official21:dev:eea:698 · F</summary>

**Source:** Only days that can be worked should be included when Saturdays and Sundays are not worked they should not be included, the same with public holidays).
**Semantic decision:** F — All corrupt Saturday/Sunday or their conditional exclusion; generic non-working-day paraphrase omits the specified days.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Aðeins dagar sem má vinna skal taka til þeirra þegar ekki er tekið á sásterumog sunnudagum (sama með opinbera fríum).
**Candidate 1:** Einungis daga sem má vinna á skaltu taka inn þegar riddarogur og laugardagur eru ekki vinna á, þegar ekki maga skal taka í skrá borgardagsdögum (public holiday).
**Candidate 2:** Aðeins daga sem má vinnast eiga aukið þegar Söndag og sunnudagur koma ekki í vinnuna. Sama má við borgarkennidayggi).
**Candidate 3:** Einnig skal taka til eitt fyrir hvern dag sem er hægt að vinna þegar ekki er að vinna á sólarhringum og sólarhringardagum, sama skal fyrir opinbera frídagana.).
**Candidate 4:** Einungis skal taka til daga sem má vinna og ekki einu sinni dögum sem ekki ræði að vinna skal ekki taka til þeirra, svo og opinbera frídaga).
**Candidate 5:** Einnig skal taka bara dagirnar sem auðvelda að starfræði, þegar sjónda og sólarhringar eru ekki starfræði skal ekki taka það, samt í opinbera fríar).
**Candidate 6:** Einungis daga sem geta verið virkt skulu fylgt saman þegar Söndagur og sunnudagar eru ekki virkt eða einnig að sama máli berast lausnardagur í opinbersamfélagi.
**Candidate 7:** Aðeins daga sem eru hægt að vinna eiga að skrá inn þegar sár og sunnudagar eru ekki vinna eiga ekki að skrá þau inn, sama við opinbera helgana).

</details>

<details><summary>A · greedy · p13official21:dev:eea:50 · F</summary>

**Source:** Similar studies, for at least three soil types, must be reported for all relevant metabolites, degrada tion and reaction products which in soil degradation studies account at any time for more than 10 % of the amount of active substance added.
**Semantic decision:** F — Soil types and degradation/reaction products are corrupted, with the at-any-time qualifier missing.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Tilkynna verður um svipaðar rannsóknir á að minnsta kosti þremur grunnfærum fyrir öll viðeigandi umbrotsefni, umbrot og framleiðsluefni sem í rannsóknum á umbrotnun grunnfæra gefa stærri en 10% af skömmtum virka efna sem bætt er við.

</details>

<details><summary>A · greedy · p13official21:dev:opensubtitles:1012 · P</summary>

**Source:** I'll do whatever you ask.
**Semantic decision:** P — Promise to do whatever is asked retained despite tense/inflection.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Ég geri hvað sem þú baðir.

</details>

<details><summary>A · G8 · p13official21:dev:ema:1718 · P</summary>

**Source:** Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.
**Semantic decision:** P — Candidate6 retains co-administration, P-gp inducer, decreased mean AUC, shortened half-life and possible reduced pharmacodynamic effects.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [6]
**Candidate 0:** Samhliða lyfjagjöf edoxaban og P-gp hvötarefnisins rífampicins leiddi til minnkaðs meðaltals AUC fyrir edoxaban og skemmings helmingunartíma, sem gæti hægt að lækka lyfhrifum þess.
**Candidate 1:** Samhliða lyfjagjöf edoxaban og P-gp örvaðs rifampicins leiddi til minnkaðrar meðal AUC fyrir edoxaban og skerta helmingunartíma, sem geta áttað minnkuð lyfhrif.
**Candidate 2:** Samtímis gjöf edoxabans og P-gp örva, rifampicins, leiddi til minnkar á meðal AUC fyrir edoxaban og minnkaðs helmingunartíma, sem gæti skerðað lyfhrifum.
**Candidate 3:** Samhliða lyfjagjöf edoxabans og P-gp örva rifampicins leiddi til minnkaðs AUC fyrir edoxaban og minnkaðs helmingunarsíðu, sem hugsanlega leikur á að færi lyfhrifum eins.
**Candidate 4:** Samhliða lyfjagjöf edoxabans og P-gp örva (rifampicins) leiddi til minnkaðs meðal AUC fyrir edoxaban og skerðingar helmingunartíma, sem gæti haft mögulega áhrif á lyfhrif.
**Candidate 5:** Samhliða lyfjagjöf edoxabans og P-gp örvaðar rifampicins leiddi til minnkunar á meðal AUC fyrir edoxaban og skerðingar á helmingunartíma, í tengslum við hugsanlega minnkun á lyfhrifum.
**Candidate 6:** Samtímis gjöf edoxaban með P-gp örva rifampicini leiddi til minnkaðs á meðal AUC fyrir edoxaban og styttingar á helmingunartíma, sem hugsanlega leiddi til minnkaðs lyfhrifins.
**Candidate 7:** Samhliða lyfjagjöf edoxabans og P-gp örva rífampicins leiddi til minnkaðs meðaltals AUC fyrir edoxaban og styttrar helmingunartíma, sem geta orðið minnkað lyfhrifinn.

</details>

<details><summary>A · greedy · p13official21:dev:eea:1216 · F</summary>

**Source:** That task shall be coordinated with the existing regional cooperation programmes and shall include, where appropriate, the organisation of relevant training activities.
**Semantic decision:** F — Existing regional cooperation programmes becomes research programmes at community level.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Það verkefni skal samræma við tilstaðar rannsóknaráætlunum á sviði bandalagsins og skal það innihalda, eftir því sem við á, stjórna viðeigandi þjálfunartaknum.

</details>

<details><summary>A · greedy · p13official21:dev:eea:1991 · F</summary>

**Source:** Paragraph AG27 is amended and after paragraph AG29, paragraph AG29A is added.
**Semantic decision:** F — The AG prefixes identifying the amended paragraphs are lost.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Í 27. lið er breytt og eftir 29. lið bætist við 29. lið A.

</details>

<details><summary>A · G8 · p13official21:dev:eea:281 · F</summary>

**Source:** The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.
**Semantic decision:** F — All corrupt maturity band/former-latter matching and residual long/short-position definition.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Skömmtur af því (því sem er síðasta sem), sem staðfestur fyrir síðasta (því sem er fyrsta) í tilteknu þurrðarfar, skal vera staðallir í þeirri far, sem óstaðaðir langa eða stór og lágar staðaliðið skal vera óstaðað staðaliði í sama þurrðarfar.
**Candidate 1:** Hlutfall fyrri (sári) sem fyrirbyggja sér sári (fyrri) í tilteknu útbrotserfi skal vera sári í því útbrotserfi, þar sem óbillaður lengur eða stuttur ástand ásættast í sama útbrotserfi.
**Candidate 2:** Hlutfall fyrstu (sá eftirfarandi) sem samsvarar sá eftirfarandi (fyrsti) í tiltekinni þroskaþyngd skulu vera samsvarandi staðsetningar í þessum þroskaþyngdina en hlutabúnaður til biliðar eða skuldbandið skulu vera ósamsvarandi staðsetningar í sama þroskaþyngd.
**Candidate 3:** Skammtur af þeim sem eru upptekin fyrir (síðar) af þeim sem eru upptekin fyrir (síðar) í viðkomandi ákvörðunarhópi skal vera upptekin staðan í þeim hópi, en eftirskipti langa eða skorta skal vera upptekin staðan í sama hópi.
**Candidate 4:** Magn miðla (frummið) sem samhæft er af síðari (fyrri) miðla (frummið) yfir í viðkomandi vörnaklófa skal vera samhæft staður í þeirri klófi, en ósamhæft staður yfir í sömu klófi skal vera staður yfir á milli.
**Candidate 5:** Fjöldi framskeðinnar (-fylginnar) sem samsvarar framskeðinni (-fylginni) í við ákvörðuðum blöndu skal vera samhæft stað (jaður), samanborið með því unnt er, sem samsvarandi staður, en fjölda eftirfarandi staða (eða endurstaða) á sama blöndu skal vera ósamsvarandi staður.
**Candidate 6:** Stöð fanar (látara) sem upptalta eru á meðan viðkomandi stöðvar eru í stöðu á viðkomandi stigsástanda eða stöðvar sem eru ekki upptala á viðkomandi stigsástandi skal vera staðstillar stöður í stigsástandinu, en áframhaldandi stöður sem ekki er upptala á viðkomandi stigsástandi skal vera ekki staðstillar stöður á viðkomandi stigsástandi.
**Candidate 7:** Hlutfall fyrri (sáttasamræmkaðri) eldri (sáttasamræmkaðra) er samsvarar sáttamál samsvarandi (sáttasamræmkaðri) í tilteknum meginþolarmálum skal vera samsvarandi stöður í því meginþölmum, en hlutfall eðlilega langa eða stuttar stöðu skal vera ósamræmd stöður í sambærilegum meginþölmum.

</details>

<details><summary>A · greedy · p13official21:dev:opensubtitles:1159 · F</summary>

**Source:** Somebody get me a picture of the girl.
**Semantic decision:** F — The receiver me is missing from the request to obtain a picture.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Einhver fá mynd af stúlkunni.

</details>

<details><summary>A · G8 · p13official21:dev:eso:501 · U</summary>

**Source:** The team used data from the UVES spectrograph on ESOs Very Large Telescope in Chile (to determine the properties of the star accurately), the Carnegie Planet Finder Spectrograph (PFS) at the 6.5-metre Magellan II Telescope at the Las Campanas Observatory in Chile, the HIRES spectrograph mounted on the Keck 10-metre telescope on Mauna Kea, Hawaii as well as extensive previous data from HARPS (the High Accuracy Radial velocity Planet Searcher) at ESOs 3.6-metre telescope in Chile (gathered through the M dwarf programme led by X. Bonfils and M. Mayor 2003–2010 described here).
**Semantic decision:** U — Candidate0 retains many names/numbers but instrument terminology, found-versus-used data and HARPS attribution are too uncertain for confirmed correctness. Others have clear omissions/corruption.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Hópurinn fann gögn frá UVES rannsóknartækinu sem ESO notar á Very Large Telescope í Chile (um að ákvarða eðli stjarna á nákvæmri hátt) Carnegie Planet Finder Spectrograph (PFS) á Magellan II stjörnustjörnunum sem er 6,5 metra í Las Campanas stjörnustöðinni á Chile, HIRES rannsóknartækinu á Keck 10 metra stjörnustjörnunni Mauna Kea á Hawaii og líka umfangskenndar gögn frá HARPS (HARPS radial velocity planet hunter) í 3,6 metra stjörnustjörnunni í Chile, ESO sem var framkvæmd með M dwarf stjörnumála (X. Bonfils og M. Mayor 2003-2010 sem lýst er hér) .
**Candidate 1:** Hópurinn notuðu gögn úr UVES gæðasprautunni á Very Large Telescope (VLT) ESO á Chile (til að ákvarða eiginleikar stjarnanna) Carnegie Planet Finder Spectrograph (PFS) á Magellan II sjónauki (6,5 litra) á Las Campanas stjörnustöðinni á Chile við 6,5 m stjörnustjörnuna Keck, Hawaii sem viðkomandi gæðisprautu sem stendur á 10 m stjörnustjörnu, HIRES, (Highe Accurecy Radial Veocity Planet Searcher), sem er á 3,6 m stjörnustjörnunni ESO á Chile (með M dwarf verkefninu sem leitar eftir prótaðir (lead by X. Bonfils and M. Mayor 2003-2010) sem lýst er hér, gengu í samhengi M dwarf verkefnisins).
**Candidate 2:** Hópurinn notaði gagna úr UVES litrófið ESO Very Large Telescope í Chile (að ákvarða eðlis stjarna á ákvarðanlegt hátt) Carnegie Planet Finder Spectrograph (PFS) í 6,5 m á Magellan II litrófi í Las Campanas stjörnustöðinni í Chile, HIRES litrófið sem hafi verið sett á Keck 10 m litrófið í Mauna Kea í Hawaii og líka mörg gagnir frá HARPS (High Accuracy Radial velocity Planet Searcher) litrófið í 3,6 m litrófið í Chile eftir M dwarfs úrræði X. Bonfils og M. Mayor 2003-2010 sem lýst er hér.
**Candidate 3:** Hópurinn notaði þau gögn úr UVES skýrasmiði í Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjarna), Carnegie Planet Finder Spectrograph (PFS) á 6,5- metra Magellan II sjónauka í Las Campanas stjörnustöðinni í Chile, HIRES skýrasmiðin á Keck 10- metrasetjunni í Mauna Kea á Hawaii og í aðra mælikvarða TAGAS og HARPS (The High Accuracy Radial velocity Planet Searcher) í ESO 3,6- metrasetjunni í Chile (myndast innan af M dwarf örlögum X. Bonfils og M. Mayor 2003-2010 sem lýst er hér).
**Candidate 4:** Líkamsrannsóknin varðandi stjörnu í jörðu notuð gögn úr UVES tæknifotslitinu á Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjarna á nákvæm handtak), Carnegie Planet Finder Spectrograph (PFS) í 6,5 m stjörnustjörnunni Magellan II í Las Campanas stjörnustöðinni í Chile, HIRES tæknifotslitinn á Keck 10 m stjörnustjörnunni í Mauna Kea í Hawaii, ásamt mikilvægu gögnum frá HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6 m stjörnustjörnunni í Chile (þar sem gögnin voru safnað með M dwarf prófið, sem framkvæmdastjórið var X. Bonfils og M. Mayor á tíðum 2003-2010 sem lýst er hér).
**Candidate 5:** Teiminn notaði upplýsingum úr UVES litrófsmáli ESO Very Large Telescope í Chile (til að ákvarða eiginleikar stjarnanar nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5-metrar Magellan II litskýrinu í Las Campanas stjörnustöðinni í Chile, HIRES litrófsmálið á Keck 10-metrar litskynni í Mauna Kea í Hawaii, og helvítis fyrri upplýsingum úr HARPS (High Accuracy Radial velocity Planet Searcher) í Chile (hafnað við M dwarf-æðinni X Bonfils og M Mayor 2003-2010 sem lýst er hér, og sem ljúkurðir vart gagnið úr 3,6-metrar litrófsmailli ESO í Chile).
**Candidate 6:** Hópurinn notuði upplýsingum úr UVES mælinum á Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjarnans nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5 m Magellan II mælinu í Las Campanas stjörnustöðinni í Chile, HIRES mælini á Keck 10 m litilvanslensnu í Mauna Kea í Hawaii og umfangsrikum gögnum í HARPS (High Accuracy Radial velocity Planet Searcher) í Chile (gerðirnar rannsóknar í M litilvöxtum, framkvæmdar af X. Bonfils og M. Mayor 2003-2010, sem lýst er hér).
**Candidate 7:** Hópurinn notaði gögn úr UVES litrófi á Very Large Telescope ESO í Chile (til að ákvarða eiginleikastarfsemi stjarna á nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) í Magellan II sjónaukinni í Las Campanas stjörnustöðinni í Chile (6,5 metra svarthæð), HIRES litrófið á Keck 10 metra sjónauka á Mauna Kea í Hawaii (stöðuð á sama stjörnustöð ESO í Chile, 3,6 metra svarthæði) og fyrri gögn í HARPS (High Accuracy Radial velocity Planet Searcher) sem ESO gaf í Chile (á M dwarfs verkefni X. Bonfils og M. Mayor 2003-2010 sem lýst er hér)

</details>

<details><summary>A · G8 · p13official21:dev:eea:1461 · F</summary>

**Source:** All industrial uses of gas are considered.
**Semantic decision:** F — No candidate preserves industrial uses being considered; closest5 substitutes work in general.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Í þeim tali er um öll starfsmenyki gasins.
**Candidate 1:** Ífram er að taka til allra gjafir tekjur í gjöf.
**Candidate 2:** Í öllum vinnuauðkenni gas.
**Candidate 3:** Takmörkuð er allar notkun gass í vinnu.
**Candidate 4:** Tilgreind eru allar notkun öndu í rekstri.
**Candidate 5:** Taka er mið af öllum notkun gass í vinnunni.
**Candidate 6:** Tilkynnt er um öllum tæknikerfinu, sem meðferð er fyrir gjöfinni, um gas.
**Candidate 7:** Tilgreint er um öll atvinnuauðgjöf gasins.

</details>

<details><summary>A · G8 · p13official21:dev:eso:70 · P</summary>

**Source:** This is only the sixth of these huge storms to be spotted since 1876.
**Semantic decision:** P — Candidate6 retains only sixth huge storm detected since1876 despite inflection.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [6]
**Candidate 0:** Þetta er aðeins sexustur af þessum stórum andrúm sem koma fram síðan 1876.
**Candidate 1:** Þetta er bara sexstríðarinn í þessu fjarlægnum stormi sem sást síðan árið 1876.
**Candidate 2:** Þetta er aðeins sjöttni af þessum stórum stormum sem komu fram frá 1876.
**Candidate 3:** Þetta er aðeins sjötta af þessu stórum stormi sem greint hefur verið í sér frá árið 1876.
**Candidate 4:** Þetta er aðeins sjötta þessar eirir sinna sem fyrir sé sýnt í gegnum ár frá 1876.
**Candidate 5:** Þetta er aðeins sjökthugbúið stormið sem gegnast fyrir 1876.
**Candidate 6:** Þetta er aðeins sjötta þessara miklum storma sem greinst hefur eftir 1876.
**Candidate 7:** Þetta er aðeins sex af þessum umræðum sem tækt hefur verið síðan 1876.

</details>

<details><summary>A · greedy · p13official21:dev:eea:534 · F</summary>

**Source:** Council Directive 74/60/EEC of 17 December 1973 on the approximation of the laws of the Member States relating to the interior fittings of motor vehicles.
**Semantic decision:** F — Interior fittings becomes inner phenomena, losing the regulated object.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Tilskipun ráðsins 74/60/EBE frá 17. desember 1973 um samræmingu á lögum aðildarríkjanna varðandi innri fyrirbæri vélkrafta ökutækja.

</details>

<details><summary>A · greedy · p13official21:dev:eso:323 · F</summary>

**Source:** They were able to make the sharpest direct observation ever , of the centre of a distant galaxy, the bright quasar 3C 279, which contains a supermassive black hole with a mass about one billion times that of the Sun, and is so far from Earth that its light has taken more than 5 billion years to reach us.
**Semantic decision:** F — Billion is changed to million for both mass and light-travel time.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þau komu að gera skarpsmári beinu sjónauki á miðju fjarlægri vetrarbrauta, 3C 279, sem er björtur kvarnir 3C 279, sem inniheldur öflugan massamikla svarthol með massi um milljóna tímann stærri en sólin og er svo fjarlægt frá Jörðinni að ljósinn hennar hefur tekið meira en 5 milljón ára til okkar.

</details>

<details><summary>A · G8 · p13official21:dev:eea:2037 · U</summary>

**Source:** Those criteria should not be considered to be exhaustive.
**Semantic decision:** U — Several render exhaustive as perfect/complete. Cannot confidently certify the intended non-exhaustiveness distinction.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Einnig skal ekki taka þessi viðmiðanir sem fylgja alveg.
**Candidate 1:** Þessi viðmiðanir skulu ekki teljast nákvæmar.
**Candidate 2:** Ekki skal telja þessar viðmiðanir fullkomlínar.
**Candidate 3:** Ekki skal telja þessi viðmiðanir fullkomi.
**Candidate 4:** Ekki skal telja þessar viðmiðanir fullkomnir.
**Candidate 5:** Ekki skal telja þessar viðmiðanir fullkomin.
**Candidate 6:** Sem ekki séu upplýsandi skal ekki telja þessi viðmiðanir fullkomin.
**Candidate 7:** Ekki skal telja þær viðmiðanir alveg upplaus.

</details>

<details><summary>A · G8 · p13official21:dev:eea:85 · P</summary>

**Source:** For the estimation of these concentrations all relevant information on the plant protection product and on the active substance must be taken into account.
**Semantic decision:** P — Candidate7 preserves concentration estimation and taking all relevant plant-protection-product/active-substance information into account.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [7]
**Candidate 0:** Til að áætla niðurstöður við þessar styrkur verður að taka tillit til allra viðeigandi upplýsinga um plöntuvarnarefnið og virka innihaldsefnið.
**Candidate 1:** Við mat á þessum styrk á að taka yfir allar þær upplýsingar sem tengjast vörublöðvörn og virka innihaldsefnið.
**Candidate 2:** Til áætlunar á þessum styrk, gilda allar viðeigandi upplýsingar um plöntuverndar lyf og virka efnið.
**Candidate 3:** Vegna matar á þessum styrkur áður sem meðferð er beitt verður að taka í tillit til allra viðeigandi upplýsinga um plöntuverndarvörn og virka efnin.
**Candidate 4:** Við mat á þessum styrkleika skulu taka til athygli á allar viðeigandi upplýsingar um plöntuvarnarefnið og virka efnin.
**Candidate 5:** Vegna matar á þessum styrkleikum verður að taka tillit til allra viðeigandi upplýsinga um plöntsöng og virka innihaldsefnin.
**Candidate 6:** Við áætlanir á þessum þéttni skulu taka tillit til allrar viðeigandi upplýsinga um plöntuhem ertu og virku innihaldsefnin.
**Candidate 7:** Við mat á þessum styrk skulu taka til athygli allar viðeigandi upplýsingar um plöntuverndarlyf og virka efnið.

</details>

<details><summary>A · greedy · p13official21:dev:eso:446 · P</summary>

**Source:** “Astronomers have waited for data like this for over a decade.
**Semantic decision:** P — Astronomers waiting over ten years for such data retained; grammatical errors do not alter the claim.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** „Stjörnufræðingar höfðu bíðið um gögn eins og þetta í meira en tíu ár.

</details>

<details><summary>A · greedy · p13official21:dev:ema:325 · F</summary>

**Source:** If you get lower abdominal pain, gain any weight rapidly, feel sick or are vomiting or if you have difficulty in breathing, talk to your doctor straight away who might ask you to stop using this medicine (see in section 4 under “Serious side effects”).
**Semantic decision:** F — Lower abdominal pain is corrupted and feeling sick becomes getting infections.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Ef þú færð magavart, færð þig hratt þyngd, færð sýkingar eða er uppköst, eða hefur vandamál við öndun, skaltu tafarlaust ræða við lækninn sem kann að spyrja þig um að hætta notkun lyfsins (sjá kafla 4 undir „Alvarlegar aukaverkanir“).

</details>

<details><summary>A · G8 · p13official21:dev:eea:1914 · P</summary>

**Source:** This Regulation shall enter into force on the third day following that of its publication in the Official Journal of the European Union.
**Semantic decision:** P — Exact source/hypothesis semantic reuse from card91: Candidate5 preserves third-day entry into force after Official Journal publication.
**Inspected / Correct indices:** [4] / [4]
**Candidate 0:** Reglugerð þessi öðlast gildi fyrri daginn eftir að hún er birt í Stjórnartíðindum Evrópusambandsins.
**Candidate 1:** Reglugerð þessi öðlast gildi síðar á þriðju degi eftir birtun hennar í Stjórnartíðindum Evrópusambandsins.
**Candidate 2:** Reglugerð þessi öðlast gildi þriðja daga eftir greiningu hennar í Stjórnartíðindum Evrópusambandsins.
**Candidate 3:** Reglugerð þessi öðlast gildi fyrri um þriðju degi eftir birtu henni í Stjórnartíðindum Evrópusambandsins.
**Candidate 4:** Reglugerð þessi öðlast gildi þriðju degi eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.
**Candidate 5:** Reglugerð þessi öðlast gildi á þriðja degi eftir birtun hennar í Stjórnartíðindum Evrópusambandsins.
**Candidate 6:** Reglugerð þessi öðlast gildi fyrir þriðja dag eftir birtun hennar í Stjórnartíðindum Evrópusambandsins.
**Candidate 7:** Reglugerð þessi öðlast gildi þriggja daga eftir talið er hún birt í Stjórnartíðindum Evrópusambandsins.

</details>

<details><summary>A · greedy · p13official21:dev:eso:726 · F</summary>

**Source:** They wanted to study the interaction between a young generation of stars and the cold clumps that were assembling into these first galaxies.
**Semantic decision:** F — Young generation of stars becomes star formations; assembling into galaxies becomes already assembled in them.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þau vildu rannsaka milliverkun á ungu stjörnumyndunum og kaltum klumpum sem voru samanbúin í þessum fyrstu vetrarbrautum.

</details>

<details><summary>A · greedy · p13official21:dev:eea:1461 · F</summary>

**Source:** All industrial uses of gas are considered.
**Semantic decision:** F — Industrial uses becomes use at work, losing the specific scope.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Íhugað er allar notkun gass í vinnu.

</details>

<details><summary>A · G8 · p13official21:dev:eso:765 · F</summary>

**Source:** “If it keeps spinning rapidly it might end its life in one of the most energetic explosions in the Universe, known as a long-duration gamma-ray burst,” says the lead scientist of the project, Hugues Sana, of the University of Leuven in Belgium.
**Semantic decision:** F — All corrupt energetic explosion/long-duration gamma-ray burst and/or rotation condition and attribution.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** „Ef hún helst snúa hratt, kannski hægt að betur enda líf hennar í einu vonum stóru geislun efnis í alheiminu sem kallast langtímagerma- föstu,“ sagði Hugues Sana, leiðandi vísindamannnar á verkefninu, í Leuven-háskóla í Belgíu.
**Candidate 1:** „Ef það hreyfir hraða um sig, kann að enda lífi sínu í eins af verulegustu mjúksteifjunum í alheiminu, sem kallast lengdar gammalekaflug,“ sagði Hugues Sana, aðalhálfur verkefnisins í Leuven háskóla í Belgíu.
**Candidate 2:** „Ef hann helst hreyfa hraða gæti hann farið fyrir létinu af einu af mesta kjarnasprautum í alheiminu, sem hefur þýðið lengdarsamprunnar“, sagði letri vísindamaður um verkefnið, Hugues Sana, frá Leuven-universíti í Belgíu.
**Candidate 3:** „Ef hún hefur styrkur hraða er mögulegt að hún studdi á einu af erfiðasta sprengingunum alheimisins, sem kallast langtíma gama gegnburður,“ sagði Hugues Sana, leiðsögnarhæfileiki verkefnisins, um frá Sturtarháskólanum í Belgíu.
**Candidate 4:** „Ef það hreyfir hratt getur það endað líf síðarinn í einum langvinnu rassliði úr vetrarbrauta sem kallast langvinn rassliður,” sagði Hugues Sana, leiðbeinandi vísindamaður á verkefnið á vísindagardinu í Leuven í Belgíu.
**Candidate 5:** „Ef það hreyfir sér hratt, getur það fengið einhverju lengstu gamma-losunarins í alheiminu, sem kallast langvarandi gamma-losunarins,“ sagði Hugues Sana, leiðbeinandi vísindamanna á verkefnið, frá Leuven universítíti í Belgíu.
**Candidate 6:** „Ef það virðist snúast hraðlega kann það að enda lífið í sjónið eins langvarandi gammablárbrot sem er hefði náð í vetrarbraut,“ sagði Hugues Sana, letri vettvangi verkefnisins, frá Leuven-í Belgía.
**Candidate 7:** „Ef það haldar að snúast hraðlega, getur það komið fyrir í einkennilega segara fyrir sér, sem þjónustu er kallað á móttöku á alheiminu“ segir Hugues Sana, aðalhæfileikarmanninn í verkefninu, sem er stjörnufræðingur í Leuven-í Belíegeiðinu.

</details>

<details><summary>A · greedy · p13official21:dev:opensubtitles:2508 · F</summary>

**Source:** Rose, we have a guest in the living room.
**Semantic decision:** F — Living room becomes an unspecified room.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Rose, við höfum gest í herberginu.

</details>

<details><summary>A · greedy · p13official21:dev:ema:1100 · P</summary>

**Source:** If you miss a dose, take your next dose as scheduled.
**Semantic decision:** P — Missed dose and next scheduled dose retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Ef þú gleymir skammtinum, taktu næsta skammt samkvæmt áætlun.

</details>

<details><summary>A · greedy · p13official21:dev:ema:2013 · P</summary>

**Source:** There is no evidence to suggest that eptotermin alfa alters fertility.
**Semantic decision:** P — No evidence of altered fertility and drug identity retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Ekki er neitt til staðar til að sýna fram á að eptotermin alfa breytir frjósemi.

</details>

<details><summary>A · G8 · p13official21:dev:eso:302 · F</summary>

**Source:** This is because the tilt of the orbit is normally unknown.
**Semantic decision:** F — None preserves unknown orbital inclination; outputs substitute side, vein, car, or unrelated terms.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Það er vegna þess að hliðin kringliðarhringarinnar er venjulega ekki þekkt.
**Candidate 1:** Það er vegna þess að stojakiltur í kringlunum er venjulega ekki þekkt.
**Candidate 2:** Það er vegna þess að bláæðin er venjulega ekki þekkt.
**Candidate 3:** Þetta er vegna þess að þjóðor meginfirarðið er venjulega ekki þekkt.
**Candidate 4:** Það er vegna þess að hálfan bílinn er venjulega ekki þekktur.
**Candidate 5:** Þetta kemur fyrir vegna þess að umhverfisstig um reikninga sé vanlega ekki þekkt.
**Candidate 6:** Þetta er vegna þess að fækkun ró á meginborði er venjulega óþekkt.
**Candidate 7:** Þetta er vegna þess að um námi banvændisins er venjulega ekki vitað.

</details>

<details><summary>A · greedy · p13official21:dev:ema:1718 · F</summary>

**Source:** Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.
**Semantic decision:** F — Possible decreases in pharmacodynamic effects become unspecified possible effects.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Samhliða lyfjagjöf edoxabans og P-gp örvaðs rífampicins leiddi til minnkaðrar meðal AUC fyrir edoxaban og skerðingar helmingunartíma, sem geta haft mögulega áhrif á lyfhrifum.

</details>

<details><summary>A · greedy · p13official21:dev:ema:1765 · P</summary>

**Source:** Take this leaflet or some tablets with you so that your doctor knows exactly what you have taken.
**Semantic decision:** P — Take leaflet/tablets so doctor knows what was taken; minor inflection only.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Takið þessi fylgiseðil eða töflur með þér svo að læknirinn þekki nákvæmlega hvað þú hefur tekið.

</details>

<details><summary>A · G8 · p13official21:dev:ema:1192 · P</summary>

**Source:** It is used to prevent pregnancy.
**Semantic decision:** P — Exact source/hypothesis semantic reuse from card63: Candidate2 correctly states use to prevent pregnancy.
**Inspected / Correct indices:** [2] / [2]
**Candidate 0:** Hann er notað til að koma í veg fyrir þungun.
**Candidate 2:** Það er notað til að koma í veg fyrir þungun.
**Candidate 5:** Það er notað til að forðast þungun.

</details>

<details><summary>A · G8 · p13official21:dev:eea:574 · F</summary>

**Source:** All rear-window, roof-panel and partition switches intended for use by occupants in the rear of the vehicle shall be capable of being switched off by a driver-controlled switch which is located forward of a vertical transverse plane passing through the R points of the front seats.
**Semantic decision:** F — All corrupt controls and specified geometric driver-switch location; some reverse front/rear or on/off.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Allir plássskiptir í bakgondunum, tegliðgu eða vekjudegiinn eftir rútinu sem ætlaðir eru innlendum í rútinu á vagninu, skulu fylgja að meðferðum handa handstjórnandi skiptu sem er staðsett fyrir viðri hlið yfir lágkvennsri tegundra velfær frá deilunum í veflungunum í fyrstu sætur.
**Candidate 1:** Allir opinum-og meðalvinna skiptir, sem gefnar eru út á bak hluta ökutækisins, skulu vera færir til að skipta á með skipti sem umhverfur er í skipti með ökumað.
**Candidate 2:** Allir slíkar snjallavirkir á aftursvæði, fjallvirkju eða ristilvirkju sem notaðir eru af innbyggjendum í aftur svæði ökutækisins, eiga að vera að slíkum snjálfavirkum snjallavirkjum sem beitt er við á borð við hlutaðeigandi veggir og er búin frá hlutar fyrir fjölskyldu.
**Candidate 3:** Allar höðvaka, loftmælin og partína, sem ætlaðar eru til notkunar um eykil í eftirbilinu, skulu geta verið hægt að slökkva með þeim hlévigum sem stjórnmandur tekur stjórn á og er í framan á flatri yfirgegnum sem fer í R-stöðum á framan hljóðar.
**Candidate 4:** Hverja afturslögun, skuggaskipti og voru skipti sem ætlaðir eru fyrir notendum á eftirrásum ökutækisins, skulu hafna hægt að slökkva með skipti sem annar eru í stjórn ökutækisins og er meðferðir fyrir gegn hægri, levurlega ás og snúa gegn R stigum í framanstaðum.
**Candidate 5:** Allar beldir til að setja aftan, eftir húð á rútinu og málur á höfuðsviðum, sem inngjafa einstaklingar á aftan í ökutækinu, skulu geta verið skiptir aftur á með skipti sem er leyft með skipti sem er í stjórn við hendi ökumanns og er í fyrirlaga við hliðsviðinn sem flugi yfir R-stöðum í fyrirsviðum.
**Candidate 6:** Allir bakglas, tegli og dílslökkur sem ætlaðir eru til notkunar fyrir einstaklinga í framan við ökutæki skulu geta verið slökkt af með skjallu sem einstaklingur hafði takmarka í fyrirriða við lygrarplan sem fer úr R-stigum fyrir sæti.
**Candidate 7:** Öll bakgluggi, húðafæð og rækur sem ætlað eru til notkunar innsæitöku í aftur af vélinn skal geta verið skiptur á til aftur af skipti sem er fluttur með áhættuvarnir sem er settur fyrir ofan frá lyngir þrúgengu hliðar sem snúa um R-stig innri rúms í skrifstöðum.

</details>

<details><summary>A · G8 · p13official21:dev:eea:15 · F</summary>

**Source:** Where studies are conducted using active substance produced in the laboratory or in a pilot plant production system, the studies must be repeated using active substance as manufactured, unless it can be justified that the test material used is essentially the same for the purposes of environmental testing and assessment.
**Semantic decision:** F — No candidate preserves pilot-plant production plus the full justified environmental-equivalence exception.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Ef rannsóknir eru framkvæmdar með virkum efni sem framleitt er í rannsóknarstofu eða í flagna kemmtustóla skal endurskoða rannsóknina með virkum efnið, samkvæmt framleiðslum áræði fyrir virk efnið, nema við eftirkvæði geti komið fram á að prófunarinnihaldsefnið er í alvöru svipað fyrir umhverfisskrutningu og mat á umhverfisins.
**Candidate 1:** Ef rannsóknir eru gert með virkum efni sem framleidd er í rannsóknaráðstöðu eða í rannsóknarstofum, skulu rannsóknirnar endurtekin með virkum efnum eins og þau eru framleidd, nema það sé greinilegt að prófunarinnihaldsefnið, sem notað er, sé næstum svipuð fyrir umhverfisrannsóknir og mat.
**Candidate 2:** Ef rannsóknir eru gerðar með virkum efni sem framleitt er í rannsóknartegundum eða í rannsóknartegundum í rannsóknarstofu verður að endurtaka rannsóknirnar með virkum efnum eins og þau eru framleidd, nema valdið sé á grundvelli þess að prófunarvörunin er í sambandi með umhverfisrannsóknir og við mat á umhverfið.
**Candidate 3:** Ef rannsóknir eru framkvæmdar með virkum efni sem framleitt er í rannsóknarkerpi eða í rannsóknarstofu, gerast þær endurtaka með virkum efni sem framleitt er, nema það sé greinilegt að prófunarinnihaldsefnið sé í raun svipuð til þess að gefast sé í rannsóknir á umhverfisástandi.
**Candidate 4:** Ef rannsóknir eru gerðar með virkum efni sem framleiðir er í rannsóknarkerfi í rannsóknarkerfi síðan hefur verið sett á eða í rannsóknarkerfi í rannsóknarkerfi síðan hefur verið sett á, skulu rannsóknirnar endurtakið með virkum efni eins og það er framleiðið, nema hægt sé að ræða að tilrauninu sem er notað er sé að essi eingöngu sambærilegt á þýðingu fyrir um rannsóknir á umhverfi.
**Candidate 5:** Ef rannsóknir eru gerðar með virka efninum, sem framleitt hefur verið í rannsóknarstofunni eða í rannsóknarskírði með lyfjaskiptum, skulu rannsóknirnar endurtakið með virku efnið eins og það er framleitt, nema má rökseiga að prófunarinnu sé í alvöru sömu til þess að rannsaka umhverfið.
**Candidate 6:** Ef verkefnið er gert með virku innihaldsefninu sem framleiðið er í rannsóknarskýrslunni eða í rannsóknaræði, þarf að endurtaka rannsóknina með virku innihaldsefninu sem framleiðið er, nema rétt sé kallað á að tilstilli að mismunandi virku innihaldsefninu sé í öllu orkun til að framkvæma rannsókn á umhverfið og meta á það.
**Candidate 7:** Ef rannsóknir eru gerðar með virka efni sem framleiðið er í rannsóknastofunni eða í áætlunarrannsóknarstjórn, þarf að endurtaka rannsóknina með virku efni eins og það er framleiðið, nema ótímis sé hægt að ræða að prófunarmattið sem notað er sé í aðtraði sambærilegt við umhverfi rannsókn og mat.

</details>

<details><summary>A · greedy · p13official21:dev:eso:1051 · F</summary>

**Source:** The technique used by Teague, which derived averaged variations in the flow of the gas as small as a few percent, revealed the impact of multiple planets on the gas motions nearer to the star.
**Semantic decision:** F — Multiple planets becomes family of Earths and derived small variations becomes caused average changes.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Tæknið sem Teague notaði, sem leiddi til meðalbreytinga á flæði gassins eins minnka og nokkrar prósentar, sýndi áhrif fjölskyldu jörðanna á flæði gassins nálægri stjörnunni.

</details>

<details><summary>A · greedy · p13official21:dev:opensubtitles:3209 · P</summary>

**Source:** Because it's not safe there.
**Semantic decision:** P — Exact source/hypothesis semantic reuse from card25: Unsafe location retained with awkward grammar.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Það er ekki örugg í því.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eea:15 · F</summary>

**Source:** Where studies are conducted using active substance produced in the laboratory or in a pilot plant production system, the studies must be repeated using active substance as manufactured, unless it can be justified that the test material used is essentially the same for the purposes of environmental testing and assessment.
**Semantic decision:** F — All eight lose the pilot-production-system distinction and/or the essential-equivalence exception for environmental testing.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Ef rannsóknir eru framkvæmdar með virkum efni sem framleitt er í rannsóknarstofu eða í flagna kemmtustóla skal endurskoða rannsóknina með virkum efni eins og það er framleitt, nema bein skal réttar að réttlætisgildum af völdum prófunarfyrrfyrir- ingarins sé að sameiginlega hlutverk prófunarfyrrfyrir- ingarins sé það sama ef prófunarfyrrfyrir- ingarinn er notaður í umhverfisrannsókn.
**Candidate 1:** Ef rannsóknir eru gert með virkum efni sem framleidd er í rannsóknarstöðum eða í reykkahúsum skal endurskoða rannsóknina með virkum efni eins og það er framleitt, nema nauðsynlegt sé að rannsóknar- efnið er venjulegt, að því er varðar umhverfisrannsóknir og mat á því.
**Candidate 2:** Ef rannsóknir eru gerðar með virka efni sem framleitt er í rannsóknarstöðum eða í reynslustöðum skal endurskoða rannsóknirnar með virkum efni eins og það er framleitt, nema framkvæmdastillingin geti verið rökstudd um að prófunarefnið, sem er notað í prófunum, sé í orðið samsvarandi hjá þeim þegar þau eru notaðir í umhverfismati.
**Candidate 3:** Ef rannsóknir eru framkvæmdar með virkum efni sem framleitt er í vinnslustöðum eða í vinnslustöðum, sem notað gerast í rannsóknarskífun, þarf að endurtaka rannsóknirnar með virkum efni sem framleitt er, nema jöfnun geti verið rökstudd að prófunarinnihaldsvörnin séu á grundvelli umfangs samsvarað prófunarinnihaldsvörni sem notað er í umhverfisrannsóknir og mat.
**Candidate 4:** Ef rannsóknir eru gerðar með virkum efni sem framleitt er í rannsóknarfyrirtæki eða í rannsóknarfyrirtæki sem er notað í forhætti við framleiðslu, skal endurtaka rannsóknirnar í samræmi við virkt efni sem framleitt er, nema afhent sé rétt að það sé samsvarandi vandamálarmat framleiðslu- og rannsóknar- fyrirtækisins.
**Candidate 5:** Ef rannsóknir eru framkvæmdar með virkum efni sem framleitt er í rannsóknarstofu eða í framleiðsluverkefni sem notuð er í starfsverki eftir fjölfræðingi þarf að endurtaka rannsóknirnar með virkum efni sem framleitt er, nema ástæða komi fram af því að prófunarefnin, sem notað er, er í heil fyrir umhverfisrannsóknirnar.
**Candidate 6:** Ef verkefni eru framkvæmdar með virku efni sem framleitt er í rannsóknarsvæði eða í rannsóknarsvæði með framleiðsluverkun í sér stöð, verður að endurtaka rannsóknirnar með virku efni eins og það er framleitt, nema það komi fram á ábyrgðað að prófunarsamsettan mun varðar erfiðleikarum þess að prófunarsamsettan sé sambærilegur, að öðrum kosti, við umhverfisrannsóknir og -gagna.
**Candidate 7:** Ef rannsóknir eru framkvæmdar með virka efni sem framleitt er í rannsóknastofunni eða í áætlunarstofnun, þarf að endurtaka rannsóknirinn með virku efni eins og það er framleitt, nema vera máð að ræða að prófunarefnið sem notað er sé í raunsviðitt sú samanborið og samanburður, að því er varðar umhverfisrannsóknir og mati.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eso:775 · F</summary>

**Source:** A team of astronomers, led by Istvan Dékány of the Pontificia Universidad Católica de Chile, has now used data from this survey, taken between 2010 and 2014, to make a remarkable discovery - a previously unknown component of our home galaxy, the Milky Way.
**Semantic decision:** F — All eight corrupt a key leader/discovery/component-of-the-Milky-Way relation.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Hópur stjörnufræðinga, lögð undir Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notað gögnum úr þessari rannsókn, sem gerð var á tímabilinu 2010-2014, til að gera nákvæmri uppgötvun - og gáttur sem var aldrei greint frá í húð í völdum þessarar vetrarbrautar.
**Candidate 1:** Hópur stjarnvísindamanna, hjá stjörnufræðingum Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notað gögn úr þessum skoðanum, sem gerð var á milli 2010 og 2014, til að gera ógangan viðmiðanlegri upptökin - þátt í okkar heimsverðu vetrarbrauta sem ekki var vitað áður.
**Candidate 2:** Hópur stjörnufræðinga, gefnu félagi Istvan Dékány hjá Pontificia Universidad Católica de Chile, hefur nýlega notið gögnum úr þessari rannsókn, sem gerð var á bilinu 2010 til 2014, til sérstakrar uppgötvunar - aðgang að sér, sem var aldrei komið fram, í heimsverðu vetrarbrautarinni, Vetrarbrautarinni.
**Candidate 3:** Hópur stjörnufræðinga, sem leitur stjörnufræðingi Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur ný ekki meðtöldu niðurstöður úr þessari rannsókn, sem tólgast á tímabilinu 2010 til 2014, til mjög mikilvægs uppgötvunar - nýju tilvik af hluta sólastjörnu okkar, Vetrarbrautarinnar.
**Candidate 4:** Hópur stjörnufræðinga, sem eru leitur undir strengs Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notað gögnum frá þessari rannsókn, sem tóknar voru á milli 2010 og 2014, til mikiðar uppáhalds uppgjör – einstaka hluti hópsins, milíkvikunnar.
**Candidate 5:** Hópur stjörnufræðinga, undir forystu Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notuð gögn úr slímu rannsókninni, sem tóknar voru á árinu 2010 til 2014, til þess að gera óvænlegan fund - aðalætin sem við um þátt frá heimskjóðum okkar, Frjóhvernina.
**Candidate 6:** Hópur stjörnufræðinga, sem stjörnufræðingar Istvan Dékány frá Pontificia Universidad Católica de Chile leidur, hefur nú notað gögn úr samanburðarfarannsókninni, sem gerð var undir stjarnvísindamálinu, á tímabilinu 2010-2014, til framlitslegra uppgötvunar – sem var áður óþekktur hluta heimsvæðisins, Vetrarbrautarinnar.
**Candidate 7:** Hópur stjörnufræðinga, leitt af István Dékány við Pontificia Universidad Católica de Chile, hefur nú notuð niðurstöður þessarar skoðunar, sem tómist á aldrinum 2010 til 2014, til að ná í nákvæmri náminu - af því sem ekki var vitað áður um í vetrarbrautinni.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:opensubtitles:1159 · U</summary>

**Source:** Somebody get me a picture of the girl.
**Semantic decision:** U — Request for a girl's picture is recognizable, but malformed accusative construction and make/get wording leave recipient/action uncertain.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Einhvern geri mig mynd af stúlkunni.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eea:1461 · F</summary>

**Source:** All industrial uses of gas are considered.
**Semantic decision:** F — Gas is omitted and industrial use is not faithfully specified.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Í öllum notkunir í vinnuþætti eru tekin tillit.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eso:1051 · U</summary>

**Source:** The technique used by Teague, which derived averaged variations in the flow of the gas as small as a few percent, revealed the impact of multiple planets on the gas motions nearer to the star.
**Semantic decision:** U — Averaged few-percent variations and multiple-planet relation remain linguistically unclear.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Tæknið sem Teague notaði, sem sáði meðalbreytingar á flæði gassins eins og nokkrum prozentum, benti í ljós áhrif fjölbreyttra reikistjarna á flæði gassins nálægt stjörnunni.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eea:1914 · P</summary>

**Source:** This Regulation shall enter into force on the third day following that of its publication in the Official Journal of the European Union.
**Semantic decision:** P — Candidate5 retains entry into force on the third day following publication in the EU Official Journal.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [5]
**Candidate 0:** Reglugerð þessi öðlast gildi fyrri daginn eftir að hún er birt í Stjórnartíðindum Evrópusambandsins.
**Candidate 1:** Reglugerð þessi öðlast gildi síðar á þriðja degi eftir birtun hennar í Stjórnartíðindum Evrópusambandsins.
**Candidate 2:** Reglugerð þessi öðlast gildi þriðja daga frá þeim sem hún er birt í Stjórnartíðindum Evrópusambandsins.
**Candidate 3:** Reglugerð þessi öðlast gildi þriðja degi eftir að hún birt er í Stjórnartíðindum Evrópusambandsins.
**Candidate 4:** Reglugerð þessi öðlast gildi í þriðja degi eftir birtu henni í Stjórnartíðindum Evrópusambandsins.
**Candidate 5:** Reglugerð þessi öðlast gildi á þriðja degi eftir birtun hennar í Stjórnartíðindum Evrópusambandsins.
**Candidate 6:** Reglugerð þessi öðlast gildi fyrri daginn eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.
**Candidate 7:** Reglugerð þessi öðlast gildi í þriðja degi eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eso:491 · U</summary>

**Source:** ALMA can observe in different frequency bands.
**Semantic decision:** U — Candidate4 contains frequency ranges, but the observation action is not clear; other candidates mistranslate bands.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** ALMA getur athugað á milli í mismunandi fjölda fjöldaða.
**Candidate 1:** ALMA getur fylgst með framkvæmdaferð að mismunandi þurrktíðnefndum.
**Candidate 2:** ALMA getur rannsakað milli samsættunarbundinna fyrirbæri.
**Candidate 3:** ALMA getur gaknt á mismunandi geimsjónabilum.
**Candidate 4:** ALMA má fara beina upp á mismunandi tíðnisvæðum.
**Candidate 5:** ALMA getur mælt í mismunandi fjölda árskors.
**Candidate 6:** ALMA getur metað í mismunandi fjölda.
**Candidate 7:** ALMA getur fylgst með tjóna í mismunandi fjölda fjölda.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eso:768 · P</summary>

**Source:** Both components are classed as O-type stars.
**Semantic decision:** P — Both components being O stars is preserved; inflection errors are minor.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Bæði hlutin eru flokkaðar sem O- stjörnur.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:ema:1718 · P</summary>

**Source:** Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.
**Semantic decision:** P — Candidate6 retains concomitant dosing, P-gp-inducer rifampicin, mean AUC decrease, shorter half-life and possible pharmacodynamic reduction.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [6]
**Candidate 0:** Samhliða gjöf edoxabans ásamt P-gp örvaðilum, rifampicini, leiddi til minnkaðs mína AUC forðastöðu edoxabans og minnkaðs helmingunartíma, geta hugsanlega leikið á minnkaðum lyfhrifum.
**Candidate 1:** Samhliðagjöf edoxaban og P-gp örva rifampicins leiddi til minnkaðs AUC fyrir edoxaban og minnkunar helmingunartíma, með hugsanlega minnkun á lyfhrifum.
**Candidate 2:** Notkun edoxabans samtímis rifampicíni, P-gp örva, leiddi til minnkar á meðal AUC fyrir edoxaban og minnkaðs helmingunartíma, sem gæti valdið minni verkun lyfsins.
**Candidate 3:** Samhliða lyfjagjöf edoxaban og P-gp örva rifampicins leiddi til minnkaða meðal AUC fyrir edoxaban og minnkaðra helmingunarskammts, sem hugsanlega gæti minnað virkni lyfs.
**Candidate 4:** Samhliða gjöf edoxabans og P-gp örva rifampicins leiddi til minnkaðs meðaltals AUC fyrir edoxaban og minni helmingunartíma sem hugsanlega leiddi til minnkaðrar lyfhrífina.
**Candidate 5:** Samhliða gjöf edoxaban og gangólfræðisbænda, rifampicins, leiddi til minnkaðrar meðal AUC fyrir edoxaban og minni helmingunartíma, sem gæti einnig valdið minnkuðum lyfhrifum.
**Candidate 6:** Samtímis gjöf edoxaban með P-gp örva rifampicini leiddi til minnkaðrar meðal AUC gildi fyrir edoxaban og styttingar á helmingunartíma, mögulega minnkaðri lyfhrifum þess.
**Candidate 7:** Samhliða lyfjagjöf edoxabans og rifampicins, P-gp örvi, leiddi til minni meðal AUC fyrir edoxaban og minnkaðrar helmingunardauða, með hugsanlega minnkaðri lyfhrifum.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:ema:1406 · F</summary>

**Source:** Concomitant use with yellow fever vaccine and with live virus and bacterial vaccines (see section 4.5).
**Semantic decision:** F — All eight mistranslate yellow fever and/or replace the vaccine/virus/bacterial-vaccine objects.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Rannsóknir komu fram að samhliða bóluefni við gulvafæð og lifandi veirusjúkdómsefni og sýklameðferð (sjá kafla 4.5).
**Candidate 1:** Samhliða notkun með llautakvilli og lifandi veiru- og bakteríukvilli (sjá kafla 4.5).
**Candidate 2:** Samhliða meðferð með barnaveiki gegn gulavarna og lifandi veiru og bakteríum (sjá kafla 4.5).
**Candidate 3:** Samhliða notkun með fangavísi- bóluefni og lifandi veirulyfjameðferð (sjá kafla 4.5).
**Candidate 4:** Samhliða notkun á bóluefni við gulaveru og lifandi veirusjónum og bakteríu (sjá kafla 4.5).
**Candidate 5:** Samhliða notkun millivefja fyrir gulvindur og lifandi veiru- og bakteríusmita (sjá kafla 4.5).
**Candidate 6:** Notkun samhliða geisla gegn gulteypuleiðum og lifandi veiru- og bakteríusmitun (sjá kafla 4.5).
**Candidate 7:** Notkun samhliða barnaæxlisbóluefni og lifandi veiru- og bakteríubóluefni (sjá kafla 4.5).

</details>

<details><summary>t0500795 · greedy · p13official21:dev:ema:1100 · P</summary>

**Source:** If you miss a dose, take your next dose as scheduled.
**Semantic decision:** P — Missed dose and taking the next scheduled dose are retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Ef þú gleymir skammtinum, skal taka næsta skammt eins og áætlað er.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:opensubtitles:3209 · U</summary>

**Source:** Because it's not safe there.
**Semantic decision:** U — Negated safety retained, but 'in it/that' does not clearly preserve 'there'.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Því það er ekki örugg í því.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:opensubtitles:996 · P</summary>

**Source:** What kind of man would that make me?
**Semantic decision:** P — Exact source/hypothesis semantic reuse from card127: What kind of man would that make me retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Hvers konar maður myndi það gera mig?

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eea:1552 · F</summary>

**Source:** The analytical result shall be reported as x +/– U whereby x is the analytical result and U is the expanded measurement uncertainty, using a coverage factor of 2 which gives a level of confidence of approximately 95 % (U = 2u).
**Semantic decision:** F — Expanded measurement uncertainty is replaced by an unrelated exposure/measures expression.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Greina skal niðurstöður greiningar sem x +/– U þar sem x er niðurstöður greiningar og U er útsetningarráðstafanirinn með því að nota 2 gildi fyrir umfangsþátt, sem gefur til kynna um öryggi í um 95% (U = 2u).

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eso:924 · F</summary>

**Source:** ESO was delighted to welcome Italys Minister of Education, Universities and Research, H.E. Stefania Giannini, to the ceremony, which was also attended by the Italian Consul General in Munich, Renato Cianfarani, the ESO Council President, Patrick Roche, and the Italian ESO Council Delegates, Nicolò DAmico (who is also President of INAF) and Matteo Pardo, Scientific Attaché at the Italian Embassy in Berlin.
**Semantic decision:** F — Minister's country/title, ceremony and several attendee roles are corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** ESO var ánægð af því að bjóða Stefania Giannini, íslandsskonar menntamaður, H.E., til sérstakrar stefnumatsins sem einnig tókst í henni Renato Cianfarani, alþjóðasamtryggingaforslanur í Múnich, Patrick Roche, forseti ráðsins ESO og Nicolò DAmico (sem er líka forseti INAF) og Matteo Pardo, vísindaaðila í vettvangi Ítalíu í Berlín.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eea:574 · F</summary>

**Source:** All rear-window, roof-panel and partition switches intended for use by occupants in the rear of the vehicle shall be capable of being switched off by a driver-controlled switch which is located forward of a vertical transverse plane passing through the R points of the front seats.
**Semantic decision:** F — All eight corrupt switch types, rear-occupant control and/or the specified geometric location.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Allar bakvara, skugga- og hlíftrúar, sem ætlaðar eru til notkunar hjá notendum í aftanrás, skulu vera komar við stöðvun með því að snúa við skiptivissu sem stjórnast er handa ökumann eftir eyðublöður sem snúst yfir í beinhuldri hálfan spjalla sem snúst gagnsæði R stöðvarinnar í frumkantanum.
**Candidate 1:** Allir opinum-og meðalgluggar, loftfæri og skiptala sem eru ætluð til notkunar af ökumenninni í eftirrásinni ökutækisins skulu vera mögulegar til að slaka á með skilfræðilegu kviarsemill sem er í fæstu á þrírúmmál sem fer þegar fyrir R-stöður vefstendur.
**Candidate 2:** Allir slíkar snjallavélur sem er ætlað til notkunar fyrir ökumaður í fram- baki ökutækisins, sem snemjast við bakglugga, háls- hettuklukka og deildarliðir, skulu vera færðar fyrir takmarkandi snjallavél sem er sett fram á baki fyrir hæðar svæði sem snemi gegn R-stöðum í framsetningu sættana.
**Candidate 3:** Allar höðvaka, loftmælin og partína, sem ætlaðar eru til notkunar um hvertvörð á ökutækinu, skulu geta verið skipt upp með skipta sem er stjórnunarlögð og er í fram á hliðinni yfir hliðferðnarplan (transverse plane) sem fer úr R-stóðum fyrstu sætta.
**Candidate 4:** Hverja afturslögun, skuggaskipti og voru skipti sem ætlaðir eru fyrir notendum í eftirrás æxilsins skulu mögulegar til að slífa með skipulag sem stjórnarið annast og er sett fyrir borði lausar slímu.
**Candidate 5:** Allar beldturýlur, rassaræði og hylkjufyrirskiptar sem ætlað eru til notkunar af einstaklingum á rassar hluta ökutækisins skulu geta verið stöðug til að slíta á lokun sem er skiptið með fylgiseðli sem er í framhliða spilagra, loftmælispilinn sem fer í gegnum R-stig fyrirsetta.
**Candidate 6:** Allir bakglas, tegli og dílslökkur sem ætlaðir eru til notkunar fyrir einstaklinga í aftanrosti ökutækisins skulu heimilt er slökkvitað við sem ökumennaframfylgt bylgjuskjöl sem er sett fyrir við alla hliðschím fyrir rótaþrengið á fyrri sæti fyrir mats punktum.
**Candidate 7:** Öll bakglugga, húðafæð og þyrpingar, sem ætlaðir eru til notkunar inntækja í baka ökutækisins, skulu geta verið hættur af sjálft, með öllum áhættumælandi stöðlum sem eru í bil við sig á borð við stökka hliðinni og eru á gegnum R-stig af uppsetningum í framsetrunum.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:ema:1582 · P</summary>

**Source:** The treatment-free period, however, should take into account the pharmacological properties of the products used previously.
**Semantic decision:** P — Candidate6 retains a treatment-free period and pharmacological properties of previously used drugs.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [6]
**Candidate 0:** Meðan á meðferðarfraslengd er að finna skal þó taka tillit til lyfjamennsla vörunnar sem notað var áður.
**Candidate 1:** Meðferðarframanstundin skal þó að gera tillit til lyfjaskipta vörunnar sem notað er.
**Candidate 2:** Meðferðarframtíminn skal þó taka tillit til lyfjafræðilegra eiginleika lyfja sem hafa verið notaðir áður.
**Candidate 3:** Hins vegar skal meðferðarframanlegur tíminn taka tillit til lyfjafræðilegrar eiginleika lyfja sem notuð voru áður.
**Candidate 4:** Meðferðarframanstundin skal þó taka til tekinn lyfjahefðbundin eiginleiki lyfinna sem notaðir hafa verið áður.
**Candidate 5:** Hugtakir byggist á því, áttur þó að tvílið teki fram lyfjafræðilegar eiginleikar lyfana, sem hafa verið notuð fyrir þessa meðferð.
**Candidate 6:** Meðan án meðferðar tíminn heildar skal þó hafa í huga lyfjafræðileg eiginleikar lyfjanna sem eru notaðir áður.
**Candidate 7:** Meðferðarframtímabilinu skal þó íhuga lyfjafræðilegar eiginleika lyfja sem notaðir hafa verið áður.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eea:1585 · P</summary>

**Source:** The Commission shall submit a final evaluation report at the end of the Programme.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Framkvæmdastjórnin skal leggja fram endanleg matsskýrslu að lokum áætlunarinnar.
**Candidate 1:** Framkvæmdastjórnin skal leggja fram endanleg mataráðgerð eftir að áætlunin er lokið.
**Candidate 2:** Framkvæmdastjórnin skal leggja fram endanlega matsskýrslu við lok áætlunarinnar.
**Candidate 3:** Framkvæmdastjórnin skal leggja fram endanlega matsskil á lokum áætluninnar.
**Candidate 5:** Framkvæmdastjórnin skal leggja fram endanleg matsskýrslu við lok áætlunarinnar.
**Candidate 6:** Framkvæmdastjórnin skal leggja fram endanleg matsskýrslu eftir að áætlunin er lokið.
**Candidate 7:** Framkvæmdastjórnin skal leggja fram endanlegar matsskýrslu samkvæmt áætluninu.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:ema:1192 · P</summary>

**Source:** It is used to prevent pregnancy.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Inspected / Correct indices:** [2] / [2]
**Candidate 0:** Hún er notað til að koma í veg fyrir þungun.
**Candidate 2:** Það er notað til að koma í veg fyrir þungun.
**Candidate 6:** Það er notað til að koma í veg fyrir barnshreyfileika.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eea:1991 · F</summary>

**Source:** Paragraph AG27 is amended and after paragraph AG29, paragraph AG29A is added.
**Semantic decision:** F — The AG prefixes identifying the amended paragraphs are lost.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Í 27. lið er breytt og eftir 29. lið bætist við 29. lið A.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eso:323 · F</summary>

**Source:** They were able to make the sharpest direct observation ever , of the centre of a distant galaxy, the bright quasar 3C 279, which contains a supermassive black hole with a mass about one billion times that of the Sun, and is so far from Earth that its light has taken more than 5 billion years to reach us.
**Semantic decision:** F — Billion is changed to million in both black-hole mass and light travel time; other scientific content is corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þau komu fram til skarpsíðu beinu sjónauka á miðju fjölli fjarlægri vetrarbrauta, 3C 279, sem er björtur kvarnafjölda og inniheldur öflugan massa sársaukans sem er um bil ein milljón sinnum stærri en sólin, og er svo langt frá Jörðinni að ljós hennar hefur tekið meira en 5 milljón ára til okkar.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eso:206 · F</summary>

**Source:** The survey was sensitive to planets between 75 million kilometres and 1.5 billion kilometres from their stars (in the Solar System this range would include all the planets from Venus to Saturn) and with masses ranging from five times the Earth up to ten times Jupiter.
**Semantic decision:** F — All eight change the upper distance of1.5 billion km to million/trillion or another wrong magnitude.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Skoðunin var sérþekkandi fyrir reikistjörnur á bilinu 75 milljónir kílómetrar til 1,5 milljónir kílómetrar frá stjörnunum (í Jörðavegi upplýsir um allar reikistjörnurnar frá Venus til Saturn) og með massafjölda á bilinu frá fimm sinnum jörðu til tíu sinnum Júpíturni.
**Candidate 1:** Skýrslugjöfin var næmurverk fyrir reikistjörnur á milli 75 milljóna og 1,5 milljóna kílómetra frá stjörnur (í sólkerfinu farið eru öll reikistjörnurnar frá Venus til Saturns) og heildarmassa á bilinu frá fimm sinnum jörðu upp í tíu sinnum Júpítur.
**Candidate 2:** Slíkt rannsókn var næm fyrir reikistjörnur á bilinu milli 75 milljón km og 1,5 milljón milljón km frá stjörnunum (í sólkerfinu innihéldur allar reikistjörnurnar frá Venus til Saturn) og með massamagni á bilinu frá fimm sinnum jörða upp í tíu sinnum Júpíturni.
**Candidate 3:** Til greiningar var næm fyrir reikistjörnur á bilinu 75 milljón km til 1,5 milljón km frá stjörnum (hér í sólkerfinu eru öll reikistjörnur frá Venus yfir í Saturn) og massagildi eftir fyrir fimm sinnum verið upp í tíu sinnum Júpíturnum.
**Candidate 4:** Rannsóknin var næm við reikistjörnur sem eru á bilinu 75 milljón km til 1,5 milljón milljón km frá stjörnunum (í sólkerfinu í þessa bil er allan reikistjörnin frá Venus til Saturn) og með þyngd á bilinu fimm sinnum jörði allt að tíu sinnum Júpíturnum.
**Candidate 5:** Skoðanirnar höfðu nákvæman svið við reikistjörnur á bilinu 75 milljón km til 1 biljón km frá stjörnunum (í Jörðareikistöðunni fylgir þeim öll reikistjörnur frá Venus til Saturns) sem eru á massagildum frá fimm sinnum yfir jörðina fram að tíu sinnum Júpíturnum.
**Candidate 6:** Rannsóknin var næm fyrir reikistjörnur í milli 75 milljón km og 1,5 milljórn km frá stjörnunum (í sólkerfinu fylgir það öll reikistjörnur frá Vensu til Saturs) og með massalimma á bili frá fimm sinnum jörðu í tíu sinnum Júpíturnum.
**Candidate 7:** Skoðunin var meðvæn fyrir reikistjörnur á bilinu 75 milljón km til 1,5 milljón milljón km frá stjörnum (í sólkerfinu fylgi þess öll reikistjörnur frá Venus til Saturn) og með massagerð frá fimmrauða á Júpíturnum upp í tíurauða.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eea:534 · U</summary>

**Source:** Council Directive 74/60/EEC of 17 December 1973 on the approximation of the laws of the Member States relating to the interior fittings of motor vehicles.
**Semantic decision:** U — Directive/date retained, but translation of interior fittings is uncertain.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Tilskipun ráðsins 74/60/EBE frá 17. desember 1973 um samræmingu á lögum aðildarríkjanna varðandi innri fyrirbúningar ökutækja.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:opensubtitles:2508 · F</summary>

**Source:** Rose, we have a guest in the living room.
**Semantic decision:** F — Living room is changed to the home.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Rose, við erum með gesta í heimilinu.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:ema:1394 · F</summary>

**Source:** The most commonly reported adverse reactions (≥ 20%) among patients treated with both belatacept- based regimens (MI and LI) up to Year 3 are diarrhoea, anaemia, urinary tract infection, peripheral oedema, constipation, hypertension, pyrexia, nausea, graft dysfunction, cough, vomiting, leukopenia, hypophosphataemia, and headache.
**Semantic decision:** F — Every candidate mistranslates at least one essential adverse event or treatment condition; leukopenia is repeatedly replaced by anaemia/thrombocytopenia.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Algengustu aukaverkanirnar (≥ 20%) hjá sjúklingum sem fengu bæði reglur sem byggðar eru á belatacepti (MI og LI) til aldurshversið 3 eru niðurgangur, blóðleysi, sýking í þvagfæringum, burtverk æðar í útlöndum, hægðatregða, háþrýstingur, hita, ógleði, verkun grúnna, hósti, uppköst, blóðflagnafæð, blóðfosfatarmagsýki og höfuðverkur.
**Candidate 1:** Algengustu aukaverkanirnar sem komu fram hjá sjúklingum sem fengu bólusetninga sem byggðar voru á belatacepti (MI og LI) í allt að 3. ári eru niðurgangur, blóðleysi, þvagbólgu, þroti í burtiplöngum, bindistúkkur, háþrýstingur, hiti, ógleði, misvirkni, hósta, uppköst, blóðleysi, blóðsólcistilviki og höfuðverkur.
**Candidate 2:** Algengustu aukaverkanirnar sem greint hefur verið frá hjá sjúklingum sem hafa verið meðhöndlaðir með bæði meðferð með belatacepti (MI og LI) allt til árs 3 (≥ 20%) eru niðurgangur, blóðleysi, sýking í þvagæðum, bólga í utan æðabundinna, hægðatregða, háþrýstingur, hiti, ógleði, vansköpun gegnðagreina, hósti, uppköst, albúmfrumnarfalli, blóðfl. leif (hypophosphataemia), og höfuðverkur.
**Candidate 3:** Algengustu aukaverkanirnar sem fram komu hjá sjúklingum sem fengu beina reglum með belatacepti (MI- og LI-) allt til árs 3 (≥ 20%) eru niðurgangur, blóðleysi, sýking í þvagverkunni, bólgu í brjósti, truflun, háþrýstingur, hiti, ógleði, misvirkni á ágrunnar, hósta, uppköst, minnkun blóðflagnanna, blóðfosfatsskort og höfuðverkur.
**Candidate 4:** Algengustu aukaverkanirnar (≥ 20 %) hjá sjúklingum sem fengu lyfleysu sem byggir á belatacepti fram að ári 3 eru niðurgangi, blóðleysi, sýking í þvagæðum, bólga í umþun, hægðatregða, háþrýstingur, hiti, ógleði, skortsóknarbilun, hósti, uppköst, blóðflagnafæð, blóðfosfatfæð og höfuðverkur.
**Candidate 5:** Algengustu aukaverkanirnar sem greint var frá (≥20%) hjá sjúklingum sem fengu bæði meðferð með belatacepti-bundnum meðferðaráætlunum (MI og LI) fram í 3. ári eru niðurgangi, blóðleysi, ofnæmisbólga, bólga til burtar í burtu, kassabólga, háþrýsting, hiti, ógleði, truflun á grúnunni, hósta, uppköst, minnkun blóðflagnanna, blóðfosfatslækkun og höfuðverkur.
**Candidate 6:** Algengustu aukaverkanirnar (≥ 20%) sem greint hefur verið frá hjá sjúklingum sem fengu meðferð með belatacept-bundnum meðferðaráætlunum (MI og LI) allt að ári 3 eru niðurgangur, blóðleysi, sýkingar í þvagæðum, bólga í útlinda, hægðatregða, háþrýstingur, hita, ógleði, truflun í nýrnastarfsemi, hósti, uppköst, blóðleysi, blóðpósi, og höfuðverkur.
**Candidate 7:** Algengustu aukaverkanirnar sem fram komu hjá sjúklingum sem fengu meðferð með bólusetningum sem byggjast á belatacepti (MI- og LI) allt til ára 3 og engu annars (≥ 20%) eru niðurgangur, blóðleysi, sýking í þvagmæli, bólga í umhverfislyfinu, hægðatregða, háþrýstingur, hita, ógleði, skort í ígræðslu, hósti, uppköst, blóðleysi, blóðfosfatslækkun og höfuðverkur.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eea:1194 · F</summary>

**Source:** It should provide the Commission and the Member States with objective, reliable and comparable information and data on maritime safety and on ship pollution prevention to enable them to take any necessary initiatives to enhance the measures in place and to evaluate their effectiveness.
**Semantic decision:** F — Objectivity/comparability and ship pollution prevention are materially mistranslated.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Hún skal veita framkvæmdastjórninni og aðildarríkjunum vísanir og gögn sem eru áframhaldandi, tryggðar og jafngiltar um öryggi í sjávarbærum og um að koma í veg fyrir bælingu af sjóvökva til þess að þau geti tekið nauðsynlegar framlög til að auka ráðstafanirnar sem eru í gildi og meta skilvirkni þeirra.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eso:491 · F</summary>

**Source:** ALMA can observe in different frequency bands.
**Semantic decision:** F — Frequency bands are replaced with unrelated concert/number wording.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** ALMA getur fylgst með tónleitum á mismunandi fjölda.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eso:70 · U</summary>

**Source:** This is only the sixth of these huge storms to be spotted since 1876.
**Semantic decision:** U — Candidate4 retains sixth/large storms/since1876, but adds unclear wording and does not clearly preserve the sighting relation.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Þetta er aðeins sjötta af þessum stórum andrúm sem koma fram síðan 1876.
**Candidate 1:** Þetta er aðeins sjötind í sex stöku þessum risagerðum sem sást frá 1876.
**Candidate 2:** Þetta er aðeins sjöttni þessi umbreyktra slökkva á vegum síðustu sinni frá árið 1876.
**Candidate 3:** Þetta er aðeins sjötta af þessu mikilu stormi sem lokið hefur verið sá aftur árið 1876.
**Candidate 4:** Þetta er aðeins sjötta þessara stóru storma sem hafa komið fram í lágari síðan 1876.
**Candidate 5:** Þetta er aðeins sjökthugur stormur af þessum meginþokum sem hafa verið gengin í ljós síðan 1876.
**Candidate 6:** Þetta er eingöngu sexu kyrninga storma sem er komið fram síðan árið 1876.
**Candidate 7:** Þetta er aðeins sex af þessum umtalsverðum tækanum slöngum sem stundum á eftir 1876.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eso:302 · F</summary>

**Source:** This is because the tilt of the orbit is normally unknown.
**Semantic decision:** F — None preserves the orbital tilt; alternatives contain unrelated quantities or objects.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Það er vegna þess að það er venjulega óþekkt sem típ svæðisins er.
**Candidate 1:** Það er vegna þess að stojakilt kringum þjóða er að venjulega óvísuð.
**Candidate 2:** Það er vegna þess að bláæður í kringslinu er vanalega ekki þekkt.
**Candidate 3:** Þetta er vegna þess að þjóðor meginfirarðs er venjulega óþekkt.
**Candidate 4:** Það er vegna þess að hálfalengd kringurbreinnar er venjulega ekki þekkt.
**Candidate 5:** Það er vegna þess að framstæði sfera er venjulega ekki þekkt.
**Candidate 6:** Þetta er vegna þess að fækkun róalsins er yfirleitt ekki þekkt.
**Candidate 7:** Þetta er vegna þess að um námi banvæna umferðar líður óvænt.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:opensubtitles:480 · F</summary>

**Source:** Now we have enough evidence to charge you with murder.
**Semantic decision:** F — Criminally charging someone is replaced by registering them.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Nú hafa við nóg sönnunargögn til að skrá þig fyrir morði.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eso:726 · F</summary>

**Source:** They wanted to study the interaction between a young generation of stars and the cold clumps that were assembling into these first galaxies.
**Semantic decision:** F — Assembly of clumps into the first galaxies is not preserved.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þeir vildu rannsaka milliverkun á ungu stjörnumyndunum og kaltum klumpum sem voru að samfylgja í þessum fyrstu vetrarbrautum.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eea:1461 · U</summary>

**Source:** All industrial uses of gas are considered.
**Semantic decision:** U — Gas and industrial/work use appear in some candidates, but all-use scope and considered/listed relation remain uncertain.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Í öllum atvinnuframleiðslum eru talin um notkun gasins.
**Candidate 1:** Ífram er að taka til allra gjöfgerða gasa.
**Candidate 2:** Eftirfarandi er tekin til baka: Allar gjöf gas í vinnu.
**Candidate 3:** Tilgreind eru öll atvinnugreinan notkun gas.
**Candidate 4:** Tilgreind eru allar notkun ökutækja af gassvörunum.
**Candidate 5:** Taka er mið af öllum notkunirar gas í vinnu.
**Candidate 6:** Tilgreint er um öll starfsemi gjalds.
**Candidate 7:** Tilgreint er um öll atvinnuauðgjöf gasa.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eea:2037 · U</summary>

**Source:** Those criteria should not be considered to be exhaustive.
**Semantic decision:** U — Negation retained, but completeness/exhaustiveness is confused with adequacy/perfection; no unambiguous faithful candidate.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Þessi viðmiðanir ættu ekki að teljast vera fullnægjandi.
**Candidate 1:** Þessi viðmiðanir skulu ekki teljast nákvæmar.
**Candidate 2:** Þessum viðmiðunum skal ekki telja fullkominn.
**Candidate 3:** Ekki skal telja þessi viðmiðanir fullnægjandi.
**Candidate 4:** Ekki skal telja þessar viðmiðanir fullkomlega.
**Candidate 5:** Ekki skal telja þessar viðmiðanir fullkomlegar.
**Candidate 6:** Sem ekki er að halda að þessum viðmiðunum séu fullnægjandi.
**Candidate 7:** Ekki skal telja þessar viðmiðanir fullnægjandi.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:ema:1765 · P</summary>

**Source:** Take this leaflet or some tablets with you so that your doctor knows exactly what you have taken.
**Semantic decision:** P — Leaflet or tablets, taking them along, and doctor's knowledge of what was taken are retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Taktu þessum fylgiseðli eða töflur með þér svo að læknirinn þekki nákvæmlega hvað þú hefur tekið.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eso:765 · F</summary>

**Source:** “If it keeps spinning rapidly it might end its life in one of the most energetic explosions in the Universe, known as a long-duration gamma-ray burst,” says the lead scientist of the project, Hugues Sana, of the University of Leuven in Belgium.
**Semantic decision:** F — All eight corrupt gamma-ray-burst terminology or omit/change the most-energetic-explosion claim and associated relations.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** „Ef hún helst snúa hratt er mögulegt að hún hætti líf sitt í eitt af algengustu sprengingum í alheiminum sem kallast langvarandi gammanýrsbrot,“ sagði framkvæmdarstjóri verkefnisins, Hugues Sana, frá Leuvenhaipskóla í Belgíu.
**Candidate 1:** „Ef það hreyfir vel áfram, getur það fengið leið í lengri dauða í annað því er mest virkstökkuleiki alheimsins sem kallast langvinn gammabláskapur,“ sagði Hugues Sana, aðalhæfileiki verkefnisins í Leuven universitetsi í Belgíu.
**Candidate 2:** „Ef þetta hreyfir sér hratt er það líklegt að það endist líf sitt í einu af öflugustu rassinum I alheiminum, sem kallast langvinnur gammaglöf,“ sagði Hugues Sana, leifasjómandi verkefnisins á Stungstuðulesisstofnun Leuven í Belgíu.
**Candidate 3:** „Ef hún hefur styrkur hreyfing er mögulegt að hún studdi sínu lífi í langvarandi gammaglöp í alheiminu, sem kallast langvarandi gammaglöp,“ sagði Hugues Sana, umsjónarfræðingur verkefnisins í Leuven-í Belgíu.
**Candidate 4:** „Ef það hreyfir sér hratt getur það ekki endað lífi sínu í einum af mestur stuðulíku sprengingum í alheiminu, sem kallast langtímasefræðingurstungur,“ sagði Hugues Sana, leitir hætti verkefnisins, um stofnun Leuven í Belgíu.
**Candidate 5:** „Ef það hreyfir sér hratt, getur það fengið einhverju mestur rauðra eruðunarárennslnar, sem kallast langvísi gamma-lyfsórun, á sér lyfið,“ sagði Hugues Sana, leiðrétta aðilar verkefnisins, við almennlega studýtúrinni á áhrifum geigerhnjósta, í Leuven-í Belgíu.
**Candidate 6:** „Ef það virðist snúast hraðlega kann það að enda lífið í einum vegna langtímarvíssra γ-losna, sem er kallast langímarvíssra γ-losna“, sagði letri vinnslufræðingurinn um verkefnið, Hugues Sana, við Leuven- háskóla í Belgíu.
**Candidate 7:** „Ef hún hreyfir áfram á hraða getur fyrir hana hodur slík lengri mjólkurbrun í alheiminu og það er kallað langtímavirkan gama-glasbrun,“ segir Hugues Sana, miði-vísindamannsstjörnunar starfsins við störf, sem er framkvæmdur af Vísindumstofunu Leuven í Belgíu.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eso:464 · F</summary>

**Source:** With an estimated mass of four to five times that of Jupiter, it would be the least massive planet to be directly observed outside the Solar System.
**Semantic decision:** F — Direct observation and the least-massive planet description are not faithfully expressed.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þegar það er með fjögur til fimm sinnum þeim massamagni og Júpíter, væri það minnst massamaksplanettin sem hefur verið tekin til staðar utan sólkerfinu.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:opensubtitles:3607 · F</summary>

**Source:** Well, that makes you ugly and stupid.
**Semantic decision:** F — Ugly is changed to strange.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Það gerir þig skrítn og heimskur.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:ema:325 · F</summary>

**Source:** If you get lower abdominal pain, gain any weight rapidly, feel sick or are vomiting or if you have difficulty in breathing, talk to your doctor straight away who might ask you to stop using this medicine (see in section 4 under “Serious side effects”).
**Semantic decision:** F — Difficulty breathing is omitted and lower-abdominal location is lost.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Ef þú færð magaverkjum, þyngdar hraðlega, færð ógleði eða er uppköst, talaðir þér við lækninn strax, sem kann að spyrja þig um að hætta notkun lyfsins (sjá kafla 4 undir „Alvarlegar aukaverkanir“).

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eea:85 · P</summary>

**Source:** For the estimation of these concentrations all relevant information on the plant protection product and on the active substance must be taken into account.
**Semantic decision:** P — Candidate1 retains estimating concentrations and considering all relevant plant-protection-product and active-substance information.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [1]
**Candidate 0:** Til að meta þessar styrk gilda allar viðeigandi upplýsingar um plöntuverndarvörn og virka efnin.
**Candidate 1:** Við mat á þessum styrkleikum ber að taka tillit til allrar viðeigandi upplýsinga um plöntuverndarvörunni og virka efninu.
**Candidate 2:** Til að meta þessi þéttni skal taka til athygli allra viðeigandi upplýsinga um völdumvörnarefnið og virka efnið.
**Candidate 3:** Vegna matar fyrir þessum þéttni skulu taka tillit til allra viðeigandi upplýsinga um plöntuverndarvörn og virka efnið.
**Candidate 4:** Við mat á þessum styrkleika verður að taka tillit til öllum viðeigandi upplýsinga um plöntuverndarvörn og virka efnið.
**Candidate 5:** Vegna áætlunar á þessum styrkleika verður að taka neytir yfir allar viðeigandi upplýsingar um plöntuvarnarefnið og virka efnið.
**Candidate 6:** Til að meta þessar þéttni verður að taka tillit til allra viðeigandi upplýsinga um vörnarefnið og virka efnið.
**Candidate 7:** Við mat á þessum styrkleika verður að taka allar viðkomandi tilvik gögnum um plöntuvarnarefnið og virka efnið í tillit.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:ema:1718 · U</summary>

**Source:** Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.
**Semantic decision:** U — AUC/half-life/effect decreases retained, but rifampicin's P-gp inducer role is linguistically unclear.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Samhliða gjöf edoxabans og P-gp örvaðs rífampicíns leiddi til minnkaðrar meðal AUC fyrir edoxaban og skertri helmingunartíma, sem getur valdið minnkun á lyfhrifum.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:ema:704 · F</summary>

**Source:** The most frequently reported adverse reaction was acne, which was generally mild.
**Semantic decision:** F — Acne is replaced by kúu; the named adverse reaction is not preserved.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Algengasta aukaverkunin sem greint var frá var kúu, sem var yfirleitt væg.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eea:281 · F</summary>

**Source:** The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.
**Semantic decision:** F — Former/latter matching and maturity-band terminology are materially corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Fjöldi fyrri (sáttmálans) sem samsvarar sáttmálans (fyrri) í tilteknum nýtingablóð skal vera samsvarandi stöður í þeim bloð, en eftirfarandi langa eða stuttu stöður skulu vera ósamsvarandi stöður í sömu bloð.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:opensubtitles:1169 · P</summary>

**Source:** They're pretty as can be, aren't they?
**Semantic decision:** P — Pretty/cute and the tag question are retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Þau eru mjög sæt, ekki satt?

</details>

<details><summary>t0500795 · greedy · p13official21:dev:opensubtitles:1012 · P</summary>

**Source:** I'll do whatever you ask.
**Semantic decision:** P — Promise to do whatever is asked retained despite tense/inflection.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Ég geri hvað sem þú baðir.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eea:1716 · U</summary>

**Source:** The competent authorities of Gabon have reacted promptly to these concerns, indicating their commitment to take all measures necessary to implement applicable ICAO standards and enforce compliance with these standards as soon as possible.
**Semantic decision:** U — Prompt response and ICAO measures recognizable, but commitment/implementation wording is not clear enough to certify.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Lögbæra yfirvöldir Gabón hafa svarað þessum ábendingum tafarlaust og benda til þess að þeim séu gert allar nauðsynlegar ráðstafanir til að framfylgja viðeigandi staðlana ICAO og framfylgja þeim sem nauðsynlegt er eins fljótt og mögulegt.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eea:609 · F</summary>

**Source:** Special payments for shift work.
**Semantic decision:** F — None preserves shift work; all use unrelated or malformed work/payment categories.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Sérfræðingarbótar fyrir mótskráða starf.
**Candidate 1:** Sérstök greiðslur fyrir skiptarókur.
**Candidate 2:** Sérstakt greiðslur í starfsmeðaltali.
**Candidate 3:** Sérstök bótaríkin fyrir ísköpunarstarf.
**Candidate 4:** Sérstök greiðslur fyrir starfsstöðum.
**Candidate 5:** Sérstök greiðslur fyrir skiptaríki.
**Candidate 6:** Sérstakar borgarfjárhæðir fyrir skrefvinnu.
**Candidate 7:** Sérstaka borgningar vegna skiptausna.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eea:1216 · F</summary>

**Source:** That task shall be coordinated with the existing regional cooperation programmes and shall include, where appropriate, the organisation of relevant training activities.
**Semantic decision:** F — Regional cooperation programmes are replaced by operational measures.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þessi verkefni skal samræmd við þau rekstraraðgerðir sem eru í gildi og skal þar með talið, ef við á, stjórnun viðeigandi þjálfunaráðstafana.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eso:501 · U</summary>

**Source:** The team used data from the UVES spectrograph on ESOs Very Large Telescope in Chile (to determine the properties of the star accurately), the Carnegie Planet Finder Spectrograph (PFS) at the 6.5-metre Magellan II Telescope at the Las Campanas Observatory in Chile, the HIRES spectrograph mounted on the Keck 10-metre telescope on Mauna Kea, Hawaii as well as extensive previous data from HARPS (the High Accuracy Radial velocity Planet Searcher) at ESOs 3.6-metre telescope in Chile (gathered through the M dwarf programme led by X. Bonfils and M. Mayor 2003–2010 described here).
**Semantic decision:** U — Candidate7 retains many instruments, sizes and dates, but previous-data and M-dwarf programme/leadership linkage cannot be confidently certified.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Hópurinn notuðu gögn úr UVES fyrirfarasjónauka Very Large Telescope ESO í Chile (til að ákvarða eiginleikar stjarnans nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5-metra Magellan II sjónauka á Las Campanas stjörnustöðinni í Chile, HIRES fyrirfarasjónauka á Keck 10-metra sjónaukinni í Mauna Kea, Hawaii ásamt skömmtum fyrri gögn frá HARPS fyrirfarasjónauka sem náði að ákveðnum þroska yfir um áhrif á reikistjörnur (High Accuracy Radial velocity Planet Searcher) á 3,6-metra sjónauka ESO í Chile (frá 2003 til 2010) sem sem framkvæmdastjórnur hópsins, X. Bonfils og M. Mayor, kveiktu með M-dvergum (dwarf stars) sem lýst er hér.
**Candidate 1:** Hópurinn notuðu gögn úr UVES litrófsritunni Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjarnans nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5 m Magellan II sjónaukni í Las Campanas stjörnustöðinni í Chile, HIRES litrófsritunni á Keck 10 m stjörnustjörnunni í Mauna Kea í Hawaii ásamt umfangsmikil gögn frá HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6 m litrófsritunni í Chile (stofnuninni leit fram með M dwarf prófunina sem leiðir sér fram X. Bonfils og M. Mayor á tímabili 2003–2010 sem lýst er hér.
**Candidate 2:** Hópurinn notaði gögn úr UVES litrófsrannsókninni á Very Large Telescope ESO í Chile (að því er varðar eðlilegan eiginleikastarfsemi stjörnunnar), Carnegie Planet Finder Spectrograph (PFS) á 6,5 metra Magellan II litrótanni á Las Campanas stjörnustöðinni í Chile, HIRES litrófsrannsóknina á Keck 10-metra litrótönnunni á Mauna Kea í Hawaii samt og farganglega fyrri gögn úr HARPS (High Accuracy Radial velocity Planet Searcher) á litrótökunni 3,6 metra ESO í Chile (að því er varða M-dvergum sem X. Bonfils og M. Mayor 2003-2010 rannsakaðu (greint hér).
**Candidate 3:** Hópurinn notaði þau gögn úr UVES litrófsrannsóknunni ESO Very Large Telescope í Chile (til að meta eðlilega eiginleika stjarnunnar) Carnegie Planet Finder Spectrograph (PFS) á 6,5 metra Magellan II rannsóknartækinu í Las Campanas stjörnustöðinni í Chile, HIRES litrófsrannsóknunni á Keck 10 metra tækinum á Mauna Kea í Hawaii, sem og gallt gögn úr HARPS (High Accuracy Radial velocity Planet Searcher) í Chile (til að koma fram á þeim með M dwarf rekstrarefni sem stjórnast af X. Bonfils og M. Mayor 2003-2010 sem lýsir hér á).
**Candidate 4:** Líkamsrannsóknin varðandi stjarnan sem eru í stjörnumyndunni með UVES víðblástursmálætið í Very Large Telescope ESO í Chile (að því er varðar aðjauta eiginleikar stjarnans með hæfilegan nákvæmni), Carnegie Planet Finder Spectrograph (PFS) á 6,5-metra Magellan II sjónauka í Las Campanas stjörnustöðinni í Chile, HIRES víðblásturinn í Keck 10-metra sjónauka á Mauna Kea, Hawaii og einnig mjög mikið fyrri gögn úr HARPS (High Accuracy Radial velocity Planet Searcher) í Chile (hugsanlega með úrræðum sem gerðir var samkvæmt M-dvergumælinum sem leiddi af X. Bonfils og M. Mayor á tímabili 2003-2010 sem lýst er hér).
**Candidate 5:** Teppin notaði upplýsingum frá UVES litrófsmálaáætluninu við Very Large Telescope á Chile (til að meta eiginleika stjarnunnar nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5 m Magellan II skýslunni á Las Campanas stjórnarstöðinni í Chile, HIRES litrófsmálaáætlunina á Keck 10 m litrasmi á Mauna Kea í Hawaii og mjög miklu gagni frá upplýsingum frá HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6 m litrasmi ESO í Chile (söfnuð með M-vunnunni sem leitaði í M-dvergum í tíðni 2003-2010 sem leitarar eru frá X. Bonfils og M. Mayor).
**Candidate 6:** Hópurinn notuði upplýsingum frá UVES mælitækið á Very Large Telescope (VLT) ESO í Chile (efnismælingar til að meta eðlilega eiginleika stjarnans) Carnegie Planet Finder Spectrograph (PFS) á 6,5-mættu Magellan II mælitæki á Las Campanas stjörnustöðinni í Chile, HIRES mælitækið sem er sett á Keck 10-meðaltals teini í Mauna Kea á Hawaii, samt og frekari upplýsingum frá HARPS (High Accuracy Radial velocity Planet Searcher) sem er í 3,6-mættu teini ESO á Chile (sögð fram með M dwarf prófið, sem stóð fram framkvæmd X. Bonfils og M. Mayor á tímabilið 2003-2010, sem lýst er hér).
**Candidate 7:** Hópurinn notaði gögn úr UVES litrófsritunni í Very Large Telescope ESO í Chile (til að meta eiginleika stjarnanns mjög nákvæmlega) Carnegie Planet Finder Spectrograph (PFS) á 6,5-metrykum Magellan II sjónauka á Las Campanas stjörnustöðinni í Chile, HIRES litrófsritunni á Keck 10-metrykum sjónauka á Mauna Kea í Hawaii sem og mjög miklum gögnum frá HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6-metrykum sjónauka ESO í Chile (á M dwarfaáætlunina sem leidur fram X. Bonfils og M. Mayor 2003–2010 sem lýsir hér.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eso:446 · P</summary>

**Source:** “Astronomers have waited for data like this for over a decade.
**Semantic decision:** P — Astronomers waiting over ten years for such data is retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** „Stjörnufræðingar höfðu bíðið um gögn eins og þessi í meira en tíu ár.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eea:922 · P</summary>

**Source:** Development of CPE is checked as described in Part I.III.4.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Inspected / Correct indices:** [6] / [6]
**Candidate 0:** Tilvik CPE þarf að rannsaka eins og lýst er í kafla I.III.4.
**Candidate 1:** Rannsökun á þróun CPE er gerð eins og lýst er í II.4. skilbibla I.
**Candidate 2:** Frekari þroska CPE er lokið eins og lýst er í I. III.4.
**Candidate 3:** Fylgjar er á þróun CPE eins og lýst er í III.4. þáttur I. hluta.
**Candidate 4:** Framkvæmd CPE er kannað í samræmi við það sem kveðið er á um í I. III. 4. þátt.
**Candidate 5:** Skoðað er þróun CPE eins og lýst er í 4. hluta III. þáttar I. hlið.
**Candidate 6:** Skoðað er þróun CPE eins og fram kemur í kafla I.III.4.
**Candidate 7:** Verið er viss um þróun CPE eins og lýst er í þremur 4. lið I.III.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:ema:2013 · P</summary>

**Source:** There is no evidence to suggest that eptotermin alfa alters fertility.
**Semantic decision:** P — No evidence of an eptotermin alfa fertility effect is retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Ekki er fram á neinar vísbendingar um að eptotermin alfa hafi áhrif á frjósemi.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eea:698 · P</summary>

**Source:** Only days that can be worked should be included when Saturdays and Sundays are not worked they should not be included, the same with public holidays).
**Semantic decision:** P — Candidate4 includes only workable days and excludes unworked Saturdays/Sundays and public holidays.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [4]
**Candidate 0:** Aðeins þægir skal dagsetningar sem má vinna í þegar ekki er tekið á sásterumog sunnudagum (sásterum og sunnudagum sem ekki hefur verið tekið á) og sama með opinbera fríadagana).
**Candidate 1:** Einungis skal taka til daga sem má vinna í þegar ekki er að vinna á laugardagum og sunnudagum, ekki þannir, eins og á opinberum fríar).
**Candidate 2:** Aðeins daga sem má vinnja skal taka með í að skrá, þegar ekki er vinnu stundum á sólarhringum og sólarhringardagum skal þau ekki taka með, það sama við opinbera frídagir.
**Candidate 3:** Einnung aðeins skal fyrir dögum þegar virkjar verða, þegar ekki er að virka á sólarhringum og sólarhringa- dagum, skal þeim eigi að taka við, eins og handaùngjöf.
**Candidate 4:** Aðeins dagar sem má vinna skal talda við þegar ekki er vinna á Laugardagum og sunnudagum, að þeim skal ekki talda við, samtímis opinberum fríadagum.
**Candidate 5:** Einnig skal taka bara dagirnar sem auðveld er að vinna, þegar ekki er vinna á sólarhringum og sunnudagum skal þau ekki taka, eins og viðkomandi er um almenna fríar).
**Candidate 6:** Bara skal taka til að hverja dagur sem má vinnja skal staðfestur; ekki skal taka til dagana sem ekki er vinnu dagur, þegar ekki er vinnu dagur eftir sára og dagur sem ekki er vinnu dagur (samhengt með opinbera fríadagana).
**Candidate 7:** Aðeins þær daga skulu tekið til meðaltals þegar ekki er hægt að vinna á sásterum og sunnudögum, að því er varðar opinbera fríadögur).

</details>

<details><summary>t0500795 · G8 · p13official21:dev:ema:767 · U</summary>

**Source:** Therefore, docetaxel must not be used during pregnancy unless clearly indicated.
**Semantic decision:** U — Pregnancy prohibition retained, but candidates change or obscure the clear-clinical-indication exception.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Því má ekki nota docetaxel meðan á meðgöngu stendur nema brýnt sé notkun þess.
**Candidate 1:** Því má ekki nota docetaxel á meðgöngu nema sprauta sé óskiljanlega á til.
**Candidate 2:** Því má ekki nota doketaxel á meðgöngu nema brýna ákvarðanir til kynna.
**Candidate 3:** Því má ekki nota docetaxel á meðgöngu nema greinilega áður sé til kynna.
**Candidate 4:** Því má ekki nota docetaxel á meðgöngu nema greinilega megi gefa það.
**Candidate 5:** Því verður ekki að nota dócetaxel á meðgöngu nema ávísað sé hægt.
**Candidate 6:** Því má ekki nota dócetaxel á meðgöngu nema brýna sjálfstakandi mæli gefið til umsvara.
**Candidate 7:** Því má ekki nota dócetaxel á meðgöngu nema algjörlegar ábendingar þessi.

</details>

<details><summary>t0500795 · G8 · p13official21:dev:eea:281 · F</summary>

**Source:** The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.
**Semantic decision:** F — All eight corrupt maturity-band terminology and/or former/latter matching and residual long/short positions.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Skammtur af því sem er samræmdur af því sem er samræmdur (því sem er samræmdur af því sem er samræmdur) á tilteknum vinnu-þætti skulu vera samræmd stöður á því vinnuþætti, samanboriðið því sem er ekki samræmdur (samræmdur því sem er ekki samræmdur), samanboriðið því sem er ekki samræmdur (samræmdur því sem er ekki samræmdur) á tilteknum vinnuþætti.
**Candidate 1:** Fjölda þeirra sem fyrri (sári) stóðu í hæfnivísi sem síðari (fyrri) stóðu í gengið hægðatyngd skal vera í stóðum í hægðatyngdinni, en eftirtakir stórt eða stuttur stóð er í því stóð sem eftir er ekki samsvarandi.
**Candidate 2:** Ílætið fráfaldinn (fráfaldinn) sem uppfyllir (uppfyllur) henni (fráfaldinn) í tilgreint stundistengdri fjarskiptatengda skal vera samræmd stöðvarina í þeirri tengdri fjarskiptatengdri, en eftirlætið stundistengd stöðurinn um stundistengdri tengdri fjarskiptatengdri skal vera ósamræmd stöðurinn í sama tengdri fjarskiptatengdri.
**Candidate 3:** Skammtur af þeim sem eru sambærilegum (hins vegar svörunar) af þeim sem eru sambærilegum (anversrar) í viðkomandi vinnustigsbraut skal vera viðmiðunarmassa í viðkomandi braut, en eftirfjarvinnu skammtar skulu vera ósambærir í sama vinnustigsbrautinni.
**Candidate 4:** Magn miðla (frummið) sem samhæft er af síðari (fyrri) miðla (frummið) á tilteknum útfallabréfi skal vera samhæft stöður á þessum útfallabréfi, en efnast langa eða stunda stöður skal vera fráhafna stöður á þessum útfallabréfi.
**Candidate 5:** Fjöldi framsómum (síðast) sem samsvarast við síðast (framsómum) í viðkomandi gildistærðarritu skal vera samsvarandi stöðvar í þeirri ritu, þó að eitthvað í hópi gildistærðaannars eða lægra stöðvans hafi ekki samsvaranleg stöð.
**Candidate 6:** Framvinsta (sákasta) sem samrýmist sá meira (sákasta) í geymdum aldringsbrennsluþroti skulu vera samrýmvedur stöður í þeirri breiði, ásamt því sem grunnvenja lags eða stóra stöða er ekki samrýmist í sama aldringsbrennsluþroti.
**Candidate 7:** Hlutar fyrri (sáttmiðar síðar) sem látasta við sáttmið síðar (fyrri) í tilteknum brottsbreyta skulu vera sáttmiði í þeirri brottsbreyti, þó viðlátstu langan eða stuttan stöðu skulu vera ósáttmiðir fyrir sama brottsbreyti.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eea:50 · F</summary>

**Source:** Similar studies, for at least three soil types, must be reported for all relevant metabolites, degrada tion and reaction products which in soil degradation studies account at any time for more than 10 % of the amount of active substance added.
**Semantic decision:** F — Soil types, degradation/reaction products and the quantitative qualifying relation are corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Tilkynna verður um svipaðar rannsóknir á að minnsta kosti þremur jarðefnum fyrir öll viðeigandi umbrotsefni, brotthvarf efnasöfnun og framleiðsluefni sem í rannsóknum á brotthvarfinu gefa stundum meira en 10% af skömmtum virka efna sem bætt eru í jarðefninu.

</details>

<details><summary>t0500795 · greedy · p13official21:dev:eso:919 · F</summary>

**Source:** "Thanks to several giant telescopes currently under construction, including ESOs E-ELT and the NASA/ESA/CSA James Webb Space Telescope due to launch for 2018, we will soon be able to study the atmospheric composition of these planets and to explore them first for water, then for traces of biological activity.
**Semantic decision:** F — Atmospheric composition is lost; telescope launch is changed into going to planets.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** „Takinn er við nokkrar stórum sjónaukum sem eru í framkvæmd og þar með talið ESOs E-ELT og James Webb Space Telescope frá NASA, ESA og CSA sem ætlar að fara í reikistjörnur árið 2018, getum við náið í geimstofu þessara reikistjarna og rannsakað þær fyrst um vatn, síðan um einkenni líffræðilegrar virkni.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eea:922 · P</summary>

**Source:** Development of CPE is checked as described in Part I.III.4.
**Semantic decision:** P — Candidate6 checks CPE development and preserves the nested PartI/III.4 reference.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [6]
**Candidate 0:** Tilvik CPE þróað er metað eins og lýst er í kafla III.4 í II. hlið.
**Candidate 1:** Rannsökast stöðluð er á þróun hópaþekkingarsíauðsins samkvæmt því sem lýst er í lið III.4 í þátttöku I.
**Candidate 2:** Frekari þroska CPE er lokið eftir þeirri rök sem lýst er í hluta III.4 í I. hvað varðar.
**Candidate 3:** Framdæling CPE er endurskoðað sem lýst er í hluta III.4 í I. kappanum.
**Candidate 4:** Framdæming CPE er rannsakað eins og lýst er í III.4. hluta I. hlið.
**Candidate 5:** Meðhöndlun á þróun á CPE er gerð eins og lýst er í IV.4 í hluta I. III.
**Candidate 6:** Skoðað er þróun CPE eins og fram kemur í hluta III.4 í I. hlið.
**Candidate 7:** Verkun CPE er hafað eftirlit með, eins og lýst er í III.4. hlið í I. hálfskipti.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:ema:1100 · P</summary>

**Source:** If you miss a dose, take your next dose as scheduled.
**Semantic decision:** P — Missed dose and next scheduled dose retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Ef þú gleymir skammti skal taka næsta skammt samkvæmt áætlun.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eea:85 · P</summary>

**Source:** For the estimation of these concentrations all relevant information on the plant protection product and on the active substance must be taken into account.
**Semantic decision:** P — Candidate1 retains concentration estimation and all relevant product/active-substance information.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [1]
**Candidate 0:** Til að meta þessar styrk gilda allar viðeigandi upplýsingar um plöntuverndarvörur og virka efnin.
**Candidate 1:** Við mat á þessum styrkleikum ber að taka tillit til allrar viðeigandi upplýsinga um plöntuverndarvöruna og virka efnið.
**Candidate 2:** Til að meta þessi innihaldsmagn, gilda allar viðeigandi upplýsingar um plöntuverndarvörn og virka efnið.
**Candidate 3:** Vegna matar fyrir þessum þéttni skulu taka tillit til allra viðeigandi upplýsinga um plöntuverndarvörn og virka efnið.
**Candidate 4:** Við mat á þessum styrkleika verður að taka tillit til öllum viðeigandi upplýsinga um plöntuverndarvörn og virka efnið.
**Candidate 5:** Vegna matar á þessum þéttni skulu taka tillit til allra viðeigandi upplýsinga um vörnaráðstöfunina og virka efnið.
**Candidate 6:** Við áætlanir á þessum þéttni skulu taka tillit til allra viðeigandi upplýsinga um vörnarefnið og virka efnið.
**Candidate 7:** Við mat á þessum styrk skulu taka til þess varðandi allar viðeigandi upplýsingar um plöntuverndarvörn og virka innihaldsefnin.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:ema:2013 · P</summary>

**Source:** There is no evidence to suggest that eptotermin alfa alters fertility.
**Semantic decision:** P — No evidence of an eptotermin alfa fertility effect retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Engin vísbending er til staðar um að eptotermin alfa hafi áhrif á frjósemi.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eea:1461 · U</summary>

**Source:** All industrial uses of gas are considered.
**Semantic decision:** U — Some candidates retain gas and work/industry use, but industrial scope and considered relation are not unambiguous.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Í öllum atvinnuframleiðsluminnustörunum er takað.
**Candidate 1:** Í uppbótarmiða eru í tölu gassamtölu.
**Candidate 2:** Það er finnt allar notkun gass í vinnufræðilegu tilgangi.
**Candidate 3:** Allar notkunar gass í atvinnustofnum eru íhug.
**Candidate 4:** Hverja gjöf gasa í vinnuhúsum er íhugast.
**Candidate 5:** Tilgreindar eru allar notkun gass í vinnu.
**Candidate 6:** Allar notkun gasa í vinnuþjálfun eru íhugað.
**Candidate 7:** Tilgreint er um öll atvinnuauðgjöf gasins.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eso:765 · F</summary>

**Source:** “If it keeps spinning rapidly it might end its life in one of the most energetic explosions in the Universe, known as a long-duration gamma-ray burst,” says the lead scientist of the project, Hugues Sana, of the University of Leuven in Belgium.
**Semantic decision:** F — Every candidate corrupts the gamma-ray-burst/energetic-explosion claim; some also reverse the spinning condition or change the country.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** „Ef hún helst hratt hreyfing er hún líklega hægt að enda lífi sínu í einu enda lengstu gamma-rárasprehællunar sem unnt hefur verið,“ segir Hugues Sana, aðalhafa verkefnisins í Leuven-í Írlandi.
**Candidate 1:** „Ef það hreyfir hraða um sig, kann það að leiða að dauða í annað því er hröðuð sig og það er hreinanir langvarandi gamma-losi,“ segir Hugues Sana, leiðtaka rannsóknarinnar við framkvæmdarefni, sem er stjörnufræðingur við Leuven-háskóla í Belgíu.
**Candidate 2:** „Ef hann helst hreyfa hraða gæti lífinn endað í einni af alvarlegustu geislunum í alheiminu, sem kjarna-geislun, sem er kallað lengri geislun,“ segir letri- aðgerðarfræðingurin, Hugues Sana, frá Leuven-universíti í Belgíu.
**Candidate 3:** „Ef hún hefur til staðar hreyft hvolflega, kann hún að enda lífi sínu í einu af fínnlegustu geimselldreifinu í alheiminum, sem nefnast langvinn og mælist með gammaglösum,“ sagði Hugues Sana, framhaldsrannsakinn verkefnisins, við universitíð Leuven í Belgíu.
**Candidate 4:** „Ef það hreyfir á hraði getur það endað líf sitt í einu af erfiðustu sprengingu Vetrarbrautarinnar, kallast langtíma gammaveirsli,“ segir Hugues Sana, aðalhenda verkefnisins í leirastofnun Leuven í Belgía.
**Candidate 5:** „Ef það hægir að snúast hratt mundi það líka enda lífi sínu í eina af öflusta sprengingu í alheiminn, sem kallast langtímastaða gammagröðurskammti,“ sagði Hugues Sana, rannsóknarstjóri verkefnisins við Universtitímun Leuven í Belgíu.“
**Candidate 6:** „Ef hún hreyfir áfram hraða þá kanni að hún stöðvist stórum geimhreyfi, sem kallast langtímamöguleg gémma- rögugginga,“ sagði Hugues Sana, hinn aðalhæfisstjörnufræðingur, sem stofnaði verkefnið í Leuven universitets í Belgíu.
**Candidate 7:** „Ef hún hreyfir sig hratt getur hún farið með lífinu í einu af sterkustu innbrotum í alheiminu, þar sem það kallast langtímamjólkur og sem er algerlegt,“ sagði Hugues Sana, aðalhöfundur verkefnisins við stofnuninni í Leuven í Belgíu.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eea:534 · U</summary>

**Source:** Council Directive 74/60/EEC of 17 December 1973 on the approximation of the laws of the Member States relating to the interior fittings of motor vehicles.
**Semantic decision:** U — Directive/date retained, but interior-fittings terminology remains uncertain.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Tilskipun ráðsins 74/60/EBE frá 17. desember 1973 um samræmingu laga aðildarríkjanna varðandi innri fyrirbúningar ökutækja.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:opensubtitles:1159 · F</summary>

**Source:** Somebody get me a picture of the girl.
**Semantic decision:** F — The receiver me is missing from the request to obtain a picture.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Einhver fá mynd af stúlkunni.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:ema:1394 · F</summary>

**Source:** The most commonly reported adverse reactions (≥ 20%) among patients treated with both belatacept- based regimens (MI and LI) up to Year 3 are diarrhoea, anaemia, urinary tract infection, peripheral oedema, constipation, hypertension, pyrexia, nausea, graft dysfunction, cough, vomiting, leukopenia, hypophosphataemia, and headache.
**Semantic decision:** F — Every candidate materially changes essential adverse events, treatment details or the time/frequency qualifiers.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Algengustu aukaverkanirnar (≥ 20%) sem tilkynnt var um hjá sjúklingum sem fengu báða lyfjameðferðin sem byggð er á belatacepti (MI og LI) allt til árs 3 eru niðurgangur, blóðleysi, þvagsýking, bólga á frumabólgu, póstbólga, háþrýstingur, hiti, ofning, blöðruðaframferð, hósta, uppköst, blóðleysi, blóðfosfatýrráði, og höfuðverkur.
**Candidate 1:** Algengustu aukaverkanirnar sem komu fram hjá sjúklingum sem fengu bólusetninga sem byggðar voru á belatacepti (MI og LI) í allt að 3. ári eru niðurgangur, blóðleysi, þvagbólga, þroti í útlægju hálfs, hægðatafla, háþrýstingur, hiti, ógleði, gráðuversnun, hósti, uppköst, blóðflagnafæð, blóðfosfatsfall og höfuðverkur.
**Candidate 2:** Algengustu aukaverkanir (>= 20%) fjöldis úr meðferðina með belatacepti (MI og LI) á ár 1-3 eru niðurgangur, blóðleysi, niðurbjúg, bólga í útlægum þrota, hægðatregða, háþrýstingur, hiti, ógleði, gróðurlosn, hósti, uppköst, hvítblæði, blóðesiðskorti og höfuðverkur.
**Candidate 3:** Algengustu aukaverkanirnar sem fram komu (≥ 20%) hjá sjúklingum sem fengu bæði meðferð með belatacept-bundnum meðferðaráætlunum (MI og LI) í allt að 3. ári voru niðurgangur, blóðleysi, nefðisbólga, útflýtisbólga, hægðistgjöf, háþrýstingur, hiti, ógleði, skerta græðslu, hósta, uppköst, blóðleysi, blóðfosfatsminning og höfuðverkur.
**Candidate 4:** Algengustu aukaverkanirnar sem fram komu hjá sjúklingum sem fengu bæði reglur sem byggðar voru á belatacepti (MI og LI) til 3. árs eru niðurgangur, blóðleysi, sýking í þvagæðum, útflæðisbólga, hægðatregða, háþrýstingur, hiti, ógleði, þroskubólgur á grúnunni, hósta, uppköst, blóðleysi, blóðfosfatslækkun og höfuðverkur.
**Candidate 5:** Algengustu aukaverkanirnar sem greint var frá (≥20%) hjá sjúklingum sem fengu bæði meðferð með belatacepti-bundnum meðferðaráætlunum (MI og LI) fram í 3. ári eru niðurgangi, blóðleysi, þvagræs, bjúgur sem til er utan víðblástra, kringvæði, háþrýsting, hiti, ógleði, skerðingu grúnunni, hósta, uppköst, hvítblóðfall, blóðfosfatarmilt og höfuðverkur.
**Candidate 6:** Algengustu aukaverkanirnar (≥ 20%) sem greint hefur verið frá hjá sjúklingum sem fá meðferð með bæði belataceptgerðarinni (mi- og LI) í allt að 3 árinu eru niðurgangur, blóðleysi, sýkingar í þvagæðum, bólga í útlinda, hægðatregða, háþrýstingur, hiti, ógleði, truflun í nýrnastarfsemi, hósti, uppköst, daufkyrningafæð, blóðblöðruð skertt, höfuðverkur.
**Candidate 7:** Algengustu aukaverkanirnar sem fram komu hjá sjúklingum sem fengu meðferð með bólusetningar sem byggðar voru á belatacepti (MI og LI) allt til ár 3 eru niðurgangur, blóðleysi, sýking í þvagfrumum, bólga í útlinda, neftrýmis, háþrýstingur, hiti, ógleði, misvirkni á frumunni, hósti, uppköst, blóðleysi, litalsýki og höfuðverkur.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:ema:1406 · F</summary>

**Source:** Concomitant use with yellow fever vaccine and with live virus and bacterial vaccines (see section 4.5).
**Semantic decision:** F — None preserves the complete yellow-fever/live-virus/bacterial-vaccine relation; even the English-parenthesis candidate substitutes viruses/germs.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Rannsókn með geislavöðva og lifandi veiruveiru og veirubólueyðandi bóluefni (sjá kafla 4.5).
**Candidate 1:** Samhliða notkun með llúpurfíflalysupilli og lifandi veiruskyðis- og bakteríumlýfum (sjá kafla 4.5).
**Candidate 2:** Samhliða meðferð með brúggi-æxlisbóluefni og með lifandi veirubóluefni og lifrarbóluefni (sjá kafla 4.5).
**Candidate 3:** Samhliða notkun með fangavíðæxli og lifandi veirum og bakteríum (sjá kafla 4.5).
**Candidate 4:** Samhliða notkun á aðeins heilbrigðisbóluefni gegn gulvífur og lifandi veirus og bakteríumbóluefni (sjá kafla 4.5).
**Candidate 5:** Samhliða notkun milliveitandi bóluefna gegn gulleyskurbólgu og lifandi veiruvefja og bakteríuvefja (sjá kafla 4.5).
**Candidate 6:** Samhliða notkun gegnsæi fasa- og lifandi veiru og sýklubóluefnis (sjá kafla 4.5).
**Candidate 7:** Notkun samhliða eisturveiru (yellow fever vaccine) og lifandi veirum og sýklum (see 4.5).

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eso:491 · F</summary>

**Source:** ALMA can observe in different frequency bands.
**Semantic decision:** F — Different frequency bands are not preserved.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** ALMA getur fylgt á milli mismunandi tímamálaband.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:opensubtitles:1012 · P</summary>

**Source:** I'll do whatever you ask.
**Semantic decision:** P — Promise to do whatever is asked retained despite tense/inflection.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Ég geri hvað sem þú baðir.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eea:1216 · U</summary>

**Source:** That task shall be coordinated with the existing regional cooperation programmes and shall include, where appropriate, the organisation of relevant training activities.
**Semantic decision:** U — Regional cooperation and relevant training organization are recognizable, but the existing-programme qualifier and coordination wording remain uncertain.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Það verkefni skal samræma við tilhögunar áætlunum um samstarfi á svæðum og skal það innihalda, eftir því sem við á, skipulagningu viðeigandi þjálfunaráðstöfunum.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eso:726 · F</summary>

**Source:** They wanted to study the interaction between a young generation of stars and the cold clumps that were assembling into these first galaxies.
**Semantic decision:** F — Assembly into the first galaxies is changed into accompanying them.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þeir vildu rannsaka milliverkun á yngri hópi stjarna og kaltum klumpum sem var að samfylgja í þessum fyrstu vetrarbrautum.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eso:446 · P</summary>

**Source:** “Astronomers have waited for data like this for over a decade.
**Semantic decision:** P — Astronomers waiting over ten years for such data is retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** „Stjörnufræðingar höfðu bíðið um gögn eins og þessi í meira en tíu ár.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:opensubtitles:996 · U</summary>

**Source:** What kind of man would that make me?
**Semantic decision:** U — The question about what kind of person this makes the speaker is recognizable, but the relation is malformed.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Hvers konar maður myndi það mér vera?

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eea:609 · F</summary>

**Source:** Special payments for shift work.
**Semantic decision:** F — No candidate faithfully specifies shift work.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Sérfræðingarbótar fyrir mótskráða starf.
**Candidate 1:** Sérstöku greiðslur fyrir staðdavinnu.
**Candidate 2:** Sérstakt greiðslur í starfsmeðaltali.
**Candidate 3:** Sérstakar greiðslur til skipta.
**Candidate 4:** Sérstakt greiðslur fyrir starfsstöðum.
**Candidate 5:** Sérstækan sendið vegna starfsins.
**Candidate 6:** Sérfræðilegar greiðslur fyrir stöktun.
**Candidate 7:** Sérþekkingar fyrir skiptahrif.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eea:1461 · F</summary>

**Source:** All industrial uses of gas are considered.
**Semantic decision:** F — Gas is changed to liquid.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Í allri notkun vökva í vinnuþætti er tekið tillit.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:ema:704 · F</summary>

**Source:** The most frequently reported adverse reaction was acne, which was generally mild.
**Semantic decision:** F — Acne is replaced by kúu; the named adverse reaction is not preserved.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Algengasta aukaverkunin sem greint var frá var kúu, sem var yfirleitt væg.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eea:698 · U</summary>

**Source:** Only days that can be worked should be included when Saturdays and Sundays are not worked they should not be included, the same with public holidays).
**Semantic decision:** U — Some general workable-day exclusion is recognizable, but weekend/holiday conditional inclusion is not clear enough to certify.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Aðeins þægir skal dagsetningar sem má vinna með, þegar ekki er vinna á sásterum og sólarhringum skal þá ekki hafa þá til staðar, samanborið með opinberum fríáðum dögum).
**Candidate 1:** Einungis skal taka til daga sem má vinna í þeim dagsetningu sem cifur ekki staðið á laugardaginn og laugardaginn, en ekki í þeim dagsetningu sem cifur ekki staðið í laugardaginn, og sama er við opinbera losunarheimdar).
**Candidate 2:** Aðeins daga sem má vinnast eiga aukið í aðalframanum en ekki daga sem koma stundum ekki fyrir vinnu þá skal ekki auka á aðalframanum, svo sem um er að ræða frógjóðagarða).
**Candidate 3:** Einnig aðeins daga sem ná má vinnu á við við fullaríki og helgir, þó ekki að við fullaríki, veli að sameiginlegum helgum)
**Candidate 4:** Einungis skal taka til daga sem má vinna og ekki einu sinni dögum sem ekki ræði að vinna skal ekki taka til þeirra, svo og opinbera fríar).
**Candidate 5:** Bara þeir daga skulu felldir til þegar þeir er mögulegar, baran daga skulu þegar þeir eru ekki ráða skal ekki felldir, eins og opinberar helgir).
**Candidate 6:** Bara skal taka þau daga sem hyggja má vinnu að þeim skal ekki taka þau daga (sásterur og sunnudagar) af sömu sambærilegu hlutum).
**Candidate 7:** Aðeins þær daga skulu tekið til meðferðar þegar ekki er vinna á sólarhringum og sólarborgum ef þau eru ekki vinna á skulu þau ekki tekið til meðferðar (samtíma bólgudagarnir).

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eea:1194 · F</summary>

**Source:** It should provide the Commission and the Member States with objective, reliable and comparable information and data on maritime safety and on ship pollution prevention to enable them to take any necessary initiatives to enhance the measures in place and to evaluate their effectiveness.
**Semantic decision:** F — Objective information and ship pollution prevention are materially corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Hún skal veita framkvæmdastjórninni og aðildarríkjunum vísbendingar og upplýsingar sem eru áframhaldandi, vissar og samanburðarlegt um öryggi á sjávarbærum og um aðferðir til að koma í veg fyrir útbergun afhættu í skipum til þess að þau geti tekið nauðsynlegar frumkvæði til að auka ráðstafanir sem liggja fyrir og meta skilvirkni þeirra.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eea:574 · F</summary>

**Source:** All rear-window, roof-panel and partition switches intended for use by occupants in the rear of the vehicle shall be capable of being switched off by a driver-controlled switch which is located forward of a vertical transverse plane passing through the R points of the front seats.
**Semantic decision:** F — All eight corrupt switch types, rear-occupant/driver control and the geometric location.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Allar bakvara, skrifþemur og mörkuða stöflur sem notendur á að leysa fram á aftan ökutækinn skulu hægt að slípa við með takirskipti sem er innlenda skipti við aksturshjúpandi skipti sem er á borð við hlið þess sem slípað er.
**Candidate 1:** Allir opinbreytur á bakgluggi, loftbrúnar- og vallaföllum sem eru ætlað af notenda í bakinn á ökutækinu skal hægt að slíta af með ölastilskipti sem er að finna fyrir aftan útfallandi, hliðshliðs, hliðar sem fara þegar í R-stigum í fyrri staðasta.
**Candidate 2:** Allir bletur í frávit, veggur- röð og breiðu, sem ætluð eru til notkunar af innsæi í frægum einingum, skulu hægt að slípa við með skruflum, sem er stjórnáttuð af ökumaður, sem er í hvort sinn á borði fyrir framan.
**Candidate 3:** Allar höðvindur, þeirmyndir og hlífir sem verða að nota einstaklingar í aftanrás ökutækisins skulu geta verið skipt upp af afmælu við vissir sem notkunartiltekinn snýr í fæstu við hliðandi hliðir sem fer á R-stöðum í fyrirhliðarstöðum.
**Candidate 4:** Hverja afturslíð, skugga- og skjallusvif sem ætlaðar eru fyrir notendum í eftirrás æxilsins skulu mögulegar til að hætta í skipandi áhættusvif sem annast eru á frammeri og borðar laug þar sem meginlega skjaldar gegn hringar yfir R-stöð á framansetjunum.
**Candidate 5:** Allar beldturýrur, rúppelnötur og hylkjufyrirskiptar sem notendur á bakinn í ökutækinu ættu að aðstoðast því að skiptast úr notkun með því að stýra á skipti sem skiptir úr notkun samkvæmt öllum þeim stöddum sem stýrir hægt fyrir borðinni á borði.
**Candidate 6:** Allir bakglas, tegli og dílslökkur sem ætlaðar eru til notkunar innlenda í aftan vélinni eða til handa notenda yfir tillit til akstursvirkja skulu hægt að slökkva af með bylgjuskjöl sem er takmarkaður af aksturshjálpum sem er í færri stöðum en hringið gegn svipplínu sem ferri nálægir R-loka í hliðarseturinnar.
**Candidate 7:** Öll bakgluggi, húðafæð og þyrpingar, sem gefin eru út fyrir notendur á bakslag af ökutækinu, skulu hægt að skiptast á við sjálfti handa ökumeðhöndlunandi fléttkorni sem er staðsett fyrir við húðhlið sem verður í sig á hlið innri rúms sem skilur R-stöðu fyrirsettrar.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eso:70 · P</summary>

**Source:** This is only the sixth of these huge storms to be spotted since 1876.
**Semantic decision:** P — Candidate6 retains only the sixth huge storm seen since1876.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [6]
**Candidate 0:** Þetta er aðeins sexustur þessara mikla storma sem sáust síðan 1876.
**Candidate 1:** Þetta er aðeins sjötind í sex stöku þessum risagerðum sem fyrir farið hefur verið síðan árið 1876.
**Candidate 2:** Þetta er aðeins sjöttni þessi umbreyktra slökkva á reynslu frá 1876.
**Candidate 3:** Þetta er aðeins sjötta af þessu mikilu stormi sem settar voru fram síðan 1876.
**Candidate 4:** Þetta er aðeins sjötta þessara eirra rjunanna sem komið hefur fram í gegnum 1876.
**Candidate 5:** Þetta er aðeins sjökthugur stormur sem hafa verið sýnt í sér frá 1876.
**Candidate 6:** Þetta er aðeins sjötta þessara mikla storma sem komist hægt að sjá síðan 1876.
**Candidate 7:** Þetta er aðeins sex af þessum umtalsverðum tölum sem sést hefur skoðað síðan 1876.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eso:501 · U</summary>

**Source:** The team used data from the UVES spectrograph on ESOs Very Large Telescope in Chile (to determine the properties of the star accurately), the Carnegie Planet Finder Spectrograph (PFS) at the 6.5-metre Magellan II Telescope at the Las Campanas Observatory in Chile, the HIRES spectrograph mounted on the Keck 10-metre telescope on Mauna Kea, Hawaii as well as extensive previous data from HARPS (the High Accuracy Radial velocity Planet Searcher) at ESOs 3.6-metre telescope in Chile (gathered through the M dwarf programme led by X. Bonfils and M. Mayor 2003–2010 described here).
**Semantic decision:** U — Several candidates retain names and sizes, but telescope/spectrograph and M-dwarf programme relations are not reliably faithful.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Hópurinn notuðu gögn úr UVES fyrirfarasjónauka Very Large Telescope ESO í Chile (til að ákvarða eiginleikar stjarnans nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5-metra Magellan II sjónauka á Las Campanas stjörnustöðinni í Chile, HIRES fyrirfarasjónauka á Keck 10-metra sjónaukinni í Mauna Kea, Hawaii ásamt skömmtum fyrirvara á HARPS (HARPS High Accuracy Radial velocity Planet Searcher) fyrir 3,6-metra sjónauka ESO í Chile (söfnuð í M dwarf prófun sem stóð fram á yfirhóp X. Bonfils og M. Mayor 2003-2010 sem lýst er hér.
**Candidate 1:** Hópurinn notuðu gögn úr UVES litrófsritunni á Very Large Telescope ESO í Chile (að því er varðar nákvæm eiginleikar stjarna), Carnegie Planet Finder Spectrograph (PFS) á 6,5 m litrófsritunni í Magellan II, Mauna Kea, Hawaii (búin í Las Campanas stjörnustöðinni í Chile) og HIRES litrófsrituna sem er á Keck 10 m litrófuntann í Mauna Kea, Hawaii sem og fjörtökunum gögnum frá HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6 m litrófuntann í Chile (þannig sem framkvæmd var með M-dvergumálinu (M dwarf programme) X. Bonfils og M. Mayor 2003–2010 sem lýst er hér).
**Candidate 2:** Hópurinn notuði gögn úr UVES litrófunarbúnaði Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjarna) Carnegie Planet Finder Spectrograph (PFS) á 6,5 m litrófunarbúnaði Magellan II á Las Campanas stjörnustöðinni á Chile, HIRES litrófunarbúnaði á Keck 10 m litrófunarbúnaði á Mauna Kea í Hawaii og líka stórum gögnum frá HARPS (High Accuracy Radial velocity Planet Searcher) í Chile á 3,6 m litrófunarbúnaði ESO (fert með M-dvergumælinum í 2003-2010 sem leitin hefur farið með X. Bonfils og M. Mayor 2003-2010).
**Candidate 3:** Hópurinn notuði gögn úr UVES litrófsritinu á Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjarna á nákvæmri hátt), Carnegie Planet Finder Spectrograph (PFS) á 6,5 metra Magellan II litrófsritinu á Las Campanas stjörnustöðinni á Chile, HIRES litrófsritinu á Keck 10 metra litrófsritinu á Mauna Kea á Hawai og líka mikil fyrri gögn úr HARPS (High Accuracy Radial velocity Planet Searcher) í Chile (til að koma með litrófsgögn í samræmi við M dwarf ferlið, frá 2003 til 2010, sem leitir X. Bonfils og M. Mayor 2003–2010, sem uppáð er hér).
**Candidate 4:** Lífræna samanburðarhópurinn notuði gögn úr UVES-geimsjónauki Very Large Telescope ESO í Chile (til að athuga eiginleikar stjarna á vissu) Carnegie Planet Finder Spectrograph (PFS) á 6,5-metrar Magellan II geimsjónauki í Las Campanas stjörnustöðinni í Chile, HIRES geimsjónauki í Keck 10-metrar geimsjónauki á Mauna Kea, Hawaii og lífi nóg af fyrri gögnum úr HARPS (High Accuracy Radial velocity Planet Searcher) í 3,6-metrar geimsjónauki ESO í Chile (sámskipti undir M dwarfs kynslögu, framkvæmd við X. Bonfils og M. Mayor 2003-2010 sem lýst er hér á).
**Candidate 5:** Teingin notaði upplýsingum frá UVES litrófi ESO Very Large Telescope í Chile (til að talinn eiginleika stjarnans nákvæmlega) PFS litrófarni Carnegie Planet Finder Spectrograph (PFS) á 6,5 m litrófi Magellan II á Las Campanas stjörnustöðinni í Chile, HIRES litrófið á Keck 10 m litrófi á Mauna Kea í Hawaii og öðrum mikiðum upplýsingum frá HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6 m litrófi ESO í Chile (fengin með M-dvergumælingum (M dwarf programme) X. Bonfils og M. Mayor 2003-2010 sem lýst er hér).
**Candidate 6:** Hópurinn notuði upplýsingum úr UVES mælinum á Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjarnans nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5 m magáranlegum Magellan II sjónauka í Las Campanas stjörnustöðinni í Chile, HIRES mælinum á Keck 10 m stjörnustjörnunni í Mauna Kea í Hawaii og lífrænt fyrri upplýsingum úr HARPS (High Accuracy Radial velocity Planet Searcher) í Chile í 3,6 m stjörnustjörnunni á ESO (settra með M dwarf hópnum, hóp X. Bonfils og M. Mayor 2003-2010 sem lýst er hér).
**Candidate 7:** Hópurinn notaði gögn úr UVES litrófi á Very Large Telescope ESO í Chile (til að ákvarða eiginleikastarfsemi stjarna á nákvæmlega) Carnegie Planet Finder Spectrograph (PFS) í Magellan II sjónauki í Las Campanas stjörnustöðinni í Chile, HIRES litrófið á Keck 10-metra sjónauka á Mauna Kea í Hawaii aukastiglega, nýanlega gögn úr HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6-metrar sjónauka ESO í Chile (sem fengist var á háttarferðinni fyrir líghæðarstjarna í 2003-2010 sem leiti X. Bonfils og M. Mayor 2003-2010 um hér fyrir sig).

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eea:1914 · P</summary>

**Source:** This Regulation shall enter into force on the third day following that of its publication in the Official Journal of the European Union.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Inspected / Correct indices:** [5] / [5]
**Candidate 0:** Reglugerð þessi öðlast gildi fyrri daginn eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.
**Candidate 1:** Reglugerð þessi öðlast gildi síðar en þriðja dag eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.
**Candidate 2:** Reglugerð þessi öðlast gildi þriðja daga eftir að hún var birt í Stjórnartíðindum Evrópusambandsins.
**Candidate 3:** Reglugerð þessi öðlast gildi þriðja dag eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.
**Candidate 4:** Reglugerð þessi öðlast gildi þriðja degi eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.
**Candidate 5:** Reglugerð þessi öðlast gildi á þriðja degi eftir að hún er birt í Stjórnartíðindum Evrópusambandsins.
**Candidate 7:** Reglugerð þessi öðlast gildi þriggja daga eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eso:464 · F</summary>

**Source:** With an estimated mass of four to five times that of Jupiter, it would be the least massive planet to be directly observed outside the Solar System.
**Semantic decision:** F — Estimated mass is changed to distance.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þegar það er fjarlægð sem er fjórar til fimm sinnum stærri en Júpíter væri það minnst massastærri reikistjarna sem hefur verið tekið beint sjón af utan sólarkerfisins.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eea:1552 · F</summary>

**Source:** The analytical result shall be reported as x +/– U whereby x is the analytical result and U is the expanded measurement uncertainty, using a coverage factor of 2 which gives a level of confidence of approximately 95 % (U = 2u).
**Semantic decision:** F — Expanded measurement uncertainty and coverage factor are mistranslated.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Greina skal niðurstöðuna sem x +/– U þar sem x er niðurstöðu greiningarinnar og U er útþekktur málstöfunarmall, með 2 gildi fyrir umfrymisfaktori, sem gefur til kynna um 95% öryggi (U = 2u).

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eso:1051 · F</summary>

**Source:** The technique used by Teague, which derived averaged variations in the flow of the gas as small as a few percent, revealed the impact of multiple planets on the gas motions nearer to the star.
**Semantic decision:** F — Flow variations are changed into average-density variations and multiple planets into diverse planets.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Tæknið sem Teague notaði, sem leiddi til meðalþéttni breytinga á flæði gassins sem var eins minni en nokkur prósent, benti í ljós áhrif fjölbreyttra reikistjarna á flæði gassins nálægt stjörnunum.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:ema:1765 · P</summary>

**Source:** Take this leaflet or some tablets with you so that your doctor knows exactly what you have taken.
**Semantic decision:** P — Taking leaflet or tablets so the doctor knows exactly what was taken is retained; grammar errors are minor.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Taktu þessi fylgiseðil eða töflur með þér svo að læknirinn veitist nákvæmlega hvað þú hefur tekið.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eso:768 · P</summary>

**Source:** Both components are classed as O-type stars.
**Semantic decision:** P — Both components being O stars is preserved; inflection errors are minor.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Bæði hlutin eru flokkaðar sem O- stjörnur.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:opensubtitles:2508 · F</summary>

**Source:** Rose, we have a guest in the living room.
**Semantic decision:** F — Living room is changed to the home.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Rose, við erum með gest í heimilinu.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eea:281 · F</summary>

**Source:** The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.
**Semantic decision:** F — Maturity band, former/latter matching and residual positions are corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Hlutfall fyrri (sáttmálans) sem samsvarar síðari (fyrri) í tilteknum útverkunarbólgum skal vera samsvarandi stöður í þeim bólgu, en hlutabúnaður á lengri eða styttri tíma skal vera ósamsvarandi stöður í sama bólgu.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:opensubtitles:3209 · P</summary>

**Source:** Because it's not safe there.
**Semantic decision:** P — Negated safety at that location is faithfully expressed as a natural reply; the explicit because connective is omitted.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Það er ekki öruggt þar.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eea:1991 · F</summary>

**Source:** Paragraph AG27 is amended and after paragraph AG29, paragraph AG29A is added.
**Semantic decision:** F — The AG prefixes identifying the amended paragraphs are lost.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Í 27. lið er breytt og eftir 29. lið bætist við 29. lið A.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eso:919 · F</summary>

**Source:** "Thanks to several giant telescopes currently under construction, including ESOs E-ELT and the NASA/ESA/CSA James Webb Space Telescope due to launch for 2018, we will soon be able to study the atmospheric composition of these planets and to explore them first for water, then for traces of biological activity.
**Semantic decision:** F — Construction, launch and atmospheric composition are corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** „Takinn er við nokkrum stórum sjónaukum sem eru í framhaldshús, þar meðtöldum ESO E-ELT og James Webb Space Telescope frá NASA, ESA og CSA sem koma til ramma árið 2018, getum við nánast hvarfisþéttni þessara reikistjarna og rannsaka þær fyrst með vatni, síðan með einkennum líffræðilegra virkni.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eea:1716 · U</summary>

**Source:** The competent authorities of Gabon have reacted promptly to these concerns, indicating their commitment to take all measures necessary to implement applicable ICAO standards and enforce compliance with these standards as soon as possible.
**Semantic decision:** U — Prompt response, commitment and ICAO action retained, but ensuring compliance versus making measures adequate is unclear.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Lögbær yfirvöld í Gabón hafa svarað þessum ábendingum tafarlaust og gefið til kynna að þau hafi skuldbindingu til að gera allar nauðsynlegar ráðstafanir til að framfylgja viðeigandi staðla ICAO og gera þær fullnægjandi eins fljótt og auðið er.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:opensubtitles:1169 · U</summary>

**Source:** They're pretty as can be, aren't they?
**Semantic decision:** U — Pretty/intensification becomes an unclear fine/maybe phrase.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þau eru fínt eins og kannski er, ekki satt?

</details>

<details><summary>t1000902 · greedy · p13official21:dev:ema:1718 · U</summary>

**Source:** Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.
**Semantic decision:** U — AUC and half-life changes retained; the P-gp inducer modifier remains unclear.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Samhliða gjöf edoxabans og P-gp örvaðs rífampicíns leiddi til minnkaðrar meðal AUC fyrir edoxaban og skerta helmingunartíma, sem getur valdið minnkun á lyfhrifum.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eso:491 · U</summary>

**Source:** ALMA can observe in different frequency bands.
**Semantic decision:** U — Frequency-related wording occurs, but frequency bands and the observing action remain unclear.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** ALMA getur athugað á mismunandi fyrirbæri.
**Candidate 1:** ALMA getur fylgt gegnum mismunandi tímamæri.
**Candidate 2:** ALMA getur rannsakað á mismunandi völdum.
**Candidate 3:** ALMA getur gakkt á mismunandi geislamagni.
**Candidate 4:** ALMA getur kynntið á mismunandi tíðnisamböndum.
**Candidate 5:** ALMA getur mælt á mismunandi fjölda árskors.
**Candidate 6:** ALMA getur metað í fleiri breytilegum beinbreytum.
**Candidate 7:** ALMA getur fylgst með tjónum á mismunandi fjölda fyrirbæra.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:opensubtitles:480 · U</summary>

**Source:** Now we have enough evidence to charge you with murder.
**Semantic decision:** U — Evidence/murder retained; skrá fyrir does not confidently establish the intended charge-with relation.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Nú hafa við nægilega sönnunargögn til að skrá þig fyrir morði.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eea:281 · F</summary>

**Source:** The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.
**Semantic decision:** F — Every candidate corrupts maturity bands and the former/latter matching or residual-position relation.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Fjöldi þeirra (frum) sem sem sem (sam) nema í fyrri (slík) stjórnast í tilteknu fullnægjandi vaxtarbruk, skal vera samhæft stöðurnar í þeirri vaxtarbruk, á sama hátt skal sú stöður sem ekki nema í samhæfi er sú stöðu í samhæfni.
**Candidate 1:** Hlutfall fyrri (sári) sem fyrirbyggja sér svörun fyrri (sári) í viðkomandi lífsgildið skulu vera svöruna stöður á þeirri lífsgildi, en hlutan álengd eða skammstöð valdið ósvöruna á þeirri lífsgildi.
**Candidate 2:** Hlutfall fyrri (sá eftirfarandi) sem samræmt er með sínu fyrri (sá fyrri) í tilteknum tíðniþætti skal vera samræmd staðsetningar í þessum þætti, en hlutfall eftirfarandi eða fyrri staðsetningar skal vera ósamræmd staðsetningar fyrir sama þætti.
**Candidate 3:** Það magn, sem fyrri (síðari) óseti, sem síðara (fyrri) samhengur, á tilteknum þrosklagsbili skal vera samhengur stöðurnar í þessum bili, meðan aðvinna langa eða stóra stöður skulu vera ósamhengdar stöðurnar í sama bili.
**Candidate 4:** Magn miðlaðrar (næmstri) sem eru samhengt við síðari (fyrari) miðlaðar miðlaðrar á viðkomandi alldagisköfnum skal vera samhengt staðahlutirnar í þessum sköfnum, en eftirfallin lengur eða styttri staðahlut skal vera ósamhengnd staðahluturinn fyrir sama sköfnum.
**Candidate 5:** Fjöldi fráfarna (nýfarna) sem samrýmast við henni (fráfarið) í þeim gildistærði sem kveðið er á um skal vera samrýmast stöðurnar í þeim gildistærði, svo sem gildistímaröskuð stöðurinn skal vera uppfærðar stöðurinn í það gildistærð.
**Candidate 6:** Höfnunarmagn þeirra sem eru samsvarandi á þann millimagn sem síðan (fyrri) er samsvarandi skal vera samsvarandi staðfestir í þessum millimagni, en hlutlaus staðfestir laga eða stærri skal vera ósamsvarandi staðfestir í sama millimagni.
**Candidate 7:** Hlutfall fyrri (sáttmars) sem sambærast fyrir viðmiðunarhóp sem sambærir sér er hlutfall sambærilega stöðvar í þeirri hópi, en eftirfylgni stöðu fyrir aðstæður um lengi eða stæku þá er hlutfall sambærilega stöður í samanburðarrófi.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:ema:1582 · P</summary>

**Source:** The treatment-free period, however, should take into account the pharmacological properties of the products used previously.
**Semantic decision:** P — Candidate6 retains the period without treatment and pharmacological properties of previously used drugs.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [6]
**Candidate 0:** Meðan á meðferðarfrasluminni ávallt skal taka tillit til lyfjafræðilegum eiginleikum lyfja sem er notað í forsendu.
**Candidate 1:** Meðferðarframanstundin skal þó hafa í huga lyfjafræðilegan eiginleikar lyfjanna sem notað hafa verið áður.
**Candidate 2:** Meðferðarframtíminn ætti þó að taka tillit til lyfjamannslegu eiginleika lyfja sem notaðir voru áður.
**Candidate 3:** Hins vegar ætti meðferðarfraslengdi að taka tillit til lyfjafræðilegrar eiginleika lyfja sem notuð voru áður.
**Candidate 4:** Þó skal taka í tillit til lyfjafræðilegar eiginleika lyfjanna sem höfði verið notuð áður.
**Candidate 5:** Meðferðarfráfalls ávinningin á að taka tillit til lyfjamenna eiginleika lyfinna sem notuð hafa verið áður.
**Candidate 6:** Meðan án meðferðar tíminn hefur að alveg í huga lyfjafræðileg eiginleikar lyfjanna sem notuð var áður.
**Candidate 7:** Meðferðarfrí meðferðarfríðum átökum skal þó taka tillit til lyfjafræðilegra eiginleika af vörunum sem notuð eru fyrir.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eso:924 · F</summary>

**Source:** ESO was delighted to welcome Italys Minister of Education, Universities and Research, H.E. Stefania Giannini, to the ceremony, which was also attended by the Italian Consul General in Munich, Renato Cianfarani, the ESO Council President, Patrick Roche, and the Italian ESO Council Delegates, Nicolò DAmico (who is also President of INAF) and Matteo Pardo, Scientific Attaché at the Italian Embassy in Berlin.
**Semantic decision:** F — Several attendees and institutional roles are omitted or changed.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** ESO var ánægð af því að viðtaka Stefania Giannini, ráðherra í menntun og vísindum í Ítalíu, sem var einnig á festinaði, sem samstarfsmenn ESO, Patrick Roche, og tilvísunarmenn ESO frá Ítalíu, Nicolò DAmico (sem er líka forseti INAF) og Matteo Pardo, vísindamennsja í hustru í Ítalíu í Berlín.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eso:775 · U</summary>

**Source:** A team of astronomers, led by Istvan Dékány of the Pontificia Universidad Católica de Chile, has now used data from this survey, taken between 2010 and 2014, to make a remarkable discovery - a previously unknown component of our home galaxy, the Milky Way.
**Semantic decision:** U — Candidate5 retains leadership, dates and a previously unknown part, but the home-galaxy/component construction is too unclear to certify.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Hópur stjarnvísindamanna, gefinn stjórn af Istvan Dékány frá Pontificia Universidad Católica de Chile, noti nýtta gögnum úr þessari rannsókn, sem gerð var á tímabilinu 2010-2014, til mjög mikilvægs uppgötvu - til þess að fá til út af því að það er fundið áður ekki, hlut af heimilidreiddi Vetrarbrautinni.
**Candidate 1:** Hópur stjarnvísindamanna, hjá stjörnufræðingum Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notuð gögnum af þessari rannsókn, sem gerð var á tímabilinu 2010 til 2014, til bæði innánlega vörunsins og sérfræðilega frábrugga hennar.
**Candidate 2:** Hópur stjörnufræðinga, gefinn stjórn af Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notuð gögn úr kortlagningunni, sem tóku sér stað á milli 2010 og 2014, til að koma fram aukin þrýsting Heimastjörnu, Vetrarbrautarskynnar.
**Candidate 3:** Hópur stjörnufræðinga, yfir skipana Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nýlega notað gögnum úr þessum mælingum, sem áttust um tímabilinu 2010 til 2014 til að gera mikilvægt uppgötvun - nýtt aðalhlið í heimalauna okkar, Vetrarbrautarinni.
**Candidate 4:** Hópur stjörnufræðinga, undir forystu Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notað gögnum úr þessari rannsókn, sem stóð undir 2010-2014, til að gera mikilvæga uppgötvun - yfirleitt óþekkt þýði á heimalaust vetrarbrautarinni.
**Candidate 5:** Hópur stjörnufræðinga, undir forystu Istvan Dékány frá Pontificia Universidad Católica de Chile, notið gögnum úr þessari skoðun, sem gerð var 2010-2014, til þess að fá skilvirkri uppgötvun - þann hluti af heimakjörinu, Vetrarbrautarinnar, sem var aldrei vitað.
**Candidate 6:** Hópur stjörnufræðinga, sem stjörnufræðingur Istvan Dékány frá Pontificia Universidad Católica de Chile leidur, hefur nú notað gögn úr samanburðarins sem fengist var á tímabilinu 2010 til 2014 til að koma fram mikilvægar upptöku - sem var aðra í gegnum sinn um að það sé einstakleiðandi hluti húðraðarvöldsins, stjörnumerminn Vetrarbrautin.
**Candidate 7:** Hópur stjörnufræðinga, leitt af István Dékány við Pontificia Universidad Católica de Chile, hefur nú notuð niðurstöður þessarar skoðunar, sem tómist á aldrinum 2010 til 2014, til frábæra uppgötvunar - aðalhlutverk heimsverðra vetrarbrautarinnar, vetrarbrautinnar.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eea:15 · F</summary>

**Source:** Where studies are conducted using active substance produced in the laboratory or in a pilot plant production system, the studies must be repeated using active substance as manufactured, unless it can be justified that the test material used is essentially the same for the purposes of environmental testing and assessment.
**Semantic decision:** F — All eight lose the pilot-production distinction and/or corrupt the essential-equivalence exception and environmental-testing purpose.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Ef rannsóknir eru framkvæmdar með virk efni sem framleitt er í rannsóknarskírteini og í prófunarhúsa verða þær að rífa með virk efni eins og hann er framleitt, nema það unnt sé að rökstýra að prófunarefnið sé í alvöru samanborið við úrprófunarsemi við umhverfisrannsóknir.
**Candidate 1:** Ef rannsóknir eru gert með virkum efni sem myndast í húsi, eða í anlegum framleiðsluverum, þarf að endurtaka rannsóknirnar með virkum efni sem myndast eftir framleiðslu, nema það sé víxlur á því að rannsóknarefnið, sem notuð er, sé næstum eins fyrirhugaðtilmæli við umhverfisrannsóknir og mats.
**Candidate 2:** Ef rannsóknir eru gerðar með virka efni sem framleitt er í rannsóknarstöðum eða í reynslustöðum skal endurskoða rannsóknina með virku efni eins og það er framleitt, nema virku efnið sé áframhaldssamhæfð í þeim tilgangi að það sé nákvæmlegt eðlilegt efni fyrir umræður á umhverfisáritun og áritun.
**Candidate 3:** Ef rannsóknir eru framkvæmdar með virkum efni sem framleitt er í rannsóknarstofu eða í fyrirvinnuframleiðslueftirfarðar, skal endurskoða rannsóknirnar með virkum efni eins og þetta er framleitt, nema hún geti verið rökstudd að prófunarefnið sem notað er sé í í grunnvirkum skyni við umhverfisrannsóknir og mat.
**Candidate 4:** Ef rannsóknir eru gerðar með virkum efni sem framleitt er í rannsóknarstofu eða í fyrirtækisverkunartæki, ætti að endurtaka rannsóknina með virkum efni eins og sem það er framleitt, nema valdið sé áður því að prófunarefnið sé í raun háttjarna sambærilegt við umhverfissýsla og mat.
**Candidate 5:** Ef rannsóknir eru gerðar með virka efninu, sem framleitt er í rannsóknarstofu eða í framleiðsluverkefni sem notuð er í fyrirtækjasambandi, verður að endurskoða rannsóknina með virku efninu sem framleitt er, nema framkvæmdin getur komið fram á að prófunarefnið sem notuð er sé í raun samsvarslega í umhverfisprófunum.
**Candidate 6:** Ef rannsóknir eru framkvæmdar með virkum efni sem framleidd er í rannsóknarstofu eða í forhætti og framleiðsluverklun, skal endurtaka rannsóknina með virkum efnum eins og þau eru framleidd, nema hægt sé að rökstýra að prófunarvörunni sem notað er sé aðeins það sama fyrir umhverfisskyldun og mat.
**Candidate 7:** Ef rannsóknir eru gerðar með virka efni sem framleitt er í rannsóknarstofu eða í rannsóknarstofuhúðar verka verða þarf rannsóknirnar endurskoðar með virku efni eins og framleiðið er, nema það sé hægt að ræða að prófunarfyrrandi efnið sé essið að því er varðar umhverfisskyldur.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eso:302 · F</summary>

**Source:** This is because the tilt of the orbit is normally unknown.
**Semantic decision:** F — No candidate preserves orbital tilt; alternatives refer to unrelated movement, quantities or objects.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Það er vegna þess að hliðra kringliðarinnar er venjulega óþekkt.
**Candidate 1:** Það er vegna þess að stojakilt grunnrækslanar er venjulega ekki þekkt.
**Candidate 2:** Það er vegna þess að bláæðin er venjulega óþekkt.
**Candidate 3:** Þetta er vegna þess að þjóðorháttur hringrar er venjulega ekki þekkt.
**Candidate 4:** Það er vegna þess að hálfalengd hringrarinnar er yfirleitt óþekkt.
**Candidate 5:** Það er vegna þess að ástæðan í umferminu er fyrir góðu tilstilli óþekkt.
**Candidate 6:** Þetta er vegna þess að fækkun hreyfsins er yfirleitt ekki þekkt.
**Candidate 7:** Þetta er vegna þess að um nálarvegsstöðunni er venjulega ekki vitað.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eso:206 · F</summary>

**Source:** The survey was sensitive to planets between 75 million kilometres and 1.5 billion kilometres from their stars (in the Solar System this range would include all the planets from Venus to Saturn) and with masses ranging from five times the Earth up to ten times Jupiter.
**Semantic decision:** F — Seven candidates have wrong distance magnitudes; candidate4 fixes billion but loses the five-Earth-mass lower bound and corrupts the Solar-System qualifier.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Skoðunarmiðið fannist næm fyrir reikistjörnur á bilinu 75 milljón km til 1,5 milljón á milli stjörnu (í sólkerfinu fingi það allar reikistjörnurnar frá Venus til Saturn) og yfirborði voru vistskvæða úr fyrstum jörðar til tíu fyrir Júpíter.
**Candidate 1:** Skýrslugjöfin var næm fyrir reikistjörnum á milli 75 milljónum og 1,5 milljónum kílómetra frá stjörnunum (á sólkerfinu voru þessi svið borið allar reikistjörnurnar frá Venus til Saturns) og þeim sem tókst af fimm til tíu gildum Júpíters.
**Candidate 2:** Slíkt rannsókn var næm fyrir reikistjörnur milli 75 milljón kílómetra og 1,5 milljón kílómetra frá stjörnurnar (í sólkerfinu fylli hún öll reikistjörnurnar frá Venus til Saturna) og af heildarmassa á milli fimm sinnum þjóðar og tíu sinnum Júpítra.
**Candidate 3:** Til greiningar voru fjarreikistjörnur margar milljónum á milli 1 tíma milljónar kílómetra frá stjörnunni (í sólkerfinu catches allur fjarreikistjörnurnar frá Venus að Satúri) og þeir hvetta vart í fimm þrepu jörðar upp í tíu þrepu Júpíturnar.
**Candidate 4:** Rannsóknin var næm við reikistjörnur sem eru á milli 75 milljón km og 1,5 milljarða km frá stjörnunum (í sólarssjóarnafinu þyrir þess allar reikistjörnurnar frá Venus til Sáters) og miðað við massafjölda sem var fimm sinnum yfir og eitt tíu sinnum yfir Júpíturni.
**Candidate 5:** Skoðanirnar höfðu nákvæmni við reikistjörnur á bilinu 75 milljón km til 1,5 milljón milljón km frá stjörnunum (í sólarssjónarfræðinu vegi allar reikistjörnurnar frá Venus og í saman burtu af Saturni) og með massamagni á bilinu fimm sinnum fyrir upphafssvæði árið til tíu sinnum fyrir Júpítur.
**Candidate 6:** Rannsóknin var næm fyrir reikistjörnur í milli 75 milljón km og 1,5 milljórn km frá stjörnunum (í sólkerfinu fylgi þess allar reikistjörnurnar frá Vensu til Soturs) og með massalimma frá fimm sinnum jörðu að tíu sinnum Júpíturnum.
**Candidate 7:** Skoðunin var nægileg fyrir reikistjörnur milli 75 milljón km og 1,5 milljón km frá stjörnurnar (í sólkerfinu farið eru allar reikistjörnurnar frá Vensu til Saturn) og á massafjölda þar til fyrir fyrir fimm sinnum jörðnum upp í tíu sinnum Júpíturnum.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eea:1585 · P</summary>

**Source:** The Commission shall submit a final evaluation report at the end of the Programme.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Inspected / Correct indices:** [0, 5] / [0, 5]
**Candidate 0:** Framkvæmdastjórnin skal leggja fram endanleg matsskýrslu að lokum áætlunarinnar.
**Candidate 1:** Framkvæmdastjórnin skal leggja fram endanleg mataráðgerð eftir að áætlunin er lokið.
**Candidate 2:** Framkvæmdastjórnin skal leggja fram endanlega matsskýrslu við lok áætlunarinnar.
**Candidate 3:** Framkvæmdastjórnin skal leggja fram endanlega matsskil á lokum áætlunarinnar.
**Candidate 5:** Framkvæmdastjórnin skal leggja fram endanlega matsskýrslu eftir að áætlunin er lokið.
**Candidate 6:** Framkvæmdastjórnin skal leggja fram endanlega ávísaða sk r á um endanlega mat eftir að áætlunin liggur af.
**Candidate 7:** Framkvæmdastjórnin skal leggja fram endanlegar matarannsóknaráðskrif við lok áætlunarinnar.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:ema:325 · F</summary>

**Source:** If you get lower abdominal pain, gain any weight rapidly, feel sick or are vomiting or if you have difficulty in breathing, talk to your doctor straight away who might ask you to stop using this medicine (see in section 4 under “Serious side effects”).
**Semantic decision:** F — Stopping the medicine is changed into using it; symptom details are also corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Ef þú færð magaverk, þyngdar hraðlega, finnur fyrir uppköstum eða þrýstir, eða hefur í þröskulda öndun, skaltu tafarlaust ræða við lækninn sem kann að kveikja þig að nota lyfið (sjá kafla 4 undir „Alvarlegar aukaverkanir“).

</details>

<details><summary>t1000902 · G8 · p13official21:dev:ema:1192 · P</summary>

**Source:** It is used to prevent pregnancy.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Inspected / Correct indices:** [1] / [1]
**Candidate 0:** Hún er notað til að koma í veg fyrir þungun.
**Candidate 1:** Það er notað til að koma í veg fyrir þungun.
**Candidate 3:** Það er notað til að drega úr því að þungun kemur.
**Candidate 5:** Það er notað til að forðast þungun.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:ema:767 · P</summary>

**Source:** Therefore, docetaxel must not be used during pregnancy unless clearly indicated.
**Semantic decision:** P — Candidate0 retains the pregnancy prohibition with an exception only when a clear need arises.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [0]
**Candidate 0:** Því má ekki nota docetaxel meðan á meðgöngu stendur nema myndist greinilega þörf.
**Candidate 1:** Því má ekki nota docetaxel á meðgöngu nema sprauta sé tilkynnt á tæka hátt.
**Candidate 2:** Því má ekki nota doketaxel á meðgöngu nema fyrir hægt sé að tilgreina það.
**Candidate 3:** Þar af leiðandi má ekki nota docetaxel á meðgöngu nema það sé tilgreint skýrt.
**Candidate 4:** Því má ekki nota docetaxel á meðgöngu nema að því er skýrt tilskipun.
**Candidate 5:** Því verður ekki að nota dócetaxel á meðgöngu nema ávísað sé hægt.
**Candidate 6:** Því má ekki nota dócetaxel á meðgöngu nema brýna sjálfstætt mælt sé fyrir um.
**Candidate 7:** Því má ekki nota dócetaxel á meðgöngu nema skýrt séð til um.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eso:323 · F</summary>

**Source:** They were able to make the sharpest direct observation ever , of the centre of a distant galaxy, the bright quasar 3C 279, which contains a supermassive black hole with a mass about one billion times that of the Sun, and is so far from Earth that its light has taken more than 5 billion years to reach us.
**Semantic decision:** F — Both billion quantities become million and black-hole content is lost.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þeir komu að skarpsmári beinu sjónauki á miðju fjarreikisvetrarbrauta, 3C 279, sem er björtur kvarnarmiði með massu sem er um milljón sinnum stærri en sólin og er svo langt frá Jörðinni að ljósið hafa tekið meira en 5 milljón ára til okkar.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:eea:50 · F</summary>

**Source:** Similar studies, for at least three soil types, must be reported for all relevant metabolites, degrada tion and reaction products which in soil degradation studies account at any time for more than 10 % of the amount of active substance added.
**Semantic decision:** F — Soil types, reaction products and the any-time quantitative condition are corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Í öllum þeim rannsóknum sem hafa að minnsta kosti þriggja grunnflokka verður að greina frá jafngildum rannsóknum fyrir öll viðkomandi umbrotsefni, brotthvarf og hlutverki sem í rannsóknum á brotthvarfi grunnar nýta yfirleitt meira en 10% af skammti virku efna sem bætt er við.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:ema:1718 · P</summary>

**Source:** Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.
**Semantic decision:** P — Candidate2 retains P-gp-inducer rifampicin, decreased mean edoxaban AUC, shorter half-life and possible reduced pharmacodynamic effects.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [2]
**Candidate 0:** Samhliða gjöf edoxabans ásamt P-gp örvaðilum, rifampicini, leiddi til minnkaðs mína AUC for edoxabani og skerta helmingunartíma, sem gæti haft mögulega fækkunar á lyfhrifum.
**Candidate 1:** Samhliða gjöf edoxabans og viðbótarvirkra P-gp ruglaði rifampicin leiddi til minnkuðs meðal AUC fyrir edoxaban og styttri helmingunartíma, sem getur dregið úr lyfhrifum.
**Candidate 2:** Notkun edoxabans samtímis rifampicíni, P-gp örva, leiddi til minnkar meðal AUC fyrir edoxaban og minnkunar helmingunartíma, sem hugsanlega minnkaði lyfhrif.
**Candidate 3:** Samhliða lyfjagjöf edoxabans og P-gp örva rífampicíns leiddi til þess að meðaltal AUC fyrir edoxaban minnkaði og haldaði skilun halda, með hugsanlega minnkun á lyfhrifum.
**Candidate 4:** Samhliða notkun edoxabans og P-gp örvuðleysa (P-gp inducer) rífampicins leiddi til að minnka meðal AUC fyrir edoxaban og skoðaði sköpun á helmingunartíma, sem geta verið að færa minni lyfhrifum þess.
**Candidate 5:** Notkun edoxabans samtímis rifampicíni, P-gp örvuhvítandi lyfi, leiddi til minnkaðrar meðal AUC fyrir edoxaban og skerðingar á helmingunartíma, sem getur valdið minnkun á lyfhrifum.
**Candidate 6:** Samhliða gjöf edoxabans og P-gp örvaðs rifampicins leiddi til minnkaðrar meðal AUC fyrir edoxaban og skerta helmingunartíma, sem hugsanlega leiddi til minnkaðrar lyfhrifar.
**Candidate 7:** Samhliða lyfjagjöf edoxabans og P-gp virkjaða rífampicíns leiddi til minnkaðs meðal AUC fyrir edoxaban og styttingar helmingunartíma, sem getur haft minnkuð áhrif lyfsins.

</details>

<details><summary>t1000902 · greedy · p13official21:dev:opensubtitles:3607 · F</summary>

**Source:** Well, that makes you ugly and stupid.
**Semantic decision:** F — Ugly is changed to strange.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Það gerir þig skrítn og heimskur.

</details>

<details><summary>t1000902 · G8 · p13official21:dev:eea:2037 · U</summary>

**Source:** Those criteria should not be considered to be exhaustive.
**Semantic decision:** U — Negation retained, but exhaustive/complete versus perfect/adequate wording remains uncertain.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Þær viðmiðanir skulu ekki talið fullkomi.
**Candidate 1:** Þessi viðmiðanir skulu ekki teljast nákvæmar.
**Candidate 2:** Þessar viðmiðanir skulu ekki teljast fullkomlegar.
**Candidate 3:** Ekki skal telja þessi viðmiðanir fullkomlar.
**Candidate 4:** Ekki skal telja þessar viðmiðanir fullkomlega.
**Candidate 5:** Ekki skal telja þessar viðmiðanir fullkomlegar.
**Candidate 6:** Sem ekki séu upplýstri sú kennsluviðmiði.
**Candidate 7:** Ekki skal telja þær viðmiðanir alveg upplausn.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:opensubtitles:3607 · F</summary>

**Source:** Well, that makes you ugly and stupid.
**Semantic decision:** F — Ugly is changed to strange.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Það gerir þig skrítn og heimskur.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eea:698 · U</summary>

**Source:** Only days that can be worked should be included when Saturdays and Sundays are not worked they should not be included, the same with public holidays).
**Semantic decision:** U — The workable-day condition is partly recognizable but weekend/public-holiday exclusions are not reliably clear.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Aðeins þarf að taka til daganna sem má vinna að því er gögn fylgja sára og sunnudögum eigi að það sé talað, sem somi heimildar- daga).
**Candidate 1:** Einungis skal taka til daga sem má vinna í þeim dagsetningu sem cifur ekki staðið á laugardaginn og laugardaginn, en ekki í þeim dagsetningu sem cifur ekki staðið í laugardaginn, og sama er við opinbera losunarheimdar).
**Candidate 2:** Aðeins daga sem má vinnja skal taka með í aðalframanum en ekki daga með stundum laugardags eða laugardagsdagsins þegar það er ekki laugardagur, eins og opinbera fríadagur).
**Candidate 3:** Einnig aðeins dagar sem má virka skulu ítarlega, ef sára og sunnudagur er ekki virkt skulu þau ekki vera ítarlega, sami við almennt fríar).
**Candidate 4:** Einungis skal taka til daga sem má vinna og ekki einu sinni dögum sem ekki ræði að vinna skal ekki taka til þeirra, svo og opinbera fríar).
**Candidate 5:** Einnig skal taka bara dagir sem má auðvelda er þegar ekki er að vinna á laugardagum og laugardagum, og sama við opinbera frídddagana).
**Candidate 6:** Einungis skal taka til daga sem hyggja má vinnu að þeim skal ekki taka til daga sem ekki er vinnuð á laugardagum og sáttmædagjöfum (reikandi dagum).
**Candidate 7:** Aðeins þær daga skulu tekið til meðferðar þegar ekki er sett að vinna á laugardagum og sunnudagum, að því er varðar opinbera fríadagana).

</details>

<details><summary>t1500729 · greedy · p13official21:dev:opensubtitles:1159 · F</summary>

**Source:** Somebody get me a picture of the girl.
**Semantic decision:** F — The receiver me is missing from the request to obtain a picture.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Einhver fá mynd af stúlkunni.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eso:726 · U</summary>

**Source:** They wanted to study the interaction between a young generation of stars and the cold clumps that were assembling into these first galaxies.
**Semantic decision:** U — Young stars and cold clumps retained, but assembling into the first galaxies is still unclear.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þeir vildu rannsaka milliverkun á yngri stjörnuhópi og kaltum klumpum sem var að skipta saman í þessum fyrstu vetrarbrautum.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eso:775 · F</summary>

**Source:** A team of astronomers, led by Istvan Dékány of the Pontificia Universidad Católica de Chile, has now used data from this survey, taken between 2010 and 2014, to make a remarkable discovery - a previously unknown component of our home galaxy, the Milky Way.
**Semantic decision:** F — Every candidate materially corrupts the previously unknown component of the home galaxy or the discovery/leadership relation.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Hópur stjörnufræðinga, undir forystu Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notað gögnum úr þessari rannsókn, sem gerð var á tímabilinu 2010-2014, til að gera mikilvægri uppgötvun - og gagnsæi sem hefur ekki orðið þegar fyrir á, sem er í heimaveröndunum okkar, Galdrabirginu.
**Candidate 1:** Hópur stjörnufræðinga hjá Pontificia Universidad Católica de Chile, frá ledum Istvan Dékány, hefur fengið gögn frá þessari rannsókn, sem tóku sér stað á milli 2010 og 2014, til að gera skjóttar uppgötvun – einstöku þátttaka okkar himnhalds, vísnar.
**Candidate 2:** Hópur stjörnufræðinga, gefnu félagi Istvan Dékány hjá Pontificia Universidad Católica de Chile, hefur nýlega notið gögn úr þessari tæknifari, sem tóku sér stað á milli 2010 og 2014, til uppgjörs - þar sem áttistu óvæntur þátt í vetrarbrautinni okkar, Vetrarbrautarinni.
**Candidate 3:** Hópur stjörnufræðinga, leit frá Istvan Dékány, Pontificia Universidad Católica de Chile, notaði gögn úr þessari rannsókn, sem gerð var á milli árs 2010 og 2014, til að koma á tilfinningu - voruplan i vetrarbrautarannum sem ekki var vitað um fyrir hlið.
**Candidate 4:** Hópur stjörnufræðinga, undir forystu Istvan Dékány og Pontificia Universidad Católica de Chile, hefur nú notað gögn úr þessum rannsókn, sem gerð var 2010 til 2014, til að koma að óvart þekktu mörkuðu þátti í Vetrarbrautinu okkar.
**Candidate 5:** Hópur stjörnufræðinga, undir forystu Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nú notuð gögn úr slímu mælingum, sem gerðir voru á milli 2010 og 2014, til þess að gera mikilvægt uppgötvun - aðra, sem ekki hefur verið þekkt, aðstandandi þjóð- kvarða okkar, Vetrarbrautarinnar.
**Candidate 6:** Hópur stjörnufræðinga, sem ferðast á stjörnuprófi sem Isztvan Dékány fór að hað í Pontificia Universidad Católica de Chile, hefur nú samanborið gögn úr, sem gnittastarfandi verið, af þessari myndun, á meðan á henni stóð, á milli 2010 og 2014, að því er varðar aðeins óþekkt lykilþátt í heimakjörinu, Vetrarbrautinu.
**Candidate 7:** Hópur stjörnufræðinga, leitt af István Dékány við Pontificia Universidad Católica de Chile, hefur nú notuð niðurstöður þessarar skoðunar, sem tóku sér stað á milli 2010 og 2014, til að gera frákomin uppgötvun - fyrir hinn sýnt hluta Vetrarbrautarinnar.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eea:50 · F</summary>

**Source:** Similar studies, for at least three soil types, must be reported for all relevant metabolites, degrada tion and reaction products which in soil degradation studies account at any time for more than 10 % of the amount of active substance added.
**Semantic decision:** F — Soil types, degradation/reaction products and quantitative qualifying relation are corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Í öllum þeim rannsóknum sem hafa að minnsta kosti þriggja grunnflokka verður að greina frá jafngildum rannsóknum fyrir öll viðkomandi umbrotsefni, leysingu og hlutabreytingar sem í rannsóknum á leysingu grunnflokka gefa stærri en 10% af skömmtum virku efna sem bætt eru upp.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:ema:2013 · P</summary>

**Source:** There is no evidence to suggest that eptotermin alfa alters fertility.
**Semantic decision:** P — No evidence of an eptotermin alfa effect on fertility retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Engin merki benda til þess að eptotermin alfa hafi áhrif á frjósemi.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eso:464 · U</summary>

**Source:** With an estimated mass of four to five times that of Jupiter, it would be the least massive planet to be directly observed outside the Solar System.
**Semantic decision:** U — Mass range and direct viewing are recognizable, but least-massive construction is not clear enough to certify.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þegar það er með fjögur til fimm sinnum þyngri massu en Júpíter væri það minnst þyngstu reikistjarna sem hefur verið tekið beinu sjón af utan sólkerfisins.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eea:1194 · F</summary>

**Source:** It should provide the Commission and the Member States with objective, reliable and comparable information and data on maritime safety and on ship pollution prevention to enable them to take any necessary initiatives to enhance the measures in place and to evaluate their effectiveness.
**Semantic decision:** F — Objective/reliable information is not retained, despite improved ship-pollution wording.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Hún skal veita framkvæmdastjórninni og aðildarríkjunum vísanir og gögn sem eru áframhaldsnæg og samanburðarhæfar um öryggi á sjávarbærum og um aðferðir til að koma í veg fyrir mengun af skipum til þess að þau geti tekið nauðsynlegar aðgerðir til að auka ráðstafanir sem eru í gildi og meti skilvirkni þeirra.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eea:15 · F</summary>

**Source:** Where studies are conducted using active substance produced in the laboratory or in a pilot plant production system, the studies must be repeated using active substance as manufactured, unless it can be justified that the test material used is essentially the same for the purposes of environmental testing and assessment.
**Semantic decision:** F — Every candidate loses the pilot-production-system distinction or corrupts the equivalence exception/environmental-testing purpose.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Ef rannsóknir eru framkvæmdar með virk efni sem framleitt er í rannsóknarkerfi í vinnslustöðum eða í prófunaraðstæðum á rannsóknarkerfi verði á að endurtaka rannsóknirnar með virk efni eins og það er framleitt, nema útsettum úrprófunarefni sé áður skýrt að það sé í öflugu samræmi við umhverfisprófunina.
**Candidate 1:** Ef rannsóknir eru gert með virkum efni sem verða framleitt í rannsóknarkerfi í stofninu eða í vettvangarkerfi, verða rannsóknirnar endurtekin með virkum efni eins og þau er framleidd, nema það sé greinilegt að prófunarvörunin, sem er notaður, sé aðallega svipuð fyrir umhverfisrannsóknir og mat.
**Candidate 2:** Ef rannsóknir eru gerðar með virka efni sem er framleitt í rannsóknarstöðum eða í reynslustöðum skal endurskoða rannsóknina með virku efni eins og það er framleitt, nema virku efnið sé áthríða sambærilegt í umhverfisrannsóknir og -vottorðir.
**Candidate 3:** Ef rannsóknir eru gerðar með virka efni sem framleitt er í rannsóknarstöðum eða á vettvangi, verða þær endurtökum, með virku efni sem eru framleitt, nema fram kemi rétttaki um að prófunarfjöldaði sem notað er sé jafn virkt að því er varðar umhverfismati.
**Candidate 4:** Ef rannsóknir eru gerðar með virkum efni sem eru framleidd á vinnsluverum milli, upprunum, í rannsóknarkerfi, þarf að endurtaka rannsóknina með virkum efni eins og það er búið að framleiða, nema verði hægt að rökstýra að prófunarefnið, sem notað er, sé aðallega það sama við umhverfiseftirlit og mat.
**Candidate 5:** Ef rannsóknir eru gerðar með virka efninu, sem er framleitt í rannsóknarstofu eða í framleiðsluverkefni sem notuð er í aðalrannsóknarmál, skal endurtaka rannsóknina með virka efninu sem það er framleitt, nema það sé auðkennað að prófunarmatið, sem er notað, sé í raun samtímis í umhverfismálum og mati.
**Candidate 6:** Ef verkefni eru gerðar með virka efni sem framleitt er í rannsóknarstofu eða í forlínuferlisstöfunarmiða, verður að endurtaka rannsóknarnar með virku efni eins og það er framleitt, nema staðfesta sé að prófunarefnin sé í ítarlegu tilvikum sambærilegt við prófunar- efnið sem notuð er við umhverfisrannsóknir og mat á.
**Candidate 7:** Ef rannsóknir eru gerðar með virka efni sem framleiðið er í rannsóknastofunni eða í áætlunarstofnun, þarf að endurtaka rannsóknina með virka efni eins og það er framleitt, nema fundist sé rétt fyrir að prófunarinnihaldsefnið, sem er notað, sé í heittanlegu hluta sá sama ef ragð er að rannsóknir á umhverfi.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eea:922 · P</summary>

**Source:** Development of CPE is checked as described in Part I.III.4.
**Semantic decision:** P — Candidate1 describes investigating CPE development with the correct nested PartI/III/4 reference.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [1]
**Candidate 0:** Ekki er gerð annaðhvort varðandi þróun CPE sem lýst er í lið II. III. 4 í I.
**Candidate 1:** Rannsókn á þróun CPE er farið fram samkvæmt grein 4 í III. hluta I. þeirrar skipulagi sem sett er fram.
**Candidate 2:** Frekari þroska CPE er lyst í þeim málum sem ræða er í III.4. hluta I. hlið.
**Candidate 3:** Framdæling CPE er vaktað eins og lýst er í IV-lið III. hluta I. hlið.
**Candidate 4:** Framkvæmd CPE er kannað í samræmi við það sem kveðið er á um í hluta I.III.4.
**Candidate 5:** Meðferð varðar þróun á CPE eftir því sem lýst er í hluta I.III.4.
**Candidate 6:** Framkvæmd CPE er metið eins og lýst er í lið III.4 í I. hlið.
**Candidate 7:** Þókun CPE er metið eins og lýst er í lið III.4 í hóp I.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eso:501 · U</summary>

**Source:** The team used data from the UVES spectrograph on ESOs Very Large Telescope in Chile (to determine the properties of the star accurately), the Carnegie Planet Finder Spectrograph (PFS) at the 6.5-metre Magellan II Telescope at the Las Campanas Observatory in Chile, the HIRES spectrograph mounted on the Keck 10-metre telescope on Mauna Kea, Hawaii as well as extensive previous data from HARPS (the High Accuracy Radial velocity Planet Searcher) at ESOs 3.6-metre telescope in Chile (gathered through the M dwarf programme led by X. Bonfils and M. Mayor 2003–2010 described here).
**Semantic decision:** U — Several names and sizes retained, but telescope/spectrograph and programme relations remain linguistically unreliable.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Hópurinn notaði gögn úr UVES víðblástur ESO Very Large Telescope í Chile (til að fá nákvæma upplýsingar um stjörnuna), Carnegie Planet Finder Spectrograph (PFS) á 6,5 metra Magellan II víðblástur í Las Campanas stjörnustöðinni í Chile, HIRES víðblástur, sem er á Keck 10 metra víðblástri á Mauna Kea á Hawaii, og mollega garna gögn úr HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6 metra víðblástri ESO í Chile (safaðin með M dwarfs verkefni leit hefðbundinni X. Bonfils og M. Mayor á tímabili 2003-2010 sem lýst er hér).
**Candidate 1:** Hópurinn notuðu gögn úr UVES litrófsritunni Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjörnunnar nákvæmlega) Carnegie Planet Finder Spectrograph (PFS) á 6,5 metra Magellan II stjörnustjörnunni í Las Campanas stjörnustöðinni í Chile, HIRES litrófsritunni, sem er á Keck 10 metra stjörnustjörnunni í Mauna Kea í Hawaii, og vandlega fyrri gögn úr HARPS litrófamælitilgreinunni (High Accuracy Radial velocity Planet Searcher) á 3,6 metra stjörnustjörnunni ESO í Chile (fjallandi með áætluninu M dwarfs sem stjórnast af X. Bonfils og M. Mayor 2003-2010 sem lýst er hér).
**Candidate 2:** Hópurinn notaði gagna úr UVES litrófið á Very Large Telescope ESO í Chile (til að meta eðlilegan eiginleika stjarna), Carnegie Planet Finder Spectrograph (PFS) á 6,5 m Magellan II skjöl við Las Campanas stjörnustöðinni í Chile, HIRES litrófið á Keck 10 m skjólin í Mauna Kea í Hawaii, ásamt mjög mikiðum gagnum frá HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6 m skjólin ESO í Chile (sáttmálann var beint til með M daufu áframhaldslýsingum sem leiddu X. Bonfils og M. Mayor 2003–2010 og lýst er hér).
**Candidate 3:** Hópurinn notaði þau gögn úr UVES-geislunartækið á Very Large Telescope (VLT) ESO í Chile ( til að mæla árangrir stjarna á nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5 metra Magellan II sjónaukanum í Las Campanas stjörnustöðinni á Chile, HIRES geislunartækið á Keck 10 metra sjónaukanum í Mauna Kea á Hawaii og líka mikilvægum gögnum úr HARPS (High Accuracy Radial velocity Planet Searcher) sem ESO hefur í 3,6 metra sjónaukanum í Chile (sérstakar frá stjörnu rannsókninni MEPS (MEPS for M dwarfs) sem stjórnað er af X. Bonfils og M. Mayor á tímum 2003-2010 sem lýst er hér fyrir frá).
**Candidate 4:** Líkamsrannsóknin varð vaxtarfelldar gögn úr UVES-geimsjónaukinni ESO Very Large Telescope á Chile (til að meta eiginleika stjarna á betur marki) Carnegie Planet Finder Spectrograph (PFS) á 6,5 meðal Magellan II geimsjónaukinni í Las Campanas stjörnustöðinni á Chile, HIRES geimsjónaukinni á Keck 10 meðal Mauna Kea á Hawaii, sem og mjög mikil skjaldkökutæki HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6 meðal geimsjónaukinni ESO í Chile, sem safnað var undir M dwarfs kynslögu með framfæri X. Bonfils og M. Mayor 2003-2010 sem lýst er hér.
**Candidate 5:** Teingin notaði gagna frá UVES gæslustafni Very Large Telescope ESO í Chile (til að talsta vera á eiginleika stjörnu), Carnegie Planet Finder Spectrograph (PFS) á Magellan II sjónaukinni í Las Campanas stjörnustöðinni í Chile, HIRES gæslustafnið á Keck 10-metrarjónunni í Mauna Kea á Hawaii sem og mikilvæga gagna frá HARPS (High Accuracy Radial velocity Planet Searcher) við 3,6 m jónunni í Chile (samtaka var frá M dwarfs verkefni X. Bonfils og M. Mayor 2003-2010 sem lýst er hér).
**Candidate 6:** Hópurinn notuðu gagna frá UVES litrófarniðu á Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjarnans nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5 m litrófið Magellan II í Las Campanas stjörnustöðinni í Chile, HIRES litrófarniðu sem komið var á Keck 10 m litrófið á Mauna Kea í Hawaii, auk umfangsriktar gagna frá HARPS (High Accuracy Radial velocity Planet Searcher) í Chile, sem er 3,6 m litróf á Very Large Telescope ESO og er kvenskjastarfverki X. Bonfils og M. Mayor á tímamörkum 2003-2010 (greint fyrir hér).
**Candidate 7:** Hópurinn notaði gögn úr UVES litrófsritunni á Very Large Telescope ESO í Chile (til að meta eiginleika stjarna á nákvæmlega stigi), Carnegie Planet Finder Spectrograph (PFS) á 6,5 m litrófsritunni Magellan II í Las Campanas stjörnustöðinni í Chile, HIRES litrófsrituninni á Keck 10 m litrófsrannsóknastjörnunni í Mauna Kea á Hawaii auk árangurskvæðra gögn frá HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6 m litrófsritunni í Chile (skráð með M dwarfs verkefni X. Bonfils og M. Mayor 2003-2010 sem lýst er hér).

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eso:206 · F</summary>

**Source:** The survey was sensitive to planets between 75 million kilometres and 1.5 billion kilometres from their stars (in the Solar System this range would include all the planets from Venus to Saturn) and with masses ranging from five times the Earth up to ten times Jupiter.
**Semantic decision:** F — Every candidate changes1.5 billion km into million/trillion; some also change mass bounds.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Skoðunin var næm fyrir reikistjörnur á milli 75 milljón kílómetra og 1,5 milljón kílómetra frá stjörnunum (í sólkerfinu voru þessi bil sá um allar reikistjörnurnar frá Venus til Saturn) og á massaflokkum frá fimm sinnum jörðunum til tíu sinnum Júpíturnar.
**Candidate 1:** Skýrslugjöfin var næm fyrir reikistjörnum á milli 75 milljón km og 1,5 milljón milljón km frá stjörnunum (í sólkerfinu nemur allur reikistjörnin frá Venus til Saturn) og öryggisviktum á milli fimm sinnum farna og tíu sinnum Júpíturnar.
**Candidate 2:** Slíkt rannsókn var næm um reikistjörnu milli 75 milljón km og 1,5 milljón milljón km frá stjörnunum (að því er varðar sólkerfið voru þessi milligildi af reikistjörnunum frá Venus til Saturna) og með massameðferð frá fimm sinnum Jörðu upp í tíu sinnum Júpíter.
**Candidate 3:** Vélarann er næmar fyrir reikistjörnur sem eru á milli 75 milljón km og 1,5 milljón km frá stjörnum (í sólkerfinu eru allar reikistjörnurnar frá Venus til Saturn í veggja þess) og eru af massamagni á milli fimm sinnum af jörð og títum af Júpíturnum.
**Candidate 4:** Skýrslugjöfin var ákvæðisfræðilegt við reikistjörnu sem eru á bilinu 75 milljón km til 1,5 milljón milljón km frá stjörnunum (í sólkerfinu vanta allar reikistjörnurnar frá Venus til Saturn) og á massagildum á bilinu frá fimm sinnum jörðu í það saman til tólf sinnum Júpítur.
**Candidate 5:** Skoðanirnar höfðu var alvarlegar vegna reikistjarna sem eru á borð við 75 milljón km og 1,5 milljón milljón km frá stjörnunum (í sólkerfinu og nú er það bil um öll reikistjörnurnar frá Venus og í saman burtu af Saturn) og sem vega massamagn frá fimm sinnum jörðu bein þar til tíu sinnum Júpíter.
**Candidate 6:** Rannsóknin var næm fyrir reikistjörnur í milli 75 milljón km og 1,5 milljón milljón km frá stjörnunum (í sólkerfinu ekki bori á öll reikistjörnurnar frá Venus til Saturn) og þeir voru með þyngdarhæða á bilinu frá fimm sinnum jörðu upp í tíu sinnum Júpítr.
**Candidate 7:** Rannsóknin var næm fyrir reikistjörnur á milli 75 milljón km og 1,5 milljón km frá stjörnurnar (í sólkerfinu fari allar reikistjörnurnar frá Venus til Saturns) og á massamagni á milli fimm sinnum fyrir úr Jörðina og tíu sinnum fyrir Júpíter.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:ema:1394 · F</summary>

**Source:** The most commonly reported adverse reactions (≥ 20%) among patients treated with both belatacept- based regimens (MI and LI) up to Year 3 are diarrhoea, anaemia, urinary tract infection, peripheral oedema, constipation, hypertension, pyrexia, nausea, graft dysfunction, cough, vomiting, leukopenia, hypophosphataemia, and headache.
**Semantic decision:** F — Every candidate mistranslates critical adverse-event items or treatment/frequency qualifiers.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Algengustu aukaverkanirnar sem greint hefur verið frá (≥ 20%) hjá sjúklingum sem fengu bæði meðferð með belatacept-bundnum meðferðaráætlanum (MI og LI) allt til árs 3 eru niðurgangur, blóðleysi, bólga í þvaglötu, bólga í útlimum, munaleysi, háþrýstingur, hiti, ógleði, vansköpun ávefja, hósti, uppköst, blóðflagnafæð, blóðfosfatsfalli og höfuðverkur.
**Candidate 1:** Algengustu aukaverkanir sem greint hefur verið frá hjá sjúklingum sem fengu bæði lyfjameðferð með belatacepti (MI- og LI- meðferð) allt til ára 3 eru niðurgang, blóðleysi, þvagertilbæling, bólga í útlimum, hægðatregðu, háþrýstingur, hiti, ógleði, vanstarfsemi æxlis, hósti, uppköst, blóðflagnafæð, blóðfosfatsfalli og höfuðverkur.
**Candidate 2:** Algengustu aukaverkanir sem fram komu í tilkynningum úr meðferð með belatacept-setningum (MI- og LI-) þar sem meðferð var stöðugt í ár 3 eru niðurgangur, blóðleysi, þvagbólgu í þvagblöðru, bólga í útlimum, hægðatregðu, háþrýsting, hiti, ógleði, skemmdarvirkni, hósta, uppköst, sveigjanleika, blóðfall, sleitthvati og höfuðverkur.
**Candidate 3:** Algengustu aukaverkanirnar sem fram koma (≥ 20%) hjá sjúklingum sem fengu bæði meðferð með belatacept-bundnum meðferðaráætlunum (MI og LI) í allt fram til ári 3 eru niðurgangur, blóðleysiskort, sýking í þvagvegnum, útlægum þyrpingum, hægarlæga, háþrýstingur, hita, ógleði, aðvörun, hósta, uppköst, blóðleysi, lágklófa- blóðsalt, og höfuðverki.
**Candidate 4:** Algengustu aukaverkanirnar sem fram komu hjá sjúklingum sem fengu bæði reglur sem byggðar voru á belatacepti (MI og LI) til árs 3 (≥ 20%) eru niðurgangur, blóðleysi, þvagþroska, útbrot í útlægum þrota, hægðatregðu, háþrýstingur, hiti, ógleði, starfshemjandi æxlun, hósti, uppköst, sýrusta, blóðfallsminna blóðásíðagildi og höfuðverk.
**Candidate 5:** Algengustu aukaverkanirnar sem greint var frá (≥20%) hjá sjúklingum sem fengu bæði meðferð með belatacepti-bundnum meðferðaráætlunum (MI og LI) fram í 3. ári eru niðurgangi, blóðleysi, ofnæmisveiru í niðurbolti, útflæðiseyði, hægðatregðu, háþrýstingur, hita, ógleði, truflun í grúnni, hósti, uppköst, albúmfrumnakláði, blóðfosfatsfall, og höfuðverkur.
**Candidate 6:** Algengustu aukaverkanirnar sem greint hefur verið frá hjá sjúklingum sem fengu bæði belatacept-hópum með miðlun (MI) og Lí (LI) meðferð í allt að 3 árinu eru niðurgangur, blóðleysi, sýking í þvagvegjum, bólga í útlimum, hægðatregða, háþrýstingur, hiti, ógleði, truflun í gegnumveg, hósti, uppköst, hvíldarfall, blóðblöðruefni, höfuðverkur og höfuðverkur.
**Candidate 7:** Algengustu aukaverkanirnar sem greint hefur verið frá hjá sjúklingum sem fengu bæði reglum með belatacept (MI- og LI-gerð) allt til ár 3 eru niðurgangur, blóðleysi, baktersýking í þvagsvöðum, útbrot í útlimum, þvagslagi, háþrýstingur, hiti, ógleði, utanvirkni truflun, hósti, uppköst, hvíldastorkni, blóðfosfatsfalli og höfuðverkur.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eso:491 · F</summary>

**Source:** ALMA can observe in different frequency bands.
**Semantic decision:** F — No candidate faithfully expresses observing in different frequency bands.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** ALMA getur athugað á milli í mismunandi fjölda fjöldaða.
**Candidate 1:** ALMA getur könnuð skoðun á mismunandi beitingabilum.
**Candidate 2:** ALMA getur rannsakað á mismunandi völdum.
**Candidate 3:** ALMA getur gakkt á mismunandi geislavistur.
**Candidate 4:** ALMA má fara beina upp á mismunandi tíðnisímum.
**Candidate 5:** ALMA getur mælt í mismunandi fjölda ár.
**Candidate 6:** ALMA getur metað í fleiri ávalltignasamböndum.
**Candidate 7:** ALMA getur fylgst með tjóna í mismunandi fjölda fyrirbæra.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eea:85 · P</summary>

**Source:** For the estimation of these concentrations all relevant information on the plant protection product and on the active substance must be taken into account.
**Semantic decision:** P — Candidate7 retains estimating concentrations and all relevant plant-protection-product and active-substance information.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [7]
**Candidate 0:** Til að áætla þessa styrkleika skal tekið tillit til allra viðeigandi upplýsinga um plöntuverndarvörn og virku efnin sem þau innihalda.
**Candidate 1:** Við mat á þessum styrkleikum ber að taka til hliðar allar viðeigandi upplýsingar um plöntuverndarvarnarefnið og virka efnið.
**Candidate 2:** Til að meta þessi þéttni skal taka tilhlýðilegt upplýsinga um plöntuvarnarefnið og virka efnið í tillit.
**Candidate 3:** Vegna matar fyrir þessum þéttni skulu taka tillit til allra viðeigandi upplýsinga um plöntuverndarvörn og virka efnið.
**Candidate 4:** Við mat á þessum styrkleika verður að taka tillit til öllum viðeigandi upplýsinga um plöntuverndarvörn og virka efnið.
**Candidate 5:** Vegna áætlanar um þessi styrk verða að taka neytir yfir allar viðeigandi upplýsingar um plöntuvarnarefnið og virka efnið.
**Candidate 6:** Við áætlanir á þessum þéttni skulu taka tillit til allra viðeigandi upplýsinga um plöntuverndarvörn og virka efnið.
**Candidate 7:** Við mat á þessum styrk skulu taka til greina öllum viðeigandi upplýsingum um plöntuvarnarefnið og virka efnið.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eea:1552 · F</summary>

**Source:** The analytical result shall be reported as x +/– U whereby x is the analytical result and U is the expanded measurement uncertainty, using a coverage factor of 2 which gives a level of confidence of approximately 95 % (U = 2u).
**Semantic decision:** F — Expanded measurement uncertainty is changed to diluted measurement technique and coverage factor is corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Greina skal greinilegri niðurstöðuna sem x +/– U þar sem x er greinileg niðurstöðu og U er útþynnt mælitækni, með því að nota 2 gildi fyrir umfrymisstærð sem gefur til kynna 95% öryggi (U = 2u).

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eso:1051 · F</summary>

**Source:** The technique used by Teague, which derived averaged variations in the flow of the gas as small as a few percent, revealed the impact of multiple planets on the gas motions nearer to the star.
**Semantic decision:** F — Flow-variation observable is altered and multiple planets become a family of planets.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Aðferðin sem Teague notaði, sem leiddi til meðalþéttni breytilegra flæðis gassins sem var í nokkra prósentum, leiddu fram áhrif fjölskyldu reikistjarna á flæði gassins nálægri stjörnunni.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eea:1216 · U</summary>

**Source:** That task shall be coordinated with the existing regional cooperation programmes and shall include, where appropriate, the organisation of relevant training activities.
**Semantic decision:** U — Existing regional cooperation programmes are recognizable, but organizing training activities becomes unclear management of training technique.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þessi verkefni skal samræmd við tilstaðar áætlunum um sameiginlega starfsemi á svæðum og skal þar með innihalda, eftir því sem við á, stjórnun viðeigandi þjálfunartækni.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:opensubtitles:1012 · P</summary>

**Source:** I'll do whatever you ask.
**Semantic decision:** P — Promise to do whatever is asked retained despite tense/inflection.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Ég geri hvað sem þú baðir.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eso:323 · F</summary>

**Source:** They were able to make the sharpest direct observation ever , of the centre of a distant galaxy, the bright quasar 3C 279, which contains a supermassive black hole with a mass about one billion times that of the Sun, and is so far from Earth that its light has taken more than 5 billion years to reach us.
**Semantic decision:** F — Billion becomes million in both mass and light-travel time.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þau gáfu til þess að gera skarpsmesti beinu sjónauki á miðju fjarlægri vetrarbrauta, 3C 279, sem er bjartur kvarnfræðileg stjörnu og inniheldur öflugan svarthol með massa sem er um milljón sinnum stærri en sólin okkar og er svo fjarlægt frá Jörðinni að ljós hennar hefur tekið meira en 5 milljón ára til okkar.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eea:281 · F</summary>

**Source:** The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.
**Semantic decision:** F — All eight corrupt maturity-band, former/latter matching and residual-position relations.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Fjölda tekjutengda (framan) sem eru semlagðir með framan (faraan) í geymdum afurðafhlaðnarskala skal vera samræmt stöður í þeirri skipulag, þar sem undangenginn stöður í afurðaþráði eða stöður í stöðuhluta skal vera ósamræmandar í sama skipulag.
**Candidate 1:** Hlutfall fyrri (sári) sem fyrirbyggja sér svörun með sári (fyrri) í tilteknu útheimaleika skal vera svörunmótað stöð á þeirri útheimaleika, en ósvörunmótað stöð skal vera hlutur sem fyrirbyggja sama útheimaleika.
**Candidate 2:** Ílætið fráfenginn (slíkt núna) sem uppfyllir það líka það (fráfenginn) í tilteknu þroskaþætti skal vera uppfyllt staðurinn í þessum þroskaþætti en skorrðað staðurinn til aðgengilegs lán eða lán sem er ekki uppfyllt skal vera uppfyllt staðurinn í samræmdri þroskaþætti.
**Candidate 3:** Þannig skulu ordin meðferðinni (látin) fyrri (slíti) séu tengd meðferðinni (slíti) í tilteknu þegari stærðferðarbrunnu, þar sem meðskammtin sem enn standa í stærðferðarbrunninu skulu vera ótengd meðferðinni fyrir sama brunn.
**Candidate 4:** Magn miðlaðrar (næmstri) sem eru aðhöfðir miðlaðri (fyrri) í tekið útvarpshallra skal vera miðlaðir staðstöðurnar í þann útvarpshallra, en efnast langa eða stunda staðstöður skal vera ómiðlaðar staðstöðurnar í sömu útvarpshallra.
**Candidate 5:** Fjöldi framsómasta (nýjasta) sem samrýmast við henni (framsómasta) í viðkomandi vinstri (farsómasta) stigastæði skal vera samrýmastakandi staðurinn í þeim stigastöðum svo fjárhöfn við varðandi stigastöðuna sé uppfærð staður sem samrýmast ekki.
**Candidate 6:** Stöðuðar af fyrri (sáttastíf) sem sáttastífurinn samhægir sáttastífurinn í tiltekinni útverkslagabliki skulu vera samhægar stöður í bliknum, en hlökk staðstilla, sem eftir er eða eftir er á, skulu vera ósamhæfðar stöður í þeinni blik.
**Candidate 7:** Hlutar af fyrri (sáttarmáli sem fyrri (sáttarmáli sem síðari), sem samræmar eru sáttamála síðari (fyrri) í tilteknu útfræðiskerfi skal vera samræmd stöður í því kerfi, en ósamræmd stöður skal vera í því kerfi sem við er að ræða við sama útfræðiskerfi.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eso:446 · P</summary>

**Source:** “Astronomers have waited for data like this for over a decade.
**Semantic decision:** P — Astronomers waiting over ten years for such data is retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** „Stjörnufræðingar höfðu bíðið um gögn eins og þessi í meira en tíu ár.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:opensubtitles:996 · P</summary>

**Source:** What kind of man would that make me?
**Semantic decision:** P — Exact source/hypothesis semantic reuse from card127: What kind of man would that make me retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Hvers konar maður myndi það gera mig?

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eea:1585 · P</summary>

**Source:** The Commission shall submit a final evaluation report at the end of the Programme.
**Semantic decision:** P — Candidate2 faithfully states that the Commission submits a final evaluation report at programme end.
**Inspected / Correct indices:** [0, 1, 2, 3, 5, 6, 7] / [2]
**Candidate 0:** Framkvæmdastjórnin skal leggja fram endanleg matsskýrslu að lokum áætluninni.
**Candidate 1:** Framkvæmdastjórnin skal leggja fram lokasigaskelláknir á lokum áætluninnar.
**Candidate 2:** Framkvæmdastjórnin skal leggja fram endanlega matsskýrslu við lok áætlunarinnar.
**Candidate 3:** Framkvæmdastjórnin skal leggja fram endanlega matsskiláða skýrslu fyrir lok áætlunarinnar.
**Candidate 5:** Framkvæmdastjórnin skal leggja fram endanlega matsskýrslu eftir áætluninni.
**Candidate 6:** Framkvæmdastjórnin skal leggja fram endanlega ávísaðan sk rslu a lokum áætlunarinnar.
**Candidate 7:** Framkvæmdastjórnin skal leggja fram endanlegar matsskjölin á lokum áætlunarinnar.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eea:1716 · U</summary>

**Source:** The competent authorities of Gabon have reacted promptly to these concerns, indicating their commitment to take all measures necessary to implement applicable ICAO standards and enforce compliance with these standards as soon as possible.
**Semantic decision:** U — Prompt action and commitment retained, but enforcement of standards compliance remains unclear.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Lögbær yfirvöld í Gabón hafa orðið tafarlaust við þessum áhyggjuefni og benda til þess að þau séu bundnir til að gera allar nauðsynlegar ráðstafanir til að framfylgja gildandi staðlar ICAO og gera þeim fullnægjandi eins fljótt og auðið er.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eso:491 · F</summary>

**Source:** ALMA can observe in different frequency bands.
**Semantic decision:** F — Frequency bands are missing.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** ALMA getur fylgst með breytilegum fjölda á milli.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:ema:1192 · P</summary>

**Source:** It is used to prevent pregnancy.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Inspected / Correct indices:** [1] / [1]
**Candidate 0:** Hún er notað til að koma í veg fyrir þungun.
**Candidate 1:** Það er notað til að koma í veg fyrir þungun.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:ema:1718 · U</summary>

**Source:** Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.
**Semantic decision:** U — P-gp inducer role remains unclear despite preserved AUC/half-life/effect changes.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Samhliða gjöf edoxabans og P-gp örvaðs rífampicíns leiddi til minnkaðrar meðal AUC fyrir edoxaban og skertrar helmingunartíma, sem getur valdið minnkun á lyfhrifum.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:ema:767 · U</summary>

**Source:** Therefore, docetaxel must not be used during pregnancy unless clearly indicated.
**Semantic decision:** U — Pregnancy prohibition retained, but the exception becomes unclear permission/decision rather than a clear clinical indication.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Því má ekki nota docetaxel meðan á meðgöngu stendur nema brýna markmiðið sé fylgt.
**Candidate 1:** Því má ekki nota docetaxel á meðgöngu nema sprauta sé óhöfugleg.
**Candidate 2:** Því má ekki nota doketaxel á meðgöngu nema brýna ákvarðanir til kynna.
**Candidate 3:** Því má ekki nota docetaxel á meðgöngu nema greinilega ákveðin sé.
**Candidate 4:** Því má ekki nota docetaxel á meðgöngu nema greinilega megi gefa til.
**Candidate 5:** Því verður ekki að nota dócetaxel á meðgöngu nema ávísað sé korthæft.
**Candidate 6:** Því má ekki nota dócetaxel á meðgöngu nema greinilega fylgist.
**Candidate 7:** Því má ekki nota dócetaxel á meðgöngu nema algjörlega er ákveðið.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eea:1991 · F</summary>

**Source:** Paragraph AG27 is amended and after paragraph AG29, paragraph AG29A is added.
**Semantic decision:** F — The AG prefixes identifying the amended paragraphs are lost.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Í 27. lið er breytt og eftir 29. lið bætist við 29. lið A.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:ema:704 · F</summary>

**Source:** The most frequently reported adverse reaction was acne, which was generally mild.
**Semantic decision:** F — Acne is replaced by an unrelated cures/naps word.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Algengasta aukaverkunin sem greint var frá var kúrur sem var yfirleitt væg.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eso:768 · P</summary>

**Source:** Both components are classed as O-type stars.
**Semantic decision:** P — Both components being O stars is preserved; inflection errors are minor.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Bæði hlutin eru flokkaðar sem O- stjörnur.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:ema:1765 · U</summary>

**Source:** Take this leaflet or some tablets with you so that your doctor knows exactly what you have taken.
**Semantic decision:** U — Taking leaflet/tablets retained; doctor knowing versus giving an account is unclear.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Taktu þessum fylgiseðil eða töflur með þér svo að læknirinn veiti nákvæmlega grein fyrir hvað þú hefur tekið.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eso:924 · F</summary>

**Source:** ESO was delighted to welcome Italys Minister of Education, Universities and Research, H.E. Stefania Giannini, to the ceremony, which was also attended by the Italian Consul General in Munich, Renato Cianfarani, the ESO Council President, Patrick Roche, and the Italian ESO Council Delegates, Nicolò DAmico (who is also President of INAF) and Matteo Pardo, Scientific Attaché at the Italian Embassy in Berlin.
**Semantic decision:** F — Attendee names and roles are omitted or changed, with repeated fabricated affiliations.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** ESO var ánægð af því að viðvöktast Stefania Giannini, ráðherra yfir menntun og vísindum í Ítalíu, sem var einnig á festinaði, sem samkvæmt hópi ESO, Patrick Roche, forseti ráðsins og Níkóló DAmico, vísindasamstólsdelegat í Ítalíu, sem er líka forseti INAF, og Matteo Pardo, vísindasamstólsdelegat í Ítalíu, sem er vísindasamstólsdelegat í Ítalíu.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eea:609 · F</summary>

**Source:** Special payments for shift work.
**Semantic decision:** F — None preserves shift work; alternatives concern steps, permanent work or other unrelated categories.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Sérstök greiðslur við skrefverk.
**Candidate 1:** Sérstök greiðslur vegna skrefverkunar.
**Candidate 2:** Sérstakt greiðslur í starfsmeðaltali.
**Candidate 3:** Sérstakar greiðslur til skrefa.
**Candidate 4:** Sérstakt greiðslur fyrir starfsstöðum.
**Candidate 5:** Sérstækku greiðslur fyrir skiptir.
**Candidate 6:** Sérstakar greiðslur fyrir stöðugir vinnur.
**Candidate 7:** Sérstakar greiðslur fyrir röðað krafta.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eea:2037 · U</summary>

**Source:** Those criteria should not be considered to be exhaustive.
**Semantic decision:** U — Negated completeness/exhaustiveness remains ambiguous with perfection/adequacy.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6] / []
**Candidate 0:** Þessi viðmiðanir skulu ekki teljast fullnægjandi.
**Candidate 1:** Þessi viðmiðanir skulu ekki teljast nákvæmar.
**Candidate 2:** Þessum viðmiðunum ber ekki að telju fullkomlega.
**Candidate 3:** Ekki skal telja þessi viðmiðanir fullkomlar.
**Candidate 4:** Ekki skal telja þessi viðmiðanir fullkomnir.
**Candidate 5:** Ekki skal telja þessar viðmiðanir fullkomlegar.
**Candidate 6:** Sem ekki séu annars konar skilvirkt að meta þessi viðmiðanir.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:ema:1100 · P</summary>

**Source:** If you miss a dose, take your next dose as scheduled.
**Semantic decision:** P — Missed dose and next scheduled dose retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Ef þú gleymir skammti skal taka næsta skammt samkvæmt áætlanum.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eso:919 · F</summary>

**Source:** "Thanks to several giant telescopes currently under construction, including ESOs E-ELT and the NASA/ESA/CSA James Webb Space Telescope due to launch for 2018, we will soon be able to study the atmospheric composition of these planets and to explore them first for water, then for traces of biological activity.
**Semantic decision:** F — Agencies and launch are corrupted; water is generalized to liquids.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** „Takinn er við nokkrum stórum sjónaukum sem eru í framkvæmd og þar með talið ESO E-ELT og James Webb geimsjónauka NASA/ESO/CSC sem verður að fara í reynd árið 2018, getum við náið nægilega í stað að rannsaka samsetning lofttegunda þessara reikistjarna og rannsaka þær fyrst með vökvum, síðan með einkennum líffræðilegra virkni.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eea:1461 · F</summary>

**Source:** All industrial uses of gas are considered.
**Semantic decision:** F — Industrial-use qualifier is omitted and all activity of gases is substituted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Í allri starfsemi gasa er tekið tillit til.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eea:1461 · U</summary>

**Source:** All industrial uses of gas are considered.
**Semantic decision:** U — Gas, all-use scope and work/industry are partly retained, but considered versus specified and industrial scope remain uncertain.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Í öllum atvinnuframleiðslum er tekið tillit til gasa.
**Candidate 1:** Ífram er að taka til allra gjöfgerða gasa.
**Candidate 2:** Í öllum vinnuauðgöngum er tekið tillit til gasa.
**Candidate 3:** Tilgreind eru öll atvinnuleg notkun gasa.
**Candidate 4:** Í allri gjöf gasa er tekið tillit til.
**Candidate 5:** Taka er mið af öllum notkunir á gas í vinnu.
**Candidate 6:** Talið er með öllum notkunum gas í vinnuverum.
**Candidate 7:** Tilgreint er um öll atvinnustarfsemi gegn gas.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eea:281 · F</summary>

**Source:** The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.
**Semantic decision:** F — Maturity-band and former/latter matching terminology is corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Fjöldi fyrri (sáttmálans) sem samsvarast við síðustu (fyrsta) í tilteknum vaxtarbrukum skal vera samsvarandi stöður í þeim brukum, en eftirfarandi stöður langa eða stuttar skal vera ósamsvarandi stöður í sama brukum.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:eea:534 · U</summary>

**Source:** Council Directive 74/60/EEC of 17 December 1973 on the approximation of the laws of the Member States relating to the interior fittings of motor vehicles.
**Semantic decision:** U — Directive/date retained, but translation of interior fittings is uncertain.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Tilskipun ráðsins 74/60/EBE frá 17. desember 1973 um samræmingu á lögum aðildarríkjanna varðandi innri fyrirbúningar ökutækja.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:opensubtitles:480 · F</summary>

**Source:** Now we have enough evidence to charge you with murder.
**Semantic decision:** F — Criminal charging is replaced by an unrelated defecation verb.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Nú hafa við nægilega sönnunargögn til að skíta þig um morð.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:ema:1406 · F</summary>

**Source:** Concomitant use with yellow fever vaccine and with live virus and bacterial vaccines (see section 4.5).
**Semantic decision:** F — Every candidate corrupts yellow-fever vaccine and/or the live-virus/bacterial-vaccine objects.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Rannsókn með bóluefni gegn gulaater (yellow fever vaccine) og lifandi veiruvefna og bakteriuvafna (sjá kafla 4.5).
**Candidate 1:** Samhliða notkun með llautakvilli og lifandi veiru- og bakteríukvilli (sjá kafla 4.5).
**Candidate 2:** Samhliða meðferð með brúggi-vefjaleyfi til bólgu og lifandi veirus- og bakteríuskuldbindinga (sjá kafla 4.5).
**Candidate 3:** Samhliða notkun með fangavísi- bóluefni og lifandi veirus- og bakteríubóluefni (sjá kafla 4.5).
**Candidate 4:** Samhliða notkun á aóverkun við gulaverk og lifandi veirusjónhvarf og bakteríusjónhvarf (sjá kafla 4.5).
**Candidate 5:** Samhliða notkun milli bóluefna gegn gulvístu og lifandi veirus og bakteríum (sjá kafla 4.5).
**Candidate 6:** Notkun samhliða gallspetnavaxtarlyfjum og lifandi veirum og bakteríumaxtarlyfjum (sjá kafla 4.5).
**Candidate 7:** Notkun samhliða barnaæxluskotandi bóluefni og lifandi veiruefni og bakteríuefni (sjá kafla 4.5).

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eso:302 · F</summary>

**Source:** This is because the tilt of the orbit is normally unknown.
**Semantic decision:** F — Orbital tilt is omitted or replaced by unrelated quantities in every candidate.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Það er vegna þess að það er venjulega óþekkt sem típ svæðisins er.
**Candidate 1:** Það er vegna þess að stojakilt skírteini er venjulega óvænt.
**Candidate 2:** Það er vegna þess að bláæðin er venjulega óþekkt.
**Candidate 3:** Þetta er vegna þess að þjóðorháttur æxli er venjulega óþekkt.
**Candidate 4:** Það er vegna þess að hálfalengd reikslinnar er venjulega óþekkt.
**Candidate 5:** Þetta kemur vegna þess að ástæðan er venjulega ekki þekkt.
**Candidate 6:** Þetta er vegna þess að fækkun róalsins er yfirleitt ekki þekkt.
**Candidate 7:** Þetta er vegna þess að um reikningarlega ekki er vitað um þyngingu hringrar.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:opensubtitles:2508 · F</summary>

**Source:** Rose, we have a guest in the living room.
**Semantic decision:** F — Living room is changed to the home.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Rose, við erum með gesta í heimilinu okkar.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eso:70 · P</summary>

**Source:** This is only the sixth of these huge storms to be spotted since 1876.
**Semantic decision:** P — Candidate6 retains only the sixth of the huge storms appearing/coming to notice since1876.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [6]
**Candidate 0:** Þetta er aðeins sexustur af þessum mikilu og meira stormi sem hafa verið leit úr 1876.
**Candidate 1:** Þetta er aðeins sjötta af þessu mikla hryggjastjörnum sem komu sýnilega frá 1876.
**Candidate 2:** Þetta er aðeins sjöttni þessi umbreyktra slökkva storma sem fyrirhuguð hefur verið Þegar 1876.
**Candidate 3:** Þetta er aðeins sjötta af þessu mikilu stormi sem settar voru fram síðan 1876.
**Candidate 4:** Þetta er aðeins sjötta þessara eirum rjunanna sem komið hefur fram í gegnum árin 1876.
**Candidate 5:** Þetta er aðeins sjökthugbúið stormið sem gegnt hefur verið í alifærum tíðum frá árinu 1876.
**Candidate 6:** Þetta er aðeins sjötta þessara mikill storma sem komu fram síðan árið 1876.
**Candidate 7:** Þetta er aðeins sex af þessum umtalsverðum tækanum slökkum sem stundum á og þau hafa verið leitt á frá 1876.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:opensubtitles:3209 · P</summary>

**Source:** Because it's not safe there.
**Semantic decision:** P — Because it is not safe there is retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Því það er ekki öruggt þar.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:opensubtitles:1169 · P</summary>

**Source:** They're pretty as can be, aren't they?
**Semantic decision:** P — Very pretty/cute and the tag question retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Þeir eru mjög sæt, ekki satt?

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eea:574 · F</summary>

**Source:** All rear-window, roof-panel and partition switches intended for use by occupants in the rear of the vehicle shall be capable of being switched off by a driver-controlled switch which is located forward of a vertical transverse plane passing through the R points of the front seats.
**Semantic decision:** F — All eight corrupt switch types, control roles and the specified geometry.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Allar bakvara, skuggu- og hlíftrúar, sem ætlaðar eru til notkunar hjá notendum í aftanrás, skulu vera kominn við stöðvun með því að beita skiptingar sem er skiptingur í ökutækisstýri sem er staðsett fyrir við úttektarfélaga sem beinast í gáttarrúm sem ferst í frumþoknunarsíðum.
**Candidate 1:** Allir opinum-heimildir á afturglugga, húðveggjum og drepum, sem eru ætluð um að nota í afturglugga ökutækisins, skulu geta verið skipt af með klúður sem hefur stjórn úr ökumaðu og er í framhluta hliðar sem fer yfir R-stig innan efnaþilra.
**Candidate 2:** Allir bletur í afturslipi, tegur- ríkjum og skiptu, sem ætluð eru til notkunar af innsæi upp í vélinn, skulu geta verið hægt að slökkva með veitingsbúnaði sem er í fæstu miðað við yfirlið sem gengur á gegnum R-staðir færnum sæta.
**Candidate 3:** Allar höðvindur, þekjuvindur og hlífir sem verða notaðir af farþega á réttarhlið vélins skulu geta verið hætt með tillögu sem er viðhaldsstaður handa ökumenn og er í fæstu við hliðferðnar flatar sem ferðast ganga gängi í R-stöðum í hljóðsetta í framanbelti vél.
**Candidate 4:** Allir rútu, afslökkaplantar og fasanna, sem ætlaðir eru til notkunar fyrir neytendum í rassrúti ökutækisins, skulu hafna hægt að slíkum grofum sem kveðið er á um að borðast við ökumenn eftir skipti ef gegn hægt er að slíkum grofum sem kveðið er á um að borðast við umsjón við eftirruð.
**Candidate 5:** Allar beldturýlur, rassstæður og hlaupir, sem ætlaðir eru til notkunar hófuþega í aftanfæri ökutækisins, skulu geta verið slökkt af með stjórnsýslustjórnandi beldti, sem er á færi frá hæður, sem fer eftir R-stöðum í vörslumstöðum í framanlegu.
**Candidate 6:** Allir bakglas, tegularsögunum og taksalyfjagerum, sem ætlað eru að nota einstaklingar í aftan hálsi ökutækisins, skulu vera gerðar á að skiptast niður með höndleggjandi lykilsemri sem er í fænistrið frá ristirni fyrir uppsettur sætu.
**Candidate 7:** Öll bakgluggi, húðafæð og þyrpingar, sem ætlaðar eru til notkunar af hvert sem er í baksvæðum ökutækisins, skulu geta verið stöðugrar af kjölfariðinni sem stjórna er og er fyrir ofan frá lyngnaviði sem fluttir gegn R-stigunum á framsvæðum sætta.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eso:765 · F</summary>

**Source:** “If it keeps spinning rapidly it might end its life in one of the most energetic explosions in the Universe, known as a long-duration gamma-ray burst,” says the lead scientist of the project, Hugues Sana, of the University of Leuven in Belgium.
**Semantic decision:** F — All eight corrupt the spinning/gamma-ray-burst claim or essential scientific/institutional details.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** „Ef hún helst hratt hryggir hún helst í einu af strengustu sprengingunum í alheiminu, þekkt eftir hún sem langvinnur gamma-losi,“ sagði Hugues Sana, aðalhafa verkefnisins í Leuven-í Írlandi.
**Candidate 1:** „Ef það hreyfir vel áfram, getur það fengið leiðina svo lengi að deiluð verið með því sem er lengur til í alheiminn, sem er kallað langtímamagn grámunngur,“ segir leiðandi vinnslu- kerfisfræðingurinn í verkefnið, Hugues Sana, í Leuven í Belgía.
**Candidate 2:** „Ef hann helst að snúa hratt- gætu hann endað lífi sínu í eftirfarandi lengstu gammaveskju í alheiminu sem kjarnaviðtök er kallað,“ segir Hugues Sana, umsjónherra verkefnisins sem stofnast í Leuven í Belgía.
**Candidate 3:** „Ef hún hefur áfram hrein endurhreinir flæðið getur hún verið að enda lífi sínu í einum af sterkustu sprengingu í alheiminu, sem nefnast langvinnri gama- rænþrýstingi,“ segir frumkvæðisvísindamaður verkefnisins, Hugues Sana, frá Leuven háskóla í Belgíu.
**Candidate 4:** „Ef það hreyfir sér hratt getur það endað líf sinni á einu af mesta heilastiglegustu sprengingunum í alheiminu sem ketra kallað er langvinnur gamma-geimsburður,“ sagði teindinni við verkefnið Hugues Sana við Leuven hafnís við Belgía.
**Candidate 5:** „Ef það hægir að snúast snúa mundi það líka enda lífi sínu í eina af öflusta sprengingu í alheiminn, sem kallast langtímasefði gamma-losanir,“ sagði leitaraheimsjóðasagna frá verkefninu, Hugues Sana úr Leuven- háskóla í Belgíu.
**Candidate 6:** „Ef hún hreyfir sér hratt kann pa koma í lok mínútu eins af mestar forþrýstingjum í alheiminu, sem kallast langtímamært gammagrößeaslagi,“ sagar framkvæmdarstjóri verkefnisins, Hugues Sana, frá Leuven-íverslunni í Belgíu.
**Candidate 7:** „Ef hún hreyfir sig hratt getur hún farið með lífinu í einu af sterkustu sprengingunum sem semst er í alheiminu, sem kallast langtímamjölf gammöðlosa,“ sagði Hugues Sana, hóparáðanda verkefnisins í Leuven arneti í Belgíu.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:ema:1718 · P</summary>

**Source:** Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.
**Semantic decision:** P — Candidate3 retains P-gp-inducer rifampicin and reduced mean AUC, shorter half-life and possible reduced pharmacodynamic effects.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [3]
**Candidate 0:** Samhliða gjöf edoxabans ásamt P-gp örvaðilum, rifampicini, leiddi til minnkaðs mína AUC for edoxabani og minni callhaldarstig, til að geta minni áhrif á lyfhrif.
**Candidate 1:** Samhliðagjöf edoxabans og viðbótarvirkra P-gp ruglaðs, rifampicins, leidur til minnkaðs meðaltals AUC fyrir edoxaban og minnkaðs helmingunarskammtar, með hugsanlegri minnkun á lyfhrifum.
**Candidate 2:** Notkun edoxabans samtímis rifampicíns, sem virkir P-gp, leiddi til minnkaðs meðal AUC fyrir edoxaban og minnkaðs helmingunartíma, sem gæti miklu tilhlýðilega dregið úr lyfjafræðilegum áhrifum lyfja.
**Candidate 3:** Samhliða lyfjagjöf edoxabans og P-gp örva rífampicíns leiddi til þess að meðaltal AUC fyrir edoxaban minnkaði og styttri helmingunartími, sem gæti valdið minnkun á lyfhrifum.
**Candidate 4:** Samhliða gjöf edoxabans og P-gp örvaðar rífampicíns leiddi til minnkaðs meðaltals AUC fyrir edoxaban og minnkunar helmingunartíma, sem geta komið fram minnkun á lyfhrifum þess.
**Candidate 5:** Notkun edoxabans samtímis rifampicíni, P-gp örva, leiddi til minnkaðrar meðal AUC fyrir edoxaban og minnuðs helmingaldags, sem gát ekki aukið minnkað lyfhrif hins þá.
**Candidate 6:** Samhliða gjöf edoxabans og P-gp virkjaðar rifampicins leiddi til minnkaðrar meðal AUC fyrir edoxaban og minnkaðrar helmingunartíma, með mögulegri minnkun á lyfhrifum.
**Candidate 7:** Samhliða lyfjagjöf edoxabans og P-gp virkjaðs rífampicíns leiddi til minnkaðs meðal AUC fyrir edoxaban og minnkaðs helmingunartíma, með hugsanlega minnkun á lyfhrifum.

</details>

<details><summary>t1500729 · greedy · p13official21:dev:ema:325 · F</summary>

**Source:** If you get lower abdominal pain, gain any weight rapidly, feel sick or are vomiting or if you have difficulty in breathing, talk to your doctor straight away who might ask you to stop using this medicine (see in section 4 under “Serious side effects”).
**Semantic decision:** F — Adds dry mouth and corrupts nausea/lower-abdominal detail, despite retaining breathing and stopping medicine.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Ef þú færð kviðverki, þyngdar hraða, fæst eða hefur uppköst, færð munnþurrka eða ef þér er erfitt við öndun, skaltu tafarlaust ráðfæra þig við lækninn sem kann að spyrja þig um að hætta notkun lyfsins (sjá kafla 4 undir „Alvarlegar aukaverkanir“).

</details>

<details><summary>t1500729 · G8 · p13official21:dev:ema:1582 · P</summary>

**Source:** The treatment-free period, however, should take into account the pharmacological properties of the products used previously.
**Semantic decision:** P — Candidate2 retains a treatment-free period and pharmacological properties of previously used medicines.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [2]
**Candidate 0:** Meðan á meðferðarfrasluminnum stendur skal íhuga lyfjafræðileg eiginleika lyfju sem notað er áður.
**Candidate 1:** Að því er varðar án meðferðar tíma skal hún íhuga lyfjamæti lyfjanna sem notað eru áður.
**Candidate 2:** Meðferðlaus tímabil skal þó taka tillit til lyfjafræðilegu eiginleika lyfja sem notað hafa verið áður.
**Candidate 3:** Hins vegar ætti meðferðarframanum að hafa í huga lyfjameindir vörunnar sem settar hafa verið í notkun áður.
**Candidate 4:** Í meðferðarfríumánaði skal þó taka tillit til lyfjafræðilegra eiginleika lyfja sem notað eru áður.
**Candidate 5:** Meðferðarfráfalls ávinningin á þó að tekið er tillit til lyfjamenginda lyfja sem notað hafa verið áður.
**Candidate 6:** Meðan án meðferðar tíminn hefur að alveg í huga lyfjafræðileg eiginleikar lyfjanna sem eru notaðir áður.
**Candidate 7:** Meðferðarfrí meðferðarfríðum átökum skal þó taka tillit til lyfjafræðilegra eiginleika afurðanna sem notuð hafa verið áður.

</details>

<details><summary>t1500729 · G8 · p13official21:dev:eea:1914 · P</summary>

**Source:** This Regulation shall enter into force on the third day following that of its publication in the Official Journal of the European Union.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Inspected / Correct indices:** [5] / [5]
**Candidate 0:** Reglugerð þessi öðlast gildi fyrri daginn eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.
**Candidate 1:** Reglugerð þessi öðlast gildi þriðju daga eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.
**Candidate 2:** Reglugerð þessi öðlast gildi þriðja daga frá því henni var birt í Stjórnartíðindum Evrópusambandsins.
**Candidate 3:** Reglugerð þessi öðlast gildi þriðja daginn eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.
**Candidate 4:** Reglugerð þessi öðlast gildi þriðja dag eftir birtingu hennar í Stjórnartíðindum Evrópusambandsins.
**Candidate 5:** Reglugerð þessi öðlast gildi á þriðja degi eftir að hún er birt í Stjórnartíðindum Evrópusambandsins.
**Candidate 7:** Reglugerð þessi öðlast gildi þriggja daga eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eea:574 · F</summary>

**Source:** All rear-window, roof-panel and partition switches intended for use by occupants in the rear of the vehicle shall be capable of being switched off by a driver-controlled switch which is located forward of a vertical transverse plane passing through the R points of the front seats.
**Semantic decision:** F — Every candidate corrupts switch types, control roles or the required transverse-plane geometry.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Öll bakglas, skuggu- og hlíftrúar, sem hafa áætlanir til að nota eftirfarandi innbyggjendur í hálfu ökutækisins, skulu geta verið skipt upp með skipti sem er í öllum stjórnunarefni og er í færi við hlið þess sem snúa yfir R-stöðvar fyrirfarandi sæta.
**Candidate 1:** Allir opinbreytingar á bakglugga, loftfæri og skiptala sem ætlað eru til notkunar af notandum í aftanum bílna eiga að því að hægt sé að slökkva þeim með meðhöndlun af dráttarlæti sem mun er fyrir aftan bólgunni sem fer yfir R-stig innan efna í framanstaðum.
**Candidate 2:** Allir upphylkisflæði á afturslu, húðendur og þilfari, sem ætlaðir eru til notkunar af einstaklingum í afturhluta ökutækisins, skulu geta verið offnar með skipti sem er stjórnund raðað hjá ökuma og er staðsett fram á hlutaþéttu hliðar sem fer yfir R-staðir fyrstu sætur.
**Candidate 3:** Allar höðvindurir, skiptir sem er upp henni og rauðunir sem eru ætluð fyrirtækjum í enda vagnarins skulu hægt að slökkva með skipti sem er stjórnunarskipti á fyrir við og er sett fyrir fram á flatri yfirgegnum sem gagnegi R-stöðum fyrir sæti.
**Candidate 4:** Hverja afturslökk, skuggaskipti og voru skipti sem ætlaðir eru fyrir notendum á afturslæti ökutækisins skal geta verið skiptur aftur í slökki með ræðingvarðandi skipti sem verður í framhluta miðlæga línu sem stuttir R-staðir í framansetur.
**Candidate 5:** Allar takkrúmptir, takkstæður og hlaupir, sem ætlaðir eru til notkunar hófuþega í aftastfæri ökutækisins, skulu geta verið slökkt af með því að stýra með flugvallarstýringu sem er í fyrir sig frá lóðreiknum borðlínnum sem gegnast R-þéttum á framsetningu sætana.
**Candidate 6:** Allir bakglas, tegundir á hálfvegg og þörmum, sem ætlaðir eru til notkunar sem sjálfir hafa stað í aftan bil vélins, skulu hægt að koma á við á ökumennafæstri skiptistikki sem er í fænistri við ferðarmálaþátt.
**Candidate 7:** Öll bakgluggi, húðafæðir og skiptir upp með skiptispilum, sem ætluð eru til notkunar fyrir færa í eftirrækti ökutækisins, skulu vera búin til að skiptast við innan gegn ökumenn sjálfmælum þess milli, sem er í fyrirhliði vöðvalegra upp- og niðurlosrunarflaks sem hefur mesta atkomið R-stöðum í framansetturnar.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:ema:767 · U</summary>

**Source:** Therefore, docetaxel must not be used during pregnancy unless clearly indicated.
**Semantic decision:** U — Pregnancy prohibition retained, but none clearly preserves the clinical-indication exception.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Því má ekki nota docetaxel meðan á meðgöngu stendur nema brýna upplýsingar liggja fyrir um það.
**Candidate 1:** Því má ekki nota docetaxel á meðgöngu nema sprauta sé snún.
**Candidate 2:** Því má ekki nota doketaxel á meðgöngu nema brýna ákvarðanir til kynna það.
**Candidate 3:** Því má ekki nota docetaxel á meðgöngu nema greinilega áður sé til kynna.
**Candidate 4:** Því má ekki nota docetaxel á meðgöngu nema greinilega megi gefa til.
**Candidate 5:** Því verður ekki að nota docetaxel á meðgöngu nema brýna efni geri til kynna það.
**Candidate 6:** Því má ekki nota dócetaxel á meðgöngu nema brýna sjúkdóm sé til staðar.
**Candidate 7:** Því má ekki nota dócetaxel á meðgöngu nema skýrt séð til um að gera.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:opensubtitles:996 · P</summary>

**Source:** What kind of man would that make me?
**Semantic decision:** P — Exact source/hypothesis semantic reuse from card127: What kind of man would that make me retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Hvers konar maður myndi það gera mig?

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eso:919 · F</summary>

**Source:** "Thanks to several giant telescopes currently under construction, including ESOs E-ELT and the NASA/ESA/CSA James Webb Space Telescope due to launch for 2018, we will soon be able to study the atmospheric composition of these planets and to explore them first for water, then for traces of biological activity.
**Semantic decision:** F — Atmospheric composition, construction and launch are corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** „Takinn er við nokkrar stóra sjónaukar sem eru í framhaldshreyminu, þar á meðal ESO E-ELT og James Webb Space Telescope NASA/ESA/CSA sem verður að fara í reynd fyrir árs 2018, getum við nánast líkamaleif í lofthjúpum þessara reikistjarna og rannsaka þá fyrst um vatn og síðan um einkenni líffræðilegra virkni.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:opensubtitles:3607 · F</summary>

**Source:** Well, that makes you ugly and stupid.
**Semantic decision:** F — Ugly is replaced by an unrelated cloud/sky word.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Það gerir þig skýja og heimskur.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eea:698 · U</summary>

**Source:** Only days that can be worked should be included when Saturdays and Sundays are not worked they should not be included, the same with public holidays).
**Semantic decision:** U — Some workable-day exclusion is recognizable, but weekend and public-holiday conditions are not reliably faithful.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Aðeins þægir skal dagsetningar sem má vinna á, ekki þær nema sára og sunnudagsetningar séu vinna, og það sama við opinbera fríar).
**Candidate 1:** Einungis skal taka til daga sem átt má vinna á, ef ekki er vinna á sólarhringum og sólarheimdamönum, skal þau ekki taka til, eins og almennum fríar).
**Candidate 2:** Aðeins daga sem má vinnast eiga að taka að skrá þegar eigi verndast í laugardagana og laugardagana eiga ekki að taka að skrá, öfugt um opinbera fríedaga).
**Candidate 3:** Einnig skal taka þungum fyrir hér að framan að einnig séu dögum sem má vinna í sámótt og sólarhringum, einungis ekki við þeim dögum, sem er hins vegar búið að vinna.
**Candidate 4:** Einungis skal taka til daga sem má vinna og ekki einu sinni daga skal taka til rýmistöðva, hverja fyrstigildi, eða daga sem ekki vinna skal ekki taka til.
**Candidate 5:** Einnig skal taka bara þá dagsetur sem má vinnu um sig þegar ekki er vinnuskrifað á laugardagana og dögudegi skal þeim ekki taka til, eins og um almenna fríar er rætt.
**Candidate 6:** Einungis skal taka til daga sem hyggja má vinnu að þeir er ekki tekið í félagi, ef ekki er vinnustaður af laugardagum og laugardagum skal þeim ekki taka til, sama við opinbera fríar).
**Candidate 7:** Aðeins þær daga skulu tekið til meðferðar þegar ekki er vinna á sólarhringum og sólarborgum, eins og líka skal fylgja almennum fríegundum).

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eea:1991 · F</summary>

**Source:** Paragraph AG27 is amended and after paragraph AG29, paragraph AG29A is added.
**Semantic decision:** F — The AG prefixes identifying the amended paragraphs are lost.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Í 27. lið er breytt og eftir 29. lið bætist við 29. lið A.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:ema:2013 · P</summary>

**Source:** There is no evidence to suggest that eptotermin alfa alters fertility.
**Semantic decision:** P — No evidence of an eptotermin alfa fertility effect is retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Ekki er nein merki til að sýna fram á að eptotermin alfa breytti frjósemi.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eea:281 · F</summary>

**Source:** The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.
**Semantic decision:** F — Maturity-band, former/latter and residual long/short relations are corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Framfæra (sá eftirfarandi) sem samsvarast við síðari (fyrri) í tilteknum útfallarbrjóstagrein skulu vera samsvarandi stöður í þeim brjótagreini, en ósamsvarandi stöður skulu vera fyrir hana í sama brjótagreini.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:ema:1718 · F</summary>

**Source:** Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.
**Semantic decision:** F — Possible decreases in pharmacodynamic effects lose the decrease direction; inducer modifier is also unclear.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Samhliða gjöf edoxabans og P-gp örvaðs rífampicíns leiddi til minnkaðrar meðal AUC fyrir edoxaban og skertri helmingunartíma, sem getur haft mögulega áhrif á lyfhrifum.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:ema:325 · F</summary>

**Source:** If you get lower abdominal pain, gain any weight rapidly, feel sick or are vomiting or if you have difficulty in breathing, talk to your doctor straight away who might ask you to stop using this medicine (see in section 4 under “Serious side effects”).
**Semantic decision:** F — Most symptoms/instructions now retained, but lower-abdominal location is lost as generic stomach pain.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Ef þú færð magaverkjum, þyngjast hraðlega, finnur fyrir ógleði eða hefur uppköst eða ef þú hefur erfiðleikar við öndun, skaltu tafarlaust ræða við lækninn sem kann að spyrja þig um að hætta notkun lyfsins (sjá kafla 4 undir „Alvarlegar aukaverkanir“).

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eea:1585 · P</summary>

**Source:** The Commission shall submit a final evaluation report at the end of the Programme.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Inspected / Correct indices:** [2] / [2]
**Candidate 0:** Framkvæmdastjórnin skal leggja fram endanleg matsskýrslu að lokum áætluninni.
**Candidate 1:** Framkvæmdastjórnin skal leggja fram endanleg matsskýrslu eftir að áætlanirnar hafa komið í kjölfar.
**Candidate 2:** Framkvæmdastjórnin skal leggja fram endanlega matsskýrslu við lok áætlunarinnar.
**Candidate 3:** Framkvæmdastjórnin skal leggja fram endanlega matsskil á lokum áætluninnar.
**Candidate 5:** Framkvæmdastjórnin skal leggja fram endanlega matsskýrslu eftir áætlunina.
**Candidate 6:** Framkvæmdastjórnin skal leggja fram endanleg matsskýrslu eftir að áætlunin er lokið.
**Candidate 7:** Framkvæmdastjórnin skal leggja fram endanlegar matsskýrslu samkvæmt áætluninni.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eso:924 · F</summary>

**Source:** ESO was delighted to welcome Italys Minister of Education, Universities and Research, H.E. Stefania Giannini, to the ceremony, which was also attended by the Italian Consul General in Munich, Renato Cianfarani, the ESO Council President, Patrick Roche, and the Italian ESO Council Delegates, Nicolò DAmico (who is also President of INAF) and Matteo Pardo, Scientific Attaché at the Italian Embassy in Berlin.
**Semantic decision:** F — Italy is changed to Iceland and institutional/person roles are materially corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** ESO var ánægð af því að viðtaka Stefania Giannini, íslandar háskólastjóri, sem var innlendum tilbúin í sérfræðinga og rannsókna, og viðkomandi íslandsríkis- samræðustjóri í Múnich, Renato Cianfarani, Patrick Roche, forseti ráðsins ESO, og delegatir íslands á ráði ESO, Nicolò DAmico (sem er einnig forseti INAF) og Matteo Pardo, vísindamálaráðherra íslands í Börsledda.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:ema:704 · F</summary>

**Source:** The most frequently reported adverse reaction was acne, which was generally mild.
**Semantic decision:** F — Acne is replaced by a ball/bump word.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Algengasta aukaverkunin sem greint var frá var kúlu, sem var yfirleitt væg.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eso:206 · F</summary>

**Source:** The survey was sensitive to planets between 75 million kilometres and 1.5 billion kilometres from their stars (in the Solar System this range would include all the planets from Venus to Saturn) and with masses ranging from five times the Earth up to ten times Jupiter.
**Semantic decision:** F — Seven candidates change distance magnitude; candidate4 fixes billion but changes planets to plants and corrupts the Solar-System/mass qualifiers.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Skoðunin var næmant fyrir reikistjörnur á milli 75 milljón km og 1,5 milljón milljón km frá stjörnur (í sólkerfinu fylgir það öll reikistjörnur frá Venus til Saturn) og með massafjölda á milli fimm sinnum gildis ríkisins og tíu sinnum gildi Júpítrs.
**Candidate 1:** Skýringin var hræðilegur við reikistjörnur á milli 75 milljón km og 1,5 milljón milljón km frá stjörnunum (í sólkerfinu nemur allar reikistjörnurnar frá Venus til Surtur) og með massaverkun frá fimm sinnum jörðu til tíu sinnum Júpíturnar.
**Candidate 2:** Slíkt öryggi haldið sér til að rannsaka reikistjörnur á milli 75 milljóna km og 1,5 milljóna km frá stjörnum (í sólkerfinu eru þessi bil yfir öll reikistjörnur frá Venus til Saturn) og með massamagni á bilinu frá fimm sinnum jörða upp í tíu sinnum Júpíturnum.
**Candidate 3:** Til greiningar var næm við reikistjörnur sem eru á milli 75 milljón km og 1,5 milljón km frá stjörnum (í sólkerfinu eru allar reikistjörnurnar frá Venus til Saturn í himninum) og á massamagni frá fimm sinnum jörð að tíu sinnum Júpíter.
**Candidate 4:** Skýrslugjöf var næm fyrir plöntur á bilinu 75 milljón km að 1,5 milljarða km frá stjörnur (hér í sólkerfinu engar planetir eru bula undir Venus og stjörnin Saturn) og massan á milli fimm sinnum líkan og tíu sinnum Júpíturnar.
**Candidate 5:** Skoðunin var nægðrar varanir á reikistjörnum milli 75 milljón km og 1,5 milljón km frá stjörnunum (í sólkerfinu fylgir það öll reikistjörnurnar frá Vensu til Saurons) og massareikistökurnar fengu frá fimm sinnum jörð uppfærðar hinum tíðnum tén sinnum Júpíter.
**Candidate 6:** Rannsóknin var nægileg fyrir reikistjörnur á bilinu 75 milljón kílómetra til 1.5 milljón milljón kílómetra frá stjörnunum (í sólkerfinu innihélt hún öll reikistjörnurnar frá Venus til Saturn) og massafjölda á bilinu frá fimm sinnum jörðinni upp í tíu sinnum Júpíturnum.
**Candidate 7:** Skoðunin var meðvæn fyrir reikistjörnur á milli 75 milljón km og 1,5 milljón km frá stjörnunum (í sólkerfinu voru þessar bil með öllum reikistjörnunum frá Vensu til Sáterni) og með þyngd á milli fimm sinnum yfirvöld og tíu sinnum Júpíters.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eso:446 · P</summary>

**Source:** “Astronomers have waited for data like this for over a decade.
**Semantic decision:** P — Astronomers waiting over ten years for such data is retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** „Stjörnufræðingar höfðu bíðið um gögn eins og þessi í meira en tíu ár.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eea:281 · F</summary>

**Source:** The amount of the former (latter) which are matched by the latter (former) in a given maturity band shall be the matched positions in that band, while the residual long or short position shall be the unmatched position for the same band.
**Semantic decision:** F — Every candidate corrupts maturity bands, former/latter matching and residual positions.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Skömmtun af þeirri (hinn) sem samrýmast hinn (fyrri) á því gáttu skal vera samrýmteigarstörf í þessari gáttu, en eftirfyrir langa eða stafaða störf skal vera ósamrýmteigarstörf fyrir sama gátt.
**Candidate 1:** Hlutfall uppsaffinnar (uppsaffinnar) sem stunda í látasta (fyrri) stöðum skal vera sá uppsaffinn stöðu í svipuðu stöðugt íbúðahluta, en hlutastöðum áfram eða aftur að þeim stöðugt íbúðahluta skal vera sú uppsaffinn stöðu sem ekki er svipaður í svipuðu íbúðahluta.
**Candidate 2:** Ílætið fráfenginn (læstur) sem virðist henni (fráfenginn) í tiltekinni útvarpsbili skal vera utvarpsstöður sem virðist, þar sem eftirlætið er stóru eða stánar útvarpsstöð.
**Candidate 3:** Magn úr fyrri (sáttari) sem sér sambærilegt við sáttari (fyrirliggjandi) í tiltekinni þroskaþætti skal vera sambærilegar stöður í þessum þroskaþætti, en eftirlistur stöður í lengri eða stuttri þroska skal vera ósambærilegar stöður við þann þroskaþætti.
**Candidate 4:** Magn miðla (frummið) sem samhæft er af síðari (fyrari) miðla (frummið) yfir í viðkomandi vörnakvarða skal vera samhæft staðurinn í þeirri vörnakvarða, á meðan viðtakarnir eða stakarnir sem eftir eiga ekki að vera samhæft staðurinn í sama vörnakvarða.
**Candidate 5:** Fjöldi framsómum (síðast) sem eru samsvarandi við síðast (framsómum) í tilteknum vinstri (líng) nafnumiðalínnum skal vera samsvarandi stöðvar í þeim nafnumíðalinu, svo fjárhæfnar langann eða stóran stöðvinnu skal vera ósamsvarandi stöðvar í sama nafnumíðalinu.
**Candidate 6:** Fyrri (sölu) skammturinn sem hentar á meðferð eftirfarandi (fyrri) meðferð, í tilteknum aldurshluta, skal vera upphaflegi skammturinn í þeim hluta, en lasar skammturinn sem hentar ekki meðferð, skal vera óupptakaður skammtur í sama hluta.
**Candidate 7:** Hlutfall fyrri (sáttarmála) sem sáttarmálarann (sáttamál), sem sáttarmála, samhvarfir í þeim nýttunarflokki, skal vera samhvarfstaðan í því nýttunarflokki, en staðarlengi eða státlengi hvorki sáttamála skal vera staðarlengi eða státlengi sáttamálans, sem samhvarfir ekki, í þeim nýttunarflokki.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:ema:1582 · P</summary>

**Source:** The treatment-free period, however, should take into account the pharmacological properties of the products used previously.
**Semantic decision:** P — Candidate6 retains a period without treatment and consideration of pharmacological properties of previously used medicines.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [6]
**Candidate 0:** Meðan á meðferðarfraslum er að ræða skal hún athygli á lyfjafræðilegum eiginleikum lyfja sem notað voru áður.
**Candidate 1:** Að því er varðar án meðferðartímabil skal hún íhuga lyfjamenganleika lyfja sem notaðar hafa verið áður.
**Candidate 2:** Meðferðarframtíminn skal þó taka tillit til lyfjafræðilegra eiginleika lyfja sem hafa verið notaðir áður.
**Candidate 3:** Hins vegar skal meðferðarframanlegur tíminn taka tillit til lyfjafræðilegrar eiginleika lyfja sem notuð voru áður.
**Candidate 4:** Í meðferðarfrigið ætti þó að hafa fyrirhugga þá aðferðafrigið áfram fyrir einkenni lyfjafræðilega af völdum lyfja sem notaðir hafa verið áður.
**Candidate 5:** Hins vegar skal meðferðarfraslunin taka tillit til lyfjafræðilegra eiginleika lyfinna sem hafa verið notaðir áður.
**Candidate 6:** Meðan án meðferðar tíminn hefur að alveg í huga skal vísa til lyfjafræðilegra eiginleika lyfja sem hafa verið notaðir áður.
**Candidate 7:** Meðferðarframtímabilinu skal þó íhuga lyfjafræðilegar eiginleika lyfja sem notaðir hafa verið áður.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eso:726 · F</summary>

**Source:** They wanted to study the interaction between a young generation of stars and the cold clumps that were assembling into these first galaxies.
**Semantic decision:** F — Cold clumps become pressures and the assembly relation is corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þeir vildu rannsaka milliverkun á yngri hóp stjarna og kaltum þrýstingum sem var að setja sér í þessi fyrstu vetrarbrautum.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:opensubtitles:1012 · P</summary>

**Source:** I'll do whatever you ask.
**Semantic decision:** P — Promise to do whatever is asked retained despite tense/inflection.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Ég geri hvað sem þú baðir.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eso:1051 · F</summary>

**Source:** The technique used by Teague, which derived averaged variations in the flow of the gas as small as a few percent, revealed the impact of multiple planets on the gas motions nearer to the star.
**Semantic decision:** F — Flow variation and multiple planets are mistranslated.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Tæknið sem Teague notaði, sem leiddi til meðalþéttni breytilegra flæðis gassins eins minna en nokkur prósent, sýndi áhrif fjölskyldu reikistjarna á flutninga gassins nálægri stjörnunni.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eea:1461 · U</summary>

**Source:** All industrial uses of gas are considered.
**Semantic decision:** U — Gas/work-use scope partly retained, but industrial use and considered versus specified remain unclear.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Í öllum atvinnuframleiðsluminnustörunum er tekið tillit til gasa.
**Candidate 1:** Í upplýsingum um notkun gasins í vinnustofnunum er taldur um öll notkun.
**Candidate 2:** Í öllum vinnuauðkenni gasins er tekið tillit.
**Candidate 3:** Í allri starfsemi gjaldagas er íhugað.
**Candidate 4:** Í allar gjöf gasa í vinnuhúsum er talið upp.
**Candidate 5:** Tilgreindar eru allar notkunar á gas í vinnu.
**Candidate 6:** Tilgreint er um öll starfsemi gjalds.
**Candidate 7:** Tilgreint er um öll atvinnustarfsemi gegn gas.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eea:609 · F</summary>

**Source:** Special payments for shift work.
**Semantic decision:** F — No candidate preserves shift work.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Sérfræðingarbótar fyrir mótskráða starf.
**Candidate 1:** Sérstöku greiðslur fyrir staðdum vinnu.
**Candidate 2:** Sérstakt greiðslur í starfsmeðaltali.
**Candidate 3:** Sérstöku greiðslur til að íhafa starfsemi.
**Candidate 4:** Sérstöku greiðslur fyrir þrægjöfnun.
**Candidate 5:** Sérstöku senda til að starfa eftir stöðum.
**Candidate 6:** Sérfræðilegar greiðslur fyrir stöktum starf.
**Candidate 7:** Sérþætur greiðslur fyrir röðað krafta.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eso:501 · U</summary>

**Source:** The team used data from the UVES spectrograph on ESOs Very Large Telescope in Chile (to determine the properties of the star accurately), the Carnegie Planet Finder Spectrograph (PFS) at the 6.5-metre Magellan II Telescope at the Las Campanas Observatory in Chile, the HIRES spectrograph mounted on the Keck 10-metre telescope on Mauna Kea, Hawaii as well as extensive previous data from HARPS (the High Accuracy Radial velocity Planet Searcher) at ESOs 3.6-metre telescope in Chile (gathered through the M dwarf programme led by X. Bonfils and M. Mayor 2003–2010 described here).
**Semantic decision:** U — Several names and sizes retained, but telescope/spectrograph, prior-data and M-dwarf programme relations remain unreliable.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Hópurinn notuðu gögn úr UVES fyriröntuheqt sem vörnastyrk ESO Very Large Telescope í Chile (til að ákvarða eiginleika stjarna á góðan nákvæmni), Carnegie Planet Finder Spectrograph (PFS) á 6,5, mælikvarðanum Magellan II á Las Campinas stjörnustöðinni í Chile, HIRES fyriröntuheqt á Keck 10 mælikvarðanum í Mauna Kea á Hawaii, og námlegar gögn úr HARPS (HARPS for High Accuracy Radial velocity Planet Searcher) á 3,6 mælikvarðanum í Chile hjá ESO (búið hér, með M dwarf prófið undir forystu X. Bonfils og M. Mayor 2003-2010).
**Candidate 1:** Hópurinn notuðu gögn úr UVES litrófsritunni Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjarnans nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5 m Magellan II sjónaukni í Las Campanas stjörnustöðinni í Chile, HIRES litrófsritunni á Keck 10 m stjörnustjörnunni í Mauna Kea í Hawaii ásamt umfangsmikil fyrri gögn úr HARPS (High Accuracy Radial velocity Planet Searcher) sjónaukinni ESO í Chile sem er 3,6 m (sagað af X. Bonfils og M. Mayor 2003-2010 og lýst hér).
**Candidate 2:** Hópurinn notaði gögn úr UVES litrófið Very Large Telescope ESO í Chile (að því er varðar að ákvarða eiginleika stjörnu á vissum hátt), Carnegie Planet Finder Spectrograph (PFS) í Magellan II sjónauka 6,5 mítra í Las Campanas stjörnustöðinni í Chile, HIRES litrófið á Keck 10 mítra sjónauka í Mauna Kea í Hawaii, og líka gæðið geymslu hugbundinna gögnum úr HARPS (High Accuracy Radial velocity Planet Searcher) í Chile (sagað er í bókunni X. Bonfils og M. Mayor 2003-2010, sem lýsir að færið er í M þverbætið, sem stjórnduðu X. Bonfils og M. Mayor 2003-2010).
**Candidate 3:** Hópurinn notaði þau gögn úr UVES litrófsritanna á Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjarna á nákvæmri hátt), Carnegie Planet Finder Spectrograph (PFS) á 6,5 metra Magellan II litrófsritanum á Las Campanas stjörnustöðinni á Chile, HIRES litrófsritann á Keck 10 metra stjörnustjörnunni á Mauna Kea á Hawaii, sem og gallt gögn úr HARPS litrófsritanum (High Accuracy Radial velocity Planet Searcher) á 3,6 metra litrófsritunni at ESO í Chile (háttar frá M dwarf verkefninu sem leiddi af X. Bonfils og M. Mayor áraði 2003-2010 sem lýst er hér, sem framkallað hefur eftir).
**Candidate 4:** Líkamsrannsóknin notaði gögn úr UVES geimflæði ESO Very Large Telescope í Chile (til að meta eðlilegan eiginleika stjarna) Carnegie Planet Finder Spectrograph (PFS) á 6,5 m Magellan II geimruna í Las Campanas stjörnustöðinni í Chile, HIRES geimflæðið í Keck 10 m geimruna í Mauna Kea á Hawaii og meðal löndar aðrar gögn úr HARPS (High Accuracy Radial velocity Planet Searcher) í Chile sem ESO sert fyrir 3,6 m geimrun um Shapley (ledi af X. Bonfils og M. Mayor 2003-2010 sem lýst er hér) bólgur.
**Candidate 5:** Teiminn notaði upplýsingum frá UVES litrófsritinu Very Large Telescope ESO í Chile (til að ákvarða eiginleikar stjarnanar nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5-metrar Magellan II sjónauka í Las Campanas stjórnarstöðinni í Chile, HIRES litrófsritinu á Keck 10- metra sjónauka í Mauna Kea, Hawaii og frekar gögn frá HARPS (High Accuracy Radial velocity Planet Searcher) á 3,6-metrar sjónauka ESO í Chile (gerðin hafa verið lokuð með M dwarfs verkefninu sem leitað hefur X. Bonfils og M. Mayor 2003-2010 sem lýst er hérna).
**Candidate 6:** Hópurinn notuði gagna frá UVES litrófsritinu Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjarnans nákvæmlega), Carnegie Planet Finder Spectrograph (PFS) á 6,5 m litrófsritinu Magellan II í Las Campanas stjörnustöðinni í Chile, HIRES litrófsritinu sem er á Keck litrófsritinu 10 m á Mauna Kea í Hawaii og líka umfangsrík gagna úr HARPS (High Accuracy Radial Velocity Planet Searcher) litrófsritið í 3,6 m litrófsritinu ESO í Chile (söfnuð í M dwarf verkefninu X. Bonfils og M. Mayor 2003-2010 sem lýst er hér fyrir sig).
**Candidate 7:** Hópurinn notaði gögn úr UVES litrófi Very Large Telescope ESO í Chile (til að ákvarða eiginleika stjarnanns mjög nákvæmlega) Carnegie Planet Finder Spectrograph (PFS) á 6,5-metrykum Magellan II sjónauka á Las Campanas stjörnustöðinni í Chile, HIRES litrófið á Keck 10-metrykum sjónauka á Mauna Kea í Hawaii og langt gengið gögn úr HARPS (High Accuracy Radial velocity Planet Searcher) í Chile, sem ESO mennti með 3,6-metrykum sjónauka (X. Bonfils og M. Mayor 2003–2010, sem lýst er hér, fannst gögnin með M-dverf prófi), sem hvarfur sáttamáli voru á gengið við viðtökum á stjörnum.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eso:323 · F</summary>

**Source:** They were able to make the sharpest direct observation ever , of the centre of a distant galaxy, the bright quasar 3C 279, which contains a supermassive black hole with a mass about one billion times that of the Sun, and is so far from Earth that its light has taken more than 5 billion years to reach us.
**Semantic decision:** F — Billion becomes million in both mass and travel time; black-hole content is corrupted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þau gáfu til þess að gera skarpsmesti beinu sjónauki á miðju fjarlægri vetrarbrauta, 3C 279, sem er bjartur kvarnfrumur sem inniheldur öflugan massa súrlífsöfn sem er um milljón sinnum stærri en sólin og er svo fjarlægt frá Jörðinni að ljósið hennar hefur tekið meira en 5 milljón ára til okkar.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eea:922 · P</summary>

**Source:** Development of CPE is checked as described in Part I.III.4.
**Semantic decision:** P — Candidate6 checks CPE development with the correct nested PartI/III.4 reference.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [6]
**Candidate 0:** Tilvik CPE þróað er metað eins og lýst er í kafla III.4 í II. hlið.
**Candidate 1:** Rannsókn á þróun CPE er farið að skýra sviði I. III.4.
**Candidate 2:** Frekari þróun CPE er lokið eftir þeirri mælingu sem lýst er í liður III.4 í I. hluta.
**Candidate 3:** Framdæling CPE er endurskoðað sem lýst er í hluta III.4 í I. kappanum.
**Candidate 4:** Framfæring CPE er kannað samkvæmt því sem lýst er í III.4. hluta I. þáttar.
**Candidate 5:** Skoðun var á þróun CPE, eins og lýst er í IV-lið í III. hluta I. hversu komið var fram.
**Candidate 6:** Skoðað er þróun CPE eins og fram kemur í lið III.4 í I. hlið.
**Candidate 7:** Verið er að kanna þróun CPE eins og lýst er í það III.4. hálfsnið I. hvaða líka.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eso:464 · U</summary>

**Source:** With an estimated mass of four to five times that of Jupiter, it would be the least massive planet to be directly observed outside the Solar System.
**Semantic decision:** U — Mass range/direct viewing recognizable, but least-massive construction remains unclear.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þegar það er með fjögur til fimm sinnum þyngri massamagni en Júpíter væri það minnst þyngstu reikistjarna sem hefur verið tekið beinu sjón af utan sólkerfisins.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:opensubtitles:1169 · P</summary>

**Source:** They're pretty as can be, aren't they?
**Semantic decision:** P — Very pretty/cute and the tag question retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Þeir eru mjög sæt, ekki satt?

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eea:50 · F</summary>

**Source:** Similar studies, for at least three soil types, must be reported for all relevant metabolites, degrada tion and reaction products which in soil degradation studies account at any time for more than 10 % of the amount of active substance added.
**Semantic decision:** F — Soil types, degradation/reaction products and the >10% qualifying relation are corrupted or omitted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Í öllum þeim rannsóknum sem hafa ákvæði um það að verða sambærilegum skulu tilkynntar um sömu rannsóknir á að minnsta kosti þremur jarðefnum, fyrir öll viðkomandi umbrotsefni, leysis- og hlutabreyttr efni sem í rannsóknum á leysisjarðefnis uppfylla aðeins stuttu skammta af virku efninu sem bætt var við.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eso:765 · F</summary>

**Source:** “If it keeps spinning rapidly it might end its life in one of the most energetic explosions in the Universe, known as a long-duration gamma-ray burst,” says the lead scientist of the project, Hugues Sana, of the University of Leuven in Belgium.
**Semantic decision:** F — Every candidate corrupts the spinning condition, gamma-ray-burst meaning or other key scientific details.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** „Ef hún helst snúast hratt kann hún að enda lífi sínu í meiri innöndunarskapi alheimisins, sem kallast langhringa gammasetn,“ sagði Hugues Sana, aðalhæfileiki verkefnisins við tilliti til kynns krausum geislana í sér fyrir sig á sérstaklega langhringa gammasetn, sem hafa stórt innöndunarnum.
**Candidate 1:** „Ef það hreyfir vel áfram, getur það farið úr lífi sínu í einhverri mesta orkunskapinn í alheiminu og þekkuð er lengdskipti gammönu-geislun fyrir mynda“ segir leiðandi vinnslu- kerfið Hugues Sana við Leuven- háskóla í Belgíu.
**Candidate 2:** „Ef hann helst hreyfja á hraða hátt getur hann komist leit af lífi sínu í einu af meist orkulegustu beinandi sprengingu alheimsins, þekkt upp í kveiktis gammal þrýstingu,“ sagði Hugues Sana, leiðtogi verkefnisins, ástæðan við stjörnufræði við Leuven- háskóla í Belgíu.
**Candidate 3:** „Ef hún hefur áfram hrein endurhreinir hringir getur hún verið ein apenni meira öflugasta sprengingu alheimsins, sem þegar kallast langvarandi gamma-losi,“ sagði Hugues Sana, aðalhæfileikarfara verkefnisins við miðlunarfar, um evíslamálarhæfileikann í Leuven- í Belgíu.
**Candidate 4:** „Ef það hreyfir sér hratt getur það endað líf sinni á einu af erfiðustu sprengingu Vetrarbrautarinnar, kallast langtíma gammaveikið sprengistökkur,“ segir Hugues Sana, hinn frumfra umsval, við verkefninu, við framkvæmdargrein stofnunarinnar í Leuven í Belgíu.
**Candidate 5:** „Ef það hægir áfram í hraðri vetrarbraut verður það líka lokið á einum af öflugustu brennslu í alheiminu, sem nefnist langvarandi gammagrasslagur (gamma-ray burst),“ segir Hugues Sana, leitarhálfar verkefnisins í Leuven arneti í Belgíu.
**Candidate 6:** „Ef það virðist snúast hraðlega kann það að enda lífið í einum vegna langtímarvíssistungna líffærisfjölsa, sem kallast langtímarvíssastungna gamma-geminn, í alheiminu,“ sagði leita vinnsluþjónusta insjómsýsins, Hugues Sana, frá Leuven almenna reiknifélagi í Belgíu.
**Candidate 7:** „Ef hún hreyfir sig hratt getur hún farið með lífinu í einn af öflugustu sprengingum alheimsins, þar sem nánu kveðið „langtíma gammöðursstyrkur““ segir leiðandi þátttakandi vísindamaðurinn á verkefninu, Hugues Sana, í Leuven-universíti í Belgíu.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eea:85 · P</summary>

**Source:** For the estimation of these concentrations all relevant information on the plant protection product and on the active substance must be taken into account.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Inspected / Correct indices:** [1] / [1]
**Candidate 0:** Til að áætla niðurstöður við þessar þéttni skal taka tilhögun af allum viðeigandi upplýsingum um plöntuverndarvörunni og virka efnið.
**Candidate 1:** Við mat á þessum styrkleikum ber að taka tillit til allrar viðeigandi upplýsinga um plöntuverndarvöruna og virka efnið.
**Candidate 2:** Til að meta þessi þéttni skal taka tilhlýðilega tillit til þess að svo miklu nemandi upplýsinga um plöntuvarnarefni og virka efni sem þessi þéttni er á.
**Candidate 3:** Við mat á þessum styrkleika skal íhuga allar viðeigandi upplýsingar um plöntuvarnarefnið og virka efnið.
**Candidate 4:** Við mat á þessum styrkleika verður að taka tillit til öllum viðeigandi upplýsinga um plöntuverndarvörn og virka efnið.
**Candidate 5:** Við mat á þessum styrkleikum skal taka tillit til allra viðeigandi upplýsinga um plöntuverndarvörn og virka efnið.
**Candidate 6:** Við áætlanir á þessum þéttni skulu taka tillit til allra viðeigandi upplýsinga um plöntuverndarvörn og virka efnið.
**Candidate 7:** Við mat á þessum styrk skulu taka til athygli allra viðeigandi upplýsinga um plöntuverndarvörn og virka efnið.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:ema:1192 · P</summary>

**Source:** It is used to prevent pregnancy.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Inspected / Correct indices:** [1] / [1]
**Candidate 0:** Hún er notað til að koma í veg fyrir þungun.
**Candidate 1:** Það er notað til að koma í veg fyrir þungun.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:opensubtitles:2508 · F</summary>

**Source:** Rose, we have a guest in the living room.
**Semantic decision:** F — Living room is changed to the home.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Rose, við erum með gest í heimilinu.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:ema:1394 · F</summary>

**Source:** The most commonly reported adverse reactions (≥ 20%) among patients treated with both belatacept- based regimens (MI and LI) up to Year 3 are diarrhoea, anaemia, urinary tract infection, peripheral oedema, constipation, hypertension, pyrexia, nausea, graft dysfunction, cough, vomiting, leukopenia, hypophosphataemia, and headache.
**Semantic decision:** F — Every candidate mistranslates critical adverse-event items or treatment/frequency qualifiers.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Algengustu aukaverkanirnar sem greint var frá hjá sjúklingum sem fengu bæði reglur sem byggðar voru á belatacepti (MI og LI) allt til ára 3 eru niðurgangur, blóðleysi, þvagræs, bælingur í burtu, træstataldi, háþrýstingur, hita, ógleði, skilvirkni grunnliðar, hósk, uppköst, öndunarfrumubrest, blóðflysið og andlitsvernd.
**Candidate 1:** Algengustu aukaverkanirnar sem komu fram hjá sjúklingum sem fengu bæði meðferð með belatacept-ferlinu (MI og LI) allt til ára 3 eru niðurgangur, blóðleysi, þvagrind, vefjaskemmdir, hægðatregða, háþrýstingur, hiti, ógleði, grunnvirkni grúnna, hósti, uppköst, hvítaflögu, blóðfosfatsminnkun og höfuðverkur.
**Candidate 2:** Yfirleitt tilkynntar aukaverkanir (≥ 20%) hjá sjúklingum sem hafa verið meðhöndlaðir með bæði belatacept-bundnum meðferðum (MI og LI) allt til ár 3 eru niðurgangur, blóðleysi, niðurgangsbólga, útbrot í líkamshvötum, hægðatregðu, háþrýstingur, hjáveiki, ógleði, skertri frumudrátt, hósti, uppköst, hvíldarfæð, blóðsólfæði, ofskort.
**Candidate 3:** Algengustu aukaverkanirnar sem fram komu hjá sjúklingum sem fengu beina reglum með belatacepti (MI-og LI) allt til árs 3 (≥ 20%) eru niðurgangur, blóðleysi, sýking í þvagverkunum, bólgu í útlimum, hægðatregðu, háþrýstingur, heiður, ógleði, skortskerðing, hósti, uppköst, minnkun á blóðkorni, blóðpúfaðsblóðskort og höfuðverk.
**Candidate 4:** Algengustu aukaverkanirnar sem fram komu hjá sjúklingum sem fengu bæði reglanir sem byggðar voru á belatacepti (MI og LI) til árs 3 (≥ 20%) eru niðurgangur, blóðleysi, þvagrannslu í þvagkerfi, bólga við brjósti, þvaglag, háþrýstingur, hiti, ógleði, truflun á grúnni, hósti, uppköst, hvítblóðfall, blóðfosfatslækkun og höfuðverkur.
**Candidate 5:** Algengustu aukaverkanirnar sem greint var frá (≥ 20%) hjá sjúklingum sem fengu meðferð með bæði belatacept-bundnum meðferðaráætlunum (MI og LI) fram í 3. ári eru niðurgangi, blóðleysi, þvagrind, bólgusótt sem til er í útlægri lífi, hægðatregðu, háþrýstingur, hiti, ógleði, skortsbrest, hósti, uppköst, svepparfræðilegú lekkun, blóðpísfærin og höfuðverkur.
**Candidate 6:** Algengustu aukaverkanirnar (≥ 20%) sem greint hefur verið frá hjá sjúklingum sem fengu meðferð með belatacept-bundnum meðferðaráætlunum (MI og LI) allt að ári 3 eru niðurgangur, blóðleysi, sýking í þvagmeðferðarvegis, bólga við brúnir, verulega hægðatregðu, háþrýstingur, hiti, ógleði, óvirkni gegn tíðna, hósti, uppköst, blóðleysi, ofsýrnaskort, höfuðverkur og hornbínum.
**Candidate 7:** Algengustu aukaverkanirnar sem greint var frá hjá sjúklingum sem fengu bæði meðferð með belatacept- byggðum meðferðareglum (MI og LI) allt að ári 3 eru niðurgangi, blóðleysi, sýking í þvagsvöðum, útbrot í lífeyrissvæðum, mæði, háþrýstingur, hiti, ógleði, veiruvetnismerki, hósti, uppköst, sáðbólgur, blóðflagnafæð og höfuðverkur.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eea:1552 · F</summary>

**Source:** The analytical result shall be reported as x +/– U whereby x is the analytical result and U is the expanded measurement uncertainty, using a coverage factor of 2 which gives a level of confidence of approximately 95 % (U = 2u).
**Semantic decision:** F — Expanded uncertainty and coverage factor are mistranslated.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Greina skal niðurstöður greiningar sem x +/– U þar sem x er niðurstöður greiningar og U er útþekkt mælitækni, með því að nota 2 gildi fyrir umfrymisfalt og gefur það um 95% öryggi (U = 2u).

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eso:491 · P</summary>

**Source:** ALMA can observe in different frequency bands.
**Semantic decision:** P — Candidate0 conveys that ALMA can observe across different frequencies; the preposition and omitted explicit band noun are rough but the core capability is retained.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [0]
**Candidate 0:** ALMA getur athugað á milli mismunandi tíðni.
**Candidate 1:** ALMA getur fylgst með framkvæmdaferil að mismunandi þætti.
**Candidate 2:** ALMA getur rannsakað milli samsættunar í mismunandi þéttnibreiðum.
**Candidate 3:** ALMA getur gaknt á mismunandi geislalengdum.
**Candidate 4:** ALMA getur rannsakað milli annarra tíðansbrennslubandanna.
**Candidate 5:** ALMA getur mælt á mismunandi fjölmyndarbrennslu.
**Candidate 6:** ALMA getur metað í fleiri breytilegum beinbreytum.
**Candidate 7:** ALMA getur fylgst með tjörnunum á mismunandi fyrningagreinum.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:ema:1100 · P</summary>

**Source:** If you miss a dose, take your next dose as scheduled.
**Semantic decision:** P — Missed dose and next scheduled dose retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Ef þú gleymir eftir skammti skal taka næsta skammt eins og áætlað er.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eea:15 · F</summary>

**Source:** Where studies are conducted using active substance produced in the laboratory or in a pilot plant production system, the studies must be repeated using active substance as manufactured, unless it can be justified that the test material used is essentially the same for the purposes of environmental testing and assessment.
**Semantic decision:** F — All eight lose the pilot-production-system distinction and/or the equivalence exception for environmental testing.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Ef rannsóknir eru framkvæmdar með virk efni sem framleitt er í rannsóknarskírteini og í prófunarskeiðis- kerfi skulu endurtaki rannsóknirnar með virk efni eins og það er framleitt, nema aðild sé nauðsynleg við að rannsóknarefnið sé í grundvelli jafnvægi við umhverfisrannsóknir og meta.
**Candidate 1:** Ef rannsóknir eru gert með virk efni sem framleitt er í rannsóknarstofu eða í pakkningarráðstöfunum í vinnsluinginum, skal endurtaka rannsóknirnar með virk efni eins og það er framleitt, nema komið sé fram á ábyrgð til þess að prófunardefnin sem notuð er er í raun í heila samræmi við prófunir á umhverfið.
**Candidate 2:** Ef rannsóknir eru gerðar með virka efni sem framleitt er í rannsóknarstöðum eða í rannsóknarstöðum sem gefið er upp efnisins, þá verður að endurtaka rannsóknirnar með efnið sem afhengist er, nema gerð sé útskýrt að prófunarefnið sem notað er sé í raun hátt íhuguð samanborið við umhverfismál.
**Candidate 3:** Ef rannsóknir eru gerðar með virka efni sem framleitt er í rannsóknarstofu eða í starfsmálarefni sem gefið er upp á rannsóknarstofu eru þær þarf að endurtaka með virku efni sem framleitt er, nema vera getur röksettur á að prófunarefnið sem notuð er sé í raun vera að öllu leyti svipuð af markmiði umhverfisprófunar- og -mat.
**Candidate 4:** Ef rannsóknir eru gerðar með virkum efni sem framleitt er í rannsóknarkerfi eða í rannsóknarkerfi sem er notaður með virkum efni, skal endurskoða rannsóknina með virkum efni eins og þau eru framleidd, nema fram komi rétt fyrir að prófunarefnið, sem notuð er, sé í alvöru sá sama við umhverfisrannsóknir og mat.
**Candidate 5:** Ef rannsóknir eru gerðar með virka efninum, sem framleitt hefur verið í rannsóknarstöðinni eða í forkvöðum, verður að endurtaka rannsóknirnar með virka efninum eins og það er framleitt, nema stuðlað sé að því að prófunarefnið sé í síðari lagi samanburðarhæfi við mælingar á umhverfismálum.
**Candidate 6:** Ef verkefni eru gerðar með virka efni sem framleitt er í rannsóknarstofu eða í forspýningarbúnaði og ef störf verkefnanna er gert á grunnstofum skal endurtaka rannsóknana með virku efni eins og það er framleitt, nema auðkennd sé að prófunarefnið, sem notað er, sé í ýmsum þáttum jöfur eins við umhverfisrannsóknir og -metan.
**Candidate 7:** Ef rannsóknir eru gerðar með virka efni sem framleiðið er í rannsóknastofunni eða í áætlunarstofnun, þá verður þær endurtaktar með virku efni eins og það er framleiðið, nema fram geti lagt mat á að prófunarefnið er í raun egillegt eins.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:ema:1718 · P</summary>

**Source:** Co-administration of edoxaban with the P-gp inducer rifampicin led to a decrease in mean edoxaban AUC and a shortened half-life, with possible decreases in its pharmacodynamic effects.
**Semantic decision:** P — Candidate6 retains P-gp-inducer rifampicin, decreased mean AUC, shorter half-life and possible reduced pharmacodynamic effects.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [6]
**Candidate 0:** Samhliða gjöf edoxabans ásamt P-gp örvaðilum, rifampicini, leiddi til minnkaðs mína AUC for edoxabani og minni callhaldarlyfs, til mögulegrar minnkunar á lyfhrifum.
**Candidate 1:** Samhliðagjöf edoxabans og viðbótarlyfja-P-gp, rifampicins, leiddi til minnkaðs AUC fyrir edoxaban og minnkunar helmingunartíma, sem getur haft áhrif á minnkun lyfhrifar.
**Candidate 2:** Notkun edoxabans samtímis rifampicíni, P-gp örva, leiddi til minnkar á meðal AUC fyrir edoxaban og minnkaðs helmingunartíma, sem gæti haft mögulega áhrif á lyfhrifum.
**Candidate 3:** Samhliða lyfjagjöf edoxabans og P-gp örva rífampicins leiddi til lækjun á meðal AUC fyrir edoxaban og skertum helmingunartíma, sem hugsanlega leikdu til minnkaðrar lyfhrifar.
**Candidate 4:** Samhliða notkun edoxabans og P-gp örvaðar rífampicíns leiddi til minnkaðs meðaltals AUC fyrir edoxaban og minnkunar helmingunartíma, sem geta komið fram minnkun á lyfhrifum þess.
**Candidate 5:** Notkun edoxabans samtímis rifampicini, P-gp örva, leiddi til minnkaðrar meðal AUC fyrir edoxaban og takmarkaðrar helmingunartíma, sem gæti gert að minnka áhrifum þess á lyfhrif.
**Candidate 6:** Samtímis gjöf edoxaban og P-gp örvið rifampicins leiddi til minnkaðs á meðal AUC fyrir edoxaban og styttingar á helmingunartíma, sem hugsanlega leiddi til minnkaðs lyfhrif.
**Candidate 7:** Samhliða lyfjagjöf edoxabans og P-gp virkjaðs rífampicíns leiddi til minnkaðs meðal AUC fyrir edoxaban og minnkaðs helmingunartíma, með mögulegri lækkun á lyfhrifum.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eea:534 · U</summary>

**Source:** Council Directive 74/60/EEC of 17 December 1973 on the approximation of the laws of the Member States relating to the interior fittings of motor vehicles.
**Semantic decision:** U — Directive/date retained, but translation of interior fittings is uncertain.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Tilskipun ráðsins 74/60/EBE frá 17. desember 1973 um samræmingu á lögum aðildarríkjanna varðandi innri fyrirbúningar ökutækja.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eso:302 · F</summary>

**Source:** This is because the tilt of the orbit is normally unknown.
**Semantic decision:** F — Orbital tilt is omitted or replaced by unrelated concepts in every candidate.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Það er vegna þess að það er venjulega óþekkt sem típ svæðisins er.
**Candidate 1:** Það er vegna þess að stojakilt grunnlægur geimstig er vanamálið óþekkt.
**Candidate 2:** Það er vegna þess að bláæðin er venjulega óþekkt.
**Candidate 3:** Þetta er vegna þess að þjóðgerð röðunarlega er óþekkt.
**Candidate 4:** Það er vegna þess að hálfalengd reikslisins er yfirleitt óþekkt.
**Candidate 5:** Þetta kemur vegna þess að ástæðan í umferðinni er venjulega óþekkt.
**Candidate 6:** Þetta er vegna þess að fækkun róarins er yfirleitt ekki þekkt.
**Candidate 7:** Þetta er vegna þess að umframhaldandi vetrarbrauturinn er vanalega ekki þekkt.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eea:1216 · F</summary>

**Source:** That task shall be coordinated with the existing regional cooperation programmes and shall include, where appropriate, the organisation of relevant training activities.
**Semantic decision:** F — Regional cooperation programmes become existing operations.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Þessi verkefni skal samræmd við þá rekstrur sem eru í gildi og skal það innihalda, eftir því sem við á, skipulagningu viðeigandi þjálfunaráðstöfunum.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eso:768 · P</summary>

**Source:** Both components are classed as O-type stars.
**Semantic decision:** P — Both components being O stars is preserved; inflection errors are minor.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Bæði hlutin eru flokkaðar sem O- stjörnur.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:opensubtitles:480 · F</summary>

**Source:** Now we have enough evidence to charge you with murder.
**Semantic decision:** F — Charging someone with murder becomes an unrelated defecation verb.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Nú hafa við nóg sönnunargögn til að skíta þig um morð.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eso:70 · P</summary>

**Source:** This is only the sixth of these huge storms to be spotted since 1876.
**Semantic decision:** P — Candidate6 retains only the sixth huge storm detected/reported since1876.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / [6]
**Candidate 0:** Þetta er aðeins sexustur af þessum stórum andstyrkum sem komið hefur fram síðan 1876.
**Candidate 1:** Þetta er aðeins sjötthöfs einsa og þessi risagerðir samanlegt síðan árið 1876.
**Candidate 2:** Þetta er aðeins sjöttna af þessum öflugum slökkum sem fyrir eftir hefur komið fram síðan frá 1876.
**Candidate 3:** Þetta er aðeins sjöttháttur þessum miklu stormi sem fékkst síðan árið 1876.
**Candidate 4:** Þetta er aðeins sjötta þessar eirir skjálfta sem komið hefur fram síðan 1876.
**Candidate 5:** Þetta er aðeins sjökthugur stormur sem hafa verið sýndir síðast árið 1876.
**Candidate 6:** Þetta er aðeins sjötta þessi miklir storma sem greint hefur verið úr síðan 1876.
**Candidate 7:** Þetta er aðeins sex stóru hættum sem höfðu komið fram síðan 1876.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eea:1461 · F</summary>

**Source:** All industrial uses of gas are considered.
**Semantic decision:** F — Gas is replaced by weapons.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Í allri notkun vopna er tekið tillit til.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:opensubtitles:3209 · P</summary>

**Source:** Because it's not safe there.
**Semantic decision:** P — Because it is not safe there is retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Því það er ekki öruggt þar.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:ema:1406 · U</summary>

**Source:** Concomitant use with yellow fever vaccine and with live virus and bacterial vaccines (see section 4.5).
**Semantic decision:** U — Candidate5 supplies the correct English parenthesis and vaccine relations, but the Icelandic yellow-fever term remains malformed; not certified as a faithful Icelandic translation.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Rannsókn með bóluefnum gegn gultsvefu og lifandi veiruvefnum og bakteríuvöfum (sjá kafla 4.5).
**Candidate 1:** Samhliða notkun með llárannar bóluefni, og lifandi veirusjúkrar- og bakteríuhvata bóluefni (sjá kafla 4.5).
**Candidate 2:** Samhliða meðferð með brúggi-vefja fyrir gula-vefju og með lifandi veirusótt og bakteríusótt (sjá kafla 4.5).
**Candidate 3:** Samhliða notkun með fangavínskortelyfi og fangavínskortelyfi með lifandi veirus og bakteríumbóluefnum (sjá kafla 4.5).
**Candidate 4:** Samhliða notkun á bóluefni gegn gulvafæri og lifandi veirus og bakteri (sjá kafla 4.5).
**Candidate 5:** Samhliða notkun milli bóluefna gegn gultbólgu (yellow fever vaccine) og lifandi veiru- og baktería-bóluefna (sjá kafla 4.5).
**Candidate 6:** Samhliða notkun gegnsæi gegn gula sýkingu og lifandi veirusakvilli og bakteriakmála (sjá kafla 4.5).
**Candidate 7:** Notkun samhliða barnaefri bóluefni og lifandi veirusótt og sýkingusótt (sjá kafla 4.5).

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eso:775 · U</summary>

**Source:** A team of astronomers, led by Istvan Dékány of the Pontificia Universidad Católica de Chile, has now used data from this survey, taken between 2010 and 2014, to make a remarkable discovery - a previously unknown component of our home galaxy, the Milky Way.
**Semantic decision:** U — Leadership, dates and parts of the unknown-component claim improve, but discovery/home-galaxy linkage is not reliably clear.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 6, 7] / []
**Candidate 0:** Hópur stjarnvísindamanna, gefinn undir forystu Istvan Dékány frá Pontificia Universidad Católica de Chile, notið gögnum úr þessari rannsókn, sem gerð var á tímabilinu 2010-2014, til uppgjörs sem haldið er hættu - einstaka samstæði Vetrarbrautarinnar, sem ekki varð hefur verið þekkt áður.
**Candidate 1:** Hópur stjarnvísindamanna, hjálfar István Dékány, Pontificia Universidad Católica de Chile, notuður gögnum úr þessu skoðun, sem gerðar voru 2010 til 2014, til uppgjörs á mikilvægu hátt - það inniheldur fyrr ekki þekkt þátt í okkar heimskjá, Vetrarbrautinni.
**Candidate 2:** Hópur stjörnufræðinga, undir forystu Istvan Dékány hjá Pontificia Universidad Católica de Chile, hefur nýlega notið gögnum úr þessari rannsókn, sem gerð var á tímabilinu 2010-2014, til frábrugða uppgötvunar - uppáhaldsnokkur þessarar vetrarbrautar, Vetrarbrautarinnar.
**Candidate 3:** Hópur stjörnufræðinga, yfir hönd Istvan Dékány frá Pontificia Universidad Católica de Chile, hefur nýlega notað gögnum úr þessum rannsókn, sem tóku sér stað á milli 2010 og 2014, til þess að gera ófyrirsögulegri uppgötvun - þeirra undirstöðu á heimakjörinu, Vetrarbrautinni.
**Candidate 4:** Hópur stjörnufræðinga, undir forystu Istvan Dékány og Pontificia Universidad Católica de Chile, hefur nú notuð gögn frá þessari rannsókn, sem tekið hefur verið á milli 2010 og 2014, til svernilegrar uppgötvunar - áfram höfðu ekki verið borin fram einhver þessar eril minnkerstu hlutur Vetrarbrautarinnar.
**Candidate 5:** Hópur stjörnufræðinga, undir forystu Istvan Dékány frá Pontificia Universidad Católica de Chile, notuðu gögnum úr skoðuninni, sem gerð var 2010-2014, til þess að gera upptöku uppgötvun - fyrir hliðar þekktur hluti í heimakjöllinni víxli.
**Candidate 6:** Hópur stjörnufræðinga, undir forystu Istvan Dékánys af Pontificia Universidad Católica de Chile, hefur haft viðbót um nánar atriða á samanburðargögnum sem komið voru fram á öðrum ársverkefninu sem stóð á milli 2010 og 2014, sem var sérstaklega óþekkt þátt af heimsverðu vetrarbrautinni, Vetrarbrautinni.
**Candidate 7:** Hópur stjörnufræðinga, leittar af Istvan Dékány við Pontificia Universidad Católica de Chile, fann í þessari skynun af miðlunarmyndun á milli 2010 og 2014 nánar reikistarfsemi - einhvern sem hefur orðið frá, sem er aðalstafan inntakslæknis Vetrarbrautarinnar.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eea:1914 · P</summary>

**Source:** This Regulation shall enter into force on the third day following that of its publication in the Official Journal of the European Union.
**Semantic decision:** P — Candidate5 faithfully preserves entry into force on the third day after EU Official Journal publication.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 5, 7] / [5]
**Candidate 0:** Reglugerð þessi öðlast gildi fyrri daginn eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.
**Candidate 1:** Reglugerð þessi öðlast gildi síðar á þriðja degi eftir að hún var birt í Stjórnartíðindum Evrópusambandsins.
**Candidate 2:** Reglugerð þessi öðlast gildi þriðja daga eftir að hún var birt í Stjórnartíðindum Evrópusambandsins.
**Candidate 3:** Reglugerð þessi öðlast gildi þriðja dag eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.
**Candidate 4:** Reglugerð þessi öðlast gildi þriðja degi eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.
**Candidate 5:** Reglugerð þessi öðlast gildi á þriðja degi eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.
**Candidate 7:** Reglugerð þessi öðlast gildi þriggja daga eftir að hún birtist í Stjórnartíðindum Evrópusambandsins.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eso:491 · U</summary>

**Source:** ALMA can observe in different frequency bands.
**Semantic decision:** U — Observing and frequency bands improve, but added numbers as the observed object is unclear.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** ALMA getur fylgst með tölum á mismunandi tíðnibandum.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eea:1716 · U</summary>

**Source:** The competent authorities of Gabon have reacted promptly to these concerns, indicating their commitment to take all measures necessary to implement applicable ICAO standards and enforce compliance with these standards as soon as possible.
**Semantic decision:** U — Prompt action/commitment retained; standards implementation and compliance enforcement remain unclear.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Lögbær yfirvöld í Gabón hafa svarað þessum áhættu tafarlaust og benda til þess að þeir hafi skuldbindingu til að gera allar nauðsynlegar ráðstafanir til að framfylgja viðeigandi staðlana ICAO og gera þau gildi eins fljótt og unnt er.

</details>

<details><summary>t2000728 · G8 · p13official21:dev:eea:2037 · U</summary>

**Source:** Those criteria should not be considered to be exhaustive.
**Semantic decision:** U — Exhaustiveness/completeness remains ambiguous with adequacy or perfection.
**Inspected / Correct indices:** [0, 1, 2, 3, 4, 6, 7] / []
**Candidate 0:** Þessi viðmiðanir skulu ekki teljast fullnægjandi.
**Candidate 1:** Þessi viðmiðanir skulu ekki teljast nákvæmar.
**Candidate 2:** Þessar viðmiðanir skulu ekki teljast fullkomnir.
**Candidate 3:** Ekki skal telja þessi viðmiðanir fullkomnir.
**Candidate 4:** Ekki skal telja þessar viðmiðanir fullkomnir.
**Candidate 6:** Sem ekki er að halda að þessum viðmiðunum séu fullnægjandi.
**Candidate 7:** Ekki skal telja þessar viðmiðanir fullnægjandi.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:eea:1194 · F</summary>

**Source:** It should provide the Commission and the Member States with objective, reliable and comparable information and data on maritime safety and on ship pollution prevention to enable them to take any necessary initiatives to enhance the measures in place and to evaluate their effectiveness.
**Semantic decision:** F — Objective information becomes continuous information, and ship pollution is narrowed/altered.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Hún skal veita framkvæmdastjórninni og aðildarríkjunum upplýsingar og gögn sem eru áframhaldandi, áreiðanleg og samanburðarhæfar um öryggi á sjávarbærum og um aðferðir til að koma í veg fyrir mengun afurða úr skipum til þess að þau geti tekið nauðsynlegar frumkvæði til að auka ráðstafanirnar sem liggja fyrir og meti skilvirkni þeirra.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:ema:1765 · P</summary>

**Source:** Take this leaflet or some tablets with you so that your doctor knows exactly what you have taken.
**Semantic decision:** P — Taking leaflet/tablets so the doctor knows exactly what was taken is retained.
**Inspected / Correct indices:** [0] / [0]
**Candidate 0:** Taktu þessi fylgiseðil eða töflur með þér svo að læknirinn þekki nákvæmlega hvað þú hefur tekið.

</details>

<details><summary>t2000728 · greedy · p13official21:dev:opensubtitles:1159 · U</summary>

**Source:** Somebody get me a picture of the girl.
**Semantic decision:** U — Requesting a girl's picture retained, but the recipient me is omitted.
**Inspected / Correct indices:** [0] / []
**Candidate 0:** Einhver fá mynd af stelpunni.

</details>

## 逐句结果 / All 256 anchor translations


<details><summary>Anchor: p13official21:test:opensubtitles:2621</summary>

**Source:** I'm glad you found one another."
**Reference:** Ég er svo ánægð að þið funduð hvort annað."
**Before:** Mér gleður að þú hafir fundið annað hvort."
**After:** Ég er ánægður að þú hafir fundið annan."

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2543</summary>

**Source:** Ready your breakfast and eat hearty for tonight we dine in hell!
**Reference:** Eldið ykkur morgunmat og matist vel því í kvöld snæðum við í helvíti!
**Before:** Búðu þig til morgunmatar og borðaðu heilaga fyrir kvöldinni við borðum í helvítinn!
**After:** Búið þér morgunmat og borðaðu heilaga fyrir kvöldinni við borðum í helvítinn!

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:3404</summary>

**Source:** A mother never gives up on her child.
**Reference:** Móðir snýr aldrei baki við barni sínu.
**Before:** Mamma gefur aldrei upp á barni sínu.
**After:** Mamma gefur aldrei upp á barni sínu.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2128</summary>

**Source:** Don't you worry about those dope smokers and nudists down below there?
**Reference:** Hefurðu ekki áhyggjur af dóphausunum og striplingunum þarna?
**Before:** Ekki hafa áhyggjur af þeim doppaheyrum og náttúruhæðum niðri í þessu?
**After:** Ekki hafa áhyggjur af þessum döpumrúmstjörnum og náttuglum þarna niðri?

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:1340</summary>

**Source:** Why are you fucking with our minds?
**Reference:** Af hverju ruglarðu hugsanir okkar?
**Before:** Af hverju ertu að ræða á heimilin okkar?
**After:** Af hverju ertu að reiða á hugsvörunnar okkar?

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:1252</summary>

**Source:** Jonny didn't ask us to pay him back for...
**Reference:** Jonny rukkaði okkur ekki um...
**Before:** Jonny bað okkur ekki um að borga honum tilbúi fyrir...
**After:** Jonny bað okkur ekki um að borga honum tilbúi fyrir...

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:1810</summary>

**Source:** General Hershberg's got me investigating a Medal of Honour.
**Reference:** Hershberg ofursti fékk mig til að rannsaka heiðursorðuna.
**Before:** Hershberg hefur mér farið í rannsókn á glæsir.
**After:** Hershberg hefur mér verið að rannsaka glæsir.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:3337</summary>

**Source:** But maybe, if we got away from here, if we went somewhere safe, it could be different.
**Reference:** En kannski ef við kæmumst burt héðan, ef við færum á öruggan stað, gæti það breyst.
**Before:** En kannski, ef við farið úr hér, ef við farið til öruggs staðar, gæti það verið annars konar.
**After:** En kannski, ef við færum frá hér, ef við fórum til öruggs staðar, gæti það verið öðruvísi.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:387</summary>

**Source:** At least it's not gonna happen at this place.
**Reference:** Það gerist að minnsta kosti ekki hérna.
**Before:** Það verður ekki til hérna.
**After:** Það verður ekki að gerast hérna.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:38</summary>

**Source:** Disco Universe Sweepstakes are just a week away.
**Reference:** Disco Universe keppnin er eftir viku.
**Before:** Disco Universe Sweepstakes er bara viku fyrir.
**After:** Disco Universe Sweepstakes er bara viku fyrir.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:3622</summary>

**Source:** No, you can't have ice cream for breakfast.
**Reference:** Nei, þú getur ekki fengið ís í morgunverð.
**Before:** Nei, þú getur ekki fengið ískrím fyrir morgunmat.
**After:** Nei, þú getur ekki fengið ísþremmi á morgunmat.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:1319</summary>

**Source:** Should she go slinking around as if she disgraced herself?
**Reference:** Á hún að læðast um líkt og hún þurfi að skammast sín?
**Before:** Á hún að fara í skjálfti um um sem hún hafði misstakast sjálfan sér?
**After:** Á hún að fara í skildum um um sem hún hafði misstörfu sig?

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2209</summary>

**Source:** Much has been made of the hostility between our countries.
**Reference:** Mikið hefur verið gert úr fjandskapnum milli ríkja okkar.
**Before:** Miklum hefur verið gerð af ósáttinu milli landa okkar.
**After:** Miklum hefur verið gerð af óþýði milli landa okkar.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:284</summary>

**Source:** If you muck this up, you will have me to answer to.
**Reference:** Ef þú spillir þessu er mér að mæta.
**Before:** Ef þú mislir þetta verður ég að svara.
**After:** Ef þú mislir þetta verður ég að svara.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:1803</summary>

**Source:** What are you planning on telling her?
**Reference:** Hvað ætlarðu að segja henni?
**Before:** Hvað ætlarðu að segja henni?
**After:** Hvað ætlarðu að segja henni?

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:3265</summary>

**Source:** There's a police convention out there.
**Reference:** Það er lögregluráðstefna þarna úti.
**Before:** Það er lögreglukonar úti.
**After:** Það er lögreglukonarinnur þarna.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2355</summary>

**Source:** He shoved his cock inside me and humped me three times.
**Reference:** Hann tróð skaufanum inn í mig og hamaðist þrisvar.
**Before:** Hann skræði kynlautinn sína inn í mig og humpaði mig þremur sinnum.
**After:** Hann skræði kynlíf sitt inn í mig og humpaði mig þremur sinnum.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:1913</summary>

**Source:** Only the guard knew I took the tapes.
**Reference:** Vörðurinn einn vissi að ég tók spólurnar.
**Before:** Bara verndarið vissi að ég tók taflan.
**After:** Bara verndarið vissi að ég tók tauparnar.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2508</summary>

**Source:** So, I'm guessing Mike's already told you about his girlfriend?
**Reference:** Mike hefur líklega sagt þér frá kærustunni sinni?
**Before:** Svo ég er að grunni að Mike hafi sagt þér frá kærustunni sínum?
**After:** Svo ég er að gera hyndur á að Mike hafi þegar sagt þér frá kærustunni sínum?

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:1959</summary>

**Source:** I noticed you wrapped up in the libretto.
**Reference:** Ég sá að þú lifðir þig inn í óperutextann.
**Before:** Ég sá þig bundinn í skörluninu.
**After:** Ég sá þig í röð í sköpunarkerfinu.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:1869</summary>

**Source:** You've given me something to work on now.
**Reference:** Þú hefur gefið mér efnivið til að vinna úr núna.
**Before:** Þú hefur gefið mér eitthvað til að vinna á núna.
**After:** Þú hefur gefið mér eitthvað til að vinna á núna.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:3620</summary>

**Source:** Is there some other road we can take?
**Reference:** Getum við farið einhverja aðra leið?
**Before:** Er einhver annar leið sem við getum tekið?
**After:** Er einhver annar leið sem við getum tekið?

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:1596</summary>

**Source:** I stuffed it in my pocket.
**Reference:** Ég setti hana í vasann.
**Before:** Ég skrúfaði það í vaktina.
**After:** Ég skildi það í vattið.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:750</summary>

**Source:** What we need to do is find out what the spirit needs, and then get it back to her.
**Reference:** Fáum að vita hvað andinn þarf og látum hana fá það.
**Before:** Það sem við þurfum að gera er að finna hvað geislann þarf og fá hann til hennar.
**After:** Það sem við þurfum að gera er að finna hvað sprautan þarf og þá færa hana aftur til hennar.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2721</summary>

**Source:** No, but one day, I'll take that cane away...
**Reference:** Nei, en einn góðan veðurdag á ég eftir að taka stafinn...
**Before:** Nei, en eitt dagur, færi ég þessu stóðinn...
**After:** Nei, en einn daginn, ég fær þennan stöng...

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2205</summary>

**Source:** What did you want to talk to me about?
**Reference:** Hvað vildirðu ræða við mig um?
**Before:** Hvað vildirðu tala við mig um?
**After:** Hvað vildirðu tala við mig um?

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2627</summary>

**Source:** Jafar is large and in charge!
**Reference:** Jafar leikur lausum hala og ræður ríkjum!
**Before:** Jafar er stór og í stjórn!
**After:** Jafar er stór og í stjórn!

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2164</summary>

**Source:** You didn't have the guts to do it yourself.
**Reference:** Þú hafðir ekki kjark til þess sjálfur.
**Before:** Þú hefur ekki hægt til að gera það sjálfur.
**After:** Þú hafðir ekki undanþegi til að gera það sjálfur.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:156</summary>

**Source:** I'm gonna write a book about Leland P. Fitzgerald.
**Reference:** Ég ætla að skrifa bók um Leland P. Fitzgerald.
**Before:** Ég ætla að skrifa bók um Leland P. Fitzgerald.
**After:** Ég ætla að skrifa bók um Leland P. Fitzgerald.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:1601</summary>

**Source:** I don"t plan on wearing it that long.
**Reference:** Ég ætla ekki að vera lengi í honum.
**Before:** Ég ætla ekki að vera í því lengi.
**After:** Ég ætla ekki að vera í því lengi í því.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2843</summary>

**Source:** These pants will give you a miracle.
**Reference:** Þessar buxur munu færa þér kraftaverk.
**Before:** Þessar pantar munu gefa þér sársauk.
**After:** Þessir burtir munu gefa þér sársauka.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:834</summary>

**Source:** Just that you're doing a really good job.
**Reference:** Bara að þú stæðir þig vel.
**Before:** Bara að þú gerir mjög góða vinnu.
**After:** Bara að þú gerir mjög góða vinnu.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:854</summary>

**Source:** Teddy was furious that I'd taken tranquillizers.
**Reference:** Teddy varð vitlaus yfir að ég notaði róandi lyf.
**Before:** Teddy var uppískur af því að ég hafði tekið róandi lyf.
**After:** Teddy var uppöflinn af því að ég hafði tekið róandi lyf.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:3044</summary>

**Source:** Isn't there someone in some league, who's left- footed?
**Reference:** Er ekki einhver í einhverri svona deild sem er örfættur?
**Before:** Er ekki einhver í einhverri hópi sem er höfður höndinni til vinstri?
**After:** Er enginn í einhverri hóp sem er höfður frá hliðar?

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2978</summary>

**Source:** Give Sydelle one more thing to complain about.
**Reference:** Þá fær Sydelle enn eitt umkvörtunarefnið.
**Before:** Gefðu Sydelle eitt fleiri að gruna um.
**After:** Gefðu Sydelle eitt meira til að gruna um.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2775</summary>

**Source:** You knew they were coming!
**Reference:** Þú vissir að þeir væru að koma!
**Before:** Þú vissir að þeir komu!
**After:** Þú vissir að þeir komu!

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2998</summary>

**Source:** You can make all the jokes you want, Alvin, but not even you can make this interesting.
**Reference:** Þú getur grínast eins og þú vilt, Alvin, en jafnvel þú getur ekki gert þetta áhugavert.
**Before:** Þú getur gert allt sem þú vilt, Alvin, en ekki einu sinni gert þetta áhugaverð.
**After:** Þú getur gert allt það sem þér vantar, Alvin, en ekki einu sinni gert þetta áhugaverð.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:437</summary>

**Source:** Remember when I had great hair?
**Reference:** Manstu þegar ég var með frábært hár?
**Before:** Manstu þegar ég var með frábær hár?
**After:** Manstu þegar ég var með frábæra hár?

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2920</summary>

**Source:** If I'm not Anastasia, the Empress will know right away.
**Reference:** Ef ég er ekki Anastasía, mun keisaraynjan vita það strax.
**Before:** Ef ég er ekki Anastasiu mun hvernig fyrir sig viti henni.
**After:** Ef ég er ekki Anastasiu mun hvernig fyrst vissi henni.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2253</summary>

**Source:** Should I go talk to Sverrir?
**Reference:** Á ég að fara að tala við Sverri?
**Before:** Á ég að fara og tala við Sverrir?
**After:** Á ég að fara og tala við Sverrir?

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:486</summary>

**Source:** No. I was not given the panties, last night or any other time.
**Reference:** Það lét mig enginn fá nærbuxurnar, hvorki í gærkvöldi né í annan stað.
**Before:** Nei, ég fann ekki í panteyrinn, síðan kvöldi eða öðru sinni.
**After:** Nei, ég var ekki gefinn pantönum, í gærkvöldi eða öðru sinni.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2997</summary>

**Source:** Yes, I sleep with every American you send my way.
**Reference:** Já, ég sef hjá öllum Könum sem þú sendir til mín.
**Before:** Já, ég sofði með hvert Amerískum sem þú sendir í átt.
**After:** Já, ég sofði með hvert Amerískum sem þú sendir mér.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:1878</summary>

**Source:** That's not what Optimus would want.
**Reference:** Optimus hefði ekki viljað það.
**Before:** Það er ekki það sem Optimus vildi.
**After:** Það er ekki það sem Optimus myndi vilja.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:936</summary>

**Source:** Ma'am, I need the gentleman's signature so we can begin.
**Reference:** Ég þarf að fá undirskrift hans svo við getum byrjað.
**Before:** Frú, ég þarf undirskriftur herra til að byrja.
**After:** Frú, ég þarf undirskriftur herra svo við getum byrjað.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:1121</summary>

**Source:** Of course you're right, Starling... but it doesn't change anything.
**Reference:** Auðvitað er það rétt, Starling... en það breytir engu.
**Before:** Að mikið er þú rétt, Starling... en það breytir ekkert.
**After:** Að sjálfsögðu ertu rétt, Starling... en það breytir ekkert.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2571</summary>

**Source:** Since when do you ask me personal questions?
**Reference:** Síðan hvenær spyrðu mig persónulegra spurninga?
**Before:** Frá hverju spyrðu mig persónulegar spurningar?
**After:** Hvenær spyrðu mig persónulegar spurningar?

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:1317</summary>

**Source:** General Barnicke's gone until tomorrow morning.
**Reference:** Barnicke kemur ekki fyrr en í fyrramálið.
**Before:** Barnicke hefur farið til baka.
**After:** Barnicke hefur farið til burtu í morgun.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:669</summary>

**Source:** Plus I get to wear a crown.
**Reference:** Svo fæ ég að hafa kórónu.
**Before:** Og ég fær að vera með hrygg.
**After:** Og ég fær að vera í hrygg.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:3260</summary>

**Source:** Why didn't you tell me you were looking?
**Reference:** Því sagðirðu ekki að þú værir að leita?
**Before:** Af hverju sagðirðu mér ekki að þú værir að leita?
**After:** Af hverju sagðirðu mér ekki að þú værir að leita?

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:3454</summary>

**Source:** And I work for Danny.
**Reference:** Og ég vinn hjá Danny.
**Before:** Og ég vinn fyrir Danny.
**After:** Og ég vinn fyrir Danny.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:1033</summary>

**Source:** I know Jeremiah a lot better than you guys.
**Reference:** Ég þekki Jeremiah mun betur en þið.
**Before:** Ég þekki Jeremiah betur en þið.
**After:** Ég þekki Jeremiah betur en þið.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:3071</summary>

**Source:** It takes time to get used to our climates.
**Reference:** Það tekur tíma að venjast loftslaginu.
**Before:** Það tekur tíma til að ná við umvarpum okkar.
**After:** Það tekur tíma til að ná þessið við umvarpum okkar.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2669</summary>

**Source:** Like houses, friendships need strong foundations.
**Reference:** Líkt og húsin þarf vináttan traustan grunn.
**Before:** Eins og hús þarf vinir sterkar grunn.
**After:** Eins og húsa þarf vinnumyndir sterkar grundvöllar.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:2130</summary>

**Source:** Because Mr. Doyle called and said you have not been there all week.
**Reference:** Því að herra Doyle hringdi og sagði að þú hafir ekki mætt alla vikuna.
**Before:** Því að Doyle hringdi og sagði að þú hefur ekki verið þar í viku.
**After:** Því að Mr Doyle hringdi og sagði að þú hefðir ekki verið þar í viku.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:3595</summary>

**Source:** Because I promise you it will get very ugly, very fast.
**Reference:** Því ég lofa þér að þetta verður fljótt ljótt.
**Before:** Því ég lofa þér að það verði mjög skrítið og fljótt.
**After:** Því ég lofa þér að það verður mjög skríti og fljótt.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:3484</summary>

**Source:** If you do not give me the house you promised I shall be forced to return to England.
**Reference:** Ef þú lætur mig ekki fá húsið eins og þú lofaðir neyðist ég til að fara aftur til Englands.
**Before:** Ef þú gefur mér húsinn sem þú lofaðir mér skal ég vera forðast til England.
**After:** Ef þú gefur mér húsinn sem þú lofaðir mér skal ég vera forðast til að fara til Englands.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:1537</summary>

**Source:** This could be your liver right now.
**Reference:** Þetta gæti verið lifrin í ykkur núna.
**Before:** Þetta gæti verið lifurinn þinn núna.
**After:** Þetta gæti verið lifurinn þinn núna.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:939</summary>

**Source:** Put it in the envelope, Mrs. Rochon.
**Reference:** Settu hann í umslagið, frú Rochon.
**Before:** Settu það í pakkanum, frú Rochon.
**After:** Settu það í pakkið, frú Rochon.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:1127</summary>

**Source:** Each one was printed by the same machine?
**Reference:** Voru þau öll prentuð á sömu vél?
**Before:** Var hver einn útsettur af sama vél?
**After:** Var hver einn útbúinn af sama vél?

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:997</summary>

**Source:** So is there a Mrs. Mysterio?
**Reference:** Er til einhver frú Dularfull?
**Before:** Er það ekki frú Mysterio?
**After:** Er það ekki frú Mysterio?

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:153</summary>

**Source:** It was utterly dark in the abyss before my feet.
**Reference:** Það var niðamyrkur í hyldýpinu við fætur mér.
**Before:** Það var öflugt dimmt í dalinni fyrir fótum mínum.
**After:** Það var öflugt dimmt í dalinni fyrir fótum mínum.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:609</summary>

**Source:** You can find everything I've described in a museum right now.
**Reference:** Þú getur séð þetta á hvaða safni sem er.
**Before:** Þú getur fundið allt sem ég lýst í geymsluverkið núna.
**After:** Þú getur fundið allt sem ég lýsti í geymsluverki núna.

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:343</summary>

**Source:** Did you see all the batteries that guy bought?
**Reference:** Sáuð hvað hann keypti mikið af rafhlöðum?
**Before:** Sástu alla jafnframt baterin sem maðurinn keypti?
**After:** Sástu alla rafbrennslur sem þessi gaur keypti?

</details>

<details><summary>Anchor: p13official21:test:opensubtitles:168</summary>

**Source:** I don't know, I've never met him.
**Reference:** Veit ekki, hef aldrei hitt hann.
**Before:** Ég hef ekki hitt hann nokkurn tímann.
**After:** Ég hef aldrei hitt hann.

</details>

<details><summary>Anchor: p13official21:test:eea:1780</summary>

**Source:** Annex A is replaced by Annex A to this Regulation.
**Reference:** Í stað viðauka A komi viðauki A við þessa reglugerð.
**Before:** A-fylgni komið í stað A-fylgis við þessa reglugerð.
**After:** A-fasmið er ísettur í stað A-ákvæða við þessa reglugerð.

</details>

<details><summary>Anchor: p13official21:test:eea:1814</summary>

**Source:** The producer must ensure that all wood originate from legal sources.
**Reference:** Framleiðandi skal tryggja að allur viður komi frá löglegum aðilum.
**Before:** Framleiðandinn skal tryggja að allt skerði sé úr löglegum upprunum.
**After:** Framleiðandi skal tryggja að allt sköfur séu úr löglegum upprunum.

</details>

<details><summary>Anchor: p13official21:test:eea:44</summary>

**Source:** The maximum duration of the studies is 24 months.
**Reference:** Rannsóknirnar mega að hámarki taka 24 mánuði.
**Before:** Hámarksgildi lengdar rannsóknanna er 24 mánuðir.
**After:** Hámarksgildi tímamagns rannsóknanna er 24 mánuðir.

</details>

<details><summary>Anchor: p13official21:test:eea:1471</summary>

**Source:** Prices including all taxes, levies and VAT.
**Reference:** Verð með öllum sköttum, álögðum gjöldum og VSK.
**Before:** Verð þar sem tilgreind er allar skattir, skattatöflur og gildaaukaverði.
**After:** Verð þar sem tilgreind er allar skattir, skattatökin og gildaaukaverða skattagátt.

</details>

<details><summary>Anchor: p13official21:test:eea:613</summary>

**Source:** Number of overtime hours paid in the representative month.
**Reference:** Fjöldi greiddra yfirvinnustunda í viðmiðunarmánuðinum.
**Before:** Fjöldi frávinnlaðra klukkustundanna sem greidd eru í fulltrúar mánuði.
**After:** Fjöldi frávinnlaðra stundanna sem greidd eru í fulltrúar mánuði.

</details>

<details><summary>Anchor: p13official21:test:eea:1322</summary>

**Source:** Assessment and verification: a declaration of compliance shall be provided.
**Reference:** Mat og sannprófun: leggja skal fram yfirlýsingu um að þessi viðmiðun sé uppfyllt.
**Before:** Mat og sannprófun: Leggja skal fram skýrslu um samræmi við kröfurnar.
**After:** Mat og sannprófun: Leggja skal fram skýrslu um samræmi við kröfur.

</details>

<details><summary>Anchor: p13official21:test:eea:1343</summary>

**Source:** THOD for aerobically non degradable organic substances is set to zero.
**Reference:** THOD fyrir lífræn efni, sem eru ólífbrjótanleg við loftháðar aðstæður, er núll.
**Before:** THOD fyrir líftengd, ódegraðandi, lífræna efni er sett í nálg.
**After:** THOD fyrir líftengd, ódegraðandi lífræna efni er sett í nálg.

</details>

<details><summary>Anchor: p13official21:test:eea:1565</summary>

**Source:** International cooperation is essential given the global nature of the problem.
**Reference:** Með tilliti til þess að vandinn er hnattræns eðlis er alþjóðleg samvinna nauðsynleg.
**Before:** Alþjóðlega samstarf er nauðsynlegt vegna alheimsáhrifanna á vandamálið.
**After:** Alþjóðlegur samstarf er nauðsynlegt vegna alþjóðlega vandamálsins.

</details>

<details><summary>Anchor: p13official21:test:eea:669</summary>

**Source:** Long-term breaks should be of more than one year.
**Reference:** Langvarandi hlé eru þau sem eru lengri en eitt ár.
**Before:** Langtíma frestir skulu vera lengur en eitt ár.
**After:** Langtíma frestir skulu vera lengri en eitt ár.

</details>

<details><summary>Anchor: p13official21:test:eea:607</summary>

**Source:** Years of career break in the current enterprise (optional).
**Reference:** Hve mörg ár hafa fallið úr í starfi hjá núverandi fyrirtæki (valkvætt).
**Before:** Ár af skipti í starfsáttamönnum í núverandi fyrirtæki (valfrjáls).
**After:** Ár af vinnustöðvum í núverandi fyrirtæki (valfrjáls).

</details>

<details><summary>Anchor: p13official21:test:eea:1503</summary>

**Source:** If this kind of costs exists, they will be reported separately.
**Reference:** Ef þess háttar kostnaður er fyrir hendi skal tilgreina hann sérstaklega.
**Before:** Ef slík kosti eru til koma þeir til skýrslu í sérstökum skilyrðum.
**After:** Ef slík kostnaður er til hægt verður að gefa útgáfu af þeim í sérstökum skýrslum.

</details>

<details><summary>Anchor: p13official21:test:eea:1855</summary>

**Source:** The product must be easily recyclable.
**Reference:** Það verður að vera auðvelt að endurvinna vöruna.
**Before:** Lyfið verður að vera auðvelt að endurnýja.
**After:** Vörunni skal vera auðvelt að endurvinna.

</details>

<details><summary>Anchor: p13official21:test:eea:615</summary>

**Source:** Annual days of sick leave not paid by the employer (optional).
**Reference:** Árlegur fjöldi leyfisdaga vegna veikinda sem vinnuveitandi greiðir ekki (valkvætt).
**Before:** Árslegar dagir fyrir sjúkdómsframsölu sem vinnuveitandi gefur ekki til (valfræðileg).
**After:** Árslegar dagir til sjúkratrygginga sem vinnuveitandi gefur ekki út (frjáls).

</details>

<details><summary>Anchor: p13official21:test:eea:1259</summary>

**Source:** This term of office is renewable once.
**Reference:** Heimilt er að endurnýja skipunartímann einu sinni.
**Before:** Þessi stund er endurnýttuð einu sinni.
**After:** Þessi stundir í formi eru endurnýjandi einu sinni.

</details>

<details><summary>Anchor: p13official21:test:eea:707</summary>

**Source:** True zeros should be registered as numerical zeros.
**Reference:** Raunveruleg núllgildi skulu skráð með tölulegum núllum.
**Before:** Sagðar nálægir skal skráð sem tölfræðilegar nálægir.
**After:** Sannir númeraðar nul skal skráð sem nul.

</details>

<details><summary>Anchor: p13official21:test:eea:1965</summary>

**Source:** After paragraph 97B, paragraph 97C is added.
**Reference:** Lið 97C er bætt við á eftir lið 97B.
**Before:** Eftir 97B-lið bætist við 97C-lið.
**After:** Eftir 97B-lið bætist við lið 97C.

</details>

<details><summary>Anchor: p13official21:test:eea:2015</summary>

**Source:** After paragraph 103E, paragraph 103F is added.
**Reference:** Lið 103F er bætt við á eftir lið 103E.
**Before:** Eftir 103E skrá er færður 103F.
**After:** Í stað 103E-umli bætist við lið 103F.

</details>

<details><summary>Anchor: p13official21:test:eea:679</summary>

**Source:** This relates to the gross earnings paid during the reference year.
**Reference:** Þetta lýtur að vergum tekjum sem eru greiddar á viðmiðunarárinu.
**Before:** Þetta varðar heildarverði sem er greitt í viðmiðunaryrki.
**After:** Þetta varðar fráhaldsnæmi sem greidd er á viðmiðunarárinu.

</details>

<details><summary>Anchor: p13official21:test:eea:21</summary>

**Source:** Soils used must, wherever possible, be freshly sampled.
**Reference:** Jarðvegssýni verða ætíð að vera nýtekin sé þess nokkur kostur.
**Before:** Sólar sem notaðir verða, hvenær sem mögulegt er, að taka nýtt sýni úr.
**After:** Þar sem notuð eru jarðverur verður, hvenær sem mögulegt er, að taka nýja sýni frá þeim.

</details>

<details><summary>Anchor: p13official21:test:eea:1301</summary>

**Source:** The CDVtox of the recommended dosage shall not exceed 4,500 l/wash.
**Reference:** CDVtox fyrir ráðlagðan skammt skal ekki fara yfir 4.500 lítra á þvott.
**Before:** CDVtox af ráðlögðum skömmtum skal ekki vera meiri en 4.500 l/ágjöf.
**After:** CDVtox af ráðlögðum skömmtum skal ekki fara yfir 4.500 l/óskur.

</details>

<details><summary>Anchor: p13official21:test:eea:1599</summary>

**Source:** Tackling harmful conduct online, in particular grooming and cyber-bullying.
**Reference:** Að bregðast við skaðlegu innihaldi á Netinu, einkum nettælingu og rafrænu einelti.
**Before:** Hræða áhrifandi hætti í netinu, einkum ásamt húðgerð og netbólga.
**After:** Að leita á skaðlegri hætti í neti, einkum í því skyni að fá og koma upp á netinu.

</details>

<details><summary>Anchor: p13official21:test:ema:1306</summary>

**Source:** You can take the tablet with or without food.
**Reference:** Taka má töfluna með eða án fæðu.
**Before:** Takið töfluna með eða án matar.
**After:** Þú getur tekið töfluna með eða án matar.

</details>

<details><summary>Anchor: p13official21:test:ema:2270</summary>

**Source:** The dose should not exceed one daily drop in the affected eye(s).
**Reference:** Skammturinn á ekki að vera meiri en einn dropi í sjúkt auga (augu) á sólarhring.
**Before:** Skammturinn skal ekki vera stærri en eitt skammt í dag í sýnuáhættu/áhættu- auga/eingjöld.
**After:** Skammturinn skal ekki fara yfir einn skammt í dag í sýktu augunum.

</details>

<details><summary>Anchor: p13official21:test:ema:453</summary>

**Source:** Mark the point with a surgical marker.
**Reference:** Merkja skal svæðið með tússpenna fyrir skurðaðgerðir.
**Before:** Markaðu stiginn með skurðlæknismerki.
**After:** Markaðu stiginn með skurðlækningsmerki.

</details>

<details><summary>Anchor: p13official21:test:ema:2637</summary>

**Source:** Greater than 70 % of patients enrolled exhibited 3+ overexpression.
**Reference:** Meira en 70 % sjúklinga sem voru prófaðir sýndu 3+ yfirtjáningu.
**Before:** Meira en 70% sjúklinga sem tóku þátt í rannsókninni sýndu 3+ yfirmyndun.
**After:** Meira en 70% sjúklinga sem tóku þátt í rannsókninni sýndu 3+ yfirmyndun.

</details>

<details><summary>Anchor: p13official21:test:ema:2291</summary>

**Source:** Elonva is indicated for use in infertility (see section 4.1).
**Reference:** Elonva er ætlað til notkunar við ófrjósemi (sjá kafla 4.1).
**Before:** Elonva er ætlað til notkunar á ófrjósemi (sjá kafla 4.1).
**After:** Elonva er ætlað til notkunar á þáttum ófrjósemi (sjá kafla 4.1).

</details>

<details><summary>Anchor: p13official21:test:ema:2722</summary>

**Source:** See also ‘Bleeding or bruising after you stop treatment in section 4.
**Reference:** Sjá einnig „Blæðingar eða mar eftir að meðferð er hætt“ í kafla 4.
**Before:** Sjá einnig „Blæðingar eða sláður eftir að meðferð er hætt í kafla 4.
**After:** Sjá einnig „Blæðingar eða slökkvur eftir að meðferð er hætt í kaflanum 4.

</details>

<details><summary>Anchor: p13official21:test:ema:2175</summary>

**Source:** Breast-feeding must be stopped on initiation of treatment with Voriconazole Accord.
**Reference:** Hætta verður brjóstagjöf þegar meðferð með Voriconazole Accord hefst.
**Before:** Hætta verður brjóstagjöf við upphaf meðferðar með Voriconazole Accord.
**After:** Hætta verður brjóstagjöf þegar meðferð með Voriconazole Accord hefst.

</details>

<details><summary>Anchor: p13official21:test:ema:1656</summary>

**Source:** Each containing 250 mg of cream.
**Reference:** Í hverjum poka eru 250 mg af kremi.
**Before:** Hver inniheldur 250 mg af smjör.
**After:** Hver inniheldur 250 mg af smjör.

</details>

<details><summary>Anchor: p13official21:test:ema:635</summary>

**Source:** Table 4 provides dose modification guidance for dinutuximab, GM-CSF and IL-2.
**Reference:** Tafla 4 veitir leiðbeiningar um skammtaaðlögun dínútúxímabs, GM-CSF og IL-2.
**Before:** Í töflu 4 er fyrir hendi leiðbeiningar um skammtaaðlögun fyrir dinútúxímab, GM-CSF og IL-2.
**After:** Í töflu 4 er kveðið á um leiðbeiningar um skammtaaðlögun fyrir dinutuximab, GM-CSF og IL-2.

</details>

<details><summary>Anchor: p13official21:test:ema:2124</summary>

**Source:** If in doubt, talk to your doctor or pharmacist.
**Reference:** Ef þú ert í vafa, skaltu leita ráða hjá lækninum eða lyfjafræðingi.
**Before:** Ef þú ert í vanda skaltu tala við lækninn eða lyfjafræðing.
**After:** Ef þú ert í visslum skaltu ræða við lækninn eða lyfjafræðing.

</details>

<details><summary>Anchor: p13official21:test:ema:2632</summary>

**Source:** Data on Black racial groups was limited.
**Reference:** Takmarkaðar upplýsingar liggja fyrir um fólk af svörtum kynstofnum.
**Before:** Upplýsingar um Svarta kynþátta voru takmörkuð.
**After:** Upplýsingar um sáttmálum varðandi sjúklinga af hvítum kynþáttdreifum voru takmarkaðar.

</details>

<details><summary>Anchor: p13official21:test:ema:2064</summary>

**Source:** IVIg recipients should be monitored for clinical signs and symptoms of haemolysis.
**Reference:** Fylgjast þarf með sjúklingum sem fá immúnóglóbúlín í æð og gæta að því hvort einkenni blóðlýsu koma fram.
**Before:** Fylgjast skal með klínískum einkennum og einkennum um blóðmyndun hjá þeim sem fá IVIg.
**After:** Fylgjast skal með þeim sem fá IVIg með tilliti til klínískra einkenna um blóðmyndun.

</details>

<details><summary>Anchor: p13official21:test:ema:464</summary>

**Source:** Monitor for ADRs related to afatinib.
**Reference:** Fylgjast á með aukaverkunum sem tengjast afatinibi.
**Before:** Fylgjast skal með ofangreindum aukaverkunum af völdum afatinibs.
**After:** Fylgjast skal með ofnæmisviðbrögðum sem tengjast afatinibi.

</details>

<details><summary>Anchor: p13official21:test:ema:1638</summary>

**Source:** Statistical analyses are therefore presented only for influenza-infected subjects.
**Reference:** Tölfræðigreining er því einungis fyrir inflúensusýkta einstaklinga.
**Before:** Í þessum rannsóknum er því aðeins sýnt út greining á tölum fyrir sjúklinga með inflúensu.
**After:** Í þessum rannsóknum er því aðeins sýnt út greiningar á tölum fyrir sjúklinga sem voru sýktir af inflúensu.

</details>

<details><summary>Anchor: p13official21:test:ema:794</summary>

**Source:** Thymanax 25 mg film-coated tablets are available in calendar blisters.
**Reference:** Thymanax 25 mg filmuhúðaðar töflur fást í dagatalsþynnum.
**Before:** Thymanax 25 mg filmuhúðaðar töflur eru fáanlegar í árskirtuþynnum.
**After:** Thymanax 25 mg filmuhúðaðar töflur eru fáanlegar í árskirtuþynnum.

</details>

<details><summary>Anchor: p13official21:test:ema:228</summary>

**Source:** Excessive growth of hair may be a result of underlying diseases.
**Reference:** Óeðlilega mikil hæring getur verið vegna sjúkdóma sem liggja að baki.
**Before:** Of stór þrota getur verið afleiðing við undirliggjandi sjúkdómum.
**After:** Óháður hárvekkjastarf getur verið afleiðing eitil sjúkdóma.

</details>

<details><summary>Anchor: p13official21:test:ema:2203</summary>

**Source:** Severe renal impairment is a contraindication to use.
**Reference:** Ekki má nota lyfið handa sjúklingum með alvarlega skerta nýrnastarfsemi.
**Before:** Alvarleg skerta nýrnastarfsemi er mótefni við notkun lyfsins.
**After:** Alvarleg skerðing á nýrnastarfsemi er mótefni við notkun.

</details>

<details><summary>Anchor: p13official21:test:ema:2323</summary>

**Source:** It is important to drink plenty of water to avoid dehydration.
**Reference:** Mikilvægt er að drekka mikið af vatni til að koma í veg fyrir ofþornun.
**Before:** Mikilvægt er að drekka mikið af vatni til að forðast þvagmyndun.
**After:** Mikilvægt er að drekka mikið af vatni til að forðast útþurrð.

</details>

<details><summary>Anchor: p13official21:test:ema:1918</summary>

**Source:** The presented safety information is derived principally from paediatric patients.
**Reference:** Fyrirliggjandi öryggisupplýsingar eru einkum til komnar út frá börnum.
**Before:** Tilkynntar upplýsingar um öryggi eru aðallega úr upplýsingum um sjúklinga á börnastigi.
**After:** Umskiptin upplýsingar um öryggi eru aðallega frá sjúklingum á börnaldi.

</details>

<details><summary>Anchor: p13official21:test:ema:1788</summary>

**Source:** Magnetic resonance imaging is necessary to confirm the diagnosis of PRES.
**Reference:** Segulómun er nauðsynleg til að staðfesta greiningu PRES.
**Before:** Magnafjölgunartæki er nauðsynlegt til að staðfesta sjúkdómssýnina á grundvelli PRES.
**After:** Magnafjölgunartæki er nauðsynlegt til að staðfesta sjúkdómsgreiningu á PRES.

</details>

<details><summary>Anchor: p13official21:test:ema:2490</summary>

**Source:** If you are left-handed, do what comes naturally to you.
**Reference:** Þeir sem eru örvhentir eiga að gera það sem þeim finnst eðlilegast.
**Before:** Ef þú ert höndlegra skaltu gera það sem kemur fyrir þér eðlilega.
**After:** Ef þú ert höfðaður skaltu gera það sem er eðlilegt við þig.

</details>

<details><summary>Anchor: p13official21:test:eso:487</summary>

**Source:** The observations were made while the ALMA array was still being constructed.
**Reference:** Mælingarnar fóru fram þegar ALMA var enn í smíðum.
**Before:** Mælingarnar voru gerðar meðan ALMA tækið var enn búið til.
**After:** Mælingarnar voru gerðar á meðan ALMA tækið var enn búið til.

</details>

<details><summary>Anchor: p13official21:test:eso:1019</summary>

**Source:** MATISSE will observe brighter objects than METIS, but with higher spatial resolution.
**Reference:** MATISSE kemur til með að rannsaka bjartari fyrirbæri en METIS en í meiri upplausn aftur á móti.
**Before:** MATISSE mun fylgjast með björtum einkennum en METIS, en með hærra tímabilsupplýsinga.
**After:** MATISSE mun fylgjast með björtum fyrirbærum en METIS, en með hærri tímamarkskerfi.

</details>

<details><summary>Anchor: p13official21:test:eso:383</summary>

**Source:** The Hubble observations detect the dust and ALMA the molecular emission.
**Reference:** Mælingar Hubbles sýndu rykið en mælingar ALMA sameindaútgeislunina.
**Before:** Hubble myndir eru fyrir til að greina ryk og ALMA myndir eru fyrir til að greina lífræn losun.
**After:** Hubble myndir grein fyrir ryki og ALMA sýnir fram á sameindaspeglingu.

</details>

<details><summary>Anchor: p13official21:test:eso:476</summary>

**Source:** The results are published in the journal Science on 7 June 2013.
**Reference:** Niðurstöðurnar eru birtar í tímaritinu Science sem kom út 7. júní 2013.
**Before:** Niðurstöðurnar eru birtar í tímabili Science 7. júní 2013.
**After:** Niðurstöðurnar eru birtar í tímaritinu Science 7. júní 2013.

</details>

<details><summary>Anchor: p13official21:test:eso:839</summary>

**Source:** The Caisey Harlingten and ASH2 telescopes.
**Reference:** Caise Harlingten og ASH2 sjónaukarnir.
**Before:** Caisey Harlingten og ASH2 sjónaukarnir.
**After:** Caisey Harlingten og ASH2 sjónaukarnir.

</details>

<details><summary>Anchor: p13official21:test:eso:1198</summary>

**Source:** The new observations are thus the first direct confirmation of such models.
**Reference:** Niðurstöður mælinganna eru þar af leiðandi fyrsta beina staðfestingin á útreikningunum.
**Before:** Nýjar mælingar eru því fyrsta beinu staðfesting á slíkum líkennum.
**After:** Nýjar mælingarnar eru þess vegna fyrstu beinu staðfesting á slíkum líkani.

</details>

<details><summary>Anchor: p13official21:test:eso:20</summary>

**Source:** These galaxies span a vast range of distances from us.
**Reference:** Allar eru þessar vetrarbrautir í mismikilli fjarlægð frá okkur.
**Before:** Þessi vetrarbraut eru í miklu fjarlægri mörkum frá okkur.
**After:** Þessi vetrarbraut eru langt og mikið fjarlægð frá okkur.

</details>

<details><summary>Anchor: p13official21:test:eso:1</summary>

**Source:** “The spectrum of a planet is like a fingerprint.
**Reference:** „Litróf reikistjörnu er eins og fingrafar.
**Before:** „Svæði reikistjarna er eins og vörn.
**After:** „Svæði reikistjarna er eins og fingraf.

</details>

<details><summary>Anchor: p13official21:test:eso:278</summary>

**Source:** Centaurus A has therefore been observed with many different telescopes.
**Reference:** Vetrarbrautin hefur þess vegna verið viðfangsefni fjölmargra ólíkra sjónauka.
**Before:** Því hefur Centaurus A verið mælt með með margum mismunandi sjónaukum.
**After:** Því hefur Centaurus A verið mælt með með margum mismunandi sjónaukum.

</details>

<details><summary>Anchor: p13official21:test:eso:514</summary>

**Source:** This star formation region is forming many stars.
**Reference:** Þetta stjörnumyndunarsvæði er að mynda margar stjörnur.
**Before:** Þessi stjörnumyndunarsvæði myndast mörg stjörnur.
**After:** Þessi stjörnumyndunarsvæði myndast mörgum stjörnum.

</details>

<details><summary>Anchor: p13official21:test:eso:1088</summary>

**Source:** Weather statistics are available here.
**Reference:** Upplýsingar um veður má finna hér.
**Before:** Vetrarannsóknir eru hér fyrir.
**After:** Útgáfufræðilegar gögn eru hér.

</details>

<details><summary>Anchor: p13official21:test:eso:825</summary>

**Source:** The process of dust trapping is explained in an earlier release (eso1325).
**Reference:** Þetta ferli, þegar ryk festist, er útskýrt í eldri fréttatilkynningu (eso1325).
**Before:** Framkvæmdarferlið um uppsöfnun duftar er skýrt í fyrri útleiðingu (eso1325).
**After:** Framkvæmdarferlið um að trapa á ryk er skýrt í fyrri útgáfu (eso1325).

</details>

<details><summary>Anchor: p13official21:test:eso:705</summary>

**Source:** Normal long-duration GRBs last between 2 and 2000 seconds.
**Reference:** Venjulegir langir gammablossar standa yfir í 2 til 2000 sekúndur.
**Before:** Lengd eðlilegra rauðum geislameinsbrotna er á bilinu 2 til 2000 sekúndur.
**After:** Alvarlegar langtíma GRB eru á bilinu 2 til 2000 sekúndur.

</details>

<details><summary>Anchor: p13official21:test:eso:1086</summary>

**Source:** Media representatives and other outreach groups will also be attending the event.
**Reference:** Fjölmiðlar og fræðsluhópar munu einnig sækja atburðinn.
**Before:** Tilskipendum fjölmi og öðrum hópum sem hafa áhersla til að taka til bæjar í sér verða einnig aðstoðar.
**After:** Tilskipendum fjölmiðla og öðrum hópum sem hafa útöku verða einnig aðstoðarstofnunin.

</details>

<details><summary>Anchor: p13official21:test:eso:434</summary>

**Source:** The guest of honour was the President of Chile, Sebastián Piñera.
**Reference:** Sebastián Piñera, forseti Chile, var heiðursgestur.
**Before:** Gesturinn var Sebastián Piñera, forseti Chile.
**After:** Gesturinn var Sebastián Piñera, forseti Chile.

</details>

<details><summary>Anchor: p13official21:test:eso:504</summary>

**Source:** The precise extent of the habitable zone depends on many factors.
**Reference:** Umfang lífbeltisins veltur á ýmsum þáttum.
**Before:** Nákvæmur útborður sætisins tekur til mikillra þátta.
**After:** Nákvæmlega umfang sætisins sem er viðhóflegur tekur til mikillra þátta.

</details>

<details><summary>Anchor: p13official21:test:eso:136</summary>

**Source:** ALMA is radically different from visible-light and infrared telescopes.
**Reference:** ALMA er gerólík sjónaukum sem sjá sýnilegt og innrautt ljós.
**Before:** ALMA er alvarlega mismunandi frá sjónaukum sem sýna í ljósi og innrauðu ljósi.
**After:** ALMA er ólík sýnilegum sjónaukum og infraröntungasjónaukum.

</details>

<details><summary>Anchor: p13official21:test:eso:1073</summary>

**Source:** Analysis of this spectrum indicated that its atmosphere is cloudy.
**Reference:** Greining á litrófinu sýnir að lofthjúpurinn er skýjaður.
**Before:** Greining á þessari röð sýndi að lofthjúpurinn sé skúttur.
**After:** Greining á þessari röð sýndi að lofthjúpurinn sé skýjaður.

</details>

<details><summary>Anchor: p13official21:test:eso:349</summary>

**Source:** The results described here use some of these Science Verification data.
**Reference:** Gögnin sem notuð voru fyrir þessa rannsókn var að hluta til aflað við þessar prófanir.
**Before:** Niðurstöðurnar sem koma fram hér eru notaðar sumar af þessum gögn um sannprófun á vísindum.
**After:** Niðurstöðurnar sem hér er lýst nota einhverjar af þessum gögn um vísindalegt sannprófun.

</details>

<details><summary>Anchor: p13official21:test:eso:400</summary>

**Source:** ESPRESSO will feature radial velocity precision of 0.35 km/hour or less.
**Reference:** ESPRESSO mun ná að greina sjónstefnuhraða niður í 0,35 km/klst eða minna.
**Before:** ESPRESSO mun koma fram með nákvæmni á hraða sem er 0,35 km/klst. eða minna.
**After:** ESPRESSO mun koma fram með nákvæmni á hraða 0,35 km/klst. eða minna.

</details>

<details><summary>Anchor: p13official21:test:eso:1108</summary>

**Source:** As a result the starlight looks redder when it arrives on Earth.
**Reference:** Þess vegna virðast stjörnur oft rauðleitari en þær eru í raun og veru.
**Before:** Af þessu leiðir stjörnuljósinn að vera rauðari þegar hann kemur á Jörðina.
**After:** Af þessu leið reynist stjörnuljós rauðari þegar hann kemur á Jörðina.

</details>

<details><summary>Anchor: p13official21:test:eso:989</summary>

**Source:** Martín-Doménechs team chemically modelled gas-grain formation of methyl isocyanate.
**Reference:** Hópur Martín-Doménech gerði líkön á gas-kornamyndun metýl-ísósýanats.
**Before:** Martín-Doménechs hópur myndlegaði stofnun gasgrána af metýlisókanat.
**After:** Hópur Martín-Doménechs myndlegaði stofnun gasgrána af mýetis ísókanat.

</details>

<details><summary>Anchor: p13official21:test:eea:79</summary>

**Source:** Justified estimates must be made of the expected concentrations of the active substance and relevant metabolites, degradation and reaction products, in soil, groundwater, surface water and air, following use as proposed or already occurring.
**Reference:** Rökstutt mat verður að koma fram á áætluðum styrk virka efnisins, og viðkomandi umbrots-, niðurbrots- og hvarfaefna, í jarðvegi, grunnvatni, yfirborðsvatni og lofti, eftir núverandi notkun eða ráðgerða notkun.
**Before:** Gera verður réttar mat á búist við því hvað varðar búist við þeim styrk virka efnisins og viðkomandi umbrotsefna, umbrotsefni og framleiðsluefni í jarðvökum, grunnvatn, yfirborðsvökum og lofthjálpum, eftir notkun eins og mælt er fyrir um eða þegar það hefur orðið til.
**After:** Gera verður réttar mat á búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hvað varðar búist við því hva

</details>

<details><summary>Anchor: p13official21:test:eea:930</summary>

**Source:** Wells in microtitre plates are coated overnight with recommended dilutions of purified immunoglobulin fractions of antibodies of reference quality.
**Reference:** Bollar í míkrótítrunarplötum eru þaktir næturlangt með ráðlögðum þynningum af hreinsuðum ónæmisglóbúlín- þáttum mótefna sem standast kröfur um viðmiðunargæði.
**Before:** Vell í mífítrýpum eru klæddar á nótt með ráðlögðu þynningu af hreinsuðu immunglóbúlíniðafrakkomu mótefna sem eru á viðmiðunarmiðstöð.
**After:** Vellir í mælitöflum eru klúft í næurna með ráðlagðri þynningu af hreinsuðu immunglóbúlínafli mótefna sem eru á viðmiðunarmiðgildi.

</details>

<details><summary>Anchor: p13official21:test:eea:351</summary>

**Source:** The application of GLP principles to health and environmental safety data generated for regulatory purposes may be mandatory.
**Reference:** Beiting meginreglna um góðar starfsvenjur við rannsóknir á gögn um öryggi heilbrigðis og umhverfis, sem safnað er eftir föstum reglum, getur verið lögbundin.
**Before:** Tilgreining á GLP- meginreglum á heilsu og umhverfisöryggisupplýsingum sem gefin eru út fyrir reglulegar ábendingar getur verið skilyrði.
**After:** Gildi GLP- meginreglur um vinnslu til að fá heilbrigðis og umhverfisöryggisgögn, sem eru framkvæmdar til regluríkja, geta verið skylt.

</details>

<details><summary>Anchor: p13official21:test:eea:1144</summary>

**Source:** Successful participation in interlaboratory studies that assess laboratory proficiency is the best way to prove the competence in specific analyses.
**Reference:** Árangursrík þátttaka í rannsóknum með öðrum rannsóknarstofum, þar sem frammistaða rannsóknarstofa er metin, er vænlegust til þess að staðfesta hæfni í sértækum efnagreiningum.
**Before:** Reynsla í samstarfsrannsóknum á rannsóknarþjálfun sem meta þjálfa rannsóknarstofa er besta leiðin til að sýna fram á færni í sérstökum greiningum.
**After:** Reynsla í samstarf við rannsóknir á milli rannsóknarstofa sem meta færni rannsóknarstofa er besta leiðin til að sýna fram á færni í sérstökum greiningum.

</details>

<details><summary>Anchor: p13official21:test:eea:1409</summary>

**Source:** The port security assessment is the basis for the port security plan and its implementation.
**Reference:** Áhættumat fyrir höfn er undirstaða verndaráætlunar hafnar og framkvæmdar hennar.
**Before:** Portvænslasannsóknin er grunnur fyrir portvænslatákn og framkvæmd þess.
**After:** Portvænslatilgjöf er grundvöllur fyrir portvænslatáknin og framkvæmd þess.

</details>

<details><summary>Anchor: p13official21:test:eea:1831</summary>

**Source:** However fibreboards classified as class A will be accepted if they do not represent more than 50 % of the total wood and wood-based materials used in the product.
**Reference:** Trefjaplötur sem flokkaðar eru sem E1 munu þó samþykktar ef þær eru ekki meira en 50% af samanlögðu innihaldi viðar og efna úr viði sem notuð eru í vöruna.
**Before:** Hins vegar munu þeir sem eru flokkaðir sem A flokkur vera viðkomandi ef þeir eru ekki meira en 50% af heildarstærði vetrarbrauta og vetrarbrautafundna í vörunni.
**After:** Hins vegar verður viðurkennd þeirra vefjaskírni sem eru flokkaðar í flokk A ef þær eru ekki meira en 50% af heildarvöxt og vöxtarafurðum sem notaðar eru í vörunni.

</details>

<details><summary>Anchor: p13official21:test:eea:995</summary>

**Source:** The objectives and characteristics of indices for variable 110 (production) also apply to the indices for the variables on building construction and civil engineering.
**Reference:** Markmið og einkenni vísitalna fyrir breytu 110 (framleiðslu) gilda einnig um vísitölur breytna fyrir byggingarstarfsemi og mannvirkjagerð.
**Before:** Markmið og eiginleikar fyrir vísitölur fyrir breytilegt 110 (framleiðslu) gilda einnig um vísitölur fyrir breytilega vinnu- og byggingarvísitölurnar.
**After:** Markmið og eiginleikar vísitölur fyrir breytilegan 110 (framleiðslu) gilda einnig um vísitölur fyrir breytilega 110 (byggingar) og 110 (búnaðar- og samfélagsverkefni).

</details>

<details><summary>Anchor: p13official21:test:eea:2090</summary>

**Source:** Member States shall require the competent authorities to monitor compliance with this Regulation effectively and take all necessary measures to ensure such compliance.
**Reference:** Aðildarríki skulu skylda lögbær yfirvöld til að hafa eftirlit með því að farið sé með virkum hætti eftir þessari reglugerð og gera allar nauðsynlegar ráðstafanir til að tryggja að farið sé að ákvæðum hennar.
**Before:** Aðildarríkin skulu kveða á um það í þátttakendur lögbæra yfirvalda til að fylgja með skilvirkum hætti reglugerðinni og gera allar nauðsynlegar ráðstafanir til að tryggja það.
**After:** Aðildarríkin skulu krefjast þess að lögbærum yfirvöldum sé gerð skilvirkan eftirlit með því að þau uppfylli þessa reglugerð og þeim gerist allar nauðsynlegar ráðstafanir til að tryggja það.

</details>

<details><summary>Anchor: p13official21:test:eea:1387</summary>

**Source:** In the case of international maritime transport services, the Member States concerned shall cooperate in the security assessment.
**Reference:** Ef um er að ræða alþjóðlega sjóflutningaþjónustu skulu hlutaðeigandi aðildarríki eiga samstarf um áhættumat.
**Before:** Ef um er að ræða alþjóðlega flutningaþjónustu á sjávarbærum skal viðkomandi aðildarríki samskipa í mati á öryggis.
**After:** Í þeim tilvikum sem varðar alþjóðlega flutningaþjónustu á sjávarbrautum skulu hlutaðeigandi aðildarríki samskipa í öryggismati.

</details>

<details><summary>Anchor: p13official21:test:eea:136</summary>

**Source:** Member State shall recognize the documents of compliance and safety management certificates issued by, or on behalf of, the administrations of third countries if it is satisfied that they demonstrate compliance with the provisions of this Regulation.
**Reference:** Aðildarríki skal viðurkenna þau samræmingarskjöl og öryggisstjórnunarskírteini sem stjórnvöld í þriðju löndum, eða annar fyrir þeirra hönd, hefur gefið út ef það er sannfært um að með þeim sé farið að ákvæðum þessarar reglugerðar.
**Before:** Aðildarríki skal viðurkenna skjöl um samræmi við og öryggisstýringu sem tilskipanir eru af stjórnunum þriðju landa eða fyrir henni ef það er fullgengi að þeir sýni fram á samræmi við ákvæði þessarar reglugerðar.
**After:** Aðildarríki skal viðurkenna skjöl um samræmismiðlun og öryggisstörfum sem útgefna stjórnarstofur þriðju landa eða fyrir hennar og gera sér vissu á því að þeir sýni fram á að þau uppfylli ákvæði þessarar reglugerðar.

</details>

<details><summary>Anchor: p13official21:test:eea:1354</summary>

**Source:** Testing at low dosages may be performed by use of OECD 308 (August 2000) or an equivalent method.
**Reference:** Ef prófanir eru gerðar með litlum skömmtum má nota OECD 308 (frá ágúst 2000) eða jafngilda aðferð.
**Before:** Gera má rannsóknir á lágum skömmtum með því að nota OECD 308 (á augustus 2000) eða sambærilegan aðferð.
**After:** Prófun á lágum skömmtum má framkvæma með notkun OECD-staðals 308 (á augustus 2000) eða sambærilegs aðferðar.

</details>

<details><summary>Anchor: p13official21:test:eea:63</summary>

**Source:** The placement of these devices in the soil should not result in preferential flow paths.
**Reference:** Staðsetning þessara tækja í jarðveginum má ekki breyta farvegi vatnsins.
**Before:** Setning þessara tækjanna í jarði ætti ekki að leysa til ábendingar flæðislega leiða.
**After:** Setning þessara búnaðar í jarði ætti ekki að leysa til ávistu flæðisleiða.

</details>

<details><summary>Anchor: p13official21:test:eea:1485</summary>

**Source:** Prices will be collected twice per year, at the beginning of each six-month period, (January and July) and will refer to the average prices paid by the industrial end-user for electricity over the previous six months.
**Reference:** Verðsöfnun á sér stað tvisvar á ári, í upphafi hvers sex mánaða tímabils (janúar og júlí) og er vísað til þess meðalverðs sem notendur í atvinnurekstri greiða fyrir rafmagn undanfarna sex mánuði.
**Before:** Verður safnað tvisvar á ári, fyrir hvert sex mánaða tímabili (í janúar og júlí) og tengist meðalverðum sem rekstraraðilarnir gefa upp fyrir rafmagn í síðustu sex mánuði.
**After:** Verður safnað tvisvar á ári, fyrir hvern sex mánaða tímabili (í janúar og júlí), og verður vísað til meðalverðs sem atvinnu, sem nota vél, greiður fyrir rafmagni á síðustu sex mánuði.

</details>

<details><summary>Anchor: p13official21:test:eea:1160</summary>

**Source:** Separation of dioxins from interfering chlorinated compounds such as PCBs and chlorinated diphenyl ethers should be carried out by suitable chromatographic techniques (preferably with a florisil, alumina and/or carbon column).
**Reference:** Aðgreining díoxína frá klóruðum efnasamböndum, sem hafa truflandi áhrif, svo sem PCB-efnum og klóruðum dífenýletrum, skal eiga sér stað með heppilegum skiljunaraðferðum (helst á flórísíls-, súráls- og/eða kolefnissúlu).
**Before:** Fjölgun díoxína frá klóríðuðum efnasamböndum svo sem PCB-efnum og klóralíðuðum dífenýleterum skal fara fram með viðeigandi lífrænri greiningartækni (til ætlunar með florisíliði, álómati og/eða kólum).
**After:** Að því er varðar að skipta úr díoxínum úr óvirkandi klóríntengdum efnasamböndum svo sem PCB-efnum og klóralíntengdum dífenýleterum skal nota viðeigandi lífræn greiningaraðferðir (til ætlunar með florisíl, álúmíníni og/eða kólínu rista).

</details>

<details><summary>Anchor: p13official21:test:eea:1323</summary>

**Source:** If refills are not provided, the weight of the total primary packaging shall not exceed 3,7 g per wash for tablets and 1,7 g per wash for all other products.
**Reference:** Ef áfyllingar eru ekki í boði skal þyngd grunnumbúðanna í heild ekki vera meiri en 3,7 grömm á þvott ef um er að ræða töflur og 1,7 grömm á þvott fyrir allar aðrar vörur.
**Before:** Ef ekki er veitt endurtekningar skal þyngd heildarfráseldsins ekki vera meira en 3,7 g fyrir hverja þvag fyrir töflur og 1,7 g fyrir hverja þvag fyrir öll önnur vörur.
**After:** Ef endurtekinn fylling er ekki veitt skal þyngd heildarfráselds ekki fara yfir 3,7 g í hverja þvagrind fyrir töflur og 1,7 g í hverju þvagrind fyrir öll önnur vörur.

</details>

<details><summary>Anchor: p13official21:test:eea:371</summary>

**Source:** Test facility inspections should be conducted on a regular, routine basis to establish and maintain records of the GLP compliance status of test facilities.
**Reference:** Prófunarstöðvar skulu skoðaðar reglubundið og að staðaldri til að kanna og halda skrár um stöðu samræmis prófunarstöðvanna við góðar starfsvenjur við rannsóknir.
**Before:** Rannsóknarstöðvar skulu rannsakaðar reglulega og með eftirliti til að koma á fót og viðhalda skrár um GLP- samræmi rannsóknarstöðva.
**After:** Rannsóknarstöðvar skulu rannsaka á reglulegu, eftirlitsferli til að koma á og viðhalda skrár um uppfyllingu kröfum um rannsóknarreglur (GLP).

</details>

<details><summary>Anchor: p13official21:test:eea:1612</summary>

**Source:** Actions will aim at encouraging and assisting Internet service providers to develop, as a tool of self regulation, ‘child safe labelling for web pages.
**Reference:** Aðgerðir skulu miða að því að hvetja og aðstoða þjónustuveitendur Netsins við að þróa merkinguna „öruggt fyrir börn“ fyrir vefsíður, sem úrræði til sjálfseftirlits.
**Before:** Aðgerðir verða beint til þess að örva og stuðla að búnaði fyrirtækja í netvísunum til að þróa, sem tæki fyrir sjálfri reglur, „öryggismerki fyrir barn á vefsvanum“.
**After:** Aðgerðir verða að markmiði að hvetja til og stuðla að því að búnaðarstofnanir í netvörunni þjóna sérstaða reglum með því að þróa „börnöryndu merkingu fyrir vefsvanir“.

</details>

<details><summary>Anchor: p13official21:test:eea:879</summary>

**Source:** If more than one water source is utilised for fish production, fish representing all water sources must be included for sampling.
**Reference:** Ef vatn úr fleiri en einni lind er notað við fiskframleiðslu skal velja fisk úr öllum vatnslindum til sýnatöku.
**Before:** Ef fleiri en einn vatnsorð er notað til fiskaræktar verður að taka til sýnatöku fisk sem eru allir vatnsorðin.
**After:** Ef fleiri en einn vatnsstofa er notaður til að framleiða fiski verður að taka sýni úr fiskum sem eru allar vatnsstofurnar.

</details>

<details><summary>Anchor: p13official21:test:eea:1059</summary>

**Source:** The domestic output price index for an economic activity measures the average price development of all goods and related services resulting from that activity and sold on the domestic market.
**Reference:** Vísitala innlends framleiðsluverðs vegna atvinnustarfsemi mælir meðalverðþróun á öllum vörum og tengdri þjónustu vegna þeirrar starfsemi sem eru seldar á innanlandsmarkaði.
**Before:** Haggerðarverðsins fyrir innlend starfsemi er mælt með meðalverðaþróun á öllum vörum og tengdum þjónustu sem fylgir starfsemi þess og selst á innlendri markaði.
**After:** Hagprófunarstigi innanlands fyrir efnahagsaðgerð mæltu við meðalverðaþróun á öllum vörum og tilheyrandi þjónustu sem af völdum þessarar starfsemi koma og seljast á innlendri markaði.

</details>

<details><summary>Anchor: p13official21:test:eea:665</summary>

**Source:** Citizenship is defined as the legal nationality of each person, and a citizen is a person who is a legal national by birth or naturalisation, whether by declaration, option, marriage or other means.
**Reference:** Ríkisborgararéttur er skilgreindur sem ríkisfang hvers manns sem hann öðlast við fæðingu eða við veitingu þegnréttar hvort sem það gerist í kjölfar umsóknar, með ættleiðingu, hjónabandi eða með öðrum hætti.
**Before:** Borgarhöfði er skilgreind sem lögfræðileg borgarhöfði hvers einstaklings og borgari er einstaklingur sem er lögfræðilegur borgur vegna fæðu eða innleiðslu, hvort með yfirskrifti, vali, mannaframleiðslu eða annars konar.
**After:** Borgarleiki er skilgreind sem lögfræðilegur ríki hvers einstaklings og borgari er einstaklingur sem er lögfræðilegt ríkisborgari með upphaf eða innleiðslu, hvort sem um leiðir að því að kveðja á um, að vali, atkvæði eða annars konar hætti.

</details>

<details><summary>Anchor: p13official21:test:eea:1509</summary>

**Source:** Therefore, in the interest of clarity of legislation, it is appropriate to merge those provisions in one single legislative act.
**Reference:** Til að tryggja gagnsæi í löggjöf er því rétt að sameina þessi ákvæði í einni lagagerð.
**Before:** Því er rétt að samþykkja þessar ákvæði í einu samkvæmt lögum til að gera skýrleikar á lögum greinilegari.
**After:** Því er rétt að samþykkja þessi ákvæði í einu gildisskrá.

</details>

<details><summary>Anchor: p13official21:test:ema:1152</summary>

**Source:** Change from baseline in body weight was similar for patients treated with sitagliptin relative to placebo.
**Reference:** Breytingar á þyngd frá grunnlínu voru svipaðar fyrir sjúklinga sem meðhöndlaðir voru með sitagliptíni miðað við þá sem fengu lyfleysu.
**Before:** Breyting frá grunngildi á líkamsþyngd var svipuð hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.
**After:** Breyting frá upphafsgildi líkamsþyngdar var svipuð hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.

</details>

<details><summary>Anchor: p13official21:test:ema:2113</summary>

**Source:** As the effective dose is 7 mSv when the recommended activity of 370 MBq of florbetapir (18F) is administered, these adverse reactions are expected to occur with low probability.
**Reference:** Þar sem virkur skammtur er 7 mSv þegar ráðlagður 370 MBq skammtur af florbetapir (18F) er gefinn eru litlar líkur á slíkum aukaverkunum.
**Before:** Þar sem virkt skammturinn er 7 mSv þegar ráðlagður virkni 370 MBq af florbetapíri (18F) er gefið, er búist við að slæmum líkur á að þessi aukaverkanir komi fram.
**After:** Þar sem skammturinn sem hefur áhrif er 7 mSv þegar ráðlagður virkni 370 MBq af florbetapiri (18F) er gefið, er búist við að slíkar aukaverkanir komi fram með lítil líkur.

</details>

<details><summary>Anchor: p13official21:test:ema:1610</summary>

**Source:** The true extent of CNS penetration of lamivudine and its relationship with any clinical efficacy is unknown.
**Reference:** Í hve miklum mæli lamivúdín kemst raunverulega inn í miðtaugakerfið og samband þessa við klíníska verkun er ekki þekkt.
**Before:** Vitað er ekki um hversu mikil innrennsli lamivúdíns í heilaæði og sambandi við klíníska verkun.
**After:** Líklegur magn innrennslis lamivúdíns í heilaheilabúla og tengslin við klíníska verkun eru ekki þekkt.

</details>

<details><summary>Anchor: p13official21:test:ema:2580</summary>

**Source:** In case a vaginal ring or transdermal patch has been used, the woman should start using IOA preferably on the day of removal, but at the latest when the next application would have been due.
**Reference:** Ef notaður hefur verið skeiðarhringur eða forðaplástur á konan að hefja notkun IOA sama dag og getnaðarvörnin er fjarlægð en í síðasta lagi þegar komið er að næstu ísetningu.
**Before:** Ef hettuglösum eða útsettrið skjaldskrækur hafa verið notaðir skal konan hefja notkun IOA fyrst og fremst á deginu sem henni er fjarlægð, en síðar en næstum notkunurinn væri réttur.
**After:** Ef hettuglösum eða útskúlum hafa verið notaðir á gæðamál skal konan hefja notkun á innrennslisþéttni, einkum á þeim degi sem þær eru fjarlægðar, en síðarlegt á næsta dag sem þarf að nota þær.

</details>

<details><summary>Anchor: p13official21:test:ema:1495</summary>

**Source:** Check again to make sure the correct dose of Tevagrastim is in the syringe.
**Reference:** Athugaðu aftur hvort rétt magn Tevagrastim er í sprautunni.
**Before:** Athugaðu aftur til að tryggja að réttur skammtur af Tevagrastim sé í sprautunni.
**After:** Athugaðu aftur til að tryggja að réttur skammtur af Tevagrastim sé í sprautunni.

</details>

<details><summary>Anchor: p13official21:test:ema:1332</summary>

**Source:** The incidence of treatment discontinuation due to adverse events was 7.4% for Lyxumia compared to 3.2% in the placebo group during the main 24-week treatment period.
**Reference:** Tíðni þess að meðferð var hætt vegna aukaverkana var 7,4% hjá þeim sem fengu Lyxumia samanborið við 3,2% hjá lyfleysuhópnum meðan á 24 vikna aðalmeðferðartímanum stóð.
**Before:** Tíðni þess að meðferð var hætt vegna aukaverkana var 7,4% hjá Lyxumia samanborið við 3,2% í lyfleysu hópnum á megin 24 vikna meðferðartímabilinu.
**After:** Tíðni þess að meðferð var hætt vegna aukaverkana var 7,4% hjá Lyxumia samanborið við 3,2% í lyfleysuþáttinni á megin 24 vikna meðferðartímabilinu.

</details>

<details><summary>Anchor: p13official21:test:ema:1414</summary>

**Source:** Invokana has no or negligible influence on the ability to drive, cycle, and use tools or machines.
**Reference:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, hjólreiða og notkunar tækja eða véla.
**Before:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, kílóhlaða og notkunar tækja eða véla.
**After:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, kringlunar og notkunar tækja eða véla.

</details>

<details><summary>Anchor: p13official21:test:ema:74</summary>

**Source:** ARICLAIM should normally not be used for children and adolescents under 18 years.
**Reference:** Venjulega ætti ekki að nota ARICLAIM handa börnum og unglingum undir 18 ára aldri.
**Before:** ARICLAIM á ekki venjulega að nota handa börnum og unglingum yngri en 18 ára.
**After:** ARICLAIM á ekki venjulega notað handa börnum og unglingum yngri en 18 ára.

</details>

<details><summary>Anchor: p13official21:test:ema:2652</summary>

**Source:** Put the needle fully into the skin as shown by your nurse or doctor (see picture 6).
**Reference:** Stingdu nálinni í húðina eins og læknirinn eða hjúkrunarfræðingur sýna þér (sjá mynd 6).
**Before:** Settu nálinni fullt inn í húðina eins og það er sýnt af hjá hjúkrunarfræðingnum eða lækninum (sjá mynd 6).
**After:** Settu nálinni fullt inn í húðina eins og hjá hjúkrunarfræðingnum eða lækninum sýnt er á mynd 6 (sjá mynd 6).

</details>

<details><summary>Anchor: p13official21:test:ema:2744</summary>

**Source:** Clinical experience in pregnant women is limited, but congenital anomalies and abortions have been reported.
**Reference:** Klínísk reynsla af notkun hjá barnshafandi konum er takmörkuð, en tilvik um meðfædd frávik og fósturlát hafa komið fram.
**Before:** Klínísk reynsla hjá þunguðum konum er takmörkuð en tilkynnt hefur verið um fæðingar- og fósturvísbrot.
**After:** Klínísk reynsla hjá þunguðum konum er takmörkuð en tilkynnt hefur verið um fæðingarvandamál og fóstri.

</details>

<details><summary>Anchor: p13official21:test:ema:992</summary>

**Source:** Animal studies have shown excretion of retagabine and/or its metabolites in breast milk.
**Reference:** Dýrarannsóknir hafa sýnt útskilnað retigabíns og/eða umbrotsefna þess í mjólk.
**Before:** Dýrarannsóknir hafa sýnt fram á útskilnaður retagabíns og/eða umbrotsefna þess í brjóstamjólk.
**After:** Dýrarannsóknir hafa sýnt að útskilnaður er af retagabíni og/eða umbrotsefnum þess í brjóstamjólk.

</details>

<details><summary>Anchor: p13official21:test:ema:2650</summary>

**Source:** Patients should be advised that in the event of any sudden visual defect, they should stop taking Sildenafil Actavis and consult a physician immediately (see section 4.3).
**Reference:** Ráðleggja á sjúklingum að hætta töku Sildenafil Actavis og hafa strax samband við lækni ef þeir finna fyrir skyndilegri sjónskerðingu (sjá kafla 4.3).
**Before:** Sjúklingum skal ráðlagt að hætta tafarlaust meðferð með Sildenafil Actavis ef þeir fá sér ólíka sjónskerðingu og leita læknis tafarlaust (sjá kafla 4.3).
**After:** Sjúklingum skal ráðlagt að hætta að taka Sildenafil Actavis ef þeir fá sýnarslysi og leita læknis strax (sjá kafla 4.3).

</details>

<details><summary>Anchor: p13official21:test:ema:441</summary>

**Source:** Limited clinical data suggest a comparable effect on time to recovery of severe neutropenia for pegfilgrastim to filgrastim in patients with de novo acute myeloid leukaemia (see section 5.1).
**Reference:** Takmarkaðar klínískar upplýsingar benda til sambærilegra áhrifa pegfilgrastims og filgrastims á þann tíma sem líður þar til daufkyrningafæð gengur til baka, hjá sjúklingum með nýgreint (de novo) brátt kyrningahvítblæð i (sjá kafla 5.1).
**Before:** Takmörkuð klínísk gögn benda til sambærilegs áhrifa á tíma til endurnauðsyns fyrir alvarlega blóðnýmisskort hjá sjúklingum með de nýtt bráða frumukrabbameini (sjá kafla 5.1).
**After:** Takmarkaðar klínískar upplýsingar benda til svipaðrar áhrifa á tíma til endurheimta alvarlegs daufkyrningafæð vegna pegfilgrastims og filgrastims hjá sjúklingum með nýbyggða brátt frumudrengsæi (sjá kafla 5.1).

</details>

<details><summary>Anchor: p13official21:test:ema:1433</summary>

**Source:** Aseptically add sodium pertechnetate (Tc 99m) solution (from step d above) to the tilmanocept powder vial.
**Reference:** Bætið með smitgátuðum hætti natríum pertechnetate (Tc 99m) lausn (úr skrefi d hér á undan) í hettuglasið með tilmanocept stofninum.
**Before:** Blanda skal natríum perteknetat (Tc 99m) lausn (frá d-stigi hér að ofan) við tilmanócept duft í hettuglasinu.
**After:** Að því að óbrotið er bætt natríum perteknetat (Tc 99m) lausn (frá d-stiginn hér að framan) í hettuglasinu með tilmanócept dufti.

</details>

<details><summary>Anchor: p13official21:test:ema:2077</summary>

**Source:** White capsules with “OGT 918” printed in black on the cap and “100” printed in black on the body.
**Reference:** Hvít hylki með „OGT 918“ prentað með svörtu á hettuna og „100“ prentað með svörtu á neðri hlutann.
**Before:** Hvítir hylki með „OGT 918“ á svörtu í kappenum og „100“ á svörtu í hylkjunni.
**After:** Hvít hylki með „OGT 918“ á svörtu í kappenum og „100“ á svörtu í hylkjunni.

</details>

<details><summary>Anchor: p13official21:test:ema:772</summary>

**Source:** These effects are called interactions, and can lead to serious side effects, or prevent proper control of other conditions you may have.
**Reference:** Þessi áhrif eru kölluð milliverkanir og geta valdið alvarlegum aukaverkunum, eða komið í veg fyrir viðeigandi meðferð annarra sjúkdóma hjá þér.
**Before:** Þessar áhrif eru nefndar milliverkanir og geta leitt til alvarlegra aukaverkana eða hindraði viðeigandi eftirliti með öðrum sjúkdómsstöðum sem þú getur haft.
**After:** Þessi áhrif eru nefndar milliverkanir og geta leitt til alvarlegra aukaverkana eða koma í veg fyrir að ná réttum stjórn á öðrum sjúkdómum sem þú getur haft.

</details>

<details><summary>Anchor: p13official21:test:ema:430</summary>

**Source:** Keep the needle in your skin after the dose counter has returned to 0 and count slowly to 6.
**Reference:** Haltu nálinni í húðinni eftir að skammtateljarinn sýnir aftur 0 og teldu hægt upp að 6.
**Before:** Haltu nálina í húðinni eftir að skammtatöflunni hefur orðið til 0 og tölutölvuðu hægt fyrir 6.
**After:** Haltu nálinni á húðinni eftir að skammtaríkið hefur náð 0 og tölur þér langt á 6.

</details>

<details><summary>Anchor: p13official21:test:ema:1458</summary>

**Source:** This is important to make the medicine easier and more comfortable to inject.
**Reference:** Þetta er mikilvægt til þess að auðveldara og þægilegra sé að sprauta lyfinu.
**Before:** Þetta er mikilvægt að gera lyfið auðveldari og gamall til inndælingar.
**After:** Þetta er mikilvægt að gera lyfið auðveldari og gamall til að sprauta því.

</details>

<details><summary>Anchor: p13official21:test:ema:382</summary>

**Source:** In the controlled clinical studies in chronic ITP with eltrombopag, increases in serum alanine aminotransferase (ALT), aspartate aminotransferase (AST) and bilirubin were observed (see section 4.8).
**Reference:** Í klínískum samanburðarrannsóknum á eltrombópagi hjá ITP-sjúklingum kom fram hækkun á alanínamínótransferasa (ALAT), aspartatamínótransferasa (ASAT) og bílírúbíní í sermi (sjá kafla 4.8).
**Before:** Í klínískum samanburðarrannsóknum á langvinna blóðstorkuæxli með eltrombópagi komu fram hækkanir á alanínamínótransferasi í sermi (ALT), aspartatamínótransferasi (AST) og bilirúbíni (sjá kafla 4.8).
**After:** Í klínískum samanburðarrannsóknum á langvarandi sjálfvakta blóðflagnafæð með eltrombópagi kom fram aukningu á alanín amínótransferasa í sermi (ALT), aspartat amínótransferasa (AST) og bilirúbíni (sjá kafla 4.8).

</details>

<details><summary>Anchor: p13official21:test:ema:970</summary>

**Source:** In patients with mild hepatic impairment (Child-Pugh A), there was no significant changes in pharmacokinetics compared with normal healthy volunteers.
**Reference:** Hjá sjúklingum með væga skerðingu á lifrarstarfsemi (Child-Pugh A) voru engar marktækar breytingar á lyfjahvörfum samanborið við heilbrigða sjálfboðaliða.
**Before:** Hjá sjúklingum með vægt skerta lifrarstarfsemi (Child-Pugh A) var engin marktæk breytingar á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.
**After:** Hjá sjúklingum með væga skerðingu á lifrarstarfsemi (Child-Pugh A) var engin marktæk breytingar á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.

</details>

<details><summary>Anchor: p13official21:test:ema:709</summary>

**Source:** The other ingredients are sodium chloride, succinic acid, polysorbate 80, 2- phenoxyethanol and water for injections.
**Reference:** Önnur innihaldsefni eru natríumklóríð, succinic sýra, polysorbat 80, 2-fenoxýetanól og vatn fyrir stungulyf.
**Before:** Önnur innihaldsefni eru natríumklóríð, súkfinýlsýra, pólýsorbat 80, 2-fenóxýlethanól og vatn fyrir stungulyf.
**After:** Önnur innihaldsefni eru natríumklóríð, súkfinýlsýra, pólýsórbat 80, 2- fenoxýetanól og vatn fyrir stungulyf.

</details>

<details><summary>Anchor: p13official21:test:eso:43</summary>

**Source:** These super heavyweight stars are extremely rare, forming solely within the densest star clusters.
**Reference:** Þessar ofvöxnu stjörnur eru fágætar og myndast eingöngu innan í þéttum stjörnuþyrpingum.
**Before:** Þessar sterkir stjörnur eru mjög sjaldgæfar og eru aðeins að finna í þokustyrkurum.
**After:** Þessir öflugir stjörnur eru mjög sjaldgæfar og eru aðeins að finna í þokustuastöðum.

</details>

<details><summary>Anchor: p13official21:test:eso:714</summary>

**Source:** By studying this effect it is possible to map out the places where gravity is strongest, and hence where the matter, including dark matter, resides.
**Reference:** Með því að rannsaka áhrifin er hægt að kortleggja hvar þyngdarkrafturinn er mestur og þar af leiðandi hvar efnið, þar á meðal hulduefnið, er.
**Before:** Með þessari rannsókn er hægt að mynda út staðir þar sem svæðið er stærsti og því þar sem efnið, þar með talið dökk efni, er.
**After:** Með þessari rannsókn er hægt að koma á mynd af staðnum þar sem svæðið er stærsti og því þar sem efnið, þar með taldir dökk efni, er að vera.

</details>

<details><summary>Anchor: p13official21:test:eso:134</summary>

**Source:** And yet, even under construction, ALMA has become the best telescope of its kind - as reflected by the extraordinary number of astronomers who requested time to observe with ALMA.
**Reference:** Þrátt fyrir að ALMA sé enn í smíðum er röðin nú þegar orðin besti sjónauki sinnar tegundar í heiminum og endurspeglast það í þeim mikla fjölda stjörnufræðinga sem óskað hafa eftir tíma til að nota ALMA.
**Before:** En þó, jafnvel á framhaldsstöðum, hefur ALMA verið besta sjónauki af þessu tegund - eins og fram kemur óeðlilegur fjölda stjörnufræðinga sem krefðu tíma til að fara með ALMA.
**After:** En þó hefur ALMA verið besta sjónauki af þessu tegund sem það er í byggingu - eins og sýnt er út frá óvenjulegu fjölda stjörnufræðinga sem beiðni voru til um tíma til að sjást með ALMA.

</details>

<details><summary>Anchor: p13official21:test:eso:38</summary>

**Source:** The formation processes of these distant planets are likely to be quite different from those in our Solar System and in Beta Pictoris.
**Reference:** Líklega myndast þessar fjarlægu reikistjörnur með ólíkum hætti en reikistjörnurnar í sólkerfinu okkar og við Beta Pictoris.
**Before:** Myndunarferli þessara fjarreikistjörnur eru líklega verulegari mismunandi en í sólkerfinu okkar og Beta Pictoris.
**After:** Myndunarferlin við myndun þessara fjarreikanda er líklega munu vera mjög ólíkur en í sólkerfinu og Beta Pictoris.

</details>

<details><summary>Anchor: p13official21:test:eso:1123</summary>

**Source:** The galaxy Messier 83 (eso0825) is located about 15 million light-years away in the constellation of Hydra .
**Reference:** Vetrarbrautin Messier 83 (eso0825) er í um 15 milljón ljósára fjarlægð í stjörnumerkinu Vatnaskrímslinu.
**Before:** Galænur Messier 83 (eso0825) er um 15 milljón ljósára fjarlægð í stjörnumerkinu Hýdru.
**After:** Galnur Messier 83 (eso0825) er um 15 milljón ljósára fjarlægð frá Jörðinni í stjörnumerkinu Hýdru.

</details>

<details><summary>Anchor: p13official21:test:eso:710</summary>

**Source:** The VST KiDS survey will allow astronomers to make precise measurements of dark matter, the structure of galaxy halos, and the evolution of galaxies and clusters.
**Reference:** Kortlagningin nefnist VST KIDS og gerir stjörnufræðingum kleift að mæla nákvæmlega staðsetningu hulduefnis, uppbyggingu vetrarbrautahjúpa og þróun vetrarbrauta og þyrpinga.
**Before:** VST KiDS rannsóknin mun gera stjörnufræðingum kleift að gera nákvæmar mælingar á dökku efninu, myndun hringjar í vetrarbrautum og þróun vetrarbrauta og vetrarbrautahópa.
**After:** VST KiDS rannsóknin mun gera stjörnufræðingum kleift að gera nákvæmar mælingar á dökkum efni, myndun hringa vetrarbrauta og þróun vetrarbrauta og þyrpinga.

</details>

<details><summary>Anchor: p13official21:test:eso:1167</summary>

**Source:** Here the visible light emitted by the stars that are forming inside the cloud is completely absorbed by the dust.
**Reference:** Þar gleypir rykið sýnilegt ljós sem stjörnurnar sem eru að myndast innan í skýinu gefa frá sér.
**Before:** Hér birti ljós sem stjörnurnar sem eru í myndun í þvagið út og frýsir allt úr því af rykjunni.
**After:** Hér fráhvarfandi ljós sem stjörnurnar sem eru að mynda sig í þvagið frásogast algerlega af rykjunum.

</details>

<details><summary>Anchor: p13official21:test:eso:558</summary>

**Source:** This proves that the star formation in NGC 3572 has been ongoing for at least 10–20 million years and would imply that the planet formation process could proceed on much longer timescales than previously thought.
**Reference:** Það sannar að stjörnumyndun í NGC 3572 hefur staðið yfir í 10-20 milljónir ára og gefur til kynna að myndunarferli sólkerfa gæti haldið áfram í mun lengri tíma en áður var talið.
**Before:** Þetta sýnir út frá því að stjörnumyndun í NGC 3572 hefur verið áfram í að minnsta kosti 10-20 milljarða ára og myndar það til þess að vetrarbrautin fari fram á mikið lengri tíma en áður var talið.
**After:** Þetta sýnir út frá því að stjörnumyndun í NGC 3572 hefur verið áfram í að minnsta kosti 10-20 milljarða ára og myndar það til þess að fyrirbæri vetrarbrautarnar getur komið fram á mikið lengri tímaþrengi en áður var talið.

</details>

<details><summary>Anchor: p13official21:test:eso:760</summary>

**Source:** Extreme stars like the two components of VFTS 352, play a key role in the evolution of galaxies and are thought to be the main producers of elements such as oxygen.
**Reference:** Ofsafengnar stjörnur eins og í VFTS 352 leika lykilhlutverk í þróun vetrarbrauta og eru taldar meginuppspretta frumefna á borð við súrefni.
**Before:** Hámarkssjár eins og tvö hlutir VFTS 352 spila mikilvægar hlutverki í þróun vetrarbrauta og eru talin vera aðalmyndandi efni sem eigið er ökutípu.
**After:** Alvarlegir stjörnur eins og tvö hlutir VFTS 352 spája í þróun vetrarbrauta og eru talin að vera aðalmyndandi efni svo sem oxíum.

</details>

<details><summary>Anchor: p13official21:test:eso:502</summary>

**Source:** The first five signals are very confident, while the sixth is tentative, and seventh more tentative still.
**Reference:** Fyrstu fimm merkin voru mjög sannfærandi en meiri óvissa ríkir um það sjötta og enn meiri óvissa um hið sjöunda.
**Before:** Fyrstu fimm vísbendingarnar eru mjög vissar en sjötthundruðið er tilbúin og sjötthjárnið enn tilbúin.
**After:** Fyrstu fimm vísbendingarnar eru mjög góðar, þar sem sexa er tilbúin og sjöta enn frekar tilbúin.

</details>

<details><summary>Anchor: p13official21:test:eso:284</summary>

**Source:** The alignment between the ring of stars seen by the NTT in infrared light and the gas seen by ALMA at millimetre wavelengths highlights different aspects of similar structures in the galaxy.
**Reference:** Uppröðun stjörnuhringsins sem NTT greinir í innrauðu ljósi og gassins sem ALMA sér á millímetrasviðinu, sýnir vel ólíka afstöðu svipaðra forma í vetrarbrautinni.
**Before:** Sjálfkærir stjörnur sem NTT sér og gas sem ALMA sér í millímetra ljósi benda til mismunandi hlutverka á svipaðum lígröðum í vetrarbrautinni.
**After:** Samræmi á milli stjörnurnar sem NTT sýnir í innrauðum ljósi og gasins sem ALMA sýnir í millímetra röntgenljós birtir mismunandi þáttir af svipuðum myndum í vetrarbrautinni.

</details>

<details><summary>Anchor: p13official21:test:eso:356</summary>

**Source:** The nebula lies more than four hundred times further away than the famous star.
**Reference:** Þokan er þó meira en fjögur hundruð sinnum lengra í burtu en stjarnan fræga.
**Before:** Nebulinn er meira en fjórhundrað sinnum fjarlægur en fræg stjarnan.
**After:** Nebúnurinn er meira en fjórhundrað sinnum fjarlægri en frægast stjarnan.

</details>

<details><summary>Anchor: p13official21:test:eso:1181</summary>

**Source:** By combining light from three of the VLTIs 1.8-metre Auxiliary Telescopes with the AMBER instrument, this facility allows astronomers to see details equivalent to those a telescope with a mirror of 85 metres in diameter would see.
**Reference:** Með því að sameina ljós frá þremur 1,8 metra aukasjónaukum VLTI við AMBER mælitækið gátu stjörnufræðingar greint smáatriði sem væri aðeins gerlegt með sjónauka með 85 metra spegilþvermál.
**Before:** Með því að setja ljósi úr þremur VLT-1,8 m sjónaukum ásamt AMBER mælitækinu geta stjörnufræðingar sést nákvæmar upplýsingar eins og sjónauki með 85 metra í yfirborði myndi sjá.
**After:** Með því að setja ljósi úr þremur VLT-aðhliðatækinum 1,8 metra í sér með AMBER mælitækinni geta stjörnufræðingar sést nákvæmari upplýsingar og þau sem sjónauki með 85 metra diametrar myndi sjá.

</details>

<details><summary>Anchor: p13official21:test:eso:45</summary>

**Source:** This would make the system similar to our Solar System in terms of the number of planets (seven as compared to the Solar Systems eight planets).
**Reference:** Þetta sólkerfi geymir því svipaðan fjölda reikistjarna og sólkerfið okkar (sjö reikistjörnur í samanburði við átta í sólkerfinu okkar).
**Before:** Þetta myndi gera kerfinu svipað á sólkerfinu okkar í þeim skyni um fjölda reikistjarna (sjö samanborið við átta reikistjörnurnar í sólkerfinu).
**After:** Þetta myndi gera kerfið svipuður heimsferilinn í þeim hætti að fjölda reikistjarna (sjö samanborið við átta reikistjörnurnar í heimsferilinu).

</details>

<details><summary>Anchor: p13official21:test:eso:716</summary>

**Source:** From the gravitational lensing effect, these groups turn out to contain around 30 times more dark than visible matter.
**Reference:** Þyngdarlinsuhrifin sýna að hóparnir innihalda um 30 sinnum meira hulduefni en sýnilegt efni.
**Before:** Frá því sem grátrýmisins skiptir út, eru þessi hópar um það bil 30 sinnum meiri dökku en sýnileg efni.
**After:** Frá því að gráttvöldin hreyfir út kemur úr þessu að þessi hópar innihaldi um 30 sinnum meira dýrum en sýnilegar.

</details>

<details><summary>Anchor: p13official21:test:eso:554</summary>

**Source:** In the lower part of the image a big chunk of the molecular cloud that gave birth to these stellar youngsters still can be seen.
**Reference:** Á neðri helmingi myndarinnar sést stór hluti af sameindaskýinu sem gat af sér stjörnurnar ungu.
**Before:** Í lágri hluta myndarinnar er stór flögu af líkamlegu loftþokunni sem fæddi þessar stjörnuunglingar enn í lagi.
**After:** Í lágari hluta myndarinnar er enn að sjá stór hlut af sameindaskýinu sem fæddi þessi ungbura stjörnur.

</details>

<details><summary>Anchor: p13official21:test:eso:212</summary>

**Source:** This is one of the most dramatic images ever created by the VLT.
**Reference:** Þetta er ein glæsilegasta mynd sem tekin hefur verið með VLT.
**Before:** Þetta er einn af mesta skáðulegustu myndunum sem VLT hefur gerst.
**After:** Þetta er ein af þeim skáðustu myndunum sem VLT hefur gerst.

</details>

<details><summary>Anchor: p13official21:test:eso:410</summary>

**Source:** In either case these objects are intriguing - either as planets without stars, or as the tiniest possible objects in a range spanning from the most massive stars to the smallest brown dwarfs.
**Reference:** Hvor sem raunin er, eru þetta áhugaverð fyrirbæri - annað hvort sem reikistjörnur án stjarna eða minnstu mögulegu fyrirbærin á bili sem spannar massamestu stjörnurnar til smæstu brúnu dverganna.
**Before:** Í báðum tilvikum eru þessi efni íhugað - annaðhvort sem reikistjörnur án stjarna eða minnkunarmálastarfsemi sem er mörguð frá stærstu stjörnum til minnkunarmála.
**After:** Í báðum tilvikum eru þessi fyrirbæri - annaðhvort sem reikistjörnur án stjarna eða minnkasta mögulega fyrirbæri á bilinu frá massamaksstjörnum til minnkasta brúnnarþurrna.

</details>

<details><summary>Anchor: p13official21:test:eso:241</summary>

**Source:** None of the current theories predict these objects,” says Benoît Epinat, another member of the team.
**Reference:** Ekki er til nein kenning í dag sem spáir fyrir um slíka hegðun“ segir Benoît Epinat, meðlimur í hópnum.
**Before:** Enginn þessara hófs áætlana fylgir þessu, sagði Benoît Epinat, annarur aðilar hópsins.
**After:** „Enginn þessara kenndra þekkingar getur búið til þess að fylgja þessum fyrirbærum“ segir Benoît Epinat, einhverjir annarra aðila hópsins.

</details>

<details><summary>Anchor: p13official21:test:eso:803</summary>

**Source:** The team combined these UltraVISTA observations with those from the NASA Spitzer Space Telescope, which probes the cosmos at even longer, mid-infrared wavelengths.
**Reference:** Stjörnufræðingarnir skeytti þessum gögnum UltraVISTA síðan saman við myndir frá Spitzer geimsjónauka NASA, sem mælir mið-innrauðar bylgjulengdir sem eru enn lengri.
**Before:** Hópurinn samantekti þessum UltraVISTA mælingum við þau sem Spitzer geimsjónaukinn NASA gerir á lengri miðlungsinnfræðilegum ljóslennum.
**After:** Hópurinn samið þessar UltraVISTA mælingar við þær sem Spitzer geimsjónauka NASA gerði á lengri miðlungsinnraustu ljós.

</details>

<details><summary>Anchor: p13official21:test:eso:871</summary>

**Source:** A team of astronomers led by Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) first used the ULTRACAM system on ESOs New Technology Telescope to measure these brightness changes very precisely.
**Reference:** Hópur stjörnufræðinga undir forystu Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) notaði fyrst ULTRACAM mælitækið á New Technology Telescope ESO til að mæla birtubreytingarnar með mikilli nákvæmni.
**Before:** Hópur stjörnufræðinga, leidur af Adam Hardy (Universidad Valparaíso í Valparaíso í Chile), fyrst notuði ULTRACAM kerfið á New Technology Telescope ESO til að mæla ljósþurrkunina mjög nákvæmlega.
**After:** Hópur stjörnufræðinga, undir forystu Adam Hardy (Universidad Valparaíso í Chile), notuði fyrst ULTRACAM kerfið á New Technology Telescope ESO til að mæla ljósþurrðar breytingarnar mjög nákvæmlega.

</details>

<details><summary>Anchor: p13official21:test:eso:843</summary>

**Source:** An albedo of 1 corresponds to perfect reflecting white, while 0 is totally absorbing black.
**Reference:** Endurskinshlutfallið 1 samsvarar hvítu yfirborði með fullkomið endurvarp á meðan 0 þýðir að það gleypir ljós að öllu leyti.
**Before:** Albedo sem er 1 samsvarar fullkominni spillingu hvítt, en 0 samsvarar alveg inntöku svarta.
**After:** Albedo sem er 1 samsvarar fullkominni spillingu hvítra, en 0 samsvarar alveg inntöku svarta.

</details>

<details><summary>Anchor: p13official21:test:eea:852</summary>

**Source:** These actions may include comparison of the effectiveness of processes, methods and tools related to the chosen themes, mutual transfer and application of good practice, exchanges of personnel, joint development of products, processes, strategy and methodology, adaptation to different contexts of methods, tools and processes identified as good practice, and/or dissemination of results, profile-raising materials and events.
**Reference:** Aðgerðirnar geta falist í því að bera saman skilvirkni vinnsluferla, aðferða og tóla, sem tengjast þeim þemum sem eru valin, í gagnkvæmri miðlun og ástundun góðra starfsvenja, í starfsmannaskiptum, sameiginlegri þróun vara, vinnsluferla, skipulags og aðferðafræði, í því að aðlaga að ólíku samhengi aðferðir, tól og vinnsluferli, sem eru skilgreind sem góðar starfsvenjur, og/eða í útbreiðslu niðurstaðna og kynningarefnis og skipulagningu viðburða.
**Before:** Þessi aðgerðir geta farið til samanburðar á virkni kerfanna, aðferða og tækjanna sem tengjast valinu þóknunum, mismunandi skipti og beitingu góðrar starfsvenjur, skiptis í starfsmenn, sameiginlega vinnu á vörum, kerfum, áætlunum og aðferðum, aðlögun á mismunandi yfirborði aðferða, tækja og kerfa sem eru tilgreind sem góðar starfsvenjur og/eða dreifingu niðurstöðva, upplýsingaverkana og tilvikana.
**After:** Þessi aðgerðir geta farið í sér samanburð á virkni ferlana, aðferða og tækjanna sem tengjast valinu þóknunum, mismunandi skipti og beitingu góðra starfsvenjur, skipti inni í starfsmenn, sameiginlega vinnslu vöru, ferla, áætlunar- og aðferðafræðis, aðlögun áframhaldsnarfa á mismunandi upphafsrami, tækjum og ferlum sem greind eru góðar starfsvenjur og/eða dreifingu niðursettrar niðurstöðu, upplýsingaverndar- og tilvik.

</details>

<details><summary>Anchor: p13official21:test:eea:1524</summary>

**Source:** In the case of bulk liquid products the lot or sublot shall be thoroughly mixed in so far as possible and in so far it does not affect the quality of the product, by either manual or mechanical means immediately prior to sampling.
**Reference:** Þegar um er að ræða fljótandi farm í lausu máli skal blanda framleiðslueininguna eða framleiðsluhlutann eins vandlega og unnt er, annaðhvort handvirkt eða vélvirkt, rétt áður en sýni er tekið.
**Before:** Ef um er að ræða vökva í magni skal lotur eða undirlotur leysa vel saman eins og mögulegt er og það skuli ekki hafa áhrif á gæði vörunnar, með annaðhvort tæknilegum eða mannafræðilegum aðferðum fyrir upplýsingaskrárnun.
**After:** Ef um er að ræða vökva í magni skal lotur eða undirlotur vera vel blandað með því markmiði að það geti verið, eins og mögulegt er, og það skuli ekki hafa áhrif á gæði vörunnar, með annaðhvort tæknilegum eða mannafræðilegum aðferðum fyrir sér að tekin sé sýnilyf.

</details>

<details><summary>Anchor: p13official21:test:eea:779</summary>

**Source:** In order to encourage the exchange of information and best practice, the focus of these actions will be on supporting the dissemination of expertise present in business universities and training centres and in the new economy in matters such as management and administrative skills, as well as deploying distance-learning facilities.
**Reference:** Í því skyni að stuðla að skiptum á upplýsingum og bestu viðteknu starfsvenjum verður með þessum aðgerðum lögð áhersla á stuðning við miðlun sérfræðiþekkingar, sem er til staðar í viðskiptaháskólum og menntasetrum og í hinu nýja efnahagskerfi, einkum færni á sviði reksturs og stjórnsýslu og einnig að koma upp aðstöðu fyrir fjarnám.
**Before:** Til þess að hvetja til upplýsingaskipta og bestu starfsvenjur verður aðeins aðstoðar meðferð á sérstökum faglegum menntunum í viðskiptaháskólum og umfjöllum og í nýju efnahagskerfinu á þeim sviði sem stjórnun og stjórnsýsluskapi og einnig að nota fyrirframhaldandi fjöldeysisstofnana.
**After:** Til þess að hvetja til skipta á upplýsingum og bestu starfsvenjur verður aðeins aðeins að stuðla að útsendingu sérfræðis sem er í viðskiptaháskólum og þjálfunastofnunum og nýju efnahagsverum á þeim sviði sem stjórnunarskil á og stjórnsýsluskil og að setja fyrir nytjalegu fyrirframhaldsskrifstofnanir.

</details>

<details><summary>Anchor: p13official21:test:eea:2023</summary>

**Source:** If an entity applies Puttable Financial Instruments and Obligations Arising on Liquidation (Amendments to IAS 32 and IAS 1), issued in February 2008, for an earlier period, the amendments in paragraphs 6, 9, A1 and A12 shall be applied for that earlier period.
**Reference:** Ef eining beitir Innleysanlegir fjármálagerningar og skuldbindingar sem verða til við félagsslit (breytingar á IAS-staðli 32 og IAS-staðli 1), sem voru gefin út í febrúar 2008, á fyrra tímabili, skal beita breytingum í lið 6, 9, A1 og A12 fyrir það fyrra tímabil.
**Before:** Ef eining hefur beitt fyrir sér Pútandi fjárhagslegar eignir og skuldbindingar sem koma fram við útskrif (breytingar á IAS-staðli 32 og IAS-staðli 1) sem gefin eru út í febrúar 2008, fyrir tidinu sem er fyrir, skal beita breytingunum í 6., 9., A1- og A12-liðum fyrir þann tid.
**After:** Ef eining beitir til Setningar og skuldbindinga sem koma fram við endurnýtingu (breytingar á IAS-sta- li 32 og IAS-sta-li 1), sem gefin voru út í febrúar 2008, fyrir tidinu sem er fyrir eftir skal beita breytingarnar í 6., 9., A1- og A12-liðum fyrir þann tid sem er fyrir eftir.

</details>

<details><summary>Anchor: p13official21:test:eea:1203</summary>

**Source:** Over the past years, as more decentralised agencies have been created, the budgetary authority has looked to improve transparency and control over the management of the Community funding allocated to them, in particular concerning the budgetisation of the fees, financial control, power of discharge, pension scheme contributions and the internal budgetary procedure (code of conduct).
**Reference:** Eftir því sem fleiri sjálfstæðar stofnanir hafa verið settar á laggirnar á undanförnum árum hefur fjárveitingavaldið hugað að því að auka gagnsæi og eftirlit með umsýslu fjár sem veitt er til þeirra frá Bandalaginu, einkum varðandi það að þjónustutekjur séu taldar með í fjárlögum-, fjármálastjórn, heimildir til að samþykkja fjárlagameðferð, framlög í lífeyrissjóði og fjárhagsáætlunargerð innan stofnunarinnar (starfsreglur).
**Before:** Í fyrirhugaðum árum hefur fundið til að bæta gagnsæi og eftirlit með stjórnun fjármagns bandalagsins sem er gefinn þeim, einkum að því er varðar fjárhagsaðgerð fyrir skuldbindingar, fjármálakeppni, stjórna, lífeyrisbótakvöðvörun og innri fjármálaferlið (reglur um hæfni).
**After:** Á síðustu árum hefur verið skiptist fram meira undirhaldsstofnanir og því hefur fjármálavirkja- yfirvaldið leitað til þess að bæta gagnsæi og eftirlit með stjórnun fjárgeymsla Bandalagsins sem þau fá til úthlutunar, einkum að því er varðar fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega fjárhagslega

</details>

<details><summary>Anchor: p13official21:test:eea:43</summary>

**Source:** Where plant protection products containing the active substance are intended to be used in cold climatic conditions, the tests have to be conducted where DT50lab, determined at 10 °C and at a moisture content of the soil related to a pF value of 2 to 2,5 (suction pressure) is greater than 90 days.
**Reference:** Þegar nota á plöntuvarnarefni, sem innihalda virka efnið, í köldu loftslagi verða prófanirnar að fara fram þar sem DT50lab er meira en 90 dagar, ákvarðað við 10°C og í jarðvegi með rakainnihaldi sem miðast við pF-gildi 2 til 2,5 (sogþrýstingur).
**Before:** Ef áætlun er að nota plöntuverndarvörur sem innihalda virka efni í kaltum loftslagjöknum skulu prófanir framkvæmdar þegar DT50lab, á 10°C og með vökvaþéttni yfir í jarðinu sem tengist pF gildi 2 til 2,5 (sýruefri styrkur), er meiri en 90 daga.
**After:** Ef áætlað er að nota plöntuvarnarefni sem innihalda virka efni í kaltum varmaástandi skulu prófanir fara fram þegar DT50lab, sem ákvarðað er við 10°C og á vökvaþéttni yfir um landi sem tengist pF gildi 2 til 2,5 (sýruefri styrkur), er meiri en 90 daga.

</details>

<details><summary>Anchor: p13official21:test:eea:571</summary>

**Source:** To check power-operated windows/roof-panel systems/partition systems with reversing devices, a measuring instrument/test rod shall be placed through the opening from the inside of the vehicle or, in the case of a partition system, from the rear part of the passenger compartment in such a way that the cylindrical surface of the rod contacts any part of the vehicle structure which forms the boundary of the window/roof-panel aperture/partition.
**Reference:** Ef gera á athugun á rafstýrðum rúðum/þaklúgukerfum/skilrúmskerfum með enduropnunarbúnaði er mælitæki/prófunarstöng sett í gegnum opið innan frá úr ökutækinu eða, þegar um er að ræða skilrúmskerfi, frá aftari hluta farþegarýmis með þeim hætti að sívalt yfirborð stangarinnar snertir einhvern þann hluta ökutækisins sem afmarkar gluggann/þaklúguopið/skilrúmið.
**Before:** Til að athuga verkstæða-gerðir glugga/þekjuflagna/fyrirhluta með bakslögunartækni skal setja mælitæki/prófunarrod út í skýrinu frá inni á ökutækinu eða, ef um fyrirhluta er að ræða, frá enda hluta sjónsykisins og þannig að hringræn yfirborð prófunarroðsinnar snertir allt yfirborð ökutæknisins sem myndar skýrinu/þekjuflagna/fyrirhluta.
**After:** Til að kanna áræði öllu þar sem styrk er notað til að opna glugga/þekjuflöt/virki með endurkomuferli skal setja mælitæki/prófunartörl yfir slíkt opnun í innanbúningu ökutækisins eða, ef um er að ræða virki, frá afturhlið sjóðarinnar, þannig að hringlífurinn snertir einhverja hluta af byggingu ökutækisins sem eru viðmiðunarmörk slíks opnunar.

</details>

<details><summary>Anchor: p13official21:test:eea:1768</summary>

**Source:** The competent authorities of Ukraine confirmed their preparedness to continue comprehensive oversight of Ukraine Cargo Airways and their commitment to provide the Air Safety Committee with the complete decision regarding the effectiveness of the implementation by Ukraine Cargo Airways of its corrective action plan.
**Reference:** Lögbær yfirvöld í Úkraínu staðfestu að þau væru reiðubúin til að hafa áfram alhliða eftirlit með Ukraine Cargo Airways og þau skuldbinda sig til að veita Flugöryggisnefndinni afdráttarlausan úrskurð að því er varðar skilvirkni framkvæmda Ukraine Cargo Airways á áætlun flugrekandans um aðgerðir til úrbóta.
**Before:** Lögbær yfirvöld í Úkraíni staðfestu framkvæmdastjórnina um Úkrain Cargo Airways að halda áfram almennu eftirliti og það að veita flugöryggisnefndinni fullan ákvörðun um árangursáhrif framkvæmdar Úkrain Cargo Airways af áætlun sinni um leiðréttingar.
**After:** Lögbæru yfirvöldum Úkraíns staðfestu að þeir hafi tilhögun til að halda áfram almennu eftirliti með flugfélög Ucrain Cargo Airways og að þeim sé skyldt að veita flugöryggisnefndinni fullkomna ákvörðun um framkvæmd árangursáætlunar flugfélags Ucrain Cargo Airways.

</details>

<details><summary>Anchor: p13official21:test:eea:1751</summary>

**Source:** On the basis of the common criteria, and in view of the fact that, to date, ICAO has not agreed to the closure of any of the findings raised during its audits, it is assessed that, at present, the competent authorities of Indonesia have failed to demonstrate that they have performed their regulatory and oversight responsibilities in compliance with ICAO standards with respect to all the carriers they certify.
**Reference:** Á grundvelli sameiginlegu viðmiðananna og í ljósi þess að enn sem komið er hefur Alþjóðaflugmálastofnunin ekki samþykkt lyktir neinna þeirra mála sem komu í ljós við úttektir hennar er það metið svo að eins og sakir standa hafi lögbær yfirvöld í Indónesíu ekki getað sýnt fram á að þau hafi gætt ábyrgðar sinnar á sviði reglusetningar og eftirlits í samræmi við staðla Alþjóðaflugmálastofnunarinnar með tilliti til allra flugrekenda sem þau votta.
**Before:** Á grundvelli sameiginlegra viðmiðana og með tilliti til þess að ICAO hefur ekki samþykkt að loka neinu af niðurstöðum sem komu fram í skoðunum sínum, er greint að lögbær yfirvöld Indóneeslands hafi ekki sýnt fram á að þeir hafi uppfyllt skyldur sitt um reglur og eftirlit með flugrekendum, í samræmi við staðla ICAO, að því er varðar öll flugrekendum sem þau sannfæra.
**After:** Á grundvelli sameiginlegra viðmiðana og með tilliti til þess að ICAO hefur ekki samþykkt að lokastarfsemi einhverja af niðurstöðum sem komið var fram í endurskoðunum sínum, er metin að lögbæra yfirvald Indónesíu hafi núna missið áfram að sýna fram á að þau hafi uppfyllt skuldbindingar sínar um stjórnsýslu og eftirlit í samræmi við staðla ICAO að því er varðar öll flutningafélög sem þau veita vottorð fyrir.

</details>

<details><summary>Anchor: p13official21:test:eea:386</summary>

**Source:** Purpose: to inform the management and staff of the facility of the reason for the test facility inspection or study audit that is about to take place, and to identify the facility areas, study(ies) selected for audit, documents and personnel likely to be involved.
**Reference:** Markmið: að tilkynna stjórn og starfsliði prófunarstöðvarinnar um ástæðuna fyrir því að skoða á prófunarstöðina eða gera úttekt á rannsóknum og nefna þá hluta prófunarstöðvarinnar, rannsókn(ir), skjöl og starfsmenn sem líklegt er að komi við sögu við skoðunina eða úttektina.
**Before:** Tilgangur: til að upplýsa stjórnun og starfsfólki í stöðinni um ástæðu eftir rannsókn á eða rannsókn á eftirliti með prófunarstöðvarina sem er að fara fram, og til að greina útgáfur stöðvarinnar, rannsóknirnar sem valin eru fyrir eftirlit, skjöl og starfsfólki sem líklega verða að taka þátt í eftirlitinu.
**After:** Tilgangur: til að upplýsa stjórnun og starfsmenn viðkomandi stöðvar um ástæðu eftir eftirliti með prófunarstöðvar eða rannsóknar eftirlit sem er að fara fram og til að greina útgáfu stöðvarinnar, þeim staðum í henni sem rannsóknirnar, sem valin eru fyrir eftirlit, skjal og starfsfólki sem líklegt er að taka þátt í.

</details>

<details><summary>Anchor: p13official21:test:eea:409</summary>

**Source:** Purpose: to determine whether the test facility, if engaged in studies using animals or other biological test systems, has support facilities and conditions for their care, housing and containment, adequate to prevent stress and other problems which could affect the test system and hence the quality of data.
**Reference:** Markmið: að ákvarða hvort prófunarstöðin, ef þar eru stundaðar rannsóknir með dýr eða önnur líffræðileg prófunarkerfi, hefur yfir að ráða búnaði og aðstöðu þar sem hægt er að hirða um þau, koma þeim fyrir og einangra þau á annan viðeigandi hátt þannig að koma megi í veg fyrir streitu og önnur vandamál sem gætu haft áhrif á prófunarkerfið og þar af leiðandi á gæði gagnanna.
**Before:** Tilgangur: til að ákvarða hvort prófunarstöð varði stofnun og skilyrði til að hafa áhættuvernd fyrir dýrum eða öðrum líffræðilegum prófunarkerfum, svo að það geti komið í veg fyrir þróun og annað vandamál sem geta haft áhrif á prófunarkerfinu og þannig gagnasmiði.
**After:** Tilgangur: til að ákvarða hvort prófunarstöð varði stofnun og skilyrði fyrir meðhöndlun og húsmiðlun og innrennsli þeirra, sem hún er í notkun í rannsóknum með dýrum eða öðrum líffræðilegum prófunarkerfum, séu nægilegar til að koma í veg fyrir þróun og aðrar vandamál sem geta haft áhrif á prófunarkerfið og þar af leiðandi gæði gagna.

</details>

<details><summary>Anchor: p13official21:test:eea:882</summary>

**Source:** Following at least two years of absence of any clinical or other sign of VHS and/or IHN, all farms in the zone or any farm in a non-approved zone which are to be approved must be health-inspected twice per year for two years.
**Reference:** Þegar liðin eru minnst tvö ár án þess að nokkur klínísk vísbending eða önnur vísbending hafi fundist um veirublæðingu og/eða iðradrep verður að fara fram heilbrigðisskoðun að minnsta kosti tvisvar á ári í tvö ár á öllum eldisstöðvum á svæðinu eða á hverri eldisstöð sem á að viðurkenna á svæði sem ekki er viðurkennt.
**Before:** Eftir að einkenni af VHS og/eða IHN hafa ekki komið fram í að minnsta kosti tvær ár verður að sjúkrahita allar búið í svæðinu eða einn búið í svæðinu sem ekki hefur verið samþykktur, tvisvar á ári í tvær ár.
**After:** Eftir að einkenni af völdum VHS og/eða IHN hafa ekki komið fram í að minnsta kosti tvær ár verður að sjúkrahagskýrslugerð vera fyrir öll bújörð í svæðinu eða einn bújörð í svæðinu sem er ekki samþykkt og þarf að samþykkja, tvisvar á ári í tveimur árum.

</details>

<details><summary>Anchor: p13official21:test:eea:2125</summary>

**Source:** In addition, the sub-processing should only consist of the operations agreed in the contract between the data exporter and the data importer incorporating the standard contractual clauses provided for in this Decision and should not refer to different processing operations or purposes so that the purpose limitation principle set out by Directive 95/46/EC is respected.
**Reference:** Þá skal ráðstöfun til undirverktaka aðeins fela í sér þær aðgerðir sem samþykktar eru í samningnum milli gagnaútflytjanda og gagnainnflytjanda og sem inniheldur föstu samningsákvæðin sem kveðið er á um í þessari ákvörðun og þessi ráðstöfun skal ekki ná yfir annars konar gagnavinnslu eða hafa annan tilgang svo að meginreglan um takmörkun vegna tilgangs, sem sett er fram í tilskipun 95/46/EB, sé virt.
**Before:** Auk þess skal undirvinnslunin einungis vera aðgerðirnar sem samþykktar voru í samningnum um gagnaflutning og gagnainnflutning, þar sem fylgja staðla samningsreglum sem kveðið er á um í þessari ákvörðun og ekki má vísa til annarra aðgerða eða tiltekna áfengis svo að meginreglunni um takmarkaðri markmiði, sem sett er fram í tilskipun 95/46/EB, sé fylgt.
**After:** Auk þess skal undirvinnslunni einungis vera aðgerðirnar sem samningurinn um gagnaútandi og gagnainn- haldandi gerðu samþykktar og þar með talið staðla- samningarsamkvæðin sem kveðið er á um í þessari ákvörðun og ekki vísa til annarra aðgerða eða viðmiðana svo að því að markaðssetningu á markmiðum, sem settar eru fram í tilskipun 95/46/EB, sé uppfyllt.

</details>

<details><summary>Anchor: p13official21:test:eea:2178</summary>

**Source:** The parties agree that on the termination of the provision of data-processing services, the data importer and the sub-processor shall, at the choice of the data exporter, return all the personal data transferred and the copies thereof to the data exporter or shall destroy all the personal data and certify to the data exporter that it has done so, unless legislation imposed upon the data importer prevents it from returning or destroying all or part of the personal data transferred.
**Reference:** Aðilar eru sammála um að við lok gagnavinnslunnar skulu gagnainnflytjandinn og undirverktakinn skila gagnaútflytjandanum öllum persónuupplýsingum, sem hafa verið fluttar, og afritum af þeim, ef hann óskar eftir því, eða eyðileggja allar persónuupplýsingarnar og veita gagnaútflytjandanum fulla vissu fyrir því að hann hafi gert það nema lög, sem gagnainnflytjandinn heyrir undir, komi í veg fyrir að hann geti skilað eða eyðilagt allar persónuupplýsingar sem hafa verið fluttar eða hluta þeirra.
**Before:** Sjálfboði þeirra er að við lok dæmisfræðisþjónustunnar skulu innflytjendur persónuupplýsinga og undirfyrirtæki, á völdum útflutningsins, gefa innflytjandi upplýsingahöfnin öllum persónuupplýsingunum sem hafa verið flutt og afritum þeim eða eyða allar persónuupplýsingarnar og sannprófa innflytjandi upplýsingahöfnum að það hafi gert það, nema löggjöf sem sett er á innflytjandi upplýsingahöfnum hindrar það að gefa innflytjandi upplýsingahöfnum öllum persónuupplýsingunum sem hafa verið flutt og afritum eða eyða allar persónuupplýsingarnar og sannprófa innflytjandi upplýsingahöfnum að það hafi gert það.
**After:** Sérhverjir hafa samþykkt að þegar geymslur á gagnavinnsluþjónustu eru lokið skulu gagnaútgjaldið og undirgreiddur gagnaþolendur, í vali útgjaldandi gagna, senda til útgjaldandi gagna öllum persónulegum gögnum sem hafa verið flutt og afritum þeirra eða eyða allar persónulegar gögnin og sannprófa útgjaldandi gagna að þau hafi gert það, nema löggjöf sem sett er á gagnaútgjaldið stendur í veg fyrir það að hann geti ekki sendið eða eyddi allar persónulegar gögnum eða hluta þeirra.

</details>

<details><summary>Anchor: p13official21:test:eea:1190</summary>

**Source:** Indeed, there is a need for technical and scientific support and a high level of stable expertise to properly apply the Community legislation in the fields of maritime safety and ship pollution prevention, to monitor its implementation and to evaluate the effectiveness of the measures in place.
**Reference:** Raunar er þörf á tækni- og vísindalegri aðstoð og öflugri og yfirgripsmikilli sérfræðiþekkingu til að beita með réttum hætti löggjöf Bandalagsins á sviði siglingaöryggis og varna gegn mengun frá skipum, fylgjast með framkvæmd hennar og meta skilvirkni þeirra ráðstafana sem eru fyrir hendi.
**Before:** Það er þörf á tæknilegri og vísindalegu stuðningu og mikil stöðugt sérfræðileg mat til að beita rétt fyrir löggjöf bandalagsins um öryggi á sjó og að koma í veg fyrir að hægt sé að bæta úr skellunni af skipum, til að fylgjast með framkvæmdi hennar og meta árangur ráðstafana sem eru í gildi.
**After:** Það er þörf á tæknilegri og vísindalegu stuðningu og mikil stöðugt sérfræðileg mat til að beita framkvæmd árekstur Bandalagsins í sviði öryggis á sjó og að koma í veg fyrir að hægt sé að bregðast við framkvæmd þess og meta árangur ráðstafana sem eru í gildi.

</details>

<details><summary>Anchor: p13official21:test:eea:850</summary>

**Source:** When implementing this strand the Commission will in particular ensure consistency and complementarity with the activities conducted by other Commission services or by European agencies; in particular, the European Foundation for the Improvement of Living and Working Conditions and the Community RTD Framework programme and the European Centre for the Development of Vocational Training (Cedefop).
**Reference:** Við framkvæmd aðgerða í þessum flokki mun framkvæmdastjórnin sérstaklega sjá til þess að þær séu í samræmi við og komi til fyllingar starfsemi sem aðrar þjónustugreinar framkvæmdastjórnarinnar eða evrópskar stofnanir stýra, einkum Evrópustofnun um bætt lífskjör og starfsskilyrði, rammaáætlunbandalagsins um rannsóknir og tækniþróun og Evrópumiðstöð um þróun starfsmenntunar (CEDEFOP).
**Before:** Þegar framkvæmd þessarar hóps er gerð mun framkvæmdastjórnin sérstaklega tryggja samræmi og aukabill við starfsemi annarra þjónustu framkvæmdastjórnarinnar eða evrópskra stofnana; sérstaklega Evrópuð stofnun fyrir bætur á aðgerðum til að bæta lífsgjafar- og vinnuþáttum og rannsóknaráætlun evrópska samanburðarríkisins um rannsóknir á tæknilegri og tæknilega sviði og Evrópuskrána fyrir þjálfun í sviði starfsþjálfunar (Cedefop).
**After:** Þegar framkvæmd þessara strandar verður að ráða framkvæmdastjórnin einkum að samræmi og aukabundning við starfsemi annarra þjónustuveitenda framkvæmdastjórnarinnar eða evrópskra stofnana sé tryggt; einkum með því að tryggja starfsemi Evrópusamstofnunarinnar fyrir bætur á aðgerðum til að bæta lífvernd og vinnuþátttöku og rannsóknaráætlunina um rannsóknir og uppbyggingu á rannsóknarskilyrðum í bandalaginu (RTD) og Evrópska stofnunarinnar fyrir þjálfun í sviði starfsþjálfunar (Cedefop).

</details>

<details><summary>Anchor: p13official21:test:eea:568</summary>

**Source:** This device shall reverse the window/roof panel/partition before it exerts a pinch force of more than 100 N within the opening of 200 mm to 4 mm above the top edge of a power-operated window/partition or in front of the leading edge of a sliding roof panel and at the trailing edge of a tilting roof panel.
**Reference:** Þessi búnaður skal enduropna gluggann/þaklúguna/skilrúmið áður en klemmuaflið nær gildinu 100 N, innan ops sem er 200 mm til 4 mm yfir efri brún rafstýrðrar rúðu/skilrúms eða framan við leiðandi brún rennandi þaklúgu og við aftari brún þaklúgu sem er hnikað til.
**Before:** Þetta tæki skal snúa glugga/þörmu/teppi fyrir fram á þann tíma sem það skuli stunda meira en 100 N á 200 mm til 4 mm yfir háttar brún í glugga/þörmu/teppi eða fyrir framan háttar brún í slímhlaupi þörmunnar eða yfir háttar brún í hlaupi þörmunnar.
**After:** Þessi búnaður skal endurskoða glugga/þörmu/vefjarlægð áður en það skilur meira en 100 N áræðisþrýstingi innan opnunar sem er 200 mm til 4 mm yfir hátrarlið vélí eða þrátt við hátrarlið þolsþörmu og í fyrirhlið hátrarlið þolsvefjarlæggings.

</details>

<details><summary>Anchor: p13official21:test:eea:1557</summary>

**Source:** The Commission Communication ‘i2010 - A European Information Society for growth and employment (COM(), developing the Lisbon strategy, seeks to ensure coherence across the Commission's information society and media policies in order to reinforce the significant contribution of information and communication technologies to the performance of the economies of Member States.
**Reference:** Í orðsendingu framkvæmdastjórnarinnar „i2010 – upplýsingasamfélagið í Evrópu í þágu hagvaxtar og atvinnu“(COM (), þar sem Lissabon-áætlunin er útfærð, er leitast við að tryggja samræmi innan stefnu framkvæmdarstjórnarinnar um upplýsingasamfélagið og fjölmiðla í því skyni að styrkja mikilvægt framlag upplýsinga- og samskiptatækni til efnahagslegrar afkomu aðildarríkjanna.
**Before:** Í orðsendingu framkvæmdastjórnarinnar „i2010 – Evrópska upplýsingahópi til vaxtar og launþátta (COM(2009) 478, þjálfun í lögum um stefnumarkmið í Lissabon, er aðstoða að tryggja samhliða meðferð í ramma- og fjarskiptalögunum framkvæmdastjórnarinnar til að veita verulega þátttöku upplýsingakerfa og fjarskipta- kerfa í hagstöðum aðildarríkjanna.
**After:** Í orðsendingu framkvæmdastjórnarinnar „i2010 – Evrópska upplýsinga- og fjarskiptahósi til vaxtar og starfsemi (COM(2009) 478, þar sem hún er að því að stuðla að samræmi í upplýsingahópi framkvæmdastjórnarinnar og fjarskiptavísindum, til að styrkja mikilvægan þátt upplýsingatækni og fjarskipta- tækni við efnahagskerfi aðildarríkjanna,“ er miðað við að tryggja samræmi milli upplýsingahópsins og fjarskiptavísindaframkvæmdastjórnarinnar.

</details>

<details><summary>Anchor: p13official21:test:eea:1716</summary>

**Source:** In addition, the competent authorities of Gabon provided evidence to the Commission of the adoption of a new civil aviation code in May 2008, of the development of specific operating regulations for airworthiness and operations, and informed that the decision to establish an independent civil aviation agency (ANAC) was taken and should be promulgated in July 2008.
**Reference:** Þar að auki létu lögbær yfirvöld í Gabon framkvæmdastjórninni í té sönnun þess efnis að samþykktar hefðu verið nýjar reglur um almenningsflug í maí 2008 og að í undirbúningi væru sérstakar rekstrarreglur um lofthæfi og rekstur og tilkynntu þau að ákvörðun hefði verið tekin um að koma á fót sjálfstæðri stofnun á sviði almenningsflugs (ANAC) sem vænst er að verði tilkynnt um í júlí 2008.
**Before:** Einnig lagði lögbær yfirvöld í Gabón fram sannanir um samþykki fyrir framkvæmda- stjórnina um nýja flugregla fyrir ríkisflugina í maí 2008, um þróun sértækra rekstri reglur um flugþekkingu og rekstur og tilkynnti um það að ákvörðunin um að setja stofnun sem er óháð flugmálastofnunum (ANAC) var tekin og ber að framkvæma hana í júlí 2008.
**After:** Að auki lagði lögbæra yfirvald í Gabón fram sönnunargögn um það að nýtt samþykkti samantekt um samkvæmt- stofnunum fyrir flugvernd og -rekstur, á maí 2008, um þróun sérstakra rekstrarreglna um flugvélstarfsemi og rekstur og tilkynnti um það að ákvörðunin um að setja stofnun sem er óháð og starfandi fyrir flugvernd (ANAC) var tekin og ber að hún verði framkvæmdar á júlí 2008.

</details>

<details><summary>Anchor: p13official21:test:eea:2120</summary>

**Source:** In order to facilitate data flows from the European Union, it is desirable for processors providing data-processing services to several data controllers in the European Union to be allowed to apply the same technical and organisational security measures irrespective of the Member State from which the data transfer originates, in particular in those cases where the data importer receives data for further processing from different establishments of the data exporter in the European Union, in which case the law of the designated Member State of establishment should apply.
**Reference:** Til að auðvelda gagnaflæði frá Evrópusambandinu er æskilegt að vinnsluaðilar, sem veita mörgum ábyrgðaraðilum gagna í Evrópusambandinu gagnavinnsluþjónustu, fái leyfi til að beita sömu tæknilegu og skipulagslegu öryggisráðstöfunum, óháð því frá hvaða aðildarríki gögnin eru flutt, einkum í þeim tilvikum þar sem gagnainnflytjandinn tekur við gögnum til frekari vinnslu frá mismunandi starfsstöðvum útflutningsaðila í Evrópusambandinu, en þá gilda lög þess aðildarríkis þar sem starfsstöðin er staðsett.
**Before:** Til þess að auðvelda gagnaflokkun frá Evrópusambandinu er æskilegt að rekstraraðilar sem veita gagna- rekstrarþjónustu fyrir nokkrar gagna- stjórnendur í Evrópusambandinu séu heimilt að beita sömu tæknilegum og stjórnsýsluframkvæmdaöryggismeðferðum án tillits til þess aðildarríkis sem gagnaflutningin er frá, einkum þegar gagna- innflytjandinn fær gögn til frekari rekstri frá annarra stofnana úr gagna- flutningslandi í Evrópusambandininu, þá skal beita löggjöf þeirra aðildarríkis sem sett er á stað.
**After:** Til þess að auðvelda gagnaflokkun frá Evrópusambandinu er æskilegt að vinnslumyndandi, sem veitir gagna- rekstrarþjónustu fyrir nokkrar gagna- haldandi einstaklinga í Evrópusambandinu, sé heimilt að beita sömu tæknilegum og stjórnsýslulegum öryggismeðferðum án tillits til þess aðildarríkis sem gögnin koma frá, einkum þegar gagna- innflytjendur fær gögn til frekari rekstri frá annarra starfshúsum úr gagna- útflytjendunni í Evrópusambandinu, þá skal beita lögum þeirra aðildarríkis sem sett er á staðfestingu.

</details>

<details><summary>Anchor: p13official21:test:eea:1601</summary>

**Source:** Activities will encourage the design, development or adaptation and/or promotion of effective technological tools to deal adequately with illegal content and to fight against harmful conduct online, in particular those tools made available free of charge for easy general use by stakeholders, and will also encourage the promotion by service operators of safe, responsible use of connections in order to protect children against illegal and harmful activities.
**Reference:** Með aðgerðunum er hvatt til hönnunar, þróunar og aðlögunar og/eða eflingar á skilvirkum tæknibúnaði til að bregðast við ólöglegu innihaldi á fullnægjandi hátt og berjast gegn skaðlegri háttsemi á Netinu, einkum búnaði sem er til umráða án endurgjalds og er viðkomandi aðilum auðveldur til almennra nota, þjónustuaðilar eru einnig hvattir til að efla örugga og ábyrga notkun tenginga til að verja börn gegn ólöglegum og skaðlegum athöfnum.
**Before:** Starfsemi þess er hún áhuga til að stuðla að hönnun, þróun eða aðlögun og/eða framkvæmd virka tækni til að fylgjast fullnægjandi með ólögum við ólöglegu innihaldi og beri að berjast gegn skaðlegri aðgerðum í netinu, einkum þeim tækjum sem eru frjálsir af staðnum til að nýta auðveldlega og að þau séu notaðar af markaðsleyfishafi, og mun einnig stuðla að því að rekstraraðilar stofna starfsþjónustunnar stuðla að öruggri og ábyrgði notkun tenginga til að vernda börnin gegn ólögum og skaðlegum starfsemi.
**After:** Starfsemi verður að hvetja til þess að hönnu og þróa tækni- og tækniframkvæmd eða uppfærðar og/eða að stuðla að því að virkja skilvirka tækni til að gera viðeigandi ráðstafanir gegn ólögum í hlutabréfsáttamála og berjast gegn skaðlegri aðgerðum á netinu, einkum þeim tækjum sem eru frjálsir fyrir notendur með beinni rekstri og að þau séu notaðir með öryggis- og ábyrgðarskynli, og verður einnig að hvetja til að þeir sem stofna rekstur senda út á því að vera áfram að nota örugga og ábyrgðarskynlæg tæki til að vernda börn gegn ólögum og skaðlegum starfsemi.

</details>

<details><summary>Anchor: p13official21:test:ema:1156</summary>

**Source:** Epoprostenol: limited data obtained from a study (AC-052-356 [BREATHE-3]) in which 10 paediatric patients received the combination of bosentan and epoprostenol indicate that after both single- and multiple-dose administration, the Cmax and AUC values of bosentan were similar in patients with or without continuous infusion of epoprostenol (see section 5.1).
**Reference:** Epópróstenól: Takmarkaðar upplýsingar úr rannsókn (AC-052-356 [BREATHE-3]) þar sem 10 börn fengu samsetta meðferð með bósentani og epópróstenóli benda til þess að eftir bæði staka og endurtekna skammta séu Cmax og AUC gildi bósentans svipuð hjá sjúklingum, með eða án samfellds innrennslis epópróstenóls (sjá kafla 5.1).
**Before:** Epoprostenol: Tilkynntar upplýsingar úr rannsókninni (AC-052-356 [BREATHE-3]) þar sem 10 barn voru gefin samsetta meðferð með bosentani og epóprostenól benda til þess að eftir skammta af einum og margum skömmtum, var Cmax og AUC gildi fyrir bosentan svipuð hjá sjúklingum með eða án stöðugrar innrennslis með epóprostenóli (sjá kafla 5.1).
**After:** Epoprostenól: takmarkaðar upplýsingar sem fengnar voru í rannsókninni (AC-052-356 [BREATHE-3]) þar sem 10 sjúklingar með börnafæð fengu samsetningu bósentans og epóprostenóls benda til þess að eftir skammta af báðum staka og margra skammta var Cmax og AUC gildi bósentans svipuð hjá sjúklingum með eða án áframhaldandi innrennsli af epóprostenól (sjá kafla 5.1).

</details>

<details><summary>Anchor: p13official21:test:ema:607</summary>

**Source:** Since the possibility of increased risk of cancer development in patients with newly diagnosed dysplasia treated with infliximab is not established, the risk and benefits to the individual patients must be carefully reviewed and consideration should be given to discontinuation of therapy.
**Reference:** Þar sem ekki hefur verið gengið úr skugga um hugsanlega aukna hættu á krabbameinsmyndun hjá sjúklingum með nýgreindan misvöxt sem fá infliximab, verður að endurskoða gaumgæfilega áhættu og ávinning fyrir hvern sjúkling um sig og íhuga á að stöðva meðferð.
**Before:** Þar sem ekki hefur verið sýnt fram á möguleika á aukinni hættu á krabbameinsuppkomu hjá sjúklingum með nýtt greiningu á vefjaskipta og sem fá infliximab, er nauðsynlegt að endurskoða áhættu og ávinning fyrir hverju sjúklingi og íhuga skal hvort þessi meðferð sé hætt.
**After:** Þar sem ekki er sýnt fram á möguleika á aukinni hættu á krabbameinsuppbrot hjá sjúklingum með nýja greiningu á vefjaskipta sem fá meðferð með infliximabi, skal endurskoða áhættu og ávinning hjá einstaklingum varlega og íhuga að hætta meðferð.

</details>

<details><summary>Anchor: p13official21:test:ema:3025</summary>

**Source:** Based on individual patient response and tolerability, the dose may be increased to 300 mg (15 ml) per day after an interval of 3 to 7 days, and if needed, to a maximum dose of 600 mg (30 ml) per day after an additional 7-day interval.
**Reference:** Eftir svörun og þoli hvers sjúklings má auka skammtinn í 300 mg (15 ml) á sólarhring eftir 3-7 daga og ef þörf krefur í hámarksskammt, 600 mg (30 ml) á sólarhring, eftir 7 daga til viðbótar.
**Before:** Bundin þar sem tilgreind er svörun og þol sjúklings er metið má auka skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga fresti og ef nauðsyn krefur í 600 mg (30 ml) á dag eftir 7 daga fresti.
**After:** Bundnuð við svörun og þol sjúklings er hægt að auka skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga fresti og ef nauðsyn krefur í 600 mg (30 ml) á dag eftir 7 daga fresti.

</details>

<details><summary>Anchor: p13official21:test:ema:2498</summary>

**Source:** Direct administration of dapagliflozin to weanling juvenile rats and indirect exposure during late pregnancy (corresponding to the second and third trimesters of pregnancy with respect to human renal maturation) and lactation are each associated with increased incidence and/or severity of renal pelvic and tubular dilatations in progeny.
**Reference:** Bein lyfjagjöf dapagliflozins hjá ungum rottum sem eru nýhættar á spena og óbein útsetning á síðari hluta meðgöngu (tímabil sem svarar til annars og síðasta þriðjungs meðgöngu hvað varðar nýrnaþroska hjá mönnum) og þegar ungar eru á spena, tengjast hvert fyrir sig aukinni tíðni og/eða umfangi útvíkkana á nýrnaskjóðum og nýrnapíplum hjá afkvæmum.
**Before:** Bein gjöf dapagliflozins til fósturskynja ungum rottum og óbein útsetningur á meðan á seinkun stendur (samsvarar annars vegar og þrjár vikum meðgöngu í tengslum við nýrnastarfsemi hjá mönnum) og meðal eða meðal alvarleika blöndunar í kyrningahúð og blöndum er sambærilegt við aukna tíðni og/eða alvarleika blöndunar í kyrningahúð og blöndum í barni.
**After:** Bein gjöf dapagliflozins til þess að hægja á undangengnum rottum og óbein útsetningur á meðan á seinkun stendur (sem samsvarar annarri og þriðju meðferðartímabili með tilliti til nýrnastarfsemi hjá mönnum) og meðal meðgöngu tengist hvers kyns afleiðinga aukinni tíðni og/eða alvarleika þrýstingar og þrýstingarblöndna í nýrum.

</details>

<details><summary>Anchor: p13official21:test:ema:978</summary>

**Source:** Similarly, the geometric mean AUC (CV%) values at Cycle 6 were higher among the subcutaneous group than the intravenous group; 4088 μg day/mL (34.2) versus 3630 μg day/mL (32.8) respectively) with a resulting adjusted geometric mean ratio [90% CI] of 1.10 [0.98-1.24].
**Reference:** Sömuleiðis var margfeldismeðaltal AUC (flatarmál undir þéttniferli) (fráviksstuðull) í meðferðarlotu 6 hærra hjá hópnum sem fékk MabThera undir húð en hjá hópnum sem fékk MabThera í æð; 4.088 μg dag/ml (34,2) borið saman við 3.630 μg dag/ml (32,8) respectively og leiðrétt hlutfall margfeldismeðaltala [90% öryggismörk] var því 1,10 [0,98-1,24].
**Before:** Eins og áður var meðalgeðið AUC (CV%) gildi í 6. lotu hærri hjá undirhúða hópnum en hjá hópnum sem fengu inndælingu í bláæð; 4088 μg dag/ml (34,2) samanborið við 3630 μg dag/ml (32,8) í skiptum röðum, sem leiddi til að jafnframt með bilun á meðalgeðið [90% CI] 1,10 [0,98-1,24].
**After:** Að jafnframt var meðalgeðið AUC (CV%) gildi við 6. lotu hærri hjá undirhúðaþýðinum en þeim sem fengu inndælingu í bláæð; 4088 μg daga/ml (34,2)% samanborið við 3630 μg daga/ml (32,8)% og endurheimtur meðaltalsgeðsliðar [90% CI] var 1,10 [0,98-1,24].

</details>

<details><summary>Anchor: p13official21:test:ema:2690</summary>

**Source:** Adverse effects not observed in clinical studies but seen in the rat and to a lesser extent in the mouse at exposure levels similar to human exposure levels and with possible relevance for clinical use were liver changes, indicating an adaptive response such as increased weight and centrilobular hypertrophy, fatty infiltration and increased liver enzymes in plasma.
**Reference:** Aukaverkanir, sem komu ekki fram í klínískum rannsóknum, en sáust hjá rottum og hjá músum þó í minna mæli, við skammta sem eru svipaðir meðferðarskömmtum hjá mönnum og skipta hugsanlega máli við klíníska notkun, voru lifrarbreytingar sem gefa til kynna aðlögunarsvörun eins og aukna þyngd og stækkun í miðju lifrarblaða, fituíferð og aukningu á lifrarensímum í plasma.
**Before:** Aukaverkanir sem ekki sást í klínískum rannsóknum en sáust hjá rottum og mjög minni marki hjá músum við útsetningu sem jafngildir útsetningu fyrir menn og geta haft áhrif á klínískan notkun voru breytingar á lifur sem benda til þess að það sé að því er varðar aðlagaða svörun eins og aukin þyngd og þrýsting í miðlókum, fituskerðingu og aukin lifrarensím í blóði.
**After:** Aukaverkanir sem ekki komu fram í klínískum rannsóknum en komu fram hjá rottum og mjög minni leyti hjá músum við útsetningu sem var svipuð útsetningu fyrir menn og hafa hugsanleg áhrif á klíníska notkun voru breytingar á lifur, sem benda til þess að það sé þrálátur svörun eins og aukin þyngd og þrýsting í miðlópu, fitusvæfni og aukin lifrarensím í blóði.

</details>

<details><summary>Anchor: p13official21:test:ema:1968</summary>

**Source:** In a post-hoc analysis, those patients with a baseline MRI with at least one Gd-enhancing lesion and nine T2 lesions had a two-year risk of suffering a second event of 56% in the placebo group and 21% in the AVONEX treatment group.
**Reference:** Í undanfaraorsaka greiningu þeirra sjúklinga sem voru með MRI grunnlínu með eina Gd-aukna skemmd og níu T2 skemmdir voru 56 % í lyfleysu hópnum og 21 % í AVONEX meðferðar hópnum í hættu að verða fyrir öðru kasti á tveggja ára tímabili.
**Before:** Í eftirgreindri greiningu voru sjúklingar með Gd-aukið magaheilkenni á grunngreiningu með MRI og einn eða fleiri magaheilkenni og níu T2 heilkenni í hliðstæðum 56% á tvö ár á líkurinni að fá annan sýkingu í lyfleysugruppanum og 21% í AVONEX meðferðarhópnum.
**After:** Í afturhópa greiningu var hættan á að þessir sjúklingar fengið annan áfall í tvær ár 56% í lyfleysugruppi og 21% í AVONEX meðferðarhópnum.

</details>

<details><summary>Anchor: p13official21:test:ema:129</summary>

**Source:** Clinical studies have demonstrated that ProQuad can be given simultaneously (but at separate injection sites) with Prevenar and/or hepatitis A vaccine, or with monovalent or combination vaccines comprised of diphtheria, tetanus, acellular pertussis, Haemophilus influenzae type b, inactivated poliomyelitis, or hepatitis B antigen.
**Reference:** Klínískar rannsóknir hafa sýnt fram á að hægt er að gefa ProQuad á sama tíma (en á öðrum stungu- stað) og Prevenar og/eða lifrarbólgu A bóluefni eða með eingildu eða samsettum bóluefnum með barnaveiki, stífkrampa, frumulausan kíghósta, Haemophilus influenzae af gerð b, deyddum mænu- sóttar eða lifrarbólgu B mótefnavökum.
**Before:** Klínískar rannsóknir hafa sýnt fram á að ProQuad má gefa samhliða (en í mismunandi stungustöðum) með Prevenar og/eða lifrarbóluefni gegn lifrarbólgu A eða einstök eða samsetta bóluefni sem innihalda dýpkransa, tétanus, ófrumna kútusótt, Haemophilus influenzae tegund b, óvirkjaða mænirétta eða lifrarbólgu B mótefni.
**After:** Klínískar rannsóknir hafa sýnt fram á að ProQuad má gefa samhliða (en í mismunandi stungustaðum) með Prevenar og/eða bóluefni gegn lifrarbólgu A eða einstökum eða samsetnum bóluefnum sem innihalda dópkerfisbólgu, tétansúsbólgu, ófrumku kíghálsareykingu, Haemophilus influenzae tegund b, óvirkri mænusótt eða lifrarbólgu B mótefninu.

</details>

<details><summary>Anchor: p13official21:test:ema:2253</summary>

**Source:** In a post-hoc analysis, lower mortality was observed in the lenalidomide/low dose dexamethasone arm 6.8% (15/220) compared to the lenalidomide/standard dose dexamethasone arm 19.3% (43/223), in the newly diagnosed multiple myeloma patient population, with a median follow up of 72.3 weeks.
**Reference:** Í greiningu sem var gerð eftir á, kom fram lægri dánartíðni í arminum sem fékk lenalídómíð/lágskammta dexametasón 6,8% (15/220) samanborið við arminn sem fékk lenalídómíð/staðlaðan skammt af dexametasóni 19,3% (43/223) í sjúklingahópnum sem var með nýlega greint mergæxli og var miðgildi eftirfylgni 72,3 vikur.
**Before:** Í eftirgreindri greiningu kom fram lægra dánarhlutfall í lenalídómíð/ lágum skammti dexametasón hópnum 6,8% (15/220) samanborið við lenalídómíð/venjulega skammti dexametasón hópinn 19,3% (43/223) hjá sjúklingum með fjölbreyttur mýléma sem höfðu nýlega verið greint fyrir, með miðgildi eftirfylgni 72,3 vikur.
**After:** Í afturgreindri greiningu kom fram lægra dánartíðni í lenalídómíð/dúm skammti dexametasóni hópnum 6,8% (15/220) samanborið við lenalídómíð/venjulegt skammti dexametasóni hópinn 19,3% (43/223) hjá sjúklingum með fjölbreytt mænusótt sem var nýttaðir á meðferð og fylgst var með þeim í miðgildi 72,3 vikna fresti.

</details>

<details><summary>Anchor: p13official21:test:ema:1190</summary>

**Source:** In these cases it is therefore recommended that the Zonegran total dose should be rounded up or down to the nearest available dose that can be achieved with commercially available capsule strengths of Zonegran (25 mg, 50 mg and 100 mg).
**Reference:** Í slíkum tilfellum er því mælt með því að heildarskammturinn af Zonegran sé minnkaður eða stækkaður í næsta skammt sem hægt er að gefa með hylkjum af þeim styrkleika af Zonegran sem fáanleg eru (25 mg, 50 mg og 100 mg).
**Before:** Í þessum tilfellum er því mælt með að hefja eða lækka heildarskammtinn af Zonegran upp eða niður í næstu fáanlegri skammti sem getur verið náð með lyfjagigtum af styrkuríki Zonegran (25 mg, 50 mg og 100 mg).
**After:** Í þessum tilvikum er því ráðlagt að ná næstu fyrirbæri skammti sem er að gera með Zonegran með því að kviða upp eða niður, sem er aðgengilegt og er að gera með lyfjafræðilegum styrk í hylkjum af Zonegran (25 mg, 50 mg og 100 mg).

</details>

<details><summary>Anchor: p13official21:test:ema:1404</summary>

**Source:** Based on more than 200 mother/child pairs treated for HIV, serum concentrations of lamivudine in breastfed infants of mothers treated for HIV are very low (less than 4% of maternal serum concentrations) and progressively decrease to undetectable levels when breastfed infants reach 24 weeks of age.
**Reference:** Samkvæmt niðurstöðum frá yfir 200 pörum móður/barns í meðferð við HIV, er þéttni lamivúdíns í sermi ungbarna á brjósti hjá mæðrum í HIV-meðferð mjög lág (innan við 4% af þéttni í sermi móður) og lækka jafnt og þétt niður fyrir greinanleg mörk þegar brjóstmylkingarnir ná 24 vikna aldri.
**Before:** Byggt á meira en 200 móður/börn par sem fengu meðferð gegn HIV, eru þéttni lamivúdíns í sermi hjá barnum sem fá brjóstagjöf, hjá móður sem færð meðferð gegn HIV, mjög lág (minna en 4% af þéttni móðurserms) og minnka áfram til ógreinanlegu stigi þegar barn sem fá brjóstagjöf ná 24 vikna aldri.
**After:** Byggt á meira en 200 móður/börn par sem fengu meðferð gegn HIV, eru þéttni lamivúdíns í sermi hjá barnum sem fá brjóstagjöf mjög lág (minna en 4% af þéttni móðursermis) og minnka sjaldnar til ógreinanlega þéttni þegar barn er 24 vikna.

</details>

<details><summary>Anchor: p13official21:test:ema:3031</summary>

**Source:** Due to the potential for 2 to 4 fold higher plasma levels of cinacalcet in patients with moderate to severe hepatic impairment (Child-Pugh classification), cinacalcet should be used with caution in these patients and treatment should be closely monitored (see sections 4.2 and 5.2).
**Reference:** Vegna þess að plasmaþéttni cinacalcets getur hækkað 2 til 4 falt hjá sjúklingum með í meðallagi til alvarlega skerta lifrarstarfsemi (Child-Pugh flokkun) skal nota cinacalcet með varúð hjá þessum sjúklingum og fylgjast skal náið með meðferðinni (sjá kafla 4.2 og 5.2).
**Before:** Vegna mögulegrar hækkaðrar plasmagildi af 2 til 4 faldi af cinacalceti hjá sjúklingum með miðlungs eða alvarlega skerta lifrarstarfsemi (Child-Pugh flokkun) skal gæta varúðar við notkun cinacalcets hjá þessum sjúklingum og fylgjast náið með meðferð (sjá kafla 4.2 og 5.2).
**After:** Vegna möguleika á 2 til 4 faldri hækkun plasmagilda cínakalcets hjá sjúklingum með miðlungs alvarlega til alvarlega skerta lifrarstarfsemi (Child-Pugh flokkun) skal gæta varúðar við notkun cínakalcets hjá þessum sjúklingum og eiga að fylgjast náið með meðferð (sjá kafla 4.2 og 5.2).

</details>

<details><summary>Anchor: p13official21:test:ema:2944</summary>

**Source:** Chemical, physical and microbiological in-use stability has been demonstrated for 28 days at 2-8°C. Once opened, the product may be stored for a maximum of 28 days at 2°C to 8°C. Other in-use storage times and conditions are the responsibility of the user.
**Reference:** Sýnt hefur verið fram á efnafræðilegan, eðlisfræðilegan og örverufræðilegan stöðugleika við notkun í 28 daga við 2-8°C. Eftir að penninn hefur verið notaður einu sinni, má nota hann í allt að 28 daga ef hann er geymdur við 2° til 8°C. Notkun og geymsla umfram þennan tíma eða við önnur geymsluskilyrði er á ábyrgð notanda.
**Before:** Einnig hefur verið sýnt fram á efnisfræðilega, eðlisfræðilega og líffræðilega stöðugleika í notkun í 28 daga við 2-8°C. Eftir að lyfið er opnað má geyma það í hámarksgildi 28 daga við 2°C til 8°C. Á öðrum gildaðum geymsluþolum og skilyrðum er ábyrgð notanda.
**After:** Einnig hefur verið sýnt fram á efnisfræðilega, eðlisfræðilega og örveruframleiðsluþollega stöðugleika í notkun í 28 daga við 2-8°C. Eftir að lyfið er opnað má geyma það í hámarkshraða 28 daga við 2°C til 8°C. Önnur geymslutíma og skilyrði fyrir geymslu í notkun falla undir ábyrgð notanda.

</details>

<details><summary>Anchor: p13official21:test:ema:1385</summary>

**Source:** Lynparza is indicated as monotherapy for the maintenance treatment of adult patients with platinum-sensitive relapsed BRCA-mutated (germline and/or somatic) high grade serous epithelial ovarian, fallopian tube, or primary peritoneal cancer who are in response (complete response or partial response) to platinum-based chemotherapy.
**Reference:** Lynparza er ætlað til einlyfjaviðhaldsmeðferðar hjá fullorðnum sjúklingum eftir bakslag platínunæms þekjufrumukrabbameins með stökkbreytt BRCA (kímlínu og/eða líkamsfrumu) með miklum vefjabreytingum (HGS [high grade serous]) í eggjastokkum, eggjaleiðara eða lífhimnu (frumkrabbamein) sem svara (algjör svörun eða svörun að hluta til) krabbameinslyfjameðferð sem byggist á platínu.
**Before:** Lynparza er ætlað til einlyfjameðferðar við viðhaldsmeðferð hjá fullorðnum sjúklingum með brusteyða (platinum-sensitive) BRCA-skerta (germlinngreindur og/eða líffæra) hægri stigs serusjámskipti í eggjastokkum, egg-veggum eða frumhöfn sem eru í svörun (fullanleg svörun eða hluta af svörun) við krabbameinslyfjameðferð á grundvelli platínums.
**After:** Lynparza er ætlað til einlyfjameðferðar við viðhaldsmeðferð hjá fullorðnum sjúklingum með brusteplatínunæmi sem hafa endurkomnu BRCA-skiltrúa (germlin- og/eða líffæra) kyrningafæð, kyrningahluta eða frumþekju í kyrningahluta sem eru með hópa (háttar stig) og svara (heildarsvörun eða hluta svörun) lyfjafræðilegri gegnplatíni meðferð.

</details>

<details><summary>Anchor: p13official21:test:ema:1916</summary>

**Source:** The clinically important adverse reactions associated with the use of thalidomide in combination with melphalan and prednisone or dexamethasone include: deep vein thrombosis and pulmonary embolism, peripheral neuropathy, severe skin reactions including Stevens Johnson Syndrome and toxic epidermal necrolysis, syncope, bradycardia, and dizziness (see sections 4.2, 4.4 and 4.5).
**Reference:** Klínískt mikilvægar aukaverkanir tengdar notkun talidomíðs samhliða melfalan og prednisóni eða dexametasón eru meðal annars: blóðsegamyndun í bláæðum og blóðrek í lungum, kvillar í úttaugakerfi, alvarleg viðbrögð í húð, þar með talið Stevens-Johnson heilkenni og Lyells heilkenni (drep í húðþekju), hægsláttur, stöðuháð blóðþrýstingsfall og svimi (sjá kafla 4.2, 4.4 og 4.5).
**Before:** Klínískt mikilvæg áhrif sem tengjast notkun thalidomids samhliða melphalan og prednisóni eða dexametasoni eru: djúpt blóðtungaæxli og lungnablokk, útbreiðslu í líkamansvæðum, alvarlegar húðviðbrögð, þar með talið Stevens-Johnson heilkenni og eiturverkanir í húð, skjálfti, hægur hjartsláttur og sundli (sjá kafla 4.2, 4.4 og 4.5).
**After:** Klínískt mikilvæg áhrif sem tengjast notkun thalidomíðs í samsettri meðferð með melphalan og prednisóni eða dexametasóni eru: segamyndun í djúpt bláæð og lungnablokk, útbrot í líffærum taugum, alvarlegar húðviðbrögð, þar með talið Stevens-Johnson heilkenni og eiturverkanir í húðþekju, sundl, hægur hjartsláttur og sundli (sjá kafla 4.2, 4.4 og 4.5).

</details>

<details><summary>Anchor: p13official21:test:ema:979</summary>

**Source:** Such reactions to insulin or to the excipients can cause large-scale skin reactions (rash and itching all over the body); severe swelling of skin or mucous membranes (angiooedema), shortness of breath, a fall in blood pressure with rapid heart beat and sweating.
**Reference:** Slíkt ofnæmi fyrir insúlíni eða hjálparefnunum getur valdið meiriháttar húðbreytingum (útbrot og kláði um allan líkamann), verulegri bólgu í húð eða slímhúð (ofsabjúgur), mæði, lækkuðum blóðþrýstingi með hröðum hjartslætti og aukinni svitamyndun.
**Before:** Slíkar viðbrögð við insúlíni eða hjálparefninu geta valdið stórum húðviðbrögðum (útbrot og kláði alls á líkamanum); alvarlegum bólgu í húð eða slímhúð (blæðingar), mörkuðu öndun, lækkaðu blóðþrýstingi með hröðum hjartsláttur og svitandi.
**After:** Slíkar viðbrögð við insúlíni eða hjálparefninu geta valdið alvarlegum húðviðbrögðum (útbrot og kláði á öllu líkamanum) sem eru meðalvægar bólur í húð eða slímhúð (ofnæmi), mæði, brjóstagjöf, lækkað blóðþrýstingur með hratt hjartsláttur og svitandi.

</details>

<details><summary>Anchor: p13official21:test:ema:2183</summary>

**Source:** For intravenous use, infusion systems with Actrapid at concentrations from 0.05 international unit/ml to 1.0 international unit/ml human insulin in the infusion fluids 0.9% sodium chloride, 5% dextrose and 10% dextrose inclusive 40 mmol/l potassium chloride using polypropylene infusion bags, are stable at room temperature for 24 hours.
**Reference:** Fyrir gjöf í bláæð er Actrapid stöðugt við stofuhita í 24 klst., í styrkleikum 0,05 alþjóðlegar einingar/ml til 1,0 alþjóðlegar einingar/ml af mannainsúlíni í eftirfarandi innrennslisvökvum; 0,9% natríumklóríði, 5% glúkósa og 10% glúkósa með 40 mmól/l af kalíumklóríði, þegar notaðaðir eru pólýprópýlen innrennslispokar.
**Before:** Fyrir notkun í bláæð, innrennslisstöfun með Actrapid á styrkleikum frá 0,05 evrópskum einingum/ml til 1,0 evrópskum einingum/ml af mannainsúlíni í innrennslisflókinu 0,9% natríumklóríð, 5% dextros og 10% dextros, þar með talið 40 mmól/l kloríðkorni, með pólýprópýlen innrennslispokum, eru stöðugar við stofuhita í 24 klukkustundir.
**After:** Fyrir notkun í æð, innrennslisverkjur með Actrapid á styrkleikum frá 0,05 evrópskum einingum/ml til 1,0 evrópskum einingum/ml af mannainsúlíni í innrennslistu 0,9% natríumklóríð, 5% dextrosa og 10% dextrosa, þar með talið 40 mmól/l kloríðkloríð, sem eru í pólýprópýlen innrennslispoka, eru stöðug við stofuhita í 24 klst.

</details>

<details><summary>Anchor: p13official21:test:ema:437</summary>

**Source:** Lenvatinib should not be started in patients with fistula to avoid worsening and lenvatinib should be permanently discontinued in patients with oesophageal or tracheobronchial tract involvement and any Grade 4 fistula (see section 4.2); limited information is available on the use of dose interruption or reduction in management of other events, but worsening was observed in some cases and caution should be taken.
**Reference:** Ekki skal hefja meðferð með lenvatinibi hjá sjúklingum með fistil til að forðast versnun og hætta skal meðferð með lenvatinibi til frambúðar hjá sjúklingum þar sem vélinda eða barki og berkjur eiga í hlut og í tilfellum allra 4. stigs fistla (sjá kafla 4.2), takmarkaðar upplýsingar liggja fyrir um skammtahlé eða skammtaminnkun við meðferð á öðrum atvikum, en versnun varð í sumum tilvikum og því skal gæta varúðar.
**Before:** Ekki skal hefja meðferð með lenvatinibi hjá sjúklingum með glæi til að koma í veg fyrir versnun og hætta skal meðferð með lenvatinibi á lengi hjá sjúklingum með eitilhlið í lungnabrunni eða öxl eða þrýstihlið og allar 4. stigs glæi (sjá kafla 4.2); takmörkuð upplýsingar liggja fyrir um notkun skiptis á skammti eða minnkaðs skammts við meðferð annarra tilvikanna en þegar versnun kom fram í sumum tilfellum skal gæta varúðar.
**After:** Ekki skal hefja meðferð með lenvatinibi hjá sjúklingum með þræða til að koma í veg fyrir versnun og hætta skal meðferð með lenvatinibi hjá sjúklingum með eitilhneigingu í lálíu eða öxl- eða lungnabrotni og allra 4. stigs þræða (sjá kafla 4.2); takmarkaðar upplýsingar liggja fyrir um notkun skiptis á skammti eða minnkaða skammts við meðferð annarra ástanda en það hefur komið fram aukin ástand í sumum tilvikum og því skal gæta varúðar.

</details>

<details><summary>Anchor: p13official21:test:ema:1366</summary>

**Source:** The risk may increase in case of treatment combination with other medicinal products that may also provoke hyperkalaemia (salt substitutes containing potassium, potassium-sparing diuretics, ACE inhibitors, angiotensin II receptor antagonists, non steroidal anti- inflammatory medicinal products (NSAIDs, including selective COX-2 inhibitors), heparin, immunosuppressives (cyclosporin or tacrolimus), and trimethoprim).
**Reference:** Aukin hætta getur verið við samhliða meðferð með öðrum lyfjum sem einnig geta valdið blóðkalíumhækkun (saltuppbót sem inniheldur kalíum, kalíumsparandi þvagræsilyf, ACE-hemlar, angíótensín II viðtakablokkar, bólgueyðandi gigtarlyf (NSAID, þar með talið sértækir COX-2 hemlar), heparín, ónæmisbælandi lyf (ciclosporín eða takrólímus) og trímetóprím.
**Before:** Hætta getur aukist ef meðferð er gefin samhliða öðrum lyfjum sem geta líka valdið kalsíumhækkun (saltbúnaður sem inniheldur kalíum, kalíumhaldandi þvagræsilyf, ACE-hemlar, angiotensín II viðtakahemlar, bólgueyðandi lyf (NSAID, þar með talið sérstök COX-2 hemlar), heparín og ónæmisbælandi lyf (cyclosporin eða tacrolimus) og trimetóprími).
**After:** Hætta getur aukist ef meðferð er gefin samhliða öðrum lyfjum sem geta líka valdið kalsíumhækkun (saltsetningar sem innihalda kalíum, kalíuspillaðir þvagræsilyf, ACE-hemlar, angiotensin II viðtakahemlar, bólgueyðandi lyf (NSAID, þar með talið sérstök COX-2 hemlar), heparín og ónæmisbælandi lyf (cyclosporin eða tacrolimus) og trimetóprími).

</details>

<details><summary>Anchor: p13official21:test:ema:1364</summary>

**Source:** The efficacy and safety of Xultophy (once-daily) compared to unchanged GLP-1 receptor agonist therapy (dosed according to label), were studied in a 26-weeks randomised, open-label, treat-to-target trial in patients with type 2 diabetes mellitus inadequately controlled on a GLP-1 receptor agonist and metformin alone (74.2%) or in combination with pioglitazone (2.5%), sulphonylurea (21.2%) or both (2.1%).
**Reference:** Verkun og öryggi Xultophy (einu sinni á sólarhring) í samanburði við óbreytta meðferð með GLP-1 viðtakaörva (skammtar samkvæmt fyrirmælum), voru rannsökuð í 26 vikna slembiraðaðri, opinni, meðferðarmiðaðri rannsókn á sjúklingum með sykursýki af tegund 2, sem ekki er stjórnað á fullnægjandi hátt með GLP-1 viðtakaörva og metformíni einu sér (74,2%) eða í samsettri meðferð með píóglítazóni (2,5%), súlfónýlúrealyfi (21,2%) eða báðum (2,1%).
**Before:** Verkun og öryggi Xultophy (einu sinni á dag) var rannsökuð samanborið við óbreytt GLP-1 viðtakahemillæka meðferð (skammtar samkvæmt merkjum) í 26 vikna slembiraðaðri, opinni, meðferð til markstigs rannsókn hjá sjúklingum með sykursýki af tegund 2 sem ekki höfðu náð nægilega samræmi við meðferð með GLP-1 viðtakahemillæku og metformíni einu sér eða í samsettri meðferð með pioglitazóni (2,5%), súlfónýlúrealyfi (21,2%) eða bæði (2,1%).
**After:** Verkun og öryggi Xultophy (einu sinni á dag) var borið saman við óbreytt GLP-1 viðtakaheilkenni meðferð (skammtar eftir merkingum) í 26 vikna slembiraðaðri, opinni, rannsókn þar sem meðferð var hafin til markmiða hjá sjúklingum með sykursýki af tegund 2 án fullnægjandi stjórnunar með GLP-1 viðtakaheilkenni og metformíni einu sér (74,2%) eða í samsettri meðferð með pioglitazóni (2,5%), súlfónýlúrealyfi (21,2%) eða bæði (2,1%).

</details>

<details><summary>Anchor: p13official21:test:ema:1905</summary>

**Source:** In a pooled analysis of the data from 13 studies, the overall incidences of adverse events, serious adverse events and adverse events resulting in discontinuation of therapy were comparable in patients treated with 25 mg alogliptin, 12.5 mg alogliptin, active-control or placebo.
**Reference:** Í samantektargreiningu á gögnum úr 13 rannsóknum var heildartíðni aukaverkana, alvarlegar aukaverkanir og aukaverkanir sem leiddu til meðferðarrofs, sambærileg hjá sjúklingum sem fengu 25 mg af alógliptíni, 12,5 mg af alógliptíni, virkum samanburðarhóp og þeim sem voru á lyfleysu.
**Before:** Í samanburðarrannsókn á gögnum frá 13 rannsóknum var heildartíðni aukaverkana, alvarlegra aukaverkana og aukaverkana sem leiddi til þess að meðferð var hætt jafngild í sjúklingum sem fengu 25 mg af aloglíptini, 12,5 mg af aloglíptini, virka samanburðarlyf eða lyfleysu.
**After:** Í samantektar greiningu á gögnum frá 13 rannsóknum var heildartíðni aukaverkana, alvarlegra aukaverkana og aukaverkana sem leiddi til þess að meðferð var hætt jafngild í sjúklingum sem fengu 25 mg af aloglíptini, 12,5 mg af aloglíptini, virka samanburðarlyf eða lyfleysu.

</details>

<details><summary>Anchor: p13official21:test:eso:503</summary>

**Source:** The planets in the habitable zone and those closer to the star are expected to always have the same side facing the star, so that their day and year will be the same lengths, with one side in perpetual sunshine and the other always night.
**Reference:** Talið er að reikistjörnurnar í lífbeltinu og þær sem eru næstar stjörnunni snúi alltaf sömu hlið sinni að stjörnunni þannig að dagur og ár eru jafnlöng og önnur hliðin er alltaf í sólskini en hin í eilífu myrkri.
**Before:** Reikistjörnurnar í búsetustað og þær sem eru nálægri stjörnunni eru búst á sama hliði í samræmi við stjörnuna svo að dagur og ár þeirra séu jafnvægar, með einhverja hliðinni í sólgeymi og hinna hliðinni alltaf í nótt.
**After:** Hjá reyndar er búist við að reikistjörnurnar í búsetustað og þær sem eru nærri stjörnunni hafi alltaf sama hlið á sér til stjarnunnar svo að dagur og ár þeirra séu jafn lengdar, með einhverja hliðinni í sundl og hinu annarri alltaf nætur.

</details>

<details><summary>Anchor: p13official21:test:eso:918</summary>

**Source:** "With such short orbital periods, the planets are between 20 and 100 times closer to their star than the Earth to the Sun. The structure of this planetary system is much more similar in scale to the system of Jupiters moons than to that of the Solar System," explains Michaël Gillon.
**Reference:** „Umferðartímarnir eru svo stuttir að reikistjörnurnar eru 20 til 100 sinnum nær móðurstjörnunni en Jörðin frá sólinni. Uppbygging þessa sólkerfis svipar því meira til Júpíters og tungla hans en sólkerfinu okkar,“ segir Michaël Gillon.
**Before:** „Með slæma umferðarfráhringum eru plönturnir í 20 til 100 sinnum nálægri fjarlægð frá stjörnunni en jörðin frá sólinni,“ segir Michaël Gillon. „Staðsetningur þessarar reikistjarna er mjög lítiltar sambærilegur við reikistjarnanir Júpíters en reikistjarnanir á sólkerfinu,“ segir Michaël Gillon.
**After:** „Með slíkum stuttum hringi er fyrirbærið á milli stjarna og jörðs um 20 til 100 sinnum nærri stjörnunni en Júpíterhjúpinarnir eru í námi við Júpíter og Júpíterhjúpinarnir eru lítilvillilega svipuðar við Júpíter og Júpíterhjúpinarnir eru lítilvillilega svipuðar við sólkerfinu,“ segir Michaël Gillon.

</details>

<details><summary>Anchor: p13official21:test:eso:873</summary>

**Source:** Several theories have been proposed, and, while some of these have already been ruled out, it is possible that the effects are caused by magnetic field variations in the larger of the two stars, somewhat similar to the smaller changes seen in the Sun.
**Reference:** Nokkrar tilgátur hafa verið settar fram og þótt sumar hafi þegar verið útilokaðar er mögulegt að áhrifin séu af völdum breytinga á segulsviði stærri stjörnunnar, svipað þeim segulsviðsbreytingum sem verða á sólinni og eru nokkuð umfangsminni.
**Before:** Fyrir hendi hefur verið lagt fram nokkrar lýsingar og þótt sumar þeirra hafi nú þegar verið fjarlægðar er mögulegt að áhrifin séu af völdum breyttinga á magnæði stjarnaðs, sem er stærri af tveimurum, jafngildi smára breytinganna sem sjón varðandi sólin.
**After:** Framhaldi hafa verið sett fram nokkrar lýsingar og þótt sumar þeirra hafi þegar verið fyrirbiðjaðar er mögulegt að áhrifin séu af völdum breyttinga á vetrarbrautum í stærri stjörnunni, sem líkist örlítið meira breytingum á stjörnunni í sólinni.

</details>

<details><summary>Anchor: p13official21:test:eso:1138</summary>

**Source:** “Terrestrial planets similar to our Earth are obvious targets for the search for life outside the Solar System, while comets are suspected to have played an important role in the appearance and development of life on our planet,” adds his colleague Emmanuël Jehin, who leads the cometary part of the project.
**Reference:** „Bergreikistjörnur sem líkjast jörðinni eru augljós skotmörk fyrir leitina að lífi utan sólkerfisins en halastjörnurnar eru taldar hafa leikið mikilvægt hlutverk í uppruna og þróun lífs á reikistjörnunni okkar“ bætir Emmanuël Jehin við en hann leiðir halastjörnuþátt verkefnisins.
**Before:** „Jafnframt er greinileg markmiðið við leitina á lífi utan sólarkerfisins, en fyrirhugað er að reykjum hefur verið mikilvægt þátt í uppbótar og þróun lífs á okkur jörðinni,“ sagði Emmanuël Jehin, samstarfsmaður hans, sem stjórnaður er meðferðarinnar sem gerir um reykjum.
**After:** „Jafnframt er greinileg markmiðið við leitir lifur utan sólkerfisins, en komar eru hugtakandi til að hafa haft mikilvæga þátt í uppbrot og þróun lífs á okkur jörðinni,“ bætir Emmanuël Jehin samstarfsmaðurinn um það.

</details>

<details><summary>Anchor: p13official21:test:eso:611</summary>

**Source:** “With Mars losing that much water, the planet was very likely wet for a longer period of time than previously thought, suggesting the planet might have been habitable for longer,” said Michael Mumma, a senior scientist at Goddard and the second author on the paper.
**Reference:** „Þar sem Mars hefur glatað svo miklu vatni var reikistjarnan líklega blaut í lengri tíma en áður var talið, sem bendir til að Mars gæti hafa verið lífvænleg í lengri tíma,“ sagði Michael Mumma, vísindamaður við Goddard og annar höfundur greinarinnar.
**Before:** „Þegar Mars missti svona mikið vatn var jörðin líklega vökvað lengur en áður hefur verið talið og það bendir til þess að hún hafi verið fyrirhuguð fyrir lengri tíma,“ sagði Michael Mumma, hæsta vísindamannur í Goddard og annar aðalhöfundur greinarinnar.
**After:** „Þegar Mars tapaði svona mikið af vatni var reikistjarnan líklega vökvað lengur en áður hafi verið talið og það bendir til þess að hún gæti verið búsettur fyrir lengri tíma en áður hefur verið talið,“ sagði Michael Mumma, hópi sánni vísindamanna við Goddard og annar aðalhöfundur greinarinnar.

</details>

<details><summary>Anchor: p13official21:test:eso:165</summary>

**Source:** "The detailed analysis of the faint light from two of the most distant galaxies we found suggests that the very first generation of stars may have contributed to the energy output observed," says Eros Vanzella of the INAF Trieste Observatory, a member of the research team.
**Reference:** „Við grannskoðuðum ljós tveggja fjarlægustu vetrarbrautanna sem við fundum og bendir sú athugun okkar til að fyrstu kynslóðir stjarna gætu hafa lagt til orkuútgeisluna sem við sáum“ segir Eros Vanzella við stjörnustöðina í Trieste og meðlimur í rannsóknarhópnum.
**Before:** „Nákvæmri greiningin á ljósið frá tveimur fjarlægustu vetrarbrautum sem við fundum hefur leitt til þess að fyrsta stjörnufræðilegur yfirfallið hafi hafa þátt í orkuúrræði sem við sýndum,“ sagði Eros Vanzella frá INAF Trieste stjörnustöðinni, aðildari rannsóknartækisins.
**After:** „Mikilvægri greining á ljósið frá tveimur fjarlægustu vetrarbrautum sem við fundum sýnir að fyrsta stjörnufræðingarnir gætu hafa veitt það til að því er varðar orkuútgjöfina sem við sjáum,“ sagði Eros Vanzella, hjá INAF Trieste stjörnustöðinni og aðildari rannsóknartækisins.

</details>

<details><summary>Anchor: p13official21:test:eso:80</summary>

**Source:** But the new study using the VLT has found that much of the stars energy is being absorbed and scattered by dust clouds before it gets to Earth - it is actually more luminous than previously thought and among the brightest stars known.
**Reference:** Nýja rannsóknin með VLT hefur hins vegar sýnt fram á að rykský gleypa og dreifa stórum hluta orkunnar sem stjarnan gefur frá sér áður en hún berst til jarðar - hún er því í raun miklu bjartari en áður var talið og er meðal skærustu stjarna sem vitað er um.
**Before:** Nýtt rannsókn með VLT hefur fundið að mikið af orku stjarna er tekið upp og dreifin af rykskýum áður en það kemur til jörðar - það er í raun bjartari en áður var talið og á sér stað eins birtastu stjarnan sem vitað er um.
**After:** En nýja rannsóknin með VLT hefur komið í ljós að miklu af orku stjarna er tekið upp og dreifin af rykskýum áður en hún kemur til Jörðar - hún er í raun bjartari en áður var talið og er einnig bjartari en flestu stjörnurnar sem vitað er um.

</details>

<details><summary>Anchor: p13official21:test:eso:1069</summary>

**Source:** By using the SPHERE instrument on ESOs Very Large Telescope (VLT) - one of the most powerful planet-hunting instruments in existence - the international team has made the first robust detection of a young planet, named PDS 70b, cleaving a path through the planet-forming material surrounding the young star.
**Reference:** Með SPHERE mælitækinu á Very Large Telescope (VLT) ESO - sem er eitt öflugasta reikistjörnuleitartæki heims - sáu stjörnufræðingarnir hvernig reikistjarnan unga, PDS 70b, plægir sig í gegnum efnisskífuna sem umlykur stjörnuna.
**Before:** Með notkun SPHERE mælitækisins á Very Large Telescope (VLT) ESO - einni af öflugustu mælitækjum til að leita fyrir reikistjörnur - hefur alþjóðlegur hópurinn gert fyrstu rauða greiningu á unga reikistjörnu, nafnd PDS 70b, sem hefur komað í gegnum umhverfi sem myndar reikistjörnur.
**After:** Með notkun SPHERE mælitækisins á Very Large Telescope (VLT) ESO - einni af öflugustu mælitækjum til að leita fyrir reikistjörnum - hefur alþjóðlegur hópurinn gert fyrstu rannsókn á ungar reikistjörnunni, nánu sem PDS 70b, og hafnaði leið yfir efnið sem myndast í kringum unga stjörnuna.

</details>

<details><summary>Anchor: p13official21:test:eso:226</summary>

**Source:** Stefano Bagnulo (Armagh Observatory, Northern Ireland, United Kingdom) explains the advantages: "The light from a distant exoplanet is overwhelmed by the glare of the host star, so its very difficult to analyse - a bit like trying to study a grain of dust beside a powerful light bulb.
**Reference:** Stefano Bagnulo (Armagh stjörnustöðinni á Norður Írlandi) útskýrir kosti þessarar aðferðar: „Ljós frá fjarlægri fjarreikistjörnu hverfur í birtu móðurstjörnunnar svo mjög erfitt er að mæla það - ekki ósvipað því að rannsaka rykkorn við hlið mjög bjartrar ljósaperu.
**Before:** Stefano Bagnulo (Armagh Observatory, Norður-Írland, Breska konungsríkið) útskýrir ávinningarnar: „Ljósið frá fjarlægri jörðuverja er undanþegið af glárastjarna, svo það er mjög erfitt að greina - einnig eins og að reyna að rannsaka stórskyni dösum í burtu öflugu ljósboltu.
**After:** Stefano Bagnulo (Armagh Observatory, Norður-Írland, Breska konungsríkið) útskýrir hversu ávinningar eru: „Ljósi frá fjarlægri rúmreikistjörnu er undanþegið af glárastjörnunnar sem hún er í og það er mjög erfitt að greina - einhvers öfugt eins og að reyna að rannsaka ryk í ljósbólgu sem er nálægt.

</details>

<details><summary>Anchor: p13official21:test:eso:329</summary>

**Source:** The experiment marks the first time that APEX has taken part in VLBI observations, and is the culmination of three years hard work at APEXs high altitude site on the 5000-metre plateau of Chajnantor in the Chilean Andes, where the atmospheric pressure is only about half that at sea level.
**Reference:** Með tilrauninni er APEX í fyrsta sinn notaður í VLBI mælingum og er hápunkturinn á þriggja ára erfiðisvinnu við APEX sjónaukann sem er í 5.000 metra hæð yfir sjávarmáli á Chajnantor sléttunni í Andesfjöllum Chile, þar sem loftþrýstingur er helmingi minni en við sjávarmál.
**Before:** Framkvæmdin er fyrsta sinn sem APEX hefur taka þátt í VLBI mælingum og endurtekið þriggja ára vinnu á hægri stöðu APEX á 5000 metra hæði Chajnantors á Andes fjallunni í Chile, þar sem lofthvítur er aðeins um hálftil þess sem á hafihæði.
**After:** Sjálfur er það fyrsta sinn sem APEX hefur tekið þátt í VLBI mælingum og er endapunkti þriggja ára vinnu á hægri stöð við APEX á 5000 metrar hæðarstöðinu í Chileands Endabergum þar sem lofthvarf er aðeins um hálft því sem á sjóhæði.

</details>

<details><summary>Anchor: p13official21:test:eso:63</summary>

**Source:** “Studying afterglows is vital to further our understanding of the objects that become gamma-ray bursts and what they tell us about star formation in the early Universe,” says the studys lead author Jochen Greiner from the Max-Planck Institute for Extraterrestrial Physics in Garching bei München, Germany.
**Reference:** „Það er nauðsynlegt að rannsaka glæður blossanna svo auka megi skilning okkar á þeim fyrirbærum sem mynda gammablossa og hvað þau segja okkur um myndun stjarna snemma í sögu alheimsins“ segir Jochen Greiner, aðalhöfundur greinar um rannsóknina, og stjarneðlisfræðingur við Max-Planck-Institut für extraterrestrische Physik í Garching við München í Þýskalandi.
**Before:** „Mælingar á eftirglæðum eru mikilvægar til þess að nýja okkar skilningu um fyrirbæri sem verða gammönu röntgengljósa og hvað þeir segja okkur um stjörnumyndun í fyrsta alheiminu,“ sagði Jochen Greiner, leiðsögnarréttari greinar um rannsóknina frá Max-Planck stofnuninni fyrir geimfræði í Garching í Þeistigum í Þýskalandi.
**After:** „Við rannsóknina á eftirglæði er nauðsynlegt til að ná frekari skilningu á fyrirbæri sem verður gammölslos og hvað þeir segja okkur um stjörnumyndun í syfulegu alheiminn,“ sagði Jochen Greiner, aðalhöfundur rannsóknarinnar við Max-Planck Institute for Extraterrestrial Physics í Garching bei München í Þýskalandi.

</details>

<details><summary>Anchor: p13official21:test:eso:908</summary>

**Source:** This bridge, which has not been seen before (and is too faint to show up in this picture), is somewhat bluer than either galaxy, indicating that it consists of stars created in gas that was drawn away from NGC 1387 by the gravitational pull of NGC 1399.
**Reference:** Þessi brú hafði ekki sést áður (og er of dauf til að koma fram á myndinni) en hún er nokkuð blárri en hin vetrarbrautin sem bendir til þess að hún samanstandi af stjörnum sem mynduðust úr gasi sem NGC 1399 hrifsaði úr NGC 1387.
**Before:** Þessi brú, sem hefur ekki séð áður (og er of ljósgæf til að sýna í myndinni) er einhverskju blárri en annar galdrar, sem benda til þess að hún er úr stjörnum sem eru myndar úr gasi sem var dragað út frá NGC 1387 af gildislagi NGC 1399.
**After:** Þessi brú, sem hefur ekki séð áður og er of ljósgæf til að sjást í þessari mynd, er einhverslárörvarrúmlegri en annar galdrarinnar, sem benda til þess að hún samanstendur af stjörnum sem eru búin til úr gass sem var dragað frá NGC 1387 með gegnþrýstingu NGC 1399.

</details>

<details><summary>Anchor: p13official21:test:eso:179</summary>

**Source:** These violent explosions rip through the molecular gas clouds in their immediate surroundings, but after the shockwaves have travelled more than about ten light-years they are weaker, and may instead compress clouds that are a little further away, triggering the formation of new generations of stars.
**Reference:** Höggbylgjur þessara orkuríku sprenginga tæta sundur sameindagasskýin í kring en eftir að þær hafa ferðast meira en tíu ljósár eða svo, hafa þær veikst en geta þjappað fjarlægari skýjum saman og þannig hrundið af stað myndun nýrra kynslóða stjarna.
**Before:** Þessi rauðar sprengingar skipta um milli líkamsgasvefnanna í nálægum umhverfi þeirra en eftir að skjálftan hefur farið meira en um tíu ljósára er þær vægar og geta þó styrkt það úr því að þeim verði það hægra veður og myndi þau koma upp í nýjar ævihóp stjarna.
**After:** Þessi öflugir sprengingar rífa í gegnum líkamlega gasský í náttúrunni þeirra en eftir að skjálftan hefur farið meira en um tíu ljósára er þær vægari og geta þó þegar komið úr þeim þokum sem eru stutt fjarlægri og hvetja upp nýjar ævihóp stjarna.

</details>

<details><summary>Anchor: p13official21:test:eso:538</summary>

**Source:** Previous observations had shown hotter, but much less dense, gas streaming away from NGC 253s star-forming regions, but alone this would have little, if any, impact on the fate of the galaxy and its ability to form future generations of stars.
**Reference:** Eldri rannsóknir höfðu sýnt að heitara en ekki jafn þétt gas streymdi burt frá stjörnumyndunarsvæðum NGC 253 en að það eitt hefði lítil eða ekki nokkur áhrif á örlög vetrarbrautarinnar og getu hennar til að mynda nýjar kynslóðir stjarna.
**Before:** Fyrri mælingar hafa sýnt að gasið var heitt en mjög þykktur, á umferð frá stjörnumyndunarsvæðum NGC 253, en einnig ekki hafi það miklu áhrif á lífinu stjörnuþyrpingarins og hæfni til að mynda fjölda nýja stjarna í framtíðinni.
**After:** Fyrri mælingar hafa sýnt hitari, en mjög þykkara, gasströngir sem fór út frá stjörnumyndunarsvæðum NGC 253, en einnig hefði það minna áhrif á lífinu gegn stjörnuþyrpingu og getu hennar til að mynda fjölda nýja stjarna í framtíðinni.

</details>

<details><summary>Anchor: p13official21:test:eso:436</summary>

**Source:** At the ceremony, which was broadcast live on the internet, representatives of ALMAs international partners were also present: ESOs Director General, Tim de Zeeuw, the Director of the USAs National Science Foundation Subra Suresh, and the Senior Vice Minister of Japans Ministry of Education, Culture, Sports, Science and Technology Teru Fukui, along with the Director of ALMA Thijs de Graauw.
**Reference:** Athöfnin var send út í beinni útsendingu á netinu en hana sóttu einnig fulltrúar aðildarríkja ALMA: Tim de Zeeuw, framkvæmdarstjóri ESO; Subra Suresh, forstjóri National Science Foundation í Bandaríkjunum; Teru Fukui aðstoðarráðherra mennta-, menningar-, íþrótta-, vísinda- og tæknimála í Japan og Thijs de Graauw, stjórnanda ALMA stjörnustöðvarinnar.
**Before:** Í því sérþýðisstefnumiði, sem var sendið á netinu, voru einnig til staðar fulltrúar ALMA alþjóðlega samstarfsins: Tim de Zeeuw, framkvæmdarstjóri ESO, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum
**After:** Í þessari íbúskerði, sem var útsendin á netinum, voru einnig fulltrúar ALMA alþjóðlega samstarfsins: Tim de Zeeuw, framkvæmdarstjóri ESO, Subra Suresh, framkvæmdarstjóri National Science Foundation í Bandaríkjunum, og Teru Fukui, hálfstjóri menntastofnunar Japans um náms- og menntakeppni, kennslu og tækni, ásamt Thijs de Graauw, framkvæmdarstjóri ALMA.

</details>

<details><summary>Anchor: p13official21:test:eso:881</summary>

**Source:** Using standard candles - such as the variable stars within IC 1613 and the less-common Type Ia supernova explosions, which can seen across far greater cosmic distances - astronomers have pieced together a cosmic distance ladder, reaching deeper and deeper into space.
**Reference:** Með hjálp staðalkerta eins og breytistjörnunum í IC 1613 og sprengistjörnum af gerð Ia, sem sjást úr mikilli fjarlægð í geimnum, hafa stjörnufræðingar smíðað fjarlægðarstiga sem nær lengra og lengra út í geiminn.
**Before:** Með stöðugum brennmyndum - svo sem breytilegir stjörnur í IC 1613 og minnkunarefni af tegund Ia sem sjást fyrir um langt yfir rými - hafa stjarnvísindamenn samið sérhæfðan stjörnuferil, sem náðir djúptari og djúptari í geimnum.
**After:** Með stöðugum brennslu - eins og breytilegir stjörnur í IC 1613 og minna alvarlegar af tegund Ia vanbrotar, sem sjást yfir miklu langt í geimnum - hafa stjarnvísindamenn samið sérhæfisliðun í geimnum, sem náir djúpt inn í geiminn.

</details>

<details><summary>Anchor: p13official21:test:eso:806</summary>

**Source:** “We found no evidence of these massive galaxies earlier than around one billion years after the Big Bang, so were confident that this is when the first massive galaxies must have formed,” concludes Henry Joy McCracken, a co-author on the paper.
**Reference:** „Við fundum engin merki um þessar efnismiklu vetrarbrautir fyrr en um einum milljarði ára eftir Miklahvell og erum því nokkuð viss um að þá hafi fyrstu efnismiklu vetrarbrautirnar myndast,“ segir Henry Joy McCracken, meðhöfundur greinarinnar.
**Before:** „Við fundum engin vísbending um þessi stóra vetrarbraut fyrir um einn milljón ár eftir stórmyndunina, svo varum við öryggi á að þetta sé það þegar fyrsta stóra vetrarbrautinu myndast,“ segir Henry Joy McCracken, meðhöfundur greinarinnar.
**After:** „Við fundum engin vísbending um þessi meginvirkar vetrarbrautir fyrr en í um bil milljarða ára eftir stórfjölgunina, svo varum við öryggi á að þetta sé það þegar fyrstu meginvirkar vetrarbrautirnar mynduðust,“ segir Henry Joy McCracken, meðhöfundur greinarinnar.

</details>

<details><summary>Anchor: p13official21:test:eso:512</summary>

**Source:** Another team member, Ana Duarte Cabral from the Laboratoire d'Astrophysique de Bordeaux, France, emphasises that "the ALMA observations reveal the spectacular details of the motions of the filamentary network of dust and gas, and show that a huge amount of gas is flowing into a central compact region".
**Reference:** Annar meðlimur í rannsóknarhópnum, Ana Duarte Cabral við Laboratoire dAstrophysique de Bordeaux í Frakklandi, undirstrikar að „mælingar ALMA leiða í ljós stórkostleg smáatriði í hreyfingu gas- og rykslæðanna og sýna að geysimikið magn af gasi streymir inn að þéttasta svæðinu í miðjunni.“.
**Before:** Önnur liðmanni í hópnum, Ana Duarte Cabral frá Laboratoire d'Astrophysique de Bordeaux í Frakklandi, kemur fram á það að „sýnir ALMA mælingarinnar skýrslu um snertingu vetrarbrauta og gasins í sér, og sýna að mikil magn af gasi flæðist inn í miðvettanum“.
**After:** Önnur liðamann í ALMA-gerðinni, Ana Duarte Cabral frá Laboratoire d'Astrophysique de Bordeaux í Frakklandi, kemur fram á það að „sýnir ALMA-mælingar sérstaklega skýrslu um hreyfingar dreifingarréttunar ryks og gasins og sýna að mikill magn gasa flæsti inn í miðlun þess komastu“.

</details>

<details><summary>Anchor: p13official21:test:eso:1100</summary>

**Source:** The combination of images taken by three exceptional telescopes, the ESO Very Large Telescope on Cerro Paranal , the MPG/ESO 2.2-metre telescope at ESOs La Silla observatory and the NASA/ESA Hubble Space Telescope, has allowed the stunning Jewel Box star cluster to be seen in a whole new light.
**Reference:** Myndir teknar með þremur sjónaukum, Very Large Telescope ESO á Cerro Paranal, 2,2 metra MPG/ESO sjónaukanum í La Silla stjörnustöðinni og Hubble geimsjónauka NASA og ESA, sýna hina glæsilegu lausþyrpingu Skartgripaskrínið í glænýju ljósi.
**Before:** Samsetningu myndirnar sem tveggja sérstaka sjónauka tóku, Very Large Telescope ESO á Cerro Paranal, MPG/ESO 2,2 metra sjónaukanum í La Silla stjörnustöð ESO og Hubble geimsjónaukanum NASA/ESA, hefur leitt til þess að sjúkla stjörnuþyrpingin séu horfin í nýju ljós.
**After:** Samsetning á myndum sem trefu þriggja sérstaka sjónauka, Very Large Telescope ESO í Cerro Paranal, MPG/ESO 2,2 metra sjónaukanum í La Silla stjörnustöð ESO og Hubble geimsjónaukanum NASA og ESA, hefur gert kleift að sjá stjörnumerkinu Jewel Box í nýju ljósi.

</details>

<details><summary>Anchor: p13official21:test:eso:1168</summary>

**Source:** R Coronae Australis itself is not visible to the unaided eye, but the tiny, tiara-shaped constellation in which it lies is easily spotted from dark sites due to its proximity on the sky to the larger constellation of Sagittarius and the rich star clouds towards the centre of our own galaxy, the Milky Way.
**Reference:** R Coronae Australis sést ekki með berum augum en litla kórónulaga stjörnumerkið sem hún tilheyrir sést auðveldlega við góðar aðstæður sökum nálægðar þess á himninum við stjörnumerkið Bogmanninn og stjörnumprýtt svæðið við miðju okkar Vetrarbrautar.
**Before:** R Coronae Australis sjálfur er ekki sýnt með óhjálpar augu en stuttur, tiara- skipti stjörnumerkin sem það er í er greint frá fyrir svartum staðsetningum vegna nálægri fjarlægðs á himninum við stærri stjörnumerkin Sígítrarinn og rólega stjörnumyndunum í miðju okkar vetrarbrauta, Vetrarbrautarinnar.
**After:** R Coronae Australis sjálfur er ekki sýnt á auga án hjálpar, en það litla, tiara-þekkt stjörnumerkin sem það er í er auðveldlega sýnt frá dökkum staðsetningu vegna nærþegna þess við stærri stjörnumerkin Sagittarius og þrýstingarstjörnum í miðju Vetrarbrautarinnar.

</details>

<details><summary>Anchor: p13official21:test:eso:1046</summary>

**Source:** “Measuring the flow of gas within a protoplanetary disc gives us much more certainty that planets are present around a young star,” said Christophe Pinte of Monash University in Australia and Institut de Planétologie et d'Astrophysique de Grenoble (Université de Grenoble-Alpes/CNRS) in France, and lead author on one of the two papers.
**Reference:** „Að mæla gasflæði í frumsólkerfisskífu gefur okkur miklu meiri vissu um að plánetur leynist í kringum stjörnuna ungu,“ sagði Christophe Pinte við Monash háskóla í Ástralíu og aðalhöfundur einnar af tveimur greinum.
**Before:** „Mælingar á flæði gasins í rigningardreifinni gefa okkur miklu meiri öryggi um að reikistjörnur séu í kringum ungri stjörnu,“ sagði Christophe Pinte frá Monash háskóla í Austurríki og Institut de Planétologie et d'Astrophysique de Grenoble (Université de Grenoble-Alpes/CNRS) í Frakklandi, og hafi verið aðalhöfundur annars af tveimur greinunum.
**After:** „Mælingar á flæði gass í ristli rúmvegsfjölda gefa okkur miklu meiri öryggi um að reikistjörnur séu í kringum ung stjörnu,“ sagði Christophe Pinte við Monash School of Science í Austurríki og Institut de Planétologie et d'Astrophysique de Grenoble (Université de Grenoble-Alpes/CNRS) í Frakklandi, aðalhöfundur annars af tveimur greinunum.

</details>

<details><summary>Anchor: p13official21:test:eso:105</summary>

**Source:** The OmegaCAM consortium is comprised of institutes in the Netherlands (NOVA, in particular the Kapteyn Institute / OmegaCEN Groningen and Leiden Observatory), Germany (in particular the university observatories of Munich, Göttingen and Bonn) and Italy (INAF, in particular the Padua and Naples Observatories).
**Reference:** Í OmegaCAM samstarfinu eru stofnanir frá Hollandi (NOVA, sér í lagi Kapteyn-stofnunin / OmegaCEN Groningen og Leiden stjörnustöðin), Þýskalandi (sér í lagi stjörnustöðvar háskóla í München, Göttingen og Bonn) og Ítalíu (INAF, sér í lagi stjörnustöðvarnar í Padúa og Napólí).
**Before:** OmegaCAM samstarfsstofan er samanstöndur stofna í Hollandi (NOVA, einkum Kapteyn stofan / OmegaCEN í Groningen og Leiden stjörnufræðistofnun), Þýskalands (einkum stjörnufræðistofnanir í München, Göttingen og Bonn) og Ítalíu (INAF, einkum Padua og Naples stjörnufræðistofnanir).
**After:** OmegaCAM samstarfshópurinn samanstendur af stofum í Hollandi (NOVA, einkum Kapteyn stofan / OmegaCEN í Groningen og Leiden stofan), í Þýskalandi (einkum stjörnufræðistofnanir í München, Göttingen og Bonn) og í Ítalíu (INAF, einkum Padua og Naples stjörnufræðistofnanir).

</details>

## 最终anchor语义逐条审核 / Final anchor semantic cases


<details><summary>after · G8 · p13official21:test:eea:79 · F</summary>

**Source:** Justified estimates must be made of the expected concentrations of the active substance and relevant metabolites, degradation and reaction products, in soil, groundwater, surface water and air, following use as proposed or already occurring.
**Semantic decision:** F — All eight corrupt environmental compartments and/or concentration/product categories. Candidate5 omits the soil/water/air list entirely; none preserves the full estimation requirement.
**Candidate 0:** Rekja skal réttlega út á viðbótarmiklum styrk virka efnisins og viðkomandi umbrotsefnanna, deilumengunar- og efni sem vist er að uppfæra, í jarðvågi, grunnvatni, yfirborðsvatni og lofthjúpum eftir notkun eins og legg ut er eða þegar hafa orðið fram.
**Candidate 1:** Við útreikninga, sem skýrða skal, verður að meta virkt efni og viðeigandi umbrotsefni og niðurgangsefni, afgengingu og vöruframleiðingum í jarðinu, grundvallawatn, yfirborðsvatni og lofthorni, eftir notkun sem mælt er fyrir um eða er nú þegar komið fram.
**Candidate 2:** Gera verður réttar mat á búist við því hvað efni og þá efnasöfnum sem hún valdar, umbrotum og vökvum og áhrifum, sem hún gengur í út í erði, jurtigrunni, yfirborðsvatni og lofti, að lokum notað er eins og mælt er fyrir um eða það hefur orðið til.
**Candidate 3:** Gera skal réttlætanlega mat á hugsanlegum þéttni virka efnisins og viðkomandi umbrotsefna, umbrotsefna umferðar og afleiðingar, í jarðvökvi, vatnshaldvegi, yfirborðsvökvi og lofthjálpum eftir notkun eins og hún er í tillögu eða þar sem hún hefur í för með sér.
**Candidate 4:** Gera verður réttunarskömmtun á hugsanlegum þéttni virka efnisins og viðeigandi umbrotsefna, umbrotsefnisfalla, deytingar- og viðbrögðaafurða í jarðvatni, grundvatni, yfirborðsvatni og lofthjúpum eftir notkun eins og forsluð er eða þegar það hefur orðið.
**Candidate 5:** Gera skal réttan mat á viðfangsefnisstyrkleika virka efnisins og viðkomandi umbrotsefni, umbrotsefni og framleiðslutegundum við notkun eins og mælt var fyrir um eða sem hefur orðið til staðar.
**Candidate 6:** Sjálfkæri mat skal gera á virku efninu og viðkomandi umbrotsefnum og framleiðsluefnum í jarðvökunni, grundvöldvökunni, yfirborðsvökunni og lofthjúpum, eftir notkun eins og tillögð er eða þar sem það hefur orðið til.
**Candidate 7:** Kvilla skal ábyrgð á áætlaðri mat á hugsanlegum þéttni virku efnisins og viðkomandi umbrotsefna, umbrotsefnisfalla, runudeppi og efni í jarðvinnumið, vökvavatn, yfirborðsvatni og lofti eftir notkun sem kvikinn hefur átt til eða þegar það hefur orðið til.

</details>

<details><summary>before · G8 · p13official21:test:eso:871 · P</summary>

**Source:** A team of astronomers led by Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) first used the ULTRACAM system on ESOs New Technology Telescope to measure these brightness changes very precisely.
**Semantic decision:** P — Candidate1 preserves AdamHardy-led astronomy team, ULTRACAM/NewTechnologyTelescope and precise brightness-change measurements.
**Candidate 0:** Hópur stjörnufræðinga, gefinn á byrjun Adam Hardy (Universidad Valparaíso, Valparaíso í Chile), notuði fyrst þann ILTRACAM kerfi við New Technology Telescope ESO til að mæla venjulega breytir á svæðum.
**Candidate 1:** Hópur stjörnufræðinga, leitt af Adam Hardy (Università Valparaiso, Valparaiso í Chile), fyrst notaði ULTRACAM kerfið á New Technology Telescope ESO til þess að mæla fyrir ljósstigsbreytingunum mjög nákvæmlega.
**Candidate 2:** Hópur stjörnufræðinga, gefinn gefið leitil til Adam Hardy (Universidad Valparaíso, Valparaíso, Chile), notuði ULTRACAM kerfið á New Technology Telescope ESO til að mæla skýrlega á birtum breytum á stjörnunum.
**Candidate 3:** Hópur stjarnvísindamanna, á borð Adam Hardy (Universidad Valparaíso, Valparaíso í Chile) fyrst notuði ULTRACAM kerfið á New Technology Telescope ESO til að mæla ljósverkni í þessum skiptum.
**Candidate 4:** Hópur stjarnvísinda, yfirskipað Adam Hardy (Universidad Valparaíso í Chile), notuði fyrst ULTRACAM kerfinu á New Technology Telescope ESO til að mæla bæði áhrif á ljósstyrkurinni svo nákvæmlega sem mögulegt er.
**Candidate 5:** Hópur stjörnufræðinga, yfirskipuð Adam Hardy (Universidad Valparaíso í Chile), nýtti ULTRACAM kerfið á New Technology tealli ESO til að mæla skýrlega úr breytni á ljósstyrkum.
**Candidate 6:** Fjölskylda stjörnufræðinga, leitt af Adam Hardy (Universidad Valparaíso í Valparaíso í Chile), fyrst notuð hefur ULTRACAM kerfið á New Technology Telescope ESO til að mæla í mjög nákvæmri hætti um breytanir ljósafmagns.
**Candidate 7:** Starfsfélög stjörnufræðinga, leitt á forysti Adam Hardy (Universidad Valparaíso, Valparaíso í Chile), fannst fyrst og fyrst með ULTRACAM kerfinu á New Technology Telescope ESO til að mæla ljósmagna breytina mjög nákvæmlega.

</details>

<details><summary>after · greedy · p13official21:test:eso:714 · F</summary>

**Source:** By studying this effect it is possible to map out the places where gravity is strongest, and hence where the matter, including dark matter, resides.
**Semantic decision:** F — Gravity is strongest becomes the area is largest; the gravitational mapping relation is lost.
**Candidate 0:** Með þessari rannsókn er hægt að koma á mynd af staðnum þar sem svæðið er stærsti og því þar sem efnið, þar með taldir dökk efni, er að vera.

</details>

<details><summary>after · G8 · p13official21:test:eea:43 · F</summary>

**Source:** Where plant protection products containing the active substance are intended to be used in cold climatic conditions, the tests have to be conducted where DT50lab, determined at 10 °C and at a moisture content of the soil related to a pF value of 2 to 2,5 (suction pressure) is greater than 90 days.
**Semantic decision:** F — All eight corrupt cold-climate use, soil moisture or suction-pressure conditions. Numeric temperature/pF/DT50 thresholds alone are insufficient.
**Candidate 0:** Ef efna- verndarvörur, sem innihalda virka efnið, ætla að nota í kædiviðmiðum, skulu þá framkvæmdar prófanir þar sem DT50lab, sem ákveðið er við 10°C og í vökvastigi soðsins sem tengist pF-gildi 2 til 2,5 (síuþrýsting) er meiri en 90 dagar.
**Candidate 1:** Ef notkun á plöntuverndarvörum með virka efni er áhugað fyrir fötgerð með varma, skulu prófanir gert þar sem DT50lab, á 10 °C og varma í jarðsvörun sem tengist pF gildi 2 til 2,5 (sæfiling) er meiri en 90 daga.
**Candidate 2:** Ef um er að ræða notkun plöntuvarnarefna sem innihalda virka efni í kaltum líðrar víxlu, þarf að framkvæma prófanir þar sem DT50lab, sem er ákvarðaður við 10°C og vökvastigi í landi sem tengist pF gildi 2 til 2,5 (slökkt þrýsting) hefur verið stærri en 90 daga.
**Candidate 3:** Ef varnarefni, sem innihalda virka efni, eru ætlað að nota í fölgunslagi við sól, verða prófanirnar framkvæmdar þegar DT50lab, á nýmanni 10°C og á vökvaþéttni jarðins, sem tengd er til pF-gildi 2 til 2,5 (sökuþrýsting), er greinilegri en 90 dagar (DT50lab).
**Candidate 4:** Ef vænting er að plantavörur, sem innihalda virka efni, séu notaðar við kalt vegna í vetrarýnnum skulu prófanir fara fram þegar DT50lab, á 10°C og á vökvaþéttni yfir í yfirborði á pF gildi 2-2,5 (sæmeðgengileg álag) er meiri en 90 dagar.
**Candidate 5:** Ef upp hentar að nota plöntuverndarvörur sem innihalda virka efni í kaldsafnablöndum þarf að framkvæma prófanir þar sem DT50lab, ákvarðað við 10 °C og á vökvaþéttni jarðar, sem tengist pF-gildi 2-2,5 (sirkvintengsla), er meiri en 90 dagar.
**Candidate 6:** Ef flöguðar varnarefni, sem innihalda virka efni, ætla að nota í kæðilegum aðstæðum, skal gera prófanir þar sem DT50lab, sem ákvarðað er við 10 °C og í vöðvabroti sem tengist pF gildi 2-2,5 (þrýsting) er meiri en 90 daga.
**Candidate 7:** Ef lyf, sem innihalda öryggisþætt þar sem verulega varðar krabbamein, ætla að nota í sólfráhvöruna, skulu prófanir verið gerðar, ef DT50lab, á 10 °C og með límhvarfinu í yfirborði á pF gildi 2 til 2,5 (þrýstingstilvika), er meiri en 90 daga.

</details>

<details><summary>after · greedy · p13official21:test:ema:2323 · U</summary>

**Source:** It is important to drink plenty of water to avoid dehydration.
**Semantic decision:** U — Drinking water and avoidance are retained; cannot certify the nonstandard dehydration term útþurrð as semantically equivalent.
**Candidate 0:** Mikilvægt er að drekka mikið af vatni til að forðast útþurrð.

</details>

<details><summary>after · greedy · p13official21:test:eea:1557 · F</summary>

**Source:** The Commission Communication ‘i2010 - A European Information Society for growth and employment (COM(), developing the Lisbon strategy, seeks to ensure coherence across the Commission's information society and media policies in order to reinforce the significant contribution of information and communication technologies to the performance of the economies of Member States.
**Semantic decision:** F — Invents COM(2009)478 and loses the Lisbon-strategy relation and coherent policy/institution descriptions.
**Candidate 0:** Í orðsendingu framkvæmdastjórnarinnar „i2010 – Evrópska upplýsinga- og fjarskiptahósi til vaxtar og starfsemi (COM(2009) 478, þar sem hún er að því að stuðla að samræmi í upplýsingahópi framkvæmdastjórnarinnar og fjarskiptavísindum, til að styrkja mikilvægan þátt upplýsingatækni og fjarskipta- tækni við efnahagskerfi aðildarríkjanna,“ er miðað við að tryggja samræmi milli upplýsingahópsins og fjarskiptavísindaframkvæmdastjórnarinnar.

</details>

<details><summary>after · G8 · p13official21:test:eea:1751 · F</summary>

**Source:** On the basis of the common criteria, and in view of the fact that, to date, ICAO has not agreed to the closure of any of the findings raised during its audits, it is assessed that, at present, the competent authorities of Indonesia have failed to demonstrate that they have performed their regulatory and oversight responsibilities in compliance with ICAO standards with respect to all the carriers they certify.
**Semantic decision:** F — All eight corrupt audit closure and/or regulatory oversight obligations. Several change Indonesia to India; the closest variants still mangle the responsibility/standards relation.
**Candidate 0:** Á grundvelli sameiginlegra viðmiðana og með tilliti til þess að til þessa kosti ICAO hefur ekki samþykkt að loka á einhverju af sérþekkingunum sem upprunum komu meðan á upplýsingarefnaeftirliti hafa verið gerðar, er metað sem lögbæra yfirvöld Indóneseyðar hafi slíkt nokkuð að ekki verið hafa að sýna fram á að þau hafi skuldbundið ábyrgð á reglum og eftirliti með þeim í samræmi við stöður ICAO að því er varðar allir flug- og flugmálanir sem þau gangi út.
**Candidate 1:** Á grundvelli sameiginlegra viðmiðana og í þeim tilvikum að ICAO hefur ekki komið sami um niðurstöður sem upplýstir voru í endurskoðunum þeirra til þess að næst þó hefur ekki verið sami um niðurstöður sem upplýstir voru í endurskoðunum þeirra, er metin að lögbæra yfirvald Indónesíu hafi ekki komið fram á það að þeir stunda skuldbindingum og eftirlitsbundnum skyldum sínar í samræmi við staðli ICAO að því er varðar allar flutningafélög sem þau staðfesta.
**Candidate 2:** Á grundvelli sameiginlegra viðmiðana og með tilliti til þess að ICAO hefur ekki komið á samkomulagi að loka einhverju af niðurstöðum sem kom á vegum á skoðunum sínum, er gert útreikning á því að þegar staðfestir lögbærum yfirvöldum í Indônesía hafi þeir ekki haldið við þá að þeir hafi framfylgt ábyrgðar- og eftirlitsaldra sínar í samræmi við gildandi staðla ICAO á þeim flutningsfélögum sem þær færa út sönnun.
**Candidate 3:** Á grundvelli sameiginlegra viðmiðana og með tilliti til þess að ICAO hefur ekki komið á ákvörðun um lokun af niðurstöðum sem komu fram í endurskoðuninni, er metin að lögbæru yfirvöldum í Indíen séu núna hins vegar hafa missað þá tryggingu og eftirlitsþáttum sínum með tilliti til ICAO-gagnsæi að því er varðar allir flutningafélög sem þau hafa staðfest.
**Candidate 4:** Af grundvelli sameiginlegra viðmiðana og með tilliti til þess að ICAO hefur ekki samþykkt að slaka á einhverjum niðurstöðum sem komið hafa fram í endurskoðunum sínum, er þegar matið er lagt á að lögbæru yfirvöldum í Indóneesíu hafi ekki sýnt fram á að þeir hafi framfylgt ábyrgðir sína sem er aðeins að skilja reglulögbundnar og eftirlitsbörnin að því er varðar öll flutningsfyrirtæki sem þau sannreyni.
**Candidate 5:** Á grundvöllum sameilda viðmiðunarframlaga og með tilliti til þess að ICAO hefur enn ekki samþykkist þess að slökkva á neinu af niðurstöðunum sem greint hefur verið við í endurskoðunum til þess er útgáfu er notað, er greint að lögbær yfirvöld í Indónsíu hafi nú þegar missið sér um að sýna fram á að þeir hafi gerð skuldbandsverndarráðstefnur sinnar og eftirlitið í samræmi við stöðlun ICAO að þeim allar flutningafélög sem þeir veita vottorð fyrir.
**Candidate 6:** Með tilliti til þess að ICAO hefur ekki samþykkist að loka neinu af niðurstöðunum sem hafa komið framum í skoðunum sínum, er ákvarðað að gæði lögbærra yfirvalda Indonesia hafi núna misstir að sýna fram á að þau hafi framfylgt ábyrgð þeirra sem er að verða um eftirlit og reglur sem ICAO stendur fyrir að hægt sé að staðfesta allar flugrekendum sem þau formögnir.
**Candidate 7:** Á grundvelli sameiginlegra viðmiðana og miðað við það að nú þegar ICAO hefur ekki komist að samþykkt fyrirframmi til lokunar á alla fjölli sem sýnt hefur verið fram á með skoðunum sínum, er talið að þegar í þeirri stigi hafa lögbær yfirvöld í Indíen ekki sýnt fram á að þau hafi uppfyllt þá borsmiðla og eftirlitsbundnar skuldbindingar sína í samræmi við gildandi staðla ICAO að því er varðar öll flutningsfélög sem þau hafa staðfesta.

</details>

<details><summary>after · G8 · p13official21:test:eso:514 · P</summary>

**Source:** This star formation region is forming many stars.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Candidate 0:** Þessi vetrarbraut verður fjöldi stjarna.
**Candidate 1:** Þessi stjörnumyndunarsvæði myndar mörg stjörnur.
**Candidate 2:** Þessi stjörnumyndunarsvæði myndir mörg stjörnur.
**Candidate 3:** Þessi stjörnumyndunarsvæði getur myndast margra stjarna.
**Candidate 4:** Þessi stjörnumyndunarsvæði myndast mörgum stjörnum.
**Candidate 5:** Þetta stjörnumyndunar svæði myndast mörg stjörnur.
**Candidate 6:** Þessi svæði við myndun stjarna er myndandi margar stjörnur.

</details>

<details><summary>before · greedy · p13official21:test:eso:1073 · F</summary>

**Source:** Analysis of this spectrum indicated that its atmosphere is cloudy.
**Semantic decision:** F — Spectrum becomes sequence and cloudy is not preserved.
**Candidate 0:** Greining á þessari röð sýndi að lofthjúpurinn sé skúttur.

</details>

<details><summary>after · G8 · p13official21:test:eso:1100 · U</summary>

**Source:** The combination of images taken by three exceptional telescopes, the ESO Very Large Telescope on Cerro Paranal , the MPG/ESO 2.2-metre telescope at ESOs La Silla observatory and the NASA/ESA Hubble Space Telescope, has allowed the stunning Jewel Box star cluster to be seen in a whole new light.
**Semantic decision:** U — Candidate3 is closest with the telescope list, Jewel Box cluster and new-light relation, but the image-taking/three-telescope clause is malformed enough that full fidelity cannot be certified. Other variants corrupt the cluster or instruments.
**Candidate 0:** Samsetning myndum, sem trefkyn grífar sjónaukar tekin, Very Large Telescope ESO í Cerro Paranal, MPG/ESO 2,2 metra sjónaukinn í La Silla stjörnustöð ESO og NASA/ESA Hubble geimsjónaukinn, hefur leitt til þess að tókast stafturinn Jewel Box stjörnuloki í frá í ný tímum.
**Candidate 1:** Samsetningu myndirnar sem trefna sjónaukar náðu til, þrjá sérstaka sjoða sjónaukar, Very Large Telescope (ESO) í Cerro Paranal, MPG/ESO 2,2 metrar sjoða í La Silla stjörnustöð ESO og Hubble geimsjónauka NASA og ESA, hefur metað Jewel Box stjörnumerkið í nýveru ljós.
**Candidate 2:** Þessi samsetning ámyndanna, sem trefra sjónaukar skilja, ESO Very Large Telescope á Cerro Paranal , MPG/ESO 2,2-metrar sjónaukanum í La Silla stjörnustöð ESO og NASA/ESA Hubble geimsjónaukanum, hefur leitt til þess að sjúta í nýju ljósi niðurstöðu stjörnumerks Júvellingskúpu.
**Candidate 3:** Samsetning ámyndanna, sem trefjum sjónaukum, Very Large Telescope ESO í Cerro Paranal, MPG/ESO 2,2-metrar sjónaukanum í La Silla stjörnustöð ESO og Hubble geimsjónaukanum NASA og ESA, hefur leitt til sjónar hjá Jewel Box stjörnustjörnuþyrpingunni í nýju ljósi.
**Candidate 4:** Samborgið myndir sem nýst með þremur sérstökum sjónauka, Very Large Telescope ESO í Cerro Paranal, MPG/ESO 2,2 metra sjónaukanum í La Silla stjörnustöð ESO og Hubble geimflensujónustu NASA og ESA, hefur gert kleift að sjá stjörnumynnum í Jewel Box í nýju ljósi.
**Candidate 5:** Sú samsetning myndir sem mótaður var af þremur aðstæður síunóma sjónauka, Very Large Telescope ESO á Cerro Paranal, MPG/ESO 2,2 m ið sjónauka í La Silla stjörnustöð ESO og Hubble geimsjónauka NASA/ESA hafa gert hæfileg sýn af jólstöfunni í nýja ljósi.
**Candidate 6:** Samsetning á myndum sem trefuga sjónaukar tveggja hafa tekin, Very Large Telescope Very Large Telescope ESO í Cerro Paranal, MPG/ESO 2,2 metra sjónauka í La Silla stjörnustöð ESO og Hubble geimsjónauka NASA og ESA, hefur leitt til þess að bjarta hólfin sjást í nýju ljósi.
**Candidate 7:** Samsett myndirnar sem náðnað var með þremur sérstaka sjónaukum, Very Large Telescope ESO í Cerro Paranal, MPG/ESO 2,2-metrar sjónaukanum á La Silla stjörnustöð ESO og Hubble geimsjónauka NASA/ESAs, hafa leitt til þess að sýna stjörnulokið Jewel Box í nýlega ljósi.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:2721 · F</summary>

**Source:** No, but one day, I'll take that cane away...
**Semantic decision:** F — Take that cane away is changed to getting the stick, losing the removal action.
**Candidate 0:** Nei, en einn daginn, ég fær þennan stöng...

</details>

<details><summary>before · greedy · p13official21:test:eso:400 · F</summary>

**Source:** ESPRESSO will feature radial velocity precision of 0.35 km/hour or less.
**Semantic decision:** F — Radial component of velocity precision is omitted.
**Candidate 0:** ESPRESSO mun koma fram með nákvæmni á hraða sem er 0,35 km/klst. eða minna.

</details>

<details><summary>before · G8 · p13official21:test:eso:839 · P</summary>

**Source:** The Caisey Harlingten and ASH2 telescopes.
**Semantic decision:** P — Candidate1 preserves both named telescopes with correct Icelandic telescope noun.
**Candidate 0:** Caisey Harlingten og ASH2 stjörnustjörnunum.
**Candidate 1:** Caisey Harlingten og ASH2 sjónaukarnir.
**Candidate 3:** Caisey Harlingten og ASH2 sjónaukann.
**Candidate 4:** Caisey Harlingten og ASH2 sjónauki.
**Candidate 6:** Caisey Harlingten og ASH2 sjónaukarnar.

</details>

<details><summary>before · G8 · p13official21:test:ema:1152 · P</summary>

**Source:** Change from baseline in body weight was similar for patients treated with sitagliptin relative to placebo.
**Semantic decision:** P — Candidates1/3/4/5/6 preserve body-weight change from baseline, similar sitagliptin-versus-placebo comparison.
**Candidate 0:** Breyta á líkamsþyngd frá upphafsgildi var svipuð hjá sjúklingum sem fengu sitagliptin í samanburði við lyfleysu.
**Candidate 1:** Breyting á líkamsþyngd frá grunngildi var svipað fyrir sjúklinga sem fengu sitagliptín samanborið við lyfleysu.
**Candidate 2:** Áhrif á líkamsþyngd frá upphafsskammti voru svipuð hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.
**Candidate 3:** Breyting á líkamsþyngd frá upphafsgildi var svipuð hjá sjúklingum sem fengu sitagliptin samanborið við lyfleysu.
**Candidate 4:** Breyting á líkamsþyngd frá upphafsgildi var sambærileg hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.
**Candidate 5:** Breyting frá upphafsgildi á líkamsþyngd var svipuð hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.
**Candidate 6:** Breyting í líkamsþyngd frá upphafi var svipuð hjá sjúklingum sem fengu sitagliptin samanborið við sjúklinga sem fengu lyfleysu.
**Candidate 7:** Breyting frá grunngildi á líkamsþyngd hjá sjúklingum sem fengu sitagliptin samanborið við lyfleysu.

</details>

<details><summary>after · greedy · p13official21:test:eea:850 · F</summary>

**Source:** When implementing this strand the Commission will in particular ensure consistency and complementarity with the activities conducted by other Commission services or by European agencies; in particular, the European Foundation for the Improvement of Living and Working Conditions and the Community RTD Framework programme and the European Centre for the Development of Vocational Training (Cedefop).
**Semantic decision:** F — The foundation's living/working conditions remit is replaced by life-protection/work-participation wording, and RTD institutional roles are corrupted.
**Candidate 0:** Þegar framkvæmd þessara strandar verður að ráða framkvæmdastjórnin einkum að samræmi og aukabundning við starfsemi annarra þjónustuveitenda framkvæmdastjórnarinnar eða evrópskra stofnana sé tryggt; einkum með því að tryggja starfsemi Evrópusamstofnunarinnar fyrir bætur á aðgerðum til að bæta lífvernd og vinnuþátttöku og rannsóknaráætlunina um rannsóknir og uppbyggingu á rannsóknarskilyrðum í bandalaginu (RTD) og Evrópska stofnunarinnar fyrir þjálfun í sviði starfsþjálfunar (Cedefop).

</details>

<details><summary>before · G8 · p13official21:test:eea:1751 · F</summary>

**Source:** On the basis of the common criteria, and in view of the fact that, to date, ICAO has not agreed to the closure of any of the findings raised during its audits, it is assessed that, at present, the competent authorities of Indonesia have failed to demonstrate that they have performed their regulatory and oversight responsibilities in compliance with ICAO standards with respect to all the carriers they certify.
**Semantic decision:** F — All corrupt country, closure-of-findings, regulatory/oversight duties or certified-carrier scope; correct Indonesia in7 does not fix remaining clauses.
**Candidate 0:** Á grundvelli sameiginlegra viðmiðanna og miðað við það að ICAO hefur ekki þegar samþykkist gagnvart lokun af mörgum niðurstöðum sem upprunandi skoðanir hafa leitt fram, er greint að lögbæra yfirvöld Indíans hafi ekki komið fram á því að þau hafi lögð fram eftirlits- og regluminniverk fyrir sér í samræmi við staðla ICAO að því er varðar allir flutningsfélög sem þau staðfesta.
**Candidate 1:** Béðið ánægjandi viðmiðunum og með tilliti til þess að ICAO hefur ekki samþykkist skal ekki taka til greina, til þess að þeir hafa sýnt fram á að lögbær yfirvald í Indónesía hafi ekki sýnt fram að þeir hafi komið á fót reglum og eftirlitsþörfum sínum í samræmi við ICAO-rúmmál um allt flugum sem þau sannfæra.
**Candidate 2:** Á grundvelli sameiginlegra viðmiðanna og með tilliti til þess að ICAO hefur ekki samþykkist leyfis nema á einhverjum niðurstöðum sem stofnaði á með skoðunum, er gert útreikning á því að núverandi lögbæra yfirvöld Indóneisinni hafi ekki sýnt fram á að þau hafi fullnægt yfirmiðilum sínum um reglufyrirkomulag og eftirlit með öllum flutningameðallögum sem þau staðfesta.
**Candidate 3:** Á grundvelli sameiginlegra viðmiðana og í þeim tilviki að ICAO hefur ekki komið á samkomulagi um lokuð af niðurstöðum sem komu fram í endurskoðuninni, er talið að lögbæra yfirvöld Indíans hafi ekki snýið fram að þeir hafi uppfyllt ræðubærar og eftirlitsbærar skyldur sína í samræmi við stöður ICAO að því er varðar öll flutningafélög sem þau samþykkja.
**Candidate 4:** Af grundvelli sameiginlegra viðmiðana og með tilliti til þess að ICAO hefur ekki samþykkt fyrir hendi skoðunaraðgerðirnar í beinu um hvern af skynsöguðum niðurstöðum sem þeir voru að ræða, er ákvarðanir gerðar á því að gagnvart útgáfu ICAO hefur lögbær yfirvald í Indóleni ekki sýnt fram á að þau hafi uppfyllt ákvæði um skuldbindingar og eftirlit með flugmálum í samræmi við stöðu ICAO að teknu tilliti til öllum flugfélöganna sem þau staðfesta.
**Candidate 5:** Á grundvöllum sameiginlegra viðmiðana og með tilliti til þess að ICAO hefur ekki samþykkt að loka ákvarðanann sem upp komu í sannprófunins sína til auglá, er metin þýði lögbær yfirvöld í Indókanum hafa ekki sýnt fram á að þau hafi framfylgt ábyrgð sín með reglur og eftirliti í samræmi við stöðlu ICAO að því er varðar alla flutningsfélög sem þau sannreyna.
**Candidate 6:** Með tilliti til þess að ICAO hefur ekki samþykkist að loka neinu af niðurstöðunum sem hafa verið tekið fram í endurskoðun, er ákvarðað að, þegar í tímanum, hafi lögbær yfirvald í Indónenía ekki sýnt fram á að þau hafi stuðlað yfirvalda- og eftirlitsaldila sína í samræmi við verklagsstaðla ICAO við aðgerðir til allra flugfara sem þau sannfæra.
**Candidate 7:** Á grundvelli sameiginlegra viðmiðana og miðað við það að ICAO hafi ekki samþykktur að slökkva á neinum niðurstöðum sem koma fram í eftirliti sín með þá tilskildum aðstöðu, er matin liðin að lögbær yfirvöld Indónesíu hafi ekki sýnt fram á að þau hafi uppfyllt fulltrúa skuldbindingar sínar um reglulegu og eftirlits- mannkun í samræmi við stöðu ICAO að því er varðar öll flutningsfélög sem þau bindir undir.

</details>

<details><summary>before · G8 · p13official21:test:eso:1088 · F</summary>

**Source:** Weather statistics are available here.
**Semantic decision:** F — Weather statistics becomes winter research, radio data or unrelated records in every candidate.
**Candidate 0:** Vetrarannsóknir eru hér.
**Candidate 1:** Útvarps-íslendingarnám birtaðar eru hér.
**Candidate 2:** Útabréf yfir vakt er hér.
**Candidate 3:** Vetrarannsóknarupplýsingar eru hér.
**Candidate 4:** Vetnaskýrslur eru hér fyrir hendi.
**Candidate 5:** Útvarpsgögur eru hér fyrir.
**Candidate 6:** Vetrarannsóknarupplýsingar eru hér fyrir.
**Candidate 7:** Útvarps-eyðubúnað er hér fyrir.

</details>

<details><summary>before · G8 · p13official21:test:ema:1190 · F</summary>

**Source:** In these cases it is therefore recommended that the Zonegran total dose should be rounded up or down to the nearest available dose that can be achieved with commercially available capsule strengths of Zonegran (25 mg, 50 mg and 100 mg).
**Semantic decision:** F — All corrupt rounding/nearest available dose or commercially available capsule-strength requirement.
**Candidate 0:** Í þeim tilfellum er því mælt með að heildarskammtur Zonegran sé snúin upp eða niður til næstum fyrirbærrar skammtsins sem er hægt að ná með skammtastyrku Zonegran innleiðisbúnaðar (25 mg, 50 mg og 100 mg).
**Candidate 1:** Í þessum tilfellum er því ráðlagt að kenna við að ná nálægri þéttni frá toölum af Zonegran í að minnsta kosti eða að hásta þann stærri nálægri þéttni sem getur náð með sárið fyrir handa capsúlum af Zonegran (25 mg, 50 mg og 100 mg).
**Candidate 2:** Í slíkum tilvikum er því mælt með að nýta allra talna skammta Zonegran sem er fáanlegt og reyna má með skammtokynnum af Zonegran sem eru fáanleg í markaðsleyfi (25 mg, 50 mg og 100 mg).
**Candidate 3:** Í þessum tilfellum er því mælt með að þann heildarlyfjagjöf sem gefast er með Zonegran sé kviðupanleg eða kviðinn niður, að nægri frá fyrirbæri lyfsstyrkurinu sem er að komast á með öflugum, aðgengi Zonegran (25 mg, 50 mg og 100 mg).
**Candidate 4:** Í slíkum tilvikum er því ráðlagt að enduruppið þéttni skammta með Zonegran, að lokinni nálægri skammti sem má ná með kílum styrk Zonegran (25 mg, 50 mg og 100 mg) sem eru fyrir handa markaðsleyfis.
**Candidate 5:** Í þessum tilvikum er því ráðlagt að hefja viðbótareinkennum af heildarskammtinum af Zonegran upp eða niður í næstu færanlega skammt sem er hægt að ná við af lyfjagigt fyrir skammta af Zonegran (25 mg, 50 mg og 100 mg).
**Candidate 6:** Í þessum tilfellum er því mælt með því að ná skuggaðan, nálægri skammti sem færi að ná með útsækjandi skammti úr kapslerum með virðingu til nálægri skammts af Zonegran (25 mg, 50 mg og 100 mg).
**Candidate 7:** Í þessum tilfellum er því ráðlagt að aðlaga umsóknina eða niðri í nálægri fyrirbæri skammtinum, sem hægt er að ná með vörnum af breytilegu fæðu (25 mg, 50 mg og 100 mg) sem eru fyrir handelsráð.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:3265 · F</summary>

**Source:** There's a police convention out there.
**Semantic decision:** F — Police convention is not expressed by the invented compound.
**Candidate 0:** Það er lögreglukonar úti.

</details>

<details><summary>after · greedy · p13official21:test:ema:1458 · F</summary>

**Source:** This is important to make the medicine easier and more comfortable to inject.
**Semantic decision:** F — More comfortable is translated as old (gamall); injection comfort is not retained.
**Candidate 0:** Þetta er mikilvægt að gera lyfið auðveldari og gamall til að sprauta því.

</details>

<details><summary>before · greedy · p13official21:test:ema:2323 · F</summary>

**Source:** It is important to drink plenty of water to avoid dehydration.
**Semantic decision:** F — Dehydration becomes urine formation.
**Candidate 0:** Mikilvægt er að drekka mikið af vatni til að forðast þvagmyndun.

</details>

<details><summary>before · G8 · p13official21:test:ema:430 · F</summary>

**Source:** Keep the needle in your skin after the dose counter has returned to 0 and count slowly to 6.
**Semantic decision:** F — Each candidate changes in-skin to on-skin, slow to fast, dose counter or the complete ordered instruction.
**Candidate 0:** Geymið nálina á húðinni eftir að skammtahlutarinnur hefur náð 0 og rannsakaði hratt að 6.
**Candidate 1:** Haldið nálinni á húðinni eftir að skammtaríkið hefur náð 0 og tölutakaðst fljótlega til 6.
**Candidate 2:** Geymið nálina í húðinni eftir að gömlunarkílurinn hefur orðið 0 og tölulastu hraðar til 6.
**Candidate 3:** Haldið nálinni á húðinni eftir að skammtaalitinn hefur farið til 0 og tölur hægt langt saman til 6.
**Candidate 4:** Haltu nálina í húðinni á eftir að skammtaleyfið hefur náð 0 og töljaði slæmar til 6.
**Candidate 5:** Haltu nálinni á húðina í lok 0 og tölutakkaðu hægt til 6.
**Candidate 6:** Haltu nálina lengi í húðinni eftir að skammtalistið er aðeins 0 og rannsakaðu hana að 6.
**Candidate 7:** Haldið nálina í húðinni þegar töflu upphaflega hefur orðið að 0 og tölutöluðið slönguð eftir að getið er 6.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:3454 · P</summary>

**Source:** And I work for Danny.
**Semantic decision:** P — And I work for Danny preserved.
**Candidate 0:** Og ég vinn fyrir Danny.

</details>

<details><summary>after · G8 · p13official21:test:eea:1323 · F</summary>

**Source:** If refills are not provided, the weight of the total primary packaging shall not exceed 3,7 g per wash for tablets and 1,7 g per wash for all other products.
**Semantic decision:** F — All eight corrupt primary packaging and/or refill/per-wash conditions; retaining the3.7/1.7 numbers is insufficient.
**Candidate 0:** Ef ekki er mögulegt að fá endurtekna gjöf skulu þyngd heildarskilyrða, að því er varðar öllum flokka, ekki vera meiri en 3,7 g til hreinsunar eftir hverjum þvottum varðandi töflur og 1,7 g til hreinsunar eftir hverjum þvottum varðandi öll öðrum vörur.
**Candidate 1:** Ef fyllingu er ekki veitt skal þyngd heildarríkans búnaðarauðlauna ekki fara yfir 3,7 g fyrir hverja þvælingu og 1,7 g fyrir hverja þvæling eftir þvælingafæð fyrir öll önnur vörur.
**Candidate 2:** Ef ekki er veitt endurinnleiðir skal þyngd alls fyrirsöfnunareyris ekki fara yfir 3,7 g ferlsins fyrir töflur og 1,7 g ferlsins fyrir öll önnur vörur.
**Candidate 3:** Ef endurtekinn skammtur er ekki veitt skal þyngd heildarfráselds ekki vera meiri en 3,7 g í hverju þvagrindu fyrir töflur og 1,7 g í hverju þvagrindu fyrir öll önnur vara.
**Candidate 4:** Ef ekki er útgefandi endurprehöld, skal veflag heildarfyrirtækisins ekki fara yfir 3,7 g í hverja þvagfæranir fyrir töflur og 1,7 g í hverju þvagfæranir fyrir öll önnur vörur.
**Candidate 5:** Ef endurýnir eru ekki fylgt eftir skal þyngd heildarfræðilegra umbúta sem gefið er upp ekki vera meira en 3,7 g í hverjum þvottu fyrir töflur og 1,7 g í hverjum þvottu fyrir öll önnur vara.
**Candidate 6:** Ef endurtekningar er ekki til, skal hveinlegur heildaráföngin ekki fara yfir 3,7 g fyrir hverja þvotta fyrir töflur og 1,7 g fyrir hverja þvotta fyrir alla önnur vara.
**Candidate 7:** Ef notkun endurtekna uppsettunar er ekki hægt skal þyngdarafurðin ekki fara yfir 3,7 g á hverja vatning af töflum og 1,7 g á hverja vatning af öllum öðrum vörum.

</details>

<details><summary>after · greedy · p13official21:test:eea:568 · F</summary>

**Source:** This device shall reverse the window/roof panel/partition before it exerts a pinch force of more than 100 N within the opening of 200 mm to 4 mm above the top edge of a power-operated window/partition or in front of the leading edge of a sliding roof panel and at the trailing edge of a tilting roof panel.
**Semantic decision:** F — Reverse movement becomes revise, and window/partition/roof positions and the force geometry are corrupted or omitted.
**Candidate 0:** Þessi búnaður skal endurskoða glugga/þörmu/vefjarlægð áður en það skilur meira en 100 N áræðisþrýstingi innan opnunar sem er 200 mm til 4 mm yfir hátrarlið vélí eða þrátt við hátrarlið þolsþörmu og í fyrirhlið hátrarlið þolsvefjarlæggings.

</details>

<details><summary>before · G8 · p13official21:test:eso:63 · F</summary>

**Source:** “Studying afterglows is vital to further our understanding of the objects that become gamma-ray bursts and what they tell us about star formation in the early Universe,” says the studys lead author Jochen Greiner from the Max-Planck Institute for Extraterrestrial Physics in Garching bei München, Germany.
**Semantic decision:** F — All corrupt afterglows/gamma-ray bursts or scientific/institutional attribution.
**Candidate 0:** "Að rannsaka eftirgláðurnar er mikilvægt til þess að við sýnir meira af stjörnunum sem verða geimstorkur og sem segja við um stjörnumyndun fyrirheimisins", segir Jochen Greiner, hópyfni greinar um rannsóknina frá Max-Planck institúturinni fyrir geimfræði í Garching bei München í Þýskalandi.
**Candidate 1:** „Nauðsynlegt er að fá nánari nátmetun af stjörnum sem verða gamma-geislir og hve þau segja okkur um stjörnuformiðið í börnum alheiminu,“ sagði Jochen Greiner, forritandi greinarinnar, frá Max-Planck stofnuninni fyrir forraði-geðsniði í Garching við München í Þýskalandi.
**Candidate 2:** „Viðgangsprófanir skipta málið í frekari námi við skilningu á einingunum sem fleygja gammatillögun og hvað þær segja okkur um stjörnumyndun á fyrsta lagi alheimsins“, sagði Jochen Greiner, aðalhöfundur rannsóknarinnar frá Max-Planck stofnuninni fyrir fjölafurðatengda vísindanir í Garching í München í Þýskalandi.
**Candidate 3:** „Mannnmælingar á eftirglænum eru mikilvægar að því að því að framlengja skilning okkar um efnablöndur sem verða og hvað þeir segja okkur um stjörnumyndun á frumumjórninu,“ sagði Jochen Greiner, aðalhöfundur greiningarannsóknarinnar, frá Max-Planck stofnuninu fyrir geimfræði í Garching í München, Þýskalandi.
**Candidate 4:** "Að taka átöllu á eftirglæðum er mikilvægra þar sem það lætur okkur frekar skilja hvaða fyrirbæri gama-grásskjálftan eru og hvað þær segja okkur um stjörnumyndun í fyrstu evíni heims", sagði Jochen Greiner, leiðsöguhólls greinar í frambúrsjónunar-stofu í Garching í München í Þýskalandi.
**Candidate 5:** „Atprýma áfangan er mikilvægt því að auka skilning á lagi sem verða gymlaugabrot og hvað þeir segja okkur um stjörnumyndun í fyrstu alheiminum,“ sagði Jochen Greiner, leiðsöguherra rannsóknarinnar í Max-Planck stofnun um geimfluttni í Garching í München í Þýskalandi.
**Candidate 6:** „Með það sem varðar að æðast eftirglæði er mikilvægt til að drepið skilningu okkar um fyrirbæri sem verið er og hvað þau sega okkur um stjörnumyndun á fundinu fyrir Burtuðu Vetrarbrautana,“ sagði Jochen Greiner, aðalhöfundur rannsóknarinnar, frá Max-Planck stofnuninu fyrir raffræn fjölgaða í Garching bei München í Þýskalandi.
**Candidate 7:** „Vera með þátttöku á eftirlitusbolunum er háttfalt til að hafa frekari skilningu um fyrirbjóða sem verða gamma-geislur og veita okkur þáttar á stjörnumyndun á fyrri alheiminu,“ sagði Jochen Greiner, leiðsögnarstjóri rannsóknarinnar, frá Max-Planck stofnuninu fyrir geimfræði í Garching í Nemöđunum.

</details>

<details><summary>after · greedy · p13official21:test:eea:21 · F</summary>

**Source:** Soils used must, wherever possible, be freshly sampled.
**Semantic decision:** F — Soils become earth creatures (jarðverur); the sampled material is changed.
**Candidate 0:** Þar sem notuð eru jarðverur verður, hvenær sem mögulegt er, að taka nýja sýni frá þeim.

</details>

<details><summary>before · greedy · p13official21:test:ema:74 · P</summary>

**Source:** ARICLAIM should normally not be used for children and adolescents under 18 years.
**Semantic decision:** P — Normal avoidance for children/adolescents under18 and drug identity preserved.
**Candidate 0:** ARICLAIM á ekki venjulega að nota handa börnum og unglingum yngri en 18 ára.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:3337 · P</summary>

**Source:** But maybe, if we got away from here, if we went somewhere safe, it could be different.
**Semantic decision:** P — Retains the conditional possibility of a different outcome after leaving for a safe place; grammar is awkward.
**Candidate 0:** En kannski, ef við færum frá hér, ef við fórum til öruggs staðar, gæti það verið öðruvísi.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:936 · P</summary>

**Source:** Ma'am, I need the gentleman's signature so we can begin.
**Semantic decision:** P — Preserves request for the gentleman's signature before beginning; inflection is imperfect.
**Candidate 0:** Frú, ég þarf undirskriftur herra svo við getum byrjað.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:2130 · P</summary>

**Source:** Because Mr. Doyle called and said you have not been there all week.
**Semantic decision:** P — Retains Doyle calling and reporting that the addressee has not been there for a week.
**Candidate 0:** Því að Mr Doyle hringdi og sagði að þú hefðir ekki verið þar í viku.

</details>

<details><summary>after · G8 · p13official21:test:ema:2944 · F</summary>

**Source:** Chemical, physical and microbiological in-use stability has been demonstrated for 28 days at 2-8°C. Once opened, the product may be stored for a maximum of 28 days at 2°C to 8°C. Other in-use storage times and conditions are the responsibility of the user.
**Semantic decision:** F — All eight corrupt chemical/physical/microbiological in-use stability or user responsibility;6 assigns responsibility to a commission. The28-day/temperature numbers alone are insufficient.
**Candidate 0:** Sýnt hefur verið fram á efnafræðilegt, eðlisfræðilegt og örveruframleiðsluefnaþáttur var þrálát á 28 daga við 2-8°C. Eftir að lyfið er opnað má geyma það í 28 daga við 2°C til 8°C. Önnur geymslutíma og skilyrði fyrir geymslu í notkun er ábyrgð notanda.
**Candidate 1:** Var sýnt fram á efnafræðileg, eðlileg og smitfræðileg stöðugleik fyrir notkun á 28 daga í 2-8°C. Ef lyfið er opnað má geyma það í 28 daga á 2°C til 8°C. Viðbótarviðeitkunir vegna geymslu áfram staðsettar af notendanum.
**Candidate 2:** Eðlilegt efni, eðlileg eða smitvexluaðstæði á innan notkunar hefur verið sýnt fram á 28 daga við 2-8°C, en eftir að lyfið hefur verið opnað má geyma það í að hámarki 28 daga við 2°C til 8°C. Hversu langan geymslu- og þar til viðskipti- tíma er hægt með, og hversu mikil við stofnunstengda hitastigi og þilfari, er ábyrgð notanda.
**Candidate 3:** Stöðugleiki efnislegri, eðlisfræðilegri og örverufræðilega væntingaraðstæðunnar hafa verið sýnt fram á 28 daga við 2-8°C. Eftir að lyfið er opnað má geyma það í hámarksgildi 28 daga við 2°C til 8°C. Aðrir gildi viðgenginna geymslu við notkun eiga aðalstjóri notanda.
**Candidate 4:** Erfildnir efnislegar, eðlisflokka og svepparfræðilegar varanleiki hafa verið sýnt fram á 28 daga við 2-8°C. Eftir að lyfið hefur verið opnað má geyma það í hámarkshraðanum 28 daga við 2°C til 8°C. Aðra geymsluþol og skilyrði þess er ábyrgi notanda notandanlegra.
**Candidate 5:** Einnig hefur verið sýnt fram á efnisfræðilegu, efnafræðilega og líffræðilega stöðugleika í notkun á 28 daga við 2-8°C. Geymið skal hafa að endanlega 28 daga við 2°C til 8°C eftir að lyfið er opnað. Ákveðnir geymslu- og geymslu- ástandi notanda eiga að höndum.
**Candidate 6:** Sýnt hefur verið fram á efnisfræðilegur, eðlisfræðilegur og vefjaskynið stöðugleika aðsýnilegra geymslunnar í 28 daga við 2-8°C. Að opnað er það má geyma lyfið í hámarkshluta 28 daga við 2°C til 8°C. Framkvæmdanefndin er ábyrgð á öðrum geymsluþolum og skilyrðum innan geymslu.
**Candidate 7:** Erfitt er í samsvara við efnisfræðilega, eðlisfræðilega og sýlumótefnafræðilega notkun, að því er varðar tiltekin 28 dagar við 2-8°C. Eftir að lyfið hefur verið opnað má geyma það í hámarkshluti 28 daga við 2°C til 8°C. Önnur geymsluþol og -skilyrði eru ábyrgð notanda.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:3404 · P</summary>

**Source:** A mother never gives up on her child.
**Semantic decision:** P — Mother never giving up on her child retained despite imperfect idiom.
**Candidate 0:** Mamma gefur aldrei upp á barni sínu.

</details>

<details><summary>before · G8 · p13official21:test:eso:1069 · F</summary>

**Source:** By using the SPHERE instrument on ESOs Very Large Telescope (VLT) - one of the most powerful planet-hunting instruments in existence - the international team has made the first robust detection of a young planet, named PDS 70b, cleaving a path through the planet-forming material surrounding the young star.
**Semantic decision:** F — All corrupt robust detection, powerful planet-hunting qualification or path through planet-forming material.
**Candidate 0:** Með notkun SPHERE mælitæknisins á Very Large Telescope (VLT) ESO, sem er einn af öflugustu mælitækninum til að finna reikistjörnur, hafnar alþjóðlegur hópurinn fyrstu koma fram þjóðarafurðir að fara í gegnum hringringar sem reikistjörnur eru með fyrirbyggjandi efni í kringum þessa ungasta stjörnu.
**Candidate 1:** Samkvæmt notkun SPHERE mælitækisins á Very Large Telescope ESO (VLT) - einni af þeim mesti kröftugu mælitækjum sem liggja á milli í alheimsins - hefur alþjóða hópurinn gert fyrstu rannsókn á ungbirtu jörðu, nétt nöfnun PDS 70b, í gangi um jörðu- myndunarmat sem snýst um unnu stjörnu.
**Candidate 2:** Með notkun SPHERE tækninu á Very Large Telescope (VLT) ESO - einkennistæklisins eftir fyrstu sterkustu greiningu á unga reikistjörnu, PDS 70b, hefur alþjóðlegur hópur gert fyrstu álykt á hana.
**Candidate 3:** Með notkun SPHERE mælitækisins á Very Large Telescope (VLT) ESO, sem er einn af blönduðum mælitæki sem notuð er til að reyna á reikistjörnum - hefur alþjóðalegt hópurin gert fyrstu skallega grein fyrir unga reikistjörnuðann PDS 70b og hafði að skugga um efnið sem umhverfur og byggir á um á unnu stjörnuna.
**Candidate 4:** Með notkun SPHERE mælitækisins á Very Large Telescope (VLT) ESO hefur alþjóðlegur hópurinn gert fyrsta þyngra undirgreinanlegan greiningu á ungar aðfeldi, númer PDS 70b, og koma í gegnum fyrirhlið aðfeldisins í kringum unga stjörnuna.
**Candidate 5:** Með notkun SPHERE tækninu á Very Large Telescope ESO (VLT) - einar hæst vetrarbrautaskoti vetrarbrautanna sem liggja á sér - hefur Alþjóðasamfélkið kjaftð aðalfélagið áður á unga veg í barnartraustu PDS 70b sem berst um kringum unna stjörnuna.
**Candidate 6:** Með notkun SPHERE mælitækisins á Very Large Telescope (VLT) ESO - sem er einn af stærstu sártibúnaði til að taka sjón fyrir heimsjóða - hefur alþjóðalegur hópurin gert fyrstu þræðilega greiningu á ungar heimsjóð, núnan PDS 70b, sem snúaði á gangi úr sviði mörkuðu fyrirbyggjandi efnisins kring umhverfið um rjótt stjörnunni.
**Candidate 7:** Með notkun SPHERE mælitækisins á Very Large Telescope (VLT) ESO - annarri sætasta mælitækisins til að finna reikistjörnur - hefur alþjóða hópurinn, nýtt fyrstu áhrifar á það yngri reikistjörnu, nýtt neinu, nöfnuð PDS 70b, í korninu um um um borgun af byggjandi efninu af reikistjörnunni.

</details>

<details><summary>after · greedy · p13official21:test:eea:1965 · P</summary>

**Source:** After paragraph 97B, paragraph 97C is added.
**Semantic decision:** P — Correctly adds paragraph97C after97B.
**Candidate 0:** Eftir 97B-lið bætist við lið 97C.

</details>

<details><summary>after · greedy · p13official21:test:eea:879 · F</summary>

**Source:** If more than one water source is utilised for fish production, fish representing all water sources must be included for sampling.
**Semantic decision:** F — Fish representing all water sources becomes fish that are all the water stations, corrupting the representation relation.
**Candidate 0:** Ef fleiri en einn vatnsstofa er notaður til að framleiða fiski verður að taka sýni úr fiskum sem eru allar vatnsstofurnar.

</details>

<details><summary>before · greedy · p13official21:test:eso:329 · F</summary>

**Source:** The experiment marks the first time that APEX has taken part in VLBI observations, and is the culmination of three years hard work at APEXs high altitude site on the 5000-metre plateau of Chajnantor in the Chilean Andes, where the atmospheric pressure is only about half that at sea level.
**Semantic decision:** F — Culmination becomes repetition, and atmospheric pressure becomes an invented air-whiteness term.
**Candidate 0:** Framkvæmdin er fyrsta sinn sem APEX hefur taka þátt í VLBI mælingum og endurtekið þriggja ára vinnu á hægri stöðu APEX á 5000 metra hæði Chajnantors á Andes fjallunni í Chile, þar sem lofthvítur er aðeins um hálftil þess sem á hafihæði.

</details>

<details><summary>before · G8 · p13official21:test:eso:179 · F</summary>

**Source:** These violent explosions rip through the molecular gas clouds in their immediate surroundings, but after the shockwaves have travelled more than about ten light-years they are weaker, and may instead compress clouds that are a little further away, triggering the formation of new generations of stars.
**Semantic decision:** F — All corrupt molecular clouds/shockwave weakening or farther-cloud compression triggering stars.
**Candidate 0:** Þessi rauði sprengingar brjóta í rauði geimvökum í nálægt umhverfi, en eftir að hryggjaröndum hafa flutt þær meira en um tíu ljósára breytir eru þær vægar og geta þess vegna þá rauði geimvökum sem eru stutt fyrir, hlauparaðar á nýju ævindrömur úr stjörnum.
**Candidate 1:** Þessi ömurlegar sprengingar sérstaklega beinu þéttum gaskúlum í nálægri umhverfi þeirra, en eftir að skjálftabláinum hefur fara meira en um tíu ljósára færrar eru þær vægari, og geta þá þess að þrýsti það í slíkir hófar sem eru stuttar fyrir er, olli þau að myndi framleika nýrrar ævi stjarna.
**Candidate 2:** Þessi erfiðir sprengingar skola fyrir efnisgaslegar loftniður í nálægum umhverfi sínu, en eftir það að skjölmálum hafa farið í meira en um tíu ljósára er þær stærri og geta þar af leiðandi styttri loftnámi sem eru næstum lengur en það, sem hefur það hvarfefni myndun nýrra ástanda stjarna.
**Candidate 3:** Þessi veruleg afblæðing hlaup hraða alls undir þær stunguhringar sem eru í umkringlum svæðum en eftir að þær hlaupar hraðir hafa komið fram yfir um árum eru þær eins styttri og geta þó því komið til þess að þrýstir einhverjar skýir sem eru í frikum, og því geta þau indráttar nýra fæðuna stjörnur.
**Candidate 4:** Þessi sáramjögnur leggja undir kúnaþokum og eru því að vinna eftir að skerðingar hafa farið meira en um tíu ljósára, ættar þeir því að skrýða hliðsjónsskaða sem eru fyrir um um það bil þar sem þeim verður að hraða upp nýjar starfi.
**Candidate 5:** Þessar rauða sprengingar skapa skímmur um umhverfisglæði í nálægt svæði, en eftir að skjaldnir eru mikið langt um tíð sem vísi um eina títandi ljósáranum eru þær værir öðruvísi kræftar og geta gera það hryðjá á um umhverfisglæði sem eru lítið færri burt, að hlaupi úr því myndun nýjar æðagrennna.
**Candidate 6:** Þessir alvarlegar sprengingar koma í gegnum mótvega gasglönn og þær komna þá að strax en skeljum þeirri stjörnum tíðbreytingum en þegar skeljungur hefur farið frekar en um tíu ljósára þá eru þær styttr og geta í stað bittið nýgátir af lofti sem eru stuttar til staðar og hefur þá hátt áhrif á myndun nýu árafjölda stjarna.
**Candidate 7:** Við þessi kraftaverk eru þess arðbergir gert í það gáttu í líkamlega gasmyndum í íbúgildi þeirra en eftir að óhömmunarkræfir hafa farið yfir í meira en um tíu ljósára er þeir vægar og hægt er í stað að þrýstir þeim sem eru í nærri þátt og löguðu þeim, að því er varðar myndun nýrra æxlisflokka.

</details>

<details><summary>after · G8 · p13official21:test:ema:3025 · U</summary>

**Source:** Based on individual patient response and tolerability, the dose may be increased to 300 mg (15 ml) per day after an interval of 3 to 7 days, and if needed, to a maximum dose of 600 mg (30 ml) per day after an additional 7-day interval.
**Semantic decision:** U — Candidate6 preserves response, tolerability, doses and maximum, but the additional7-day interval is not explicit. Other variants lose the maximum or corrupt patient response, so no fully certified dosing candidate.
**Candidate 0:** Á grundvelli áhrifa hverja sjúklings og þols má auki skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga fresti og þegar þörf krefst, í 600 mg (30 ml) á dag eftir viðbótar 7 daga fresti.
**Candidate 1:** Bundinu viðvörun sjúklingsins og þola má auka skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga tímabili, og ef þörf er á að bæta skammtinn í 600 mg (30 ml) á dag eftir viðbótarsöfnun á sig 7 daga.
**Candidate 2:** Bundnuð gegn það hátt hvað viðkomandi sjúklingur sér og þoli, má auka skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga fresti, en ef þörf er á að stafa það innan við hámarksskammtinn 600 mg (30 ml) á dag eftir viðbótarmiða 7 daga fresti.
**Candidate 3:** Bundinn á svið sjúklingarráðbendingar og þolanleika er hægt að auka skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga frest og, ef þörf krefur, í 600 mg (30 ml) á dag eftir 7 daga fresta.
**Candidate 4:** Á grundvelli þess hversu jóklega hafa sjúklingar sérstaðað svörun og þolað skammtinn má auka í 300 mg (15 ml) á dag eftir 3 til 7 daga hávaða, ef þörf er á að auka skammtinn í 600 mg (30 ml) á dag eftir 7 daga hávaða.
**Candidate 5:** Bundið á því að því sem þátttakandi sjúklingur sér um hjálfu og því að það þolir það getur aukið skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga fresti, og ef þörf er á að auka skammtinn getur verið aukið í 600 mg (30 ml) á dag eftir fresti í 7 daga.
**Candidate 6:** Byggt á svörun hjá einstaklingum og þolanleika er hægt að auka skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga tímabili og, ef þörf krefur, í hámarksskammtinn í 600 mg (30 ml) á dag eftir 7 daga tímabili.
**Candidate 7:** Í ljós sjúklingarsvörun og þol má auka skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga tímabili og ef þörf er á að auka skammtinn í 600 mg (30 ml) á dag eftir frekari 7 daga tímabili.

</details>

<details><summary>before · G8 · p13official21:test:eso:45 · P</summary>

**Source:** This would make the system similar to our Solar System in terms of the number of planets (seven as compared to the Solar Systems eight planets).
**Semantic decision:** P — Candidate6 preserves similarity to our Solar System by planet count, seven versus eight. The malformed similarity adjective must receive the same treatment as the semantically equivalent after-model candidate6.
**Candidate 0:** Þetta myndar á kerfinu jafnvægi sólarkerfinu í því skyni að aðfærðirnir eru sá fær og sólarkerfinu tveggja mánaðarins.
**Candidate 1:** Það myndi gera kerfið sambærilegt úr sólarkerfinu, í þáttum fjarstæða (sjö geimfara í samanburði við átta fjarstæðum úr sólarkerfinu).
**Candidate 2:** Þetta myndar kerfið svipað á sólkerfinu okkar í skömmtum fyrir fyrirbæri fyrir fjölda reikistjarna (sjö miðað við átta reikistjörnurnar í sólkerfinu).
**Candidate 3:** Þetta myndi skaðað kerfið eins og sólarkerfið okkar í því skyni að fjölda reikistjarna (símað við aðalrök stóra sólarkerfisins).
**Candidate 4:** Þetta myndi gera kerfið svipaði á sólkerfinu og hefur sama fjölda reikistjarna (sjö af miðjunum við eights reikistjörnur í sólaæðinu).
**Candidate 5:** Þetta myndi benda stöðina til sólarkerfinu í skyninu hvað varðar fjölda reikistjarna (sjö fyrir sig samanborið við fyrir sig eigndreifin af sólarkerfinu).
**Candidate 6:** Það myndi geri kerfið svipufram á sólkerfinu okkar í þeim þáttum sem um getur um fjölda reikistjarna (sjö þegar samanborið við átta reikistjarna í sólarkerfinu).
**Candidate 7:** Það myndar saman kerfinum við sólarkerfið í skömmtum fjölda reikistjarna (sjö, samanborið við átta reikistjörnurnar í sólarkerfinu).

</details>

<details><summary>after · greedy · p13official21:test:eso:179 · F</summary>

**Source:** These violent explosions rip through the molecular gas clouds in their immediate surroundings, but after the shockwaves have travelled more than about ten light-years they are weaker, and may instead compress clouds that are a little further away, triggering the formation of new generations of stars.
**Semantic decision:** F — Molecular clouds become bodily clouds and compressing distant clouds is lost; star formation alone is insufficient.
**Candidate 0:** Þessi öflugir sprengingar rífa í gegnum líkamlega gasský í náttúrunni þeirra en eftir að skjálftan hefur farið meira en um tíu ljósára er þær vægari og geta þó þegar komið úr þeim þokum sem eru stutt fjarlægri og hvetja upp nýjar ævihóp stjarna.

</details>

<details><summary>before · G8 · p13official21:test:eso:514 · P</summary>

**Source:** This star formation region is forming many stars.
**Semantic decision:** P — Candidate5 retains star-forming region forming many stars; case/voice agreement is rough but entities and process clear.
**Candidate 0:** Þessi vetrarbraut verður fjöldi stjarna.
**Candidate 1:** Við skýrfjöldinum eru enn mörg stjörnur búin til að mynda.
**Candidate 2:** Þessi stjörnumyndunarféluga myndast mörg stjörnur.
**Candidate 3:** Þessi stjörnumyndunarsvæði myndast marga stjörnur.
**Candidate 4:** Þennan stjörnufrumuhópi myndast margir stjörnur.
**Candidate 5:** Þetta stjörnumyndunar svæði myndast mörg stjörnur.
**Candidate 6:** Einnig eru mörg stjörnur úr þessum myndunarlaga.
**Candidate 7:** Þessi stjörnumyndunarsvæði myndast mörg stjörnur.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:1317 · F</summary>

**Source:** General Barnicke's gone until tomorrow morning.
**Semantic decision:** F — Absence until tomorrow morning replaced by going back.
**Candidate 0:** Barnicke hefur farið til baka.

</details>

<details><summary>before · greedy · p13official21:test:ema:129 · F</summary>

**Source:** Clinical studies have demonstrated that ProQuad can be given simultaneously (but at separate injection sites) with Prevenar and/or hepatitis A vaccine, or with monovalent or combination vaccines comprised of diphtheria, tetanus, acellular pertussis, Haemophilus influenzae type b, inactivated poliomyelitis, or hepatitis B antigen.
**Semantic decision:** F — Several vaccine antigens, including diphtheria/pertussis/polio, are invented or corrupted terms.
**Candidate 0:** Klínískar rannsóknir hafa sýnt fram á að ProQuad má gefa samhliða (en í mismunandi stungustöðum) með Prevenar og/eða lifrarbóluefni gegn lifrarbólgu A eða einstök eða samsetta bóluefni sem innihalda dýpkransa, tétanus, ófrumna kútusótt, Haemophilus influenzae tegund b, óvirkjaða mænirétta eða lifrarbólgu B mótefni.

</details>

<details><summary>after · G8 · p13official21:test:eso:1138 · F</summary>

**Source:** “Terrestrial planets similar to our Earth are obvious targets for the search for life outside the Solar System, while comets are suspected to have played an important role in the appearance and development of life on our planet,” adds his colleague Emmanuël Jehin, who leads the cometary part of the project.
**Semantic decision:** F — All eight corrupt terrestrial planets and/or comets and the project-lead role, losing the stated life-search and cometary-development contrast.
**Candidate 0:** „Terrosæjum eins og Þjóðvarinu eru óhöfðilegar markmið fyrir leitir í lifi utan sólarverjar en hásvikum telst að karmi hafi hafa mikilvæga þátt í útlægð og þróun lífis á plannettunni okkar,“ bætir Emmanuël Jehin, ráðgjafengi verkefnisins, við aðgerðina með hásvikum.
**Candidate 1:** „Já, landþjálfar sem eru svipuð úr öllum er auðveldlega meginstöðvar leitunar lífs utan sólkerfinu, en í þrýstingi fyrir mér getur fuglakos verið að hafa tekið mikilvægar hlutdeild í því að líf verði upp og þyngsleit á jörðunni,“ sagði ráðhammanum hans, Emmánuele Jehin, sem stjórnar hluti verklingskosti verkefnisins.
**Candidate 2:** „Rýmki sem líka eru við úr öllum rýmkinu eru óhuguðum markmiði í leitir yfir lífi utan sólkerfisins, en kyrningar eru grunur á að hafa hafa mikilvæga þátt í því að fæddist og þróast lífi á okkur reikistjarnanum,“ bætir Emmanuël Jehin, ráðgjafan hans, við samstarfsverkefninni, við kyrpingarhvarfana.
**Candidate 3:** „Jafnframt er greinileg markaður í leitunum á líf í utan sólaþyrpingar, en á fimmtarænnum beltum er hugtak til þess að þeir hafi haft mikilvæga þátt í útgáfu og þróun lífs á okkar vetrarbraut,“ bætir Emmanuël Jehin samstarfsaðili hinn við bæturverkefninu við að velja með beltum.
**Candidate 4:** „Hliðstæður fyrir leit á lifur utan sólarveranda er sýnt greinilega þyngdarverur sem líkast hafa lífi, en svo er grunur á að reykjum hefur verið mikilvægar þátttakir í þeirri myndun og vaxt lifa á þessari reikistjörnu,“ bætir Emmanuël Jehin, hinur vini um reykja verkefnið, til viðvarandi.
**Candidate 5:** „Planeterar sem líka hafa fyrir sig í hliðsjón sjálfvítanirum til að leita lífs utan sólkerfin er og sprengjuskor kanni að hafi haft mikilvæg árangurstöðu við færingu og þróun lífs á áin okkar,“ bætir Emmanuël Jehin samengenda-efndinn hans við niðurstöðuna um sprengjuskor.
**Candidate 6:** „Tjarna vegra fyrir að vinnsluskerfum gætu verið dýrakveðið, en ristireiðar eru grunur um að hafi haft mikilvægan þátt í því að lífið hefur myndast og þróast á jörðinni,“ bætir upp Emmanuël Jehin í hluta meðal, sem stjórnaði ristireiðarins á verkefninu.
**Candidate 7:** „Hljóðandi markmiður við leitina á lífinu reikistjörnum sem líka líkjast öllum okkar jörðum eru fjölskylda reikistjörnur, en plöntur hafa líklegt verið markvægu hlutverki í áætlununum um hliðstæðustjörnustöfun og þróun lífs á okkar reikistjörnum,“ bætir Emmanuël Jehin samfélagið, dráttur með reikistjörnunum, við verkefnið.

</details>

<details><summary>before · greedy · p13official21:test:eso:714 · F</summary>

**Source:** By studying this effect it is possible to map out the places where gravity is strongest, and hence where the matter, including dark matter, resides.
**Semantic decision:** F — Strongest gravity becomes largest area; mapping relation corrupted.
**Candidate 0:** Með þessari rannsókn er hægt að mynda út staðir þar sem svæðið er stærsti og því þar sem efnið, þar með talið dökk efni, er.

</details>

<details><summary>after · G8 · p13official21:test:eso:716 · F</summary>

**Source:** From the gravitational lensing effect, these groups turn out to contain around 30 times more dark than visible matter.
**Semantic decision:** F — All eight corrupt the lensing inference and/or dark-versus-visible matter comparison; the copied English term in6 does not rescue the garbled ratio/object.
**Candidate 0:** Frá slæmhæfa myndun stuttar þessi hópar eru um 30 sinnum tekið daufri en sýnilegu efni.
**Candidate 1:** Frá rauðliglæsingu kemur úr þessu að þessar hópar innihaldi um 30 sinnum meiri þurrar en útfallir.
**Candidate 2:** Í gegnsviknumagalausningu, skal sjón af þessum hópum að þeir innihaldi um 30 sinnum meira dýru en sýnilegt efnis.
**Candidate 3:** Frá andstræna glerlækkandi áhrifum verða þessi hópar í samanstandandi 30 sinnum meira duft en séðan fyrir.
**Candidate 4:** Af fjölda gildandi myndunarafstöðvar verða þessar hópur ná yfir að innihalda um 30 sinnum meira dökku en litsyfri efnin.
**Candidate 5:** Í ljósreglukringu sem gengur í ljós eru þessi hópar um 30 sinnum meiri dýr og mjög djúp um síðan heimilt út.
**Candidate 6:** Frá því að það er þegar mjög svæga (gravitational lensing) þjóðirnar eru í kringum 30 þrjá meiri dýgari en litanlega efni.
**Candidate 7:** Af geimfrumnæmi sem styrkir lentein, upplýst hóparnar í um það bil 30-föld meiri dunkanar en sýnilegar efnin.

</details>

<details><summary>before · G8 · p13official21:test:eso:1100 · F</summary>

**Source:** The combination of images taken by three exceptional telescopes, the ESO Very Large Telescope on Cerro Paranal , the MPG/ESO 2.2-metre telescope at ESOs La Silla observatory and the NASA/ESA Hubble Space Telescope, has allowed the stunning Jewel Box star cluster to be seen in a whole new light.
**Semantic decision:** F — Every candidate changes telescope number, JewelBox identity, instrument/site details or seeing-in-new-light relation;5 introduces denial.
**Candidate 0:** Samsetningu myndanna sem tveggja skilgreindir sjónaukar gefa til, Very Large Telescope (ESO) í Cerro Paranal, MPG/ESO 2,2 metra sjónaukann í La Silla stjörnustöð ESO og Hubble geimsjónaukinn NASA/ESO, hefur leitt til sérstakrar litningar onnir.
**Candidate 1:** Samsetningu myndirnar, sem tveggja sjónauka ESO Very Large Telescope á Cerro Paranal, MPG/ESO 2,2-metrar sjónauka í La Silla stjörnustöð ESO og NASA/ESA Hubble geimflutningssjónauka hafa lauk í stórum þáttum að sjá svona kyrrt og fetu bæjar stjörnuþyrpingu sem er nýtt hjá ný.
**Candidate 2:** Þessi samsetta myndir úr fjörum óvenjulegum sjónauka, Very Large Telescope ESO á Cerro Paranal, MPG/ESO 2,2 metra sjónauka í La Silla stjörnustöð ESO og NASA/ESA Hubble geimstjörnu, hafa gert kleift að sjá stútt í nýju ljósi rauðbyssavirkja stjörnuþyrpingunni.
**Candidate 3:** Samsetning ámyndanna, sem tveggja stökkbreyta sjónauka tóku afkerða, Very Large Telescope ESO í Cerro Paranal, MPG/ESO 2,2 metra sjónauka á La Silla stjörnustöð ESO og Hubble geimstjörnustjórnunarstofnunar NASA og ESA, hefur gert kleift að sjá hvarfefna stjörnueyðið Jewel Box.
**Candidate 4:** Sjónaukorna sem lokuð hafa sú glæsilega Jewel Box stjörnuþyrpingin, sem ESO Very Large Telescope á Cerro Paranal, MPG/ESO 2,2-metrar sjónaukanin á La Silla stjörnustöð ESO og NASA/ESA Hubble geimfarsjónaukanin, hefur leitt í ljós að ný.
**Candidate 5:** Sjónauka á þremur skilgreindum sjónauka, Very Large Telescope ESO á Cerro Paranal, MPG/ESO 2,2 metra sjónauka í La Silla stjörnustöð ESO og Hubble geimfarsrétta NASA/ESAs, hafa hafnað því að sjónaukinn í Jewel Box stjörnufalinn séð í öllu nýjum ljósi.
**Candidate 6:** Samsetningu myndirnar sem fyrirhugaðar sjónaukar borið hafa reið á, Vélaráktengið ESO í Cerro Paranal, MPG/ESO 2,2 mítna sjónaukanum í La Silla stjörnustöð ESO og NASA/ESO Hubble geimsjónaukanum hafði gert kleift að sjá Stíkuríkju stjörnuþyrpinguna í nýju ljósi.
**Candidate 7:** Samhliða myndir úr þremur undanteknum stjörnustofnum ESO Very Large Telescope á Cerro Paranal, MPG/ESO 2,2-metra stjörnustjörnin í La Silla stjörnustöð ESO og NASA/ESA Hubble geimsjónaukinni, hafa leitt til þess að sýna stjörnulokaðartýrunin inntöku í nýju ljósi.

</details>

<details><summary>before · G8 · p13official21:test:ema:2183 · F</summary>

**Source:** For intravenous use, infusion systems with Actrapid at concentrations from 0.05 international unit/ml to 1.0 international unit/ml human insulin in the infusion fluids 0.9% sodium chloride, 5% dextrose and 10% dextrose inclusive 40 mmol/l potassium chloride using polypropylene infusion bags, are stable at room temperature for 24 hours.
**Semantic decision:** F — Every candidate changes potassium chloride to sodium chloride or invented salt, or loses critical solution/stability details.
**Candidate 0:** Fyrir innrennslisnotkun eru innrennslisfyrirtæki með Actrapid á styrk frá 0,05 alþjóðlegu eining/ml til 1,0 alþjóðlegu eining/ml af mannainsúlíni í innrennslisvökva 0,9% natríumklóríð, 5% drexsúlósi og 10% drexsúlósi, þar með talið 40 mmól/l kórtilklóríð í innrennslisflögunum með pólýprópýlen innrennslisútblöðum, stöðug fyrir 24 klst.
**Candidate 1:** Fyrir gjöf í bláæð, innrennsliskerfi sem innihalda Actrapid með styrk frá 0,05 evrópsk/ílínúmsvörun/ml til 1,0 evrópsk/ílínúmsvörun/ml manna insúlíns á innrennslisrás 0,9% natríumklóríð, 5% dextros og 10% dextros, að meðtöldu 40 mmol/l natríumklóríð með pólýprópýlen innrennslibösur, eru stöðug á stofuhita í 24 klst.
**Candidate 2:** Fyrir notkun í bláæð, innrennslissjónavélar með Actrapid með styrk frá 0,05 alþjóðlegum einingum/ml til 1,0 alþjóðlegum einingum/ml af manna insúlíni í innrennslisvatni 0,9% natríumklóríð, 5% dextrosi og 10% dextrosi, í samhliða 40 mmol/l natríumklóríð, með pólýprópýlen innrennslisúrnautum, eru stöðugar við hemilstig í 24 klukkustundir.
**Candidate 3:** Fyrir notkun með innrennslisverkju, geymslurör um Actrapid með styrk frá 0,05 evrópskum einingum/ml til 1,0 evrópskum einingum/ml af insúlíni úr mönnu í innrennslitengdum vökva 0,9% natríumklóríð, 5% dextros og 10% dextros, með hugsanlega 40 mmól/l natríumklóríð, á 24 klst. stað við stofuhita.
**Candidate 4:** Fyrir innrennslisnot: innrennsliskerfi með Actrapid í styrk frá 0,05 alríkis eining/ml til 1,0 alríkis eining/ml af mannainsúlíni í innrennslisinu 0,9% natríumklóríð, 5% dextros og 10% dextros, þar með talið 40 mmól/l natríumklóríð, í pólýprópýlens innrennslispakkningum, eru stöðugir við stofuhita í 24 klukkustundir.
**Candidate 5:** Til notkunar í æð, innrennslistengd með Actrapid í þéttni frá 0,05 evrópskum einingum/ml til 1,0 evrópskum einingum/ml af mannainsúlíni í innrennslisvökva 0,9% natríumklóríð, 5% dextrosa og 10% dextrosa, með 40 mmol/l kútríumklóríð, á 24 klukkustundum við stofuhita, er stöðugur.
**Candidate 6:** Fyrir notkun í bláæð, innrennsliskerfi með Actrapid í þéttni frá 0,05 evrópskri eining/ml til 1,0 evrópskri eining/ml af mansinsúlíni í innrennslisfluðunum 0,9% natríumklóríð, 5% dextros og 10% dextros, þar með talið 40 mmól/l natríumklóríð, sem nota á pólýprópýlen innrennslislögunum, eru stöðug á stofuhita í 24 klukkustundir.
**Candidate 7:** Fyrir gjaf í bláæð notuðar innrennslisstykki með Actrapid með styrkleika frá 0,05 einstök eining/ml til 1,0 einstök eining/ml af mannainsúlíni í innrennslisflókinu 0,9% natríumklóríð, 5% dextros og 10% dextros, tæknilegur, 40 mmól/l natríumklóríð, með pólýprópýleninnrennsliskörfum, eru stöðugir við stofuhita í 24 klukkustundir.

</details>

<details><summary>before · G8 · p13official21:test:eea:1323 · F</summary>

**Source:** If refills are not provided, the weight of the total primary packaging shall not exceed 3,7 g per wash for tablets and 1,7 g per wash for all other products.
**Semantic decision:** F — All corrupt refills/primary packaging or per-wash quantity units.
**Candidate 0:** Ef ekki er tilfullt að gefa endurnýjunum skal þyngd heildarfræðilegra umbúða ekki vera meiri en 3,7 g til úthreinsunar, handa töflum og 1,7 gr/ úthreinsun handa öðrum lyfjum.
**Candidate 1:** Ef fylgikerfi ekki eru til boði skal ekki vera meira en 3,7 g á heildarförun í hreinun fyrir töflur og 1,7 g á hreinun fyrir öll önnur afurð.
**Candidate 2:** Ef ekki er veitt uppsetningar skal þyngd heildarfylgsins ekki fara yfir 3,7 g til útbrotunar á hverri lykja af töflum og 1,7 g til útbrotunar á öllum öðrum lyfjum.
**Candidate 3:** Ef endurtekinn skammtur er ekki veitt skulu þyngdar hluti öllra hefðbundna umbúða ekki vera stærri en 3,7 gr/þvag fyrir töflur og 1,7 gr/þvag fyrir öllu öðrum vörum.
**Candidate 4:** Ef ekki er útgefandi endursetningar skal hægður heildarfyrirbærlisums pakkningar ekki vera meiri en 3,7 g í hverjum þvagrindi fyrir töflur og 1,7 g í hverjum þvagrindi fyrir allar önnur lyf.
**Candidate 5:** Ef meir tilbúinum afbúnum er ekki tilfyltur, má ekki vera meira en 3,7 gr/ryk fyrir töflur og 1,7 gr/fjölda gráðu fyrir önnur vörur.
**Candidate 6:** Ef tilbætur eru ekki veittar skal vigt heildarfræðilegra umbúða ekki vera meira en 3,7 g í hverjum þurrfæðu fyrir töflur og 1,7 g í hverjum þurrfæðu fyrir öll aðra vara.
**Candidate 7:** Ef ekki er fylgt við endurtekna af lyfjagjöfum, skal þyngdar hluta heildarfráselds ekki vera meiri en 3,7 g hver ríma með töflum og 1,7 g hver ríma með öðrum lyfjum.

</details>

<details><summary>after · greedy · p13official21:test:ema:129 · F</summary>

**Source:** Clinical studies have demonstrated that ProQuad can be given simultaneously (but at separate injection sites) with Prevenar and/or hepatitis A vaccine, or with monovalent or combination vaccines comprised of diphtheria, tetanus, acellular pertussis, Haemophilus influenzae type b, inactivated poliomyelitis, or hepatitis B antigen.
**Semantic decision:** F — Diphtheria and acellular pertussis names are replaced by corrupt terms including smoking; the vaccine list is not preserved.
**Candidate 0:** Klínískar rannsóknir hafa sýnt fram á að ProQuad má gefa samhliða (en í mismunandi stungustaðum) með Prevenar og/eða bóluefni gegn lifrarbólgu A eða einstökum eða samsetnum bóluefnum sem innihalda dópkerfisbólgu, tétansúsbólgu, ófrumku kíghálsareykingu, Haemophilus influenzae tegund b, óvirkri mænusótt eða lifrarbólgu B mótefninu.

</details>

<details><summary>after · greedy · p13official21:test:ema:2175 · P</summary>

**Source:** Breast-feeding must be stopped on initiation of treatment with Voriconazole Accord.
**Semantic decision:** P — Correctly requires stopping breast-feeding when Voriconazole Accord treatment begins.
**Candidate 0:** Hætta verður brjóstagjöf þegar meðferð með Voriconazole Accord hefst.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:1121 · P</summary>

**Source:** Of course you're right, Starling... but it doesn't change anything.
**Semantic decision:** P — You are right and it changes nothing retained; malformed opening is grammatical/style noise.
**Candidate 0:** Að mikið er þú rétt, Starling... en það breytir ekkert.

</details>

<details><summary>after · greedy · p13official21:test:eso:349 · P</summary>

**Source:** The results described here use some of these Science Verification data.
**Semantic decision:** P — Retains that the results described here use some Science Verification data; inflections are awkward.
**Candidate 0:** Niðurstöðurnar sem hér er lýst nota einhverjar af þessum gögn um vísindalegt sannprófun.

</details>

<details><summary>before · G8 · p13official21:test:ema:1495 · P</summary>

**Source:** Check again to make sure the correct dose of Tevagrastim is in the syringe.
**Semantic decision:** P — Candidates2/3 preserve rechecking correct Tevagrastim dose in syringe.
**Candidate 0:** Athugaðu á ný og sjá að réttur skammtur af Tevagrastim sé til staðar í sprautunni.
**Candidate 1:** Athugaðu aftur að vísa á að réttur skammtur af Tevagrastim sé fyrir hendi í sprautunni.
**Candidate 2:** Athugaðu aftur til þess að tryggja að réttur skammtur af Tevagrastim sé í sprautunni.
**Candidate 3:** Athugaðu aftur til að tryggja að réttur skammtur af Tevagrastim sé í sprautunni.
**Candidate 4:** Skoðaðu aftur til að tryggja að rétta skammtur af Tevagrastim sé í sprautunni.
**Candidate 5:** Skoðið aftur að talin sé réttur skammtur af Tevagrastim í sprautunni.
**Candidate 6:** Athugaðu aftur til að sjá að réttur skammtur af Tevagrastim sé í sprautunni.
**Candidate 7:** Komið aftur og gætið úr skugga um að réttur skammtur af Tevagrastim sé í sprautunni.

</details>

<details><summary>after · greedy · p13official21:test:ema:2690 · F</summary>

**Source:** Adverse effects not observed in clinical studies but seen in the rat and to a lesser extent in the mouse at exposure levels similar to human exposure levels and with possible relevance for clinical use were liver changes, indicating an adaptive response such as increased weight and centrilobular hypertrophy, fatty infiltration and increased liver enzymes in plasma.
**Semantic decision:** F — Adaptive response becomes persistent response and centrilobular hypertrophy becomes pressure; fatty infiltration is also corrupted.
**Candidate 0:** Aukaverkanir sem ekki komu fram í klínískum rannsóknum en komu fram hjá rottum og mjög minni leyti hjá músum við útsetningu sem var svipuð útsetningu fyrir menn og hafa hugsanleg áhrif á klíníska notkun voru breytingar á lifur, sem benda til þess að það sé þrálátur svörun eins og aukin þyngd og þrýsting í miðlópu, fitusvæfni og aukin lifrarensím í blóði.

</details>

<details><summary>before · greedy · p13official21:test:ema:3025 · F</summary>

**Source:** Based on individual patient response and tolerability, the dose may be increased to 300 mg (15 ml) per day after an interval of 3 to 7 days, and if needed, to a maximum dose of 600 mg (30 ml) per day after an additional 7-day interval.
**Semantic decision:** F — Maximum600mg constraint omitted; additional-interval qualification not explicit.
**Candidate 0:** Bundin þar sem tilgreind er svörun og þol sjúklings er metið má auka skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga fresti og ef nauðsyn krefur í 600 mg (30 ml) á dag eftir 7 daga fresti.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:1803 · P</summary>

**Source:** What are you planning on telling her?
**Semantic decision:** P — Exact source/hypothesis semantic reuse from card85: Question about what to tell her preserved.
**Candidate 0:** Hvað ætlarðu að segja henni?

</details>

<details><summary>before · G8 · p13official21:test:eea:43 · U</summary>

**Source:** Where plant protection products containing the active substance are intended to be used in cold climatic conditions, the tests have to be conducted where DT50lab, determined at 10 °C and at a moisture content of the soil related to a pF value of 2 to 2,5 (suction pressure) is greater than 90 days.
**Semantic decision:** U — Candidate2 retains most conditions/numbers but suction pressure becomes a nonstandard collection-pressure term; cannot certify the technical condition. Others clearly corrupted.
**Candidate 0:** Ef lyf sem vernda plöntu innihaldu virka efnisins eru ætlað til notkunar í kaltum umhverfismatsstöðum, skulu prófanir fara fram í kópum þar sem DT50lab, ákvarðað í 10°C og í mjóðinni í yfirborði til 2-2,5 sýrum (sýrueðli) er meiri en 90 dagar.
**Candidate 1:** Ef notkun á plöntuhemlum sem innihalda virka efni er áhugað fyrir hjálagtum líghraðum aðstæðum, þarf að framkvæma prófunnar þar sem DT50lab, sem ákvörðuð er í 10°C og víðmyndastigi í jarði sem tengist pF gildi 2 til 2,5 (lengingssvefi), er meiri en 90 daga.
**Candidate 2:** Ef um er að ræða notkun plöntuvarnarefna sem innihalda virka efni í kaltum loftsskilyrðum þarf að framkvæma prófanir þar sem DT50lab, sem er ákvarðaður við 10°C og vökvastigi í jörðu sem tengist pF-gildi 2 til 2,5 (safniþrýstingi) er stærri en 90 dagar.
**Candidate 3:** Ef um er að ræða notkun plöntuvarnarefna sem innihalda virka efnin með fyrirvaranum með hárna líffæri á að prófa þau ef DT50lab, á vísanlega 10°C og á vökvaþéttni yfir í jarðæðin sem tengist pF gildi 2 til 2,5 (þrýsting) er að vera meiri en 90 daga.
**Candidate 4:** Ef vörn völdum á plöntum er áhugað til notkunar við kaltikvarða skal framkvæma prófanir þar sem DT50, á 10°C og vökvasityrningu sem tengist pF gildi 2 til 2,5 (sýruþrýstingur), er stærri en 90 daga.
**Candidate 5:** Ef hægt hefur verið að nota plöntuhemjandi vörur sem innihalda virka efnin þar sem það er notað við kalt skýra, skulu mælingar gefnar ásamt þeim þar sem DT50lab, á 10 °C og á rýmubroti sem tengist 2-2,5 (sirkvöðubroti) er meiri en 90 dagar.
**Candidate 6:** Ef flöguðar varnarefni, sem innihalda virka efnið, eru ætlaðir notuð við kæli varnirinnar skal gera prófanir þar sem DT50lab, sem ákvarðað er við 10° C og í vökvalegu þurrði sem tengd er pF gildinum 2-2,5 (útsæðisþrýstingi), er meiri en 90 daga.
**Candidate 7:** Ef lyf, sem innihalda virku efnin, ætlað er að nota við kaltum loftstengdum ástandi, skulu tilraunir gefnar upp ef DT50lab, á 10 °C og með 2 til 2,5 (sýrufjölgunarhlutfall), er meiri en 90 daga.

</details>

<details><summary>after · greedy · p13official21:test:ema:3025 · F</summary>

**Source:** Based on individual patient response and tolerability, the dose may be increased to 300 mg (15 ml) per day after an interval of 3 to 7 days, and if needed, to a maximum dose of 600 mg (30 ml) per day after an additional 7-day interval.
**Semantic decision:** F — Retains the dose numbers but omits the maximum-dose qualification and does not clearly retain an additional interval; these are key dosing constraints.
**Candidate 0:** Bundnuð við svörun og þol sjúklings er hægt að auka skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga fresti og ef nauðsyn krefur í 600 mg (30 ml) á dag eftir 7 daga fresti.

</details>

<details><summary>after · G8 · p13official21:test:eso:611 · F</summary>

**Source:** “With Mars losing that much water, the planet was very likely wet for a longer period of time than previously thought, suggesting the planet might have been habitable for longer,” said Michael Mumma, a senior scientist at Goddard and the second author on the paper.
**Semantic decision:** F — All eight corrupt the habitability inference or wetness/time claim and/or the scientist attribution; several also conflate Mars with Earth.
**Candidate 0:** „Þegar Mars tapaði svona miklu vatni var jörðin líklega lítið útvarpað fyrir lengri tíma en til að átt hefur verið, sem bendir til þess að það þykkist hafa verið hamlandi lengur,“ sagði Michael Mumma, fullkomnari vísindamaður hjá Goddard og annar aðalhöfundur greinarinnar.
**Candidate 1:** „Þegar Mars missti svona vökvi, var jörðin líklega vökva í lengri tíma en það var áður leitt til, sem bendir til þess að átti væri til fósturlandi,“ sagði Michael Mumma, hópi stærsta vísindamanna við Goddard og komnstu að aðra aðalhöfundar greinarinnar.
**Candidate 2:** „Þegar Mars mislisti svo miklu vatni, var reikistjarnan líklega vökvað lengur en gert var ráð fyrir, hvað gæti átt að megi vera búseti fyrir lengur“ sagði Michael Mumma, hópi fundinn í geði við viðkomandi grein.
**Candidate 3:** „Þegar Mars tapar svona mikið vatn verður reikistjarnan líklega vökvi lengur en áður var talið, sem gefur til kynna að reikistjarnan hafi verið færri í lengri tíma en áður“ sagði Michael Mumma, hæfilegur þekkingarstjóri við NASA í Goddard og annar umönnunaraðili á greinarinni.
**Candidate 4:** „Við því að Mars losnaði svæði sínu svo miklu vatn, var fáanlega líkleglegt að jörðin væri vatnsvæna lengur en áður hefur verið greint og það gefur til kynna að það hafi verið fæðuð lengur en í fyrra tímann“ sagði Michael Mumma, frá Goddard og annar hluthafandi aðallshöfundur greinarinnar.
**Candidate 5:** „Þegar Mars tapast um það mikið af vatni var líður hafði hún líka vísi í lengri tíma en áður var talið, sem bendir til þess að lítillega væntir væntaði hlutaðeigandi svæði á vetrarbrautinu,“ sagði Michael Mumma, hópnum sáttmálann síðkomnda líffræðingur við Goddard and aðra aðalhöfundur greinarinnar.
**Candidate 6:** „Við því að Mars tapaði svona miklum vatni var líklega vökvað lengur en áður var alvöru, sem bendir til þess að fyrirbæri fyrir líðandi væri lengur“ sagði Michael Mumma, sem er sérstakari vísindamannur í Goddard og annar aðalhöfundur greinarinnar.
**Candidate 7:** „Þegar Mars tapaði svo mikið af vatni, var reikistjarnan líklega vökvað lengur en til skiptis hefur verið um, sem gefur til kynna að reikistjarnan væri hæfur fyrir mannsstíflu lengur,“ sagði Michael Mumma, sérstakari vísindamaður við Goddard og annar aðalhöfundur greinarinnar.

</details>

<details><summary>before · G8 · p13official21:test:eso:710 · F</summary>

**Source:** The VST KiDS survey will allow astronomers to make precise measurements of dark matter, the structure of galaxy halos, and the evolution of galaxies and clusters.
**Semantic decision:** F — All corrupt dark matter/halo structure or evolution/cluster measurement list.
**Candidate 0:** VST KiDS verndir sér með skilverskum mælingum á dökkum rafum, myndun um sertleyfi stjörnuvöldanna og skiptingu stjörnuvöxta og knotta.
**Candidate 1:** VST KiDS rannsóknin mun gera stjörnufræðingum kleift að gera nákvæmar mælingar á dýrkaríki, rými úr galdrarum og myndun þeirra og þróunar sjónbergja.
**Candidate 2:** VST KiDS rannsóknin hefur áhrif á rannsóknarstjórnar á nákvæmar mælingum á djöfulu, stökkbreytingu í hela vetrarbrauta og þróun vetrarbrauta og vetrarbrautahluta.
**Candidate 3:** VST KiDS rannsókninni er grunin til stærðfræðinga til að gera nákvæmar mælingar á dæmunni, stökkbreytingunni hringjum stjörnuverða og vörnunum stjörnuverða og fjölmagnsins.
**Candidate 4:** VST KiDS mælingarinn mun láta stjörnufræðingum gera nákvæmar mælingar á doku, myndun haldar gegna í vetrarbrautum og þróun vetrarbrauta og vetrarbrautahópa.
**Candidate 5:** VST KiDS rannsóknin tekur stærðfræðingum tæknilega getu að gera nákvæmar mælingar á duskaeði, myndun helu í vetrarbrautum og sjónbæruþroska vetrarbrautar og vetrarbrautaklúða.
**Candidate 6:** VST KiDS skoðunin gerir stjörnufræðingum kleift að gera nákvæmar mælingar á dökktu efni, structúrunni á kringum gegnum snotta hjá vetrarbrautum og sjónukerfi og þróun vetrarbrauta og býla.
**Candidate 7:** VST KiDS tæki verður stærðfræðingum að mæla nákvæmlega um dökk efni, bylgjuloki vetrarbrauta og þróun vetrarbrautta og hóptar.

</details>

<details><summary>before · greedy · p13official21:test:eso:512 · F</summary>

**Source:** Another team member, Ana Duarte Cabral from the Laboratoire d'Astrophysique de Bordeaux, France, emphasises that "the ALMA observations reveal the spectacular details of the motions of the filamentary network of dust and gas, and show that a huge amount of gas is flowing into a central compact region".
**Semantic decision:** F — Filamentary dust/gas network and its motions are corrupted or absent.
**Candidate 0:** Önnur liðmanni í hópnum, Ana Duarte Cabral frá Laboratoire d'Astrophysique de Bordeaux í Frakklandi, kemur fram á það að „sýnir ALMA mælingarinnar skýrslu um snertingu vetrarbrauta og gasins í sér, og sýna að mikil magn af gasi flæðist inn í miðvettanum“.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:3454 · P</summary>

**Source:** And I work for Danny.
**Semantic decision:** P — And I work for Danny preserved.
**Candidate 0:** Og ég vinn fyrir Danny.

</details>

<details><summary>before · G8 · p13official21:test:eea:1814 · F</summary>

**Source:** The producer must ensure that all wood originate from legal sources.
**Semantic decision:** F — No candidate retains wood from legal sources with producer obligation.
**Candidate 0:** Framleiðandi skal tryggja að verður allir frá lögboðum.
**Candidate 1:** Framleiðandinn skal tryggja að allt vökvi úr skuldum.
**Candidate 2:** Vinnaraðilið þarf að tryggja að allt eystur vera úr lögboðum ásamt.
**Candidate 3:** framleiðandinn skal tryggja að allir stiga úr lögboðum.
**Candidate 4:** Framleiðandi verður að tryggja að öll stæði úr varð leyfðum.
**Candidate 5:** Varandahöfundur verður að tryggja að öll stærðbergur séu frá löglegum upprætingum.
**Candidate 6:** Umsækjandinn verður að tryggja að allt dyr er úr lögboðum.
**Candidate 7:** Framleiðandinn skal sjá til þess að allt skerthorni hafi orðið úr lögbeina upprunum.

</details>

<details><summary>before · greedy · p13official21:test:eea:1965 · P</summary>

**Source:** After paragraph 97B, paragraph 97C is added.
**Semantic decision:** P — 97C added after97B retained exactly.
**Candidate 0:** Eftir 97B-lið bætist við 97C-lið.

</details>

<details><summary>after · G8 · p13official21:test:eso:179 · F</summary>

**Source:** These violent explosions rip through the molecular gas clouds in their immediate surroundings, but after the shockwaves have travelled more than about ten light-years they are weaker, and may instead compress clouds that are a little further away, triggering the formation of new generations of stars.
**Semantic decision:** F — All eight corrupt molecular clouds, shock-wave compression or the new-star-generation consequence. Candidate1's last clause becomes a new public army, not stars.
**Candidate 0:** Þessi rístunir ristir hring í lífrænu gasglernum í nálægum umhverfi þeirra, en eftir að skeltur losn hefur farið meira en um tíu ljósára er þær vægari og geta þó styrkað umbylgir sem eru næstum lengur í burtu og kalla upp nýjar aldurshópa stjarna.
**Candidate 1:** Þessi ömurlegar sprengingar sækja í þeim efnisgasþokum sem liggja í nálarbundnum umhverfi þeirra en eftir að skjálftabláðir hafa fara í meira en um tíu ljósára til burtar er þær værir þá vægari og geta þó þess vegna þrýstir þokum sem eru stjarnaðarrar fyrir er skiptið í myndun nýrrar almannaherunnar.
**Candidate 2:** Þessi erfiðir sprengingar hraðar inn í efnaþynni í nýgöldum um stað, en eftir að skjálftan hefur farið mikið fyrir og í hátt um tíu ljósára breytist þær og gætu í stað þær komið samfleytt upp og þá viltu þær þynnum og eru að auka nýe þunglum.
**Candidate 3:** Þessi verulegir sprengingar hlaupa um tilfinningar gaskúlana en eftir að skellublöndur hafa farið meira en um tíu ljósára er þær minna og geta þar af leið sátt á kúlum sem eru lítið langt frá staðnum og þessu að nýverja stjörnum.
**Candidate 4:** Þessi sáramjögnur leggja undir kúlur í nánu kringum sér og eftir að skarpsvæðin hafa mændi meira en nánast tíu ljósára styrkur lágari en þeir reynja í stað þyrpingu á gegnum þær sem eru lítið fjarlægari og verða þannig að skipta á myndun nýrra stjarnaætlanir.
**Candidate 5:** Þessir rauða sprengingar skapa skífa um umhverfisverið, en eftir að sternaskjólfum hefur fara fyrir meira en um tíu ljósára er þeir vægari og geta í stað því batið lofthjúpum sem eru stuttar á við, sem kallar til myndunar nýrrar stjörnur.
**Candidate 6:** Þessir alvarlegar sprengingar koma í gegnum mótvega gástu og þarf þær þannig að þær verði minna eftir að skjótmörkum hefur farið meira en nánast tíu ljósára, og geta þær í stað þá samþætta gásti sem eru stuttar í nánast þess og hvetja þau til nýrra tíðanna stjarna.
**Candidate 7:** Við þessi alvarlega sprengingu ar þeir gert í það gáslagi sem er í nánu kringum við það en eftir að skjálftin hafa komið í ljós meira en um tíu ljósára eru þeir svæðið minni lægri og hugsanlega hægt komast í þeim og þeir hreyfið þau og koma þannig upp nýjar afmönnum stjarna.

</details>

<details><summary>before · G8 · p13official21:test:eso:611 · F</summary>

**Source:** “With Mars losing that much water, the planet was very likely wet for a longer period of time than previously thought, suggesting the planet might have been habitable for longer,” said Michael Mumma, a senior scientist at Goddard and the second author on the paper.
**Semantic decision:** F — No candidate preserves both wet-longer and habitable-longer inference with the attribution.
**Candidate 0:** „Þegar Mars tapaði svona mikið vatni var reykjalegur lítið lígrótt lengri tíma en áður hafi tilkynnt um, sem gefur til kynna að reynslugrein leyfilegt hafi verið á reynslum á réttum stigi um lengri tíma“ sagði Michael Mumma, fyrirfræðingur í Goddard og annar aðalhöfundur greinarinnar.
**Candidate 1:** „Þegar Mars missti svona vökvi, var jörðin það líklegast húðann í lengri tíma en áður hefur verið heldur, sem bendir til þess að húðin hafi verið búsettarflugu í lengri tíma,“ sagði Michael Mumma, hæstur rannsóknarmannur við Goddard og aðra aðalhöfundur á greininni.
**Candidate 2:** „Þegar Mars mislist svo mikt vökvi, var reikistjörnin hægt á lengri tíma en áður hefur verið talið og er hugsanleg að reikistjörnin hafi verið hálegri lengur,“ sagði Michael Mumma, hæfilegur vísindamannur í Goddard og annar aðalhöfundur greinarinnar.
**Candidate 3:** „Þegar Mars tapar svona mikið af vatni, var líklega hágægt af vatn á langri tíma en áður hefur verið tilkynnt, sem bendir til að hún væri í lagi fyrirhugaðar,“ sagði Michael Mumma, hæsta vísindamannur í Goddard- viðbótarins.
**Candidate 4:** „Við því að Mars losar svona mikið vatn, er líklegt að jörðinni væri langtíma vatnslagur en um kom í fyrri tíma, sem hugsanlega gefur til kynna að hún séið í trúnaði lengur“ sagði Michael Mumma, frægur vísindamaður í Goddard og annar aðalhöfundur greinarins.
**Candidate 5:** „Þegar Mars tekur úr sig svona mikið af vatni, var reikistjörnin víðtaklega vatn til lengri tíma en við ávartum áður, sem sugir að reikistjörnin hafi verið ferskja í lengri tíma,“ sagði Michael Mumma, aðalhæfilegur vísindamannur í Goddard og annar í greininni.
**Candidate 6:** „Við því að Mars missti svona mikið vatn, var líklegt að jörðin væri líka vapastofugt í lengri tíma en áður hafi verið leitt til, sem bendir til þess að það væri hægt að vera í stað sinni lengra,“ sagði Michael Mumma, hæfilegur vísindamann í Goddard og annar rannsóknaraðili á greininni.
**Candidate 7:** „Þegar Mars tapaði svæði sem er svæðið með það miklu af vatni, er líklegt til að jörðin væri umfanglega vökvað í lengri tíma en greint hefur verið frá, sem getur gert til kynna að jörðin væri húðu að vera fyrir undirbúning lengur“ sagði Michael Mumma, meistararannsóknari í Goddard og annar erlendur á greininni.

</details>

<details><summary>before · G8 · p13official21:test:eso:1138 · F</summary>

**Source:** “Terrestrial planets similar to our Earth are obvious targets for the search for life outside the Solar System, while comets are suspected to have played an important role in the appearance and development of life on our planet,” adds his colleague Emmanuël Jehin, who leads the cometary part of the project.
**Semantic decision:** F — All corrupt terrestrial planets, comets and origin/development-of-life inference or attribution.
**Candidate 0:** „Terrosplanets sem líka eru við okkur á Jörðina eru greinilegar markmiði fyrir leikfega lif og áður um rafmjaðarflugum,“ sagði Emmannuel Jehin, aðilarinn hjá sér, sem stjórnar rafmjaðarflugum í verkefnið, „veitir stutt að þær hafi leitt verið til mikilvægs hlutleysins í fækkun og þróun lífs á Jörðinni.“
**Candidate 1:** „Já, viðum er neikvæðan áhuga að leitir til lífs eru mælt með sem áttur að leitir frá lífi á utan sólarkerfisins, en við erum búin til að bjóða til komna sér í ljós að þeir hafi verið mikilvægar fyrir birtustu og þróun lífs á Eristuverjum okkar.“ Emmanuël Jehin, samstarfsmaðurinn, er aðeins að segja að rýmurinn hefur baik áhrif á birtun og þróun lífs á Eristuverjum okkar.
**Candidate 2:** „Sýna fyrir er að jörðulykur, sem er svipuð út í Miðjan, séu aðeins markmiði í leitinni að lifi út um sólkerfinu en á sjálfu sér eru ekki tilfinnt að kettilunum séu hafa mikilvægar þátttöku í mælikerfinu á jörðinni okkar,“ sagði Emmanuël Jehin samfélagsið hans, sem fylgir hjá meðferðina með kettilum.
**Candidate 3:** „Jafnvægar jarðverur, og líkin, eru skýrðar markmið fyrir leit á lifi utan sólarbardar, en erfðaköstunum er gert vísbending um að þær hafi verið mikilvægar fyrir dýrum á jarðverönum okkar við uppjöfnun og þróun lífs,“ sagði samtímis Emmanuël Jehin, fylgjara hjá framkvæmdarmeðluninni, sem stjórnera aðferðarinnar um erfðaköstur.
**Candidate 4:** „Umbóðir til að leita lífs fyrir utan sólarveranda, en fyrirhuguð er að flóttir hafi haft mikilvægar þátt í sýnileginu og þróun lífs á Jörðinni,“ bætir Emmanuël Jehin samfélagið til að segja með um um flóttirnir sem skipuleggja sérstaklega þátt í umferð og þróun lífs á Jörðinni.
**Candidate 5:** „Tilundin af völdum er að hraðarjörðir, sem eru svipaðir áréttu heiminn okkar, séu tilbúnar til að leita á lifi utan sólarvettisins, en sást að kornir hafi hafa mikilvæg árangur á komunnann á sér stað við útbreitt og þróun lífis á heiminn okkar,“ bætir Emmanuël Jehin, samtaktanefndur hans, til þess.
**Candidate 6:** „Lokafrjálsir, er einnig í svæðinu, sem nemur fyrir svæðið við að leita lífs utan sólarverksins, en áfanga er gert ráð fyrir að reykisverkur hafi haft mikilvægar áhrif á það sem barfur á lífi á ökutísinu okkar,“ sagði Emmanuël Jehin, samstarfsmaður hans, sem stjórnar hópnum sem styrkir reykisverkina.
**Candidate 7:** „Hljóðandi markmiðið við leitina á líf til herjalds í reikistjörnunum er jörðin okkar, sem eru eins og verið getað og úr námi, en fyrirbærið er á að flátar hafi haft mikilvægar hætti á upprunum og þróun lífs á jörðinni,“ sagði Emmanuël Jehin, samstarfsmaður hans, sem stjórnar draparinnar.

</details>

<details><summary>after · G8 · p13official21:test:eea:930 · F</summary>

**Source:** Wells in microtitre plates are coated overnight with recommended dilutions of purified immunoglobulin fractions of antibodies of reference quality.
**Semantic decision:** F — All eight corrupt plate/well identity, coating action or purified immunoglobulin-fraction requirements; none preserves the full laboratory procedure.
**Candidate 0:** Vélur á miðlæga hettuslökum eru klædd um næstum með tilvísanlegri þynningu innrennslisefnis í samræmi við gildandi gæðasamræmi.
**Candidate 1:** Wells í vefjasprautukort eru klædur á næstum rúm með ráðlagðum þykkni efnisbrotu ónæmissímabreytta mótefna frá viðmiðunarráðgöngum.
**Candidate 2:** Hettuglöfur í mikið títra plátum eru húðuð á nóttum með ráðlagða þynningu ónæmisglobekínu af sérstökum mótefnabilum með gagnvart stofnlegu gæðatölum.
**Candidate 3:** Vellir í litlýska plátum eru útskítar undir fyrrum eftir sveifli úr tilmæltum gerðum brúnslu ónæmismótefna í sérstökum immunóglóbúlínlínum.
**Candidate 4:** Vell í vefjaplatti eru klæddar í sorpu með ráðlagðum blandaðum þroskaðum immúnóglióbílín frumum mótefna í viðmiðunarskífu.
**Candidate 5:** Wells í mælitæki voru útfellt á næurna tíma með tilætluða þynningu af hreinsuðu immunglóbúlínþætti mótefna við viðmiðunar gildi.
**Candidate 6:** Vellir í minkvæði plátum eru klippaðar um næturkvöld með ráðlögðum þynningu á hreinsuðum immunóglóbúlínafjölda mótefna með viðmiðunar gæðum.
**Candidate 7:** Vell í mæliglösum eru áflæst í næurnum með tilvísanlegu þynningu af hreinsuðum immunglóbúlínni færibilum ónæmis sem eru á viðmiðunargildi.

</details>

<details><summary>before · G8 · p13official21:test:ema:2323 · U</summary>

**Source:** It is important to drink plenty of water to avoid dehydration.
**Semantic decision:** U — Candidate0 approximates drinking fluids to avoid drying out, but dehydration term and water-specific object uncertain; no confirmed fully correct rendering.
**Candidate 0:** Mikilvægt er að drekka miklu vökva til að forðast útþurrkun.
**Candidate 1:** Mikilvægt er að drekka marga vatni til að forðast þurrka.
**Candidate 2:** Mikilvægt er að drukkja mikið vatn til að koma í veg fyrir vatnsþurrkun.
**Candidate 3:** Mikilvægt er að drekka munur af vatni til að forðast þvagræsingu.
**Candidate 4:** Mikillvigt er að drekka mikið vatn til að falið úr þvagi.
**Candidate 5:** Mikilvægt er að drekka mjög víðtækt vatn til að forðast þurrkun.
**Candidate 6:** Mikilvægt er að drekka mikið af vatni til að koma í veg fyrir útbrot á vatnsþurrku.
**Candidate 7:** Mikilvægt er að drekka mikið af vatni til að forðast þráþykki.

</details>

<details><summary>before · greedy · p13official21:test:eea:1471 · F</summary>

**Source:** Prices including all taxes, levies and VAT.
**Semantic decision:** F — Levies become tax tables and VAT is corrupted.
**Candidate 0:** Verð þar sem tilgreind er allar skattir, skattatöflur og gildaaukaverði.

</details>

<details><summary>after · greedy · p13official21:test:ema:772 · P</summary>

**Source:** These effects are called interactions, and can lead to serious side effects, or prevent proper control of other conditions you may have.
**Semantic decision:** P — Preserves interactions causing serious side effects or preventing control of other conditions; grammatical errors do not change these relations.
**Candidate 0:** Þessi áhrif eru nefndar milliverkanir og geta leitt til alvarlegra aukaverkana eða koma í veg fyrir að ná réttum stjórn á öðrum sjúkdómum sem þú getur haft.

</details>

<details><summary>after · greedy · p13official21:test:eea:136 · F</summary>

**Source:** Member State shall recognize the documents of compliance and safety management certificates issued by, or on behalf of, the administrations of third countries if it is satisfied that they demonstrate compliance with the provisions of this Regulation.
**Semantic decision:** F — Compliance documents and safety-management certificates are corrupted and the conditional recognition requirement is not faithfully expressed.
**Candidate 0:** Aðildarríki skal viðurkenna skjöl um samræmismiðlun og öryggisstörfum sem útgefna stjórnarstofur þriðju landa eða fyrir hennar og gera sér vissu á því að þeir sýni fram á að þau uppfylli ákvæði þessarar reglugerðar.

</details>

<details><summary>after · G8 · p13official21:test:eea:1409 · P</summary>

**Source:** The port security assessment is the basis for the port security plan and its implementation.
**Semantic decision:** P — Candidate6 preserves port-security assessment as the basis of the port-security plan and its implementation; syntax is awkward.
**Candidate 0:** Portværisúttekktingur er grundvöllur við portværisáætlunina og framkvæmd hennar.
**Candidate 1:** Portvörunaröryggi er grundvöllur til að útbúa flutningsöryggisáætlun og framfylgjast við hana.
**Candidate 2:** Portverndarúttekkningin er grunnur áður að útbreiðskapastefnu um portvernd og framkvæmd hennar sé gerð.
**Candidate 3:** Portversigun matsið er grunnur fyrir portversigun áætlunina og framkvæmd hennar.
**Candidate 4:** Portvænna matið er grundvöllur atvinnuáætlunar á portvænisviðfang og framkvæmd þess.
**Candidate 5:** Portverndarætlunin er grundvaelin fyrir portverndaráætlun og framkvæmd hennar.
**Candidate 6:** Upptaka mat á öryggi hafnarinnar er grunnur á áætlun um öryggi hafnarins og í framkvæmd hennar.
**Candidate 7:** Rökströskjálta mati skiptir eftir á grundvelli port- öryggisáætlunar og framkvæmdar hennar.

</details>

<details><summary>after · greedy · p13official21:test:eso:760 · F</summary>

**Source:** Extreme stars like the two components of VFTS 352, play a key role in the evolution of galaxies and are thought to be the main producers of elements such as oxygen.
**Semantic decision:** F — The key-role predicate and oxygen term are corrupted, so the specific stellar-evolution/element-production claim is incomplete.
**Candidate 0:** Alvarlegir stjörnur eins og tvö hlutir VFTS 352 spája í þróun vetrarbrauta og eru talin að vera aðalmyndandi efni svo sem oxíum.

</details>

<details><summary>after · greedy · p13official21:test:eea:1323 · F</summary>

**Source:** If refills are not provided, the weight of the total primary packaging shall not exceed 3,7 g per wash for tablets and 1,7 g per wash for all other products.
**Semantic decision:** F — Primary packaging and per-wash terms are corrupted despite retaining the numbers.
**Candidate 0:** Ef endurtekinn fylling er ekki veitt skal þyngd heildarfráselds ekki fara yfir 3,7 g í hverja þvagrind fyrir töflur og 1,7 g í hverju þvagrind fyrir öll önnur vörur.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:1121 · P</summary>

**Source:** Of course you're right, Starling... but it doesn't change anything.
**Semantic decision:** P — Preserves agreement with Starling and the statement that this changes nothing.
**Candidate 0:** Að sjálfsögðu ertu rétt, Starling... en það breytir ekkert.

</details>

<details><summary>after · greedy · p13official21:test:ema:2124 · U</summary>

**Source:** If in doubt, talk to your doctor or pharmacist.
**Semantic decision:** U — Doctor/pharmacist advice is present, but cannot certify the malformed condition visslum as equivalent to in doubt.
**Candidate 0:** Ef þú ert í visslum skaltu ræða við lækninn eða lyfjafræðing.

</details>

<details><summary>after · greedy · p13official21:test:ema:1152 · P</summary>

**Source:** Change from baseline in body weight was similar for patients treated with sitagliptin relative to placebo.
**Semantic decision:** P — Faithfully retains similar baseline body-weight change for sitagliptin versus placebo.
**Candidate 0:** Breyting frá upphafsgildi líkamsþyngdar var svipuð hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.

</details>

<details><summary>after · G8 · p13official21:test:eso:871 · U</summary>

**Source:** A team of astronomers led by Adam Hardy (Universidad Valparaíso, Valparaíso, Chile) first used the ULTRACAM system on ESOs New Technology Telescope to measure these brightness changes very precisely.
**Semantic decision:** U — Candidate3 is closest, retaining team/instrument and precise brightness changes, but does not explicitly retain first use and has nonstandard measurement wording; other candidates corrupt measurements or roles.
**Candidate 0:** Hópur stjörnufræðinga, sem Adam Hardy (Universidad Valparaíso) fékk aðalstjórn, notuði ULTRACAM kerfið á New Technology Telescope ESO við uppbyggingu til að mæla ljósmörkshreyfanir svipaðar, mjög nákvæmlega.
**Candidate 1:** Hópur stjörnufræðinga, sem fékk umsjón af Adam Hardy (Universidad Valparaíso í Chile), notuðu áfengunarsjóðinni (ULTRACAM) á New Technology Telescope ESO til að mæla bláæðalíuða breytir á mjög nákvæman hátt.
**Candidate 2:** Hópur stjörnufræðinga, undir forystu Adam Hardy (Universidad Valparaíso í Chile), notuði fyrst ULTRACAM kerfið á New Technology Telescope ESO til að mæla vélbreytingunum mjög nákvæmlega.
**Candidate 3:** Hópur stjarnvísindamanna, á forystu Adam Hardy (Universidad Valparaíso, Valparaíso í Chile), notaði ULTRACAM kerfið á New Technology Telescope ESO til að mæla björtni breytunina mjög nákvæmlega.
**Candidate 4:** Hópur stjarnvísindamanna, undir forystu Adam Hardy (Universidad Valparaíso, Valparaíso í Chile), notaði ULTRACAM kerfið á New Technology Telescope ESO til að mæla sköpnum bilum á fjarlægði.
**Candidate 5:** Hópur stjörnufræðinga, sem leitur stjörnufræðing Adam Hardy (Universidad Valparaíso, Valparaíso í Chile), fannst fyrst með ULTRACAM kerfismælinu á New Technology Telescope ESO til að mæla skerðingu á ljósstærðum með mjög nákvæmri nákvæmni.
**Candidate 6:** Hópur stjörnufræðinga, yfir á móti Adam Hardy (Universidad Valparaíso, Valparaíso í Chile), notaði aðallega ULTRACAM kerfið á New Technology Telescope ESO til að mæla vikum breytingar á ljósstyrkleikum.
**Candidate 7:** Starfsmenn stjörnufræðinga, undir forystum Adam Hardy (Universidad Valparaíso, Valparaíso, Chile), notuðu áttaða ULTRACAM kerfið á New Technology Telescope ESO til að mæla ljósgreiningar þessarar skertrar breytningar mjög nákvæmlega.

</details>

<details><summary>after · G8 · p13official21:test:ema:635 · P</summary>

**Source:** Table 4 provides dose modification guidance for dinutuximab, GM-CSF and IL-2.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Candidate 0:** Tafla 4 fylgir leiðbeiningum um að breyta skömmtum af dínútkúsimab, GM-CSF og IL-2.
**Candidate 1:** Í töflu 4 eru leiðbeiningar um að breyta skömmtum dinutuximabs, GM-CSF og IL-2.
**Candidate 2:** Í töflu 4 eru veittar leiðbeiningar um að aðlaga skammta dinutuximabs, GM-CSF og IL-2.
**Candidate 3:** Í töflu 4 er kveðið á um leiðbeiningar um breyttingu á skammti af dinutuximabi, GM-CSF og IL-2.
**Candidate 4:** Í töflu 4 eru leiðbeiningar fyrir skammtausnumörkuun fyrir dinutuximab, GM-CSF og IL-2.
**Candidate 5:** Í töflu 4 er geri leiðbeiningar um að hafa breytt skammtafjölda dinutuximabs, GM-CSF og IL-2.
**Candidate 6:** Tafla 4 liggur fyrir leiðbeiningar um breytingar á skammti af dinutuximabi, GM-CSF og IL-2.
**Candidate 7:** Í töflu 4 er gefin leiðbeiningar um aðlögun skammta af dinutuximabi, GM-CSF og IL-2.

</details>

<details><summary>after · greedy · p13official21:test:eea:615 · F</summary>

**Source:** Annual days of sick leave not paid by the employer (optional).
**Semantic decision:** F — Sick leave becomes health insurance and not paid becomes not issued; the variable being recorded changes.
**Candidate 0:** Árslegar dagir til sjúkratrygginga sem vinnuveitandi gefur ekki út (frjáls).

</details>

<details><summary>before · greedy · p13official21:test:eso:179 · F</summary>

**Source:** These violent explosions rip through the molecular gas clouds in their immediate surroundings, but after the shockwaves have travelled more than about ten light-years they are weaker, and may instead compress clouds that are a little further away, triggering the formation of new generations of stars.
**Semantic decision:** F — Molecular gas clouds and compression of farther clouds triggering stars are corrupted.
**Candidate 0:** Þessi rauðar sprengingar skipta um milli líkamsgasvefnanna í nálægum umhverfi þeirra en eftir að skjálftan hefur farið meira en um tíu ljósára er þær vægar og geta þó styrkt það úr því að þeim verði það hægra veður og myndi þau koma upp í nýjar ævihóp stjarna.

</details>

<details><summary>after · G8 · p13official21:test:ema:382 · P</summary>

**Source:** In the controlled clinical studies in chronic ITP with eltrombopag, increases in serum alanine aminotransferase (ALT), aspartate aminotransferase (AST) and bilirubin were observed (see section 4.8).
**Semantic decision:** P — Candidate2 retains controlled chronic-ITP studies with eltrombopag and increases in serum ALT, AST and bilirubin, including section4.8; its observation verb is malformed.
**Candidate 0:** Í klínískum, samanburðarrannsóknum á langvarandi sjúkdómi af völdum ITP með eltrombópagi kom fram hækkun á alanínaminótransferasa í sermi (ALT), aspartataminótransferasa í sermi (AST) og bilirúbíni (sjá kafla 4.8).
**Candidate 1:** Í klínískum, samanburðarrannsóknum á langvarandi aldverksbjúgur með eltrombópag varð vart við hækkun á alanínamínótransferasa (ALT), aspartatamínótransferasa (AST) og bilirúbíni í sermi (sjá kafla 4.8).
**Candidate 2:** Í klínískum samanburðarrannsóknum á langvarandi ITP með eltrombópag voru aukningar á alanínaminótransferasa (ALT), aspartataminótransferasa (AST) og bilirúbíni í sermi sátt (sjá kafla 4.8).
**Candidate 3:** Í klínískum samanburðarrannsóknum á sjúklingum með langvinna og langvarandi alnæmisþrýsting, með eltrómbópag, kom fram hækkanir á alanín aminótransferasa í sermi (ALT), aspartat aminótransferasa (AST) og bilirubín (sjá kafla 4.8).
**Candidate 4:** Í klínískum samanburðarrannsóknum á langvinnri segamyndunartíðni (chronic ITP) með eltrombópag, komu fram aukningu á alanínaminótransferasa í sermi (ALT), aspartataminótransferasa (AST) og bilírubíni (sjá kafla 4.8).
**Candidate 5:** Í klínískum samanburðarrannsóknum á langvarandi útflötum blóðstorknunar, sem gengið var fram af eltrombópagi, kom fram aukning á alanín amínótransferasa í sermi (ALT), aspartat amínótransferasa í sermi (AST) og bilirubíni (sjá kafla 4.8).
**Candidate 6:** Í klínískum samanburðarrannsóknum á langvarandi æðalegri ITP í tengslum við eltrombópag rannsökuð voru hækkun á alaninamínótransferasa (ALT), aspartatamínótransferasa (AST) og bilirúbíni í sermi (sjá kafla 4.8).
**Candidate 7:** Í klínískum samanburðarrannsóknum á langvarandi sjúklingum með blóðfalli af völdum ITP (chronic ITP) og ílát með eltrombópag, kom fram aukning á alanín aminótrensa í sermi (ALT), aspartat aminótrensa (AST) og bilirúbínu (sjá kafla 4.8).

</details>

<details><summary>after · greedy · p13official21:test:eso:20 · F</summary>

**Source:** These galaxies span a vast range of distances from us.
**Semantic decision:** F — A wide range of distances is collapsed to being very far away, losing the diversity/range claim.
**Candidate 0:** Þessi vetrarbraut eru langt og mikið fjarlægð frá okkur.

</details>

<details><summary>before · greedy · p13official21:test:ema:2690 · F</summary>

**Source:** Adverse effects not observed in clinical studies but seen in the rat and to a lesser extent in the mouse at exposure levels similar to human exposure levels and with possible relevance for clinical use were liver changes, indicating an adaptive response such as increased weight and centrilobular hypertrophy, fatty infiltration and increased liver enzymes in plasma.
**Semantic decision:** F — Centrilobular hypertrophy becomes pressure and fatty infiltration becomes fat reduction; plasma also generalized to blood.
**Candidate 0:** Aukaverkanir sem ekki sást í klínískum rannsóknum en sáust hjá rottum og mjög minni marki hjá músum við útsetningu sem jafngildir útsetningu fyrir menn og geta haft áhrif á klínískan notkun voru breytingar á lifur sem benda til þess að það sé að því er varðar aðlagaða svörun eins og aukin þyngd og þrýsting í miðlókum, fituskerðingu og aukin lifrarensím í blóði.

</details>

<details><summary>before · greedy · p13official21:test:ema:607 · F</summary>

**Source:** Since the possibility of increased risk of cancer development in patients with newly diagnosed dysplasia treated with infliximab is not established, the risk and benefits to the individual patients must be carefully reviewed and consideration should be given to discontinuation of therapy.
**Semantic decision:** F — Newly diagnosed dysplasia is replaced by tissue-change/metabolism wording, losing the specified diagnosis.
**Candidate 0:** Þar sem ekki hefur verið sýnt fram á möguleika á aukinni hættu á krabbameinsuppkomu hjá sjúklingum með nýtt greiningu á vefjaskipta og sem fá infliximab, er nauðsynlegt að endurskoða áhættu og ávinning fyrir hverju sjúklingi og íhuga skal hvort þessi meðferð sé hætt.

</details>

<details><summary>after · G8 · p13official21:test:ema:1610 · F</summary>

**Source:** The true extent of CNS penetration of lamivudine and its relationship with any clinical efficacy is unknown.
**Semantic decision:** F — All eight lose the true extent of CNS penetration or replace the anatomical/process relation with brain-muscle, exposure or concentration wording.
**Candidate 0:** Lögbæru upplýsingum er ekki fyrir hendi hvaða hækkun lamivudín hefur á fæðubiltir og víðmiðið áfram í klíníska verkun.
**Candidate 1:** Hluti innferð lamivúdíns og neyslur þess við klínískri virkni er ekki þekkt.
**Candidate 2:** Reyndar útsetning á höfuðvöðva fyrir lamivúdíni og tengsl með lyfhrifu eru ekki þekkt.
**Candidate 3:** Öryggi fyrir að lamivudin kom í heila líkamans og Engin vísa á eftir áframhaldandi klínískri verkun samtímis lamivudini er óþekkt.
**Candidate 4:** Ráðstæður endurtekinn umfang gnjandi lamivúdíns í heilaheilabúla og tengslir við klíníska verkun eru ekki þekktir.
**Candidate 5:** Hlutarhlut af innfæringu lamivúdíns í heila hjáleitt og tengsl hjá klínískri verkun eru ekki þekkt.
**Candidate 6:** Verste magalag lamivúdíns og tengsl við klíníska virkni þess er óþekkt.
**Candidate 7:** Nákvæmar þéttni lamivúdíns og lamivúdíns og tengsl við klíníska verkun eru ekki þekkt.

</details>

<details><summary>before · greedy · p13official21:test:eso:1086 · F</summary>

**Source:** Media representatives and other outreach groups will also be attending the event.
**Semantic decision:** F — Media/outreach groups attending an event not intelligibly conveyed.
**Candidate 0:** Tilskipendum fjölmi og öðrum hópum sem hafa áhersla til að taka til bæjar í sér verða einnig aðstoðar.

</details>

<details><summary>before · G8 · p13official21:test:ema:2944 · F</summary>

**Source:** Chemical, physical and microbiological in-use stability has been demonstrated for 28 days at 2-8°C. Once opened, the product may be stored for a maximum of 28 days at 2°C to 8°C. Other in-use storage times and conditions are the responsibility of the user.
**Semantic decision:** F — No candidate preserves chemical/physical/microbiological stability plus maximum storage and user responsibility; chemical often becomes genetic.
**Candidate 0:** Sýnt hefur verið fram á efnafræðilega, eðlisfræðilega og örveruefnafræðilega stöðugleika lyfsins á 28 daga við 2-8°C. Ef lyfið hefur verið opnað er geyma að eftirlits gætu verið lauk í aukastöðu 28 daga við 2°C til 8°C. Annar geymsleiðslutími og -setningskvarðar eru ábyrgð ásjónavélar.
**Candidate 1:** Erfðabundin, eðlisfræðileg og sýlisfræðileg stöðugleiki í notkun hefur verið sýnt fram á 28 daga við 2-8° C. Eftir að lyfið er opnað má geyma það í hámarki 28 daga við 2° C til 8° C. Aðra geymslutíma og skilyrði er ábyrgð notanda.
**Candidate 2:** Eðli á meðferð eftir myndunar sést í efna-, eðlis- og líffræðilegar viðbrögð í 28 daga við 2-8°C. Eftir opnun er má geyma lyfið í hámarkstímabili 28 daga við 2°C til 8°C. Hjá notendur er ábyrgð á öðrum geymslu- og staðbendingum.
**Candidate 3:** Stöðugleiki efnisins, efna- og sýkluháttar in- ú notkun, hefur verið sýnt fram fyrir í 28 dagar við 2-8°C. Eftir að lyfið er opnað má geyma það í 28 dagana við 2°C til 8°C. Annars máli notendur ábyrgð á geymslutíma og kvarðargildum.
**Candidate 4:** Erfildan stöðugleiki af völdum efna, vefja og örvahefða er sýnt fram á 28 daga við 2-8°C. Eftir að lyfið er opnað getur það geymt í hámarki 28 daga við 2°C til 8°C. Annar stjórnunarmat og skilyrði fyrir lyfjagjöfina er ábyrgð notanda.
**Candidate 5:** Eru sýnt fram á efnafræðilegur, eðlisfræðilegur og líffræðilegur tíðni í notkun í 28 daga við 2-8°C. Eftir opnun má geyma lyfið í 28 daga við 2°C til 8°C. Þar til er hvers konar geymsluþol og skilyrði er ábyrgð notanda.
**Candidate 6:** Sýnt hefur verið fram á efnisfræðilega, orkugreinilega og sýklaskapamálgæði í notkun fyrir 28 daga við 2-8°C. Eftir að lyfið er opnað má geyma það í hámarksgildi 28 daga við 2°C til 8°C. Áður en notanda sýnir það fyrir sér er ákvæði notanda fyrir önnur gilda- og stillingartíma.
**Candidate 7:** Eintakaástandið fyrir efnisfræðilega, eðlisfræðilega og sýlumótefnaheilkenni hafa verið sýnt fram á 28 daga á 2-8°C. Eftir að lyfið hefur verið opnuð má geyma það í hámarki 28 daga á 2°C til 8°C. Annars gagnstöðvar við geymslu eftir notkun bera ábyrgð notanda.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:2209 · U</summary>

**Source:** Much has been made of the hostility between our countries.
**Semantic decision:** U — The much-has-been-made idiom and hostility term are malformed; cannot certify equivalence of this wording.
**Candidate 0:** Miklum hefur verið gerð af óþýði milli landa okkar.

</details>

<details><summary>after · greedy · p13official21:test:eso:512 · F</summary>

**Source:** Another team member, Ana Duarte Cabral from the Laboratoire d'Astrophysique de Bordeaux, France, emphasises that "the ALMA observations reveal the spectacular details of the motions of the filamentary network of dust and gas, and show that a huge amount of gas is flowing into a central compact region".
**Semantic decision:** F — The filamentary network and central compact region are corrupted, not just inflectional errors.
**Candidate 0:** Önnur liðamann í ALMA-gerðinni, Ana Duarte Cabral frá Laboratoire d'Astrophysique de Bordeaux í Frakklandi, kemur fram á það að „sýnir ALMA-mælingar sérstaklega skýrslu um hreyfingar dreifingarréttunar ryks og gasins og sýna að mikill magn gasa flæsti inn í miðlun þess komastu“.

</details>

<details><summary>after · G8 · p13official21:test:eso:63 · F</summary>

**Source:** “Studying afterglows is vital to further our understanding of the objects that become gamma-ray bursts and what they tell us about star formation in the early Universe,” says the studys lead author Jochen Greiner from the Max-Planck Institute for Extraterrestrial Physics in Garching bei München, Germany.
**Semantic decision:** F — All eight corrupt the gamma-ray-burst objects, early-Universe inference or author attribution. Candidate0 drops the gamma-ray-burst object entirely.
**Candidate 0:** „Það er mikilvægt að rannsaka eftirglæði,“ segir Jochen Greiner, aðalhöfundur greinarinnar, úr Max-Planck Institute for Extraterrestrial Physics í Garching bei München í Þýskalandi. „Það vinsamast okkur þekkingu á því og hvað þau segja okkur um stjörnumyndun í sykla alheimi,“ segir hann.
**Candidate 1:** „Nauðsynlegt er að rannsaka eftirreinkjarnar við frekari skilningu á fyrirbærum sem verða gammalöndur og hvað þeim er að segja um stjörnumyndun á ólögum vetrarbrautarnar,“ sagði Jochen Greiner, aðalhöfundur rannsóknsins frá Max-Planck Institute for Extraterrestrial Physics í Garching bei München í Þýskalandi.
**Candidate 2:** „Við rannsóknir á seytingum eftir skemmdir er grunnvægur að því að því læsa meira um hvers konar fyrirtæki verða skemmdar og hversu þau tilkynna okkur um stjörnumyndun á fyrstu alheimnum,“ segir Jochen Greiner aðalhöfundur rannsóknarinnar við Max-Planck Institute for Extraterrestrial Physics í Garching bei München í Þýskalandi.
**Candidate 3:** „Mælt að af því að rannsaka eftirglæði er mikilvægt að því að björgunin sem fara út í geimnum verði belstur og tilhögunin við myndun stjarna á frákomulegum lífi,“ sagði Jochen Greiner, aðalhöfundur rannsóknarinnar frá Max-Planck Institute for Extraterrestrial Physics í Garching bei München í Þýskalandi.
**Candidate 4:** „Starfandi árekstur er marktækur til að ná frekari skilningu á fyrirbæri sem verður við röntgenloska og hvað þeir segja okkur um myndun stjarna í fyrsta alheiminu,“ sagði Jochen Greiner, aðalhöfundur greiningarinnar frá Max-Planck stofnuninni fyrir rásagjöf í Garching bei München í Þýskalandi.
**Candidate 5:** „Atprófa eftirglæði er mikilvægt að því að framlengja skilningu okkar yfir fyrirbæri sem verða til gammalskyntri og sem þau segja okkur um stálfæri í syklingum á frumuríkinu,“ sagði Jochen Greiner, aðalhöfundur rannsóknarinnar, frá Max-Planck Institute for Extraterrestrial Physics í Garching bei München í Þýskalandi.
**Candidate 6:** „Að rannsaka eftirglæði er mikilvægt til að ná því í skref að skilja hvers kyns gögn sem verða fyrir gniti og hvað þeir sega okkur um myndun stjarna í syfilsvörunni,“ sagði Jochen Greiner, forritaður aðalhöfundur rannsóknarinnar frá Max-Planck Institute for Extraterrestrial Physics í Garching bei München í Þýskalandi.
**Candidate 7:** „Vísindamálið er að rannsaka eftirglæði, sem er mikilvægt síður því að æfa okkur skilning á hlutaðeigandi fyrirbæri sem verður gamma-glæmur og hvað þeir segja okkur um stjörnumyndun á fyrsta eví sinna,“ sagði Jochen Greiner undirhópsrétta greinar verkefnisins fyrir frammistöðu stjörnufræðisfræðisfræðinganna við Max-Planck Institute for Extraterrestrial Physics í Garching bei München í Þýskalandi.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:2621 · F</summary>

**Source:** I'm glad you found one another."
**Semantic decision:** F — Reciprocal found one another becomes singular found another; mutual reunion is lost.
**Candidate 0:** Ég er ánægður að þú hafir fundið annan."

</details>

<details><summary>before · greedy · p13official21:test:ema:2124 · F</summary>

**Source:** If in doubt, talk to your doctor or pharmacist.
**Semantic decision:** F — In doubt becomes in trouble, changing the consultation condition.
**Candidate 0:** Ef þú ert í vanda skaltu tala við lækninn eða lyfjafræðing.

</details>

<details><summary>after · G8 · p13official21:test:eea:2125 · F</summary>

**Source:** In addition, the sub-processing should only consist of the operations agreed in the contract between the data exporter and the data importer incorporating the standard contractual clauses provided for in this Decision and should not refer to different processing operations or purposes so that the purpose limitation principle set out by Directive 95/46/EC is respected.
**Semantic decision:** F — All eight corrupt the sub-processing/contract-party relation, standard clauses or purpose-limitation requirement. Candidate5 still changes the processing object and contract roles.
**Candidate 0:** Auk þess skal undirfjölfunina einungis vera þær rekstrarferlir sem samþykkt hafa verið í samningi um útflutningina og innflutningina og sem eiga við góðar samningsmálarnar sem kveðið er á um í þessari ákvörðun og hún skulu ekki vísa til annarra rekstrarferlur eða viðbrögða að því er varðar að þessi reglun verði hefur verið fyrir hendi.
**Candidate 1:** Að auki skulu undirpremingin einungis hluti af þeim rekstur sem samningin um gögnum fyrir útflutning og gögninni innflutning gerir samkvæmt lögunum í gagnvísindaskilmálum, sem kveðið er á um í þessari ákvörðun, og ekki skipta yfir annars konar rekstrur eða mál sem því að halda að þeirri meginreglun um takmarkanir á markmiðum, sem kveðið er á um í tilskipun 95/46/EB.
**Candidate 2:** Að auki ætti undirefnirinni nauðsynlegt að skipuleggja þær starfsemi sem samningurinn um gagnamögnun og innflytjandi gagnaleiðandi setti upp, með því að ná við gilda samningarkerfi sem kveðið er á um í þessari ákvörðun, og að leiðirist ekki við annarri aðgerðir auðkenninga eða aðstæður, svo að þessi meginreglur um takmarkanir á aðstæðum, sem mælt er fyrir um í tilskipun 95/46/EB, séu beitt.
**Candidate 3:** Auk þess skulu niðri verkefnið aðeins vera aðgerðirnar sem samningurinn setti að gera um og samrýmast viðunandi samningartakna, sem kveðið er á um í þessari ákvörðun, og skulu ekki vísa til annarra verkefna eða viðmiðana sem þær eru til að þessi meginreglur um takmarkaðri markmiði vera heimilaðar.
**Candidate 4:** Í aukinni skulu undirvinnslan einungis eiga aðgerðana sem samið er við um í samningnum um gagnaútandi og gagnainnöndunaraðili, þar sem fylgja staðla samninga sem mælt er fyrir um í þessari ákvörðun, svo að hún víki ekki til annarra aðgerða eða þeirra meginemi og gildi henni vísbendingin um eftirlit með að tryggja því að markmið notið með fyrir skipanir skuli uppfyllt.
**Candidate 5:** Að auki skal undirprentunin einungis vera í kjölfar starfsemi, sem samningin um gögnutilflutningu og gögninn flytjandi samþykkja, sem samræmt er við innflytjandi gögn samkvæmt staðla samningar sem mælt er fyrir um í þessari ákvörðun og að ekki tekist til mismunandi starfsemi eða að því er varðar annað á tilgangi en að því er varðar skilgreindur meginreglur um takmörkun á tilgangi samkvæmt tilskipun 95/46/EB.
**Candidate 6:** Auk þess skulu undirvinnslan eingöngu vera aðgerðirnar sem samningurinn færi til samkvæmt skurðlegum samningaskuli sem kveðið er á um í þessari ákvörðun og ekki má vísa til mismunandi aðgerða eða annarra meginvissula þar sem markið er við að aðstoðarviðmiðunartiltekinn heimild hafi verið settur í tilskipun 95/46/EB.
**Candidate 7:** Að auki skal undirbreiðingu eingöngu vera fyrirframfararaukningin sem samið er við samninginn milli gagnaflutningsins og gagnainnflutningsins og - viðaðar staðla samningsgerðar, sem kveðið er á um í þessari ákvörðun, og að ekki vera vísað til annars samningarráðstafanna sem, sem kveðið er á um í tilskipun 95/46/EB, er setjað við.

</details>

<details><summary>after · G8 · p13official21:test:eso:356 · U</summary>

**Source:** The nebula lies more than four hundred times further away than the famous star.
**Semantic decision:** U — Several variants retain the400-times comparison, but nebula naming and the farther-than versus distance-from relation are too malformed to certify a fully faithful candidate.
**Candidate 0:** Þynnuðan nefnir er meira en fjögur hundrað sinnum fjarlægari en frægja stjarnan.
**Candidate 1:** Þurrkið er fjarlægri en fyrir fjögur hundrað sinnum en þessi frægast stjarnan.
**Candidate 2:** Neifarfarina er meira en fjögur hundrað sinnum fjarlægri en fræga stjörnin.
**Candidate 3:** Nebulaði er lengur en fjórir hundruð sinnum fjarlægari en föstur stjörnu.
**Candidate 4:** Nebúnunin er meira en fjórhundrað sinnum fjarri stjörnunni.
**Candidate 5:** Nebularann er meira en fjögur hundruð sinnum fjarlægri en þeim frægum stjörnunum.
**Candidate 6:** Nebulann er meira en fjögur hundruð sinnum langt frá stjörnunni, sem er fræg.
**Candidate 7:** Neyslunin er meira en fjórhundrað sinnum fjarlægri en frægasta stjarnan.

</details>

<details><summary>before · G8 · p13official21:test:ema:3025 · U</summary>

**Source:** Based on individual patient response and tolerability, the dose may be increased to 300 mg (15 ml) per day after an interval of 3 to 7 days, and if needed, to a maximum dose of 600 mg (30 ml) per day after an additional 7-day interval.
**Semantic decision:** U — Most omit maximum/additional interval. Candidate7 has maximum600mg but patient-response/tolerance and interval syntax remain uncertain.
**Candidate 0:** Með tilliti til þeirra svörun og þoli sjúklings er hægt að auka skammtinn í 300 mg (15 ml) á sólarhring eftir 3 til 7 daga tímabili og ef þörf er að vera að auka skammtinn í 600 mg (30 ml) á sólarhring eftir 7 daga tímabili.
**Candidate 1:** Bundinu svörun og þróun hjá hverjum sjúklingi má aukast skammturinn í 300 mg (15 ml) á dag eftir 3 til 7 daga fresti og ef þörf er ráðlaggt að aukast í 7 daga fresti í 600 mg (30 ml) á dag.
**Candidate 2:** Býð að skammtinum 300 mg (15 ml) á dag, eftir 3 til 7 daga tímabili, og ef þörf er á 600 mg (30 ml) á dag, eftir 7 daga tímabili.
**Candidate 3:** Bundinn á svið sjúklingsvarðar og þol mætti, má auka skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga fresti, ef þörf krefur skammtinn í 600 mg (30 ml) á dag eftir einkennum 7 daga.
**Candidate 4:** Hjá sjúklingum sem svara bæði meðferðinni og geta næstum 300 mg (15 ml) á dag áfram í 3 til 7 daga, en ef þörf er á að bæta skammtinn í 600 mg (30 ml) á dag að viðbótarmörkum 7 daga.
**Candidate 5:** Bundið á því að það sé 300 mg (15 ml) skammturinn er aukinn til 3 x 7 daga meðferðarinnar og ef þörf er einnig upptekinn í 600 mg (30 ml) skammturinn á 7 daga fresti.
**Candidate 6:** Byggt á svörun hjá einstaklingum og þolanleika getur skammtinn vers hæft í 300 mg (15 ml) á dag eftir 3 til 7 daga gáfa og, ef þörf er, í helstu skammti 600 mg (30 ml) á dag eftir 7 daga aukka.
**Candidate 7:** Sérfræðilega síðan sem fyrir sér stendur virkni og þol ágera má aukast skammtinn í 300 mg (15 ml) á dag eftir 3 til 7 daga tímabili og ef þörf er á að auka síðan í 7 daga að hámarksskammtinum 600 mg (30 ml) á dag.

</details>

<details><summary>after · G8 · p13official21:test:eso:1069 · F</summary>

**Source:** By using the SPHERE instrument on ESOs Very Large Telescope (VLT) - one of the most powerful planet-hunting instruments in existence - the international team has made the first robust detection of a young planet, named PDS 70b, cleaving a path through the planet-forming material surrounding the young star.
**Semantic decision:** F — All eight lose the young planet cleaving a path through planet-forming material around the young star; some change the planet to a star/fetus.
**Candidate 0:** Við notkun SPHERE mælitækisins á Very Large Telescope (VLT) ESO - einnar af öflugustu mælitækjunum sem ganga úr landi - hefur alþjóðlegur hópurin gert fyrstu raunverulega greiningu á ungum föstum sem nefnist PDS 70b og hætti hægða í umhverfi sem byggist á fyrirbæri fósturins.
**Candidate 1:** Samkvæmt notkun SPHERE-mælitækisins á Very Large Telescope ESO (VLT) - einni af þeim mesti kröftugu mælitækjum sem liggja á milli fyrir sjóð og sjálfurnar fyrir reikistjörnur - hefur alþjóðlegur hópurinn gert fyrsta rauðan einkenni á unga reikistjörnunni, nöfnuð PDS 70b, í sjálfsveigum sem koma úr formandi efninu umhverfis þess.
**Candidate 2:** Með notkun SPHERE mælitækisins á Very Large Telescope (VLT) ESO - sem er ein af þeim mestar af skýrsluverkunum til að reyna fyrir reikistjörnum - hafa alþjóðlegur hópurinn gefið upp fyrstu kraftaðan uppgötvun yngri reikistjarnans, nemitu PDS 70b, og slegið leið úr fyrirbæri nýfórstuna, sem bundið er í um yngri stjörnuna.
**Candidate 3:** Með notkun SPHERE mælitækisins á Very Large Telescope (VLT) ESO, sem er einn af blástarprófunarmælitækinu sem er til staðar, hefur alþjóðlegur hópurin gert fyrstu víxlaðan upplýsingar um þángur, nafnd PDS 70b, í gegnum efni sem bundi gerðar úr reikistjörnunni.
**Candidate 4:** Með notkun SPHERE mælitækisins á Very Large Telescope (VLT) ESO - einum af öflugustu mælitækjum sem standa eru fyrir sólarhjálp - hópurinn aðstoðaði fyrsta hæfurðaðan skynmynd unga reikistjarnans, sem nefnist PDS 70b, með skorlausum mælingum og sýnt út ýmsar leiðir fyrir myndun reikistjarnanna í hringi um hlið þess.
**Candidate 5:** Með notkun SPHERE mælitækisins á Very Large Telescope (VLT) ESO, einn af öflugustu mjög fyrirhuguðum mælitækjum til að koma á fót hreyfinga jörða -ð er PDS 70b - hefur alþjóðlegur hópurinn gert fyrstu mikið og sterkustu ákvörðun á ungarjörðinni og veitti götuna í umhverfi þess sem hvíldir hreyfingu jörðunnar.
**Candidate 6:** Með notkun SPHERE mælitækisins á Very Large Telescope (VLT) ESO - sem er einn af öflugustu mælitækjum til að leita að fyrirbærum stjörnur - hefur alþjóða hópurinn gert fyrstu þrænsi áhersla á ungar stjörnur, núnan PDS 70b, sem snúaði á þá úrgangs einu meðalum í umhverfi stjörnunnar.
**Candidate 7:** Með notkun SPHERE mælitækisins á Very Large Telescope ESO (VLT) - annarri sætasta mælitækisins til að leita að reikistjörnum - hefur alþjóðlegur hópurinn komið fyrstu starfsemi á þungri og fyrir hættu til yngri reikistjarna, PDS 70b, sem leitar að réttum meginbrigði í umhverfið fyrir reikistjarna.

</details>

<details><summary>before · G8 · p13official21:test:ema:1433 · F</summary>

**Source:** Aseptically add sodium pertechnetate (Tc 99m) solution (from step d above) to the tilmanocept powder vial.
**Semantic decision:** F — None preserves aseptic addition plus complete solution/powder-vial identity; sterile solution alone is not aseptic addition.
**Candidate 0:** Aefnid mixtúru safa skiptið úr flösku (frá fyrirlið d hér að framan) í hettuglasinu með tilmanocept dufti.
**Candidate 1:** Aðruflæsingi skal gefa natríum perteknetat (Tc 99m) lausn (frá d-stigi hér að ofan) í hettuglasinu með tilmanocept dufti.
**Candidate 2:** Aflsa evicóðuð lausn (Np 99m) (frá d-stignum hér að ofan) til geymsluspýru með tilmanócepti í hettuglasi.
**Candidate 3:** Að og á ekki sterra afhældu sodium pertechnetat (Tc 99m) lausn (frá d-stiginn hér að framan) til tilmanocept stungulyfsins í hettuglasinu.
**Candidate 4:** Aðkúmu niður natríum pertechnetat (Tc 99m) lausn (frá d liði hér á ofan) í hettuglasinu sem inniheldur tilmanocept duft.
**Candidate 5:** Nota skal sæfða natríum pertechnetat (Tc 99m) lausn (fra d stig hér á ofan) til tilmanocept duftfylgiseðils í hettuglasi.
**Candidate 6:** Aa skammtinu af natriumpertechnetat (Tc 99m) lausn (frá d-stignum hér að framan) á tilmanocept duftaflöskuna í hettuglasinu.
**Candidate 7:** Samsænka aðeins naútupsertechnetat (Tc 99m) lausn (frá d-stigi fyrir aftur hér) í hettuglasinu með tilmanocept innihaldi.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:2130 · P</summary>

**Source:** Because Mr. Doyle called and said you have not been there all week.
**Semantic decision:** P — Doyle called, saying you were not there during the week retained.
**Candidate 0:** Því að Doyle hringdi og sagði að þú hefur ekki verið þar í viku.

</details>

<details><summary>after · G8 · p13official21:test:ema:1385 · F</summary>

**Source:** Lynparza is indicated as monotherapy for the maintenance treatment of adult patients with platinum-sensitive relapsed BRCA-mutated (germline and/or somatic) high grade serous epithelial ovarian, fallopian tube, or primary peritoneal cancer who are in response (complete response or partial response) to platinum-based chemotherapy.
**Semantic decision:** F — All eight corrupt essential cancer eligibility: platinum sensitivity/relapse, BRCA mutation, high-grade serous epithelial type or anatomical sites. Copying some English names does not restore the full indication.
**Candidate 0:** Lynparza er ætlað til einlyfjaveinnar meðferðar við viðhaldsmeðferð fullorðinna sjúklinga með BRCA-breytur (germline- og/eða sjúkdómsfrumabreytur) í eitilfrumakrabbamein í eggjastokkum, lúðrunni eða frumna í kviða sem er í endurtekinu, bráða (frum- og/eða hlutaðeigð) sermisskýr og svaraði (fullanlega svar eða hlutafall) þvagrannslu með vetnisfjölli.
**Candidate 1:** Lynparza er ætlað til einlyfjameðferðar við hvarfefnastjórnandi endurvinnslu hjá fullorðnum sjúklingum með BRCA-snarpanntegnd (germlinne- og/eða líffæra) sekk slímhúðafkýrskuldbendingar, stórbreyt, öskjuvöðva, eða frumkyrningar í kringlómanngilinu sem hafa svarað (fullkominn svörun eða aðlagað svörun) lyfjameðferð með platinúm.
**Candidate 2:** Lynparza er ætlað til einlyfjameðferðar til viðhaldsmeðferðar hjá fullorðnum sjúklingum með BRCA-affnslag sem stuttir er fyrir platín og með hæga sérþekkingar í kyrningafæðum, kyrningaholtum eða fyrir grunnkrabbamein í kyrningahelmi, sem hafa svörun (fullkomnu svörun eða hlutafullan svörun) við eitla með platín.
**Candidate 3:** Lynparza er ætlað til einlyfjameðferðar við viðhaldsmeðferð hjá fullorðnum sjúklingum með brustehexaflögu-þáttatalna (germligne- eða líkamalegt) BRCA-gerðar, seyðirfloskavöxtur í hægurri stigi í eggjastokkum, holgjörðum eða frumþekju sem er vegna sjúkdóms í meðferð (fullanlaust svörun eða hluta svörun) sem svarar til meðferðar með platín í bakgrunum.
**Candidate 4:** Lynparza er ætlað til einlyfja meðferðar við viðhaldsmeðferð hjá fullorðnum sjúklingum með brastefnavirkt endurtekið BRCA-smita (germline og/eða sjálfsbundin) líthjúpskrúfa í eggjastokkum, eftirlimni eða fyrir upphaf líffærskrampa í kæfa, sem hafa svörun (heildarsvörun eða hluta sjón) við þar til hefur verið notað krabbameinslyfjameðferð með platinum.
**Candidate 5:** Lynparza er ætlað til einlyfja meðferðar við viðhaldsmeðferðar hjá fullorðnum sjúklingum með BRCA-hágrunnar (germline og/eða líffæra) hægðaeitilkynns eggjastokka (serous epithelial ovarian), hægðastokka (fallopian tube) eða grunnkrabbameins í keppslisbólu sem hefur upphafðar til að sjá (heilbrigði svörun eða hlutfallslegan svörun) á þá grundvelli á롤um.
**Candidate 6:** Lynparza er ætlað til einlyfjameðferðar við viðhaldsmeðferð hjá fullorðnum sjúklingum með bróktrýstæð krabbamein í seröuml; heil fyrir lifur (serous epithelial ovarian, fallopian tube, or primary peritoneal cancer) með BRCA-verkun (germline and/or somatic) sem bregðast aftur og sem svaraðar eru (fullkominn svörun eða hluta sjúkrasvörun) við meðferð með platíníum.
**Candidate 7:** Lynparza er ætlað til einlyfjameðferðar við viðhaldsmeðferð hjá fullorðnum sjúklingum með brísins- hjátrusögu (germlin- og/eða líkamans) óheilbrigða serískri ægishaldna kyrningasjúkdóms í maga, kyrningaslagaslag, eða grunnklínveiru sjúkdóms með krypir (kominn í fullanlegu (viðfullanlega) eða hlutfallslegan (viðhlutfallslegan) svörun) frá接种化疗platin.

</details>

<details><summary>before · G8 · p13official21:test:ema:437 · F</summary>

**Source:** Lenvatinib should not be started in patients with fistula to avoid worsening and lenvatinib should be permanently discontinued in patients with oesophageal or tracheobronchial tract involvement and any Grade 4 fistula (see section 4.2); limited information is available on the use of dose interruption or reduction in management of other events, but worsening was observed in some cases and caution should be taken.
**Semantic decision:** F — All corrupt fistula/site/grade or permanent-discontinuation instructions; some invert stopping.
**Candidate 0:** Ekki skal hefja meðferð með lenvatinibi hjá sjúklingum með liðverða til að koma í veg fyrir versnun og ekki skal hætta meðferð með lenvatinibi hjá sjúklingum með fæðu í munni eða fyrir öndunarfæraneti og eftir sem jöfn (aðeins fyrir í 4. gráðu) og að ráðlagðar upplýsingar liggja fyrir um notkun skilyrða, skorts eða minnkaða skammts í meðferð þar sem ekki varðar aðra aukaverkanir og versnun kom fram hjá sumum tilvikum.
**Candidate 1:** Ekki skal hefja meðferð með lenvatinibi hjá sjúklingum með glötu til að koma í veg fyrir aukningu á sjúkdóminn og skal stöðva meðferð með lenvatinibi hjá sjúklingum með raðavatnshvati eða enda- og skógræði og þeim sjúklingum sem fá 4. stigs glós (sjá kafla 4.2); takmarkaðar upplýsingar liggja fyrir um notkun skammtsins stuttra eða minnkaðs til að hefja meðferð á öðrum tilvikum, en versnun séð í nokkrum tilvikum og þá skal gæta varúðar.
**Candidate 2:** Ekki ætti að hefja meðferð með lenvatinibi hjá sjúklingum með glæs to ofnæmi til að koma í veg fyrir versnun lenvatinibs og skal stöðvulega hætta meðferð með lenvatinibi hjá sjúklingum með svæði sem tengist mergkviðum eða brota og einhverri miðað við fargi 4 glæs (sjá kafla 4.2); takmörkuð upplýsingar liggja fyrir um notkun skrefaframsýklunar eða minnkaða skammta í öðrum tilvikum, en versnið fylgdi eftir í sumum tilviki og mikilvægar kröfur skulu tekið.
**Candidate 3:** Ekki á að hefja meðferð með lenvatinibi hjá sjúklingum með liðskur og utan að varta þegar meðferðin er hætt í lengi og hægt er að halda meðferð með lenvatinibi hjá sjúklingum með sýringu í rásaræði eða öndunarfæra og sjúklingum með 4. stigs liðskur (sjá kafla 4.2); takmörkuð upplýsingar liggja fyrir um notkun skiptis á skammti eða minnkað skammtar í meðferð hjá sjúklingum fyrir önnur aukaverkanir, en versnun kom fram í einstakum tilfellum og ráð gegn því skal gæta varúðar.
**Candidate 4:** Ekki skal hefja meðferð með lenvatinibi hjá sjúklingum með gáta vegna þess að hún getur versnað og hægt ætti að hætta notkun lenvatinibs tilvara hjá sjúklingum með ítar í þroti eða hrygglofshrygg og hvaða kostar 4. stigs gáta (sjá kafla 4.2); fyrirbæri er að komi fram um takmarkaðar upplýsingar um því hvort stöðuga stöðugleika eða minnkaður skammtur sé notað við meðferð annarra ástanda og því að breytingar á skömmtum hafa orðið til bata komu fram hjá sumum tilvikum, þá skal gæta varúðar.
**Candidate 5:** Hefja skal ekki meðferð með lenvatinibi hjá sjúklingum með fiðlun til að koma í veg fyrir versnun sjúkdómsins og stöðvarenda skal meðferð með lenvatinibi af loknum hjá sjúklingum með svæði á áxli eða tunguhraði þar sem svæðið verður með höndum og í sumum tilvikum sem verður miðað við 4. stigs, að því tilskildu að það er einungis skýrt um að gefa að stöðva skammtatíma, að minnka skammta eða breyta meðferð í innan sér við aðgerðir annarra tilbreytinga og að breyta meðferðinni, en versnun átti fyrir hendi í sumum tilvikum og skal gæta varúðar.
**Candidate 6:** Lenvatinib skal ekki hefja hjá sjúklingum með glæsi til að koma í veg fyrir versnun og hætta skal meðferð með lenvatinibi á lengi þegar um sjúklinga er að ræða smút í sársaka eða asta og tréða eða þrúða og einhverjar smút í 4. stigs (sjá kafla 4.2); takmörkuð upplýsingar eru fyrirliggjandi um notkun skrefa tímabundið eða minnkaðs á meðferð á öðrum tilvikum, en versnun kom fram í sumum tilvikum og vart ber að gæta varúðar.
**Candidate 7:** Ekki á að byrja meðferð með lenvatinibi hjá sjúklingum með glæi til að forðast að það væri að versna, og lyfjagjöf á lenvatinibi skal hægt gauð til að hjá sjúklingum með uppsvæði í lagsmíði eða öndulifshorni og lyfja sem liggja í 4. stigs (sjá kafla 4.2); fyrirbæri á upplýsingum um að hamla meðferð eða minnka skammta við meðferð fyrir annað sjúkdómur er takmörkuð, en versnun varst fyrir tilteknum tilvikum og þá á að gæta varúðar.

</details>

<details><summary>after · greedy · p13official21:test:eso:1073 · F</summary>

**Source:** Analysis of this spectrum indicated that its atmosphere is cloudy.
**Semantic decision:** F — Spectrum is replaced by a sequence/row, changing the object of the analysis.
**Candidate 0:** Greining á þessari röð sýndi að lofthjúpurinn sé skýjaður.

</details>

<details><summary>before · greedy · p13official21:test:ema:978 · F</summary>

**Source:** Similarly, the geometric mean AUC (CV%) values at Cycle 6 were higher among the subcutaneous group than the intravenous group; 4088 μg day/mL (34.2) versus 3630 μg day/mL (32.8) respectively) with a resulting adjusted geometric mean ratio [90% CI] of 1.10 [0.98-1.24].
**Semantic decision:** F — Adjusted geometric mean ratio is corrupted, despite most numeric values being copied.
**Candidate 0:** Eins og áður var meðalgeðið AUC (CV%) gildi í 6. lotu hærri hjá undirhúða hópnum en hjá hópnum sem fengu inndælingu í bláæð; 4088 μg dag/ml (34,2) samanborið við 3630 μg dag/ml (32,8) í skiptum röðum, sem leiddi til að jafnframt með bilun á meðalgeðið [90% CI] 1,10 [0,98-1,24].

</details>

<details><summary>before · G8 · p13official21:test:eea:1471 · F</summary>

**Source:** Prices including all taxes, levies and VAT.
**Semantic decision:** F — No candidate preserves the full taxes/levies/VAT list; closest6 substitutes obligations and non-VAT value tax.
**Candidate 0:** Verð, þar með talið alla styrk, skatt og gilda skattatiltekni.
**Candidate 1:** Verð sem takmörkuð er allarum skattum og skattaraðskrafa, skuldum og markaðsskatta.
**Candidate 2:** Verðið skal inntaka allar skálds og skattatöflur.
**Candidate 3:** Verð þar sem tilgreind eru allar skálds eftir tilskildir og gilda skattaárekströr.
**Candidate 4:** Verðin með inntöku öllum skáls, skrifstofum og auðskilnaðarsskattinum.
**Candidate 5:** Verð þar sem tilgreindir eru allar skattir og skattrík og markaðsskipulag.
**Candidate 6:** Verð þar sem fela upp allar skatta, skuldbindingar og gildisskatt.
**Candidate 7:** Verð þar sem tilgreind eru allar skattir, tilbótir og töldeysakerfi.

</details>

<details><summary>before · greedy · p13official21:test:ema:970 · P</summary>

**Source:** In patients with mild hepatic impairment (Child-Pugh A), there was no significant changes in pharmacokinetics compared with normal healthy volunteers.
**Semantic decision:** P — Hepatic impairment, Child-PughA, no significant PK change and healthy-volunteer comparison all retained.
**Candidate 0:** Hjá sjúklingum með vægt skerta lifrarstarfsemi (Child-Pugh A) var engin marktæk breytingar á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.

</details>

<details><summary>before · greedy · p13official21:test:eea:1855 · F</summary>

**Source:** The product must be easily recyclable.
**Semantic decision:** F — Product changes to medicine and recyclable to renewable/renewable action.
**Candidate 0:** Lyfið verður að vera auðvelt að endurnýja.

</details>

<details><summary>after · greedy · p13official21:test:eso:1181 · F</summary>

**Source:** By combining light from three of the VLTIs 1.8-metre Auxiliary Telescopes with the AMBER instrument, this facility allows astronomers to see details equivalent to those a telescope with a mirror of 85 metres in diameter would see.
**Semantic decision:** F — The equivalence to an85m mirror is not retained; the sentence instead describes more detailed information and corrupt auxiliary-instrument wording.
**Candidate 0:** Með því að setja ljósi úr þremur VLT-aðhliðatækinum 1,8 metra í sér með AMBER mælitækinni geta stjörnufræðingar sést nákvæmari upplýsingar og þau sem sjónauki með 85 metra diametrar myndi sjá.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:2164 · F</summary>

**Source:** You didn't have the guts to do it yourself.
**Semantic decision:** F — Lack of courage becomes lack of ability, changing the psychological assertion.
**Candidate 0:** Þú hefur ekki hægt til að gera það sjálfur.

</details>

<details><summary>after · G8 · p13official21:test:eso:881 · F</summary>

**Source:** Using standard candles - such as the variable stars within IC 1613 and the less-common Type Ia supernova explosions, which can seen across far greater cosmic distances - astronomers have pieced together a cosmic distance ladder, reaching deeper and deeper into space.
**Semantic decision:** F — All eight corrupt standard candles, TypeIa supernovae or the cosmic-distance-ladder construction; none retains the complete distance-measurement argument.
**Candidate 0:** Við notkun hefðbundinna brennslu - svo sem breytilegum stjörnum í IC 1613 og minna víkulegar styrkurþroti af tegund Ia - hefur stjörnufræðingar myndið kröfu saman stjörnuframfar, sem náði skýrri og skýrri í útvegri geim.
**Candidate 1:** Að nota eiginstöðunarhol - eins og breytilegar stjörnur í IC 1613 og smáhöfn fyrir Ia-ífurnapskiptir sem hægt er að sjá í miklum fjarlægðum - hefur stjörnufræðingi smitast upp við þokunnarhóp um fjarlægð, sem namst hægra og hægra inn í geiminn.
**Candidate 2:** Staðlaðum bólum, eins og breytilegum stjörnum í IC 1613 og minni- algengri afgera af afgerunarþátt Ia, sem er hægt að sjást í miklu lengri geimfræðilegu afflöngi - hafa stjörnufræðingar samið gegn alvarlegum geimferðum saman geimfræðilega geimstigall, sem yfirdegt enn frekar inn í geiminn.
**Candidate 3:** Með stöðugum myndunni - svo sem þessara breytilegara stjarna í IC 1613 og minna alvarlegra tilbætur af tegund Ia, sem snýr til lengri fjarlægð í geimnum - hafa stjarnvísindamenn samanstött geimvegsbæði ásamt sjónuninu í rúm.
**Candidate 4:** Með hjálp staðla kérna, eins og breyttra stjörnur í IC 1613 og minni alvarlega kraftarölum af tegund Ia, sem sjást í örsvarlegri fjarlægð, hefur stjörnufræðingi sett slíka yfirbúnaðarlag í raun.
**Candidate 5:** Hjá stjörnufræðingum hefur verið haft þróun á litrófum - eins og breytilegir stjörnur í IC 1613 og færri en alvarlega af tegund Ia ofurvarfár sem skemmdir eru á frekar langri af stjörnuverðins - og þeir hafa haft saman sköpuninn á farir burtum á stjörnum í skyni að ná djúprar og djúprar meðferð í geimnum.
**Candidate 6:** Samkvæmt því að nota hefðbundnar brennslur, eins og breytilegar stjörnur í IC 1613 og minni ítarlegari Ia-tykku sprengistjörni, sem yrði hægari og hægari á geimnum en stjarnanirna, hefur stjörnufræðingar samsettu geimfræðilega afstaða, sem nærst yfir öllu geimnum sem er hægt.
**Candidate 7:** Með viðbúnum ljósin - eins og breittum stjörnum í IC 1613 og minna fyrirbæri það sem vantar eftir stjörnumlætingum af tíðni Ia, sem er sjást langt yfir stórri geimfræðilegan fjarlægan milli - hafa stjarnvísindamenn hægt að samskiptast og samskiptast niður í geiminum í stöðugri rannsókn eftir rannsóknirnar.

</details>

<details><summary>before · greedy · p13official21:test:eea:571 · F</summary>

**Source:** To check power-operated windows/roof-panel systems/partition systems with reversing devices, a measuring instrument/test rod shall be placed through the opening from the inside of the vehicle or, in the case of a partition system, from the rear part of the passenger compartment in such a way that the cylindrical surface of the rod contacts any part of the vehicle structure which forms the boundary of the window/roof-panel aperture/partition.
**Semantic decision:** F — Powered/reversing systems and cylindrical contact geometry corrupted; any part becomes all surface.
**Candidate 0:** Til að athuga verkstæða-gerðir glugga/þekjuflagna/fyrirhluta með bakslögunartækni skal setja mælitæki/prófunarrod út í skýrinu frá inni á ökutækinu eða, ef um fyrirhluta er að ræða, frá enda hluta sjónsykisins og þannig að hringræn yfirborð prófunarroðsinnar snertir allt yfirborð ökutæknisins sem myndar skýrinu/þekjuflagna/fyrirhluta.

</details>

<details><summary>after · greedy · p13official21:test:ema:978 · F</summary>

**Source:** Similarly, the geometric mean AUC (CV%) values at Cycle 6 were higher among the subcutaneous group than the intravenous group; 4088 μg day/mL (34.2) versus 3630 μg day/mL (32.8) respectively) with a resulting adjusted geometric mean ratio [90% CI] of 1.10 [0.98-1.24].
**Semantic decision:** F — Geometric-mean and adjusted geometric-mean-ratio terminology is corrupted despite the retained numeric values.
**Candidate 0:** Að jafnframt var meðalgeðið AUC (CV%) gildi við 6. lotu hærri hjá undirhúðaþýðinum en þeim sem fengu inndælingu í bláæð; 4088 μg daga/ml (34,2)% samanborið við 3630 μg daga/ml (32,8)% og endurheimtur meðaltalsgeðsliðar [90% CI] var 1,10 [0,98-1,24].

</details>

<details><summary>after · greedy · p13official21:test:ema:74 · P</summary>

**Source:** ARICLAIM should normally not be used for children and adolescents under 18 years.
**Semantic decision:** P — Preserves the usual restriction against ARICLAIM use in children/adolescents under18.
**Candidate 0:** ARICLAIM á ekki venjulega notað handa börnum og unglingum yngri en 18 ára.

</details>

<details><summary>after · greedy · p13official21:test:eso:538 · F</summary>

**Source:** Previous observations had shown hotter, but much less dense, gas streaming away from NGC 253s star-forming regions, but alone this would have little, if any, impact on the fate of the galaxy and its ability to form future generations of stars.
**Semantic decision:** F — Much less dense becomes much thicker, reversing a crucial physical property.
**Candidate 0:** Fyrri mælingar hafa sýnt hitari, en mjög þykkara, gasströngir sem fór út frá stjörnumyndunarsvæðum NGC 253, en einnig hefði það minna áhrif á lífinu gegn stjörnuþyrpingu og getu hennar til að mynda fjölda nýja stjarna í framtíðinni.

</details>

<details><summary>before · greedy · p13official21:test:ema:1458 · F</summary>

**Source:** This is important to make the medicine easier and more comfortable to inject.
**Semantic decision:** F — More comfortable becomes old.
**Candidate 0:** Þetta er mikilvægt að gera lyfið auðveldari og gamall til inndælingar.

</details>

<details><summary>after · G8 · p13official21:test:eso:1088 · F</summary>

**Source:** Weather statistics are available here.
**Semantic decision:** F — All eight inspected candidates replace weather statistics with winter research, astronomy, hydrogen reports, radio failures or malformed unrelated terms.
**Candidate 0:** Vetrarannsóknir eru hér.
**Candidate 1:** Útgáfur er að talið um veðrastaðal.
**Candidate 2:** Útabréf yfir vetrarbrautir eru hér.
**Candidate 3:** Vetrarannsóknarupplýsingar eru hér.
**Candidate 4:** Vetnaskýrslur eru hér fyrir hendi.
**Candidate 5:** Útvarpsbilunir eru hér fyrir hendi.
**Candidate 6:** Vetrarannsóknarritar eru hér fyrir hendi.
**Candidate 7:** Útvarps- og veídafræðilegar gagnasöfn eru hér.

</details>

<details><summary>after · greedy · p13official21:test:eso:705 · F</summary>

**Source:** Normal long-duration GRBs last between 2 and 2000 seconds.
**Semantic decision:** F — Normal GRBs are described as serious GRBs; the normal-category qualifier is not retained.
**Candidate 0:** Alvarlegar langtíma GRB eru á bilinu 2 til 2000 sekúndur.

</details>

<details><summary>after · G8 · p13official21:test:ema:1495 · P</summary>

**Source:** Check again to make sure the correct dose of Tevagrastim is in the syringe.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Candidate 0:** Athugaðu á ný og sjá að réttur skammtur af Tevagrastim sé í sprautunni.
**Candidate 1:** Athugaðu aftur að vísa að réttur skammtur af Tevagrastim sé í sprautunni.
**Candidate 2:** Athugaðu aftur til að vera sannar um að réttur skammtur af Tevagrastim sé í sprautunni.
**Candidate 3:** Athugaðu aftur til að tryggja að réttur skammtur af Tevagrastim sé í sprautunni.
**Candidate 4:** Skoðaðu aftur til að tryggja að rétta skammtur af Tevagrastim sé í sprautunni.
**Candidate 5:** Skoðaðu aftur til að tryggja að réttur skammtur af Tevagrastim sé í sprautunni.
**Candidate 6:** Athugaðu aftur til að sjá að réttur skammtur af Tevagrastim sé í sprautunni.
**Candidate 7:** Kannaðu aftur til að tryggja að réttur skammtur af Tevagrastim séu í sprautunni.

</details>

<details><summary>after · greedy · p13official21:test:eso:908 · F</summary>

**Source:** This bridge, which has not been seen before (and is too faint to show up in this picture), is somewhat bluer than either galaxy, indicating that it consists of stars created in gas that was drawn away from NGC 1387 by the gravitational pull of NGC 1399.
**Semantic decision:** F — The bluer comparison and gravitational-pull mechanism are corrupted; this is not merely a grammatical issue.
**Candidate 0:** Þessi brú, sem hefur ekki séð áður og er of ljósgæf til að sjást í þessari mynd, er einhverslárörvarrúmlegri en annar galdrarinnar, sem benda til þess að hún samanstendur af stjörnum sem eru búin til úr gass sem var dragað frá NGC 1387 með gegnþrýstingu NGC 1399.

</details>

<details><summary>before · greedy · p13official21:test:eea:21 · F</summary>

**Source:** Soils used must, wherever possible, be freshly sampled.
**Semantic decision:** F — Soil is rendered as suns; required object of fresh sampling corrupted.
**Candidate 0:** Sólar sem notaðir verða, hvenær sem mögulegt er, að taka nýtt sýni úr.

</details>

<details><summary>before · greedy · p13official21:test:eea:63 · F</summary>

**Source:** The placement of these devices in the soil should not result in preferential flow paths.
**Semantic decision:** F — Preferential flow paths becomes indication-like flow paths, losing the hydraulic concept.
**Candidate 0:** Setning þessara tækjanna í jarði ætti ekki að leysa til ábendingar flæðislega leiða.

</details>

<details><summary>before · greedy · p13official21:test:ema:2490 · F</summary>

**Source:** If you are left-handed, do what comes naturally to you.
**Semantic decision:** F — Left-handed condition is lost in an unrelated hand adjective.
**Candidate 0:** Ef þú ert höndlegra skaltu gera það sem kemur fyrir þér eðlilega.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:2128 · F</summary>

**Source:** Don't you worry about those dope smokers and nudists down below there?
**Semantic decision:** F — Smokers/nudists and the negative question are not preserved.
**Candidate 0:** Ekki hafa áhyggjur af þeim doppaheyrum og náttúruhæðum niðri í þessu?

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:939 · F</summary>

**Source:** Put it in the envelope, Mrs. Rochon.
**Semantic decision:** F — Envelope becomes package.
**Candidate 0:** Settu það í pakkanum, frú Rochon.

</details>

<details><summary>after · G8 · p13official21:test:eea:1059 · F</summary>

**Source:** The domestic output price index for an economic activity measures the average price development of all goods and related services resulting from that activity and sold on the domestic market.
**Semantic decision:** F — All eight corrupt the domestic output-price-index identity or measurement relation; average prices alone do not preserve this specific economic index.
**Candidate 0:** Innri verðþáknífur fyrir efnahagsaðstöðu mælar með hjálp af meðaltalsverðþróunar á öllum vörum og tilheyrandi þjónustu, sem ákvarða sjálfur það starfshlut, og seljandi á innlandsmarkaðinum.
**Candidate 1:** Í innlendri verðsámskipti við efnahagshlutun gefur vísitöl uppruna verðs, sem metast saman, allra vörum og tengdri þjónustu sem leiðir af þessari efnahagshlutun og er selgt á innlandsmarkaðnum.
**Candidate 2:** Staðbundinn merkingargreining á afurðöryggi við efnahagsaðgerð mæltir út efnaskiptamagnina sem byggja á framkvæmd þessarar einingar og selt eftir staðbundinni markaði.
**Candidate 3:** Þjóðlegur verðþáknífur varðandi hagkvæma starfsemi mælt er efnið meðalverðaþróunar öllum vörum og viðkomandi þjónustum, sem útbúa af þessari starfsemi, og sem selst á innlendu markaði.
**Candidate 4:** Verðstengd endurvinnslutilviki innlandsins fyrir efnahagsaðgerðin mælti fyrir að minnsta kosti vörum og tilheyrandi þjónustu hafa farið fram af þessari aðgerð og seldar á innlendum markaðinum.
**Candidate 5:** Innlendur verðið efnahagsaðgerðarmerkistingu miður með því að miða verðgerð allra vörunnar og þeirra íhlutdeila sem afgerast í þessu starfsemi og selst á innri sjóðinu.
**Candidate 6:** Ættandi verðleiðsæti fyrir innlend útgjöld við efnahagsaðsetningu mæla með verðsjálfu útgátameðaltilkynna allra vörur og tengdra þjónustu sem fylgir þessari starfsemi og seldan við innlendan markað.
**Candidate 7:** Hagverðsmál forverkunarkorts fyrir efnahagsaðstöðu eru miðað um meðalverðaþróun öllum vörum og viðkomandi þjónustu sem falla fram af þeirri starfsemi og selst á innri markaðinum.

</details>

<details><summary>before · G8 · p13official21:test:eso:504 · F</summary>

**Source:** The precise extent of the habitable zone depends on many factors.
**Semantic decision:** F — Habitable zone is replaced by unrelated invented terms in every candidate.
**Candidate 0:** Mikilvægur smásvæði heimskara svæðis er háð margri fyrirliggjandi færibreyttra.
**Candidate 1:** Nákvæmri fæðingarvettirinninn til stjórnar á margum þætti.
**Candidate 2:** Nákvæmur fjarlægð trúheimilsins er háð margra þáttanna.
**Candidate 3:** Nákvæmar tíðni sævægar svæðisins tekur til mörga aðstæðna.
**Candidate 4:** Vissan styrkur sömu ramma sé stjórnun margrar aðstæðna.
**Candidate 5:** Nákvæmur umfang sætþjálanda varar til mörgu fyrirbæra.
**Candidate 6:** Nákvæm fjarlægð sæfisvettilsins er háð margra aðstæðna.
**Candidate 7:** Mikilvægar vinnsluáætlunin hægt er hálfátti hjástuðunarbanna.

</details>

<details><summary>after · G8 · p13official21:test:ema:1190 · U</summary>

**Source:** In these cases it is therefore recommended that the Zonegran total dose should be rounded up or down to the nearest available dose that can be achieved with commercially available capsule strengths of Zonegran (25 mg, 50 mg and 100 mg).
**Semantic decision:** U — Several preserve nearest-dose adjustment and25/50/100mg, but rounding-up wording or commercially available capsule strengths is corrupted. Candidate7 is closest but cannot be certified as rounding both up and down.
**Candidate 0:** Í slíkum tilvikum er því ráðlagt að náraðar númerið skammti í núngildi sé nálginn eða minnkaður úr númerið skammti sem er fyrir hendi og getur komið til með skammtahækkunum af Zonegran (25 mg, 50 mg og 100 mg) sem eru fyrir hendi.
**Candidate 1:** Í slíkum tilvikum er því ráðlagt að heildarskammtur af Zonegran skoðaðist upp eða niður í næstu fáanlegri skammti sem er unnt að ná með skammta í cöllnibundnum hylkjum af Zonegran (25 mg, 50 mg og 100 mg).
**Candidate 2:** Í slíkum tilvikum er því mælt með að heildarskammtur Zonegran sé snúinn upp eða niður í næstu fáanlegt skammt sem getur verið að ná með sölulegu lyfjahvarfaútreikninguskammtum af Zonegran (25 mg, 50 mg og 100 mg).
**Candidate 3:** Í þessum tilvikum er því mælt með að því má að endurtaka eða niðurt svigrúmst skammtinn af Zonegran allsauknum og gera það nálægt viðskiptagildi mumnum með afmynntum skömmtum Zonegran (25 mg, 50 mg og 100 mg).
**Candidate 4:** Í slíkum tilvikum er því ráðlagt að endurvarsa eða niður varða heildarskammtur af Zonegran, sem næstu fáanlegri skammti er að komast við með því að nota 25 mg, 50 mg og 100 mg skammtar af Zonegran sem eru fyrirliggjandi á launamarkaði.
**Candidate 5:** Í þessum tilvikum er því ráðlagt að heildarskammtur af Zonegran sé snúinn upp eða niður að næsta fáanlegri skammti sem er hægt að nota, sem sé á meðferðarheimildir af styrk fósturlíffræðilegra hylkjanna af Zonegran (25 mg, 50 mg og 100 mg).
**Candidate 6:** Í þessum tilvikum er því ráðlagt að hefja eða niður á að þá heildarskammtur af Zonegran ná næstliðanum meðgöngu þess skammts sem er að ná við með geymsluferðir á skömmtum Zonegran (25 mg, 50 mg og 100 mg).
**Candidate 7:** Í slíkum tilvikum er því mælt með að heildarskammtur af Zonegran sé varður eða minnkaður í næstu fáanlegri skammti sem er mögulegt að ná með kapslum af fáanlegri styrk Zonegran (25 mg, 50 mg og 100 mg).

</details>

<details><summary>after · G8 · p13official21:test:eea:1814 · F</summary>

**Source:** The producer must ensure that all wood originate from legal sources.
**Semantic decision:** F — All eight candidates corrupt the wood/material object; legal origin alone does not preserve the producer's requirement for all wood.
**Candidate 0:** Framleiðandi skal tryggja að allt okkar leitar í völ væri úr löglegum upprunum.
**Candidate 1:** Framleiðandinn skal tryggja að allt vökvi úrgerðist úr lögmætanum.
**Candidate 2:** Vefjaframleiðandi skal tryggja að allt lundur séu úr réttgildum upprunum.
**Candidate 3:** framleiðandi verður að tryggja að allt skóði upprunandi úr löglegu upprunandi.
**Candidate 4:** Framleiðandi verður að tryggja að allt dyr úr skíði sé frá löglegum aðstöðum.
**Candidate 5:** Varanahöfundur skal tryggja að allir stærðir forðaist úr réttlegri upprunum.
**Candidate 6:** Framleiðandi verður að sjá til þess að öll stiga unnið frá lögboðlegum upprunum.
**Candidate 7:** Framleiðandinn skal sjá til þess að allt varfengi komi frá réttmætum upprunum.

</details>

<details><summary>after · greedy · p13official21:test:eso:825 · U</summary>

**Source:** The process of dust trapping is explained in an earlier release (eso1325).
**Semantic decision:** U — Earlier release and identifier are retained; cannot certify the nonstandard trapping verb trapa as the intended dust-trapping process.
**Candidate 0:** Framkvæmdarferlið um að trapa á ryk er skýrt í fyrri útgáfu (eso1325).

</details>

<details><summary>before · greedy · p13official21:test:eso:538 · F</summary>

**Source:** Previous observations had shown hotter, but much less dense, gas streaming away from NGC 253s star-forming regions, but alone this would have little, if any, impact on the fate of the galaxy and its ability to form future generations of stars.
**Semantic decision:** F — Much less dense becomes very dense; changes the gas property.
**Candidate 0:** Fyrri mælingar hafa sýnt að gasið var heitt en mjög þykktur, á umferð frá stjörnumyndunarsvæðum NGC 253, en einnig ekki hafi það miklu áhrif á lífinu stjörnuþyrpingarins og hæfni til að mynda fjölda nýja stjarna í framtíðinni.

</details>

<details><summary>after · G8 · p13official21:test:eso:349 · P</summary>

**Source:** The results described here use some of these Science Verification data.
**Semantic decision:** P — Candidate0 retains results noted here using some of these scientific verification data, despite malformed syntax. Other variants are less clear.
**Candidate 0:** Niðurstöðurnar sem merktar eru hér meðan nota sér sum þessara, vísindalegra sannprófunar gögn.
**Candidate 1:** Niðurstöðurnar sem kveðið er á um hér notið sumum af þessum djöfnunarskýrslum.
**Candidate 2:** Niðurstöðurnar hér sem lýst er vega hluta af þessum gögn til uppgjörs verndunar.
**Candidate 3:** Niðurstöðurnar sem lýsað er hér notast einhverju af þessum gagnum um vísindalegu faggildingu.
**Candidate 4:** Niðurstöðurnar sem lýst er hér nota aðeins stöðu þessara upplýsinga um sannprófun á vísindum.
**Candidate 5:** Niðurstöðurnar sem lýst er hér eru notaðar þessara hagskýrslur um vissu.
**Candidate 6:** Niðurstöðurnar, sem er lýst hér, ná að sumum þessara Skjaldskilgreiningarupplýsingum.
**Candidate 7:** Niðurstöðurnar sem lýst er hér, notuðu sumí þessara postgreisa til sannvottunar.

</details>

<details><summary>before · greedy · p13official21:test:eea:607 · F</summary>

**Source:** Years of career break in the current enterprise (optional).
**Semantic decision:** F — Career break becomes unrelated career changes.
**Candidate 0:** Ár af skipti í starfsáttamönnum í núverandi fyrirtæki (valfrjáls).

</details>

<details><summary>after · greedy · p13official21:test:eea:1190 · F</summary>

**Source:** Indeed, there is a need for technical and scientific support and a high level of stable expertise to properly apply the Community legislation in the fields of maritime safety and ship pollution prevention, to monitor its implementation and to evaluate the effectiveness of the measures in place.
**Semantic decision:** F — Community legislation becomes collision wording, and ship-pollution prevention and monitoring are lost.
**Candidate 0:** Það er þörf á tæknilegri og vísindalegu stuðningu og mikil stöðugt sérfræðileg mat til að beita framkvæmd árekstur Bandalagsins í sviði öryggis á sjó og að koma í veg fyrir að hægt sé að bregðast við framkvæmd þess og meta árangur ráðstafana sem eru í gildi.

</details>

<details><summary>before · G8 · p13official21:test:ema:1414 · U</summary>

**Source:** Invokana has no or negligible influence on the ability to drive, cycle, and use tools or machines.
**Semantic decision:** U — Candidate6 has correct driving/tools/machines but cycling is an uncertain foreign loan; others change cycling or effects.
**Candidate 0:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, vélræðna og notkunar vélj átta eða vél.
**Candidate 1:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, kringgjafar og notkunar tækja eða véla.
**Candidate 2:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, vélar og notkunar vélana eða véla.
**Candidate 3:** Invokana hefur engin áhrif eða óveruleg áhrif á hæfni til aksturs, byssu og notkunar verkja eða vél.
**Candidate 4:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, kringgöngu og notkunar tæki eða vél.
**Candidate 5:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, kíklans og notkunar vélka eða véla.
**Candidate 6:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, cíklings eða notkunar tækja eða véla.
**Candidate 7:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, ciklingu og notkunar vélaga eða véla.

</details>

<details><summary>before · greedy · p13official21:test:eso:611 · F</summary>

**Source:** “With Mars losing that much water, the planet was very likely wet for a longer period of time than previously thought, suggesting the planet might have been habitable for longer,” said Michael Mumma, a senior scientist at Goddard and the second author on the paper.
**Semantic decision:** F — Habitable becomes intended/planned; the central inference is lost.
**Candidate 0:** „Þegar Mars missti svona mikið vatn var jörðin líklega vökvað lengur en áður hefur verið talið og það bendir til þess að hún hafi verið fyrirhuguð fyrir lengri tíma,“ sagði Michael Mumma, hæsta vísindamannur í Goddard og annar aðalhöfundur greinarinnar.

</details>

<details><summary>before · G8 · p13official21:test:eso:356 · U</summary>

**Source:** The nebula lies more than four hundred times further away than the famous star.
**Semantic decision:** U — Candidate5 preserves >400times distance and famous-star comparison, but nebula is an uncertain nonstandard loan form; no confidently Icelandic full rendering.
**Candidate 0:** Nebuðið er meira en fjórar hundraðsinna fjarlægð frá fyrsta stjörnunni.
**Candidate 1:** Nebúnaðurinn er meira en fjórum hundraðum sinnum fjarri en frægasta stjörnin.
**Candidate 2:** Neifarfarina er meira en fjögur hundraðsin tíð ekki fyrir stjörnuna.
**Candidate 3:** Nebulónið er meira en fjórir hunda sinnum fjarlægri en fyrirvistasta stjarnan.
**Candidate 4:** Nebúanum er meira en fjórum hundrað tímann fjarri en frægum stjörnunum.
**Candidate 5:** Nebularann er meira en fjögur hundruð sinnum fjarlægri en þeirri frægri stjörnunni.
**Candidate 6:** Nebulann er meira en fjórhundrað sinnum fjarlægri en uppsprettastjörnurinn.
**Candidate 7:** Nebulinn er meira en fjórhundraðsinna fjarlægir en frægast stjarnan.

</details>

<details><summary>after · greedy · p13official21:test:eso:611 · F</summary>

**Source:** “With Mars losing that much water, the planet was very likely wet for a longer period of time than previously thought, suggesting the planet might have been habitable for longer,” said Michael Mumma, a senior scientist at Goddard and the second author on the paper.
**Semantic decision:** F — Habitable is changed to inhabited/settled and the senior-scientist attribution is corrupted.
**Candidate 0:** „Þegar Mars tapaði svona mikið af vatni var reikistjarnan líklega vökvað lengur en áður hafi verið talið og það bendir til þess að hún gæti verið búsettur fyrir lengri tíma en áður hefur verið talið,“ sagði Michael Mumma, hópi sánni vísindamanna við Goddard og annar aðalhöfundur greinarinnar.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:1596 · F</summary>

**Source:** I stuffed it in my pocket.
**Semantic decision:** F — Stuffing something in a pocket becomes leaving it in a different material/location.
**Candidate 0:** Ég skildi það í vattið.

</details>

<details><summary>after · G8 · p13official21:test:eea:1509 · P</summary>

**Source:** Therefore, in the interest of clarity of legislation, it is appropriate to merge those provisions in one single legislative act.
**Semantic decision:** P — Candidate6 retains bringing provisions together in one legislative act to ensure clarity of the laws, despite substantial grammatical imperfections.
**Candidate 0:** Því er rétt að samgjör að þeim ákvæðum í þeirri essu gerð landslöggjafar sem getur veitt skýrt yfir ákvæði með öðrum gerðum.
**Candidate 1:** Því er réttlætanlegt að samþykkja þessar ákvæði í einu löggjaldrisskrá.
**Candidate 2:** Því er rétt að samana þessi ákvæði í eina gerða lagagóða.
**Candidate 3:** Þar af leiðandi er rétt að gera allar þær ákvæði í eina storkuverkefni.
**Candidate 4:** Því er rétt að sami þessar ákvæði í einu gera einsa löggjöf.
**Candidate 5:** Af þessari sökum er viðeigandi að samfleyta þessa ákvæði í eina leyfulegri gerð.
**Candidate 6:** Því er rétt að eina þessar ákvæði séu sami í einni lagagóða gerð til að tryggja skýrleika lagana.
**Candidate 7:** Því eru rétt að samruna þessum ákvæðum í einu gildisskrá.

</details>

<details><summary>before · greedy · p13official21:test:ema:709 · U</summary>

**Source:** The other ingredients are sodium chloride, succinic acid, polysorbate 80, 2- phenoxyethanol and water for injections.
**Semantic decision:** U — Ingredient list largely recognizable, but succinic-acid rendering is nonstandard and cannot confidently certify chemical identity.
**Candidate 0:** Önnur innihaldsefni eru natríumklóríð, súkfinýlsýra, pólýsorbat 80, 2-fenóxýlethanól og vatn fyrir stungulyf.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:939 · F</summary>

**Source:** Put it in the envelope, Mrs. Rochon.
**Semantic decision:** F — Envelope becomes package; the requested container changes.
**Candidate 0:** Settu það í pakkið, frú Rochon.

</details>

<details><summary>after · greedy · p13official21:test:eea:1855 · P</summary>

**Source:** The product must be easily recyclable.
**Semantic decision:** P — Preserves requirement that recycling the product be easy.
**Candidate 0:** Vörunni skal vera auðvelt að endurvinna.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:1317 · F</summary>

**Source:** General Barnicke's gone until tomorrow morning.
**Semantic decision:** F — Absence until tomorrow morning becomes having left this morning; the temporal claim changes.
**Candidate 0:** Barnicke hefur farið til burtu í morgun.

</details>

<details><summary>after · G8 · p13official21:test:ema:2183 · F</summary>

**Source:** For intravenous use, infusion systems with Actrapid at concentrations from 0.05 international unit/ml to 1.0 international unit/ml human insulin in the infusion fluids 0.9% sodium chloride, 5% dextrose and 10% dextrose inclusive 40 mmol/l potassium chloride using polypropylene infusion bags, are stable at room temperature for 24 hours.
**Semantic decision:** F — All eight corrupt potassium chloride, international units, infusion bags or room-temperature conditions;6 explicitly substitutes sodium chloride for potassium chloride.
**Candidate 0:** Fyrir notkun í æð: Innrennslisfyrirkomulag með Actrapid á styrkleikum frá 0,05 evrópsk einingar/ml til 1,0 evrópsk einingar/ml mannainsúlín í innrennslissvögunni 0,9% natríumklóríð, 5% dextros og 10% dextros, þar með talið 40 mmól/l kóltklóríð, með pólýprópýlen innrennslispoka, eru stöðug á stofuhita í 24 klst.
**Candidate 1:** Til notkunar í æð, innrennslisstöðvar með Actrapid í styrkleikum 0,05 alþjóðlegar einingar/ml allt að 1,0 alþjóðlegar einingar/ml af mannainsúlíni í innrennslismyndunum, 0,9% natríumklóríð, 5% dexstrúr og 10% dexstrúr, að meðtölum 40 mmól/l kútríumljúð, með pólýprópýlen innrennslisútblöndum, eru stöðug við stofuhita í 24 klst.
**Candidate 2:** Ef notuð er sem inntæki eru innrennslistæki með Actrapid með styrks frá 0,05 alþjóðlegum einingum/ml til 1,0 alþjóðlegum einingum/ml af mannainsúlíni í innrennslistu blóðvökva 0,9% natríumklóríð, 5% dextros og 10% dextros, með þeim með 40 mmol/l kalíumklórala, á stöðugum hitastigi í 24 klst.
**Candidate 3:** Til notkunar í æð er þéttni Actrapid eftir stofnun frá 0,05 evrópsk rúmmál/ml til 1,0 evrópsk rúmmál/ml af manneinsinsúlíni í innrennslisflögunni 0,9% natríumklóríð, 5% dextros og 10% dextros, í tölu með 40 mmol/l kútríumlíð, í pólýprópýlen innrennslisskurðum varðar stöðug og við stofuhita í 24 klst.
**Candidate 4:** Fyrir innrennsli í bláæð eru innrennslisstöðvar sem notuð eru Actrapid á styrkleikum frá 0,05 evigt eining/ml til 1,0 evigt eining/ml af mennska insúlíni í innrennslisvökva 0,9% natríumklóríð, 5% kviksynjali og 10% kviksynjali auk 40 mmól/l kloríðkloríð með pólýprópýlen innrennslisútblöndum og þær eru stöðugar við stofuhita í 24 klst.
**Candidate 5:** Til notkunar í æð, innrennslistengd kerfi sem gefa Actrapid í styrkleikum frá 0,05 evrahópa/ml til 1,0 evrahópa/ml af mannainsúlíni í innrennslisvökvunum 0,9% natríumklóríð, 5% dextros og 10% dextros, þar með tali 40 mmol/l kloríðkloríð í púlpitengdum innrennslisúrtum við stofuhita varðar þau stöðug 24 tíma.
**Candidate 6:** Fyrir notkun í bláæð, innrennslisvörunar með Actrapid í styrk frá 0,05 evrópsk eining/ml til 1,0 evrópsk eining/ml af mannsinsúlíni í innrennslisvökva, 0,9% natríumklóríð, 5% dextros og 10% dextros, þar með talið 40 mmol/l natríumklóríð, sem nota á pólýprópýlen innrennslislögunum, eru stöðug á stofuhita í 24 klst.
**Candidate 7:** Til notkunar í æð, innrennslissjónar með Actrapid með styrk frá 0,05 evrópskum einingum/ml til 1,0 evrópskum einingum/ml af mannainsúlíni í innrennslisvökva 0,9% natríumklóríð, 5% dextros og 10% dextros, tæknilegur, 40 mmól/l játraskór, sem eru í pólýprópýlen innrennslispokum, eiga stöðugleika við stofuhita í 24 klst.

</details>

<details><summary>before · greedy · p13official21:test:eea:1190 · F</summary>

**Source:** Indeed, there is a need for technical and scientific support and a high level of stable expertise to properly apply the Community legislation in the fields of maritime safety and ship pollution prevention, to monitor its implementation and to evaluate the effectiveness of the measures in place.
**Semantic decision:** F — Ship-pollution prevention becomes preventing improvement of an unexplained impact; stable expertise also corrupted.
**Candidate 0:** Það er þörf á tæknilegri og vísindalegu stuðningu og mikil stöðugt sérfræðileg mat til að beita rétt fyrir löggjöf bandalagsins um öryggi á sjó og að koma í veg fyrir að hægt sé að bæta úr skellunni af skipum, til að fylgjast með framkvæmdi hennar og meta árangur ráðstafana sem eru í gildi.

</details>

<details><summary>after · greedy · p13official21:test:eea:1503 · U</summary>

**Source:** If this kind of costs exists, they will be reported separately.
**Semantic decision:** U — Conditional costs and separate reports are suggested, but the edition/issuing paraphrase is malformed and cannot be certified as faithful reporting.
**Candidate 0:** Ef slík kostnaður er til hægt verður að gefa útgáfu af þeim í sérstökum skýrslum.

</details>

<details><summary>before · G8 · p13official21:test:ema:382 · P</summary>

**Source:** In the controlled clinical studies in chronic ITP with eltrombopag, increases in serum alanine aminotransferase (ALT), aspartate aminotransferase (AST) and bilirubin were observed (see section 4.8).
**Semantic decision:** P — Candidates0/7 preserve controlled chronicITP studies with eltrombopag and increased serum ALT/AST/bilirubin plus section4.8.
**Candidate 0:** Í klínískum, samanburðarrannsóknum á langvinnri ITP með eltrombópagi komu fram aukningu á alanínamínótransferasa í sermi (ALT), aspartatamínótransferasa í sermi (AST) og bilirubin (sjá kafla 4.8).
**Candidate 1:** Í klínískum, samanburðarrannsóknum á langvinnt blóðfall með eltrombópagi höfðu orðið til aukningu á alanínamínótransferasi (ALT), aspartatamínótransferasi (AST) og bilirúbíni í sermi (sjá kafla 4.8).
**Candidate 2:** Í klínískum samanburðarrannsóknum á langvarandi ITP með eltrombópagi komu fram hækkun á alanín aminótrentrasíði (ALT), aspartat aminótrentrasíði (AST) og bilirúbíni (sjá kafla 4.8).
**Candidate 3:** Í klínískum samanburðarrannsóknum á langvinna blóðflæðisbólgu með eltrombópagi komu fram hækkaðir gildi alaninamínótransferasa í sermi (ALT), aspartatamínótransferasa (AST) og bilirúbíns (sjá kafla 4.8).
**Candidate 4:** Í klínískum samanburðarrannsóknum á langvinnri ITP með eltrombópagi komu fram aukningu á alanínamínótransferasa (ALT), aspartatamínótransferasa (AST) og blóðrúrubíni í sermi (sjá kafla 4.8).
**Candidate 5:** Í klínískum samanburðarrannsóknum á langvinnum blóðflæðismyndun (chronic ITP) með eltrombópagi komu fram aukningu á alanín amínótransfereiníði (ALT), aspartat amínótransfereiníði (AST) og bilirúbíni í sermi (sjá kafla 4.8).
**Candidate 6:** Í klínískum samanburðarrannsóknum á langvarandi æðasjúkdómi, sem meðferð var stundað með eltrombópagi, komu fram hækkanir á alanín amínótransferasi í sermi (ALT), aspartat amínótransferasi (AST) og bilirubini (sjá kafla 4.8).
**Candidate 7:** Í klínískum samanburðarrannsóknum á langvinnri ITP með eltrombópagi kom fram aukning á alanínamínótransferasa í sermi (ALT), aspartatamínótransferasa (AST) og bilirubíni (sjá kafla 4.8).

</details>

<details><summary>after · G8 · p13official21:test:ema:970 · P</summary>

**Source:** In patients with mild hepatic impairment (Child-Pugh A), there was no significant changes in pharmacokinetics compared with normal healthy volunteers.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Candidate 0:** Hjá sjúklingum með vægt skerta lifrarstarfsemi (Child-Pugh A) voru engin marktæk breytingar á lyfjahvörfum borið saman við eðlilega heilbrigða sjálfboðaliða.
**Candidate 1:** Hjá sjúklingum með væga skerðingu á lifrarstarfsemi (Child-Pugh A) komu engin marktæk breytingar fram á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.
**Candidate 2:** Hjá sjúklingum með væga skerðingu á lifrarstarfsemi (Child-Pugh A) var enginn marktæk breytingar á lyfjahvörfum miðað við eðlilega heilbrigðan sjálfboðalið.
**Candidate 3:** Hjá sjúklingum með væga skerðingu á lifrarstarfsemi (Child-Pugh A) komu engin marktækar breytingar fram á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.
**Candidate 4:** Hjá sjúklingum með væg vansköpun í lifur (Child-Pugh A) var ekki marktæk breytingar á lyfjahvörfum samanborið við eðlilega, heilbrigða sjálfboðaliða.
**Candidate 5:** Hjá sjúklingum með vægan lifrarbilun (Child-Pugh A) var engin marktæk breyting á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.
**Candidate 6:** Hjá sjúklingum með væga skerta lifrarstarfsemi (Child-Pugh A) var enginn marktæk breytingar á lyfjahvörfum samanborið við eðlilega heilbrigðan einstaklinga.
**Candidate 7:** Hjá sjúklingum með væga skerðingu á lifrarstarfsemi (Child-Pugh A) var ekki marktækt breytingar á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.

</details>

<details><summary>after · greedy · p13official21:test:eea:2090 · F</summary>

**Source:** Member States shall require the competent authorities to monitor compliance with this Regulation effectively and take all necessary measures to ensure such compliance.
**Semantic decision:** F — Competent authorities become the apparent recipients of monitoring rather than clearly the authorities required to monitor compliance; agent roles change.
**Candidate 0:** Aðildarríkin skulu krefjast þess að lögbærum yfirvöldum sé gerð skilvirkan eftirlit með því að þau uppfylli þessa reglugerð og þeim gerist allar nauðsynlegar ráðstafanir til að tryggja það.

</details>

<details><summary>before · greedy · p13official21:test:eea:1716 · F</summary>

**Source:** In addition, the competent authorities of Gabon provided evidence to the Commission of the adoption of a new civil aviation code in May 2008, of the development of specific operating regulations for airworthiness and operations, and informed that the decision to establish an independent civil aviation agency (ANAC) was taken and should be promulgated in July 2008.
**Semantic decision:** F — Airworthiness becomes aviation knowledge; civil-aviation and promulgation relations also corrupted.
**Candidate 0:** Einnig lagði lögbær yfirvöld í Gabón fram sannanir um samþykki fyrir framkvæmda- stjórnina um nýja flugregla fyrir ríkisflugina í maí 2008, um þróun sértækra rekstri reglur um flugþekkingu og rekstur og tilkynnti um það að ákvörðunin um að setja stofnun sem er óháð flugmálastofnunum (ANAC) var tekin og ber að framkvæma hana í júlí 2008.

</details>

<details><summary>after · greedy · p13official21:test:eea:607 · F</summary>

**Source:** Years of career break in the current enterprise (optional).
**Semantic decision:** F — Years of career break becomes years of workstations; the employment-break variable is lost.
**Candidate 0:** Ár af vinnustöðvum í núverandi fyrirtæki (valfrjáls).

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:3337 · P</summary>

**Source:** But maybe, if we got away from here, if we went somewhere safe, it could be different.
**Semantic decision:** P — Getting away from here, safe destination and possible different outcome all retained despite inflection.
**Candidate 0:** En kannski, ef við farið úr hér, ef við farið til öruggs staðar, gæti það verið annars konar.

</details>

<details><summary>after · G8 · p13official21:test:eea:1354 · P</summary>

**Source:** Testing at low dosages may be performed by use of OECD 308 (August 2000) or an equivalent method.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Candidate 0:** Gera má rannsóknir á lágu skömmtum með því að nota OECD-staðli 308 (á augustus 2000) eða sambærilega aðferð.
**Candidate 1:** Prófanir á lágum skömmtum má ganga fram með notkun OECD-308 (á ágúst 2000) eða sambærilegu aðferð.
**Candidate 2:** Prófun í lágum skömmtum má framkvæma með nota OECD 308 (á augustus 2000) eða sambærilegri aðferð.
**Candidate 3:** Prófir á smá skömmtum má framkvæma með notkun OECD-staðla 308 (á august 2000) eða sambærilegri aðferð.
**Candidate 4:** Gera má prófanir við lágum skömmtum með því að nota OECD-staðli 308 (á augustus 2000) eða jafngildri aðferð.
**Candidate 5:** Reyndar má prófa á lágum skömmtum með því að nota OECD-staðli 308 (á augustus 2000) eða jafngildri aðferð.
**Candidate 6:** Prófanir á lágum skömmtum geta verið gerðir með samræmi við OECD-staðli 308 (á augustus 2000) eða jafngildri aðferð.
**Candidate 7:** Rannsóknir við lágum skömmtum geta verið framkvæmdar með því að nota OECD stofnunin 308 (á augustus 2000) eða sambærilegt aðferð.

</details>

<details><summary>after · G8 · p13official21:test:eso:502 · F</summary>

**Source:** The first five signals are very confident, while the sixth is tentative, and seventh more tentative still.
**Semantic decision:** F — All eight lose or corrupt the confidence ordering: first five strong, sixth tentative, seventh even more tentative. Candidate0 also drops the seventh.
**Candidate 0:** Fyrstu fimm vísbindingarnir eru mjög tétrar en sjötta er enn afberkt.
**Candidate 1:** Fyrstu fimm hættuna eru mjög ruglu en sjöunduð er frekar til hættu.
**Candidate 2:** Fyrstu fimm víxler eru mjög örvæntugar en sex. sjötthurðin er enn þrálát.
**Candidate 3:** Fyrstu fimm yfirbeina eru mjög gófa, þar sem sexuð er til hættulega og sjöðu til hættulega enn frekar.
**Candidate 4:** Fyrstu fimm mörk eru mjög góð meðtækt og síðustu sex markaðslegt og síðustu sjö markaðslegari enn.
**Candidate 5:** Fyrstu fimm útvarpinu eru mjög tunglæga, en sjötthunnu er tilfinningarskeiðis og sjötthunni ánægjarstefnu.
**Candidate 6:** Eftirfarandi fimm merkjur eru mjög áhatnir og sexist er fyrir haldið og sjötthist er fyrir haldið enn enn frekar.
**Candidate 7:** Fyrstu fimm verka eru mjög góð tilhlýðingu en sjötthi er tilheyrandi, svo sjöthi er alveg tilheyrandi.

</details>

<details><summary>after · greedy · p13official21:test:eea:409 · F</summary>

**Source:** Purpose: to determine whether the test facility, if engaged in studies using animals or other biological test systems, has support facilities and conditions for their care, housing and containment, adequate to prevent stress and other problems which could affect the test system and hence the quality of data.
**Semantic decision:** F — Containment becomes infusion and preventing stress becomes preventing development; the facility requirements change.
**Candidate 0:** Tilgangur: til að ákvarða hvort prófunarstöð varði stofnun og skilyrði fyrir meðhöndlun og húsmiðlun og innrennsli þeirra, sem hún er í notkun í rannsóknum með dýrum eða öðrum líffræðilegum prófunarkerfum, séu nægilegar til að koma í veg fyrir þróun og aðrar vandamál sem geta haft áhrif á prófunarkerfið og þar af leiðandi gæði gagna.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:3044 · F</summary>

**Source:** Isn't there someone in some league, who's left- footed?
**Semantic decision:** F — Left-footed changes to left-handed.
**Candidate 0:** Er ekki einhver í einhverri hópi sem er höfður höndinni til vinstri?

</details>

<details><summary>after · G8 · p13official21:test:eso:434 · F</summary>

**Source:** The guest of honour was the President of Chile, Sebastián Piñera.
**Semantic decision:** F — All eight preserve the name/presidency but replace guest of honour with queen or unrelated invented roles.
**Candidate 0:** Drottningurinn var Sebastían Piñera, forseti Chile.
**Candidate 1:** VG-ríkjaheirinn var Sebastián Piñera, forseti Chile.
**Candidate 2:** Vinuvaldandi var Sebastián Piñera, forseti Chile.
**Candidate 3:** Dýrilögð matnargrein var Sebastián Piñera, forseti Chile.
**Candidate 4:** Ótrússer hisahlutin var Sebastián Piñera, forseti Chile.
**Candidate 5:** Þokinn sitt var Sebástíán Piñera, forseti Chile.
**Candidate 6:** Gassæfarveröðinn var Sebastián Piñera, forseti Chile.
**Candidate 7:** Kveikningsfélagið var Sebastián Piñera, forseti Chile.

</details>

<details><summary>after · G8 · p13official21:test:eea:2090 · P</summary>

**Source:** Member States shall require the competent authorities to monitor compliance with this Regulation effectively and take all necessary measures to ensure such compliance.
**Semantic decision:** P — Candidate1 preserves the requirement for competent-authority effective compliance monitoring and all necessary measures.
**Candidate 0:** Aðildarríkin skulu krefjast þess að lögbær yfirvöld fylgi þessarar reglugerðar með árangri og þessari þörf hafi verið allar nauðsynlegar ráðstafanir til að tryggja að þær vera farið fram.
**Candidate 1:** Aðildarríkin skulu kveða á um þess að lögbært yfirvald sé sjá um skilvirkan eftirlit með því að þessi reglugerð sé uppfyllt og beri þeim tekið allar nauðsynlegar ráðstafanir til að tryggja það.
**Candidate 2:** Aðildarríkin skulu krafast lögbærum yfirvöldum að fylgjast vel með því að þeir stilli þessar reglur væntum til fullnægjandi og gera allar nauðsynlegar ráðstafanir til að tryggja það.
**Candidate 3:** Aðildarríkin skulu gera lögbæru yfirvöldum þess að eftirlit sé farið fram á það að þau uppfylli þessa reglugerð á skilvirkan hátt og takkist allar nauðsynlegar ráðstafanir til að tryggja það.
**Candidate 4:** Aðildarríkin skulu krefjast þess að lögbærum yfirvöldum sé kynnt eftir því að þau séu í hópi til að fylgjast með því að þessari reglugerð sé fullgilt og að þeim sé fylgt allra nauðsynlegra ráðstafana til að tryggja að slík fullgilding eigi sú.
**Candidate 5:** Aðildarríkin skulu krefjast þess að lögbærum yfirvöldum sé framkvæmdastjórnin fylgja vel að þessari reglugerð sé fullnægjandi uppfyllt og þeim gerist allar nauðsynlegar ráðstafanir til að tryggja það.
**Candidate 6:** Aðildarríkin skulu krefjast þess að lögbær yfirvöld hafi hvers konar þörf á að eftirlit með því sé framfylgt hentuglega og að þau teki allar nauðsynlegar ráðstafanir til að tryggja það.
**Candidate 7:** Aðildarríki skulu krefjast þess að lögbær yfirvöld hafi á skilvirkan eftirlit með því að þau uppfylli þessa reglugerð og skuli taka allar nauðsynlegar ráðstafanir til að tryggja það.

</details>

<details><summary>after · greedy · p13official21:test:eea:63 · U</summary>

**Source:** The placement of these devices in the soil should not result in preferential flow paths.
**Semantic decision:** U — Cannot certify the malformed preferential-flow qualifier and causal wording as the intended soil-flow restriction.
**Candidate 0:** Setning þessara búnaðar í jarði ætti ekki að leysa til ávistu flæðisleiða.

</details>

<details><summary>before · greedy · p13official21:test:eso:554 · F</summary>

**Source:** In the lower part of the image a big chunk of the molecular cloud that gave birth to these stellar youngsters still can be seen.
**Semantic decision:** F — Molecular cloud and still visible become physical fog and still okay.
**Candidate 0:** Í lágri hluta myndarinnar er stór flögu af líkamlegu loftþokunni sem fæddi þessar stjörnuunglingar enn í lagi.

</details>

<details><summary>before · G8 · p13official21:test:eso:716 · F</summary>

**Source:** From the gravitational lensing effect, these groups turn out to contain around 30 times more dark than visible matter.
**Semantic decision:** F — No candidate preserves gravitational lensing and dark/visible-matter30-to-one comparison.
**Candidate 0:** Frá slæmu merginormsins færa þessar hópar um 30 sinnum gömul en myndarbúið.
**Candidate 1:** Af rafþekjum í silíðum fjallar þessi hópar um 30 sinnum mikið skemmt á dökkum fyrirritum en réttum.
**Candidate 2:** Í gegnsviknumagalausningu, skal þessi hópar innihalda um 30 sinnum mikið skemmta en myndarvænni efni.
**Candidate 3:** Frá andstræna skýlun er sáttmálum þessi til að koma fram að þeir innihaldi um 30 sinnum fleiri dýraríki en sýnilegt (dark matter).
**Candidate 4:** Framkvæmd grátrumýlunar gefur þessi hópar yfirleitt 30 sinnum meiri skertu en sýnilegt.
**Candidate 5:** Í ljósmyndunartruflunum urðu þessi hópar aðeins í um 30 sinnum miklar djúpt en sýnilegar efnis.
**Candidate 6:** Stöurnáingurinn ser yfir þessi hópar í aldur 30-faldi mikið skemmta en myndi.
**Candidate 7:** Af geimfræðilegri myndun þess, upphafstækur þessi hópar eru um það bil 30 sinnum mikið skerðri en litlaður vatn.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:3044 · F</summary>

**Source:** Isn't there someone in some league, who's left- footed?
**Semantic decision:** F — Left-footed is replaced by a headed/from-the-side phrase; the requested football attribute disappears.
**Candidate 0:** Er enginn í einhverri hóp sem er höfður frá hliðar?

</details>

<details><summary>before · greedy · p13official21:test:ema:1152 · P</summary>

**Source:** Change from baseline in body weight was similar for patients treated with sitagliptin relative to placebo.
**Semantic decision:** P — Body-weight change from baseline similar for sitagliptin versus placebo retained.
**Candidate 0:** Breyting frá grunngildi á líkamsþyngd var svipuð hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.

</details>

<details><summary>before · G8 · p13official21:test:eea:1354 · P</summary>

**Source:** Testing at low dosages may be performed by use of OECD 308 (August 2000) or an equivalent method.
**Semantic decision:** P — Candidates2/6 retain low-dose testing, OECD308August2000 and equivalent-method alternative.
**Candidate 0:** Gera má rannsókn á lágum skömmtum með tilvísun á OECD 308 (á august 2000) eða jafngildri aðferð.
**Candidate 1:** Gera má rannsóknir á litlum skömmtum með að nota OECD 308 (á augustus 2000) eða samsvarandi aðferð.
**Candidate 2:** Prófun í lágum skömmtum má framkvæma með nota OECD 308 (á augustus 2000) eða sambærilegri aðferð.
**Candidate 3:** Hægt er að nota OECD 308 (á augustus 2000) eða jafngildan aðferð til að mæla úr líkamsrannsóknum við lítinn skammtar.
**Candidate 4:** Gera má rannsóknir á lágum skömmtum með þeim aðferðum sem gerðar eru með OECD 308 (á augustus 2000) eða sambærilegri aðferð.
**Candidate 5:** Reyndar má prófa á lágum skömmtum með sérhæfðum aðferðum, sem samkvæmt OECD 308 (August 2000) eru komin í ljós eða samsvarandi aðferð.
**Candidate 6:** Prófun í lágum skömmtum má framkvæma með notkun OECD 308 (á august 2000) eða sambærilegrar aðferða.
**Candidate 7:** Rannsóknir á lítilum skömmtum má gerð með rannsóknarmskerfi OECD 308 (á augustus 2000) eða jafngildri.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:2164 · F</summary>

**Source:** You didn't have the guts to do it yourself.
**Semantic decision:** F — Guts/courage becomes an unrelated exempt-person term.
**Candidate 0:** Þú hafðir ekki undanþegi til að gera það sjálfur.

</details>

<details><summary>after · G8 · p13official21:test:eso:908 · F</summary>

**Source:** This bridge, which has not been seen before (and is too faint to show up in this picture), is somewhat bluer than either galaxy, indicating that it consists of stars created in gas that was drawn away from NGC 1387 by the gravitational pull of NGC 1399.
**Semantic decision:** F — All eight corrupt faintness/bluer colour, stellar origin or gravitational pulling relation; none preserves the bridge explanation.
**Candidate 0:** Þessi brú, sem hefur ekki séð áður og er of lágt til að sjá það í myndinni, er líklega blárari en annarði vetrarbrautin og gefur til kynna að það er úr stjörnum sem eru búin upp í gas sem lítið var frá NGC 1387 við því að viðbrigðisverk NGC 1399 veldur það.
**Candidate 1:** Þessi brú, sem hefur ekki sést áður (og er of fallegur til að sjá upp í þessari mynd), er blár en annar galdrirnar, sem býr til að það besti er af stjörnum sem reynist í gas sem var tekinn úr NGC 1387 vegna þyngdshlutfalls NGC 1399.
**Candidate 2:** Þessi brú, sem hefur aldrei séð svona (og er of myndarlegur til að sýna í myndinni), er aðeins fjarlægari en annarri vetrarbrautinu og gefur til kynna að hún samanstendur af stjörnum sem eru úr gæmi sem NGC 1387 var dragað út frá NGC 1399 vegna svæðislagar.
**Candidate 3:** Þetta brú, sem hafa ekki sést áður (og er of myrt til að sýna í myndinni), er smávísi fjarlægari en önnur vetrarbraut, að þeim tilgangi að það samanstendur af stjörnum sem byggðust út úr gasi sem NGC 1387 var dragið frá með gildistirningum NGC 1399.
**Candidate 4:** Þessi brú, sem hefur ekki sést áður (og er of skertur til að sýna í myndinni), er mikið grári en annarri vetrarbrautinni og bendir til þess að hún er úr stjörnum sem fóru upp í gasskipti sem snattur var frá NGC 1387 samkvæmt áfalli á NGC 1399.
**Candidate 5:** Þessi brú, sem hefur ekki séð áður (og er of þungur til að sjást í þessari mynd) er börn búnar breiðari en annar hvolf vetrarbrautarnar og benda til þess að það sé staðað fyrir úr myndum úr gasi, sem var draginn úr NGC 1387 af því að NGC 1399 dragir hana á sig.
**Candidate 6:** Þessari brú, sem hefur aldrei komið fram áður og er öfugt dimmaður til að sjást í þessari mynd, er einhversliður vardur en annar galdrar, sem benda til þess að hann innihaldi stjörnur sem eru myndaðar úr gasi sem var snúið úr NGC 1387 af þeim gigtarvengslum NGC 1399.
**Candidate 7:** Þess stefnu, sem hefur ekki sést áður og er ýmsilega blár en annar galnir, gefur til kynna að það samanstendur af stjörnum sem voru uppmyndar úr gasi sem var drífinn úr NGC 1387 vegna svæðisvörunar NGC 1399.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:2128 · F</summary>

**Source:** Don't you worry about those dope smokers and nudists down below there?
**Semantic decision:** F — Dope smokers and nudists are replaced by unrelated/corrupt terms; the worried question is also altered.
**Candidate 0:** Ekki hafa áhyggjur af þessum döpumrúmstjörnum og náttuglum þarna niðri?

</details>

<details><summary>after · G8 · p13official21:test:eso:710 · F</summary>

**Source:** The VST KiDS survey will allow astronomers to make precise measurements of dark matter, the structure of galaxy halos, and the evolution of galaxies and clusters.
**Semantic decision:** F — All eight corrupt dark matter, halo structure or galaxy/cluster evolution; candidate4 still replaces halo structure by galactic-family positions.
**Candidate 0:** VST KiDS verndar sér með skiljanlegum mælingum á dökkum vetrarbrautum, þróun vetrarbrauta og vetrarbrautahrolla og stjörnumerkinu.
**Candidate 1:** VST KiDS rannsóknin mun gera stærðfræðingum kleift að gæta nákvæmra mælinga á dökkum efni, lígræðslu úr glerhlaupi vetrarbrauta og sjónakerfinu og þróun vetrarbrauta og vetrarbrautagreinar.
**Candidate 2:** VST KiDS rannsóknin hefur ávinning fyrir stjörnufræðingar sem geta gerð nákvæmar mælingar á dreifibundið vökva, myndun svæða kettillar vetrarbrautanna og myndun vetrarbrauta og þrýstingar.
**Candidate 3:** VST KiDS rannsókninni er unnt stjörnufræðingar að gera nákvæmar mælingar á dökkum efni, stökkbreytingum vetrarbrauta og miglingum hliða vetrarbrautanna og þremum.
**Candidate 4:** VST KiDS rannsóknin gerir stjörnufræðingum kleift að gera nákvæmar mælingar á dökkum efninu, stæðum vetrarbrautafjölskyldunnar og þróun vetrarbrauta og vetrarbrautahópa.
**Candidate 5:** VST KiDS rannsóknin tekur stærðfræðingum auðkenna nákvæmar mælingar á djöfullum, þróun svæða vetrarbrautum og hliðs vetrarbrauta, og þróun vetrarbrautar og þróunar vetrarbrautahópa.
**Candidate 6:** VST KiDS verndaráætlunin mun láta stjörnufræðingum mæla nákvæmlega á dark matter (svarkyrningum), gegnumbúðir rimmalausa snotta og þróun ramma og þunga.
**Candidate 7:** VST KiDS rannsóknin mun gera stjörnufræðingum kleift að gera nákvæmar mælingar á dýrum í djöfula, byggingu útlægjar vetrarbrauta og þróun vetrarbrautanna og vetrarbrautahópa.

</details>

<details><summary>after · greedy · p13official21:test:ema:992 · P</summary>

**Source:** Animal studies have shown excretion of retagabine and/or its metabolites in breast milk.
**Semantic decision:** P — Retains animal studies showing retagabine and/or metabolite excretion in breast milk.
**Candidate 0:** Dýrarannsóknir hafa sýnt að útskilnaður er af retagabíni og/eða umbrotsefnum þess í brjóstamjólk.

</details>

<details><summary>before · greedy · p13official21:test:ema:2175 · P</summary>

**Source:** Breast-feeding must be stopped on initiation of treatment with Voriconazole Accord.
**Semantic decision:** P — Breastfeeding must stop at treatment initiation retained.
**Candidate 0:** Hætta verður brjóstagjöf við upphaf meðferðar með Voriconazole Accord.

</details>

<details><summary>after · G8 · p13official21:test:ema:2652 · P</summary>

**Source:** Put the needle fully into the skin as shown by your nurse or doctor (see picture 6).
**Semantic decision:** P — Candidate1 correctly says to insert the needle fully into the skin as shown by doctor/nurse and retains picture6.
**Candidate 0:** Setjið nálinni fullt í húðina eins og náein eða læknirinn sýnir (sjá mynd 6).
**Candidate 1:** Setjið nálina að fullu í húðina eins og læknirinn eða hjúkrunarfræðinginn sýnir (sjá mynd 6).
**Candidate 2:** Settu nálinni að fullu í húðina eins og verja hjá sjúklingi eða lækni sýnir (sjá mynd 6).
**Candidate 3:** Settu nálinni á fullu í húðina eins og meðferðarlæknirinn eða meðferðarátrið sjúklingarnar sýna (sjá mynd 6).
**Candidate 4:** Settu nálinni fullt inn í húðina eins og fræðandi eða hjúkrunarfræðingurinn sýnir (sjá mynd 6).
**Candidate 5:** Setjið nálinni yfir í húðina eins og hjá sjúklingarinni eða lækninum sýnt er í sýni (sjá mynd 6).
**Candidate 6:** Settu nálinu hvarflega í húðina eins og nálinn kemur fram á sér við hjúkruninum eða lækninn (sjá mynd 6).
**Candidate 7:** Settu nálinni í brjóstið fullt inn við þig og ruglar þinni fyrir hjá sjúklingaryfirlindinum eða lækninum (sjá mynd 6).

</details>

<details><summary>before · greedy · p13official21:test:eso:908 · F</summary>

**Source:** This bridge, which has not been seen before (and is too faint to show up in this picture), is somewhat bluer than either galaxy, indicating that it consists of stars created in gas that was drawn away from NGC 1387 by the gravitational pull of NGC 1399.
**Semantic decision:** F — Too faint becomes light-giving; galaxy/gravity terms also corrupted.
**Candidate 0:** Þessi brú, sem hefur ekki séð áður (og er of ljósgæf til að sýna í myndinni) er einhverskju blárri en annar galdrar, sem benda til þess að hún er úr stjörnum sem eru myndar úr gasi sem var dragað út frá NGC 1387 af gildislagi NGC 1399.

</details>

<details><summary>before · greedy · p13official21:test:eea:1503 · F</summary>

**Source:** If this kind of costs exists, they will be reported separately.
**Semantic decision:** F — Separately reported becomes reporting under special conditions.
**Candidate 0:** Ef slík kosti eru til koma þeir til skýrslu í sérstökum skilyrðum.

</details>

<details><summary>before · greedy · p13official21:test:ema:992 · P</summary>

**Source:** Animal studies have shown excretion of retagabine and/or its metabolites in breast milk.
**Semantic decision:** P — Animal studies, excretion, drug/metabolites and breast milk all retained.
**Candidate 0:** Dýrarannsóknir hafa sýnt fram á útskilnaður retagabíns og/eða umbrotsefna þess í brjóstamjólk.

</details>

<details><summary>after · greedy · p13official21:test:eea:1471 · F</summary>

**Source:** Prices including all taxes, levies and VAT.
**Semantic decision:** F — The VAT and levy wording is corrupted beyond inflection, failing to preserve the specified taxes.
**Candidate 0:** Verð þar sem tilgreind er allar skattir, skattatökin og gildaaukaverða skattagátt.

</details>

<details><summary>after · G8 · p13official21:test:ema:437 · F</summary>

**Source:** Lenvatinib should not be started in patients with fistula to avoid worsening and lenvatinib should be permanently discontinued in patients with oesophageal or tracheobronchial tract involvement and any Grade 4 fistula (see section 4.2); limited information is available on the use of dose interruption or reduction in management of other events, but worsening was observed in some cases and caution should be taken.
**Semantic decision:** F — All eight corrupt fistula/anatomical involvement or discontinuation conditions. Candidate0 explicitly reverses the instruction to stop treatment.
**Candidate 0:** Ekki skal hefja meðferð með lenvatinibi hjá sjúklingum með liðverða til að koma í veg fyrir versnun og ekki skal hætta meðferð með lenvatinibi hjá sjúklingum með fæðu í munna eða flogfræðurs eða flogfræðisverkur og einhverja 4. stigs liðverða (sjá kafla 4.2); takmarkaðar upplýsingar liggja fyrir um notkun skrefa meðferðar eða skammtalækningar við meðferð á önnur tilvik, en versnun kom fyrir fyrir mælt í tilvikum og nauðsynlegt er að gæta varúðar.
**Candidate 1:** Ekki skal hefja meðferð með lenvatinibi hjá sjúklingum með glötu þar með tilliti til þess að hægt sé að auka og ekki skal þegar einmitt nota lenvatinib hjá sjúklingum með bíldu í hlökku eða stofnauðskera og hvernig sem er fjölda 4 stigar glötu (sjá kafla 4.2); takmarkaðar upplýsingar liggja fyrir um notkun skiptis á skömmtum eða minnkaðar skammta vegna meðferðar á öðrum ábendingum en á baklanum varð vart við skoðun og það skal gæta varúðar.
**Candidate 2:** Ekki ætti að hefja meðferð með lenvatinibi hjá sjúklingum með glæs to ofnæmi til að koma í veg fyrir versnun og slökkva skal meðferð með lenvatinibi hjá sjúklingum með þvaggjúlkur/þræðubrjóstur- og efnalegur skerðingar og hvegna (4.2) fyrir 4. stigs glæs to (aukít máttar upplýsingar um skiptingu á skömmtum eða minnkaðan skammt eftir aðlögu meðferðar annarra aukna tilvik efnis, en versnun sást hjá nokkrum tilvika og gæta skal varúðar.
**Candidate 3:** Ekki á að hefja meðferð með lenvatinibi hjá sjúklingum með liðarmaslóð til að útiloka aukningu sjúkdóms og hætta skal að lenvatinib sé hætt viðvarandi hjá sjúklingum með svæði á háls eða lágæða og öllu stigi 4 liðarmaslóð (sjá kafla 4.2); takmarkaðar upplýsingar liggja fyrir um notkun skiptis á skömmtum eða minnkaðrar skammta við meðferð á öðrum fyrirvara til viðbótar en aukning fór fram í nokkrum tilvikum og skal gæta varúðar.
**Candidate 4:** Ekki skal hefja meðferð með lenvatinibi hjá sjúklingum með þræðaleið, til að koma í veg fyrir versnun og skal hætta meðferð með lenvatinibi hafa sjúklingar með ítar í þræðaleið eða í lungnabrennileið og allt að 4. stig þræðaleið í allt meðan í meðferð stendur (sjá kafla 4.2); takmarkaðar upplýsingar liggja fyrir um notkun skamslyfsinnils eða lækkunar í meðferð máli fyrir önnur tilvik, en versnun kom fram í sumum tilvikum og þess á að gæta varúðar.
**Candidate 5:** Hefja skal ekki meðferð með lenvatinibi hjá sjúklingum með liðþarm til að koma í veg fyrir versnun sjúkdómsins og stöðuga hætta skal meðferð með lenvatinibi hjá sjúklingum með ítarlið eða stúðubronns- eða öxltrýni og hvort sem er í 4. stigs lið þarm (sjá kafla 4.2). Önnur upplýsingar eru takmarkaðar um meðferð með skammtahætti eða minnkaðri skömmtun við meðferð annarra sjúkdóma en hins vegar hefur verið fram komið aukning hjá nokkrum tilvikum og skal gæta varúðar.
**Candidate 6:** Ekki skal hefja meðferð með lenvatinibi hjá sjúklingum með geið þegar tryggð er að geið skyndi til að koma lengur í búnað og hægt er að fengja það aðeins við meðferðina (meðferðarheimild) hjá sjúklingum með aðstoð í geið á lálægum og hollægum liðum til að hafa hafa skyndi með á vágar (sjá kafla 4.2). Að finnunum er til að finnast er búið til að nota skammtatap eða minnka skammta við meðferð á önnur atriði, en þegar það varðar að ljúga viðbótarhætti varðar aðeins að seljast við, og skal gæta varúðar þegar sjúkdómið versnaði.
**Candidate 7:** Ekki á að byrja meðferð með lenvatinibi hjá sjúklingum með glæsi til að forðast að það væri aukin og ekki á að halda meðferð með lenvatinibi hjá sjúklingum með efnatengdum eða þræðingar í lungnaslagræði eða hvaða stig 4 á gráðu glæsi (sjá kafla 4.2); takmarkaðar upplýsingar liggja fyrir að notað sé stöðugt að gáttu hálfu meðferðaráhvarf eða minnka áhættu meðferð vegna annarra áborða en það hækkaði sjúkdóm af breytingum í smástundum og það skal gæta varúðar.

</details>

<details><summary>after · G8 · p13official21:test:eso:45 · P</summary>

**Source:** This would make the system similar to our Solar System in terms of the number of planets (seven as compared to the Solar Systems eight planets).
**Semantic decision:** P — Candidate6 preserves similarity to our Solar System by planet count, seven versus eight; the similarity adjective is malformed but the comparison is clear.
**Candidate 0:** Þetta myndi laga kerfið með þokunni svo að sólarkerfinu þar sem að vollar sem er í þessum kerfi (sjö til samanburðar við átta gler í sólarkerfinu).
**Candidate 1:** Það myndi gera kerfið sambærilegt úr sólkerfi okkar í því skyni að fjöldi reikur (sjö á móti áttu í sólkerfinu).
**Candidate 2:** Þetta myndi gera kerfið svipuð verjanda sætuskerlum á grundvelli fjölda reikistjarna (sjö eftir samanburði við átta reikistjörnurnar í verjanda sætuskerlunni).
**Candidate 3:** Þetta myndi skaðað kerfið eins og sólkerfi okkar í þeirri lagi að fá fjögurra reikistjörnum (sjötugt samanborið við átta reikistjörnurnar í sólkerfinu).
**Candidate 4:** Þetta myndi gera kerfið svipað helstu reikistjörnuvera í ljósglerfinu (sjö jörðir samanborið við aðrir árshlutar einar reikistjörnuvera).
**Candidate 5:** Þetta myndi gera kerfið svipuðið sólarkerfinu vegna fjölda plöntu (sjö við þá átta plöntu sólarkerfisins).
**Candidate 6:** Það myndi geri kerfið svipufram sólkerfisins okkar í þeim þáttum sem færust í fjölda reikistjarna (sjö þegar samanborið við átta reikistjarna í sólarkerfinu).
**Candidate 7:** Það myndi bregða skipunina í líkum sólarbreyta í það lagi að fjölda reikistjarna (sjö með tilliti til þeirra á móti þeim sólarbreyti sem hefur átt níu reikistjörnur).

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:1878 · P</summary>

**Source:** That's not what Optimus would want.
**Semantic decision:** P — Exact source/hypothesis semantic reuse from card78: Negated claim about what Optimus would want retained.
**Candidate 0:** Það er ekki það sem Optimus vildi.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:936 · P</summary>

**Source:** Ma'am, I need the gentleman's signature so we can begin.
**Semantic decision:** P — Need the gentleman signature to begin retained; inflection errors only.
**Candidate 0:** Frú, ég þarf undirskriftur herra til að byrja.

</details>

<details><summary>before · greedy · p13official21:test:ema:2650 · F</summary>

**Source:** Patients should be advised that in the event of any sudden visual defect, they should stop taking Sildenafil Actavis and consult a physician immediately (see section 4.3).
**Semantic decision:** F — Sudden visual defect becomes a different visual impairment; sudden-onset condition is lost.
**Candidate 0:** Sjúklingum skal ráðlagt að hætta tafarlaust meðferð með Sildenafil Actavis ef þeir fá sér ólíka sjónskerðingu og leita læknis tafarlaust (sjá kafla 4.3).

</details>

<details><summary>before · G8 · p13official21:test:eso:434 · F</summary>

**Source:** The guest of honour was the President of Chile, Sebastián Piñera.
**Semantic decision:** F — Candidate3 gives a guest but omits honour status; all others corrupt guest/president roles.
**Candidate 0:** Drottningurinn var Sebastían Piñera, forseti Chile.
**Candidate 1:** Jafiðið sýnitsýna var Sebastián Piñera, forseti Chile.
**Candidate 2:** Vinuvaldandi var Sebastián Piñera, forseti Chile.
**Candidate 3:** Gesturinn var Piñera Sebastián, forseti Chile.
**Candidate 4:** Stórarfélagið var hér með forsetanum, Sebastián Piñera, forsetanum Chile.
**Candidate 5:** Höfuðsmanur Chile, Sebastián Piñera var beinmannið.
**Candidate 6:** Gassögumennin var Sebastián Piñera, forseti Chile.
**Candidate 7:** Kveikningsborgarni var Próprésident Chile, Sebastián Piñera.

</details>

<details><summary>after · greedy · p13official21:test:eso:1168 · F</summary>

**Source:** R Coronae Australis itself is not visible to the unaided eye, but the tiny, tiara-shaped constellation in which it lies is easily spotted from dark sites due to its proximity on the sky to the larger constellation of Sagittarius and the rich star clouds towards the centre of our own galaxy, the Milky Way.
**Semantic decision:** F — The tiara-shape descriptor and rich star clouds are corrupted; the latter becomes pressure stars.
**Candidate 0:** R Coronae Australis sjálfur er ekki sýnt á auga án hjálpar, en það litla, tiara-þekkt stjörnumerkin sem það er í er auðveldlega sýnt frá dökkum staðsetningu vegna nærþegna þess við stærri stjörnumerkin Sagittarius og þrýstingarstjörnum í miðju Vetrarbrautarinnar.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:1601 · P</summary>

**Source:** I don"t plan on wearing it that long.
**Semantic decision:** P — Intention not to wear it for long preserved; minor comparative-duration wording.
**Candidate 0:** Ég ætla ekki að vera í því lengi.

</details>

<details><summary>after · G8 · p13official21:test:eea:409 · F</summary>

**Source:** Purpose: to determine whether the test facility, if engaged in studies using animals or other biological test systems, has support facilities and conditions for their care, housing and containment, adequate to prevent stress and other problems which could affect the test system and hence the quality of data.
**Semantic decision:** F — All eight corrupt care/housing/containment requirements or prevention of stress; several replace stress by development or depression and change the required facilities.
**Candidate 0:** Tilgangur: til að ákvarða hvort prófunarstöðvar, ef á sér stað prófanir handa dýrum eða annarri líffræðilegu prófunarkerfum, hafi stuðningsaðstæður og skilyrði til að hafa á heimsóknum, viðtökum og inngripunandi áhrifum og að þau uppfylli nauðsynleg skilyrði til að koma í veg fyrir þrýsting og aðrar vandamál sem geta haft áhrif á prófunarkerfið og þess vegna þarðar gæði gagna.
**Candidate 1:** Tilgangur: að ákvarða hvort prófunarstöðvar, ef þar er gerð rannsóknir með dýrum eða öðrum líffræðilegum prófunarkerfum, eiga til stuðnings og skilyrði fyrir að fylgja þeim, hýsa og þéla þeim, sem nægur og fullnægjandi gætu komið í veg fyrir þunglyndi og aðrar vandamál og hafi þau áhrif á prófunarkerfið og því gæði gagna.
**Candidate 2:** Tilgangur: að ákveða hvort prófunarstöð varði til þess hvaða þyngd og aðstæður fyrir aðhófi, heimilis- stöðu og tilhögun fyrir þau erannkvæmar og geta komið í veg fyrir þrösti og aðrar vandamál hjá prófunarsniðinu og þannig gert gæni á gæði gagna.
**Candidate 3:** Tilgangur: til að ákvarða hvort prófunaraðsetningur, ef henni er hóp hafa verið tilraunum með dýrum eða öðrum lífverulegra prófunarkerfum, er ásamt starfshlutum til að stuðla að henni, húsi henni og hafa hún í fanglæti, hvað varðar meðferð og varðandi áhættu gegn þröstum og öðrum vandamála sem gætu haft áhrif á prófunarkerfið og þannig á gæði gagna.
**Candidate 4:** Tilgangur: að ákvarða hvort prófunarstöð, í þeim tilfelli að prófa þýðir eða annað lífveruleg prófunakerfi, hefur stuðningsaðstæður og skilyrði fyrir að halda þeim, veita dýrum og tölum, að skilvirkan hátt til að koma í veg fyrir þróun og aðra vandamál sem gætu haft áhrif á prófunakerfinu og þar með leið og gæti aukið gæði gagna.
**Candidate 5:** Markmiðið: að ákvarða hvort rannsóknarstöð, ef hún er í rannsóknir með dýrum eða annarri líffræðilegri prófunarkerfi, fylgir meðferðarstöðum og skilyrðum til að fylgjast með henni, fyrir húð og meðhöndlun, sem fullnægjandi er til að koma í veg fyrir ávatið og önnur vandamál sem geta haft áhrif á prófunarkerfið og þar af leiðandi gæti á gæði gagna.
**Candidate 6:** Tilgangur: að meta að prófunarstöðvar, ef þær taka þátt í rannsóknum á dýrum eða annarra lífvirkra prófunarkerfa, hafi stuðningsaðstæður og skilyrði til að viðhafa þá, hýsa þá og því að þau séu fyrirhuguð, svo að það koma í veg fyrir þróun og aðrar vandamál sem getur haft áhrif á prófunarkerfið og þar með heldur gæði gagna.
**Candidate 7:** Tilgangur: að ákvarða hvort prófunarstöðvar, ef þar eru rannsóknir með dýrum eða aðrar líffræðilegar prófunarkerfum, hafa áætlanir til stuðnings og aðstoðar þess, að því er varðar varðveitingu, atvinnu og samkvæmt fjarlægingu, til að koma í veg fyrir þróun og aðrar vandamál sem gætu haft áhrif á prófunarkerfinn og þannig gætu haft áhrif á gæði gagna.

</details>

<details><summary>after · greedy · p13official21:test:eea:1831 · F</summary>

**Source:** However fibreboards classified as class A will be accepted if they do not represent more than 50 % of the total wood and wood-based materials used in the product.
**Semantic decision:** F — Fibreboards and wood/wood-based materials become unrelated tissue/growth terms.
**Candidate 0:** Hins vegar verður viðurkennd þeirra vefjaskírni sem eru flokkaðar í flokk A ef þær eru ekki meira en 50% af heildarvöxt og vöxtarafurðum sem notaðar eru í vörunni.

</details>

<details><summary>after · greedy · p13official21:test:eea:571 · F</summary>

**Source:** To check power-operated windows/roof-panel systems/partition systems with reversing devices, a measuring instrument/test rod shall be placed through the opening from the inside of the vehicle or, in the case of a partition system, from the rear part of the passenger compartment in such a way that the cylindrical surface of the rod contacts any part of the vehicle structure which forms the boundary of the window/roof-panel aperture/partition.
**Semantic decision:** F — The rear passenger-compartment location and cylindrical rod geometry are corrupted.
**Candidate 0:** Til að kanna áræði öllu þar sem styrk er notað til að opna glugga/þekjuflöt/virki með endurkomuferli skal setja mælitæki/prófunartörl yfir slíkt opnun í innanbúningu ökutækisins eða, ef um er að ræða virki, frá afturhlið sjóðarinnar, þannig að hringlífurinn snertir einhverja hluta af byggingu ökutækisins sem eru viðmiðunarmörk slíks opnunar.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:3404 · P</summary>

**Source:** A mother never gives up on her child.
**Semantic decision:** P — Mother never giving up on her child retained despite imperfect idiom.
**Candidate 0:** Mamma gefur aldrei upp á barni sínu.

</details>

<details><summary>before · G8 · p13official21:test:eea:79 · F</summary>

**Source:** Justified estimates must be made of the expected concentrations of the active substance and relevant metabolites, degradation and reaction products, in soil, groundwater, surface water and air, following use as proposed or already occurring.
**Semantic decision:** F — All corrupt degradation/reaction products or soil/groundwater/surface-water/air compartments and justified-estimation scope.
**Candidate 0:** Vottun skal gera grunngottar áætlanir um hliðstæðan þéttni virka efnisins og viðkomandi umbrotsefna, umbrotsefnaþekkingar og efni sem eru afleidd úr umbroti í jarðvökunni, grunnvatni, yfirborðsvökunni og lofthvöði, eftir notkun eins og mælt er fyrir um eða þegar það hefur verið að sé.
**Candidate 1:** Gera verður réttar áætlanir um búist við styrk virka efnisins og viðkomandi umbrotsefna, umbrotsefnafræðilegum afleiðingum og lyfjagöfum í jarðabúði, grundvökva, yfirborðawatni og lofthjóði eftir notkun sem mælt var fyrir um eða sem þegar eru til.
**Candidate 2:** Gera verður réttar mat á búistæðum þéttni virka efnisins og viðkomandi umbrotsefna og framleiðslu- og hlutverkafæra í jarðinu, grunnvatni, yfirlokvatni og loysi eftir notkun eins og pú er ráðið eða hafa orðið til.
**Candidate 3:** Gera skal réttar mataríki um hugsanlegu styrk virka efnisins og viðeigandi umbrotsefna, umbrotsefni og framleiðsluafurða í jarðverri, grundvöllvöru, vöðva, baksvöru, yfirborðsvöru og lofti, eftir notkun eins og mælt er fyrir um eða þegar það er gerð.
**Candidate 4:** Gera verður réttleggrekninga um búnaður og fyrirhuguðum styrk virka efnisins og áhrifalega umbrotsefnis og umbrotsefnifæri í jarðvatni, grunnvatni, yfirbólguvatni og lofthjóði, eftir notkun eins og mælt er fyrir um eða sem hefur þegar orðið.
**Candidate 5:** Gera skal réttan mat á viðfangseðlandi styrk virka efnisins og viðkomandi umbrotsefna, umbrotsefnisstofna ogafbrotu í jarðverri, grunnvatni, yfirborðsvatni og lofthvötu eftir notkun eins og hún hefur komið fyrir eða á bilinu.
**Candidate 6:** Sjálfkærar mat skal gera á virku efninu og viðkomandi umbrotsefnum og framleiðsluefnum í jarðvökju, grunnvatni, yfirborðsvökju og lofthjálp, eftir notkun eins og mælt er fyrir um eða þar sem það hefur orðið.
**Candidate 7:** Komi réttlætt mat á búist við á því að áætlaðir þéttni virka efnisins og viðkomandi umbrotsefnis, umbrotsefna- og framleiðsluefnis, í jarðvökva, jarðvatn, yfirborðsvökva og lofti eigi að fylgja, eftir notkun sem leið og til kynna kemur fram eða það er hafa orðið til komið.

</details>

<details><summary>before · G8 · p13official21:test:eso:1198 · P</summary>

**Source:** The new observations are thus the first direct confirmation of such models.
**Semantic decision:** P — Candidate4 preserves new observations as first direct confirmation of these models.
**Candidate 0:** Nýja mælingarnar eru því fyrsta beinu staðfestir á slíkum líkamum.
**Candidate 1:** Nýjar mælingarnar eru því fyrsta beinu staðfestur á slíkum líkani.
**Candidate 2:** Nýjar upplýsingarnar eru það í þessu samhengi fyrstu beina staðfestir á sva tíma líkam.
**Candidate 3:** Nýir mælingarnar eru því fyrsta beinu staðfestingin á slíkum líkani.
**Candidate 4:** Nýjar mælingarnar eru því fyrsta beinu staðfestingu þessara líkönanna.
**Candidate 5:** Nýir mælingarnar eru því fyrstu beinu staðfestingar á slíkum skipum.
**Candidate 6:** Nýja mælingarnar eru þannig fyrsta beinkoll á slíkum líkamerjum.
**Candidate 7:** Nú skulu nýjar mælingarnar höfðast í fyrsta sinn að draga beint í ljósi samræmingu um svona líkennur.

</details>

<details><summary>before · G8 · p13official21:test:eea:2120 · F</summary>

**Source:** In order to facilitate data flows from the European Union, it is desirable for processors providing data-processing services to several data controllers in the European Union to be allowed to apply the same technical and organisational security measures irrespective of the Member State from which the data transfer originates, in particular in those cases where the data importer receives data for further processing from different establishments of the data exporter in the European Union, in which case the law of the designated Member State of establishment should apply.
**Semantic decision:** F — All corrupt processor/controller/importer/exporter roles or the establishment-law conditions.
**Candidate 0:** Til þess að draga úr flutningum gögn frá Evrópusambandi er réttlegt að meðferðarþegar fá gögn (processors) sem veita gagnagjaferaðlun þátttakendur í Evrópusambandinu séu heimilt að gera sömu tæknilega og stjórnsýslu- öryggisvörunir án tillits til aðildarríkis þar sem gögnin bori fram samkvæmt, einkum þegar gagnasamfærðarið bahar gögn sem öðrum stöðum útflutningsþegara í Evrópusambandinu gefa nýtt gagnafrumskerfið, þar sem skal beita löggjöf tilnefndrar aðildarríkisins.
**Candidate 1:** Til þess að gera gagnagjaf frá Evrópusambandinu auðvelt er æskilegt að vinnuveitendur, sem veitir gagna- rekstrarþjónustu til meira endurspeglinga gagna-/innprófunaryfirvalda í Evrópusambandinu, séu heimilt að beita sömu tæknilegum og stjórnsýsluefnislegum öryggismeðferðum án tillits til aðildarríkis af því frá sem gagna- rekstrarflytjan er hér fyrir fram á, einkum þegar gagna- innflytjandan næst gagna frá annarra stofnanum fyrir gagna- úflings í Evrópusambandininu, þá skal þá beita löggjöf landsins þar sem stofnunin er tilnefnd.
**Candidate 2:** Til þess að auðvelda gagnagjöf frá Evrópu- samræðunni ætti því að hægt sé að aðildarríkinu á að veita gagna- útvarpsfyrirtækinum sem fá gögn, sem eru útvarpaðir, samanborið við fleiri gagna- megi í Evrópu- samræðunni, sambærilegar tæknilegar og stjórnsýslu- kerfi, án tillits til aðildarríkisins þar sem gagnirnir eru sendar úr, einkum þegar gagna- innameðaerðin fær gögn til frekari gagna- útvarps frá mismunandi stofnunum sem senda gagna í Evrópu- samræðunni, og án tillits til hvers aðildarríkis sem stofnun sendir gagna í Evrópu- samræðunni.
**Candidate 3:** Til þess að auðvelda gagnamöguleika frá Evrópusambandinu ber, í tengslum við þau stjórnendur gagnasjóða sem fá gagnagjaf, að heimila vera að þau ekki skuli fá að gera sami tæknilega og stjórnunarheimildir án tillits til þess aðildarríkis, sem gagnamálastarfsemi er hnefil frá, einkum þegar gagnamálastarfsemi hefur viðkomist frá mismunandi stofnunum gagnamálastarfsemi í Evrópusambandininu, þá skal beita lögum þeirra aðildarríkis, sem tilnefnt er til staðfestu.
**Candidate 4:** Til þess að skipti gögn fari greinilega um evrópubandalaginu er krafist að tæknifyrirtækjum sem leggja út gögn í fjölda í umfangi tilskipana evrópubandalagsins að vera heimilt að beita sömu tæknilegar og stjórnsýslustöfunar- kerfin, óháð því hvaða aðildarríki gögnin koma frá, einkum þegar innfylgjandi er fjármálagjafa gefi gögn til frekari gjafar úr annarrum stofnanum úr evrópubandalagsins sem sendir gögnum, þá skal beita löggjöf staðfestu aðildarríkisins.
**Candidate 5:** Til þess að auðvelda gagnamögnun frá Evrópusambandinu er það bein til að heimila rekstillum sem veita gagnagjafarþjónustu fyrir nokkrum gagna- skipum í Evrópusambandinu að beita sömu tæknilegum og stjórnsýsluverkunum að því er varðar aðildarríkið sem gagnaferðin hefur upprunalegt, einkum þegar gagna- innflytjendurinn fær gagna frá annarra stöðvum skýrimþáttanna, sem skýrsluþéttur evrópska aðilinn er sendur úr, og ætti þá að beita lagi tilnefnda aðilsins.
**Candidate 6:** Til þess að auðvelda gagnagjöf frá Evrópusambandinu er hægt að heimila vinnu- stofum, sem veita gagna- reikningssér, einstaka gagnaarkar til vísindaábyrgja í Evrópusambandinu, að beita sama tæknilega og stjórnsýslufyrirbyggjandi ráðstöfunum óháð því hvaða aðildarríki gagnaflutningin hefur upphaf, einkum þegar gagna- innflytjandi fær gagna til fyrirframreikninga frá annarri stofa útflutningsdómara í Evrópusambandinu, þá skal beita lögum tilnefnda aðildarríkisins.
**Candidate 7:** Til þess að auðvelda flutninga gögn frá Evrópusambandinu, er þá þarf að leyfa gjafara, sem veita gagnavinnuþjónustu fyrir nokkrum gagnavinnu- tilhöndlumannir í Evrópusambandininu, að beita sömu tæknilegum og stjórnunarlögum um öryggi án tillits til hvaða aðildarríkis flutningin komur frá, einkum þegar gagnasjóandi fær gagna frá öðrum stöðum gagnasjóandi í Evrópusambandininu við að slík gagna verði fara út til frekari gagnavinnu, þá skal beita lögum þeirra aðildarríkis sem verið er í því skyni.

</details>

<details><summary>after · greedy · p13official21:test:eso:278 · P</summary>

**Source:** Centaurus A has therefore been observed with many different telescopes.
**Semantic decision:** P — CentaurusA observed/measured with many different telescopes retained; duplicated preposition only.
**Candidate 0:** Því hefur Centaurus A verið mælt með með margum mismunandi sjónaukum.

</details>

<details><summary>after · G8 · p13official21:test:ema:1918 · P</summary>

**Source:** The presented safety information is derived principally from paediatric patients.
**Semantic decision:** P — Candidate4 retains that safety information derives principally from child-age patients, despite nonstandard inflections.
**Candidate 0:** Sannaðar öryggisupplýsingar eru samanstöddar aðallega af upplýsingum um sjúklinga þunglara.
**Candidate 1:** Sjaldnara er útgun öryggiskennið búin til frá sjúklingum sem fá meðferð við sjúkdómi í sjóða.
**Candidate 2:** Tilkynntu upplýsingar varðandi öryggi eru í meira um rúm úr sjúklingum þar sem verið er að rannsaka.
**Candidate 3:** Ráðlagt vísindaupplýsingar um öryggi færa verða frá yngri sjúklingum.
**Candidate 4:** Umskýrslur um öryggi eru aðallega frá upplýsingum varðandi sjúklinga á börnald.
**Candidate 5:** Sjálfraðlega er öryggiupplýsingarinnar höfðu byggð á sjúklingum hjá börnum.
**Candidate 6:** Tilgreindar öryggishagana byggja aðallega á umönnunum hjá börnum.
**Candidate 7:** Frá því sem skýrt er fyrir um varðandi öryggi er upprunalega sem flóð af upplýsingum um sjúklinga á aldrinum.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:2721 · F</summary>

**Source:** No, but one day, I'll take that cane away...
**Semantic decision:** F — Taking away a cane is not preserved.
**Candidate 0:** Nei, en eitt dagur, færi ég þessu stóðinn...

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:1601 · P</summary>

**Source:** I don"t plan on wearing it that long.
**Semantic decision:** P — Preserves not intending to wear it for that long, with redundant wording.
**Candidate 0:** Ég ætla ekki að vera í því lengi í því.

</details>

<details><summary>before · G8 · p13official21:test:eea:1059 · F</summary>

**Source:** The domestic output price index for an economic activity measures the average price development of all goods and related services resulting from that activity and sold on the domestic market.
**Semantic decision:** F — No intelligible domestic output-price index measuring average price development; multiple scope/quantity relations corrupted.
**Candidate 0:** Innri verðsinsleifur fyrir efnahagsaðstöðu mæla með sér miðgildi verðsverkis allra vörum og tengda þjónustu sem kemur fram af ákvörðun sjálfri þess og seljast á innlanum markaði.
**Candidate 1:** Í innlendri veruverðskrá fyrir efnahagsaðgerð er mælt fyrir um miðgildi verufram- vikranna allra vörva og tilheyrandi þjónustu sem komist er fram af þessari starfsemi og er selgt á innlands- markaðinum.
**Candidate 2:** Staðbundinn merkmið um útgjöld fyrir efnahagsaðgerð mælið verði arsmerki á vísitölu hinra vörus og tengda þjónustu sem er afkvæmat fyrir það aðgerð og selis á innlöginu.
**Candidate 3:** Þjóðlega verðþýðisstykkin fyrir vinnu- hag, að því er varðar kostnaðarbúning, miðar tíðni á meðaltali verðs fyrir öll vörur og tilheyrandi búningi, sem leiðir af þessari hag og seldur á innlandsmarkaðinu.
**Candidate 4:** Haglegur vísitilraun um útbreiðslu verð við efnahagsaðgerð metir með hlutföllu ástaþroska af öllu efninu og tengdum þjónustum sem það fer fram og selstu á innlendu markaðinum.
**Candidate 5:** Innri verðaðiðaþáttur fyrir efnahagsaðstoður miðir það þá verðbreytingu samkvæmt þeirri aðstæðum sem hafa í sér eða tengjast þeirri sjálfri aðstöðu og selskoðaðir á innri markaðinum.
**Candidate 6:** Ættarverðleið seði fyrir innri verð (domestic output price index) fyrir rekstrarhóf tilkynnt er með því að meta meðalverðaráhrif gögnum og þeirra þjónustu sem þeir eru fyrir framleiðslu og seljast á innlandsmarkaðinu af komið út úr þeirri rekstrarhófi.
**Candidate 7:** Hagverðin fyrir innri útgjöf efnahagsaðstæðu eru miðað um meðal verðskipti allra vörna og tengda þjónustu úr sér sér í þessari aðstæði og seljandi á innri markaðinum.

</details>

<details><summary>before · greedy · p13official21:test:eea:879 · F</summary>

**Source:** If more than one water source is utilised for fish production, fish representing all water sources must be included for sampling.
**Semantic decision:** F — Fish representing all water sources becomes fish being all water sources; source term also malformed.
**Candidate 0:** Ef fleiri en einn vatnsorð er notað til fiskaræktar verður að taka til sýnatöku fisk sem eru allir vatnsorðin.

</details>

<details><summary>before · greedy · p13official21:test:eea:136 · F</summary>

**Source:** Member State shall recognize the documents of compliance and safety management certificates issued by, or on behalf of, the administrations of third countries if it is satisfied that they demonstrate compliance with the provisions of this Regulation.
**Semantic decision:** F — Certificates and issuance/on-behalf-of relationship not preserved; directives substituted.
**Candidate 0:** Aðildarríki skal viðurkenna skjöl um samræmi við og öryggisstýringu sem tilskipanir eru af stjórnunum þriðju landa eða fyrir henni ef það er fullgengi að þeir sýni fram á samræmi við ákvæði þessarar reglugerðar.

</details>

<details><summary>after · G8 · p13official21:test:eso:504 · F</summary>

**Source:** The precise extent of the habitable zone depends on many factors.
**Semantic decision:** F — All eight corrupt the habitable-zone/extent terms; dependence on many factors alone is insufficient.
**Candidate 0:** Mikilvægur smásvæði heimskara svæðisinni tengist mörgum þætti.
**Candidate 1:** Nákvæmri útreikning húsverkefnisþyrpingarinnar byggist á mörgum þættum.
**Candidate 2:** Nákvæmur útsetingardýrareikinn er háð margra þátta.
**Candidate 3:** Nákvæmlega umhverfisrauður svæðið sér hátt við mörgum þáttum.
**Candidate 4:** Vissulegur staðauslag sætisvæðisins verður háð mörgum þáttum.
**Candidate 5:** Nákvæm merki um að hverjum stigi bordræktarvægans er fyrir hendi við margar þættir.
**Candidate 6:** Nákvæm fjarlægð sætisvægurs er háð mörgum þáttum.
**Candidate 7:** Mikilvægur rými sjálftímanalegrar svæðis viðhafðrar, sem stendur til mörgum þætti.

</details>

<details><summary>before · G8 · p13official21:test:ema:635 · P</summary>

**Source:** Table 4 provides dose modification guidance for dinutuximab, GM-CSF and IL-2.
**Semantic decision:** P — Candidates4/7 preserve Table4 providing dose-modification guidance for all three named treatments.
**Candidate 0:** Tafla 4 fylgir fyrirmælum um skammtaaðlögun fyrir dinútúximab, GM-CSF og IL-2.
**Candidate 1:** Í töflu 4 fyrirfylgja eru leiðbeiningar um skammtaaðlögun fyrir dinútúxímab, GM-CSF og IL-2.
**Candidate 2:** Í töflu 4 fyrirboði breytilegum skömmtum af dinutuximabi, GM-CSF og IL-2.
**Candidate 3:** Í töflu 4 er kveðið á um leiðbeiningar um skammtahönnun af dinutuximabi, GM-CSF og IL-2.
**Candidate 4:** Tafla 4 gefur leiðbeiningar um skammtaaðlögun fyrir dinutuximab, GM-CSF og IL-2.
**Candidate 5:** Í töflu 4 er gerð leiðbeiningar um skammtahöfnun fyrir dinutuxímab, GM-CSF og IL-2.
**Candidate 7:** Í töflu 4 er gefin leiðbeiningar um aðlögun skammta af dinutuximabi, GM-CSF og IL-2.

</details>

<details><summary>before · G8 · p13official21:test:eea:386 · U</summary>

**Source:** Purpose: to inform the management and staff of the facility of the reason for the test facility inspection or study audit that is about to take place, and to identify the facility areas, study(ies) selected for audit, documents and personnel likely to be involved.
**Semantic decision:** U — Candidate2 retains many inspection-purpose elements but forthcoming audit/inspection syntax is unclear; cannot confirm complete procedural meaning.
**Candidate 0:** Tilgangur: til að bæta með fyrirhugaðri fyrirumsar eða verkefni fyrir rannsóknir á sviði afurðasviðs, sem er aðstoðar- eða í náum til rannsóknar, og til að tilgreina svið afurðasviðs, sem verkefnið er afveldi fyrir rannsóknarna, skjálftir og starfsfólki sem líklegt er að taka þátt í rannsóknum.
**Candidate 1:** Markmið: til að tilkynna stjórnun og starfsfólki stöðvarinnar um ástæðu til að framkvæma eftirlit með notkun eftirlitsstöðvarar eða rannsóknar eftirlits og til að koma á áhrif stöðvarins, rannsóknar(annað) sem valnumurinn var settur, skjala og starfsfólki sem líklega verður að taka þátt í.
**Candidate 2:** Tilgangur: til að upplýsa stjórnun og starfsfólki viðkomandi stofunnar um ástæður prófunar á eða rannsókn á eða í nálsið aðgerð þar sem prófunarstofanum er skoðuð eða rannsakað, og til að greina svið stofunnar, rannsóknirnar sem valin eru til skoðunar, skjöl og starfsmenn sem líklegt er að sé í tali við sem stofuð er.
**Candidate 3:** Tilgangur: til að tilkynna framkvæmdarstjóra og starfsfólki viðkomandi stofnunar um ástæðan af eftirliti með prófunarstofu eða rannsóknarupptaka sem tekst er til, og til að sýna fram á svæði stofnunar, rannsóknir sem jafnað er á fyrir upptaka, skjöl og starfsmenn sem líklegt er að taka þátt í.
**Candidate 4:** Tilgangur: til að koma fram árað fyrir stjórnun og starfsfólki stofnunarinnar um ástæður til að framkvæma eftirlit með stofnunni eða rannsókn eftirlit með rannsóknum (rannsóknir) sem verða að koma fram og til að greina sér stofnisvettindir, útgáfu rannsókna (rannsókna) sem verða að valað, skjaldir og starfsfólki sem líklega verða að taka þátt í rannsókninni.
**Candidate 5:** Tilgangur: til að upplýsa stjórn- og starfsfólki í stofunni ástæðan fyrir athuganir á rannsóknarstaðnum eða rannsóknar í samhæfi sem er að komast fyrir og til að þýða svið í staðnum, rannsóknirnar sem valin eru fyrir athuganir, skjöl og starfsfólk sem gæti komið fyrir í athuganir.
**Candidate 6:** Tilgangur: til að upplýsa stjórnun og starfsmenn stöðvarinnar um sönnun í eftirlit með aðstæðum á prófunarstöðunum, stöðu eða rannsóknum, sem er að fara fram, til að tilgreina svæði stöðvarinnar, rannsókn eða rannsóknir sem verða til að vera í eftirlitinu, upplýsinga og starfsfólks sem líklega gerir mismunur í meðan á eftirlitið stendur.
**Candidate 7:** Tilgangur: til að upplýsa stjórnun og starfsfólk stöðuins um ástæðu eftirlits á rannsóknastöðnum eða rannsóknir á fyrirhugaði sem verður til að taka sér til, og til að kanna um sjálfkrafa stöðunnar, rannsóknir (raunir) sem velkomið eru til eftirlits, skjöl og starfsmenn sem líklega munu taka þátt í.

</details>

<details><summary>after · G8 · p13official21:test:eea:679 · F</summary>

**Source:** This relates to the gross earnings paid during the reference year.
**Semantic decision:** F — All eight corrupt gross earnings and/or the reference year; cleaned wages and basic payments do not preserve gross earnings.
**Candidate 0:** Þetta varðar hreinsujuðgjöf sem greidd er á viðmiðunaryrki.
**Candidate 1:** Þetta varðar hreinsaðar laun sem greidd er á viðmiðunarári.
**Candidate 2:** Þetta varðar fyrirbæri sem er gefin upp á tilvísunarári.
**Candidate 3:** Þetta varðar frábrotnaðarávinnt sem greidd er á viðmiðunargáttinn.
**Candidate 4:** Þetta varðar grunngreiðslur sem greiðst í viðmiðunareldi.
**Candidate 5:** Þetta varðar heildarfræði, sem er greiðin á viðmiðunaryrki.
**Candidate 6:** Þetta varðar hryggjarningabreytingar sem greiðast í viðmiðunar árið.
**Candidate 7:** Þetta varðar fjárhægastarfsemi sem er greitt á viðmiðunarríkinu.

</details>

<details><summary>before · G8 · p13official21:test:eea:1509 · P</summary>

**Source:** Therefore, in the interest of clarity of legislation, it is appropriate to merge those provisions in one single legislative act.
**Semantic decision:** P — Candidate0 combines provisions in one legislative act for clarity of legislation; minor spelling/grammar.
**Candidate 0:** Því er rétt að samfleyta þessar ákvæði í einni laggjöf til að gera skýrleika á löggjöfina.
**Candidate 1:** Því er rétt að flagna þessi ákvæði í einn skipuð löggjaf.
**Candidate 2:** Því er rétt að samþykkja þá ákvæði í eina einsti löggjaf.
**Candidate 3:** Þar af leiðandi er rétt að gera saman þessar ákvæði í einni lag-gerð.
**Candidate 4:** Því er rétt að samfleytu þessum ákvæðum í einni sameiginlegu löggjöf.
**Candidate 5:** Því er rétt að samgöf þessara ákvæða í einni lagagjaldeyti til að býða til skýramiklunar.
**Candidate 6:** Því er rétt að eftirbyggja það í þeim ástandi sem gerir skýrleika löggjafar á eitt slegið löggjaf.
**Candidate 7:** Því eru rétt að samruna þessum ákvæðum í einni mengandi laggjöf til að gera lögunina auðveldara.

</details>

<details><summary>before · greedy · p13official21:test:eso:20 · F</summary>

**Source:** These galaxies span a vast range of distances from us.
**Semantic decision:** F — Vast range of distances becomes much farther boundaries; diversity of distances not retained.
**Candidate 0:** Þessi vetrarbraut eru í miklu fjarlægri mörkum frá okkur.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:1596 · F</summary>

**Source:** I stuffed it in my pocket.
**Semantic decision:** F — Stuffing into a pocket becomes screwing into a watch/shift.
**Candidate 0:** Ég skrúfaði það í vaktina.

</details>

<details><summary>before · greedy · p13official21:test:eea:1144 · F</summary>

**Source:** Successful participation in interlaboratory studies that assess laboratory proficiency is the best way to prove the competence in specific analyses.
**Semantic decision:** F — Successful interlaboratory participation becomes experience; laboratory-proficiency relation corrupted.
**Candidate 0:** Reynsla í samstarfsrannsóknum á rannsóknarþjálfun sem meta þjálfa rannsóknarstofa er besta leiðin til að sýna fram á færni í sérstökum greiningum.

</details>

<details><summary>before · G8 · p13official21:test:eso:908 · F</summary>

**Source:** This bridge, which has not been seen before (and is too faint to show up in this picture), is somewhat bluer than either galaxy, indicating that it consists of stars created in gas that was drawn away from NGC 1387 by the gravitational pull of NGC 1399.
**Semantic decision:** F — All corrupt bridge faintness/colour or gravitational-pull origin, despite copied NGC numbers.
**Candidate 0:** Þessi brú, sem hefur ekki séðð áður (og er of seyðið til að vera sem séður á myndinni), er blár en oss annan vetrarbraut, sem benda til að henni fái upp stjörnur sem eru myndar úr gasi sem lítið var drag teir úr NGC 1387 af völdum gærhlaustur á NGC 1399.
**Candidate 1:** Þessi brú, sem hefur ekki séð áður (og sést ekki vel í myndinni) er merkurblár en annar galni, sem bendir til að það er stjörnur sem eru búin úr gasið sem var tekin úr NGC 1387 vegna þá þrálags sem NGC 1399 hefur á höndinni.
**Candidate 2:** Þetta brú, sem hefur ekki séðð áður (og er of þungur til að sýna í myndinni), er örlítið fjarlægari en annar útflugan og bendir til þess að hann séu stjörnur sem eru myndaðar úr gasi sem komið var mæði af NGC 1387 vegna gagnsemi NGC 1399.
**Candidate 3:** Þetta brú, sem hafa ekki séð þar fyrir (og er of lágt til að lítur upp í þessari mynd), er fargari en hvert stjarnafugli einu sér, sem gefur til kynna að það samanstendur af stjörnum sem byggðuðu út úr gassins sem tókst úr NGC 1387 vegna áhættuhvítanums NGC 1399.
**Candidate 4:** Þetta brú, sem hefur ekki séð áður (og er yfirveldur til að sýna í myndinni) er mikið grátt en annar galdrirnar, til að gefa til áherslu á að það er stjörnur sem eru unnið úr gasi sem leidstyrkir NGC 1399 gleypt úr NGC 1387.
**Candidate 5:** Þessi brú, sem hefur ekki séð áður (og er of dýr hvolið til að koma fram í myndinni), er hvolfri en öllum vetrarbrautum, sem benda til þess að hann séu þyrpingar sem eru created í gasi sem gefinn verið frá NGC 1387 af gegnum sjón á NGC 1399.
**Candidate 6:** Þessari brú, sem hefur aldrei komið fram (og er of svart til að koma fram í þessari mynd), er bær seinni en annar galnur og gefur til kynna að hann sést af stjörnum sem birtust úr gasi sem var kallað úr NGC 1387 af því að það leggast við áhrif þráðs NGC 1399.
**Candidate 7:** Þessi brú, sem hefur ekki séð áður og er ekki til stæðara til að sjá upp í myndinni, er aðeins viðbriggrein en annarra vetrarbrauta, sem bendir til þess að það séu stjörnur sem eru framleiddar úr gasi sem var dragið út frá NGC 1387 af gegnþrýstingi NGC 1399.

</details>

<details><summary>after · greedy · p13official21:test:eea:1144 · F</summary>

**Source:** Successful participation in interlaboratory studies that assess laboratory proficiency is the best way to prove the competence in specific analyses.
**Semantic decision:** F — Successful participation is weakened to experience/cooperation; the success qualification needed to demonstrate competence is lost.
**Candidate 0:** Reynsla í samstarf við rannsóknir á milli rannsóknarstofa sem meta færni rannsóknarstofa er besta leiðin til að sýna fram á færni í sérstökum greiningum.

</details>

<details><summary>before · greedy · p13official21:test:eso:760 · F</summary>

**Source:** Extreme stars like the two components of VFTS 352, play a key role in the evolution of galaxies and are thought to be the main producers of elements such as oxygen.
**Semantic decision:** F — Oxygen element production becomes an unrelated vehicle-type expression.
**Candidate 0:** Hámarkssjár eins og tvö hlutir VFTS 352 spila mikilvægar hlutverki í þróun vetrarbrauta og eru talin vera aðalmyndandi efni sem eigið er ökutípu.

</details>

<details><summary>before · G8 · p13official21:test:eea:679 · F</summary>

**Source:** This relates to the gross earnings paid during the reference year.
**Semantic decision:** F — No candidate preserves gross earnings paid in reference year; gross earnings becomes base payments/tax/unrelated invented terms.
**Candidate 0:** Þetta varðar hryggjaríkur sem gefinn eru á í viðmiðunarefni.
**Candidate 1:** Þetta varðar hagskattin á því sem greidd er á viðmiðunarári.
**Candidate 2:** Þetta varðar fyrirbærin laun, sem er greitt meðan á viðmiðunarliðinu stendur.
**Candidate 3:** Það varðar heildarnafnaráðgengi sem er gefin í viðmiðunar árinu.
**Candidate 4:** Þetta varðar grunngreiðslurnar í samkvæmta ári.
**Candidate 5:** Þetta varðar heildarnafn fyrir áletra á viðmiðunaröldinni.
**Candidate 6:** Þetta varðar grunngreiðslur sem teknum eru út ásamt ákvörðunarsjóði.
**Candidate 7:** Það tengist fjárhæðum sem stöðvar eru fram á viðmiðunar árinu.

</details>

<details><summary>before · greedy · p13official21:test:eea:1831 · F</summary>

**Source:** However fibreboards classified as class A will be accepted if they do not represent more than 50 % of the total wood and wood-based materials used in the product.
**Semantic decision:** F — Wood/materials become galaxies; fibreboards omitted.
**Candidate 0:** Hins vegar munu þeir sem eru flokkaðir sem A flokkur vera viðkomandi ef þeir eru ekki meira en 50% af heildarstærði vetrarbrauta og vetrarbrautafundna í vörunni.

</details>

<details><summary>before · greedy · p13official21:test:eea:850 · F</summary>

**Source:** When implementing this strand the Commission will in particular ensure consistency and complementarity with the activities conducted by other Commission services or by European agencies; in particular, the European Foundation for the Improvement of Living and Working Conditions and the Community RTD Framework programme and the European Centre for the Development of Vocational Training (Cedefop).
**Semantic decision:** F — Complementarity and the named institutions/programmes are materially corrupted.
**Candidate 0:** Þegar framkvæmd þessarar hóps er gerð mun framkvæmdastjórnin sérstaklega tryggja samræmi og aukabill við starfsemi annarra þjónustu framkvæmdastjórnarinnar eða evrópskra stofnana; sérstaklega Evrópuð stofnun fyrir bætur á aðgerðum til að bæta lífsgjafar- og vinnuþáttum og rannsóknaráætlun evrópska samanburðarríkisins um rannsóknir á tæknilegri og tæknilega sviði og Evrópuskrána fyrir þjálfun í sviði starfsþjálfunar (Cedefop).

</details>

<details><summary>before · greedy · p13official21:test:eea:615 · F</summary>

**Source:** Annual days of sick leave not paid by the employer (optional).
**Semantic decision:** F — Sick leave and unpaid-by-employer relation corrupted.
**Candidate 0:** Árslegar dagir fyrir sjúkdómsframsölu sem vinnuveitandi gefur ekki til (valfræðileg).

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:1878 · P</summary>

**Source:** That's not what Optimus would want.
**Semantic decision:** P — Faithfully states this is not what Optimus would want.
**Candidate 0:** Það er ekki það sem Optimus myndi vilja.

</details>

<details><summary>before · greedy · p13official21:test:eea:568 · F</summary>

**Source:** This device shall reverse the window/roof panel/partition before it exerts a pinch force of more than 100 N within the opening of 200 mm to 4 mm above the top edge of a power-operated window/partition or in front of the leading edge of a sliding roof panel and at the trailing edge of a tilting roof panel.
**Semantic decision:** F — Vehicle controls become anatomical/unrelated terms and geometry is corrupted.
**Candidate 0:** Þetta tæki skal snúa glugga/þörmu/teppi fyrir fram á þann tíma sem það skuli stunda meira en 100 N á 200 mm til 4 mm yfir háttar brún í glugga/þörmu/teppi eða fyrir framan háttar brún í slímhlaupi þörmunnar eða yfir háttar brún í hlaupi þörmunnar.

</details>

<details><summary>after · greedy · p13official21:test:eso:329 · F</summary>

**Source:** The experiment marks the first time that APEX has taken part in VLBI observations, and is the culmination of three years hard work at APEXs high altitude site on the 5000-metre plateau of Chajnantor in the Chilean Andes, where the atmospheric pressure is only about half that at sea level.
**Semantic decision:** F — The Chajnantor/Andes location is lost or corrupted and atmospheric pressure is not faithfully named.
**Candidate 0:** Sjálfur er það fyrsta sinn sem APEX hefur tekið þátt í VLBI mælingum og er endapunkti þriggja ára vinnu á hægri stöð við APEX á 5000 metrar hæðarstöðinu í Chileands Endabergum þar sem lofthvarf er aðeins um hálft því sem á sjóhæði.

</details>

<details><summary>before · G8 · p13official21:test:ema:970 · P</summary>

**Source:** In patients with mild hepatic impairment (Child-Pugh A), there was no significant changes in pharmacokinetics compared with normal healthy volunteers.
**Semantic decision:** P — Candidates0/1/2/3/6 retain mild impairment, no significant PK change, Child-PughA and healthy volunteers.
**Candidate 0:** Hjá sjúklingum með vægt skerta lifrarstarfsemi (Child-Pugh A) voru engin marktæk breytingar á lyfjahvörfum borið saman við eðlilega heilbrigða sjálfboðaliða.
**Candidate 1:** Hjá sjúklingum með vægt skerðingu á lifrarstarfsemi (Child-Pugh A) komu engin marktæk breytingar fram á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.
**Candidate 2:** Hjá sjúklingum með væga skerðingu á lifrarstarfsemi (Child-Pugh A) varð ekki marktæk breytingar á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.
**Candidate 3:** Hjá sjúklingum með vægt skerta lifrarstarfsemi (Child-Pugh A) var engin marktæk breytingar í lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.
**Candidate 4:** Hjá sjúklingum með vægari lifrarstarfsemi (Child-Pugh A) voru ekki marktæk breytingar á lyfjahvörfum samanborið við eðlilega, heilbrigða sjálfboðaliða.
**Candidate 5:** Hjá sjúklingum með vægan lifrarbilun (Child-Pugh A) varð ekki marktækt breytingar á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.
**Candidate 6:** Hjá sjúklingum með vægt skerta lifrarstarfsemi (Child-Pugh A) var enginn marktæk breytingar á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.
**Candidate 7:** Hjá sjúklingum með vægt skerðingu á lifrarstarfsemi (Child-Pugh A) var ekki marktækt breytingar á lyfjahvörfum samanborið við heilbrigðan heilbrigði hjá sjálfboðaliðum.

</details>

<details><summary>before · greedy · p13official21:test:eea:1323 · F</summary>

**Source:** If refills are not provided, the weight of the total primary packaging shall not exceed 3,7 g per wash for tablets and 1,7 g per wash for all other products.
**Semantic decision:** F — Refills, primary packaging and per-wash units corrupted.
**Candidate 0:** Ef ekki er veitt endurtekningar skal þyngd heildarfráseldsins ekki vera meira en 3,7 g fyrir hverja þvag fyrir töflur og 1,7 g fyrir hverja þvag fyrir öll önnur vörur.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:2209 · P</summary>

**Source:** Much has been made of the hostility between our countries.
**Semantic decision:** P — Much being made of discord/hostility between our countries retained despite rough grammar.
**Candidate 0:** Miklum hefur verið gerð af ósáttinu milli landa okkar.

</details>

<details><summary>before · G8 · p13official21:test:ema:1385 · F</summary>

**Source:** Lynparza is indicated as monotherapy for the maintenance treatment of adult patients with platinum-sensitive relapsed BRCA-mutated (germline and/or somatic) high grade serous epithelial ovarian, fallopian tube, or primary peritoneal cancer who are in response (complete response or partial response) to platinum-based chemotherapy.
**Semantic decision:** F — All corrupt clinical cancer subtype, mutation/platinum-sensitivity/relapse conditions or response qualifications.
**Candidate 0:** Lynparza er ætlað til einlyfjameðferðar til viðhaldsmeðferðar hjá fullorðnum sjúklingum með hægtengd endurheimt af völdum BRCA-þroska (germlingsþroska og/eða líffærasþroska) sem eru í hæstu líffærasýkingu í eggjastokki, hárgangabreiddan eggjastokk, fæðubrunni eða frumhöfn og berinni svörun (heildarfullan svörun eða hlutfallslegan svörun) við krabbameinslyfjameðferð með platínum.
**Candidate 1:** Lynparza er ætlað til einlyfjameðferðar við hvarfefnum aðgerðir hjá fullorðnum sjúklingum með BRCA-skurðsmit sem eru með hægri gráðu gráðuöðraudalaugakrabbamein í eitrunarvegum, fallopianvegi eða fyrirbyggðum krabbameini í kæli og svara meðferð með járnplatinum (platinum-based chemotherapy) í öðru lagi (fullanleg meðferð eða aðlagað meðferð).
**Candidate 2:** Lynparza er ætlað til einlyfjameðferðar til viðhaldsmeðferðar hjá fullorðnum sjúklingum með BRCA-affnslag sem stuttir er fyrir platín og með hæga sérþekkingu í kyrningafjölli, kyrklaga eða frumskýja (serous epithelial ovarian, fallopian tube, or primary peritoneal cancer), sem fá svörun (heildarsvörun eða hlutaþéttnisvörun) af lyfjameðferð með platín (platinum-based chemotherapy).
**Candidate 3:** Lynparza er ætlað til einlyfjameðferðar til viðhaldsmeðferðar hjá fullorðnum sjúklingum með BRCA-stökkbreyt sem verður aldrei sjúkur af nýgengi (germlíngefni eða líffæri) á hægri skali serusföng í eggjastokki, getnaflabúð eða frumuð eggjastokka (ovík, kílirháttar og eða víðmál) sem eru í svörun (fullan svörun eða hlutlaus svörun) af gegnum lyfjafræðilegan platinum meðferð.
**Candidate 4:** Lynparza er ætlað til einlyfja meðferðar við viðhaldslifur hjá fullorðnum sjúklingum með BRCA-skiltið (germlin- og/eða líffæra) hæga gráðu serusæju eggjastokk, fallopian-tunga eða grunnkjaftari- krabbamein sem tilvikið er við lyfjameðferð með platíníu en sjúklingurinn sýnir svörun (fullanleg svörun eða hlutfallsleg svörun).
**Candidate 5:** Lynparza er ætlað til einlyfja meðferðar til viðhaldsmeðferðar hjá fullorðnum sjúklingum með Brca-háþrýstingsertæka (germline and/or somatic) hægðaháttar, sérþekkingar (serous epithelial) eggjastokka, fallopian-tappa (fallopian-tapastokka) eða hægðaháttar sjálfkrafa frumuhúð (primary peritoneal cancer) sem svara (heildar- eða hluta- svar) á meðferð með platínum í bakgrunni.
**Candidate 6:** Lynparza er ætlað til einlyfjameðferðar við viðhaldsmeðferð hjá fullorðnum sjúklingum með BRCA-germlínnum, krabbamein í seröuml;uphafa eggjastokku, fallopian- túpu eða gríneftir í rúmmælum sem eru hækkar af völdum platinum og tengist platinumbundinni krabbameinslyfjum (platinum-based chemotherapy) við óvikaðar (fullkominni svörun eða hluta af svörun) eða óvikaðar svörun.
**Candidate 7:** Lynparza er ætlað til einlyfjameðferðar við viðhaldsmeðferð hjá fullorðnum sjúklingum með brísna BRCA, (germlin- eða eða líffæra) segnaþéttnis ægileg eitilkrabbamein í eggjastokki, háheilablöðru eða grunnbrjóst, með svörun (heiluhliði eða hlutverk heiluhliðar) við eitlaferlifæra meðferð með platinum.

</details>

<details><summary>after · greedy · p13official21:test:eso:554 · P</summary>

**Source:** In the lower part of the image a big chunk of the molecular cloud that gave birth to these stellar youngsters still can be seen.
**Semantic decision:** P — Retains a large remaining part of the molecular cloud in the lower image and its origin of the young stars.
**Candidate 0:** Í lágari hluta myndarinnar er enn að sjá stór hlut af sameindaskýinu sem fæddi þessi ungbura stjörnur.

</details>

<details><summary>after · greedy · p13official21:test:eso:710 · F</summary>

**Source:** The VST KiDS survey will allow astronomers to make precise measurements of dark matter, the structure of galaxy halos, and the evolution of galaxies and clusters.
**Semantic decision:** F — Structure of galactic halos becomes formation of galactic rings; the specified measured structure changes.
**Candidate 0:** VST KiDS rannsóknin mun gera stjörnufræðingum kleift að gera nákvæmar mælingar á dökkum efni, myndun hringa vetrarbrauta og þróun vetrarbrauta og þyrpinga.

</details>

<details><summary>before · G8 · p13official21:test:eso:136 · U</summary>

**Source:** ALMA is radically different from visible-light and infrared telescopes.
**Semantic decision:** U — Candidate6 approximates visible/infrared light but phrase says telescopes coming into light; exact spectral comparison uncertain. Others omit visible-light restriction.
**Candidate 0:** ALMA er skömmu ólík af skyni geymslu og infrarámetru sjónauka.
**Candidate 1:** ALMA er til mikilvægu mismunandi frá sjónauki og innrauðu sjónauki.
**Candidate 2:** ALMA er umfangsmikil mismunandi en sjónauka og innrauða sjónauka.
**Candidate 3:** ALMA er svo alvarlega mismunandi á móti sjónauða og infráleifiskortferli.
**Candidate 4:** ALMA er aðallega skipt úr sjónauki og in-fræðilegu sjónauki.
**Candidate 5:** ALMA er hátt mismunur burt af sjónaukum og innrauða sjónaukum.
**Candidate 6:** ALMA er framangreint mismunandi frá sjónaukum sem koma í ljósi og innrauða ljósi.
**Candidate 7:** ALMA er umfangsmikill mismunandi frá sjónaukum og innrauðu sjónaukum.

</details>

<details><summary>before · G8 · p13official21:test:eea:852 · F</summary>

**Source:** These actions may include comparison of the effectiveness of processes, methods and tools related to the chosen themes, mutual transfer and application of good practice, exchanges of personnel, joint development of products, processes, strategy and methodology, adaptation to different contexts of methods, tools and processes identified as good practice, and/or dissemination of results, profile-raising materials and events.
**Semantic decision:** F — All omit/corrupt several process-comparison, good-practice, personnel, adaptation or dissemination list elements.
**Candidate 0:** Þessir aðgerðir geta samanstendur samanburði á verkun, aðferðum og verkefnum sem tengjast úrskurðum, meðskipti á starfsmenn, samstarfi í vörum, ferli og aðferðum, samstarfi í þátttöku, aðferðir og ferli sem er til þess að verða góðar starfsvenjur, aðferðir og ferli sem tengjast uppruna, aðgerðir og hæfisreglur, aðferðir, verkefni og ferli sem eru til þess að verða góðar starfsvenjur, aðgerðir um aðupun á aðgerðir og vörum, vörum og tilvikum, aðgerðir um hægðatrifari, vörum og tilvikum, og aðgreining á niðurstöðum, aðgerðum um aðupun á vörum og tilvikum og sýningu á hæfisreglum, verkefnum og tilvikum.
**Candidate 1:** Síðan má taka til greina þess að þessi aðgerðir hvað varðar samanburð yfir skilvirkni ferlanna, getnaðarferla og vörn sem tengist ákveðnu kerfinu, viðbótarhreyfingum og notkun góðra færni, skilbreytingu umsjóna, sameiginlegri vörnumyndun, sameiginlegri vinnslu ferla, áætlunar og aðferða-, vörnarmeðferðar og aðrar aðferða inntöku sem greind eru hvaða fyrirbæris, og/eða að auka, að því er varðar, niðurstaður, úrræði og tilfinningar.
**Candidate 2:** Þessi aðgerð geta felldir í samanburð á verkun, aðferðir og búnaður sem tengjast valinu þóknunum, aðskilinn skipti um manna, samstarfsverkun á vörum, ferli og aðferðum, hefðbundin þróun varanir, ferla og aðferða, aðlögun á samhengi við mismunandi kringumastilslu, búnað og ferli, sem auðveldar er kallað slík, og/eða dreifingu á niðurstöðum, af völdum hentugleika og tilvikum.
**Candidate 3:** Í þessum aðgerðum geta komið fyrir samanburður á virkni vinnu- aðferða, aðferða og búnaðar, sem tengist ákveðnum umbreykjunum, hvort samanburður á heimildum, samþætun eftir dagskilyrðum, skipti þeirra í hand, starfsgreiðslu aðferða, vinnu og áætlana, aðgerðir og aðferðir á tengslum við mismunandi skilyrði og skipti skiptir í hand, eða framlaggingu niðurstöðva, þungaði- og aðskiljandi hlutum og tilvikum.
**Candidate 4:** Þessi aðgerðir geta náð meðferð, aðferðir og tækni, sem tengjast tilgreindu þrengslum, samanburði um virkni á þeim, einangra flutningu og beitingu góðra aðgerða, millifyrirbréfum um starfsmenn, sameiginlegri þróun afurða, aðferða og aðferðar, stjórnun á vegum til að ná að mismunandi þætti aðferða, tækja og aðferða sem gefnu til góða aðgerða og/eða blettur niðurstöður, aðgreiningar og tilfinningar.
**Candidate 5:** Þessi aðgerðir geta tengst samanburð á verkun, aðferðum og hlutum sem tengjast tilvistið þema, mismunandi dreifingu og beitingu góðrar aðferða, skipti í aðila, sameiginlega þróun vöru, aðferða og áætlana, aðlögun á aðferðum, hlutum og aðferðum sem tengjast góðar aðferðir, og/eða raunabreyting á niðurstöðum, meðalhæðarvinnslu og tilvikum.
**Candidate 6:** Þessar aðgerðir geta verið í samanburði á virkjunum, aðferðum og tækjum sem tengjast valinum þóknunum, bæði sjálfsmæli og notkun góðra starfsmála, skipti í hlutum, sameiginlega þátttöku, samstarfs á vörum, aðgerðum, stefnumála og aðferðum, samræmingar á mismunandi tæknilegum ráðstöfunum, tækjum og aðferðum sem gefin eru upp sem góða starfsmálaráðstöfun, og/eða framlags útlits, trefu- og tæknivísi og tilfella.
**Candidate 7:** Þessi aðgerðir geta innihaldið samanburð á verkun skiptislegra kerfanna, þjóðaferða og tækja sem tengjast vökvunni, aðstoð og beiting á góðum starfsmönnum, skipti í einstöku í móti um leiðbeiningar, samvirkan tækning eftir vöru, kerfum, áætlun og aðferða-, samhliða þróun vörum, kerfanna, áætlunar eða aðferða og aðferða sem ólíkun sjálfkvæmum aðstæðum er greind að vera góðum starfsemi, tækjum og kerfum, og/eða miðlun á niðurstöðum, vísitækum efninum og tilheyri fyrirkomulagum.

</details>

<details><summary>after · G8 · p13official21:test:eso:825 · F</summary>

**Source:** The process of dust trapping is explained in an earlier release (eso1325).
**Semantic decision:** F — No inspected candidate retains both the dust-trapping process and its explanation in an earlier release. Generic procedure or powder-holding alone is incomplete.
**Candidate 0:** Undirstuðuð er það mátt að trapa dufti í meðferð (eso1325).
**Candidate 1:** Í forföldunni er lýst hvernig þýskja er lagt upp (eso1325).
**Candidate 2:** Efnið við útingu ryks er skýrt fram á forfæru skilningi (eso1325).
**Candidate 3:** Neytisfer glökkstíðni er útskýrt í fyrra útgáfu (eso1325).
**Candidate 4:** Verklagurinn um sköpumafnun er skýrt út í fyrri útgáfu (eso1325).
**Candidate 5:** Úrbókin er skýrt upp í fyrri útgáfu (eso1325).
**Candidate 6:** Framkvæmd þeirrar aðgerða er skýrpuð í fyrri útgefningu (eso1325).
**Candidate 7:** Afurðin að tryggja að dufti haldið á sér stað er lögð fram í skráðri losunarupplýsingum (eso1325).

</details>

<details><summary>before · greedy · p13official21:test:ema:2722 · F</summary>

**Source:** See also ‘Bleeding or bruising after you stop treatment in section 4.
**Semantic decision:** F — Bruising not preserved.
**Candidate 0:** Sjá einnig „Blæðingar eða sláður eftir að meðferð er hætt í kafla 4.

</details>

<details><summary>before · greedy · p13official21:test:eso:710 · F</summary>

**Source:** The VST KiDS survey will allow astronomers to make precise measurements of dark matter, the structure of galaxy halos, and the evolution of galaxies and clusters.
**Semantic decision:** F — Structure of galactic halos becomes formation of rings in galaxies.
**Candidate 0:** VST KiDS rannsóknin mun gera stjörnufræðingum kleift að gera nákvæmar mælingar á dökku efninu, myndun hringjar í vetrarbrautum og þróun vetrarbrauta og vetrarbrautahópa.

</details>

<details><summary>before · greedy · p13official21:test:ema:772 · P</summary>

**Source:** These effects are called interactions, and can lead to serious side effects, or prevent proper control of other conditions you may have.
**Semantic decision:** P — Interactions, serious adverse effects and interference with control of other conditions retained.
**Candidate 0:** Þessar áhrif eru nefndar milliverkanir og geta leitt til alvarlegra aukaverkana eða hindraði viðeigandi eftirliti með öðrum sjúkdómsstöðum sem þú getur haft.

</details>

<details><summary>before · G8 · p13official21:test:eso:881 · F</summary>

**Source:** Using standard candles - such as the variable stars within IC 1613 and the less-common Type Ia supernova explosions, which can seen across far greater cosmic distances - astronomers have pieced together a cosmic distance ladder, reaching deeper and deeper into space.
**Semantic decision:** F — No correct standard-candle/variable-star/TypeIa/cosmic-distance-ladder explanation.
**Candidate 0:** Með stöðugum bannlar - svo sem breytilegir stjörnur innan IC 1613 og lítilegir af tegund Ia ræktarstyrkur, sem sjá má yfir miklu stjörnuferil - hafa stjörnufræðingar samið raflínu sem náir skýrri stjörnuferill- með það að koma öðru og öðru að misna í geimnum.
**Candidate 1:** Nauðsynlegir býli - sem eru ávísu sjónbúnaður, eins og breytilegir stjörnur í IC 1613 og lítill en vanfreyi af tegund Ia eftirlitsbrotum - hefur stjörnufræðingar samið sternur til sér og hentar lengri og lengri í geimnum.
**Candidate 2:** Stjörnufræðingar hafa laust saman stjörnumælanæri skipti sem reynir öðrum styrkurstjörnuríkum í IC 1613 og fleira sárstjörnur af tegund Ia sem er um leiðir í smástirri stjörnustig í geiminn.
**Candidate 3:** Með stöðugum myndunni - svo sem þessu umlægðu stjörnu fyrir alíkunum í IC 1613 og umlægðu stjörnuflæði af tegund Ia, sem má sjá í hári langri geimfræðilegri sjálfbrundi -, hafa stjörnufræðingar gengið saman sjálfbrundi frá sjálfbrundi í geimnum og náði sjálfbrundi sem náði djúpu og djúpu til geimsins.
**Candidate 4:** Með hjálp staðla kérna, svo sem breyttra stjörnurnar í IC 1613 og lágsvægar breyttra stjörnuþjónusturar af tegund Ia, sem sjáist á mjög langa fjarlægð, hafa stjörnufræðingar reynst saman stjörnuþjálfan sem nánast í djúpu og djúpu í geimnum.
**Candidate 5:** Hjá stjörnufræðingum hefur verið haft þróun á litunum - eins og breytandi stjörnur í IC 1613 og minnkunar fyrir gerð Ia af æxlun í himnu, sem sjár er um örlítið lengri rúm - og hefur þeir lagt saman lítilt stjarnrúmmál í far seinnum inni í geiminn.
**Candidate 6:** Með staðallum baka- og burtkirkja - svo sem breytilegir stjörnur í IC 1613 og minnkunar Ia geislaskipti, sem sjáðar á lengra himnir - hefur stjörnufræðingar komið saman stjarnvagnsvallann, sem nærster og síðar til umfangsgerðar.
**Candidate 7:** Með viðbúnum ljósinum, eins og breytilegir stjörnur í IC 1613 og minnkri úrferri af tegund Ia sem sjást í langa stjörnumál, hafa stjörnufræðingar reiknað út svörunarladd á geimnum, sem lægri og lægri kemur í geiminn.

</details>

<details><summary>before · G8 · p13official21:test:eea:1524 · F</summary>

**Source:** In the case of bulk liquid products the lot or sublot shall be thoroughly mixed in so far as possible and in so far it does not affect the quality of the product, by either manual or mechanical means immediately prior to sampling.
**Semantic decision:** F — No candidate preserves bulk-liquid/manual-or-mechanical/thorough mixing and immediate-before-sampling constraint together.
**Candidate 0:** Ef um er að ræða vökvafræðilega vörur skal lotinu eða undirlotinu að blanda þau vel og eftir það sem er mögulegt, að því tilskildu sem það hefur ekki áhrif á gæði vörunnar með beinum eða tæknilegum aðferðum áður en sýnatöku er gerð.
**Candidate 1:** Ef um er að ræða magnafæð blender hóðinu eða undirhóðunni í allt að fyrir hendi, þar sem það hefur ekki áhrif á gæði lyfsins, með beintilvirkjum eða með virkju, innan þeirra sér sem er, fyrir að sýna eðlilegt.
**Candidate 2:** Ef um er að ræða vatnsþætti skal lotur eða undirlotur mergið vel eftir því sem unnt er og það skalt ekki hafa áhrif á gæði vörunnar, með annaðhvort tæknilegri eða tæknilegri aðferð í tafarlaust fyrir vali sýnu.
**Candidate 3:** Fyrir vökvi öryggismerkjum fyrir vökva í umfjöllum skal lauseða blanda lot eða undirlot í hvorki dæmigerðum máli né með séslæknum taka til að það hafi ekki áhrif á gæðisvörv vörunnar, fyrir það sem getur að verja.
**Candidate 4:** Í örsýnum vökva tilgreiningar skal hitti í eðlilega fullkomlega hætti, að liðnum eða undirliðum, svo fremst sem unnt er og eftir það ekki skipti á gæði vörunnar, með annaðhvort manna eða tæknilegum hætti áður en sýnatæking er gerð.
**Candidate 5:** Ef um er að ræða ígrunalegar vörur skal blanda loti eða undirlotu í sérhverju hæfileikum sem unnt er og í sérhverju hæfileikum sem hún hefur málefni við gæði vörunnar, með beina eða tæknilegum aðstæðum, innan við sýnatök.
**Candidate 6:** Ef um er að ræða vökva í þynnu skal lotið eða undirlotið tekið fullt blandað með öllum fyrir sitt hæfilegum leyti sem einnig má er við og það gerir ekki nein áhrif á gæði lyfsins, með annaðhvort tæknilegum eða mannaþætti að lokum á forstöðu ísambendingar.
**Candidate 7:** Hjá þeim vörum sem eru lífverudreifingar skal lotur eða undirlotur lagað til að blanda vel upp, að því marki sem unnt er og á kosti fyrir gæðavinningu, með annaðhvort fyrirhæfilegum eða tæknilegum hátt, áður en sýna er gerð.

</details>

<details><summary>after · G8 · p13official21:test:eso:1198 · P</summary>

**Source:** The new observations are thus the first direct confirmation of such models.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Candidate 0:** Þessar nýjar mælingar eru þannig fyrstu beinu stafræna sannprófun á slíkum líkani.
**Candidate 1:** Nýjar mælingarnar eru þess vegna fyrstu beina staðfestin fyrir slíkar líkani.
**Candidate 2:** Nýjar upptöku eru þess Vilur fyrstu beinu staðfestingu fyrir slíkum líkani.
**Candidate 3:** Útgáttur niðurfellingin er þess vegna fyrsta beinu staðfestingu fyrir slíkum líkani.
**Candidate 4:** Nýjar mælingarnar eru því fyrsta beinu staðfestingu þessara líkönanna.
**Candidate 5:** Nýir mælingar eru þess vegna fyrstu beina staðfestingar á slíkum skipulagum.
**Candidate 6:** Nýjar mælingarnar eru þess vegna fyrstu beina staðfestingu fyrir slíkar líkenni.
**Candidate 7:** Nú skulu nýjar mælingarnar vera fyrstu beinu staðfestingu fyrir slíkar líkani.

</details>

<details><summary>before · greedy · p13official21:test:eso:705 · F</summary>

**Source:** Normal long-duration GRBs last between 2 and 2000 seconds.
**Semantic decision:** F — GRB is replaced by a corrupted red-radiation/cancer term; numbers alone do not preserve the claim.
**Candidate 0:** Lengd eðlilegra rauðum geislameinsbrotna er á bilinu 2 til 2000 sekúndur.

</details>

<details><summary>before · G8 · p13official21:test:eso:502 · F</summary>

**Source:** The first five signals are very confident, while the sixth is tentative, and seventh more tentative still.
**Semantic decision:** F — All corrupt signals and ordered sixth/seventh increasing uncertainty.
**Candidate 0:** Fyrstu fimm öryggisöryggisverk eru mjög tunglavíkar en sjötthundraði er tilbún þess og sjötthundrunum er tilbún enn enn.
**Candidate 1:** Fyrstu fimm hættarinnar eru mjög áreiðanir, en sexútt er í betru tilviki og sjötútt enn fremur.
**Candidate 2:** Fyrstu fimm merkingarnir eru mjög þekkju, þar sem sjöttháttinu er fyrstu enda, síðsta ein hagalega enn.
**Candidate 3:** Fyrstu fimm yfirburðarnar eru mjög vissar en sexu yfirburðurinn er tækur og sjönu yfirburðurinn er enn tækrari.
**Candidate 4:** Fyrstu fimm mörk eru mjög róleg, en síðustu er í fjögurri sinn vottinn, og sjönum liggur sinn í fyrirsvörun.
**Candidate 5:** Fyrstu fimm útgefinu eru mjög tunglæga, en sjötthunni er næmið, en sjötthunni sína er engin næmið.
**Candidate 6:** Eftirfarandi fimm merkimiði eru mjög vissar en sjötthundurför varðandi sjötthundurför.
**Candidate 7:** Fyrstu fimm verkaðar eru til birta, en síðasti er þannig tilbúin.

</details>

<details><summary>before · greedy · p13official21:test:eso:278 · P</summary>

**Source:** Centaurus A has therefore been observed with many different telescopes.
**Semantic decision:** P — CentaurusA observed/measured with many different telescopes retained; duplicated preposition only.
**Candidate 0:** Því hefur Centaurus A verið mælt með með margum mismunandi sjónaukum.

</details>

<details><summary>before · G8 · p13official21:test:eea:2125 · F</summary>

**Source:** In addition, the sub-processing should only consist of the operations agreed in the contract between the data exporter and the data importer incorporating the standard contractual clauses provided for in this Decision and should not refer to different processing operations or purposes so that the purpose limitation principle set out by Directive 95/46/EC is respected.
**Semantic decision:** F — Every candidate corrupts sub-processing/data-agent/contract or purpose-limitation relationships; correct directive number alone insufficient.
**Candidate 0:** Auk þess skal undirfjölfunina einungis gilda rekstri sem samkvæmt samningnum milli gagnaflutnings- og gagnainnflutningsins þar sem undirfylltar samningargreinar eru gert samkvæmt þessari ákvörðun og hún skal ekki vísa til mismikla rekstri eða tilskusviða til þess að meginreglunni um takmarkaða markmiði sem sett er fram í tilskipun 95/46/EB sé fylgt.
**Candidate 1:** Að auki skulu undirrekandi forritinu einungis innihalda það sama aðgerðir sem samningin um dreifingu gögnum inni og út gerðir innihalda staðla samningsaðgerðirnar sem kveðið er á um í þessari ákvörðun og skulu ekki beita aðrar rekstrarafurðir eða tilgangi svo að þetta reglur um takmarkaða meginmarkmiði, sem kveðið er á um í tilskipun 95/46/EB, sé uppfyllt.
**Candidate 2:** Að auki ætti að undirprentunin sé eingöngu skipulaginn sem samið er í samninginu um gagnamögnunaraðlun og -skráningu, þar sem uppáhaldar samningarlögum er fylgjað sem kveðið er á um í þessari ákvörðun og ekki má vísa til annars aðrar starfseininga eða til að skilgreina mismunandi upplýsingaverndar, svo að meginreglur sem kveðið er á um um að ræða með tilskipun 95/46/EB séu uppfylltar.
**Candidate 3:** Auk þess skulu niðri verkefnið aðeins vera aðgerðir sem samþykkt var um í samninginum um gagnamögnunaraðskriftar í niðurverkefni, sem samhliða staðla samningsaðgerðirnar sem kveðið er á um í þessari ákvörðun, og það skal ekki vísa til annarra verkefna eða aðskildra þeirra markaðsins fyrir að viðeigandi meginreglun fyrir markaðssetningu, sem kveðið er á um í tilskipun 95/46/EB, sé nýtt.
**Candidate 4:** Í aukinni skipti skal undirkerfið aðeins vera upptöku sem samkvæmt samningi hansinni milli gögnumfæra og gögnuminnna, þar sem fylgjast er með staðla samningsmála sem kveðið er á um í þessari ákvörðun, og upptöku skal ekki vísa við mismunandi rekstrarferli eða aðstæður svo að meginreglunin um takmörkuð viðmiðanir, sem til komið er í tilskipun 95/46/EB, sé uppfyllt.
**Candidate 5:** Að auki skal undirprentunin einungis vera í samræmnum rekstri sem samþykkt er milli gagnaútgefanda og gagnainnöfnunar eftir fyrirbyggjandi samningslögum sem kveðið er á um í þessari ákvörðun og leið og ekki verða um annað fyrirkomulag eða tilgangar til að fylgja því að bólguskeiðisreglunni sem kveðið er á um í tilskipun 95/46/EB sé fylgt eftir.
**Candidate 6:** Auk þess skulu undirbúningarnar aðeins vera réttar þeir starfsemi, sem samningin um geymslu gögnum innleiðir, sem samþykktar eru samkvæmt þessum ákvörðun og geta ekki tekist til annarra starfsemi eða hagsmuna svo að meginreglurnar um takmarkaðina aðferð, sem kveðið er á um í tilskipun 95/46/EB, sé uppfylltar.
**Candidate 7:** Að auki skal undirbreiði það líka aðeins vera aðgerðir sem samið eru samkvæmt samningi um gagnaútgjöf og gagnainnflytjendustarfsemi, þar sem eftirfarandi kostir til skipulags er kveðið á um, og skal ekki vísa til annarra aðgerða eða ástæða sem birta þann reglunni um takmarkaða markmið í tilskipun 95/46/EB.

</details>

<details><summary>after · G8 · p13official21:test:ema:2323 · U</summary>

**Source:** It is important to drink plenty of water to avoid dehydration.
**Semantic decision:** U — Water/fluid intake is retained in several candidates, but the dehydration term in0/6 cannot be certified; others use clearly unrelated conditions.
**Candidate 0:** Mikilvægt er að drekka miklu vökva til að forðast útþurrkun.
**Candidate 1:** Mikilvægt er að drekka marga vatn til að koma í veg fyrir úðaútdrep.
**Candidate 2:** Mikilvægt er að drukkja mikið af vatni til að forðast útsæði.
**Candidate 3:** Mikilvægt er að drekka munur af vatni til að forðast útfjarlægingu.
**Candidate 4:** Mikillvægt er að drekka munanlega vatn til að koma í veg fyrir þvagsýringu.
**Candidate 5:** Það er mikilvægt að drekka víkkum í vatn til að koma í veg fyrir þvagræsingu.
**Candidate 6:** Það er mikilvægt að drekka mikið vatn til að forðast útþurrð.
**Candidate 7:** Mikilvægt er að drekka mikið af vatni til að forðast þrátingu.

</details>

<details><summary>before · G8 · p13official21:test:eea:850 · F</summary>

**Source:** When implementing this strand the Commission will in particular ensure consistency and complementarity with the activities conducted by other Commission services or by European agencies; in particular, the European Foundation for the Improvement of Living and Working Conditions and the Community RTD Framework programme and the European Centre for the Development of Vocational Training (Cedefop).
**Semantic decision:** F — All corrupt named institutions/programme and complementarity; living conditions often becomes liver conditions.
**Candidate 0:** Þegar framkvæmdastjórnin beitt þessum flokknum mun hún sérstaklega tryggja samræmi og aukabils við starfsemi annarra stofnana framkvæmdastjórnarinnar eða evrópsku stofnana; sérstaklega evrópska stofnuninni fyrir bætur á aðstoðar- og vinnuskilyrði og evrópsku stofnuninni fyrir inntöku og svæði um rannsóknir og þjálfun í sviði starfsfæranotkunar (Cedefop).
**Candidate 1:** Þegar framkvæmd þessa ísla kemur til stunda skal framkvæmdastjórnin sérstaklega tryggja samræmi og aðstoð sem notið er af starfsemi annarra þjónustu framkvæmdastjórnarinnar eða Evrópuþjónustuverkefna; sérstaklega Evrópuþjónustuáðeigandi stofnuninni vegna aðlögunar á viðskiptum á lifrar- og verkunarskilyrði, evrópskra rannsóknar- og þjálfnauðlögum (R&T-D) og evrópsku stofnun vegna þjálfunar á sviði rekjafræðilegrar hæfis (Cedefop).
**Candidate 2:** Þegar framkvæmdað er þetta slegið mun framkvæmdastjórnin sérstaklega tryggja samræmi og aðstoð með starfsemi annarra þjónustu framkvæmdastjórnarinnar eða Evrópuðra stofnana; sérstaklega evrópskeru stofnuninni til bæjar ástæðna um að uppruna og vinna á aðstæðum fyrir lifun og vinnu og Evrópukerfiðum um vöktun og uppbyggingu á tækifærslu og starfsmen (RTD) að því er varðar evrópska stofnuninni til framhalds að þjálfa (Cedefop).
**Candidate 3:** Þegar framkvæmdað er þetta markvegi mun framkvæmdastjórnin, einkum, tryggja samvirkni og auðmat með starfsemi annarra framkvæmda aðila framkvæmdastjórnarinnar eða evrópubóta; einkum með hjálp Evrópubandalsins fyrir aukningu á aðstæðum í atvikum og launirmiða ESB og Evrópulánastofnunarinnar fyrir þjálfun í starfsemi (Cedefop).
**Candidate 4:** Þegar framkvæmd þess fyrirhvarfs er gerð gerir framkvæmdastjórnin sérstaklega með íhaldanleið og aðstoðanleið við starfsemi annarra búðanna framkvæmdastjórnarinnar eða Evrópuþjónustufundanna; sérstaklega, Evrópu stofnuninni fyrir aukningu á lifun og vinnumiðlun og Evrópu rannsóknasviðið á rannsóknir á tæknifestum hætti (fyrir schnell herferð (Rafend) og Evrópu stofnuninni fyrir þjálfun og þjálfun hugbúnaðar (Cedefop)).
**Candidate 5:** Við framkvæmd þessara þærms skal framkvæmdastjórnin sérstaklega tryggja samræmi og aukin starfsemi yfirleitt í þeim stofnunum sem framkvæma starfsemi áframhaldandi framkvæmda- stjórnarinnar eða áframhaldandi ESB-stofnunum, einkum Evrópuríkimannastofnuninni fyrir aðlögun lífsmálayfirvalda og atvinnu- og skuldbindingabundinni rannsóknar- og fjármála- áætlun Sambandsins og Evrópasviðið fyrir þjálfun í hæfis (Cedefop).
**Candidate 6:** Þegar framkvæmd þessarar skipar gerist mun framkvæmdastjórnin sérstaklega tryggja sam síni og til æxlis með starfsemi annarra þjónustuveitana fram völdum framkvæmdastjórnarinnar eða Evrópuþjónustudeyminu; sérstaklega evrópska stofnuninni fyrir hæfi og sviði við að auka sjóði og vinnu ástand og aðila EES yfirráðasamfelti um rannsóknir á tækninum og vinnuskyldur (RTD) og evrópsku stofnuninni fyrir þjálfun í sviði vinnsluaðstæðna (Cedefop).
**Candidate 7:** Þegar framkvæmdastjórnin fari fram í þessum marki skal hún, sérstaklega, tryggja samræmi og viðbótarmeðferð við starfsemi annarra þjónustu framkvæmdastjórnarinnar eða Evrópubótagernjana; sérstaklega með evrópsku stofnuninni fyrir aðgerðir við bælingu á lifrar- og vinnumörkuðum skilyrðum og með evrópsku tveggja stofnun fyrir tækifæringar í sviði starfsemi (RTD) og evrópsku stofnun fyrir hæfni á launamarkaði (Cedefop).

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:1803 · P</summary>

**Source:** What are you planning on telling her?
**Semantic decision:** P — Exact source/hypothesis semantic reuse from card85: Question about what to tell her preserved.
**Candidate 0:** Hvað ætlarðu að segja henni?

</details>

<details><summary>before · greedy · p13official21:test:eso:1168 · F</summary>

**Source:** R Coronae Australis itself is not visible to the unaided eye, but the tiny, tiara-shaped constellation in which it lies is easily spotted from dark sites due to its proximity on the sky to the larger constellation of Sagittarius and the rich star clouds towards the centre of our own galaxy, the Milky Way.
**Semantic decision:** F — Constellation shape/Sagittarius/rich star clouds corrupted; rich clouds becomes calm star formation.
**Candidate 0:** R Coronae Australis sjálfur er ekki sýnt með óhjálpar augu en stuttur, tiara- skipti stjörnumerkin sem það er í er greint frá fyrir svartum staðsetningum vegna nálægri fjarlægðs á himninum við stærri stjörnumerkin Sígítrarinn og rólega stjörnumyndunum í miðju okkar vetrarbrauta, Vetrarbrautarinnar.

</details>

<details><summary>before · greedy · p13official21:test:eea:2090 · F</summary>

**Source:** Member States shall require the competent authorities to monitor compliance with this Regulation effectively and take all necessary measures to ensure such compliance.
**Semantic decision:** F — Member-State requirement for competent authorities to monitor compliance becomes participants following regulation; monitoring relation missing.
**Candidate 0:** Aðildarríkin skulu kveða á um það í þátttakendur lögbæra yfirvalda til að fylgja með skilvirkum hætti reglugerðinni og gera allar nauðsynlegar ráðstafanir til að tryggja það.

</details>

<details><summary>after · G8 · p13official21:test:eea:850 · F</summary>

**Source:** When implementing this strand the Commission will in particular ensure consistency and complementarity with the activities conducted by other Commission services or by European agencies; in particular, the European Foundation for the Improvement of Living and Working Conditions and the Community RTD Framework programme and the European Centre for the Development of Vocational Training (Cedefop).
**Semantic decision:** F — All eight corrupt named agency/programme functions or the consistency/complementarity relation; institutional references are not faithfully preserved.
**Candidate 0:** Þegar framkvæmdastjórnin beitir þessi aðalað mun hann einkum sjá til þess að hefja samræmi og einnig samhengi við starfsemi annarra þjónustuveitenda fram- samtaka eða Evrópuðum stofnunum; einkum Evrópuða stofnuninni fyrir aðlögu aðgerðaáætlunina um að bæta aðstæður á starfsemi og vinnu, aðlaga og evrópsku ramma um rannsóknarfarið og tækniskipta (Community RTD Framework programme) og Evrópuskiptasviði fyrir þjálfun í sviði starfsemi (Cedefop).
**Candidate 1:** Þegar framkvæmd þessa þáttar verður framkvæmdastjórnin sérstaklega til að tryggja samrýmanleika og viðbótarmot ertingu sem annarra þjónustu framkvæmdastjórnarinnar eða Evrópuþjónustuverkefna þáttars og einkum í þáttum Evrópusamannamálsstofnunarinnar við fram- búnun við- og atvinnulífs- og vinnumiðlun og áætluninni um rannsóknarsviðin sem bandalagið fer að framkvæma og Evrópuskrána fyrir fræðslu og atvinnugreiðslu (Cedefop).
**Candidate 2:** Þegar framkvæmd þessa umferðarferlsar er gerð verður skipulegur framkvæmdastjórninni einkum að tryggja samræmi og aukunnar aðgerðir við starfsemi annarra þjónustuveitana sem framkvæmdastjórnin féðir eða Evrópuþjónustufenganna; einkum Evrópulánðsamtök Stofnunarinnar fyrir bætt við aðstoð að lifun og atvinnuumstöðu og rannsóknarefninu Evrópusambandsins um viðtak í aðstoðar- og rannsóknaráætlunum á geðhæfingu (RTD) og Evrópuskrána fyrir þjálfun í sviði starfsemi (Cedefop).
**Candidate 3:** Þegar framkvæmdaferðingin er framkvæmd á þessari stöðu verður framkvæmdastjórnin sérstaklega að tryggja samræmi og aðstoðandi þátttaka við starfsemi annarra þjónustuveitenda fram- krafsnefnda eða evrópskra stofnana; sérstaklega evrópsks stofnunar fyrir að þróun á aðstæðum fyrir aðstoð í lifun og vinnslu og evrópsks rannsóknaráætlunarinnar um efnahagsmísun umfram- lagt og evrópsks stofnunar fyrir þróun hæfis- og hæfismótunar (Cedefop).
**Candidate 4:** Þegar framkvæmd þess fyrirferðarferðar er hægt verður framkvæmdastjórnin einkum að tryggja samræmi og að það skuli vera auðveldari við starfsemi annarra þjónustu framkvæmdastjórnarinnar eða evrópska stofnana; sérstaklega evrópska stofnunin fyrir stjórnun lífsgreina og atvinnulífsgreina og evrópska stofnunina fyrir umfangs- breytilegra rannsóknatengdedu (European Centre for the Development of Vocational Training (Cedefop)).
**Candidate 5:** Við framkvæmd þessara þærms verður framkvæmdastjórnin í beitingu þessarar áætlunar aðtils einkum að tryggja samkvæmni og tilbúnan samhæfni við starfsemi annarra þjónustuveitana framkvæmdastjórnarinnar eða evrópskra stofnana; einkum þar sem um er að ræða Evrópuð byggingarfyrirtækisstofnunina sem er skilvirk viðmæli til að bæta lífsmiðun og atvinnu- og starfsemi og áætlun Evrópusambandsins um stærðfræðilegum og tækniiðlum og áætlun Evrópuðs aðstæður fyrir efnainntöku (Cedefop).
**Candidate 6:** Þegar framkvæmd þessarar helar er farið fram verður framkvæmdastjórninni sérstaklega að tryggja meðferð og að þær starfsemi, sem annar afstarar stofnanir eða starfsstofnanir Evrópusambandsins fari fram, jafnframt takmarkanir á því að um leiðandi verði hafi verið að ræða utanvaranir á viðskiptum í Tænu aðila Evrópusambandsins. Einnig varðar Evrópusamansæði Evrópusamansætana í aðgerðum um nýrra og framhaldandi rannsóknir á sviði starfsemi (Community RTD Framework programme) og Evrópuleg stofnun sem færir um þjálfun í efnisfræðilegu þjálfun (Cedefop).
**Candidate 7:** Þegar framkvæmd veitandi er með þessum strandi mun framkvæmdastjórnin einnig sjá til þess að samræmi og fylling við starfsemi annarra þjónustuaðildarréttar framkvæmdastjórnarinnar eða ríkisstofnana á Evrópu verði viðvart; einkum Evrópu stofnuninni til bækt gagnsæi á aðstoð á líf og vinnslu- ástandi og rannsóknaráætluninni að þróun tækniframfara í Bandalaginu og Evrópuskiptilbúnaðarstofnuninni Cedefop.

</details>

<details><summary>before · greedy · p13official21:test:eso:1181 · F</summary>

**Source:** By combining light from three of the VLTIs 1.8-metre Auxiliary Telescopes with the AMBER instrument, this facility allows astronomers to see details equivalent to those a telescope with a mirror of 85 metres in diameter would see.
**Semantic decision:** F — Mirror85metres in diameter becomes85metres in surface; auxiliary-telescope identity also drops.
**Candidate 0:** Með því að setja ljósi úr þremur VLT-1,8 m sjónaukum ásamt AMBER mælitækinu geta stjörnufræðingar sést nákvæmar upplýsingar eins og sjónauki með 85 metra í yfirborði myndi sjá.

</details>

<details><summary>before · G8 · p13official21:test:eea:2090 · U</summary>

**Source:** Member States shall require the competent authorities to monitor compliance with this Regulation effectively and take all necessary measures to ensure such compliance.
**Semantic decision:** U — Candidate2 has most required actions but makes monitored compliance explicitly their own; broad regulatory oversight relation uncertain. Others materially corrupted.
**Candidate 0:** Aðildarríki skulu krefjast lögbærra yfirvalda til að fylgjast með því að þessi reglugerð sé fullgilt og gera allar nauðsynlegar ráðstafanir til að tryggja það.
**Candidate 1:** Aðildarríkin skulu kveða á um það að lögbær yfirvöld eigi að fylgja til þess að þetta reglugerð sé fullgilt og geta allar nauðsynlegar ráðstafanir til að tryggja það.
**Candidate 2:** Aðildarríkin skulu krafast lögbærum yfirvöldum að fylgjast vel með því að þau uppfylli þessari reglugerð og gera allar nauðsynlegar ráðstafanir til að tryggja það.
**Candidate 3:** Aðildarríkin skulu kveða á reikfærni á það að lögbær yfirvöld eigi fylgjast með því að þau uppfylli þessa reglugerð eigi stuðullega og geri allar nauðsynlegar ráðstafanir til að tryggja það.
**Candidate 4:** Aðildarríkin skulu kveða á um það í skjal til lögbærra yfirvalda að þau fylgi áfram þessar reglugerðar með skilvirkan áhættueftirliti og gera allar nauðsynlegar ráðstafanir til að tryggja það.
**Candidate 5:** Aðildarríkin skulu kveða á um að lögbæra yfirvaldar hafi verið fylgt eftir skilvirku sannprófuninni að gera sinni til að fylgja skilyrðum þessarar reglugerðar og tekni allar nauðsynlegar ráðstafanir til að tryggja slíka sannprófun.
**Candidate 6:** Aðildarríkin skulu kveða á um það í þátttakendum, þar sem um er að ræða, að þau fylgi áfram þessari reglugerð með skilvirku hætti og aðeins þær aðgerðir sem nauðsynleg eru taka til að tryggja það.
**Candidate 7:** Aðildarríki skulu krefjast þess að lögbær yfirvöldi hafi skilvirkum eftirliti þannig að þau munu vera að fylgja reglugerðinni vel og gera allar nauðsynlegar ráðstafanir til að tryggja það.

</details>

<details><summary>after · greedy · p13official21:test:ema:607 · U</summary>

**Source:** Since the possibility of increased risk of cancer development in patients with newly diagnosed dysplasia treated with infliximab is not established, the risk and benefits to the individual patients must be carefully reviewed and consideration should be given to discontinuation of therapy.
**Semantic decision:** U — Risk/benefit review and possible discontinuation are retained, but cannot certify the dysplasia and cancer-development terminology.
**Candidate 0:** Þar sem ekki er sýnt fram á möguleika á aukinni hættu á krabbameinsuppbrot hjá sjúklingum með nýja greiningu á vefjaskipta sem fá meðferð með infliximabi, skal endurskoða áhættu og ávinning hjá einstaklingum varlega og íhuga að hætta meðferð.

</details>

<details><summary>before · greedy · p13official21:test:eea:1557 · F</summary>

**Source:** The Commission Communication ‘i2010 - A European Information Society for growth and employment (COM(), developing the Lisbon strategy, seeks to ensure coherence across the Commission's information society and media policies in order to reinforce the significant contribution of information and communication technologies to the performance of the economies of Member States.
**Semantic decision:** F — Invented COM identifier and corrupted Lisbon/policy/ICT-economic relations.
**Candidate 0:** Í orðsendingu framkvæmdastjórnarinnar „i2010 – Evrópska upplýsingahópi til vaxtar og launþátta (COM(2009) 478, þjálfun í lögum um stefnumarkmið í Lissabon, er aðstoða að tryggja samhliða meðferð í ramma- og fjarskiptalögunum framkvæmdastjórnarinnar til að veita verulega þátttöku upplýsingakerfa og fjarskipta- kerfa í hagstöðum aðildarríkjanna.

</details>

<details><summary>before · G8 · p13official21:test:eea:409 · F</summary>

**Source:** Purpose: to determine whether the test facility, if engaged in studies using animals or other biological test systems, has support facilities and conditions for their care, housing and containment, adequate to prevent stress and other problems which could affect the test system and hence the quality of data.
**Semantic decision:** F — No candidate preserves all support facilities for care/housing/containment and prevention of stress; repeated housing/monitoring substitutes lose concepts.
**Candidate 0:** Tilgangur: til að ákvarða hvort prófunarfyrirkomulag, ef það er í rannsóknáða með dýrum eða öðrum líffræðilegum prófunarkerfum, ábyrg í því að fá til að stuðla að því til þess að fá aðstoð, háfestur og sjálfsvæði, að fullnægjandi leyti, til að koma í veg fyrir þrýsting og aðra vandamál sem geta haft áhrif á prófunarfyrirkomulag og þannig á gæði gagna.
**Candidate 1:** Tilgangur: til að ákvarða hvort prófunarstöð varðandi dýraeiningu eða annað líffræðilegt prófunarkerfi, ef um rannsóknir er að ræða, ná til stofnana og skilyrða fyrir að hafa stöðu og stjórn fyrir þeim til að verja, ræða og felgi henni, að fullnægi og takmarka að því að það stóð á því að það hvaldi því að það komi í veg fyrir þol og aðrar vandamálur, sem geta haft áhrif á prófunarkerfið og þar af leið og gagnasamþykki.
**Candidate 2:** Tilgangur: til að ákvarða hvort prófunarstöð, ef tilheyrir rannsóknum á dýrum eða annarri líffræðilegri prófunarkerfi, ásamt tilhlýðilegu aðstoðann og skilyrðum til að sjást, veita og fylgja þeim, séu nægilegur til þess að koma í veg fyrir stress og aðra vandamál sem geta haft áhrif á prófunarkerfið og þannig á gæði gagnanna.
**Candidate 3:** Tilgangur: til að ákvarða hvort prófunaraðstöður, ef þar hafa verið gerðar prófanir á dýrum eða annarra líffræðilegra prófunarkerfum, hafa stuðningsaðstöðu til að fylgjast með þeim og handhafa þær og tekja til innrennslisvörn, nóg til að koma í veg fyrir þrýsting og önnur vandamál sem geta haft áhrif á prófunarkerfinu og þannig gætu ákvæði.
**Candidate 4:** Tilgangur: til að ákvarða hvort prófunarásetning, í sambandi við rannsóknir á dýrum eða öðrum líffræðilegum prófunarstöðum, hafi stuðningaraðstöðvar og skilyrði fyrir meðhöndlun, heimilis- og skilferlun, viðkvæmar til að koma í veg fyrir þunglyndi og aðra vandamál sem geta haft áhrif á prófunarstöðuna og þannig gagnkvæmni gagna.
**Candidate 5:** Markmiðið: að ákvarða hvort rannsóknarstofan, ef hún taki þátt í rannsóknum með dýrum eða öðrum líffræðilegum prófunarkerfum, fylgir staða og fyrirkomulag til að fylgjast með henni, fyrirhuga og inngjaf, nákvæmt til að koma í veg fyrir árás og aðrar vandamál sem geta haft áhrif á prófunarkerfinu og þannig á gæði gagna.
**Candidate 6:** Tilgangur: til að ákveða hvort prófunarfyrirtæki, ef það gengur í rannsóknir á dýrum eða annarra líffræðilegrar prófunarkerfum, ábyrgjast í sambandi með ábyrgjastarfsemi og skilyrðum fyrir meðhöndslu, húða og innrennslisreglur, sem nægir það að hafa áhrif á hóli prófunarkerfisins og þannig gætu á lagi gagnasammanstæðið.
**Candidate 7:** Tilgangur: að ákvarða hvort prófunarstöðvar, ef þar til rannsóknir eru gerðar með dýrum eða öðrum líffræðilegum prófunarkerfinni, hafa stuðningarstöðvar og skilyrði til að fylgjast með þær, hýsja þær og fylgjast með þær, að fullnægjandi leyti til að koma í veg fyrir þróun og aðra vandamál sem gætu haft áhrif á prófunarkerfinu og þar afleiðandi gæði gagna.

</details>

<details><summary>before · G8 · p13official21:test:ema:2652 · U</summary>

**Source:** Put the needle fully into the skin as shown by your nurse or doctor (see picture 6).
**Semantic decision:** U — Closest5 retains needle/nurse/doctor but fully becomes for all; full-insertion modifier/syntax uncertain. Other candidates change nurse or action.
**Candidate 0:** Settu nálina laus til í húðina eins og hjá svefnfóðurinn eða lækninum sýnist (sjá mynd 6).
**Candidate 1:** Setjið nálina fullt í húðina eins og náin eða læknirinn sýnir eftir (sjá mynd 6).
**Candidate 2:** Settu nálinni full komið í húðina eins og nálsa sjúklinga er sjá kjölfar hjá hjúkrunarfræðingi eða lækninum (sjá mynd 6).
**Candidate 3:** Settu nálinni á fullu í húðina eins og meðferðarlæknirinn eða meðferðaráeinandi sýnir (sjá mynd 6).
**Candidate 4:** Settu nálinni fullt inn í húðina eins og fræðandi eða hjúkrunarfræðingurinn sýnir (sjá mynd 6).
**Candidate 5:** Settu nálinni fyrir öll í húðina eins og sýnist fyrir hjá hjúkrunarfræðinginn eða lækninum (sjá mynd 6).
**Candidate 6:** Settu nálina allt inn í húðina eins og verið er sýnt frá hjá hjúkrunartækinni eða lækninum (sjá mynd 6).
**Candidate 7:** Settu nálinni í sækni í húðina eins og vefjakerdin eða læknirinn sýnir (sjá mynd 6).

</details>

<details><summary>after · G8 · p13official21:test:eea:1524 · F</summary>

**Source:** In the case of bulk liquid products the lot or sublot shall be thoroughly mixed in so far as possible and in so far it does not affect the quality of the product, by either manual or mechanical means immediately prior to sampling.
**Semantic decision:** F — All eight corrupt bulk-liquid form, manual/mechanical mixing or sampling timing. Candidate6 changes bulk liquid to liquid in a thin film and does not retain the immediate timing.
**Candidate 0:** Ef um er að ræða vökvafræðilega vörur skal lotur eða undirlotur dreifu að fullu þannig að sem unnt er og hvorki áhrifin á gæði vörunnar sem eðlilega þyngi eða annaðhvort er tekið á hjá í móti sýnatöku.
**Candidate 1:** Ef um er að ræða magnafull efnasamsettar vara skal lotið eða undirlotið leikað verulega eins og mögulegt er og þannig að hann skuli ekki hafa áhrif á gæði vörunnar, með annaðhvort virkju eða vélarefni, rétt áður en sýnatökur eru gerðar.
**Candidate 2:** Þegar um er að ræða vörublandt vöru skal lotin eða undirlotur vera tiltekinn skal fór hægt í fullu úr endurskoðun eftir því hversu kostur, og ef það hefur ekki áhrif á gæði vörunnar, skilvirk eða tæknileg, innan þeirra staðar þar sem sýnir er til að tekja eftir.
**Candidate 3:** Ef um er að ræða vökva í massagreiða vara skal lotur eða undirlotur blandað vel á þann leyti sem unnt er og nauðsynlegt og þannig að það hafi ekki áhrif á gæði vörunnar, með beina eða tæknilegum aðferðum, fyrir eftir sýnatöku.
**Candidate 4:** Í öllu tilviki sem varðar styrku vatnsbylgjuvarnir skulu lotur eða undirlotur nægilega blandaðir, að svo miklu leyti sem unnt er og mælt skal eftir að blöndun samanblandaðar varnir einkennum einkennum og ekki árangur varnarsins, með annaðhvort henda eða virka aðferðum, nánast fyrir því að taka eftirlitsprófun.
**Candidate 5:** Í þeim tilfellum þar sem um er að ræða blönduð vökva eru lotur eða undirlotur helst blönduð, eins og mögulegt er og svo langt að það hafi ekki áhrif á gæði vörunnar, með annaðhvort sjálfvirkum eða með tæknilegum aðferðum fyrir vöktun.
**Candidate 6:** Ef um er að ræða vökva í þynnu skal lotur eða undirlotur liggja öfluga blandað saman eins og hægt er og í því tilvikum að hann hafi ekki áhrif á gæði vörunnar, með annaðhvort með hendur eða tæknilegum hætti áður en sýnatöku er gerð.
**Candidate 7:** Hjá þeim vörum sem eru í magni, sem eru vökva, skulu loti eða undirlotið vera hreinsamt blönduð, að því marki sem unnt er, og að því marki að það hafi ekki áhrif á gæði vörunnar, með annaðhvort aðgerð sem stjórnaður stendur eða með tæknilegum aðgerðum fyrir skilruðun.

</details>

<details><summary>after · G8 · p13official21:test:ema:430 · U</summary>

**Source:** Keep the needle in your skin after the dose counter has returned to 0 and count slowly to 6.
**Semantic decision:** U — Candidate3 retains return to0 and slow counting to6, but on-skin wording and a nonstandard dose-counter term prevent certifying the full injection instruction; other variants add errors.
**Candidate 0:** Geymið nálina á húðinni eftir að skammtaríkið hefur náð 0 og tölulætið langt á milli 0 og 6.
**Candidate 1:** Haltu nálinni á húðinni eftir að skammtaríkið hefur náð 0 og tölutakaðst fljótlega til 6.
**Candidate 2:** Geymið nálina á húðinni eftir að gömlunarkílurinn hefur orðið 0 og tölulæsa því hægt um 6.
**Candidate 3:** Haldið nálinni á húðinni eftir að skammtaalitinn hafi endað sér aftur á 0 og talið rólega út í 6.
**Candidate 4:** Haltu nálina í húðinni á eftir að skammtaleyfið hefur náð 0 og töljaði þér svo langt að 6.
**Candidate 5:** Haltu nálina í húðinni í lok 0 og skiptið þér svolítið öll yfir til 6.
**Candidate 6:** Haltu nálina lengur í húðinni eftir að skammtalistið hafi náð 0 og rannast hægt í 6.
**Candidate 7:** Haldið nálina í húðinni þegar töflu upphaflega hefur orðið að 0 og tölutöluð saman allt milli 1 og 6.

</details>

<details><summary>after · greedy · p13official21:test:eso:1086 · F</summary>

**Source:** Media representatives and other outreach groups will also be attending the event.
**Semantic decision:** F — Media representatives and attendance at the event are corrupted into unrelated agency wording.
**Candidate 0:** Tilskipendum fjölmiðla og öðrum hópum sem hafa útöku verða einnig aðstoðarstofnunin.

</details>

<details><summary>before · G8 · p13official21:test:eso:825 · F</summary>

**Source:** The process of dust trapping is explained in an earlier release (eso1325).
**Semantic decision:** F — No candidate preserves dust trapping; closest2 says an unclear outing of dust.
**Candidate 0:** Undirstuðuð er ferlið um ávestingslag og það er lýst í fyrri losun (eso1325).
**Candidate 1:** Í forföllum losunarinni er leiðbeinin greint fyrir (eso1325).
**Candidate 2:** Efnið við útingu ryksins er útskráð í fyrri útgáfu (eso1325).
**Candidate 3:** Neytisfer glösumstíðni er útskýrt í fyrri útvegð (eso1325).
**Candidate 4:** Verklagskeðjunin er skýrt í fyrri losun (eso1325).
**Candidate 5:** Hreyfanefndur þess sem dorunnir eru er útskýrt í fyrri útgáfu (eso1325).
**Candidate 6:** Fyrirmyndin um aðskilnað dagssvæða er gefin upp í fyrri losunarmynd (eso1325).
**Candidate 7:** Afurðin um skrúfaskipti er lýst í fyrri rannsóknum (eso1325).

</details>

<details><summary>before · G8 · p13official21:test:eea:1144 · F</summary>

**Source:** Successful participation in interlaboratory studies that assess laboratory proficiency is the best way to prove the competence in specific analyses.
**Semantic decision:** F — No candidate retains successful interlaboratory proficiency participation; experience/precision/opportunity substitutes change the proposition.
**Candidate 0:** Reynsla í rannsóknir á milli stofna, sem meta færni rannsóknaraðstæðna, er besta leiðinni til að sannfæra færni í tilteknum greiningum.
**Candidate 1:** Viðrekta þátttöku í rannsóknum milli rannsóknarstofa sem mati á nákvæmni rannsóknarstofa er besta leiðin til að sannfæra nákvæmni í sérstökum greiningum.
**Candidate 2:** Reynsla í samstarfsrannsóknum á rannsóknarkerfi sem meta nákvæmni rannsóknarstofu er besta leiðin til að sýna fram á nákvæmni í sérstakri greiningum.
**Candidate 3:** Fullnægjandi tækifæri í samstarf um rannsóknir á rannsóknarstofum, þar sem mat er breyttri staðfestu, er besta leiðin til að sýna fram á tengd reynslu.
**Candidate 4:** Við fullnægjandi þátttöku á samstarfi írannstu stofnunar sem meta stærðfræðilegum hæfni er besta ways til að sýna fram á hæfni í sérstakri greiningu.
**Candidate 5:** Aðlögun í samstarf sem mæli er mat yfir nytjalegu fyrirskiptum í rannsóknir á nytjalegu fyrirhæfni er besta leiðin til að sýna fram á færni í tilteknum greiningum.
**Candidate 6:** Reynsla í yfirvöldum rannsóknir, sem meta kröfur fyrir rannsóknarstjórnar, er besta leiðin til að sýna fram á menntun- kunninu í sérstökum greiningum.
**Candidate 7:** Reynsla við þátttöku í samstarfsrannsóknum á verkefni, þar sem nákvæmni í rannsóknastofum er metin, er besta leiðin til að sýna fram á náið í sérstökum greiningum.

</details>

<details><summary>before · G8 · p13official21:test:eso:80 · F</summary>

**Source:** But the new study using the VLT has found that much of the stars energy is being absorbed and scattered by dust clouds before it gets to Earth - it is actually more luminous than previously thought and among the brightest stars known.
**Semantic decision:** F — All corrupt absorption/scattering by dust or stellar luminosity inference; some make the star itself reachEarth.
**Candidate 0:** En ný rannsóknin sem notuð var VLT hefur fundið að margi áburts er fenguð og slembið af rykiklónu fyrir geimnum en áður var tekið með - geðs er enn á eða bjánlegri en ætluð og er meðal bjóðsastjarna sem vitað er um.
**Candidate 1:** En nýr rannsóknin með VLT hefur leitt í ljós að mjög fyrirvirkni stjarnanna koma úr fyrirvirkni rykskæðlanna áður en stjarnan fæst til Ørðis - það er í raun sveigja stjörnurnar lengur en áður var talið og það er einn af björtustu stjörnunum sem vitað er um.
**Candidate 2:** En þessan nýja rannsókn með VLT hefur fundið að mikið af orku stjarnaðs er gefið til útsunnar og sprengtedins af rykskýum fyrir áður en það nær jörðinni - sem hefur í raun víst mikla ljós en virðist áður þegar það var talið og við um björtustu stjarna sem vitað er um.
**Candidate 3:** En í nýju rannsókninni með VLT hefurðið fundið að mikill orku stjörnurnar er samtans meðferðu og dreifður af rykskúum fyrir ásamt jörð, sem er í raun leysi magar en voru einungis hugtakandi og er meðal bjartasta stjörnunum sem vitað er um.
**Candidate 4:** En ný rannsóknin með VLT hefur fundið að fyrirrosturinn er að vera upp og út í stjörnumyndun, á móti eru stjörnurinn sýnilegri en áður taldist og innan þeirra er einnig ljóslegri.
**Candidate 5:** En nýtt rannsókn með VLT hefur fundið að tilfelli um það að mikið af orku stjarnaðs er seyptur og skilgreitt út af rykskyni áður en hann kemur til Jörðar - það er í raun mikil Útlitari en áður var talin og í samanburðarlistinni.
**Candidate 6:** En nýtt rannsókn með VLT hefur fundið að mikið af orku stjarna er borist og dreifist út af rykkykju áður en stjarnan ná yfir til Jörðar - hún er í raun fyrrandi ljósriðar en til þess var talið og von sérstaklega ljóslegasti stjarnan sem það er þekkt.
**Candidate 7:** Nýtt rannsókn á VLT talið það að mikið af orku stjarna sé tekið til holtar og dreifinn af duftamóta fyrir áður en það kemur til Jörðar, - orkuð er það hjá stjörnum nánari en gegn áður vart var að rasa og það er aðeins eins bjart og það er þess jákvætt.

</details>

<details><summary>after · G8 · p13official21:test:eea:852 · F</summary>

**Source:** These actions may include comparison of the effectiveness of processes, methods and tools related to the chosen themes, mutual transfer and application of good practice, exchanges of personnel, joint development of products, processes, strategy and methodology, adaptation to different contexts of methods, tools and processes identified as good practice, and/or dissemination of results, profile-raising materials and events.
**Semantic decision:** F — All eight lose parts of the action list, especially mutual transfer, adaptation across contexts, or profile-raising materials/events, and corrupt selected themes or tools.
**Candidate 0:** Þessir aðgerðir geta samanstendur af samanburði á verkun þeirra ferl- og aðferða sem tengjast tilbúinum greinum, mismunandi skipti og beitingu góðu aðferða, skiptum um starfsmenn, sameiginlegri þróun vöru, kerfanna og fyrirkomulags, aðlögun á erfiðum skilyrðum áferðanna og aðferða og kerfin sem auðkenndir eru sem góðar aðferðir, og/eða framlengingu á niðurstöðum, afmæli og tilvikum.
**Candidate 1:** Séu þessi aðgerðir eins og að bilun á virkni kerfa, aðferða og búnaðar sem tengjast tilvistum þóknunum, milliverður skipti og beiting á góðum starfsemi, skipti í tækjur, sameiginleg þróun vörum, kerfa, áætlunar- og aðferða- meðferð og aðlögun ágnarávísundar- kerfa, búnaðar og kerfa sem tilgreindar eru sem góðar starfsemi, og/eða útsendun niðurstaðna, fræðsluþætta- og upphafgerðum, aðgerða og upphafsgerðum.
**Candidate 2:** Þessi aðgerðir geta í sér samanburð á skilvirkni ferlinna, aðferða og vélva sem tengjast þeim þróttengslum sem velunin hefur verið valin fyrir, hins vegar tengd munta vinnslu og beitingu góðra starfsvenna, skipti inn- og út á starfsmenn, sameiginlegur þróun vörva, ferla, aðferða- og aðferðafræðilegra aðferða og aðferða, aðlögun á þeim aðferðum, vélvörunum og ferlum sem greindir eru góðri starfsvenja, og/eða dreifingu á niðurstöðum, upprunalegum fræðslu- og dagskriftabúnaði og tilvikum.
**Candidate 3:** Í þessum aðgerðum geta verið borið saman virkni ferla og aðferða, sem tengjast völdum sem valinum er rætt, tveggja hreyfing sem varðar aðild til að ganga úr og beiting á góðum venjulegu aðgerðum, skiptum á starfsmönnum, sameiginlegur vinnslu varnir, ferla og aðferða og þróun aðferða og ferla sem tengjast góðum venjulegu aðgerðum, og/eða dreifingu niðurstöðva, rannsóknaraðgerða og tilviks.
**Candidate 4:** Þessi aðgerðir geta náð því að meta virkni ferla, aðferða og þátta sem tengjast völdum sem velkomið tveggja gerðir, mismunandi flutninga og beitingu góðrar auðlindunarreglna, millifyrriða átt til starfsmanna, sameiginlega vinnslu á vörum, ferlum, áætlanum og aðferðaferlinu, uppfærslu aðferða, hlutverpa og ferli sem greint hefur verið góðri auðlindunarreglur á mismunandi bakgrunnum og hægt er að nota, að greiða út niðurstöður, framkvæmdar- og fanveltnings- upplýsingar og upplýsingar um tilvik.
**Candidate 5:** Þessi aðgerðir geta verið meðferðarferli með samanburði á skilgreindum nýtingu á aðgerðum, aðferðum og tækjum sem tengjast valinu greinunum, milliverkun og beitingu góðra starfsmálayfnda, skiptum á starfsmönnum, sameiginlegri þróun vöru, aðferða- og ferli-verkunar og aðferða- og ferli-gerðar, aðlögun á þeim aðferðum, tækjum og aðferðum sem eru tilgreind sem góðrar starfsmálayfndar og/eða framfylgjanleika á niðurstöðum, áætlunum og aðferða- og leifaskiptum.
**Candidate 6:** Þessar aðgerðir geta verið að koma til samanburðar á virkni verkefnanna, aðferðum og aðfærslum þar sem um tilvika ákvarðaðra kafla eru að ræða, miðlæga sendingu og beitingu góðra venja, skiptis um starfsmenn, sameiginlega þróun vörum, verkefna, áætlana og aðferðafræði, aðlögun á forskriftum á aðferðum, aðferðum og verkefnum sem lýst er sem góða venja, og/eða dreifingu á niðurstöðum, vísunargreina og athugamerkingar.
**Candidate 7:** Þessar aðgerðir geta innihaldið samanburð á skilvirkni verkefna, aðferða og hlutaðeigandi aðferða sem tengjast þeim þóknum sem velun var með, meðferð og beiting á góðum venjulegu starfsemi, skipti um starfsmenn, sameiginlega þróun vöru, verkefna, stefnufarar og aðferða- og aðferðafræði, aðlögun á aðrar kringumstæður aðferða, hluta- og aðferða- og verkefnivöruna sem lýst er sem góðar starfsemi og/eða dreifingu á niðurstöðum, upplýsingum um það og auðkenni og tilheyri fyrirkomulag.

</details>

<details><summary>before · greedy · p13official21:test:eea:409 · F</summary>

**Source:** Purpose: to determine whether the test facility, if engaged in studies using animals or other biological test systems, has support facilities and conditions for their care, housing and containment, adequate to prevent stress and other problems which could affect the test system and hence the quality of data.
**Semantic decision:** F — Animal care/housing/containment omitted and stress becomes development.
**Candidate 0:** Tilgangur: til að ákvarða hvort prófunarstöð varði stofnun og skilyrði til að hafa áhættuvernd fyrir dýrum eða öðrum líffræðilegum prófunarkerfum, svo að það geti komið í veg fyrir þróun og annað vandamál sem geta haft áhrif á prófunarkerfinu og þannig gagnasmiði.

</details>

<details><summary>after · greedy · p13official21:test:eea:1716 · F</summary>

**Source:** In addition, the competent authorities of Gabon provided evidence to the Commission of the adoption of a new civil aviation code in May 2008, of the development of specific operating regulations for airworthiness and operations, and informed that the decision to establish an independent civil aviation agency (ANAC) was taken and should be promulgated in July 2008.
**Semantic decision:** F — The civil-aviation code adoption and airworthiness regulations are corrupted, and the Commission recipient is lost.
**Candidate 0:** Að auki lagði lögbæra yfirvald í Gabón fram sönnunargögn um það að nýtt samþykkti samantekt um samkvæmt- stofnunum fyrir flugvernd og -rekstur, á maí 2008, um þróun sérstakra rekstrarreglna um flugvélstarfsemi og rekstur og tilkynnti um það að ákvörðunin um að setja stofnun sem er óháð og starfandi fyrir flugvernd (ANAC) var tekin og ber að hún verði framkvæmdar á júlí 2008.

</details>

<details><summary>before · G8 · p13official21:test:ema:1610 · U</summary>

**Source:** The true extent of CNS penetration of lamivudine and its relationship with any clinical efficacy is unknown.
**Semantic decision:** U — CNS entry and unknown efficacy relationship partly recognizable in1/3, but true extent/penetration wording is too uncertain to confirm.
**Candidate 0:** Líklegur upplýsingar um útferð áhöfnun lamivúdíns í miðtaugakerfi og tengsl við klíníska verkun eru ekki til staðar.
**Candidate 1:** Hluti innferðar lamivúdíns í miðtaugakerfið og tengingin við klíníska verkun er ekki þekkt.
**Candidate 2:** Reyndar útsetning á höfuðvöðva og myndun lamivúdíns á við áhrif í klínískum tilvikum er ekki þekkt.
**Candidate 3:** Vitað er ekki að vera hversu mikil bera lamivúdín eykur til miðtaugakerfisins og hvaða tengsl með klínískri verkun er.
**Candidate 4:** Ráðstæði endurtekis lamivúdíns til útbrotar í heilaheilabúanefni og tengsl þess við klíníska virkni eru ekki þekktir.
**Candidate 5:** Hjáhlutin lamivúdín í heilaæðum og tengsl þess við klíníska verkun eru ekki þekkt.
**Candidate 6:** Verulegri hátti lamivudíns innrennslis í lifrar- og heilaætlun er ekki þekkt, né tengsl þess við lyfjaformi fyrir klínískri verkun.
**Candidate 7:** Nákvæmar mælingar á inntaki lamivúdíns í miðtaugakerfið og tengsl með klínísku verkun, staðfest ekki í tengslum við nýrnastarfsemi.

</details>

<details><summary>after · G8 · p13official21:test:ema:1152 · P</summary>

**Source:** Change from baseline in body weight was similar for patients treated with sitagliptin relative to placebo.
**Semantic decision:** P — Candidates0,1,3,5,6,7 faithfully retain comparable baseline body-weight change for sitagliptin versus placebo. Checked diff variants contain no hidden changes.
**Candidate 0:** Breyting á líkamsþyngd frá upphafsgildi var svipuð hjá sjúklingum sem fengu sitagliptín í samanburði við lyfleysu.
**Candidate 1:** Breytingar á líkamsþyngd frá grunngildi voru svipuð hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.
**Candidate 2:** Áhrif aðgengi sitagliptins frá grunngildi voru svipað hjá sjúklingum sem fengu meðferð með sitagliptíni miðað við lyfleysu.
**Candidate 3:** Breyting á líkamsþyngd frá upphafsgildi var svipuð hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.
**Candidate 4:** Breyting á líkamsþyngd frá upphafsgildi var svipuð hjá sjúklingum sem fengu sitagliptín samkvæmt lyfleysu.
**Candidate 5:** Breyting frá upphafsgildi líkamsþyngd var svipuð hjá sjúklingum sem fengu sitagliptín samanborið við lyfleysu.
**Candidate 6:** Breyting í líkamsþyngd frá upphafi var svipuð hjá sjúklingum sem fengu sitagliptin samanborið við lyfleysu.
**Candidate 7:** Breyting frá grunngildi líkamsþyngd var svipað hjá sjúklingum sem fengu sitagliptín miðað við lyfleysu.

</details>

<details><summary>before · G8 · p13official21:test:ema:1918 · P</summary>

**Source:** The presented safety information is derived principally from paediatric patients.
**Semantic decision:** P — Candidate4 retains presented safety information mainly derived from paediatric patients, using a child-stage paraphrase.
**Candidate 0:** Sýndar upplýsingar um öryggi liggja aðallega fram fyrir sjúklinga á aldrinum 0-12 ára.
**Candidate 1:** Tilvist öryggiskenndir eru aðallega úr upplýsingum um sjúklinga fyrir börn.
**Candidate 2:** Tilkynntu upplýsingar varðandi öryggi eru í algengu rökstuddar frá sjúklingum á aldri.
**Candidate 3:** Ráðlagðar upplýsingar um öryggi ræðast aðallega frá sjúklingum til handa börnum.
**Candidate 4:** Tilkynnt upplýsingar um öryggi eru, aðallega, úr upplýsingum um sjúklinga á börnastigi.
**Candidate 5:** Sjálfkærar öryggisupplýsingar eru, að höfðu sérstaklega grun í hjá börnum.
**Candidate 6:** Tilkynntum öryggishagana byggist hins vegar áhluti hjá börnum.
**Candidate 7:** Tilkynntar upplýsingar um öryggi eru meðal sinni frá upplýsingum um sjúklinga börn.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:3265 · U</summary>

**Source:** There's a police convention out there.
**Semantic decision:** U — The compound used for police convention is malformed and cannot be certified as the intended meeting.
**Candidate 0:** Það er lögreglukonarinnur þarna.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:2621 · F</summary>

**Source:** I'm glad you found one another."
**Semantic decision:** F — Finding one another becomes finding either one.
**Candidate 0:** Mér gleður að þú hafir fundið annað hvort."

</details>

<details><summary>after · greedy · p13official21:test:ema:2490 · F</summary>

**Source:** If you are left-handed, do what comes naturally to you.
**Semantic decision:** F — Left-handed is lost and replaced by an unrelated headed/addressed word.
**Candidate 0:** Ef þú ert höfðaður skaltu gera það sem er eðlilegt við þig.

</details>

<details><summary>before · G8 · p13official21:test:ema:1788 · U</summary>

**Source:** Magnetic resonance imaging is necessary to confirm the diagnosis of PRES.
**Semantic decision:** U — Candidate2 retains correct English MRI expansion and PRES diagnosis but supplies a contradictory/corrupt Icelandic term; cannot count a fully correct Icelandic candidate.
**Candidate 0:** Gagnvirk skýrslugreiðslu er nauðsynleg til að statra vísbendingu um PRES.
**Candidate 1:** Vera nauðsynlegt að skoða PRES með skynhleði.
**Candidate 2:** Takmörkuðtakmörkuðhvarf (magnetic resonance imaging, MRI) er nauðsynlegt til að staðfesta sjúkdómukvarðanina (PRES).
**Candidate 3:** Magnæskímyndun er nauðsynleg til að staðfesta sjúkdómurinn með sérfæranlif.
**Candidate 4:** Magnsöfnun eru nauðsynleg til að staðfesta sjúkdómssýkingu áfram á PAT- hópum.
**Candidate 5:** Magneðaæðatæknin er nauðsynlegt til að staðfesta sjúkdómssýnina á vegum PRES.
**Candidate 6:** Magnaheilkenni- myndmyndun er nauðsynleg til að staðfesta sýnun á PRES.
**Candidate 7:** Magneðsensíslimm bláæðmyndin er nauðsynlegt til að staðfesta sjúkdómsskýringu á PRES.

</details>

<details><summary>before · greedy · p13official21:test:eso:825 · U</summary>

**Source:** The process of dust trapping is explained in an earlier release (eso1325).
**Semantic decision:** U — Dust accumulation is approximately related to trapping, but powder/release terminology is not confidently correct.
**Candidate 0:** Framkvæmdarferlið um uppsöfnun duftar er skýrt í fyrri útleiðingu (eso1325).

</details>

<details><summary>before · G8 · p13official21:test:eso:349 · F</summary>

**Source:** The results described here use some of these Science Verification data.
**Semantic decision:** F — No candidate preserves results using ScienceVerification data; outputs reverse use relation or substitute unrelated reports.
**Candidate 0:** Niðurstöðurnar sem merktar eru hér notuð sumar af þessum skýringabákmiðum.
**Candidate 1:** Niðurstöðurnar sem gefin eru upp eru notaðar af þessum gagnum um vísindalega sannprófun.
**Candidate 2:** Niðurstöðurnar hér á eftir vega nauðsynlegt af þessum vísindatökum.
**Candidate 3:** Niðurstöðurnar sem lýsað er hér byggja á sumum upplýsingum um vísindaleikaupplýsingar.
**Candidate 4:** Niðurstöðurnar sem lýst er hérinnar eru notaðar á sumum þessara upplýsinga um sannprófun á vísindum.
**Candidate 5:** Niðurstöðurnar sem lýst er hér eru notaðar nokkrar af þessum skýrslugjöfum um vísindalegan sannprófun.
**Candidate 6:** Niðurstöðurnar, sem er lýst hér, ná að sumum þessara Skýrslugjafar.
**Candidate 7:** Niðurstöðurnar sem lýst er hér, skipta séríð af þessum rannsóknarupplýsingum.

</details>

<details><summary>after · G8 · p13official21:test:eea:1144 · F</summary>

**Source:** Successful participation in interlaboratory studies that assess laboratory proficiency is the best way to prove the competence in specific analyses.
**Semantic decision:** F — All eight lose successful participation and/or corrupt interlaboratory proficiency and proof of competence; candidate4's adequate participation still has corrupted institutional/competence objects.
**Candidate 0:** Reynsla í rannsóknir á milli rannsóknarstofa, þar sem sannpróf er gerð á kröftu rannsóknarþjónustu, er bestu leiðin til að sannreyna það.
**Candidate 1:** Viðrekta þátttöku í rannsóknir milli rannsóknarstofa sem mati á nákvæmni rannsóknarstofa er besta aðferðin til að sýna fram á nákvæmni í sérstakan greiningu.
**Candidate 2:** Reynsla í samstarfsrannsóknum á rannsóknarkerfi sem meta nákvæmni rannsóknarstofu er besta leiðin til að sýna fram á nákvæmni við tilteknar greiningar.
**Candidate 3:** Reynsla í samstarfinu milli rannsóknarstofa og stafanir efla stærðfræðilegu atvinnu er góða leiðin til að sannreyna nákvæmni í sérstökum greiningum.
**Candidate 4:** Við fullnægjandi þátttöku í samstarfi írannstu stofnunar sem meta störfum er besta leiðin til að sýna fram á störfarráðgögn í sérstökri greiningu.
**Candidate 5:** Að taka átt í samstarf við rannsóknahúsum þar sem mælt er fyrir um fagleika rannsóknarstofa er besta leiðin til að sannreyna nákvæmni í sérstökum greiningum.
**Candidate 6:** Reynsla í rannsóknir á milli rannsóknarstofa sem meta náið rannsóknarstofa er besta leiðin til að sannprófa nákvæmni í sérstöku greiningu.
**Candidate 7:** Reynsla við þátttöku í samstarfsrannsóknum á verkefni þar sem nýrra kunnáttu stofnanna er geymd er besta leiðin til að sýna fram á þágu tiltekinna greininga.

</details>

<details><summary>after · greedy · p13official21:test:ema:2650 · F</summary>

**Source:** Patients should be advised that in the event of any sudden visual defect, they should stop taking Sildenafil Actavis and consult a physician immediately (see section 4.3).
**Semantic decision:** F — Any sudden visual defect is reduced to a malformed vision-accident condition, losing the sudden/any-defect trigger.
**Candidate 0:** Sjúklingum skal ráðlagt að hætta að taka Sildenafil Actavis ef þeir fá sýnarslysi og leita læknis strax (sjá kafla 4.3).

</details>

<details><summary>after · G8 · p13official21:test:eso:839 · P</summary>

**Source:** The Caisey Harlingten and ASH2 telescopes.
**Semantic decision:** P — Reused exact source+hypothesis semantic decisions; group P requires a known correct candidate, group F requires all distinct candidates known wrong.
**Candidate 0:** Caisey Harlingten og ASH2 sjónauki.
**Candidate 1:** Caisey Harlingten og ASH2 sjónaukarnir.
**Candidate 2:** Caisey Harlingten og ASH2 sjónaukarnirnar.
**Candidate 3:** Caisey Harlingten og ASH2 sjónaukar.
**Candidate 6:** Caisey Harlingten og ASH2 sjónaukarnar.

</details>

<details><summary>after · G8 · p13official21:test:eso:136 · U</summary>

**Source:** ALMA is radically different from visible-light and infrared telescopes.
**Semantic decision:** U — Candidate3 may intend a contrast with visible/infrared telescopes, but malformed comparison and visible-light wording prevent certification. Other variants omit or corrupt the wavelength distinction.
**Candidate 0:** ALMA er í sjaldgæfum undirrofsi frá sjónaukum og innrauðum sjónaukum.
**Candidate 1:** ALMA er hröður mismunandi frá sjónaukum og innrauðu sjónaukum.
**Candidate 2:** ALMA er umfangslega mismunandi sjónaukum sem séðlægt og infraröntunga.
**Candidate 3:** ALMA er svo ólíkraða og sýnilegum sjónauvum og innrauðum sjónauvum.
**Candidate 4:** ALMA er að öllu leyti semskurðaður frá sjónaukum sem sýna í blett eða inndælsluvitru.
**Candidate 5:** ALMA er háttar bátur frá sjónaukum og innrauða sjónaukum.
**Candidate 6:** ALMA er framangreind mismunandi frá sjónaukum sem sjástu og innrauðu.
**Candidate 7:** ALMA er umfangsmikill mismunandi frá sjónaukum og innrauðum sjónaukum.

</details>

<details><summary>after · G8 · p13official21:test:ema:1788 · F</summary>

**Source:** Magnetic resonance imaging is necessary to confirm the diagnosis of PRES.
**Semantic decision:** F — All eight corrupt MRI or the PRES diagnosis; candidate4 copies MRI in English but changes the diagnosed condition.
**Candidate 0:** Gagnkvæmmyndarkerfi er nauðsynlegt til að staðfesta sjúkdóm sjúklinga með PRES-þvagrannsókn.
**Candidate 1:** Vitrunarmyndun að meðferð hjá sjúklingum með PRES er nauðsynleg til að staðfesta sjúkdómssóknina við lyfjameðferð.
**Candidate 2:** Takmörkuðtakmörkuðmyndavissun er nauðsynleg til að staðfesta sjúkdómsgreiningu fyrir PRESS.
**Candidate 3:** Magnæskímsímameðferð er nauðsynlegt til þess að sanna sjúkdómsgreiningu á PRES.
**Candidate 4:** Magnsöfnunareinkenn [magnetic resonance imaging (MRI)] er nauðsynleg til að staðfesta PAT-geðhvarfinu.
**Candidate 5:** Magneðaæðatækniskýring er nauðsynleg til að staðfesta sjúkdóm sýnilegu og glæsilegu.
**Candidate 6:** Magneðsmyndunarmyndkafla er nauðsynlegt til að staðfesta sýnun á PRES.
**Candidate 7:** Skráð magnra upplýsingar eru nauðsynlegar til að staðfesta sjúkdóminn PRES.

</details>

<details><summary>after · greedy · p13official21:test:ema:970 · P</summary>

**Source:** In patients with mild hepatic impairment (Child-Pugh A), there was no significant changes in pharmacokinetics compared with normal healthy volunteers.
**Semantic decision:** P — Preserves mild hepatic impairment Child-Pugh A and no significant pharmacokinetic change versus healthy volunteers.
**Candidate 0:** Hjá sjúklingum með væga skerðingu á lifrarstarfsemi (Child-Pugh A) var engin marktæk breytingar á lyfjahvörfum samanborið við eðlilega heilbrigða sjálfboðaliða.

</details>

<details><summary>after · G8 · p13official21:test:eea:386 · F</summary>

**Source:** Purpose: to inform the management and staff of the facility of the reason for the test facility inspection or study audit that is about to take place, and to identify the facility areas, study(ies) selected for audit, documents and personnel likely to be involved.
**Semantic decision:** F — All eight corrupt or omit the selected studies, facility areas or forthcoming-inspection purpose. Candidate2 omits the selected-study identification and forthcoming timing.
**Candidate 0:** Tilgangur: að aðgestar stjórnvöld og starfsfólk stöðvarinnar um afkvæma skoðun á prófunarstöðvarinnar eða skoðun á rannsóknum sem hefur náð því að komi fram og skoðunarskilnaðið sem verður til að skoða, staðstöðvar rannsóknar sem vel og framlögð hefur verið við skoðunina, skjöl og starfsmenn sem líkleglega eru til þess að taka þátt í skoðun.
**Candidate 1:** Tilgangur: til að upplýsa stjórnveitendum og starfsfólki viðkomandi staðar um ástæður til að eftirlit með staðsetningu prófunarstöðvar eða rannsóknarpróf, sem eru að koma fram, og til að greina umræddum vettvangi, viðrænum rannsókn, sem verður að valað, skjöl og starfsmenn sem líklega eru að taka þátt í prófun eða rannsókn.
**Candidate 2:** Tilgangur: til að upplýsa stjórnninga og stofnunarstarfsmenn um ástæður eftirlits á prófunarstöðvarinnar eða eftirlit með rannsóknirnar og til að greina þær svið stofnunar sem hafa verið valið fyrir eftirlit, skjöl og starfsmenn sem líklegt er að það sé að þau gangi til.
**Candidate 3:** Tilgangur: til að tilkynna framkvæmdarstjóra og starfsmanni ástæða við eftirlitsins á prófunarstöðvarinnar eða skoðunareftirlitsáritun sem fer fram og til að viðurkenna svæði stofunnar, rannsóknirnar sem verða að verða til kynna í skoðun, skjöl og starfsmenn sem líklegt er að hafi þátt í henni.
**Candidate 4:** Til: til að upplýsa stjórnun og starfsmenn stöðvarinnar um ástæðu til að framkvæma eftirlit með eftirlitsaðferðum í prófunarstöðvar eða eftirlitsráðstöfun, sem er að komast, og til að greina það yfir svið stöðvarinnar sem áfturnar voru úr útlögum, skjöl og starfsmenn sem líklegt er að leynist í eftirlitsaðferðum.
**Candidate 5:** Til: til að tilkynna framkvæmdastjórnina og starfsfólk á starfshúsinu um ástæðu til að rannsaka eða ganga úr skugga um gagnaúttekin matvísindaskoðun (audit) sem komi að því erfengi, og til að ákvarða þær stöðvastöðvar, greinir og starfsfólk sem líklega gætu komið í gegnum.
**Candidate 6:** Tilgangur: til að upplýsa stjórnun og starfsmenn stöðvarinnar um sökum í eftirliti með aðgerða-stöðvar eða rannsóknar- eftirliti sem verður að fara fram og til að kanna svið stöðvarinnar sem rannsóknar(eye) eru velur eftir, skjölin og starfsmenn sem líklega komast að aðgerða- eða rannsóknar-stöðvarinnar.
**Candidate 7:** Tilgangur: til að upplýsa stjórnun og starfsfólk stöðvarinnar um ástæðu á eftirliti með prófunarstöðu eða framkvæmdar- eftirliti með rannsóknir sem lýkur og til að ákveða yfirvöld og skjöl sem líklegt er að taka þátt í eftirlits- rannsóknunum og útbúa til stuðningar.

</details>

<details><summary>after · greedy · p13official21:test:opensubtitles:3484 · F</summary>

**Source:** If you do not give me the house you promised I shall be forced to return to England.
**Semantic decision:** F — The negative condition if you do not give becomes if you give; return/forced wording is also corrupted.
**Candidate 0:** Ef þú gefur mér húsinn sem þú lofaðir mér skal ég vera forðast til að fara til Englands.

</details>

<details><summary>before · greedy · p13official21:test:opensubtitles:3484 · F</summary>

**Source:** If you do not give me the house you promised I shall be forced to return to England.
**Semantic decision:** F — NOT giving the house becomes giving it, reversing the premise.
**Candidate 0:** Ef þú gefur mér húsinn sem þú lofaðir mér skal ég vera forðast til England.

</details>

<details><summary>after · G8 · p13official21:test:eea:2120 · F</summary>

**Source:** In order to facilitate data flows from the European Union, it is desirable for processors providing data-processing services to several data controllers in the European Union to be allowed to apply the same technical and organisational security measures irrespective of the Member State from which the data transfer originates, in particular in those cases where the data importer receives data for further processing from different establishments of the data exporter in the European Union, in which case the law of the designated Member State of establishment should apply.
**Semantic decision:** F — All eight corrupt controller/processor/exporter/importer roles or organisational-security/legal-establishment conditions. Candidate4 replaces organisational measures with stable-security-treatment wording.
**Candidate 0:** Til að auðvelda gagnaflokkun frá Evrópusambandinu er æskilegt að meðferðandi fyrirtækjum, sem veita gagnavinnsluþjónustu fyrir nokkrar gagnaegingarstjórar í Evrópusambandinu, sé heimilt að beita eins tæknilegra og stjórnskipulagsöryggis- aðgerða án tillits til þess aðildarríkis sem gögnum er sendin frá, einkum þegar gagnaðövalu fær gögn til frekari gagnavinnslu frá annarra starfsmanns gagnaútöluðs aðila í Evrópusambandininu, því skal gilda lög tilnefnda aðildarríkis.
**Candidate 1:** Til þess að auðvelda gagnaflokkun úr Evrópusambandinu er æskilegt að vinnslumannir, sem veitir gagna- vinnsluþjónustu fyrir nokkrir gagna-/við- haldara í Evrópusambandinu, séu veitt hæfi á þeim að beita eins tækni- og stjórnsýslufyrirkomulag sem að öðrum tíma fylgir aðildarríkið, sem frá því að gagnaflutningin er upphafð, einkum þegar gagna- inntakið fær gagna til frekari vinnslu frá mismunandi stöðum útgefandans í Evrópusambandininu, þá skal nota löggjaf við- tilnefnda aðildarríkisins um staðfestu.
**Candidate 2:** Til þess að auðvelda gagnagjöf frá Evrópu- samræmingunni ætti því að hægt sé að aðildarréttar vinnuhöfundar sem veita gagnagjafar- aðstoð fyrir nokkrar gagna-til- stjóra í Evrópusambandinu að beita sambærilegum tæknilegum og stjórnsýslustöðumökkum án tillits til aðildarríkis þar sem upp- færslan gagnanna koma frá, einkum þegar upptöku gagnasamþæginda fær gagna til frekari gagnavöktunar frá annarri starfsmanns stofnunar gagna- senda í Evrópusambandinu, þá skal beita löggjöf þess aðildarríkis sem aðildarsvæði innkaupstofnunarinnar.
**Candidate 3:** Til að auðsökja gagnaflokkun frá Evrópusambandinu er það æskilegt að upplsingulari sem veitir gagnavinnsluþjónustu fyrir nokkrar gagna- megir í Evrópusambandinu verði heimilt að beita sömu tæknilegum og stjórnsýslulegum öryggiságregum án tillits til þess aðildarríkis þar af leiðandi framfæri gagna verður heimilt, einkum þegar gagnainnöndandi tekur gögn til frekari gagnavinnslu frá annars staðar sem gagnaútgjafa fjöl undir staðfestu í Evrópusambandininu, þá skal beita lögum þeirra aðildarríkis sem setur er upplýsingum til staðfestunar á.
**Candidate 4:** Til þess að skipti gögn hafi greiðslega orsakstækni frá Evrópusambandinu skal gagnvirkja, sem veita gagnagjafarþjónustu fyrir nokkur gagna- meðhöndlendur í Evrópusambandinu, vera heimilt að beita samskonnum tæknilegum og stöðuga öryggismeðferðarvörlum, án tillits til hvaða aðildarríkis gagnaflutningin er frá, einkum þegar gagna- innflytjendurin fær gögn frá annarri stofnun útflutningsgagna í Evrópusambandinu til frekari gagna- meðhöndlunar, þá skal löggjöf tilnefnis aðildarríkisins, þar sem stofnunin er staðfest, gilda.
**Candidate 5:** Til þess að auðvelda gagnaflokkun frá Evrópusambandinu er það bein til að heimila rekstillum sem veita gagnagjafarþjónustu fyrir nokkur gagnvirkjaraðilar í Evrópusambandinu að beita sömu tæknilegum og stjórnsýslumótunum öryggismati án tillits til þess aðildarríkis sem gagnframiðalaginn hefur fengið gögnum, einkum þegar rekstillinn fær gögn til frekari gagnavinnslu frá annarri starfsemi gagnaútandi í Evrópusambandinu, þá skal beita lögum tilnefndar aðildarríkis.
**Candidate 6:** Til þess að auðvelda gagnagjöf frá Evrópusambandinu er æskilegt að geymdarlýsföng, sem veita gagna- meðhöndlunssérvið aðildarríkjum í Evrópusambandinu, séið heimilt að beita eins tæknilegra og skipulagslega öryggis- ráðstöfunum án tillits til þess aðildarríkis sem rekstrurinn er frá, einkum þegar gagna innflytjandi fær gögn til frekari gagna- meðhöndlunar frá mismunandi stofnunum útflutningsaðila í Evrópusambandinu, þá skal beita lögum þeirra aðildarríkis sem sett er á við.
**Candidate 7:** Til þess að auðvelda gagnaleiðir frá Evrópusambandinu, er þá þarf að leyfa vinnsluþegum, sem veita gagnavinnsluþjónustu fyrir nokkur gagnvirkjastjóra í Evrópusambandinu, að beita sama tæknilegum og stjórnsýslulegum öryggismörkum án tillits til þess aðildarríkis sem gagnaflutningurinn hefur komið fram frá, einkum þegar gagnaflutninginn hefur sent gögn til annars aðildarríkisins á milli viðkomandi rekstraraðila gagnaflutningsins í Evrópusambandinu, þá skal gilda lög þess aðildarríkis sem tilnefnt er vegi viðsetningarupptaðrar stofnana.

</details>

<details><summary>after · G8 · p13official21:test:eea:1471 · F</summary>

**Source:** Prices including all taxes, levies and VAT.
**Semantic decision:** F — All eight corrupt VAT and/or levies rather than preserving the complete tax-inclusive-price condition.
**Candidate 0:** Verð, þar me áhverju skattaukum, skuldbindingum og gervogi.
**Candidate 1:** Verð sem takmarkast allarum skatta og skattatilteknar og skipulagi.
**Candidate 2:** Verði þar sem allar skatta, skuldbindingar og gilda skatteydis.
**Candidate 3:** Verð þar sem tilgreind eru öll skálds eftirþegar og skatteysku skattatrefni.
**Candidate 4:** Verðin þar með í töflum, skattum, skattatöldum skatti og skatttegundum.
**Candidate 5:** Verð þar sem þar til hafa verið skráð heildaraukningar, skatt eða skattatökin og örvunarskeiðisauka.
**Candidate 6:** Verð þar sem fela upp allar skattir, krafir og skattatfærslu.
**Candidate 7:** Verð þar sem allar skatta og skólar og gilda skatteydislega.

</details>

<details><summary>before · G8 · p13official21:test:eea:1409 · F</summary>

**Source:** The port security assessment is the basis for the port security plan and its implementation.
**Semantic decision:** F — No correct port-security-assessment-as-basis-for-plan relation; several reverse assessment/plan or change port.
**Candidate 0:** Portvænslarasmat er grunn úr áætlun um portvænslu og framkvæmd þeirrar.
**Candidate 1:** Portvæsnarænsla er grundvöllur við áætlunina um vænskun á hafðum og framkvæmd hennar.
**Candidate 2:** Portverndarúttekkningin er grunnur á portverndarefni og framkvæmdi þess.
**Candidate 3:** Vaktarúttekkandi mat á vörðunartökum er grunnur fyrir vaktarútgáfu aðurstofunnar og framkvæmd hennar.
**Candidate 4:** Portvættaráætlunin er grunnur fyrir mat á portvættamál og beitingu þess.
**Candidate 5:** Portaðbelti mat er grunnur fyrir portaðbeltakerfið og framkvæmd þess.
**Candidate 6:** Upprétting á öryggi borgarinnar er grunur fyrir áætlun á öryggis borgarins og framkvæmd hennar.
**Candidate 7:** Rörverndarskyldur í vikilund eiga að vera grundvöll fyrir rörverndarplofið og framkvæmd þess.

</details>

<details><summary>after · greedy · p13official21:test:ema:2722 · F</summary>

**Source:** See also ‘Bleeding or bruising after you stop treatment in section 4.
**Semantic decision:** F — Bruising is replaced by extinguishers/switching wording rather than a bruising adverse effect.
**Candidate 0:** Sjá einnig „Blæðingar eða slökkvur eftir að meðferð er hætt í kaflanum 4.

</details>

<details><summary>after · G8 · p13official21:test:ema:1433 · F</summary>

**Source:** Aseptically add sodium pertechnetate (Tc 99m) solution (from step d above) to the tilmanocept powder vial.
**Semantic decision:** F — No candidate preserves aseptic addition of the stated solution from step d above. Candidate5 only specifies sterile solution, not aseptic technique;0 reverses above/below.
**Candidate 0:** Aefnid úr bakkrænngjafandi vökvi af natríum pertechnetat (Tc 99m) lausn (frá d-stiginn hér fyrir neðan) skal bæta upp í hettuglasið með tilmanocept dufti.
**Candidate 1:** Að því að víðgjafa efnið, vatnsburts natríum perteknetat (Tc 99m) lausn (frá d-stiginn hér að framan), skal bæta það í hettuglas með tilmanocept stofnum.
**Candidate 2:** Aflsa evicósteróetat (Tc 99m) lausn (frá d stigi hér að ofan) uppi á tilmanocept duftvökvið í apfæri.
**Candidate 3:** Að og augnunum að því að bæta natríum pertechnetat (Tc 99m) lausn (frá d-stiginn hér að framan) í hettuglasinu með tilmanocept dufti.
**Candidate 4:** Að þeim niðurbreytu skal bæta natríumpertektetat (Tc 99m) lausn (frá d-staðli hér að ofan) við vefjaskammtinn í hettuglasinu með tilmanocept-dufti.
**Candidate 5:** Nota skal sæfða natríum pertechnetat (Tc 99m) lausn (úr d-staðli hér að ofan) í hettuglas með tilmanócept dufti.
**Candidate 6:** Aa skilervi skal blanda natríum pertechnetat (Tc 99m) lausn (frá d-stiginn hér aefri) á tilmanócept duft í hettuglas.
**Candidate 7:** Aðskildaverk, síðan útsett eftir öryggismiðlun, aðselti í tilmanocept duftglas með hettuglasið (sá sem fyrir hér á fram fæst).

</details>

<details><summary>before · greedy · p13official21:test:eso:918 · F</summary>

**Source:** "With such short orbital periods, the planets are between 20 and 100 times closer to their star than the Earth to the Sun. The structure of this planetary system is much more similar in scale to the system of Jupiters moons than to that of the Solar System," explains Michaël Gillon.
**Semantic decision:** F — Jupiter moons becomes planets; scale comparison is corrupted.
**Candidate 0:** „Með slæma umferðarfráhringum eru plönturnir í 20 til 100 sinnum nálægri fjarlægð frá stjörnunni en jörðin frá sólinni,“ segir Michaël Gillon. „Staðsetningur þessarar reikistjarna er mjög lítiltar sambærilegur við reikistjarnanir Júpíters en reikistjarnanir á sólkerfinu,“ segir Michaël Gillon.

</details>

<details><summary>after · G8 · p13official21:test:ema:1414 · P</summary>

**Source:** Invokana has no or negligible influence on the ability to drive, cycle, and use tools or machines.
**Semantic decision:** P — Candidate6 preserves no/negligible effect on driving, handling a bicycle and using tools or machines, with awkward grammar.
**Candidate 0:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, hlaupi eða notkunar viðvörunnar eða vélar.
**Candidate 1:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, leikar og notkunar vélum eða véla.
**Candidate 2:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, hjóla og notkunar vélsla eða véla.
**Candidate 3:** Invokana hefur engin áhrif eða óveruleg áhrif á hæfni til aksturs, byssu og notkunar verkjar eða vélka.
**Candidate 4:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, kringgöngu og notkunar tæki eða vél.
**Candidate 5:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, hálsbólgu og notkunar tæknilegra eða vélaga.
**Candidate 6:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, höndla hjól og nota verkfæri eða vélar.
**Candidate 7:** Invokana hefur engin eða óveruleg áhrif á hæfni til aksturs, kringganga og notkunar vélaga eða véla.

</details>

<details><summary>after · G8 · p13official21:test:eso:80 · P</summary>

**Source:** But the new study using the VLT has found that much of the stars energy is being absorbed and scattered by dust clouds before it gets to Earth - it is actually more luminous than previously thought and among the brightest stars known.
**Semantic decision:** P — Candidate2 retains stellar energy absorbed and scattered by dust before reaching Earth, greater luminosity than previously thought, and placement among the brightest known stars; plural inflection is imperfect.
**Candidate 0:** En í nýju rannsókninni sem notuð var VLT varð ályktuna á að mikið af orku stjarnaðar fleygi og dreifir í rykskýi áður en þær ná yfir fyrir Jörðina - og er virkilega ljósnarvararlegari en víst var og í sameiginlegu björgunarefni stjarna.
**Candidate 1:** En nýr rannsóknin með VLT hefur komið fram að mikill af orku stjarnaðs er tekið upp og skumi af rykskýum áður en stjarnan kom til jörðinnar – hjá starvunum er sjálfur bjartari en telst áður og hans er einn af bjartustu stjarna sem það er þekkt af.
**Candidate 2:** En þessan nýja rannsókn með VLT hefur fundið að mikið af orku stjarnanna er tekið upp og dreifin af rykskýi áður en hún kemur til jörðar - orðið er meiri björtu en áður var talið og á meðal björtustu stjörnur sem þekktar hafa verið.
**Candidate 3:** En í nýju rannsóknina sem notaði VLT varðar stjörnum varð framkallar rýmkið varð fremur meira heimilt á slysli rýmsins en í fyrra rannsóknunum, sem varðar stjörnum, og voru einnig víst skýðin fyrir að það verði birtari en áður varð eftirlit með og að því er til fyrir tilvikum er einnig fyrirbært og er tilfelli litlegasta stjörnurnar sem vitað er um.
**Candidate 4:** En nýi rannsóknin með VLT- orðið að munu af millenniaiðisvirkni stjarnanna að leysast og dreifast af rykafjölda fyrir á Earth og er í raun munu ljósandi enn frekar en ætti að telja og er einnig bjarts meðal brestasta stjarna sem vitað er um.
**Candidate 5:** En nýtt rannsókn með VLT hefur komið í ljós að umtalsvert forstæðina borða og dreifast af rykskýi áður en þeir ná yfir til Jörðar - þau eru í raun brjáltímisli sterra en ýtindi hafa gert mælingum á þeim og birtustu mestar stjörnur.
**Candidate 6:** En nýtt rannsókn með VLT hefur komið í ljós að flestaríkis litan stjarnanna er saman tekið og dreifin af rykklóum áður en þær ná á Jörðina - þannig er fyrrandi ljósins leiðandi og það líður fyrir á meðal þær björtustu stjörnur sem vitað er um.
**Candidate 7:** En rannsóknin sem átti VLT að þeim sást, lenti fram að fjölliði stjarna er borin til sér í geislun og dreifingu með rykskýi áður en stjarnan ná að Jörðinni - hún er í raun verið gegnleiki stjarna en áður var víklað.

</details>

<details><summary>after · greedy · p13official21:test:eso:400 · F</summary>

**Source:** ESPRESSO will feature radial velocity precision of 0.35 km/hour or less.
**Semantic decision:** F — The radial component of radial velocity is omitted; generic speed precision is less specific than the stated measurement.
**Candidate 0:** ESPRESSO mun koma fram með nákvæmni á hraða 0,35 km/klst. eða minna.

</details>

<details><summary>before · G8 · p13official21:test:eea:930 · F</summary>

**Source:** Wells in microtitre plates are coated overnight with recommended dilutions of purified immunoglobulin fractions of antibodies of reference quality.
**Semantic decision:** F — All corrupt microtitre wells/coating overnight or purified immunoglobulin/reference-quality dilutions.
**Candidate 0:** Vélur á miðlæga hettuglasum eru lausn undir einn sólarhring með tilgreindri þynningu úr því að þynna ónæmisglóbúlíni fyrir öryggishæfðum mótefni.
**Candidate 1:** Wells á milliglaðutækinu eru klavaðir eftir kvöld með ráðlögðum þynningu af gilduðum ónæmisglóbúlínfráhófum mótefna, sem eru til staðar.
**Candidate 2:** Hettuglöfur í mikið gluggu eru úða út í nálægt tíma með ráðlögðum þynningum af hreinsuðri immunglóbúlín frumum mótefna miðað við viðmiðunarmeðferð.
**Candidate 3:** Vellir í bilsuflöginna eru klúftir til baka með tilmeðræði þolsum tómörum af gerðarimmúnóglóbúlíni frahófum mótefna með viðmiðunarmikilli gildum.
**Candidate 4:** Vell í lyfjaplatti eru klúft í nálægt tíma með skammta (recommended dilutions) úr gerð nýrnaefnum í samræmi við staðbundna gildi.
**Candidate 5:** Wells í mífretturplaðum eru útfellt í svolíti smá tímar sem ráðlögða þynningu af hreinsuðu immunglóbúlín-skilum mótefna af gæða við viðmiðunarmál.
**Candidate 6:** Vellir á milliseðlunarplátum eru klippið með ráðlagðum þynningum úr gerðnum immungólóbínlíffrásundum mótefna með viðmiðunarmikilli gæði.
**Candidate 7:** Vell í mífurýrfræðum æsast á næurnum með viðeigandi þynningum úr hreinsuðum immunglóbúlni í sérstökum stigi mótefna af gertgöngu stærðfræðilegu gæfni.

</details>

<details><summary>after · greedy · p13official21:test:ema:709 · U</summary>

**Source:** The other ingredients are sodium chloride, succinic acid, polysorbate 80, 2- phenoxyethanol and water for injections.
**Semantic decision:** U — Other ingredients are recognizable, but cannot certify the unusual succinic-acid term as the correct chemical.
**Candidate 0:** Önnur innihaldsefni eru natríumklóríð, súkfinýlsýra, pólýsórbat 80, 2- fenoxýetanól og vatn fyrir stungulyf.

</details>

<details><summary>before · greedy · p13official21:test:eso:349 · F</summary>

**Source:** The results described here use some of these Science Verification data.
**Semantic decision:** F — Results using verification data becomes results being used; source/data roles reverse.
**Candidate 0:** Niðurstöðurnar sem koma fram hér eru notaðar sumar af þessum gögn um sannprófun á vísindum.

</details>

<details><summary>after · greedy · p13official21:test:eso:918 · F</summary>

**Source:** "With such short orbital periods, the planets are between 20 and 100 times closer to their star than the Earth to the Sun. The structure of this planetary system is much more similar in scale to the system of Jupiters moons than to that of the Solar System," explains Michaël Gillon.
**Semantic decision:** F — Earth-Sun and Jupiter-moon scale comparisons are corrupted into repetitive Jupiter wording.
**Candidate 0:** „Með slíkum stuttum hringi er fyrirbærið á milli stjarna og jörðs um 20 til 100 sinnum nærri stjörnunni en Júpíterhjúpinarnir eru í námi við Júpíter og Júpíterhjúpinarnir eru lítilvillilega svipuðar við Júpíter og Júpíterhjúpinarnir eru lítilvillilega svipuðar við sólkerfinu,“ segir Michaël Gillon.

</details>

## 已训练样本逐条审核 / Known-seen fitting cases


<details><summary>after · fit-greedy · OpenSubtitles18:183388 · P</summary>

**Source:** Thanks for taking us up here.
**Reference:** Takk fyrir að koma með okkur hingað.
**Semantic decision:** P — Retains thanks for bringing/taking us up here.
**Candidate 0:** Takk fyrir að taka okkur upp hérna.

</details>

<details><summary>after · fit-greedy · ParIce21:tatoeba:6374 · P</summary>

**Source:** Do it the way he tells you to.
**Reference:** Gerðu það eins og hann segir þér.
**Semantic decision:** P — Preserves doing it as he instructs.
**Candidate 0:** Gerðu það eins og hann segir þér að gera.

</details>

<details><summary>before · fit-greedy · ParIce21:tatoeba:7662 · P</summary>

**Source:** If you wish to take, you must first learn to give.
**Reference:** Ef þú vilt taka, verðurðu fyrst að læra að gefa.
**Semantic decision:** P — Preserves learning to give first as a condition for taking.
**Candidate 0:** Ef þú vilt taka þá verður fyrst að læra að gefa.

</details>

<details><summary>after · fit-greedy · ParIce21:ema:158245 · F</summary>

**Source:** If someone else is injecting you, they can also use the back and side of your upper arms (see grey areas in picture 7).
**Reference:** Ef einhver annar sprautar þig má líka nota upphandleggina aftanverða og til hliðanna (sjá grá svæði á mynd 7).
**Semantic decision:** F — Grey areas become green and upper-arm specificity is lost.
**Candidate 0:** Ef einhver annar er að sprauta þig getur hann einnig notað bak og hliðar handleggja ykkar (sjá grænu svæði í mynd 7).

</details>

<details><summary>before · fit-greedy · ParIce21:eso:2710 · P</summary>

**Source:** Earlier measurements suggested that the system was younger.
**Reference:** Eldri mælingar bentu til að kerfið væri yngra.
**Semantic decision:** P — Preserves earlier measurements suggesting the system was younger; tense/inflection is imperfect.
**Candidate 0:** Fyrri mælingar benda til þess að kerfið væri yngri.

</details>

<details><summary>before · fit-greedy · ParIce21:tatoeba:6374 · P</summary>

**Source:** Do it the way he tells you to.
**Reference:** Gerðu það eins og hann segir þér.
**Semantic decision:** P — Preserves doing it as he tells the addressee.
**Candidate 0:** Gerðu það eins og hann segir.

</details>

<details><summary>before · fit-greedy · ParIce21:ema:185074 · P</summary>

**Source:** Infusion-related adverse events are infrequent when the rate of anidulafungin infusion does not exceed 1.1 mg/min.
**Reference:** Innrennslistengdar aukaverkanir eru mjög sjaldgæfar ef hraði anidulafungins innrennslis fer ekki yfir 1,1 mg/mínútu.
**Semantic decision:** P — Preserves rare infusion-related adverse events when anidulafungin rate does not exceed1.1mg/min.
**Candidate 0:** Aukaverkanir tengdar innrennslis eru sjaldgæfar þegar innrennsli af anidulafungini er ekki hærra en 1,1 mg/mínútu.

</details>

<details><summary>before · fit-greedy · ParIce21:eea:2890153 · F</summary>

**Source:** What is the legal basis for the data source?
**Reference:** Hver er lagagrundvöllurinn fyrir gagnaheimildinni?
**Semantic decision:** F — Data source becomes data summary/aggregation, changing the object whose legal basis is requested.
**Candidate 0:** Hver er lögleg grundvöllur fyrir gagnasamantektina?

</details>

<details><summary>before · fit-greedy · OpenSubtitles18:183388 · P</summary>

**Source:** Thanks for taking us up here.
**Reference:** Takk fyrir að koma með okkur hingað.
**Semantic decision:** P — Preserves thanks for bringing us up here.
**Candidate 0:** Takk fyrir að taka okkur upp hingað.

</details>

<details><summary>before · fit-greedy · ParIce21:eea:3227721 · P</summary>

**Source:** The ‘Red Tractor Farm Assurance Combinable Crops & Sugar Beet Scheme’ was submitted on 4 April 2012 to the Commission with the request for recognition.
**Reference:** Áætlunin um „Red Tractor Farm Assurance Combinable Crops & Sugar Beet Scheme“ var lögð fram til fram- kvæmdastjórnarinnar 4. apríl 2012 ásamt beiðni um viðurkenningu.
**Semantic decision:** P — Preserves the named scheme,4April2012 submission, Commission and recognition request.
**Candidate 0:** „Red Tractor Farm Assurance Combinable Crops & Sugar Beet Scheme“ var lagt fram á 4. apríl 2012 til framkvæmdastjórnarinnar með beiðni um viðurkenningu.

</details>

<details><summary>after · fit-greedy · ParIce21:eea:3205170 · F</summary>

**Source:** The creative and artistic work of authors and performers necessitates an adequate income as a basis for further cre- ative and artistic work, and the investments required par- ticularly for the production of phonograms and films are especially high and risky.
**Reference:** Til þess að höfundar og listflytjendur geti unnið áfram að skapandi og listrænu starfi er nauðsynlegt að tryggja þeim nægilegar tekjur af skapandi og listrænu framlagi sínu; einnig er nauðsynleg fjárfesting, einkum vegna framleiðslu hljóðrita og kvikmynda, mjög mikil og áhættusöm.
**Semantic decision:** F — Authors/performers become registered persons/telescopes, and the adequate-income requirement and media investments are corrupted.
**Candidate 0:** Krafti og menningarlega verkefni skráðra og sjónaukana þarf að vera fullnægjandi til að gera grundvöll fyrir frekari krafti og menningarlega verkefni og þar sem nauðsynlegt er að sjá um fjárfestingar, einkum við framleiðslu hljóðmyndanna og myndasafna, eru sú fjárhagslegur og hættulegur.

</details>

<details><summary>after · fit-greedy · ParIce21:ema:185074 · P</summary>

**Source:** Infusion-related adverse events are infrequent when the rate of anidulafungin infusion does not exceed 1.1 mg/min.
**Reference:** Innrennslistengdar aukaverkanir eru mjög sjaldgæfar ef hraði anidulafungins innrennslis fer ekki yfir 1,1 mg/mínútu.
**Semantic decision:** P — Preserves infrequent infusion adverse events and the1.1mg/min ceiling.
**Candidate 0:** Aukaverkanir tengdar innrennslisferlum eru sjaldgæfar þegar innrennsli af anídúláfúngíni nær ekki yfir 1,1 mg/mín.

</details>

<details><summary>before · fit-greedy · ParIce21:ema:158245 · F</summary>

**Source:** If someone else is injecting you, they can also use the back and side of your upper arms (see grey areas in picture 7).
**Reference:** Ef einhver annar sprautar þig má líka nota upphandleggina aftanverða og til hliðanna (sjá grá svæði á mynd 7).
**Semantic decision:** F — The injection location loses upper-arm specificity; arms alone also include other regions.
**Candidate 0:** Ef einhver annar er að sprauta þig getur hann einnig notað bak og hliðar handleggjum ykkar (sjá gráu svæðið í mynd 7).

</details>

<details><summary>before · fit-greedy · ParIce21:ema:377570 · P</summary>

**Source:** Thyrogen should not be used during breast-feeding.
**Reference:** Ekki skal nota Thyrogen við brjóstagjöf.
**Semantic decision:** P — Correctly prohibits Thyrogen during breast-feeding.
**Candidate 0:** Notið Thyrogen ekki meðan á brjóstagjöf stendur.

</details>

<details><summary>before · fit-greedy · ParIce21:eso:5121 · F</summary>

**Source:** But dry conditions are not the only requirement, the detectors need to be cooled to a very low temperature of –269 degrees Celsius - just 4 degrees above absolute zero - for them to work.
**Reference:** Ekki aðeins þarf að vera þurrt heldur verður að kæla mælitækin niður í –269°C - aðeins 4 gráður yfir alkuli - til þess að þau virki sem skildi.
**Semantic decision:** F — Dry conditions are omitted and absolute zero becomes total radiation, corrupting the cooling requirement.
**Candidate 0:** En það er ekki einn skilyrði, þarf að kæra mælitækinu í mjög lágan hita, –269 gráður C, bara 4 gráður yfir heildargeislun, til að þau verka.

</details>

<details><summary>after · fit-greedy · ParIce21:eso:821 · F</summary>

**Source:** In Messier 18 the blue and white colours of the stellar population indicate that the clusters stars are very young, probably only around 30 million years old. Being siblings means that any differences between the stars will only be due to their masses, and not their distance from Earth or the composition of the material they formed from.
**Reference:** Í Messier 18 benda bláu og hvítu litir stjarnanna til þess að þyrpingin sé mjög ung, líklega aðeins í kringum 30 milljón ára. Stjörnurnar eru systur svo eini munurinn á þeim er kominn til af massa þeirra en ekki fjarlægð frá jörðinni eða samsetningu efnisins sem myndaði þær.
**Semantic decision:** F — Sibling/shared-origin status becomes being representatives; the central common-origin premise is corrupted.
**Candidate 0:** Í Messier 18 birta blár og hvít litur stjörnumyndunar þess að stjörnurnar í þeim eru mjög ungar, hugsanlega bara um 30 milljón ára gamall. Að vera fulltrúar þýðir að allar munurar milli stjarnaðs verði aðeins af massamagni þeirra og ekki af fjarlægð frá Jörðinni eða samsetningu efna sem þau myndaðust úr.

</details>

<details><summary>before · fit-greedy · ParIce21:ema:185234 · F</summary>

**Source:** In GEICAM 9805 study, alopecia persisted into the follow-up period (median follow-up time of 10 years and 5 months) and was observed to be ongoing in 49 patients (9.2 %) in TAC arm and 35 patients (6.7 %) in FAC arm.
**Reference:** Í GEICAM 9805 rannsókninni var hármissir viðvarandi eftir að eftirfylgnitímabilið hófst (miðgildi eftirfylgni var 10 ár og 5 mánuðir) og var enn til staðar hjá 49 sjúklingum (9,2%) í TAC hópnum og 35 sjúklingum (6,7%) í FAC hópnum.
**Semantic decision:** F — Alopecia becomes a blood/skull term, changing the adverse event despite retained follow-up numbers.
**Candidate 0:** Í GEICAM 9805 rannsókninni var blóðkúpu eftirfram í eftirfylgnitímabilinu (miðgildi eftirfylgnitíma 10 ára og 5 mánuði) og sást að það hafi áfram áfram hjá 49 sjúklingum (9,2%) í TAC hópnum og 35 sjúklingum (6,7%) í FAC hópnum.

</details>

<details><summary>before · fit-greedy · ParIce21:ema:391314 · F</summary>

**Source:** Vaccination should be postponed during any illness with fever >38.5°C.
**Reference:** Fresta skal bólusetningu við öll veikindi með hita > 38,5°C.
**Semantic decision:** F — Any illness with fever is narrowed to infection with fever; not all illnesses are infections.
**Candidate 0:** Fresta skal bólusetningu meðan á sýkingi stendur með hita > 38,5°C.

</details>

<details><summary>after · fit-greedy · ParIce21:eso:2710 · P</summary>

**Source:** Earlier measurements suggested that the system was younger.
**Reference:** Eldri mælingar bentu til að kerfið væri yngra.
**Semantic decision:** P — Exact source/hypothesis reuse from inspected fit card4: Preserves earlier measurements suggesting the system was younger; tense/inflection is imperfect.
**Candidate 0:** Fyrri mælingar benda til þess að kerfið væri yngri.

</details>

<details><summary>after · fit-greedy · OpenSubtitles18:1029178 · F</summary>

**Source:** She'd smile at me. She was so sweet, but you could see it in her eyes.
**Reference:** Hún brosti til mín. Var svo indæl en maður sá það í augum hennar.
**Semantic decision:** F — The smiling action is replaced by malformed laugh-at wording; the stated facial action is not retained.
**Candidate 0:** Hún hlæddi sig á mig. Hún var svo sæt, en þú gætir séð það í augunum hennar.

</details>

<details><summary>after · fit-greedy · ParIce21:eso:5121 · F</summary>

**Source:** But dry conditions are not the only requirement, the detectors need to be cooled to a very low temperature of –269 degrees Celsius - just 4 degrees above absolute zero - for them to work.
**Reference:** Ekki aðeins þarf að vera þurrt heldur verður að kæla mælitækin niður í –269°C - aðeins 4 gráður yfir alkuli - til þess að þau virki sem skildi.
**Semantic decision:** F — Dry-condition requirement is omitted and absolute zero is corrupted into a different/nonstandard concept.
**Candidate 0:** En það er ekki einn skilyrði, þarf að kælja mælitækin í mjög lágan hita, –269 gráður Celsíus - bara 4 gráður yfir alheilabott - til að þau verki.

</details>

<details><summary>after · fit-greedy · ParIce21:eea:1150937 · F</summary>

**Source:** Commission Implementing Decision 2011/215/EU of 4 April 2011 implementing Council Directive 97/78/EC as regards transhipment at the border inspection post of introduction of consignments of products intended for import into the Union or for third countries (3) is to be incorporated into the Agreement.
**Reference:** Fella ber inn í samninginn framkvæmdarákvörðun framkvæmdastjórnarinnar 2011/215/ESB frá 4. apríl 2011 um framkvæmd tilskipunar ráðsins 97/78/EB að því er varðar umfermingu afurðasendinga, sem eru ætlaðar til innflutnings til Sambandsins eða þriðju landa, á skoðunarstöð á landamærum þar sem sendingarnar eru fluttar inn (3).
**Semantic decision:** F — Transhipment and the entry border-inspection-post/consignment relation are corrupted.
**Candidate 0:** Fella ber inn í samninginn framkvæmdarákvörðun framkvæmdastjórnarinnar 2011/215/ESB frá 4. apríl 2011 um framkvæmd tilskipunar ráðsins 97/78/EB að því er varðar flutningaflutning á viðfangsjóði fyrir inngöngu afurða til innflutnings í Sambandið eða þriðju landi (3).

</details>

<details><summary>after · fit-greedy · ParIce21:eea:2890153 · F</summary>

**Source:** What is the legal basis for the data source?
**Reference:** Hver er lagagrundvöllurinn fyrir gagnaheimildinni?
**Semantic decision:** F — Data source becomes data summary/aggregation, changing the requested legal-basis object.
**Candidate 0:** Hver er lagaleg grundvöllur fyrir gagnasamantektina?

</details>

<details><summary>before · fit-greedy · ParIce21:eea:1150937 · F</summary>

**Source:** Commission Implementing Decision 2011/215/EU of 4 April 2011 implementing Council Directive 97/78/EC as regards transhipment at the border inspection post of introduction of consignments of products intended for import into the Union or for third countries (3) is to be incorporated into the Agreement.
**Reference:** Fella ber inn í samninginn framkvæmdarákvörðun framkvæmdastjórnarinnar 2011/215/ESB frá 4. apríl 2011 um framkvæmd tilskipunar ráðsins 97/78/EB að því er varðar umfermingu afurðasendinga, sem eru ætlaðar til innflutnings til Sambandsins eða þriðju landa, á skoðunarstöð á landamærum þar sem sendingarnar eru fluttar inn (3).
**Semantic decision:** F — Border inspection post and transhipment are replaced by malformed transport/skin-station wording.
**Candidate 0:** Fella ber inn í samninginn framkvæmdarákvörðun framkvæmdastjórnarinnar 2011/215/ESB frá 4. apríl 2011 um framkvæmd tilskipunar ráðsins 97/78/EB að því er varðar flutninga á viðfangshúðstöðvar fyrir inngangur afurða til innflutnings í Sambandið eða þriðju landi (3).

</details>

<details><summary>before · fit-greedy · ParIce21:eea:3205170 · F</summary>

**Source:** The creative and artistic work of authors and performers necessitates an adequate income as a basis for further cre- ative and artistic work, and the investments required par- ticularly for the production of phonograms and films are especially high and risky.
**Reference:** Til þess að höfundar og listflytjendur geti unnið áfram að skapandi og listrænu starfi er nauðsynlegt að tryggja þeim nægilegar tekjur af skapandi og listrænu framlagi sínu; einnig er nauðsynleg fjárfesting, einkum vegna framleiðslu hljóðrita og kvikmynda, mjög mikil og áhættusöm.
**Semantic decision:** F — Creative/artistic work becomes women's studies/scanning, and authors/performers and media are corrupted.
**Candidate 0:** Kvennafræði og skönnunarverk af skrifu- og sjónauðsins þurfa til fullnægjandi laun til að vera grundvöllur fyrir frekari kvennafræði og skönnunarefni og fjárhagsinu sem þurfi sérstaklega í tengslum við framleiðslu hljóðmyndanna og myndasjónauðsins er sérstaklega mikil og hættulegt.

</details>

<details><summary>after · fit-greedy · ParIce21:tatoeba:7662 · P</summary>

**Source:** If you wish to take, you must first learn to give.
**Reference:** Ef þú vilt taka, verðurðu fyrst að læra að gefa.
**Semantic decision:** P — Exact source/hypothesis reuse from inspected fit card2: Preserves learning to give first as a condition for taking.
**Candidate 0:** Ef þú vilt taka þá verður fyrst að læra að gefa.

</details>

<details><summary>before · fit-greedy · ParIce21:eso:821 · F</summary>

**Source:** In Messier 18 the blue and white colours of the stellar population indicate that the clusters stars are very young, probably only around 30 million years old. Being siblings means that any differences between the stars will only be due to their masses, and not their distance from Earth or the composition of the material they formed from.
**Reference:** Í Messier 18 benda bláu og hvítu litir stjarnanna til þess að þyrpingin sé mjög ung, líklega aðeins í kringum 30 milljón ára. Stjörnurnar eru systur svo eini munurinn á þeim er kominn til af massa þeirra en ekki fjarlægð frá jörðinni eða samsetningu efnisins sem myndaði þær.
**Semantic decision:** F — Being siblings becomes being a representative; the common-origin premise is not retained.
**Candidate 0:** Í Messier 18 birta blá og hvítt lit stjörnuþyrpingarinnar til kynna að stjörnurnar í þeim eru mjög ungir, hugsanlega bara um 30 milljón ára gamall. Að vera fulltrúi ber til að allar munurar milli stjarnaðsins séu aðeins af massamagnið og ekki af fjarlægð frá Jörðinni eða samsetningu efnið sem þau mynduðu úr.

</details>

<details><summary>after · fit-greedy · ParIce21:ema:391314 · F</summary>

**Source:** Vaccination should be postponed during any illness with fever >38.5°C.
**Reference:** Fresta skal bólusetningu við öll veikindi með hita > 38,5°C.
**Semantic decision:** F — Any febrile illness is narrowed to infection, changing the vaccination-delay condition.
**Candidate 0:** Fresta skal bólusetningu meðan á sýkingi með hita > 38,5°C stendur.

</details>

<details><summary>after · fit-greedy · ParIce21:ema:185234 · F</summary>

**Source:** In GEICAM 9805 study, alopecia persisted into the follow-up period (median follow-up time of 10 years and 5 months) and was observed to be ongoing in 49 patients (9.2 %) in TAC arm and 35 patients (6.7 %) in FAC arm.
**Reference:** Í GEICAM 9805 rannsókninni var hármissir viðvarandi eftir að eftirfylgnitímabilið hófst (miðgildi eftirfylgni var 10 ár og 5 mánuðir) og var enn til staðar hjá 49 sjúklingum (9,2%) í TAC hópnum og 35 sjúklingum (6,7%) í FAC hópnum.
**Semantic decision:** F — Alopecia becomes a blood/skull term; the adverse-event identity is wrong.
**Candidate 0:** Í GEICAM 9805 rannsókninni var blóðkúpu áfram í eftirfylgni (miðgildi eftirfylgnitíma var 10 ár og 5 mánuðir) og var það viðhaldið hjá 49 sjúklingum (9,2%) í TAC hópnum og 35 sjúklingum (6,7%) í FAC hópnum.

</details>

<details><summary>after · fit-greedy · ParIce21:ema:377570 · P</summary>

**Source:** Thyrogen should not be used during breast-feeding.
**Reference:** Ekki skal nota Thyrogen við brjóstagjöf.
**Semantic decision:** P — Correctly prohibits Thyrogen during breast-feeding.
**Candidate 0:** Ekki skal nota Thyrogen meðan á brjóstagjöf stendur.

</details>

<details><summary>before · fit-greedy · OpenSubtitles18:1029178 · F</summary>

**Source:** She'd smile at me. She was so sweet, but you could see it in her eyes.
**Reference:** Hún brosti til mín. Var svo indæl en maður sá það í augum hennar.
**Semantic decision:** F — Smile becomes an unrelated degree/cry-like verb rather than the specified smiling action.
**Candidate 0:** Hún myndi gráða á mig. Hún var svo sæt, en þú gætir séð það í augunum hennar.

</details>

<details><summary>after · fit-greedy · ParIce21:eea:3227721 · P</summary>

**Source:** The ‘Red Tractor Farm Assurance Combinable Crops & Sugar Beet Scheme’ was submitted on 4 April 2012 to the Commission with the request for recognition.
**Reference:** Áætlunin um „Red Tractor Farm Assurance Combinable Crops & Sugar Beet Scheme“ var lögð fram til fram- kvæmdastjórnarinnar 4. apríl 2012 ásamt beiðni um viðurkenningu.
**Semantic decision:** P — Preserves the named scheme, date, Commission recipient and recognition request.
**Candidate 0:** „Red Tractor Farm Assurance Combinable Crops & Sugar Beet Scheme“ var lögð fram til framkvæmdastjórnarinnar 4. apríl 2012 með beiðni um viðurkenningu.

</details>

# 0.8B Archive and First 3B Round

Date:2026-11-17. The user authorized the3B transition through official Colab. Preserve all0.8B models in place without deleting or overwriting them.

## Conclusions and strength of evidence

| Question | Finding | Scope |
| --- | --- | --- |
| Why no reliable DAPO gain? | Both weak candidates and reward misranking are observed;no reward-only causal control. | Prioritizing candidate ability is a working judgement,not a proven attribution ranking. |
| Candidate ability | Only3/24 technical groups contain an observedG candidate;none of10 long groups do;coverage did not improve after technical SFT. | Fixed small AI-reviewed diagnostic atT=.7,max320;not a population rate or RL-impossibility proof. |
| Reward | MetricX misranks semantics;T6 selectedSFT picksG in all3 covered groups yet has63/247 discordant tier-comparable pairs. | Small sample;neither global calibration nor global failure established. |
| Implementation | R5 corrects earlier precision/logp mismatch;30 steps still show no reliable chrF++/BLEU gain. | R5 chrF++ change−1.367,95%CI[−3.742,+.862]Use the later matchedFP32 result,not the earlier mixed-precision number. |
| Absolute SFT ceiling? | Not established;rank16 at both LRs exactly fits32 pairs. | Memorization does not establish broad-task capacity. |
| Guaranteed by more SFT? | No;development chrF++ falls35.41→26.20/24.64 with semantic deterioration. | Tiny-set overfitting does not prove the earlier broad run was overfit. |
| Why switch? | A resource decision to seek a reliable base sooner. | Not evidence that3B is already better. |

### Unresolved budget and variance factors

R5 has only30 continuous updates,one seed and128 diagnostic-development cases. Its chrF++ change CI spans−3.742 to+0.862. This establishes no reliable gain,not algorithmic ineffectiveness or a uniquely dominant candidate-capacity cause. RL update budget,learning rate and related settings are not causally separated.

## Available 0.8B checkpoints

Inventory reads real files and SHA256s;aliases remain at original paths. All entries are LoRA adapters,not standalone full models.

Explicitly load the pinned base then attach the adapter. Exact resume additionally requires matching optimizer,RNG,order and configuration.

| Role | Path | SHA256 | Bytes | State files |
| --- | --- | --- | --- | --- |
| SFT400_FINAL_UNSELECTED;do not replace selected SFT200 | D:\deep learning project\runs\r0_technical_sft_2026-11-17\final_trained_adapter | 32dd7931c828d3c5ae069391cb7a4411acb70d8a93c670a1864276b375a2df52 | 43346432 |  |
| SFT200_SELECTED_TECHNICAL_COMPARATOR;coverage goal failed | D:\deep learning project\runs\r0_technical_sft_2026-11-17\selected_candidate_adapter | 89c874b1e04b011c6ee3f41f499c373b47826a7f106b9d61eaa83fdce85c77ae | 43346432 |  |
| PRIMARY_08B_FROZEN_COMPARATOR;not validated broad DAPO base | D:\deep learning project\runs\r0_v3_colab_2026-11-13\nll_adapter | ebb4575fda36002c76ddb7e999a4e12c44a0be9ddb20b1e4e092d708e6a050e9 | 43346432 |  |
| LOCAL_OLD_SFT_COMPARATOR;different evaluation distribution | D:\deep learning project\runs\sft_round1\best | e32ae12d4ece8416352a6920d422766a5cf00e7b29ae5a528efda4dc4645a411 | 43346432 |  |

Full machine-readable inventory accompanies this report.

<details><summary>All checkpoint paths</summary>

| Role | Path | SHA256 | State files |
| --- | --- | --- | --- |
| ENGINEERING_SMOKE_ONLY | D:\deep learning project\runs\grpo_smoke\checkpoint-1 | 19a56c31a064723af4f2d6462c95538218dff695afdd2615b82e9df4414675ce | D:\deep learning project\runs\grpo_smoke\checkpoint-1\training_state.pt |
| ENGINEERING_SMOKE_ONLY | D:\deep learning project\runs\grpo_smoke\checkpoint-2 | 67ad1558c1a932db9a3b583457b9f50ddd8a3e77074ba1a46aae787d496cd531 | D:\deep learning project\runs\grpo_smoke\checkpoint-2\training_state.pt |
| ENGINEERING_SMOKE_ONLY | D:\deep learning project\runs\grpo_smoke\last | 67ad1558c1a932db9a3b583457b9f50ddd8a3e77074ba1a46aae787d496cd531 | D:\deep learning project\runs\grpo_smoke\last\training_state.pt |
| TINY_SET_FIT_PROBE;not a stronger R0 | D:\deep learning project\runs\r0_cause_diagnosis_2026-11-17\snapshots\A_lowLR\files\adapter | 0005c04ac9c5cab85466aab6e13fea82020550443bf447aeb972c97c4c0d3576 | D:\deep learning project\runs\r0_cause_diagnosis_2026-11-17\snapshots\A_lowLR\files\metadata.json; D:\deep learning project\runs\r0_cause_diagnosis_2026-11-17\snapshots\A_lowLR\files\optimizer_rng.pt |
| TINY_SET_FIT_PROBE;not a stronger R0 | D:\deep learning project\runs\r0_cause_diagnosis_2026-11-17\snapshots\B_highLR\files\adapter | bc3e92e8b33068101a4443af0f66fc44653d3ddb88e3a8cea8faf85f970c2e92 | D:\deep learning project\runs\r0_cause_diagnosis_2026-11-17\snapshots\B_highLR\files\metadata.json; D:\deep learning project\runs\r0_cause_diagnosis_2026-11-17\snapshots\B_highLR\files\optimizer_rng.pt |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_colab_2026-11-11\best_adapter | 81b369a5f6c6343c160c99c4d3271f2ecb63781363b05e9c89e7b2703b77785f |  |
| SFT400_FINAL_UNSELECTED;do not replace selected SFT200 | D:\deep learning project\runs\r0_technical_sft_2026-11-17\final_trained_adapter | 32dd7931c828d3c5ae069391cb7a4411acb70d8a93c670a1864276b375a2df52 |  |
| SFT200_SELECTED_TECHNICAL_COMPARATOR;coverage goal failed | D:\deep learning project\runs\r0_technical_sft_2026-11-17\selected_candidate_adapter | 89c874b1e04b011c6ee3f41f499c373b47826a7f106b9d61eaa83fdce85c77ae |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_technical_sft_2026-11-17\snapshots\t000000\files\adapter | ebb4575fda36002c76ddb7e999a4e12c44a0be9ddb20b1e4e092d708e6a050e9 | D:\deep learning project\runs\r0_technical_sft_2026-11-17\snapshots\t000000\files\checkpoint.json; D:\deep learning project\runs\r0_technical_sft_2026-11-17\snapshots\t000000\files\optimizer_rng.pt; D:\deep learning project\runs\r0_technical_sft_2026-11-17\snapshots\t000000\files\state.json |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_technical_sft_2026-11-17\snapshots\t100000\files\adapter | 1d13157c3ea63fc6bf62085369bb9fc20d741f30f9d038fb946ee2a303d995a8 | D:\deep learning project\runs\r0_technical_sft_2026-11-17\snapshots\t100000\files\checkpoint.json; D:\deep learning project\runs\r0_technical_sft_2026-11-17\snapshots\t100000\files\optimizer_rng.pt; D:\deep learning project\runs\r0_technical_sft_2026-11-17\snapshots\t100000\files\state.json |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_technical_sft_2026-11-17\snapshots\t200000\files\adapter | 89c874b1e04b011c6ee3f41f499c373b47826a7f106b9d61eaa83fdce85c77ae | D:\deep learning project\runs\r0_technical_sft_2026-11-17\snapshots\t200000\files\checkpoint.json; D:\deep learning project\runs\r0_technical_sft_2026-11-17\snapshots\t200000\files\optimizer_rng.pt; D:\deep learning project\runs\r0_technical_sft_2026-11-17\snapshots\t200000\files\state.json |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_technical_sft_2026-11-17\snapshots\t400000\files\adapter | 32dd7931c828d3c5ae069391cb7a4411acb70d8a93c670a1864276b375a2df52 | D:\deep learning project\runs\r0_technical_sft_2026-11-17\snapshots\t400000\files\checkpoint.json; D:\deep learning project\runs\r0_technical_sft_2026-11-17\snapshots\t400000\files\optimizer_rng.pt; D:\deep learning project\runs\r0_technical_sft_2026-11-17\snapshots\t400000\files\state.json |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v2_colab_2026-11-12\best_adapter | 806b9857024868131140da43ad3975d7c8653b97e5687420e4499a3769995847 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\best_adapter | 0f075c31d0bee3192f2b449a59b7ba6ca3f9370ad219b1c6a98fcf00a01660df |  |
| PRIMARY_08B_FROZEN_COMPARATOR;not validated broad DAPO base | D:\deep learning project\runs\r0_v3_colab_2026-11-13\nll_adapter | ebb4575fda36002c76ddb7e999a4e12c44a0be9ddb20b1e4e092d708e6a050e9 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-000000-tokens-000000000\adapter | 806b9857024868131140da43ad3975d7c8653b97e5687420e4499a3769995847 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-000110-tokens-000072484\adapter | 7e92768e4a4a7034de690215fc8dd3c80a7a2464677d7f17cd6c5cb718e07665 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-000219-tokens-000144823\adapter | 06915a921e3d118c25c27fdf513cd9b708b539287911bb651d45a2d1c2e622d5 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-000302-tokens-000200507\adapter | 41446b607d9ce0118903006516d76f311bb36699c9f13d0e2f96278b11663b9f |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-000412-tokens-000273437\adapter | 976393363875665f0623caba113ff6fea79c26c5b8229a1366466f40ce1a7859 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-000521-tokens-000346749\adapter | a2e44f3798b344d23d59dbc68b33078cd6270142590ff80e4556f1eca0b1538a |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-000601-tokens-000400263\adapter | 483b3ef1e3e054e0b5c665a7d9ed5a4eee54a7ac1cd5852dc4e01e1ccdcdeecc |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-000821-tokens-000545534\adapter | 60345e7073eb4b4ce1f03efcb86750ba63ab3ea2745e2d6c020f9862d382a137 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-000903-tokens-000600408\adapter | 0f075c31d0bee3192f2b449a59b7ba6ca3f9370ad219b1c6a98fcf00a01660df |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-001012-tokens-000673695\adapter | 424466bdc774fee1f586ad1b238184dd61aa44f7665c0a4c0385dadc116e507a |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-001122-tokens-000745982\adapter | 7818d509239d386a928cc8d13cb06e0130a6ad87dec92791235a22cfc0fd1bf1 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-001203-tokens-000800159\adapter | 68a153ed3aee1f9a75eb23eadaaa6aed150a6b79604a8f14c38a1aee5e689f29 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-001313-tokens-000873419\adapter | 56d9186a6babf919370ac9f4347c629f65afe26eabb67521fafc4077225e3934 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-001423-tokens-000946533\adapter | 57c6895e40201adaaed1944eaf960ba6556f2dd8d1aec36f35e0c6a627c9526b |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-001504-tokens-001000225\adapter | 1e8c44a85d42b75046736725cde05431630fdff9de683beaccf67c2e0e3d28ac |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-001613-tokens-001072986\adapter | d8c947b6b27c62fc40ea21e3a799f75015a5cf058cf96084d927f6477525482d |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-001724-tokens-001145520\adapter | 6869953e49cf6c3446f4077d18d9e2ce6be4da3b0a20218121d2039cd6746386 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-001916-tokens-001274051\adapter | 7a953520689a0d69c141757289f2c901d5881852a7540d3ae314c3e77c40d758 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-002026-tokens-001347448\adapter | 3d3139d96b73f664a8cd17d0523a0eacc002740620696cb8de260eab1dd8ddac |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\r0_v3_colab_2026-11-13\recovery\checkpoints\step-002106-tokens-001400474\adapter | ebb4575fda36002c76ddb7e999a4e12c44a0be9ddb20b1e4e092d708e6a050e9 |  |
| ENGINEERING_SMOKE_ONLY | D:\deep learning project\runs\sft_preflight\best | c21ee508882c37a44ff60b28084f3ca2a8ce0377297deb01d738cf140b2c5778 |  |
| ENGINEERING_SMOKE_ONLY | D:\deep learning project\runs\sft_preflight\checkpoint-10 | c21ee508882c37a44ff60b28084f3ca2a8ce0377297deb01d738cf140b2c5778 |  |
| ENGINEERING_SMOKE_ONLY | D:\deep learning project\runs\sft_preflight\checkpoint-16 | d228e96c458e5e2aebfee59c0bcf27c3106813398d0089f9c53937bf910b5160 |  |
| ENGINEERING_SMOKE_ONLY | D:\deep learning project\runs\sft_preflight\checkpoint-20 | c2dc0ac2fe09bc4dac4c1e15e9bbd6ca51f6825f4175b1a9432185b7bea260f5 |  |
| ENGINEERING_SMOKE_ONLY | D:\deep learning project\runs\sft_preflight\checkpoint-8 | 33a60864a3669c04e3ac9ced4768a185cf0514f5ebe76d291cb95202606256cd |  |
| ENGINEERING_SMOKE_ONLY | D:\deep learning project\runs\sft_preflight\last | c2dc0ac2fe09bc4dac4c1e15e9bbd6ca51f6825f4175b1a9432185b7bea260f5 |  |
| ENGINEERING_SMOKE_ONLY | D:\deep learning project\runs\sft_resumecheck\checkpoint-20 | c2dc0ac2fe09bc4dac4c1e15e9bbd6ca51f6825f4175b1a9432185b7bea260f5 |  |
| ENGINEERING_SMOKE_ONLY | D:\deep learning project\runs\sft_resumecheck\last | c2dc0ac2fe09bc4dac4c1e15e9bbd6ca51f6825f4175b1a9432185b7bea260f5 |  |
| LOCAL_OLD_SFT_COMPARATOR;different evaluation distribution | D:\deep learning project\runs\sft_round1\best | e32ae12d4ece8416352a6920d422766a5cf00e7b29ae5a528efda4dc4645a411 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\sft_round1\checkpoint-100 | a67f9c04b9e419e702f1b3b9459434e341309ce6df4ef16bb9c1f1ef0ae4ab10 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\sft_round1\checkpoint-125 | 413229407644befdcfd3a96da87a3d6f1c0230cd7fd33ae711db84c3673cea2f |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\sft_round1\checkpoint-150 | 57d143058b7d177016372aa41cb69635d79479af286c5b3be70ff9426a7608b0 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\sft_round1\checkpoint-200 | 5e3f8d2109b42210ceb29d640afab15dc0a515abcf82dd2f210950d33e72dfb6 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\sft_round1\checkpoint-250 | e32ae12d4ece8416352a6920d422766a5cf00e7b29ae5a528efda4dc4645a411 |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\sft_round1\checkpoint-50 | b4ea4efbe14aa0d82bc87d71e57d43933059562eb0db5f32b1a34606b6d141eb |  |
| historical_or_recovery;not automatically selected | D:\deep learning project\runs\sft_round1\last | e32ae12d4ece8416352a6920d422766a5cf00e7b29ae5a528efda4dc4645a411 |  |
| DAPO_EXPERIMENTAL;no reliable quality gain established | D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\attempt_B\snapshots\step_010\files\adapter | d17f36d72a820bfd6751d369f31bd5feb957edc3f687704abfc7b0b1eaa9afa9 | D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\attempt_B\snapshots\step_010\files\checkpoint.json; D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\attempt_B\snapshots\step_010\files\optimizer_rng.pt; D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\attempt_B\snapshots\step_010\files\state.json |
| DAPO_EXPERIMENTAL;no reliable quality gain established | D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\attempt_B\snapshots\step_020\files\adapter | 6459550315c99393d8cbc82894431deaf457fe960cc5d730c81230cb61565052 | D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\attempt_B\snapshots\step_020\files\checkpoint.json; D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\attempt_B\snapshots\step_020\files\optimizer_rng.pt; D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\attempt_B\snapshots\step_020\files\state.json |
| DAPO_EXPERIMENTAL;no reliable quality gain established | D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\attempt_B\snapshots\step_030\files\adapter | 6c47a6b5ea2f074b922df77ef27b0b536f3df6b838dab3d879f1b94eb0366683 | D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\attempt_B\snapshots\step_030\files\checkpoint.json; D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\attempt_B\snapshots\step_030\files\optimizer_rng.pt; D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\attempt_B\snapshots\step_030\files\state.json |
| DAPO_EXPERIMENTAL;no reliable quality gain established | D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\snapshots\step_010\files\adapter | d17f36d72a820bfd6751d369f31bd5feb957edc3f687704abfc7b0b1eaa9afa9 | D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\snapshots\step_010\files\checkpoint.json; D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\snapshots\step_010\files\optimizer_rng.pt; D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\snapshots\step_010\files\state.json |
| DAPO_EXPERIMENTAL;no reliable quality gain established | D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\snapshots\step_020\files\adapter | 6459550315c99393d8cbc82894431deaf457fe960cc5d730c81230cb61565052 | D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\snapshots\step_020\files\checkpoint.json; D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\snapshots\step_020\files\optimizer_rng.pt; D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\snapshots\step_020\files\state.json |
| DAPO_EXPERIMENTAL;no reliable quality gain established | D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\snapshots\step_030\files\adapter | 6c47a6b5ea2f074b922df77ef27b0b536f3df6b838dab3d879f1b94eb0366683 | D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\snapshots\step_030\files\checkpoint.json; D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\snapshots\step_030\files\optimizer_rng.pt; D:\deep learning project\experiments\dapo_fp32_control_2026-11-16\snapshots\step_030\files\state.json |

</details>

## 3B starting point and scope

Choose the public3.09B instruction model,pinned above. Its model card does not establish Icelandic translation quality. [Official model card](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct)

Scale,generation,pretraining and tokenizer all change;this is a practical baseline transition,not a parameter-only ablation.

Use native BF16 frozen-base LoRA with the stated fixed recipe;never truncate targets silently.

Re-encode the protected T6 candidate pool with the3B tokenizer;mix by actual target tokens and cap pair exposure at2. The dataset is heuristically filtered and sampled AI-reviewed,not fully human-certified.

Record unadapted3B outputs and fixed development checkpoints;then evaluate128 diagnostic-development cases and32 G8 sources. Reused data are not untouched test. MetricX does not select SFT checkpoints.

Readiness requires semantic and candidate evidence with general retention,not a tiny metric uptick;reward ranking remains a separate pre-DAPO check.

## Three-hour budget

| Stage | Estimate | Deliverable |
| --- | --- | --- |
| Setup | 20–35min | Frozen inputs and baseline |
| SFT / Training | 60–100min | Checkpoints/full states |
| Evaluation/export | 30–45min | Predictions,metrics,candidates,durable archive |
| Review/report | 15–25min | Bilingual result and promotion decision |

Target three hours onL4,subject to measured throughput. Reserve at least35min for evaluation/export;report any partial budget honestly. Finishing a run is not baseline qualification.

Cap allocation at180min and training at100min,no automatic extension. Estimated4–6CU,settled account difference governs.

## Prior evidence

| Evidence | Path |
| --- | --- |
| T6 | D:\deep learning project\reports\r0_technical_sft_2026-11-17\TECHNICAL_SFT_RESULTS_2026-11-17.html |
| T7 | D:\deep learning project\reports\r0_cause_diagnosis_2026-11-17\R0_CAUSE_DIAGNOSIS_RESULTS_2026-11-17.html |
| R5 | D:\deep learning project\reports\dapo_fp32_control_2026-11-16\R5_FP32_DAPO_RESULTS_2026-11-16.html |

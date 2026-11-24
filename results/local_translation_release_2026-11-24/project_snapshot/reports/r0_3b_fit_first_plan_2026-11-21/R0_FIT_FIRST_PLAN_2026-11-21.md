# Verify fit, then targeted SFT

2026-11-21 · Europe/Berlin · PROPOSAL ONLY

## Decision

Prioritize SFT trainability and correct-candidate coverage on technical medium/long sources. Pause further DAPO. Reward verification is a separate prerequisite for returning to RL. Preserve both endpoints and start any production SFT from P15, before DAPO.

## Evidence and limits

| Evidence | Observed | Interpretation |
| --- | --- | --- |
| P15 known-seen training audit | 7/16 correct before and after; long0/4 | Observed failure to recover some seen meanings; not a tiny-set overfit test or proof of capacity ceiling |
| P16 R0 sampling audit | 6/16 groups contain a confirmed correct candidate; technical medium/long2/8 | Candidate coverage is a concrete bottleneck on this panel |
| P16 matched128 evaluation | chrF++44.007→41.837; BLEU17.943→16.921 | Reject this pilot as an upgrade |
| Reward top1 audit | 5/16 confirmed correct at each endpoint; strict wrong preference in1 good group per endpoint | Reward errors coexist with coverage limitations; counts do not identify the causal contribution to regression |

Semantic labels are conditional same-assistant judgments with uncertainty, not native-Icelandic certification. The7/16 result does not prove inability to learn: examples generally had only1–2 exposures. The previous coverage phase inherited optimizer state and decayed LR from1e-5 toward5e-6. Repeating that configuration unchanged is not the proposed action.

## Gate1: tiny-set fit

Select64 real training-side parallel pairs,32 medium and32 long, inspecting every reference for key meaning. Do not insert test errors or their paraphrases. Replace uncertain references. Freeze32 in-training audit items,16 per length stratum.

Use a disposable P15 copy, repeated tiny-set exposure, up to0.25M target tokens and45 minutes of actual training, about45–60 minutes including load/checks. Same tokenizer/prompt, target-only loss and rank16 all-linear LoRA; fresh AdamW with fixed peak LR3e-5; dropout disabled for the fit probe. Check masks/EOS, trainable parameters, gradients and real parameter change.

Predeclared engineering gate: at least26/32 preserve key meaning, including12/16 long items, assessed by free generation, not teacher-forced loss alone. Passing demonstrates tiny-set fit, not R0 quality. Failure stops scale-up and triggers inspection of the failing SFT configuration/data component; no automatic longer run, rank search or RL.

Deliberately fitting a tiny dataset is a training-debugging method. This project's sample counts and thresholds are budget-constrained engineering choices, not published universal DAPO standards.[Official Lightning debugging guidance](https://api.lightning.ai/docs/pytorch/stable/debug/debugging_intermediate) / Deliberate tiny-set fitting is a debugging technique. Our sample sizes and thresholds are project choices, not universal DAPO requirements.

## Gate2: bounded targeted SFT

Start only after Gate1. Reload original P15 and discard the fit-probe adapter. Aim for10k–20k pairs, approximately1M unique target tokens and roughly two exposures, capped at2M targets. Availability/quality must be verified first. Target-token mixture:40% technical medium,40% technical long,20% general/technical-short replay.

Reuse the filtered pool with additional checks for omissions, negation, argument roles, numbers, technical terms and template duplication. MetricX alone does not certify references. Exclude overlapping train/development/final sources using exposure records and document IDs where available; disclose missing document IDs. If enough unexposed validation sources cannot be established, stop at data preparation.

One production configuration: existing rank16 LoRA, same base, no quantization; BF16 frozen base plus FP32 LoRA; fresh AdamW, peak3e-5,3% warmup, cosine to3e-6, gradclip1, dropout0.05; global valid-target-token loss and approximately4096 target tokens/update; no silent truncation. This is a declared setting, not a claim of optimal LR.

Cheap development check at0.5M; fixed greedy/G8 semantic check at1M. If neither correct-candidate coverage nor key semantic errors improve, do not extend to2M. Loss decrease alone cannot unlock continuation. Inspect clear general regression and stop on sustained regression. One round only, at most2M targets and4 hours including in-training development checks.

## R0 acceptance and reward

Select one checkpoint on separated development data, seal weights, then evaluate a new final panel once:128 greedy sources and64 technical G8 groups(short16/medium24/long24). Match FP32 inference, prompt, G8/T0.7 and EOS. Final sources do not tune LR/data/checkpoints; the old128-source anchor is not a new confirmation set.

Retain the previous project criteria: at least39/64 groups with a confirmed correct candidate; at least12/24 medium,12/24 long and8/16 short; general chrF++ loss no worse than1.5 and no broad new key-meaning regression. Report greedy semantics, mixed-quality groups, uncertainty and paired intervals. Promote only with substantial candidate improvement and consistent final semantics; otherwise retain original R0. These are project acceptance criteria, not DAPO theory.

Do not retrain MetricX or search reward mixtures. Build64 fixed good/bad comparisons on independent training-side sources, split by source into calibration/verification. Lock current MetricX and plain chrF++ as two diagnostic candidates before scoring, with references/labels checked first. Require at least90% correct critical negation/number/role rankings and80% overall on verification, disclosing small-sample uncertainty. chrF++ may also fail; it is not assumed superior and cannot be the sole evaluator when used as reward.

Schedule a separate1.5–2 hour DAPO pilot only if both R0 acceptance and reward verification pass. No RL if either fails. Passing SFT does not automatically fix the reward.

## Time, preservation and stopping

| Stage | Expected | Bound |
| --- | --- | --- |
| Data/reference QA and unexposed splits | 45–60min | Complete before GPU allocation; insufficient data stops preparation |
| Colab setup + tiny fit | 45–60min | Failure stops scale-up |
| Targeted SFT including dev | 3–4h | Up to2M targets; no-benefit stop at1M; timing cap wins |
| Final evaluation + reward check | 60–90min | Frozen checkpoint; no tuning on final panel |
| Verified export + reports | 30–45min | Reserve before training; original deadline never resets |

With ready data, expect6–8 hours total: up to1 hour preparation and at most7 hours allocated Colab time. Reserve the final2 hours for evaluation, reward verification and persistence. Reduce training tokens if time is insufficient; do not skip verification or lower criteria. Previous SFT processed about2.1M targets in2.16 hours; budget more slowly for long sources. First10 minutes measure throughput only and freeze a feasible token cap.

A failed fit probe should end the attempt in about1–2 hours. Eight hours is a spending cap, not a promise of a strong R0. Save configuration/data hashes/exposure/candidates/labels/full optimizer-RNG checkpoints and bilingual MD/HTML under dated D-drive directories. All model work stays on Colab; no local models, foreground-browser or power changes.

Evidence files: D:/deep learning project/experiments/r0_3b_coverage_sft_2026-11-20/training_fit_review/summary.json ; D:/deep learning project/experiments/r0_3b_coverage_sft_2026-11-20/training_fit_reference_spotcheck.json ; D:/deep learning project/reports/dapo_p15_3b_pilot_2026-11-21/DAPO_P15_3B_RESULTS_2026-11-21.html

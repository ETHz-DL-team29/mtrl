# Filtered-data SFT execution record

2026-11-19 · Updated UTC: 2026-11-19T13:37:06.381194+00:00

This is a running record, not a completed-results report. Only observed optimizer updates are reported as facts; final translation quality, correct-candidate coverage and DAPO suitability remain pending.

## Objective and preserved baseline

Continue supervised fine-tuning the existing A adapter of general-purpose Qwen2.5-3B-Instruct, targeting unseen technical medium/long translation and G=8 correct-candidate coverage while preserving general translation. Original A is unchanged; this phase performs no DAPO or MetricX calls.

Original A: D:\deep learning project\runs\r0_3b_overnight_2026-11-18\final_selected_adapter

A weights SHA256: 9acc23c9595ac0b771bf8f21d125d18f3e993c3f449775377262e7ab73020199

## Verified progress and budget

| Item | Value |
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

Subsequent user constraint: computer off by18:00 and resume after20:00. A17:00 freeze/full backup is scheduled, followed by owned-GPU release only after verification. The21:41 entry above is the original continuous-allocation deadline. Any evening allocation must use only the remaining cumulative8h budget after subtracting actual segment1 usage; the released pause is not GPU time. No20:00 allocation is automatic.

Pause/resume plan: D:\deep learning project\experiments\r0_3b_filtered_sft_2026-11-19\USER_PAUSE_AND_RESUME_2026-11-19.md

The first100 updates locked3M new target tokens from conservative measured throughput, remaining evaluation time and a0.8 safety factor, without using quality scores. Counts include EOS and exclude prompt/padding; whole-example boundaries may leave a small shortfall.

## Data and training recipe

| Item | Value |
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

Use the GPU-filtered parallel corpus pool, including ParIce sources; this is not an all-WMT training set. Exposure order interleaves strata by cumulative target-token deficit. At most2 visits per pair; the3M prefix has about67.4k distinct sources.

## Preflight verification

All100k pairs were retokenized and input/target lengths verified before training, after correcting older prompt-length metadata affected by the chat-template return type. Three meaningful CPU math tests passed. GPU checks confirmed the exact A weights, zero explicit-shift loss difference, finite gradients and a nonzero first-update parameter delta.

First-update evidence: {"parameter_L2_delta": 0.006688808290085558, "finite": true, "grad_norm": 4.554614543914795}

The frozen protocol retains several false draft flags from its ancestor proposal. They do not describe the current execution. Current authorization, data freeze, CPU readiness and real GPU updates are recorded in a dated execution ledger; the checkpoint-bound protocol hash is not rewritten after updates begin.

## Development, checkpoints and final evaluation

Development has128 sources,32 per stratum. Greedy/NLL are checked every500k targets; a fixed24-source technical G=8 set at1M intervals and the endpoint. Selection uses reviewed development checkpoints with general-regression safeguards. The256-source final greedy test and64-source technical G=8 are generated only after weights are sealed and never select the model.

These are fixed subsets of historical official holdouts, not a never-evaluated new benchmark. Source-based labels are P=key meaning correct, F=clear error, U=uncertain. A G=8 group is covered after confirming at least one P; F requires inspecting all distinct candidates. Checkpoint names are hidden during same-assistant review, without claiming external native certification.

| A development baseline | Value |
| --- | --- |
| Overall chrF++ | 36.32325711068724 |
| Technical chrF++ | 36.59669402064523 |
| Technical medium/long chrF++ | 36.61265000576855 |
| Target NLL | 1.5703537802019245 |

These scores identify the starting point on this fixed development set. Do not directly compare them with historical50/44 scores on different samples; they do not yet establish an improvement.

## Persistence, interruptions and cost

Every100 updates or250k targets, save the adapter, Adam state, RNG, data cursor and protocol hashes. D-drive mirrors verify every chunk and whole archive. Input upload resumed from20/27 chunks in the same runtime and passed the final hash. Mirror repairs affected only the local downloader; the training worker and original8h deadline were preserved.

An independent aftercare helper touches only this phase-owned runtime: verify two final exports, run the pre-frozen historical16-source panel if the original budget allows, then release GPU. A separate hard8h guard remains. The final report requires actual predictions and semantic review; lower training loss or successful export is not a translation-quality qualification.

## Artifact index

| Content | Location |
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

# Segment1 results and safe pause

2026-11-19 · Verified UTC: 2026-11-19T16:41:37.336472+00:00

Full pause backup and GPU release completed at17:07 CET. It is safe to shut down the computer. A fresh read-only query confirms zero assigned runtimes and zero hourly consumption. Primary/secondary archives, adapter, optimizer/RNG and committed history were reverified successfully.

## Committed progress

| Item | Value |
| --- | --- |
| Recoverable updates | 1753 |
| Recoverable new target tokens | 2116552 |
| Frozen target | 3000000 |
| Remaining target tokens | 883448 |
| GPU allocated wall time segment1, seconds | 12395.729388237 |
| Remaining cumulative8h GPU budget, seconds | 16404.270611763 |
| Observed paid-compute-unit balance drop | 6.577003469176191 |
| Original A preserved | True |

At the17:00 freeze the worker had advanced beyond the latest full checkpoint. Recoverable progress is step1753 and2,116,552 target tokens. The later82 unsaved updates are not counted as committed progress; untouched raw logs are retained and those updates can be repeated after resume.

## Matched fixed-development results

| Targets | Overall chrF++ | Technical chrF++ | Technical medium/long chrF++ | General chrF++ | Target NLL |
| --- | --- | --- | --- | --- | --- |
| 0 | 36.32 | 36.60 | 36.61 | 32.50 | 1.5704 |
| 500990 | 40.68 | 41.09 | 40.98 | 35.26 | 1.3695 |
| 1001129 | 43.64 | 43.80 | 44.14 | 41.10 | 1.2719 |
| 1501089 | 45.56 | 46.08 | 46.26 | 38.68 | 1.2159 |
| 2000188 | 45.77 | 46.36 | 46.66 | 37.98 | 1.1808 |

| Stratum | Original A chrF++ | 2M checkpoint chrF++ | Delta |
| --- | --- | --- | --- |
| general | 32.50 | 37.98 | +5.49 |
| technical_short | 36.50 | 44.17 | +7.67 |
| technical_medium | 33.98 | 42.11 | +8.13 |
| technical_long | 37.76 | 48.68 | +10.92 |

Overall chrF++ rises from36.32 to45.77 and technical medium/long from36.61 to46.66; all four strata exceed original A. General translation was higher at1M and later receded, so the latest checkpoint is not automatically the best overall choice. These quality scores belong to the evaluated2,000,188-token checkpoint, not the unevaluated2,116,552-token recovery state.

These are metric changes on a fixed128-source development set, not independent final-test results or DAPO qualification. A/1M/2M G=8 predictions are generated and preserved, but source-based P/F/U semantic review remains pending. Reference similarity does not replace correct-candidate coverage. Final weights are not selected/sealed and final-test predictions have not been generated.

The development set contains32 sources per stratum; this report adds no significance claim. The results are positive evidence for learned generalizable patterns, without establishing broad cross-domain reliability. Lower training loss alone is not treated as quality evidence.

## Evening continuation

After the user returns after20:00 and requests continuation, obtain an available native-BF16 GPU, preferablyL4, restore the adapter/optimizer/RNG/cursor and original order, and continue the remaining883,448 targets. Do not restart from A, reset the LR schedule or increase the3M target. GPU availability is not guaranteed.

Resume requires an explicit budget amendment: segment1 allocated about3.44h, leaving about4.56h of total GPU allowance. Offline time after release consumes no allocation. The old continuous21:41 deadline does not directly apply to segment2; compute a new deadline from the remaining cumulative8h allowance without mutating the segment1 protocol hash. Restore all development-candidate adapters so earlier checkpoints remain selectable.

Next: complete development semantic review; continue to the frozen budget or registered stopping rule; select and seal one checkpoint using development evidence only; then generate matched-precision independent before/after tests and G=8, complete semantic/statistical analysis, and distinguish R0 readiness from reward-calibration readiness. No DAPO is launched in this phase.

## Recovery artifacts and audit trail

| Content | Path |
| --- | --- |
| Resume handoff | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\resume_handoff.json |
| Fresh release and integrity verification | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\pause_verified_status_2026-11-19.json |
| Primary archive | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\snapshots\user_pause_20261119_1700\archive.zip |
| Second verified archive | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\pause_export_verified_copy.zip |
| Full recovery files | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\snapshots\user_pause_20261119_1700\files |
| Historical full checkpoints | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\snapshots |
| Raw pause-time logs | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\snapshots\user_pause_20261119_1700\files\raw_run_at_pause |
| Exact committed history | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\snapshots\user_pause_20261119_1700\files\run\updates.jsonl |
| Fixed development predictions | D:\deep learning project\runs\r0_3b_filtered_sft_2026-11-19\snapshots\user_pause_20261119_1700\files\run\evaluation |
| Pause and budget plan | D:\deep learning project\experiments\r0_3b_filtered_sft_2026-11-19\USER_PAUSE_AND_RESUME_2026-11-19.md |
| Original execution report | D:\deep learning project\reports\r0_3b_filtered_sft_2026-11-19\R0_3B_FILTERED_SFT_RUNNING_2026-11-19.html |
| Execution source/tools | D:\deep learning project\experiments\r0_3b_filtered_sft_2026-11-19\execution_tools |

Pause archive SHA256: 770edc12cf34ddf4300ddb701ada927da2d93469899741383ee5b71377307977

Recovery adapter SHA256: ab39d1612c5e69b5aca10a1f180e6f4e7bec7d23b3ca3d09f8f0e5d069e052b0

Optimizer/RNG SHA256: 7bbabeddeff3704dc30ff375c53e9b06481295bcbb61835f647967f0731c475c

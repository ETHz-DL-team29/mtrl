# Full-state continuation execution record

2026-11-20 · Updated UTC: 2026-11-20T11:27:24.457310+00:00

User authorization: continue with a4h ceiling, extending only if useful improvement remains. This file records observations, not a completed-quality claim. Original A, the2M development candidate and the2.116M recovery state remain separate and preserved.

## State and budget

| Item | Value |
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

The absolute wall deadline covers today preparation, upload, environment recovery, training, development selection, final evaluation and export, with a conservative5minute initial-preparation allowance. Today is at most4h and both segments remain within8h cumulative GPU allocation; reconnections do not reset timing. The final75min are reserved for evaluation/export.

## Continuation contracts and implementation amendments

Both prior archives, adapter, optimizer/RNG,1753 committed updates and2,116,552 targets were reverified. Data/order/target-only loss/original protocol/LoRA/Adam/RNG/LR progress remain continuous. The82 previously uncommitted updates are repeated from the saved state; raw logs are preserved without counting them as committed.

The new absolute deadline replaces the old continuous deadline through an explicit segment2 amendment. The packaged old allocation budget is retained. Before launch the new budget is bound to its own SHA; the execution source manifest removes only the superseded budget entry, while every code/data/weight hash remains verified. The original protocol is unchanged. A failed control-channel handshake was recovered through a fresh channel on the same L4 without another allocation.

Source amendment diff: D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\resume_code_amendment.diff

Independent budget-manifest proof: D:\deep learning project\experiments\r0_3b_filtered_sft_resume_2026-11-20\control_evidence\allocation_manifest_amendment.json

All3 CPU math tests passed from the correct source directory. An initial wrong-directory launch caused an import collection error before training and is recorded. The new GPU environment also checks these contracts before resumed updates.

## Locked development semantic review

| Model | Confirmed G8 covered/24 | G8 uncertain/24 | Greedy correct/32 | Greedy uncertain/32 |
| --- | --- | --- | --- | --- |
| A | 2 | 5 | 4 | 5 |
| t1001129 | 4 | 5 | 6 | 6 |
| t2000188 | 6 | 8 | 9 | 6 |

All168 development cards were reviewed and locked with checkpoint names hidden. P means key meaning correct and untruncated; G8 F requires inspecting all distinct candidates; U remains uncertain and is neither credited as P nor represented as proven failure. Confirmed technical coverage2→4→6 is relative progress, not broad reliability.

Review is by the same AI assistant, not external native-speaker certification or perfect context-blind adjudication. These24 development sources do not replace the64-source final technical G8 test after weight sealing.

## Conditional extension to3.5M

First complete the original3M target. Add a single500k tail only after3M semantic review, nondecreasing confirmed coverage and greedy P versus the previous semantic checkpoint, technical chrF gain≥0.5, general chrF≥originalA−1.5, and sufficient conservative remaining time. Keep Adam/cursor and the original floor LR1e−5, without warmup reset or stretching the already executed cosine schedule.

If the gate fails, select the best eligible reviewed development checkpoint and evaluate it without forcing training to fill4h. Selection remains confirmed coverage first; within1 covered source, break ties by greedy semantic P,technical medium/long chrF and earlier checkpoint. Final tests never select weights.

## Matched3B and0.8B comparison

After selection is sealed, generate fixed256-source greedy and64-source G8 for oldA and selected3B. If the original deadline permits, evaluate the pre-fixed historical0.8B selected200k technical continuation with identical sources/instruction,nativeBF16,greedy batch8 and G8 sampling. If only greedy fits, mark missing G8 explicitly. This compares practical checkpoints, not a matched-exposure size ablation.

The80-source final greedy semantic sample was hash-frozen before any final outputs. Report final metrics,stratum deltas,paired bootstrap and source-based G8 audit separately. A historical50 and this phase45.77 on different sets are not directly comparable.

## Persistence and artifact index

| Content | Location |
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

New full-state checkpoints are mirrored to D with per-chunk and archive SHA verification. Final export needs two verified copies; release only this owned runtime after supplemental GPU work. A separate hard-deadline guard remains. Export or lower loss does not establish R0 qualification before semantic/final reporting is complete.

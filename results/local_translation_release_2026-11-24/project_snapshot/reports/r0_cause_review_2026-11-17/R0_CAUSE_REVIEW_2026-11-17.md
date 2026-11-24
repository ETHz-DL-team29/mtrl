# R0 causal review: capacity ceiling not established

Date:2026-11-17. Review of completed technical SFT and paired evaluation records only; no new GPU allocation or training.

The observed failure belongs to this continuation recipe and semantic-coverage objective. It does not establish a 0.8B SFT ceiling, nor uniquely prove insufficient training tokens.

## Established facts

| Fact | Implication |
| --- | --- |
| Frozen base; rank16 LoRA;10,822,656 trainable parameters | This is a constrained adaptation configuration, not a full-capacity ceiling test |
| 399,895 target tokens;10,539 unique pairs;selected model at200,770 tokens | Most pairs appeared once within this continuation; earlier training exposure may exist |
| LR1e-5→1e-6;one training seed;one configuration | Conservative continuation was tested without learning-rate, adapter-capacity or data-scaling controls. |
| 372 adapter tensors changed;finite gradients;technical NLL1.73553→1.70585 | Weights updated and supervised prediction changed; this is not proof of adequate optimization or bug-free training. |
| Selected technical coverage3→3/24;long0→0/10 | Complete-candidate coverage did not expand on this fixed diagnostic subset |
| SFT uses target-token cross entropy;selection uses chrF++/NLL and retention guards | MetricX is auxiliary and cannot cause this SFT learning shortfall |

## Interpretation to correct

This was a conservative strengthening experiment, not a capacity-limit experiment. Falling teacher-forced NLL can coexist with poor free generation; that motivates a training-fit/generalization diagnosis, not a unique causal conclusion.

The recorded final400k checkpoint performs worse than selected200k on the final128. This does not establish that every larger SFT run fails. The general-retention guard alone does not prove technical overfitting.

## Minimal discriminating diagnosis — proposed, not executed

Fix quality-reviewed pairs actually seen by the selected checkpoint. Compare original/selected per-pair NLL,greedy translation and semantic retention across strata. Report held-out results separately; training fit is not generalization.

| Result | Diagnostic implication |
| --- | --- |
| Training examples translate poorly too | Audit loss alignment, prompting/tokenization and optimization, then test fitting a small clean subset. |
| Changing LR or adapter capacity enables fitting | The original optimization/adaptation recipe was limiting; this does not establish a universal0.8B ceiling. |
| Training examples fit;held-out examples fail | Prioritize coverage,alignment quality and generalization |
| Multiple audited configurations still fail on a clean small subset | Then investigate representation/pretraining/adapter restrictions; this alone still does not prove a universal0.8B ceiling. |

Memorizing a small subset does not establish target generalization, and one LoRA setup failing does not establish insufficient base-model capacity.

## Evidence

Full completed results: D:/deep learning project/reports/r0_technical_sft_2026-11-17/TECHNICAL_SFT_RESULTS_2026-11-17.html

Protocol: D:/deep learning project/runs/r0_technical_sft_2026-11-17/exported/protocol.json

Structured results: D:/deep learning project/runs/r0_technical_sft_2026-11-17/analysis/results.json

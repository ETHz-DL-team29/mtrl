# Bounded 3B R0 SFT Continuation and Tonight’s Launch Guide

Date: 2026-11-17. Code, data and notebook are prepared locally; no continuation GPU allocation or new 3B training has been executed.

**Continue the saved Qwen2.5-3B weights without fresh LoRA,model replacement or DAPO. Test whether another bounded SFT stage improves correct candidate availability;qualification is not guaranteed.**

For tonight, use [Colab notebook](../../experiments/r0_3b_continue_2026-11-17/R0_3B_CONTINUE_2026-11-17.ipynb) and the [companion code/data bundle]Use the matching notebook and bundle linked here.

## Why continue SFT

Selection-development scores keep improving without an observed plateau. Historical SFT exposure differs,so the result does not establish a capacity ceiling;continued improvement also does not guarantee qualification.

| Round1 measure | Observed |
| --- | --- |
| Actual targets | 999931 |
| Dev64 weighted chrF++ | 36.476431290709485 |
| Dev64 general chrF++ | 35.54763100658314 |
| Dev64 technical-long chrF++ | 38.29559574729537 |
| Separate diagnostic128 chrF++ | 34.457398965701834 |
| Old0.8B SFT200 same128 | 36.03694982273706 |
| Technical G8 groups with G | 2/24;old SFT2003/24 |
| Long G8 groups with G | 0/10 in both |

These two scores use different data/aggregation. Preserve the original report as history;this document records the subsequent bounded-continuation decision.

## Exact parent and preservation

| Item | Value |
| --- | --- |
| Base | Qwen/Qwen2.5-3B-Instruct |
| Base revision | aa8e72537993ba99e69dfaafa59ed015b17504d1 |
| Parent adapter | D:\deep learning project\runs\r0_3b_round1_2026-11-17\selected_candidate_adapter |
| Parent SHA256 | 1ecf014712c7eb0004eaa20de58f54b0346cc4bd67b0ce07e3c7e30084e6c41f |
| Parent step / targets | 926 /999931 |
| New local experiment | D:\deep learning project\experiments\r0_3b_continue_2026-11-17 |
| New local result destination | D:\deep learning project\runs\r0_3b_continue_2026-11-17 |
| Drive destination | MyDrive/deep learning project/r0_3b_continue_2026-11-17/ |

Weight continuation uses a fresh stage optimizer,not exact round1 optimizer resume. Preserve all earlier files;new full states include optimizer,RNG,cursor,plateau state and identities.

## Frozen data and budget

The medium bucket supplies223758 targets under the exposure cap. Use a nominal900k stage,actual898707,instead of increasing repetition to force1M. Cumulative 3B targets would be1898638;this is not an exposure-matched cross-model ablation.

| Stratum | Target tokens | Share | First-use pairs relative to round1 | First-use target tokens |
| --- | --- | --- | --- | --- |
| general | 359998 | 40.06% | 10211 | 183152 |
| technical_short | 44999 | 5.01% | 0 | 0 |
| technical_medium | 223758 | 24.90% | 0 | 0 |
| technical_long | 269952 | 30.04% | 686 | 127113 |

| Data item | Value |
| --- | --- |
| Eligible pool | 38640 |
| Selected unique pairs | 25381 |
| Example exposures | 26677 |
| Additional target tokens | 898707 |
| Max exposures this stage | 2 |
| Max cumulative exposures | 3 |
| Known semantic exclusions | {'known_semantic_quarantine': 31} |
| Candidate-pool SHA256 | 13393429c1234556cd7b5d6561408964fc39d44b33bffdd670503377ed9761b4 |

This is not a newly collected corpus. First-use examples are mainly10211 general and686 technical-long pairs;short/medium are repeats from the protected pool. The cumulative cap covers this3B SFT chain,not pretraining or0.8B history.

Retain filtering/quarantine,check exact normalized protected sources/references,and encode with the same tokenizer without truncation. This is not full native or document-level certification.

## Training recipe

| Parameter | Value |
| --- | --- |
| GPU | L4 recommended;native BF16 required;A100 also possible |
| Precision | Frozen BF16 base + FP32 adapter;final evaluation FP32/TF32off |
| Trainable modules | Existing rank16/alpha32 LoRA:q/k/v/o/gate/up/down |
| Dropout / AdamW weight decay / clip | .05 / .01 /1 |
| Stage peak LR / final LR | 5e-5 /1e-5 |
| Schedule | 2% warmup,cosine to20% of peak |
| Effective batch / microbatch | 32 /4,OOM retry to2/1 |
| Seed | 2026111741 |
| Planned evaluation targets | 0,250000,500000,750000,stage end≈898707 |
| Additional target cap | 900000 |
| Training-loop wall cap | 100min,including in-loop development/backup |
| Overall worker budget | 180min from first code cell;reserve40min before ending updates |

Lower peak LR is a conservative stage choice,not a demonstrated optimum. LR/order/exposure changes prevent attributing every difference solely to more tokens. Preserve the existing adapter structure and base.

## Automatic stopping and selection

Recompute parent outputs on the current GPU;the baseline is the trained parent,not the original raw3B.

Enforce general retention and failure guards. Stop after two checkpoints without an eligible≥0.3 weighted gain. This heuristic is not significance testing;choose the best eligible checkpoint with the registered tie-breaks and parent fallback.

Record failures/partials honestly;wall limits can reduce completed targets.

## Acceptance and DAPO

Generate the fixed128 and32 G8 banks. Automatic output is numeric preview only;semantic judgement and reward validation remain separate.

Judge core semantics,candidate availability and general retention. Earlier12/24 and4/10 targets remain project heuristics,not universal RL thresholds;smaller gains may justify a restricted pilot rather than broad qualification.

If plateau plus poor candidates persists,stop further automatic SFT and revisit starting-point fit. Validate a new untouched quality holdout and reward before bounded standard DAPO and later efficiency comparisons.

## Tonight’s steps

| Step | Action | Check |
| --- | --- | --- |
| 1 | Upload the notebook in Edge. | Do not launch the old round1 replay. |
| 2 | Select L4 and connect. | T4 is blocked. |
| 3 | Run all and authorize Drive. | Verify the output path. |
| 4 | Upload the companion bundle. | Parent/hash verification passes. |
| 5 | Wait for setup/tests. | Expect8 checks;do not bypass errors. |
| 6 | Launch the foreground worker once. | Generate the parent baseline first, then confirm Drive_checkpoint_verified t000000 before starting updates. |
| 7 | Verified export then flush/release. | No automatic R0 acceptance. |
| 8 | Download both to D: and import. | Preserve old runs. |

Confirm initial and first periodic backups before leaving. No MCP is required;an open browser does not guarantee runtime continuity.

## Time and compute estimate

| Stage | L4 estimate |
| --- | --- |
| Authorization/upload/install/download | 15–30min,including user interaction |
| Parent baseline and initial dev | 10–20min |
| SFT updates for898707 targets | About74min at previous203 targets/s |
| In-loop dev/Drive backups | 15–30min,included in100min loop cap |
| Final greedy/G8/export/flush | 15–30min |
| Normal end-to-end target | About2.5–3h;180min worker budget,not a success guarantee |
| Estimated CU | About4.5–6 based on the previous observed round;actual Colab consumption applies |

Healthy execution ends automatically after verified backup/Drive flush. Failed backup/authorization can require manual shutdown;the worker budget is not a platform-enforced billing cap. [Official runtime API](https://github.com/googlecolab/colabtools/blob/main/google/colab/runtime.py), [official Drive API](https://github.com/googlecolab/colabtools/blob/main/google/colab/drive.py).

## Backups,interruptions and D: import

Periodic and stage archives contain full states and verified hashes. Final export contains all outputs,selected adapter and last full state;other stages stay in Drive checkpoint archives.

Do not silently restart after interruption. Full states are saved,but automatic resume is not implemented in this launch notebook.

Colab cannot directly write local D:. Use Drive then explicit Save as to D:.

Save both files to: `D:/deep learning project/runs/r0_3b_continue_2026-11-17/night_download/`

Then in PowerShell run: `& "C:/Users/andre/AppData/Local/Programs/Python/Python313/python.exe" "D:/deep learning project/experiments/r0_3b_continue_2026-11-17/import_results.py"`

The standard-library importer checks hashes,safe paths and no-overwrite;it creates a numeric preview without allocating a GPU or certifying semantics.

## Verification and deliverables

Completed local CPU and syntax checks do not constitute an end-to-end GPU or live Drive test.

| File | Purpose |
| --- | --- |
| R0_3B_CONTINUE_2026-11-17.ipynb | User launch notebook |
| continuation_bundle.zip | 115.5 MiB;matching code/data/parent adapter |
| protocol.json / data_summary.json | Frozen parameters and actual exposure data |
| source/source_manifest.json | Every frozen file hash |
| import_results.py | CPU-only safe local import |
| PREPARED_NOT_STARTED.txt | Explicit not-started status |

Bundle SHA256: `49a7bb0f1508504161e7201242fac3bb3e4755441730fb4c6a8dcac3ba90f7d1`Preparation preserves round1 results in their original locations.

<details><summary>Frozen source SHA256 inventory</summary>

| File | SHA256 |
| --- | --- |
| b3_core.py | 7f9e7d40094d0e2f54a1f9d10c01923396fa8003119266acc6e7ea4747c42365 |
| b3_setup_worker.py | c619f14600634816c7cef5693b2bcf9075d6a7c51d0b331973dfde71041c9145 |
| b3_store.py | 95465eee6eb17e2ce58e02b817b9f9321ed4e28a9751dea260e9c4da1d64618d |
| b3_train.py | 6bafa4d35007be0db6055855ed6167b8a19d7444aac3c35ea18d51572747fd12 |
| b3_update.py | c9bb9ddb7f85901839f3a5f42b8534b7112c8e091bbd7c47b301b9ecd7089e8d |
| b3_worker.py | 063ed350739b273e64e7f967b84c26f67a56007567b289f00a0d2756756c6b7b |
| c3_rules.py | 89236a9896b8c26cb730258d25449670d9cfb1a28ef8a14a6bcfa9b057d10828 |
| data/decode_dev.jsonl | 643265919dadeaded9c37b2af74730158961f2f06373a41dd74536f32a5e4c4c |
| data/dev.jsonl | 505627c0de101bbfb86d4f90aaa83be58e4d3f50311e7d951c6676c09dfc97dd |
| data/encoded_train.json | efd634e0ab07bf4b741dd0a7e88d0553468de400b8732aa0153305ad439aa50b |
| data/evaluation128.jsonl | 082b3ca2d0dceaa3d9ffe635f97c9934fa960f06e005fc8ede47dc80d60c18eb |
| data/evaluation_reference_review.json | a3f2b4d05d6380128a63480ff8f7471fb01c8fad2f832f955126946b2a06bf98 |
| data/exclusions.json | 808b55fdd0430dd20225925e349e45c65a3a918dc3b03dfb22d928e6ff123529 |
| data/exposure_order.json | 89b9fcfd537fb58c74953247ab29814f8497f31c6b204885cf9a552756f120b3 |
| data/g8_32.jsonl | 2c14ef4dffa527199422ea446809e23586958d19c588a3a902ff5104d94d3724 |
| data/length_rejections.json | 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 |
| data/preparation_summary.json | 2a1cd2a7cb77ffc756b06a4a841d9470b8ff3335f7349c6e8d78494c95d9ef5b |
| data/prior_exposure_counts.json | 9f3b2279409b3c05bf1a25f0c1e4a83379d118bc6e738d077afb775236363bb4 |
| data/quality_followup_lock.json | 122a5840083dac4b69aac259b191b2c58cf010df00b00e3852f54c7df9566dce |
| data/quality_review_lock.json | 5e67fa088a37a4b00a723ff842494c443e3d18d44f1b27df11e52558ef5e8eb6 |
| data/semantic_quarantine_ids.json | 96d16b50de07f92ba2be3aef17ae1c6f6ca3c8398a8a0a7ee3c88a9427ff1281 |
| data/train.jsonl | ca9ca4158d2fcc99c0735012ae0fe47be2890d32801654369ea84151623b0012 |
| data/training_quality_followup_reviews.json | 12b9c9a28ef96cbd91632230207afc37c925c4975571f4d48767fe23d56ecdbe |
| data/training_quality_reviews.json | e88f0d7ad46c2fc0fcad46dfcfb2c44677471c9e6a792ce10daaac2f421e4aee |
| mtgrpo/__init__.py | d841cefd0c317a840959ee520b7313acbb38e620c9844b22221cd6af2bd4b55d |
| mtgrpo/common.py | 5a8a0593f0d177010ee07a8591a6d563fe69d77a7dd71a980a2f53c79b7840f4 |
| mtgrpo/data.py | 6a008a7cc60064e236f9f8151d397471c77308f64e728427ea39f220b92b1302 |
| mtgrpo/models.py | 2e1df0d7a3bc5f1c7067e475256d5fc4473f4dc9595ba5eb530c9cb8824e62fe |
| mtgrpo/r0_core.py | 38399a0793e3f37305d85e0cc84ce94b24254cffeadae1ba75b738b0d97debee |
| mtgrpo/r0_train.py | 368815f1a7a83b4e9924bb33cb542768965d0803c2704a0823e6692804594cf4 |
| mtgrpo/r1_core.py | 1d66ba906f9e508682b1185ccd8185ccd283d4e963eada13e5083f3751026d39 |
| mtgrpo/sft_data.py | c7d40916075abda196a854a300e4d548ebd55dc3b16bfacdb74c1c4c89480329 |
| mtgrpo/telemetry.py | 398c39f80579c68bdba3745a2d3e1f1d2a6d6286f783885c83a2ed8081a6a3a3 |
| protocol.json | 36d341e499a8c24b60ed66b53d03d4e5e5a8912a8e22c674d8195efaa62dab90 |
| requirements-colab.txt | f3f3f47580d7a37d5899fa5b102b86c354c12d5a8b69f082c69eb6d0901c8889 |
| tests/test_b3.py | f24ebf012a6106cb6fa972b0b9cdb4ba2303a80f3a587410df6c7a35c89c21c6 |
| tests/test_continuation.py | 7532e8bb475ec4e5140eed3464b73777f518f00d27c1e665ba2603d3352eeae6 |
| warmstart_adapter/adapter_config.json | a7653e861a5aabe2bac359cb28a6318d2884ab96f4aa4e9470ff1df89cb23b4e |
| warmstart_adapter/adapter_model.safetensors | 1ecf014712c7eb0004eaa20de58f54b0346cc4bd67b0ce07e3c7e30084e6c41f |

</details>

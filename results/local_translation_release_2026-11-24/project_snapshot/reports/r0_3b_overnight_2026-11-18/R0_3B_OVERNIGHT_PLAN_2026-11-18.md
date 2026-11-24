# Adaptive continuation within eight GPU hours

Date: 2026-11-18 (Europe/Berlin). This is the execution plan. Consult execution_status and the RESULTS report for actual completion and observed values; planned outcomes are not presented as results.

## Objective and existing evidence

The objective is a more reliable English-to-Icelandic SFT starting policy, especially for technical medium/long sentences, while retaining general translation. Eight hours is a cumulative GPU allocation ceiling, not a requirement to spend it all or a promised score.

The previous 3B checkpoint scored34.46 chrF++ on128 reused diagnostic sources versus36.04 for the older0.8B SFT200; the paired interval crossed zero. Only2/24 technical G=8 groups, and0/10 long groups, contained a clearly good candidate. These observations identify an actor coverage gap, not a model-capacity ceiling or proof that SFT explains every DAPO failure.

Reward misranking is separate evidence. Improving SFT does not automatically repair MetricX; actor quality and reward readiness are assessed separately.

## Budget, preservation and control

| Item | Registered arrangement |
| --- | --- |
| Actual GPU | approximately22.0GiB |
| Allocation start | 2026-11-18 00:35:19 Berlin |
| Absolute release deadline | 2026-11-18 08:35:19 Berlin |
| Included | Setup, training, evaluation, review idle time and transfers |
| Persistence | Hashed full optimizer/RNG snapshots to D:, final duplicate verified export |
| Existing models | Older0.8B and first3B preserved |
| Workflow | Same Colab workflow, authorized official CLI control, no Drive mount dependency |

## Stage A: bounded continuation

Continue the trained, nonzero LoRA selected in round1 with a fresh AdamW stage. The stream has898,707 additional target tokens in a40/5/25/30 general/short/medium/long mixture. A pair is used at most twice in this stage and three times cumulatively on this3B chain. LR5e-5,2% warmup, cosine decay to20%.

Evaluate fixed dev64 at0/250k/500k/750k/end. Stop after two checks without an eligible weighted chrF++ gain of at least0.3. Keep the best eligible checkpoint with parent fallback, rather than selecting by the final update or training loss. All128 regenerated parent hypotheses and full token sequences match the saved previous-round outputs exactly.

Generated dev64 comprises32general/8short/12medium/12long cases. A separate fixed144-pair teacher-forced NLL set (64general/24short/28medium/28long;8,649 target tokens) supports NLL diagnostics and tie-breaking; these sets are distinct.

## New data: quality checks before training

Approximately3.22million locally available ParIceFiltered, OpenSubtitles and Tatoeba pairs were scanned. Exact source/reference overlap with the entire prior3B candidate pool and exact/heuristic near overlap with known development/evaluation data were excluded. Language, number, length, encoding, OCR and completeness checks were applied. A64-pair source/reference review found5 clear defects and18 cautions, including omitted clauses, changed drug names, OCR and lost qualifiers; V3 rules were then frozen. V1/V2 and their reviews are preserved.

Current V3 has28,948pairs: general3,608, technical-short3,538, medium15,131 and long6,671. It remains a candidate pool, not universally qualified training data. Once actor A exits completely, use pinned MetricX QE(source,human reference) as auxiliary screening: FP32,batch8, reject rather than truncate inputs beyond1536, error≤4 and at most20minutes. If incomplete, use only the prespecified category-interleaved scored prefix. Then hash-sample32passing pairs for score-blind review; R/U>V3 contains28,948 candidate pairs:3,608 general,3,538 short,15,131 medium and6,671 long. Candidates are not automatically approved training data. After A fully releases actor memory, pinned MetricX QE scores source/human-reference pairs as an auxiliary filter: FP32, batch8, reject inputs over1536 without truncation, error≤4,20-minute cap. A partial run uses only the prespecified proportionally interleaved scored prefix. Then32 accepted pairs are reviewed by fixed hash without numeric scores; more than2 clear/uncertain defects triggers revision or stopping.

Reusing the scorer for data selection and later RL rewards introduces dependence. QE is not semantic certification, so independent reference/source review remains necessary. Heuristic deduplication does not establish document-level independence or pretraining decontamination.

## Stage B and optional follow-up

Review A on fixed32 greedy sources and32×8 samples. If fresh data pass QA, one bounded changed-data stage B may start from the best non-regressing A checkpoint or the original parent. Prefer fresh technical medium/long pairs and general replay within remaining exposure allowances; the provisional ceiling is approximately1.5–1.8million target tokens at around3e-5 LR. Exact scope, parent, data order, LR and stops are hashed before any B outputs; these ranges are not executed values.

General-retention guards remain anchored to the original3B parent across stages to avoid accumulating a1.5-point drop per stage. Stop on plateau or semantic regression. A short additional stage is considered only with continuing gains, qualified data and preserved final evaluation/backup time; no repeated small-pool training merely to fill eight hours.

## Evaluation separation and final judgement

Old dev64 selects checkpoints; reused128 andG8 guide diagnostics and follow-up. A fresh128-source holdout was frozen before any outputs on those sources and reviewed using only source/reference: primary112, with all128 and A-only76 sensitivity analyses. The prior3B pool audit found no heuristic near matches. Generate this new holdout only after sealing the final weight choice; do not use it for model selection or further adaptation.

Compare the selected3B, original3B parent and older0.8B SFT200 under identical sources/references and matched FP32 generation settings. Report chrF++, BLEU, source-stratified paired bootstrap intervals, technical medium/long results, semantic errors and G8 good-candidate coverage. State single-seed, small semantic sample and same-AI-reviewer limitations. Reserve at least approximately75minutes for final fresh-holdout comparisons and backups.

The final conclusion separates (1) whether the actor has useful good-candidate coverage and semantic contrast for a small DAPO pilot, and (2) whether the reward pipeline is reliable. There is no universal chrF++ admission threshold. If the model is still inadequate, report specific failure evidence and the next discriminating action, without promising that more SFT must work.

## Execution amendment before stage B

At02:22UTC, the original error≤4 pool had failed32-pair QA (20A/9C/2R/1U;fixed R+U≤2 gate). The failed records were retained. V4 tightened error to≤3, added archaic-quotation, role and clinical-term rules, and reclassified107 generic star/moon/sun dialogues as general. A disjoint32 review passed the same gate with19A/11C/2U;both U pairs and7 globally found OCR cases were excluded, leaving17,282 approved pairs.

Before any B output, the parent A adapter,3B/rank16,LR3e-5,seed2026111841,fresh AdamW and1,799,948-target stream were frozen:47,241 unique pairs,55,010 exposures,including14,792 fresh pairs. General/short/medium/long target shares are40/5/25/30,with≤2 uses per stage and≤3 cumulatively. All11 CPU checks passed. The original eight-hour ceiling and75-minute final reserve remain. A is a working parent, not a qualified R0: technical G8 coverage4/24 and long0/10.

## Conditional amendment

At B500k,weighted chrF++38.70→38.88 and long40.56→39.17. Metadata show B long targets51.3% legal,28.6% medical,5.5% astronomy,while5/24 reused long cases have astronomy provenance;this is correlational. This amendment supersedes the initial optional-follow-up condition: consider C only after a frozen-rule B plateau stop at≤1.05m,completed review showing insufficient actor coverage,and≥165minutes remaining at launch.

C is not yet executed:cap300k targets,same3B/rank16,LR2e-5,seed2026111842,checks0/150k/300k;general/short/medium/long remain40/5/25/30,with approximately equal four-domain targets within each technical length. Use only the approved V4 pool and vetted general replay,unchanged QA and≤2/≤3 exposure caps. Preserve the best A/B parent and all existing weights. Preparation,training,evaluation,review and backup must fit roughly90minutes,with the same75-minute final reserve and8h ceiling. Skip C if its conditions fail.

## Optional C skipped

Before upweighting rare domains,an additional balanced32 review gave21A9C2R and exposed domain mislabels. After conservative relabelling,a disjoint32 review gave21A7C4R,exceeding the unchanged R+U≤2 gate:star plurality,author identity,comparative incidence and context-resolved references. Skip C rather than relax the gate or repeatedly filter until passing. B data remain frozen;complete its selection/stopping flow,seal the best A/B/original parent,and evaluate independently. Prepared C code is not C training:C GPU updates0.

## Additional fresh G8 measurement

This adds final measurement only:reuse the16 technical IDs (4short/6medium/6long) of the earlier frozen24-source semantic subset and generate16×8 for selected3B,original3B and older0.8B. The112 primary and128/76 sensitivity sets remain. Seal weights before any fresh generation;no later training. Lock72 greedy labels first,then shuffle24 candidates per source with model identities hidden and lock384 labels before aggregation. Identical source/translation pairs keep identical labels;these are not384 independent expert decisions.

The final evaluation source was frozen at04:01UTC with SHA b3d8d39667789939db4c0ac6196d5d6af8388169cf83cfddecb22b9067e99651. The wrapper verifies it and exports both source and identity;the original eight-hour deadline remains.

<details><summary>Frozen parameters and files</summary>

| Parameter | Value |
| --- | --- |
| target_token_budget | 900000 |
| actual_stream_tokens | 898707 |
| mixture | {'general': 0.4, 'technical_short': 0.05, 'technical_medium': 0.25, 'technical_long': 0.3} |
| seed | 2026111741 |
| lr | 5e-05 |
| warmup_fraction | 0.02 |
| final_lr_fraction | 0.2 |
| lora_rank | 16 |
| lora_alpha | 32 |
| lora_dropout | 0.05 |
| weight_decay | 0.01 |
| clip | 1.0 |
| effective_batch | 32 |
| microbatch_start | 4 |
| max_total_tokens | 1024 |
| max_target_tokens | 384 |
| max_pair_exposures | 2 |
| checkpoints | [0, 250000, 500000, 750000, 900000] |
| base_frozen | True |
| precision | native BF16 base+FP32 adapter;matched FP32 final generation |
| max_cumulative_pair_exposures | 3 |
| early_stop | {'patience': 2, 'min_weighted_chrf_gain': 0.3, 'only_eligible_improvements': True} |

| Directory | Purpose |
| --- | --- |
| D:\deep learning project\experiments\r0_3b_overnight_2026-11-18 | Frozen code,data,protocol,QA |
| D:\deep learning project\runs\r0_3b_overnight_2026-11-18 | Actual logs,checkpoints,verified exports |
| D:\deep learning project\reports\r0_3b_overnight_2026-11-18 | Bilingual plan and final results |

</details>

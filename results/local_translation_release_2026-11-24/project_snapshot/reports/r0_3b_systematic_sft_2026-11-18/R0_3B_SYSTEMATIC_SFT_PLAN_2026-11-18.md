# Systematic translation SFT for a capable 3B R0

PLAN ONLY — NOT STARTED

Decision: preserve current 3B A and create a separate continuation branch from it. The origin remains the general-purpose Qwen2.5-3B-Instruct, never a translation specialist or a DAPO checkpoint. This round comprises one larger SFT run and prespecified acceptance; 0.8B is preserved for a later comparison.

The goal is materially better faithful translations and correct-candidate availability on unseen technical sentences while retaining general translation. Lower loss or a small overlap-score gain is insufficient. Improvement is a testable objective, not a guaranteed outcome or quantified probability.

| Fixed | Proposal |
| --- | --- |
| Actor lineage | Qwen2.5-3B-Instruct → prior SFT → A → new systematic SFT |
| Parent adapter | D:\deep learning project\runs\r0_3b_overnight_2026-11-18\final_selected_adapter |
| Parent SHA256 | 9acc23c9595ac0b771bf8f21d125d18f3e993c3f449775377262e7ab73020199 |
| Data goal | 50k–100k distinct filtered parallel pairs, with sampled reference QA; not yet prepared |
| Training exposure | Nominal 3.0M NEW target tokens; timing-locked 2.5/3.0/3.5/4.0M, max 2 passes |
| Compute | Original Colab/Edge + official CLI workflow; prefer L4; at most 8h GPU wall |
| Primary outcome | Semantic P coverage of matched G8 on 64 unseen technical sources |
| Current action | Write proposal and evidence only; no data-build/model call/GPU allocation/training |

<details><summary>Evidence and the hypothesis being tested</summary>

## Evidence and the hypothesis being tested

| Observed | Supports | Does not establish |
| --- | --- | --- |
| 0.8B clean32 fitting: both LRs trainchrF100 and32/32exact; heldout35.41→26.20/24.64 | Repeated tiny-set fitting can memorize without generalizing | Universal0.8B capacity ceiling; all broadSFT already overfit |
| 3B parent999,931targets; A adds898,707; selected A chain≈1,898,638targets | Current A is already meaningfully task-adapted, not a zero-shot model | A has received adequate translation-scale supervision |
| A fresh112 chrF44.17 vs parent41.27, paired+2.90[1.17,4.71] | SFT has produced real gains on that set | Every further SFT will improve; score predicts faithful technical outputs |
| B executed1,000,317targets; selectedB at500,620; candidate gains did not improve confirmed coverage | More similar continuation can fail the semantic objective | Any larger/more diverse dataset is futile |
| P10 primary64 chrF32.004→29.753; BLEU7.271→5.263; originalG8 P3/16 | The tested small DAPO did not establish benefit; technical candidate support is weak | RL is universally ineffective; sole cause is SFT; no3B model can learn the task |

Working hypothesis: A still lacks sufficiently broad, faithful and adequately learned English–Icelandic mappings, particularly technical meanings and longer-range relations. Broader reliable supervision with adequate exposure is a justified engineering attempt, not an identified exclusive cause. Data, exposure and length handling form a recipe; gains cannot be causally assigned to one ingredient here.

Historical44.17 and P10’s new-set33.44 differ in sources,prompt and constructed distribution; they are not a regression of unchanged A. Regenerate A and the new candidate on the same frozen test. This plan’s P means semantically usable, corresponding to historical G, not the older major-defect partial-P label.

</details>

<details><summary>Scope, initialization and excluded work</summary>

## Scope, initialization and excluded work

| Item | Fixed decision |
| --- | --- |
| Task | English→Icelandic, standalone sentence/segment translation; not certified document translation |
| Origin | General-purpose Qwen2.5-3B-Instruct @ aa8e72537993ba99e69dfaafa59ed015b17504d1 |
| Initialization | Load public/local pinned base plus existingA LoRA; preserve nonzero weights; freshAdamW |
| 0.8B | Preserve all prior checkpoints; no second training branch this round |
| Adaptation | Existingrank16,alpha32,seven attention/MLP projection classes; frozenbase |
| Excluded | No DAPO, reward retuning, translation-specialist start, backtranslation, synthetic-teacher distillation, tiny-set refitting, rank search or full-parameter switch in this round |

Continuing A remains downstream specialization from a general-purpose model and preserves verified learning. Failure does not automatically authorize another rank/model/language switch or run; such changes need a new bounded comparison.

</details>

<details><summary>Training data: scale, coverage and provenance</summary>

## Training data: scale, coverage and provenance

Rescan existing ParIce/ParIceFiltered,OpenSubtitles and Tatoeba archives onCPU, targeting50k–100k distinct pairs rather than just the previous sub30k fresh pool. Raw size is not clean-data availability. Require50k eligible distinct pairs before this larger-run launch; otherwise report data-supply failure first.

| Stratum | Target-token share | Intent |
| --- | --- | --- |
| General | 30% | Standalone general statements/questions, retain lexical and sentence translation |
| Technical short | 15% | Terminology in complete sentences, facts/numbers/roles |
| Technical medium | 30% | Conditions, agents/objects, clause relations |
| Technical long | 25% | Complete multi-clause segments without dropping qualifiers |

Register technical length bands using English words:short≤12,medium13–40,long41–120. Ordinary dialogue mentioning stars/galaxies is not automatically scientific. General data also span lengths. Aim for20%–35% of technical target tokens each from medical,legal and astronomy/science,with other technical domains filling the remainder. Record supply-driven deviations before model outputs; do not manufacture quotas by repeating a few pairs or inventing domain labels.

At least70% of planned new target tokens should come from sources absent from A’s actual training lineage; at most30% may be high-quality replay. Novelty is relative to actual A exposure,not universal pretraining novelty. Also record old0.8B/discardedB exposure. Deduplicate first-pass training; only a second broad pass may repeat each selected pair once,without tiny-set oversampling.

WMT supplies task/resource context,not one interchangeable corpus label. The local Tatoeba manifest references aWMT26 recipe entry; ParIce/OpenSubtitles retain their own archive/version/SHA. Verify year,split and prior use before any separate officialWMT benchmark. The constructed256-source test is not an officialWMT score.

</details>

<details><summary>Supervision quality before GPU allocation</summary>

## Supervision quality before GPU allocation

| Check | Treatment |
| --- | --- |
| Alignment/completeness | Reject obvious missing/extra clauses, adjacent-sentence contamination, dialogue fragments requiring unavailable context |
| Entities and numbers | Flag changed names,drug names,dosages,negation,units,dates and roles; distinguish legitimate number spelling/format changes |
| Encoding/OCR | Quarantine broken words,unrecoverable mojibake and OCR; no guessed repairs |
| Language | Use source/target language checks with short-text uncertainty; do not reject technical terminology simply for ASCII spelling |
| Duplicates/conflicts | Deduplicate normalized sources/pairs; quarantine unresolvable conflicting targets; preserve multilingual characters |
| Length | Tokenize with pinned3B tokenizer; reject full examples over limits; never silently truncate target clauses |
| Reference quality | MetricX,if used diagnostically,is auxiliary only; no reward-score-only acceptance of a reference |

Review200 hash-selected pairs:40general,40short,60medium,60long,without model outputs orMetricX scores. Launch requirements:≤4 clear material defects,≤20 uncertain pairs,and≤5% clear defects in each stratum. Allow at most one filter revision plus a disjoint200-pair re-audit; a second failure stops before GPU allocation. Preserve every decision and rule change. Sampling is not full native certification.

AI review can assist,but AI-rewritten references and same-assistant judgements are not independent human gold evaluation. Prefer qualified Icelandic checks of critical technical facts when available; otherwise disclose provenance/uncertainty without inventing expert review.

</details>

<details><summary>Splits, exclusions and a fixed final test</summary>

## Splits, exclusions and a fixed final test

Freeze development/final-test sources before selecting the training stream. Prefer document/provenance groups; otherwise use available metadata and normalized sentence groups with caveats. Exclude actual A training,known historical train/dev/test/reward-control and inspected review sources/references,including heuristic near duplicates. Use5gram retrieval andJaccard≥0.85 with documented retrieval coverage/limitations.

Do not construct novelty by discarding every untrained candidate pool and sampling only its tail; this shifts difficulty/domain. Use prespecified domain×length quotas,not model-score selection. Incomplete history supports only no-known-overlap,not absolute unseen/pretraining-decontaminated claims.

| Use | Size | Rule |
| --- | --- | --- |
| Dev greedy/NLL | 128 =32 per general/short/medium/long | May guide checkpoint selection; independent from training |
| Dev semantic/G8 | 32greedy (8perstratum),24technicalG8sources (8pertechnicalstratum) | Fixed IDs; no changing failure cases into training references |
| Final matched greedy | 256 =64 per stratum | A and ONEdev-selected candidate; inspect once after weight seal |
| Final technicalG8 | 64sources:16short+24medium+24long | Same sources,seeds,T.7,G8 for A/candidate |
| Final greedy semantics | 80sources:20perstratum | BlindA/candidate; selected before any outputs |
| Historical sets | Keep unchanged | Regression context only; no claim that inspected old sets remain fresh |

Source/reference QA precedes outputs; uncertain references enter a separate appendix. Freeze primaryIDs,all exclusions and source/reference hashes before GPU calls. Final outcomes cannot trigger another checkpoint choice on the same test.

</details>

<details><summary>Training recipe and implementation constraints</summary>

## Training recipe and implementation constraints

| Setting | Planned |
| --- | --- |
| Loss | Target-only causal cross entropy,including correctEOS; global valid-target-token mean across accumulated microbatches |
| LoRA | r16/alpha32/dropout.05;q,k,v,o,gate,up,down; existingA values retained |
| Optimizer | FreshAdamW;LR5e-5;betas(.9,.999);eps1e-8;wd.01;clip1 |
| Schedule | 60k target-token warmup; hold peak until timing lock; then cosine to20% of peak at locked final token |
| Batch | Effective32examples;micro4→2→1 only forOOM; preserve effectivebatch via accumulation |
| Length | Prompt≤1024,targetincludingEOS≤512,total≤1536; preserve whole targets |
| Precision | NativeBF16 frozenbase+FP32LoRA training; matchedFP32 final evaluation;TF32off |
| Padding/packing | Dynamicpadding and lengthbucketing;no cross-example packing this round |
| Exposure | First broad pass preferred; max2new passes; no answer-based sample oversampling |
| Seeds | {"data": 2026111891, "split": 2026111892, "train": 2026111893, "sampling": 2026111894, "bootstrap": 2026111895, "blind": 2026111896} |

Reuse the audited trainer and pinned dependencies,not an automatic framework upgrade. Check changed paths for targetmask/EOS,manualCE,padding/accumulation denominators,exact A loading,recovery and length rejection. Do not repeat the0.8B32-pair memorization probe. Log actual trainable parameters,layer gradients,valid targets and update magnitude.

Index the schedule by valid target tokens: warm up linearly through 60k, then start cosine decay at max(60k, tokens seen at timing lock), ending at 20% of the peak. If 100 updates finish before warmup completes, finish warmup first. Retained probe updates need no retrospective schedule change or optimizer restart.

Track32 fixed actual training pairs during the ordinary run,reporting NLL/greedy separately from dev,without extra optimization. This is a low-cost fit trace,not a new memorization experiment or promotion criterion.

</details>

<details><summary>Actual scale and the eight-hour feasibility bound</summary>

## Actual scale and the eight-hour feasibility bound

| Historical record | tokens | trainseconds | targettokens/s |
| --- | --- | --- | --- |
| StageA | 898707 | 4317.0 | 208.2 |
| StageB | 1000317 | 4894.4 | 204.4 |

Historical train segments average204–208targettokens/s under their recorded implementation; this is not a forecast guarantee for the new lengths. At205/s,3M/5M/10Mtargets require roughly4.07/6.78/13.55hours of training alone. Setup,development,finalgeneration and exports are additional. Do not promise5M–10M plus acceptance in8hours.

Nominal NEW exposure is3M,hardmax4Mtargets,about3.3–4.4times A’s0.9M increment—not pretraining-scale training.50k–100k denotes the prepared unique pool; report actual distinct exposures/passfraction separately,never as if the whole pool was consumed.

| Phase | Planning envelope |
| --- | --- |
| Setup/verification | About30minutes; included in overall480-minute cap |
| Training + scheduleddev + intermediate saving | Up to330minutes from firstallocation; less if setup is slow |
| Final dev decision + matched final generation + durable exports | Reserve120minutes; starts no later than allocation+360minutes |
| Total | Hard480minutes from FIRSTGPUallocation; CPUpreparation/postrelease labels/report outsideGPUcap |

These are planning envelopes,not additive permission beyond480minutes. Training ends by first allocation+360minutes. The first100 real updates remain on the trajectory. Lock once to the largest feasible2.5/3/3.5/4M grid using step-throughput25thpercentile,futuredev/save reserves and0.8safetyfactor. Never extend for quality or changeLR afterward. If no grid fits,preservepartialprogress and report infeasibility rather than calling a reduced prefix a complete larger run.

A partial budget follows the frozen interleaved domain/length stream,not an easy-first prefix. Only after completing pass1 may a second seededshuffle begin,with atmost2usesperpair. One complete pass is an objective,not an8-hour guarantee; incomplete execution is explicitly flagged.

Before GPU allocation, count full target tokens for the first 50k distinct pairs in the interleaved stream. If this already exceeds the 4M hard cap, report the mismatch and revise the written budget before allocation. Stop at full-example boundaries; actual tokens may be slightly below the target, never truncate translations to hit a round number.

</details>

<details><summary>Development evaluation, selection and early stopping</summary>

## Development evaluation, selection and early stopping

Every0.5Mvalid targets save a fullstate and evaluate fixeddev128 NLL/greedy. FullG8/semanticdev checkpoints are onlyA zero,approximately1M,2M and the final target. CPU review may run while GPU training continues; final-test outputs remain unread.

Dev eligibility requires general chrF decline≤1.5 from A and no new widespread structural failure. Form a tie set of eligible candidates within one covered source of the maximum technical G8 coverage, then rank by greedy semantic P count, medium/long chrF, and earlier checkpoint. A fixed maximum-based set avoids nontransitive pairwise ties. Identity or scores never justify relabeling U as P.

Two flat0.5Mmetric checks trigger inspection,not an automatic overlap-only stop. Stop for plateau only when the latesttwo completed semanticdev reviews show no coverage/greedysemantic gain and technicalchrF improves<0.5. Missing reviews are not failure evidence; continue only within the fixed cap. General decline>3points or repeated broad semantic/output collapse triggers rollback/stop. Nonfinitevalues,wrongweights or inconsistentrecovery stop immediately.

Seal exactly one selectedweightSHA before final evaluation. Select only revieweddev candidates;fall back to an earlier reviewedcheckpoint orA rather than exhaust exporttime waiting. IfA remainsbest,report no strongerR0 from this run.

</details>

<details><summary>Correct candidates and blinded review</summary>

## Correct candidates and blinded review

P preserves core meaning,roles,numbers,negation,conditions and important clauses,allowing minor nonsemantic grammar/inflection issues. F denotes material mistranslation,omission,addition,inversion or unusableoutput. U is uncertain. Only nonempty,untruncatedP counts as correct. ReportP+U as an uncertainty upperbound,not confirmedaccuracy.

Shuffle matchedA/newG8candidates without model,checkpoint,reward or metricidentity;source and checked reference remain visible. Identical source+hypothesis requires consistent labels; disagreements receive a symmetric U sensitivity analysis rather than favorable relabeling. Lock/hashlabels before unblinding. Count critical semantic error types separately from overlap.

| Quantity | Definition |
| --- | --- |
| Coverage@8 | Fraction of sources with at leastoneP among8; source-level paired comparison |
| Correctcandidate rate | Pcount / all8N candidates; not equivalent to sourcecoverage |
| Mixedgroups | Sources containingP andF;descriptive RLopportunity,not a reason to reject all-correctgroups |
| Greedysemantic usability | Pfraction on fixed80source subset |
| Uncertainty | Ucounts andP+Ucoverageupperbound; AIreview notnativegold |

</details>

<details><summary>Project acceptance: what counts as reaching the goal</summary>

## Project acceptance: what counts as reaching the goal

These are proposed exante projecttargets,not publishedDAPOadmissionrules. They require material semantic progress rather than a1–2pointchrFgain. Freeze them with the exacttest before execution and never lower them after results.

| Acceptance | Target | Interpretation |
| --- | --- | --- |
| Primary technicalCoverage@8 | ≥39/64sources (≥60.9%) | DefiniteP only; short≥8/16,medium≥12/24,long≥12/24 |
| Substantial improvement claim (separate) | At least13/64 additional covered sources net; paired95%coveragegain interval lower>0 | ≥20.3percentagepoint target; not an absolute R0 qualification requirement |
| Greedysemantic usability | Technical≥30/60;general≥14/20 | Coremeaningusable,not perfectnative-style output; smallsampleuncertainty disclosed |
| Overlap/retention guards | GeneralchrFdelta≥−1.5;overall andtechnicaldelta≥0 | Pairedintervals reported; pointguard is not statistical proof of noninferiority |
| Criticalerrors | No broad increase in number/negation/role/condition failures; disclose allcounts | No hiding regressions behind a mean score |
| Integrity | Matchedgeneration,knownleakagechecks,verifiedweights/exports,fullactualexposure | No qualification without auditable artifacts |

Three outcomes:1targetsmet—freeze the next-stage projectR0 withAI/single-seed limitations;2reliablebutinsufficientgain—preserve an improved candidate and list gaps without broad certification;3no material gain/regression—retainA and stop extending thisrecipe. Data/budget infeasibility is incomplete execution,not a demonstrated model capacity failure.

Absolute R0 capability and substantial improvement over A are separate outcomes. Meeting the absolute semantic/coverage targets with retention guards can qualify the project R0 without a13-source gain, but does not support a substantial-gain claim. If matched evidence shows A already meets the absolute targets, acknowledge A as usable rather than demand a large new gain as the definition of reliability. No native-level reliability promise follows without independent semantic review.

Use2000 paired source-stratified bootstrap replicates forcoverage,chrF++ andBLEU.512candidates are not512independent sources. Intervals exclude training seed,document clustering andlabel error;reportU bounds/domain results. One chain does not establish cross-seed stability or leaderboard standing.

</details>

<details><summary>Reward and subsequent SFT/DAPO comparisons</summary>

## Reward and subsequent SFT/DAPO comparisons

R0quality andMetricXcalibration are independent statuses. This SFT does not optimize/select qualification throughMetricX. Preserve failed reward controls; betterR0 does not repair reward. Conversely,significant gains in a30stepDAPO are not the definition of translation capability.

| Later branch | Controls |
| --- | --- |
| R0 zero update | Exact same frozenR0 andtest |
| R0 continuedSFT | Same eligibletrainingsources;supervisedtargets;log tokens/time/memory |
| R0 standardDAPO | SameR0 andsourcepool;fixed validatedreward/sampling;log allgeneration/scoring/update costs |
| Efficiencyvariants | Compare to fixedstandardDAPO,not a differentR0/data/reward;equalGPUtime andqualityversuscost curves |

SFT directly accessesreferences;reference-rewardDAPO accesses supervision differently. Disclose information,data andtotal actual compute rather than equatingupdatecounts. Later formalcomparisons need another sealedfinal evaluation; this round’s inspectedtest becomes historical/development data.

</details>

<details><summary>Colab operation, recovery and accounting</summary>

## Colab operation, recovery and accounting

Keep the Edge/officialColabCLI/D-drive mirroring workflow. CompleteCPU dataQA/tokenization before allocatingGPU. PreferL4;T4 requires measurement and the same wall deadline with potentially lower achievabletokens,not purchasedquota or equalwork promises. Keep one ownedruntime identity to avoid accidentalCPU/GPU switches.

Save recoverablestate every100updates orapproximately0.25Mtargets,whicheverfirst:adapter,AdamW,scheduler,all RNG,epoch/bucket order,cursor andbudget. Mirror at least every0.5M fullstate toD withSHA verification. Send15secondheartbeats and inspect the ownedruntime without repeatedly creatingGPUs.

Verified directD-drive transfers are primary;Drive is optional redundancy,not proof ofcompleted saving. Recovery never resets the first allocationdeadline. Distinguish retainedlogicalupdates from discarded/recomputedphysicalupdates. Verify finaladapter/fullstate on D before release,and account for setup,waits,scoring,recovery andtransfers.

Historical account observations suggest roughly1.8–2CU/h forL4;reserveabout15–18CU forplanning an8h ceiling,not as a current price/quota promise. Read actualGPU,balance andconsumptionrate atlaunch. CPUpreparation andpostrelease semanticreview/reporting take additionaltime;8hGPU is not an8h endtoendreview guarantee.

</details>

<details><summary>Deliverables and reproducibility</summary>

## Deliverables and reproducibility

| Artifact | Content |
| --- | --- |
| Datasetmanifest | ArchiveURL/version/SHA,eligible/rejectedcounts,actualdomain/lengthmix,exactuniques,targettokens,new-to-Afraction |
| QAandexclusions | Every200paircard,labels,filterversions,heldoutchecks,nearduplicateretrievallimits |
| Frozenexecutionprotocol | Finaldatahashes,seeds,prompt,tokenlimits,exacttargetlock/LR,budgetdeadline,allsoftwareversions |
| Trainingrecords | Loss/NLL/gradnorm,tokenexposure,perpairhistory,devchecks,checkpoints,RNG/optimizer/scheduler,bucketorder |
| Blindreview | Cards,hiddenidentitymap,lockedlabels/hash,duplicateconsistency,uncertainupperbounds |
| Finalcomparison | All256pairedgreedy,all64×8×2candidates,semantics,bootstrap,domain/lengthresults,criticalerrors |
| Model | Selectedadapter plus exactbase/hash andloadinstructions;originalA andalloldweights unchanged |
| Cost/report | GPUminutes/CU/peakmemory,logicalvsphysicalwork,datedbilingualMD/HTML,CSV/JSON,CPUreproduction |

This proposal lives underexperiments/r0_3b_systematic_sft_2026-11-18;create the matchingrunsdirectory only for actualexecution. A plan is never an executedexperiment. Newartifacts remainon D;credentials/proxytokens remainprivate and outside deliverybundles.

</details>

<details><summary>Launch order and explicit stop rules</summary>

## Launch order and explicit stop rules

| Step | Action | On failure |
| --- | --- | --- |
| 1CPU | Inventoryhistory;rebuildeligiblepool;review200;freeze splits/trainorder | Supply/QA insufficient→noGPU |
| 2CPU | Pin source/dependencies;targetmask/load/recovery checks;hashinputs | Implementation mismatch→fix beforeGPU |
| 3GPU | OwnedL4;firstallocationdeadline;loadA;baseline/dev;first100realupdates | OOM/throughput infeasible→savepartial,do not promisefullrun |
| 4Lock | Freeze timing-onlytarget andschedulerhorizon once | No feasible2.5Mgrid→incompletefeasibility outcome |
| 5Train | Broad interleavedSFT;scheduleddev/semantics;durable states | Collapse/confirmedplateau/deadline→stop,retainbestdevcandidate |
| 6Seal | ChooseONE revieweddevcandidate;sealSHA beforetest | No candidatebetterthanA→A remainsselected;report honestly |
| 7Evaluate | Generate matchedA/candidate test256 andG8;exportall;releaseGPU | Export cannotverify→prioritize save/release withincap,markincomplete |
| 8CPU | Lockblindlabels,unblind,bootstrap,acceptance/status,bilingualreport | Do not lower thresholds,relabel for outcome,or run anotherSFT automatically |

If targetsremainunmet,the conclusion is failure of this bounded data/scale/rank16recipe—not thatQwen cannottranslate or3Bhititsceiling. Anotherrepeat is not automatically a fix. Any next investment must targetevidence with onechangedfactor,such as adaptationcapacity,and is not silently addedhere.

</details>

<details><summary>Evidence and technical references</summary>

## Evidence and technical references

D:\deep learning project\reports\r0_cause_diagnosis_2026-11-17\R0_CAUSE_DIAGNOSIS_RESULTS_2026-11-17.md · SHA256 e93fccf5c295cc6b78890a65c0ee47bd5a111b4a8213a9478130d014d2ef038a

D:\deep learning project\reports\r0_technical_sft_2026-11-17\TECHNICAL_SFT_RESULTS_2026-11-17.md · SHA256 6309a834be474d8550d2fade06b02b6b306f334157158001c881a955cdf605a6

D:\deep learning project\reports\r0_3b_round1_2026-11-17\R0_3B_ROUND1_RESULTS_2026-11-17.md · SHA256 d318acc84aec0b9953b6c862230f63e8f76c1675f2fc87cac24468659394ca0c

D:\deep learning project\reports\r0_3b_overnight_2026-11-18\R0_3B_OVERNIGHT_RESULTS_2026-11-18.md · SHA256 fd2860c75e0ea09b02225f134733ec10a1f5a6f4a977ce9880fe52cff1bc6a33

D:\deep learning project\runs\r0_3b_overnight_2026-11-18\stage_A\exported\run\summary.json · SHA256 ffd877ff52275a4f5a4f2fb20caf8bee7b4cf74cbc0d5af0006c960e37046401

D:\deep learning project\runs\r0_3b_overnight_2026-11-18\stage_B\exported\run\summary.json · SHA256 d6f0621995b879c3cf3662a12b7565d2f24ec3119897b3eaeba49bf66812d80e

D:\deep learning project\runs\dapo_3b_xl_exploratory_2026-11-18\analysis\results.json · SHA256 c58c5ca721c1515d6feeb78a8a98cc44cdb794ed935d39919b11438e3b223975

D:\deep learning project\data\processed\train.manifest.json · SHA256 acb3afd67879a2c0402ddf6943712694c0705639b48b5d37e7ed24a6bff95b6a

D:\deep learning project\data\raw\r2_2026-11-13\download_manifest.json · SHA256 09ca26f24c1bfaa7b4dc01a9a29c8943ffc87a3b5a0ba217df1d584d1461e55c

[Qwen2.5-3B-Instruct official model card](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct) — General-purpose causal model origin; no claim of certified Icelandic translation quality

[Hugging Face TRL SFT Trainer](https://huggingface.co/docs/trl/en/sft_trainer) — Reference for response-only supervision; existing audited trainer will be reused, not automatically replaced by latest TRL

[Hugging Face PEFT LoRA reference](https://huggingface.co/docs/peft/v0.21.0/package_reference/lora) — Adapter rank,alpha and target-module semantics; no claim that larger rank solves this task

[WMT21 Translation Task](https://www.statmt.org/wmt21/translation-task.html) — English/Icelandic task and supplied training-corpus context; not a claim that all current data are official WMT21 train or test

[ParIce corpus provider](https://parice.arnastofnun.is/) — Source corpus identity, with actual local archive/version hashes recorded separately

References verify method semantics. Scale,LR,budget,mixture andacceptance are projectproposals,not officialrecommendations or provenoptima. Pin executionversions rather than replacing historicalrecords with changingdocumentation.

</details>

<details><summary>Current completion status</summary>

## Current completion status

| Status | Value |
| --- | --- |
| Writtenplan | Completed2026-11-18 |
| ParentAhash | Verified unchanged |
| 50k–100kqualitypool | Notyetprepared |
| Exactexecutiondata/schedule | Notyetfrozen |
| Newtrainerimplementation | Notyetimplemented/validated |
| GPUallocation/training | Notstarted |
| Expectedqualification | Objective only;no successprobability promised |

The next actual work is CPUdatapreparation,supervisionQA and executioncode. GPUlaunch follows only after those pass andfreeze. This document fulfills the requestedwrittenplan;it is not an instructionalreadyreceived tostarttraining.

</details>

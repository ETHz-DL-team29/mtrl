# Fixed-P18 reference-MetricX DAPO experiment record

Date: 2026-11-23 · Europe/Berlin

**Status: data and source prepared; GPU allocation has not succeeded. Reward calibration and DAPO have not run.**

This is a preparation and connection-failure record, not a training-results report. No new checkpoint or new translation/reward-ranking measurements exist.

## Objective and fixed conditions

Use the existing P18 SFT checkpoint of general-purpose Qwen2.5-3B-Instruct to test calibrated DAPO for English→Icelandic technical translation. Preserve the original R0. No new SFT and no translation-specialist replacement model.

The six-hour user wall budget includes preparation, setup, training, evaluation and persistence. Anchor: **10:49:30 CET**; policy-training cutoff **15:19:30 CET**; absolute deadline **16:49:30 CET**. Allocation/reconnection does not reset it. Unexecuted work is not training time.

Original checkpoint:

`D:\deep learning project\runs\r0_3b_recovery_sft_2026-11-21\final_selected_adapter`

Original adapter SHA256:

`7f7a4914c5f403e757fdb882c3576ac68f2b0fa6edc00e537087716b28ddb07e`

The adapter SHA256 was rechecked when inputs were frozen; original files were not overwritten. Base-model revision above, LoRA r64/alpha128.

## Why this round

Historical P21 on the reused 128 sources gave chrF++ about49.401→49.887 with a paired interval spanning zero, and BLEU29.398→29.319. Same-assistant semantic source passes were20/64→23/64 for greedy and10/32→8/32 for technicalG8, with long sources0/12→0/12. This is historical context, not a new measurement or proof of a capacity ceiling/mandatory SFT.

This round enlarges the source pool, audits references, uses separated evaluation sources and validates automatic rewards first. Reference-mode MetricX has already been tried historically; adding a reference is not presented as an unprecedented fix.

## Data provenance and actual sizes

Training sources come from the existing17,911-pair P18 production SFT partition, without WMT test training. Technical subsets are primarily ParIce21.10 EMA/EEA/ESO; general examples include OpenSubtitles18/Tatoeba/TED2020/statistics. The local ParIce21.10 artifact is not synonymous with a WMT26 training set or all officially listed resources.

|Stratum|Sources|Target|
|---|---:|---:|
|General|400|400|
|Technical short|400|400|
|Technical medium|700|700|
|Technical long|499|500|
|Total|1999|2000|

The initial2000 pool becomes1999 after an unreliable replacement reference is excluded. The approximate20/20/35/25 mixture is retained without padding with an unaudited substitute. Pool size is not update count; attempted/used groups, generated tokens and actual GPU time must be reported.

## Reference audit and isolation

246 source/reference cards were individually inspected. A preserves core meaning with minor grammar/phrasing tolerance; R marks clear fidelity/extraction/identifier problems; U marks uncertain semantics or missing context. These are same-assistant judgments, not independent native certification.

Calibration retains27of32 originals and4of5 in one bounded replacement round, giving31 sources:16fit/15validation. Gate thresholds are not relaxed. The13 original stratified training audit examples contain10A/2R/1U;3 replacements contain2A/1R. **Not all1999 training references were individually reviewed; the pool is not certified error-free.**

Examples include all-cause→cardiovascular mortality narrowing, EC/ESB identifier changes, DT90/DT50 mismatch, up-to1000→more-than1000, planet-candidates→confirmed-planets and mentioned-medicines→medicines-other-than-those-mentioned. These establish residual reference risks, not a representative corpus-wide error estimate.

<details><summary>Per-panel reference counts</summary>

```json
{
  "UTC": "2026-11-23T10:12:21.760852+00:00",
  "reviewer": "Same AI assistant,not native certification",
  "definition": "A core source meaning preserved;minor grammar/phrasing tolerated;R clear fidelity/extraction issue;U contextual/semantic uncertainty",
  "audited_cards": 246,
  "by_panel": {
    "calibration": {
      "A": 27,
      "R": 3,
      "U": 2
    },
    "calibration_reserve": {
      "A": 4,
      "R": 1
    },
    "dev": {
      "R": 4,
      "A": 58,
      "U": 2
    },
    "test": {
      "A": 109,
      "U": 6,
      "R": 13
    },
    "test_reserve": {
      "A": 1
    },
    "train_replacement": {
      "A": 2,
      "R": 1
    },
    "train_sample": {
      "A": 10,
      "U": 1,
      "R": 2
    }
  },
  "all_training_refs_individually_reviewed": false,
  "training_audit": "13stratified original examples+3replacement references;bad/uncertain removed",
  "all_selected_evaluation_references_reviewed": true,
  "all_calibration_references_reviewed": true,
  "no_model_outputs_consulted": true
}
```

</details>

The new dev set has48sources(12perstratum), final set96(24perstratum), chosen in predeclared order from accepted references. Greedy semantic review uses64sources; technicalG8 uses24(8each length). These are new project research heldouts, not official WMT26 benchmark scores or proof of pretraining novelty. The earlier proposed64/128 panels shrink to48/96 before any new output due to reference audit.

Exact source/reference protection covers58 historical evaluation files, the100,642 training pool and38,640 historical actual-lineage source hashes. Train/dev/test/calibration pairwise exact intersections and fit/validation source overlap are zero. Word5gram Jaccard≥.85 finds zero matches between all256 reserve candidates and the100,642 training rows, and zero internal candidate matches. Inputs shorter than5words use exact protection only. This is not semantic/document/pretraining decontamination proof.

<details><summary>Frozen inputs and counts</summary>

```json
{
  "UTC": "2026-11-23T10:12:21.761715+00:00",
  "train_sources": 1999,
  "mixture": {
    "general": 400,
    "technical_short": 400,
    "technical_medium": 700,
    "technical_long": 499
  },
  "dev_sources": 48,
  "test_sources": 96,
  "final_g8_technical_sources": 24,
  "greedy_semantic_sources": 64,
  "calibration_sources": 31,
  "calibration_fit": 16,
  "calibration_validation": 15,
  "data_SHA256": {
    "calibration.jsonl": "610978c08820359f782e7732428f791c22ae1c5c3d4f532a921fbf9da109d862",
    "dev.jsonl": "9cfeb3d810b625da28f81fcd54309fb4dc7ea6394f750580ded80f14f34ca1d3",
    "evaluation.jsonl": "8c3f315418c67470af56f38bfdacd6107bb768a66e4a0bad99303a9fcca5d35c",
    "review_selection.json": "34c9319fb5aa503ec4433953d20808598e00420d2d30c2f966b585af12f106a6",
    "train.jsonl": "57d8a74744d8c880c30232f2b4fefeddb7c162e3dbc572880daf41dcdccf25e1"
  },
  "parent_SHA256": "7f7a4914c5f403e757fdb882c3576ac68f2b0fa6edc00e537087716b28ddb07e",
  "near_duplicate_audit_SHA256": "883829ac113877c5ea4bb4cecbc2cd0247ec344c19dd6c8c83fb536331814172",
  "reference_QA_labels_SHA256": "999febfe6f70ceb9cf411c597b01eabd302d6c7bd8b984701fb10873eb359731",
  "reference_QA_counts": {
    "calibration": {
      "A": 27,
      "R": 3,
      "U": 2
    },
    "calibration_reserve": {
      "A": 4,
      "R": 1
    },
    "dev": {
      "R": 4,
      "A": 58,
      "U": 2
    },
    "test": {
      "A": 109,
      "U": 6,
      "R": 13
    },
    "test_reserve": {
      "A": 1
    },
    "train_replacement": {
      "A": 2,
      "R": 1
    },
    "train_sample": {
      "A": 10,
      "U": 1,
      "R": 2
    }
  },
  "deadline": {
    "user_request_anchor_unix": 1795427370.0,
    "deadline_unix": 1795448970.0,
    "training_deadline_unix": 1795443570.0,
    "maximum_user_wall_hours": 6,
    "deadline_Berlin": "2026-11-23 16:49:30 CET",
    "no_deadline_reset": true,
    "preparation_included": true
  },
  "scientific_outputs_seen": 0
}
```

</details>

<details><summary>Near-duplicate audit</summary>

```json
{
  "UTC": "2026-11-23T10:03:21.070855+00:00",
  "candidates": 256,
  "training_rows_scanned": 100642,
  "threshold": 0.85,
  "word_ngram": 5,
  "matches": [],
  "mutual_matches": [],
  "limitations": "Fewer-than5word inputs use prior exact exclusion only;not a semantic or document/pretraining contamination proof"
}
```

</details>

## Reward calibration and stop rules

Flow: **source→R0 candidates→scorer reads source+candidate+reference→DAPO**. References never enter actor prompts; no reference-token cross-entropy is applied.

Pinned MetricX and tokenizer revisions above; calibrate the actual BF16 inference precision. Maximum1536inputtokens, reject overlong rather than silently truncate. Lower error is better; base reward=1−clip(error,0,25)/25.

Compare raw reference-mode rewards and conservative numeric/unit/reference-confirmed EMA brand guards. Equivalent dose conversions are allowed; spelled numbers/ambiguous thousands trigger conservative skips. Guards do not detect every negation, relation, cause, sign, terminology or omission error; they are not a semantic oracle.

Onlyfit selects the recipe by source-balanced P/F ranking accuracy,tie raw. Onlyfit selects a threshold with≥90%proxy-positive precision and≥8positive predictions, maximizing balanced accuracy; tie precision then highest threshold. Validation never selects the recipe/threshold.

Validation must meet all: overall source-balanced ranking≥75%, technical medium/long ranking≥60%, proxy-positive precision≥80%,≥8positive candidates and≥3mixed-proxy groups. Failure means zero policy updates and early stop, with no gate relaxation/manual online-reward fallback. Candidate pairs are correlated; labels are historical same-assistant judgments, and class prevalence affects precision. Calibration precision does not guarantee equal precision on low-success deployment groups.

<details><summary>Original calibration protocol</summary>

```json
{
  "UTC": "2026-11-23T09:58:07.000882+00:00",
  "starting_adapter_SHA256": "7f7a4914c5f403e757fdb882c3576ac68f2b0fa6edc00e537087716b28ddb07e",
  "reference_mode_already_tried_in_history": true,
  "question": "Can pinned MetricX reference scores or conservative numeric/brand guards rank known P above F on source-held-out training candidates?",
  "candidate_annotation": "Previously sealed same-assistant P/F,not native certified;new data-reference audit required",
  "fit_sources": 16,
  "validation_sources": 16,
  "split_by_source": true,
  "recipe_candidates": [
    "raw",
    "guarded"
  ],
  "guard_fixed_penalties": {
    "numeric": 0.25,
    "EMA_anchor": 0.25,
    "empty_copy_repetition_reward": 0
  },
  "scorer": {
    "model": "google/metricx-24-hybrid-large-v2p6",
    "revision": "51e875ba5c525c81627cfd135ee10f43c87dce00",
    "tokenizer": "google/mt5-xl",
    "tokenizer_revision": "63fc6450d80515b48e026b69ef2fbbd426433e84",
    "precision": "BF16 inference of pinned checkpoint,calibrated in this actual precision",
    "maximum_input_tokens": 1536,
    "reject_overlong": true,
    "reference_hidden_from_actor": true
  },
  "selection": "Choose highest source-balanced fit pair-ranking accuracy,tie raw;threshold by highest fit balanced accuracy among fit proxy-positive precision>=.90 and at least8 predicted positives",
  "frozen_gate": {
    "validation_source_balanced_pair_accuracy_min": 0.75,
    "validation_technical_medium_long_pair_accuracy_min": 0.6,
    "validation_proxy_positive_precision_min": 0.8,
    "minimum_validation_predicted_positive_candidates": 8,
    "minimum_validation_mixed_proxy_groups": 3
  },
  "no_gate_relaxation": true,
  "if_fail": "Stop without policy updates;preserve calibration evidence and release owned GPU",
  "new_policy_updates": 0,
  "baseline_preserved": true,
  "validation_limitations": "Only16heldout sources,correlated candidate pairs,prior sameAI judgments,not proof of scorer reliability or Icelandic native correctness",
  "budget": {
    "user_request_anchor_unix": 1795427370.0,
    "deadline_unix": 1795448970.0,
    "training_deadline_unix": 1795443570.0,
    "maximum_user_wall_hours": 6,
    "deadline_Berlin": "2026-11-23 16:49:30 CET",
    "no_deadline_reset": true,
    "preparation_included": true
  }
}
```

</details>

<details><summary>Audited calibration manifest and amendment</summary>

```json
{
  "UTC": "2026-11-23T10:12:21.740902+00:00",
  "SHA256": "610978c08820359f782e7732428f791c22ae1c5c3d4f532a921fbf9da109d862",
  "fit_sources": 16,
  "validation_sources": 15,
  "no_new_scores_seen": true,
  "protocol_SHA256": "884e7adc8d34ff87d6cde86719b669fe2147e894a54157656349b767074b5578",
  "files": {
    "p22_guard.py": "098ce723fb32888d5a68c6d810997d4b6640345516cf8db1cec6e2ac43bd2334",
    "p22_scorer.py": "bc1f90cb7e9b378ca29b00cb6624af92116c747300624aa45285ae04db1cb693",
    "p22_calibration_worker.py": "0e69a240a200b1b6ac0c4bebe0af6cfb43bdaff68b222e4a39db16c88250dc20"
  },
  "amendment": "One bounded source/reference-only replenishment;4of5 references accepted,gate thresholds unchanged",
  "threshold_tiebreak": "Fit balanced accuracy,then precision,then highest threshold;validation never used"
}
```

</details>

## DAPO only after calibration passes

This is an unexecuted plan. Actor FP32base+LoRA/SDPA/TF32off, BF16scorer resident on GPU. Actual-GPU preflight must validate native sampler parity, teacher/sampler probabilities, finite nonzero gradients, first-update parameter movement and memory. Do not silently change precision after failure.

FixedG8/T.7/top-p1/top-k0,prompt1024/completion512,EOSincluded,prompt/pad/truncatedexcluded,soft-lengthbuffer64. LR3e−6,AdamW(.9,.999),eps1e−8,weight_decay0,gradclip1; clips.2/.28,4accepted sources/rollout,2epochs,maximum120actualupdates and32attempts/rollout.

An eligible group needs≥2valid candidates,both sides of the calibrated proxy threshold and nonzero reward variance. These are proxy-mixed groups, not confirmed-correct translation groups. Log all attempts,exclusions,candidates,rewards,advantages,old/newlogps,gradients,clipping and resources.

Every20updates evaluate48devsources and immediately save that point’s weights/cloud optimizer+RNG. Mirror every dev weight checkpoint toD; only the selected endpoint promises durable optimizer+RNG. Other cloud optimizer states are temporary scratch. Select by dev technical chrF+++BLEU with general/overall chrF retention within1.5,tie earliest. Preserve R0 without automatic promotion.

Early stop: single overalldev chrFdrop>2 or generaldrop>3;two overall drops>1.5;two latest technical combined scores below prior best>.5;insufficient eligible groups;numeric/memory/parity failure;time cutoff. Final comparisons use96greedy sources,24technicalG8 sources and64semantic sources with paired bootstrap intervals. Final data never selects checkpoints. One bounded exploratory run is not a multiseed formal efficiency comparison.

## Observed Colab connection blocker

Official-CLI L4/A100 allocation POSTs repeatedly return503. One H100 request returns400 at GET (unsupported request,noGPU). No experiment GPU has been allocated,no training executes in the user CPU runtime,and no compute units are purchased. After manual connection,the API shows one NONE/CPU runtime,balance406.6471255 and rate.08units/hour. Positive balance rules out exhausted balance,not capacity/policy/account/connection issues.503 alone is not proof of an account ban.

Continuous allocation attempts are stopped. Unbound user runtimes are not released/restarted. A manually connected singleL4/A100 explicitly for this experiment can be adopted under the original deadline. A read-only UI check stopped because the safety tool could not reliably determine the browser URL; no bypass or browser-setting change followed.

The officialFAQ explains dynamic hardware availability even with paid access. Other users’503reports do not diagnose this account.

<details><summary>Saved run state</summary>

```json
{
  "date": "2026-11-23",
  "UTC": "2026-11-23T10:12:22.465496+00:00",
  "phase": "REFERENCE_QA_COMPLETE_WAITING_GPU_ALLOCATION",
  "new_policy_updates": 0,
  "train_sources": 1999,
  "dev_sources": 48,
  "test_sources": 96,
  "calibration_sources": 31
}
```

</details>

## Reviewable artifacts

- Experiment: `D:\deep learning project\experiments\dapo_metricx_reference_2026-11-23`
- Run: `D:\deep learning project\runs\dapo_metricx_reference_2026-11-23`
- Source and fixed inputs: `D:\deep learning project\experiments\dapo_metricx_reference_2026-11-23\source`
- Reference cards/labels: `reference_QA/cards.jsonl`, `reference_QA/labels.jsonl`under experiment）
- Protocol: `calibration_protocol.json`
- Frozen inputs: `input_freeze.json`
- Near duplicates: `near_duplicate_audit.json`
- Lineage audit: `historical_lineage_exact_audit.json`
- Gate math: `host_scripts/p22_gate_math.py`
- Training source: `source/p22_train.py`, `source/p22_worker.py`

Local work is data processing,light tests and transfer,without neural model loading. Data/model copies reside onD; host scripts also remain in the original workspace. Syntax success is not GPU execution validation.

If GPU allocation remains unavailable,the outcome is an infrastructure blocker,not evidence that DAPO fails.

<details><summary>Full reference audit: calibration</summary>

```json
[
  {
    "card": 0,
    "panel": "calibration",
    "id": "OpenSubtitles18:456790",
    "stratum": "general",
    "subcorpus": "OpenSubtitles18",
    "source": "She didn't call Tyler.",
    "reference": "Hún hringdi ekkií Tyler.",
    "grade": "A",
    "note": "She did not call Tyler retained; missing space in ekkii noted as formatting noise,not repaired or treated as native-quality prose."
  },
  {
    "card": 1,
    "panel": "calibration",
    "id": "OpenSubtitles18:1440437",
    "stratum": "general",
    "subcorpus": "OpenSubtitles18",
    "source": "How old is the woman that he is marrying?",
    "reference": "Hversu gömul er konan sem hann kvænist?",
    "grade": "A",
    "note": "Question about age of woman he is marrying retained."
  },
  {
    "card": 2,
    "panel": "calibration",
    "id": "OpenSubtitles18:1162594",
    "stratum": "general",
    "subcorpus": "OpenSubtitles18",
    "source": "Do you have any money left?",
    "reference": "Áttu einhvern pening eftir?",
    "grade": "A",
    "note": "Question whether any money remains retained."
  },
  {
    "card": 3,
    "panel": "calibration",
    "id": "OpenSubtitles18:888652",
    "stratum": "general",
    "subcorpus": "OpenSubtitles18",
    "source": "And the children are learning so much from him.",
    "reference": "Og börnin læra svo margt af honum.",
    "grade": "A",
    "note": "Children learning much from him retained."
  },
  {
    "card": 4,
    "panel": "calibration",
    "id": "ParIce21:tatoeba:1307",
    "stratum": "general",
    "subcorpus": "tatoeba",
    "source": "We were talking to each other all the time.",
    "reference": "Við töluðum við hvorn annan sí og æ.",
    "grade": "A",
    "note": "Past reciprocal talking continually retained."
  },
  {
    "card": 5,
    "panel": "calibration",
    "id": "OpenSubtitles18:1512181",
    "stratum": "general",
    "subcorpus": "OpenSubtitles18",
    "source": "Well, the kids are asleep.",
    "reference": "Jæja, krakkarnir eru sofandi.",
    "grade": "A",
    "note": "Well,the kids are asleep retained."
  },
  {
    "card": 6,
    "panel": "calibration",
    "id": "OpenSubtitles18:950499",
    "stratum": "general",
    "subcorpus": "OpenSubtitles18",
    "source": "I mean, he laughs like this.",
    "reference": "Ég meina, hann hlær svona.",
    "grade": "A",
    "note": "I mean,he laughs like this retained."
  },
  {
    "card": 7,
    "panel": "calibration",
    "id": "OpenSubtitles18:1347949",
    "stratum": "general",
    "subcorpus": "OpenSubtitles18",
    "source": "Chon is cold metal.",
    "reference": "Chon er kaldur málmur.",
    "grade": "A",
    "note": "Chon,cold metal retained."
  },
  {
    "card": 8,
    "panel": "calibration",
    "id": "ParIce21:ema:75816",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Complete blood counts must be performed regularly during therapy with imatinib.",
    "reference": "Gera þarf heildar blóðkornatalningu reglulega meðan á meðferð með imatinibi stendur.",
    "grade": "A",
    "note": "Complete blood counts regularly during imatinib therapy retained."
  },
  {
    "card": 9,
    "panel": "calibration",
    "id": "ParIce21:ema:340346",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "The median follow-up duration was 22.9 months.",
    "reference": "Miðgildi eftirfylgnitíma var 22,9 mánuðir.",
    "grade": "A",
    "note": "Median follow-up22.9months retained."
  },
  {
    "card": 10,
    "panel": "calibration",
    "id": "ParIce21:ema:307431",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Studies in mice and rats showed developmental effects (see section 5.3).",
    "reference": "Rannsóknir á músum og rottum hafa sýnt áhrif á þroska (sjá kafla 5.3).",
    "grade": "A",
    "note": "Mouse/rat studies,developmental effects and5.3 retained."
  },
  {
    "card": 11,
    "panel": "calibration",
    "id": "ParIce21:ema:381117",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Tractocile can be used to delay the premature birth of your baby.",
    "reference": "Tractocile má nota til þess að seinka yfirvofandi fyrirburafæðingu.",
    "grade": "A",
    "note": "Tractocile delaying premature delivery retained; imminent phrasing noted,core indication intact."
  },
  {
    "card": 12,
    "panel": "calibration",
    "id": "ParIce21:ema:174449",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "IMVANEX may not fully protect all people who are vaccinated.",
    "reference": "Hugsanlegt er að IMVANEX verndi ekki fyllilega alla bólusetta einstaklinga.",
    "grade": "A",
    "note": "May not fully protect all vaccinated people and drug retained."
  },
  {
    "card": 13,
    "panel": "calibration",
    "id": "ParIce21:ema:304926",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Steady-state was achieved within two weeks.",
    "reference": "Jafnvægi náðist innan tveggja vikna.",
    "grade": "A",
    "note": "Steady state achieved within two weeks retained."
  },
  {
    "card": 14,
    "panel": "calibration",
    "id": "ParIce21:ema:93435",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Do not eat or drink for 10 minutes after taking this medicine.",
    "reference": "Hvorki skal borða né drekka í 10 mínútur eftir að lyfið er tekið.",
    "grade": "A",
    "note": "Neither eat nor drink for10minutes after taking medicine retained."
  },
  {
    "card": 15,
    "panel": "calibration",
    "id": "ParIce21:ema:204738",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "It is not recommended to drink alcohol during treatment with Leflunomide Winthrop.",
    "reference": "Ekki er ráðlegt að neyta áfengis á meðan á Leflunomide Winthrop meðferð stendur.",
    "grade": "A",
    "note": "Alcohol not advised during Leflunomide Winthrop treatment retained."
  },
  {
    "card": 16,
    "panel": "calibration",
    "id": "ParIce21:ema:207320",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "It will contain either 30, 60 or 120 sprays, depending on the pack size that has been prescribed for you.",
    "reference": "Hann inniheldur 30, 60 eða 120 úðaskammta, eftir því hvaða pakkningastærð hefur verið ávísað.",
    "grade": "A",
    "note": "Pack size, 30/60/120 sprays and prescribed relation retained."
  },
  {
    "card": 17,
    "panel": "calibration",
    "id": "ParIce21:ema:240705",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "NSAIDs (i.e. acetylsalicylic acid at anti-inflammatory dosage regimens, COX-2 inhibitors and non-selective NSAIDs) may reduce the diuretic, natriuretic and antihypertensive effects of thiazide diuretics and the antihypertensive effects of angiotensin II receptor antagonists.",
    "reference": "Bólgueyðandi gigtarlyf (þ.e. asetýlsalisýlsýra í bólgueyðandi skömmtum, COX-2 hemlar og ósértæk bólgueyðandi gigtarlyf) geta minnkað þvagræsandi, natríumlosandi og blóðþrýstingslækkandi verkun tíazíðþvagræsilyfja og blóðþrýstingslækkandi verkun angíótensín II blokka.",
    "grade": "A",
    "note": "NSAID classes, diuretic/natriuretic/BP reduction and angiotensin antagonist effects retained."
  },
  {
    "card": 18,
    "panel": "calibration",
    "id": "ParIce21:ema:129902",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "For further information on interaction potential of aprepitant at higher and multiple doses, please refer to the Summary of Product Characteristics for EMEND 80 mg hard capsules and EMEND 125 mg hard capsules.",
    "reference": "Til frekari upplýsinga um hugsanlegar milliverkanir stærri og fleiri skammta aprepitant, sjá samantekt á eiginleikum lyfs fyrir EMEND 80 mg hörð hylki og EMEND 125 mg hörð hylki.",
    "grade": "A",
    "note": "Aprepitant interaction, higher/multiple doses and EMEND 80/125 mg forms retained."
  },
  {
    "card": 19,
    "panel": "calibration",
    "id": "ParIce21:eea:2327631",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "Specific working conditions may have detrimental effects on the safety and health of workers.",
    "reference": "Sérstakar aðstæður á vinnustað geta haft skaðleg áhrif á öryggi og heilsu starfsmanna.",
    "grade": "A",
    "note": "Specific workplace conditions may harm worker safety/health retained."
  },
  {
    "card": 20,
    "panel": "calibration",
    "id": "ParIce21:ema:345823",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "The pharmacodynamic effect of factor VIIa gives rise to an increased local formation of factor Xa, thrombin and fibrin.",
    "reference": "Lyfhrif storkuþáttar VIIa auka staðbundna myndun á storkuþætti Xa, trombíni og fíbríni.",
    "grade": "A",
    "note": "VIIa effect increases local Xa/thrombin/fibrin formation retained."
  },
  {
    "card": 21,
    "panel": "calibration",
    "id": "ParIce21:ema:330553",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "The effects of fixed dose combination of telmisartan/HCTZ on mortality and cardiovascular morbidity are currently unknown.",
    "reference": "Áhrif ákveðinnar skammtasamsetningar (fixed dose combination) telmisartans/hýdróklórtíazíðs á tíðni hjarta- og æðasjúkdóma og dánartíðni vegna þeirra eru ekki þekkt.",
    "grade": "R",
    "note": "Reference narrows mortality to cardiovascular-related mortality; original says mortality and cardiovascular morbidity."
  },
  {
    "card": 22,
    "panel": "calibration",
    "id": "ParIce21:eea:1150826",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "The attached examples concerning the practical appli cation of points 1, 2 and 3 of this decision are part of this decision.",
    "reference": "Meðfylgjandi dæmi um beitingu 1., 2. og 3. liðar þessarar ákvörðunar í reynd eru hluti af þessari ákvörðun.",
    "grade": "R",
    "note": "Visible split OCR word appli cation; omit from reference calibration despite recoverable meaning."
  },
  {
    "card": 23,
    "panel": "calibration",
    "id": "ParIce21:eea:541759",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "Directive 2009/73/EC repeals Directive 2003/55/EC of the European Parliament and of the Council (12) which is incorporated into the EEA Agreement and which is consequently to be repealed under the EEA Agreement.",
    "reference": "Tilskipun 2009/73/ESB fellir úr gildi tilskipun Evrópuþingsins og ráðsins 2003/55/EB (12), sem hefur verið felld inn í EES-samninginn og ber því að fella gerðina brott úr samningnum.",
    "grade": "R",
    "note": "2009/73/EC rendered 2009/73/ESB (EU), while the EC/EB suffix matters for legal identifier fidelity."
  },
  {
    "card": 24,
    "panel": "calibration",
    "id": "ParIce21:eea:1597674",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Plan for the emergency vaccination against classical swine fever of pigs in pig holdings with a marker vaccine The plan submitted by Romania to the Commission on 27 September 2006 for the emergency vaccination against classical swine fever of pigs in pig holdings with a marker vaccine, in the area as set out in point 3 of the Annex, is approved.",
    "reference": "Áætlun um neyðarbólusetningu með merkibóluefni gegn svínapest í svínum á svínabújörðum Áætlunin, sem Rúmenía lagði fyrir framkvæmdastjórnina 27. september 2006 um neyðarbólusetningu með merkibóluefni gegn svínapest í svínum á svínabújörðum á því svæði sem fram kemur í 3. lið viðaukans, er samþykkt.",
    "grade": "A",
    "note": "Romanian emergency marker vaccination approval, date and Annex area retained; heading concatenated but self-contained."
  },
  {
    "card": 25,
    "panel": "calibration",
    "id": "ParIce21:ema:34924",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "An individual patient data based meta-analysis, which included data from all 12 controlled clinical studies in anaemic cancer patients conducted with NeoRecormon (n=2301), showed an overall hazard ratio point estimate for survival of 1.13 in favour of controls (95 % CI 0.87, 1.46).",
    "reference": "Safngreining á upplýsingum um einstaka sjúklinga, sem innihélt gögn úr öllum 12 klínísku samanburðarrannsóknunum hjá krabbameinssjúklingum með blóðleysi sem gerðar voru með NeoRecormon (n=2301), sýndi áhættuhlutfall fyrir heildarlifun 1,13, viðmiðunarhóp í hag (95 % öryggisbil 0,87, 1,46).",
    "grade": "A",
    "note": "12 trials, n2301, survival HR1.13 favoring controls and CI retained."
  },
  {
    "card": 26,
    "panel": "calibration",
    "id": "ParIce21:ema:175057",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "In a clinical trial with 107 children and adolescent patients (3 to 17 years of age) treated with combination therapy of peginterferon alfa-2b and ribavirin, dose modifications were required in 25 % of patients, most commonly for anaemia, neutropenia and weight loss.",
    "reference": "Í klínískri rannsókn með 107 börnum og unglingum (3 til 17 ára) sem fengu samsetta meðferð með peginterferon alfa-2b og ríbavírini þurfti að breyta skömmtum hjá 25% sjúklinga, yfirleitt vegna blóðleysis, daufkyrningafæðar og þyngdartaps.",
    "grade": "A",
    "note": "107 children, ages3-17, combined agents, 25percent dose modifications and causes retained."
  },
  {
    "card": 27,
    "panel": "calibration",
    "id": "ParIce21:eea:3083679",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Commission Delegated Regulation (EU) 2017/2365 of 18 December 2017 amending Directive 2014/24/EU of the European Parliament and of the Council in respect of the application thresholds for the procedures for the award of contracts ( 1 ) is to be incorporated into the EEA Agreement.",
    "reference": "Fella ber inn í EES-samninginn framselda reglugerð framkvæmdastjórnarinnar (ESB) 2017/2365 frá 18. desember 2017 um breytingu á tilskipun Evrópuþingsins og ráðsins 2014/24/ESB að því er varðar beitingu viðmiðunarfjárhæða við útboð og gerð samninga (1).",
    "grade": "A",
    "note": "Regulation2017/2365/date, directive2014/24/EU, thresholds and EEA incorporation retained."
  },
  {
    "card": 28,
    "panel": "calibration",
    "id": "ParIce21:ema:192992",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "In subgroup analyses, for subjects in the 60 mg treatment group who were dose reduced to 30 mg in the ENGAGE AF-TIMI 48 study (for body weight 60 kg, moderate renal impairment, or concomitant use of P-gp inhibitors), the event rate was: 2.29% per year for the primary endpoint, compared to the event rate of 2.66% per year for the matching subjects in the warfarin group HR (95% CI): 0.86 (0.66, 1.13).",
    "reference": "Í greiningu á undirhópum var tíðni tilvika 2,29% á ári fyrir aðalendapunktinn hjá einstaklingum í 60 mg meðferðarhópnum sem fengu skammtinn minnkaðan í 30 mg, í ENGAGE AF-TIMI 48 rannsókninni, (vegna líkamsþyngdar 60 kg, miðlungsmikið skertrar nýrnastarfsemi eða samhliða notkunar P-gp hemla), samanborið við 2,66% tíðni tilvika á ári hjá pöruðum einstaklingum í warfarínhópnum HR (95% CI): 0,86 (0,66; 1,13).",
    "grade": "U",
    "note": "Body weight 60kg lacks comparison sign in both texts; likely extraction damage makes eligibility threshold ambiguous."
  },
  {
    "card": 29,
    "panel": "calibration",
    "id": "ParIce21:ema:252360",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "Overall, the safety profile in patients co-infected with hepatitis B and/or C was similar to that observed in patients without hepatitis B or C co-infection, although the rates of AST and ALT abnormalities were higher in the subgroup with hepatitis B and/or C co-infection for all treatment groups.",
    "reference": "Í öllum meðferðarhópum var almennt aukaverkanamynstur hjá sjúklingum með samhliða sýkingu lifrarbólgu B og/eða C svipað og hjá sjúklingum sem ekki voru einnig sýktir af lifrarbólgu B og/eða C, þó tíðni frávika í AST og ALT væri hærri í undirhópnum með samhliða sýkingu lifrarbólgu B og/eða C í öllum meðferðarhópum.",
    "grade": "A",
    "note": "Similar overall safety, hepatitis coinfection and higher AST/ALT subgroup abnormality rates retained."
  },
  {
    "card": 30,
    "panel": "calibration",
    "id": "ParIce21:ema:177724",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "In a randomised, open label, controlled clinical trial, chemotherapy (oxaliplatin or irinotecan) and bevacizumab were given with and without panitumumab in the first-line treatment of patients with metastatic colorectal cancer (n = 1,053 n = 823 oxaliplatin cohort, n = 230 irinotecan cohort).",
    "reference": "Í slembaðri, opinni, klínískri samanburðarrannsókn var gefin lyfjameðferð (oxaliplatin eða irinotecan) og bevacizumab, með og án panitumumabs, sem fyrsta meðferð við krabbameini í ristli eða endaþarmi með meinvörpum (n = 1.053 n = 823 oxaliplatin hópur, n = 230 irinotecan hópur).",
    "grade": "A",
    "note": "Randomized open trial, chemotherapy/bevacizumab +/-panitumumab, indication and cohort numbers retained; punctuation awkward but aligned."
  },
  {
    "card": 31,
    "panel": "calibration",
    "id": "ParIce21:ema:169847",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "If your doctor considers that the benefits of taking Revolade outweigh the risks, you will be closely monitored during treatment. if you are at risk of blood clots in your veins or arteries, or you know that blood clots are common in your family.",
    "reference": "Ef læknirinn telur að ávinningur af meðferð með Revolade sé meiri en áhættan verður haft náið eftirlit með þér meðan á meðferðinni stendur. ef þú átt á hættu að fá blóðtappa í bláæð eða slagæð, eða ef þú veist að blóðtappar eru algengir í fjölskyldunni.",
    "grade": "U",
    "note": "Second if-clause lacks governing instruction/context; excluded as context-dependent incomplete reference pair."
  }
]
```

</details>

<details><summary>Full reference audit: calibration_reserve</summary>

```json
[
  {
    "card": 240,
    "panel": "calibration_reserve",
    "id": "ParIce21:eso:7407",
    "stratum": "technical_medium",
    "subcorpus": "eso",
    "source": "Its formation is closely linked to two other familiar molecules, oxygen and water, which are critical for life.",
    "reference": "Myndun hennar er nátengd tveimur öðrum kunnuglegum sameindum, súrefni og vatni, sem eru lífi nauðsynlegar.",
    "grade": "A",
    "note": "Formation linked oxygen/water molecules critical to life retained."
  },
  {
    "card": 241,
    "panel": "calibration_reserve",
    "id": "ParIce21:ema:342400",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "The needle cap of the pre-filled pen contains latex (dry natural rubber) that may cause hypersensitivity reactions when handled by or when Enbrel is administered to persons with known or possible latex sensitivity.",
    "reference": "Nálarhlífin fyrir áfyllta lyfjapennann inniheldur latex (þurrkað náttúrulegt gúmmí) sem getur valdið ofnæmisviðbrögðum þegar það er handleikið eða þegar Enbrel er gefið einstaklingi sem vitað er að sé, eða er hugsanlega viðkvæmur fyrir latexi.",
    "grade": "A",
    "note": "Prefilled pen needle cap latex and handler/recipient known/possible allergy retained."
  },
  {
    "card": 242,
    "panel": "calibration_reserve",
    "id": "ParIce21:ema:162906",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "If you are taking any other medicines mentioned under “Other medicines and Ceplene” or if you are to have an operation or special X-ray investigation requiring an injection, talk to your doctor.",
    "reference": "Ráðfærðu þig við lækninn ef þú tekur önnur lyf en þau sem nefnd eru í „Notkun annarra lyfja samhliða Ceplene“ eða ef þú ert á leið í uppskurð eða sérstaka röntgenrannsókn þar sem þarf að sprauta þig.",
    "grade": "R",
    "note": "Medicines mentioned in section rendered medicines other than those mentioned: inclusion/exclusion inversion."
  },
  {
    "card": 243,
    "panel": "calibration_reserve",
    "id": "ParIce21:eea:302109",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Commission Decision 2010/193/EU of 29 March 2010 amending Decision 2003/135/EC as regards the eradication and emergency vaccination plans for classical swine fever in feral pigs in certain areas of North Rhine-Westphalia and Rhineland-Palatinate (Germany)8 is to be incorporated into the Agreement.",
    "reference": "Fella ber inn í samninginn ákvörðun framkvæmdastjórnarinnar 2010/193/ESB frá 29. mars 2010 um breytingu á ákvörðun 2003/135/EB að því er varðar áætlanir um útrýmingu og neyðarbólusetningu gegn svínapest í villtum svínum á tilteknum svæðum í sambandslöndunum Nordrhein-Westfalen og Rheinland-Pfalz (Þýskalandi) (8).",
    "grade": "A",
    "note": "Decision2010/193/EU29March2010 amends2003/135/EC, swine vaccination regional names and incorporation retained."
  },
  {
    "card": 244,
    "panel": "calibration_reserve",
    "id": "ParIce21:ema:177530",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "In a population pharmacokinetic analysis in patients with hepatic edema, AUC of tolvaptan in severely (Child-Pugh class C) and mildly or moderately (Child-Pugh classes A and B) hepatic impaired patients were 3.1 and 2.3 times higher than that in healthy subjects.",
    "reference": "Í greiningu á lyfjahvörfum sjúklinga með lifrarbjúg var AUC tolvaptans hjá sjúklingum með alvarlega (Child Pugh flokkur C) eða vægt eða miðlungs (Child Pugh flokkar A og B) skerta lifrarstarfsemi 3,1 og 2,3 sinnum hærra en hjá hraustum einstaklingum.",
    "grade": "A",
    "note": "Hepatic edema PK, ChildPughC vsA/B AUC3.1/2.3times healthy retained."
  }
]
```

</details>

<details><summary>Full reference audit: dev</summary>

```json
[
  {
    "card": 45,
    "panel": "dev",
    "id": "p22official21:dev:opensubtitles:1397",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "I haven't held a football in eight years.",
    "reference": "Ég hef ekki verið í ruðningi í átta ár.",
    "grade": "R",
    "note": "Not held a football becomes not been in/played football; literal action changed."
  },
  {
    "card": 46,
    "panel": "dev",
    "id": "p22official21:dev:opensubtitles:2023",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "These shoes have come up a treat.",
    "reference": "Skórnir eru eins og nýir.",
    "grade": "A",
    "note": "Shoes came up a treat idiom faithfully expressed as like new."
  },
  {
    "card": 47,
    "panel": "dev",
    "id": "p22official21:dev:opensubtitles:1427",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "Is this my new prison?",
    "reference": "Er þetta nýja fangelsið mitt?",
    "grade": "A",
    "note": "New prison question retained."
  },
  {
    "card": 48,
    "panel": "dev",
    "id": "p22official21:dev:opensubtitles:702",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "We teach the children English, reading, writing history, geography, arithmetic and Bible stories.",
    "reference": "Við kennum börnunum ensku, lestur, skrift, sögu, landafræði, reikning og biblíusögur.",
    "grade": "A",
    "note": "Children and complete list of subjects retained; source punctuation after writing inferred."
  },
  {
    "card": 49,
    "panel": "dev",
    "id": "p22official21:dev:opensubtitles:2173",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "I brought them in, simple as that.",
    "reference": "Ég kom með þá, svo einfalt er málið.",
    "grade": "A",
    "note": "Brought them in and simple-as-that idiom retained."
  },
  {
    "card": 50,
    "panel": "dev",
    "id": "p22official21:dev:opensubtitles:654",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "So anyway, I'm Vik, the director.",
    "reference": "Allavega, ég er Vik, leikstjórinn.",
    "grade": "A",
    "note": "Vik and director self-introduction retained."
  },
  {
    "card": 51,
    "panel": "dev",
    "id": "p22official21:dev:opensubtitles:2846",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "That love's the finest thing around...",
    "reference": "Þessi ást er það besta sem til er...",
    "grade": "A",
    "note": "Love as finest thing retained."
  },
  {
    "card": 52,
    "panel": "dev",
    "id": "p22official21:dev:opensubtitles:2739",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "That is Forrest Gump, coach.",
    "reference": "Þetta er Forrest Gump þjálfi.",
    "grade": "A",
    "note": "Forrest Gump and address to coach retained."
  },
  {
    "card": 53,
    "panel": "dev",
    "id": "p22official21:dev:opensubtitles:3123",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "The night before we met.",
    "reference": "Kvöldið áður en við hittumst.",
    "grade": "A",
    "note": "Time expression night before we met retained; standalone fragment has clear aligned meaning."
  },
  {
    "card": 54,
    "panel": "dev",
    "id": "p22official21:dev:opensubtitles:2385",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "Shaleen must have the fifties.",
    "reference": "Shaleen hlýtur að hafa fimmtíu dollara seðlana.",
    "grade": "U",
    "note": "Fifties interpreted as fifty-dollar notes; absent context makes intended referent uncertain."
  },
  {
    "card": 55,
    "panel": "dev",
    "id": "p22official21:dev:opensubtitles:2987",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "Soon we were put to the test.",
    "reference": "Brátt var komið að prófinu.",
    "grade": "R",
    "note": "We were put to the test becomes it was time for the test; role/experience lost."
  },
  {
    "card": 56,
    "panel": "dev",
    "id": "p22official21:dev:opensubtitles:2700",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "On my first night in Argentina, I didn't know about the locals.",
    "reference": "Fyrsta kvöld mitt í Argentínu, vissi ég ekkert um staðarmenn.",
    "grade": "A",
    "note": "First night in Argentina and lack of local knowledge retained."
  },
  {
    "card": 57,
    "panel": "dev",
    "id": "p22official21:dev:opensubtitles:2485",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "How, maybe, after the fourth donation, even if you've technically completed, you're still conscious in some sort of way.",
    "reference": "Eins og kannski eftir fjórðu gjöfina, jafnvel þó þú sért tæknilega dáin, þá er maður einhvern veginn með meðvitund.",
    "grade": "U",
    "note": "Completed interpreted as dead in donation setting; requires missing narrative context."
  },
  {
    "card": 58,
    "panel": "dev",
    "id": "p22official21:dev:opensubtitles:819",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "Would you sail to the ends of the Earth and beyond to fetch back witty Jack and him precious Pearl?",
    "reference": "Mynduð þið sigla til enda veraldarinnar til að ná í klára Jack og Perluna hans dýrmætu?",
    "grade": "A",
    "note": "Sailing to ends of world to retrieve Jack and precious Pearl retained; beyond omitted as rhetorical emphasis."
  },
  {
    "card": 59,
    "panel": "dev",
    "id": "p22official21:dev:opensubtitles:2153",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "I knew a man who could fly.",
    "reference": "Ég þekkti mann sem flaug.",
    "grade": "A",
    "note": "Knew man who could fly expressed as knew man who flew, core ability retained."
  },
  {
    "card": 60,
    "panel": "dev",
    "id": "p22official21:dev:opensubtitles:327",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "Well, I am starting my own music site.",
    "reference": "Jæja, ég er að stofna eigin tónlistarsíðu.",
    "grade": "A",
    "note": "Starting own music site retained."
  },
  {
    "card": 61,
    "panel": "dev",
    "id": "p22official21:dev:eea:1622",
    "stratum": "technical_short",
    "subcorpus": "eea",
    "source": "Promoting investigation of the online victimisation of children.",
    "reference": "Að stuðla að rannsóknum á ofbeldi gegn börnum á Netinu.",
    "grade": "A",
    "note": "Promoting investigation of online child victimization retained."
  },
  {
    "card": 62,
    "panel": "dev",
    "id": "p22official21:dev:eea:1248",
    "stratum": "technical_short",
    "subcorpus": "eea",
    "source": "The Executive Director of the Agency shall not vote.",
    "reference": "Framkvæmdastjóri stofnunarinnar greiðir ekki atkvæði.",
    "grade": "A",
    "note": "Agency executive director shall not vote retained."
  },
  {
    "card": 63,
    "panel": "dev",
    "id": "p22official21:dev:eea:1595",
    "stratum": "technical_short",
    "subcorpus": "eea",
    "source": "Encouraging the enhancement of efficient and cost-effective awareness-raising methods and tools.",
    "reference": "Að hvetja til umbóta á skilvirkum og kostnaðarhagkvæmum aðferðum og úrræðum til vitundarvakningar.",
    "grade": "A",
    "note": "Efficient and cost-effective awareness methods/tools enhancement retained."
  },
  {
    "card": 64,
    "panel": "dev",
    "id": "p22official21:dev:ema:208",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Each vial contains 300 mg aripiprazole.",
    "reference": "Hvert hettuglas inniheldur 300 mg af aripíprazóli.",
    "grade": "A",
    "note": "Each vial300mg aripiprazole retained."
  },
  {
    "card": 65,
    "panel": "dev",
    "id": "p22official21:dev:eso:793",
    "stratum": "technical_short",
    "subcorpus": "eso",
    "source": "The new observations help to answer these questions.",
    "reference": "Nýja rannsóknin hjálpar til við að svara þessum spurningum.",
    "grade": "A",
    "note": "New observations/research help answer questions, acceptable study paraphrase."
  },
  {
    "card": 66,
    "panel": "dev",
    "id": "p22official21:dev:eso:107",
    "stratum": "technical_short",
    "subcorpus": "eso",
    "source": "The telescope optics also include correction for dispersion by the Earths atmosphere.",
    "reference": "Sjóntæki sjónaukans leiðrétta líka fyrir ljósdreifingu sem verður í lofthjúpi jarðar.",
    "grade": "A",
    "note": "Telescope optics correction of Earth atmospheric dispersion retained."
  },
  {
    "card": 67,
    "panel": "dev",
    "id": "p22official21:dev:ema:1720",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Each dose is given over a period of one or four hours.",
    "reference": "Hver skammtur er gefinn á einni eða fjórum klst.",
    "grade": "A",
    "note": "Each dose over one or four hours retained."
  },
  {
    "card": 68,
    "panel": "dev",
    "id": "p22official21:dev:ema:1826",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "The clinical relevance of this finding is unknown.",
    "reference": "Ekki er vitað hvort þessi niðurstaða skiptir máli í klínísku tilliti.",
    "grade": "A",
    "note": "Clinical relevance unknown retained."
  },
  {
    "card": 69,
    "panel": "dev",
    "id": "p22official21:dev:eea:149",
    "stratum": "technical_short",
    "subcorpus": "eea",
    "source": "This Regulation shall enter into force on 1 January 1996.",
    "reference": "Reglugerð þessi öðlast gildi 1. janúar 1996.",
    "grade": "A",
    "note": "Regulation commencement1January1996 retained."
  },
  {
    "card": 70,
    "panel": "dev",
    "id": "p22official21:dev:ema:1345",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Changes in PSA serum concentration independently do not always predict clinical benefit.",
    "reference": "Breytingar sem verða á þéttni PSA í sermi segja ekki alltaf til um klínískan árangur einar og sér.",
    "grade": "A",
    "note": "PSA serum change alone not always clinical benefit predictor retained."
  },
  {
    "card": 71,
    "panel": "dev",
    "id": "p22official21:dev:ema:874",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "You should take your temperature as you may have a fever.",
    "reference": "Þú ættir að mæla þig því þú gætir verið með hita.",
    "grade": "A",
    "note": "Measure temperature due to possible fever retained."
  },
  {
    "card": 72,
    "panel": "dev",
    "id": "p22official21:dev:ema:3009",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Blood clot in the arterio-venous fistula in patients on dialysis.",
    "reference": "Blóðkekkir í slag-bláæðarfistli hjá sjúklingum í skilun.",
    "grade": "A",
    "note": "Arteriovenous fistula clot in dialysis patients retained."
  },
  {
    "card": 73,
    "panel": "dev",
    "id": "p22official21:dev:ema:1515",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "The information presented on biotransformation and elimination is based on oral busulfan.",
    "reference": "Upplýsingar fyrir umbrot og útskilnað hér að neðan byggjast á búsúlfani til inntöku.",
    "grade": "A",
    "note": "Biotransformation/elimination information based on oral busulfan retained."
  },
  {
    "card": 74,
    "panel": "dev",
    "id": "p22official21:dev:eea:1134",
    "stratum": "technical_short",
    "subcorpus": "eea",
    "source": "They are specifically designed to avoid false negatives.",
    "reference": "Þær eru sérstaklega hannaðar þannig að þær eiga ekki að gefa rangar, neikvæðar niðurstöður.",
    "grade": "A",
    "note": "Designed to avoid false negatives retained."
  },
  {
    "card": 75,
    "panel": "dev",
    "id": "p22official21:dev:eea:706",
    "stratum": "technical_short",
    "subcorpus": "eea",
    "source": "Each record has to be either fixed-length or comma-separated.",
    "reference": "Hver skrá skal vera af fastri lengd eða aðskilin frá öðrum með kommu.",
    "grade": "R",
    "note": "Comma-separated record contents rendered each record separated from others by comma; record-format meaning changed."
  },
  {
    "card": 76,
    "panel": "dev",
    "id": "p22official21:dev:ema:1296",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Recombinant interferon alfa-2b also inhibits viral replication in vitro and in vivo.",
    "reference": "Raðbrigða interferon alfa-2b hemur einnig veirufjölgun in vitro og in vivo.",
    "grade": "A",
    "note": "Recombinant interferonalpha2b inhibition in vitro/in vivo retained."
  },
  {
    "card": 77,
    "panel": "dev",
    "id": "p22official21:dev:eea:1125",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "For other products, the minimum number of incremental samples to be taken from the lot shall be as given in Table 1.",
    "reference": "Að því er aðrar vörur varðar skal lágmarksfjöldi hlutasýna, sem taka ber úr framleiðslueiningu, vera sá sem gefinn er upp í töflu 1.",
    "grade": "A",
    "note": "Other products, minimum incremental samples, lot and Table1 retained."
  },
  {
    "card": 78,
    "panel": "dev",
    "id": "p22official21:dev:eso:600",
    "stratum": "technical_medium",
    "subcorpus": "eso",
    "source": "“We are excited to begin our search for small planets around nearby stars.",
    "reference": "„Við hlökkum til að hefja leit að litlum reikistjörnum í kringum nálægar stjörnur.",
    "grade": "A",
    "note": "Excitement to start small planets search near stars retained."
  },
  {
    "card": 79,
    "panel": "dev",
    "id": "p22official21:dev:ema:3132",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "This means you will take a total of six 400 mg capsules (2400 mg) each day.",
    "reference": "Það þýðir að taka þarf alls sex 400 mg hylki (2.400 mg) á hverjum sólarhring.",
    "grade": "A",
    "note": "Six400mg capsules totaling2400mg daily retained; thousands punctuation localized."
  },
  {
    "card": 80,
    "panel": "dev",
    "id": "p22official21:dev:ema:2336",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "Susceptibility of circulating influenza virus strains to oseltamivir has been shown to be highly variable (see section 5.1).",
    "reference": "Sýnt hefur verið fram á að næmi inflúensuveirustofna sem eru að ganga, fyrir oseltamivíri er mjög breytilegt (sjá kafla 5.1).",
    "grade": "A",
    "note": "Highly variable circulating influenza susceptibility to oseltamivir and section5.1 retained."
  },
  {
    "card": 81,
    "panel": "dev",
    "id": "p22official21:dev:eea:1779",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "Therefore, on the basis of the common criteria, it is assessed that these air carriers should continue to be subject to an operating ban (Annex A) or operating restrictions (Annex B), as the case may be.",
    "reference": "Á grundvelli sameiginlegu viðmiðananna er það því metið svo að þessum flugrekendum skuli áfram bannað að stunda flugrekstur (viðauki A) eða takmarkanir settar á flugrekstur þeirra (viðauki B), eftir því sem við á.",
    "grade": "A",
    "note": "Common criteria, continued bans AnnexA/restrictions AnnexB retained."
  },
  {
    "card": 82,
    "panel": "dev",
    "id": "p22official21:dev:ema:1782",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "Experience of treatment of infections caused by penicillin/or erythromycin resistant S. pneumoniae is limited, but so far, clinical efficacy and eradication rates have been similar compared with the treatment of susceptible S. pneumoniae.",
    "reference": "Takmörkuð reynsla er af meðferð sýkinga af völdum penisillín-/eða erýtrómýsínþolinna S. pneumoniae, en hingað til hafa klínísk áhrif og hlutfall upprætingar (eradication) verið svipuð samanborið við meðferð sýkinga af völdum næmra S. pneumoniae.",
    "grade": "A",
    "note": "Limited resistant pneumococcus experience but similar efficacy/eradication to susceptible retained."
  },
  {
    "card": 83,
    "panel": "dev",
    "id": "p22official21:dev:eea:1688",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "This Article shall also apply to non-written information exchanged during meetings at which sensitive subjects are discussed.",
    "reference": "Þessi grein skal einnig eiga við um óskráð upplýsingaskipti á fundum þar sem viðkvæm málefni eru rædd.",
    "grade": "A",
    "note": "Article applies also unwritten information at sensitive-topic meetings retained."
  },
  {
    "card": 84,
    "panel": "dev",
    "id": "p22official21:dev:eea:1952",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "It shall reclassify a financial liability as equity from the date when the instrument has all the features and meets the conditions set out in paragraphs 16A and 16B or paragraphs 16C and 16D.",
    "reference": "Hún skal endurflokka fjárskuldbindingu sem eigið fé frá þeim degi sem gerningurinn hefur öll einkenni og uppfyllir skilyrðin sem eru sett fram í liðum 16A og 16B eða í liðum 16C og 16D.",
    "grade": "A",
    "note": "Liability reclassification as equity when features/16A16B or16C16D conditions met retained."
  },
  {
    "card": 85,
    "panel": "dev",
    "id": "p22official21:dev:eso:903",
    "stratum": "technical_medium",
    "subcorpus": "eso",
    "source": "When the spots inside the Occator crater are on the side illuminated by the Sun they form plumes that reflect sunlight very effectively.",
    "reference": "Þegar blettirnir í Occator gígnum snúa að sólinni verða til strókar sem endurvarpa sólarljósi vel.",
    "grade": "A",
    "note": "Sun-facing Occator spots produce reflective plumes retained."
  },
  {
    "card": 86,
    "panel": "dev",
    "id": "p22official21:dev:eso:1150",
    "stratum": "technical_medium",
    "subcorpus": "eso",
    "source": "One of these “mini surveys” was a detailed study of NGC 253 and its environment.",
    "reference": "Nákvæm rannsókn á NGC 253 og nágrenni hennar var eitt þessara smærri kortlagningarverkefna.",
    "grade": "A",
    "note": "NGC253 environment detailed mini-survey retained."
  },
  {
    "card": 87,
    "panel": "dev",
    "id": "p22official21:dev:eea:1370",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "The main objective of this Directive is to introduce Community measures to enhance port security in the face of threats of security incidents.",
    "reference": "Meginmarkmið þessarar tilskipunar er að innleiða ráðstafanir Bandalagsins til að efla hafnarvernd andspænis ógnunum um váatvik.",
    "grade": "A",
    "note": "Community measures to improve port security against incidents retained."
  },
  {
    "card": 88,
    "panel": "dev",
    "id": "p22official21:dev:eea:1849",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "For each chemical product used in the assembly of furniture, a Safety Data Sheet or equivalent documentation shall be presented containing information on health hazard classification.",
    "reference": "Að því er varðar sérhverja efnavöru, sem er notuð við samsetningu húsgagna, skal leggja fram öryggisblað eða jafngild gögn sem innihalda upplýsingar um heilbrigðishættuflokkun.",
    "grade": "A",
    "note": "Furniture assembly chemical SDS/equivalent with health hazard classification retained."
  },
  {
    "card": 89,
    "panel": "dev",
    "id": "p22official21:dev:ema:809",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "Treatment with Herceptin alone or with a taxane may affect the heart, especially if you have ever used an anthracycline (taxanes and anthracyclines are two other kinds of medicine used to treat cancer).",
    "reference": "Meðferð með Herceptin einu sér eða ásamt taxanlyfi getur haft áhrif á hjartað, einkum ef þú hefur einhvern tímann notað antracýklínlyf (taxanlyf og antracýklínlyf eru tveir aðrir flokkar krabbameinslyfja).",
    "grade": "A",
    "note": "Herceptin +/-taxane cardiac effects especially previous anthracycline, drug classes retained."
  },
  {
    "card": 90,
    "panel": "dev",
    "id": "p22official21:dev:ema:1585",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "Vials of ceftazidime/avibactam powder should be reconstituted with 10 mL of sterile water for injections, followed by shaking until the content dissolves.",
    "reference": "Blanda á hettuglös með ceftazidimi/avibactami dufti með 10 ml af vatni fyrir stungulyf, og hrista þar til innihaldið leysist upp.",
    "grade": "A",
    "note": "Ceftazidime/avibactam10mL water for injections then shake to dissolve retained; sterile implicit in injection-water term."
  },
  {
    "card": 91,
    "panel": "dev",
    "id": "p22official21:dev:ema:2503",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "Foscan shall not be diluted nor flushed with sodium chloride or any other aqueous solution.",
    "reference": "Ekki má þynna Foscan eða skola með natríumklóríðlausn eða nokkurri annarri vatnslausn.",
    "grade": "A",
    "note": "Foscan not dilute/flush with sodium chloride or other aqueous solutions retained."
  },
  {
    "card": 92,
    "panel": "dev",
    "id": "p22official21:dev:eea:133",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "Member States shall comply with the provisions of paragraphs 13.2, 13.4 and 13.5 of the ISM Code as if the provisions thereof were mandatory, in relation to companies and ro-ro ferries.",
    "reference": "Aðildarríkin skulu, að því er varðar fyrirtæki og ekjuferjur, fara að ákvæðum liða 13.2, 13.4 og 13.5 í ISM-reglunum eins og um lögboðin ákvæði væri að ræða.",
    "grade": "A",
    "note": "ISM13.2/13.4/13.5 as mandatory for companies/ro-ro ferries retained."
  },
  {
    "card": 93,
    "panel": "dev",
    "id": "p22official21:dev:eea:150",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "By way of derogation from the first subparagraph, this Regulation shall not apply until 31 December 1997 to companies which are incorporated under Greek law, which have their principal place of business in Greece, and which operate ro-ro- ferries registered in and flying the flag of Greece providing regular services exclusively between ports situated in Greece.",
    "reference": "Þrátt fyrir fyrstu undirgrein kemur þessi reglugerð ekki til framkvæmda fyrr en 31. desember 1997 að því er varðar fyrirtæki sem eru stofnsett samkvæmt grískum lögum og hafa aðalstarfsstöð í Grikklandi og starfrækja ekjuferjur sem eru skráðar í og sigla undir fána Grikklands og sigla eingöngu í föstum áætlunarferðum milli hafna í Grikklandi.",
    "grade": "A",
    "note": "Greek company, base/flag/domestic ro-ro criteria and exemption until31Dec1997 retained."
  },
  {
    "card": 94,
    "panel": "dev",
    "id": "p22official21:dev:ema:762",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "There was also a subpopulation of 16 advanced phase patients (5 AP CML and 11 BP CML patients) that failed treatment with either imatinib alone or imatinib in addition to one or both second- generation TKIs (dasatinib and nilotinib) and for whom, based on the presence of co-morbidities, a history of TKI intolerance, or a BCR-ABL resistance mutation, the remaining approved TKI(s) were not considered appropriate treatment options.",
    "reference": "Hjá undirhópi 16 sjúklinga með langt genginn sjúkdóm (5 með CML í hröðunarfasa og 11 með CML í bráðafasa) mistókst meðferð annað hvort með imatinibi einu sér eða imatinibi ásamt öðrum eða báðum annarrar kynslóðar týrosín kínasa hemlunum (dasatinib and nilotinib) og aðrir samþykktir týrosín kínasa hemlar voru ekki taldir henta til meðferðar, vegna annarra kvilla, sögu um óþol gegn týrosín kínasa hemlum eða stökkbreytingar í BCR-ABL sem tengist ónæmi.",
    "grade": "A",
    "note": "16 advanced CML patients5AP11BP, failed TKIs, comorbidities/intolerance/resistance and unsuitability retained."
  },
  {
    "card": 95,
    "panel": "dev",
    "id": "p22official21:dev:eea:1404",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "In applying this Directive, the Commission shall take, in accordance with Decision 2001/844/EC, ECSC, Euratom (1), appropriate measures to protect information subject to the requirement of confidentiality to which it has access or which is communicated to it by Member States.",
    "reference": "Við beitingu þessarar tilskipunar skal framkvæmdastjórnin gera viðeigandi ráðstafanir, í samræmi við ákvæði ákvörðunar Kola- og stálbandalags Evrópu og Kjarnorkubandalags Evrópu 2001/844/EB (1), til að vernda trúnaðarupplýsingar sem hún hefur aðgang að eða aðildarríkin senda henni.",
    "grade": "A",
    "note": "Commission confidentiality measures, decision2001/844/EC/ECSC/Euratom and state-provided information retained."
  },
  {
    "card": 96,
    "panel": "dev",
    "id": "p22official21:dev:eea:750",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "This discussion has contributed to raising awareness in this field among public and private parties and may be an important basis for improving the conditions of the exploitation in Europe of content with a high added value in educational, cultural, social and professional terms and for the development of new multimedia goods and services, while safeguarding wide access to it.",
    "reference": "Þessi skoðanaskipti hafa stuðlað að því að vekja einkaaðila og opinbera aðila til vitundar á þessu sviði og kunna að vera traustur grundvöllur að því er varðar að bæta skilyrði fyrir hagnýtingu inntaks innan Evrópu, sem skapar mikinn virðisauka í menntunar-, menningar-, félags- og faglegu tilliti, og að því er varðar þróun nýrra margmiðlunarvara og -þjónustu, um leið að tryggja greiðan aðgang að því.",
    "grade": "A",
    "note": "Awareness, high-value content exploitation across fields, multimedia development and broad access retained."
  },
  {
    "card": 97,
    "panel": "dev",
    "id": "p22official21:dev:eea:1988",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "AG14J A condition for classifying as equity a financial instrument that otherwise meets the criteria in paragraph 16A or paragraph 16C is that the entity has no other financial instrument or contract that has (a) total cash flows based substantially on the profit or loss, the change in the recognised net assets or the change in the fair value of the recognised and unrecognised net assets of the entity and (b) the effect of substantially restricting or fixing the residual return.",
    "reference": "AG14J Skilyrði fyrir flokkun fjármálagernings sem eigið fé, sem stenst að öðru leyti viðmiðanir í lið 16A eða lið 16C, er að einingin hafi enga aðra fjármálagerninga eða samninga sem a) hafa samanlagt sjóðstreymi sem byggist að verulegu leyti á rekstrarreikningi, breytingum á færðri, hreinni eign eða breytingum á gangvirði færðrar og ófærðrar, hreinnar eignar einingarinnar og b) takmarki verulega eða fastsetji eftirstandandi arð.",
    "grade": "A",
    "note": "Equity classification,16A/16C, other cashflow-linked instruments and residual return restrictions retained."
  },
  {
    "card": 98,
    "panel": "dev",
    "id": "p22official21:dev:eea:1260",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "The Agency shall be open to the participation of third countries, which have entered into agreements with the European Community, whereby they have adopted and are applying Community law in the field of maritime safety and prevention of pollution by ships.",
    "reference": "Þriðju löndum, sem hafa gert samninga við Evrópubandalagið sem fela í sér að þau innleiða og beita lögum Bandalagsins á sviði siglingaöryggis og varna gegn mengun sjávar frá skipum, er heimil þátttaka í stofnuninni.",
    "grade": "A",
    "note": "Third-country agreements applying Community maritime safety/pollution laws and agency participation retained."
  },
  {
    "card": 99,
    "panel": "dev",
    "id": "p22official21:dev:eea:248",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Until 31 December 2004, the competent authorities may allow institutions to calculate their own-funds requirement by multiplying by 8 % the amount by which the sum of the overall net foreign-exchange position and the net gold position exceeds 2 % of the total own funds.",
    "reference": "Fram til 31. desember 2004 geta lögbær yfirvöld heimilað stofnunum að reikna út eiginfjárkröfu sína með því að margfalda með 8% þá fjárhæð sem samtala nettógjaldeyrisstöðu og nettógullstöðu er umfram 2% af samanlögðu eigin fé.",
    "grade": "A",
    "note": "Until31Dec2004,8percent of net FX+gold excess above2percent funds retained."
  },
  {
    "card": 100,
    "panel": "dev",
    "id": "p22official21:dev:eea:1636",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "In December 2005 the Justice and Home Affairs Council called upon the Commission to make a proposal for a European programme for critical infrastructure protection (‘EPCIP) and decided that it should be based on an all- hazards approach while countering threats from terrorism as a priority.",
    "reference": "Í desember 2005 bað dóms- og innanríkismálaráðið framkvæmdastjórnina um að gera tillögu að Evrópuáætlun um vernd þýðingarmikilla grunnvirkja og ákvað að miða hana við alla áhættuþætti en forvarnarstarf gegn hryðjuverkaárásum yrði sett í forgang.",
    "grade": "A",
    "note": "Dec2005 Council request for critical infrastructure program, all-hazards/terrorism priority retained."
  },
  {
    "card": 101,
    "panel": "dev",
    "id": "p22official21:dev:eea:241",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "In the case of transactions in which debt instruments, equities and commodities (excluding repurchase and reverse repurchase agreements and securities or commodities lending and securities or commodities borrowing) are unsettled after their due delivery dates, an institution must calculate the price difference to which it is exposed.",
    "reference": "Þegar um er að ræða viðskipti þar sem skuldaskjöl, hlutabréf og hrávörur (að undanskildum endurkaupasamningum og endursölusamningum og verðbréfa- eða hrávörulánveitingu og verðbréfa- eða hrávörulántökum) eru óuppgerð eftir að afhendingarfrestur er runninn út verður stofnunin að reikna út verðmismuninn.",
    "grade": "A",
    "note": "Unsettled debt/equities/commodities after delivery, repo/lending exclusions and price difference exposure retained."
  },
  {
    "card": 102,
    "panel": "dev",
    "id": "p22official21:dev:ema:2906",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "In four placebo-controlled studies, treatment with empagliflozin as monotherapy or add-on therapy to metformin, pioglitazone, or metformin plus a sulfonylurea resulted in mean changes from baseline in FPG of -20.5 mg/dl [-1.14 mmol/l] for empagliflozin 10 mg and -23.2 mg/dl [-1.29 mmol/l] for empagliflozin 25 mg compared to placebo (7.4 mg/dl [0.41 mmol/l]).",
    "reference": "Í fjórum samanburðarrannsóknum með lyfleysu leiddi einlyfjameðferð með empagliflozini eða viðbótarmeðferð samhliða metformíni, píóglítasóni eða metformíni auk súlfónýlúrealyfs til meðalbreytinga frá grunnlínu á fastandi plasmaglúkósa um -20,5 mg/dl [-1,14 mmól/l] með 10 mg af empagliflozini og -23,2 mg/dl [-1,29 mmól/l] með 25 mg af empagliflozini samanborið við lyfleysu (7,4 mg/dl [0,41 mmól/l]).",
    "grade": "A",
    "note": "Four trials, therapy combinations, both empagliflozin doses, negative FPG changes and placebo values retained."
  },
  {
    "card": 103,
    "panel": "dev",
    "id": "p22official21:dev:ema:850",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "When Edarbi is taken with chlortalidone (a water tablet), higher levels of certain chemicals in the blood (such as creatinine), which are indicators of kidney function, have been seen commonly (in less than 1 in 10 users), and low blood pressure is also common.",
    "reference": "Þegar Edarbi er tekið með klórtalidóni (vatnslosandi töflu), er algengt að hærri þéttni vissra efna í blóði (svo sem kreatíníns) sem eru mælikvarðar fyrir nýrnastarfsemi komi fram (hjá innan við 1 af hverjum 10 notendum) og lágur blóðþrýstingur er einnig algengur.",
    "grade": "A",
    "note": "Edarbi+chlortalidone renal chemicals/creatinine, <1/10 and common low BP retained."
  },
  {
    "card": 104,
    "panel": "dev",
    "id": "p22official21:dev:eea:47",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Where on the basis of soil dissipation studies it is established that DT901 > one year and where repeated application is envisaged, whether in the same growing season or in succeeding years, the possibility of accumulation of residues in soil and the level at which a plateau concentration is achieved must be investigated except where reliable information can be provided by a model calculation or another appropriate assessment.",
    "reference": "Hafi komið í ljós við rannsóknir á dreifingu í jarðvegi að DT50f er meira en eitt ár og endurtekin meðhöndlun er ráðgerð, hvort heldur sem er á sama ræktunartímabili eða á komandi árum, skal rannsaka hvort hugsanlegt er að efnaleifar hafi safnast fyrir í jarðveginum og finna þrepið þar sem stöðugum styrk er náð, nema unnt sé að fá áreiðanlegar upplýsingar með því að nota reiknilíkan eða annað mat sem hentar.",
    "grade": "R",
    "note": "Source DT901 versus reference DT50f materially different endpoint/OCR corruption; unsuitable trusted reference."
  },
  {
    "card": 105,
    "panel": "dev",
    "id": "p22official21:dev:eea:1744",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "To that effect, the SSCA should provide before the next meeting of the Air Safety Committee in November 2008 all relevant information regarding the implementation of corrective actions addressing the identified safety deficiencies by ICAO, failing which, the Commission will be compelled to decide the inclusion of all carriers licensed in Cambodia in Annex A.",
    "reference": "Í því skyni er rétt að skrifstofa flugmálayfirvalda leggi fram allar viðeigandi upplýsingar fyrir næsta fund Flugöryggisnefndarinnar í nóvember 2008 að því er varðar framkvæmd aðgerða til úrbóta á öryggisannmörkum sem Alþjóðaflugmálastofnunin hefur komist að raun um að séu fyrir hendi en sé það ekki gert er framkvæmdastjórninni nauðugur einn kostur að ákveða að skrá alla flugrekendur sem hafa fengið leyfi í Kambódíu í viðauka A.",
    "grade": "A",
    "note": "SSCA corrective actions before Nov2008 meeting and otherwise all Cambodian carriers AnnexA retained."
  },
  {
    "card": 106,
    "panel": "dev",
    "id": "p22official21:dev:eea:1987",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "AG14I The cash flows and contractual terms and conditions of a transaction between the instrument holder (in the role as a non-owner) and the issuing entity must be similar to an equivalent transaction that might occur between a non-instrument holder and the issuing entity.",
    "reference": "AG14I Sjóðstreymi, samningsskilmálar og skilyrði færslu á milli handhafa gernings (ekki í hlutverki eiganda) og útgáfueiningar verða að vera sambærileg við jafngild viðskipti sem gætu átt sér stað á milli aðila, sem er ekki handhafi gernings, og útgáfueiningar.",
    "grade": "A",
    "note": "AG14I non-owner holder/issuer cashflow and contractual comparability with nonholder retained."
  },
  {
    "card": 107,
    "panel": "dev",
    "id": "p22official21:dev:eso:136",
    "stratum": "technical_long",
    "subcorpus": "eso",
    "source": "Using these longer wavelengths allows astronomers to study extremely cold objects in space - such as the dense clouds of cosmic dust and gas from which stars and planets form - as well as very distant objects in the early Universe.",
    "reference": "Stjörnufræðingar geta notað þessar löngu bylgjulengdir ljóss til að rannsaka köldustu fyrirbærin í geimnum - til dæmis þétt gas- og rykský sem stjörnur og reikistjörnur verða til úr - en líka fjarlægustu fyrirbærin frá árdögum alheims.",
    "grade": "A",
    "note": "Longer wavelengths, very cold dust/gas star-forming objects and early-universe distant objects retained."
  },
  {
    "card": 108,
    "panel": "dev",
    "id": "p22official21:dev:ema:723",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "The recommendations given for concomitant use of darunavir and other medicinal products may therefore differ depending on whether darunavir is boosted with ritonavir or cobicistat (see sections 4.3 and 4.4), and caution is also required during the first time of treatment if switching the pharmacoenhancer from ritonavir to cobicistat (see section 4.4).",
    "reference": "Leiðbeiningar sem eru gefnar um samhliða notkun darunavirs og annarra lyfja geta því verið mismunandi eftir því hvort darunavir er örvað með ritonaviri eða cobicistati (sjá kafla 4.3 og 4.4) og einnig er nauðsynlegt að sýna aðgát í upphafi meðferðar ef lyfinu sem hefur jákvæð áhrif á lyfjahvörf er skipt úr ritonaviri í cobicistat (sjá kafla 4.4).",
    "grade": "A",
    "note": "Darunavir interactions differ by ritonavir/cobicistat, switch caution and sections retained."
  }
]
```

</details>

<details><summary>Full reference audit: test</summary>

```json
[
  {
    "card": 109,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:1715",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "Break it up, I tell you.",
    "reference": "Ég sagði, hættið að slást.",
    "grade": "A",
    "note": "Break it up idiom rendered stop fighting, acceptable conventional imperative."
  },
  {
    "card": 110,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:1892",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "You mean the other one's here too?",
    "reference": "Áttu við að hinn sé líka hér?",
    "grade": "A",
    "note": "Other one also here question retained."
  },
  {
    "card": 111,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:2999",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "I want you to train me.",
    "reference": "Ég vil að þú þjálfir mig.",
    "grade": "A",
    "note": "Want you to train me retained."
  },
  {
    "card": 112,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:1119",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "He sent me ahead with the others, while he and Geronimo remained behind.",
    "reference": "Hann sendi mig með hinum meðan hann og Geronimo urðu eftir.",
    "grade": "A",
    "note": "Sent ahead with others while he/Geronimo remain retained; ahead implicit departure contrast."
  },
  {
    "card": 113,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:3656",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "No, I will die here.",
    "reference": "Nei, ég kýs að deyja hér.",
    "grade": "U",
    "note": "Will die here rendered choose to die here; volitional reading uncertain without context."
  },
  {
    "card": 114,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:1258",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "It has to mean something.",
    "reference": "Hún hlýtur að hafa merkingu.",
    "grade": "A",
    "note": "Must mean something retained; grammatical gender of it context-dependent but no semantic claim changed."
  },
  {
    "card": 115,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:1579",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "But we have a war to win.",
    "reference": "En við verðum að vinna stríðið.",
    "grade": "A",
    "note": "War to win/need win war retained."
  },
  {
    "card": 116,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:3227",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "You're not supposed to use your powers outside of school.",
    "reference": "Þú mátt ekki nota kraftana utan skólans.",
    "grade": "A",
    "note": "Prohibition using powers outside school retained."
  },
  {
    "card": 117,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:354",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "Hey, Johnny, I just had a great idea.",
    "reference": "Johnny, ég fékk frábæra hugmynd.",
    "grade": "A",
    "note": "Johnny and new great idea retained, vocative/emphasis omitted only."
  },
  {
    "card": 118,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:518",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "Lewis, Diane, there's someone I'd like you to meet.",
    "reference": "Lewis, Diane, mig langar að kynna ykkur fyrir fólki.",
    "grade": "R",
    "note": "Someone to meet rendered plural people; number/reference altered."
  },
  {
    "card": 119,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:3355",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "He knows that Sicily, not Sardinia, has always been the key to Italy.",
    "reference": "Hann veit að Sikiley, ekki Sardinía, er lykillinn að Ítalíu.",
    "grade": "A",
    "note": "Knows Sicily not Sardinia key to Italy retained; always emphasis omitted."
  },
  {
    "card": 120,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:1951",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "How do you feel about that?",
    "reference": "Hvað finnst þér um það?",
    "grade": "A",
    "note": "How feel about that question retained."
  },
  {
    "card": 121,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:1162",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "I don't know why you're torturing him.",
    "reference": "Ég veit ekki hvers vegna þú kvelur hann.",
    "grade": "A",
    "note": "Do not know why torturing him retained."
  },
  {
    "card": 122,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:454",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "If they're a benefit, it's not my problem.",
    "reference": "Ef þær koma að gagni, kemur mér það ekki við.",
    "grade": "A",
    "note": "If beneficial not my concern retained."
  },
  {
    "card": 123,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:115",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "But, Sonny, you work in a tollbooth.",
    "reference": "En þú innheimtir vegtoll, Sonny.",
    "grade": "A",
    "note": "Sonny works collecting tolls retained."
  },
  {
    "card": 124,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:3567",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "I swear, he leers at my tits one more time, he's gonna regret it.",
    "reference": "Ef hann starir á brjóstin mín aftur þá mun hann sjá eftir því.",
    "grade": "A",
    "note": "Conditional next stare at breasts and threat of regret retained; swear emphasis omitted."
  },
  {
    "card": 125,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:685",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "Oh man, I have been banned from banks for like the next 7 years, and there is a guy down state willing to sell me a human skull, but he says all I have to do is send him a check.",
    "reference": "Ég er í bankabanni næstu 7 árin og það er maður sem vill selja mér hauskúpu úr manni en hann segir að ég verði að senda honum ávísun.",
    "grade": "A",
    "note": "Seven-year banking ban, skull seller and check requirement retained; downstate location omitted as minor setting detail."
  },
  {
    "card": 126,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:3682",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "At any rate, not for some weeks.",
    "reference": "Að minnsta kosti ekki í nokkrar vikur.",
    "grade": "A",
    "note": "Not for several weeks retained."
  },
  {
    "card": 127,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:373",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "We are not adorable, okay?",
    "reference": "Við erum ekki sæt, ókei?",
    "grade": "A",
    "note": "We not adorable retained."
  },
  {
    "card": 128,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:1",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "Everyone present, sir, but the surgeon.",
    "reference": "Já, herra, allir nema læknirinn.",
    "grade": "A",
    "note": "Everyone except surgeon/doctor present retained."
  },
  {
    "card": 129,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:530",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "I want you to meet Betty.",
    "reference": "Ég vil þú hittir Betty.",
    "grade": "A",
    "note": "Want you meet Betty retained despite minor missing conjunction."
  },
  {
    "card": 130,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:3309",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "I was born normal, but this woman deliberately ruined me.",
    "reference": "Ég fæddist eðlilegur en þessi kona hér hefur vísvitandi eyðilagt mig.",
    "grade": "A",
    "note": "Born normal, woman deliberately ruined speaker retained."
  },
  {
    "card": 131,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:1916",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "Either we call backup, or get out of here.",
    "reference": "Biðjum um aðstoð eða förum héðan.",
    "grade": "A",
    "note": "Call backup or leave alternatives retained."
  },
  {
    "card": 132,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:779",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "I didn‘t argue with her.",
    "reference": "Ég þrætti ekki við hana.",
    "grade": "A",
    "note": "Did not argue with her retained."
  },
  {
    "card": 133,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:3575",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "Who's that at this hour of the night?",
    "reference": "Hver er þetta svona síðla kvölds?",
    "grade": "A",
    "note": "Who at late hour of night question retained."
  },
  {
    "card": 134,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:3625",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "Max, is this just an excuse to grope Marcy?",
    "reference": "Max, er þetta afsökun til að káfa á Marcy?",
    "grade": "A",
    "note": "Max excuse to grope Marcy retained."
  },
  {
    "card": 135,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:1566",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "What if we play into this thing?",
    "reference": "Hvað ef við spilum í þetta?",
    "grade": "U",
    "note": "Play into this thing idiom unclear without context; literal Icelandic not reliable standalone reference."
  },
  {
    "card": 136,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:2717",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "This is just two people talking?",
    "reference": "Erum við bara tvær manneskjur að spjalla?",
    "grade": "A",
    "note": "Just two people talking question retained."
  },
  {
    "card": 137,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:2565",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "No, I meant Vince Vaughn.",
    "reference": "Ég átti við Vince Vaughn.",
    "grade": "A",
    "note": "Correcting intended referent to Vince Vaughn retained; initial no discourse particle omitted."
  },
  {
    "card": 138,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:1924",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "You seem like a really nice person, but were you pregnant last week?",
    "reference": "Þú virðist vera indæl manneskja en varstu ófrísk í síðustu viku?",
    "grade": "A",
    "note": "Nice person but pregnant last week question retained."
  },
  {
    "card": 139,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:1312",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "So, sure, he can't stomach your telling him what to do.",
    "reference": "Hann þolir ekki að þú segir honum fyrir verkum.",
    "grade": "A",
    "note": "Cannot stomach being told what to do retained."
  },
  {
    "card": 140,
    "panel": "test",
    "id": "p22official21:test:opensubtitles:2016",
    "stratum": "general",
    "subcorpus": "opensubtitles",
    "source": "They were unaware of this until they entered our planetary system.",
    "reference": "Þær vissu ekki af þessu fyrr en þær komu í okkar sólkerfi.",
    "grade": "A",
    "note": "Unaware until entering our planetary/solar system retained."
  },
  {
    "card": 141,
    "panel": "test",
    "id": "p22official21:test:eso:658",
    "stratum": "technical_short",
    "subcorpus": "eso",
    "source": "Galaxy clusters contain up to a thousand individual galaxies.",
    "reference": "Vetrarbrautaþyrpingar geta innihaldið meira en þúsund stakar vetrarbrautir.",
    "grade": "R",
    "note": "Up to1000 galaxies reversed to more than1000; inequality materially wrong."
  },
  {
    "card": 142,
    "panel": "test",
    "id": "p22official21:test:ema:60",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Always take Carbaglu exactly as your doctor has instructed you.",
    "reference": "Farið ætíð nákvæmlega eftir fyrirmælum læknis um skammtastærð.",
    "grade": "R",
    "note": "Carbaglu name entirely omitted and instruction narrowed to dosage; not reliable brand-sensitive reference."
  },
  {
    "card": 143,
    "panel": "test",
    "id": "p22official21:test:ema:1115",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Therefore, the combination should be administered with caution, especially in the elderly.",
    "reference": "Því skal nota þessar samsetningar með varúð, einkum hjá öldruðum.",
    "grade": "A",
    "note": "Combination cautious especially elderly retained."
  },
  {
    "card": 144,
    "panel": "test",
    "id": "p22official21:test:eso:933",
    "stratum": "technical_short",
    "subcorpus": "eso",
    "source": "Emission from a number of molecular gases was detected.",
    "reference": "Í mælingunum sást útgeislun frá ýmsum sameindum á gasformi.",
    "grade": "A",
    "note": "Detected emission from multiple molecular gases retained."
  },
  {
    "card": 145,
    "panel": "test",
    "id": "p22official21:test:eea:2003",
    "stratum": "technical_short",
    "subcorpus": "eea",
    "source": "After paragraph 136, a heading and paragraph 136A are inserted.",
    "reference": "Nýrri fyrirsögn og lið 136A er bætt við á eftir 136. lið.",
    "grade": "A",
    "note": "Heading and136A inserted after136 retained."
  },
  {
    "card": 146,
    "panel": "test",
    "id": "p22official21:test:ema:2860",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Take two tablets in the morning.",
    "reference": "Takið tvær töflur að morgni.",
    "grade": "A",
    "note": "Two tablets morning retained."
  },
  {
    "card": 147,
    "panel": "test",
    "id": "p22official21:test:ema:2985",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Pink, round and biconvex film-coated tablets.",
    "reference": "Bleikar, kringlóttar og tvíkúptar filmuhúðaðar töflur.",
    "grade": "A",
    "note": "Pink round biconvex film-coated tablet descriptors retained."
  },
  {
    "card": 148,
    "panel": "test",
    "id": "p22official21:test:ema:2134",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Never take your inhaler apart.",
    "reference": "Þú skalt aldrei taka innöndunartækið í sundur.",
    "grade": "A",
    "note": "Never dismantle inhaler retained."
  },
  {
    "card": 149,
    "panel": "test",
    "id": "p22official21:test:eea:1324",
    "stratum": "technical_short",
    "subcorpus": "eea",
    "source": "The weight of refill packaging shall not exceed 1,7 g per wash.",
    "reference": "Þyngd umbúða með áfyllingu skal ekki fara yfir 1,7 grömm á þvott.",
    "grade": "A",
    "note": "Refill packaging<=1.7g per wash retained."
  },
  {
    "card": 150,
    "panel": "test",
    "id": "p22official21:test:ema:973",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Most side effects are mild to moderate.",
    "reference": "Flestar aukaverkanirnar eru vægar eða miðlungs alvarlegar.",
    "grade": "A",
    "note": "Most adverse effects mild/moderate retained."
  },
  {
    "card": 151,
    "panel": "test",
    "id": "p22official21:test:ema:1945",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Pioglitazone should be discontinued if any deterioration in cardiac symptoms occurs.",
    "reference": "Hætta skal meðferð með pioglitazoni ef einkenni frá hjarta hjarta versna.",
    "grade": "R",
    "note": "Duplicated hjarta token indicates visible extraction/editorial damage; exclude without repairing reference."
  },
  {
    "card": 152,
    "panel": "test",
    "id": "p22official21:test:ema:144",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Consumption of alcohol and medicinal products containing alcohol should be avoided.",
    "reference": "Forðast skal neyslu áfengis og lyf sem innihalda alkóhól.",
    "grade": "A",
    "note": "Avoid alcohol and alcohol-containing medicines retained."
  },
  {
    "card": 153,
    "panel": "test",
    "id": "p22official21:test:ema:1153",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Concomitant use is contraindicated (see section 4.3).",
    "reference": "Samhliðanotkun er frábending (sjá kafla 4.3).",
    "grade": "A",
    "note": "Concomitant contraindication and4.3 retained."
  },
  {
    "card": 154,
    "panel": "test",
    "id": "p22official21:test:ema:1929",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Co-administration of Ribavirin Mylan and didanosine is not recommended.",
    "reference": "Samhliða gjöf Ribavirin Mylan og dídanósíns er ekki ráðlögð.",
    "grade": "A",
    "note": "Ribavirin Mylan+didanosine not recommended retained."
  },
  {
    "card": 155,
    "panel": "test",
    "id": "p22official21:test:ema:48",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "After preparing the Enbrel solution, immediate use is recommended.",
    "reference": "Ráðlagt er að nota Enbrel lausn strax eftir blöndun.",
    "grade": "A",
    "note": "Enbrel solution use immediately after preparation retained."
  },
  {
    "card": 156,
    "panel": "test",
    "id": "p22official21:test:ema:2673",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Always use a new needle for activation.",
    "reference": "Notaðu ávallt nýja nál við virkjunarferlið.",
    "grade": "A",
    "note": "Always new needle for activation retained."
  },
  {
    "card": 157,
    "panel": "test",
    "id": "p22official21:test:ema:1466",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Each capsule contains 80 mg of sucrose (in the 80 mg capsule).",
    "reference": "Hvert hylki inniheldur 80 mg af súkrósa (í 80 mg hylkinu).",
    "grade": "A",
    "note": "80mg sucrose in80mg capsule retained."
  },
  {
    "card": 158,
    "panel": "test",
    "id": "p22official21:test:eso:1067",
    "stratum": "technical_short",
    "subcorpus": "eso",
    "source": "The team tested several hypotheses to explain the unexpected change in speed.",
    "reference": "Stjörnufræðingarnir prófuðu ýmsar tilgátur til að útskýra þessa óvæntu hraðabreytingu.",
    "grade": "A",
    "note": "Team/astronomers tested hypotheses for unexpected speed change retained."
  },
  {
    "card": 159,
    "panel": "test",
    "id": "p22official21:test:ema:959",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Allergic type hypersensitivity reactions are possible with OBIZUR.",
    "reference": "Ofnæmisviðbrögð eru möguleg við notkun OBIZUR.",
    "grade": "A",
    "note": "OBIZUR possible allergic hypersensitivity retained."
  },
  {
    "card": 160,
    "panel": "test",
    "id": "p22official21:test:ema:484",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "No interaction studies have been performed with Cholib.",
    "reference": "Ekki hafa verið gerðar neinar rannsóknir á milliverkunum með Cholib.",
    "grade": "A",
    "note": "No Cholib interaction studies retained."
  },
  {
    "card": 161,
    "panel": "test",
    "id": "p22official21:test:ema:3088",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Cardboard box with 1 or 10 PET bottles of 10 doses.",
    "reference": "Pappaaskja með 1 eða 10 PET glösum sem innihalda 10 skammta.",
    "grade": "A",
    "note": "Cardboard box1or10PET bottles of10doses retained."
  },
  {
    "card": 162,
    "panel": "test",
    "id": "p22official21:test:ema:1359",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Proteinuria has been observed with cabozantinib.",
    "reference": "Prótein í þvagi hefur komið fram við notkun cabozantinibs.",
    "grade": "A",
    "note": "Cabozantinib-associated proteinuria retained."
  },
  {
    "card": 163,
    "panel": "test",
    "id": "p22official21:test:ema:1443",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "It might be necessary to postpone the vaccination until recovery.",
    "reference": "Hugsanlega er nauðsynlegt að fresta bólusetningu þar til barninu batnar.",
    "grade": "U",
    "note": "Reference adds child as recipient, absent source; context-dependent specificity excluded."
  },
  {
    "card": 164,
    "panel": "test",
    "id": "p22official21:test:ema:498",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Omidria is not recommended in women of childbearing potential not using contraception.",
    "reference": "Omidria er ekki ætlað til notkunar handa konum á barneignaraldri sem ekki nota getnaðarvarnir.",
    "grade": "U",
    "note": "Not recommended rendered not intended for use; medical recommendation strength uncertain, exclude conservative audit."
  },
  {
    "card": 165,
    "panel": "test",
    "id": "p22official21:test:ema:2646",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Metabolites and parent drug are excreted in the bile.",
    "reference": "Umbrotsefni og lyfið skiljast út með galli.",
    "grade": "A",
    "note": "Parent drug/metabolites biliary excretion retained."
  },
  {
    "card": 166,
    "panel": "test",
    "id": "p22official21:test:ema:1825",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Take your next normal dose at its scheduled time.",
    "reference": "Taktu næsta venjulega skammt á áætluðum tíma.",
    "grade": "A",
    "note": "Next normal dose at scheduled time retained."
  },
  {
    "card": 167,
    "panel": "test",
    "id": "p22official21:test:ema:1851",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Reduce next dose by 25%.",
    "reference": "Næsti skammtur minnkaður um 25%.",
    "grade": "A",
    "note": "Next dose reduction by25percent retained."
  },
  {
    "card": 168,
    "panel": "test",
    "id": "p22official21:test:ema:2053",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "Constipation may be a preceding symptom.",
    "reference": "Hægðatregða er hugsanlegt undanfarandi sjúkdómseinkenni.",
    "grade": "A",
    "note": "Constipation possible preceding symptom retained."
  },
  {
    "card": 169,
    "panel": "test",
    "id": "p22official21:test:eea:1609",
    "stratum": "technical_short",
    "subcorpus": "eea",
    "source": "Enhancing cooperation, exchange of information, experience and best practices between stakeholders.",
    "reference": "Að bæta samstarf og skipti á upplýsingum, reynslu og bestu starfsvenjum milli hagsmunaaðila.",
    "grade": "A",
    "note": "Stakeholder cooperation/info/experience/best practices exchange retained."
  },
  {
    "card": 170,
    "panel": "test",
    "id": "p22official21:test:ema:1828",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "The use of classical swine fever vaccines is prohibited.",
    "reference": "Notkun bóluefna gegn svínapest er bönnuð.",
    "grade": "A",
    "note": "Classical swine fever vaccine use prohibited retained."
  },
  {
    "card": 171,
    "panel": "test",
    "id": "p22official21:test:eea:891",
    "stratum": "technical_short",
    "subcorpus": "eea",
    "source": "In some cases, ovarian fluid must be examined (Tables 1A to C).",
    "reference": "Í sumum tilfellum verður að rannsaka hrognavökva (tafla 1A–C).",
    "grade": "A",
    "note": "Some cases ovarian fluid examined and1A-C tables retained."
  },
  {
    "card": 172,
    "panel": "test",
    "id": "p22official21:test:eso:98",
    "stratum": "technical_short",
    "subcorpus": "eso",
    "source": "The VST will make three public surveys over the next five years.",
    "reference": "Á næstu fimm árum verða unnin þrjú opinber kortlagningarverkefni með VST.",
    "grade": "A",
    "note": "VST three public surveys next5years retained."
  },
  {
    "card": 173,
    "panel": "test",
    "id": "p22official21:test:ema:1751",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "High density polyethylene (HDPE) bottle, capped with a polypropylene child-resistant closure, containing 60 film-coated tablets and a polyester coil.",
    "reference": "Glas úr háþéttni pólýetýleni (HDPE), með pólýprópýlen barnaöryggisloki, sem inniheldur 60 filmuhúðaðar töflur og pólýester vafning.",
    "grade": "A",
    "note": "HDPE/polypropylene childproof closure,60film tablets/polyester coil retained."
  },
  {
    "card": 174,
    "panel": "test",
    "id": "p22official21:test:eso:162",
    "stratum": "technical_medium",
    "subcorpus": "eso",
    "source": "It is bright and recognisable enough to be seen even in observations of very faint and faraway galaxies.",
    "reference": "Hún er björt og auðþekkjanleg, jafnvel í ljósi mjög daufra og fjarlægra vetrarbrauta.",
    "grade": "A",
    "note": "Bright recognizable signal even faint/distant galaxy light retained; observations phrased in light."
  },
  {
    "card": 175,
    "panel": "test",
    "id": "p22official21:test:eso:431",
    "stratum": "technical_medium",
    "subcorpus": "eso",
    "source": "The special filter for observing hydrogen emission was kindly made available by the VPHAS+ Consortium.",
    "reference": "VPHAS+ samstarfið lagði góðfúslega fram síuna sem notuð var til að safna vetnisljómuninni.",
    "grade": "A",
    "note": "VPHAS+ consortium supplied hydrogen emission filter retained."
  },
  {
    "card": 176,
    "panel": "test",
    "id": "p22official21:test:ema:116",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "Cases of photosensitivity reactions have been reported with thiazides diuretics (see section 4.8).",
    "reference": "Greint hefur verið frá tilfellum um ljósnæmisviðbrögð við gjöf tíazíð þvagræsilyfja (sjá kafla 4.8).",
    "grade": "A",
    "note": "Thiazide photosensitivity reports and4.8 retained."
  },
  {
    "card": 177,
    "panel": "test",
    "id": "p22official21:test:ema:1705",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "The elimination of unchanged cysteamine in the urine has been shown to range between 0.3 % and 1.7% of the total daily dose in four patients; the bulk of cysteamine is excreted as sulphate.",
    "reference": "Sýnt var fram á að útskilnaður óbreytts cysteamíns í þvag er á bilinu 0,3% til 1,7% af heildardagsskammti fjögurra sjúklinga; meginhluti cysteamíns er skilinn út sem súlfat.",
    "grade": "A",
    "note": "Unchanged urine cysteamine0.3-1.7percent daily in4patients, bulk sulfate retained."
  },
  {
    "card": 178,
    "panel": "test",
    "id": "p22official21:test:eso:215",
    "stratum": "technical_medium",
    "subcorpus": "eso",
    "source": "It shows not just the brilliant massive stars, but hundreds of thousands of much fainter stars that were previously invisible.",
    "reference": "Á henni sjást ekki einungis skærar og massamiklar stjörnur heldur mörg hundruð þúsund miklu daufari stjörnur sem voru áður ósýnilegar.",
    "grade": "A",
    "note": "Bright massive plus hundreds thousands fainter previously invisible stars retained."
  },
  {
    "card": 179,
    "panel": "test",
    "id": "p22official21:test:ema:1873",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "In very rare cases, allergic reactions, some severe, sometimes with difficulty in breathing, have been reported and may require immediate medical care.",
    "reference": "Örsjaldan hefur verið tilkynnt um ofnæmisviðbrögð, sum alvarleg stundum með öndunarörðugleikum, sem gætu þurft tafarlausa læknismeðferð.",
    "grade": "A",
    "note": "Very rare severe allergy/breathing difficulty may require immediate care retained."
  },
  {
    "card": 180,
    "panel": "test",
    "id": "p22official21:test:eea:1388",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "Port security plans shall be approved by the Member State concerned before implementation.",
    "reference": "Hlutaðeigandi aðildarríki skal samþykkja verndaráætlanir hafna áður en þeim er hrint í framkvæmd.",
    "grade": "A",
    "note": "Member-state port security approval before implementation retained."
  },
  {
    "card": 181,
    "panel": "test",
    "id": "p22official21:test:eso:830",
    "stratum": "technical_medium",
    "subcorpus": "eso",
    "source": "All three telescopes recorded a sudden drop in brightness as Eris blocked the light of the distant star.",
    "reference": "Allir sjónaukarnir þrír mældu skyndilega birtuminnkun stjörnunnar þegar Eris gekk fyrir hana.",
    "grade": "A",
    "note": "Three telescopes sudden dimming due Eris occulting star retained."
  },
  {
    "card": 182,
    "panel": "test",
    "id": "p22official21:test:ema:151",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "Correspondingly, the incidences of nocturnal hypoglycaemia were 32% in the insulin glargine / lispro group versus 52% in the NPH / regular group.",
    "reference": "Samsvarandi tíðni blóðsykursfalls að nóttu var 32% í glargíninsúlín/líspró hópnum á móti 52% í NPH/ venjulega hópnum.",
    "grade": "A",
    "note": "Nocturnal hypoglycemia32vs52percent and glargine/lispro vsNPH/regular groups retained."
  },
  {
    "card": 183,
    "panel": "test",
    "id": "p22official21:test:eea:2142",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "The Commission shall evaluate the operation of this Decision on the basis of available information three years after its adoption.",
    "reference": "Framkvæmdastjórnin skal meta framkvæmd ákvörðunar þessarar á grundvelli fyrirliggjandi upplýsinga þremur árum eftir samþykkt hennar.",
    "grade": "A",
    "note": "Commission operation evaluation based available information3years after adoption retained."
  },
  {
    "card": 184,
    "panel": "test",
    "id": "p22official21:test:ema:2345",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "This was confirmed in rats with partial urethral obstruction, where mirabegron decreased the frequency of non-voiding contractions without affecting the voided volume per micturition, voiding pressure, or residual urine volume.",
    "reference": "Þetta var staðfest hjá rottum sem höfðu hindrun að hluta til í þvagrás, þar sem mirabegron lækkaði tíðni samdrátta án þvagláts án þess að hafa áhrif á rúmmál þvags í hverju þvagláti, þvaglátsþrýsting eða rúmmál þvagsins sem eftir var í blöðrunni.",
    "grade": "A",
    "note": "Partial rat urethral obstruction, fewer nonvoid contractions, unchanged volumes/pressure retained."
  },
  {
    "card": 185,
    "panel": "test",
    "id": "p22official21:test:ema:2302",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "At week 16, all ACR Ped components demonstrated clinically relevant improvement from baseline (see Table 8).",
    "reference": "Í 16. viku sýndu allir þættir ACR Ped ávinning sem skipti máli klínískt frá grunnlínu (sjá töflu 8).",
    "grade": "A",
    "note": "Week16 allACR Ped components clinically relevant improvement andTable8 retained."
  },
  {
    "card": 186,
    "panel": "test",
    "id": "p22official21:test:ema:2586",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "Non-clinical data from cynomolgus monkeys revealed no special hazards for humans based on repeat- dose toxicity studies, safety pharmacology evaluations, and reproductive and developmental toxicity studies.",
    "reference": "Forklínískar upplýsingar úr rannsóknum á cynomolgus-öpum sýndu ekki fram á sérstaka áhættu fyrir menn á grundvelli rannsókna á eiturverkunum eftir endurtekna skammta, lyfjafræðilegu öryggi og eiturverkunum á æxlun og þroska.",
    "grade": "A",
    "note": "Cynomolgus preclinical no special human hazard, repeated-dose/safety/reproduction/development retained."
  },
  {
    "card": 187,
    "panel": "test",
    "id": "p22official21:test:eea:198",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "The results of the audits and reviews should be brought to the attention of all personnel having responsibility in the area involved.",
    "reference": "Niðurstöður endurskoðana og endurmats skulu kynntar þeim starfsmönnum sem bera ábyrgð á viðkomandi svæði.",
    "grade": "A",
    "note": "Audit/review results brought to responsible personnel retained."
  },
  {
    "card": 188,
    "panel": "test",
    "id": "p22official21:test:ema:2995",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "The treatment-free period, however, should take into account the pharmacological properties of the veterinary products used previously.",
    "reference": "Meðferðarlausa tímabilið verður þó að taka mið af lyfjafræðilegum eiginleikum þeirra dýralyfja sem voru notuð áður.",
    "grade": "A",
    "note": "Treatment-free period considers prior veterinary drugs pharmacological properties retained."
  },
  {
    "card": 189,
    "panel": "test",
    "id": "p22official21:test:eso:546",
    "stratum": "technical_medium",
    "subcorpus": "eso",
    "source": "The strikingly different colours of NGC 2014 and NGC 200 are the result of both the different chemical makeup of the surrounding gas and the temperatures of the stars that are causing the clouds to glow.",
    "reference": "Litamuninn á NGC 2014 og NGC 200 má bæði rekja til mismunandi efnasamsetningar gassins í kring og hitastigs stjarnanna sem lýsa upp skýin.",
    "grade": "A",
    "note": "Both NGC identifiers, different colors from gas chemistry and illuminating star temperatures retained; astronomical factual truth not independently certified."
  },
  {
    "card": 190,
    "panel": "test",
    "id": "p22official21:test:eso:605",
    "stratum": "technical_medium",
    "subcorpus": "eso",
    "source": "The new estimate is based on detailed observations of two slightly different forms of water in Marss atmosphere.",
    "reference": "Nýja matið er byggt á nákvæmum mælingum á tveimur mismunandi gerðum vatns í lofthjúpi Mars.",
    "grade": "A",
    "note": "Estimate based on two water forms measured in Mars atmosphere retained."
  },
  {
    "card": 191,
    "panel": "test",
    "id": "p22official21:test:ema:3131",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "This can lead to swelling of the clear layer in the front of the eye and cause blurred vision.",
    "reference": "Þetta getur valdið bólgu í glæra laginu framan á auganu og valdið óskýrri sjón.",
    "grade": "A",
    "note": "Swelling clear front eye layer and blurred vision retained."
  },
  {
    "card": 192,
    "panel": "test",
    "id": "p22official21:test:ema:2726",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "The ALIMTA maintenance safety profiles from the two studies JMEN and PARAMOUNT were similar.",
    "reference": "Öryggissnið fyrir ALIMTA sem viðhaldsmeðferð var svipað í JMEN og PARAMOUNT rannsóknunum.",
    "grade": "A",
    "note": "ALIMTA maintenance safety similarity JMEN/PARAMOUNT retained."
  },
  {
    "card": 193,
    "panel": "test",
    "id": "p22official21:test:eea:931",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "Following rinsing with PBS-Tween-20 buffer, biotinylated antibodies of a specificity corresponding to that of the coating antibodies are added and allowed to react for 60 minutes at 20 °C.",
    "reference": "Eftir skolun með PBS-Tween-20 jafnalausn er bíótínuðum mótefnum, með sérhæfni sem svarar til sérhæfni húðunarefnanna, bætt við og leyft að bindast í 60 mínútur við 20 °C.",
    "grade": "A",
    "note": "PBS-Tween20 rinse, specificity-matched biotin antibodies,60min20C retained."
  },
  {
    "card": 194,
    "panel": "test",
    "id": "p22official21:test:eso:272",
    "stratum": "technical_medium",
    "subcorpus": "eso",
    "source": "There is also possibly a very much fainter trace of a counter jet extending to the lower right.",
    "reference": "Í neðra hægra horninu eru svo merki um enn daufari gagnstæðan strók.",
    "grade": "R",
    "note": "Possibly faint counterjet trace rendered definite evidence; scientific uncertainty materially strengthened."
  },
  {
    "card": 195,
    "panel": "test",
    "id": "p22official21:test:eso:422",
    "stratum": "technical_medium",
    "subcorpus": "eso",
    "source": "This new telescope is the largest telescope in the world exclusively dedicated to surveying the sky at visible wavelengths (eso1119).",
    "reference": "Þessi nýi sjónauki er sá stærsti í heiminum sem helgaður er kortlagningu himins í sýnilegu ljósi (eso1119).",
    "grade": "A",
    "note": "World-largest telescope dedicated visible sky survey andeso1119 retained."
  },
  {
    "card": 196,
    "panel": "test",
    "id": "p22official21:test:eea:1272",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "The Commission shall make available to the Agency any information the latter considers relevant to that evaluation.",
    "reference": "Framkvæmdastjórnin skal láta stofnuninni í té hvers kyns upplýsingar sem stofnunin telur að skipti máli í tengslum við matið.",
    "grade": "A",
    "note": "Commission provides Agency information latter considers relevant retained."
  },
  {
    "card": 197,
    "panel": "test",
    "id": "p22official21:test:ema:2285",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "Angiotensin II is the principal pressor agent of the RAAS, with effects that include vasoconstriction, stimulation of synthesis and release of aldosterone, cardiac stimulation, and renal reabsorption of sodium.",
    "reference": "Angíótensín II er helsta þrýstingsvaldandi efnið í RAAS og eru helstu áhrif þess æðasamdráttur, örvun nýmyndunar og losunar aldósteróns, hjartaörvun og endurupptaka natríums í nýrum.",
    "grade": "A",
    "note": "AngiotensinII RAAS principal pressor, vasoconstriction/aldosterone/cardiac/renal sodium effects retained."
  },
  {
    "card": 198,
    "panel": "test",
    "id": "p22official21:test:ema:1682",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "Antithrombin, a 58 kD, 432 amino-acid glycoprotein, belongs to the serpin (serine protease inhibitor) superfamily.",
    "reference": "Andtrombín, sem er 58kD, 432 amínósýru glýkóprótein, tilheyrir serpín (serín próteasa hemla) stórfjölskyldunni.",
    "grade": "A",
    "note": "Antithrombin58kD432aminoacid glycoprotein serpin superfamily retained."
  },
  {
    "card": 199,
    "panel": "test",
    "id": "p22official21:test:ema:1795",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "Take Xarelto on a regular basis and for as long as your doctor keeps prescribing it.",
    "reference": "Taktu Xarelto reglulega, svo lengi sem læknirinn segir þér að gera það.",
    "grade": "A",
    "note": "Regular Xarelto for as long as prescribed retained."
  },
  {
    "card": 200,
    "panel": "test",
    "id": "p22official21:test:eea:1702",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "A potential ECI which does not satisfy the cross-cutting criteria will not be considered to be an ECI.",
    "reference": "Hugsanlegt þýðingarmikið grunnvirki í Evrópu, sem ekki uppfyllir þverlægu viðmiðanirnar, skal ekki teljast þýðingarmikið grunnvirki í Evrópu.",
    "grade": "A",
    "note": "ECI failing cross-cutting criteria not ECI retained; abbreviation expanded."
  },
  {
    "card": 201,
    "panel": "test",
    "id": "p22official21:test:eso:398",
    "stratum": "technical_medium",
    "subcorpus": "eso",
    "source": "The majority of planet candidates detected by this transit method are very distant from us.",
    "reference": "Þær reikistjörnur sem hafa fundist með þessari þvergönguaðferð eru alla jafna mjög fjarlægar.",
    "grade": "R",
    "note": "Planet candidates become planets found, losing unconfirmed status; exclude scientific reference overstatement."
  },
  {
    "card": 202,
    "panel": "test",
    "id": "p22official21:test:ema:1883",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "Taking ABILIFY tablets with some medicines may need to change your dose of ABILIFY tablets.",
    "reference": "Þegar ABILIFY töflur eru teknar með sumum lyfjum getur þurft að breyta ABILIFY töfluskammtinum.",
    "grade": "A",
    "note": "Some concurrent drugs may require ABILIFY dose change retained."
  },
  {
    "card": 203,
    "panel": "test",
    "id": "p22official21:test:ema:1681",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "After disease flare, children received Simponi 30 mg/m2 (maximum 50 mg) + MTX.",
    "reference": "Eftir að sjúkdómurinn blossaði upp fengu börnin 30 mg/m2 af Simponi (hámark 50 mg) + metótrexat.",
    "grade": "A",
    "note": "Children postflare Simponi30mg/m2 max50mg+MTX expanded methotrexate retained."
  },
  {
    "card": 204,
    "panel": "test",
    "id": "p22official21:test:ema:2335",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "Strimvelis is transported directly to the medical facility where the infusion will be administered.",
    "reference": "Strimvelis er flutt beint á sjúkrahúsið þar sem innrennslið er gefið.",
    "grade": "A",
    "note": "Strimvelis direct transport to infusion facility retained."
  },
  {
    "card": 205,
    "panel": "test",
    "id": "p22official21:test:ema:2334",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "Solutions of CINQAERO diluted in sodium chloride 9 mg/mL (0.9%) solution for infusion may be stored refrigerated at 2 °C-8 °C (or not above 25 °C if dilution has taken place in controlled and validated aseptic conditions), protected from light for up to 16 hours.",
    "reference": "Geyma má CINQAERO lausnir þynntar með natríum klóríð 9 mg/ml (0,9%) innrennslislyfi, lausn í kæli við 2°C-8°C (eða ekki við hærra hitastig en 25°C ef þynning hefur farið fram við stýrðar og gildaðar smitgátaraðstæður), varðar gegn ljósi í allt að 16 klst.",
    "grade": "A",
    "note": "CINQAERO NaCl9mg/mL0.9percent,2-8C or<=25C validated aseptic, light-protected<=16h retained."
  },
  {
    "card": 206,
    "panel": "test",
    "id": "p22official21:test:ema:342",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "If your dose is greater than the number of units left in the pen, you may either inject the amount remaining in your current pen and then use a new pen to complete your dose, OR inject the full dose with a new pen.",
    "reference": "Ef skammturinn þinn er meiri en þær einingar sem eftir eru í pennanum getur þú annað hvort sprautað því sem eftir er og notað síðan nýjan penna til að klára skammtinn EÐA nota nýjan penna fyrir allann skammtinn.",
    "grade": "A",
    "note": "Insufficient pen units: remainder+new to complete OR full new pen retained."
  },
  {
    "card": 207,
    "panel": "test",
    "id": "p22official21:test:eea:1295",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "The Competent Bodies are recommended to take into account the implementation of recognised environmental management schemes, such as EMAS or ISO 14001, when assessing applications and monitoring compliance with the criteria (note: it is not required to implement such management schemes).",
    "reference": "Mælt er með því að þar til bærar stofnanir taki tillit til þess, við mat á umsóknum og eftirlit með því að viðmiðanir séu uppfylltar, hvort viðurkenndum umhverfisstjórnunarkerfum, svo sem EMAS eða ISO 14001, er beitt (aths.: ekki er gerð krafa um að slíkum stjórnunarkerfum sé beitt).",
    "grade": "A",
    "note": "Competent bodies consider EMAS/ISO14001, not required, in assessment/compliance retained."
  },
  {
    "card": 208,
    "panel": "test",
    "id": "p22official21:test:eso:566",
    "stratum": "technical_long",
    "subcorpus": "eso",
    "source": "“Unless we are observing Beta Pictoris at a very unusual time, the carbon monoxide must be continuously replenished,” said Bill Dent, an ESO astronomer at the Joint ALMA Office in Santiago, Chile, and lead author on a paper published today in the journal Science.",
    "reference": "„Kolmónoxíðið hlýtur að vera í stöðugri endurnýjun við Beta Pictoris, nema við séum að rannsaka hana á mjög sérstöku tíma,“ sagði Bill Dent, stjörnufræðingur hjá ESO við Joint ALMA Office í Santiago í Chile, aðalhöfundur greinarinnar um rannsóknina sem birtist í dag í tímaritinu Science.",
    "grade": "A",
    "note": "Unless unusual epoch, continuously replenished CO near Beta Pictoris, Bill Dent/ESO/ALMA/Science retained."
  },
  {
    "card": 209,
    "panel": "test",
    "id": "p22official21:test:eea:237",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "In addition they may allow the requirement on a bought exchange-traded or OTC option to be the same as that for the instrument underlying it, subject to the constraint that the resulting requirement does not exceed the market value of the option.",
    "reference": "Að auki geta þau leyft að eiginfjárkrafan sem tengist kauprétti, sem verslað er með á verðbréfamarkaði eða kauprétti sem verslað er með utan verðbréfamarkaða, sé sú sama og fyrir skjalið sem liggur til grundvallar, að því tilskildu að krafan sem af því leiðir fari ekki yfir markaðsvirði kaupréttarins.",
    "grade": "R",
    "note": "Bought option denotes purchased option, not necessarily call; Icelandic kauprettur narrows generic instrument to call option."
  },
  {
    "card": 210,
    "panel": "test",
    "id": "p22official21:test:eea:633",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Employees are all persons who have a direct employment contract with the enterprise or local unit and receive remuneration, irrespective of the type of work performed, the number of hours worked (full or part-time) and the duration of the contract (fixed or indefinite).",
    "reference": "Launamenn eru þeir sem fyrirtækið eða starfsstöðin hefur gert beinan ráðningarsamning við og fá launagreiðslur, án tillits til þess hvers konar vinna er unnin, fjölda vinnustunda (hvort um er að ræða fullt starf eða hlutastarf) og tímabils samningsins (hvort hann er tímabundinn eða ótímabundinn).",
    "grade": "A",
    "note": "Employees direct contract+pay regardless work/hours/duration retained."
  },
  {
    "card": 211,
    "panel": "test",
    "id": "p22official21:test:ema:879",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "Your doctor should also monitor your liver function while you are being treated with VFEND by doing blood tests. you are known to have cardiomyopathy, irregular heart beat, slow heart rate or an abnormality of electrocardiogram (ECG) called ‘long QTc syndrome.",
    "reference": "Læknirinn ætti einnig að fylgjast með lifrarstarfseminni á meðan VFEND meðferð stendur með því að taka blóðprufur. fram hefur komið hjartavöðvakvilli, óreglulegur hjartsláttur, hægsláttur eða frávik á hjartarafriti (ECG), svokölluð lenging á QTc-bili.",
    "grade": "U",
    "note": "Concatenated liver monitoring and separate cardiac-history bullet lacks governing context; unsuitable standalone pair."
  },
  {
    "card": 212,
    "panel": "test",
    "id": "p22official21:test:eso:1000",
    "stratum": "technical_long",
    "subcorpus": "eso",
    "source": "These galaxies are known for a much higher rate of star formation compared to sedate Milky Way-like galaxies, making these structures ideal to study galaxy growth and the interplay between gas, dust, stars, and the black holes at the centres of galaxies.",
    "reference": "Þessar vetrarbrautir eru þekktar fyrir miklu örari stjörnumyndun samanborið við vetrarbrautir á borð við okkar eigin, sem gerir þær kjörnar til rannsókna á vexti vetrarbrauta og víxlverkunar gass, ryks, stjarna og svarthola í miðju þeirra.",
    "grade": "A",
    "note": "Higher star formation than Milky-Way-like galaxies, ideal growth/gas/dust/star/black-hole interplay retained."
  },
  {
    "card": 213,
    "panel": "test",
    "id": "p22official21:test:eso:595",
    "stratum": "technical_long",
    "subcorpus": "eso",
    "source": "The data were obtained by ALMA; the Combined Array for Research in Millimeter-wave Astronomy: a millimeter array consisting of 23 parabola antennas in California; the Submillimeter Array a submillimeter array consisting of eight parabola antennas in Mauna Kea, Hawaii; the Plateau de Bure Interferometer; the NAOJ Nobeyama Radio Observatory 45m radio telescope; USAs National Radio Astronomy Observatory 12m telescope; USA's Five College Radio Astronomy Observatory 14m telescope; IRAMs 30m telescope; and the Swedish-ESO Submillimeter Telescope as a supplement.",
    "reference": "Gögnum var aflað með ALMA; Combined Array for Research in Millimeter-wave Astronomy: Millímetraröð sem samanstendur af 23 loftnetum í Kaliforníu; Submillimeter Array, hálfsmillímetraröð sem samanstendur af átta loftnetum á Mauna Kea á Hawaii; Plateau de Bure Interferometer; 45 metra útvarpssjónauka NAOJ Nobeyama Radio Observatory; bandaríska 12 metra sjónauka National Radio Astronomy Observatory; bandaríska 14 metra sjónauka Five College Radio Astronomy Observatory; 30 metra sjónauka IRAM og auk þess Swedish-ESO Submillimeter Telescope.",
    "grade": "A",
    "note": "Full telescope list and23/8antenna,45/12/14/30m numbers retained; parabola descriptor implicit standard dish context."
  },
  {
    "card": 214,
    "panel": "test",
    "id": "p22official21:test:eea:1959",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Except as stated in paragraph 22A, a contract that will be settled by the entity (receiving or) delivering a fixed number of its own equity instruments in exchange for a fixed amount of cash or another financial asset is an equity instrument.",
    "reference": "Að undanskildu því sem tekið er fram í lið 22A er samningur, sem einingin gerir upp með því að (taka við eða) afhenda fastan fjölda eiginfjárgerninga sinna í skiptum fyrir fasta fjárhæð handbærs fjár eða annarrar fjáreignar, eiginfjárgerningur.",
    "grade": "A",
    "note": "Except22A fixed own-equity count for fixed cash/assets means equity retained."
  },
  {
    "card": 215,
    "panel": "test",
    "id": "p22official21:test:eea:326",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "To facilitate the mutual acceptance of test data generated for submission to Regulatory Authorities of the OECD member countries, harmonisation of the procedures adopted to monitor good laboratory practice compliance, as well as comparability of their quality and rigour, are essential.",
    "reference": "Til að auðvelda gagnkvæma viðurkenningu á prófunargögnum sem eru lögð fyrir lögbær yfirvöld í aðildarríkjum Efnahags- og framfarastofnunarinnar er mikilvægt að aðferðir við eftirlit með góðum starfsvenjum við rannsóknir séu samræmdar og að hægt sé að gera samanburð á því hversu góðar og strangar þær eru.",
    "grade": "A",
    "note": "OECD mutual test acceptance requires harmonized GLP monitoring comparable quality/rigor retained."
  },
  {
    "card": 216,
    "panel": "test",
    "id": "p22official21:test:eea:1608",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Taking account of national legislation, activities will aim to complement the existing actions by improving cooperation with domain name registries in Member States, and encouraging positive relationships with registries outside the EU to enable earlier detection of potentially illegal content and minimise the longevity of websites known to offer child sexual abuse content.",
    "reference": "Að teknu tilliti til landslöggjafar skulu aðgerðir miða að því að vera til fyllingar fyrirliggjandi aðgerðum með auknu samstarfi við skráningarstöðvar yfir lénsheiti í aðildarríkjunum, og verða hvatning til árangursríks sambands við skráningarstöðvar utan Evrópusambandsins svo að unnt verði að fylgjast með innihaldi sem hugsanlega er ólöglegt og lágmarka líftíma vefsetra sem vitað er að bjóða efni þar sem börn eru misnotuð kynferðislega.",
    "grade": "A",
    "note": "National law, domestic/foreign registry cooperation and illicit child-abuse-site detection/lifetime reduction retained; earlier nuance omitted."
  },
  {
    "card": 217,
    "panel": "test",
    "id": "p22official21:test:eea:41",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Similar studies for one soil must be reported for all relevant metobolites, degradation and reaction products which occur in soil and which at any time during the studies account for more than 10 % of the amount of active substance added, except where their DT50 values were able to be determined from the results of the degradation studies with the active substance.",
    "reference": "Gera skal grein fyrir svipuðum rannsóknum á einni jarðvegsgerð með tilliti til allra umbrots-, niðurbrots- og hvarfaefna sem koma fyrir í jarðvegi, og nema á einhverjum tímapunkti meðan á rannsókninni stendur meira en 10% af viðbættu magni virka efnisins, nema þegar unnt er að ákvarða DT50-gildi þeirra á grundvelli niðurstaðna úr niðurbrotsrannsóknum með virka efninu.",
    "grade": "A",
    "note": "One soil metabolites/degradation/reaction >10percent with DT50 exception retained."
  },
  {
    "card": 218,
    "panel": "test",
    "id": "p22official21:test:eea:2043",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "For national SEPA direct debits, the same national interchange fee or other agreed inter-bank remuneration between the payment service providers of the payee and of the payer could be used as that which existed before the date of application of this Regulation.",
    "reference": "Að því er varðar beingreiðslur innan sameiginlegs evrugreiðslusvæðis er heimilt að nota sama millibankagjaldið innanlands eða annað millibankagjald, sem samið er um, milli greiðslumiðlana viðtakanda greiðslu og greiðanda og var notuð fyrir gildistökudag þessarar reglugerðar.",
    "grade": "U",
    "note": "Source national SEPA debits, reference SEPA generally; domestic scope unclear in standalone pair."
  },
  {
    "card": 219,
    "panel": "test",
    "id": "p22official21:test:eea:1980",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "AG14E The total expected cash flows of the instrument over the life of the instrument must be substantially based on the profit or loss, change in the recognised net assets or fair value of the recognised and unrecognised net assets of the entity over the life of the instrument.",
    "reference": "AG14E Samanlagt vænt sjóðstreymi á gildistíma gerningsins skal byggjast að verulegu leyti á rekstrarreikningi, breytingum á færðri, hreinni eign eða gangvirði færðrar og ófærðrar, hreinnar eignar einingarinnar á gildistíma gerningsins.",
    "grade": "A",
    "note": "AG14E life-of-instrument expected cashflows linked profit/loss/net assets/fair value retained."
  },
  {
    "card": 220,
    "panel": "test",
    "id": "p22official21:test:eea:275",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "In addition they may allow the requirement on a bought exchange-traded or OTC commodity option to be the same as that for the commodity underlying it, subject to the constraint that the resulting requirement does not exceed the market value of the option.",
    "reference": "Að auki geta þau leyft að eiginfjárkrafan sem tengist kauprétti í hrávöru, sem verslað er með á verðbréfamarkaði eða kauprétti í hrávöru sem verslað er með utan verðbréfamarkaða, sé sú sama og fyrir hrávöruna sem liggur til grundvallar, að því tilskildu að krafan sem af því leiðir fari ekki yfir markaðsvirði kaupréttarins.",
    "grade": "R",
    "note": "Generic bought commodity option narrowed to call option kauprettur, potentially excludes purchased puts."
  },
  {
    "card": 221,
    "panel": "test",
    "id": "p22official21:test:eso:944",
    "stratum": "technical_long",
    "subcorpus": "eso",
    "source": "We now know that this was caused by the larger star of the pair expelling huge amounts of gas and dust in a short amount of time, which led to the distinctive lobes, known as the Homunculus Nebula, that we see in the system today.",
    "reference": "Í dag vitum við að ástæða þess var sú að stærri stjarnan í kerfinu varpaði frá sér miklu magni af gasi og ryki á mjög stuttum tíma sem leiddi til myndunar tveggja kekkja sem kallast Litli maðurinn og við sjáum í kerfinu í dag.",
    "grade": "A",
    "note": "Larger binary star expelled gas/dust quickly, producing observed Homunculus lobes retained."
  },
  {
    "card": 222,
    "panel": "test",
    "id": "p22official21:test:eea:45",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Soil residue studies must be reported where DT50lab is greater than one-third of the period between the application and harvest and where absorption by the succeeding crop is possible, except where soil residues at sowing or planting of a succeeding crop can be reliably estimated from the data of the soil dissipation studies or where it can be justified that these residues can not be phytotoxic to or leave unacceptable residues in rotational crops.",
    "reference": "Gera skal grein fyrir rannsóknum á efnaleifum þegar DT50lab er meira en einn þriðji af tímabilinu frá meðhöndlun og fram að uppskeru og möguleiki er á að næsta ræktun geti sogað upp efnaleifar, nema þegar unnt er að meta efnaleifar í jarðvegi við sáningu eða gróðursetningu fyrir næstu ræktun með áreiðanlegum hætti út frá gögnum úr rannsóknum á dreifingu í jarðvegi eða þegar unnt er að færa rök að því að þessar efnaleifar geti ekki verið plöntum skaðvænlegar eða skilið eftir sig óviðunandi leifar í víxleftirtekju.",
    "grade": "A",
    "note": "DT50lab>one-third application-harvest, succeeding crop uptake, reliable residue/nonphytotoxic exceptions retained."
  },
  {
    "card": 223,
    "panel": "test",
    "id": "p22official21:test:eea:1321",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Assessment and verification: the exact formulation of the product shall be provided to the Competent Body, together with copies of the material safety data sheets of each ingredient which shall indicate the relevant classification or lack thereof of each ingredient, and also a declaration of compliance with this criterion.",
    "reference": "Mat og sannprófun: veita skal þar til bærum aðila nákvæmar upplýsingar um efnasamsetningu vörunnar ásamt afritum af öryggisleiðbeiningum fyrir hvert innihaldsefni, þar sem greint er frá flokkun þeirra eða að þau séu ekki flokkuð, ásamt yfirlýsingu um að þessi viðmiðun sé uppfyllt.",
    "grade": "A",
    "note": "Exact formulation/SDS each ingredient classification plus compliance declaration retained."
  },
  {
    "card": 224,
    "panel": "test",
    "id": "p22official21:test:eea:803",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Measures to strengthen the capacity of key players involved in promoting gender equality should include the exchange of information, experience and best prac- tices among networks, including the network of Parliamentary Committees for Equal Opportunities for Women and Men in Member States and in the European Parliament and the Commission's experts' networks.",
    "reference": "Ráðstafanir til þess að auka afköst þeirra sem gegna meginhlutverki í því að stuðla að jafnrétti kynjanna skulu felast í skiptum á upplýsingum og miðlun reynslu og bestu viðtekinna starfsvenja milli netkerfa, þar með talið netkerfi þingnefnda um jöfn tækifæri fyrir karla og konur í aðildarríkjunum og í Evrópuþinginu og netkerfi sérfræðinga framkvæmdastjórnarinnar.",
    "grade": "R",
    "note": "Source split best prac- tices extraction damage; exclude without text repair."
  },
  {
    "card": 225,
    "panel": "test",
    "id": "p22official21:test:eea:1927",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "A puttable instrument is a financial instrument that gives the holder the right to put the instrument back to the issuer for cash or another financial asset or is automatically put back to the issuer on the occurrence of an uncertain future event or the death or retirement of the instrument holder.",
    "reference": "Innleysanlegur gerningur er fjármálagerningur sem gefur handhafa rétt til að skila gerningnum aftur til útgefanda gegn handbæru fé eða annarri fjáreign, eða er sjálfkrafa innleyst hjá útgefanda við óþekktan atburð sem á sér stað í framtíðinni eða við andlát eða starfslok handhafa gerningsins.",
    "grade": "A",
    "note": "Puttable holder return for cash/assets or automatic uncertain event/death/retirement retained."
  },
  {
    "card": 226,
    "panel": "test",
    "id": "p22official21:test:eea:68",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "The test must always be performed for relevant metabolites, degradation and reaction products which account at any time for more than 10 % of the amount of active substance added unless sufficient information on their degradation is available from the test performed in accordance with point 2.9.1.",
    "reference": "Prófið skal ætíð gert á viðkomandi umbrots-, niðurbrots- og hvarfaefnum, sem nema á einhverjum tímapunkti meira en 10% af viðbættu magni virka efnisins, nema fullnægjandi upplýsingar um niðurbrot þeirra liggi fyrir úr prófi sem fram fer samkvæmt lið 2.9.1.",
    "grade": "A",
    "note": "Always test relevant products>10percent unless2.9.1 sufficient degradation info retained."
  },
  {
    "card": 227,
    "panel": "test",
    "id": "p22official21:test:eea:1327",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "The product shall be compared in its washing performance with reference detergents of the same type according to the EU eco-detergents performance test ‘Award of the EU eco-label to laundry detergents: performance test of household detergents (version 4 December 2002 and its subsequent amendments).",
    "reference": "Þvottahæfni vörunnar skal prófuð með samanburði við viðmiðunarþvottaefni af sömu gerð í samræmi við þvottahæfnisprófun ESB fyrir þvottaefni sem óskað er eftir að fái umhverfismerki „Veiting umhverfismerkis ESB til þvottaefna: þvottahæfnisprófun á þvottaefnum til heimilisnota“ (4. útgáfa, frá desember 2002, og síðari breytingar á henni).",
    "grade": "R",
    "note": "Version dated4December2002 rendered fourth edition fromDecember2002; date/version number misinterpreted."
  },
  {
    "card": 228,
    "panel": "test",
    "id": "p22official21:test:ema:938",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "It is unclear whether or not there is a direct association between pioglitazone and macular oedema but prescribers should be alert to the possibility of macular oedema if patients report disturbances in visual acuity; an appropriate ophthalmological referral should be considered.",
    "reference": "Ekki er ljóst hvort beint samband er á milli pioglitazóns og sjónudepilsbjúgs, en þeir sem ávísa lyfinu ættu að vera á varðbergi gagnvart mögulegum sjónudepilsbjúg ef sjúklingar lýsa truflun á sjónskerpu; íhuga þarf þá viðeigandi tilvísun til augnlæknis.",
    "grade": "A",
    "note": "Unclear pioglitazone/macular edema causation, visual disturbance caution and eye referral retained."
  },
  {
    "card": 229,
    "panel": "test",
    "id": "p22official21:test:eea:1597",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Actions will aim to promote cooperation and exchange of best practices, tools, methods, experience and infomation at international level in order to encourage common approaches and methods of work and improve and enhance the effectiveness, cost-efficiency and the range of global initiatives.",
    "reference": "Aðgerðir skulu miða að því að efla samstarf og skipti á bestu starfsvenjum, úrræðum, aðferðum, reynslu og upplýsingum á alþjóðlegum vettvangi með það að markmiði að hvetja til sameiginlegra nálgana og vinnuaðferða og bæta og efla skilvirkni, kostnaðarhagkvæmni og alþjóðleg framtaksverkefni.",
    "grade": "A",
    "note": "International cooperation/best practices/tools/methods/info, common approaches and effective cost-efficient initiatives retained."
  },
  {
    "card": 230,
    "panel": "test",
    "id": "p22official21:test:ema:2271",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "The MAH commits to performing the studies and additional pharmacovigilance activities detailed in the Pharmacovigilance Plan, as agreed in the version dated 28 February 2005 of the Risk Management Plan (RMP) presented in Module 1.8.2. of the Marketing Authorisation and any subsequent updates of the RMP agreed by the CHMP.",
    "reference": "Markaðsleyfishafi skuldbindur sig til að gera rannsóknir og vinna viðbótarverkefni tengd lyfjagát sem tilgreind eru í áætlun um lyfjagát, eins og fram kemur í útgáfu dagsett 28. febrúar 2005 af áætlun um áhættustjórnun sem lýst er í kafla 1.8.2. í markaðsleyfinu og öllum uppfærslum á áætlun um áhættustjórnun sem CHMP samþykkir.",
    "grade": "A",
    "note": "MAH studies/pharmacovigilance,28Feb2005RMPmodule1.8.2 and CHMP updates retained."
  },
  {
    "card": 231,
    "panel": "test",
    "id": "p22official21:test:eea:2145",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Where contracting parties decide to make changes in this regard or subcontract the processing operations that are the subject matter of the contract they shall be required to enter into a new contract which shall comply with the standard contractual clauses set out in the Annex.",
    "reference": "Ákveði samningsaðilar að gera breytingar hvað þetta varðar eða að semja við undirverktaka um gagnavinnsluna, sem er efni samningsins, skal þess krafist að þeir geri nýjan samning sem er í samræmi við föstu samningsákvæðin sem sett eru fram í viðaukanum.",
    "grade": "A",
    "note": "Contract changes/subcontracted processing require new Annex standard-clause contract retained."
  },
  {
    "card": 232,
    "panel": "test",
    "id": "p22official21:test:eea:1940",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "For the purposes of applying this condition, the entity shall not consider non-financial contracts with a holder of an instrument described in paragraph 16A that have contractual terms and conditions that are similar to the contractual terms and conditions of an equivalent contract that might occur between a non-instrument holder and the issuing entity.",
    "reference": "Við beitingu þessa skilyrðis skal einingin ekki taka til greina aðra samninga en fjárhagslega við handhafa gernings, sem lýst er í lið 16A, þar sem samningsskilmálar og skilyrði eru sambærileg við samningsskilmála og skilyrði samsvarandi samnings sem gæti komist á milli aðila, sem er ekki handhafi gernings, og útgáfueiningar.",
    "grade": "A",
    "note": "Do not consider nonfinancial16Aholder contracts comparable with nonholder contracts retained."
  },
  {
    "card": 233,
    "panel": "test",
    "id": "p22official21:test:eea:307",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "In order to allow competent authorities to monitor the appropriateness of the plus-factor on an ongoing basis, institutions shall notify promptly, and in any case no later than within five working days, the competent authorities of overshootings that result form their back-testing programme and that would according to the above table imply an increase of a plus-factor.",
    "reference": "Í því skyni að gera lögbærum yfirvöldum kleift að fylgjast stöðugt með því að upphækkunarstuðullinn sé réttur skulu stofnanir tilkynna lögbærum yfirvöldum, eins fljótt og auðið er og aldrei síðar en innan fimm viðskiptadaga, lögbærum yfirvöldum um yfirskot sem áætlun þeirra um afturvirkt eftirlit leiðir í ljós eða sem fælu í sér hækkun á upphækkunarstuðli samkvæmt töflunni hér á undan.",
    "grade": "R",
    "note": "Overshoot resulting from backtest AND implying plus-factor rise rendered OR; duplicate competent-authorities phrase also present."
  },
  {
    "card": 234,
    "panel": "test",
    "id": "p22official21:test:ema:40",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "Administration of the product at overdose (up to 5-fold of the recommended dose for 6 months) resulted in marked reductions in blood pressure, decreases in red blood cell count (effects attributable to the pharmacological activity of the product) and increases in Blood Urea Nitrogen (BUN).",
    "reference": "Ofskömmtun lyfsins (allt að 5-faldur ráðlagður skammtur í 6 mánuði) olli greinilegri blóðþrýstings- lækkun, fækkun rauðra blóðkorna (verkun sem er tilkomin vegna lyfjafræðilegrar verkunar lyfsins) og hækkun á blóðnitri.",
    "grade": "R",
    "note": "Visible split blóðþrýstings- lækkun extraction damage; excluded without repair."
  },
  {
    "card": 235,
    "panel": "test",
    "id": "p22official21:test:eea:805",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Furthermore this Programme should be opened up for participation by the applicant countries of Central and Eastern Europe, in accordance with the conditions established in the Europe Agreements, in their additional protocols and in the decisions of the respective Association Councils, to Cyprus, Malta and Turkey.",
    "reference": "Enn fremur ætti löndum í Mið- og Austur-Evrópu, sem hafa sótt um aðild að Evrópusam bandinu, að vera frjálst að taka þátt í áætluninni í samræmi við þau skilyrði sem um getur í Evrópusamningunum, í viðbótarbókunum við þá og í ákvörðunum viðkomandi samstarfsráða fyrir Kýpur, Möltu og Tyrkland.",
    "grade": "R",
    "note": "Visible Evrópusam bandinu split and Cyprus/Malta/Turkey participation attached to councils, scope distorted."
  },
  {
    "card": 236,
    "panel": "test",
    "id": "p22official21:test:eea:2080",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Where appropriate, with regard to the nature of the payment transaction concerned, for all invoicing of goods and services in the Community, a supplier of goods and services that accepts payments covered by this Regulation shall communicate its IBAN and the BIC of its payment service provider to its customers.",
    "reference": "Þegar við á vegna eðlis viðkomandi greiðslna að því er varðar gerð allra vöru- og þjónustureikninga í Bandalaginu skal aðili, sem býður vöru og þjónustu og tekur við greiðslum, sem falla undir þessa reglugerð, upplýsa viðskiptavini sína um alþjóðlegt bankareikningsnúmer sitt og auðkenniskóða banka greiðslumiðlunar sinnar.",
    "grade": "A",
    "note": "Community invoices, covered payments and supplier disclosure ofIBAN/service-providerBIC retained."
  }
]
```

</details>

<details><summary>Full reference audit: test_reserve</summary>

```json
[
  {
    "card": 245,
    "panel": "test_reserve",
    "id": "p22official21:test:eea:478",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "Member States shall bring into force the laws, regulations and administrative provisions necessary to comply with this Directive by 1 October 1999; however, if the publication of the texts referred to in Article 3 is delayed beyond 1 April 1999, the Member States shall comply with this obligation six months after the actual date of publication of these texts.",
    "reference": "Aðildarríkin skulu samþykkja nauðsynleg lög og stjórnsýslufyrirmæli til að fara að tilskipun þessari eigi síðar en 1. október 1999; hafi birting textanna, sem um getur í 3. gr., dregist fram yfir 1. apríl 1999 ber aðildarríkjunum að standa við þessa skuldbindingu innan sex mánaða frá birtingu fyrrnefndra texta.",
    "grade": "A",
    "note": "Transposition1Oct1999 unless publication beyond1Apr1999 then6months from actual publication retained."
  }
]
```

</details>

<details><summary>Full reference audit: train_replacement</summary>

```json
[
  {
    "card": 237,
    "panel": "train_replacement",
    "id": "ParIce21:ema:178435",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "In both rats and dogs, AST/ALT elevations were observed in most studies, of which the increase in ALT in rats was not normalised after recovery.",
    "reference": "Hjá bæði rottum og hundum urðu AST/ALT hækkanir í flestum rannsóknum og ALT hækkun hjá rottum gekk ekki til baka eftir að meðferð var hætt.",
    "grade": "A",
    "note": "Rats/dogs, AST/ALT elevation, persistent rat ALT after stopping treatment retained in recovery paraphrase."
  },
  {
    "card": 238,
    "panel": "train_replacement",
    "id": "ParIce21:eso:383",
    "stratum": "technical_short",
    "subcorpus": "eso",
    "source": "How many stars might eventually start to shine within Lupus 4?",
    "reference": "Hve margar stjörnur gætu að lokum orðið til í Lupus 4?",
    "grade": "A",
    "note": "How many stars eventually shine expressed as form in Lupus4, acceptable astrophysical contextual paraphrase."
  },
  {
    "card": 239,
    "panel": "train_replacement",
    "id": "ParIce21:eso:9099",
    "stratum": "technical_long",
    "subcorpus": "eso",
    "source": "For the first time, a Japanese team of astronomers led by Bunyo Hatsukade from the National Astronomical Observatory of Japan, have used ALMA to detect the radio emission from molecular gas in two dark LGRB hosts - GRB 00819B and GRB 05102 - at about 4.3 billion and 6.9 billion light-years, respectively.",
    "reference": "Í fyrsta sinn hefur hópur japanskra stjörnufræðinga undir forystu Bunyo Hatsukade við National Astronomica Observatory of Japan notað ALMA til að mæla útvarpsgeislun frá sameindagasi í hýsilvetrarbrautum tveggja langra gammablossa - GRB 00819B og GRB 05102 - sem eru í um 4,3 milljarða og 6,9 milljarða ljósára fjarlægð.",
    "grade": "R",
    "note": "Dark qualifier of LGRB hosts omitted, institution OCR damaged; exclude precise technical reference."
  }
]
```

</details>

<details><summary>Full reference audit: train_sample</summary>

```json
[
  {
    "card": 32,
    "panel": "train_sample",
    "id": "OpenSubtitles18:917646",
    "stratum": "general",
    "subcorpus": "OpenSubtitles18",
    "source": "I'm not that desperate.",
    "reference": "Ég er ekki svona örvæntingarfull.",
    "grade": "A",
    "note": "Not that desperate preserved; gendered Icelandic acceptable without gender context."
  },
  {
    "card": 33,
    "panel": "train_sample",
    "id": "ParIce21:statisl:962",
    "stratum": "general",
    "subcorpus": "statisl",
    "source": "The data are based on the Statistics Iceland Labour Force Survey.",
    "reference": "Tölurnar eru byggðar á niðurstöðum úr vinnumarkaðsrannsókn Hagstofu Íslands.",
    "grade": "A",
    "note": "Data based on Statistics Iceland Labour Force Survey preserved."
  },
  {
    "card": 34,
    "panel": "train_sample",
    "id": "ParIce21:tatoeba:283",
    "stratum": "general",
    "subcorpus": "tatoeba",
    "source": "When are we eating? I'm hungry!",
    "reference": "Hvenær borðum við? Ég er svöng!",
    "grade": "A",
    "note": "Question about eating and hunger retained."
  },
  {
    "card": 35,
    "panel": "train_sample",
    "id": "ParIce21:ted2020:383",
    "stratum": "general",
    "subcorpus": "ted2020",
    "source": "So Melcher Media's team, who's on the East coast -- and we're on the West coast, building the software -- takes our tool and, every day, drags in images and text.",
    "reference": "Þannig að lið Melcher Media, sem er á austurströndinni -- og við erum á vesturströndinni, að búa til hugbúnaðinn -- tekur tólið okkar og dregur, á hverjum degi, inn myndir og texta.",
    "grade": "A",
    "note": "East/West teams, software role and daily image/text insertion retained."
  },
  {
    "card": 36,
    "panel": "train_sample",
    "id": "ParIce21:eea:1876",
    "stratum": "technical_short",
    "subcorpus": "eea",
    "source": "That Directive also contains provisions concerning the emergency vaccination of feral pigs.",
    "reference": "Í þeirri tilskipun eru einnig ákvæði sem varða neyðarbólusetningu villtra svína.",
    "grade": "A",
    "note": "Directive provisions for emergency vaccination of wild pigs retained."
  },
  {
    "card": 37,
    "panel": "train_sample",
    "id": "ParIce21:ema:367561",
    "stratum": "technical_short",
    "subcorpus": "ema",
    "source": "The treatment effect was established early and was sustained.",
    "reference": "Áhrif meðferðarinnar komu snemma fram og héldust.",
    "grade": "A",
    "note": "Early onset and persistence of treatment effect retained."
  },
  {
    "card": 38,
    "panel": "train_sample",
    "id": "ParIce21:eso:74",
    "stratum": "technical_short",
    "subcorpus": "eso",
    "source": "The E-ELT is ESOs most ambitious project so far.",
    "reference": "E-ELT er stærsta verkefni ESO hingað til.",
    "grade": "U",
    "note": "Most ambitious translated largest; uncertain whether this project characterization is sufficiently faithful for calibration-free train sample approval."
  },
  {
    "card": 39,
    "panel": "train_sample",
    "id": "ParIce21:eea:2394499",
    "stratum": "technical_medium",
    "subcorpus": "eea",
    "source": "The text of Decision 2011/130/EU in the Icelandic and Norwegian languages, to be published in the EEA Supplement to the Official Journal of the European Union, shall be authentic.",
    "reference": "Íslenskur og norskur texti ákvörðunar 2011/130/ESB, sem verður birtur í EES-viðbæti við Stjórnartíðindi Evrópusambandsins, telst fullgiltur.",
    "grade": "A",
    "note": "Decision identifier, Icelandic/Norwegian authentic texts and EEA Supplement publication retained."
  },
  {
    "card": 40,
    "panel": "train_sample",
    "id": "ParIce21:ema:394623",
    "stratum": "technical_medium",
    "subcorpus": "ema",
    "source": "Vidaza is contraindicated in patients with advanced malignant hepatic tumours (see sections 4.3 and 4.4).",
    "reference": "Vidaza er ekki ætlað sjúklingum með illkynja lifraræxli (sjá kafla 4.3 og 4.4).",
    "grade": "R",
    "note": "Advanced hepatic tumour qualifier omitted; contraindicated rendered not intended. Unsuitable precise medical reference."
  },
  {
    "card": 41,
    "panel": "train_sample",
    "id": "ParIce21:eso:907",
    "stratum": "technical_medium",
    "subcorpus": "eso",
    "source": "These comparatively small telescopes, equipped with suitable spectrographs, are powerful tools for this kind of research.",
    "reference": "Þessir tiltölulega litlu sjónaukar, útbúnir viðeigandi litrófsritum, eru öflug tæki til rannsókna af þessu tagi.",
    "grade": "A",
    "note": "Relatively small telescopes, suitable spectrographs and powerful research tools retained."
  },
  {
    "card": 42,
    "panel": "train_sample",
    "id": "ParIce21:eea:1084717",
    "stratum": "technical_long",
    "subcorpus": "eea",
    "source": "The European Food Safety Authority (hereinafter the Authority) concludes in its opinion of 21 October 2008 (11) that Saccharomyces cerevisiae NCYC Sc47, as produced by the applicant Société Industrielle Lesaffre, can be presumed safe for the target species, consumers and the wider environment.",
    "reference": "Matvælaöryggisstofnun Evrópu (hér á eftir nefnd „stofnunin“) komst að þeirri niðurstöðu í áliti sínu frá 21. október 2008 (11) að gengið skuli út frá því að Saccharomyces cerevisiae NCYC Sc47, eins og umsækjandinn Société Industrielle Lesaffre framleiðir það, sé öruggt fyrir markdýrategundir, neytendur og umhverfið í heild.",
    "grade": "A",
    "note": "EFSA date, yeast strain/applicant and presumed safety for targets/consumers/environment retained."
  },
  {
    "card": 43,
    "panel": "train_sample",
    "id": "ParIce21:ema:403025",
    "stratum": "technical_long",
    "subcorpus": "ema",
    "source": "When Bexsero is given to you or your child, the very common side effects (may affect more than 1 in 10 people) that you or your child may get (reported in all age groups) are: pain/tenderness at the injection site, redness of the skin at the injection site, swelling of the skin at the injection site, hardness of the skin at the injection site.",
    "reference": "Þegar þér eða barninu er gefið Bexsero eru algengustu aukaverkanirnar (mjög algengar, geta komið fram hjá meira en 1 af hverjum 10 einstaklingum) sem þú eða barnið getið fundið fyrir (sem var greint frá í öllum aldurshópum): verkur/eymsli á stungustað, húðroði á stungustað, húðbólga á stungustað, hersli á stungustað.",
    "grade": "A",
    "note": "Bexsero frequency >1/10, all ages and four injection-site adverse effects retained."
  },
  {
    "card": 44,
    "panel": "train_sample",
    "id": "ParIce21:eso:9567",
    "stratum": "technical_long",
    "subcorpus": "eso",
    "source": "“After careful and lengthy data processing, we have now achieved the accuracy required for the ground-based observations of Gaia to be implemented as part of the orbit determination,” says Martin Altmann, lead of the Ground Based Optical Tracking (GBOT) campaign at the Centre for Astronomy of Heidelberg University, Germany.",
    "reference": "„Eftir langa gagnaúrvinnslu höfum við nú loks náð þeirri nákvæmni sem þarf til þess að mælingar Gaia séu framúrskarandi,“ sagði Martin Altmann, umsjónarmaður Ground Based Optical Tracking (GBOT) herferðarinnar við Center for Astronomy við Heidelbergháskóla í Þýskalandi.",
    "grade": "R",
    "note": "Reference replaces required ground-based Gaia orbit-determination accuracy with excellent Gaia measurements; core technical purpose omitted."
  }
]
```

</details>

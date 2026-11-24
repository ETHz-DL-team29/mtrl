# Execution and reproducibility

2026-11-24 · Europe/Berlin

This records the executed workflow and **does not launch a new run or allocate a GPU**. The original window is November23 at21:50:49 CET to November24 at07:50:49 CET. Its budget contains an absolute deadline and must not be reused to silently authorize another night.

## Freeze inputs

- Original SFT baseline:`D:\deep learning project\runs\r0_3b_recovery_sft_2026-11-21\final_selected_adapter`, weight SHA256:`7f7a4914c5f403e757fdb882c3576ac68f2b0fa6edc00e537087716b28ddb07e`。
- Existing DAPO-120:`D:\deep learning project\experiments\wmt26_shortmid_night_2026-11-23\source\candidate_adapter`; its fingerprint, original location and configuration are recorded in`protocol.json`。
- The only general-purpose starting base is Qwen/Qwen2.5-3B-Instruct, revision `aa8e72537993ba99e69dfaafa59ed015b17504d1`。
- Original WMT release: wmt-conference/wmt26-general-mt, commit `63aa5d24311a7e7e3e8173528f3771c7e8b4be78`；raw SHA256 `de286ce336f10367bedfe0611764b2569b538a9c57db20467fc8c1fa84838291`。
- 198English-to-Icelandic documents with complete official refA. Source uses`src_text`, without using`gold_transcript`to replace ASR text; no images or audio are supplied.

Freeze the original SFT R0 and existing DAPO-120 adapters and their fingerprints. Use the pinned general-purpose Qwen model and WMT data revisions above. Preserve all198 English-to-Icelandic documents and official refA. Inputs are text-only src_text; do not replace ASR text with gold_transcript or add other media.

## Segment source and prepare data

Source segmentation uses pySBD0.3.4 with exact offsets, separators and tails, protecting fenced/inline code and URLs. Seven boundary cases and lossless reconstruction of all198 sources passed. The2551 units include251 obvious markup/counter units, all copied exactly by all three models; they are not2551 natural-language sentences.

Before WMT outputs, freeze1200 training sources:400general,400technical-short and400technical-medium, plus36dev and72historical holdout sources. Short means≤12 English whitespace words and medium13–40. Exclude exact normalized WMT source-unit overlaps. This is not proof against every near duplicate or overlap with prior SFT/pretraining.

## Colab runtime

The host supervisor used existing official Colab CLI authentication to create this experiment's L4, preserving unrelated runtimes. Neural work runs under /content/p25_project. Host work is below-normal-priority CPU preparation/statistics and capped transfer:142 upload parts at≤1MiB/s, one512KiB/s checkpoint downloader and an additional≤128KiB/s completed-batch backup. No purchase or local neural-model loading occurred.

The remote worker verifies source_manifest and installs pinned dependencies; see run/environment.json. The actor uses FP32, SDPA and TF32 disabled. Checks cover batch-versus-single next-token logits, native G8 sampling, sampler/teacher log-probability parity and actual nonzero parameter updates. Final CPU replay reconstructs every one of the240 actual optimizer losses from saved traces.

## Initial WMT comparison

Alternate adapters by blocks of eight original documents, with four units per batch, greedy decoding, max_new_tokens1024 and a2048-token nontruncating prompt limit. Persist atomic batch JSONs, reconstruct original documents, and score unchanged refA. The actor never receives reference text. Retain long units, difficult cases and truncated outputs in primary scores.

Metrics are sacrebleu2.6.0 chrF++ with word_order2 and BLEU13a. Use2000 fixed-seed paired bootstrap resamples of original documents within domains. The initial predeclared rule requires positive chrF++ interval lower bound and nonnegative BLEU point difference. It failed, triggering the frozen conditional arm. No bootstrap seeds were searched for significance.

## Specialized DAPO

Restart from original P18 rather than continue old DAPO. The pinned MetricX scorer receives source+candidate+reference in BF16, clamps raw error to[0,25] and uses1-error/25 reward. Revisions are listed above. There is no new SFT, reference-token supervised loss or new human-label reward.

Use G8,T0.7,top_p1,top_k0,max completion512 and soft-length buffer64. Collect four accepted source groups per rollout within32 attempts. Retain groups with≥2valid candidates, nonzero actual reward variance and≥2word/punctuation sequences. This does not certify semantic correctness or P/F mixtures. The absolute proxy threshold is logged but not used for eligibility.

AdamW uses LR3e-6, two epochs, dual clip.2/.28, gradient clipping1 and global active-token normalization. Complete all240 updates, evaluating dev and saving weights every20. **No metric-regression early stop.** Time, numerical and data protections remain. Dev selection maximizes technical short/medium macro chrF++ among checkpoints retaining overall/general within1.5 of R0, then BLEU, then earliest step. Step120 was selected without using WMT or the historical72.

## Endpoint evaluation and auxiliary audit

Evaluate one dev-selected endpoint on all198 WMT documents, reusing the identical original-R0 predictions. Score the historical72 ParIce pairs separately and disclose their prior examination.

Exploratory length subsets retain whole refA:55all-units≤12-word documents (all speech), and153all-units≤40-word documents (3news/18social/132speech). Thresholds match the original protocol, but this subset analysis was added after initial WMT and before specialized endpoint scores. It is exploratory, unadjusted for multiple comparisons and does not replace the198-document primary result.

The pre-output audit selected24sources (no eligible short/medium software units; no post-output replacements), yielding72model/source pairs and52deduplicated blind judgments. Seal P/F/U annotations and hashes before opening identity mappings. Report five formatting/counter sources separately from19 substantive sources. This same-assistant audit is not independent Icelandic-native certification or a population correctness estimate. Preserve all outputs and reasons in the casebook.

## Persistence, resume and integrity

Persist12regular weight checkpoints (20…240) and one shortmid_selected_full under runs/snapshots. Only the selected full checkpoint includes AdamW/RNG; other weights are warm-startable, not exact optimizer resumes. Verify chunk, ZIP and internal-file SHA256s. Keep two scientific-export ZIP copies on D; they are not offsite backups. Release only this run's L4 after verification, then confirm its assignment is absent. The absolute ten-hour release guard takes priority.

This is a specialized DAPO/WMT pilot, not yet a selective-token-update or prefix-reuse comparison. The selected endpoint is step120, but exploration consumed240updates; do not hide selection/search cost by reporting only120steps. Accepted-group rate is not correct-candidate coverage.

## Artifact entry points

- Main report: `reports/wmt26_shortmid_night_2026-11-23/WMT26_AND_SHORTMID_DAPO_RESULTS_2026-11-23.html`
- Full casebook: `reports/wmt26_shortmid_night_2026-11-23/WMT26_SEMANTIC_CASEBOOK_2026-11-24.html`
- Frozen code,data,hashes: `experiments/wmt26_shortmid_night_2026-11-23/source`
- Host execution scripts: `experiments/wmt26_shortmid_night_2026-11-23/host_scripts`
- Scientific export: `runs/wmt26_shortmid_night_2026-11-23/exported`
- Checkpoint catalog: `runs/wmt26_shortmid_night_2026-11-23/checkpoint_catalog.json`
- Resource ledger: `runs/wmt26_shortmid_night_2026-11-23/resource_ledger.json`

A new experiment requires a new directory, explicitly authorized budget and absolute deadline, followed by frozen code/data/selection. Do not overwrite this run or choose training examples from WMT output quality. Loading an adapter requires the same general Qwen base and revision; a LoRA adapter is not a standalone3B model. Execute neural code only on Colab.

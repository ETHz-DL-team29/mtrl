# 0.8B checkpoint quick reference — 2026-11-17

- **Frozen comparator**：`runs/r0_v3_colab_2026-11-13/nll_adapter`. Common start for older DAPO and subsequent SFT; matched FP32 diagnosis on128cases gives chrF++34.567 and BLEU15.701.
- **Selected technical SFT200**：`runs/r0_technical_sft_2026-11-17/selected_candidate_adapter`. Adds200770target tokens and165updates; matched128case chrF++36.037/BLEU16.031. Improvement intervals cross zero and technical G8 coverage remains3/24; reliable improvement is unestablished.
- **Final SFT400**：`runs/r0_technical_sft_2026-11-17/final_trained_adapter`. Adds399895target tokens and330updates; not selected as best candidate and must not be confused with SFT200.
- **Earlier local SFT**：`runs/sft_round1/best`. Historical results preserved. Original logs show step250 chrF++30.003 on50old dev sentences with max_new_tokens96; step200 scores30.303. Count50 is the sample count. The previously recalled score near50 has not been mapped to a precise evaluation protocol and cannot be attributed as this checkpoint's original comprehensive score. The old set and current128cases are not directly comparable.
- **DAPO30 / Experimental DAPO30**：`experiments/dapo_fp32_control_2026-11-16/attempt_B/snapshots/step_030/files/adapter`. Complete state/records are preserved. Translation improvement is unproven and this does not replace frozen R0.
- **Tiny fitting probes**：`runs/r0_cause_diagnosis_2026-11-17/snapshots/A_lowLR/files/adapter`and`B_highLR/files/adapter`. Memorizes32cases while dev quality worsens; not a stronger R0.

All paths are relative to D:/deep learning project. Full SHA256s and available state files are in CHECKPOINT_ALIASES_08B_2026-11-17.json;all57 canonical checkpoint paths are in the complete inventory.
All paths are relative to D:/deep learning project. Alias JSON includes full hashes and status paths; the complete catalog contains57checkpoint paths.

These are adapters. Load the local Qwen3.5-0.8B base explicitly,revision2fc06364715b967f1860aea9cf38778875588b17,then attach the chosen PEFT adapter. Saved historical /content paths are not current local paths. Adapter-only loading does not restore AdamW/RNG/data cursor.
These are adapters requiring the matching base. Exact resumption additionally requires the complete optimizer, RNG and data order; adapter loading alone is insufficient.

Historical files such as R0_SELECTION_2026-11-13.json contain decisions made at the time,including needs_more_sft=true. The Nov17 diagnosis supersedes that certainty:neither an absolute0.8B SFT ceiling nor the necessity of moreSFT has been established. Preserve old files as provenance rather than silently rewriting them.
Historical needs_more_sft=true reflects the judgment at that time. The November17diagnosis establishes neither mandatory additional SFT nor a capacity ceiling. Original records remain for traceability, not as the latest causal conclusion.

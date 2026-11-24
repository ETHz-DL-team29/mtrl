# Eight-hour3B R0 recovery and evidence

Authorized execution; checkpoint quality remains to be measured.

Produce and evaluate a reusable generic-Qwen-derived English→Icelandic checkpoint while preserving P15. This is a targeted12-source review, not exhaustive literature coverage; large-model or10B-token results do not guarantee this8h run.

## Revisions to the earlier proposal

| Item | Frozen execution decision |
| --- | --- |
| Origin | Same generic Qwen2.5-3B-Instruct + originalP15 adapter; no translation-specialist weights |
| Capacity | rank16/alpha32→rank64/alpha128; preserve scale2 and old blocks; new B columns zero |
| Optimizer | fresh AdamW; old decayed optimizer state not reused |
| Fit probe | 64 source/reference pairs audited;32 free-generation checks;P≥26/32,longP≥12/16;LR1e-4;at most250k targets/45min actual training |
| Production | Discard fit weights;restart expanded original;LR5e-5→5e-6,50k warmup;BF16 base+FP32 LoRA;all-linear;dropout.05 |
| Data | 17,911pairs,991,863unique target tokens,two exposures1,983,726targets;about10/10/40/40% general/short/medium/long |
| QA | 80 reference pairs inspected,16 excluded from fit;103 total production quarantines;not native-certified full-pool audit |
| Evaluation | New selecteddev128/final128,old selected input exclusions;source5gramJaccard≥.85 vs100642pool yielded0hits;not proven document/pretraining independence |
| Selection | Reviewed devG8 coverage→greedyP→technicalCF→earlier;generalCF delta≥−1.5;final test never selects weights |
| Budget | Conservative research-inclusive hard deadline2026-11-22 04:40CET;training must stop≥2h earlier;no reset |
| Allocation | One owned ColabL4;no local neural training/inference;no foreground browser/power changes |
| Priority | This run focuses on SFT and checkpoint acceptance;no DAPO,MetricX retraining or preference-method sweep |

Throughput measured in the first30 production updates can reduce the target budget. Main training is capped at4h. Failure of the fit gate stops scale-up;no semantic improvement at1M stops continuation. Save full recovery state at1M/final and intermediate adapters, with D-drive hashes and a deadline that never resets.

Deliver original R0, the development-selected adapter,FP32 inference,independent evaluation and bilingual reports. If predefined project criteria such asG8≥39/64 andlong≥12/24 fail,the result remains unqualified; a saved checkpoint is not proof of sufficient quality.

## Source-by-source interpretation

### ALMA · ICLR2024

[ALMA · ICLR2024](https://arxiv.org/abs/2309.11674)

Uses monolingual adaptation followed by high-quality parallel SFT, including Icelandic. Its extensive monolingual stage cannot be reproduced within this8h run.

Adopt quality-focused parallel SFT; no specialist weights or ALMA performance claim.

### AMI WMT25 · 3B English-to-Icelandic

[AMI WMT25 · 3B English-to-Icelandic](https://aclanthology.org/2025.wmt-1.46/)

The closely matched3B Icelandic system uses10B English/Icelandic pretraining tokens, SFT and additional stages, and remains behind leading systems.

Treat as evidence of substantial language adaptation, not proof of a3B ceiling or a short-run guarantee.

### LoRA Learns Less and Forgets Less · TMLR2024

[LoRA Learns Less and Forgets Less · TMLR2024](https://arxiv.org/abs/2405.09673)

Standard low-rank settings can underperform full tuning while forgetting less in studied programming/math regimes; this does not prove rank16 inadequate for Icelandic.

Avoid conflating low-rank adaptation with model capacity; increase adaptation space.

### LoRA Without Regret · Original authors' 2025 experiments

[LoRA Without Regret · Original authors' 2025 experiments](https://thinkingmachines.ai/blog/lora/)

Finds that layer coverage, adapter capacity, batch size and LR matter; higher LoRA LR is useful in studied settings, not an exact Icelandic hyperparameter prescription.

Keep all-linear coverage; test rank64 and fresh higher-LR optimization through a fit gate.

### rsLoRA · 2023

[rsLoRA · 2023](https://arxiv.org/abs/2312.03732)

Discusses how scaling affects learning as rank increases.

Studies the rank-dependent scaling of adapter updates.

Preserve scale2 through zero-padded rank expansion rather than mixing a new scaling rule into this run.

### QLoRA · NeurIPS2023

[QLoRA · NeurIPS2023](https://arxiv.org/abs/2305.14314)

Low-bit frozen bases reduce tuning memory; reported results are not a universal lossless guarantee.

Retain BF16 because it fits, avoiding a new quantization variable.

### DoRA · ICML2024

[DoRA · ICML2024](https://arxiv.org/abs/2402.09353)

Magnitude/direction decomposition is a candidate alternative, without verified benefit for this task.

Defer additional methods until a useful R0 exists.

### LoRA+ · ICML2024

[LoRA+ · ICML2024](https://arxiv.org/abs/2402.12354)

Studies different learning rates for A/B and their effect on adaptation efficiency.

Investigates unequal learning rates for adapter factors.

Avoid a new factor-LR search; use one declared optimizer setting.

### ALMA-R/CPO · ICML2024

[ALMA-R/CPO · ICML2024](https://arxiv.org/abs/2401.08417)

Preference optimization improves existing translation models and highlights imperfect human references.

Inspect references and keep uncertainty; defer preference training.

### Official Qwen2.5 SFT example

[Official Qwen2.5 SFT example](https://qwen.readthedocs.io/en/v2.5/training/SFT/ms_swift.html)

An official example uses all-linear LoRA and1e-4, on a different model/data setting; it is not an optimum for our task.

Use1e-4 for the fit probe and5e-5 for bounded production SFT, with generalization checks.

### Official PEFT LoRA documentation

[Official PEFT LoRA documentation](https://huggingface.co/docs/peft/v0.22.0/package_reference/lora)

Rank, alpha and target modules define the adapter. Execution stays on the already verified peft0.21.2 environment.

Verify copied old blocks, zero new B columns and module-output parity.

### Official Lightning training-debugging guidance

[Official Lightning training-debugging guidance](https://api.lightning.ai/docs/pytorch/stable/debug/debugging_intermediate)

Deliberately fitting a tiny dataset is a debugging technique for trainability.

64 audited pairs and32 free-generation checks; fitting is distinct from generalization.

## Local evidence and unresolved claims

Previous known-seen audit7/16,long0/4;DAPO G8 coverage6/16→6/16 andmatchedchrF++44.007→41.837. These motivate fit and coverage work but do not establish a3B ceiling,an optimalLR or guaranteed rank-expansion benefit.

Same-assistant semantic review retains uncertainty. Formal conclusions require independent human review,replication and a credible reward; AI review is not native-expert blinded certification.

Evidence and executed inputs are archived separately without overwriting prior results.

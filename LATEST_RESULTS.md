# Latest experiment results

**2026-11-23–24 · P25 short/medium DAPO · Latest completed run**

Original R0 is the P18 Qwen2.5-3B-Instruct SFT adapter. The latest arm starts from it, completes240updates and selects step120 using dev only. Original R0 is preserved and no new SFT was performed.

## Primary WMT26 comparison

198 official English-to-Icelandic documents, translated as source units and then reassembled. Official refA is unchanged; all models use the same FP32/greedy protocol. These are automatic scores, not the official competition's human ranking.

|Model|Registry ID|chrF++|BLEU|
|---|---|---:|---:|
|Original SFT R0|`qwen25-3b-sft-r0`|39.72|19.76|
|Previous DAPO-120|`qwen25-3b-dapo-reference`|39.91|20.87|
|**Latest specialized DAPO-120**|**`qwen25-3b-dapo-shortmid`**|**40.83**|**21.70**|

**Versus SFT R0: chrF++ +1.12, paired 95% CI [-0.06, +2.56]; BLEU +1.94, CI [-0.07, +5.22]. Both intervals include zero, so the predeclared primary gain rule is not met. This is a promising candidate, not a proven universally stronger translation model.**

## Length subsets and fidelity

- 153 complete documents whose source units are all at most 40 words: chrF++40.42→41.88 and BLEU17.33→20.33, with positive paired intervals. This is an exploratory, speech-heavy secondary analysis without multiplicity correction; it does not replace the 198-document primary result.
- 55 complete documents whose units are all at most 12 words: no reliable improvement. Improved pure-short translation is not established.
- The same assistant audited 24 presampled source units under blinding: 19 substantive items changed from P4 to P5; five formatting/counter items are reported separately. This is neither native-expert certification nor a population correctness estimate.

The153-document short/medium secondary subset is positive but exploratory; the55all-short documents show no reliable gain. A small same-assistant audit gives limited semantic evidence and is not native-expert certification. All difficult cases remain in the primary benchmark.

## Open the evidence

- [Full English HTML report](results/local_translation_release_2026-11-24/project_snapshot/reports/wmt26_shortmid_night_2026-11-23/WMT26_AND_SHORTMID_DAPO_RESULTS_2026-11-23.html)
- [Full Markdown report](results/local_translation_release_2026-11-24/project_snapshot/reports/wmt26_shortmid_night_2026-11-23/WMT26_AND_SHORTMID_DAPO_RESULTS_2026-11-23.md)
- [Conclusions, resources and next steps](results/local_translation_release_2026-11-24/project_snapshot/reports/wmt26_shortmid_night_2026-11-23/CONCLUSIONS_AND_NEXT_STEP_2026-11-24.html)
- [Complete case-by-case audit](results/local_translation_release_2026-11-24/project_snapshot/reports/wmt26_shortmid_night_2026-11-23/WMT26_SEMANTIC_CASEBOOK_2026-11-24.html)
- [Execution and reproducibility](results/local_translation_release_2026-11-24/project_snapshot/reports/wmt26_shortmid_night_2026-11-23/EXECUTION_REPRODUCIBILITY_2026-11-24.html)
- [Results figure](results/local_translation_release_2026-11-24/project_snapshot/reports/wmt26_shortmid_night_2026-11-23/results_overview.png)
- [Machine-readable primary metrics](results/local_translation_release_2026-11-24/project_snapshot/runs/wmt26_shortmid_night_2026-11-23/wmt_shortmid/paired_metrics.json)
- [All SFT and historical results](results/local_translation_release_2026-11-24/README.md)
- [Use the models](models/README.md)

The proposed next step is an independent-seed replication of this fixed recipe, followed by selective-token or prefix-reuse efficiency comparisons. Replication has not started. Baseline comparisons must continue to share the same original SFT R0.

Public model downloads: [Hugging Face guide](models/HUGGING_FACE.md). Repository publication is managed by the owner.

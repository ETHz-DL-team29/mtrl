## Final interpretation and next step

**Keep the specialized DAPO candidate, while recognizing that a reliably stronger general translation model has not been established. Original P18 remains the shared SFT R0. The new artifact is a DAPO candidate, not a relabeled SFT baseline.**

|Model|WMT26 chrF++|WMT26 BLEU|
|---|---:|---:|
|Original SFT R0|39.72|19.76|
|Existing DAPO-120|39.91|20.87|
|Specialized endpoint|40.83|21.70|

Relative to original R0, full WMT chrF++ is **+1.12** with95%CI **[-0.06,+2.56]**, and BLEU **+1.94** withCI **[-0.07,+5.22]**. Both point estimates improve, but both intervals narrowly include zero. The predeclared198-document primary rule is not met. Bootstrap seeds, difficult documents and the primary metric were not changed to obtain a pass.

### What the short-medium evidence says

- **153complete WMT documents with all source units≤40words**: chrF++ **40.42→41.88**, difference interval **[+0.02,+2.69]**; BLEU **17.33→20.33**, interval **[+0.46,+4.83]**. Positive exploratory evidence. The subset includes132speech documents; analysis was added after initial WMT and lacks multiplicity correction, so it cannot replace full-test confirmation.
- **55complete documents with all units≤12words**: chrF++ **43.66→43.61**, BLEU **21.46→21.33**, without reliable gain. **Pure-short improvement is not established.**
- **Historical ParIce72cases**: chrF++ **51.69→52.25**, BLEU **23.91→25.13**, both intervals crossing zero. Technical short/medium point estimates improve, while general chrF++ **41.28→40.18**. Report tradeoffs and uncertainty rather than only the best subgroup.

The153whole-document short/medium subset shows positive exploratory differences: chrF++ **+1.46**,CI **[+0.02,+2.69]**, and BLEU **+3.00**,CI **[+0.46,+4.83]**. However132documents are speech, the analysis was added after initial WMT, and multiplicity is unadjusted. The55all-short documents show no reliable gain. The historical72-pair ParIce set has positive overall/technical point estimates but zero-crossing intervals and a general-subset decline. Thus the evidence supports a promising short/medium candidate, not a confirmed pure-short or universal improvement.

### What individual outputs show

The actual blind audit contains24source units, including19substantive items and five formatting/counter items. On the19, the same assistant labeled original R0 P4/F13/U2 and the specialized candidate P5/F11/U3: oneF→P and oneF→U, with no observedP→F. This small, non-native-certified audit is **not a population correctness estimate**.

- In the Jade/Beck reunion example, original R0 omits the key tell-him action; this round restores`segja honum það`, a traceable semantic improvement.
- `volcano`、`organizing the strike`and other simple but critical meanings remain problematic across all three models. Short does not automatically mean easy.
- Old DAPO severely repeats in the Robin Roefs example; this round does not, but all three versions still contain material match-information errors. Removing repetition does not make the whole translation correct.
- The casebook retains all sampled sources and all three translations, not just selected illustrations. All models copy251obvious formatting-only WMT units exactly; these are not counted as substantive translation successes.

The Jade/Beck example recovers the missing tell-him action. Volcano and organizing the strike remain problematic across all three models. The old DAPO loops on the Robin Roefs example, whereas the new version does not, yet the new sentence still contains material match-information errors. The complete casebook retains every selected source/output. All three models copy the251obvious formatting units exactly; these are not counted as successful language translations in the substantive audit.

### Does this prove insufficient SFT

The evidence does **not** support the absolute claim that R0 cannot undergo DAPO and must receive more SFT first. There were zero new SFT updates, yet positive WMT/technical signals appeared. Nor does this establish a3B capacity ceiling. Persistent key lexical errors also prevent claiming translation mastery.

Sampler/teacher parity, actual parameter changes, all240objective replays and complete WMT reconstruction pass. This checks those implementation components, **not reward semantic validity**. This round does not repeat an independent per-source G8 correctness/ranker audit, so it cannot quantify the remaining candidate-coverage versus reward-ranking bottlenecks. A bad greedy output does not prove all eight samples are wrong; a higher automatic metric does not prove complete semantic correctness.

### One concrete next step

**Next, replicate this short/medium DAPO recipe rather than blindly add SFT or merely extend training.** Start from the same original P18 and1200-source pool with one new prespecified sampling/order seed, run up to120updates and evaluate the fixed120-step endpoint without WMT checkpoint selection. Preserve identical scoring/decoding and report full WMT, the same secondary subsets and key semantic checks. Based on this run, reserve roughly3–4hours on one L4 including setup/evaluation/export, excluding unpredictable queuing. This is a next-round recommendation; it was not launched here.

If replication supports the short/medium gain, freeze original-R0→standard-DAPO as the control before selective-token/prefix-reuse comparisons, matching starts,data,budgets and actual GPU time/memory. If gains remain metric-only or nonreplicable, audit actual G8 candidates and reference-based reward before choosing reward changes or targeted SFT. Do not infer a capacity ceiling. No efficiency-method comparison was implemented in this round, so no speed result is an innovation gain.

### What the profiling says about efficiency

Across240updates, attempt514source groups, accept480, and generate4112candidates with152262completion tokens. **The extra formatting-diversity filter rejects only1otherwise-eligible group.** Quality changes cannot be attributed to this filter or presented as a validated efficiency innovation. Acceptance rate is not correct-candidate coverage.

Optimizer phases sum to59.24minutes; the complete DAPO phase, including generation,scoring,teacher passes,dev and snapshots, spans about2.39hours. Search consumed240updates even though the selected parameters are from120. Report training-pipeline time and quality separately from the entire evaluation/export-inclusive experiment. Multiplying losses by a token mask alone does not establish reduced matrix computation; no such speed gain was tested here.

### Delivered checkpoint and resources

- Specialized candidate: **P25-shortmid-step120**, full adapter folder: `D:\deep learning project\runs\wmt26_shortmid_night_2026-11-23\snapshots\shortmid_selected_full\files\adapter`。
- weights SHA256: `40ee8312ead89272fd5e8190a3b8e1da91d5f0ff641721840600585ff4308c86`. This adapter still requires the same general-purpose Qwen3B base and cannot run independently.
- Original R0 is preserved and hash-verified. All12regular checkpoints from20…240and the selected full AdamW/RNG state are persisted. Other regular checkpoints are not claimed to support exact optimizer resumption.
- GPU allocation to release: **6.03h**; request start to release: **6.23h**; account compute-unit difference: **11.68**, not exclusively attributable if the account had other activity. Scientific exports, internal files and checkpoints are verified. The dedicated L4 is released and confirmed absent from allocation listings.

Original R0 is hash-verified and preserved. All12regular checkpoints and the selected full AdamW/RNG state are saved. The account balance difference is not exclusive attribution if there was other account activity. Verified scientific exports and checkpoints are on D, and this run's L4 is released and confirmed absent. All neural work ran on Colab.

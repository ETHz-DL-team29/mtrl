# Mixed SFT Continuation

Date:2026-11-12. Prepared; improvement over the original model is not yet established.

## Preservation and starting point

Both earlier adapters remain intact, with independent D-drive snapshots. Continue old SFT step250 on the same 0.8B policy and r16/alpha32 adapter. Write all new results into a separate run.

## Data

- Clean training pairs: 13717; unique target tokens: 678677.
- New validation: 80 source/reference pairs excluded from both earlier training sets; greedy selection subset32.
- Target-token exposure: general40%, technical short15%, medium25%, long20%.
- Planned whole-target stream: 1199995 tokens, 44485 example exposures. This includes explicit replay rather than pretending repeated examples are new unique data.
- Historical dev/tests and the earlier G8 sources/references remain excluded from training. Normalized equality does not rule out all near-duplicate leakage.
- 40 stratified training-pair spot checks and32 decode-validation pair checks; obvious OCR defects quarantined. Heuristic and AI screening are not native-speaker certification.

## Training

Peak LR5e-5, 3% warmup, cosine decay over1.2M target tokens. Effective batch16, microbatch2. Target-only token-weighted CE including EOS; prompts and padding excluded. Maximum full sequence768 tokens; no silent reference truncation.

Stop at the first of1.2M target tokens or3 accumulated training hours; evaluate every150k tokens and checkpoint about every5min. Early-stop after3 stale evaluations once450k tokens have been consumed. Frozen schedules/order, optimizer and RNG are resumed through two state slots.

## Validation and promotion

Checkpoint score gives general and technical domains equal weight; technical lengths are weighted equally. Invalid outputs contribute0 chrF. There is no arbitrary10% structural-failure veto. NLL breaks ties. These are selection proxies; semantic checks remain necessary.

After training, recheck matched historical32 prompts at G8/T1/256 tokens with MetricX QE, reusing the cached old baseline. Inspect meaning, negation, names, numbers and long-span relations before claiming a stronger/DAPO-ready R0. No DAPO updates in this run.

Estimate: roughly2–3h on T4 from earlier measured throughput, workload dependent. The3h cap preserves the best candidate for review. This is not a compute-unit or charge estimate.

Frozen source bundle SHA256: `663360a350ea59b5d411e697ae395441a8e53d03f2882127de79b32c7d7d4a04`.

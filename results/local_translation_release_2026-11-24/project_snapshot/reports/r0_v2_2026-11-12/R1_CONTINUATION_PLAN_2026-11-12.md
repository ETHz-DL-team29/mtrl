# R1 混合 SFT 续训 / Mixed SFT Continuation

日期 / Date: 2026-11-12. 状态 / Status: 准备完成，尚未声明新模型优于原模型 / Prepared; improvement not yet established.

## 保留与起点 / Preservation and starting point

保留原 R0 和旧 SFT，并在 D 盘 `runs/archives/r0_before_r1_2026-11-12` 保存独立适配器快照。本轮从旧 SFT step250 接着训练，模型仍为0.8B，LoRA r16/alpha32不变。结果写入新目录 `r1_sft_2026-11-12`。

Both earlier adapters remain intact, with independent D-drive snapshots. Continue old SFT step250 on the same 0.8B policy and r16/alpha32 adapter. Write all new results into a separate run.

## 数据 / Data

- 清洗后训练对 / Clean training pairs: 13717; unique target tokens: 678677.
- New validation: 80 source/reference pairs excluded from both earlier training sets; greedy selection subset32.
- 目标token曝光 / Target-token exposure: general40%, technical short15%, medium25%, long20%.
- Planned whole-target stream: 1199995 tokens, 44485 example exposures. This includes explicit replay rather than pretending repeated examples are new unique data.
- Historical dev/tests and the earlier G8 sources/references remain excluded from training. Normalized equality does not rule out all near-duplicate leakage.
- 40 stratified training-pair spot checks and32 decode-validation pair checks; obvious OCR defects quarantined. Heuristic and AI screening are not native-speaker certification.

## 训练 / Training

Peak LR5e-5, 3% warmup, cosine decay over1.2M target tokens. Effective batch16, microbatch2. Target-only token-weighted CE including EOS; prompts and padding excluded. Maximum full sequence768 tokens; no silent reference truncation.

训练上限为120万目标token或累计3小时，先到者停止；每15万token做一次完整验证，约每5分钟保存检查点。连续3次验证没有改善且已训练45万token时早停。学习率和token顺序在续跑时保持冻结，优化器/RNG通过双槽状态文件恢复。

Stop at the first of1.2M target tokens or3 accumulated training hours; evaluate every150k tokens and checkpoint about every5min. Early-stop after3 stale evaluations once450k tokens have been consumed. Frozen schedules/order, optimizer and RNG are resumed through two state slots.

## 验证与命名 / Validation and promotion

Checkpoint score gives general and technical domains equal weight; technical lengths are weighted equally. Invalid outputs contribute0 chrF. There is no arbitrary10% structural-failure veto. NLL breaks ties. These are selection proxies; semantic checks remain necessary.

训练后用原32提示、G=8、T=1、256新token上限和MetricX QE复核，并复用已保存旧SFT基线以避免重复计算。检查关键词、否定、名字、数字及长句关系；未经这些检查不将候选宣称为更强或DAPO就绪。本轮不做DAPO更新。

After training, recheck matched historical32 prompts at G8/T1/256 tokens with MetricX QE, reusing the cached old baseline. Inspect meaning, negation, names, numbers and long-span relations before claiming a stronger/DAPO-ready R0. No DAPO updates in this run.

预计 / Estimate: roughly2–3h on T4 from earlier measured throughput, workload dependent. The3h cap preserves the best candidate for review. This is not a compute-unit or charge estimate.

Frozen source bundle SHA256: `663360a350ea59b5d411e697ae395441a8e53d03f2882127de79b32c7d7d4a04`.

# New R0 implementation / 新 R0 实现

Date: 2026-11-11. Local workspace: `D:\deep learning project`.

This is a new candidate baseline, independent from historical `runs/sft_round1`.
这是独立的新候选基线，保留旧模型与旧结果。

## Data / 数据

Public OPUS Tatoeba v2023-04-12 and ParIce v1 English–Icelandic pairs, both listed in the WMT26 constrained recipe. Initially6,000 train/400dev; final OCR quarantine leaves **5,085 train /375dev**, preserving all historical200dev sources, plus86mixed generation-dev prompts. Initial target-token strata30%≤32,45%33–96,25%>96; final exact strata and token counts are in `manifest.json`. Maximum prompt+target768tokens, never truncate targets. Reserve20% general short sentences before final quarantine (final1,198Tatoeba /3,887ParIce). ParIce is mainly legal/technical, so broad-domain competence is not guaranteed. These are aligned sentences/short spans, not constructed whole documents.

公开 OPUS 英冰训练对；保留旧开发集，加入中长句并固定20%通用短句。初次抽查发现ParIce截断和OCR问题后，加强为：复制、格式、数字、字符/词数比、句末完整性、私用区字符、超长粘连词、项目符号数量、语言与归一化去重过滤。全部 WMT26 英冰测试文档及旧探针来源用于精确去重。没有文档 ID，因此不能保证文档级或近重复隔离。语义对齐仍需核查 `alignment_review.jsonl` 的 60 条样本，过滤不等同于正确金标准。

The60-pair pre-run AI screening identified clear remaining OCR/alignment defects. A conservative quarantine removes915training rows,25fresh-dev rows and10generation-dev entries (the latter overlap dev). Every rejection and reason is preserved; the original60-pair audit records rejected or needs-semantic-review status. This is not native-speaker certification. Manifest includes archive/data SHA256, counts, exclusions and token distributions. No test-set tuning.

## Training / 训练

Pinned original `Qwen/Qwen3.5-0.8B` revision `2fc06364715b967f1860aea9cf38778875588b17`; LoRA r16/alpha32/dropout0.05, same text projections as the original experiment. CUDA BF16 if supported, otherwise FP16 with loss scaling; SDPA attention. Microbatch2, effective16, target-token-weighted CE including EOS; prompt/padding labels ignored. Two pilots LR5e-5/1e-4, each20k target tokens. Select by dev generation constraints and chrF++; start the formal100k run from the original base, never a pilot checkpoint. All stages share the same frozen100k-token LR schedule (3% warmup, cosine to10% LR).

两个等预算试跑选择学习率，正式训练重新从原始模型开始。预算按真实目标 token（含 EOS）计算，单个样本不能完整装入剩余额度时停止。开发集每25k token评估；试跑每10k，试跑生成32条，正式生成全部86条；混合旧开发句与新长度分层句。完整375条开发集计算NLL。

## Selection / 选择

Prefer checkpoints whose structural failure and wrong-language rates are each≤10%, then higher dev chrF++, then lower NLL. This10% is a project screening rule, not a universal competence threshold. If none pass, the pointer remains provisional. Repetition, copying, empty/truncated outputs and language errors are recorded. Semantic validation of negation, entities, numbers and omissions is required before treating the candidate as accepted R0.

检查点选择以生成表现为主，NLL只用于同分排序；所有结果先标记为候选。G=8,T=1采样工具保留候选组用于诊断，不做DAPO更新。其chrF++分数不是MetricX训练奖励，尚未验收真实奖励排序。

## Persistence and budgets / 恢复与预算

Colab compatibility findings: its preinstalledtorchao0.10 conflicts withPEFT0.21 and is removed only in the task runtime (no quantization is used). Newtorch versions report emulatedBF16 support onT4; the loader now requiresSM80+ for nativeBF16 and usesFP16 onT4. FP16loss-scaling starts at512; overflows are safely skipped and retried at lower scales without advancing the optimized-token budget. Logs charge physical retry work and elapsed time. Preflight exercises the same optimizer-update function as formal training.

Checkpoint state includes LoRA weights, tokenizer, AdamW, scaler, Python/torch/CUDA RNG, exact example cursor, consumed target tokens, evaluation cursor, best metrics and cumulative time. Data/config hashes must match on resume. Complete checkpoint directories precede atomic `last.json` pointer publication. Retain incomplete directories for recovery; do not overwrite. CUDA nondeterminism and hardware/kernel changes can prevent bitwise equality despite restored state.

Colab notebook mounts Drive with user authorization; checkpoints go to `MyDrive/deep learning project/r0_2026-11-11`. New code/data are embedded in the notebook ZIP; no personal credentials, local model weights or historical checkpoints are uploaded. Preflight checks representative short/medium/long targets, finite gradients, GPU memory, generation and measured throughput. Below15 targettokens/s, stop and inspect fallback kernels. Estimates exclude generation/download/IO. Four-hour pipeline wall budget is checked between updates; a long evaluation can extend this. CU billing is read from Colab UI, not inferred from wall time. No purchases and no automatic300k extension.

## Running / 运行

Upload `R0_Qwen35_08B_2026-11-11.ipynb` to Colab, select a GPU and inspect available CU. Run bootstrap, authorize Drive, download/preflight, then pipeline. Do not run readiness before reviewing the candidate and remaining quota. If the session is interrupted, rerun setup and pipeline with the same Drive path; it resumes the last complete checkpoint. Existing run config cannot be changed silently.

Local data preparation requires `langid` plus existing model tokenizer:

```powershell
python -m mtgrpo.r0_data --legacy-root 'D:\deep learning project'
python -m pytest tests/test_r0.py -q
```

The new setup uses 140k total training target tokens. No result score or accepted R0 is claimed until the actual cloud run and semantic checks are complete.

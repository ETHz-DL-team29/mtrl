# New R0 implementation

Date: 2026-11-11. Local workspace: `D:\deep learning project`.

This is a new candidate baseline, independent from historical `runs/sft_round1`.
This is a separate candidate baseline; previous models and results are preserved.

## Data

Public OPUS Tatoeba v2023-04-12 and ParIce v1 English–Icelandic pairs, both listed in the WMT26 constrained recipe. Initially6,000 train/400dev; final OCR quarantine leaves **5,085 train /375dev**, preserving all historical200dev sources, plus86mixed generation-dev prompts. Initial target-token strata30%≤32,45%33–96,25%>96; final exact strata and token counts are in `manifest.json`. Maximum prompt+target768tokens, never truncate targets. Reserve20% general short sentences before final quarantine (final1,198Tatoeba /3,887ParIce). ParIce is mainly legal/technical, so broad-domain competence is not guaranteed. These are aligned sentences/short spans, not constructed whole documents.

The60-pair pre-run AI screening identified clear remaining OCR/alignment defects. A conservative quarantine removes915training rows,25fresh-dev rows and10generation-dev entries (the latter overlap dev). Every rejection and reason is preserved; the original60-pair audit records rejected or needs-semantic-review status. This is not native-speaker certification. Manifest includes archive/data SHA256, counts, exclusions and token distributions. No test-set tuning.

## Training

Pinned original `Qwen/Qwen3.5-0.8B` revision `2fc06364715b967f1860aea9cf38778875588b17`; LoRA r16/alpha32/dropout0.05, same text projections as the original experiment. Native CUDA BF16 if supported, otherwise FP16 with loss scaling; SDPA attention. Microbatch2, effective16, target-token-weighted CE including EOS; prompt/padding labels ignored. Two pilots LR5e-5/1e-4, each20k target tokens, each using the same100k-token LR schedule. Select by dev generation constraints and chrF++; start the formal run from the original base, never a pilot checkpoint. BEFORE formal training, freeze its maximum LR schedule at300k tokens (3%warmup, cosine to10%LR), with the first budget stop at100k. This permits exact optimizer/RNG/data/schedule continuation to300k only if dev keeps improving; the prepared corpus contains320,534target tokens, so100k is only0.312epoch.

Two equal-budget pilots select the learning rate; production training restarts from the original model. The budget counts actual target tokens including EOS and stops if the next complete example exceeds the remainder. Dev evaluation runs every25k tokens; pilots every10k, generating32 pilot examples and all86 production examples. Generation mixes historical dev sentences and new length-stratified cases; NLL uses all375 dev cases.

## Selection

Prefer checkpoints whose structural failure and wrong-language rates are each≤10%, then higher dev chrF++, then lower NLL. This10% is a project screening rule, not a universal competence threshold. If none pass, the pointer remains provisional. Repetition, copying, empty/truncated outputs and language errors are recorded. Semantic validation of negation, entities, numbers and omissions is required before treating the candidate as accepted R0.

Checkpoint selection prioritizes generation, using NLL only to break ties; all results remain candidates. The G=8,T=1 tool preserves sampled groups for diagnosis without DAPO updates. Its chrF++ scores are not MetricX training rewards; actual reward ranking is not validated.

## Persistence and budgets

Colab compatibility findings: its preinstalledtorchao0.10 conflicts withPEFT0.21 and is removed only in the task runtime (no quantization is used). Newtorch versions report emulatedBF16 support onT4; the loader now requiresSM80+ for nativeBF16 and usesFP16 onT4. FP16loss-scaling starts at512; overflows are safely skipped and retried at lower scales without advancing the optimized-token budget. Logs charge physical retry work and elapsed time. Preflight exercises the same optimizer-update function as formal training.

Checkpoint state includes LoRA weights, tokenizer, AdamW, scaler, Python/torch/CUDA RNG, exact example cursor, consumed target tokens, evaluation cursor, best metrics and cumulative time. Data/config hashes must match on resume. Complete checkpoint directories precede atomic `last.json` pointer publication. Retain incomplete directories for recovery; do not overwrite. CUDA nondeterminism and hardware/kernel changes can prevent bitwise equality despite restored state.

Colab notebook mounts Drive with user authorization; checkpoints go to `MyDrive/deep learning project/r0_2026-11-11`. New code/data are embedded in the notebook ZIP; no personal credentials, local model weights or historical checkpoints are uploaded. Preflight checks representative short/medium/long targets, finite gradients, GPU memory, generation and measured throughput. Below15 targettokens/s, stop and inspect fallback kernels. Estimates exclude generation/download/IO. Four-hour pipeline wall budget is checked between updates; a long evaluation can extend this. CU billing is read from Colab UI, not inferred from wall time. No purchases and no automatic300k extension. Before the formal stage, only the parent controller was replaced to freeze this extendable schedule; the active pilot worker was allowed to finish unchanged. Original and updated source bundles and elapsed wall time are retained.

## Running

Upload `R0_Qwen35_08B_2026-11-11.ipynb` to Colab, select a GPU and inspect available CU. Run bootstrap, authorize Drive, download/preflight, then pipeline. Do not run readiness before reviewing the candidate and remaining quota. If the session is interrupted, rerun setup and pipeline with the same Drive path; it resumes the last complete checkpoint. Existing run config cannot be changed silently.

Local data preparation requires `langid` plus existing model tokenizer:

```powershell
python -m mtgrpo.r0_data --legacy-root 'D:\deep learning project'
python -m pytest tests/test_r0.py -q
```

The initial plan used140k total target tokens (two20k pilots plus100k formal); actual continuation and quality results are recorded below.

## Actual execution

Use the delivered notebook in its actual staged order:100k first, then the recorded dev-based continuations. Do not replace the initial100k stop with a larger fresh-run budget: a different final minibatch can change the update trajectory. Existing Drive paths resume/reuse the saved run. For a separate reproduction, choose a new Drive run-root consistently in every cell and recheck development results before continuing; recorded continuation scores belong to the original experiment.

The local model is stored at`D:/deep learning project/runs/r0_colab_2026-11-11/best_adapter`and requires the original pinned base. The following is a usage example; training and final diagnosis ran on Colab, and new-code speed was not remeasured locally.

```python
from mtgrpo.models import Policy

policy = Policy("cuda",
    adapter=r"D:/deep learning project/runs/r0_colab_2026-11-11/best_adapter",
    attention_implementation="sdpa")
try:
    row = {"source": "The meeting starts at nine tomorrow.",
           "instruction": "Translate the following English text into Icelandic. Return only the Icelandic translation."}
    result = policy.generate(policy.prompt_ids(row, max_prompt_tokens=768), max_new_tokens=128)
    print(result["hypothesis"])
    print("truncated:", result["truncated"])
finally:
    policy.close()
```

The inference ZIP contains the selected adapter/tokenizer and evaluation evidence. Full AdamW/scaler/RNG/data-cursor checkpoints remain in Google Drive. Historical local runs are retained. A successful load or automatic language screen does not certify semantic fidelity.

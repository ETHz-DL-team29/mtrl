**Latest WMT comparison: [SFT and current DAPO results](../LATEST_RESULTS.md)**

# Models and research handoff

Three core adapters are public on HF; Code and reports are maintained on the huaq branch.**

[Public links and downloads](HUGGING_FACE.md)

Start here:

Extract the recipient ZIP, enter its `mtrl` directory, then list and verify adapters without neural dependencies or network access. Install a GPU-compatible PyTorch and the listed inference requirements. The first explicit generation downloads the pinned public base unless an appropriate local base is supplied. The ZIP contains LoRA deltas, not full base weights.

## Recommended entry points

| ID | Role | Stage |
|---|---|---|
| `qwen25-3b-sft-r0` | shared 3B baseline | SFT |
| `qwen35-08b-sft-r0` | preserved 0.8B R0 | SFT |
| `qwen35-08b-sft-technical` | technical candidate | SFT |
| `qwen25-3b-dapo-shortmid` | current dev-selected step120 | DAPO |
| `qwen25-3b-dapo-reference` | previous comparison | DAPO |

Historical SFT adapters with explicit inference folders are also preserved below. These are not every intermediate training snapshot and are not ranked by quality. Original files remain unchanged.

## Inference and further training

```bash
python scripts/models.py generate --model qwen25-3b-sft-r0 --text "Put the book on the table."
python scripts/models.py generate --model qwen35-08b-sft-r0 --text "Put the book on the table."
python scripts/models.py generate --model qwen25-3b-dapo-shortmid --text "Put the book on the table." --samples 8
```

The default is the recorded-style FP32 path. For ordinary inference on smaller GPUs choose a supported reduced precision explicitly; this is not a promise of score equivalence. No neural inference or training was rerun on the packaging computer.

```bash
python scripts/models.py generate --model qwen25-3b-sft-r0 --precision float16 --text "Hello."
python scripts/models.py generate --model qwen25-3b-sft-r0 --base-path /path/to/pinned/qwen-base --offline --text "Hello."
```

Integrate into your own SFT/RL code:

```python
from mtrl.checkpoints import load_translation_model, translate

model, tokenizer, info = load_translation_model(
    "qwen25-3b-sft-r0", device="cuda", trainable=True,
)
# Existing LoRA parameters are trainable. No optimizer step happens here.
# Exact historical DAPO additionally requires its archived dropout/optimizer/sampling settings.
```

Install the local package or add `src` to PYTHONPATH. English-to-Icelandic is the demonstrated task. Other tasks are not validated. These research models can mistranslate critical facts. The API exposes adapter continuation, not an exact historical optimizer/RNG resume.

Colab example: [notebooks/use_shared_models.ipynb](../notebooks/use_shared_models.ipynb). It performs inference only unless you separately write a training loop.

## Results and executed code

- [Results index](../results/local_translation_release_2026-11-24/README.md)
- [Registry and hashes](registry.json)
- `results/local_translation_release_2026-11-24/project_snapshot/experiments/` archives executed P18 SFT, 0.8B technical SFT and P25 DAPO source. Historical absolute paths and budgets are provenance; do not relaunch expired-budget scripts unchanged.
- The collaborator's original `src/mtrl/train/`, scorers and experimental implementation were preserved. The added loader exposes saved weights.

Executed historical scripts are archived separately; the collaborator's original training/scoring code was not replaced. Historical scripts include fixed Colab paths and expired absolute budgets and are not a new training launch command.

## Storage and future sharing

Three selected models are now hosted publicly with pinned commits and verified weights. See [HUGGING_FACE.md](HUGGING_FACE.md). The full local ZIP preserves all14 adapters; historical variants were not uploaded.

## Base licenses

Base-model and source-data terms still apply. This handoff does not relicense the repository or adapters. Official pinned model cards:

- [Qwen3.5-0.8B / Apache-2.0](https://huggingface.co/Qwen/Qwen3.5-0.8B/blob/2fc06364715b967f1860aea9cf38778875588b17/README.md)
- [Qwen2.5-3B-Instruct / qwen-research](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/blob/aa8e72537993ba99e69dfaafa59ed015b17504d1/README.md)

## Complete local adapter inventory

|ID|Stage|LoRA r|Weight MiB|Card|
|---|---|---:|---:|---|
|`qwen25-3b-sft-r0`|sft|64|456.81|[card](cards/qwen25-3b-sft-r0.md)|
|`qwen25-3b-dapo-shortmid`|dapo|64|456.81|[card](cards/qwen25-3b-dapo-shortmid.md)|
|`qwen35-08b-sft-r0`|sft|16|41.34|[card](cards/qwen35-08b-sft-r0.md)|
|`qwen35-08b-sft-technical`|sft|16|41.34|[card](cards/qwen35-08b-sft-technical.md)|
|`qwen25-3b-dapo-reference`|dapo|64|456.81|[card](cards/qwen25-3b-dapo-reference.md)|
|`archive-r0-3b-coverage-sft-2026-11-20-final-selected-adapter`|sft|16|114.25|[card](cards/archive-r0-3b-coverage-sft-2026-11-20-final-selected-adapter.md)|
|`archive-r0-3b-filtered-sft-resume-2026-11-20-final-selected-adapter`|sft|16|114.25|[card](cards/archive-r0-3b-filtered-sft-resume-2026-11-20-final-selected-adapter.md)|
|`archive-r0-3b-overnight-2026-11-18-final-selected-adapter`|sft|16|114.25|[card](cards/archive-r0-3b-overnight-2026-11-18-final-selected-adapter.md)|
|`archive-r0-3b-round1-2026-11-17-final-trained-adapter`|sft|16|114.25|[card](cards/archive-r0-3b-round1-2026-11-17-final-trained-adapter.md)|
|`archive-r0-3b-round1-2026-11-17-selected-candidate-adapter`|sft|16|114.25|[card](cards/archive-r0-3b-round1-2026-11-17-selected-candidate-adapter.md)|
|`archive-r0-colab-2026-11-11-best-adapter`|sft|16|41.34|[card](cards/archive-r0-colab-2026-11-11-best-adapter.md)|
|`archive-r0-technical-sft-2026-11-17-final-trained-adapter`|sft|16|41.34|[card](cards/archive-r0-technical-sft-2026-11-17-final-trained-adapter.md)|
|`archive-r0-v2-colab-2026-11-12-best-adapter`|sft|16|41.34|[card](cards/archive-r0-v2-colab-2026-11-12-best-adapter.md)|
|`archive-r0-v3-colab-2026-11-13-best-adapter`|sft|16|41.34|[card](cards/archive-r0-v3-colab-2026-11-13-best-adapter.md)|

# Public model sharing — 2026-11-24

Three models are uploaded and public. Anonymous metadata/configuration access and remote LFS weight hashes were verified against the original local adapters. Code was initially delivered locally for the owner to push.

|Local ID|Public Hub|Pinned commit|
|---|---|---|
| `qwen35-08b-sft-r0` | [huaq99/mtrl-qwen35-08b-en-is-sft-r0](https://huggingface.co/huaq99/mtrl-qwen35-08b-en-is-sft-r0) | `c95800cbefea66cbe449a482c7515a74a6984564` |
| `qwen25-3b-sft-r0` | [huaq99/mtrl-qwen25-3b-en-is-sft-r0](https://huggingface.co/huaq99/mtrl-qwen25-3b-en-is-sft-r0) | `ae660dd4ea272fff7caf840d2c9ccc76401e6780` |
| `qwen25-3b-dapo-shortmid` | [huaq99/mtrl-qwen25-3b-en-is-dapo-shortmid-v1](https://huggingface.co/huaq99/mtrl-qwen25-3b-en-is-dapo-shortmid-v1) | `1ec9cfaa813582bda509676497da2ffb2e69e6bc` |

These are LoRA adapters, not full Qwen bases. Recipients may perform inference or continue SFT/RL under the applicable licenses without using the owner's HF login or token. The 3B base uses qwen-research and the 0.8B base uses Apache-2.0. Public download does not waive licensing or data terms.

## Download using this repository

```bash
pip install huggingface_hub
python scripts/download_models.py --model all-hosted
python scripts/models.py verify --model qwen35-08b-sft-r0
python scripts/models.py verify --model qwen25-3b-sft-r0
python scripts/models.py verify --model qwen25-3b-dapo-shortmid
```

The downloader fetches only the three registered hosted adapters and verifies pinned commits and SHA256 hashes. Other historical versions require the complete local ZIP. Git-ignored weights are not included in a Git clone.

In a GPU environment, install compatible PyTorch and `setup/requirements-checkpoint-use.txt`, then run:

```bash
python scripts/models.py generate --model qwen25-3b-sft-r0 --text "Put the book on the table."
python scripts/models.py generate --model qwen25-3b-dapo-shortmid --text "Put the book on the table."
```

The default FP32 path requires substantial GPU memory. Ordinary inference can explicitly use `--precision float16` or supported `bfloat16`; this does not guarantee reproduction of FP32 benchmark scores.

Standalone Colab notebook: [use_hf_models.ipynb](../notebooks/use_hf_models.ipynb). Upload the local notebook to Colab. Packaging did not start GPU training or execute this notebook.

HF's standard `adapter_config.json` uses a portable base-model ID and revision;`original_adapter_config.json` retains the original configuration. Weight bytes are unchanged. The repository downloader restores the original configuration to match frozen local hashes, while the loader explicitly selects the correct base.

Verification record: [hf_publication.json](hf_publication.json); results: [LATEST_RESULTS.md](../LATEST_RESULTS.md). The complete local bundle preserves 14 adapters.

The three public research adapters are pinned above. Public downloads require no account. The verified weight hashes match the source files; no merging, quantization or retraining occurred. Only three selected adapters are hosted; fourteen are preserved locally. Code and results are maintained separately on the repository huaq branch; the owner controls publication of subsequent changes.

# Model and experiment delivery — 2026-11-24

- Fourteen actual LoRA adapters are preserved locally: twelve SFT and two DAPO, including default 0.8B/3B baselines and labeled historical variants. Original weights were not moved, merged, quantized or overwritten.
- Three core adapters are public on Hugging Face: 0.8B SFT R0, 3B SFT R0 and the latest 3B DAPO candidate. Anonymous configuration access and remote LFS weight hashes were verified. See [public links and instructions](models/HUGGING_FACE.md).
- The homepage and [LATEST_RESULTS.md](LATEST_RESULTS.md) highlight P25 with matched WMT26 results, exploratory subsets, confidence intervals and limitations.
- Portable commands expose model listing, integrity checks, hosted downloads and inference. The Python loader supports trainable adapters for new experiments, but does not restore historical optimizer/RNG state.
- All 41 CPU tests passed during delivery. Fourteen adapter hashes/tensor structures passed. Packaging/localization did not allocate a GPU, retrain models or rerun neural inference.
- The complete local delivery ZIP contains code, reports and actual adapters; it excludes full Qwen base weights and credentials. Files under artifacts/ and deliveries/ are Git-ignored. The preserved original ZIPs predate this English-only edition.
- Base licenses remain applicable: Apache-2.0 for Qwen3.5-0.8B and qwen-research for Qwen2.5-3B-Instruct, together with source-data/project terms.
- The original code/results delivery was pushed by the owner as commit f82bd68 on huaq. This English edition is prepared as a new local commit named `update md file and code`, for the owner to push.

All Git-managed text and embedded archive text have English editions. Historical failed generations containing Chinese fragments use explicitly bracketed English explanations; recorded metric values continue to describe the original predictions. See [English-edition provenance and recovery](results/local_translation_release_2026-11-24/ENGLISH_EDITION.md) before rescoring display excerpts.

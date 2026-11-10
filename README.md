# mtrl

Compute-efficient reinforcement learning (GRPO-style) for low-resource English-to-xx machine translation with small language models.

**Current stage: zero-shot evaluation.** No training yet. Off-the-shelf Qwen3.5-0.8B and Qwen3.5-2B translate a fixed set of segments; the outputs are checked, scored and summarised to decide whether, and how, RL training is worthwhile. The stage answers four questions:

1. How good are the models zero-shot on each direction, and how much headroom is left?
2. With thinking enabled, what share of the generated tokens is reasoning, and does it improve quality?
3. When sampling G = 8 translations per segment at T = 1.0, how much does the reward vary within a group? Near-zero variance means GRPO gets no learning signal.
4. How often do outputs fail the rule-based gate (parse failure, empty output, copied source, wrong language, abnormal length), and for which reasons?

Training code (SFT, GRPO) exists only as documented placeholder modules.

**Core data convention:** every model output is split into a *reasoning* part and a *translation* part, and the tokens of each part are counted separately (`Rollout.reasoning`, `Rollout.translation`). Both planned methods, selective token updates and reasoning-prefix reuse, depend on this split.

Code is developed on a laptop; all scripts run on a single-GPU Linux server (RTX 4070 Super, 12 GB).

---

## 1. Repository layout

| Path | Contents |
| --- | --- |
| `configs/zeroshot.yaml` | Experiment config: directions, models, thinking settings, sampling, prompt template, metrics |
| `configs/quick.yaml` | Quick end-to-end check: en-is only, Qwen3.5-0.8B, thinking off, 5 documents; results go to `runs/quick/` |
| `configs/env/local_4070S_12G.yaml` | Hardware and paths: dtype, vLLM memory settings, scoring batch size |
| `configs/env/euler_1080Ti_11G.yaml` | Placeholder (comments only) for the Euler cluster; not used yet |
| `configs/languages.yaml` | Per target language: English name, fastText label, allowed length ratio, WMT26 language code |
| `src/mtrl/common/` | Shared foundation used by every stage |
| `src/mtrl/common/config.py` | Loads and merges the experiment and env configs; writes `config.resolved.yaml` |
| `src/mtrl/common/env_setup.py` | Sets cache directories, reads `.env`, checks that the GPU matches the env name |
| `src/mtrl/common/records.py` | Record types: `Segment` (source and optional reference), `Rollout` (one model output), `Score` (gate result, metrics, reward) |
| `src/mtrl/common/jsonl_io.py` | jsonl read/write, crash-safe append, set of completed keys for resuming |
| `src/mtrl/common/flops_accounting.py` | FLOPs accounting from token counts (pure functions) |
| `src/mtrl/data/segment_loader.py` | `load_segments()`: reads processed `Segment` files |
| `src/mtrl/data/wmt26_converter.py` | WMT26 test set -> `Segment` rows; HTML-to-text cleanup |
| `src/mtrl/generation/` | Producing model outputs |
| `src/mtrl/generation/prompting.py` | `build_messages()` and `parse_output()` (reasoning/translation split, wrapper stripping) |
| `src/mtrl/generation/vllm_generate.py` | Generation with vLLM |
| `src/mtrl/scoring/` | Judging model outputs |
| `src/mtrl/scoring/rule_gate.py` | Rule-based gate: parse_fail, empty, copy_source, wrong_lang, length_ratio |
| `src/mtrl/scoring/metrics.py` | MetricX-24 (QE and reference-based), CometKiwi22, chrF++, COMET-22 behind one signature |
| `src/mtrl/scoring/reward.py` | `reward = gate * (1 - MetricX_QE / 25)` |
| `src/mtrl/analysis/zeroshot_stats.py` | Summary tables and figures |
| `src/mtrl/train/` | Placeholders: `sft.py`, `grpo.py`, `masks.py`, `prefixes.py` |
| `scripts/run.py` | **Main entry point**: runs all stages for one config |
| `scripts/` (others) | One script per stage: `download.py`, `prepare_data.py`, `generate.py`, `score.py`, `analyze.py` |
| `scripts/verify_metricx.py` | One-off check that our MetricX scores match the official implementation (Section 3.7) |
| `scripts/_cli.py` | Shared command-line arguments of the stage scripts |
| `setup/` | Dependency list and server install script |
| `tests/` | CPU-only tests; no GPU packages required |
| `data/`, `runs/` | Data and run outputs; not tracked by git (see Section 5) |

---

## 2. Installation (Linux server, once)

```bash
git clone https://github.com/ETHz-DL-team29/mtrl.git && cd mtrl
```

```bash
bash setup/install_local_4070S_12G.sh mtrl
```

The script creates the conda environment `mtrl` with Python 3.11 (or reuses an existing one; the server's current `mtrl` environment uses Python 3.12, which vLLM also supports), installs **vLLM first** so that vLLM determines the torch and CUDA versions, then installs `setup/requirements.txt` and the package itself (`pip install -e .`), and writes the installed versions to `setup/requirements.lock.txt`. **Commit that file after the first successful install.** The script downloads no models or data; `scripts/run.py` does that.

Create the per-machine settings file:

```bash
cp .env.example .env
```

Edit `.env` and set:

- `HF_TOKEN=...`: Hugging Face token used for all model downloads;
- `MTRL_ENV=local_4070S_12G`: the env config this machine uses, so that `--env` never has to be typed.

`.env` is git-ignored. CometKiwi22 (`Unbabel/wmt22-cometkiwi-da`) is gated: accept its terms on the Hugging Face model page with the account that owns the token.

Verify the install:

```bash
conda activate mtrl && pytest -q
```

---

## 3. Running

Everything is driven by one command and one config file. Run from the repository root inside the `mtrl` environment.

### 3.1 Quick end-to-end check (run this first)

```bash
python scripts/run.py configs/quick.yaml
```

This runs en-is only, Qwen3.5-0.8B, thinking off and 5 documents, and finishes in a few minutes. Afterwards `runs/quick/report/summary.md` should exist. If a stage fails, the error is in `runs/quick/logs/<stage>.log`.

### 3.2 Full zero-shot run

```bash
python scripts/run.py configs/zeroshot.yaml
```

Start it inside `tmux` so that it survives a dropped SSH connection. Results go to `runs/zeroshot_v1/`.

### 3.3 What `run.py` does

It runs five stages in order, each in its own process. Generation and scoring therefore never share the GPU, and scoring loads one metric model at a time.

| Stage | Script | What it does |
| --- | --- | --- |
| `download` | `download.py` | **The only stage that uses the network.** Downloads the policy models, the scorer models and the tokenizers they load (MetricX + mT5, CometKiwi + InfoXLM, COMET-22 + XLM-R) into the Hugging Face cache, and the WMT26 test set and fastText `lid.176.bin` into `data/`. Fails early if a required model is unavailable; warns if a gated optional one (CometKiwi) is |
| `prepare` | `prepare_data.py` | Offline: converts `data/raw/wmt26-genmt.jsonl` into `data/processed/{direction}/{split}.jsonl`; skips directions that already exist |
| `generate` | `generate.py` | Greedy + G sampled outputs with vLLM -> `rollouts.jsonl` |
| `score` | `score.py` | Gate, metrics, reward -> `scores.jsonl` |
| `analyze` | `analyze.py` | Summary tables and figures -> `report/` |

Where downloads go: models and tokenizers in the Hugging Face cache (`paths.hf_home` in the env config); everything else under `data/` (`data/raw/` for the test set, `data/models/` for fastText, `data/processed/` for converted segments).

Useful variations:

| Goal | Command |
| --- | --- |
| Run only some stages | `python scripts/run.py configs/zeroshot.yaml --stages score,analyze` |
| Use another env config | `python scripts/run.py configs/zeroshot.yaml --env <name>` |
| Change what is run | Edit or copy the config: `directions`, `models`, `thinking`, `limit`, `metrics` |

The stage scripts can also be run directly for debugging, e.g. `python scripts/score.py --config configs/zeroshot.yaml --metric chrf`. They accept `--model`, `--thinking true/false`, `--limit N` and (score only) `--metric NAME`; command-line values override the config.

### 3.4 Resuming after an interruption

Re-run the same command.

- `generate.py` appends to `rollouts.jsonl` after every `chunk_size` segments (default 50) and skips keys `(seg_id, sample_idx, model, thinking)` that already exist. An interruption loses at most the chunk in progress.
- `score.py` keeps one part file per stage, `score_parts/{gate,<metric>}.jsonl`, each resumed independently by the same key. `scores.jsonl` is rebuilt from the part files at the end of every run.
- A line truncated by an interruption is skipped on read (with a warning), and the next append starts on a fresh line.
- `download` and `prepare` skip anything already present.

### 3.5 Data: WMT26 General MT test set

Source: `data/wmt26-genmt.jsonl` of [wmt-conference/wmt26-general-mt](https://github.com/wmt-conference/wmt26-general-mt) (format checked on 2026-11-10).

- 198 documents per English-to-X direction; the same English documents for every target language.
- Human references exist for en-is and en-et only; en-hy, en-be and en-kk are scored with reference-free metrics only.
- Inputs are documents (median ~400 characters, max ~4,700). The `<p>` / `<br>` markup is converted to one line per paragraph and HTML entities are unescaped.
- Speech-domain inputs are ASR transcripts (the official text input); the manual transcript is kept in `meta.gold_transcript`. Video and screenshot inputs are ignored.
- This is the official test set; WMT26 has no separate dev set, so `split: test`.

### 3.6 Expected runtime (estimate, not measured)

Full run: 5 directions x 198 documents x 2 models x 2 thinking settings x 9 outputs (1 greedy + 8 samples) = 35,640 outputs.

- Thinking off: assuming ~400 tokens per output (document-level), about 7M generated tokens.
- Thinking on: assuming ~1,400 tokens per output, about 25M generated tokens.
- At an assumed vLLM throughput of ~5k tokens/s (0.8B) and ~2.5k tokens/s (2B) on the 4070 Super, generation takes about 3 hours; scoring adds about 1-1.5 hours.

**Total: about 4-5 hours, which should fit in one night.** The throughput figures are assumptions. After the quick check, re-estimate from measured throughput:

```bash
python -c "import pandas as pd; d=pd.read_json('runs/quick/compute.jsonl',lines=True); g=d[d.type=='gen']; print((g.reasoning_tokens+g.translation_tokens).sum()/g.wall_s.sum(),'gen tok/s')"
```

If the full run is not expected to finish overnight, report the estimate before reducing its scope.

### 3.7 Verifying MetricX

Run once on the GPU server after the quick check, before trusting any reward:

```bash
python scripts/verify_metricx.py configs/quick.yaml
```

It scores the same inputs (the first 16 rollouts, or references if no rollouts exist yet) with our implementation and with the official `MT5ForRegression` from google-research/metricx (cloned into `data/external/metricx` on first use, never pip-installed), and prints both scores and their absolute difference per example, plus the maximum and mean difference for the QE and, when every example has a reference, the reference-based mode. It exits with `OK` and status 0 if the maximum difference is within the tolerance (0.05 for bf16, 1e-3 for fp32; override with `--tol`), and with `MISMATCH` and status 1 otherwise.

---

## 4. Configuration

- **Experiment configs** (`configs/zeroshot.yaml`) specify *what* to run and contain no paths or memory settings. **Env configs** (`configs/env/*.yaml`) specify hardware and paths only. A top-level key defined in both, or an unknown key, raises an error.
- **Env selection:** `--env` if given, otherwise `MTRL_ENV` from the shell or `.env`.
- **Env naming:** `[provider]_[gpu]_[gdram]`, e.g. `local_4070S_12G`. The file name, the `name` field and the env name used must be identical, and the memory in the name must equal `gpu.mem_gb`.
- **GPU check** at the start of `generate.py` and `score.py`; any failure aborts the run instead of silently downgrading:
  - the device name must contain `gpu.match`;
  - total memory must be within 15% of `gpu.mem_gb`;
  - `dtype: bf16` requires compute capability >= 8.0;
  - `use_vllm: true` requires compute capability >= 7.0.
- Relative paths in env configs are resolved against the repository root.
- `limit` (experiment config) keeps only the first N documents per direction; `null` means all.
- Output length limits: 3072 tokens with thinking off, 6144 with thinking on, sized for document-level inputs. `vllm.max_model_len: 8192` must cover the prompt plus the output limit.
- The `len_ratio` ranges in `languages.yaml` are initial values; re-tune them from the length distribution of the greedy outputs.

---

## 5. Outputs (`runs/{run_name}/`)

| File | Contents |
| --- | --- |
| `config.resolved.yaml` | Merged config, git commit and timestamp (rewritten by every `generate.py` / `score.py` run) |
| `rollouts.jsonl` | One `Rollout` per line: raw output, reasoning and translation, prompt/reasoning/translation token counts, finish reason, parse status. Greedy outputs have `sample_idx = -1`; samples have `0..G-1` |
| `score_parts/gate.jsonl` | Gate result and failure reason per rollout |
| `score_parts/<metric>.jsonl` | Metric value per rollout. Empty or unparsable translations are not scored; reference-based metrics are computed only where a reference exists |
| `scores.jsonl` | One `Score` per line: gate result, `metrics` dict (missing metrics omitted, never written as 0), reward. Reward is 0 if the gate fails and null if the gate passes but MetricX-QE has not been computed yet |
| `compute.jsonl` | `type=header`: GPU name, memory, compute capability. `type=gen`: tokens, FLOPs, wall time and GPU memory per generation chunk. `type=score`: inputs, tokens, FLOPs and wall time per scoring chunk |
| `report/summary.csv` | All statistics per (direction, model, thinking) |
| `report/summary.md` | Main table and gate-failure breakdown |
| `report/reward_thinking.png` | Greedy reward with thinking on vs. off, per direction |
| `report/reward_std_hist.png` | Distribution of the within-group reward standard deviation |

Main columns of `summary`:

| Column | Meaning |
| --- | --- |
| `qe_greedy_mean` | Mean MetricX-24 QE of greedy outputs (0-25, lower is better) |
| `kiwi_greedy_mean` | Mean CometKiwi22 of greedy outputs (if available) |
| `reward_greedy_mean` | Mean reward of greedy outputs |
| `gate_fail_rate`, `gate_fail_<reason>` | Share of scored rollouts failing the gate, overall and per reason |
| `reward_std_within_group_mean` | Standard deviation of the G sampled rewards per segment, averaged over segments |
| `frac_low_variance_groups` | Share of segments whose within-group std is below `analysis.low_variance_eps` (groups rejected entirely by the gate count as low-variance) |
| `best_of_G_minus_mean` | Per segment, max minus mean of the G rewards, averaged; a rough measure of learnable headroom |
| `reasoning_tokens_mean`, `translation_tokens_mean` | Mean token counts of the two output parts |
| `reasoning_token_share` | Reasoning tokens as a share of all generated tokens |
| `truncation_rate` | Share of outputs with `finish_reason == "length"` |
| `B_test_flops` | Generation plus scoring FLOPs |

**FLOPs accounting:**

- Forward pass: 2 * N * tokens; training step: 6 * N * tokens. Parameter counts N come from the config (`models[].n_params`, `scorer_params`), so analysis never loads a model.
- Prompt tokens are counted once per rollout, without credit for vLLM prefix caching; generation FLOPs are therefore an upper bound.
- Scorer input tokens are counted with the mT5 tokenizer for all neural metrics, which is an approximation for the COMET models.

---

## 6. Implementation notes

- **Thinking switch.** Thinking is controlled by the chat-template argument `enable_thinking`, not by the prompt.
  - With thinking on, the Qwen3.5 template ends the prompt with `<think>`, so the output usually contains only the closing `</think>`. `parse_output` handles both forms.
  - Thinking on but no `</think>` in the output (typically truncation at the length limit) is recorded as `parse_ok = False`.
- **Wrapper stripping.** The rules live in two lists in `generation/prompting.py`, `PREFIX_PATTERNS` and `QUOTE_PAIRS`; extend them there.
- **Seeds.** Sampling seeds are derived from `seg_id`, so results do not depend on chunking or on where a run was resumed.
- **MetricX-24.** The official repository is not a dependency.
  - Its `MT5ForRegression` is equivalent to running Hugging Face `MT5ForConditionalGeneration` for one decoder step from token 0, reading the logit of `<extra_id_10>` (id 250089) and clamping it to [0, 25]. The checkpoint weights load directly into the Hugging Face class.
  - Input format and truncation (1536 tokens, trailing EOS removed) follow the official `predict.py`.
- **CometKiwi22** is gated. Without access, `score.py` prints a warning and skips this metric; all other metrics still run.
- **fastText and numpy >= 2.** The known `copy=False` incompatibility is worked around in `scoring/rule_gate.py` (`predict_lang`).

---

## 7. Open items

- **Never run on a GPU yet.** vLLM generation, MetricX / COMET scoring and the NVML GPU check have only been written, not executed. Expect fixes after the first quick check.
- **MetricX equivalence.** MetricX is computed with `MT5ForConditionalGeneration` instead of the official `MT5ForRegression` (see Section 6). Run `scripts/verify_metricx.py` (Section 3.7) on the server before trusting the rewards.
- **MetricX input length.** MetricX truncates its input (source + translation) to 1536 tokens. Roughly the longest 10-15% of WMT26 documents exceed this, so their QE score covers only the beginning of the document.
- **Qwen3.5 in vLLM.** The small Qwen3.5 models are published as image-text-to-text. Text-only prompts worked on this server in October 2026 with `limit_mm_per_prompt={image: 0, video: 0}`; re-check after a vLLM upgrade.
- **CometKiwi22 access.** Access worked in October 2026; re-check if the token or account changes.
- **MetricX bf16 checkpoint.** Confirm that `google/metricx-24-hybrid-large-v2p6-bfloat16` exists. If it does not, `download` and `score` fall back to the fp32 checkpoint loaded in the env dtype.

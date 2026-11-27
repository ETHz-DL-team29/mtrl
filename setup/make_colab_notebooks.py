"""Writes the two Colab notebooks (edit here, not in the .ipynb files):

    python setup/make_colab_notebooks.py

  setup/colab_run.ipynb         template: set REF and CONFIGS in the first code cell, Run all
  setup/colab_smoke_test.ipynb  checks a fresh runtime end to end (setup, tests, SFT, RL, resume)

Both are thin: installation is setup/colab_setup.sh, the experiment pipeline is
scripts/run_experiments.py, the experiment itself is a training YAML.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_URL = "https://github.com/ETHz-DL-team29/mtrl.git"
DRIVE = "/content/drive/MyDrive/mtrl"   # must match configs/env/_colab.yaml (runs_dir, ckpt_dir)


def md(s):
    return {"cell_type": "markdown", "metadata": {}, "source": s.strip("\n").splitlines(keepends=True)}


def code(s):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": s.strip("\n").splitlines(keepends=True)}


CLONE = f"""
from google.colab import drive
drive.mount('/content/drive')
import os
for d in ('runs', 'ckpt', 'data_cache'):
    os.makedirs(f'{DRIVE}/{{d}}', exist_ok=True)

%cd /content
if not os.path.isdir('/content/mtrl/.git'):
    !git clone -q {REPO_URL} /content/mtrl
!git -C /content/mtrl fetch -q && git -C /content/mtrl checkout -q {{REF}} && (git -C /content/mtrl pull -q --ff-only 2>/dev/null || true)
%cd /content/mtrl
!git log --oneline -1
"""

SETUP = """
!bash setup/colab_setup.sh
import sys
sys.path.insert(0, '/content/mtrl/src')   # this kernel started before mtrl was installed
os.environ['MTRL_ENV'] = open('.env').read().split('=', 1)[1].strip()
print('MTRL_ENV =', os.environ['MTRL_ENV'])
"""


def colab_run():
    return [
        md("""
# mtrl on Colab: run experiments

The experiment is a training YAML; this notebook only runs it. To use it:

1. **Runtime → Change runtime type**: **L4** (recommended, bf16) or A100 40/80 GB.
   T4 only does fp16, which may overflow with Qwen3.5.
2. Edit the **first code cell** (`REF`, `CONFIGS`, `EVAL`).
3. **Runtime → Run all.**

What happens (`scripts/run_experiments.py`):

| Step | What |
|---|---|
| setup | `setup/colab_setup.sh`: packages, scorer and mtdata venvs, env config for this GPU (skips what is already there) |
| data | builds the splits for the directions the configs use; cached on Drive (`mtrl/data_cache`), so later sessions skip it |
| train | each config in order; runs and checkpoints are on Drive (`mtrl/runs`, `mtrl/ckpt`) |
| evaluate | greedy evaluation on the config's eval split (NTREX-128 `ntrex_dev` by default) |
| compare | one table over these runs |

**Disconnected?** Open the notebook again and Run all: finished steps are skipped and
training resumes from its last checkpoint. Set `schedule.max_hours` in the config below
the session length to stop cleanly with a checkpoint.

**Trying a variation without committing it:** write a YAML on Drive that inherits from
one in the repo, and put its path in `CONFIGS`:

```yaml
# /content/drive/MyDrive/mtrl/configs/try_lr.yaml
base: /content/mtrl/configs/train/ym/wide_all_ref.yaml
run_name: try_lr_5e-5
optim: {lr: 5.0e-5}
```

The merged config and the git commit end up in `mtrl/runs/<run_name>/config.resolved.yaml`.
Move configs worth keeping into `configs/train/` in the repo.

**Speed:** Colab's CPU makes small batches and token-by-token generation about 3x slower
than the local server; RL runs are better there (docs/training.md, Platforms).
"""),
        code("""
# ---------------- edit this cell only ----------------
REF = 'train/merge-ym'        # branch, tag or commit of the code (a commit pins the run)
CONFIGS = [                   # training YAMLs, run in order: repo paths or files on Drive
    'configs/train/quick_sft.yaml',
]
EVAL = True                   # evaluate each run after training
# ------------------------------------------------------
"""),
        md("## Drive and code"),
        code(CLONE),
        md("## Setup (idempotent)"),
        code(SETUP),
        md("## Data, training, evaluation"),
        code(f"""
args = ' '.join(CONFIGS) + ('' if EVAL else ' --no-eval')
!python scripts/run_experiments.py {{args}} --data-cache {DRIVE}/data_cache
"""),
        md("## Training curves"),
        code(f"""
import json, pathlib
import matplotlib.pyplot as plt
from mtrl.common.train_config import load_train_config

fig, axes = plt.subplots(1, 2, figsize=(12, 3.5))
for cfg in CONFIGS:
    name = load_train_config(cfg).train.run_name
    run = pathlib.Path('{DRIVE}/runs') / name
    tl = [json.loads(l) for l in (run / 'train_log.jsonl').read_text().splitlines()]
    key = 'reward' if 'reward' in tl[0] else 'loss'
    axes[0].plot([x['step'] for x in tl], [x[key] for x in tl], label=f'{{name}} ({{key}})')
    vp = run / 'val_log.jsonl'
    vl = [v for v in map(json.loads, vp.read_text().splitlines()) if 'val_chrf' in v] if vp.exists() else []
    axes[1].plot([v['step'] for v in vl], [v['val_chrf'] for v in vl], marker='o', label=name)
axes[0].set_title('training: reward (RL) or loss (SFT)'); axes[0].set_xlabel('step'); axes[0].legend()
axes[1].set_title('validation chrF++ (ntrex_val)'); axes[1].set_xlabel('step'); axes[1].legend()
plt.tight_layout(); plt.show()
"""),
    ]


def colab_smoke_test():
    return [
        md("""
# mtrl on Colab: smoke test

Checks a fresh runtime end to end: setup, unit tests, a few SFT and RL steps with
Qwen3.5-2B on en-is and en-kk, and resume from a checkpoint. About 15–25 minutes, mostly
installs and the first model download. Pick **L4** (or A100) under Runtime → Change
runtime type, then Run all. To run real experiments use `setup/colab_run.ipynb`.
"""),
        code("REF = 'train/merge-ym'   # branch or commit to test"),
        code(CLONE),
        code(SETUP),
        md("## Unit tests"),
        code("!python -m pytest -q tests 2>&1 | tail -3"),
        md("## SFT and RL smoke runs (6 steps each), starting from scratch"),
        code(f"""
!rm -rf {DRIVE}/runs/quick_sft {DRIVE}/runs/quick_rl {DRIVE}/ckpt/quick_sft {DRIVE}/ckpt/quick_rl
!python scripts/run_experiments.py configs/train/quick_sft.yaml configs/train/quick_rl.yaml --no-eval --data-cache {DRIVE}/data_cache
"""),
        md("## Resume: raise the step count; training must continue at step 6, not 0"),
        code("""
!sed -i 's/steps: 6/steps: 8/' configs/train/quick_sft.yaml
!python scripts/train.py configs/train/quick_sft.yaml 2>&1 | grep -E "resumed|^\\[sft\\]" | cut -c1-160
!git checkout -q configs/train/quick_sft.yaml
"""),
        md("## Summary to report back"),
        code(f"""
import json, pathlib
runs = pathlib.Path('{DRIVE}/runs')
for r in ['quick_sft', 'quick_rl']:
    log = [json.loads(l) for l in (runs / r / 'train_log.jsonl').read_text().splitlines()]
    val = [json.loads(l) for l in (runs / r / 'val_log.jsonl').read_text().splitlines()] if (runs / r / 'val_log.jsonl').exists() else []
    print(r, '| steps', len(log), '| max vram_gb', max(x.get('vram_gb', 0) for x in log),
          '| median sec/step', sorted(x['sec'] for x in log[1:])[len(log[1:]) // 2] if len(log) > 1 else None,
          '| nonfinite', sum(x.get('skipped_nonfinite', 0) for x in log),
          '| last val', {{k: v for k, v in (val[-1] if val else {{}}).items() if k in ('val_chrf', 'val_gate_pass', 'error')}})
"""),
    ]


def write(path, cells):
    nb = {"cells": cells, "metadata": {"accelerator": "GPU", "colab": {"provenance": [], "gpuType": "L4"},
                                       "kernelspec": {"display_name": "Python 3", "name": "python3"},
                                       "language_info": {"name": "python"}},
          "nbformat": 4, "nbformat_minor": 0}
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
    print(path)


if __name__ == "__main__":
    write(HERE / "colab_run.ipynb", colab_run())
    write(HERE / "colab_smoke_test.ipynb", colab_smoke_test())

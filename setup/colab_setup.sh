#!/usr/bin/env bash
# Set up mtrl in a Google Colab runtime. Idempotent: every part is skipped when it is
# already in place, so every notebook can start with it (setup/colab_run.ipynb,
# setup/colab_smoke_test.ipynb). Run from the repo root:
#
#   bash setup/colab_setup.sh
#
# What it does, and why:
#   1. Runtime Python (Colab's own, 3.13): transformers 5.x + peft for Qwen3.5 training,
#      fastText from the fasttext-numpy2 fork (the only build with Python 3.13 wheels),
#      flash-linear-attention (Triton kernels for Qwen3.5's linear-attention layers).
#      Removes Colab's torchao 0.10: peft refuses to attach LoRA next to torchao < 0.16.
#   2. Scorer venv (Python 3.12, /content/score-venv): MetricX / COMET need
#      transformers 4.x and numpy<2, which conflict with (1) and have no 3.13 wheels.
#   3. mtdata venv (Python 3.12, /content/mtdata-venv): training-data download only.
#   4. mtrl itself, editable, into (1) and (2): no PYTHONPATH needed.
#   5. fastText language-ID model (data/models/lid.176.bin).
#   6. The env config for this GPU (scripts/pick_env.py colab) set as MTRL_ENV in .env
#      (other lines of .env, e.g. HF_TOKEN, are kept).
# The venv paths must match configs/env/_colab.yaml (python.score, python.mtdata).
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
RUNTIME_PY="${RUNTIME_PY:-python}"             # override only to test this script elsewhere
SCORE_VENV="${SCORE_VENV:-/content/score-venv}"
MTDATA_VENV="${MTDATA_VENV:-/content/mtdata-venv}"
cd "$REPO"

step() { echo; echo "[setup] $*"; }

step "uv"
"$RUNTIME_PY" -m pip show -q uv >/dev/null 2>&1 || "$RUNTIME_PY" -m pip install -q uv
UV="$("$RUNTIME_PY" -c 'import shutil, sys, os; print(shutil.which("uv") or os.path.join(os.path.dirname(sys.executable), "uv"))')"
# Colab's runtime is a system Python (uv needs --system for it); a test run may point
# RUNTIME_PY at a conda env instead.
if [ "$RUNTIME_PY" = "python" ]; then RT=(--system); else RT=(--python "$RUNTIME_PY"); fi

step "1. runtime packages ($("$RUNTIME_PY" -V))"
if "$RUNTIME_PY" - <<'EOF' 2>/dev/null
import fasttext, fla, peft, sacrebleu, transformers, yaml, pynvml, pytest
assert transformers.__version__.startswith("5")
EOF
then
  echo "already installed"
else
  "$UV" pip install "${RT[@]}" -q "transformers>=5" "peft>=0.17" fasttext-numpy2 sacrebleu pyyaml \
    nvidia-ml-py huggingface_hub pytest "flash-linear-attention==0.6.0"
fi
if "$RUNTIME_PY" -m pip show -q torchao >/dev/null 2>&1; then
  echo "removing torchao $("$RUNTIME_PY" -m pip show torchao | awk '/^Version/ {print $2}') (peft needs none or >= 0.16)"
  "$RUNTIME_PY" -m pip uninstall -y -q torchao
fi

step "2. scorer venv ($SCORE_VENV)"
if [ -x "$SCORE_VENV/bin/python" ] && "$SCORE_VENV/bin/python" -c "import comet, transformers, torch" 2>/dev/null; then
  echo "already installed"
else
  "$UV" venv -q --allow-existing -p 3.12 "$SCORE_VENV"
  "$UV" pip install --python "$SCORE_VENV/bin/python" -q -r setup/requirements-score.txt
fi

step "3. mtdata venv ($MTDATA_VENV)"
if [ -x "$MTDATA_VENV/bin/mtdata" ]; then
  echo "already installed"
else
  "$UV" venv -q --allow-existing -p 3.12 "$MTDATA_VENV"
  "$UV" pip install --python "$MTDATA_VENV/bin/python" -q "mtdata[hf]==0.5.1"
fi

step "4. mtrl (editable) into the runtime and the scorer venv"
"$UV" pip install "${RT[@]}" -q --no-deps -e "$REPO"
"$UV" pip install --python "$SCORE_VENV/bin/python" -q --no-deps -e "$REPO"

step "5. fastText language ID"
mkdir -p data/models
[ -f data/models/lid.176.bin ] || wget -q -O data/models/lid.176.bin \
  https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
ls -la data/models/lid.176.bin | awk '{print $5, $9}'

step "6. env config for this GPU"
ENV_NAME="$("$RUNTIME_PY" scripts/pick_env.py "${PROVIDER:-colab}")"
# replace only the MTRL_ENV line: .env may also hold HF_TOKEN
touch .env
grep -v '^MTRL_ENV=' .env > .env.tmp || true
echo "MTRL_ENV=$ENV_NAME" >> .env.tmp && mv .env.tmp .env
echo "$ENV_NAME -> .env"

step "versions"
"$RUNTIME_PY" -c "import sys, torch, transformers, peft, fla; print('runtime: python', sys.version.split()[0], '| torch', torch.__version__, '| transformers', transformers.__version__, '| peft', peft.__version__, '| fla', fla.__version__, '| cuda', torch.cuda.is_available())"
"$SCORE_VENV/bin/python" -c "import sys, torch, transformers, numpy; print('scorer : python', sys.version.split()[0], '| torch', torch.__version__, '| transformers', transformers.__version__, '| numpy', numpy.__version__)"
"$MTDATA_VENV/bin/mtdata" --version | head -1
echo "[setup] done"

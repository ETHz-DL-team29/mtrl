#!/usr/bin/env bash
# Install mtrl on the RTX 4070 Super Linux box (models and data are downloaded later by scripts/run.py).
# Uses a conda env (miniforge) instead of a venv inside the repo.
# Usage: bash setup/install_local_4070S_12G.sh [env_name]   (run from the repo root)
set -euo pipefail

ENV_NAME="${1:-mtrl}"
PY_VERSION="3.11"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

eval "$(conda shell.bash hook)"
if conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  echo "[install] reusing conda env '$ENV_NAME'"
else
  conda create -y -n "$ENV_NAME" "python=$PY_VERSION"
fi
conda activate "$ENV_NAME"
python --version

# 1) vLLM first: it decides the torch / CUDA versions.
pip install vllm
# 2) everything else, without letting pip touch torch.
python -c "import torch; print('torch', torch.__version__, 'cuda', torch.version.cuda)"
pip install -r "$REPO_ROOT/setup/requirements.txt"
pip install -e "$REPO_ROOT"
python -c "import torch, vllm; print('after deps: torch', torch.__version__, 'vllm', vllm.__version__)"

# 3) record exact versions
pip freeze --exclude-editable > "$REPO_ROOT/setup/requirements.lock.txt"
echo "[install] done. Versions in setup/requirements.lock.txt (commit it)."
echo "[install] next: cp .env.example .env, fill in HF_TOKEN, then: python scripts/run.py configs/quick.yaml"

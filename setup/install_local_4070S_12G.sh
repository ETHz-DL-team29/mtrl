#!/usr/bin/env bash
# Install mtrl on the RTX 4070 Super Linux box. Creates (or reuses) two conda envs:
#   mtrl        generation (vLLM; transformers 5.x, needed by Qwen3.5)
#   mtrl-score  everything else: download, prepare, score, analyze, tests
#               (COMET needs transformers<5, numpy<2, so it cannot share the vLLM env)
# scripts/run.py starts each stage with the right interpreter (env config key `python`).
# Models and data are downloaded later by scripts/run.py, not here.
# Usage (from the repo root): bash setup/install_local_4070S_12G.sh
set -euo pipefail

GEN_ENV="mtrl"
SCORE_ENV="mtrl-score"
GEN_PY="3.12"
SCORE_PY="3.11"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

eval "$(conda shell.bash hook)"

make_env() {   # make_env <name> <python version>
  if conda env list | awk '{print $1}' | grep -qx "$1"; then
    echo "[install] reusing conda env '$1'"
  else
    conda create -y -n "$1" "python=$2"
  fi
}

# 1) generation env: vLLM first, so that it decides torch / CUDA / transformers
make_env "$GEN_ENV" "$GEN_PY"
conda activate "$GEN_ENV"
pip install vllm
pip install -r "$REPO_ROOT/setup/requirements-generate.txt"
pip install -e "$REPO_ROOT"
python -c "import torch, vllm, transformers; print('[install] gen env: torch', torch.__version__, 'vllm', vllm.__version__, 'transformers', transformers.__version__)"
pip freeze --exclude-editable > "$REPO_ROOT/setup/requirements-generate.lock.txt"
conda deactivate

# 2) scoring env: COMET pulls a compatible torch / transformers 4.x / numpy 1.x
make_env "$SCORE_ENV" "$SCORE_PY"
conda activate "$SCORE_ENV"
pip install -r "$REPO_ROOT/setup/requirements-score.txt"
pip install -e "$REPO_ROOT"
python -c "import torch, transformers, comet; print('[install] score env: torch', torch.__version__, 'cuda', torch.cuda.is_available(), 'transformers', transformers.__version__)"
pip freeze --exclude-editable > "$REPO_ROOT/setup/requirements-score.lock.txt"
conda deactivate

echo "[install] done. Commit setup/requirements-*.lock.txt."
echo "[install] check that configs/env/local_4070S_12G.yaml 'python:' points at:"
echo "          $(conda env list | awk -v n="$GEN_ENV" '$1==n {print $NF}')/bin/python"
echo "          $(conda env list | awk -v n="$SCORE_ENV" '$1==n {print $NF}')/bin/python"
echo "[install] next: cp .env.example .env, fill in HF_TOKEN, then:"
echo "          conda activate $SCORE_ENV && python scripts/run.py configs/quick.yaml"

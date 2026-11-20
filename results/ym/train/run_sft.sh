#!/usr/bin/env bash
set -euo pipefail
CFG=${1:?usage: run_sft.sh configs/sft_full.json}
HERE=$(cd "$(dirname "$0")" && pwd)
export PYTHONPATH="$HERE/code:${PYTHONPATH:-}"
ARGS=$(python3 - "$CFG" <<'PY'
import json,sys,shlex
c=json.load(open(sys.argv[1]))
args=[]
for k,v in c.items():
    args += ["--"+k.replace("_","-"),str(v)]
print(" ".join(shlex.quote(a) for a in args))
PY
)
exec python -u "$HERE/code/sft.py" $ARGS

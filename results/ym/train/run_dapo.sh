#!/usr/bin/env bash
set -euo pipefail
CFG=${1:?usage: run_dapo.sh configs/long_attn.json}
HERE=$(cd "$(dirname "$0")" && pwd)
export PYTHONPATH="$HERE/code:${PYTHONPATH:-}"
ARGS=$(python3 - "$CFG" <<'PY'
import json,sys,shlex
c=json.load(open(sys.argv[1]))
m={"max_new":"--max-new","rep_penalty":"--rep-penalty","reward_mode":"--reward-mode","ckpt_every":"--ckpt-every","mask_mode":"--mask-mode","mask_q":"--mask-q","semi_lambda":"--semi-lambda","ent_coef":"--ent-coef","init_ckpt":"--init-ckpt"}
args=[]
for k,v in c.items():
    flag="--"+k.replace("_","-")
    flag=m.get(k,flag)
    args += [flag,str(v)]
print(" ".join(shlex.quote(a) for a in args))
PY
)
exec python -u "$HERE/code/run_dapo.py" $ARGS

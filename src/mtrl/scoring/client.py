"""Client for mtrl.scoring.server, plus a helper that starts the server when needed."""
from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from mtrl.common.config import REPO_ROOT
from mtrl.scoring.server import DEFAULT_PORT


class ScorerClient:
    def __init__(self, port: int = DEFAULT_PORT, timeout: float = 600):
        self.url = f"http://127.0.0.1:{port}"
        self.timeout = timeout

    def healthy(self) -> bool:
        try:
            with urllib.request.urlopen(self.url + "/health", timeout=5) as r:
                return json.loads(r.read()).get("ok", False)
        except (urllib.error.URLError, OSError, ValueError):
            return False

    def metricx(self, srcs, hyps, refs=None) -> list[float]:
        body = {"srcs": list(srcs), "hyps": list(hyps)}
        if refs is not None:
            body["refs"] = list(refs)
        req = urllib.request.Request(self.url + "/score", data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return json.loads(r.read())["scores"]
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"scorer error: {e.read().decode(errors='replace')}") from e


def ensure_server(env_cfg, port: int = DEFAULT_PORT, log_path: Path | None = None,
                  wait_s: float = 600):
    """Return (client, process). Starts scripts/scorer_server.py with the env's scoring
    interpreter if nothing answers on `port`; process is None when a server was already up."""
    client = ScorerClient(port)
    if client.healthy():
        return client, None
    python = env_cfg.python_for("score", default=sys.executable)
    cmd = [python, str(REPO_ROOT / "scripts" / "scorer_server.py"), "--env", env_cfg.name, "--port", str(port)]
    log = open(log_path, "a") if log_path else subprocess.DEVNULL
    print(f"[scorer] starting: {' '.join(cmd)}", flush=True)
    proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
    t0 = time.time()
    while time.time() - t0 < wait_s:
        if proc.poll() is not None:
            raise RuntimeError(f"scorer server exited with code {proc.returncode} (see {log_path})")
        if client.healthy():
            print(f"[scorer] up after {time.time() - t0:.0f}s", flush=True)
            return client, proc
        time.sleep(2)
    proc.kill()
    raise TimeoutError(f"scorer server did not come up within {wait_s}s")

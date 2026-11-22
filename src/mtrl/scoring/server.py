"""MetricX-24 scoring service for training (runs in the scoring env).

Training runs in the `mtrl` env (transformers 5.x); MetricX needs the `mtrl-score` env
(transformers 4.x). The two talk over HTTP on localhost, so both share one GPU without
sharing an interpreter. The service reuses mtrl.scoring.metrics, i.e. exactly the
MetricX implementation that scripts/verify_metricx.py checked against the official one.

    GET  /health                      -> {"ok": true, "model": ..., "dtype": ...}
    POST /score {srcs, hyps, refs?}   -> {"scores": [...]}   refs given -> reference-based,
                                                              else QE (both 0 best .. 25 worst)
Start it with scripts/scorer_server.py; mtrl.scoring.client.ensure_server does that
automatically when a training run finds no server.
"""
from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DEFAULT_PORT = 8765


def score_with_backoff(M, srcs, hyps, refs, batch_size, env_cfg):
    """MetricX with the batch size halved on CUDA OOM. The GPU is shared with a training
    process whose memory use varies, so a batch that fit a moment ago may not fit now."""
    import torch

    fn = M.metricx24_ref if refs is not None else M.metricx24_qe
    bs = batch_size
    while True:
        try:
            return fn(srcs, hyps, refs, batch_size=bs, env_cfg=env_cfg)
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            if bs == 1:
                raise
            bs = max(1, bs // 2)
            print(f"[scorer] CUDA OOM, retrying with batch_size {bs}", flush=True)


def serve(env_cfg, port: int = DEFAULT_PORT, batch_size: int | None = None) -> None:
    from mtrl.scoring import metrics as M

    bs = batch_size or env_cfg.scoring["batch_size"]
    lock = threading.Lock()
    M.metricx24_qe(["warm up"], ["warm up"], None, batch_size=1, env_cfg=env_cfg)   # load once

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, obj):
            body = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            repo = M.METRICX_MODEL["bf16"] if env_cfg.dtype == "bf16" else M.METRICX_MODEL["default"]
            self._send(200, {"ok": True, "model": repo, "dtype": env_cfg.dtype})

        def do_POST(self):
            try:
                req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
                srcs, hyps, refs = req["srcs"], req["hyps"], req.get("refs")
                if len(srcs) != len(hyps) or (refs is not None and len(refs) != len(srcs)):
                    raise ValueError("srcs / hyps / refs lengths differ")
                with lock:
                    scores = score_with_backoff(M, srcs, hyps, refs, bs, env_cfg) if srcs else []
                self._send(200, {"scores": scores})
            except Exception as e:   # report instead of dropping the connection
                self._send(500, {"error": f"{type(e).__name__}: {e}"})

    print(f"[scorer] ready on 127.0.0.1:{port} (batch_size {bs})", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()

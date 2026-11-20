"""Tiny HTTP server around MetricX-24 QE (runs in the transformers-4.x venv)."""
import argparse, json, os, sys, threading, torch
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "metricx-repo"))
from metricx24 import models
import transformers

ap = argparse.ArgumentParser()
ap.add_argument("--port", type=int, default=8765)
ap.add_argument("--model", default="google/metricx-24-hybrid-large-v2p6")
ap.add_argument("--tokenizer", default="google/mt5-xl")
ap.add_argument("--max-length", type=int, default=512)
ap.add_argument("--dtype", default="float16", choices=["float32","float16"])
args = ap.parse_args()

tok = transformers.AutoTokenizer.from_pretrained(args.tokenizer)
dt = torch.float32 if args.dtype == "float32" else torch.float16
model = models.MT5ForRegression.from_pretrained(args.model, torch_dtype=dt).cuda().eval()
lock = threading.Lock()

def score(items, bs=8, refs=None):
    out = []
    with lock, torch.inference_mode():
        for i in range(0, len(items), bs):
            chunk = items[i:i+bs]
            rc = refs[i:i+bs] if refs else [None]*len(chunk)
            texts = []
            for (s, h), rf in zip(chunk, rc):
                t = "source: " + s + " candidate: " + h
                if rf: t += " reference: " + rf
                texts.append(t)
            enc = tok(texts, return_tensors="pt", padding=True, truncation=True,
                      max_length=args.max_length).to("cuda")
            preds = model(input_ids=enc.input_ids, attention_mask=enc.attention_mask).predictions
            out += [float(x) for x in preds]
    return out

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        self._send(200, {"ok": True, "model": args.model})
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        req = json.loads(self.rfile.read(n))
        self._send(200, {"scores": score(req["items"], req.get("batch_size", 8), req.get("refs"))})

print("metricx server ready on", args.port, flush=True)
ThreadingHTTPServer(("127.0.0.1", args.port), H).serve_forever()

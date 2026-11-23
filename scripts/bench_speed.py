"""Raw speed of Qwen3.5-2B on this machine, to compare platforms:

    python scripts/bench_speed.py          # needs only torch + transformers, ~1-2 min

Training: forward + backward through activations (weights frozen, like LoRA, gradient
checkpointing on) at batch 1 / 4 / 8 x 128 tokens. Generation: greedy decoding of 8
sequences, time per decoding step.

2026-11-23 results (docs/training.md, "Platforms"):
  local 4070 SUPER + Ryzen 7 9700X: 86 / 122 / 281 ms, 15 ms per decoding step
  Colab L4 + Xeon 2.20 GHz:        254 / 264 / 450 ms, 49 ms per decoding step
At batch 1 and in decoding the time is mostly CPU-side launch overhead, so the slow
Colab CPU costs ~3x; at batch 8 the gap shrinks to the GPU gap (~1.6x).
"""
import time, torch, platform, subprocess
from transformers import AutoModelForCausalLM
cpu = subprocess.run("lscpu | grep 'Model name'", shell=True, capture_output=True, text=True).stdout.split(":")[-1].strip()
print("cpu:", cpu, "| gpu:", torch.cuda.get_device_name(0))
m = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3.5-2B", dtype=torch.bfloat16).cuda()
for p_ in m.parameters(): p_.requires_grad_(False)   # like LoRA: backward through activations, no full weight grads
m.enable_input_require_grads()
m.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False}); m.train()
def fb(bs, L=128, n=3):
    ids = torch.randint(100, 20000, (bs, L), device="cuda")
    for i in range(n + 1):
        if i == 1: torch.cuda.synchronize(); t = time.time()
        m(input_ids=ids, labels=ids).loss.backward(); m.zero_grad(set_to_none=True)
    torch.cuda.synchronize(); return (time.time() - t) / n
for bs in (1, 4, 8):
    s = fb(bs); print(f"train fwd+bwd  batch {bs:2d} x 128 tok: {s*1000:7.0f} ms  ({s/bs*1000:6.1f} ms/sample)")
m.eval()
with torch.no_grad():
    ids = torch.randint(100, 20000, (8, 64), device="cuda")
    m.generate(ids, max_new_tokens=8, do_sample=False)
    torch.cuda.synchronize(); t = time.time()
    m.generate(ids, max_new_tokens=64, min_new_tokens=64, do_sample=False)
    torch.cuda.synchronize(); s = time.time() - t
print(f"generate 8 seq x 64 new tokens: {s:.2f} s  ({s/64*1000:.0f} ms per decoding step)")

"""LoRA SFT on (source, reference) pairs: cross-entropy on the reference tokens only.

The prompt is built exactly as in generation (chat template, thinking switch); the
target is the reference followed by the end-of-turn token. One step = one optimizer
update over batch_size x grad_accum examples, taken in a seeded shuffled order
(an epoch is one pass over all training segments).
"""
from __future__ import annotations

import json
import random
import time

from mtrl.common.flops_accounting import train_flops
from mtrl.train.common import checkpoint, start, validate


def encode_example(tok, seg, lang, template, thinking, max_len):
    from mtrl.generation.hf_generate import chat_prompts

    prompt = chat_prompts(tok, [seg], [lang], template, thinking)[0]
    p_ids = tok(prompt, add_special_tokens=False).input_ids
    eot = tok.convert_tokens_to_ids("<|im_end|>")
    t_ids = tok(seg.ref, add_special_tokens=False).input_ids + [eot if eot is not None else tok.eos_token_id]
    ids = (p_ids + t_ids)[:max_len]
    labels = ([-100] * len(p_ids) + t_ids)[:max_len]
    return ids, labels


def collate(examples, pad_id):
    import torch

    L = max(len(i) for i, _ in examples)
    ids = torch.full((len(examples), L), pad_id, dtype=torch.long)
    att = torch.zeros((len(examples), L), dtype=torch.long)
    lab = torch.full((len(examples), L), -100, dtype=torch.long)
    for j, (i, lb) in enumerate(examples):
        ids[j, :len(i)] = torch.tensor(i)
        att[j, :len(i)] = 1
        lab[j, :len(lb)] = torch.tensor(lb)
    return ids.cuda(), att.cuda(), lab.cuda()


def example_order(n: int, seed: int, epoch: int) -> list[int]:
    order = list(range(n))
    random.Random(seed * 7919 + epoch).shuffle(order)
    return order


def train(run) -> None:
    import torch

    s = start(run, need_scorer=False)
    t = s.cfg
    sc, sched = t.sft, t.schedule
    segs = [x for x in s.train_segs if x.ref]
    per_step = sc["batch_size"] * sc["grad_accum"]
    n_params = t.model["n_params"]
    step = s.start_step - 1
    try:
        for step in range(s.start_step, sched["steps"]):
            if s.out_of_time():
                print(f"[sft] max_hours reached at step {step}", flush=True)
                step -= 1
                break
            t0 = time.time()
            s.optimizer.zero_grad(set_to_none=True)
            loss_sum, n_tok, skipped = 0.0, 0, 0
            for micro in range(sc["grad_accum"]):
                examples = []
                for k in range(sc["batch_size"]):
                    g = step * per_step + micro * sc["batch_size"] + k      # global example index
                    order = example_order(len(segs), t.seed, g // len(segs))
                    seg = segs[order[g % len(segs)]]
                    examples.append(encode_example(s.tok, seg, s.lang_of(seg), t.prompt_template, t.thinking, sc["max_len"]))
                ids, att, lab = collate(examples, s.tok.pad_token_id)
                out = s.model(input_ids=ids, attention_mask=att, labels=lab, use_cache=False)
                if not torch.isfinite(out.loss):
                    skipped += 1
                    continue
                (out.loss / sc["grad_accum"]).backward()
                loss_sum += float(out.loss)
                n_tok += int((lab != -100).sum())
            gn = float(torch.nn.utils.clip_grad_norm_(s.params, t.optim["grad_clip"]))
            s.optimizer.step()
            done = sc["grad_accum"] - skipped
            rec = {"step": step, "loss": loss_sum / max(1, done), "grad_norm": gn, "n_target_tokens": n_tok,
                   "epoch": round((step + 1) * per_step / len(segs), 3), "skipped_nonfinite": skipped,
                   "B_back_flops": train_flops(n_tok, n_params), "sec": round(time.time() - t0, 2),
                   "vram_gb": round(torch.cuda.max_memory_allocated() / 2**30, 2)}
            s.log("train_log.jsonl", rec)
            if step % sched.get("log_every", 1) == 0:
                print("[sft]", json.dumps(rec), flush=True)
            if (step + 1) % sched["ckpt_every"] == 0:
                checkpoint(s, step)
            if sched.get("val_every") and (step + 1) % sched["val_every"] == 0:
                validate(s, step)
        if step >= s.start_step and (step + 1) % sched["ckpt_every"] != 0:   # not saved in the loop
            checkpoint(s, step)
        print(f"[sft] done: {t.run_name} at step {step} ({(time.time() - s.t0) / 3600:.2f} h)", flush=True)
    finally:
        s.close()

"""Shared bits: model, chat prompts, rollout, MetricX client, metrics."""
import json, os, re, statistics, time, urllib.request
import torch
import sacrebleu
from transformers import AutoTokenizer, AutoModelForImageTextToText

METRICX_URL = os.environ.get("METRICX_URL", "http://127.0.0.1:8765")
TGT_SCRIPT = {"isl_Latn":"Latn","sme_Latn":"Latn","lij_Latn":"Latn","lld_Latn":"Latn",
              "kaz_Cyrl":"Cyrl","hye_Armn":"Armn"}
SCRIPT_RANGES = {"Latn":[(0x41,0x7A),(0xC0,0x24F),(0x1E00,0x1EFF)],
                 "Cyrl":[(0x400,0x4FF)],"Armn":[(0x530,0x58F)]}

def load_model(model_id="Qwen/Qwen3.5-0.8B", dtype=torch.float16):
    tok = AutoTokenizer.from_pretrained(model_id)
    tok.padding_side = "left"
    model = AutoModelForImageTextToText.from_pretrained(
        model_id, dtype=dtype, device_map={"": 0})
    model.eval()
    return tok, model

def chat_texts(tok, records):
    return [tok.apply_chat_template(
        [{"role":"user","content": r["prompt"] + "\n\n" + r["source"]}],
        tokenize=False, add_generation_prompt=True, enable_thinking=False)
        for r in records]

def rollout(model, tok, records, group=8, max_new=192, temperature=1.0, rep_penalty=1.05):
    """Sample G completions for each record. Returns dict with ids/logp/hyps."""
    enc = tok(chat_texts(tok, records), return_tensors="pt", padding=True).to("cuda")
    plen = enc.input_ids.shape[1]
    with torch.inference_mode():
        out = model.generate(**enc, max_new_tokens=max_new, do_sample=True,
                             temperature=temperature, top_p=1.0, top_k=0,
                             repetition_penalty=rep_penalty,
                             num_return_sequences=group, output_scores=True,
                             return_dict_in_generate=True,
                             pad_token_id=tok.pad_token_id or tok.eos_token_id)
    seqs = out.sequences.clone()
    T = len(out.scores)
    toks = seqs[:, plen:plen + T]
    hyps = tok.batch_decode(toks, skip_special_tokens=True)
    return {"enc": enc, "seqs": seqs, "tokens": toks, "old_logp": None,
            "plen": plen, "T": T, "hyps": hyps,
            "prompt_ids": enc.input_ids.repeat_interleave(group, 0)}

def score_items(items, batch_size=8, refs=None):
    body = {"items": items, "batch_size": batch_size}
    if refs: body["refs"] = refs
    req = urllib.request.Request(METRICX_URL + "/score",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())["scores"]

def _in(ranges, cp):
    return any(a <= cp <= b for a, b in ranges)

def gate(src, hyp, tgt):
    h = (hyp or "").strip()
    if not h: return False, "empty"
    sl = len(re.findall(r"\w+", src)); hl = len(re.findall(r"\w+", h))
    if sl and (hl / sl < 0.4 or hl / sl > 2.5):
        return False, "length"
    letters = [c for c in h if c.isalpha()]
    if letters:
        frac = sum(_in(SCRIPT_RANGES[TGT_SCRIPT[tgt]], ord(c)) for c in letters) / len(letters)
        if frac < 0.5: return False, "script"
    return True, "ok"

def reward_and_gate(src, hyp, tgt, mx, lid=False):
    ok, why = gate(src, hyp, tgt)
    if ok and lid:
        from lang_gate import lang_ok
        lok, lwhy = lang_ok(hyp, tgt)
        if not lok:
            ok, why = False, lwhy
    return ((1 - mx / 25.0) if ok else 0.0), ok, why

def chrf(hyps, refs):
    if not all(refs): return None
    return sacrebleu.corpus_chrf(hyps, [refs], word_order=2).score

def append_jsonl(path, obj):
    with open(path, "a") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def generate_greedy(model, tok, records, max_new=192, batch_size=8):
    hyps = []
    with torch.inference_mode():
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            enc = tok(chat_texts(tok, batch), return_tensors="pt", padding=True).to("cuda")
            out = model.generate(**enc, max_new_tokens=max_new, do_sample=False,
                                 num_return_sequences=1,
                                 pad_token_id=tok.pad_token_id or tok.eos_token_id)
            hyps += tok.batch_decode(out[:, enc.input_ids.shape[1]:], skip_special_tokens=True)
    return [h.strip() for h in hyps]

def load_lora(model_id, adapter=None, dtype=torch.float16):
    from peft import PeftModel
    tok, model = load_model(model_id, dtype)
    if adapter:
        model = PeftModel.from_pretrained(model, adapter)
    return tok, model

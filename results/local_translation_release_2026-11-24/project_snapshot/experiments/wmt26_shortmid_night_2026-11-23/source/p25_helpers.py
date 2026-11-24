from pathlib import Path
import os, time, json, math, random, gc, signal, shutil
import numpy as np
import torch
from transformers import GenerationConfig
from sampling_capture import captured_generate
from mtgrpo.common import ROOT, read_jsonl, write_json, append_jsonl, sha256, extract_translation
from mtgrpo.models import Policy, environment_info, output_gate
from mtgrpo.dapo_core import group_advantages, soft_length_penalty, clipped_terms, log_probabilities, generate_group
from mtgrpo.telemetry import ResourceSampler
OUT = ROOT / 'run'
START = time.perf_counter()
STOP = False
SEED = 2026112322

def stop_signal(*args):
    global STOP
    STOP = True

def emit(event, **v):
    z = dict(event=event, unix=time.time(), elapsed_seconds=time.perf_counter() - START, **v)
    append_jsonl(OUT / 'events.jsonl', z)
    write_json(OUT / 'progress.json', z)
    print('P25_' + event.upper() + ':' + json.dumps(v), flush=True)

def rng():
    return dict(torch=torch.get_rng_state(), cuda=torch.cuda.get_rng_state_all(), python=random.getstate(), numpy=np.random.get_state())

def restore(v):
    torch.set_rng_state(v['torch'])
    torch.cuda.set_rng_state_all(v['cuda'])
    random.setstate(v['python'])
    np.random.set_state(v['numpy'])

def parity(details):
    a = np.asarray(details)
    a = np.abs(a)
    return dict(tokens=len(a), mean_abs_delta=float(a.mean()), p99_abs_delta=float(np.quantile(a, 0.99)), max_abs_delta=float(a.max()))

def parity_gate(p):
    assert p['mean_abs_delta'] <= 0.0005 and p['p99_abs_delta'] <= 0.002 and (p['max_abs_delta'] <= 0.01), 'Actual sampler/teacher parity failed'

def sampled(policy, prompt, maximum=512, g=8):
    policy.model.eval()
    st = time.perf_counter()
    seq, lps = captured_generate(policy.model, prompt, g=g, eos=eos_ids(policy), pad=policy.tokenizer.pad_token_id, temperature=0.7, maximum=maximum)
    torch.cuda.synchronize()
    elapsed = time.perf_counter() - st
    outputs = []
    eos = eos_ids(policy)
    for j, s in enumerate(seq):
        ids = s[prompt.shape[1]:].tolist()
        hits = [i for i, t in enumerate(ids) if t in eos]
        if hits:
            ids = ids[:hits[0] + 1]
        raw = policy.tokenizer.decode(ids, skip_special_tokens=True)
        outputs.append(dict(completion_ids=ids, sampler_logps=lps[j, :len(ids)].tolist(), raw_output=raw, hypothesis=extract_translation(raw), completion_tokens=len(ids), truncated=len(ids) >= maximum and (not ids or ids[-1] not in eos), generation_group_seconds=elapsed))
    return outputs

def preflight(policy, train):
    selected = [next((r for r in train if r['stratum'] == s)) for s in ['general', 'technical_short', 'technical_medium']]
    p = policy.prompt_ids(selected[0], max_prompt_tokens=1024)
    settings = dict(max_new_tokens=16, do_sample=True, num_return_sequences=8, num_beams=1, temperature=0.7, top_p=1.0, top_k=0, repetition_penalty=1.0, eos_token_id=eos_ids(policy), pad_token_id=policy.tokenizer.pad_token_id, use_cache=True, return_dict_in_generate=True, output_scores=True)
    torch.manual_seed(SEED + 1)
    with torch.no_grad():
        native = policy.model.generate(input_ids=p, attention_mask=torch.ones_like(p), generation_config=GenerationConfig(**settings))
    torch.manual_seed(SEED + 1)
    actual = sampled(policy, p, 16)
    delta = 0.0
    for j, o in enumerate(actual):
        expected = native.sequences[j, p.shape[1]:].tolist()
        eos = eos_ids(policy)
        hits = [i for i, t in enumerate(expected) if t in eos]
        if hits:
            expected = expected[:hits[0] + 1]
        assert expected == o['completion_ids'], 'Recorder altered native samples'
        for t, k in enumerate(expected):
            delta = max(delta, abs(float(native.scores[t][j].float().log_softmax(-1)[k]) - o['sampler_logps'][t]))
    assert delta < 1e-05
    del native, actual
    gc.collect()
    torch.cuda.empty_cache()
    details = []
    train_delta = 0.0
    for row in selected:
        prompt = policy.prompt_ids(row, max_prompt_tokens=1024)
        oo = sampled(policy, prompt, 64)
        for j, o in enumerate(oo):
            ids = torch.tensor(o['completion_ids'], device='cuda')
            with torch.no_grad():
                lp, _ = log_probabilities(policy, prompt, ids)
            if j == 0:
                with torch.enable_grad():
                    tlp, _ = log_probabilities(policy, prompt, ids)
                train_delta = max(train_delta, float((tlp.detach() - lp).abs().max()))
                del tlp
            details.extend((dict(id=row['id'], candidate=j, position=i, sampler=s, teacher=t) for i, (s, t) in enumerate(zip(o['sampler_logps'], lp.tolist()))))
        emit('preflight_source', id=row['id'], stratum=row['stratum'])
    z = dict(parity([r['teacher'] - r['sampler'] for r in details]), native_sequences_identical=True, native_logp_max_delta=delta, train_eval_max_delta=train_delta)
    write_json(OUT / 'preflight/details.json', details)
    write_json(OUT / 'preflight/summary.json', z)
    parity_gate(z)
    assert train_delta <= 0.0005
    policy.model.eval()
    emit('preflight_passed', **z)

def evaluate(policy, rows, label, g8ids):
    st = time.perf_counter()
    path = OUT / f'evaluation/{label}_greedy.jsonl'
    assert not path.exists()
    for i, row in enumerate(rows):
        p = policy.prompt_ids(row, max_prompt_tokens=1024)
        o = generate_group(policy, p, g=1, maximum=512, sample=False)[0]
        append_jsonl(path, dict(row, **o))
        if (i + 1) % 16 == 0:
            emit('evaluation_counts', label=label, completed=i + 1, total=len(rows))
    greedy_seconds = time.perf_counter() - st
    torch.manual_seed(SEED + 400)
    torch.cuda.manual_seed_all(SEED + 400)
    for i, row in enumerate([r for r in rows if r['id'] in g8ids]):
        ss = int.from_bytes(__import__('hashlib').sha256(('p25-final/' + row['id']).encode()).digest()[:4], 'big')
        torch.manual_seed(ss)
        torch.cuda.manual_seed_all(ss)
        p = policy.prompt_ids(row, max_prompt_tokens=1024)
        oo = sampled(policy, p)
        append_jsonl(OUT / f'evaluation/{label}_g8.jsonl', dict(row, outputs=oo, seed=ss))
        emit('g8_counts', label=label, completed=i + 1, total=len(g8ids))
    z = dict(label=label, greedy_count=len(rows), g8_sources=len(g8ids), greedy_seconds=greedy_seconds, total_seconds=time.perf_counter() - st, quality_metrics_intentionally_not_computed=True)
    write_json(OUT / f'evaluation/{label}_timing.json', z)
    emit('evaluation_finished', **z)
    return z

def eos_ids(policy):
    value = policy.model.generation_config.eos_token_id or policy.tokenizer.eos_token_id
    result = [value] if isinstance(value, int) else list(value)
    if policy.tokenizer.eos_token_id not in result:
        result.append(policy.tokenizer.eos_token_id)
    return result

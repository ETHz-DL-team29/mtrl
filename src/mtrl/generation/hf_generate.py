"""Generation with Hugging Face transformers: training rollouts and adapter evaluation.

vLLM (mtrl.generation.vllm_generate) is faster but cannot run on the 1080 Ti cluster and
does not see a LoRA adapter while it is being trained; this backend works everywhere and
returns the token ids the policy-gradient loss needs.
"""
from __future__ import annotations

from dataclasses import dataclass

from mtrl.common.records import Rollout, Segment
from mtrl.generation.prompting import build_messages, parse_output


@dataclass
class Batch:
    """Token-level view of N = len(rollouts) completions (row i <-> rollouts[i])."""
    input_ids: object        # [N, P + T] prompt (left-padded) + completion
    attention_mask: object   # [N, P + T]
    tokens: object           # [N, T] completion ids (padding after EOS)
    valid: object            # [N, T] bool: completion tokens up to and including the first EOS
    prompt_len: int          # P
    rollouts: list           # [Rollout]


def chat_prompts(tok, segs: list[Segment], lang_cfgs: list[dict], template: str, thinking: bool):
    return [tok.apply_chat_template(build_messages(s, lang, template), tokenize=False,
                                    add_generation_prompt=True, enable_thinking=thinking)
            for s, lang in zip(segs, lang_cfgs)]


def eos_ids(tok, model) -> list[int]:
    ids = model.generation_config.eos_token_id
    ids = list(ids) if isinstance(ids, (list, tuple)) else [ids]
    return sorted({i for i in ids + [tok.eos_token_id] if i is not None})


def completion_mask(tokens, eos: list[int]):
    """([N, T] bool True up to and including the first EOS, [N] bool row contains an EOS)."""
    import torch

    is_eos = torch.isin(tokens, torch.tensor(eos, device=tokens.device))
    after = torch.cumsum(is_eos.int(), dim=1) - is_eos.int()   # EOS seen strictly before t
    return after == 0, is_eos.any(dim=1).tolist()


def _rollouts(tok, segs, texts, valid, stopped, *, model_name, thinking, temperature, n_prompt, sample_idx):
    out = []
    for i, (seg, text) in enumerate(zip(segs, texts)):
        reasoning, translation, ok = parse_output(text, thinking)
        n_tr = len(tok.encode(translation, add_special_tokens=False)) if translation else 0
        n_all = int(valid[i].sum())
        out.append(Rollout(seg_id=seg.seg_id, sample_idx=sample_idx(i), model=model_name, thinking=thinking,
                           temperature=temperature, raw_output=text, reasoning=reasoning,
                           translation=translation, n_prompt_tokens=n_prompt[i],
                           n_reasoning_tokens=max(n_all - n_tr, 0) if thinking else 0,
                           n_translation_tokens=n_tr, finish_reason="stop" if stopped[i] else "length",
                           parse_ok=ok))
    return out


def sample_group(model, tok, segs: list[Segment], lang_cfgs: list[dict], *, template: str,
                 thinking: bool, group: int, temperature: float, top_p: float,
                 rep_penalty: float, max_new_tokens: int, model_name: str) -> Batch:
    """G samples for each of the B segments; rows are segment-major (b * G + g)."""
    import torch

    enc = tok(chat_prompts(tok, segs, lang_cfgs, template, thinking), return_tensors="pt",
              padding=True).to(model.device)
    P = enc.input_ids.shape[1]
    with torch.no_grad():   # not inference_mode: the sequences feed the loss forward afterwards
        seqs = model.generate(**enc, do_sample=True, temperature=temperature, top_p=top_p, top_k=0,
                              repetition_penalty=rep_penalty, max_new_tokens=max_new_tokens,
                              num_return_sequences=group, pad_token_id=tok.pad_token_id)
    tokens = seqs[:, P:]
    valid, stopped = completion_mask(tokens, eos_ids(tok, model))
    texts = tok.batch_decode(torch.where(valid, tokens, tok.pad_token_id), skip_special_tokens=True)
    prompt_att = enc.attention_mask.repeat_interleave(group, dim=0)
    rep_segs = [s for s in segs for _ in range(group)]
    n_prompt = prompt_att.sum(1).tolist()
    rolls = _rollouts(tok, rep_segs, texts, valid, stopped, model_name=model_name, thinking=thinking,
                      temperature=temperature, n_prompt=n_prompt, sample_idx=lambda i: i % group)
    return Batch(input_ids=seqs, attention_mask=torch.cat([prompt_att, valid.long()], dim=1),
                 tokens=tokens, valid=valid, prompt_len=P, rollouts=rolls)


def generate_greedy(model, tok, segs: list[Segment], lang_cfgs: list[dict], *, template: str,
                    thinking: bool, max_new_tokens: int, batch_size: int, model_name: str) -> list[Rollout]:
    """Greedy decoding (sample_idx = -1), longest prompts first to surface OOM early."""
    import torch

    order = sorted(range(len(segs)), key=lambda i: len(segs[i].src), reverse=True)
    out: list = [None] * len(segs)
    eos = eos_ids(tok, model)
    for b in range(0, len(order), batch_size):
        idx = order[b:b + batch_size]
        bs = [segs[i] for i in idx]
        enc = tok(chat_prompts(tok, bs, [lang_cfgs[i] for i in idx], template, thinking),
                  return_tensors="pt", padding=True).to(model.device)
        with torch.inference_mode():
            seqs = model.generate(**enc, do_sample=False, max_new_tokens=max_new_tokens,
                                  pad_token_id=tok.pad_token_id)
        tokens = seqs[:, enc.input_ids.shape[1]:]
        valid, stopped = completion_mask(tokens, eos)
        texts = tok.batch_decode(torch.where(valid, tokens, tok.pad_token_id), skip_special_tokens=True)
        rolls = _rollouts(tok, bs, texts, valid, stopped, model_name=model_name, thinking=thinking, temperature=0.0,
                          n_prompt=enc.attention_mask.sum(1).tolist(), sample_idx=lambda i: -1)
        for i, r in zip(idx, rolls):
            out[i] = r
    return out

"""Token masks for selective updates: which completion tokens get gradient, and how much.

Every mask is a function  fn(ctx: MaskContext, **params) -> weights [N, T] float  with
0 on padding. Register new ones with @register("name"); configs select them with
`mask: {name: <name>, <params>}`. The schemes from results/ym are ported one-to-one:

  full       every valid token, weight 1
  randpos    each token independently with probability q
  semi       weight 1 with probability q, else lam (soft version of randpos)
  block      one contiguous span covering a fraction q of each rollout
  vocab      tokens whose id is in a given vocabulary subset (ctx.vocab_mask)
  content    tokens that are alphabetic words of >= 2 letters (ctx.content_mask)
  highent    the top-q fraction of each rollout by policy entropy   (ym: "entpos")
  lowent     the bottom-q fraction by policy entropy
  translation  only tokens after the reasoning part (needs ctx.translation_start; with
             thinking off it equals `full`). Basis of the planned reasoning-token schemes.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

MASKS: dict[str, Callable] = {}
NEEDS_ENTROPY = {"highent", "lowent"}


def register(name: str):
    def deco(fn):
        MASKS[name] = fn
        return fn
    return deco


@dataclass
class MaskContext:
    tokens: object                  # [N, T] long, completion token ids
    valid: object                   # [N, T] bool, False on padding
    generator: object = None        # torch.Generator for reproducible random masks
    entropy: object = None          # [N, T] float, for entropy masks
    vocab_mask: object = None       # [V] bool, for `vocab`
    content_mask: object = None     # [V] bool, for `content`
    translation_start: object = None  # [N] long, first translation token per rollout


def build_mask(name: str, ctx: MaskContext, **params):
    if name not in MASKS:
        raise KeyError(f"unknown mask {name!r}; known: {sorted(MASKS)}")
    w = MASKS[name](ctx, **params).float()
    return w * ctx.valid.float()


def _rand(ctx):
    import torch

    return torch.rand(ctx.valid.shape, generator=ctx.generator, device="cpu").to(ctx.valid.device)


@register("full")
def full(ctx, **_):
    return ctx.valid


@register("randpos")
def randpos(ctx, q: float, **_):
    return _rand(ctx) < q


@register("semi")
def semi(ctx, q: float, lam: float, **_):
    import torch

    sel = _rand(ctx) < q
    return torch.where(sel, torch.ones_like(sel, dtype=torch.float), torch.full_like(sel, lam, dtype=torch.float))


@register("block")
def block(ctx, q: float, **_):
    import torch

    out = torch.zeros_like(ctx.valid)
    for i in range(ctx.valid.shape[0]):
        n = int(ctx.valid[i].sum())
        if n == 0:
            continue
        length = max(1, int(n * q))
        start = int(torch.randint(0, max(1, n - length + 1), (1,), generator=ctx.generator))
        out[i, start:start + length] = True
    return out


@register("vocab")
def vocab(ctx, **_):
    if ctx.vocab_mask is None:
        raise ValueError("mask `vocab` needs ctx.vocab_mask (mask.vocab_file in the config)")
    return ctx.vocab_mask[ctx.tokens]


@register("content")
def content(ctx, **_):
    if ctx.content_mask is None:
        raise ValueError("mask `content` needs ctx.content_mask")
    return ctx.content_mask[ctx.tokens]


def _entropy_quantile(ctx, q: float, top: bool):
    import torch

    if ctx.entropy is None:
        raise ValueError("entropy masks need ctx.entropy")
    out = torch.zeros_like(ctx.valid)
    for i in range(ctx.valid.shape[0]):
        v = ctx.valid[i]
        if not v.any():
            continue
        e = ctx.entropy[i]
        thr = torch.quantile(e[v].float(), 1 - q if top else q)
        out[i] = v & ((e >= thr) if top else (e <= thr))
    return out


@register("highent")
def highent(ctx, q: float, **_):
    return _entropy_quantile(ctx, q, top=True)


@register("lowent")
def lowent(ctx, q: float, **_):
    return _entropy_quantile(ctx, q, top=False)


@register("translation")
def translation(ctx, **_):
    import torch

    if ctx.translation_start is None:
        return ctx.valid
    pos = torch.arange(ctx.valid.shape[1], device=ctx.valid.device)[None, :]
    return pos >= ctx.translation_start[:, None]


def content_vocab_mask(tokenizer):
    """[V] bool: token is an alphabetic word piece of >= 2 letters (ym's `alpha_mask`)."""
    import re

    import torch

    n = len(tokenizer)
    m = torch.zeros(n, dtype=torch.bool)
    for i in range(n):
        piece = tokenizer.convert_ids_to_tokens(i)
        if piece is not None and re.fullmatch(r"[^\W\d_]{2,}", piece.lstrip("Ġ▁")):
            m[i] = True
    return m

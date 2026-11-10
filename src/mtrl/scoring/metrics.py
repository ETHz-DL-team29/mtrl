"""Translation metrics with one shared signature:

    fn(srcs, hyps, refs, *, batch_size, env_cfg) -> list[float]

Each neural metric loads its model once (cached in _MODELS across calls, so score.py
can feed it chunk by chunk for resumability) and `release()` frees GPU memory before
the next metric's model is loaded. Reference-based metrics must only be called on items that have a reference
(score.py filters; missing values are never written as 0).
"""
from __future__ import annotations

import gc
import warnings
from functools import lru_cache

# MetricX-24 (google-research/metricx). TODO: confirm the bf16 repo exists; we fall back
# to the fp32 repo (loaded in env dtype) if it cannot be downloaded.
METRICX_MODEL = {"bf16": "google/metricx-24-hybrid-large-v2p6-bfloat16",
                 "default": "google/metricx-24-hybrid-large-v2p6"}
METRICX_TOKENIZER = "google/mt5-xl"
METRICX_MAX_LEN = 1536
METRICX_SCORE_TOKEN = 250089   # <extra_id_10>: MetricX regresses the logit of this token
COMETKIWI_MODEL = "Unbabel/wmt22-cometkiwi-da"    # gated on HF: request access first
COMET22_MODEL = "Unbabel/wmt22-comet-da"
# Encoders whose tokenizer/config COMET fetches from the Hub when loading a checkpoint
# (names as written in each checkpoint's hparams.yaml; prefetched by scripts/download.py).
COMET_ENCODERS = {COMETKIWI_MODEL: "microsoft/infoxlm-large", COMET22_MODEL: "xlm-roberta-large"}

NEEDS_REF = {"metricx24_ref", "chrf", "comet22"}


_MODELS: dict = {}


def _cached(key, loader):
    if key not in _MODELS:
        _MODELS[key] = loader()
    return _MODELS[key]


def release() -> None:
    """Drop all loaded scorer models and free GPU memory."""
    if not _MODELS:
        return
    import torch

    _MODELS.clear()
    gc.collect()
    torch.cuda.empty_cache()


@lru_cache(maxsize=1)
def _mt5_tokenizer():
    from transformers import AutoTokenizer

    return AutoTokenizer.from_pretrained(METRICX_TOKENIZER)


def _torch_dtype(env_cfg):
    import torch

    return {"bf16": torch.bfloat16, "fp16": torch.float16, "fp32": torch.float32}[env_cfg.dtype]


# ---------------------------------------------------------------- MetricX-24
def metricx_inputs(srcs, hyps, refs) -> list[str]:
    """Input format of metricx24/predict.py: QE mode simply omits the reference."""
    if refs is None:
        return [f"source: {s} candidate: {h}" for s, h in zip(srcs, hyps)]
    return [f"source: {s} candidate: {h} reference: {r}" for s, h, r in zip(srcs, hyps, refs)]


def metricx_tokenize(texts: list[str]) -> list[list[int]]:
    """Tokenize like predict.py: truncate to 1536, then drop the trailing EOS token."""
    ids = _mt5_tokenizer()(texts, max_length=METRICX_MAX_LEN, truncation=True)["input_ids"]
    return [x[:-1] for x in ids]


def _metricx(srcs, hyps, refs, *, batch_size, env_cfg) -> list[float]:
    """MT5ForRegression == MT5ForConditionalGeneration with a single decoder step from
    token 0, reading the logit of <extra_id_10>, clamped to [0, 25]. The checkpoint's
    weights (shared/encoder/decoder/lm_head) load directly into the HF class, so the
    official model class does not need to be vendored."""
    import torch
    from transformers import MT5ForConditionalGeneration

    def load():
        dtype = _torch_dtype(env_cfg)
        repo = METRICX_MODEL["bf16"] if env_cfg.dtype == "bf16" else METRICX_MODEL["default"]
        try:
            m = MT5ForConditionalGeneration.from_pretrained(repo, torch_dtype=dtype)
        except OSError:
            warnings.warn(f"{repo} not available, falling back to {METRICX_MODEL['default']}")
            m = MT5ForConditionalGeneration.from_pretrained(METRICX_MODEL["default"], torch_dtype=dtype)
        return m.to("cuda").eval()

    model = _cached("metricx", load)

    ids = metricx_tokenize(metricx_inputs(srcs, hyps, refs))
    order = sorted(range(len(ids)), key=lambda i: len(ids[i]), reverse=True)  # OOM shows early
    scores = [0.0] * len(ids)
    with torch.inference_mode():
        for b in range(0, len(order), batch_size):
            idx = order[b:b + batch_size]
            L = max(len(ids[i]) for i in idx)
            inp = torch.zeros(len(idx), L, dtype=torch.long)
            att = torch.zeros(len(idx), L, dtype=torch.long)
            for j, i in enumerate(idx):
                inp[j, :len(ids[i])] = torch.tensor(ids[i])
                att[j, :len(ids[i])] = 1
            inp, att = inp.cuda(), att.cuda()
            dec = torch.zeros(len(idx), 1, dtype=torch.long, device="cuda")
            logits = model(input_ids=inp, attention_mask=att, decoder_input_ids=dec).logits
            pred = logits[:, 0, METRICX_SCORE_TOKEN].float().clamp(0, 25).tolist()
            for j, i in enumerate(idx):
                scores[i] = pred[j]
    return scores


def metricx24_qe(srcs, hyps, refs, *, batch_size, env_cfg):
    return _metricx(srcs, hyps, None, batch_size=batch_size, env_cfg=env_cfg)


def metricx24_ref(srcs, hyps, refs, *, batch_size, env_cfg):
    return _metricx(srcs, hyps, refs, batch_size=batch_size, env_cfg=env_cfg)


# ---------------------------------------------------------------- COMET family
class MetricUnavailable(RuntimeError):
    """Raised when a metric's model cannot be loaded (e.g. gated repo without access)."""


def _comet(model_name, data, batch_size) -> list[float]:
    from comet import download_model, load_from_checkpoint

    try:
        model = _cached(model_name, lambda: load_from_checkpoint(download_model(model_name)))
    except Exception as e:
        raise MetricUnavailable(f"cannot load {model_name} ({type(e).__name__}: {e})") from e
    return list(model.predict(data, batch_size=batch_size, gpus=1, progress_bar=False).scores)


def cometkiwi22(srcs, hyps, refs, *, batch_size, env_cfg):
    return _comet(COMETKIWI_MODEL, [{"src": s, "mt": h} for s, h in zip(srcs, hyps)], batch_size)


def comet22(srcs, hyps, refs, *, batch_size, env_cfg):
    data = [{"src": s, "mt": h, "ref": r} for s, h, r in zip(srcs, hyps, refs)]
    return _comet(COMET22_MODEL, data, batch_size)


# ---------------------------------------------------------------- chrF++
def chrf(srcs, hyps, refs, *, batch_size, env_cfg):
    from sacrebleu.metrics import CHRF

    m = CHRF(word_order=2)
    return [m.sentence_score(h, [r]).score for h, r in zip(hyps, refs)]


METRICS = {
    "metricx24_qe": metricx24_qe,
    "metricx24_ref": metricx24_ref,
    "cometkiwi22": cometkiwi22,
    "chrf": chrf,
    "comet22": comet22,
}


def count_scorer_tokens(metric: str, srcs, hyps, refs) -> int:
    """Input tokens seen by a scorer, for FLOPs accounting. Counted with the mT5 tokenizer
    for all neural metrics (COMET's XLM-R/InfoXLM vocab is a similar 250k SentencePiece;
    approximation). chrF has no model -> 0."""
    if metric == "chrf":
        return 0
    if metric.startswith("metricx"):
        return sum(len(x) for x in metricx_tokenize(
            metricx_inputs(srcs, hyps, refs if metric == "metricx24_ref" else None)))
    texts = list(srcs) + list(hyps) + (list(refs) if metric == "comet22" else [])
    return sum(len(x) for x in _mt5_tokenizer()(texts)["input_ids"])

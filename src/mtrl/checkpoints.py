"""Portable local LoRA registry. Neural libraries are imported only on explicit load."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

INSTRUCTION = "Translate the following English text into Icelandic. Return only the Icelandic translation."


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def inside(root: Path, relative: str) -> Path:
    root = root.resolve()
    if Path(relative).is_absolute() or ":" in relative:
        raise ValueError("Artifact paths must be relative to the repository")
    target = (root / relative).resolve()
    if not target.is_relative_to(root):
        raise ValueError("Artifact path escapes the repository")
    return target


def registry(root: Path | None = None) -> dict:
    root = Path(root) if root is not None else repository_root()
    result = json.loads((root / "models/registry.json").read_text(encoding="utf-8"))
    if result.get("schema_version") != 1:
        raise ValueError("Unsupported model registry schema")
    ids = [m["id"] for m in result["models"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate model ID")
    for model in result["models"]:
        if not re.fullmatch(r"[a-z0-9_-]+", model["id"]):
            raise ValueError("Invalid model ID")
        if not re.fullmatch(r"[0-9a-f]{40}", model["base_revision"]):
            raise ValueError("Missing pinned base revision")
        inside(root, model["adapter_path"])
    return result


def model_entry(model_id: str, root: Path | None = None) -> dict:
    for entry in registry(root)["models"]:
        if entry["id"] == model_id:
            return entry
    raise ValueError(f"Unknown model: {model_id}; run scripts/models.py list")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024**2), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_model(model_id: str, root: Path | None = None) -> dict:
    root = Path(root) if root is not None else repository_root()
    entry = model_entry(model_id, root)
    folder = inside(root, entry["adapter_path"])
    for name, expected in entry["files"].items():
        path = inside(folder, name)
        if not path.is_file():
            raise FileNotFoundError(f"Missing {path}. Extract the local model bundle; git clone alone excludes weights.")
        if path.stat().st_size != expected["bytes"] or sha256(path) != expected["sha256"]:
            raise ValueError(f"Artifact hash mismatch: {model_id}/{name}")
    return {"id": model_id, "verified": True, "adapter_path": str(folder)}


def load_translation_model(model_id: str, *, root: Path | None = None,
                           device: str = "cuda", precision: str = "recorded",
                           base_path: str | None = None, offline: bool = False,
                           trainable: bool = False):
    """Return (PEFT model, tokenizer, registry entry); never invoked by list/verify.

    `trainable=True` exposes adapter weights for subsequent training. Exact historical
    DAPO replay additionally requires the archived dropout/optimizer/sampling recipe.
    """
    if precision not in {"recorded", "float32", "bfloat16", "float16"}:
        raise ValueError("Unknown precision")
    root = Path(root) if root is not None else repository_root()
    entry = model_entry(model_id, root)
    verify_model(model_id, root)
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from peft import PeftModel

    if device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError("CUDA is unavailable. Use a GPU runtime, or explicitly choose device='cpu'.")
    if precision == "recorded":
        dtype = torch.bfloat16 if entry["recorded_base_rounding"] == "bfloat16_then_float32" else torch.float32
    else:
        dtype = getattr(torch, precision)
    source = base_path or entry["base_model"]
    options = {"local_files_only": offline}
    if not base_path:
        options["revision"] = entry["base_revision"]
    elif not Path(base_path).is_dir():
        raise FileNotFoundError(base_path)
    tokenizer = AutoTokenizer.from_pretrained(source, **options)
    tokenizer.pad_token = tokenizer.pad_token or tokenizer.eos_token
    tokenizer.padding_side = "left"
    if entry["architecture"] == "qwen3_5":
        from transformers import Qwen3_5ForConditionalGeneration
        constructor = Qwen3_5ForConditionalGeneration
    else:
        constructor = AutoModelForCausalLM
    # Explicit base ID/revision avoids PEFT's historical /content/... base path.
    base = constructor.from_pretrained(source, dtype=dtype, attn_implementation="sdpa", **options)
    model = PeftModel.from_pretrained(base, inside(root, entry["adapter_path"]),
                                      is_trainable=trainable, local_files_only=True)
    if precision in {"recorded", "float32"}:
        model.float()
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
    else:
        model.to(dtype=dtype)
    model.to(device)
    model.train() if trainable else model.eval()
    return model, tokenizer, entry


def translate(model, tokenizer, source: str, *, max_new_tokens: int = 1024,
              max_prompt_tokens: int = 2048, samples: int = 1, temperature: float = .7) -> list[dict]:
    if not source.strip() or samples < 1 or max_new_tokens < 1 or (samples > 1 and temperature <= 0):
        raise ValueError("Nonempty source and positive generation limits are required")
    import torch
    from transformers import GenerationConfig
    messages = [{"role": "user", "content": INSTRUCTION + "\n\n" + source}]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
    inputs = tokenizer(prompt, add_special_tokens=False, return_tensors="pt")
    if inputs.input_ids.shape[1] > max_prompt_tokens:
        raise ValueError("Prompt exceeds limit; segment the source rather than silently truncate it")
    inputs = inputs.to(next(model.parameters()).device)
    eos = model.generation_config.eos_token_id or tokenizer.eos_token_id
    eos_ids = [eos] if isinstance(eos, int) else eos
    settings = dict(do_sample=samples > 1, num_return_sequences=samples, num_beams=1,
                    max_new_tokens=max_new_tokens, repetition_penalty=1., eos_token_id=eos,
                    pad_token_id=tokenizer.pad_token_id, use_cache=True)
    if samples > 1:
        settings.update(temperature=temperature, top_p=1., top_k=0)
    was_training = model.training
    model.eval()
    try:
        with torch.inference_mode():
            output = model.generate(**inputs, generation_config=GenerationConfig(**settings))
    finally:
        model.train(was_training)
    result = []
    for sequence in output:
        ids = sequence[inputs.input_ids.shape[1]:].tolist()
        hits = [i for i, token in enumerate(ids) if token in eos_ids]
        if hits:
            ids = ids[:hits[0] + 1]
        raw = tokenizer.decode(ids, skip_special_tokens=True)
        translation = raw.rsplit("</think>", 1)[-1].strip() if "</think>" in raw else "" if "<think>" in raw else raw.strip()
        result.append(dict(raw_output=raw, translation=translation, completion_tokens=len(ids),
                           truncated=len(ids) >= max_new_tokens and bool(ids) and ids[-1] not in eos_ids))
    return result

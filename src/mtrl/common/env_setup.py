"""Process environment setup and GPU capability checks.

`setup_env` must run BEFORE importing transformers / vllm / comet.
GPU queries use NVML (pynvml) so the main process never creates a CUDA context
(vLLM's engine runs in a subprocess and dislikes a pre-initialised parent).
"""
from __future__ import annotations

import os

from mtrl.common.config import EnvConfig, load_dotenv

_CACHE_VARS = {"hf_home": "HF_HOME", "torch_home": "TORCH_HOME", "pip_cache": "PIP_CACHE_DIR"}


def setup_env(env_cfg: EnvConfig) -> None:
    load_dotenv()
    for key, var in _CACHE_VARS.items():
        if key in env_cfg.paths:
            os.environ[var] = str(env_cfg.path(key))
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")


def check_capabilities(env_cfg: EnvConfig) -> dict:
    """Fail loudly if the GPU does not match the env name or cannot do what the env asks."""
    import pynvml

    pynvml.nvmlInit()
    try:
        n = pynvml.nvmlDeviceGetCount()
        if n < env_cfg.n_gpus:
            raise RuntimeError(f"env {env_cfg.name} wants {env_cfg.n_gpus} GPU(s), found {n}")
        h = pynvml.nvmlDeviceGetHandleByIndex(0)
        name = pynvml.nvmlDeviceGetName(h)
        name = name.decode() if isinstance(name, bytes) else name
        mem_gb = pynvml.nvmlDeviceGetMemoryInfo(h).total / 1e9
        major, minor = pynvml.nvmlDeviceGetCudaComputeCapability(h)
    finally:
        pynvml.nvmlShutdown()
    cap = major + minor / 10

    if env_cfg.gpu["match"].lower() not in name.lower():
        raise RuntimeError(f"env {env_cfg.name} expects a '{env_cfg.gpu['match']}' GPU, got '{name}'")
    expected = float(env_cfg.gpu["mem_gb"])
    if abs(mem_gb - expected) / expected > 0.15:
        raise RuntimeError(f"env {env_cfg.name} expects ~{expected:.0f} GB, GPU has {mem_gb:.1f} GB")
    if env_cfg.dtype == "bf16" and cap < 8.0:
        raise RuntimeError(f"dtype bf16 needs compute capability >= 8.0, '{name}' has {cap}")
    if env_cfg.use_vllm and cap < 7.0:
        raise RuntimeError(f"vLLM needs compute capability >= 7.0, '{name}' has {cap}")
    return {"gpu_name": name, "gpu_mem_gb": round(mem_gb, 2), "compute_capability": cap,
            "n_gpus_visible": n}


def gpu_mem_used_gb() -> float:
    """Device-wide used memory on GPU 0 (all processes, incl. the vLLM engine subprocess)."""
    import pynvml

    pynvml.nvmlInit()
    try:
        used = pynvml.nvmlDeviceGetMemoryInfo(pynvml.nvmlDeviceGetHandleByIndex(0)).used
    finally:
        pynvml.nvmlShutdown()
    return round(used / 1e9, 3)

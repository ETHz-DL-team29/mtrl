"""Shared CLI helpers for scripts/ (argument parsing only)."""
import argparse


def str2bool(s: str) -> bool:
    if s.lower() in ("true", "1", "yes", "on"):
        return True
    if s.lower() in ("false", "0", "no", "off"):
        return False
    raise argparse.ArgumentTypeError(f"expected true/false, got {s!r}")


def base_parser(doc: str) -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=doc)
    ap.add_argument("--config", required=True, help="experiment YAML, e.g. configs/zeroshot.yaml")
    ap.add_argument("--env", help="env name, e.g. local_4070S_12G (default: MTRL_ENV from .env)")
    ap.add_argument("--model", action="append", help="only this model (repeatable)")
    ap.add_argument("--thinking", type=str2bool, help="only thinking=true or false")
    ap.add_argument("--limit", type=int, help="only the first N segments per direction (overrides `limit` in the config)")
    return ap

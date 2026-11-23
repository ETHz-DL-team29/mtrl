"""Print the env config name matching this machine's GPU, e.g. on Colab:

    python scripts/pick_env.py colab        # -> colab_L4_24G

Matches configs/env/{provider}_*.yaml by gpu.match (substring of the GPU name) and
gpu.mem_gb (within 15%), the same rule check_capabilities enforces. Exits non-zero when
zero or several configs match.
"""
import sys

from mtrl.common.env_setup import gpu_info, pick_env


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    name, mem = gpu_info()
    try:
        print(pick_env(sys.argv[1], name, mem))
    except RuntimeError as e:
        raise SystemExit(str(e))


if __name__ == "__main__":
    main()

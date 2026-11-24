"""Low-frequency GPU-wide and process resource samples; no third-party GPU API."""
from __future__ import annotations
import csv
import datetime
import io
import os
import subprocess
import threading
import time
from .common import append_jsonl


class ResourceSampler:
    def __init__(self, destination, interval=5):
        self.destination = destination
        self.interval = interval
        self.phase = "initializing"
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self.thread.start()

    def _run(self):
        import psutil
        process = psutil.Process(os.getpid())
        process.cpu_percent()
        while not self.stop_event.is_set():
            row = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   "monotonic": time.perf_counter(), "phase": self.phase,
                   "pid": os.getpid(), "process_rss_bytes": process.memory_info().rss,
                   "process_cpu_percent": process.cpu_percent(), "process_threads": process.num_threads()}
            try:
                flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
                result = subprocess.run([
                    "nvidia-smi", "--id=0",
                    "--query-gpu=utilization.gpu,utilization.memory,memory.used,power.draw,temperature.gpu,clocks.sm",
                    "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=4, creationflags=flags)
                if result.returncode == 0:
                    values = next(csv.reader(io.StringIO(result.stdout)))
                    keys = ["gpu_utilization_percent", "gpu_memory_utilization_percent", "gpu_total_used_mib", "gpu_power_watts", "gpu_temperature_c", "gpu_sm_clock_mhz"]
                    for key, value in zip(keys, values):
                        try: row[key] = float(value.strip())
                        except ValueError: row[key] = None
                else:
                    row["gpu_query_error"] = result.stderr.strip()
            except Exception as error:
                row["sampling_error"] = str(error)
            append_jsonl(self.destination, row)
            self.stop_event.wait(self.interval)

    def stop(self):
        self.stop_event.set()
        self.thread.join(timeout=5)

"""
tools/load_test.py
==================
Concurrency / stress-test harness for an Edge hub.

The proposal claims a single Raspberry Pi 5 supports ~50 students. This tool
turns that claim into measured numbers by driving real concurrent traffic at
the live ``/api/chat`` endpoint and reporting latency percentiles, throughput,
error rate, and (if psutil is available) CPU and memory on the machine running
the test.

Important reality check
-----------------------
Ollama serves one inference at a time, so N *simultaneous* chat requests queue
behind each other. This tool measures that honestly: run a concurrency sweep
and you will see p95 latency climb roughly linearly with concurrency while
throughput plateaus at the single-stream token rate. Real classrooms are
*bursty* (students read between questions), so report both the worst case
(all-at-once) and a paced scenario with --think-time.

Usage
-----
    # Point at a running hub and sweep concurrency levels:
    python -m tools.load_test --url http://192.168.1.1:5000 --sweep 1,5,10,25,50

    # Single level, 100 requests, 2s of think-time between a worker's requests:
    python -m tools.load_test --concurrency 10 --requests 100 --think-time 2

Pure helpers (percentile, summarize) are import-safe and unit-tested.
"""
from __future__ import annotations

import argparse
import statistics
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

DEFAULT_URL = "http://127.0.0.1:5000"
DEFAULT_MESSAGE = "What is photosynthesis?"


# ---------------------------------------------------------------------------
# Pure helpers (unit tested)
# ---------------------------------------------------------------------------

def percentile(values: list[float], p: float) -> float:
    """Nearest-rank percentile of *values* (p in [0, 100]). Empty -> 0.0."""
    if not values:
        return 0.0
    s = sorted(values)
    if len(s) == 1:
        return s[0]
    rank = max(1, min(len(s), round(p / 100.0 * len(s))))
    return s[rank - 1]


def summarize(latencies: list[float], errors: int, wall_seconds: float) -> dict:
    """Roll a batch of per-request latencies into the reported metrics."""
    ok = len(latencies)
    total = ok + errors
    throughput = round(ok / wall_seconds, 2) if wall_seconds > 0 else 0.0
    return {
        "requests": total,
        "ok": ok,
        "errors": errors,
        "error_rate": round(errors / total, 3) if total else 0.0,
        "throughput_rpm": round(throughput * 60, 1),
        "throughput_rps": throughput,
        "latency_s": {
            "mean": round(statistics.fmean(latencies), 3) if latencies else 0.0,
            "p50": round(percentile(latencies, 50), 3),
            "p95": round(percentile(latencies, 95), 3),
            "p99": round(percentile(latencies, 99), 3),
            "max": round(max(latencies), 3) if latencies else 0.0,
        },
    }


# ---------------------------------------------------------------------------
# Resource sampling (optional; needs psutil)
# ---------------------------------------------------------------------------

class _ResourceSampler:
    """Sample system CPU% and memory in a background thread while load runs."""

    def __init__(self, interval: float = 0.5):
        self.interval = interval
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self.cpu: list[float] = []
        self.mem_pct: list[float] = []
        try:
            import psutil  # noqa: F401
            self.available = True
        except ImportError:
            self.available = False

    def _run(self):
        import psutil
        while not self._stop.is_set():
            self.cpu.append(psutil.cpu_percent(interval=None))
            self.mem_pct.append(psutil.virtual_memory().percent)
            self._stop.wait(self.interval)

    def __enter__(self):
        if self.available:
            import psutil
            psutil.cpu_percent(interval=None)   # prime the counter
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
        return self

    def __exit__(self, *exc):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)

    def summary(self) -> dict | None:
        if not self.available or not self.cpu:
            return None
        return {
            "cpu_pct_mean": round(statistics.fmean(self.cpu), 1),
            "cpu_pct_max": round(max(self.cpu), 1),
            "mem_pct_mean": round(statistics.fmean(self.mem_pct), 1),
            "mem_pct_max": round(max(self.mem_pct), 1),
        }


# ---------------------------------------------------------------------------
# Load driver (needs the `requests` library + a live server)
# ---------------------------------------------------------------------------

def _one_request(url: str, payload: dict, timeout: float) -> tuple[float | None, bool]:
    """Return (latency_seconds, ok). latency is None on error."""
    import requests
    t0 = time.perf_counter()
    try:
        r = requests.post(f"{url}/api/chat", json=payload, timeout=timeout)
        dt = time.perf_counter() - t0
        return (dt, r.status_code == 200)
    except Exception:
        return (None, False)


def run_level(url: str, *, concurrency: int, requests_total: int, message: str,
              think_time: float, timeout: float) -> dict:
    """Drive *requests_total* requests through *concurrency* parallel workers."""
    payload = {"message": message, "language": "English", "subject": "Science"}
    latencies: list[float] = []
    errors = 0

    def worker(_i):
        if think_time:
            time.sleep(think_time * (_i % concurrency) / max(concurrency, 1))
        return _one_request(url, payload, timeout)

    wall0 = time.perf_counter()
    with _ResourceSampler() as sampler:
        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            futures = [pool.submit(worker, i) for i in range(requests_total)]
            for fut in as_completed(futures):
                dt, ok = fut.result()
                if ok and dt is not None:
                    latencies.append(dt)
                else:
                    errors += 1
    wall = time.perf_counter() - wall0

    result = {"concurrency": concurrency, **summarize(latencies, errors, wall)}
    res = sampler.summary()
    if res:
        result["resources"] = res
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _print_level(r: dict) -> None:
    lat = r["latency_s"]
    line = (f"  conc={r['concurrency']:>3}  ok={r['ok']:>4}  err={r['errors']:>3}  "
            f"thru={r['throughput_rpm']:>6} req/min  "
            f"p50={lat['p50']:>6}s  p95={lat['p95']:>6}s  max={lat['max']:>6}s")
    if "resources" in r:
        res = r["resources"]
        line += f"  cpu~{res['cpu_pct_mean']}%/{res['cpu_pct_max']}%  mem~{res['mem_pct_max']}%"
    print(line)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Load-test an Edge hub's /api/chat.")
    p.add_argument("--url", default=DEFAULT_URL, help="hub base URL")
    p.add_argument("--sweep", default="", help="comma list of concurrency levels, e.g. 1,5,10,25,50")
    p.add_argument("--concurrency", type=int, default=10, help="single concurrency level")
    p.add_argument("--requests", type=int, default=None,
                   help="total requests per level (default: 4x concurrency)")
    p.add_argument("--message", default=DEFAULT_MESSAGE, help="chat message to send")
    p.add_argument("--think-time", type=float, default=0.0,
                   help="seconds of staggered think-time to simulate bursty classroom use")
    p.add_argument("--timeout", type=float, default=120.0, help="per-request timeout (s)")
    args = p.parse_args(argv)

    levels = ([int(x) for x in args.sweep.split(",") if x.strip()]
              if args.sweep else [args.concurrency])

    print(f"Load test against {args.url}  (think-time={args.think_time}s)\n")
    results = []
    for conc in levels:
        total = args.requests or conc * 4
        try:
            r = run_level(args.url, concurrency=conc, requests_total=total,
                          message=args.message, think_time=args.think_time,
                          timeout=args.timeout)
        except ImportError:
            print("The `requests` library is required to drive load.", file=sys.stderr)
            return 2
        _print_level(r)
        results.append(r)

    if any(r["errors"] for r in results):
        print("\nNote: errors usually mean the server is overloaded or unreachable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

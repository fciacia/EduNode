# Edge — Performance & Footprint Audit

Measured on a dev MacBook (Apple Silicon, MPS). A Raspberry Pi 5 (CPU only) is
slower per token, so treat latencies as a **lower bound** for the Pi.

## Per-stage latency

| Stage | Cost | Notes |
|---|---|---|
| Embedder load | ~11 s (once) | `paraphrase-multilingual-MiniLM-L12-v2` + torch |
| NLLB-200 load | ~5 s (once) | only needed for non-English |
| NLLB translate | ~2.5 s / sentence | sentence-by-sentence; the non-English cost driver |
| Retrieval (ChromaDB) | ~0.04 s | negligible |
| Pedagogy (phi3) | ~3.4 s | the dominant LLM cost |
| Verification (embedding) | ~0.2 s | cheap — leaves room for a short LLM check |

**End-to-end chat:**
- English: ~3.7 s (retrieval + phi3 + verify)
- Non-English: ~+5 s (NLLB in + out)

## Memory (RSS)

| Component | RAM |
|---|---|
| Flask process warm (embedder + NLLB + torch) | ~3.5 GB |
| phi3 (separate Ollama process) | ~2.4 GB |
| Each cached MMS voice | ~0.15 GB |
| **Total (typical)** | **~5.9 GB** (within the 7.4 GB Pi budget, but tight) |

## Mitigations implemented

- **Prewarming** (`EDGE_PREWARM=1`, default on): a background thread loads the
  embedder (and NLLB if the hub serves a non-English language) at startup, so the
  first user request doesn't eat the ~16 s cold-load stall. Set `EDGE_PREWARM=0`
  to disable.
- **MMS voice cache cap** (`_MMS_CACHE_MAX=2`): keeps at most two MMS-TTS voice
  models resident (LRU), bounding RAM when several languages are used.

## Recommendations for the Pi

- **English / Tier-1 languages are within target**; non-English chat will exceed
  3 s because of NLLB — acceptable, but set expectations.
- Keep concurrent languages small (the 8 GB ceiling realistically supports phi3 +
  embedder + NLLB + one or two voices).
- Consider a smaller quantized phi3 and `ggml-base` (not larger) Whisper to stay
  in budget.

## Concurrency & load testing

The "up to 50 students per hub" figure describes **connected** students, not 50
*simultaneous* model inferences. Ollama serves one generation at a time, so
concurrent chat requests queue. The honest model of classroom use is **bursty**:
students read an answer, think, and type — so the steady-state concurrency of
*in-flight inferences* is far below the headcount.

### How to measure it

```bash
# On the hub (or a laptop on the same network), drive concurrent traffic:
python -m tools.load_test --url http://192.168.1.1:5000 --sweep 1,5,10,25,50

# Bursty (realistic) classroom: stagger requests with think-time
python -m tools.load_test --url http://192.168.1.1:5000 --concurrency 50 --think-time 8
```

`tools/load_test.py` reports, per concurrency level: requests, errors, throughput
(req/min), latency **p50 / p95 / p99 / max**, and — when `psutil` is installed —
CPU% and memory%. Run it **on the Pi target**, not a dev laptop, for figures that
back the deployment claim.

### Implemented mitigations for many concurrent students

- **Admission-control queue** ([core/request_queue.py](../core/request_queue.py)):
  a bounded gate caps simultaneous heavy inferences (`EDGE_MAX_CONCURRENCY`,
  default 2). Excess requests wait up to `EDGE_QUEUE_TIMEOUT` seconds, then get a
  graceful `503 busy` with `Retry-After` instead of pushing the node into
  out-of-memory. Live `active`/`waiting`/`rejected` metrics are exposed on
  `/api/status`. This bounds RAM regardless of how many students connect.
- **Client-side TTS offload** ([templates/chat.html](../templates/chat.html)):
  read-aloud uses the **phone's** on-device speech engine when it has a voice for
  the language (English and major ASEAN languages), so text-to-speech costs the
  hub nothing for the common case. Minority languages with no phone voice (Iban,
  Cebuano, …) fall back to the hub's neural TTS.

### Measured results (dev MacBook, phi3:mini, gate cap = 2)

Run with `tools/load_test.py`, 6 requests per level, English chat:

| Concurrency | Throughput (req/min) | p50 (s) | p95 (s) | Errors |
|---|---|---|---|---|
| 1 | 7.8 | 5.5 | 17.0 | 0 |
| 3 | 11.4 | 10.1 | 20.7 | 0 |
| 5 | 10.8 | 23.2 | 32.3 | 0 |

**What this shows (exactly the predicted shape):** throughput plateaus around
10–11 req/min — the single-stream phi3 rate — while p50 latency climbs roughly
linearly with concurrency, because requests queue behind the gate's 2 inference
slots. **Zero errors**: the admission gate makes excess requests *wait* rather than
crash the node (timeout was 120 s). A Raspberry Pi 5 (CPU-only) will show higher
absolute latencies, so re-run on the Pi to fill in the deployment table below; the
*shape* (plateau + linear latency) will hold.

### Results table (fill in from a Pi run)

| Concurrency | Throughput (req/min) | p50 (s) | p95 (s) | Errors | CPU% (max) | Mem% (max) |
|---|---|---|---|---|---|---|
| 1 | _measure_ | _measure_ | _measure_ | _measure_ | _measure_ | _measure_ |
| 5 | _measure_ | _measure_ | _measure_ | _measure_ | _measure_ | _measure_ |
| 10 | _measure_ | _measure_ | _measure_ | _measure_ | _measure_ | _measure_ |
| 25 | _measure_ | _measure_ | _measure_ | _measure_ | _measure_ | _measure_ |
| 50 (all-at-once) | _measure_ | _measure_ | _measure_ | _measure_ | _measure_ | _measure_ |
| 50 (think-time 8s) | _measure_ | _measure_ | _measure_ | _measure_ | _measure_ | _measure_ |

**Expected shape of the result:** throughput plateaus near the single-stream token
rate (≈1 inference at a time), so p95 latency climbs roughly linearly with the
number of *simultaneously waiting* requests. The all-at-once row is the worst case;
the think-time row reflects real classroom pacing and is the number to deploy
against. If the all-at-once p95 is unacceptable, the mitigation is a request queue
with a "you're number N in line" message rather than more hardware.

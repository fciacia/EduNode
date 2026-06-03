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

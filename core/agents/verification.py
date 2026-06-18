"""
core/agents/verification.py
===========================
Verification Agent. Scores how well a generated answer is grounded in the source
chunks and extracts page-level citations.

Two signals combine into the confidence:
  1. Embedding similarity of the answer to the source chunks (fast, deterministic).
  2. A short, schema-constrained LLM self-check that audits whether the answer is
     actually supported by the source text (the roadmap's anti-hallucination
     "Verification Agent"). Enabled by default; set EDGE_LLM_VERIFY=0 to skip it
     (faster). Falls back to embedding-only if the model is unavailable.
"""
from __future__ import annotations

import json
import logging
import os

from core.agents import Chunk, Verification

log = logging.getLogger(__name__)

import os

# Below CONFIDENCE_THRESHOLD an answer is flagged needs_review (amber badge).
# Calibrated against the confidence the pipeline actually produces — the LLM
# self-check compresses scores, so 0.85 was unreachable and flagged everything.
# Tune per deployment/model with tools/eval_rag.py (compare mean confidence of
# correct vs incorrect answers).
CONFIDENCE_THRESHOLD = float(os.getenv("EDGE_CONFIDENCE_THRESHOLD", "0.55"))
CITATION_FLOOR = 0.30         # per-chunk grounding sim to count as a citation
# When the LLM self-check disagrees, down-weight confidence by this factor rather
# than collapsing it: a small-model "unsupported" verdict is a soft signal, not an
# oracle, and must not erase a strong embedding grounding.
UNSUPPORTED_PENALTY = float(os.getenv("EDGE_UNSUPPORTED_PENALTY", "0.75"))

_VERIFY_SCHEMA = {
    "type": "object",
    "properties": {
        "supported":  {"type": "boolean"},
        "confidence": {"type": "number"},
    },
    "required": ["supported", "confidence"],
}


def _llm_verify(answer_en: str, chunks: list[Chunk]) -> float | None:
    """
    Ask the model whether *answer_en* is supported by the source chunks.
    Returns a confidence in [0, 1], or None if disabled/unavailable.
    """
    if os.getenv("EDGE_LLM_VERIFY", "1") == "0":
        return None
    from core.llm_engine import _ollama_generate

    source = "\n---\n".join(c.text for c in chunks)[:1200]
    prompt = (
        f"Source text:\n{source}\n\n"
        f"Answer:\n{answer_en}\n\n"
        "Is the answer fully supported by the source text above?"
    )
    raw = _ollama_generate(
        prompt,
        temperature=0.0,
        max_tokens=40,
        system="You check whether an answer is supported by source text. Be strict and concise.",
        schema=_VERIFY_SCHEMA,
    )
    if not raw:
        return None
    try:
        data = json.loads(raw)
        conf = float(data.get("confidence", 0.0))
        if not data.get("supported", False):
            conf = min(conf, 0.4)          # unsupported -> cap low
        return max(0.0, min(1.0, conf))
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        log.debug("LLM verify parse failed: %s", exc)
        return None


def _get_embedder():
    """Indirection so tests can patch the embedder."""
    from core.rag_engine import get_embedder
    return get_embedder()


def _cosine(a, b) -> float:
    import numpy as np
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def score(answer_en: str, chunks: list[Chunk]) -> Verification:
    """Return a Verification with confidence, citations and needs_review."""
    if not chunks:
        return Verification(confidence=0.0, citations=[], needs_review=True)

    embedder = _get_embedder()
    texts = [answer_en] + [c.text for c in chunks]
    vectors = embedder.encode(texts)
    answer_vec = vectors[0]
    chunk_vecs = vectors[1:]

    sims = [_cosine(answer_vec, cv) for cv in chunk_vecs]
    grounding_score = max(sims) if sims else 0.0

    best_distance = min(c.distance for c in chunks)
    retrieval_score = max(0.0, 1.0 - best_distance)

    embed_confidence = 0.5 * retrieval_score + 0.5 * grounding_score

    # The LLM self-check is a soft penalty, not a veto: when the model judges the
    # answer unsupported, down-weight the embedding confidence by UNSUPPORTED_PENALTY
    # so a borderline/off-topic answer is flagged — but a strong embedding grounding
    # (low distance + high similarity) still shows through instead of being collapsed
    # to near-zero by a single cautious small-model verdict.
    llm_confidence = _llm_verify(answer_en, chunks)
    if llm_confidence is not None and llm_confidence < 0.5:
        confidence = round(embed_confidence * UNSUPPORTED_PENALTY, 3)
    else:
        confidence = round(embed_confidence, 3)

    citations = []
    for chunk, sim in zip(chunks, sims):
        if sim >= CITATION_FLOOR:
            entry = {"source": chunk.source, "page": chunk.page}
            if entry not in citations:
                citations.append(entry)

    return Verification(
        confidence=confidence,
        citations=citations,
        needs_review=confidence < CONFIDENCE_THRESHOLD,
    )

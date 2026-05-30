"""
core/agents/verification.py
===========================
Verification Agent. Scores how well a generated answer is grounded in the source
chunks (cosine similarity in embedding space) and extracts page-level citations.
Deterministic — no extra LLM call.
"""
from __future__ import annotations

import logging

from core.agents import Chunk, Verification

log = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.85   # below this -> needs_review
CITATION_FLOOR = 0.30         # per-chunk grounding sim to count as a citation


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

    confidence = round(0.5 * retrieval_score + 0.5 * grounding_score, 3)

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

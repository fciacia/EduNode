"""
core/agents/orchestrator.py
===========================
Sequences the four-agent pipeline and owns the confidence gates:
  Translation -> Context -> Retrieval(gate) -> Pedagogy -> Verification(gate) -> Translation
"""
from __future__ import annotations

import logging

log = logging.getLogger(__name__)

RETRIEVAL_DISTANCE_GATE = 0.65   # best chunk distance above this -> non-response

_NON_RESPONSE_EN = (
    "I don't have curriculum material on that topic yet. "
    "Please ask your teacher, or try rephrasing your question."
)


def _translate_in(query: str, language: str) -> str:
    from core.agents.translation import to_english
    return to_english(query, language)


def _translate_out(answer: str, language: str) -> str:
    from core.agents.translation import to_native
    return to_native(answer, language)


def run_pipeline(query: str, language: str, student_id, subject: str = "General") -> dict:
    """
    Run the full agentic pipeline.
    Returns {answer, confidence, citations, needs_review, language}.
    """
    from core.agents import context as context_agent
    from core.agents import pedagogy, verification
    from core.rag_engine import retrieve_with_citations

    # 1. Translate query into English
    query_en = _translate_in(query, language)

    # 2. Build student context
    ctx = context_agent.build(student_id)

    # 3. Retrieve + RETRIEVAL GATE
    chunks = retrieve_with_citations(query_en, n_results=3, subject=subject)
    best_distance = min((c.distance for c in chunks), default=1.0)
    if not chunks or best_distance > RETRIEVAL_DISTANCE_GATE:
        log.info("Retrieval gate triggered (best_distance=%.3f) — controlled non-response.", best_distance)
        return {
            "answer": _translate_out(_NON_RESPONSE_EN, language),
            "confidence": 0.0,
            "citations": [],
            "needs_review": True,
            "language": language,
        }

    # 4. Reason (Phi-3)
    answer_en = pedagogy.reason(query_en, ctx, chunks)
    if not answer_en:
        return {
            "answer": _translate_out(_NON_RESPONSE_EN, language),
            "confidence": 0.0,
            "citations": [],
            "needs_review": True,
            "language": language,
        }

    # 5. Verify + VERIFICATION GATE
    #    If the embedder is unavailable (e.g. first-run download fails on an
    #    offline node), still return the answer but flag it for review rather
    #    than letting the exception surface as a 500 to the student.
    try:
        result = verification.score(answer_en, chunks)
        confidence, citations, needs_review = (
            result.confidence, result.citations, result.needs_review,
        )
    except Exception as exc:  # noqa: BLE001
        log.warning("Verification failed: %s — returning answer unverified.", exc)
        confidence, citations, needs_review = 0.0, [], True

    # 6. Translate answer back to the student's language
    answer_native = _translate_out(answer_en, language)

    return {
        "answer": answer_native,
        "confidence": confidence,
        "citations": citations,
        "needs_review": needs_review,
        "language": language,
    }

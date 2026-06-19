"""
core/agents/orchestrator.py
===========================
Sequences the four-agent pipeline and owns the confidence gates:
  Translation -> Context -> Retrieval(gate) -> Pedagogy -> Verification(gate) -> Translation

Tiered response strategy
------------------------
The retrieval distance of the best-matching curriculum chunk decides the tier:

  best_distance <= GROUNDED_GATE                      -> "grounded"
      Answer strictly from the curriculum, verified and cited.
  GROUNDED_GATE < best_distance <= SUPPLEMENTARY_GATE -> "supplementary"
      The curriculum doesn't cover it, but it's a near miss. Answer from the
      model's general knowledge, clearly labelled as NOT from the textbook and
      flagged for teacher review. Reduces "I don't know" frustration without
      pretending general knowledge is curriculum-grounded.
  best_distance > SUPPLEMENTARY_GATE                  -> "none"
      Too far off-topic — return a controlled non-response.
"""
from __future__ import annotations

import logging
import os

log = logging.getLogger(__name__)

# Best chunk distance at/below GROUNDED_GATE -> grounded (cited) answer; between
# the gates -> labelled general-knowledge answer; above -> non-response.
# The grounded gate is deliberately tight: an off-topic question that happens to
# land lexically near the curriculum (e.g. a calculus question grazing the maths
# pages) should fall to the supplementary tier, not be cited as curriculum-backed.
# Tune per deployment/model with tools/eval_rag.py.
GROUNDED_GATE = float(os.getenv("EDGE_GROUNDED_GATE", "0.55"))
SUPPLEMENTARY_GATE = float(os.getenv("EDGE_SUPPLEMENTARY_GATE", "0.85"))
# Supplementary answers come from the model's general knowledge (ungrounded,
# unverified) and carry some hallucination risk even when clearly labelled. A
# strict deployment can disable the tier (EDGE_SUPPLEMENTARY_ENABLED=0) so a
# near-miss falls straight to a controlled non-response instead.
SUPPLEMENTARY_ENABLED = os.getenv("EDGE_SUPPLEMENTARY_ENABLED", "1") != "0"

_NON_RESPONSE_EN = (
    "I don't have curriculum material on that topic yet. "
    "Please ask your teacher, or try rephrasing your question."
)

# Prepended (in English, before translation) to general-knowledge answers so the
# student always knows the reply is not drawn from their textbook.
_SUPPLEMENTARY_LABEL_EN = (
    "Note: this is not in your textbook — here is a general explanation:\n\n"
)


def _translate_in(query: str, language: str) -> str:
    from core.agents.translation import to_english
    return to_english(query, language)


def _translate_out(answer: str, language: str) -> str:
    from core.agents.translation import to_native
    return to_native(answer, language)


def _non_response(language: str) -> dict:
    return {
        "answer": _translate_out(_NON_RESPONSE_EN, language),
        "confidence": 0.0,
        "citations": [],
        "needs_review": True,
        "tier": "none",
        "language": language,
    }


def run_pipeline(query: str, language: str, student_id, subject: str = "General",
                 conversation_id: str | None = None) -> dict:
    """
    Run the full agentic pipeline.
    Returns {answer, confidence, citations, needs_review, tier, language}.

    *conversation_id* enables conversational memory: recent English turns are
    fed to the pedagogy agent so follow-up questions are answered in context.
    """
    from core.agents import context as context_agent
    from core.agents import pedagogy, verification
    from core.conversation import append_turn, get_history
    from core.rag_engine import retrieve_with_citations

    # 1. Translate query into English
    query_en = _translate_in(query, language)

    # 2. Build student context
    ctx = context_agent.build(student_id)
    history = get_history(conversation_id)

    # 3. Retrieve + measure best distance
    #    Gate on the question itself, so a clear in-curriculum question always
    #    grounds. Also try a history-augmented query so vague follow-ups
    #    ("explain that more simply") still match the topic — keep whichever
    #    retrieves better. (History alone can otherwise drag a clear question
    #    over the gate when earlier turns were about something else.)
    prior = " ".join(t["text"] for t in history if t.get("role") == "user")
    chunks = retrieve_with_citations(query_en, n_results=3, subject=subject)
    best_distance = min((c.distance for c in chunks), default=1.0)
    # Cross-lingual retrieval: the embedder is multilingual, so retrieving on the
    # student's ORIGINAL question avoids the translation noise that otherwise
    # degrades retrieval for non-English languages (measured: Thai/Vietnamese
    # grounding dropped to ~50% when retrieving on the translated query). Keep
    # whichever query grounds better. English is pass-through, so skip it.
    if language and language.lower() != "english" and query.strip() and query.strip() != query_en.strip():
        native = retrieve_with_citations(query, n_results=3, subject=subject)
        native_best = min((c.distance for c in native), default=1.0)
        if native_best < best_distance:
            chunks, best_distance = native, native_best
    if prior:
        aug = retrieve_with_citations((prior + " " + query_en).strip(), n_results=3, subject=subject)
        aug_best = min((c.distance for c in aug), default=1.0)
        if aug_best < best_distance:
            chunks, best_distance = aug, aug_best
    # The subject picker hard-filters the curriculum. If nothing matches in the
    # chosen subject, retry across ALL subjects so a science question asked while
    # "Mathematics" is selected still finds its answer.
    if best_distance > GROUNDED_GATE and subject and subject not in ("", "General"):
        anysub = retrieve_with_citations(query_en, n_results=3, subject="")
        anysub_best = min((c.distance for c in anysub), default=1.0)
        if anysub_best < best_distance:
            chunks, best_distance = anysub, anysub_best

    # 3b. TIER SELECTION
    if not chunks or best_distance > SUPPLEMENTARY_GATE:
        log.info("Non-response tier (best_distance=%.3f).", best_distance)
        return _non_response(language)

    if best_distance > GROUNDED_GATE:
        if not SUPPLEMENTARY_ENABLED:
            log.info("Supplementary disabled — non-response (best_distance=%.3f).", best_distance)
            return _non_response(language)
        # Supplementary tier: near miss — answer from general knowledge, labelled.
        log.info("Supplementary tier (best_distance=%.3f).", best_distance)
        supp_en = pedagogy.reason_supplementary(query_en, ctx, history)
        if not supp_en:
            return _non_response(language)
        answer_native = _translate_out(_SUPPLEMENTARY_LABEL_EN + supp_en, language)
        append_turn(conversation_id, "user", query_en)
        append_turn(conversation_id, "assistant", supp_en)
        return {
            "answer": answer_native,
            "confidence": 0.0,          # not curriculum-verified
            "citations": [],            # not grounded in the curriculum
            "needs_review": True,       # flag supplementary answers for teachers
            "tier": "supplementary",
            "language": language,
        }

    # 4. Grounded tier — reason (Phi-3) with conversational history for follow-ups
    answer_en = pedagogy.reason(query_en, ctx, chunks, history)
    if not answer_en:
        return _non_response(language)

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

    # 7. Remember this exchange (English) for follow-up questions
    append_turn(conversation_id, "user", query_en)
    append_turn(conversation_id, "assistant", answer_en)

    return {
        "answer": answer_native,
        "confidence": confidence,
        "citations": citations,
        "needs_review": needs_review,
        "tier": "grounded",
        "language": language,
    }

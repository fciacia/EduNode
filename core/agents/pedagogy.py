"""
core/agents/pedagogy.py
=======================
Pedagogical Reasoning Agent. Produces an English answer grounded strictly in the
retrieved curriculum chunks, tuned to the student's difficulty level.
"""
from __future__ import annotations

from core.agents import Chunk, StudentContext

_DIFFICULTY_GUIDE = {
    "simple":    "Use very short sentences and basic vocabulary.",
    "standard":  "Use clear language appropriate for a secondary school student.",
    "challenge": "You may use richer detail and introduce one extension idea.",
}


def _build_prompt(query_en: str, chunks: list[Chunk], history: list[dict] | None = None) -> str:
    context_block = "\n---\n".join(c.text for c in chunks) if chunks else ""

    history_block = ""
    if history:
        lines = [
            f"{'Student' if t.get('role') == 'user' else 'Tutor'}: {t.get('text', '')}"
            for t in history
        ]
        history_block = "Conversation so far:\n" + "\n".join(lines) + "\n\n"

    return (
        f"Curriculum context:\n{context_block}\n\n"
        f"{history_block}"
        f"Student question: {query_en}"
    )


def _build_system(context: StudentContext) -> str:
    guide = _DIFFICULTY_GUIDE.get(context.difficulty, _DIFFICULTY_GUIDE["standard"])
    return (
        "You are Edge, an offline AI tutor for rural ASEAN students. "
        "Answer ONLY using the provided curriculum context. "
        "If the context does not contain the answer, say you don't have that "
        "information yet rather than guessing. "
        f"Explain at a {context.difficulty} level for a grade {context.grade} student. "
        f"{guide} "
        "Use plain, simple words. Do NOT use chemical formulas, symbols, equations "
        "or abbreviations — write them out in words (for example, write "
        "'carbon dioxide', not 'CO2'). This keeps answers clear for young learners "
        "and accurate when translated into local languages. "
        "Keep your answer under 150 words. Respond in English."
    )


def reason(query_en: str, context: StudentContext, chunks: list[Chunk],
           history: list[dict] | None = None) -> str:
    """Generate an English, curriculum-grounded answer. Returns '' on model failure.

    *history* is the recent conversation (English turns) so the tutor can handle
    follow-up questions in context.
    """
    from core.llm_engine import _ollama_generate

    prompt = _build_prompt(query_en, chunks, history)
    system = _build_system(context)
    return _ollama_generate(prompt, temperature=0.5, system=system)


def _build_supplementary_system(context: StudentContext) -> str:
    guide = _DIFFICULTY_GUIDE.get(context.difficulty, _DIFFICULTY_GUIDE["standard"])
    return (
        "You are Edge, an offline AI tutor for rural ASEAN students. "
        "The school's curriculum does not cover this question, so answer from your "
        "own general knowledge. Give a short, safe, factual explanation suitable "
        "for a child. If you are not sure, say so plainly rather than guessing. "
        f"Explain at a {context.difficulty} level for a grade {context.grade} student. "
        f"{guide} "
        "Use plain, simple words. Do NOT use chemical formulas, symbols, equations "
        "or abbreviations — write them out in words. "
        "Keep your answer under 120 words. Respond in English."
    )


def reason_supplementary(query_en: str, context: StudentContext,
                         history: list[dict] | None = None) -> str:
    """Generate a general-knowledge answer for questions the curriculum does not
    cover. Used by the supplementary tier; the orchestrator labels the result so
    students know it is not drawn from their textbook. Returns '' on model failure.
    """
    from core.llm_engine import _ollama_generate

    prompt = _build_prompt(query_en, [], history)
    system = _build_supplementary_system(context)
    return _ollama_generate(prompt, temperature=0.5, system=system)

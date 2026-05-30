"""
core/agents/context.py
======================
Personalised Context Agent. Reads a student's grade and recent quiz performance
from SQLite and derives a difficulty hint for the pedagogy agent.
"""
from __future__ import annotations

import logging

from core.agents import StudentContext

log = logging.getLogger(__name__)


def _difficulty_from_average(avg_pct: float | None) -> str:
    if avg_pct is None:
        return "standard"
    if avg_pct < 50:
        return "simple"
    if avg_pct >= 85:
        return "challenge"
    return "standard"


def build(student_id: int | None) -> StudentContext:
    """Build a StudentContext from the student's history. Safe defaults if unknown."""
    default = StudentContext(grade="general", avg_score=0.0, weak_subjects=[], difficulty="standard")
    if not student_id:
        return default

    try:
        import core.progress_tracker as pt
        with pt._db() as conn:
            srow = conn.execute(
                "SELECT grade FROM students WHERE id=?", (student_id,)
            ).fetchone()
            if not srow:
                return default

            qrows = conn.execute(
                "SELECT topic, score, total FROM quiz_results"
                " WHERE student_id=? AND total>0 ORDER BY taken_at DESC LIMIT 10",
                (student_id,),
            ).fetchall()
    except Exception as exc:  # noqa: BLE001
        log.warning("Context build failed for student %s: %s", student_id, exc)
        return default

    grade = str(srow["grade"]) if srow["grade"] else "general"

    if qrows:
        pcts = [r["score"] / r["total"] * 100 for r in qrows]
        avg = sum(pcts) / len(pcts)
        weak = sorted({r["topic"] for r in qrows if r["score"] / r["total"] < 0.5})
    else:
        avg = None
        weak = []

    return StudentContext(
        grade=grade,
        avg_score=round(avg, 1) if avg is not None else 0.0,
        weak_subjects=weak,
        difficulty=_difficulty_from_average(avg),
    )

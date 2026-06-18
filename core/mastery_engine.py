"""
core/mastery_engine.py
======================
Per-concept mastery tracking and adaptive remediation (Issue 5).

Personalisation in Edge started as grade-level difficulty adjustment. This module
adds the next layer: it aggregates a student's quiz history **per topic** into a
mastery level, then recommends concrete next steps for the concepts they struggle
with — remedial lessons for weak topics, extra practice for developing ones.

It reads the existing ``quiz_results`` table (see core.progress_tracker); no new
schema is required.

Public API
----------
concept_mastery(student_id) -> list[dict]
    Per-topic {topic, attempts, avg_pct, level} sorted weakest-first.

recommendations(student_id, limit=3) -> list[dict]
    Adaptive next steps {topic, level, avg_pct, action, reason} for the weakest
    concepts the student has not yet mastered.
"""
from __future__ import annotations

import logging

log = logging.getLogger(__name__)

# Mastery thresholds on the running average percentage for a topic.
STRUGGLING_BELOW = 50.0     # avg_pct < 50  -> needs a remedial lesson
MASTERED_AT = 80.0          # avg_pct >= 80 -> mastered; below this -> developing

_ACTION = {
    "struggling": ("remedial lesson",
                   "Scores are low here — review the lesson and try a guided example."),
    "developing": ("extra practice",
                   "Almost there — a few more practice questions will lock this in."),
}


def _level(avg_pct: float) -> str:
    if avg_pct < STRUGGLING_BELOW:
        return "struggling"
    if avg_pct >= MASTERED_AT:
        return "mastered"
    return "developing"


def concept_mastery(student_id: int | None) -> list[dict]:
    """Aggregate every quiz attempt per topic into a mastery level.

    Returns a list sorted weakest-first (lowest average). Empty if the student is
    unknown or has no graded attempts.
    """
    if not student_id:
        return []
    try:
        import core.progress_tracker as pt
        with pt._db() as conn:
            rows = conn.execute(
                "SELECT topic, score, total FROM quiz_results"
                " WHERE student_id=? AND total>0",
                (student_id,),
            ).fetchall()
    except Exception as exc:  # noqa: BLE001
        log.warning("concept_mastery failed for student %s: %s", student_id, exc)
        return []

    # Aggregate by NORMALISED topic so 'Fractions' and ' fractions ' are one
    # concept; keep the first-seen original casing for display.
    from core.progress_tracker import normalize_topic
    buckets: dict[str, dict] = {}
    for r in rows:
        key = normalize_topic(r["topic"])
        b = buckets.setdefault(key, {"display": r["topic"], "got": 0, "possible": 0, "attempts": 0})
        b["got"] += r["score"]
        b["possible"] += r["total"]
        b["attempts"] += 1

    out = []
    for b in buckets.values():
        if b["possible"] == 0:
            continue
        avg_pct = round(b["got"] / b["possible"] * 100, 1)
        out.append({
            "topic": b["display"],
            "attempts": b["attempts"],
            "avg_pct": avg_pct,
            "level": _level(avg_pct),
        })
    out.sort(key=lambda d: d["avg_pct"])
    return out


def recommendations(student_id: int | None, limit: int = 3) -> list[dict]:
    """Adaptive next steps for the weakest not-yet-mastered concepts."""
    recs = []
    for m in concept_mastery(student_id):
        if m["level"] == "mastered":
            continue
        action, reason = _ACTION[m["level"]]
        recs.append({
            "topic": m["topic"],
            "level": m["level"],
            "avg_pct": m["avg_pct"],
            "action": action,
            "reason": reason,
        })
        if len(recs) >= limit:
            break
    return recs

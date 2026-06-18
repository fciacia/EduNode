"""
core/analytics_engine.py
========================
Teacher-facing analytics (Issue 7).

Aggregates the data Edge already logs (sessions, quiz_results, dialect_logs,
translation reports) into a class-level view so teachers can see progress trends,
the concepts students miss most, activity, and AI usage — the visibility a teacher
needs to support a classroom.

Read-only over the existing SQLite tables; no new schema.

Public API
----------
class_overview()            -> headline counts + class average
most_missed_topics(limit)   -> concepts with the lowest class average (misconceptions)
activity_by_subject()       -> session counts per subject (AI usage)
activity_by_day(days)       -> session counts per day (engagement trend)
recent_flags(limit)         -> latest translation/answer flags for review
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)

TRANSLATION_REPORTS = Path("data/translation_reports.jsonl")


def class_overview() -> dict:
    """Headline counts and the class-wide quiz average."""
    import core.progress_tracker as pt
    with pt._db() as conn:
        students = conn.execute("SELECT COUNT(*) AS n FROM students").fetchone()["n"]
        sessions = conn.execute("SELECT COUNT(*) AS n FROM sessions").fetchone()["n"]
        attempts = conn.execute("SELECT COUNT(*) AS n FROM quiz_results").fetchone()["n"]
        agg = conn.execute(
            "SELECT SUM(score) AS got, SUM(total) AS possible FROM quiz_results WHERE total>0"
        ).fetchone()
        today = conn.execute(
            "SELECT COUNT(DISTINCT student_id) AS n FROM sessions"
            " WHERE substr(started_at,1,10) = substr(?,1,10)",
            (pt._now(),),
        ).fetchone()["n"]
    possible = (agg["possible"] or 0) if agg else 0
    avg = round((agg["got"] / possible) * 100, 1) if possible else None
    return {
        "students": students,
        "sessions": sessions,
        "quiz_attempts": attempts,
        "class_avg_pct": avg,
        "active_today": today,
    }


def most_missed_topics(limit: int = 5) -> list[dict]:
    """Concepts with the lowest class average — the misconceptions to reteach."""
    import core.progress_tracker as pt
    with pt._db() as conn:
        rows = conn.execute(
            "SELECT topic,"
            "       SUM(score) AS got, SUM(total) AS possible,"
            "       COUNT(*) AS attempts,"
            "       COUNT(DISTINCT student_id) AS students"
            "  FROM quiz_results WHERE total>0"
            " GROUP BY topic HAVING possible > 0"
            " ORDER BY (CAST(SUM(score) AS FLOAT)/SUM(total)) ASC"
            " LIMIT ?",
            (limit,),
        ).fetchall()
    return [
        {"topic": r["topic"], "attempts": r["attempts"], "students": r["students"],
         "avg_pct": round(r["got"] / r["possible"] * 100, 1)}
        for r in rows
    ]


def activity_by_subject() -> list[dict]:
    """Session counts per subject (which subjects the AI is used for)."""
    import core.progress_tracker as pt
    with pt._db() as conn:
        rows = conn.execute(
            "SELECT subject, COUNT(*) AS sessions FROM sessions"
            " GROUP BY subject ORDER BY sessions DESC"
        ).fetchall()
    return [{"subject": r["subject"], "sessions": r["sessions"]} for r in rows]


def activity_by_day(days: int = 7) -> list[dict]:
    """Session counts per day for the most recent *days* with activity."""
    import core.progress_tracker as pt
    with pt._db() as conn:
        rows = conn.execute(
            "SELECT substr(started_at,1,10) AS day, COUNT(*) AS sessions"
            "  FROM sessions GROUP BY day ORDER BY day DESC LIMIT ?",
            (days,),
        ).fetchall()
    return [{"day": r["day"], "sessions": r["sessions"]} for r in reversed(rows)]


def recent_flags(limit: int = 10) -> list[dict]:
    """Latest teacher/student translation flags (also feeds the correction loop)."""
    if not TRANSLATION_REPORTS.exists():
        return []
    try:
        lines = TRANSLATION_REPORTS.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        log.warning("Could not read translation reports: %s", exc)
        return []
    out = []
    for line in lines[-limit:][::-1]:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def dashboard() -> dict:
    """Everything the teacher dashboard needs in one call."""
    return {
        "overview": class_overview(),
        "most_missed": most_missed_topics(),
        "by_subject": activity_by_subject(),
        "by_day": activity_by_day(),
        "flags": recent_flags(),
    }

"""
core/review_engine.py
======================
Spaced repetition for flashcards using Leitner boxes.

A card a student gets right moves up a box (longer interval before it returns);
a card they want to review again resets to box 1 (due immediately). Due cards are
resurfaced on the flashcard page so struggling material comes back at the right
time. Data lives in the ``review_items`` table (see progress_tracker schema).

Public API
----------
save_review(student_id, topic, front, back, verdict)  # verdict: "known" | "review"
get_due(student_id, limit=20) -> list[dict]
count_due(student_id) -> int
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from core.progress_tracker import _db, _now

# Leitner box -> days until the card is due again.
_LEITNER_DAYS = {1: 0, 2: 1, 3: 3, 4: 7, 5: 16}
_MAX_BOX = 5


def _due_in(days: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(days=days)).isoformat()


def save_review(student_id: int, topic: str, front: str, back: str, verdict: str) -> None:
    """
    Record a flashcard review and reschedule it (Leitner):
      - "known"  → advance one box (up to box 5), due further in the future
      - anything else ("review"/"again") → reset to box 1, due now
    """
    front = (front or "").strip()
    if not student_id or not front:
        return

    with _db() as conn:
        row = conn.execute(
            "SELECT box FROM review_items WHERE student_id=? AND front=?",
            (student_id, front),
        ).fetchone()
        box = row["box"] if row else 1

        box = min(box + 1, _MAX_BOX) if verdict == "known" else 1
        due = _due_in(_LEITNER_DAYS.get(box, 0))

        conn.execute(
            """
            INSERT INTO review_items (student_id, topic, front, back, box, due_at, last_seen)
            VALUES (?,?,?,?,?,?,?)
            ON CONFLICT(student_id, front) DO UPDATE SET
                topic=excluded.topic, back=excluded.back, box=excluded.box,
                due_at=excluded.due_at, last_seen=excluded.last_seen
            """,
            (student_id, topic or "", front, back or "", box, due, _now()),
        )


def get_due(student_id: int, limit: int = 20) -> list[dict]:
    """Return cards due for review now (soonest first)."""
    now = _now()
    with _db() as conn:
        rows = conn.execute(
            "SELECT topic, front, back, box FROM review_items"
            " WHERE student_id=? AND due_at<=? ORDER BY due_at ASC LIMIT ?",
            (student_id, now, limit),
        ).fetchall()
    return [dict(r) for r in rows]


def count_due(student_id: int) -> int:
    """How many cards are due for review right now."""
    if not student_id:
        return 0
    now = _now()
    with _db() as conn:
        return conn.execute(
            "SELECT COUNT(*) AS n FROM review_items WHERE student_id=? AND due_at<=?",
            (student_id, now),
        ).fetchone()["n"]

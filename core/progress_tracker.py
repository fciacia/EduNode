"""
core/progress_tracker.py
========================
Step 7 — SQLite-backed student progress, sessions, quiz results, badges,
and dialect logging.

Public API
----------
init_db()
    Create all tables (idempotent — safe to call on every startup).

get_or_create_student(name, language, grade) -> int
    Returns the student_id for the named student, creating the row if needed.

log_session(student_id, subject, message_count)
    Record a completed chat session.

log_quiz_result(student_id, topic, score, total)
    Record a quiz attempt and trigger badge evaluation.

check_and_award_badges(student_id)
    Evaluate all badge rules and INSERT any newly earned badges.

get_progress(student_id) -> dict
    Return {"badges": [...], "recent_quizzes": [...], "sessions_count": int}

log_dialect(language, raw_input, dialect_variant="")
    Append an entry to dialect_logs for future analysis.
"""

from __future__ import annotations

import logging
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger(__name__)

DB_PATH = Path(os.getenv("DB_PATH", "db/edunode.db"))

# ---------------------------------------------------------------------------
# Connection helper
# ---------------------------------------------------------------------------

def _get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")   # safe concurrent reads on Pi
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def _db():
    conn = _get_conn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

_SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    language   TEXT    NOT NULL DEFAULT 'English',
    grade      INTEGER NOT NULL DEFAULT 0,
    created_at TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id    INTEGER NOT NULL REFERENCES students(id),
    subject       TEXT    NOT NULL DEFAULT 'General',
    message_count INTEGER NOT NULL DEFAULT 0,
    started_at    TEXT    NOT NULL,
    ended_at      TEXT
);

CREATE TABLE IF NOT EXISTS quiz_results (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id),
    topic      TEXT    NOT NULL,
    score      INTEGER NOT NULL,
    total      INTEGER NOT NULL,
    taken_at   TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS badges (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  INTEGER NOT NULL REFERENCES students(id),
    badge_name  TEXT    NOT NULL,
    description TEXT    NOT NULL DEFAULT '',
    earned_at   TEXT    NOT NULL,
    UNIQUE(student_id, badge_name)
);

CREATE TABLE IF NOT EXISTS dialect_logs (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    language                TEXT NOT NULL,
    raw_input               TEXT NOT NULL,
    detected_dialect_variant TEXT NOT NULL DEFAULT '',
    logged_at               TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS review_items (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id),
    topic      TEXT    NOT NULL DEFAULT '',
    front      TEXT    NOT NULL,
    back       TEXT    NOT NULL DEFAULT '',
    box        INTEGER NOT NULL DEFAULT 1,
    due_at     TEXT    NOT NULL,
    last_seen  TEXT    NOT NULL,
    UNIQUE(student_id, front)
);

CREATE TABLE IF NOT EXISTS conversation_turns (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT    NOT NULL,
    role            TEXT    NOT NULL,
    text            TEXT    NOT NULL,
    created_at      TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_conversation ON conversation_turns(conversation_id, id);
"""


def init_db() -> None:
    """Create all tables. Idempotent — safe to call on every app startup."""
    with _db() as conn:
        conn.executescript(_SCHEMA)
    log.info("Database initialised at '%s'.", DB_PATH)


# ---------------------------------------------------------------------------
# Students
# ---------------------------------------------------------------------------

def find_student_by_name(name: str) -> int | None:
    """Return student_id for *name* (case-insensitive), or None if not found."""
    with _db() as conn:
        row = conn.execute(
            "SELECT id FROM students WHERE lower(name) = lower(?) LIMIT 1",
            (name.strip(),),
        ).fetchone()
        return row["id"] if row else None


def get_or_create_student(name: str, language: str = "English", grade: int = 0) -> int:
    """
    Return the student_id for *name*, creating the record if it does not exist.
    Matching is case-insensitive on name.
    """
    with _db() as conn:
        row = conn.execute(
            "SELECT id FROM students WHERE lower(name) = lower(?) LIMIT 1",
            (name,),
        ).fetchone()

        if row:
            return row["id"]

        cur = conn.execute(
            "INSERT INTO students (name, language, grade, created_at) VALUES (?,?,?,?)",
            (name.strip(), language, grade, _now()),
        )
        return cur.lastrowid


# ---------------------------------------------------------------------------
# Sessions
# ---------------------------------------------------------------------------

def log_session(
    student_id: int,
    subject: str = "General",
    message_count: int = 0,
    started_at: str | None = None,
) -> None:
    """Record a completed chat session for a student."""
    now = _now()
    with _db() as conn:
        conn.execute(
            "INSERT INTO sessions (student_id, subject, message_count, started_at, ended_at)"
            " VALUES (?,?,?,?,?)",
            (student_id, subject, message_count, started_at or now, now),
        )
    check_and_award_badges(student_id)


# ---------------------------------------------------------------------------
# Quiz results
# ---------------------------------------------------------------------------

def log_quiz_result(student_id: int, topic: str, score: int, total: int) -> None:
    """Record a quiz attempt and evaluate badges."""
    with _db() as conn:
        conn.execute(
            "INSERT INTO quiz_results (student_id, topic, score, total, taken_at)"
            " VALUES (?,?,?,?,?)",
            (student_id, topic, score, total, _now()),
        )
    check_and_award_badges(student_id)


# ---------------------------------------------------------------------------
# Badges
# ---------------------------------------------------------------------------

# Badge definitions: name → (description, evaluator_fn(student_id, conn) -> bool)
def _has_first_step(student_id: int, conn: sqlite3.Connection) -> bool:
    row = conn.execute(
        "SELECT COUNT(*) AS n FROM sessions WHERE student_id=?", (student_id,)
    ).fetchone()
    return (row["n"] or 0) >= 1


def _has_quiz_ace(student_id: int, conn: sqlite3.Connection) -> bool:
    row = conn.execute(
        "SELECT COUNT(*) AS n FROM quiz_results"
        " WHERE student_id=? AND total>0 AND score=total",
        (student_id,),
    ).fetchone()
    return (row["n"] or 0) >= 1


def _has_week_warrior(student_id: int, conn: sqlite3.Connection) -> bool:
    rows = conn.execute(
        "SELECT DISTINCT substr(started_at, 1, 10) AS day"
        " FROM sessions WHERE student_id=?",
        (student_id,),
    ).fetchall()
    return len(rows) >= 7


def _has_dialect_pioneer(student_id: int, conn: sqlite3.Connection) -> bool:
    # Dialect pioneer: student has ≥10 non-English dialect_log entries.
    # dialect_logs are not student-scoped; proxy via sessions language.
    row = conn.execute(
        "SELECT language FROM students WHERE id=?", (student_id,)
    ).fetchone()
    if not row or row["language"].lower() == "english":
        return False
    # Check global dialect_logs count as a proxy (any non-English entries)
    dr = conn.execute(
        "SELECT COUNT(*) AS n FROM dialect_logs WHERE lower(language) != 'english'"
    ).fetchone()
    return (dr["n"] or 0) >= 10


_BADGE_RULES: list[tuple[str, str, object]] = [
    ("First Step",       "Completed your first session.",                    _has_first_step),
    ("Quiz Ace",         "Scored 100% on a quiz.",                           _has_quiz_ace),
    ("Week Warrior",     "Active on 7 or more different days.",              _has_week_warrior),
    ("Dialect Pioneer",  "Contributed 10+ entries in a local language.",     _has_dialect_pioneer),
]


def check_and_award_badges(student_id: int) -> list[str]:
    """
    Evaluate all badge rules for *student_id*.
    INSERT any newly earned badges (UNIQUE constraint prevents duplicates).
    Returns list of newly awarded badge names.
    """
    newly_awarded: list[str] = []

    with _db() as conn:
        existing = {
            row["badge_name"]
            for row in conn.execute(
                "SELECT badge_name FROM badges WHERE student_id=?", (student_id,)
            ).fetchall()
        }

        for badge_name, description, evaluator in _BADGE_RULES:
            if badge_name in existing:
                continue
            try:
                earned = evaluator(student_id, conn)
            except Exception as exc:  # noqa: BLE001
                log.warning("Badge '%s' evaluator error: %s", badge_name, exc)
                continue

            if earned:
                try:
                    conn.execute(
                        "INSERT OR IGNORE INTO badges"
                        " (student_id, badge_name, description, earned_at)"
                        " VALUES (?,?,?,?)",
                        (student_id, badge_name, description, _now()),
                    )
                    newly_awarded.append(badge_name)
                    log.info("Badge awarded: '%s' → student %d", badge_name, student_id)
                except Exception as exc:  # noqa: BLE001
                    log.warning("Could not insert badge '%s': %s", badge_name, exc)

    return newly_awarded


# ---------------------------------------------------------------------------
# Progress summary
# ---------------------------------------------------------------------------

def get_progress(student_id: int) -> dict:
    """
    Return a progress summary dict shaped to match the progress.html template:
    {
        "student":      {"name", "language", "last_active"},
        "sessions":     int,
        "badges":       ["Quiz Ace", ...],           # list of badge name strings
        "quiz_results": [{"topic", "score", "total", "pct", "created_at"}, ...],
    }
    """
    with _db() as conn:
        row = conn.execute(
            "SELECT name, language, created_at FROM students WHERE id=?",
            (student_id,),
        ).fetchone()
        last_session = conn.execute(
            "SELECT MAX(started_at) AS last_active FROM sessions WHERE student_id=?",
            (student_id,),
        ).fetchone()
        last_active = last_session["last_active"] if last_session else None
        student = dict(row) if row else {"name": None, "language": None, "created_at": None}
        student["last_active"] = last_active or student.get("created_at")

        badge_names = [
            r["badge_name"]
            for r in conn.execute(
                "SELECT badge_name FROM badges WHERE student_id=? ORDER BY earned_at DESC",
                (student_id,),
            ).fetchall()
        ]

        quizzes_raw = conn.execute(
            "SELECT topic, score, total, taken_at"
            " FROM quiz_results WHERE student_id=? ORDER BY taken_at DESC LIMIT 10",
            (student_id,),
        ).fetchall()
        quiz_results = []
        for qrow in quizzes_raw:
            pct = round(qrow["score"] / qrow["total"] * 100, 1) if qrow["total"] else 0.0
            quiz_results.append({
                "topic":      qrow["topic"],
                "score":      qrow["score"],
                "total":      qrow["total"],
                "pct":        pct,
                "created_at": qrow["taken_at"],
            })

        sessions = conn.execute(
            "SELECT COUNT(*) AS n FROM sessions WHERE student_id=?", (student_id,)
        ).fetchone()["n"]

    return {
        "student":      student,
        "sessions":     sessions,
        "badges":       badge_names,
        "quiz_results": quiz_results,
    }


# ---------------------------------------------------------------------------
# Dialect logging
# ---------------------------------------------------------------------------

def log_dialect(
    language: str,
    raw_input: str,
    dialect_variant: str = "",
) -> None:
    """Append a dialect log entry for research / model fine-tuning."""
    with _db() as conn:
        conn.execute(
            "INSERT INTO dialect_logs"
            " (language, raw_input, detected_dialect_variant, logged_at)"
            " VALUES (?,?,?,?)",
            (language, raw_input, dialect_variant, _now()),
        )

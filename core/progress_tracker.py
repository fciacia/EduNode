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

log_content_history(student_id, kind, topic, payload, subject, language, summary) -> int
    Save a generated quiz/deck/episode so it can be reopened later.

get_content_history(student_id, kind, limit) -> list[dict]
    Return recent history entries (list view — no payload) for (student, kind).

get_content_history_item(item_id, student_id) -> dict | None
    Return one history entry with its full payload, scoped to student_id.
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

CREATE TABLE IF NOT EXISTS audit_log (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    action    TEXT    NOT NULL,
    actor     TEXT    NOT NULL DEFAULT '',
    detail    TEXT    NOT NULL DEFAULT '',
    outcome   TEXT    NOT NULL DEFAULT 'ok',
    logged_at TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_audit_time ON audit_log(logged_at);

CREATE TABLE IF NOT EXISTS teachers (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    token      TEXT    NOT NULL UNIQUE,
    role       TEXT    NOT NULL DEFAULT 'teacher',
    created_at TEXT    NOT NULL
);

-- Per-student history of generated content (quiz/cards/slides/podcast), so a
-- student can reopen and replay something they made before instead of losing
-- it on refresh. `payload` is the exact JSON the generate endpoint returned,
-- so reopening an item feeds the page the same shape as a fresh generation.
CREATE TABLE IF NOT EXISTS content_history (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id),
    kind       TEXT    NOT NULL,   -- 'quiz' | 'cards' | 'slides' | 'podcast'
    topic      TEXT    NOT NULL,
    subject    TEXT    NOT NULL DEFAULT '',
    language   TEXT    NOT NULL DEFAULT 'English',
    summary    TEXT    NOT NULL DEFAULT '',   -- short list-view text, e.g. "4/5 (80%)"
    payload    TEXT    NOT NULL,              -- JSON blob of the generated content
    created_at TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_content_history ON content_history(student_id, kind, created_at);
"""

# Columns added after v1 — applied by _migrate() so existing hub DBs upgrade in place.
_MIGRATIONS = [
    ("students", "consent_status", "TEXT NOT NULL DEFAULT 'pending'"),
    ("students", "consent_by",     "TEXT NOT NULL DEFAULT ''"),
    ("students", "consent_at",     "TEXT NOT NULL DEFAULT ''"),
]


def _migrate(conn: sqlite3.Connection) -> None:
    for table, column, decl in _MIGRATIONS:
        cols = {r["name"] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()}
        if column not in cols:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")


def init_db() -> None:
    """Create all tables and apply migrations. Idempotent — safe on every startup."""
    with _db() as conn:
        conn.executescript(_SCHEMA)
        _migrate(conn)
    log.info("Database initialised at '%s'.", DB_PATH)


# ---------------------------------------------------------------------------
# Teachers (named identities — audit attributes to a person, not a shared token)
# ---------------------------------------------------------------------------

def register_teacher(name: str, token: str, role: str = "teacher") -> int:
    """Create/update a named teacher account keyed by their access token."""
    with _db() as conn:
        cur = conn.execute(
            "INSERT INTO teachers (name, token, role, created_at) VALUES (?,?,?,?)"
            " ON CONFLICT(token) DO UPDATE SET name=excluded.name, role=excluded.role",
            (name.strip(), token, role, _now()),
        )
        row = conn.execute("SELECT id FROM teachers WHERE token=?", (token,)).fetchone()
        return row["id"] if row else cur.lastrowid


def find_teacher_by_token(token: str) -> dict | None:
    """Return {name, role} for a token, or None. Used to attribute audit entries."""
    if not token:
        return None
    with _db() as conn:
        row = conn.execute(
            "SELECT name, role FROM teachers WHERE token=? LIMIT 1", (token,)
        ).fetchone()
        return dict(row) if row else None


# ---------------------------------------------------------------------------
# Parental consent (data governance — Issue 8)
# ---------------------------------------------------------------------------

def record_consent(student_id: int, granted: bool, recorded_by: str = "") -> None:
    """Record that parental/guardian consent was obtained (or denied) for a student.

    The consent itself is a real-world act (a parent signs a form); this stores the
    auditable record of who confirmed it and when."""
    with _db() as conn:
        conn.execute(
            "UPDATE students SET consent_status=?, consent_by=?, consent_at=? WHERE id=?",
            ("granted" if granted else "denied", recorded_by.strip(), _now(), student_id),
        )
    log_audit("record_consent", actor=recorded_by,
              detail=f"student={student_id} granted={granted}")


def get_consent(student_id: int) -> dict:
    """Return {status, by, at} for a student's consent record."""
    with _db() as conn:
        row = conn.execute(
            "SELECT consent_status, consent_by, consent_at FROM students WHERE id=?",
            (student_id,),
        ).fetchone()
    if not row:
        return {"status": "unknown", "by": "", "at": ""}
    return {"status": row["consent_status"], "by": row["consent_by"], "at": row["consent_at"]}


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
    name = name.strip()
    with _db() as conn:
        row = conn.execute(
            "SELECT id FROM students WHERE lower(name) = lower(?) LIMIT 1",
            (name,),
        ).fetchone()

        if row:
            return row["id"]

        cur = conn.execute(
            "INSERT INTO students (name, language, grade, created_at) VALUES (?,?,?,?)",
            (name, language, grade, _now()),
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
# Content history (quiz / cards / slides / podcast — reopen-and-replay)
# ---------------------------------------------------------------------------

_HISTORY_LIMIT_PER_STUDENT = 30  # keep the table small on constrained hub devices

def log_content_history(
    student_id: int,
    kind: str,
    topic: str,
    payload: dict,
    subject: str = "",
    language: str = "English",
    summary: str = "",
) -> int:
    """Save a generated quiz/deck/episode so the student can reopen it later.

    Also prunes older rows beyond _HISTORY_LIMIT_PER_STUDENT for this
    (student, kind) pair, oldest first, so history can't grow unbounded."""
    import json
    with _db() as conn:
        cur = conn.execute(
            "INSERT INTO content_history"
            " (student_id, kind, topic, subject, language, summary, payload, created_at)"
            " VALUES (?,?,?,?,?,?,?,?)",
            (student_id, kind, topic, subject, language, summary, json.dumps(payload), _now()),
        )
        new_id = cur.lastrowid
        conn.execute(
            "DELETE FROM content_history WHERE id IN ("
            "  SELECT id FROM content_history WHERE student_id=? AND kind=?"
            "  ORDER BY created_at DESC LIMIT -1 OFFSET ?"
            ")",
            (student_id, kind, _HISTORY_LIMIT_PER_STUDENT),
        )
        return new_id


def get_content_history(student_id: int, kind: str, limit: int = 20) -> list[dict]:
    """Return recent history entries for (student, kind), newest first, without
    the full payload (list view only — call get_content_history_item for the body)."""
    with _db() as conn:
        rows = conn.execute(
            "SELECT id, topic, subject, language, summary, created_at"
            " FROM content_history WHERE student_id=? AND kind=?"
            " ORDER BY created_at DESC LIMIT ?",
            (student_id, kind, limit),
        ).fetchall()
    return [dict(r) for r in rows]


def get_content_history_item(item_id: int, student_id: int) -> dict | None:
    """Return one history entry's full payload, scoped to student_id so a
    student can only reopen their own items."""
    import json
    with _db() as conn:
        row = conn.execute(
            "SELECT id, kind, topic, subject, language, summary, payload, created_at"
            " FROM content_history WHERE id=? AND student_id=?",
            (item_id, student_id),
        ).fetchone()
    if not row:
        return None
    d = dict(row)
    d["payload"] = json.loads(d["payload"])
    return d


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
        "badge_descriptions": {name: desc for name, desc, _ in _BADGE_RULES},
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


# ---------------------------------------------------------------------------
# Audit log (data governance — Issue 8)
# ---------------------------------------------------------------------------

def normalize_topic(topic: str) -> str:
    """Canonical key for a free-form quiz topic so 'Fractions', ' fractions ',
    and 'Adding  fractions' don't fragment a student's mastery into separate
    concepts. Collapses whitespace and lowercases for grouping (display keeps the
    original casing the caller chooses)."""
    return " ".join((topic or "").split()).lower()


# ---------------------------------------------------------------------------
# Retention & erasure (data governance — Issue 8)
# ---------------------------------------------------------------------------

_RETENTION_TABLES = [
    ("sessions", "started_at"),
    ("quiz_results", "taken_at"),
    ("conversation_turns", "created_at"),
    ("dialect_logs", "logged_at"),
    ("audit_log", "logged_at"),
]


def purge_older_than(days: int) -> dict:
    """Delete time-stamped records older than *days*. Returns rows removed per table.
    Supports a term-based retention policy run during routine maintenance."""
    from datetime import timedelta
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    removed: dict[str, int] = {}
    with _db() as conn:
        for table, col in _RETENTION_TABLES:
            cur = conn.execute(f"DELETE FROM {table} WHERE {col} < ?", (cutoff,))
            removed[table] = cur.rowcount
    log.info("Retention purge (>%d days): %s", days, removed)
    return removed


def delete_student(student_id: int) -> dict:
    """Right-to-erasure: remove a student and their personal records."""
    removed: dict[str, int] = {}
    with _db() as conn:
        for table in ("quiz_results", "sessions", "badges", "review_items"):
            cur = conn.execute(f"DELETE FROM {table} WHERE student_id=?", (student_id,))
            removed[table] = cur.rowcount
        cur = conn.execute("DELETE FROM students WHERE id=?", (student_id,))
        removed["students"] = cur.rowcount
    log.info("Deleted student %s: %s", student_id, removed)
    return removed


def log_audit(action: str, actor: str = "", detail: str = "", outcome: str = "ok") -> None:
    """Append an audit entry for a privileged action (admin/teacher access).

    Best-effort: never raise into the request path, so an audit-table problem
    can't take down an otherwise-valid action.
    """
    try:
        with _db() as conn:
            conn.execute(
                "INSERT INTO audit_log (action, actor, detail, outcome, logged_at)"
                " VALUES (?,?,?,?,?)",
                (str(action)[:120], str(actor)[:120], str(detail)[:500],
                 str(outcome)[:20], _now()),
            )
    except Exception as exc:  # noqa: BLE001
        log.warning("Audit log write failed (%s): %s", action, exc)


def get_audit_log(limit: int = 100) -> list[dict]:
    """Return the most recent audit entries (newest first)."""
    with _db() as conn:
        rows = conn.execute(
            "SELECT action, actor, detail, outcome, logged_at"
            "  FROM audit_log ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]

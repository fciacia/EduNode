"""Tests for retention purge and right-to-erasure (data governance, Gap 13)."""
from datetime import datetime, timedelta, timezone

import core.progress_tracker as pt


def _old_ts(days):
    return (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()


def test_purge_older_than_removes_stale_rows(temp_db):
    sid = pt.get_or_create_student("Ola")
    # One recent session, one old session (backdated directly).
    pt.log_session(sid, subject="Science")
    with pt._db() as conn:
        conn.execute(
            "INSERT INTO sessions (student_id, subject, message_count, started_at, ended_at)"
            " VALUES (?,?,?,?,?)",
            (sid, "Science", 1, _old_ts(120), _old_ts(120)),
        )

    removed = pt.purge_older_than(90)
    assert removed["sessions"] == 1
    with pt._db() as conn:
        remaining = conn.execute("SELECT COUNT(*) AS n FROM sessions").fetchone()["n"]
    assert remaining == 1                      # the recent one survives


def test_delete_student_erases_personal_records(temp_db):
    a = pt.get_or_create_student("Ana")
    b = pt.get_or_create_student("Ben")
    pt.log_quiz_result(a, "Fractions", 5, 10)
    pt.log_session(a, subject="Science")
    pt.log_quiz_result(b, "Fractions", 6, 10)

    removed = pt.delete_student(a)
    assert removed["students"] == 1
    assert removed["quiz_results"] == 1
    assert pt.find_student_by_name("Ana") is None
    assert pt.find_student_by_name("Ben") is not None      # others untouched


def test_normalize_topic():
    assert pt.normalize_topic("  Fractions ") == "fractions"
    assert pt.normalize_topic("Adding  Fractions") == "adding fractions"
    assert pt.normalize_topic("") == ""

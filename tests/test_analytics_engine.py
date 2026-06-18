"""Tests for the teacher analytics engine and dashboard endpoint (Issue 7)."""
import core.analytics_engine as an
import core.progress_tracker as pt


def test_overview_counts(temp_db):
    a = pt.get_or_create_student("Ali")
    b = pt.get_or_create_student("Bea")
    pt.log_session(a, subject="Science")
    pt.log_session(b, subject="Mathematics")
    pt.log_quiz_result(a, "Fractions", 4, 10)
    pt.log_quiz_result(b, "Fractions", 6, 10)

    o = an.class_overview()
    assert o["students"] == 2
    assert o["sessions"] == 2
    assert o["quiz_attempts"] == 2
    assert o["class_avg_pct"] == 50.0          # (4+6)/(10+10)
    assert o["active_today"] == 2


def test_overview_no_quizzes_avg_none(temp_db):
    pt.get_or_create_student("Solo")
    assert an.class_overview()["class_avg_pct"] is None


def test_most_missed_sorted_low_first(temp_db):
    a = pt.get_or_create_student("Ali")
    pt.log_quiz_result(a, "Hard", 1, 10)
    pt.log_quiz_result(a, "Easy", 9, 10)
    missed = an.most_missed_topics()
    assert missed[0]["topic"] == "Hard"
    assert missed[0]["avg_pct"] == 10.0
    assert missed[0]["students"] == 1


def test_activity_by_subject(temp_db):
    a = pt.get_or_create_student("Ali")
    pt.log_session(a, subject="Science")
    pt.log_session(a, subject="Science")
    pt.log_session(a, subject="Mathematics")
    rows = {r["subject"]: r["sessions"] for r in an.activity_by_subject()}
    assert rows["Science"] == 2
    assert rows["Mathematics"] == 1


def test_recent_flags_reads_jsonl(tmp_path, monkeypatch):
    f = tmp_path / "reports.jsonl"
    f.write_text('{"language":"Iban","note":"wrong word","ts":"t1"}\n'
                 '{"language":"Thai","note":"better term","ts":"t2"}\n', encoding="utf-8")
    monkeypatch.setattr(an, "TRANSLATION_REPORTS", f)
    flags = an.recent_flags()
    assert flags[0]["language"] == "Thai"      # most recent first
    assert len(flags) == 2


def test_recent_flags_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(an, "TRANSLATION_REPORTS", tmp_path / "nope.jsonl")
    assert an.recent_flags() == []


def test_teacher_endpoint_requires_token(temp_db, monkeypatch):
    monkeypatch.setattr("app.ADMIN_TOKEN", "secret")
    from app import app
    client = app.test_client()
    assert client.get("/api/teacher/analytics").status_code == 403
    r = client.get("/api/teacher/analytics?token=secret")
    assert r.status_code == 200
    assert "overview" in r.get_json()

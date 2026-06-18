"""Tests for the per-concept mastery model and adaptive recommendations (Issue 5)."""
import core.mastery_engine as me
import core.progress_tracker as pt


def test_no_history_returns_empty(temp_db):
    sid = pt.get_or_create_student("Ana")
    assert me.concept_mastery(sid) == []
    assert me.recommendations(sid) == []


def test_unknown_student_safe(temp_db):
    assert me.concept_mastery(None) == []
    assert me.recommendations(0) == []


def test_levels_classified(temp_db):
    sid = pt.get_or_create_student("Ben")
    pt.log_quiz_result(sid, "Fractions", 2, 10)        # 20% -> struggling
    pt.log_quiz_result(sid, "Photosynthesis", 7, 10)   # 70% -> developing
    pt.log_quiz_result(sid, "Place Value", 9, 10)      # 90% -> mastered

    mastery = {m["topic"]: m for m in me.concept_mastery(sid)}
    assert mastery["Fractions"]["level"] == "struggling"
    assert mastery["Photosynthesis"]["level"] == "developing"
    assert mastery["Place Value"]["level"] == "mastered"
    # sorted weakest-first
    assert me.concept_mastery(sid)[0]["topic"] == "Fractions"


def test_multiple_attempts_aggregate(temp_db):
    sid = pt.get_or_create_student("Cara")
    pt.log_quiz_result(sid, "Fractions", 2, 10)        # then improves
    pt.log_quiz_result(sid, "Fractions", 8, 10)
    m = me.concept_mastery(sid)
    assert len(m) == 1
    assert m[0]["attempts"] == 2
    assert m[0]["avg_pct"] == 50.0                      # (2+8)/(10+10)
    assert m[0]["level"] == "developing"


def test_recommendations_skip_mastered_and_limit(temp_db):
    sid = pt.get_or_create_student("Dee")
    pt.log_quiz_result(sid, "A", 1, 10)    # struggling
    pt.log_quiz_result(sid, "B", 6, 10)    # developing
    pt.log_quiz_result(sid, "C", 7, 10)    # developing
    pt.log_quiz_result(sid, "D", 10, 10)   # mastered -> excluded

    recs = me.recommendations(sid, limit=2)
    assert len(recs) == 2
    assert recs[0]["topic"] == "A"                      # weakest first
    assert recs[0]["action"] == "remedial lesson"
    assert recs[1]["action"] == "extra practice"
    topics = {r["topic"] for r in me.recommendations(sid, limit=10)}
    assert "D" not in topics                            # mastered excluded


def test_recommendations_api_by_name(temp_db):
    sid = pt.get_or_create_student("Evie")
    pt.log_quiz_result(sid, "Fractions", 1, 10)
    from app import app
    client = app.test_client()

    r = client.get("/api/recommendations/by-name/Evie")
    assert r.status_code == 200
    body = r.get_json()
    assert body["recommendations"][0]["topic"] == "Fractions"
    assert body["mastery"][0]["level"] == "struggling"

    assert client.get("/api/recommendations/by-name/Nobody").status_code == 404

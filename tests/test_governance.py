"""Tests for per-teacher identities + parental consent (Issue 8)."""
import core.progress_tracker as pt


# --- per-teacher identities ------------------------------------------------

def test_register_and_find_teacher(temp_db):
    tid = pt.register_teacher("Ms Tan", "tok-tan", role="teacher")
    assert tid
    t = pt.find_teacher_by_token("tok-tan")
    assert t == {"name": "Ms Tan", "role": "teacher"}
    assert pt.find_teacher_by_token("nope") is None


def test_register_teacher_upserts(temp_db):
    pt.register_teacher("Old Name", "tok-1")
    pt.register_teacher("New Name", "tok-1", role="admin")   # same token
    t = pt.find_teacher_by_token("tok-1")
    assert t == {"name": "New Name", "role": "admin"}


# --- parental consent ------------------------------------------------------

def test_consent_defaults_pending(temp_db):
    sid = pt.get_or_create_student("Budi")
    assert pt.get_consent(sid)["status"] == "pending"      # migration default


def test_record_consent(temp_db):
    sid = pt.get_or_create_student("Mai")
    pt.record_consent(sid, True, recorded_by="Ms Tan")
    c = pt.get_consent(sid)
    assert c["status"] == "granted" and c["by"] == "Ms Tan" and c["at"]
    pt.record_consent(sid, False, recorded_by="Ms Tan")
    assert pt.get_consent(sid)["status"] == "denied"


# --- audit attributes to a named teacher, not a token fingerprint ----------

def test_login_audit_uses_teacher_name(temp_db, monkeypatch):
    monkeypatch.setattr("app.ADMIN_TOKEN", "admintok")
    pt.register_teacher("Mr Lee", "lee-token")
    from app import app
    client = app.test_client()

    r = client.post("/api/admin/login", json={"token": "lee-token"})
    assert r.status_code == 200 and r.get_json()["actor"] == "Mr Lee"

    entries = pt.get_audit_log()
    assert any(e["actor"] == "Mr Lee" and e["action"] == "admin_login" for e in entries)


def test_teacher_token_authorises_protected_route(temp_db, monkeypatch):
    monkeypatch.setattr("app.ADMIN_TOKEN", "admintok")
    pt.register_teacher("Mr Lee", "lee-token")
    from app import app
    client = app.test_client()
    r = client.get("/api/teacher/analytics", headers={"X-Admin-Token": "lee-token"})
    assert r.status_code == 200


def test_consent_endpoint(temp_db, monkeypatch):
    monkeypatch.setattr("app.ADMIN_TOKEN", "admintok")
    sid = pt.get_or_create_student("Sara")
    from app import app
    client = app.test_client()
    r = client.post("/api/consent", json={"student_id": sid, "granted": True},
                    headers={"X-Admin-Token": "admintok"})
    assert r.status_code == 200
    assert r.get_json()["consent"]["status"] == "granted"

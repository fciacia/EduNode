"""Tests for the audit log and privileged-access logging (Issue 8)."""
import core.progress_tracker as pt


def test_log_and_read_audit(temp_db):
    pt.log_audit("test_action", actor="tok:abc123", detail="/api/thing", outcome="ok")
    pt.log_audit("other", actor="anonymous", detail="/api/x", outcome="denied")
    entries = pt.get_audit_log()
    assert entries[0]["action"] == "other"          # newest first
    assert entries[0]["outcome"] == "denied"
    assert entries[1]["action"] == "test_action"


def test_audit_write_never_raises(temp_db, monkeypatch):
    # Even if the DB layer breaks, audit logging must not raise into the request.
    def boom():
        raise RuntimeError("db down")
    monkeypatch.setattr(pt, "_db", boom)
    pt.log_audit("x")          # should swallow the error


def test_require_admin_logs_granted_and_denied(temp_db, monkeypatch):
    monkeypatch.setattr("app.ADMIN_TOKEN", "secret")
    from app import app
    client = app.test_client()

    client.get("/api/teacher/analytics")                  # denied
    client.get("/api/teacher/analytics?token=secret")     # granted

    entries = pt.get_audit_log()
    outcomes = {e["outcome"] for e in entries}
    assert "denied" in outcomes
    assert "ok" in outcomes
    # raw token must never appear in the audit log
    assert all("secret" not in e["actor"] for e in entries)


def test_audit_endpoint(temp_db, monkeypatch):
    monkeypatch.setattr("app.ADMIN_TOKEN", "secret")
    from app import app
    client = app.test_client()
    r = client.get("/api/audit?token=secret")
    assert r.status_code == 200
    assert "entries" in r.get_json()

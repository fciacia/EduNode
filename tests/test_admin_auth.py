"""Tests for admin token hardening: cookie login instead of URL token (Gap 11)."""


def _client(monkeypatch):
    monkeypatch.setattr("app.ADMIN_TOKEN", "secret")
    from app import app
    return app.test_client()


def test_login_rejects_bad_token(temp_db, monkeypatch):
    client = _client(monkeypatch)
    r = client.post("/api/admin/login", json={"token": "wrong"})
    assert r.status_code == 403
    assert "edge_admin" not in r.headers.get("Set-Cookie", "")


def test_login_sets_httponly_cookie(temp_db, monkeypatch):
    client = _client(monkeypatch)
    r = client.post("/api/admin/login", json={"token": "secret"})
    assert r.status_code == 200 and r.get_json()["ok"] is True
    setc = r.headers.get("Set-Cookie", "")
    assert "edge_admin=" in setc
    assert "HttpOnly" in setc


def test_cookie_authorises_without_url_token(temp_db, monkeypatch):
    client = _client(monkeypatch)
    # Before login: protected route is forbidden.
    assert client.get("/api/teacher/analytics").status_code == 403
    # Log in -> cookie stored on the test client.
    client.post("/api/admin/login", json={"token": "secret"})
    # Now the same client is authorised by cookie, no ?token in the URL.
    r = client.get("/api/teacher/analytics")
    assert r.status_code == 200
    assert "overview" in r.get_json()


def test_header_token_still_works(temp_db, monkeypatch):
    client = _client(monkeypatch)
    r = client.get("/api/teacher/analytics", headers={"X-Admin-Token": "secret"})
    assert r.status_code == 200

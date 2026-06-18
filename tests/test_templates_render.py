"""Server-side render guards for the new/updated pages (Gap 9).

These run without a browser (Flask test client). They don't execute JS, but they
catch the common breakage: a route that 500s, a template syntax error, a renamed
endpoint, or the admin token leaking back into a URL. Full in-browser JS e2e is
opt-in via EDGE_SMOKE (needs `playwright install`).
"""
import pytest


@pytest.fixture
def client(temp_db, monkeypatch):
    monkeypatch.setattr("app.ADMIN_TOKEN", "secret")
    from app import app
    return app.test_client()


def test_teacher_dashboard_renders(client):
    r = client.get("/teacher?token=secret")
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert 'id="kpiGrid"' in html
    assert "ensureAuth" in html                       # cookie-login wiring present
    assert "/api/teacher/analytics" in html
    # the analytics fetch must NOT carry the token in the URL anymore
    assert "analytics?token=" not in html


def test_admin_renders_with_cookie_wiring(client):
    r = client.get("/admin?token=secret")
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert "ensureAuth" in html
    assert "/api/admin/login" in html
    assert "ingest?token=" not in html                # token no longer in fetch URLs


def test_teacher_requires_auth(client):
    assert client.get("/teacher").status_code == 403


def test_progress_page_has_recommendations_wiring(client):
    r = client.get("/progress")
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert "loadRecommendations" in html
    assert "/api/recommendations/by-name/" in html


def test_chat_page_has_client_tts_offload(client):
    r = client.get("/chat")
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert "pickBrowserVoice" in html
    assert "speechSynthesis" in html

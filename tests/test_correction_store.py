"""Tests for the teacher translation correction loop (Issue 4)."""
import pytest

import core.correction_store as cs


@pytest.fixture
def temp_corrections(tmp_path, monkeypatch):
    monkeypatch.setattr(cs, "CORRECTIONS_PATH", tmp_path / "corrections.jsonl")
    return cs.CORRECTIONS_PATH


def test_save_and_list(temp_corrections):
    cs.save_correction("Iban", original="salah", corrected="betul", english="correct")
    rows = cs.list_corrections()
    assert len(rows) == 1
    assert rows[0]["language"] == "Iban"
    assert rows[0]["corrected"] == "betul"
    assert rows[0]["english"] == "correct"
    assert rows[0]["ts"]


def test_filter_by_language(temp_corrections):
    cs.save_correction("Iban", original="a", corrected="b")
    cs.save_correction("Cebuano", original="c", corrected="d")
    assert cs.count() == 2
    assert cs.count("Iban") == 1
    assert cs.list_corrections(language="cebuano")[0]["corrected"] == "d"


def test_requires_language_and_corrected(temp_corrections):
    with pytest.raises(ValueError):
        cs.save_correction("", original="x", corrected="y")
    with pytest.raises(ValueError):
        cs.save_correction("Iban", original="x", corrected="")


def test_most_recent_first(temp_corrections):
    cs.save_correction("Iban", original="1", corrected="first")
    cs.save_correction("Iban", original="2", corrected="second")
    assert cs.list_corrections()[0]["corrected"] == "second"


def test_correction_endpoints(tmp_path, monkeypatch):
    monkeypatch.setattr(cs, "CORRECTIONS_PATH", tmp_path / "corrections.jsonl")
    monkeypatch.setattr("app.ADMIN_TOKEN", "secret")
    from app import app
    client = app.test_client()

    # Unauthorized
    assert client.post("/api/translation/correct", json={}).status_code == 403

    # Missing required field -> 400
    bad = client.post("/api/translation/correct?token=secret",
                      json={"language": "", "corrected": ""})
    assert bad.status_code == 400

    ok = client.post("/api/translation/correct?token=secret",
                     json={"language": "Iban", "original": "salah", "corrected": "betul"})
    assert ok.status_code == 200 and ok.get_json()["ok"] is True

    listing = client.get("/api/translation/corrections?token=secret")
    assert listing.status_code == 200
    body = listing.get_json()
    assert body["count"] == 1
    assert body["corrections"][0]["corrected"] == "betul"

"""Test the translation-report endpoint logs a flag for teacher review."""
import json

from app import app


def test_report_appends_jsonl(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)                 # data/ is written relative to cwd
    client = app.test_client()
    r = client.post("/api/translation/report",
                    json={"language": "Thai", "shown": "บัตรคำ", "note": "wrong word"})
    assert r.status_code == 200 and r.get_json()["ok"] is True

    line = (tmp_path / "data" / "translation_reports.jsonl").read_text(encoding="utf-8").strip()
    entry = json.loads(line)
    assert entry["language"] == "Thai"
    assert entry["note"] == "wrong word"
    assert entry["ts"]

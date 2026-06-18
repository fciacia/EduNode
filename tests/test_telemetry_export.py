"""Tests for the offline telemetry export bundle (dialect flywheel sync)."""
import json

import core.telemetry_export as te
import core.correction_store as cs
import core.progress_tracker as pt


def test_build_bundle_aggregates(temp_db, tmp_path, monkeypatch):
    monkeypatch.setattr(cs, "CORRECTIONS_PATH", tmp_path / "corr.jsonl")
    import core.analytics_engine as an
    monkeypatch.setattr(an, "TRANSLATION_REPORTS", tmp_path / "flags.jsonl")

    sid = pt.get_or_create_student("Ana", language="Iban")
    pt.log_quiz_result(sid, "Fractions", 5, 10)
    pt.log_dialect("Iban", "nama berita")
    cs.save_correction("Iban", original="salah", corrected="betul")

    bundle = te.build_bundle()
    assert bundle["counts"]["corrections"] == 1
    assert bundle["counts"]["dialect_logs"] == 1
    assert bundle["usage"]["students"] == 1
    assert bundle["translation_corrections"][0]["corrected"] == "betul"
    # de-identified: no student names anywhere in the payload
    assert "Ana" not in json.dumps(bundle)


def test_write_bundle_has_checksum(temp_db, tmp_path, monkeypatch):
    monkeypatch.setattr(cs, "CORRECTIONS_PATH", tmp_path / "corr.jsonl")
    import core.analytics_engine as an
    monkeypatch.setattr(an, "TRANSLATION_REPORTS", tmp_path / "flags.jsonl")

    out = te.write_bundle(tmp_path / "export")
    assert out.exists()
    env = json.loads(out.read_text(encoding="utf-8"))
    assert "sha256" in env and "telemetry" in env
    # checksum matches the payload it wraps
    assert env["sha256"] == te._checksum(env["telemetry"])


def test_dialect_logs_safe_without_db(monkeypatch):
    def boom():
        raise RuntimeError("no db")
    monkeypatch.setattr(pt, "_db", boom)
    assert te._dialect_logs() == []

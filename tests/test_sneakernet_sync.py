"""Tests for the sneakernet sync enhancements: manifest deploy + telemetry."""
import json

import sneakernet_sync as sn
from tools import content_manifest as cm


def _write(d, name, text):
    (d / name).write_text(text, encoding="utf-8")


def test_apply_content_manifest_bootstraps_and_verifies(tmp_path):
    content = tmp_path / "curriculum"
    content.mkdir()
    _write(content, "math.txt", "fractions")
    usb = tmp_path / "usb"
    (usb / "new_curriculum").mkdir(parents=True)

    report = sn.apply_content_manifest(usb, content_dir=content)
    assert report["ok"] is True
    assert (content / cm.MANIFEST_NAME).exists()       # bootstrapped


def test_apply_content_manifest_merges_incoming(tmp_path):
    content = tmp_path / "curriculum"
    content.mkdir()
    _write(content, "math.txt", "fractions")
    usb = tmp_path / "usb"
    inc_dir = usb / "new_curriculum"
    inc_dir.mkdir(parents=True)

    # Incoming manifest declares a higher version from the ministry.
    incoming = cm.build_manifest(content, publisher="MoE", version=5)
    (inc_dir / cm.MANIFEST_NAME).write_text(json.dumps(incoming), encoding="utf-8")

    sn.apply_content_manifest(usb, content_dir=content)
    merged = cm.load_manifest(content)
    assert merged["files"]["math.txt"]["version"] == 5
    assert merged["files"]["math.txt"]["publisher"] == "MoE"


def test_apply_content_manifest_flags_tamper(tmp_path):
    content = tmp_path / "curriculum"
    content.mkdir()
    _write(content, "a.txt", "original")
    usb = tmp_path / "usb"
    (usb / "new_curriculum").mkdir(parents=True)

    sn.apply_content_manifest(usb, content_dir=content)   # bootstraps manifest
    _write(content, "a.txt", "TAMPERED")                  # change after manifest
    report = sn.apply_content_manifest(usb, content_dir=content)
    assert report["ok"] is False
    assert "a.txt" in report["changed"]
    # ENFORCED: the tampered file is quarantined out of the curriculum tree so it
    # is never ingested.
    assert "a.txt" in report["quarantined"]
    assert not (content / "a.txt").exists()
    assert (content.parent / "_quarantine" / "a.txt").exists()


def test_export_dialect_logs_matches_schema(tmp_path, monkeypatch):
    # Guards against the legacy export query drifting from the dialect_logs schema.
    # export_dialect_logs reads db/edunode.db relative to cwd, so build one there.
    import core.progress_tracker as pt
    work = tmp_path / "work"
    db_path = work / "db" / "edunode.db"
    db_path.parent.mkdir(parents=True)
    monkeypatch.setattr(pt, "DB_PATH", db_path)
    pt.init_db()
    pt.log_dialect("Iban", "nama berita", "coastal")

    monkeypatch.chdir(work)
    monkeypatch.setattr(sn, "_stamp", lambda: "TEST")
    usb = tmp_path / "usb"
    n = sn.export_dialect_logs(usb)

    assert n == 1
    out = json.loads((usb / "exported_reports" / "dialect_logs_TEST.json").read_text(encoding="utf-8"))
    assert out[0]["language"] == "Iban"
    assert out[0]["raw_input"] == "nama berita"
    assert out[0]["detected_dialect_variant"] == "coastal"


def test_capture_telemetry_writes_bundle(temp_db, tmp_path, monkeypatch):
    import core.correction_store as cs
    import core.analytics_engine as an
    monkeypatch.setattr(cs, "CORRECTIONS_PATH", tmp_path / "corr.jsonl")
    monkeypatch.setattr(an, "TRANSLATION_REPORTS", tmp_path / "flags.jsonl")
    cs.save_correction("Iban", original="salah", corrected="betul")

    usb = tmp_path / "usb"
    n = sn.capture_telemetry(usb)
    assert n == 1
    exports = list((usb / "exported_reports").glob("telemetry_*.json"))
    assert len(exports) == 1

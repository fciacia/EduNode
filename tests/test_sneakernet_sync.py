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

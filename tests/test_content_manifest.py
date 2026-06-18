"""Tests for the versioned content manifest (Issue 10)."""
from tools import content_manifest as cm


def _write(d, name, text):
    p = d / name
    p.write_text(text, encoding="utf-8")
    return p


def test_build_and_verify_ok(tmp_path):
    _write(tmp_path, "math.txt", "fractions")
    _write(tmp_path, "sci.txt", "photosynthesis")
    manifest = cm.build_manifest(tmp_path, publisher="MoE-MY", version=2)
    assert set(manifest["files"]) == {"math.txt", "sci.txt"}
    assert manifest["files"]["math.txt"]["publisher"] == "MoE-MY"
    assert manifest["files"]["math.txt"]["version"] == 2

    report = cm.verify(tmp_path, manifest)
    assert report["ok"] is True
    assert set(report["verified"]) == {"math.txt", "sci.txt"}


def test_verify_detects_tamper_missing_untracked(tmp_path):
    _write(tmp_path, "a.txt", "original")
    _write(tmp_path, "b.txt", "keep")
    manifest = cm.build_manifest(tmp_path, publisher="x")

    _write(tmp_path, "a.txt", "TAMPERED")        # checksum changes
    (tmp_path / "c.txt").write_text("new", encoding="utf-8")   # untracked
    manifest["files"]["gone.txt"] = {"sha256": "deadbeef", "version": 1}  # missing

    report = cm.verify(tmp_path, manifest)
    assert report["ok"] is False
    assert "a.txt" in report["changed"]
    assert "gone.txt" in report["missing"]
    assert "c.txt" in report["untracked"]


def test_merge_prefers_higher_version(tmp_path):
    _write(tmp_path, "shared.txt", "v1")
    local = cm.build_manifest(tmp_path, publisher="school", version=1)

    _write(tmp_path, "shared.txt", "v3")
    _write(tmp_path, "extra.txt", "added")
    incoming = cm.build_manifest(tmp_path, publisher="MoE", version=3)

    merged = cm.merge_manifests(local, incoming)
    assert merged["files"]["shared.txt"]["version"] == 3
    assert merged["files"]["shared.txt"]["publisher"] == "MoE"
    assert "extra.txt" in merged["files"]


def test_merge_keeps_local_when_newer(tmp_path):
    _write(tmp_path, "f.txt", "local-new")
    local = cm.build_manifest(tmp_path, publisher="school", version=5)
    incoming = cm.build_manifest(tmp_path, publisher="MoE", version=2)
    merged = cm.merge_manifests(local, incoming)
    assert merged["files"]["f.txt"]["version"] == 5
    assert merged["files"]["f.txt"]["publisher"] == "school"


def test_save_and_load_roundtrip(tmp_path):
    _write(tmp_path, "a.txt", "x")
    manifest = cm.build_manifest(tmp_path, publisher="p")
    cm.save_manifest(tmp_path, manifest)
    loaded = cm.load_manifest(tmp_path)
    assert loaded["files"]["a.txt"]["sha256"] == manifest["files"]["a.txt"]["sha256"]

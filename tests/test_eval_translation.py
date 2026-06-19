"""Tests for the translation-quality (chrF) harness (Gap 8)."""
from tools import eval_translation as et


def test_chrf_identical_is_100():
    assert et.chrf("rumah saya", "rumah saya") == 100.0


def test_chrf_disjoint_is_low():
    assert et.chrf("xxxxxx", "yyyyyy") == 0.0


def test_chrf_partial_overlap_between_0_and_100():
    s = et.chrf("rumah besar", "rumah kecil")
    assert 0.0 < s < 100.0


def test_chrf_empty_handling():
    assert et.chrf("", "") == 100.0
    assert et.chrf("abc", "") == 0.0


def test_native_segment_strips_bilingual_wrapper():
    # The bridge returns "[English] x\n[Iban] y" for display; score only the translation.
    out = et.native_segment("[English] dog\n[Iban] Uduk", "Iban")
    assert out == "Uduk"
    # plain output (no wrapper) is returned as-is
    assert et.native_segment("uduk", "Iban") == "uduk"


def test_native_segment_changes_chrf():
    # Scoring the wrapper tanks chrF; scoring the segment reflects the real translation.
    raw = "[English] dog\n[Iban] uduk"
    assert et.chrf(raw, "uduk") < et.chrf(et.native_segment(raw, "Iban"), "uduk")


def test_evaluate_aggregates_per_language():
    refs = [
        {"language": "Iban", "source_en": "my house", "reference": "rumah aku"},
        {"language": "Iban", "source_en": "big",      "reference": "besai"},
        {"language": "Thai", "source_en": "water",    "reference": "น้ำ"},
    ]
    # Stub translate: echo the reference for Iban (perfect), wrong for Thai.
    def fake_translate(src, lang):
        return {"my house": "rumah aku", "big": "besai"}.get(src, "zzz")

    out = et.evaluate(refs, fake_translate)
    assert out["summary"]["Iban"]["n"] == 2
    assert out["summary"]["Iban"]["mean_chrf"] == 100.0     # perfect match
    assert out["summary"]["Thai"]["mean_chrf"] < 40         # wrong output -> low


def test_load_references_from_corrections(tmp_path, monkeypatch):
    import core.correction_store as cs
    monkeypatch.setattr(cs, "CORRECTIONS_PATH", tmp_path / "corr.jsonl")
    cs.save_correction("Iban", original="salah", corrected="rumah", english="house")
    cs.save_correction("Iban", original="x", corrected="y")   # no english -> skipped
    refs = et.load_references()
    assert len(refs) == 1
    assert refs[0] == {"language": "Iban", "source_en": "house", "reference": "rumah"}

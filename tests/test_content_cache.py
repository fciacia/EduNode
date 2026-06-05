"""Tests for the offline generated-content cache."""
import core.content_cache as cc


def test_put_then_get_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr(cc, "CACHE_DIR", tmp_path)
    payload = {"questions": [{"q": 1}], "grounded": True}
    cc.put("quiz", "Science", "English", "primary", "Photosynthesis", payload)
    assert cc.get("quiz", "Science", "English", "primary", "Photosynthesis") == payload


def test_get_miss_returns_none(tmp_path, monkeypatch):
    monkeypatch.setattr(cc, "CACHE_DIR", tmp_path)
    assert cc.get("quiz", "Science", "English", "", "Nothing here") is None


def test_key_normalizes_topic_case_and_space(tmp_path, monkeypatch):
    monkeypatch.setattr(cc, "CACHE_DIR", tmp_path)
    cc.put("slides", "Science", "English", "", "Water Cycle", {"ok": 1})
    # Same topic, different case/whitespace -> same cache entry.
    assert cc.get("slides", "Science", "English", "", "  water cycle ") == {"ok": 1}


def test_kinds_and_levels_are_distinct(tmp_path, monkeypatch):
    monkeypatch.setattr(cc, "CACHE_DIR", tmp_path)
    cc.put("quiz", "Science", "English", "primary", "Atoms", {"a": 1})
    assert cc.get("quiz", "Science", "English", "secondary", "Atoms") is None
    assert cc.get("cards", "Science", "English", "primary", "Atoms") is None

"""Tests for schema-constrained slide generation."""
import core.llm_engine as llm
from core.slide_engine import generate_slides


SLIDES_OBJ = (
    '{"slides":['
    '{"title":"Photosynthesis","bullets":["Plants make food","Uses sunlight"],"notes":"Plants make their own food using sunlight."},'
    '{"title":"Summary","bullets":["Light to food"],"notes":"That is how plants feed themselves."}]}'
)


def test_generate_slides_parses_schema_object(monkeypatch):
    monkeypatch.setattr(llm, "_ollama_generate", lambda *a, **k: SLIDES_OBJ)
    slides = generate_slides("photosynthesis", "English", "")
    assert len(slides) == 2
    assert slides[0]["title"] == "Photosynthesis"
    assert slides[0]["bullets"] == ["Plants make food", "Uses sunlight"]
    assert slides[0]["notes"]


def test_generate_slides_passes_schema(monkeypatch):
    seen = {}
    def fake(prompt, temperature=0.7, max_tokens=512, system="", schema=None):
        seen["schema"] = schema
        return SLIDES_OBJ
    monkeypatch.setattr(llm, "_ollama_generate", fake)
    generate_slides("x", "English", "")
    assert isinstance(seen["schema"], dict)
    assert "slides" in seen["schema"]["properties"]


def test_generate_slides_empty_on_blank(monkeypatch):
    monkeypatch.setattr(llm, "_ollama_generate", lambda *a, **k: "")
    assert generate_slides("x", "English", "") == []


def test_generate_slides_skips_invalid_items(monkeypatch):
    raw = '{"slides":[{"title":"","bullets":["x"]},{"title":"Good","bullets":["a","b"],"notes":"n"}]}'
    monkeypatch.setattr(llm, "_ollama_generate", lambda *a, **k: raw)
    slides = generate_slides("x", "English", "")
    assert len(slides) == 1
    assert slides[0]["title"] == "Good"

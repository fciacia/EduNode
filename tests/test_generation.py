"""Tests for schema-constrained quiz/flashcard generation and Ollama health."""
import core.llm_engine as llm
from core.llm_engine import generate_quiz
from core.flashcard_engine import generate_flashcards


# --- quiz: schema-mode output is a JSON object {"questions": [...]} ----------
QUIZ_OBJ = (
    '{"questions":['
    '{"question":"Q1?","options":["A. a","B. b","C. c","D. d"],"answer":"B","explanation":"because b"},'
    '{"question":"Q2?","options":["A. a","B. b","C. c","D. d"],"answer":"A"}]}'
)


def test_generate_quiz_parses_schema_object(monkeypatch):
    monkeypatch.setattr(llm, "_ollama_generate", lambda *a, **k: QUIZ_OBJ)
    qs = generate_quiz("x", "English", "")
    assert len(qs) == 2
    assert qs[0]["answer"] == "B"
    assert len(qs[0]["options"]) == 4
    assert qs[0]["explanation"] == "because b"
    assert qs[1]["explanation"] == ""          # missing -> empty, not KeyError


def test_generate_quiz_passes_level_hint_to_prompt(monkeypatch):
    seen = {}
    def fake(prompt, temperature=0.7, max_tokens=512, system="", schema=None):
        seen["system"] = system
        return QUIZ_OBJ
    monkeypatch.setattr(llm, "_ollama_generate", fake)
    generate_quiz("x", "English", "", level="primary")
    assert "primary school" in seen["system"]


def test_generate_quiz_passes_schema_to_model(monkeypatch):
    seen = {}
    def fake(prompt, temperature=0.7, max_tokens=512, system="", schema=None):
        seen["schema"] = schema
        return QUIZ_OBJ
    monkeypatch.setattr(llm, "_ollama_generate", fake)
    generate_quiz("x", "English", "")
    assert isinstance(seen["schema"], dict)        # schema was supplied
    assert "questions" in seen["schema"]["properties"]


def test_generate_quiz_fallback_array_in_prose(monkeypatch):
    # Model ignored schema and wrapped a bare array in prose/markdown.
    raw = 'Sure!\n```json\n[{"question":"Q?","options":["A.a","B.b","C.c","D.d"],"answer":"A"}]\n```'
    monkeypatch.setattr(llm, "_ollama_generate", lambda *a, **k: raw)
    qs = generate_quiz("x", "English", "")
    assert len(qs) == 1


def test_generate_quiz_empty_on_blank(monkeypatch):
    monkeypatch.setattr(llm, "_ollama_generate", lambda *a, **k: "")
    assert generate_quiz("x", "English", "") == []


# --- flashcards -------------------------------------------------------------
def test_generate_flashcards_parses_schema_object(monkeypatch):
    obj = '{"flashcards":[{"title":"T","body":"B","image":null},{"title":"T2","body":"B2"}]}'
    monkeypatch.setattr("core.llm_engine._ollama_generate", lambda *a, **k: obj)
    cards = generate_flashcards("x", "English", "")
    assert len(cards) == 2
    assert cards[0]["title"] == "T"
    assert cards[0]["image"] is None


# --- ollama health ----------------------------------------------------------
def test_ollama_available_true(monkeypatch):
    class R:
        status_code = 200
    monkeypatch.setattr("requests.get", lambda *a, **k: R())
    assert llm.ollama_available() is True


def test_ollama_available_false_on_error(monkeypatch):
    def boom(*a, **k):
        raise OSError("connection refused")
    monkeypatch.setattr("requests.get", boom)
    assert llm.ollama_available() is False

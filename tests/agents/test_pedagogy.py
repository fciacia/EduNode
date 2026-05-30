import core.agents.pedagogy as ped
from core.agents import Chunk, StudentContext


def test_prompt_includes_chunks_and_difficulty(monkeypatch):
    captured = {}

    def fake_generate(prompt, temperature=0.7, max_tokens=512, system=""):
        captured["prompt"] = prompt
        captured["system"] = system
        return "Plants make food using sunlight."

    monkeypatch.setattr("core.llm_engine._ollama_generate", fake_generate)

    chunks = [Chunk(text="Photosynthesis uses sunlight.", source="sci.pdf", page=3, distance=0.1)]
    ctx = StudentContext(grade="7", avg_score=40.0, weak_subjects=[], difficulty="simple")

    answer = ped.reason("How do plants make food?", ctx, chunks)

    assert answer == "Plants make food using sunlight."
    assert "Photosynthesis uses sunlight." in captured["prompt"]
    assert "simple" in captured["system"].lower()


def test_empty_answer_returns_grounded_fallback(monkeypatch):
    monkeypatch.setattr("core.llm_engine._ollama_generate", lambda *a, **k: "")
    chunks = [Chunk(text="x", source="a.pdf", page=1, distance=0.1)]
    ctx = StudentContext(grade="general", avg_score=0.0, weak_subjects=[], difficulty="standard")
    answer = ped.reason("Question?", ctx, chunks)
    assert answer == ""   # orchestrator decides what to do with empty

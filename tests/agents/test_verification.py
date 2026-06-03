import numpy as np

import core.agents.verification as ver
from core.agents import Chunk, Verification


def _fake_embedder(vectors_by_text):
    """Return an object with .encode(list[str]) -> np.ndarray matching a lookup."""
    class _E:
        def encode(self, texts):
            return np.array([vectors_by_text[t] for t in texts], dtype=float)
    return _E()


def test_grounded_answer_has_high_confidence(monkeypatch):
    answer = "Plants make food from sunlight."
    chunk_text = "Photosynthesis lets plants make food from sunlight."
    vecs = {answer: [1.0, 0.0, 0.0], chunk_text: [0.96, 0.28, 0.0]}
    monkeypatch.setattr(ver, "_get_embedder", lambda: _fake_embedder(vecs))
    monkeypatch.setattr(ver, "_llm_verify", lambda a, c: None)   # embedding-only

    chunks = [Chunk(text=chunk_text, source="sci.pdf", page=4, distance=0.1)]
    result = ver.score(answer, chunks)

    assert isinstance(result, Verification)
    assert result.confidence >= 0.85
    assert result.needs_review is False
    assert {"source": "sci.pdf", "page": 4} in result.citations


def test_offtopic_answer_flags_review(monkeypatch):
    answer = "The capital of France is Paris."
    chunk_text = "Photosynthesis lets plants make food from sunlight."
    vecs = {answer: [0.0, 1.0, 0.0], chunk_text: [1.0, 0.0, 0.0]}
    monkeypatch.setattr(ver, "_get_embedder", lambda: _fake_embedder(vecs))
    monkeypatch.setattr(ver, "_llm_verify", lambda a, c: None)

    chunks = [Chunk(text=chunk_text, source="sci.pdf", page=4, distance=0.8)]
    result = ver.score(answer, chunks)

    assert result.confidence < 0.85
    assert result.needs_review is True


def test_no_chunks_zero_confidence(monkeypatch):
    monkeypatch.setattr(ver, "_get_embedder", lambda: _fake_embedder({}))
    result = ver.score("anything", [])
    assert result.confidence == 0.0
    assert result.needs_review is True
    assert result.citations == []


def test_llm_check_lowers_confidence_of_unsupported_answer(monkeypatch):
    # Embeddings look fine, but the LLM self-check says "not supported" -> review.
    answer = "Plants make food from sunlight."
    chunk_text = "Photosynthesis lets plants make food from sunlight."
    vecs = {answer: [1.0, 0.0, 0.0], chunk_text: [0.96, 0.28, 0.0]}
    monkeypatch.setattr(ver, "_get_embedder", lambda: _fake_embedder(vecs))
    monkeypatch.setattr(ver, "_llm_verify", lambda a, c: 0.2)    # model: weakly supported

    chunks = [Chunk(text=chunk_text, source="sci.pdf", page=4, distance=0.1)]
    result = ver.score(answer, chunks)
    assert result.confidence < 0.85          # blended down by the LLM check
    assert result.needs_review is True


def test_llm_verify_parses_schema_output(monkeypatch):
    monkeypatch.setenv("EDGE_LLM_VERIFY", "1")
    monkeypatch.setattr("core.llm_engine._ollama_generate",
                        lambda *a, **k: '{"supported": false, "confidence": 0.9}')
    # supported=false caps confidence at 0.4 regardless of the reported number
    assert ver._llm_verify("ans", [Chunk("t", "s", 1, 0.1)]) == 0.4


def test_llm_verify_disabled_returns_none(monkeypatch):
    monkeypatch.setenv("EDGE_LLM_VERIFY", "0")
    assert ver._llm_verify("ans", [Chunk("t", "s", 1, 0.1)]) is None

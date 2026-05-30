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

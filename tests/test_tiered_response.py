"""Tests for the tiered response strategy in the orchestrator.

Three tiers based on best retrieval distance:
  - grounded      (distance <= GROUNDED_GATE)        -> curriculum-grounded answer
  - supplementary (GROUNDED_GATE < d <= SUPP_GATE)   -> labelled general-knowledge answer
  - none          (distance > SUPP_GATE)             -> controlled non-response
"""
import core.agents.orchestrator as orch
from core.agents import Chunk, Verification


def _chunks(distance: float):
    return [Chunk(text="Plants make food from sunlight.", source="science.txt",
                  page=1, distance=distance)]


def _patch_common(monkeypatch):
    """Stub out translation, context, history and verification (no models in tests)."""
    monkeypatch.setattr(orch, "_translate_in", lambda q, lang: q)
    monkeypatch.setattr(orch, "_translate_out", lambda a, lang: a)

    import core.agents.context as context_agent
    from core.agents import StudentContext
    monkeypatch.setattr(context_agent, "build",
                        lambda sid: StudentContext(grade="6", avg_score=0.0))

    import core.conversation as conv
    monkeypatch.setattr(conv, "get_history", lambda cid: [])
    monkeypatch.setattr(conv, "append_turn", lambda *a, **k: None)

    import core.agents.verification as verification
    monkeypatch.setattr(verification, "score",
                        lambda ans, chunks: Verification(confidence=0.9, citations=[
                            {"source": "science.txt", "page": 1}], needs_review=False))


def test_grounded_tier(monkeypatch):
    _patch_common(monkeypatch)
    import core.rag_engine as rag
    monkeypatch.setattr(rag, "retrieve_with_citations",
                        lambda q, n_results=3, subject=None: _chunks(0.40))
    import core.agents.pedagogy as ped
    monkeypatch.setattr(ped, "reason", lambda *a, **k: "Plants make food via photosynthesis.")

    out = orch.run_pipeline("How do plants eat?", "English", student_id=None)
    assert out["tier"] == "grounded"
    assert out["citations"]
    assert out["confidence"] > 0


def test_supplementary_tier(monkeypatch):
    _patch_common(monkeypatch)
    import core.rag_engine as rag
    # near-miss distance: above grounded gate, below supplementary gate
    near = (orch.GROUNDED_GATE + orch.SUPPLEMENTARY_GATE) / 2
    monkeypatch.setattr(rag, "retrieve_with_citations",
                        lambda q, n_results=3, subject=None: _chunks(near))
    import core.agents.pedagogy as ped
    called = {}

    def fake_supp(*a, **k):
        called["supp"] = True
        return "A rainbow forms when light bends through raindrops."
    monkeypatch.setattr(ped, "reason_supplementary", fake_supp)
    monkeypatch.setattr(ped, "reason", lambda *a, **k: "should not be called")

    out = orch.run_pipeline("Why are rainbows curved?", "English", student_id=None)
    assert called.get("supp") is True
    assert out["tier"] == "supplementary"
    assert out["needs_review"] is True
    assert "textbook" in out["answer"].lower()      # labelled as supplementary
    assert out["citations"] == []                   # not grounded in curriculum


def test_supplementary_can_be_disabled(monkeypatch):
    _patch_common(monkeypatch)
    monkeypatch.setattr(orch, "SUPPLEMENTARY_ENABLED", False)
    import core.rag_engine as rag
    near = (orch.GROUNDED_GATE + orch.SUPPLEMENTARY_GATE) / 2
    monkeypatch.setattr(rag, "retrieve_with_citations",
                        lambda q, n_results=3, subject=None: _chunks(near))
    import core.agents.pedagogy as ped
    monkeypatch.setattr(ped, "reason_supplementary",
                        lambda *a, **k: "should not be called")

    out = orch.run_pipeline("Why are rainbows curved?", "English", student_id=None)
    assert out["tier"] == "none"            # falls through to controlled non-response


def test_non_response_tier(monkeypatch):
    _patch_common(monkeypatch)
    import core.rag_engine as rag
    monkeypatch.setattr(rag, "retrieve_with_citations",
                        lambda q, n_results=3, subject=None: _chunks(0.98))

    out = orch.run_pipeline("What is the capital of Mars?", "English", student_id=None)
    assert out["tier"] == "none"
    assert out["confidence"] == 0.0
    assert out["citations"] == []

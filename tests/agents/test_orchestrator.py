import core.agents.orchestrator as orch
from core.agents import Chunk, StudentContext, Verification


def _patch_all(monkeypatch, *, chunks, reason_called):
    monkeypatch.setattr(orch, "_translate_in", lambda q, lang: q)
    monkeypatch.setattr(orch, "_translate_out", lambda a, lang: a)
    monkeypatch.setattr(
        "core.agents.context.build",
        lambda sid: StudentContext(grade="7", avg_score=0.0, weak_subjects=[], difficulty="standard"),
    )
    monkeypatch.setattr("core.rag_engine.retrieve_with_citations", lambda q, n_results, subject: chunks)

    def fake_reason(q, ctx, ch, history=None):
        reason_called.append(True)
        return "An answer grounded in curriculum."
    monkeypatch.setattr("core.agents.pedagogy.reason", fake_reason)

    monkeypatch.setattr(
        "core.agents.verification.score",
        lambda ans, ch: Verification(confidence=0.92, citations=[{"source": "a.pdf", "page": 2}], needs_review=False),
    )


def test_happy_path_returns_full_payload(monkeypatch):
    reason_called = []
    chunks = [Chunk(text="grounded text", source="a.pdf", page=2, distance=0.2)]
    _patch_all(monkeypatch, chunks=chunks, reason_called=reason_called)

    result = orch.run_pipeline("How do plants grow?", "English", student_id=1, subject="Science")

    assert reason_called == [True]
    assert result["answer"] == "An answer grounded in curriculum."
    assert result["confidence"] == 0.92
    assert result["needs_review"] is False
    assert result["citations"] == [{"source": "a.pdf", "page": 2}]
    assert result["language"] == "English"


def test_conversation_memory_feeds_and_records_history(monkeypatch, temp_db):
    import core.conversation as conv
    reason_called = []
    chunks = [Chunk(text="grounded text", source="a.pdf", page=2, distance=0.2)]
    _patch_all(monkeypatch, chunks=chunks, reason_called=reason_called)

    captured = {}
    def fake_reason(q, ctx, ch, history=None):
        captured["history"] = list(history or [])
        return "Photosynthesis makes food."
    monkeypatch.setattr("core.agents.pedagogy.reason", fake_reason)

    # First turn: no prior history; the exchange is recorded afterwards.
    orch.run_pipeline("What is photosynthesis?", "English", student_id=1, conversation_id="c1")
    assert captured["history"] == []
    assert [t["role"] for t in conv.get_history("c1")] == ["user", "assistant"]

    # Second turn: the first exchange is now visible to the pedagogy agent.
    orch.run_pipeline("Tell me more", "English", student_id=1, conversation_id="c1")
    assert any("photosynthesis" in t["text"].lower() for t in captured["history"])


def test_verification_gate_threads_needs_review(monkeypatch):
    # Pipeline runs to completion but confidence is below 0.85 -> amber badge.
    reason_called = []
    chunks = [Chunk(text="grounded text", source="a.pdf", page=2, distance=0.2)]
    _patch_all(monkeypatch, chunks=chunks, reason_called=reason_called)
    # Override verification to return a low-confidence, needs_review result.
    monkeypatch.setattr(
        "core.agents.verification.score",
        lambda ans, ch: Verification(confidence=0.70, citations=[{"source": "a.pdf", "page": 2}], needs_review=True),
    )

    result = orch.run_pipeline("How do plants grow?", "English", student_id=1, subject="Science")

    assert reason_called == [True]                 # generation DID run
    assert result["answer"] == "An answer grounded in curriculum."
    assert result["confidence"] == 0.70
    assert result["needs_review"] is True
    assert result["citations"] == [{"source": "a.pdf", "page": 2}]


def test_retrieval_gate_blocks_generation(monkeypatch):
    reason_called = []
    # Best distance 0.9 > SUPPLEMENTARY_GATE (0.85) -> non-response, reason() never called
    chunks = [Chunk(text="weak match", source="a.pdf", page=1, distance=0.9)]
    _patch_all(monkeypatch, chunks=chunks, reason_called=reason_called)

    result = orch.run_pipeline("Unrelated question?", "English", student_id=1, subject="Science")

    assert reason_called == []                 # generation skipped
    assert result["confidence"] == 0.0
    assert result["needs_review"] is True
    assert result["citations"] == []
    assert "don't have" in result["answer"].lower() or "do not have" in result["answer"].lower()


def test_clear_question_grounds_despite_offtopic_history(monkeypatch, temp_db):
    # Off-topic history must not drag a clear, in-curriculum question over the
    # gate: the bare question retrieves a close chunk even though the
    # history-augmented query retrieves a far one.
    import core.conversation as conv
    conv.append_turn("c3", "user", "what is 12 times 8")

    reason_called = []
    _patch_all(monkeypatch, chunks=[], reason_called=reason_called)
    close = [Chunk(text="The water cycle…", source="sci.txt", page=1, distance=0.4)]
    far   = [Chunk(text="off topic",       source="x.txt",   page=1, distance=0.9)]
    monkeypatch.setattr(
        "core.rag_engine.retrieve_with_citations",
        lambda q, n_results, subject: (far if "12 times 8" in q else close),
    )

    result = orch.run_pipeline("explain the water cycle", "English", student_id=1,
                               subject="Science", conversation_id="c3")
    assert reason_called == [True]                      # grounded, not blocked
    assert result["citations"] == [{"source": "a.pdf", "page": 2}]


def test_subject_mismatch_falls_back_to_all_subjects(monkeypatch):
    # Asking a science question while "Mathematics" is selected must still
    # ground: the subject-filtered search misses, the all-subjects retry hits.
    reason_called = []
    _patch_all(monkeypatch, chunks=[], reason_called=reason_called)
    miss = [Chunk(text="math stuff", source="m.txt", page=1, distance=0.9)]
    hit  = [Chunk(text="Digestion…", source="sci.txt", page=1, distance=0.3)]
    monkeypatch.setattr(
        "core.rag_engine.retrieve_with_citations",
        lambda q, n_results, subject: hit if subject in ("", "General") else miss,
    )

    result = orch.run_pipeline("How does digestion work?", "English", student_id=1,
                               subject="Mathematics")
    assert reason_called == [True]                      # grounded via fallback
    assert result["citations"] == [{"source": "a.pdf", "page": 2}]


def test_no_chunks_returns_non_response(monkeypatch):
    reason_called = []
    _patch_all(monkeypatch, chunks=[], reason_called=reason_called)
    result = orch.run_pipeline("Anything?", "English", student_id=1, subject="General")
    assert reason_called == []
    assert result["needs_review"] is True

import core.llm_engine as llm


def test_query_tutor_delegates_to_pipeline(monkeypatch):
    captured = {}

    def fake_pipeline(query, language, student_id, subject="General"):
        captured["args"] = (query, language, student_id, subject)
        return {"answer": "hi", "confidence": 0.9, "citations": [], "needs_review": False, "language": language}

    monkeypatch.setattr("core.agents.orchestrator.run_pipeline", fake_pipeline)

    out = llm.query_tutor("Hello?", "English", student_id=5, subject="Science")
    assert out["answer"] == "hi"
    assert out["confidence"] == 0.9
    assert captured["args"] == ("Hello?", "English", 5, "Science")

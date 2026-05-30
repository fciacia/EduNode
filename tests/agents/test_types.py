from core.agents import Chunk, StudentContext, Verification


def test_chunk_holds_citation_fields():
    c = Chunk(text="Water boils at 100C.", source="science.pdf", page=12, distance=0.2)
    assert c.source == "science.pdf"
    assert c.page == 12
    assert c.distance == 0.2


def test_student_context_defaults():
    ctx = StudentContext(grade="7", avg_score=82.0, weak_subjects=["Mathematics"], difficulty="standard")
    assert ctx.difficulty == "standard"
    assert "Mathematics" in ctx.weak_subjects


def test_verification_needs_review_flag():
    v = Verification(confidence=0.5, citations=[{"source": "a.pdf", "page": 1}], needs_review=True)
    assert v.needs_review is True
    assert v.citations[0]["page"] == 1

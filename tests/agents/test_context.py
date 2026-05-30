import core.agents.context as ctx_agent
from core.agents import StudentContext


def test_missing_student_returns_safe_defaults(temp_db):
    ctx = ctx_agent.build(student_id=9999)   # no such student
    assert isinstance(ctx, StudentContext)
    assert ctx.grade == "general"
    assert ctx.difficulty == "standard"


def test_low_average_yields_simple_difficulty(temp_db):
    import core.progress_tracker as pt
    sid = pt.get_or_create_student("Ana", "English", grade=7)
    pt.log_quiz_result(sid, "Fractions", score=2, total=10)   # 20%
    ctx = ctx_agent.build(sid)
    assert ctx.difficulty == "simple"
    assert ctx.grade == "7"


def test_high_average_yields_challenge_difficulty(temp_db):
    import core.progress_tracker as pt
    sid = pt.get_or_create_student("Ben", "English", grade=8)
    pt.log_quiz_result(sid, "Algebra", score=9, total=10)   # 90%
    ctx = ctx_agent.build(sid)
    assert ctx.difficulty == "challenge"

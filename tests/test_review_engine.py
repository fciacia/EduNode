"""Tests for Leitner spaced-repetition (review_engine)."""
import core.review_engine as rev
from core.progress_tracker import get_or_create_student


def test_review_again_is_due_now(temp_db):
    sid = get_or_create_student("Ana", "English")
    rev.save_review(sid, "Fractions", "What is a numerator?", "Top number", "review")
    assert rev.count_due(sid) == 1
    due = rev.get_due(sid)
    assert due[0]["front"] == "What is a numerator?"
    assert due[0]["box"] == 1


def test_known_advances_box_and_not_due_now(temp_db):
    sid = get_or_create_student("Ben", "English")
    rev.save_review(sid, "Fractions", "What is a denominator?", "Bottom number", "known")
    # box 1 -> 2, due tomorrow -> not due now
    assert rev.count_due(sid) == 0
    assert rev.get_due(sid) == []


def test_known_then_review_resets_box(temp_db):
    sid = get_or_create_student("Cam", "English")
    rev.save_review(sid, "T", "card", "ans", "known")   # box 2
    rev.save_review(sid, "T", "card", "ans", "known")   # box 3
    rev.save_review(sid, "T", "card", "ans", "review")  # reset to box 1, due now
    due = rev.get_due(sid)
    assert len(due) == 1
    assert due[0]["box"] == 1


def test_same_card_not_duplicated(temp_db):
    sid = get_or_create_student("Dee", "English")
    rev.save_review(sid, "T", "card", "ans", "review")
    rev.save_review(sid, "T", "card", "ans2", "review")
    due = rev.get_due(sid)
    assert len(due) == 1
    assert due[0]["back"] == "ans2"   # upsert updated the back


def test_blank_front_ignored(temp_db):
    sid = get_or_create_student("Eve", "English")
    rev.save_review(sid, "T", "  ", "ans", "review")
    assert rev.count_due(sid) == 0

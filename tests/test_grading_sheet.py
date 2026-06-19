"""Tests for the human-grading sheet scorer (Issue 2)."""
import csv

from tools import score_grading_sheet as sc
from tools import make_grading_sheet as mk


def _write_csv(path, rows, cols):
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def test_score_strict_and_lenient():
    grades = {"a": "correct", "b": "correct", "c": "partial", "d": "wrong"}
    s = sc.score(grades)
    assert s["graded"] == 4 and s["correct"] == 2
    assert s["accuracy_strict"] == 0.5                      # 2/4
    assert s["accuracy_lenient"] == 0.625                   # (2 + 0.5)/4


def test_load_grades_ignores_blank_and_invalid(tmp_path):
    p = tmp_path / "g.csv"
    _write_csv(p, [
        {"id": "a", "grade": "correct"},
        {"id": "b", "grade": ""},          # ungraded -> skipped
        {"id": "c", "grade": "maybe"},     # invalid -> skipped
    ], ["id", "grade"])
    g = sc.load_grades(p)
    assert g == {"a": "correct"}


def test_agreement_perfect_and_kappa():
    g1 = {"a": "correct", "b": "wrong", "c": "partial"}
    a = sc.agreement(g1, dict(g1))
    assert a["raw_agreement"] == 1.0
    assert a["cohen_kappa"] == 1.0


def test_agreement_partial():
    g1 = {"a": "correct", "b": "correct", "c": "wrong", "d": "wrong"}
    g2 = {"a": "correct", "b": "wrong", "c": "wrong", "d": "wrong"}
    a = sc.agreement(g1, g2)
    assert a["shared"] == 4
    assert a["raw_agreement"] == 0.75


def test_make_sheet_html_and_csv_shapes(tmp_path):
    rows = [
        {"id": "q1", "subject": "Math", "question": "What is 2+2?",
         "answer": "Four.", "tier": "grounded", "expected_keywords": "four", "grade": ""},
    ]
    csv_path = tmp_path / "g.csv"
    html_path = tmp_path / "g.html"
    mk.write_csv(rows, csv_path)
    mk.write_html(rows, html_path)
    # CSV round-trips with the grade column present and empty
    back = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    assert back[0]["id"] == "q1" and back[0]["grade"] == ""
    # HTML carries the question, answer and three radio options
    h = html_path.read_text(encoding="utf-8")
    assert "What is 2+2?" in h and 'value="correct"' in h and 'value="wrong"' in h

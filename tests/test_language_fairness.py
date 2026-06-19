"""Tests for the pure logic of the language-fairness eval (Issue 9/4)."""
from tools import eval_language_fairness as lf


def test_summarize_language_rates():
    rows = [
        {"tier": "grounded", "best_distance": 0.2, "hit": True},
        {"tier": "grounded", "best_distance": 0.3, "hit": True},
        {"tier": "supplementary", "best_distance": 0.7, "hit": False},
        {"tier": "none", "best_distance": 0.95, "hit": False},
    ]
    s = lf.summarize_language(rows)
    assert s["n"] == 4
    assert s["grounded_rate"] == 0.5          # 2/4
    assert s["answered_rate"] == 0.75         # grounded + supplementary
    assert s["non_response_rate"] == 0.25     # 1/4
    assert s["retrieval_hit_rate"] == 0.5     # 2/4


def test_summarize_empty():
    assert lf.summarize_language([]) == {"n": 0}


def test_fairness_gaps_vs_english():
    per_lang = {
        "English": {"grounded_rate": 1.0},
        "Bahasa Melayu": {"grounded_rate": 0.9},
        "Iban": {"grounded_rate": 0.4},
    }
    gaps = lf.fairness_gaps(per_lang)
    assert gaps["Bahasa Melayu"] == 0.1       # 1.0 - 0.9
    assert gaps["Iban"] == 0.6                # 1.0 - 0.4  (the bias)
    assert "English" not in gaps              # baseline excluded


def test_fairness_gaps_no_baseline():
    assert lf.fairness_gaps({"Thai": {"grounded_rate": 0.5}}) == {}

"""Tests for the pure metric helpers in tools/eval_rag.py (no models needed)."""
import json
from pathlib import Path

from tools import eval_rag
from core.agents.orchestrator import GROUNDED_GATE, SUPPLEMENTARY_GATE


def test_classify_tier_boundaries():
    assert eval_rag.classify_tier(0.0) == "grounded"
    assert eval_rag.classify_tier(GROUNDED_GATE) == "grounded"
    assert eval_rag.classify_tier((GROUNDED_GATE + SUPPLEMENTARY_GATE) / 2) == "supplementary"
    assert eval_rag.classify_tier(SUPPLEMENTARY_GATE) == "supplementary"
    assert eval_rag.classify_tier(0.99) == "none"


def test_retrieval_metrics_hit_and_precision():
    m = eval_rag.retrieval_metrics(
        ["photosynthesis.txt"],
        ["photosynthesis.txt", "other.txt", "photosynthesis.txt"],
    )
    assert m["hit"] is True
    assert abs(m["precision"] - 2 / 3) < 1e-9


def test_retrieval_metrics_miss():
    m = eval_rag.retrieval_metrics(["a.txt"], ["b.txt", "c.txt"])
    assert m["hit"] is False
    assert m["precision"] == 0.0


def test_retrieval_metrics_off_curriculum_is_none():
    m = eval_rag.retrieval_metrics([], ["whatever.txt"])
    assert m["precision"] is None and m["hit"] is None


def test_content_precision_counts_relevant_chunks():
    texts = [
        "A fraction shows a part of a whole.",      # contains 'part' + 'whole'
        "The denominator is the bottom number.",    # contains neither keyword
        "We take a part of the whole pizza.",       # contains 'part' + 'whole'
    ]
    p = eval_rag.content_precision(texts, ["part", "whole"])
    assert abs(p - 2 / 3) < 1e-9


def test_content_precision_off_curriculum_is_none():
    assert eval_rag.content_precision(["anything"], []) is None


def test_content_precision_no_chunks():
    assert eval_rag.content_precision([], ["part"]) == 0.0


def test_keyword_score_partial():
    s = eval_rag.keyword_score("Plants make food from sunlight", ["plants", "food", "moon"])
    assert s == {"matched": 2, "total": 3, "recall": 2 / 3}


def test_keyword_score_empty_keywords():
    assert eval_rag.keyword_score("anything", [])["recall"] is None


def test_aggregate_retrieval_only():
    rows = [
        {"type": "in_curriculum", "tier": "grounded", "precision": 1.0,
         "relevant_precision": 1.0, "hit": True, "keyword_recall": None, "has_citation": True},
        {"type": "in_curriculum", "tier": "none", "precision": 0.0,
         "relevant_precision": 0.5, "hit": False, "keyword_recall": None, "has_citation": False},
        {"type": "off_curriculum", "tier": "grounded", "precision": None,
         "relevant_precision": None, "hit": None, "keyword_recall": None, "has_citation": True},
    ]
    s = eval_rag.aggregate(rows)
    assert s["retrieval_hit_rate"] == 0.5
    assert s["retrieval_source_precision_at_k"] == 0.5
    assert s["retrieval_relevant_precision_at_k"] == 0.75      # (1.0 + 0.5) / 2
    assert s["tier_distribution"] == {"grounded": 2, "supplementary": 0, "none": 1}
    assert s["non_response_rate_in_curriculum"] == 0.5
    # one off-curriculum question grounded with a citation -> false grounding 100%
    assert s["false_grounding_rate_off_curriculum"] == 1.0
    assert "answer_accuracy" not in s          # no LLM scores present


def test_aggregate_with_llm_scores():
    rows = [
        {"type": "in_curriculum", "tier": "grounded", "precision": 1.0, "hit": True,
         "keyword_recall": 1.0, "confidence": 0.9, "has_citation": True},
        {"type": "in_curriculum", "tier": "grounded", "precision": 1.0, "hit": True,
         "keyword_recall": 0.0, "confidence": 0.4, "has_citation": True},
        {"type": "off_curriculum", "tier": "none", "precision": None, "hit": None,
         "keyword_recall": None, "confidence": 0.0, "has_citation": False},
    ]
    s = eval_rag.aggregate(rows, keyword_threshold=0.5)
    assert s["answer_accuracy"] == 0.5
    assert s["mean_confidence_correct"] == 0.9
    assert s["mean_confidence_incorrect"] == 0.4
    assert s["hallucination_rate"] == 0.0


def test_group_summaries_splits_by_key():
    rows = [
        {"type": "in_curriculum", "tier": "grounded", "precision": 1.0, "hit": True,
         "keyword_recall": None, "has_citation": True, "country": "Malaysia"},
        {"type": "in_curriculum", "tier": "none", "precision": 0.0, "hit": False,
         "keyword_recall": None, "has_citation": False, "country": "Vietnam"},
        {"type": "in_curriculum", "tier": "grounded", "precision": 1.0, "hit": True,
         "keyword_recall": None, "has_citation": True, "country": "Vietnam"},
    ]
    groups = eval_rag.group_summaries(rows, "country")
    assert set(groups) == {"Malaysia", "Vietnam"}
    assert groups["Malaysia"]["retrieval_hit_rate"] == 1.0
    assert groups["Vietnam"]["retrieval_hit_rate"] == 0.5
    assert groups["Vietnam"]["non_response_rate_in_curriculum"] == 0.5


def test_group_summaries_missing_key_unspecified():
    rows = [{"type": "in_curriculum", "tier": "grounded", "precision": 1.0, "hit": True,
             "keyword_recall": None, "has_citation": True}]
    groups = eval_rag.group_summaries(rows, "country")
    assert "unspecified" in groups


def test_asean_gold_set_tagged_by_country():
    gold = json.loads(Path("data/eval/gold_set_asean.json").read_text(encoding="utf-8"))
    countries = {it["country"] for it in gold["items"]}
    assert {"Malaysia", "Philippines", "Indonesia", "Vietnam"} <= countries
    for it in gold["items"]:
        assert "language" in it


def test_llm_judge_parses_schema(monkeypatch):
    monkeypatch.setattr("core.llm_engine._ollama_generate",
                        lambda *a, **k: '{"correct": true}')
    assert eval_rag.llm_judge("Q", "A") is True
    monkeypatch.setattr("core.llm_engine._ollama_generate",
                        lambda *a, **k: '{"correct": false}')
    assert eval_rag.llm_judge("Q", "A") is False


def test_llm_judge_unavailable_returns_none(monkeypatch):
    monkeypatch.setattr("core.llm_engine._ollama_generate", lambda *a, **k: "")
    assert eval_rag.llm_judge("Q", "A") is None


def test_aggregate_includes_judge_accuracy():
    rows = [
        {"type": "in_curriculum", "tier": "grounded", "precision": 1.0,
         "relevant_precision": 1.0, "hit": True, "keyword_recall": 1.0,
         "judge_correct": True, "confidence": 0.9, "has_citation": True},
        {"type": "in_curriculum", "tier": "grounded", "precision": 1.0,
         "relevant_precision": 1.0, "hit": True, "keyword_recall": 1.0,
         "judge_correct": False, "confidence": 0.5, "has_citation": True},
    ]
    s = eval_rag.aggregate(rows)
    assert s["answer_accuracy_judged"] == 0.5
    assert s["n_judged"] == 2


def test_gold_set_is_valid():
    gold = json.loads(Path("data/eval/gold_set.json").read_text(encoding="utf-8"))
    assert gold["items"]
    ids = [it["id"] for it in gold["items"]]
    assert len(ids) == len(set(ids))            # unique ids
    for it in gold["items"]:
        assert it["type"] in ("in_curriculum", "off_curriculum")
        assert it["question"].strip()
        if it["type"] == "off_curriculum":
            assert it["expected_sources"] == []

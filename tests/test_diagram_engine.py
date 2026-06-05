"""Tests for math diagram spec generation + validation."""
import json

import core.llm_engine as llm
from core.diagram_engine import generate_diagram, validate_diagram


def test_none_type_returns_none():
    assert validate_diagram({"type": "none"}) is None
    assert validate_diagram({}) is None


def test_number_line_validated_and_clamped():
    spec = validate_diagram({
        "type": "number_line", "min": 0, "max": 5, "step": 1,
        "points": [{"value": 2, "label": "a"}, {"value": 99}],   # 99 is out of range -> dropped
    })
    assert spec["type"] == "number_line" and spec["min"] == 0 and spec["max"] == 5
    assert [p["value"] for p in spec["points"]] == [2]


def test_number_line_rejected_when_min_ge_max():
    assert validate_diagram({"type": "number_line", "min": 5, "max": 5}) is None


def test_fraction_bar_drops_bad_denominator():
    spec = validate_diagram({"type": "fraction_bar", "fractions": [
        {"numerator": 1, "denominator": 0},        # invalid -> dropped
        {"numerator": 3, "denominator": 4},
    ]})
    assert len(spec["fractions"]) == 1 and spec["fractions"][0]["denominator"] == 4


def test_right_triangle_needs_positive_legs():
    assert validate_diagram({"type": "right_triangle", "base": 3, "height": 4})["base"] == 3
    assert validate_diagram({"type": "right_triangle", "base": 0, "height": 4}) is None


def test_function_plot_rejects_unsafe_expression():
    assert validate_diagram({"type": "function_plot", "expression": "2*x+1"})["expression"] == "2*x+1"
    assert validate_diagram({"type": "function_plot", "expression": "__import__('os')"}) is None


def test_flow_needs_two_steps():
    spec = validate_diagram({"type": "flow", "steps": [{"label": "Grass"}, {"label": "Frog"}]})
    assert spec["type"] == "flow" and len(spec["steps"]) == 2
    assert validate_diagram({"type": "flow", "steps": [{"label": "only one"}]}) is None


def test_cycle_needs_three_steps_and_accepts_bare_strings():
    spec = validate_diagram({"type": "cycle", "steps": ["Evaporation", "Condensation", "Precipitation"]})
    assert spec["type"] == "cycle" and [s["label"] for s in spec["steps"]][0] == "Evaporation"
    assert validate_diagram({"type": "cycle", "steps": ["a", "b"]}) is None


def test_comparison_needs_two_columns():
    spec = validate_diagram({"type": "comparison", "columns": [
        {"label": "Solid", "items": ["fixed"]}, {"label": "Gas", "items": ["fills space"]}]})
    assert len(spec["columns"]) == 2 and spec["columns"][0]["label"] == "Solid"
    assert validate_diagram({"type": "comparison", "columns": [{"label": "Solid"}]}) is None


def test_science_aliases_normalized():
    assert validate_diagram({"type": "process", "steps": [{"label": "a"}, {"label": "b"}]})["type"] == "flow"
    assert validate_diagram({"type": "lifecycle", "steps": ["a", "b", "c"]})["type"] == "cycle"


def test_type_aliases_are_normalized():
    assert validate_diagram({"type": "triangle", "base": 3, "height": 4})["type"] == "right_triangle"
    assert validate_diagram({"type": "bar", "bars": [{"label": "A", "value": 2}]})["type"] == "bar_chart"


def test_generate_diagram_parses_model_output(monkeypatch):
    obj = json.dumps({"type": "bar_chart", "bars": [{"label": "A", "value": 3}, {"label": "B", "value": 5}]})
    monkeypatch.setattr(llm, "_ollama_generate", lambda *a, **k: obj)
    spec = generate_diagram("compare 3 and 5")
    assert spec["type"] == "bar_chart" and len(spec["bars"]) == 2


def test_generate_diagram_none_when_model_says_none(monkeypatch):
    monkeypatch.setattr(llm, "_ollama_generate", lambda *a, **k: '{"type":"none"}')
    assert generate_diagram("what is your name") is None

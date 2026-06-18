"""Tests for the pure helpers in tools/load_test.py (no server needed)."""
from tools import load_test


def test_percentile_basic():
    vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert load_test.percentile(vals, 50) == 5
    assert load_test.percentile(vals, 100) == 10
    assert load_test.percentile(vals, 95) == 10


def test_percentile_edges():
    assert load_test.percentile([], 50) == 0.0
    assert load_test.percentile([42], 95) == 42


def test_summarize_counts_and_throughput():
    s = load_test.summarize([0.5, 1.0, 1.5, 2.0], errors=1, wall_seconds=2.0)
    assert s["requests"] == 5
    assert s["ok"] == 4
    assert s["errors"] == 1
    assert s["error_rate"] == 0.2
    assert s["throughput_rps"] == 2.0          # 4 ok / 2s
    assert s["throughput_rpm"] == 120.0
    assert s["latency_s"]["p50"] > 0
    assert s["latency_s"]["max"] == 2.0


def test_summarize_all_errors():
    s = load_test.summarize([], errors=3, wall_seconds=1.0)
    assert s["ok"] == 0
    assert s["error_rate"] == 1.0
    assert s["throughput_rps"] == 0.0
    assert s["latency_s"]["p95"] == 0.0

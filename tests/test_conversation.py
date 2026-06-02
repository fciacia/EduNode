"""Tests for the in-memory conversation buffer (conversational memory)."""
import core.conversation as conv


def setup_function():
    conv._store.clear()


def test_append_and_get_history():
    conv.append_turn("c1", "user", "What is a fraction?")
    conv.append_turn("c1", "assistant", "A fraction is part of a whole.")
    hist = conv.get_history("c1")
    assert [t["role"] for t in hist] == ["user", "assistant"]
    assert hist[0]["text"] == "What is a fraction?"


def test_history_capped_to_max_turns():
    for i in range(20):
        conv.append_turn("c1", "user", f"q{i}")
    hist = conv.get_history("c1")
    assert len(hist) == conv._MAX_TURNS
    assert hist[-1]["text"] == "q19"            # keeps the most recent


def test_unknown_conversation_returns_empty():
    assert conv.get_history("nope") == []
    assert conv.get_history(None) == []


def test_reset_clears_one_conversation():
    conv.append_turn("c1", "user", "hi")
    conv.reset("c1")
    assert conv.get_history("c1") == []


def test_blank_inputs_ignored():
    conv.append_turn(None, "user", "x")
    conv.append_turn("c1", "user", "")
    assert conv.get_history("c1") == []


def test_conversation_count_capped():
    for i in range(conv._MAX_CONVERSATIONS + 50):
        conv.append_turn(f"conv{i}", "user", "hi")
    assert len(conv._store) <= conv._MAX_CONVERSATIONS

"""Tests for the SQLite-backed conversation buffer (conversational memory)."""
import core.conversation as conv


def test_append_and_get_history(temp_db):
    conv.append_turn("c1", "user", "What is a fraction?")
    conv.append_turn("c1", "assistant", "A fraction is part of a whole.")
    hist = conv.get_history("c1")
    assert [t["role"] for t in hist] == ["user", "assistant"]
    assert hist[0]["text"] == "What is a fraction?"


def test_history_capped_to_max_turns(temp_db):
    for i in range(20):
        conv.append_turn("c1", "user", f"q{i}")
    hist = conv.get_history("c1")
    assert len(hist) == conv._MAX_TURNS
    assert hist[-1]["text"] == "q19"            # keeps the most recent


def test_unknown_conversation_returns_empty(temp_db):
    assert conv.get_history("nope") == []
    assert conv.get_history(None) == []


def test_reset_clears_one_conversation(temp_db):
    conv.append_turn("c1", "user", "hi")
    conv.append_turn("c2", "user", "hello")
    conv.reset("c1")
    assert conv.get_history("c1") == []
    assert conv.get_history("c2") != []          # other conversations untouched


def test_blank_inputs_ignored(temp_db):
    conv.append_turn(None, "user", "x")
    conv.append_turn("c1", "user", "")
    assert conv.get_history("c1") == []


def test_conversations_are_independent(temp_db):
    conv.append_turn("a", "user", "alpha")
    conv.append_turn("b", "user", "beta")
    assert conv.get_history("a")[0]["text"] == "alpha"
    assert conv.get_history("b")[0]["text"] == "beta"


def test_survives_reconnect(temp_db):
    # Each call opens its own connection, so data persists across them
    # (i.e. it would survive a restart).
    conv.append_turn("c1", "user", "remember me")
    assert conv.get_history("c1")[0]["text"] == "remember me"

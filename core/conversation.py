"""
core/conversation.py
====================
Conversational memory for the chat tutor, persisted in SQLite.

Each conversation (identified by a client-generated ``conversation_id``) keeps a
short buffer of recent turns in English — captured as the pipeline already
translates each turn — so the pedagogy agent can answer follow-ups in context
("explain that more simply", "give an example").

Persisted in the ``conversation_turns`` table so a buffer survives a server
restart. Each conversation is trimmed to the most recent turns so storage stays
small.
"""
from __future__ import annotations

from core.progress_tracker import _db, _now

_MAX_TURNS = 6   # keep the last 6 messages per conversation (~3 exchanges)


def get_history(conversation_id: str | None) -> list[dict]:
    """Return the recent turns for a conversation (oldest first)."""
    if not conversation_id:
        return []
    with _db() as conn:
        rows = conn.execute(
            "SELECT role, text FROM conversation_turns"
            " WHERE conversation_id=? ORDER BY id DESC LIMIT ?",
            (conversation_id, _MAX_TURNS),
        ).fetchall()
    return [{"role": r["role"], "text": r["text"]} for r in reversed(rows)]


def append_turn(conversation_id: str | None, role: str, text: str) -> None:
    """Append a turn (role: "user" | "assistant"). Blank inputs are ignored."""
    if not conversation_id or not (text or "").strip():
        return
    with _db() as conn:
        conn.execute(
            "INSERT INTO conversation_turns (conversation_id, role, text, created_at)"
            " VALUES (?,?,?,?)",
            (conversation_id, role, text, _now()),
        )
        # Trim to the most recent _MAX_TURNS for this conversation.
        conn.execute(
            "DELETE FROM conversation_turns WHERE conversation_id=? AND id NOT IN ("
            "  SELECT id FROM conversation_turns WHERE conversation_id=? ORDER BY id DESC LIMIT ?"
            ")",
            (conversation_id, conversation_id, _MAX_TURNS),
        )


def reset(conversation_id: str | None) -> None:
    """Forget a conversation (used when the student starts a new chat)."""
    if not conversation_id:
        return
    with _db() as conn:
        conn.execute(
            "DELETE FROM conversation_turns WHERE conversation_id=?",
            (conversation_id,),
        )

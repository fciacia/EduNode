"""
core/conversation.py
====================
In-memory conversational memory for the chat tutor.

Each conversation (identified by a client-generated ``conversation_id``) keeps a
short buffer of recent turns in English — captured as the pipeline already
translates each turn — so the pedagogy agent can answer follow-ups in context
("explain that more simply", "give an example").

Deliberately in-memory: a tutoring session is short-lived, so the buffer resets
when the server restarts. Bounded in both turns-per-conversation and total
conversations so it can never grow without limit.
"""
from __future__ import annotations

from collections import OrderedDict

_MAX_TURNS = 6              # keep the last 6 messages (~3 exchanges)
_MAX_CONVERSATIONS = 200    # evict the least-recently-used beyond this

_store: "OrderedDict[str, list[dict]]" = OrderedDict()


def get_history(conversation_id: str | None) -> list[dict]:
    """Return a copy of the recent turns for a conversation (oldest first)."""
    if not conversation_id:
        return []
    return list(_store.get(conversation_id, []))


def append_turn(conversation_id: str | None, role: str, text: str) -> None:
    """Append a turn (role: "user" | "assistant"). Blank inputs are ignored."""
    if not conversation_id or not (text or "").strip():
        return
    buf = _store.setdefault(conversation_id, [])
    buf.append({"role": role, "text": text})
    del buf[:-_MAX_TURNS]                 # keep only the most recent turns
    _store.move_to_end(conversation_id)   # mark as recently used
    while len(_store) > _MAX_CONVERSATIONS:
        _store.popitem(last=False)        # evict least-recently-used


def reset(conversation_id: str | None) -> None:
    """Forget a conversation (used when the student starts a new chat)."""
    _store.pop(conversation_id, None)

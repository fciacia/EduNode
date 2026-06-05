"""
core/content_cache.py
=====================
A tiny on-disk cache of generated study content (quizzes, flashcards, slides),
keyed by kind + subject + language + level + topic.

Why: phi3 generation is slow on a Raspberry Pi. Caching makes repeat topics
instant, and — because routes check the cache *before* the Ollama health check —
pre-baked content (see prebake.py) is served fully offline even when the model
isn't running.

get(kind, subject, language, level, topic) -> payload | None
put(kind, subject, language, level, topic, payload) -> None
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
from pathlib import Path

log = logging.getLogger(__name__)

CACHE_DIR = Path(os.getenv("CONTENT_CACHE_DIR", "data/cache"))


def _key(kind: str, subject: str, language: str, level: str, topic: str) -> str:
    raw = "|".join([
        kind.lower(), (subject or "").lower(), (language or "").lower(),
        (level or "").lower(), (topic or "").strip().lower(),
    ])
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def _path(kind: str, subject: str, language: str, level: str, topic: str) -> Path:
    return CACHE_DIR / kind.lower() / (_key(kind, subject, language, level, topic) + ".json")


def get(kind: str, subject: str, language: str, level: str, topic: str):
    p = _path(kind, subject, language, level, topic)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:                       # corrupt/partial file — treat as miss
        log.warning("content_cache read failed for %s: %s", p, exc)
        return None


def put(kind: str, subject: str, language: str, level: str, topic: str, payload) -> None:
    p = _path(kind, subject, language, level, topic)
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    except Exception as exc:
        log.warning("content_cache write failed for %s: %s", p, exc)

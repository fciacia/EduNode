"""
core/correction_store.py
========================
Teacher-assisted translation correction loop (Issue 4).

The dialect flywheel already lets students/teachers *flag* a bad translation
(data/translation_reports.jsonl). This module closes the loop: a teacher reviews
a flag and submits the *correct* wording, which is stored as a verified
correction pair. These pairs are exactly the supervised data needed to fine-tune
or post-edit future translation models for low-resource languages (Iban,
Cebuano, …).

Stored as JSON Lines at data/translation_corrections.jsonl so it is easy to
export, sneakernet-sync, and feed into a training pipeline.

Public API
----------
save_correction(language, original, corrected, english="", note="", by="teacher")
list_corrections(language=None, limit=200) -> list[dict]
count(language=None) -> int
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger(__name__)

CORRECTIONS_PATH = Path("data/translation_corrections.jsonl")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def save_correction(language: str, original: str, corrected: str,
                    english: str = "", note: str = "", by: str = "teacher") -> dict:
    """Persist a verified correction. Returns the stored entry.

    *original*  — the wording the system showed (the wrong/awkward translation)
    *corrected* — the teacher's verified replacement
    *english*   — the source English (optional, improves training value)
    """
    language = (language or "").strip()
    corrected = (corrected or "").strip()
    if not language or not corrected:
        raise ValueError("language and corrected text are required")

    entry = {
        "ts": _now(),
        "language": language[:60],
        "english": (english or "").strip()[:1000],
        "original": (original or "").strip()[:1000],
        "corrected": corrected[:1000],
        "note": (note or "").strip()[:500],
        "by": (by or "teacher").strip()[:60],
    }
    CORRECTIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CORRECTIONS_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    log.info("Saved translation correction for %s by %s.", language, entry["by"])
    return entry


def _read_all() -> list[dict]:
    if not CORRECTIONS_PATH.exists():
        return []
    out = []
    for line in CORRECTIONS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def list_corrections(language: str | None = None, limit: int = 200) -> list[dict]:
    """Most-recent-first verified corrections, optionally filtered by language."""
    rows = _read_all()
    if language:
        lang = language.strip().lower()
        rows = [r for r in rows if r.get("language", "").lower() == lang]
    return rows[-limit:][::-1]


def count(language: str | None = None) -> int:
    return len(list_corrections(language=language, limit=10**9))

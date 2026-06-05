#!/usr/bin/env python3
"""
prebake.py — pre-generate study content so the first tap is instant offline.

Walks the suggested topics for each subject and generates + caches a quiz,
flashcard deck, and slide deck for them. Because the API checks the content
cache before the Ollama health check, pre-baked topics are then served even
with the model stopped — ideal for a Raspberry Pi in a classroom.

    python prebake.py                       # English, no level, all subjects
    python prebake.py --lang "Bahasa Melayu" --level primary
    python prebake.py --kinds quiz,slides   # only some kinds

Requires Ollama running (it is what generates the content to cache).
"""
from __future__ import annotations

import argparse

import config as cfg
from app import _grounded_context, _suggest_topics
from core import content_cache
from core.flashcard_engine import generate_flashcards
from core.llm_engine import generate_quiz, ollama_available
from core.slide_engine import generate_slides

KINDS = ("quiz", "cards", "slides")


def bake_topic(subject: str, topic: str, language: str, level: str, kinds) -> None:
    rag, grounded, sources = _grounded_context(topic, subject)
    base = {"grounded": grounded, "sources": sources}

    if "quiz" in kinds:
        qs = generate_quiz(topic, language, rag, level)
        if qs:
            content_cache.put("quiz", subject, language, level, topic, {**base, "questions": qs})
    if "cards" in kinds:
        cards = generate_flashcards(topic, language, rag, level)
        if cards:
            content_cache.put("cards", subject, language, level, topic, {**base, "flashcards": cards})
    if "slides" in kinds:
        slides = generate_slides(topic, language, rag, level)
        if slides:
            content_cache.put("slides", subject, language, level, topic, {**base, "slides": slides})


def main() -> int:
    ap = argparse.ArgumentParser(description="Pre-generate offline study content.")
    ap.add_argument("--lang", default=cfg.HUB_LANGUAGES[0])
    ap.add_argument("--level", default="", choices=["", "primary", "secondary"])
    ap.add_argument("--subjects", default="", help="comma-separated; default = all")
    ap.add_argument("--kinds", default=",".join(KINDS), help="comma-separated: quiz,cards,slides")
    ap.add_argument("--limit", type=int, default=6, help="topics per subject")
    args = ap.parse_args()

    if not ollama_available():
        print("Ollama is not running — start it first (it generates the content to cache).")
        return 1

    subjects = [s.strip() for s in args.subjects.split(",") if s.strip()] or list(cfg.AVAILABLE_SUBJECTS)
    kinds = [k.strip() for k in args.kinds.split(",") if k.strip()]

    for subject in subjects:
        topics = _suggest_topics(subject, limit=args.limit)
        print(f"\n{subject}: {len(topics)} topics ({args.lang}, level={args.level or 'general'})")
        for topic in topics:
            print(f"  • {topic} …", flush=True)
            try:
                bake_topic(subject, topic, args.lang, args.level, kinds)
            except Exception as exc:
                print(f"    ! skipped: {exc}")
    print("\nDone. Pre-baked content will now load instantly (even with Ollama stopped).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

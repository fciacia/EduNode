"""
core/slide_engine.py
====================
Generate a short, curriculum-grounded lesson slide deck from a topic.

Public API
----------
generate_slides(topic, language, rag_context) -> list[dict]
    Returns up to MAX_SLIDES slide dicts:
        [{"title": str, "bullets": [str, ...], "notes": str}, ...]
    Returns [] on parse failure so the caller can degrade gracefully.
"""
from __future__ import annotations

import json
import logging
import re

log = logging.getLogger(__name__)

MAX_SLIDES = 6

# Structured-output schema — constrains the model to emit valid slide JSON.
SLIDE_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "slides": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title":   {"type": "string"},
                    "bullets": {"type": "array", "items": {"type": "string"}},
                    "notes":   {"type": "string"},
                },
                "required": ["title", "bullets"],
            },
        },
    },
    "required": ["slides"],
}


def generate_slides(topic: str, language: str, rag_context: str) -> list[dict]:
    """Generate a lesson deck about *topic*, grounded in *rag_context*."""
    from core.llm_engine import _ollama_generate

    context_block = (
        f"Curriculum context:\n{rag_context}\n\n" if rag_context.strip() else ""
    )
    system = (
        "You are a teacher making a short lesson slide deck for school students. "
        f"Output ONLY a JSON object with a 'slides' array of {MAX_SLIDES} slides: a title "
        "slide, a few content slides, and a summary slide. Each slide has a short 'title', "
        "3-5 short 'bullets', and 'notes' (one or two spoken sentences the teacher would "
        "say). Use simple words. Base it on the curriculum context when provided."
    )
    prompt = f"{context_block}Make a {MAX_SLIDES}-slide lesson about: {topic}\nRespond in {language}."

    raw = _ollama_generate(prompt, temperature=0.4, max_tokens=900, system=system, schema=SLIDE_SCHEMA)
    if not raw:
        return []
    return _parse_slides_json(raw)


def _parse_slides_json(raw: str) -> list[dict]:
    """Extract and validate the slide list from raw SLM output."""
    raw = re.sub(r"```(?:json)?", "", raw).strip()

    # Schema mode yields an object; tolerate a bare array too.
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if not match:
            log.warning("No slide JSON found.")
            return []
        try:
            data = json.loads(re.sub(r",\s*([}\]])", r"\1", match.group()))
        except json.JSONDecodeError as exc:
            log.warning("Slide JSON parse error: %s", exc)
            return []

    items = data.get("slides", []) if isinstance(data, dict) else data

    validated: list[dict] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        title   = item.get("title", "")
        bullets = item.get("bullets", [])
        notes   = item.get("notes", "")
        if not (isinstance(title, str) and title.strip()):
            continue
        if not isinstance(bullets, list):
            continue
        clean_bullets = [str(b).strip() for b in bullets if str(b).strip()]
        if not clean_bullets:
            continue
        validated.append({
            "title":   title.strip(),
            "bullets": clean_bullets[:6],
            "notes":   str(notes).strip(),
        })
        if len(validated) == MAX_SLIDES:
            break

    return validated

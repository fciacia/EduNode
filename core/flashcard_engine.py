"""
core/flashcard_engine.py
========================
Step 11 — Generate structured flashcard data from a topic + RAG context.

Public API
----------
generate_flashcards(topic, language, rag_context) -> list[dict]
    Returns up to 5 flashcard dicts:
        [{"title": str, "body": str, "image": str | None}, ...]
    Returns [] on parse failure.
"""

from __future__ import annotations

import json
import logging
import re

log = logging.getLogger(__name__)

MAX_FLASHCARDS = 5

# Structured-output schema — constrains the model to emit valid flashcard JSON.
FLASHCARD_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "flashcards": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "body":  {"type": "string"},
                    "image": {"type": ["string", "null"]},
                },
                "required": ["title", "body"],
            },
        },
    },
    "required": ["flashcards"],
}


def generate_flashcards(
    topic: str,
    language: str,
    rag_context: str,
    level: str = "",
) -> list[dict]:
    """
    Generate flashcards about *topic* grounded in *rag_context*.

    Each flashcard has:
        title : short keyword or concept name
        body  : 1–3 sentence explanation for a school student
        image : suggested image filename (e.g. "water_cycle.png") or null

    Returns [] on any parse failure so the caller can degrade gracefully.
    """
    from core.llm_engine import _ollama_generate, level_instruction  # shared helpers

    context_block = (
        f"Curriculum context:\n{rag_context}\n\n"
        if rag_context.strip()
        else ""
    )
    level_hint = level_instruction(level)

    system = (
        "You are a flashcard generator for school students. "
        f"Output ONLY a JSON array of exactly {MAX_FLASHCARDS} flashcards. "
        "Each flashcard must have: "
        '{"title": "short concept name", "body": "1-3 sentence explanation", '
        '"image": "relevant_image.png or null"} '
        + (level_hint + " " if level_hint else "")
        + "Do not include any text outside the JSON array."
    )

    prompt = (
        f"{context_block}"
        f"Generate {MAX_FLASHCARDS} flashcards about: {topic}\n"
        f"Respond in {language}."
    )

    raw = _ollama_generate(prompt, temperature=0.4, max_tokens=800, system=system, schema=FLASHCARD_SCHEMA)
    if not raw:
        return []

    return _parse_flashcard_json(raw)


def _parse_flashcard_json(raw: str) -> list[dict]:
    """Extract and validate a JSON array of flashcard dicts from raw SLM output."""
    # Strip markdown code fences
    raw = re.sub(r"```(?:json)?", "", raw).strip()

    # Find the JSON array
    match = re.search(r"\[.*\]", raw, re.DOTALL)
    if not match:
        log.warning("No JSON array found in flashcard response.")
        return []

    # Remove trailing commas before ] or } (LLMs often emit these)
    cleaned = re.sub(r",\s*([}\]])", r"\1", match.group())

    try:
        cards = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        log.warning("Flashcard JSON parse error: %s", exc)
        return []

    validated: list[dict] = []
    for item in cards:
        if not isinstance(item, dict):
            continue

        title = item.get("title", "")
        body  = item.get("body",  "")
        image = item.get("image", None)

        if not (isinstance(title, str) and title.strip()):
            continue
        if not (isinstance(body, str) and body.strip()):
            continue

        # Sanitise image: must be a plain filename string or null
        if image and isinstance(image, str) and image.strip():
            # Strip any path components — only the filename is safe
            image = re.sub(r"[^a-zA-Z0-9._\-]", "_", image.strip())
        else:
            image = None

        validated.append({
            "title": title.strip(),
            "body":  body.strip(),
            "image": image,
        })

        if len(validated) == MAX_FLASHCARDS:
            break

    return validated

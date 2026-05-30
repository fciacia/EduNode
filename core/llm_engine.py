"""
core/llm_engine.py
==================
Step 4 — All Ollama (SLM) interactions in one module.

Handles:
  - Two-tier language dispatch (Tier-1 direct generation / Tier-2 bridge mode)
  - RAG-grounded tutoring answers
  - Quiz MCQ generation (JSON output)
  - Podcast script generation (MAYA / NIKO dialogue)

Public API
----------
query_tutor(user_message, language, rag_context) -> str
    Returns a tutoring answer in the requested language.
    Tier-1 languages: generated directly in that language.
    Tier-2 languages: generated in English, then bridge-translated.

generate_quiz(topic, language, rag_context) -> list[dict]
    Returns up to 3 MCQ dicts:
        [{"question": str, "options": [A, B, C, D], "answer": "A"|..}, ...]
    Returns [] on any parse failure.

generate_podcast_script(topic, language) -> str
    Returns a MAYA/NIKO dialogue script as a plain string.
"""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration (env overrides)
# ---------------------------------------------------------------------------
OLLAMA_BASE = os.getenv("OLLAMA_BASE", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b-instruct-q4_K_M")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "512"))
GLOSSARY_DIR = Path("data/glossaries")


# ---------------------------------------------------------------------------
# Private: core Ollama helper
# ---------------------------------------------------------------------------

def _resolve_ollama_model() -> str:
    try:
        import requests  # type: ignore
    except ImportError:
        return OLLAMA_MODEL

    try:
        resp = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
        resp.raise_for_status()
        models = resp.json().get("models") or []
    except Exception:
        return OLLAMA_MODEL

    available = [m.get("name") for m in models if m.get("name")]
    if OLLAMA_MODEL in available or not available:
        return OLLAMA_MODEL

    fallback_model = available[0]
    log.warning("Configured Ollama model '%s' not found; using '%s' instead.", OLLAMA_MODEL, fallback_model)
    return fallback_model


def _ollama_generate(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = MAX_TOKENS,
    system: str = "",
) -> str:
    """
    POST to Ollama /api/generate.
    Returns the response text, or "" on any error.
    """
    try:
        import requests  # type: ignore
    except ImportError:
        log.error("requests library missing: pip install requests")
        return ""

    payload: dict[str, Any] = {
        "model":  _resolve_ollama_model(),
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }
    if system:
        payload["system"] = system

    try:
        resp = requests.post(
            f"{OLLAMA_BASE}/api/generate",
            json=payload,
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        return (data.get("response") or "").strip()
    except requests.exceptions.ConnectionError:
        log.warning("Ollama is not running at %s — returning fallback.", OLLAMA_BASE)
        return ""
    except Exception as exc:  # noqa: BLE001
        log.warning("Ollama request failed: %s", exc)
        return ""


# ---------------------------------------------------------------------------
# Private: tutor prompt builder
# ---------------------------------------------------------------------------

def _build_tutor_prompt(user_message: str, language: str, rag_context: str) -> str:
    context_block = (
        f"Relevant curriculum context:\n{rag_context}\n\n"
        if rag_context.strip()
        else ""
    )
    return (
        f"{context_block}"
        f"Student question: {user_message}"
    )


def _build_tutor_system(language: str) -> str:
    return (
        f"You are EduNode, a friendly offline AI tutor for school students "
        f"in rural ASEAN communities. "
        f"You MUST respond in {language}. "
        f"Keep your answer under 150 words. "
        f"Use simple language appropriate for primary or secondary school students. "
        f"If you are unsure, say so honestly rather than guessing."
    )


# ---------------------------------------------------------------------------
# Private: glossary + bridge translation (Tier-2)
# ---------------------------------------------------------------------------

def _load_glossary(language: str) -> dict[str, str]:
    """
    Load glossary JSON for a Tier-2 language.
    Returns {english_term_lower: native_term}.
    Falls back to {} if file not found.
    """
    path = GLOSSARY_DIR / f"{language.lower()}.json"
    if not path.exists():
        log.debug("No glossary found for '%s' at %s.", language, path)
        return {}
    try:
        entries = json.loads(path.read_text(encoding="utf-8"))
        return {
            e["english"].lower(): e["native"]
            for e in entries
            if "english" in e and "native" in e and e["english"] and e["native"]
        }
    except Exception as exc:  # noqa: BLE001
        log.warning("Could not load glossary for '%s': %s", language, exc)
        return {}


def _bridge_translate(english_text: str, language: str) -> str:
    """
    Tier-2 bridge mode:
      1. Ask SLM to translate english_text into {language} using glossary hints.
      2. Return bilingual output: [English] ... \\n[{language}] ...
    Falls back to English-only if translation fails or glossary is empty.
    """
    glossary = _load_glossary(language)

    glossary_hint = ""
    if glossary:
        sample = list(glossary.items())[:30]
        glossary_hint = (
            f"Key terms to use: {', '.join(f'{k}={v}' for k, v in sample)}. "
        )

    prompt = (
        f"Translate the following into {language}. "
        f"{glossary_hint}"
        f"Produce only the translation, no explanations.\n\n"
        f"Text: {english_text}\n\nTranslation:"
    )

    translated = _ollama_generate(prompt, temperature=0.3, max_tokens=300)
    if not translated:
        log.debug("Bridge translation returned empty for '%s' — using English.", language)
        return english_text

    return f"[English] {english_text}\n[{language}] {translated}"


# ---------------------------------------------------------------------------
# Public: tutoring answer
# ---------------------------------------------------------------------------

def query_tutor(user_message: str, language: str, student_id=None, subject: str = "General") -> dict:
    """
    Run the agentic pipeline and return a structured result:
        {answer, confidence, citations, needs_review, language}

    Thin wrapper over core.agents.orchestrator. Kept here so existing imports
    (`from core.llm_engine import query_tutor`) continue to work.
    """
    from core.agents.orchestrator import run_pipeline
    return run_pipeline(user_message, language, student_id=student_id, subject=subject)


def _offline_fallback(user_message: str) -> str:
    return (
        "Sorry, I could not reach the AI model right now. "
        "Please make sure Ollama is running (`ollama serve`) and try again."
    )


# ---------------------------------------------------------------------------
# Public: quiz generation
# ---------------------------------------------------------------------------

def generate_quiz(topic: str, language: str, rag_context: str) -> list[dict]:
    """
    Generate 3 multiple-choice questions about *topic*.

    Returns a list of dicts:
        [{"question": str, "options": [str, str, str, str], "answer": "A"}, ...]
    Returns [] if the SLM output cannot be parsed as valid JSON.
    """
    context_block = f"Curriculum context:\n{rag_context}\n\n" if rag_context.strip() else ""

    system = (
        "You are a quiz generator for school students. "
        "Output ONLY a JSON array of exactly 3 multiple-choice questions. "
        "Each item must have: "
        '{"question": "...", "options": ["A. ...", "B. ...", "C. ...", "D. ..."], "answer": "A"} '
        "where answer is the letter of the correct option. "
        "Do not include any text outside the JSON array."
    )

    prompt = (
        f"{context_block}"
        f"Generate 3 multiple-choice quiz questions about: {topic}\n"
        f"Respond in {language}."
    )

    raw = _ollama_generate(prompt, temperature=0.3, max_tokens=600, system=system)
    if not raw:
        return []

    return _parse_quiz_json(raw)


def _parse_quiz_json(raw: str) -> list[dict]:
    """Extract and validate a JSON array of MCQs from raw SLM output."""
    # Strip markdown code fences if present
    raw = re.sub(r"```(?:json)?", "", raw).strip()

    # Find the JSON array in the output (SLM sometimes adds preamble text)
    match = re.search(r"\[.*\]", raw, re.DOTALL)
    if not match:
        log.warning("No JSON array found in quiz response.")
        return []

    # Remove trailing commas before ] or } (LLMs often emit these)
    cleaned = re.sub(r",\s*([}\]])", r"\1", match.group())

    try:
        questions = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        log.warning("Quiz JSON parse error: %s", exc)
        return []

    validated = []
    for item in questions:
        if not isinstance(item, dict):
            continue
        q       = item.get("question", "")
        options = item.get("options", [])
        answer  = item.get("answer", "")
        if (
            isinstance(q, str) and q.strip()
            and isinstance(options, list) and len(options) == 4
            and isinstance(answer, str) and answer.upper() in ("A", "B", "C", "D")
        ):
            validated.append({
                "question": q.strip(),
                "options":  [str(o).strip() for o in options],
                "answer":   answer.upper(),
            })
        if len(validated) == 3:
            break

    return validated


# ---------------------------------------------------------------------------
# Public: podcast script generation
# ---------------------------------------------------------------------------

def generate_podcast_script(topic: str, language: str) -> str:
    """
    Generate a 6–8 exchange dialogue between two hosts:
      MAYA — the curious student host
      NIKO — the knowledgeable explainer host

    Returns a plain string formatted as:
        MAYA: ...
        NIKO: ...
        ...

    Returns a fallback stub string if generation fails.
    """
    system = (
        "You are writing a short educational podcast script for school students. "
        "Two hosts: MAYA (curious, asks questions) and NIKO (explains clearly). "
        "Write exactly 6-8 exchanges. "
        "Format each line as 'MAYA: ...' or 'NIKO: ...' with no other text. "
        f"Use {language} throughout."
    )

    prompt = f"Write a podcast episode about: {topic}"

    script = _ollama_generate(prompt, temperature=0.8, max_tokens=800, system=system)
    if not script:
        return (
            f"MAYA: Today we're learning about {topic}!\n"
            f"NIKO: That's right. Unfortunately the AI model is offline right now.\n"
            f"MAYA: Let's try again later.\n"
            f"NIKO: See you next time!"
        )

    return script

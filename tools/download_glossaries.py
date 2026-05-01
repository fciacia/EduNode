#!/usr/bin/env python3
"""
tools/download_glossaries.py
============================
Step 1A — Download Tier-2 language glossary datasets from HuggingFace.
Normalises each dataset into a flat JSON array:
    [{"english": "...", "native": "..."}, ...]
and saves to data/glossaries/<language_lower>.json

Usage:
    python tools/download_glossaries.py              # all languages
    python tools/download_glossaries.py --lang Iban  # single language
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

# ── allow running from repo root without installing the package ────────────
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import GLOSSARY_DATASETS

logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")
log = logging.getLogger("glossaries")

GLOSSARY_DIR = Path("data/glossaries")
GLOSSARY_DIR.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# Normaliser functions — one per dataset schema
# ─────────────────────────────────────────────────────────────────────────────

def _normalise_cebuano(raw_rows: list[dict]) -> list[dict]:
    """
    filbench/cebuano-readability
    Schema: {"text": str, "label": int, ...}
    The texts are Cebuano sentences scored for reading difficulty.
    We emit each text as a native sample with an empty English field
    so the RAG-boost path can inject them as context.
    """
    result = []
    for row in raw_rows:
        text = (row.get("text") or "").strip()
        if text:
            result.append({"english": "", "native": text, "language": "Cebuano"})
    log.info("  Cebuano: %d text samples normalised", len(result))
    return result


def _normalise_iban(raw_rows: list[dict]) -> list[dict]:
    """
    VynerCK/Iban-language-data
    Schema: {"english": str, "iban": str, "word_mapping": {...}, "response": str}
    We emit the english→iban pairs plus individual word_mapping entries.
    """
    result = []
    for row in raw_rows:
        eng  = (row.get("english") or "").strip()
        iban = (row.get("iban")    or "").strip()
        if eng and iban:
            result.append({"english": eng, "native": iban, "language": "Iban"})
        # Also flatten word_mapping
        for eng_word, iban_word in (row.get("word_mapping") or {}).items():
            result.append({
                "english": eng_word.strip(),
                "native":  str(iban_word).strip(),
                "language": "Iban",
            })
    # Deduplicate by (english, native)
    seen = set()
    unique = []
    for entry in result:
        key = (entry["english"].lower(), entry["native"].lower())
        if key not in seen:
            seen.add(key)
            unique.append(entry)
    log.info("  Iban: %d unique pairs normalised", len(unique))
    return unique


# Map: HuggingFace dataset id → normaliser function
NORMALISERS: dict[str, tuple[str, callable]] = {
    "Cebuano": ("filbench/cebuano-readability", _normalise_cebuano),
    "Iban":    ("VynerCK/Iban-language-data",   _normalise_iban),
}


# ─────────────────────────────────────────────────────────────────────────────
# Download + save
# ─────────────────────────────────────────────────────────────────────────────

def download_glossary(language: str) -> Path:
    """Download and normalise one language glossary. Returns output path."""
    if language not in NORMALISERS:
        raise ValueError(
            f"No normaliser for '{language}'. "
            f"Available: {list(NORMALISERS)}"
        )

    dataset_id, normalise_fn = NORMALISERS[language]
    out_path = GLOSSARY_DIR / f"{language.lower()}.json"

    log.info("Downloading '%s' from HuggingFace dataset '%s'…", language, dataset_id)

    try:
        from datasets import load_dataset  # type: ignore
    except ImportError:
        log.error(
            "The 'datasets' library is required. Run: pip install datasets"
        )
        sys.exit(1)

    try:
        ds = load_dataset(dataset_id, split="train", trust_remote_code=False)
    except Exception as exc:
        log.error("Failed to load dataset '%s': %s", dataset_id, exc)
        raise

    raw_rows = [dict(row) for row in ds]
    normalised = normalise_fn(raw_rows)

    out_path.write_text(
        json.dumps(normalised, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    log.info("  Saved %d entries → %s", len(normalised), out_path)
    return out_path


def download_all() -> None:
    """Download every glossary listed in config.GLOSSARY_DATASETS."""
    errors: list[str] = []
    for language in GLOSSARY_DATASETS:
        try:
            download_glossary(language)
        except Exception as exc:
            log.warning("Skipping '%s': %s", language, exc)
            errors.append(language)

    if errors:
        log.warning("Could not download: %s", ", ".join(errors))
    else:
        log.info("All glossaries downloaded successfully.")


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download Tier-2 language glossaries from HuggingFace."
    )
    parser.add_argument(
        "--lang",
        metavar="LANGUAGE",
        help="Download a single language (e.g. Iban, Cebuano). Omit for all.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available languages and exit.",
    )
    args = parser.parse_args()

    if args.list:
        print("Available languages:")
        for lang, ds_id in GLOSSARY_DATASETS.items():
            print(f"  {lang:15s}  →  {ds_id}")
        return

    if args.lang:
        download_glossary(args.lang)
    else:
        download_all()


if __name__ == "__main__":
    main()

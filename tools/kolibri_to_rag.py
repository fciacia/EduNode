#!/usr/bin/env python3
"""
tools/kolibri_to_rag.py
=======================
Step 1B — Export Kolibri + Khan Academy content to plain-text files that
EduNode's RAG pipeline (core/rag_engine.py) can index.

What it does:
  1. Connects to the Kolibri SQLite database (no Kolibri server required).
  2. Queries the content metadata and document text.
  3. Groups output by subject and language.
  4. Writes one plain-text file per (subject, language) pair to:
         data/curriculum/kolibri_<subject>_<lang>.txt
  5. RAG ingest will pick these up on next startup.

Usage:
    python tools/kolibri_to_rag.py                    # auto-detect Kolibri DB
    python tools/kolibri_to_rag.py --db /path/to/db   # explicit DB path
    python tools/kolibri_to_rag.py --dry-run           # print counts only

Kolibri stores content in:
    ~/.kolibri/db.sqlite3        (user install)
    /var/kolibri/db.sqlite3      (system install)
"""

from __future__ import annotations

import argparse
import logging
import re
import sqlite3
import sys
from pathlib import Path

# ── allow running from repo root ───────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import AVAILABLE_SUBJECTS

logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")
log = logging.getLogger("kolibri_rag")

OUTPUT_DIR = Path("data/curriculum")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Default Kolibri DB locations (checked in order)
KOLIBRI_DB_CANDIDATES = [
    Path.home() / ".kolibri" / "db.sqlite3",
    Path("/var/kolibri/db.sqlite3"),
    Path("/home/kolibri/.kolibri/db.sqlite3"),
]

# Map Kolibri category strings to EduNode subjects (case-insensitive substring match)
SUBJECT_MAP: dict[str, str] = {
    "math":        "Mathematics",
    "algebra":     "Mathematics",
    "geometry":    "Mathematics",
    "arithmetic":  "Mathematics",
    "science":     "Science",
    "biology":     "Science",
    "chemistry":   "Science",
    "physics":     "Science",
    "english":     "English Language",
    "reading":     "English Language",
    "environment": "Environmental Studies",
    "ecology":     "Environmental Studies",
    "digital":     "Digital Literacy",
    "computing":   "Digital Literacy",
    "technology":  "Digital Literacy",
}


def _find_kolibri_db() -> Path | None:
    for candidate in KOLIBRI_DB_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


def _map_subject(title: str, description: str) -> str:
    """Return an EduNode subject name for a Kolibri content node, or 'General'."""
    text = (title + " " + description).lower()
    for keyword, subject in SUBJECT_MAP.items():
        if keyword in text:
            return subject
    return "General"


def _clean_html(text: str) -> str:
    """Strip HTML tags and normalise whitespace."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&[a-zA-Z]+;", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def export_kolibri_content(db_path: Path, dry_run: bool = False) -> None:
    """Read Kolibri SQLite DB and write curriculum text files for RAG."""
    log.info("Opening Kolibri database: %s", db_path)

    # Kolibri's main content database schema (applies to Kolibri ≥ 0.15)
    # Table: content_contentnode  — one row per content item
    # Columns we use: title, description, lang_id, kind, available
    #
    # Kolibri also has a separate annotation/text database.
    # We extract what is available in the metadata DB; full document text
    # is stored in the channel-specific content SQLite files at:
    #   ~/.kolibri/content/databases/<channel_id>.sqlite3
    # Those are also queried when present.

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        nodes = conn.execute(
            """
            SELECT title, description, lang_id, kind, available
            FROM content_contentnode
            WHERE available = 1
              AND kind IN ('document', 'video', 'exercise', 'topic')
              AND title IS NOT NULL
              AND title != ''
            ORDER BY kind, title
            """
        ).fetchall()
    except sqlite3.OperationalError as exc:
        log.error("Could not query Kolibri DB: %s", exc)
        log.error("Ensure Kolibri has been started at least once so its DB is initialised.")
        conn.close()
        return

    conn.close()

    log.info("Found %d available content nodes.", len(nodes))

    # Group text by (subject, lang)
    buckets: dict[tuple[str, str], list[str]] = {}
    for row in nodes:
        subject = _map_subject(row["title"] or "", row["description"] or "")
        lang    = (row["lang_id"] or "en").split("-")[0].lower()  # e.g. "en-US" → "en"
        key     = (subject, lang)

        title = _clean_html(row["title"] or "")
        desc  = _clean_html(row["description"] or "")

        if title:
            buckets.setdefault(key, []).append(f"## {title}\n{desc}" if desc else f"## {title}")

    # Also scan channel content databases for document text
    content_db_dir = db_path.parent / "content" / "databases"
    if content_db_dir.exists():
        for channel_db in sorted(content_db_dir.glob("*.sqlite3")):
            _extract_channel_text(channel_db, buckets)

    if dry_run:
        log.info("Dry run — files that would be created:")
        for (subject, lang), items in sorted(buckets.items()):
            log.info("  kolibri_%s_%s.txt  (%d sections)", subject.replace(" ", "_"), lang, len(items))
        return

    written = 0
    for (subject, lang), items in sorted(buckets.items()):
        safe_subject = subject.replace(" ", "_")
        out_file = OUTPUT_DIR / f"kolibri_{safe_subject}_{lang}.txt"
        content = "\n\n".join(items)
        out_file.write_text(content, encoding="utf-8")
        log.info("  Wrote %d sections → %s", len(items), out_file)
        written += 1

    log.info("Done. %d curriculum files written to %s/", written, OUTPUT_DIR)


def _extract_channel_text(
    channel_db: Path,
    buckets: dict[tuple[str, str], list[str]],
) -> None:
    """Extract document text from a Kolibri channel content SQLite file."""
    try:
        conn = sqlite3.connect(channel_db)
        conn.row_factory = sqlite3.Row

        # The exact schema varies; attempt the most common table/column names
        try:
            rows = conn.execute(
                "SELECT title, description, lang FROM document WHERE title IS NOT NULL"
            ).fetchall()
        except sqlite3.OperationalError:
            conn.close()
            return

        for row in rows:
            subject = _map_subject(row["title"] or "", row["description"] or "")
            lang    = (row["lang"] or "en").split("-")[0].lower()
            key     = (subject, lang)
            title   = _clean_html(row["title"] or "")
            desc    = _clean_html(row["description"] or "")
            if title:
                buckets.setdefault(key, []).append(f"## {title}\n{desc}" if desc else f"## {title}")

        conn.close()
    except Exception as exc:  # noqa: BLE001
        log.debug("Could not read channel DB %s: %s", channel_db.name, exc)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export Kolibri/Khan Academy content to RAG-ready text files."
    )
    parser.add_argument(
        "--db",
        metavar="PATH",
        help="Path to Kolibri's db.sqlite3 (auto-detected if omitted).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be created without writing files.",
    )
    args = parser.parse_args()

    if args.db:
        db_path = Path(args.db)
    else:
        db_path = _find_kolibri_db()

    if db_path is None or not db_path.exists():
        log.error(
            "Kolibri database not found. Have you run Kolibri at least once?\n"
            "  python -m kolibri start\n"
            "Or specify the path with --db /path/to/db.sqlite3"
        )
        sys.exit(1)

    export_kolibri_content(db_path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

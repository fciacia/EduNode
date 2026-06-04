#!/usr/bin/env python3
"""
ingest.py — bulk-load curriculum into Edge's vector store.

Point it at a folder of PDFs/TXT/MD (e.g. a USB drive of OER textbooks) and it
copies them into the curriculum directory and indexes them into ChromaDB.

    python ingest.py                 # (re)index data/curriculum
    python ingest.py /media/usb/oer  # copy + index every file in that folder

Files are chunked and embedded with the configured EMBED_MODEL. Re-running is
idempotent (deterministic chunk IDs), so it is safe to run repeatedly.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from core.rag_engine import CURRICULUM_DIR, get_collection, ingest_pdfs

_SUFFIXES = (".pdf", ".txt", ".md")


def main(argv: list[str]) -> int:
    src = Path(argv[1]) if len(argv) > 1 else CURRICULUM_DIR
    if not src.exists():
        print(f"Path not found: {src}")
        return 1

    CURRICULUM_DIR.mkdir(parents=True, exist_ok=True)

    # If given a different folder, copy its curriculum files in first.
    if src.is_dir() and src.resolve() != CURRICULUM_DIR.resolve():
        files = [p for p in sorted(src.iterdir())
                 if p.suffix.lower() in _SUFFIXES
                 and p.name.upper() not in {"ATTRIBUTIONS.MD", "README.MD", "LICENSE.MD"}]
        if not files:
            print(f"No .pdf/.txt/.md files found in {src}")
            return 1
        for f in files:
            shutil.copy2(f, CURRICULUM_DIR / f.name)
            print(f"  + copied {f.name}")
    elif src.is_file():
        shutil.copy2(src, CURRICULUM_DIR / src.name)
        print(f"  + copied {src.name}")

    print("\nIndexing… (first run downloads the embedding model)")
    added = ingest_pdfs(CURRICULUM_DIR)
    total = get_collection().count()
    print(f"\nDone. New chunks this run: {added}  |  total chunks indexed: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

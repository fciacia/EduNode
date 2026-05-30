"""
core/rag_engine.py
==================
Step 3 — Offline RAG pipeline.

Ingests PDF and plain-text curriculum files into ChromaDB, then exposes
retrieve_context() for use by all other modules.

Public API
----------
ingest_pdfs(curriculum_dir=None)
    Idempotent. Reads every .pdf and .txt in curriculum_dir, chunks into
    ~300-word passages, and upserts into ChromaDB.  Safe to call at startup.

retrieve_context(query, n_results=3, subject=None) -> str
    Returns the top-N most relevant passages as a single string, ready to
    inject into an LLM prompt.

get_collection() -> chromadb.Collection
    Low-level access for testing.
"""

from __future__ import annotations

import hashlib
import logging
import os
import re
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Lazy imports — heavy libraries loaded on first use so startup is fast
# ---------------------------------------------------------------------------
_chroma_client = None
_collection = None

CHROMA_DIR      = Path(os.getenv("CHROMA_DIR", "data/chroma"))
CURRICULUM_DIR  = Path(os.getenv("CURRICULUM_DIR", "data/curriculum"))
COLLECTION_NAME = "edunode"
CHUNK_SIZE      = int(os.getenv("CHUNK_SIZE", "300"))   # words per chunk
CHUNK_OVERLAP   = int(os.getenv("CHUNK_OVERLAP", "30"))  # word overlap
EMBED_MODEL     = os.getenv("EMBED_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")


# ---------------------------------------------------------------------------
# ChromaDB initialisation
# ---------------------------------------------------------------------------

def get_collection():
    """Return (creating if necessary) the persistent ChromaDB collection."""
    global _chroma_client, _collection
    if _collection is not None:
        return _collection

    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError(
            "chromadb and sentence-transformers are required. "
            "Run: pip install chromadb sentence-transformers"
        ) from exc

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    _chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    _collection = _chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=_SharedEmbeddingFunction(),
        metadata={"hnsw:space": "cosine"},
    )
    log.info("ChromaDB collection '%s' ready (%d docs).", COLLECTION_NAME, _collection.count())
    return _collection


# ---------------------------------------------------------------------------
# Text extraction helpers
# ---------------------------------------------------------------------------

def _extract_text_pdf(path: Path) -> str:
    """Extract plain text from a PDF file using pypdf."""
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("pypdf is required: pip install pypdf") from exc

    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return "\n".join(pages)


def _extract_text_txt(path: Path) -> str:
    """Read a plain-text file, tolerating encoding errors."""
    return path.read_text(encoding="utf-8", errors="replace")


def _extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _extract_text_pdf(path)
    if suffix in (".txt", ".md"):
        return _extract_text_txt(path)
    log.debug("Unsupported file type '%s' — skipping.", path.name)
    return ""


def _extract_pages(path: Path) -> list[str]:
    """
    Return a list of page texts. PDFs use real page boundaries; txt/md files
    are treated as a single page.
    """
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("pypdf is required: pip install pypdf") from exc
        reader = PdfReader(str(path))
        return [(page.extract_text() or "") for page in reader.pages]
    if suffix in (".txt", ".md"):
        return [path.read_text(encoding="utf-8", errors="replace")]
    log.debug("Unsupported file type '%s' — skipping.", path.name)
    return []


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

def _chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Split *text* into overlapping word-count chunks.
    Returns a list of non-empty strings.
    """
    # Normalise whitespace
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []

    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start += chunk_size - overlap

    return [c for c in chunks if c]


def _chunk_pages(pages: list[str]) -> list[dict]:
    """
    Chunk a list of page texts, preserving the 1-based page number on each chunk.
    Returns [{"text": str, "page": int}, ...].
    """
    out: list[dict] = []
    for page_no, page_text in enumerate(pages, start=1):
        for chunk in _chunk_text(page_text):
            out.append({"text": chunk, "page": page_no})
    return out


# ---------------------------------------------------------------------------
# Chunk ID generation
# ---------------------------------------------------------------------------

def _chunk_id(filename: str, index: int, text: str) -> str:
    """
    Deterministic 16-char ID for a chunk — makes upsert idempotent.
    sha1(filename + str(index) + first_60_chars)[:16]
    """
    raw = f"{filename}|{index}|{text[:60]}"
    return hashlib.sha1(raw.encode(), usedforsecurity=False).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Subject detection from filename
# ---------------------------------------------------------------------------

_SUBJECT_KEYWORDS: dict[str, list[str]] = {
    "Mathematics":          ["math", "algebra", "geometry", "arithmetic", "calculus", "statistics"],
    "Science":              ["science", "biology", "chemistry", "physics", "ecology", "nature"],
    "English Language":     ["english", "reading", "writing", "grammar", "literature"],
    "Environmental Studies":["environment", "ecology", "climate", "geography", "earth"],
    "Digital Literacy":     ["digital", "computing", "technology", "computer", "internet", "ict"],
}


def _detect_subject(filename: str) -> str:
    name = filename.lower()
    for subject, keywords in _SUBJECT_KEYWORDS.items():
        if any(kw in name for kw in keywords):
            return subject
    return "General"


# ---------------------------------------------------------------------------
# Ingest
# ---------------------------------------------------------------------------

def ingest_pdfs(curriculum_dir: Optional[Path | str] = None) -> int:
    """
    Ingest all PDF and TXT files in *curriculum_dir* into ChromaDB.

    Idempotent — chunks are upserted using deterministic IDs so re-running
    on the same files does not duplicate data.

    Returns the number of new chunks added.
    """
    cdir = Path(curriculum_dir) if curriculum_dir else CURRICULUM_DIR
    if not cdir.exists():
        log.warning("Curriculum directory '%s' does not exist — nothing to ingest.", cdir)
        return 0

    collection = get_collection()

    files = sorted(cdir.glob("**/*.pdf")) + sorted(cdir.glob("**/*.txt")) + sorted(cdir.glob("**/*.md"))
    if not files:
        log.info("No curriculum files found in '%s'.", cdir)
        return 0

    total_added = 0

    for file_path in files:
        log.info("Ingesting '%s'…", file_path.name)
        try:
            pages = _extract_pages(file_path)
        except Exception as exc:
            log.warning("Could not read '%s': %s", file_path.name, exc)
            continue

        if not any(p.strip() for p in pages):
            log.debug("'%s' yielded no text — skipping.", file_path.name)
            continue

        page_chunks = _chunk_pages(pages)
        if not page_chunks:
            continue

        subject = _detect_subject(file_path.name)

        chunks    = [pc["text"] for pc in page_chunks]
        ids       = [_chunk_id(file_path.name, i, pc["text"]) for i, pc in enumerate(page_chunks)]
        metadatas = [
            {"source": file_path.name, "subject": subject, "grade": "general",
             "page": pc["page"], "chunk_index": i}
            for i, pc in enumerate(page_chunks)
        ]

        # Upsert in batches of 100 to keep memory usage low on the Pi
        batch_size = 100
        for batch_start in range(0, len(chunks), batch_size):
            b_end  = batch_start + batch_size
            collection.upsert(
                ids=ids[batch_start:b_end],
                documents=chunks[batch_start:b_end],
                metadatas=metadatas[batch_start:b_end],
            )

        total_added += len(chunks)
        log.info("  '%s' → %d chunks (subject: %s)", file_path.name, len(chunks), subject)

    log.info("Ingest complete. Total chunks upserted: %d. Collection size: %d.", total_added, collection.count())
    return total_added


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------

def retrieve_context(
    query: str,
    n_results: int = 3,
    subject: Optional[str] = None,
) -> str:
    """
    Query ChromaDB for the top-N passages most relevant to *query*.

    Parameters
    ----------
    query     : The user question or topic string.
    n_results : How many passages to return (default 3).
    subject   : Optional subject filter (e.g. "Mathematics").

    Returns
    -------
    A single string with passages separated by "\\n---\\n", ready to inject
    into an LLM prompt as context.  Returns "" if nothing is found.
    """
    collection = get_collection()
    if collection.count() == 0:
        log.debug("Collection is empty — returning empty context.")
        return ""

    query_params: dict = {
        "query_texts": [query],
        "n_results": min(n_results, collection.count()),
        "include": ["documents", "metadatas", "distances"],
    }

    if subject and subject != "General":
        query_params["where"] = {"subject": subject}

    try:
        results = collection.query(**query_params)
    except Exception as exc:
        log.warning("ChromaDB query failed: %s", exc)
        return ""

    docs = results.get("documents", [[]])[0]
    if not docs:
        return ""

    return "\n---\n".join(docs)


# ---------------------------------------------------------------------------
# Embedder accessor (shared with the verification agent)
# ---------------------------------------------------------------------------
_embedder = None


def get_embedder():
    """Return a cached SentenceTransformer for the configured EMBED_MODEL."""
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder


try:
    from chromadb import EmbeddingFunction as _ChromaEmbeddingFunction
except Exception:  # pragma: no cover - chromadb is always installed in practice
    _ChromaEmbeddingFunction = object


class _SharedEmbeddingFunction(_ChromaEmbeddingFunction):
    """ChromaDB embedding function backed by the single shared SentenceTransformer.

    Using this (instead of Chroma's own SentenceTransformerEmbeddingFunction) keeps
    the embedding model in memory exactly once — reused by both retrieval and the
    verification agent — instead of loading it twice.
    """

    def __call__(self, input):
        return get_embedder().encode(list(input)).tolist()

    def name(self) -> str:
        return "edunode_shared_embedder"


# ---------------------------------------------------------------------------
# Citation-aware retrieval
# ---------------------------------------------------------------------------
def retrieve_with_citations(query: str, n_results: int = 3, subject=None) -> list:
    """
    Like retrieve_context but returns structured Chunk objects carrying
    source/page/distance for citation and verification.
    """
    from core.agents import Chunk

    collection = get_collection()
    if collection.count() == 0:
        return []

    params: dict = {
        "query_texts": [query],
        "n_results": min(n_results, collection.count()),
        "include": ["documents", "metadatas", "distances"],
    }
    if subject and subject != "General":
        params["where"] = {"subject": subject}

    try:
        res = collection.query(**params)
    except Exception as exc:
        log.warning("ChromaDB citation query failed: %s", exc)
        return []

    docs  = res.get("documents",  [[]])[0]
    metas = res.get("metadatas",  [[]])[0]
    dists = res.get("distances",  [[]])[0]

    chunks = []
    for doc, meta, dist in zip(docs, metas, dists):
        meta = meta or {}
        chunks.append(Chunk(
            text=doc,
            source=meta.get("source", "unknown"),
            page=int(meta.get("page", 1)),
            distance=float(dist),
        ))
    return chunks

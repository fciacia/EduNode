"""Tests for page-aware chunking and citation retrieval."""
import core.rag_engine as rag
from core.agents import Chunk


def test_chunk_pages_extracts_per_page_chunks():
    pages = ["Photosynthesis happens in leaves. " * 30,   # page 1 text
             "Mitochondria make energy. " * 30]            # page 2 text
    chunked = rag._chunk_pages(pages)
    # Every chunk carries the 1-based page it came from
    assert all("page" in c and "text" in c for c in chunked)
    page_numbers = {c["page"] for c in chunked}
    assert page_numbers == {1, 2}


def test_retrieve_with_citations_returns_chunk_objects(tmp_path, monkeypatch):
    # Isolate ChromaDB + curriculum to a temp dir
    monkeypatch.setattr(rag, "CHROMA_DIR", tmp_path / "chroma")
    monkeypatch.setattr(rag, "_collection", None)
    monkeypatch.setattr(rag, "_chroma_client", None)
    # Pin to the small, locally-cached embedder so tests stay fast and offline.
    monkeypatch.setattr(rag, "EMBED_MODEL", "all-MiniLM-L6-v2")
    monkeypatch.setattr(rag, "_embedder", None)
    cdir = tmp_path / "curriculum"
    cdir.mkdir()
    (cdir / "science.txt").write_text(
        "Photosynthesis is how plants make food from sunlight. " * 40,
        encoding="utf-8",
    )

    rag.ingest_pdfs(cdir)
    results = rag.retrieve_with_citations("How do plants make food?", n_results=2)

    assert len(results) >= 1
    assert isinstance(results[0], Chunk)
    assert results[0].source == "science.txt"
    assert results[0].page >= 1
    assert 0.0 <= results[0].distance <= 2.0

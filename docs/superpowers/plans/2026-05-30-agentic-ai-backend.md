# Agentic AI Backend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace EduNode's single RAG-call chat backend with a 4-agent pipeline (Translation → Context → Pedagogy → Verification) that produces page-level citations and confidence scores, aligning the code with the UM-Gunners "Edge" Technical Roadmap.

**Architecture:** A new `core/agents/` package. An orchestrator sequences four small, independently testable agent modules and owns two confidence gates. `query_tutor()` becomes a thin wrapper; `/api/chat` returns a backward-compatible payload with new `confidence`/`citations`/`needs_review` fields. NLLB-200 provides real neural translation (glossary fallback for unsupported languages); page-level citations come from per-page PDF chunking.

**Tech Stack:** Python 3.11, Flask, ChromaDB, sentence-transformers (`paraphrase-multilingual-MiniLM-L12-v2`), Ollama (`phi3:mini`), HuggingFace `transformers` (`facebook/nllb-200-distilled-600M`), pytest.

**Spec:** `docs/superpowers/specs/2026-05-30-agentic-ai-backend-design.md`

---

## File Structure

| File | Responsibility | Action |
|---|---|---|
| `requirements.txt` | Add `transformers`, `pytest` | Modify |
| `pytest.ini` | Pytest config, test discovery | Create |
| `tests/conftest.py` | Shared fixtures (temp DB, temp Chroma) | Create |
| `core/agents/__init__.py` | Shared dataclasses: `Chunk`, `StudentContext`, `Verification` | Create |
| `core/rag_engine.py` | Add `get_embedder()`, `retrieve_with_citations()`; per-page chunking | Modify |
| `core/agents/translation.py` | NLLB-200 `to_english` / `to_native` + FLORES map + glossary fallback | Create |
| `core/agents/context.py` | Build `StudentContext` from SQLite | Create |
| `core/agents/pedagogy.py` | Phi-3 grounded reasoning | Create |
| `core/agents/verification.py` | Confidence scoring + citation extraction | Create |
| `core/agents/orchestrator.py` | `run_pipeline()` — sequences agents, owns gates | Create |
| `core/llm_engine.py` | `query_tutor()` → wrapper over orchestrator | Modify |
| `config.py` | `SLM_MODEL = "phi3:mini"`, `EMBED_MODEL` constant | Modify |
| `app.py` | `/api/chat` passes through new payload, resolves student before pipeline | Modify |

**Test files:** `tests/test_rag_citations.py`, `tests/agents/test_translation.py`, `tests/agents/test_context.py`, `tests/agents/test_pedagogy.py`, `tests/agents/test_verification.py`, `tests/agents/test_orchestrator.py`.

---

## Task 0: Test Infrastructure

**Files:**
- Modify: `requirements.txt`
- Create: `pytest.ini`
- Create: `tests/__init__.py`
- Create: `tests/agents/__init__.py`
- Create: `tests/conftest.py`

- [ ] **Step 1: Add dependencies to requirements.txt**

Append these lines to `requirements.txt`:

```
transformers>=4.40
pytest>=8.0
```

- [ ] **Step 2: Install**

Run: `pip install -r requirements.txt`
Expected: completes with no errors.

- [ ] **Step 3: Create pytest.ini**

Create `pytest.ini`:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v
```

- [ ] **Step 4: Create empty package markers**

Create `tests/__init__.py` (empty file).
Create `tests/agents/__init__.py` (empty file).

- [ ] **Step 5: Create shared fixtures**

Create `tests/conftest.py`:

```python
"""Shared pytest fixtures for EduNode tests."""
import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_db(monkeypatch):
    """Point progress_tracker at a throwaway SQLite file."""
    with tempfile.TemporaryDirectory() as d:
        db_path = Path(d) / "test.db"
        monkeypatch.setenv("DB_PATH", str(db_path))
        # progress_tracker reads DB_PATH at import time, so patch the module global too
        import core.progress_tracker as pt
        monkeypatch.setattr(pt, "DB_PATH", db_path)
        pt.init_db()
        yield db_path
```

- [ ] **Step 6: Verify pytest runs (no tests yet)**

Run: `pytest`
Expected: "no tests ran" (exit code 5) — confirms discovery works without errors.

- [ ] **Step 7: Commit**

```bash
git add requirements.txt pytest.ini tests/
git commit -m "test: add pytest infrastructure and shared fixtures"
```

---

## Task 1: Shared Dataclasses

**Files:**
- Create: `core/agents/__init__.py`
- Test: `tests/agents/test_types.py`

- [ ] **Step 1: Write the failing test**

Create `tests/agents/test_types.py`:

```python
from core.agents import Chunk, StudentContext, Verification


def test_chunk_holds_citation_fields():
    c = Chunk(text="Water boils at 100C.", source="science.pdf", page=12, distance=0.2)
    assert c.source == "science.pdf"
    assert c.page == 12
    assert c.distance == 0.2


def test_student_context_defaults():
    ctx = StudentContext(grade="7", avg_score=82.0, weak_subjects=["Mathematics"], difficulty="standard")
    assert ctx.difficulty == "standard"
    assert "Mathematics" in ctx.weak_subjects


def test_verification_needs_review_flag():
    v = Verification(confidence=0.5, citations=[{"source": "a.pdf", "page": 1}], needs_review=True)
    assert v.needs_review is True
    assert v.citations[0]["page"] == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/agents/test_types.py -v`
Expected: FAIL — `ImportError: cannot import name 'Chunk' from 'core.agents'`.

- [ ] **Step 3: Write minimal implementation**

Create `core/agents/__init__.py`:

```python
"""
core/agents
===========
Agentic RAG pipeline for EduNode. Shared data types live here; each agent is a
sibling module (translation, context, pedagogy, verification) and the
orchestrator sequences them.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Chunk:
    """A retrieved curriculum passage with its citation metadata."""
    text: str
    source: str
    page: int
    distance: float


@dataclass
class StudentContext:
    """Personalisation hints derived from a student's history."""
    grade: str
    avg_score: float
    weak_subjects: list = field(default_factory=list)
    difficulty: str = "standard"   # one of: simple | standard | challenge


@dataclass
class Verification:
    """Output of the Verification Agent."""
    confidence: float
    citations: list = field(default_factory=list)   # list of {"source": str, "page": int}
    needs_review: bool = False
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/agents/test_types.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add core/agents/__init__.py tests/agents/test_types.py
git commit -m "feat: add shared agent dataclasses (Chunk, StudentContext, Verification)"
```

---

## Task 2: RAG Per-Page Chunking + Citation Retrieval

**Files:**
- Modify: `core/rag_engine.py`
- Test: `tests/test_rag_citations.py`

This task makes the chunker record page numbers and adds `retrieve_with_citations()` returning `Chunk` objects. The existing `retrieve_context()` and `ingest_pdfs()` signatures are preserved.

- [ ] **Step 1: Write the failing test**

Create `tests/test_rag_citations.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_rag_citations.py -v`
Expected: FAIL — `AttributeError: module 'core.rag_engine' has no attribute '_chunk_pages'`.

- [ ] **Step 3: Add per-page chunking helper**

In `core/rag_engine.py`, add this function directly after the existing `_chunk_text` function (around line 143):

```python
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
```

- [ ] **Step 4: Add a per-page extraction helper**

In `core/rag_engine.py`, add this new function directly after `_extract_text` (around line 113). Leave the existing `_extract_text`, `_extract_text_pdf`, and `_extract_text_txt` functions in place — they are small and harmless; `_extract_pages` becomes the one used by `ingest_pdfs`:

```python
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
```

- [ ] **Step 5: Use per-page chunking in ingest_pdfs**

In `core/rag_engine.py`, inside `ingest_pdfs`, replace the body of the per-file loop that reads/chunks text. Replace lines 208-228 (the `try/except` extraction block through the `metadatas` list comprehension) with:

```python
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
```

Note: the existing `_extract_text` function and the batch-upsert loop below this block stay unchanged.

- [ ] **Step 6: Add embedder accessor and retrieve_with_citations**

In `core/rag_engine.py`, add at the end of the file:

```python
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
```

- [ ] **Step 7: Run tests to verify they pass**

Run: `pytest tests/test_rag_citations.py -v`
Expected: 2 passed. (First run downloads the embedding model — may take a minute.)

- [ ] **Step 8: Verify existing retrieval still works**

Run: `python -c "import core.rag_engine"`
Expected: no import errors.

- [ ] **Step 9: Commit**

```bash
git add core/rag_engine.py tests/test_rag_citations.py
git commit -m "feat: per-page chunking and citation-aware retrieval"
```

---

## Task 3: Config — Models & Embedder

**Files:**
- Modify: `config.py`
- Modify: `.env.example`

This task switches the default reasoning model to `phi3:mini` and centralises the multilingual embedder. The Ollama wrapper already falls back to an available model if `phi3:mini` is absent, so this is non-breaking.

- [ ] **Step 1: Update config.py active hub block**

In `config.py`, in the active (uncommented) hub block, change:

```python
SLM_MODEL     = "llama3.2:3b-instruct-q4_K_M"
```

to:

```python
SLM_MODEL     = "phi3:mini"
```

Then add this line directly below the `SLM_MODEL` line:

```python
EMBED_MODEL   = "paraphrase-multilingual-MiniLM-L12-v2"
```

- [ ] **Step 2: Update .env.example**

In `.env.example`, change:

```ini
OLLAMA_MODEL=llama3.2:3b-instruct-q4_K_M
EMBED_MODEL=all-MiniLM-L6-v2
```

to:

```ini
OLLAMA_MODEL=phi3:mini
EMBED_MODEL=paraphrase-multilingual-MiniLM-L12-v2
```

- [ ] **Step 3: Verify config imports**

Run: `python -c "import config; print(config.SLM_MODEL, config.EMBED_MODEL)"`
Expected: `phi3:mini paraphrase-multilingual-MiniLM-L12-v2`

- [ ] **Step 4: Commit**

```bash
git add config.py .env.example
git commit -m "config: switch to phi3:mini and multilingual embedder"
```

> **Operational note (not a code step):** because the embedder changed, the curriculum must be re-ingested into a fresh ChromaDB (`rm -rf data/chroma && python -c "from core.rag_engine import ingest_pdfs; ingest_pdfs()"`). The old `all-MiniLM-L6-v2` vectors are incompatible with the new model.

---

## Task 4: Translation Agent

**Files:**
- Create: `core/agents/translation.py`
- Test: `tests/agents/test_translation.py`

NLLB-200 neural translation with FLORES-200 codes. English is pass-through. Languages not in NLLB fall back to the existing glossary bridge in `llm_engine`.

- [ ] **Step 1: Write the failing test**

Create `tests/agents/test_translation.py`:

```python
import core.agents.translation as tr


def test_english_is_passthrough():
    assert tr.to_english("Hello there", "English") == "Hello there"
    assert tr.to_native("Hello there", "English") == "Hello there"


def test_flores_code_lookup():
    assert tr.flores_code("Bahasa Melayu") == "zsm_Latn"
    assert tr.flores_code("Iban") == "iba_Latn"
    assert tr.flores_code("English") == "eng_Latn"
    assert tr.flores_code("Klingon") is None   # unsupported


def test_to_english_uses_nllb_for_supported_language(monkeypatch):
    calls = {}

    def fake_translate(text, src, tgt):
        calls["args"] = (text, src, tgt)
        return "translated-to-english"

    monkeypatch.setattr(tr, "_nllb_translate", fake_translate)
    out = tr.to_english("Apa itu air?", "Bahasa Melayu")
    assert out == "translated-to-english"
    assert calls["args"] == ("Apa itu air?", "zsm_Latn", "eng_Latn")


def test_unsupported_language_falls_back_to_glossary(monkeypatch):
    # Kedayan has no FLORES code → to_native uses the glossary bridge
    monkeypatch.setattr(
        "core.llm_engine._bridge_translate",
        lambda text, lang: f"[English] {text}\n[{lang}] (glossary)",
    )
    out = tr.to_native("Water is essential.", "Kedayan")
    assert "glossary" in out
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/agents/test_translation.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'core.agents.translation'`.

- [ ] **Step 3: Write implementation**

Create `core/agents/translation.py`:

```python
"""
core/agents/translation.py
===========================
Multilingual Translation Agent. Bridges student mother-tongue <-> English using
NLLB-200. English is pass-through. Languages without a FLORES-200 code fall back
to the existing glossary bridge in llm_engine.
"""
from __future__ import annotations

import logging

log = logging.getLogger(__name__)

NLLB_MODEL = "facebook/nllb-200-distilled-600M"

# Hub language name -> FLORES-200 code. Extend as new hubs are added.
_FLORES: dict[str, str] = {
    "English":          "eng_Latn",
    "Bahasa Melayu":    "zsm_Latn",
    "Bahasa Indonesia": "ind_Latn",
    "Filipino":         "fil_Latn",
    "Vietnamese":       "vie_Latn",
    "Iban":             "iba_Latn",
    "Cebuano":          "ceb_Latn",
    "Sundanese":        "sun_Latn",
}

_model = None
_tokenizer = None


def flores_code(language: str) -> str | None:
    """Return the FLORES-200 code for a hub language name, or None if unsupported."""
    return _FLORES.get(language)


def _load():
    """Lazy-load the NLLB-200 model + tokenizer (cached singletons)."""
    global _model, _tokenizer
    if _model is None:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        _tokenizer = AutoTokenizer.from_pretrained(NLLB_MODEL)
        _model = AutoModelForSeq2SeqLM.from_pretrained(NLLB_MODEL)
    return _model, _tokenizer


def _nllb_translate(text: str, src_code: str, tgt_code: str) -> str:
    """Translate text from src FLORES code to tgt FLORES code via NLLB-200."""
    model, tokenizer = _load()
    tokenizer.src_lang = src_code
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    bos = tokenizer.convert_tokens_to_ids(tgt_code)
    generated = model.generate(**inputs, forced_bos_token_id=bos, max_length=512)
    return tokenizer.batch_decode(generated, skip_special_tokens=True)[0].strip()


def to_english(text: str, language: str) -> str:
    """Translate a student query into English. English passes through unchanged."""
    if language == "English":
        return text
    code = flores_code(language)
    if code is None:
        log.info("No FLORES code for '%s' — passing query through untranslated.", language)
        return text
    try:
        return _nllb_translate(text, code, "eng_Latn")
    except Exception as exc:  # noqa: BLE001
        log.warning("NLLB to_english failed for '%s': %s — using original text.", language, exc)
        return text


def to_native(text: str, language: str) -> str:
    """
    Translate an English answer into the student's language.
    English passes through. Unsupported languages use the glossary bridge.
    """
    if language == "English":
        return text
    code = flores_code(language)
    if code is None:
        from core.llm_engine import _bridge_translate
        return _bridge_translate(text, language)
    try:
        return _nllb_translate(text, "eng_Latn", code)
    except Exception as exc:  # noqa: BLE001
        log.warning("NLLB to_native failed for '%s': %s — using glossary bridge.", language, exc)
        from core.llm_engine import _bridge_translate
        return _bridge_translate(text, language)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/agents/test_translation.py -v`
Expected: 4 passed. (No model download — NLLB calls are mocked.)

- [ ] **Step 5: Commit**

```bash
git add core/agents/translation.py tests/agents/test_translation.py
git commit -m "feat: translation agent (NLLB-200 + glossary fallback)"
```

---

## Task 5: Context Agent

**Files:**
- Create: `core/agents/context.py`
- Test: `tests/agents/test_context.py`

Builds a `StudentContext` from the existing SQLite tables. No schema change. Difficulty is inferred from recent quiz average when present.

- [ ] **Step 1: Write the failing test**

Create `tests/agents/test_context.py`:

```python
import core.agents.context as ctx_agent
from core.agents import StudentContext


def test_missing_student_returns_safe_defaults(temp_db):
    ctx = ctx_agent.build(student_id=9999)   # no such student
    assert isinstance(ctx, StudentContext)
    assert ctx.grade == "general"
    assert ctx.difficulty == "standard"


def test_low_average_yields_simple_difficulty(temp_db):
    import core.progress_tracker as pt
    sid = pt.get_or_create_student("Ana", "English", grade=7)
    pt.log_quiz_result(sid, "Fractions", score=2, total=10)   # 20%
    ctx = ctx_agent.build(sid)
    assert ctx.difficulty == "simple"
    assert ctx.grade == "7"


def test_high_average_yields_challenge_difficulty(temp_db):
    import core.progress_tracker as pt
    sid = pt.get_or_create_student("Ben", "English", grade=8)
    pt.log_quiz_result(sid, "Algebra", score=9, total=10)   # 90%
    ctx = ctx_agent.build(sid)
    assert ctx.difficulty == "challenge"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/agents/test_context.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'core.agents.context'`.

- [ ] **Step 3: Write implementation**

Create `core/agents/context.py`:

```python
"""
core/agents/context.py
======================
Personalised Context Agent. Reads a student's grade and recent quiz performance
from SQLite and derives a difficulty hint for the pedagogy agent.
"""
from __future__ import annotations

import logging

from core.agents import StudentContext

log = logging.getLogger(__name__)


def _difficulty_from_average(avg_pct: float | None) -> str:
    if avg_pct is None:
        return "standard"
    if avg_pct < 50:
        return "simple"
    if avg_pct >= 85:
        return "challenge"
    return "standard"


def build(student_id: int | None) -> StudentContext:
    """Build a StudentContext from the student's history. Safe defaults if unknown."""
    default = StudentContext(grade="general", avg_score=0.0, weak_subjects=[], difficulty="standard")
    if not student_id:
        return default

    try:
        import core.progress_tracker as pt
        with pt._db() as conn:
            srow = conn.execute(
                "SELECT grade FROM students WHERE id=?", (student_id,)
            ).fetchone()
            if not srow:
                return default

            qrows = conn.execute(
                "SELECT topic, score, total FROM quiz_results"
                " WHERE student_id=? AND total>0 ORDER BY taken_at DESC LIMIT 10",
                (student_id,),
            ).fetchall()
    except Exception as exc:  # noqa: BLE001
        log.warning("Context build failed for student %s: %s", student_id, exc)
        return default

    grade = str(srow["grade"]) if srow["grade"] else "general"

    if qrows:
        pcts = [r["score"] / r["total"] * 100 for r in qrows]
        avg = sum(pcts) / len(pcts)
        weak = sorted({r["topic"] for r in qrows if r["score"] / r["total"] < 0.5})
    else:
        avg = None
        weak = []

    return StudentContext(
        grade=grade,
        avg_score=round(avg, 1) if avg is not None else 0.0,
        weak_subjects=weak,
        difficulty=_difficulty_from_average(avg),
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/agents/test_context.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add core/agents/context.py tests/agents/test_context.py
git commit -m "feat: context agent (student profile -> difficulty hint)"
```

---

## Task 6: Pedagogy Agent

**Files:**
- Create: `core/agents/pedagogy.py`
- Test: `tests/agents/test_pedagogy.py`

Grounded reasoning via Phi-3 (reuses `llm_engine._ollama_generate`). The prompt must include the difficulty hint and the retrieved chunks, and instruct the model to answer only from those chunks.

- [ ] **Step 1: Write the failing test**

Create `tests/agents/test_pedagogy.py`:

```python
import core.agents.pedagogy as ped
from core.agents import Chunk, StudentContext


def test_prompt_includes_chunks_and_difficulty(monkeypatch):
    captured = {}

    def fake_generate(prompt, temperature=0.7, max_tokens=512, system=""):
        captured["prompt"] = prompt
        captured["system"] = system
        return "Plants make food using sunlight."

    monkeypatch.setattr("core.llm_engine._ollama_generate", fake_generate)

    chunks = [Chunk(text="Photosynthesis uses sunlight.", source="sci.pdf", page=3, distance=0.1)]
    ctx = StudentContext(grade="7", avg_score=40.0, weak_subjects=[], difficulty="simple")

    answer = ped.reason("How do plants make food?", ctx, chunks)

    assert answer == "Plants make food using sunlight."
    assert "Photosynthesis uses sunlight." in captured["prompt"]
    assert "simple" in captured["system"].lower()


def test_empty_answer_returns_grounded_fallback(monkeypatch):
    monkeypatch.setattr("core.llm_engine._ollama_generate", lambda *a, **k: "")
    chunks = [Chunk(text="x", source="a.pdf", page=1, distance=0.1)]
    ctx = StudentContext(grade="general", avg_score=0.0, weak_subjects=[], difficulty="standard")
    answer = ped.reason("Question?", ctx, chunks)
    assert answer == ""   # orchestrator decides what to do with empty
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/agents/test_pedagogy.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'core.agents.pedagogy'`.

- [ ] **Step 3: Write implementation**

Create `core/agents/pedagogy.py`:

```python
"""
core/agents/pedagogy.py
=======================
Pedagogical Reasoning Agent. Produces an English answer grounded strictly in the
retrieved curriculum chunks, tuned to the student's difficulty level.
"""
from __future__ import annotations

from core.agents import Chunk, StudentContext

_DIFFICULTY_GUIDE = {
    "simple":    "Use very short sentences and basic vocabulary.",
    "standard":  "Use clear language appropriate for a secondary school student.",
    "challenge": "You may use richer detail and introduce one extension idea.",
}


def _build_prompt(query_en: str, chunks: list[Chunk]) -> str:
    context_block = "\n---\n".join(c.text for c in chunks) if chunks else ""
    return (
        f"Curriculum context:\n{context_block}\n\n"
        f"Student question: {query_en}"
    )


def _build_system(context: StudentContext) -> str:
    guide = _DIFFICULTY_GUIDE.get(context.difficulty, _DIFFICULTY_GUIDE["standard"])
    return (
        "You are EduNode, an offline AI tutor for rural ASEAN students. "
        "Answer ONLY using the provided curriculum context. "
        "If the context does not contain the answer, say you don't have that "
        "information yet rather than guessing. "
        f"Explain at a {context.difficulty} level for a grade {context.grade} student. "
        f"{guide} "
        "Keep your answer under 150 words. Respond in English."
    )


def reason(query_en: str, context: StudentContext, chunks: list[Chunk]) -> str:
    """Generate an English, curriculum-grounded answer. Returns '' on model failure."""
    from core.llm_engine import _ollama_generate

    prompt = _build_prompt(query_en, chunks)
    system = _build_system(context)
    return _ollama_generate(prompt, temperature=0.5, system=system)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/agents/test_pedagogy.py -v`
Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
git add core/agents/pedagogy.py tests/agents/test_pedagogy.py
git commit -m "feat: pedagogy agent (Phi-3 grounded reasoning)"
```

---

## Task 7: Verification Agent

**Files:**
- Create: `core/agents/verification.py`
- Test: `tests/agents/test_verification.py`

Computes a confidence score by comparing the answer embedding against the source chunk embeddings, and extracts page-level citations. No extra LLM call.

- [ ] **Step 1: Write the failing test**

Create `tests/agents/test_verification.py`:

```python
import numpy as np

import core.agents.verification as ver
from core.agents import Chunk, Verification


def _fake_embedder(vectors_by_text):
    """Return an object with .encode(list[str]) -> np.ndarray matching a lookup."""
    class _E:
        def encode(self, texts):
            return np.array([vectors_by_text[t] for t in texts], dtype=float)
    return _E()


def test_grounded_answer_has_high_confidence(monkeypatch):
    answer = "Plants make food from sunlight."
    chunk_text = "Photosynthesis lets plants make food from sunlight."
    vecs = {answer: [1.0, 0.0, 0.0], chunk_text: [0.96, 0.28, 0.0]}
    monkeypatch.setattr(ver, "_get_embedder", lambda: _fake_embedder(vecs))

    chunks = [Chunk(text=chunk_text, source="sci.pdf", page=4, distance=0.1)]
    result = ver.score(answer, chunks)

    assert isinstance(result, Verification)
    assert result.confidence >= 0.85
    assert result.needs_review is False
    assert {"source": "sci.pdf", "page": 4} in result.citations


def test_offtopic_answer_flags_review(monkeypatch):
    answer = "The capital of France is Paris."
    chunk_text = "Photosynthesis lets plants make food from sunlight."
    vecs = {answer: [0.0, 1.0, 0.0], chunk_text: [1.0, 0.0, 0.0]}
    monkeypatch.setattr(ver, "_get_embedder", lambda: _fake_embedder(vecs))

    chunks = [Chunk(text=chunk_text, source="sci.pdf", page=4, distance=0.8)]
    result = ver.score(answer, chunks)

    assert result.confidence < 0.85
    assert result.needs_review is True


def test_no_chunks_zero_confidence(monkeypatch):
    monkeypatch.setattr(ver, "_get_embedder", lambda: _fake_embedder({}))
    result = ver.score("anything", [])
    assert result.confidence == 0.0
    assert result.needs_review is True
    assert result.citations == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/agents/test_verification.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'core.agents.verification'`.

- [ ] **Step 3: Write implementation**

Create `core/agents/verification.py`:

```python
"""
core/agents/verification.py
===========================
Verification Agent. Scores how well a generated answer is grounded in the source
chunks (cosine similarity in embedding space) and extracts page-level citations.
Deterministic — no extra LLM call.
"""
from __future__ import annotations

import logging

from core.agents import Chunk, Verification

log = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.85   # below this -> needs_review
CITATION_FLOOR = 0.30         # per-chunk grounding sim to count as a citation


def _get_embedder():
    """Indirection so tests can patch the embedder."""
    from core.rag_engine import get_embedder
    return get_embedder()


def _cosine(a, b) -> float:
    import numpy as np
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def score(answer_en: str, chunks: list[Chunk]) -> Verification:
    """Return a Verification with confidence, citations and needs_review."""
    if not chunks:
        return Verification(confidence=0.0, citations=[], needs_review=True)

    embedder = _get_embedder()
    texts = [answer_en] + [c.text for c in chunks]
    vectors = embedder.encode(texts)
    answer_vec = vectors[0]
    chunk_vecs = vectors[1:]

    sims = [_cosine(answer_vec, cv) for cv in chunk_vecs]
    grounding_score = max(sims) if sims else 0.0

    best_distance = min(c.distance for c in chunks)
    retrieval_score = max(0.0, 1.0 - best_distance)

    confidence = round(0.5 * retrieval_score + 0.5 * grounding_score, 3)

    citations = []
    for chunk, sim in zip(chunks, sims):
        if sim >= CITATION_FLOOR:
            entry = {"source": chunk.source, "page": chunk.page}
            if entry not in citations:
                citations.append(entry)

    return Verification(
        confidence=confidence,
        citations=citations,
        needs_review=confidence < CONFIDENCE_THRESHOLD,
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/agents/test_verification.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add core/agents/verification.py tests/agents/test_verification.py
git commit -m "feat: verification agent (confidence scoring + citations)"
```

---

## Task 8: Orchestrator

**Files:**
- Create: `core/agents/orchestrator.py`
- Test: `tests/agents/test_orchestrator.py`

Sequences the four agents and owns the two gates: the retrieval gate (best distance > 0.65 → controlled non-response, no generation) and the verification gate (confidence < 0.85 → needs_review).

- [ ] **Step 1: Write the failing test**

Create `tests/agents/test_orchestrator.py`:

```python
import core.agents.orchestrator as orch
from core.agents import Chunk, StudentContext, Verification


def _patch_all(monkeypatch, *, chunks, reason_called):
    monkeypatch.setattr(orch, "_translate_in", lambda q, lang: q)
    monkeypatch.setattr(orch, "_translate_out", lambda a, lang: a)
    monkeypatch.setattr(
        "core.agents.context.build",
        lambda sid: StudentContext(grade="7", avg_score=0.0, weak_subjects=[], difficulty="standard"),
    )
    monkeypatch.setattr("core.rag_engine.retrieve_with_citations", lambda q, n_results, subject: chunks)

    def fake_reason(q, ctx, ch):
        reason_called.append(True)
        return "An answer grounded in curriculum."
    monkeypatch.setattr("core.agents.pedagogy.reason", fake_reason)

    monkeypatch.setattr(
        "core.agents.verification.score",
        lambda ans, ch: Verification(confidence=0.92, citations=[{"source": "a.pdf", "page": 2}], needs_review=False),
    )


def test_happy_path_returns_full_payload(monkeypatch):
    reason_called = []
    chunks = [Chunk(text="grounded text", source="a.pdf", page=2, distance=0.2)]
    _patch_all(monkeypatch, chunks=chunks, reason_called=reason_called)

    result = orch.run_pipeline("How do plants grow?", "English", student_id=1, subject="Science")

    assert reason_called == [True]
    assert result["answer"] == "An answer grounded in curriculum."
    assert result["confidence"] == 0.92
    assert result["needs_review"] is False
    assert result["citations"] == [{"source": "a.pdf", "page": 2}]
    assert result["language"] == "English"


def test_retrieval_gate_blocks_generation(monkeypatch):
    reason_called = []
    # Best distance 0.9 > 0.65 -> controlled non-response, reason() never called
    chunks = [Chunk(text="weak match", source="a.pdf", page=1, distance=0.9)]
    _patch_all(monkeypatch, chunks=chunks, reason_called=reason_called)

    result = orch.run_pipeline("Unrelated question?", "English", student_id=1, subject="Science")

    assert reason_called == []                 # generation skipped
    assert result["confidence"] == 0.0
    assert result["needs_review"] is True
    assert result["citations"] == []
    assert "don't have" in result["answer"].lower() or "do not have" in result["answer"].lower()


def test_no_chunks_returns_non_response(monkeypatch):
    reason_called = []
    _patch_all(monkeypatch, chunks=[], reason_called=reason_called)
    result = orch.run_pipeline("Anything?", "English", student_id=1, subject="General")
    assert reason_called == []
    assert result["needs_review"] is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/agents/test_orchestrator.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'core.agents.orchestrator'`.

- [ ] **Step 3: Write implementation**

Create `core/agents/orchestrator.py`:

```python
"""
core/agents/orchestrator.py
===========================
Sequences the four-agent pipeline and owns the confidence gates:
  Translation -> Context -> Retrieval(gate) -> Pedagogy -> Verification(gate) -> Translation
"""
from __future__ import annotations

import logging

log = logging.getLogger(__name__)

RETRIEVAL_DISTANCE_GATE = 0.65   # best chunk distance above this -> non-response

_NON_RESPONSE_EN = (
    "I don't have curriculum material on that topic yet. "
    "Please ask your teacher, or try rephrasing your question."
)


def _translate_in(query: str, language: str) -> str:
    from core.agents.translation import to_english
    return to_english(query, language)


def _translate_out(answer: str, language: str) -> str:
    from core.agents.translation import to_native
    return to_native(answer, language)


def run_pipeline(query: str, language: str, student_id, subject: str = "General") -> dict:
    """
    Run the full agentic pipeline.
    Returns {answer, confidence, citations, needs_review, language}.
    """
    from core.agents import context as context_agent
    from core.agents import pedagogy, verification
    from core.rag_engine import retrieve_with_citations

    # 1. Translate query into English
    query_en = _translate_in(query, language)

    # 2. Build student context
    ctx = context_agent.build(student_id)

    # 3. Retrieve + RETRIEVAL GATE
    chunks = retrieve_with_citations(query_en, n_results=3, subject=subject)
    best_distance = min((c.distance for c in chunks), default=1.0)
    if not chunks or best_distance > RETRIEVAL_DISTANCE_GATE:
        log.info("Retrieval gate triggered (best_distance=%.3f) — controlled non-response.", best_distance)
        return {
            "answer": _translate_out(_NON_RESPONSE_EN, language),
            "confidence": 0.0,
            "citations": [],
            "needs_review": True,
            "language": language,
        }

    # 4. Reason (Phi-3)
    answer_en = pedagogy.reason(query_en, ctx, chunks)
    if not answer_en:
        return {
            "answer": _translate_out(_NON_RESPONSE_EN, language),
            "confidence": 0.0,
            "citations": [],
            "needs_review": True,
            "language": language,
        }

    # 5. Verify + VERIFICATION GATE
    result = verification.score(answer_en, chunks)

    # 6. Translate answer back to the student's language
    answer_native = _translate_out(answer_en, language)

    return {
        "answer": answer_native,
        "confidence": result.confidence,
        "citations": result.citations,
        "needs_review": result.needs_review,
        "language": language,
    }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/agents/test_orchestrator.py -v`
Expected: 3 passed.

- [ ] **Step 5: Run the full agent suite**

Run: `pytest tests/ -v`
Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add core/agents/orchestrator.py tests/agents/test_orchestrator.py
git commit -m "feat: pipeline orchestrator with retrieval + verification gates"
```

---

## Task 9: Wire query_tutor + /api/chat

**Files:**
- Modify: `core/llm_engine.py:207-236`
- Modify: `app.py:265-292`
- Test: `tests/agents/test_query_tutor_wrapper.py`

`query_tutor()` becomes a thin wrapper returning the pipeline dict. `/api/chat` resolves the student first (so the context agent has the id) then passes the payload through.

- [ ] **Step 1: Write the failing test**

Create `tests/agents/test_query_tutor_wrapper.py`:

```python
import core.llm_engine as llm


def test_query_tutor_delegates_to_pipeline(monkeypatch):
    captured = {}

    def fake_pipeline(query, language, student_id, subject="General"):
        captured["args"] = (query, language, student_id, subject)
        return {"answer": "hi", "confidence": 0.9, "citations": [], "needs_review": False, "language": language}

    monkeypatch.setattr("core.agents.orchestrator.run_pipeline", fake_pipeline)

    out = llm.query_tutor("Hello?", "English", student_id=5, subject="Science")
    assert out["answer"] == "hi"
    assert out["confidence"] == 0.9
    assert captured["args"] == ("Hello?", "English", 5, "Science")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/agents/test_query_tutor_wrapper.py -v`
Expected: FAIL — `TypeError` (current `query_tutor` takes `rag_context`, not `student_id`/`subject`).

- [ ] **Step 3: Replace query_tutor with a wrapper**

In `core/llm_engine.py`, replace the entire `query_tutor` function (lines 207-236) with:

```python
def query_tutor(user_message: str, language: str, student_id=None, subject: str = "General") -> dict:
    """
    Run the agentic pipeline and return a structured result:
        {answer, confidence, citations, needs_review, language}

    Thin wrapper over core.agents.orchestrator. Kept here so existing imports
    (`from core.llm_engine import query_tutor`) continue to work.
    """
    from core.agents.orchestrator import run_pipeline
    return run_pipeline(user_message, language, student_id=student_id, subject=subject)
```

Note: leave `_build_tutor_prompt`, `_build_tutor_system`, `_bridge_translate`, `_load_glossary`, `_offline_fallback`, and `_ollama_generate` in place — they are still used by the agents and the glossary fallback.

- [ ] **Step 4: Run wrapper test to verify it passes**

Run: `pytest tests/agents/test_query_tutor_wrapper.py -v`
Expected: 1 passed.

- [ ] **Step 5: Update /api/chat to resolve student first and pass payload through**

In `app.py`, replace the body of `api_chat` (lines 276-292, from the `from core.llm_engine import query_tutor` line through the final `return jsonify(...)`) with:

```python
    from core.llm_engine        import query_tutor
    from core.progress_tracker  import get_or_create_student, log_session, log_dialect

    # Resolve student first so the context agent can personalise.
    sid: int | None = None
    try:
        sid = get_or_create_student(student_name, language)
    except Exception as exc:
        log.warning("Student resolution failed: %s", exc)

    result = query_tutor(message, language, student_id=sid, subject=subject)

    try:
        if sid is not None:
            log_session(sid, subject=subject, message_count=1)
        if language.lower() != "english":
            log_dialect(language, message)
    except Exception as exc:
        log.warning("Progress logging failed: %s", exc)

    return jsonify({
        "response":     result["answer"],
        "confidence":   result["confidence"],
        "needs_review": result["needs_review"],
        "citations":    result["citations"],
        "language":     result["language"],
        "student_id":   sid,
    })
```

Note: `_safe_retrieve_context` is no longer called by `api_chat` (retrieval now happens inside the pipeline). Leave the helper in place — it is still used by `/api/quiz/generate` and `/api/flashcard` (verify with the next step).

- [ ] **Step 6: Confirm _safe_retrieve_context still has other callers**

Run: `grep -n "_safe_retrieve_context" app.py`
Expected: still referenced by the quiz and flashcard routes (lines ~353 and ~491). If `api_chat` was its only caller, that would be dead code — but it is not. Do not delete it.

- [ ] **Step 7: Verify app imports cleanly**

Run: `python -c "import app"`
Expected: no import errors.

- [ ] **Step 8: Run the full test suite**

Run: `pytest tests/ -v`
Expected: all tests pass.

- [ ] **Step 9: Commit**

```bash
git add core/llm_engine.py app.py tests/agents/test_query_tutor_wrapper.py
git commit -m "feat: wire agentic pipeline into query_tutor and /api/chat"
```

---

## Task 10: End-to-End Smoke Test (manual, requires models)

**Files:** none (manual verification)

- [ ] **Step 1: Pull the model and re-ingest curriculum**

```bash
ollama pull phi3:mini
rm -rf data/chroma
python -c "from core.rag_engine import ingest_pdfs; print('chunks:', ingest_pdfs())"
```
Expected: prints a non-zero chunk count (assuming curriculum PDFs exist in `data/curriculum/`).

- [ ] **Step 2: Start the server**

```bash
ollama serve &
python app.py
```

- [ ] **Step 3: Query a topic that IS in the curriculum**

```bash
curl -s -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What is photosynthesis?","language":"English","subject":"Science","student_name":"Demo"}' | python -m json.tool
```
Expected: JSON with `response`, `confidence` > 0, and a non-empty `citations` array containing `source` + `page`.

- [ ] **Step 4: Query a topic that is NOT in the curriculum**

```bash
curl -s -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Explain quantum chromodynamics in detail.","language":"English","subject":"General","student_name":"Demo"}' | python -m json.tool
```
Expected: the controlled non-response ("I don't have curriculum material…"), `confidence: 0.0`, `needs_review: true`, empty `citations`.

- [ ] **Step 5: Query in a non-English language (NLLB path)**

```bash
curl -s -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Apakah itu fotosintesis?","language":"Bahasa Melayu","subject":"Science","student_name":"Demo"}' | python -m json.tool
```
Expected: `response` in Bahasa Melayu (first NLLB call downloads the model — slow once), citations present.

- [ ] **Step 6: Final commit (if any docs/notes added)**

```bash
git add -A
git commit -m "docs: smoke-test notes for agentic backend" || echo "nothing to commit"
```

---

## Self-Review Notes

- **Spec coverage:** 4-agent package (Tasks 1,4,5,6,7,8) ✓ · Verification + page citations (Tasks 2,7) ✓ · NLLB-200 + glossary fallback (Task 4) ✓ · Confidence-coded API (Task 9) ✓ · Multilingual embedder swap + re-ingest note (Task 3) ✓ · Phi-3 + llama fallback (Task 3, relies on existing `_resolve_ollama_model`) ✓ · 0.65 retrieval gate + 0.85 verification gate (Task 8) ✓ · Backward-compatible `response` field (Task 9) ✓.
- **English pass-through / source = UI language:** Task 4 (`to_english`/`to_native` early-return for English); Task 9 passes the UI-selected `language` straight through — no auto-detection.
- **Out of scope (honored):** no `chat.html` rendering, voice, quiz/podcast/flashcard, hardware, or teacher-review-queue UI changes.
- **Type consistency:** `Chunk{text,source,page,distance}`, `StudentContext{grade,avg_score,weak_subjects,difficulty}`, `Verification{confidence,citations,needs_review}`, and the pipeline dict `{answer,confidence,citations,needs_review,language}` are used identically across Tasks 1–9.

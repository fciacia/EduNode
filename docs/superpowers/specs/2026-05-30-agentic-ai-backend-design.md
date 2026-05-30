# EduNode Agentic AI Backend — Design Spec

**Date:** 2026-05-30
**Status:** Approved (pending written-spec review)
**Scope:** AI backend only. Aligns EduNode's code with the UM-Gunners "Edge" Technical Roadmap (AI for Education track).

---

## 1. Goal & Motivation

The Technical Roadmap specifies an **Agentic RAG pipeline** with four specialized agents and a Verification Agent that prevents hallucinations through page-level citations. The current code uses a single RAG call plus a glossary-prompt translation bridge. This spec closes that gap.

**What changes:** the reasoning backend behind `/api/chat`.
**What does NOT change (this spec):** the chat UI rendering of confidence badges/citations, voice layer, quiz/podcast/flashcard engines, hardware/deployment. The backend returns confidence + citation data ready for the UI to consume in separate work.

### Roadmap alignment matrix

| Roadmap requirement | Current state | This spec delivers |
|---|---|---|
| 4-agent pipeline (Context, Translation, Pedagogy, Verification) | Single RAG + LLM call | `core/agents/` package, one module per agent |
| Verification Agent, hallucination defense | None | `verification.py` + dual confidence gates |
| Page-level citations | Chunking discards page numbers | Per-page chunking + `retrieve_with_citations()` |
| NLLB-200 neural translation | `"respond in {language}"` prompt + glossary | `translation.py` (NLLB-200, glossary fallback) |
| Confidence-coded UI | Plain text response | `{confidence, needs_review, citations}` in API |
| `paraphrase-multilingual-MiniLM-L12-v2` embeddings | `all-MiniLM-L6-v2` | Embedding model swap + re-ingest |
| Phi-3 Mini reasoning | `llama3.2:3b` | `phi3:mini` via Ollama (llama auto-fallback) |
| 0.65 cosine similarity gate | None | Retrieval gate in orchestrator |

---

## 2. Architecture & Data Flow

A new `core/agents/` package orchestrates the 4-agent pipeline. `query_tutor()` in `llm_engine.py` becomes a thin wrapper over the orchestrator, keeping `app.py` integration minimal.

```
Student query (mother tongue, UI-selected language)
        │
        ▼
orchestrator.run_pipeline(query, language, student_id, subject)
  1. translation.to_english(query, language)        ── NLLB-200
        ↳ English skips this (pass-through)
  2. context.build(student_id)                       ── SQLite
        ↳ grade + recent performance → difficulty hint
  3. rag.retrieve_with_citations(english_query, subject)
        ↳ returns Chunks + {source, page, distance}
        ↳ RETRIEVAL GATE: best distance > 0.65 → controlled non-response
  4. pedagogy.reason(english_query, context, chunks) ── Phi-3
        ↳ English answer grounded strictly in retrieved chunks
  5. verification.score(answer, chunks)
        ↳ confidence % + page citations
        ↳ VERIFICATION GATE: confidence < 0.85 → needs_review flag
  6. translation.to_native(answer, language)         ── NLLB-200
        │
        ▼
{ answer, confidence, citations:[{source,page}], needs_review, language }
```

### Two clarifications on "all languages through the pipeline"

1. **English is pass-through.** NLLB eng→eng is lossy and pointless, so the translation agent no-ops for English. Every *non-English* language (Tier-1 and Tier-2) gets the full NLLB bridge.
2. **Source language = UI-selected language**, not auto-detected. The student already picks their language, so the roadmap diagram's "dialect detection" step is skipped in favor of the explicit selection — simpler and more reliable.

### File tree

```
core/agents/
  __init__.py        # shared dataclasses: Chunk, StudentContext, Verification
  translation.py     # NLLB-200 to_english / to_native (+ glossary fallback)
  context.py         # student grade + performance → difficulty hint
  pedagogy.py        # Phi-3 grounded reasoning
  verification.py    # confidence scoring + citation extraction
  orchestrator.py    # run_pipeline() — sequences 1-6, owns the gates
core/rag_engine.py   # + retrieve_with_citations() (page metadata)
core/llm_engine.py   # query_tutor() → thin wrapper over orchestrator
```

---

## 3. Agent Contracts

Heavy models load lazily (cached singletons) so startup stays fast and English-only hubs never pay NLLB's cost.

### `translation.py` — NLLB-200 neural bridge
```python
to_english(text: str, language: str) -> str
to_native(text: str, language: str) -> str
```
- Maps hub language names → FLORES-200 codes
  (`"Bahasa Melayu"→zsm_Latn`, `"Iban"→iba_Latn`, `"Cebuano"→ceb_Latn`,
  `"Bahasa Indonesia"→ind_Latn`, `"Sundanese"→sun_Latn`, `"English"→eng_Latn`).
- English → returns text unchanged (pass-through).
- Language not in NLLB-200's 200 languages (e.g. **Kedayan**) → falls back to the
  **existing glossary bridge** in `llm_engine.py`. Nothing regresses.
- Model: `facebook/nllb-200-distilled-600M` via `transformers`, lazy-loaded singleton.

### `context.py` — personalization
```python
build(student_id: str) -> StudentContext   # {grade, avg_score, weak_subjects, difficulty}
```
- Reads existing `progress_tracker` SQLite tables. No schema change required:
  if grade exists, use it; otherwise default to "general" and infer `difficulty`
  from recent quiz averages.
- `difficulty ∈ {simple, standard, challenge}`.
- Output becomes a one-line hint injected into the pedagogy prompt.

### `pedagogy.py` — Phi-3 grounded reasoning
```python
reason(query_en: str, context: StudentContext, chunks: list[Chunk]) -> str
```
- Reuses `llm_engine._ollama_generate()` (no duplicate Ollama client) with `phi3:mini`.
- Strict system prompt: answer **only** from provided chunks; if chunks don't cover
  the question, say so explicitly.

### `verification.py` — confidence + citations
```python
score(answer_en: str, chunks: list[Chunk]) -> Verification
# Verification = {confidence: float, citations: list[{source, page}], needs_review: bool}
```
- Embeds the answer, compares (cosine) against the source chunks it was built from.
- Citations = `{source, page}` of chunks above a per-chunk similarity floor.
- `needs_review = confidence < 0.85`.

### Shared types (`core/agents/__init__.py`)
```python
@dataclass
class Chunk:           text: str; source: str; page: int; distance: float
@dataclass
class StudentContext:  grade: str; avg_score: float; weak_subjects: list; difficulty: str
@dataclass
class Verification:    confidence: float; citations: list; needs_review: bool
```

---

## 4. RAG Citations, Embedding Model & Confidence Math

### RAG changes (`rag_engine.py`)

1. **Per-page chunking.** `_extract_text_pdf()` already loops `reader.pages`; chunk
   per page and record the page number. Metadata becomes
   `{source, subject, grade, page, chunk_index}`.
2. **New `retrieve_with_citations(query, n_results, subject) -> list[Chunk]`** returns
   structured `Chunk` objects. The existing `retrieve_context()` stays (used by
   quiz/flashcard/podcast) — surgical, no breakage.
3. **Embedding model swap** → `paraphrase-multilingual-MiniLM-L12-v2` (per roadmap).
   Queries arrive in many languages; the current `all-MiniLM-L6-v2` is English-centric.
   **Caveat:** changing the embedder changes the vector space → requires a **one-time
   re-ingest** of curriculum. Startup detects a mismatch and warns.

### Confidence math (`verification.py`) — deterministic, no extra LLM call

```
retrieval_score = 1 - best_chunk_distance
grounding_score = max cosine(answer_embedding, chunk_embedding)
confidence      = 0.5 * retrieval_score + 0.5 * grounding_score
```

### Two gates (both from the roadmap)

- **Retrieval gate** (orchestrator step 3): `best_chunk_distance > 0.65` → skip
  generation, return controlled "I don't have curriculum on this yet" non-response.
- **Verification gate** (step 5): `confidence < 0.85` → answer returned but
  `needs_review = True` (amber confidence badge in UI).

**Why embedding-based, not a second LLM self-check:** deterministic, ~10× cheaper on
the Pi, and reuses the embedder already in memory — no extra model load.

---

## 5. Models, RAM Budget & API Shape

### Model changes (`config.py` + `.env`)

| Role | Current | New | How |
|---|---|---|---|
| Reasoning | `llama3.2:3b` | `phi3:mini` (Q4) | `ollama pull phi3:mini`; existing `_resolve_ollama_model()` auto-falls back to llama if absent |
| Translation | glossary prompt | `nllb-200-distilled-600M` | `transformers`, lazy singleton |
| Embedding | `all-MiniLM-L6-v2` | `paraphrase-multilingual-MiniLM-L12-v2` | env var, re-ingest |

### RAM budget on the 8GB Pi (roadmap target 7.4GB)

```
Phi-3 Mini Q4 (Ollama)      ~2.4 GB
NLLB-200-distilled-600M     ~1.3 GB (int8)  ← lazy: first non-English query
Multilingual embedder       ~0.5 GB
ChromaDB + Flask + OS       ~1.5 GB
                            ─────────
                            ~5.7 GB  ✓ within budget
```

NLLB loads lazily — English-only hubs never pay its cost. int8 quantization (optional,
via `ctranslate2`) is the Pi optimization; dev/laptop runs plain `transformers`.

### API response shape (`app.py` `/api/chat`) — backward compatible

```json
{
  "response": "...answer in mother tongue...",
  "confidence": 0.91,
  "needs_review": false,
  "citations": [{"source": "math_grade7.pdf", "page": 12}],
  "language": "Bahasa Melayu"
}
```

`query_tutor()` returns a dict; the route passes it through. Callers reading only
`.response` keep working. Chat UI consumes `confidence`/`citations` in separate work.

---

## 6. Testing Strategy

Each agent is independently testable. Unit tests mock models (no Ollama/NLLB in CI);
optional integration tests are gated on model availability. TDD per project CLAUDE.md —
tests before implementation.

### Per-agent unit tests (`tests/agents/`)
- `test_translation.py` — language→FLORES mapping; English pass-through; Kedayan →
  glossary fallback. NLLB call mocked.
- `test_context.py` — seeded SQLite → correct `difficulty`; missing student → defaults.
- `test_pedagogy.py` — prompt includes chunks + difficulty hint; `_ollama_generate` mocked.
- `test_verification.py` — high grounding → high confidence; off-topic → low confidence +
  `needs_review=True`; citations from correct chunks.
- `test_orchestrator.py` (key) — retrieval gate (distance > 0.65 → non-response, no
  generation call); verification gate (confidence < 0.85 → `needs_review`); happy-path
  sequencing with all 4 agents mocked.

### RAG tests (`tests/test_rag_citations.py`)
- Ingest a 2-page fixture PDF → chunks carry correct `page` numbers.
- `retrieve_with_citations()` returns `Chunk` objects with populated fields.

### Success criteria (verifiable)
1. `pytest tests/agents/ tests/test_rag_citations.py` green.
2. `/api/chat` returns the new payload shape with a real query (smoke test, Ollama running).
3. A query with no curriculum coverage returns the controlled non-response, not a hallucination.

---

## 7. Out of Scope (this spec)

- Confidence badge / citation rendering in `chat.html` (UI work, separate).
- Voice STT/TTS changes.
- Quiz / podcast / flashcard engines (they keep using `retrieve_context()`).
- Hardware, captive portal, deployment, sneakernet sync.
- Teacher-review queue UI (backend emits `needs_review`; the queue itself is future work).

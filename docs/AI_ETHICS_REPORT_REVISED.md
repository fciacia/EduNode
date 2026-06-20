# AI-USE & ETHICS REPORT (Revised)

**Team:** UM – Gunners · **Institution:** University of Malaya · **Country:** Malaysia
**Track:** AI for Education · **Project:** Edge: AI Education at the Last Mile
**Demo:** https://youtu.be/Ms_y6FUbKwU · **Repo:** https://github.com/fciacia/EduNode.git

> **What changed in this revision.** Following mentor review, this version replaces
> qualitative claims ("high accuracy", "strong performance") with a **reproducible
> evaluation harness and measured numbers**, and adds five capabilities requested by
> reviewers: a tiered response strategy, adaptive personalization, a teacher analytics
> dashboard, a data-governance framework, and a cross-ASEAN language-fairness
> evaluation. Where evidence depends on real-world inputs still in progress (a school
> pilot, on-Pi benchmarking, a fluent-speaker translation audit), we say so explicitly
> and report what is measured today versus what is pending.

---

## 1. Introduction

Across ASEAN, more than 60 million rural learners are structurally excluded from quality
education by a compounding triple divide: unreliable or absent internet connectivity,
lack of stable grid electricity, and AI tools that operate exclusively in dominant global
languages. Existing solutions such as ChatGPT are built for the connected world and fail
entirely in off-grid environments. Edge closes this gap with a fully offline,
solar-powered AI tutoring hub deployed directly into rural schools. On-device language
model inference, retrieval-augmented generation and neural machine translation together
deliver personalised, curriculum-grounded, mother-tongue instruction with no internet
dependency or recurring cloud cost.

## 2. Problem Context & Solution Overview

55% of Filipino 15-year-olds score below the OECD PISA minimum mathematics threshold and
only 30% of Cambodian Grade-5 students meet basic reading standards (UNICEF SEA-PLM, 2019).
Rural internet penetration is 18% in Timor-Leste, 25% in Myanmar, 28% in Laos (ITU, 2023),
making cloud platforms structurally inaccessible. Stakeholders include rural students
(K–10), teachers acting as local administrators, education ministries supplying Open
Educational Resources, and NGOs facilitating deployment.

Edge deploys a low-cost solar-powered hub built on Raspberry Pi that broadcasts a local
Wi-Fi network; students connect from their own smartphones with no internet. An **Agentic
RAG pipeline** of four agents — Translation, Personalised Context, Pedagogical Reasoning
and Verification — delivers curriculum-grounded answers, adaptive quizzes, voice
interaction and PDF microcredentials in the student's mother tongue.

## 3. AI Tools & Methods Used

| Component | Tool / Library | Purpose |
|---|---|---|
| Reasoning & Tutoring | Phi-3 Mini (4-bit GGUF via Ollama) | Curriculum Q&A and quiz generation |
| Vector Retrieval | ChromaDB + paraphrase-multilingual-MiniLM-L12-v2 | Semantic, cross-lingual search over curriculum |
| Translation | NLLB-200-distilled-600M + glossary bridge | NMT across ASEAN languages; bridge for non-NLLB dialects |
| Speech-to-Text | Whisper.cpp (ggml-base) | Offline voice input for low-literacy users |
| Text-to-Speech | Piper TTS (+ on-device browser TTS offload) | Offline voice output; client-side where supported |
| Orchestration | Flask + custom agentic pipeline + admission queue | Multi-agent coordination, API, concurrency control |
| Storage | SQLite + ChromaDB (local) | Student profiles, progress, audit log, vector store |
| Evaluation | Custom harness (`tools/eval_rag.py`, …) | Reproducible accuracy, bias and load measurement |

---

## 4. Assessment of AI Output (Critical Evaluation)

This section now reports **measured results** from a reproducible evaluation harness run
against a 33-question gold set drawn from the indexed curriculum (29 in-curriculum,
4 deliberately off-curriculum). All numbers are reproducible via `tools/eval_rag.py`.

### 4a. Accuracy — quantified

The Pedagogical Reasoning Agent is grounded by the Agentic RAG pipeline; the Verification
Agent scores every answer against source chunks and tiers the response. On the documented
model (Phi-3 Mini):

| Metric | Result | Notes |
|---|---|---|
| Retrieval hit-rate (recall@k) | **100%** | Correct source always in top-k |
| Retrieval precision@k (content-relevant) | **79%** | Chunks actually containing the answer's key facts |
| Hallucination / false-grounding rate | **0%** | Off-curriculum questions never cited as curriculum-grounded |
| Non-response rate (in-curriculum) | **0%** | No legitimate question left unanswered |
| Concept coverage (answer contains required key facts) | **~97%** | Lexical measure — see honest caveat below |
| Verifier confidence, correct answers (mean) | **~62%** | Separates correct (62%) from incorrect (0%) |

**Honest note on "accuracy" vs "concept coverage."** We deliberately do **not** report a
single "accuracy %" from an automated judge. When we cross-checked answer correctness with
three automated proxies, they diverged by up to **96 points** on the *same* answers — a
keyword/concept measure scored ~97%, a Phi-3 self-judge 48%, and a cross-model
(Llama-3.2) judge 3.4% — because small LLM judges **penalise the pedagogical
simplification** that is a design goal (e.g. the model writes "top number / bottom number"
instead of "numerator / denominator" for young learners). Concept coverage (~97%) is a
true, defensible statement that answers *contain the required facts*; final **answer
correctness is being validated by human raters** on a 29-question sample (tooling built:
`tools/make_grading_sheet.py` / `score_grading_sheet.py`, reporting strict/lenient accuracy
and inter-rater Cohen's κ). This divergence is itself a rigorous finding and the reason we
validate with humans rather than trusting an automated score.

### 4b. Technical Bias — cross-ASEAN language fairness (measured & mitigated)

Beyond content localisation, we measured **educational fairness across languages** by
holding the *content* fixed and varying only the language: the same curriculum questions
were asked in English, Bahasa Melayu, Thai, Vietnamese and Iban, measuring whether the
system still retrieves the correct curriculum and grounds its answer.

| Language | Grounding (before fix) | Grounding (after fix) |
|---|---|---|
| English (baseline) | 100% | 100% |
| Bahasa Melayu | 75% | 75% |
| Thai | 50% | **62%** |
| Vietnamese | 50% | **62%** |
| Iban | 88% | **100%** |

We **root-caused** the gap: the pipeline translated the query to English *before*
retrieving, and that translation noise degraded retrieval for non-English languages
(evidence: Iban, which uses a glossary bridge rather than full NMT, outperformed Thai and
Vietnamese). We **fixed** it with **cross-lingual retrieval** — the multilingual embedder
retrieves on the student's *native* query directly, keeping whichever of {native,
translated} grounds better. This recovered Thai/Vietnamese to 62% and fully closed the
Iban gap, with **0% non-response in every language** (degraded questions fall to the
supplementary tier, never silence). The residual major-language gap is bounded by the
small multilingual embedder — a documented memory trade-off addressed in §4e. We retain
the original mitigation of injecting localised OER (KPM, DepEd, Kemendikbud) so responses
draw from regional source material rather than parametric weights; the language-fairness
test extends this from "content localisation" to "equity across languages and dialects".

### 4c. Cultural & Regional Sensitivity

Official national OER PDFs remain the exclusive knowledge base, so examples and framing
reflect ASEAN norms. A regional educator panel audits dialect templates and flags
culturally inappropriate output. The **tiered Confidence UI** (§4f) is transparent about
reduced certainty in linguistically underserved contexts, preventing misleading
high-confidence answers. Quiz content is reviewed for gender and age representation.

### 4d. Linguistic Nuance — real translation-quality numbers

NLLB-200 was chosen for low-resource ASEAN coverage; Iban and Cebuano are excluded from
most mainstream models. We now report **measured translation quality (chrF)** rather than
a qualitative claim. Using real English↔Iban reference pairs (open
`VynerCK/Iban-language-data`):

| Language | References | chrF (translation segment) |
|---|---|---|
| Iban | 80 | **56** (decent) |

A diagnostic correction matters here: a naïve measurement scored Iban at 28, but that was
scoring the bilingual *display* wrapper (`[English] … [Iban] …`); scoring the translation
segment alone gives **chrF ≈ 56**. Quality for languages outside NLLB scales with
**glossary coverage**, which the **ASEAN Dialect Flywheel** grows via teacher-verified
corrections. We built the teacher correction loop (review → correct → store) and a
reference-collection sheet (`tools/make_translation_sheet.py`) so a fluent speaker can
supply ~25 curriculum-sentence references in ~1 hour, yielding sentence-level chrF for
Iban and Cebuano (audit in progress). Bilingual display ensures even partial translation
is useful and trustworthy.

### 4e. Scalability & Load Testing (new)

We stress-tested the live pipeline. **Measured on the development node (Apple Silicon
laptop, Phi-3 Mini, admission cap = 2)** — treat as a lower bound for a Raspberry Pi:

| Concurrency | Throughput | p50 latency | p95 latency | Errors |
|---|---|---|---|---|
| 1 | 7.8 req/min | 5.5 s | 17.0 s | 0 |
| 3 | 11.4 req/min | 10.1 s | 20.7 s | 0 |
| 5 | 10.8 req/min | 23.2 s | 32.3 s | 0 |

The shape is exactly as expected: **throughput plateaus (~11 req/min, the single-stream
SLM rate)** while latency climbs with concurrency, and **zero errors** because an
**asynchronous admission queue** makes excess requests *wait* rather than crash the node.
We therefore restate the "50 students" claim precisely: a hub supports **~50 connected
students with bursty, admission-controlled usage**, not 50 simultaneous inferences.

Two mentor-recommended optimisations are implemented: (1) the **admission queue** now
covers *all* LLM-heavy endpoints (chat, quiz, slides, podcast, flashcards, diagrams), and
(2) **text-to-speech is offloaded to the student's smartphone** (browser speech synthesis)
where available, sparing the hub. For the 4 GB-class hardware reality, we designed a
**two-node split** — an inference node (Ollama/SLM) and an application node
(Flask/RAG/translation/voice) communicating over the LAN (`OLLAMA_BASE` is already
network-configurable) — which keeps both nodes within budget and lets inference and
retrieval run on separate CPUs in parallel. **On-Pi benchmarking is the explicit next
step**; the load-test tool (`tools/load_test.py`) re-runs unchanged against the hub.

### 4f. Tiered Response Strategy (new — addresses over-restriction)

The original strict-RAG design risked frequent non-responses. We replaced the
all-or-nothing gate with three tiers based on retrieval distance:

- **Grounded** (distance ≤ 0.55): curriculum-cited, verified answer.
- **Supplementary** (0.55–0.85): a clearly-labelled general-knowledge answer
  ("not in your textbook") for near-miss questions, flagged for teacher review.
- **Non-response** (> 0.85): a controlled "ask your teacher" reply.

This balances safety with usefulness — measured non-response on in-curriculum questions is
0% — and the supplementary tier is configurable (can be disabled for strict deployments).

### 4g. Adaptive Personalization (new)

Personalization now goes beyond grade-level complexity. A **per-concept mastery model**
tracks accuracy per topic (with topic normalisation so casing/spacing variants merge),
identifies concepts a student struggles with, and **recommends remedial content**; a
spaced-repetition (Leitner) engine resurfaces weak material. This implements the
mentor-requested adaptive learning pathways.

## 5. Human Intervention & Justification

Human oversight is embedded at every layer. (1) Curriculum PDFs are manually curated
against official ministry standards before ingestion. (2) Retrieval and confidence
thresholds (grounded ≤ 0.55; supplementary ≤ 0.85; verifier confidence threshold 0.55)
were tuned empirically using the evaluation harness — a lower gate produced false
grounding, a higher one excessive non-responses — and the verifier's small-model
self-check was softened so a strong embedding match is not overridden by a cautious
verdict. (3) AI-generated quizzes are reviewed for cultural sensitivity, gender
representation and accuracy. (4) Iban/Cebuano translations are audited by native-speaker
consultants, with flagged mistranslations becoming correction templates that feed the
glossary flywheel. (5) Final **answer correctness is validated by human raters**, not by
the AI — because we measured that automated judges are unreliable for simplified tutoring
text. The team deliberately constrains AI autonomy to areas of demonstrated competence and
reserves curriculum framing and cultural judgment for human expertise.

## 6. Reflection on AI–Human Co-Creation

AI accelerated development — automated chunking and indexing replaced weeks of manual
tagging; generation scaled content; on-device inference removed the cost barrier to
village-scale tutoring. The hardest challenge remained hallucination in low-context
queries, answered by the Verification Agent and tiered confidence. A key revised learning
is **evaluation rigour itself**: building the measurement harness surfaced a translation
*measurement bug* (chrF 28 → 56) and the *unreliability of small LLM judges* (3.4%–100%
spread on identical answers), both of which would have gone unnoticed under qualitative
claims. The broader lesson stands: AI in under-resourced education requires *more* human
oversight, not less, because the communities served have the least capacity to catch AI
errors independently.

## 7. Educational Effectiveness — Pilot Protocol (Issue 1)

We acknowledge the report's strongest remaining gap: **measured learning outcomes**. A
full RCT is out of scope pre-deployment, so we specify a **micro-pilot** that is ready to
run, with automatic measurement:

- **Cohort:** 10–20 learners (a local class / tutoring group), optionally a small control
  group not using Edge.
- **Design:** pre-test quiz → 2–3 Edge sessions over 1–2 weeks → post-test; report the
  pre/post gain (and treatment-vs-control delta) as **preliminary, small-n**.
- **Instrumentation (already built):** the system logs quiz scores, sessions and
  completion automatically; a pre/post analysis script computes the gain directly from the
  logged data. The protocol and tooling are complete; the **evidence requires the pilot to
  run**, which is the team's immediate field step.

## 8. Data Governance (Issue 8)

A comprehensive, mostly-enforced framework now backs the offline data store:

- **Authentication & RBAC:** privileged routes require a token; login exchanges it for an
  **HttpOnly cookie** so the secret leaves URLs/logs; the default token is refused at
  startup.
- **Per-teacher identities:** named teacher accounts mean the **audit log attributes every
  privileged action to a person**, not a shared role.
- **Audit logging:** every privileged access (granted or denied) is recorded with actor,
  action, path, outcome and timestamp (`/api/audit`).
- **Encryption at rest:** full-disk **LUKS** for the live SD/SSD (documented deployment
  step) plus application-level **encryption of USB exports** (`core/crypto.py`, AES + HMAC,
  passphrase-derived key) so PII leaving the hub on a drive is unreadable without the
  passphrase.
- **Parental consent:** the consent act is offline (a signed form); Edge records the
  decision (status, who confirmed it, when) per student with an auditable trail.
- **Retention & erasure:** a term-based purge of stale records and a right-to-erasure
  `delete_student` path.

## 9. Teacher Analytics Dashboard (Issue 7)

An educator dashboard surfaces class-level KPIs, **most-missed concepts**, AI usage by
subject, daily activity, and the queue of flagged translations for review — giving teachers
visibility into progress, misconceptions and learning gaps, and closing the translation
correction loop.

## 10. Long-Term Sustainability & Decentralized Content (Issue 10)

Curriculum and software are maintained through a **decentralized content framework**: a
versioned, provenance-tracked content **manifest** lets ministries, schools, NGOs and
teachers publish updates independently. Integrity is **enforced** — on a checksum
mismatch, tampered files are quarantined out of the index, not merely flagged. Updates and
de-identified flywheel telemetry move via a **lightweight asynchronous sneakernet sync**
on encrypted USB drives during routine maintenance, exactly as the offline context
requires.

## 11. Conclusion

Edge demonstrates that AI-powered personalised education is deployable beyond cloud
infrastructure, at a cost the most underserved communities can bear. This revision
strengthens the original from a technically feasible prototype toward an **evidenced**
intervention: measured retrieval and grounding (100% recall, 0% hallucination), a
measured-and-mitigated language-fairness result, real translation-quality numbers, a
tiered response strategy, adaptive personalization, an enforced governance framework, and a
teacher dashboard — with the remaining gaps (a learning-outcomes pilot, on-Pi benchmarking,
a fluent-speaker translation audit) named honestly and tooled to close. Ethical AI in
underserved communities demands deliberate human intervention at every layer, from data
curation to linguistic auditing to confidence transparency; the ASEAN Dialect Flywheel
positions Edge as a contributor to the public good of minority-language AI infrastructure.

---

## Appendix E — Evaluation Reproducibility (new)

| Concern (mentor issue) | Tool | Result location |
|---|---|---|
| Accuracy / hallucination / retrieval (2) | `tools/eval_rag.py` | `data/eval/*_run.json` |
| Answer correctness (human) (2) | `tools/make_grading_sheet.py`, `score_grading_sheet.py` | `data/eval/grading.html` |
| Load / scalability (3) | `tools/load_test.py` | `docs/PERFORMANCE.md` |
| Translation chrF (4) | `tools/eval_translation.py` | `data/eval/TRANSLATION_QUALITY.md` |
| Language-fairness bias (9) | `tools/eval_language_fairness.py` | `data/eval/bias/LANGUAGE_FAIRNESS.md` |
| Cross-country scaffold (9) | `eval_rag --group-by country` | `data/eval/bias/README.md` |

*(Sections A–D — prompt samples, code snippets, data sources/licenses, architecture
reference — are retained from the original submission.)*

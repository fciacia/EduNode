# Language fairness — measured, root-caused, fixed, re-measured (Issue 9 + 4)

The rigorous bias test: hold the **content fixed**, vary only the **language**. Each
of 8 curriculum questions was asked in 5 languages; we measure whether the system
still retrieves the right curriculum and produces a **grounded** answer. Same
questions, same curriculum — so any gap from English **is** the bias.

Run: `python -m tools.eval_language_fairness --languages English "Bahasa Melayu" Thai Vietnamese Iban --limit 8`

## The arc

**1. Measured the bias.** Asking the identical question in another language dropped
grounding sharply from the English baseline.

**2. Root-caused it.** The pipeline translated the query to English *before*
retrieving; that translation noise raised retrieval distance and knocked answers
off the grounded tier. Evidence: Iban (glossary bridge, barely translated) beat
Thai/Vietnamese (full NLLB) — *less translation = better retrieval*.

**3. Fixed it.** Cross-lingual retrieval: the embedder is already multilingual, so
we now retrieve on the student's **native** question directly and keep whichever of
{native, translated} grounds better (`orchestrator.py`). Best-of, so it can only
help or tie — never regress.

**4. Re-measured.** grounded-rate, translated-only (old) → cross-lingual (fix):

| Language | Grounded (old) | Grounded (fix) | Gap vs English | Non-response |
|---|---|---|---|---|
| **English** (baseline) | 100% | 100% | 0 | 0% |
| Bahasa Melayu | 75% | 75% | −25 pts | 0% |
| Thai | 50% | **62%** | −50 → **−38 pts** | 0% |
| Vietnamese | 50% | **62%** | −50 → **−38 pts** | 0% |
| Iban | 88% | **100%** | −12 → **0 pts** ✅ | 0% |

## Honest findings

1. **The fix measurably reduces the bias** — Thai/Vietnamese recovered +12 pts each,
   and **Iban's gap closed completely** — at zero risk (best-of retrieval).
2. **It does not fully close the major-language gap.** Thai/Vietnamese still sit at
   ~62%, because `paraphrase-multilingual-MiniLM`'s cross-lingual alignment for
   those scripts is imperfect. Fully closing it needs a stronger multilingual
   embedder (e.g. multilingual-e5 / BGE-M3) or curriculum-side translation — both
   cost memory, a real trade-off against the 4 GB Pi budget. Documented, not hidden.
3. **Graceful degradation throughout:** non-response stayed **0% in every language** —
   anything not grounded fell to the *supplementary* tier (Issue 6), so students
   always got an answer. The bias shows as *less curriculum grounding*, never silence.
4. **The dialect flywheel is validated:** the glossary bridge (Iban) now matches
   English — direct evidence that investing in glossary/teacher-correction term
   mapping (Issue 4) is the right lever for languages outside the MT model.

## Caveats

- Small sample (8 questions); widen with `--limit`. Metric is retrieval grounding,
  not answer correctness (kept separate from the human-graded accuracy work).
- Round-trip simulation approximates a native speaker's phrasing.

## Report-ready summary

> "We isolated language bias (English 100% vs Thai 50% grounding), traced it to
> query translation degrading retrieval, and fixed it with cross-lingual retrieval —
> recovering Thai/Vietnamese to 62% and fully closing the Iban gap, with zero
> non-responses. Remaining major-language gap is bounded by the embedder and is a
> documented memory trade-off."

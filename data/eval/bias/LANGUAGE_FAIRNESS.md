# Language fairness — real result (Issue 9 + Issue 4)

The rigorous bias test: hold the **content fixed**, vary only the **language**. Each
of 8 curriculum questions was asked in 5 languages; we measure whether the system
still retrieves the right curriculum and produces a **grounded** answer, or degrades.
Same questions, same curriculum — so any gap from English **is** the bias.

Run: `python -m tools.eval_language_fairness --languages English "Bahasa Melayu" Thai Vietnamese Iban --limit 8`

| Language | Grounded | Answered | Non-response | Retrieval hit | Mean distance |
|---|---|---|---|---|---|
| **English** (baseline) | 100% | 100% | 0% | 100% | 0.246 |
| Bahasa Melayu | 75% | 100% | 0% | 100% | 0.365 |
| Thai | 50% | 100% | 0% | 100% | 0.506 |
| Vietnamese | 50% | 100% | 0% | 100% | 0.472 |
| Iban | 88% | 100% | 0% | 100% | 0.359 |

**Grounding gap vs English:** Bahasa Melayu −25 pts, Thai −50 pts, Vietnamese −50 pts, Iban −12 pts.

## What this shows (the honest findings)

1. **There is measurable language bias.** The identical question grounds 100% of
   the time in English but only ~50% in Thai/Vietnamese — round-trip translation
   adds semantic noise (mean retrieval distance climbs 0.25 → 0.51) that pushes
   answers off the grounded tier.
2. **The tiered-response design contains it.** Non-response stayed **0% in every
   language** — degraded questions fell to the *supplementary* tier, not outright
   failure. Students always got an answer; the bias shows up as *less curriculum
   grounding*, not silence. (This is Issue 6's mitigation working under stress.)
3. **A counterintuitive, useful result:** **Iban (−12 pts) beat Thai/Vietnamese
   (−50 pts)** despite being a low-resource language *not in NLLB-200*. Because
   Iban falls back to the **glossary bridge** (leaving the question largely intact)
   instead of a full neural round-trip, retrieval stays closer to English. For this
   curriculum, **partial bridging beats full translation** — direct evidence for
   investing in the dialect-glossary flywheel (Issue 4) over generic MT.

## Honest caveats

- Small sample (8 questions); widen with `--limit`.
- Metric is **retrieval grounding**, not answer correctness (kept separate from the
  answer-accuracy question, which needs the human pass).
- The round-trip (translate out → back) *approximates* a native speaker's phrasing;
  real student phrasing may differ.

## Why this is the right Issue-9 test

It isolates the language variable (vs country-curriculum, where universal science
barely differs), quantifies the inequity the mentor asked about ("across languages,
dialects"), and doubles as **Issue 4** evidence by ranking where translation quality
actually hurts learning. Re-run with `--with-llm` and more questions to strengthen.

# Edge — Cross-Country Fairness & Bias Evaluation (Issue 9)

The original report identified Western-centric bias in Phi-3 Mini and mitigated
it with regional curriculum. This document defines how we **measure** fairness
across ASEAN contexts rather than asserting it — so bias is surfaced with numbers,
not assumed away.

## What we measure

Using the same harness as the accuracy evaluation (`tools/eval_rag.py`), but with
a gold set tagged by `country` and `language`, we report **per-group**:

- Retrieval hit-rate (does the curriculum surface the right material?)
- Answer accuracy (keyword recall on the key facts)
- Non-response rate (does the system refuse more often for some groups?)
- Tier distribution (grounded vs. supplementary vs. non-response)

A fair system shows **similar** scores across countries, languages, and grade
bands. A large gap for one group is a measurable bias signal pointing at a content
or model weakness for that context.

## How to run

```bash
# Per-country breakdown (retrieval-only, offline):
python -m tools.eval_rag --gold data/eval/gold_set_asean.json --group-by country

# Per-language breakdown, with the SLM for answer accuracy:
python -m tools.eval_rag --gold data/eval/gold_set_asean.json \
    --group-by language --with-llm --report data/eval/asean_run.json
```

`--group-by` accepts any tag carried on a gold item: `country`, `language`,
`subject`, or `grade`.

## Methodology notes

1. **Same concept, local framing.** The bundled `gold_set_asean.json` probes the
   same core concepts (fraction, photosynthesis, cell, respiration) with phrasing
   familiar in each country, so score gaps reflect *system* bias rather than
   different question difficulty.
2. **Load the matching curriculum first.** Retrieval/answer scores are only
   meaningful once each country's ministry curriculum is ingested into
   `data/curriculum/`. Until then this file + the tagged gold set document the
   wiring; the numbers fill in per deployment.
3. **Languages, not just countries.** Run `--group-by language` to expose the
   low-resource-language gap (e.g. Iban, Cebuano) quantitatively — this connects
   directly to the translation-quality work (see the teacher correction loop).
4. **Socioeconomic / grade fairness.** Tag items with `grade` and group by it to
   check the system isn't systematically better for one band.

## Interpreting results

| Signal | Likely cause | Action |
|---|---|---|
| Low hit-rate for one country | Curriculum for that country is thin/missing | Ingest more local material |
| High non-response for one language | Translation weak → English retrieval misses | Feed teacher corrections into the glossary flywheel |
| Accuracy gap at one grade | Difficulty calibration off for that band | Tune the pedagogy difficulty guide |
| Off-curriculum answered as grounded | Over-confident retrieval gate | Tighten `GROUNDED_GATE` |

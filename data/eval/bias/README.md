# Cross-ASEAN Bias Evaluation — Runbook (Issue 9)

The harness is **ready**; this is a *data* exercise, not a code one. Grouping by
`country`/`language` and printing a per-group fairness table already works
(`tools/eval_rag.py --group-by`). You supply real curricula + questions; you must
**not** fabricate ministry content (same integrity rule as the human grading pass).

A few MB of text, ~2 hours on a laptop. Runs on the dev machine — **nothing here
touches the Pi's SD card.**

## Step 1 — Get real curriculum (open sources)

Download a few pages of openly-published, plain-text curriculum per country, e.g.:

| Country | Source | Example topics |
|---|---|---|
| Malaysia | KSSR (Kurikulum Standard Sekolah Rendah) Science/Math | photosynthesis, fractions |
| Philippines | DepEd K-12 MELC Science/Math | photosynthesis, fractions |
| Indonesia | Kurikulum Merdeka IPA/Matematika | … |
| Vietnam | MOET science/math syllabus | … |

Keep the *same topics* across countries so differences reflect **bias**, not
different content. Save as plain `.txt` into `data/curriculum/` with a country
prefix so they get ingested:

```
data/curriculum/my_science_kssr.txt
data/curriculum/ph_science_deped.txt
```

## Step 2 — Write the gold questions

Copy `data/eval/bias_gold.template.json` → `data/eval/bias_gold.json` and fill in
real questions grounded in the curricula above. Tag every item with `country` and
`language`; set `expected_sources` to that country's filename(s). Ask the **same
question** in each country's set so accuracy is comparable.

## Step 3 — Ingest + run

```bash
python ingest.py                      # re-index data/curriculum (now multi-country)
python -m tools.eval_rag --gold data/eval/bias_gold.json \
       --group-by country --with-llm
# also try:  --group-by language
```

You get a per-country table of hit-rate, accuracy, and non-response. **Gaps
between countries are your bias signal** — e.g. if Philippines accuracy >> Iban,
that's the inequity Issue 9 asks you to surface.

## What you can honestly report

> "Evaluated identical Science/Math questions against N countries' curricula.
> Accuracy ranged X%–Y% across countries/languages; the lower-resource
> language Z showed an N-point gap, which we mitigate via [glossary flywheel /
> teacher corrections]."

## Mechanism is already proven

You don't have to take it on faith that the grouping works — a **real** breakdown
by `subject` (math vs science vs English) on the existing 33-question gold set is
in [SUBJECT_FAIRNESS.md](SUBJECT_FAIRNESS.md). Country grouping uses the exact
same path.

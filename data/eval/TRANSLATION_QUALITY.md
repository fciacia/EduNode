# Translation quality — measured (Issue 4)

chrF (character n-gram F-score, 0–100; higher = better) measures how close the
system's translation is to a human reference. It's the standard metric for
low-resource / morphologically rich languages.

## Real result — Iban

Run: `python -m tools.eval_translation --gold data/eval/translation_gold_iban.json`

| Language | n (references) | chrF | Verdict |
|---|---|---|---|
| **Iban** | 80 | **28.1** | ⚠ weak |

References are real English↔Iban pairs from the open
[VynerCK/Iban-language-data](https://huggingface.co/datasets/VynerCK/Iban-language-data)
dataset (animal + object vocabulary). **chrF ≈ 28 is poor** (good translation is
~50+), which *quantifies exactly the risk the mentor flagged* in Issue 4: Iban is
outside NLLB-200, so the pipeline falls back to the glossary bridge and translation
quality is low. This is now a number, not an assertion.

**Caveat:** these references are single words, so chrF is noisier than a
sentence-level test. The sentence-level version is one fluent speaker away (below).

## Get the sentence-level number (Iban + Cebuano)

The proper test needs reference *sentences*. Those don't exist in open corpora, so a
fluent speaker supplies them once:

```bash
# 1. Build the sheet (25 real curriculum sentences x languages)
python -m tools.make_translation_sheet --languages Iban Cebuano --n 25

# 2. A fluent speaker opens data/eval/translation_sheet.html, types the correct
#    translation per sentence, clicks "Download filled CSV" (~1 hour).

# 3. Score it
python -m tools.eval_translation --sheet translation_sheet_filled.csv
```

The sheet (`data/eval/translation_sheet.{csv,html}`) is generated and ready.

## How this connects to the bias fix

The [language-fairness result](bias/LANGUAGE_FAIRNESS.md) showed Iban *retrieval*
beat Thai/Vietnamese (glossary bridge > full MT). This chrF result shows the other
side: Iban *translation* output is weak (28). Together they say: for languages
outside the MT model, invest in the **glossary / teacher-correction flywheel** — it
already helps retrieval, and verified corrections become the reference data that
both improves output and lets us re-measure chrF over time.

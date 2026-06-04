# Glossaries — bridge-mode dictionaries for low-resource languages

Languages that **NLLB-200 cannot translate** (Iban, Kedayan, Dayak, Hmong, Isan,
Tetum…) fall back to "bridge mode": the answer is generated in English and the
small model is asked to render it in the target language, **steered by a
glossary** of real native terms so it produces genuine vocabulary instead of
defaulting to a related language (e.g. Iban defaulting to Malay).

## Format

A glossary is `data/glossaries/<language>.json`, either:

```json
{ "_attribution": "source / licence", "cat": "mayau", "house": "rumah" }
```

or a list of `{"english": "...", "native": "..."}` entries. Keys beginning with
`_` are metadata and ignored as terms.

## Bundled

- **`iban.json`** — ~790 English→Iban terms compiled from two open sources:
  - [VynerCK/Iban-language-data](https://huggingface.co/datasets/VynerCK/Iban-language-data)
    (HuggingFace, MIT licence, © Vyner[CK] Jalla) — animals & objects.
  - Iban entries from English Wiktionary via
    [kaikki.org](https://kaikki.org/dictionary/Iban/) (**CC BY-SA / GFDL** — keep
    attribution and the share-alike licence on any redistribution).

  We deliberately do **not** use sources without a clear open licence (e.g.
  borneodictionary.com, or copyrighted print dictionaries) per the project's
  open-data policy.

## The dialect flywheel

These glossaries are meant to **grow**: teachers and native speakers add terms
(and, later, correct on-device output) so coverage improves over time. To extend
Iban, append more `"english": "iban"` pairs to `iban.json`.

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

- **`iban.json`** — English→Iban word lists (animals, objects) from the
  [VynerCK/Iban-language-data](https://huggingface.co/datasets/VynerCK/Iban-language-data)
  dataset (MIT licence, © Vyner[CK] Jalla).

## The dialect flywheel

These glossaries are meant to **grow**: teachers and native speakers add terms
(and, later, correct on-device output) so coverage improves over time. To extend
Iban, append more `"english": "iban"` pairs to `iban.json`.

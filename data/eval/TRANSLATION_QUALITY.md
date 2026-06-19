# Translation quality — measured & improved (Issue 4)

chrF (character n-gram F-score, 0–100; higher = better) is the standard translation
metric for low-resource / morphologically rich languages.

## The arc: measure → diagnose → fix → re-measure

**Naive measurement said Iban was weak (chrF 28).** But inspecting the output, the
*translations were correct* — `to_native("dog","Iban")` → `Uduk` (reference: "uduk"),
`"house"` → `Rumah`. The low score was a **measurement bug**: the bridge returns a
bilingual display string `"[English] dog\n[Iban] Uduk"`, and chrF was scoring that
whole wrapper against the bare reference word.

**Fix:** score only the translation segment (`native_segment`), not the display
wrapper.

| Measure | Iban chrF (n=80) |
|---|---|
| Whole bilingual output (wrong) | 28.1 |
| **Translation only (correct)** | **56.1** |

Real Iban translation quality for covered vocabulary is **~56 — decent**, not weak.
References are real English↔Iban pairs from the open
[VynerCK/Iban-language-data](https://huggingface.co/datasets/VynerCK/Iban-language-data).

## So how do we make it *good* — and keep it improving?

The translation engine for languages outside NLLB-200 (Iban, Cebuano, …) is a
**glossary bridge**: `data/glossaries/<lang>.json` maps English terms → native terms,
fed to the SLM as hints. **Quality scales with glossary coverage** — covered
vocabulary (the 80 words above) already scores ~56; the gap is *curriculum-specific*
vocabulary not yet in the glossary.

Levers, in order:

1. **Grow glossary coverage — the dialect flywheel (primary).** Teachers add verified
   term mappings via the admin glossary editor; the speaker reference sheet
   (`tools/make_translation_sheet.py`) collects curriculum-sentence translations.
   Both feed `data/glossaries/<lang>.json`, and every addition raises chrF on the
   newly-covered vocabulary. This is the mentor-praised flywheel, and it's the right
   lever precisely because the [language-fairness result](bias/LANGUAGE_FAIRNESS.md)
   showed bridging already beats full MT for low-resource languages.
2. **Seed from open datasets.** The basic-vocabulary glossary was seeded this way;
   the same can extend coverage cheaply before any human effort.
3. **Bilingual display (already shipped).** Showing English alongside the translation
   means even partial coverage is useful and builds learner trust.
4. **Fine-tune a small MT model (future).** Once enough verified pairs accumulate,
   fine-tune on them — but that needs thousands of pairs and is post-deployment work.

## Honest caveats

- chrF is case-sensitive, so "Uduk" vs "uduk" costs a few points; the *meaning* is right.
- The 80 references are word-level; the sentence-level number comes from the speaker
  sheet (`data/eval/translation_sheet.html`, ~1 hr of a fluent speaker).
- Cebuano *is* in NLLB-200, so it uses neural MT, not the bridge — score it with the
  speaker sheet to confirm.

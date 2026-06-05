# Curriculum sources & attribution

Edge grounds its answers in the curriculum loaded here. Every source must carry a
clear open licence and attribution (matching the project's open-data policy).
This folder holds **committed sample seeds**; load real national curriculum into
the runtime `data/curriculum/` via the Admin panel or `python ingest.py`.

## Bundled sample sources

- **`openstax_biology_photosynthesis.txt`**
  Adapted from **OpenStax, *Biology 2e*, §8.2 "The Light-Dependent Reactions of
  Photosynthesis."** © Rice University. Licence: **CC BY 4.0**
  (https://creativecommons.org/licenses/by/4.0/). Source:
  https://openstax.org/details/books/biology-2e — text simplified for younger
  readers (changes were made).

- **`openstax_math_fractions.txt`**
  Adapted from **OpenStax, *Prealgebra 2e*, §4.1 "Visualize Fractions."**
  © Rice University. Licence: **CC BY 4.0**. Source:
  https://openstax.org/details/books/prealgebra-2e — text simplified (changes
  were made).

> OpenStax is **CC BY**: free to use and adapt, including commercially, **with
> attribution** and an indication that changes were made (done above).

- **`mathematics_core_lessons.txt`** and **`science_core_lessons.txt`**
  **Original lesson text written for Edge**, covering standard Grade 6–8
  mathematics and science topics (facts that are common knowledge, not taken
  from any single copyrighted source). Licence: **CC BY-SA 4.0**
  (https://creativecommons.org/licenses/by-sa/4.0/). Free to use, adapt and
  share with attribution. These are concise teaching summaries, not a
  nationally-certified syllabus — load real ministry materials per hub (below)
  for formal alignment.

## National curriculum (added per hub, not bundled)

Each hub loads its own nationally-aligned materials. These are **not** uniformly
public-domain — government educational materials are typically *"free for
educational use"* with terms that vary by country, so **verify the licence per
document** before redistribution:

- **Malaysia — KPM** Buku Teks Digital (https://www.moe.gov.my)
- **Philippines — DepEd** Learning Resources / Self-Learning Modules (https://lrmds.deped.gov.ph)
- **Indonesia — Kemendikbud** Buku Sekolah Elektronik / Merdeka (https://buku.kemdikbud.go.id)

When you ingest one, add a block here with: file name, title, issuing ministry,
URL, and the exact licence/terms stated on the source.

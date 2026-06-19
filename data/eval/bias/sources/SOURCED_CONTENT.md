# Real curriculum content sourced for the cross-country bias eval (Issue 9)

Genuinely fetched from public sources — **not fabricated**. These are official
curriculum *standards/competencies*, quoted with attribution. See the honest
limitations at the bottom before using them.

## Malaysia — KSSR Year 4 Science (DSKP, Semakan 2017)

Source: DSKP KSSR Science DLP Year 4 (Semakan 2017), via AnyFlip
<https://anyflip.com/ittl/xhob/basic/51-94>

Quoted learning standards:
- "Parts of plants that respond to stimuli such as: (i) Roots respond to water.
  (ii) Roots respond to gravity. (iii) Shoots respond to light."
- "State the meaning of photosynthesis."
- "Photosynthesis is a process where plants produce their own food."
- "Products of photosynthesis are starch and oxygen."
- References a "natural water cycle" under Materials Science.

## Philippines — DepEd Grade 5 Science (Most Essential Learning Competencies)

Source: Grade 5 Science MELCs, TeacherPH (DepEd-derived)
<https://www.teacherph.com/wp-content/uploads/2022/08/Grade-6-Science-Most-Essential-Learning-Competencies-MELCs.pdf>

Quoted competencies (extracted from the official PDF):
- "different types of mixtures and their characteristics"
- "prepare beneficial and useful mixtures such as drinks, food, and herbal medicines"
- "Characterize weather disturbances in the Philippines and describe their effects to daily life"
- "the phases of the Moon and the beliefs and practices associated with it" /
  "debug local myths and folklore about the Moon and the Stars"
- "Describe how rocks turn into soil" (S5FE-IVa-1)

## Honest limitations (read before building on this)

1. **These are competency *standards*, not explanatory prose.** "State the meaning
   of photosynthesis" is a teaching objective, not a paragraph a RAG tutor can
   ground a full answer in. Ingesting these yields thin grounding / more
   non-responses than real textbook content would.
2. **The two documents emphasise different topics** (KSSR → plants/photosynthesis;
   the DepEd extract → mixtures/weather/Moon). A clean bias test needs the *same*
   topics from both — which requires matched textbook prose, not these.
3. **Universal science barely differs across countries**, so a photosynthesis
   comparison shows little "bias". The real per-country signal is in **localised
   content** (note DepEd's "weather disturbances in the Philippines", "Moon
   folklore") and in **language** (Bahasa Melayu vs Filipino) — not in the
   universal facts.

**Implication:** the most rigorous, controllable Issue-9 test is a **language-fairness**
comparison (same content, English vs Bahasa Melayu vs Filipino vs Iban) rather than
country-curriculum — it isolates the bias variable and reuses the translation pipeline.

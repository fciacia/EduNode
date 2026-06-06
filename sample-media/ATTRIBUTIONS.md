# Curriculum diagrams & attribution

Labelled pictures shown beside chat answers (the `image` diagram type) and on
flashcards. The app serves these from the runtime `data/media/` folder; this
folder holds **committed sample diagrams**. To use them, copy them in:

    cp sample-media/* data/media/

A diagram is surfaced when a student's question keyword matches a file name
(e.g. asking about a "plant cell" finds `plant_cell.svg`). Teachers can add
their own by dropping image files (`.svg`, `.png`, `.jpg`) into `data/media/`.

## Bundled sample diagrams

- **`plant_cell.svg`** — Original schematic of a plant cell (cell wall,
  membrane, nucleus, chloroplast, vacuole), drawn for Edge.
  Licence: **CC BY-SA 4.0** (https://creativecommons.org/licenses/by-sa/4.0/).

> These are simple teaching schematics, not exam-accurate scientific
> illustrations. Replace or supplement them with your hub's own approved
> diagrams.

"""
core/pptx_export.py
===================
Render a generated slide deck into a standard PowerPoint (.pptx) file so
students can download it and study offline in PowerPoint / LibreOffice / Google
Slides. Speaker notes carry the narration text.

build_pptx(topic, slides) -> bytes
"""
from __future__ import annotations

from io import BytesIO

from pptx import Presentation


def build_pptx(topic: str, slides: list[dict]) -> bytes:
    """Build a normal title+bullets deck mirroring the on-screen slides."""
    prs = Presentation()
    layout = prs.slide_layouts[1]  # "Title and Content" — standard bullet layout

    for s in slides:
        slide = prs.slides.add_slide(layout)

        emoji = (s.get("emoji") or "").strip()
        title = (s.get("title") or "").strip()
        slide.shapes.title.text = f"{emoji} {title}".strip()

        body = slide.placeholders[1].text_frame
        body.clear()
        bullets = [b for b in (s.get("bullets") or []) if str(b).strip()]
        for i, bullet in enumerate(bullets):
            para = body.paragraphs[0] if i == 0 else body.add_paragraph()
            para.text = str(bullet).strip()

        notes = (s.get("notes") or "").strip()
        if notes:
            slide.notes_slide.notes_text_frame.text = notes

    out = BytesIO()
    prs.save(out)
    return out.getvalue()

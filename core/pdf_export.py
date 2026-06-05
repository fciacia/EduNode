"""
core/pdf_export.py
==================
Render a generated slide deck into a PDF that mirrors the on-screen slides, for
students who'd rather study a PDF than a .pptx. One landscape page per slide:
per-slide accent (bar, title, bullets), a tinted media tile holding the matched
local image or the slide's emoji (rendered to an image so it shows in the PDF),
and a faint slide-number watermark.

build_pdf(topic, slides, media_dir=None) -> bytes
"""
from __future__ import annotations

from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import Frame, HRFlowable, Paragraph

from core.media import emoji_png, find_media, load_raster

# Same accent palette the web deck and .pptx export cycle through.
PALETTE = [
    ("6366F1", "EEF0FE"), ("0EA5E9", "E5F6FE"), ("10B981", "E6F8F1"),
    ("F59E0B", "FEF3E0"), ("EC4899", "FDEAF4"), ("8B5CF6", "F1ECFE"),
]

W, H = 960, 540          # 16:9 page, points
TEXT_DARK = HexColor("#33333A")


def _hex(h: str) -> HexColor:
    return HexColor("#" + h)


def _mix(h: str, t: float) -> Color:
    """Blend hex colour t-of-the-way toward white (0=colour, 1=white)."""
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return Color(*((c + (255 - c) * t) / 255 for c in (r, g, b)))


def build_pdf(topic: str, slides: list[dict], media_dir=None) -> bytes:
    buf = BytesIO()
    c = pdfcanvas.Canvas(buf, pagesize=(W, H))

    for i, s in enumerate(slides):
        accent, tint = PALETTE[i % len(PALETTE)]
        ac = _hex(accent)

        c.setFillColor(white); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(ac);    c.rect(0, 0, 16, H, fill=1, stroke=0)          # accent bar

        c.setFillColor(_mix(accent, 0.78))                                    # number watermark
        c.setFont("Helvetica-Bold", 60)
        c.drawRightString(W - 38, H - 82, f"{i + 1:02d}")

        tx, ty, tw, th = 50, 110, 300, 320                                    # media tile
        c.setFillColor(_hex(tint)); c.roundRect(tx, ty, tw, th, 16, fill=1, stroke=0)
        _draw_media(c, s, tx, ty, tw, th, media_dir)

        story = [
            Paragraph(escape((s.get("title") or "").strip()),
                      ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=26,
                                     leading=30, textColor=ac, spaceAfter=8)),
            HRFlowable(width="100%", thickness=2.2, color=_mix(accent, 0.4),
                       spaceBefore=2, spaceAfter=14, lineCap="round"),
        ]
        bstyle = ParagraphStyle("bullet", fontName="Helvetica", fontSize=17, leading=23,
                                textColor=TEXT_DARK, leftIndent=16, spaceAfter=9,
                                bulletFontName="Helvetica", bulletFontSize=14, bulletColor=ac)
        for bullet in (s.get("bullets") or []):
            if str(bullet).strip():
                story.append(Paragraph(escape(str(bullet).strip()), bstyle, bulletText="●"))

        Frame(390, 55, 530, H - 110 - 55, leftPadding=0, rightPadding=10,
              topPadding=0, bottomPadding=0, showBoundary=0).addFromList(story, c)
        c.showPage()

    c.save()
    return buf.getvalue()


def _draw_media(c, s, tx, ty, tw, th, media_dir) -> None:
    """Place the matched local image in the tile, else the slide's emoji."""
    query = (s.get("image_query") or "").strip()
    path = find_media(query, root=media_dir) if query else None
    src = load_raster(path) if path else None
    is_emoji = src is None
    if src is None:
        src = emoji_png(s.get("emoji") or "📘")
    if src is None:
        return
    try:
        img = ImageReader(src)
        iw, ih = img.getSize()
        pad = 28
        box_w, box_h = tw - 2 * pad, th - 2 * pad
        ar = iw / ih if ih else 1
        if box_w / box_h > ar:
            h, w = box_h, box_h * ar
        else:
            w, h = box_w, box_w / ar
        if is_emoji:                       # emoji needn't fill the whole tile
            w, h = w * 0.62, h * 0.62
        c.drawImage(img, tx + (tw - w) / 2, ty + (th - h) / 2, w, h, mask="auto")
    except Exception:
        pass

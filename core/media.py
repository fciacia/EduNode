"""
core/media.py
=============
Locate teacher-supplied curriculum images and load them in a form other code
can embed. Used by the web media route (which can render SVG) and the PowerPoint
export (which can only embed raster images).
"""
from __future__ import annotations

import os
import re
from io import BytesIO
from pathlib import Path

MEDIA_DIR = Path(os.getenv("MEDIA_DIR", "data/media"))

# Extensions a browser can display (SVG included).
IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
# Extensions python-pptx can embed directly (no SVG).
RASTER_EXT = {".png", ".jpg", ".jpeg", ".gif", ".bmp"}


def _tokens(s: str) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9]+", (s or "").lower()) if len(t) > 2}


def find_media(query: str, root: Path | None = None) -> Path | None:
    """Best-effort keyword match: return a media file whose name shares a word
    with *query* (e.g. 'green leaf' -> green_leaf.png), else None."""
    root = root or MEDIA_DIR
    q = _tokens(query)
    if not q or not root.exists():
        return None
    for p in sorted(root.iterdir()):
        if p.is_file() and p.suffix.lower() in IMG_EXT and q & set(re.split(r"[^a-z0-9]+", p.stem.lower())):
            return p
    return None


# Colour-emoji fonts by platform, with a Pillow-supported bitmap strike size.
_EMOJI_FONTS = [
    ("/System/Library/Fonts/Apple Color Emoji.ttc", 160),
    ("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109),
    ("/usr/share/fonts/NotoColorEmoji.ttf", 109),
    ("C:\\Windows\\Fonts\\seguiemj.ttf", 109),
]


def emoji_png(text: str) -> BytesIO | None:
    """Render an emoji to a transparent PNG so it can be embedded where text
    fonts can't show it (e.g. a reportlab PDF). None if no emoji font is found."""
    text = (text or "").strip()
    if not text:
        return None
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return None
    for path, size in _EMOJI_FONTS:
        if not os.path.exists(path):
            continue
        try:
            font = ImageFont.truetype(path, size)
            canvas = Image.new("RGBA", (size * 3, size * 2), (0, 0, 0, 0))
            ImageDraw.Draw(canvas).text((size // 2, size // 3), text, font=font, embedded_color=True)
            bbox = canvas.getbbox()
            if not bbox:
                continue
            out = BytesIO()
            canvas.crop(bbox).save(out, "PNG")
            out.seek(0)
            return out
        except Exception:
            continue
    return None


def load_raster(path: Path) -> BytesIO | None:
    """Return embeddable PNG/JPG bytes for *path*, converting WEBP via Pillow.
    Returns None for formats python-pptx cannot embed (e.g. SVG)."""
    suffix = path.suffix.lower()
    try:
        if suffix in RASTER_EXT:
            return BytesIO(path.read_bytes())
        if suffix == ".webp":
            from PIL import Image
            out = BytesIO()
            Image.open(path).convert("RGBA").save(out, "PNG")
            out.seek(0)
            return out
    except Exception:
        return None
    return None

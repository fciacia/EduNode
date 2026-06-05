"""Tests for building a downloadable PDF deck from slide data."""
from io import BytesIO

from pypdf import PdfReader

from core.pdf_export import build_pdf

SLIDES = [
    {"title": "Photosynthesis", "bullets": ["Plants make food", "Uses sunlight"],
     "notes": "Intro.", "emoji": "🌿", "image_query": ""},
    {"title": "Summary", "bullets": ["Light becomes food"], "emoji": "🌍", "image_query": ""},
]


def _read(blob):
    return PdfReader(BytesIO(blob))


def test_build_pdf_returns_pdf_bytes():
    blob = build_pdf("photosynthesis", SLIDES)
    assert blob[:5] == b"%PDF-" and len(blob) > 1000


def test_build_pdf_one_page_per_slide():
    assert len(_read(build_pdf("x", SLIDES)).pages) == len(SLIDES)


def test_build_pdf_contains_title_and_bullets():
    text = _read(build_pdf("x", SLIDES)).pages[0].extract_text()
    assert "Photosynthesis" in text
    assert "Plants make food" in text


def test_build_pdf_embeds_matching_local_image(tmp_path):
    from PIL import Image
    Image.new("RGB", (64, 48), "green").save(tmp_path / "green_leaf.png")
    deck = [{"title": "Leaf", "bullets": ["green"], "image_query": "green leaf", "emoji": "🌿"}]
    blob = build_pdf("leaf", deck, media_dir=tmp_path)
    assert blob[:5] == b"%PDF-" and len(_read(blob).pages) == 1

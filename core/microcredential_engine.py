"""
core/microcredential_engine.py
==============================
Step 8 — Check microcredential eligibility and generate PDF certificates.

Public API
----------
MICROCREDENTIALS : dict
    {topic: {"min_score_pct": float, "quizzes_required": int, "description": str}}

check_eligibility(student_id, topic) -> bool
    Returns True if the student has met the quiz threshold for the topic.

generate_certificate_pdf(student_name, topic, student_id) -> str
    Generates an A4 PDF certificate and returns its file path.
"""

from __future__ import annotations

import logging
import os
from datetime import date
from pathlib import Path

log = logging.getLogger(__name__)

CERT_DIR = Path(os.getenv("CERT_DIR", "static/certificates"))

# ---------------------------------------------------------------------------
# Microcredential definitions
# ---------------------------------------------------------------------------

MICROCREDENTIALS: dict[str, dict] = {
    "Mathematics Foundations": {
        "min_score_pct":    70.0,
        "quizzes_required": 3,
        "description":      "Demonstrated foundational mathematics skills.",
        "colour":           (0.10, 0.36, 0.64),   # deep blue  (R, G, B 0-1)
    },
    "Science Literacy": {
        "min_score_pct":    70.0,
        "quizzes_required": 3,
        "description":      "Demonstrated scientific literacy and inquiry skills.",
        "colour":           (0.13, 0.55, 0.13),   # deep green
    },
    "English Communication": {
        "min_score_pct":    70.0,
        "quizzes_required": 3,
        "description":      "Demonstrated English language communication competency.",
        "colour":           (0.55, 0.00, 0.55),   # purple
    },
    "Digital Citizenship": {
        "min_score_pct":    70.0,
        "quizzes_required": 2,
        "description":      "Demonstrated responsible digital citizenship.",
        "colour":           (0.80, 0.40, 0.00),   # orange
    },
    "Environmental Awareness": {
        "min_score_pct":    70.0,
        "quizzes_required": 2,
        "description":      "Demonstrated environmental and sustainability awareness.",
        "colour":           (0.00, 0.55, 0.45),   # teal
    },
}

# Fallback: generic thresholds for any topic not in the list above
_DEFAULT_THRESHOLD = {"min_score_pct": 70.0, "quizzes_required": 3}


# ---------------------------------------------------------------------------
# Eligibility check
# ---------------------------------------------------------------------------

def check_eligibility(student_id: int, topic: str) -> bool:
    """
    Return True if *student_id* has met the quiz threshold for *topic*.

    Matching is case-insensitive substring: a topic of "science" will match
    the "Science Literacy" microcredential entry.
    """
    from core.progress_tracker import _get_conn  # avoid circular at module level

    thresholds = _DEFAULT_THRESHOLD
    for key, val in MICROCREDENTIALS.items():
        if topic.lower() in key.lower() or key.lower() in topic.lower():
            thresholds = val
            break

    min_pct      = thresholds["min_score_pct"]
    required_n   = thresholds["quizzes_required"]

    conn = _get_conn()
    try:
        rows = conn.execute(
            "SELECT score, total FROM quiz_results"
            " WHERE student_id=? AND lower(topic) LIKE lower(?)"
            " ORDER BY taken_at DESC LIMIT 20",
            (student_id, f"%{topic}%"),
        ).fetchall()
    finally:
        conn.close()

    if len(rows) < required_n:
        return False

    scores = [r["score"] / r["total"] * 100 for r in rows if r["total"] > 0]
    if not scores:
        return False

    avg_pct = sum(scores) / len(scores)
    return avg_pct >= min_pct


# ---------------------------------------------------------------------------
# PDF generation
# ---------------------------------------------------------------------------

def generate_certificate_pdf(
    student_name: str,
    topic: str,
    student_id: int,
) -> str:
    """
    Generate an A4 PDF microcredential certificate.

    Returns the absolute file path of the created PDF.
    Raises RuntimeError if reportlab is not installed.
    """
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
        )
    except ImportError as exc:
        raise RuntimeError(
            "reportlab is required for certificates: pip install reportlab"
        ) from exc

    CERT_DIR.mkdir(parents=True, exist_ok=True)

    safe_name  = "".join(c if c.isalnum() else "_" for c in student_name)[:30]
    safe_topic = "".join(c if c.isalnum() else "_" for c in topic)[:30]
    filename   = f"cert_{student_id}_{safe_topic}_{safe_name}.pdf"
    out_path   = CERT_DIR / filename

    # Look up accent colour
    meta   = MICROCREDENTIALS.get(topic, {})
    r, g, b = meta.get("colour", (0.10, 0.36, 0.64))
    accent = colors.Color(r, g, b)

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        topMargin=3 * cm,
        bottomMargin=3 * cm,
        leftMargin=3 * cm,
        rightMargin=3 * cm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CertTitle",
        parent=styles["Title"],
        fontSize=28,
        leading=34,
        textColor=accent,
        spaceAfter=0.3 * cm,
    )
    subtitle_style = ParagraphStyle(
        "CertSubtitle",
        parent=styles["Normal"],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#555555"),
        spaceAfter=0.8 * cm,
    )
    body_style = ParagraphStyle(
        "CertBody",
        parent=styles["Normal"],
        fontSize=12,
        leading=18,
        alignment=1,   # centred
        spaceAfter=0.5 * cm,
    )
    name_style = ParagraphStyle(
        "CertName",
        parent=styles["Normal"],
        fontSize=22,
        leading=28,
        textColor=accent,
        alignment=1,
        spaceAfter=0.3 * cm,
    )
    small_style = ParagraphStyle(
        "CertSmall",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#888888"),
        alignment=1,
    )

    description = meta.get("description", f"Demonstrated proficiency in {topic}.")
    today = date.today().strftime("%d %B %Y")

    story = [
        Spacer(1, 0.5 * cm),
        HRFlowable(width="100%", thickness=3, color=accent, spaceAfter=0.5 * cm),
        Paragraph("Edge", title_style),
        Paragraph("Offline Learning Microcredential", subtitle_style),
        HRFlowable(width="60%", thickness=1, color=colors.HexColor("#cccccc"), spaceAfter=1 * cm),
        Paragraph("This certificate is awarded to", body_style),
        Paragraph(student_name, name_style),
        Paragraph("in recognition of successfully completing", body_style),
        Paragraph(f"<b>{topic}</b>", name_style),
        Spacer(1, 0.4 * cm),
        Paragraph(description, body_style),
        Spacer(1, 0.8 * cm),
        HRFlowable(width="60%", thickness=1, color=colors.HexColor("#cccccc"), spaceAfter=0.5 * cm),
        Paragraph(f"Date: {today}", body_style),
        Spacer(1, 1.5 * cm),
        Paragraph(
            "Edge is an offline AI tutoring platform for ASEAN communities.<br/>"
            "This credential aligns with UNESCO SDG 4 — Quality Education.",
            small_style,
        ),
        HRFlowable(width="100%", thickness=3, color=accent, spaceBefore=1 * cm),
    ]

    doc.build(story)
    log.info("Certificate generated: %s", out_path)
    return str(out_path)

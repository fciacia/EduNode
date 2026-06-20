"""
tools/make_pitch_deck.py
========================
Generate the 15-slide ASEAN AI Hackathon pitch deck for Edge as a .pptx.
All metrics are the real measured values from the evaluation harness — nothing
fabricated. Run: python -m tools.make_pitch_deck
"""
from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

PRIMARY = RGBColor(0x5B, 0x3F, 0xE0)   # Edge purple
DARK = RGBColor(0x20, 0x20, 0x28)
GREY = RGBColor(0x55, 0x55, 0x60)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT = RGBColor(0x1E, 0x8E, 0x3E)    # green for "measured" wins

EMU_W, EMU_H = Inches(13.333), Inches(7.5)   # 16:9


def _bg(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def _box(slide, left, top, width, height):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    return tf


def _set(p, text, size, color=DARK, bold=False, align=PP_ALIGN.LEFT, italic=False):
    p.text = text
    p.alignment = align
    r = p.runs[0]
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    r.font.name = "Calibri"


def _accent_bar(slide):
    bar = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(0.22), EMU_H)
    bar.fill.solid(); bar.fill.fore_color.rgb = PRIMARY
    bar.line.fill.background()


def content_slide(prs, title, bullets, subtitle=None):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(s, WHITE)
    _accent_bar(s)
    tf = _box(s, Inches(0.6), Inches(0.45), Inches(12.2), Inches(1.0))
    _set(tf.paragraphs[0], title, 30, PRIMARY, bold=True)
    if subtitle:
        p = tf.add_paragraph(); _set(p, subtitle, 15, GREY, italic=True)
    body = _box(s, Inches(0.7), Inches(1.7), Inches(12.0), Inches(5.3))
    first = True
    for b in bullets:
        lvl = 0
        if isinstance(b, tuple):
            b, lvl = b
        p = body.paragraphs[0] if first else body.add_paragraph()
        first = False
        marker = "•  " if lvl == 0 else "–  "
        _set(p, marker + b, 19 if lvl == 0 else 16,
             DARK if lvl == 0 else GREY, bold=False)
        p.level = lvl
        p.space_after = Pt(8)
    return s


def title_slide(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(s, PRIMARY)
    tf = _box(s, Inches(0.9), Inches(2.2), Inches(11.5), Inches(3.0))
    _set(tf.paragraphs[0], "Edge", 72, WHITE, bold=True)
    p = tf.add_paragraph(); _set(p, "AI Education at the Last Mile", 30, WHITE)
    p = tf.add_paragraph(); _set(p, " ", 12, WHITE)
    p = tf.add_paragraph()
    _set(p, "UM – Gunners  ·  University of Malaya  ·  Malaysia", 18, WHITE)
    p = tf.add_paragraph()
    _set(p, "Track: AI for Education  ·  ASEAN AI Hackathon 2026", 16, RGBColor(0xE0, 0xD8, 0xFF))
    return s


def metrics_slide(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _bg(s, WHITE); _accent_bar(s)
    tf = _box(s, Inches(0.6), Inches(0.45), Inches(12.2), Inches(1.0))
    _set(tf.paragraphs[0], "Accuracy & Efficiency Metrics", 30, PRIMARY, bold=True)
    p = tf.add_paragraph()
    _set(p, "Reproducible via the evaluation harness (tools/eval_*.py) — measured, not claimed",
         15, GREY, italic=True)

    rows = [
        ("Metric", "Result", "What it means"),
        ("Retrieval recall@k", "100%", "Correct curriculum source always retrieved"),
        ("Retrieval precision@k", "79%", "Chunks actually containing the answer's facts"),
        ("Hallucination / false-grounding", "0%", "Off-curriculum never cited as grounded"),
        ("Non-response (in-curriculum)", "0%", "No legitimate question left unanswered"),
        ("Concept coverage", "~97%", "Answers contain the required key facts"),
        ("Iban translation (chrF)", "56", "Decent for covered vocabulary; flywheel grows it"),
        ("Load test (dev node)", "0 errors", "Admission queue holds; throughput ~11 req/min"),
    ]
    tbl = s.shapes.add_table(len(rows), 3, Inches(0.7), Inches(1.9),
                             Inches(12.0), Inches(4.4)).table
    tbl.columns[0].width = Inches(4.3)
    tbl.columns[1].width = Inches(1.9)
    tbl.columns[2].width = Inches(5.8)
    for ci in range(3):
        c = tbl.cell(0, ci)
        c.text = rows[0][ci]
        c.fill.solid(); c.fill.fore_color.rgb = PRIMARY
        run = c.text_frame.paragraphs[0].runs[0]
        run.font.color.rgb = WHITE
        run.font.bold = True
        run.font.size = Pt(15)
    for ri in range(1, len(rows)):
        for ci in range(3):
            cell = tbl.cell(ri, ci)
            cell.text = rows[ri][ci]
            r = cell.text_frame.paragraphs[0].runs[0]
            r.font.size = Pt(13)
            r.font.color.rgb = ACCENT if ci == 1 else DARK
            r.font.bold = ci == 1
    note = _box(s, Inches(0.7), Inches(6.45), Inches(12.0), Inches(0.8))
    _set(note.paragraphs[0],
         "Honest note: we report concept coverage, not a single automated \"accuracy %\" — "
         "small LLM judges scored the same answers 3.4–97%, so answer correctness is being "
         "validated by human raters. On-Pi benchmarking is the next step.",
         12, GREY, italic=True)
    return s


def build() -> Path:
    prs = Presentation()
    prs.slide_width, prs.slide_height = EMU_W, EMU_H

    title_slide(prs)

    content_slide(prs, "Problem Statement", [
        "60M+ rural ASEAN learners excluded by a triple divide: no internet, no grid power, "
        "no mother-tongue AI",
        "55% of Filipino 15-year-olds score below the PISA minimum in maths; only 30% of "
        "Cambodian Grade-5 students meet basic reading (UNICEF SEA-PLM, 2019)",
        "Rural internet penetration: 18% Timor-Leste, 25% Myanmar, 28% Laos (ITU, 2023)",
        "Cloud AI (ChatGPT, etc.) is built for the connected world and fails entirely off-grid",
    ], subtitle="Why it matters — with data")

    content_slide(prs, "The AI Solution", [
        "Edge: a fully offline, solar-powered AI tutoring hub on a Raspberry Pi",
        "Broadcasts a local Wi-Fi network — students connect from their own phones, no internet",
        "An Agentic RAG pipeline delivers curriculum-grounded answers, adaptive quizzes, voice "
        "interaction and PDF microcredentials — in the student's mother tongue",
        "≈ USD 0.60 per student per year; ≈ USD 220 solar hardware, no recurring cloud cost",
    ], subtitle="The elevator pitch")

    content_slide(prs, "Competitive Advantage", [
        "100% offline — works where cloud LLMs cannot",
        "Mother-tongue incl. low-resource languages (Iban, Cebuano) excluded from mainstream models",
        "Curriculum-grounded → measured 0% hallucination / false-grounding",
        "Tiered response + confidence transparency — usable without over-restricting",
        "Solar-powered, low-cost hardware, zero recurring fees",
    ], subtitle="What makes Edge unique")

    content_slide(prs, "Technical Architecture", [
        "Inputs: voice/text queries (English + dialects), curriculum vector store, student profiles",
        "Processing (100% offline): 4-agent Agentic RAG — Translation, Personalised Context, "
        "Pedagogical Reasoning, Verification — with cross-lingual retrieval",
        "Outputs: mother-tongue answers with page-level citations, adaptive quizzes, "
        "confidence-coded UI",
        "Hardware: Raspberry Pi + solar + battery + router; two-node split (inference + app) "
        "for memory-constrained deployments",
    ], subtitle="Inputs → AI processing → outputs (see diagram)")

    content_slide(prs, "AI Approach & Model Selection", [
        "Phi-3 Mini (4-bit GGUF via Ollama) — reasoning & tutoring; small enough for edge inference",
        "paraphrase-multilingual-MiniLM-L12-v2 — cross-lingual semantic retrieval (key to the bias fix)",
        "NLLB-200-distilled-600M — NMT across ASEAN languages; glossary bridge for non-NLLB dialects",
        "Whisper.cpp + Piper — offline speech-to-text and text-to-speech",
        "Why: open-weight, permissively licensed, ARM-optimised, fully offline",
    ], subtitle="Which models, and why")

    content_slide(prs, "Data Strategy", [
        "Curriculum: OpenStax (CC BY 4.0) + national OER from KPM, DepEd, Kemendikbud + team-authored lessons",
        "Translation references: open VynerCK/Iban-language-data + teacher-verified corrections",
        "Cleaning: manual curation against ministry standards, page-level chunking, idempotent ingestion",
        "Licensing: CC BY 4.0, MIT (Phi-3), Apache 2.0 (Piper), CC BY-NC 4.0 (NLLB)",
    ], subtitle="Sources, licensing, cleaning")

    content_slide(prs, "AI Ethics & Responsibility", [
        "Bias measured & mitigated: same question, English 100% vs Thai 50% grounding → "
        "cross-lingual retrieval recovered Thai/Vietnamese to 62%, fully closed Iban",
        "Western-centric bias mitigated by using regional OER as the sole RAG context",
        "Privacy: RBAC + per-teacher identities + audit log; encryption (LUKS + encrypted USB); "
        "parental-consent record; retention purge + right-to-erasure",
        "Human oversight at every layer — curation, linguistic audit, confidence transparency",
    ], subtitle="Bias mitigation & privacy")

    content_slide(prs, "Prototype Demonstration", [
        "Demo video: https://youtu.be/Ms_y6FUbKwU",
        "Live: grounded chat with page-level citations + confidence badge",
        "Tiered AI logic: grounded (cited) → supplementary (labelled) → controlled non-response",
        "Mobile-first PWA — students connect from their own phones; teacher analytics dashboard",
    ], subtitle="Visual proof + the AI 'logic'  (insert screenshots / GIF)")

    content_slide(prs, "Technical Hurdles (honest reflection)", [
        "Hallucination in low-context queries → Verification Agent + tiered distance gates",
        "Automated LLM judges unreliable (3.4–97% spread on identical answers) → human validation",
        "Translation 'looked weak' (chrF 28) → measurement bug; scoring the translation gives chrF 56",
        "Query translation degraded retrieval for non-English → cross-lingual retrieval fix",
        "Memory on 4 GB Pi → admission queue + client-side TTS offload + two-node split",
    ], subtitle="Bugs, hallucinations and data gaps we overcame")

    metrics_slide(prs)

    content_slide(prs, "Scalability Roadmap", [
        "One hub → one school: ~50 connected students, admission-controlled (measured, 0 errors)",
        "Two-node split (inference + application) for higher concurrency on low-memory Pis",
        "Decentralized, versioned content manifest → ministries, NGOs, schools publish independently",
        "Encrypted USB sneakernet sync → update & scale with no internet",
        "One region → ASEAN-wide via per-hub language configuration",
    ], subtitle="From one school to the ASEAN region")

    content_slide(prs, "Impact Assessment", [
        "SDG 4 (Quality Education) — curriculum-grounded tutoring at the last mile",
        "SDG 10 (Reduced Inequalities) — mother-tongue access for underserved & minority-language learners",
        "SDG 9 (Infrastructure & Innovation) — resilient, off-grid education infrastructure",
        "Regional resilience: learning continuity off-grid and in crises; minority-language preservation",
    ], subtitle="Alignment with UN SDGs & regional resilience")

    content_slide(prs, "Future Roadmap", [
        "Micro-pilot in rural schools → measured learning outcomes (pre/post, small-n)",
        "On-Pi benchmarking + two-node deployment validation",
        "Fluent-speaker translation audit → sentence-level chrF; grow the dialect-glossary flywheel",
        "Stronger embedder / fine-tuned MT as verified data accrues",
        "Hardening: encryption rollout, parental-consent workflow, retention automation",
    ], subtitle="Next steps after the hackathon")

    content_slide(prs, "Team & Contact", [
        "UM – Gunners · University of Malaya · Malaysia",
        "[Member 1] — role / contribution",
        "[Member 2] — role / contribution",
        "[Member 3] — role / contribution",
        "Repository: https://github.com/fciacia/EduNode.git   ·   Demo: https://youtu.be/Ms_y6FUbKwU",
    ], subtitle="Add 3–5 short member bios + university logo")

    out = Path("docs/Edge_PitchDeck.pptx")
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    return out


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path} ({len(Presentation(path).slides._sldIdLst)} slides)")

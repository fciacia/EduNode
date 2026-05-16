"""
app.py — EduNode Flask server (production entry point)
=======================================================
Replaces asean_ai_tutor_project.py for the modular architecture.

Start:
    ollama serve &
    python -m kolibri start &   # optional
    python app.py

Or with gunicorn:
    gunicorn -w 2 -b 0.0.0.0:5000 'app:app'
"""

from __future__ import annotations

import io
import logging
import os
import re
from functools import wraps
from pathlib import Path

# Load .env file if present (must happen before any os.getenv calls)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed — env vars must be set manually

# Use the locally-cached sentence-transformer model without phoning home to
# HuggingFace on every startup.  Set before any transformers/ST import.
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("HF_DATASETS_OFFLINE", "1")
os.environ.setdefault("HF_HUB_OFFLINE", "1")

from flask import (
    Flask, jsonify, render_template, request,
    send_file, send_from_directory, abort,
)

# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_UPLOAD_MB", "32")) * 1024 * 1024

logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(name)s  %(message)s")
log = logging.getLogger("app")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
import config as cfg

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "changeme")
AUDIO_DIR   = Path(os.getenv("AUDIO_DIR", "data/audio"))


# ---------------------------------------------------------------------------
# Auth helper
# ---------------------------------------------------------------------------

def require_admin(f):
    """Decorator: require X-Admin-Token header or ?token= query param."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("X-Admin-Token") or request.args.get("token", "")
        if not token or token != ADMIN_TOKEN:
            abort(403)
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------------------------
# Startup: DB + RAG ingest
# ---------------------------------------------------------------------------

def _startup():
    from core.progress_tracker import init_db
    from core.rag_engine import ingest_pdfs
    init_db()
    ingest_pdfs("data/curriculum")


with app.app_context():
    _startup()


def _safe_retrieve_context(query: str, subject: str) -> str:
    try:
        from core.rag_engine import retrieve_context
        return retrieve_context(query, n_results=3, subject=subject)
    except Exception as exc:
        log.warning("RAG retrieval failed for %s/%s: %s", subject, query, exc)
        return ""


# ---------------------------------------------------------------------------
# Page routes
# ---------------------------------------------------------------------------

@app.get("/")
def home():
    return render_template(
        "home.html",
        region=cfg.HUB_REGION,
        languages=cfg.HUB_LANGUAGES,
        subjects=cfg.AVAILABLE_SUBJECTS,
        kolibri_port=cfg.KOLIBRI_PORT,
    )


@app.get("/chat")
def chat():
    subject  = request.args.get("subject", "General")
    language = request.args.get("lang", cfg.HUB_LANGUAGES[0])
    return render_template(
        "chat.html",
        region=cfg.HUB_REGION,
        languages=cfg.HUB_LANGUAGES,
        subjects=cfg.AVAILABLE_SUBJECTS,
        default_subject=subject,
        default_language=language,
    )


@app.get("/quiz")
def quiz():
    return render_template(
        "quiz.html",
        region=cfg.HUB_REGION,
        languages=cfg.HUB_LANGUAGES,
        subjects=cfg.AVAILABLE_SUBJECTS,
    )


@app.get("/flashcard")
def flashcard():
    return render_template(
        "flashcard.html",
        region=cfg.HUB_REGION,
        languages=cfg.HUB_LANGUAGES,
        subjects=cfg.AVAILABLE_SUBJECTS,
    )


@app.get("/podcast")
def podcast():
    return render_template(
        "podcast.html",
        region=cfg.HUB_REGION,
        languages=cfg.HUB_LANGUAGES,
        subjects=cfg.AVAILABLE_SUBJECTS,
    )


@app.get("/progress")
def progress_page():
    return render_template(
        "progress.html",
        region=cfg.HUB_REGION,
    )


@app.get("/admin")
@require_admin
def admin():
    from core.rag_engine import get_collection
    try:
        sources = _get_sources()
    except Exception:
        sources = []
    return render_template(
        "admin.html",
        region=cfg.HUB_REGION,
        sources=sources,
        hub_id=cfg.HUB_ID,
    )


@app.get("/share/<share_id>")
def share_view(share_id: str):
    from core.p2p_share import get_shared_content
    content = get_shared_content(share_id)
    if content is None:
        abort(404)
    return render_template("share_view.html", share=content)


# ---------------------------------------------------------------------------
# QR code (hub URL)
# ---------------------------------------------------------------------------

@app.get("/qr")
def qr_code():
    try:
        import qrcode
        from PIL import Image as PILImage
    except ImportError:
        abort(503, "qrcode library not installed")

    hub_url = f"http://{cfg.HUB_IP}:{os.getenv('SERVER_PORT', '5000')}"
    qr = qrcode.make(hub_url)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


# ---------------------------------------------------------------------------
# API: status
# ---------------------------------------------------------------------------

@app.get("/api/status")
def api_status():
    from core.rag_engine import get_collection
    from core.voice_engine import WHISPER_BIN, PIPER_BIN

    # Check Ollama
    ollama_ok = False
    try:
        import requests as req
        r = req.get(
            f"{os.getenv('OLLAMA_BASE', 'http://127.0.0.1:11434')}/api/tags",
            timeout=2,
        )
        ollama_ok = r.status_code == 200
    except Exception:
        pass

    # Check Kolibri
    kolibri_ok = False
    try:
        import requests as req
        r = req.get(
            f"http://localhost:{cfg.KOLIBRI_PORT}/api/public/v1/info/",
            timeout=2,
        )
        kolibri_ok = r.status_code == 200
    except Exception:
        pass

    try:
        doc_count = get_collection().count()
    except Exception:
        doc_count = 0

    return jsonify({
        "ollama":  ollama_ok,
        "tts":     PIPER_BIN.exists(),
        "stt":     WHISPER_BIN.exists(),
        "docs":    doc_count,
        "model":   os.getenv("OLLAMA_MODEL", cfg.SLM_MODEL),
        "hub":     cfg.HUB_ID,
        "region":  cfg.HUB_REGION,
        "kolibri": kolibri_ok,
    })


# ---------------------------------------------------------------------------
# API: chat
# ---------------------------------------------------------------------------

@app.post("/api/chat")
def api_chat():
    data     = request.get_json(silent=True) or {}
    message  = (data.get("message") or "").strip()
    language = (data.get("language") or cfg.HUB_LANGUAGES[0]).strip()
    subject  = (data.get("subject")  or "General").strip()
    student_name = (data.get("student_name") or "Anonymous").strip()

    if not message:
        return jsonify({"error": "message required"}), 400

    from core.llm_engine    import query_tutor
    from core.progress_tracker import get_or_create_student, log_session, log_dialect

    rag_ctx  = _safe_retrieve_context(message, subject)
    response = query_tutor(message, language, rag_ctx)

    # Log session + dialect
    sid: int | None = None
    try:
        sid = get_or_create_student(student_name, language)
        log_session(sid, subject=subject, message_count=1)
        if language.lower() != "english":
            log_dialect(language, message)
    except Exception as exc:
        log.warning("Progress logging failed: %s", exc)

    return jsonify({"response": response, "student_id": sid})


# ---------------------------------------------------------------------------
# API: voice STT
# ---------------------------------------------------------------------------

@app.post("/api/voice/stt")
def api_voice_stt():
    if "audio" not in request.files:
        return jsonify({"error": "audio file required"}), 400

    audio_bytes = request.files["audio"].read()
    if not audio_bytes:
        return jsonify({"error": "empty audio"}), 400

    from core.voice_engine import speech_to_text
    transcript = speech_to_text(audio_bytes)
    return jsonify({"text": transcript})


# ---------------------------------------------------------------------------
# API: voice TTS
# ---------------------------------------------------------------------------

@app.post("/api/voice/tts")
def api_voice_tts():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "text required"}), 400

    from core.voice_engine import text_to_speech
    wav = text_to_speech(text)
    if not wav:
        return jsonify({"error": "TTS unavailable"}), 503

    return send_file(
        io.BytesIO(wav),
        mimetype="audio/wav",
        as_attachment=False,
    )


# ---------------------------------------------------------------------------
# API: quiz generate
# ---------------------------------------------------------------------------

@app.post("/api/quiz/generate")
def api_quiz_generate():
    data     = request.get_json(silent=True) or {}
    topic    = (data.get("topic")    or "").strip()
    language = (data.get("language") or cfg.HUB_LANGUAGES[0]).strip()
    subject  = (data.get("subject")  or "General").strip()

    if not topic:
        return jsonify({"error": "topic required"}), 400

    from core.llm_engine  import generate_quiz
    from core.quiz_engine import validate_questions

    rag_ctx   = _safe_retrieve_context(topic, subject)
    raw_qs    = generate_quiz(topic, language, rag_ctx)
    questions = validate_questions(raw_qs)

    return jsonify({"questions": questions})


# ---------------------------------------------------------------------------
# API: quiz submit
# ---------------------------------------------------------------------------

@app.post("/api/quiz/submit")
def api_quiz_submit():
    data     = request.get_json(silent=True) or {}
    questions = data.get("questions", [])
    answers   = data.get("answers",   {})
    topic     = (data.get("topic")    or "General").strip()
    student_name = (data.get("student_name") or "Anonymous").strip()
    language  = (data.get("language") or cfg.HUB_LANGUAGES[0]).strip()

    from core.quiz_engine           import score_attempt
    from core.progress_tracker      import get_or_create_student, log_quiz_result
    from core.microcredential_engine import check_eligibility, generate_certificate_pdf

    result = score_attempt(questions, answers)

    sid: int | None = None
    microcredentials_earned: list[dict] = []
    try:
        sid = get_or_create_student(student_name, language)
        log_quiz_result(sid, topic, result["score"], result["total"])

        # Check all microcredentials
        from core.microcredential_engine import MICROCREDENTIALS
        for mc_topic in MICROCREDENTIALS:
            if check_eligibility(sid, mc_topic):
                pdf_path = generate_certificate_pdf(student_name, mc_topic, sid)
                microcredentials_earned.append({
                    "topic":    mc_topic,
                    "cert_url": f"/static/certificates/{Path(pdf_path).name}",
                })
    except Exception as exc:
        log.warning("Quiz submit tracking failed: %s", exc)

    return jsonify({
        "result":                  result,
        "microcredentials_earned": microcredentials_earned,
        "student_id":              sid,
    })


# ---------------------------------------------------------------------------
# API: podcast generate
# ---------------------------------------------------------------------------

@app.post("/api/podcast/generate")
def api_podcast_generate():
    data     = request.get_json(silent=True) or {}
    topic    = (data.get("topic")    or "").strip()
    language = (data.get("language") or cfg.HUB_LANGUAGES[0]).strip()

    if not topic:
        return jsonify({"error": "topic required"}), 400

    from core.podcast_engine import generate_podcast
    result = generate_podcast(topic, language)
    return jsonify({
        "script":    result["script"],
        "audio_url": result["audio_url"],
    })


# ---------------------------------------------------------------------------
# API: audio stream
# ---------------------------------------------------------------------------

@app.get("/api/audio/<filename>")
def api_audio(filename: str):
    # Whitelist: only alphanumeric, dash, underscore, dot
    if not re.fullmatch(r"[\w\-]+\.wav", filename):
        abort(400)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    return send_from_directory(str(AUDIO_DIR), filename, mimetype="audio/wav")


# ---------------------------------------------------------------------------
# API: P2P share
# ---------------------------------------------------------------------------

@app.post("/api/share/create")
def api_share_create():
    data = request.get_json(silent=True) or {}
    content      = (data.get("content")      or "").strip()
    content_type = (data.get("content_type") or "text").strip()

    if not content:
        return jsonify({"error": "content required"}), 400

    from core.p2p_share import create_share
    share = create_share(content, content_type)
    return jsonify(share)


# ---------------------------------------------------------------------------
# API: progress
# ---------------------------------------------------------------------------

@app.get("/api/progress/<int:student_id>")
def api_progress(student_id: int):
    from core.progress_tracker import get_progress
    return jsonify(get_progress(student_id))


@app.get("/api/progress/by-name/<name>")
def api_progress_by_name(name: str):
    from core.progress_tracker import find_student_by_name, get_progress
    student_id = find_student_by_name(name)
    if student_id is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(get_progress(student_id))


# ---------------------------------------------------------------------------
# API: flashcards
# ---------------------------------------------------------------------------

@app.post("/api/flashcard/generate")
def api_flashcard_generate():
    data     = request.get_json(silent=True) or {}
    topic    = (data.get("topic")    or "").strip()
    language = (data.get("language") or cfg.HUB_LANGUAGES[0]).strip()
    subject  = (data.get("subject")  or "General").strip()

    if not topic:
        return jsonify({"error": "topic required"}), 400

    from core.flashcard_engine import generate_flashcards

    rag_ctx = _safe_retrieve_context(topic, subject)
    cards   = generate_flashcards(topic, language, rag_ctx)
    return jsonify({"flashcards": cards})


# ---------------------------------------------------------------------------
# Admin API: ingest
# ---------------------------------------------------------------------------

@app.post("/api/ingest")
@require_admin
def api_ingest():
    if "file" not in request.files:
        return jsonify({"error": "file required"}), 400

    f    = request.files["file"]
    dest = Path("data/curriculum") / f.filename
    dest.parent.mkdir(parents=True, exist_ok=True)
    f.save(str(dest))

    from core.rag_engine import ingest_pdfs
    chunks = ingest_pdfs("data/curriculum")
    return jsonify({"message": f"Ingested {f.filename}", "chunks": chunks})


# ---------------------------------------------------------------------------
# Admin API: sources
# ---------------------------------------------------------------------------

def _get_sources() -> list[dict]:
    from core.rag_engine import get_collection
    col = get_collection()
    if col.count() == 0:
        return []
    results = col.get(include=["metadatas"], limit=500)
    seen: dict[str, dict] = {}
    for meta in (results.get("metadatas") or []):
        src = meta.get("source", "unknown")
        if src not in seen:
            seen[src] = {"source": src, "subject": meta.get("subject", "General"), "chunks": 0}
        seen[src]["chunks"] += 1
    return sorted(seen.values(), key=lambda x: x["source"])


@app.get("/api/sources")
@require_admin
def api_sources():
    return jsonify({"sources": _get_sources()})


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    log.info("EduNode starting on %s:%d (hub: %s)", host, port, cfg.HUB_ID)
    app.run(host=host, port=port, debug=debug, use_reloader=False)

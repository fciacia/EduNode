"""
app.py — Edge Flask server (production entry point)
=======================================================
Replaces asean_ai_tutor_project.py for the modular architecture.

Start:
    ollama serve &
    python app.py

Or with gunicorn:
    gunicorn -w 2 -b 0.0.0.0:5000 'app:app'
"""

from __future__ import annotations

import io
import json
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
ADMIN_COOKIE = "edge_admin"

if ADMIN_TOKEN == "changeme":
    log.warning("SECURITY: ADMIN_TOKEN is the default 'changeme'. Set a strong "
                "ADMIN_TOKEN in .env before deploying — teacher/admin routes are "
                "otherwise trivially accessible.")


# ---------------------------------------------------------------------------
# Auth helper
# ---------------------------------------------------------------------------

def _token_fingerprint(token: str) -> str:
    """Short, non-reversible fingerprint of a token for audit logs (never store raw)."""
    import hashlib
    if not token:
        return "anonymous"
    return "tok:" + hashlib.sha256(token.encode()).hexdigest()[:8]


def _resolve_actor(token: str) -> str:
    """Map a token to a named identity for the audit log: a registered teacher's
    name, the built-in 'admin', or an anonymised fingerprint as a fallback."""
    if not token:
        return "anonymous"
    try:
        from core.progress_tracker import find_teacher_by_token
        t = find_teacher_by_token(token)
        if t:
            return t["name"]
    except Exception:  # noqa: BLE001
        pass
    if token == ADMIN_TOKEN:
        return "admin"
    return _token_fingerprint(token)


def _is_valid_token(token: str) -> bool:
    """A token is valid if it's the admin token or a registered teacher token."""
    if token and token == ADMIN_TOKEN:
        return True
    try:
        from core.progress_tracker import find_teacher_by_token
        return find_teacher_by_token(token) is not None
    except Exception:  # noqa: BLE001
        return False


def _busy_response():
    """Uniform 503 shed when the hub is at its concurrency limit."""
    resp = jsonify({
        "error": "busy",
        "response": "The hub is helping other students right now. "
                    "Please wait a few seconds and try again.",
    })
    resp.status_code = 503
    resp.headers["Retry-After"] = "10"
    return resp


def gated_inference(f):
    """Decorator: run an LLM-heavy endpoint under the admission gate so a burst of
    students can't exhaust the hub's memory; shed with 503 if the hub is saturated."""
    @wraps(f)
    def decorated(*args, **kwargs):
        from core.request_queue import gate
        with gate.slot() as admitted:
            if not admitted:
                return _busy_response()
            return f(*args, **kwargs)
    return decorated


def require_admin(f):
    """Decorator: require X-Admin-Token header or ?token= query param.

    Every privileged access — granted or denied — is written to the audit log
    (data governance, Issue 8) with a token fingerprint rather than the raw token.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Prefer header/cookie over the URL query so the secret isn't left in
        # browser history or server access logs.
        token = (request.headers.get("X-Admin-Token")
                 or request.cookies.get(ADMIN_COOKIE)
                 or request.args.get("token", ""))
        actor = _resolve_actor(token)
        action = request.endpoint or request.path
        if not _is_valid_token(token):
            try:
                from core.progress_tracker import log_audit
                log_audit(action, actor=actor, detail=request.path, outcome="denied")
            except Exception:  # noqa: BLE001
                pass
            abort(403)
        try:
            from core.progress_tracker import log_audit
            log_audit(action, actor=actor, detail=request.path, outcome="ok")
        except Exception:  # noqa: BLE001
            pass
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------------------------
# Startup: DB + RAG ingest
# ---------------------------------------------------------------------------

def _prewarm():
    """Load heavy models in the background so the first request isn't a ~16s stall.

    Always warms the embedder (needed for retrieval + verification). Warms NLLB
    only if the hub serves a non-English language. Disable with EDGE_PREWARM=0.
    """
    try:
        from core.rag_engine import get_embedder
        get_embedder().encode(["warm up"])
        non_english = [l for l in getattr(cfg, "HUB_LANGUAGES", []) if l != "English"]
        if non_english:
            from core.agents.translation import _load
            _load()
        log.info("Prewarm complete (embedder%s).", " + NLLB" if non_english else "")
    except Exception as exc:  # noqa: BLE001
        log.warning("Prewarm failed (models will load on first use): %s", exc)


def _startup():
    from core.progress_tracker import init_db
    from core.rag_engine import ingest_pdfs
    init_db()
    ingest_pdfs("data/curriculum")

    if os.getenv("EDGE_PREWARM", "1") != "0":
        import threading
        threading.Thread(target=_prewarm, daemon=True).start()


with app.app_context():
    _startup()


_CURATED_TOPICS = {
    "Mathematics":          ["Fractions", "Percentages", "Multiplication", "Geometry shapes", "Place value"],
    "Science":              ["Photosynthesis", "The water cycle", "States of matter", "The solar system", "Food chains"],
    "English Language":     ["Parts of speech", "Nouns and verbs", "Writing a sentence", "Reading comprehension"],
    "Environmental Studies":["The water cycle", "Recycling", "Weather and climate", "Plants and animals"],
    "Digital Literacy":     ["Using a computer", "Staying safe online", "What is the internet"],
    "_default":             ["Fractions", "Photosynthesis", "The water cycle", "Parts of speech", "Map reading"],
}


def _suggest_topics(subject: str = "", limit: int = 8) -> list[str]:
    """
    Suggest study topics — derived from heading lines in the loaded curriculum
    (so they're grounded), falling back to a curated list per subject.
    """
    from core.rag_engine import _detect_subject

    topics: list[str] = []
    seen: set[str] = set()
    cdir = Path("data/curriculum")
    if cdir.exists():
        for f in sorted(cdir.glob("*.txt")) + sorted(cdir.glob("*.md")):
            if subject and subject not in ("", "General") and _detect_subject(f.name) != subject:
                continue
            try:
                lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
            except Exception:
                continue
            for i, raw in enumerate(lines):
                line = raw.strip()
                words = line.split()
                if not (1 <= len(words) <= 6) or len(line) > 60:
                    continue
                if not line[0].isalpha() or not line[0].isupper():
                    continue
                if line == line.upper() or line[-1] in ".,:;?!" or line.startswith("Example"):
                    continue
                # A heading is followed by a longer paragraph line.
                nxt = next((l.strip() for l in lines[i + 1:i + 3] if l.strip()), "")
                if len(nxt.split()) < 6:
                    continue
                key = line.lower()
                if key not in seen:
                    seen.add(key)
                    topics.append(line)

    if not topics:
        topics = _CURATED_TOPICS.get(subject, _CURATED_TOPICS["_default"])
    return topics[:limit]


_TOPIC_TX: dict[tuple[str, str], str] = {}


def _translate_topic(text: str, language: str) -> str:
    """Translate a suggested topic into the student's language (cached)."""
    key = (language, text)
    if key not in _TOPIC_TX:
        try:
            from core.agents.translation import to_native
            _TOPIC_TX[key] = to_native(text, language) or text
        except Exception:
            _TOPIC_TX[key] = text
    return _TOPIC_TX[key]


@app.get("/api/topics")
def api_topics():
    subject  = (request.args.get("subject") or "").strip()
    language = (request.args.get("language") or "").strip()
    topics = _suggest_topics(subject)
    if language and language != cfg.HUB_LANGUAGES[0]:        # not English
        topics = [_translate_topic(t, language) for t in topics]
    return jsonify({"topics": topics})


def _grounded_context(query: str, subject: str):
    """
    Citation-aware retrieval shared by quiz and flashcard generation.

    Returns (context_str, grounded, sources):
      context_str : passages joined for the LLM prompt ("" if none)
      grounded    : True when the best chunk is within the retrieval gate (0.65),
                    i.e. the curriculum actually covers this topic
      sources     : list of {"source", "page"} when grounded, else []
    """
    try:
        from core.rag_engine import retrieve_with_citations
        chunks = retrieve_with_citations(query, n_results=3, subject=subject)
    except Exception as exc:
        log.warning("RAG retrieval failed for %s/%s: %s", subject, query, exc)
        return "", False, []

    if not chunks:
        return "", False, []

    context  = "\n---\n".join(c.text for c in chunks)
    grounded = min(c.distance for c in chunks) <= 0.65

    sources: list[dict] = []
    if grounded:
        for c in chunks:
            entry = {"source": c.source, "page": c.page}
            if entry not in sources:
                sources.append(entry)

    return context, grounded, sources


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


@app.get("/slides")
def slides():
    return render_template(
        "slides.html",
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


@app.get("/teacher")
@require_admin
def teacher_dashboard():
    return render_template("teacher.html", hub_id=cfg.HUB_ID, region=cfg.HUB_REGION)


@app.get("/api/teacher/analytics")
@require_admin
def api_teacher_analytics():
    from core.analytics_engine import dashboard
    return jsonify(dashboard())


@app.get("/api/audit")
@require_admin
def api_audit():
    """Return recent privileged-access audit entries (data governance)."""
    from core.progress_tracker import get_audit_log
    return jsonify({"entries": get_audit_log()})


@app.post("/api/admin/login")
def api_admin_login():
    """Exchange the admin token for an HttpOnly cookie so it stops riding in URLs
    (out of browser history and access logs). JS can't read the cookie."""
    from core.progress_tracker import log_audit
    data = request.get_json(silent=True) or request.form
    token = (data.get("token") or "").strip()
    actor = _resolve_actor(token)
    if not _is_valid_token(token):
        log_audit("admin_login", actor=actor, detail="/api/admin/login", outcome="denied")
        return jsonify({"error": "invalid token"}), 403
    resp = jsonify({"ok": True, "actor": actor})
    resp.set_cookie(ADMIN_COOKIE, token, httponly=True, samesite="Strict", max_age=43200)
    log_audit("admin_login", actor=actor, detail="/api/admin/login", outcome="ok")
    return resp


@app.post("/api/admin/teachers")
@require_admin
def api_register_teacher():
    """Register a named teacher identity (admin only) so the audit log attributes
    actions to a person, not a shared token."""
    from core.progress_tracker import register_teacher
    data = request.get_json(silent=True) or {}
    name  = (data.get("name") or "").strip()
    token = (data.get("token") or "").strip()
    role  = (data.get("role") or "teacher").strip()
    if not name or not token:
        return jsonify({"error": "name and token required"}), 400
    tid = register_teacher(name, token, role)
    return jsonify({"ok": True, "id": tid, "name": name, "role": role})


@app.post("/api/consent")
@require_admin
def api_record_consent():
    """Record parental/guardian consent for a student (teacher/admin only).
    The consenting act happens off-system; this stores who confirmed it and when."""
    from core.progress_tracker import record_consent, get_consent
    token = (request.headers.get("X-Admin-Token")
             or request.cookies.get(ADMIN_COOKIE) or request.args.get("token", ""))
    data = request.get_json(silent=True) or {}
    sid = data.get("student_id")
    if not sid:
        return jsonify({"error": "student_id required"}), 400
    granted = bool(data.get("granted", True))
    record_consent(int(sid), granted, recorded_by=_resolve_actor(token))
    return jsonify({"ok": True, "consent": get_consent(int(sid))})


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

    try:
        doc_count = get_collection().count()
    except Exception:
        doc_count = 0

    from core.request_queue import gate

    return jsonify({
        "ollama":  ollama_ok,
        "tts":     PIPER_BIN.exists(),
        "stt":     WHISPER_BIN.exists(),
        "docs":    doc_count,
        "model":   os.getenv("OLLAMA_MODEL", cfg.SLM_MODEL),
        "hub":     cfg.HUB_ID,
        "region":  cfg.HUB_REGION,
        "queue":   gate.stats(),
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
    conversation_id = (data.get("conversation_id") or "").strip() or None

    if not message:
        return jsonify({"error": "message required"}), 400

    from core.llm_engine        import query_tutor
    from core.progress_tracker  import get_or_create_student, log_session, log_dialect

    # Resolve student first so the context agent can personalise.
    sid: int | None = None
    try:
        sid = get_or_create_student(student_name, language)
    except Exception as exc:
        log.warning("Student resolution failed: %s", exc)

    # Admission control: cap concurrent heavy inferences so a burst of students
    # can't exhaust the hub's memory. Excess requests wait briefly, then get a
    # graceful "busy" instead of crashing the node.
    from core.request_queue import gate
    with gate.slot() as admitted:
        if not admitted:
            resp = jsonify({
                "error": "busy",
                "response": "The hub is helping other students right now. "
                            "Please wait a few seconds and ask again.",
            })
            resp.status_code = 503
            resp.headers["Retry-After"] = "10"
            return resp
        result = query_tutor(message, language, student_id=sid, subject=subject,
                             conversation_id=conversation_id)

    try:
        if sid is not None:
            log_session(sid, subject=subject, message_count=1)
        if language.lower() != "english":
            log_dialect(language, message)
    except Exception as exc:
        log.warning("Progress logging failed: %s", exc)

    return jsonify({
        "response":     result["answer"],
        "confidence":   result["confidence"],
        "needs_review": result["needs_review"],
        "tier":         result.get("tier", "grounded"),
        "citations":    result["citations"],
        "language":     result["language"],
        "student_id":   sid,
    })


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

    language = (request.form.get("language") or "auto").strip()

    from core.voice_engine import speech_to_text
    transcript = speech_to_text(audio_bytes, language)
    return jsonify({"text": transcript})


# ---------------------------------------------------------------------------
# API: voice TTS
# ---------------------------------------------------------------------------

@app.post("/api/voice/tts")
def api_voice_tts():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    language = (data.get("language") or "English").strip()
    if not text:
        return jsonify({"error": "text required"}), 400

    from core.voice_engine import text_to_speech
    wav = text_to_speech(text, language)
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
@gated_inference
def api_quiz_generate():
    data     = request.get_json(silent=True) or {}
    topic    = (data.get("topic")    or "").strip()
    language = (data.get("language") or cfg.HUB_LANGUAGES[0]).strip()
    subject  = (data.get("subject")  or "General").strip()

    if not topic:
        return jsonify({"error": "topic required"}), 400

    level    = (data.get("level") or "").strip()

    from core import content_cache
    cached = content_cache.get("quiz", subject, language, level, topic)
    if cached is not None:
        return jsonify(cached)

    from core.llm_engine  import generate_quiz, ollama_available
    from core.quiz_engine import validate_questions

    if not ollama_available():
        return jsonify({"questions": [], "error": "offline"}), 503

    rag_ctx, grounded, sources = _grounded_context(topic, subject)
    raw_qs    = generate_quiz(topic, language, rag_ctx, level)
    questions = validate_questions(raw_qs)

    payload = {"questions": questions, "grounded": grounded, "sources": sources}
    if not questions:
        payload["error"] = "generation"
    else:
        content_cache.put("quiz", subject, language, level, topic, payload)
    return jsonify(payload)


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
@gated_inference
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
# API: curriculum diagrams / media (for flashcards)
# ---------------------------------------------------------------------------

from core.media import MEDIA_DIR, find_media


@app.get("/api/media/<filename>")
def api_media(filename: str):
    """
    Serve a curriculum diagram for a flashcard. Teachers drop images into
    data/media/. The AI suggests a filename; we match tolerantly by stem so a
    suggested "photosynthesis.png" can resolve to a "photosynthesis.svg" on disk.
    """
    if not re.fullmatch(r"[\w\-]+\.(png|jpg|jpeg|gif|webp|svg)", filename or ""):
        abort(400)
    if not MEDIA_DIR.exists():
        abort(404)

    target = MEDIA_DIR / filename
    if not target.exists():
        stem = Path(filename).stem.lower()
        match = next((p for p in MEDIA_DIR.iterdir()
                      if p.is_file() and p.stem.lower() == stem), None)
        if not match:
            abort(404)
        target = match
    return send_from_directory(str(MEDIA_DIR), target.name)


@app.get("/api/media/find")
def api_media_find():
    """Best-effort: return a local image whose filename shares a keyword with
    the query, so a slide's image_query ('green leaf') can surface a matching
    diagram if a teacher has dropped one in. Returns {"file": null} otherwise."""
    match = find_media(request.args.get("q") or "")
    return jsonify({"file": match.name if match else None})


@app.post("/api/translation/report")
def api_translation_report():
    """Log a student/teacher flag that a translation looks wrong, for review
    (and feeding back into the dialect glossary flywheel)."""
    from datetime import datetime, timezone
    data  = request.get_json(silent=True) or {}
    entry = {
        "ts":       datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "language": (data.get("language") or "").strip()[:60],
        "shown":    (data.get("shown") or "").strip()[:500],
        "note":     (data.get("note") or "").strip()[:500],
        "page":     (data.get("page") or "").strip()[:120],
    }
    path = Path("data/translation_reports.jsonl")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return jsonify({"ok": True})


@app.post("/api/translation/correct")
@require_admin
def api_translation_correct():
    """Teacher submits a verified correction for a flagged translation.
    Stored as supervised data for fine-tuning future translation models."""
    from core.correction_store import save_correction
    data = request.get_json(silent=True) or request.form
    try:
        entry = save_correction(
            language=(data.get("language") or ""),
            original=(data.get("original") or ""),
            corrected=(data.get("corrected") or ""),
            english=(data.get("english") or ""),
            note=(data.get("note") or ""),
            by=(data.get("by") or "teacher"),
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"ok": True, "entry": entry})


@app.get("/api/translation/corrections")
@require_admin
def api_translation_corrections():
    from core.correction_store import list_corrections, count
    language = (request.args.get("language") or "").strip() or None
    return jsonify({"corrections": list_corrections(language=language),
                    "count": count(language=language)})


# ---------------------------------------------------------------------------
# API: slides (offline lesson deck generator)
# ---------------------------------------------------------------------------

@app.post("/api/slides/generate")
@gated_inference
def api_slides_generate():
    data     = request.get_json(silent=True) or {}
    topic    = (data.get("topic")    or "").strip()
    language = (data.get("language") or cfg.HUB_LANGUAGES[0]).strip()
    subject  = (data.get("subject")  or "General").strip()

    if not topic:
        return jsonify({"error": "topic required"}), 400

    level    = (data.get("level") or "").strip()

    from core import content_cache
    cached = content_cache.get("slides", subject, language, level, topic)
    if cached is not None:
        return jsonify(cached)

    from core.slide_engine import generate_slides
    from core.llm_engine   import ollama_available

    if not ollama_available():
        return jsonify({"slides": [], "error": "offline"}), 503

    rag_ctx, grounded, sources = _grounded_context(topic, subject)
    slides = generate_slides(topic, language, rag_ctx, level)

    payload = {"slides": slides, "grounded": grounded, "sources": sources}
    if not slides:
        payload["error"] = "generation"
    else:
        content_cache.put("slides", subject, language, level, topic, payload)
    return jsonify(payload)


@app.post("/api/slides/download")
def api_slides_download():
    """Export the current deck as a .pdf or .pptx for offline study."""
    data   = request.get_json(silent=True) or {}
    topic  = (data.get("topic") or "slides").strip()
    slides = data.get("slides") or []
    fmt    = (data.get("format") or "pptx").lower()
    if not slides:
        return jsonify({"error": "no slides"}), 400

    if fmt == "pdf":
        from core.pdf_export import build_pdf
        blob, mime, ext = build_pdf(topic, slides), "application/pdf", "pdf"
    else:
        from core.pptx_export import build_pptx
        blob = build_pptx(topic, slides)
        mime = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        ext  = "pptx"

    fname = re.sub(r"[^A-Za-z0-9]+", "_", topic).strip("_") or "slides"
    return send_file(io.BytesIO(blob), mimetype=mime, as_attachment=True,
                     download_name=f"{fname}.{ext}")


# ---------------------------------------------------------------------------
# Admin API: glossary editor (dialect flywheel)
# ---------------------------------------------------------------------------

@app.post("/api/glossary/add")
@require_admin
def api_glossary_add():
    """Teachers add a word to a low-resource-language glossary (e.g. Iban)."""
    data     = request.get_json(silent=True) or request.form
    language = (data.get("language") or "").strip()
    english  = (data.get("english")  or "").strip().lower()
    native   = (data.get("native")   or "").strip()
    if not language or not english or not native:
        return jsonify({"error": "language, english and native are required"}), 400

    from core.llm_engine import GLOSSARY_DIR
    GLOSSARY_DIR.mkdir(parents=True, exist_ok=True)
    path = GLOSSARY_DIR / f"{language.lower()}.json"

    terms: dict = {}
    attribution = "Includes teacher-contributed terms (Edge dialect flywheel)."
    if path.exists():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                attribution = loaded.pop("_attribution", attribution)
                terms = {k: v for k, v in loaded.items() if not str(k).startswith("_")}
            elif isinstance(loaded, list):
                terms = {e["english"].lower(): e["native"] for e in loaded
                         if isinstance(e, dict) and e.get("english") and e.get("native")}
        except Exception as exc:  # noqa: BLE001
            log.warning("Glossary read failed for %s: %s", language, exc)

    terms[english] = native
    ordered = {"_attribution": attribution}
    for k in sorted(terms):
        ordered[k] = terms[k]
    path.write_text(json.dumps(ordered, ensure_ascii=False, indent=2), encoding="utf-8")

    return jsonify({"ok": True, "language": language, "english": english,
                    "native": native, "count": len(terms)})


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


@app.get("/api/recommendations/<int:student_id>")
def api_recommendations(student_id: int):
    """Adaptive learning pathway: per-concept mastery + remedial next steps."""
    from core.mastery_engine import concept_mastery, recommendations
    return jsonify({
        "mastery": concept_mastery(student_id),
        "recommendations": recommendations(student_id),
    })


@app.get("/api/recommendations/by-name/<name>")
def api_recommendations_by_name(name: str):
    from core.progress_tracker import find_student_by_name
    from core.mastery_engine import concept_mastery, recommendations
    student_id = find_student_by_name(name)
    if student_id is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({
        "mastery": concept_mastery(student_id),
        "recommendations": recommendations(student_id),
    })


# ---------------------------------------------------------------------------
# API: flashcards
# ---------------------------------------------------------------------------

@app.post("/api/flashcard/generate")
@gated_inference
def api_flashcard_generate():
    data     = request.get_json(silent=True) or {}
    topic    = (data.get("topic")    or "").strip()
    language = (data.get("language") or cfg.HUB_LANGUAGES[0]).strip()
    subject  = (data.get("subject")  or "General").strip()

    if not topic:
        return jsonify({"error": "topic required"}), 400

    level    = (data.get("level") or "").strip()

    from core import content_cache
    cached = content_cache.get("cards", subject, language, level, topic)
    if cached is not None:
        return jsonify(cached)

    from core.flashcard_engine import generate_flashcards
    from core.llm_engine import ollama_available

    if not ollama_available():
        return jsonify({"flashcards": [], "error": "offline"}), 503

    rag_ctx, grounded, sources = _grounded_context(topic, subject)
    cards   = generate_flashcards(topic, language, rag_ctx, level)

    payload = {"flashcards": cards, "grounded": grounded, "sources": sources}
    if not cards:
        payload["error"] = "generation"
    else:
        content_cache.put("cards", subject, language, level, topic, payload)
    return jsonify(payload)


@app.post("/api/diagram")
@gated_inference
def api_diagram():
    """Return a validated maths-diagram spec for a question (or {diagram:null}).
    Best-effort + cached; the frontend renders the spec as exact SVG."""
    data     = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()
    subject  = (data.get("subject")  or "").strip()
    language = (data.get("language") or cfg.HUB_LANGUAGES[0]).strip()
    if not question:
        return jsonify({"diagram": None})

    from core import content_cache
    cached = content_cache.get("diagram", subject, language, "", question)
    if cached is not None:
        return jsonify(cached)

    from core.llm_engine import ollama_available
    if not ollama_available():
        return jsonify({"diagram": None})

    from core.diagram_engine import generate_diagram
    # No RAG context: diagrams come from the question's own numbers, and
    # retrieved prose tends to confuse the small model's structured output.
    spec = generate_diagram(question, "", language)
    if spec and spec.get("type") == "image":
        match = find_media(spec.get("query", ""))   # resolve to a real labelled picture
        spec = {"type": "image", "file": match.name} if match else None
    payload = {"diagram": spec}
    if spec:
        content_cache.put("diagram", subject, language, "", question, payload)
    return jsonify(payload)


# ---------------------------------------------------------------------------
# API: spaced repetition (flashcard reviews)
# ---------------------------------------------------------------------------

@app.post("/api/review/save")
def api_review_save():
    data    = request.get_json(silent=True) or {}
    name    = (data.get("student_name") or "").strip()
    front   = (data.get("front")   or "").strip()
    back    = (data.get("back")    or "").strip()
    topic   = (data.get("topic")   or "").strip()
    verdict = (data.get("verdict") or "review").strip()
    if not name or not front:
        return jsonify({"error": "student_name and front required"}), 400

    from core.progress_tracker import get_or_create_student
    from core.review_engine     import save_review, count_due

    try:
        sid = get_or_create_student(name, "English")
        save_review(sid, topic, front, back, verdict)
        return jsonify({"ok": True, "due": count_due(sid)})
    except Exception as exc:  # noqa: BLE001
        log.warning("Review save failed: %s", exc)
        return jsonify({"ok": False}), 500


@app.get("/api/review/due")
def api_review_due():
    name = (request.args.get("student") or "").strip()
    if not name:
        return jsonify({"cards": [], "count": 0})

    from core.progress_tracker import find_student_by_name
    from core.review_engine     import get_due, count_due

    sid = find_student_by_name(name)
    if not sid:
        return jsonify({"cards": [], "count": 0})

    cards = [{"title": c["front"], "body": c["back"], "topic": c["topic"]} for c in get_due(sid)]
    return jsonify({"cards": cards, "count": count_due(sid)})


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
    log.info("Edge starting on %s:%d (hub: %s)", host, port, cfg.HUB_ID)
    app.run(host=host, port=port, debug=debug, use_reloader=False)

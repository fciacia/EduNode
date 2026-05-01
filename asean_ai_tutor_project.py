#!/usr/bin/env python3
"""
EduNode — Offline AI Tutor for ASEAN Schools
=============================================
Runs entirely on a Raspberry Pi 5 (or any Linux box).
Students connect over local WiFi — no internet required.

Quick start:
    python asean_ai_tutor_project.py
    # → visit http://<your-ip>:5000  or scan the QR code printed in terminal
"""

# =============================================================================
# PHASE 0: ENVIRONMENT SETUP  (Day 1-2)
# =============================================================================
#
# HARDWARE (for demo, use your laptop first):
#   - Raspberry Pi 5 (8GB RAM) OR any Linux machine for dev
#   - 256GB SSD
#   - TP-Link TL-WR902AC or any portable router
#
# SOFTWARE INSTALLS (run on Pi terminal):
#
#   # 1. Install Ollama (runs the SLM locally)
#   curl -fsSL https://ollama.com/install.sh | sh
#   ollama pull llama3.2:3b-instruct-q4_K_M    # ~2GB — fits in Pi 5 RAM
#   # Alternative: ollama pull gemma2:2b-instruct-q4_K_M
#
#   # 2. Install Python dependencies
#   pip install flask chromadb sentence-transformers \
#               pypdf piper-tts qrcode pillow \
#               requests python-dotenv gunicorn
#
#   # 3. Install Whisper.cpp (compiled binary for ARM64)
#   git clone https://github.com/ggerganov/whisper.cpp
#   cd whisper.cpp && make
#   bash ./models/download-ggml-model.sh base.en   # ~150MB
#
#   # 4. Configure router
#   - Set Pi's static IP to 192.168.1.1
#   - Router DHCP serves 192.168.1.2 - 192.168.1.254
#   - Students navigate to http://edunode.local OR http://192.168.1.1

# =============================================================================
# PHASE 1: IMPORTS & CONFIGURATION  (Day 3)
# =============================================================================

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request,
    send_file,
    send_from_directory,
)

load_dotenv()

# ── Logging ────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("edunode")

# ── Directory layout ───────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).parent
DATA_DIR      = BASE_DIR / "data"
CHROMA_DIR    = DATA_DIR / "chroma"
UPLOADS_DIR   = DATA_DIR / "uploads"
AUDIO_OUT_DIR = DATA_DIR / "audio"
MODELS_DIR    = BASE_DIR / "models"

PIPER_BIN     = MODELS_DIR / "piper" / "piper"
PIPER_MODEL   = MODELS_DIR / "piper" / "en_US-lessac-medium.onnx"
WHISPER_BIN   = BASE_DIR / "whisper.cpp" / "main"
WHISPER_MODEL = BASE_DIR / "whisper.cpp" / "models" / "ggml-base.en.bin"

for _d in [DATA_DIR, CHROMA_DIR, UPLOADS_DIR, AUDIO_OUT_DIR, MODELS_DIR]:
    _d.mkdir(parents=True, exist_ok=True)

# ── Tunables (override via .env) ───────────────────────────────────────────
OLLAMA_BASE    = os.getenv("OLLAMA_BASE",    "http://127.0.0.1:11434")
OLLAMA_MODEL   = os.getenv("OLLAMA_MODEL",   "llama3.2:3b-instruct-q4_K_M")
EMBED_MODEL    = os.getenv("EMBED_MODEL",    "all-MiniLM-L6-v2")
CHUNK_SIZE     = int(os.getenv("CHUNK_SIZE",    "400"))
CHUNK_OVERLAP  = int(os.getenv("CHUNK_OVERLAP", "60"))
TOP_K          = int(os.getenv("TOP_K",         "5"))
MAX_TOKENS     = int(os.getenv("MAX_TOKENS",    "512"))
SERVER_HOST    = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT    = int(os.getenv("SERVER_PORT", "5000"))
ADMIN_TOKEN    = os.getenv("ADMIN_TOKEN", "change-me-in-dot-env")
MAX_UPLOAD_MB  = int(os.getenv("MAX_UPLOAD_MB", "32"))

SYSTEM_PROMPT = (
    "You are EduNode, a friendly and encouraging AI tutor for students in ASEAN "
    "schools. Explain concepts clearly using simple language. Base your answers on "
    "the provided context when available. If unsure, say so honestly. "
    "Keep responses concise (3-5 sentences) unless a longer explanation is needed."
)

# =============================================================================
# PHASE 2: RAG PIPELINE — ChromaDB + sentence-transformers  (Day 4-5)
# =============================================================================

try:
    import chromadb
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
except ImportError:
    log.error("Run: pip install chromadb sentence-transformers")
    sys.exit(1)

_embed_fn   = SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)
_chroma     = chromadb.PersistentClient(path=str(CHROMA_DIR))
_collection = _chroma.get_or_create_collection(
    name="edunode",
    embedding_function=_embed_fn,
    metadata={"hnsw:space": "cosine"},
)


def _chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split *text* into overlapping word-level chunks."""
    words  = text.split()
    chunks: list[str] = []
    step   = max(1, size - overlap)
    for i in range(0, len(words), step):
        chunk = " ".join(words[i : i + size])
        if chunk:
            chunks.append(chunk)
    return chunks


def retrieve(query: str, k: int = TOP_K, subject: Optional[str] = None) -> list[str]:
    """Return the top-k context passages for *query*."""
    total = _collection.count()
    if total == 0:
        return []
    where   = {"subject": subject} if subject else None
    results = _collection.query(
        query_texts=[query],
        n_results=min(k, total),
        where=where,
    )
    return results["documents"][0] if results["documents"] else []


# =============================================================================
# PHASE 3: DOCUMENT INGESTION — PDF / TXT → chunks → ChromaDB  (Day 5)
# =============================================================================

try:
    import pypdf
    _PYPDF_OK = True
except ImportError:
    log.warning("pypdf not installed — PDF ingestion disabled")
    _PYPDF_OK = False


def ingest_file(path: Path, subject: str = "general", grade: str = "unset") -> int:
    """
    Ingest a PDF or plain-text file into the vector store.
    Returns the number of chunks added.
    """
    path   = Path(path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        if not _PYPDF_OK:
            raise RuntimeError("pypdf is required for PDF ingestion")
        reader   = pypdf.PdfReader(str(path))
        raw_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    elif suffix in {".txt", ".md"}:
        raw_text = path.read_text(encoding="utf-8", errors="replace")
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    raw_text = re.sub(r"\s+", " ", raw_text).strip()
    if not raw_text:
        raise ValueError("No extractable text found in file")

    chunks    = _chunk_text(raw_text)
    ids, documents, metadatas = [], [], []
    for i, chunk in enumerate(chunks):
        doc_id = hashlib.sha1(
            f"{path.name}:{i}:{chunk[:60]}".encode()
        ).hexdigest()[:16]
        ids.append(doc_id)
        documents.append(chunk)
        metadatas.append({
            "source":  path.name,
            "subject": subject,
            "grade":   grade,
            "chunk":   i,
        })

    # Upsert so re-ingesting the same file is idempotent
    _collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    log.info(
        "Ingested %d chunks from '%s' [%s / grade %s]",
        len(chunks), path.name, subject, grade,
    )
    return len(chunks)


def list_sources() -> list[dict]:
    """Return unique source documents currently in the vector store."""
    if _collection.count() == 0:
        return []
    results = _collection.get(include=["metadatas"])
    seen: dict[str, dict] = {}
    for meta in results["metadatas"]:
        src = meta.get("source", "unknown")
        if src not in seen:
            seen[src] = {
                "source":  src,
                "subject": meta.get("subject"),
                "grade":   meta.get("grade"),
            }
    return list(seen.values())


# =============================================================================
# PHASE 4: OLLAMA LLM CLIENT  (Day 6)
# =============================================================================

def ollama_chat(
    user_message: str,
    context_passages: Optional[list[str]] = None,
) -> str:
    """
    Send a chat request to the local Ollama instance.
    Injects RAG context into the user turn when passages are supplied.
    """
    if context_passages:
        context_block = "\n\n".join(
            f"[Source {i + 1}]: {p}" for i, p in enumerate(context_passages)
        )
        user_content = (
            f"Use the following context to answer the question.\n\n"
            f"CONTEXT:\n{context_block}\n\n"
            f"QUESTION: {user_message}"
        )
    else:
        user_content = user_message

    payload = {
        "model":  OLLAMA_MODEL,
        "stream": False,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_content},
        ],
        "options": {
            "num_predict": MAX_TOKENS,
            "temperature": 0.7,
        },
    }

    try:
        resp = requests.post(
            f"{OLLAMA_BASE}/api/chat",
            json=payload,
            timeout=120,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        log.error("Ollama request failed: %s", exc)
        return "Sorry — the AI engine is currently unavailable. Please try again shortly."

    return resp.json().get("message", {}).get("content", "").strip()


def ollama_available() -> bool:
    """Return True if Ollama is running and the target model is present."""
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=3)
        if r.ok:
            models = [m["name"] for m in r.json().get("models", [])]
            return any(OLLAMA_MODEL.split(":")[0] in m for m in models)
    except Exception:
        pass
    return False


# =============================================================================
# PHASE 5: SPEECH — Whisper.cpp STT  +  Piper TTS  (Day 7-8)
# =============================================================================

def transcribe_audio(audio_path: Path) -> str:
    """
    Run Whisper.cpp on *audio_path* and return the transcript.
    Converts to 16 kHz mono WAV first via ffmpeg (if available).
    Returns an empty string when Whisper is not installed.
    """
    if not WHISPER_BIN.exists():
        log.warning("whisper.cpp binary not found at %s — STT disabled", WHISPER_BIN)
        return ""
    if not WHISPER_MODEL.exists():
        log.warning("Whisper model not found — STT disabled")
        return ""

    # Convert to 16 kHz mono WAV (whisper.cpp requirement)
    wav_path = audio_path.with_suffix(".wav")
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(audio_path),
             "-ar", "16000", "-ac", "1", str(wav_path)],
            check=True, capture_output=True, timeout=30,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        wav_path = audio_path  # best effort

    try:
        result = subprocess.run(
            [
                str(WHISPER_BIN),
                "-m", str(WHISPER_MODEL),
                "-f", str(wav_path),
                "--output-txt",
                "--no-timestamps",
                "-t", "4",
            ],
            capture_output=True, text=True, timeout=60, check=True,
        )
        lines = []
        for line in result.stdout.splitlines():
            line = re.sub(r"^\[.*?\]\s*", "", line).strip()
            if line:
                lines.append(line)
        return " ".join(lines)
    except subprocess.CalledProcessError as exc:
        log.error("Whisper failed: %s", exc.stderr[:200])
        return ""
    except subprocess.TimeoutExpired:
        log.error("Whisper timed out")
        return ""


def synthesize_speech(text: str) -> Optional[Path]:
    """
    Synthesize *text* to a WAV file using Piper TTS.
    Returns the path to the output file, or None if Piper is unavailable.
    """
    if not PIPER_BIN.exists():
        log.warning("Piper binary not found at %s — TTS disabled", PIPER_BIN)
        return None
    if not PIPER_MODEL.exists():
        log.warning("Piper model not found — TTS disabled")
        return None

    out_path = AUDIO_OUT_DIR / f"{uuid.uuid4().hex}.wav"
    try:
        subprocess.run(
            [
                str(PIPER_BIN),
                "--model",       str(PIPER_MODEL),
                "--output_file", str(out_path),
            ],
            input=text,
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
        return out_path if out_path.exists() else None
    except subprocess.CalledProcessError as exc:
        log.error("Piper failed: %s", exc.stderr[:200])
        return None
    except subprocess.TimeoutExpired:
        log.error("Piper timed out")
        return None


# =============================================================================
# PHASE 6: FLASK APPLICATION  (Day 9-10)
# =============================================================================

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024

ALLOWED_AUDIO_EXTS = {".webm", ".wav", ".ogg", ".mp3", ".m4a"}
ALLOWED_DOC_EXTS   = {".pdf", ".txt", ".md"}


def _require_admin() -> bool:
    """Validate the admin token from Bearer header, X-Admin-Token, or form field."""
    token = (
        request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
        or request.headers.get("X-Admin-Token", "")
        or request.form.get("admin_token", "")
    )
    return token == ADMIN_TOKEN


# ── Student-facing routes ──────────────────────────────────────────────────

@app.get("/")
def index():
    return render_template("index.html", model=OLLAMA_MODEL)


@app.post("/api/ask")
def api_ask():
    """Text Q&A endpoint.  Returns JSON {answer, tts_url}."""
    data     = request.get_json(force=True, silent=True) or {}
    question = (data.get("question") or "").strip()
    subject  = data.get("subject") or None
    tts_want = bool(data.get("tts", False))

    if not question:
        return jsonify(error="question is required"), 400
    if len(question) > 2000:
        return jsonify(error="question too long (max 2000 chars)"), 400

    passages = retrieve(question, subject=subject)
    answer   = ollama_chat(question, context_passages=passages or None)

    tts_url = None
    if tts_want:
        audio_path = synthesize_speech(answer)
        if audio_path:
            tts_url = f"/api/audio/{audio_path.name}"

    return jsonify(answer=answer, tts_url=tts_url)


@app.post("/api/voice")
def api_voice():
    """
    Voice Q&A endpoint.
    Accepts multipart/form-data with field 'audio' (WebM / WAV / OGG).
    Returns JSON {transcript, answer, tts_url}.
    """
    if "audio" not in request.files:
        return jsonify(error="audio file required"), 400

    audio_file = request.files["audio"]
    suffix     = Path(audio_file.filename or "audio.webm").suffix.lower()
    if suffix not in ALLOWED_AUDIO_EXTS:
        return jsonify(error="unsupported audio format"), 415

    with tempfile.NamedTemporaryFile(
        dir=AUDIO_OUT_DIR, suffix=suffix, delete=False
    ) as tmp:
        tmp_path = Path(tmp.name)
        audio_file.save(tmp_path)

    try:
        transcript = transcribe_audio(tmp_path)
    finally:
        tmp_path.unlink(missing_ok=True)
        tmp_path.with_suffix(".wav").unlink(missing_ok=True)

    if not transcript:
        return jsonify(
            error="Could not transcribe audio. Please speak more clearly and try again."
        ), 422

    subject  = request.form.get("subject") or None
    passages = retrieve(transcript, subject=subject)
    answer   = ollama_chat(transcript, context_passages=passages or None)

    tts_url    = None
    audio_path = synthesize_speech(answer)
    if audio_path:
        tts_url = f"/api/audio/{audio_path.name}"

    return jsonify(transcript=transcript, answer=answer, tts_url=tts_url)


@app.get("/api/audio/<filename>")
def serve_audio(filename: str):
    """Serve a Piper-synthesised audio file."""
    if not re.fullmatch(r"[A-Za-z0-9_.\-]+", filename):
        abort(400)
    return send_from_directory(AUDIO_OUT_DIR, filename, mimetype="audio/wav")


@app.get("/api/status")
def api_status():
    """Health / capability status used by the frontend UI."""
    return jsonify(
        ollama=ollama_available(),
        tts=PIPER_BIN.exists() and PIPER_MODEL.exists(),
        stt=WHISPER_BIN.exists() and WHISPER_MODEL.exists(),
        docs=_collection.count(),
        model=OLLAMA_MODEL,
    )


# ── Admin routes ───────────────────────────────────────────────────────────

@app.get("/admin")
def admin_panel():
    if not _require_admin():
        abort(401)
    return render_template("admin.html", sources=list_sources(), model=OLLAMA_MODEL)


@app.post("/api/ingest")
def api_ingest():
    """
    Upload and ingest a curriculum document (PDF / TXT / MD).
    Requires the admin token in X-Admin-Token header or admin_token form field.
    """
    if not _require_admin():
        return jsonify(error="Unauthorized"), 401

    if "file" not in request.files:
        return jsonify(error="file field required"), 400

    uploaded = request.files["file"]
    subject  = (request.form.get("subject") or "general").strip()[:64]
    grade    = (request.form.get("grade")   or "unset").strip()[:16]

    suffix = Path(uploaded.filename or "doc.pdf").suffix.lower()
    if suffix not in ALLOWED_DOC_EXTS:
        return jsonify(error=f"Unsupported file type: {suffix}"), 415

    # Use a UUID-based name to prevent path traversal
    safe_name = f"{uuid.uuid4().hex}{suffix}"
    dest_path = UPLOADS_DIR / safe_name
    uploaded.save(dest_path)

    try:
        n_chunks = ingest_file(dest_path, subject=subject, grade=grade)
    except (ValueError, RuntimeError) as exc:
        dest_path.unlink(missing_ok=True)
        return jsonify(error=str(exc)), 422

    return jsonify(
        message=f"Ingested {n_chunks} chunks from '{uploaded.filename}'",
        chunks=n_chunks,
    ), 201


@app.get("/api/sources")
def api_sources():
    if not _require_admin():
        return jsonify(error="Unauthorized"), 401
    return jsonify(sources=list_sources())


# ── QR code route ──────────────────────────────────────────────────────────

@app.get("/qr")
def serve_qr():
    """Return a PNG QR code pointing to this server's root URL."""
    try:
        import qrcode  # noqa: PLC0415
    except ImportError:
        return "qrcode library not installed", 501

    url = f"http://{request.host}/"
    img = qrcode.make(url)
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    img.save(tmp.name)
    return send_file(tmp.name, mimetype="image/png")


# =============================================================================
# PHASE 7: STARTUP HELPERS  (Day 11)
# =============================================================================

def _get_local_ip() -> str:
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def _print_qr(url: str) -> None:
    """Print an ASCII QR code in the terminal for easy phone scanning."""
    try:
        import qrcode  # noqa: PLC0415
        qr = qrcode.QRCode(border=1)
        qr.add_data(url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
    except ImportError:
        pass
    print(f"\n  → Students open:  {url}\n")


# =============================================================================
# PHASE 8: ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    local_ip = _get_local_ip()
    url      = f"http://{local_ip}:{SERVER_PORT}"

    print("\n" + "=" * 60)
    print("  EduNode — Offline AI Tutor for ASEAN Schools")
    print("=" * 60)
    print(f"  Model      : {OLLAMA_MODEL}")
    print(f"  Embeddings : {EMBED_MODEL}")
    print(f"  Documents  : {_collection.count()} chunks indexed")
    print(f"  Server     : {url}")
    print(f"  Admin      : {url}/admin  (token required)")
    print("=" * 60)

    if not ollama_available():
        log.warning(
            "Ollama not detected at %s\n"
            "  → Run `ollama serve` in a separate terminal, then retry.",
            OLLAMA_BASE,
        )

    _print_qr(url)
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=False, threaded=True)

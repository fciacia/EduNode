#!/usr/bin/env bash
# =============================================================================
# EduNode — One-shot setup script for Raspberry Pi 5 (Ubuntu / Raspberry Pi OS)
# Run as a regular user (not root).
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "============================================================"
echo "  EduNode Setup"
echo "============================================================"

# ── 1. Ollama ────────────────────────────────────────────────────────────────
if ! command -v ollama &>/dev/null; then
  echo "[1/6] Installing Ollama…"
  curl -fsSL https://ollama.com/install.sh | sh
else
  echo "[1/6] Ollama already installed — skipping."
fi

echo "      Pulling llama3.2:3b-instruct-q4_K_M (~2 GB)…"
ollama pull llama3.2:3b-instruct-q4_K_M

# ── 2. Python dependencies ───────────────────────────────────────────────────
echo "[2/6] Installing Python dependencies…"
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

# ── 3. Whisper.cpp ───────────────────────────────────────────────────────────
if [ ! -f "whisper.cpp/main" ]; then
  echo "[3/6] Building Whisper.cpp…"
  if [ ! -d "whisper.cpp" ]; then
    git clone --depth 1 https://github.com/ggerganov/whisper.cpp whisper.cpp
  fi
  cd whisper.cpp
  make -j"$(nproc)"
  bash ./models/download-ggml-model.sh base.en
  cd "$SCRIPT_DIR"
else
  echo "[3/6] Whisper.cpp already built — skipping."
fi

# ── 4. Piper TTS ─────────────────────────────────────────────────────────────
PIPER_DIR="models/piper"
mkdir -p "$PIPER_DIR"

if [ ! -f "$PIPER_DIR/piper" ]; then
  echo "[4/6] Downloading Piper TTS binary…"
  ARCH="$(uname -m)"
  if [ "$ARCH" = "aarch64" ]; then
    PIPER_URL="https://github.com/rhasspy/piper/releases/latest/download/piper_linux_aarch64.tar.gz"
  else
    PIPER_URL="https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz"
  fi
  curl -fsSL "$PIPER_URL" | tar -xz -C "$PIPER_DIR" --strip-components=1
else
  echo "[4/6] Piper already installed — skipping."
fi

if [ ! -f "$PIPER_DIR/en_US-lessac-medium.onnx" ]; then
  echo "      Downloading Piper voice model (en_US-lessac-medium)…"
  BASE="https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium"
  curl -fsSL -o "$PIPER_DIR/en_US-lessac-medium.onnx"      "$BASE/en_US-lessac-medium.onnx"
  curl -fsSL -o "$PIPER_DIR/en_US-lessac-medium.onnx.json" "$BASE/en_US-lessac-medium.onnx.json"
fi

# ── 5. ffmpeg ─────────────────────────────────────────────────────────────────
if ! command -v ffmpeg &>/dev/null; then
  echo "[5/6] Installing ffmpeg (needed for audio conversion)…"
  sudo apt-get install -y ffmpeg
else
  echo "[5/6] ffmpeg already installed — skipping."
fi

# ── 6. .env ───────────────────────────────────────────────────────────────────
if [ ! -f ".env" ]; then
  echo "[6/6] Creating .env from .env.example…"
  cp .env.example .env
  echo "      ⚠  Edit .env and set a strong ADMIN_TOKEN before deploying!"
else
  echo "[6/6] .env already exists — skipping."
fi

echo ""
echo "============================================================"
echo "  Setup complete!"
echo ""
echo "  Start EduNode:"
echo "    ollama serve &          # in one terminal"
echo "    python asean_ai_tutor_project.py"
echo ""
echo "  Or with gunicorn (production):"
echo "    ollama serve &"
echo "    gunicorn -w 2 -b 0.0.0.0:5000 'asean_ai_tutor_project:app'"
echo "============================================================"
echo ""

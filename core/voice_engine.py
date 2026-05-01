"""
core/voice_engine.py
====================
Step 5 — Speech-to-text (Whisper.cpp) and text-to-speech (Piper TTS).

Public API
----------
speech_to_text(audio_bytes: bytes) -> str
    Converts WebM/WAV audio bytes to a transcript string.
    Returns "" if Whisper.cpp binary is not installed — degrades gracefully.

text_to_speech(text: str) -> bytes
    Converts text to WAV audio bytes using Piper TTS.
    Returns b"" if Piper binary is not installed — degrades gracefully.

generate_podcast_audio(script: str) -> bytes
    Extracts spoken lines from a MAYA/NIKO script and synthesises to WAV.
    Returns b"" if Piper is not installed.
"""

from __future__ import annotations

import logging
import os
import re
import subprocess
import tempfile
import uuid
from pathlib import Path

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Binary / model paths (can be overridden via env)
# ---------------------------------------------------------------------------
WHISPER_BIN   = Path(os.getenv("WHISPER_BIN",   "whisper.cpp/main"))
WHISPER_MODEL = Path(os.getenv("WHISPER_MODEL",  "models/whisper/ggml-base.en.bin"))
PIPER_BIN     = Path(os.getenv("PIPER_BIN",      "models/piper/piper"))
PIPER_MODEL   = Path(os.getenv("PIPER_MODEL",    "models/piper/en_US-lessac-medium.onnx"))

# Subprocess timeouts (seconds) — keeps the Pi from hanging on bad input
STT_TIMEOUT   = int(os.getenv("STT_TIMEOUT",  "60"))
TTS_TIMEOUT   = int(os.getenv("TTS_TIMEOUT",  "30"))
FFMPEG_TIMEOUT = int(os.getenv("FFMPEG_TIMEOUT", "30"))


# ---------------------------------------------------------------------------
# Speech-to-text
# ---------------------------------------------------------------------------

def speech_to_text(audio_bytes: bytes) -> str:
    """
    Convert raw audio bytes (WebM from browser MediaRecorder, or WAV) to text.

    Pipeline:
      1. Write audio_bytes to a temp file.
      2. ffmpeg: convert to 16 kHz mono WAV (required by Whisper).
      3. whisper.cpp/main: transcribe WAV → transcript text.
      4. Read Whisper's .txt output file.

    Returns "" on any failure (binary missing, bad audio, timeout).
    """
    if not WHISPER_BIN.exists():
        log.info("Whisper.cpp binary not found at '%s' — STT unavailable.", WHISPER_BIN)
        return ""

    if not WHISPER_MODEL.exists():
        log.warning("Whisper model not found at '%s' — STT unavailable.", WHISPER_MODEL)
        return ""

    uid = uuid.uuid4().hex
    tmp_dir = Path(tempfile.gettempdir())
    input_file  = tmp_dir / f"edunode_stt_in_{uid}"
    wav_file    = tmp_dir / f"edunode_stt_{uid}.wav"
    # Whisper writes transcript to <wav_file>.txt automatically
    txt_file    = tmp_dir / f"edunode_stt_{uid}.wav.txt"

    try:
        input_file.write_bytes(audio_bytes)

        # ── Convert to 16 kHz mono WAV ────────────────────────────────────
        ffmpeg_result = subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(input_file),
                "-ar", "16000",
                "-ac", "1",
                "-f", "wav",
                str(wav_file),
            ],
            capture_output=True,
            timeout=FFMPEG_TIMEOUT,
        )
        if ffmpeg_result.returncode != 0:
            log.warning(
                "ffmpeg conversion failed (rc=%d): %s",
                ffmpeg_result.returncode,
                ffmpeg_result.stderr.decode(errors="replace")[:200],
            )
            return ""

        # ── Transcribe with Whisper.cpp ───────────────────────────────────
        whisper_result = subprocess.run(
            [
                str(WHISPER_BIN),
                "-m", str(WHISPER_MODEL),
                "-f", str(wav_file),
                "--output-txt",
                "--no-timestamps",
                "-of", str(wav_file),   # output file prefix (Whisper appends .txt)
            ],
            capture_output=True,
            timeout=STT_TIMEOUT,
        )

        if whisper_result.returncode != 0:
            log.warning(
                "Whisper transcription failed (rc=%d): %s",
                whisper_result.returncode,
                whisper_result.stderr.decode(errors="replace")[:200],
            )
            # Fall back to stdout in case output-txt didn't work
            return whisper_result.stdout.decode(errors="replace").strip()

        # ── Read .txt output ──────────────────────────────────────────────
        if txt_file.exists():
            transcript = txt_file.read_text(encoding="utf-8", errors="replace").strip()
        else:
            transcript = whisper_result.stdout.decode(errors="replace").strip()

        # Strip Whisper timestamp artifacts e.g. "[00:00:00.000 --> 00:00:05.000]"
        transcript = re.sub(r"\[\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\]", "", transcript)
        transcript = re.sub(r"\s+", " ", transcript).strip()

        log.info("STT transcript (%d chars): %s…", len(transcript), transcript[:60])
        return transcript

    except subprocess.TimeoutExpired:
        log.warning("STT timed out after %ds.", STT_TIMEOUT)
        return ""
    except FileNotFoundError as exc:
        log.warning("STT dependency missing: %s", exc)
        return ""
    except Exception as exc:  # noqa: BLE001
        log.warning("STT unexpected error: %s", exc)
        return ""
    finally:
        for f in (input_file, wav_file, txt_file):
            try:
                f.unlink(missing_ok=True)
            except OSError:
                pass


# ---------------------------------------------------------------------------
# Text-to-speech
# ---------------------------------------------------------------------------

def text_to_speech(text: str) -> bytes:
    """
    Synthesise *text* to WAV audio bytes using Piper TTS.

    Returns b"" if Piper is not installed or synthesis fails.
    """
    if not PIPER_BIN.exists():
        log.info("Piper TTS binary not found at '%s' — TTS unavailable.", PIPER_BIN)
        return b""

    if not PIPER_MODEL.exists():
        log.warning("Piper voice model not found at '%s' — TTS unavailable.", PIPER_MODEL)
        return b""

    if not text.strip():
        return b""

    uid      = uuid.uuid4().hex
    out_file = Path(tempfile.gettempdir()) / f"edunode_tts_{uid}.wav"

    try:
        result = subprocess.run(
            [
                str(PIPER_BIN),
                "--model",       str(PIPER_MODEL),
                "--output_file", str(out_file),
            ],
            input=text.encode("utf-8"),
            capture_output=True,
            timeout=TTS_TIMEOUT,
        )

        if result.returncode != 0:
            log.warning(
                "Piper TTS failed (rc=%d): %s",
                result.returncode,
                result.stderr.decode(errors="replace")[:200],
            )
            return b""

        if not out_file.exists():
            log.warning("Piper did not produce output file at '%s'.", out_file)
            return b""

        wav_bytes = out_file.read_bytes()
        log.info("TTS produced %d bytes for %d chars of text.", len(wav_bytes), len(text))
        return wav_bytes

    except subprocess.TimeoutExpired:
        log.warning("TTS timed out after %ds.", TTS_TIMEOUT)
        return b""
    except FileNotFoundError as exc:
        log.warning("TTS dependency missing: %s", exc)
        return b""
    except Exception as exc:  # noqa: BLE001
        log.warning("TTS unexpected error: %s", exc)
        return b""
    finally:
        try:
            out_file.unlink(missing_ok=True)
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Podcast audio
# ---------------------------------------------------------------------------

def generate_podcast_audio(script: str) -> bytes:
    """
    Extract the spoken lines from a MAYA/NIKO script and synthesise to WAV.

    Lines are joined with a short pause marker " ... " so Piper produces a
    natural-sounding pause between speaker turns.

    Returns b"" if Piper is not installed.
    """
    lines: list[str] = []
    for line in script.splitlines():
        # Match "MAYA: ..." or "NIKO: ..." — extract just the spoken part
        match = re.match(r"^(?:MAYA|NIKO)\s*:\s*(.+)$", line.strip(), re.IGNORECASE)
        if match:
            lines.append(match.group(1).strip())

    if not lines:
        # Fall back: just use the whole script
        combined = script.strip()
    else:
        combined = " ... ".join(lines)

    return text_to_speech(combined)

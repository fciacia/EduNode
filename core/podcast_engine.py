"""
core/podcast_engine.py
======================
Step 10 — Combines LLM script generation with TTS audio synthesis.

Public API
----------
generate_podcast(topic, language) -> dict
    {"script": str, "audio_path": str, "audio_url": str}
    audio_path is the on-disk WAV path (empty string if TTS unavailable).
    audio_url  is the Flask-servable URL (/api/audio/<filename>).
"""

from __future__ import annotations

import logging
import os
import uuid
from pathlib import Path

log = logging.getLogger(__name__)

AUDIO_DIR = Path(os.getenv("AUDIO_DIR", "data/audio"))


def generate_podcast(topic: str, language: str) -> dict:
    """
    Generate a MAYA/NIKO podcast episode about *topic* in *language*.

    Steps:
      1. Generate the dialogue script via llm_engine.
      2. Synthesise audio via voice_engine (returns b"" if Piper missing).
      3. Save WAV to data/audio/<uuid>.wav.
      4. Return script + paths.

    Returns
    -------
    {
        "script":     str,   # full MAYA/NIKO dialogue text
        "audio_path": str,   # absolute path to WAV file, or "" if unavailable
        "audio_url":  str,   # /api/audio/<filename>, or "" if unavailable
    }
    """
    from core.llm_engine   import generate_podcast_script
    from core.voice_engine import generate_podcast_audio

    script = generate_podcast_script(topic, language)

    wav_bytes = generate_podcast_audio(script)

    audio_path = ""
    audio_url  = ""

    if wav_bytes:
        AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        filename   = f"podcast_{uuid.uuid4().hex[:8]}.wav"
        out_file   = AUDIO_DIR / filename
        out_file.write_bytes(wav_bytes)
        audio_path = str(out_file)
        audio_url  = f"/api/audio/{filename}"
        log.info("Podcast audio saved: %s (%d bytes)", out_file, len(wav_bytes))
    else:
        log.info("TTS unavailable — podcast script only (no audio).")

    return {
        "script":     script,
        "audio_path": audio_path,
        "audio_url":  audio_url,
    }

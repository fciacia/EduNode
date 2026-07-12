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
import shutil
import subprocess
import sys
import tempfile
import uuid
from collections import OrderedDict
from pathlib import Path

log = logging.getLogger(__name__)

# Hub language name -> Whisper language code (for the -l flag). Whisper's
# multilingual model auto-detects when given "auto". Languages it cannot do
# (Iban, Cebuano, Shan, Kedayan…) simply fall back to auto-detect.
_WHISPER_LANG: dict[str, str] = {
    "English": "en", "Bahasa Melayu": "ms", "Bahasa Indonesia": "id",
    "Filipino": "tl", "Tagalog": "tl", "Vietnamese": "vi", "Thai": "th",
    "Khmer": "km", "Lao": "lo", "Burmese": "my", "Javanese": "jw",
    "Sundanese": "su",
}

# Hub language name -> macOS `say` voice. These ship with macOS and cover the
# ASEAN languages Piper has no voice for. Used only on macOS; elsewhere these
# languages produce no audio (text still shows).
_SAY_VOICE: dict[str, str] = {
    "Bahasa Melayu": "Amira",
    "Bahasa Indonesia": "Damayanti",
    "Thai": "Kanya",
    "Vietnamese": "Linh",
}

# Hub language name -> Meta MMS-TTS code (ISO 639-3). Neural voices for the
# languages neither Piper nor macOS `say` cover. Models download on first use
# (~140 MB each) and are cached in memory thereafter. Portable across OSes.
_MMS_LANG: dict[str, str] = {
    "Filipino": "tgl", "Tagalog": "tgl",
    "Khmer": "khm", "Lao": "lao", "Burmese": "mya",
}
# Cap how many MMS voice models stay resident (~150 MB each) to bound RAM on the Pi.
_MMS_CACHE_MAX = 2
_mms_cache: "OrderedDict[str, tuple]" = OrderedDict()

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

def speech_to_text(audio_bytes: bytes, language: str = "auto") -> str:
    """
    Convert raw audio bytes (WebM from browser MediaRecorder, or WAV) to text.

    *language* is the hub language name (e.g. "Bahasa Melayu"); it is mapped to a
    Whisper language code to improve accuracy. Unknown names → auto-detect.

    Pipeline:
      1. Write audio_bytes to a temp file.
      2. ffmpeg: convert to 16 kHz mono WAV (required by Whisper).
      3. whisper.cpp/main: transcribe WAV → transcript text.
      4. Read Whisper's .txt output file.

    Returns "" on any failure (binary missing, bad audio, timeout).
    """
    lang_code = _WHISPER_LANG.get(language, "auto") if language else "auto"
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
                "-l", lang_code,        # language hint ("auto" = detect)
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

def text_to_speech(text: str, language: str = "English") -> bytes:
    """
    Synthesise *text* to WAV audio bytes, choosing a TTS engine by language:

      - English              → Piper (offline neural voice)
      - ms / id / th / vi    → macOS `say` (high-quality system voices, macOS only)
      - fil / km / lo / my   → Meta MMS-TTS (neural, portable)
      - anything else        → b"" (no voice available; the UI just shows text)

    Returns b"" if no engine/voice is available or synthesis fails.
    """
    if not text.strip():
        return b""

    if language == "English":
        return _piper_tts(text)

    voice = _SAY_VOICE.get(language)
    if voice and sys.platform == "darwin" and shutil.which("say"):
        return _say_tts(text, voice)

    mms_code = _MMS_LANG.get(language)
    if mms_code:
        return _mms_tts(text, mms_code)

    log.info("No TTS voice available for '%s' — returning silence.", language)
    return b""


def _mms_tts(text: str, code: str) -> bytes:
    """Synthesise text to WAV bytes with Meta's MMS-TTS (VITS) for *code*."""
    try:
        import io
        import wave
        import numpy as np
        import torch
        from transformers import AutoTokenizer, VitsModel
    except ImportError as exc:
        log.warning("MMS-TTS dependencies missing: %s", exc)
        return b""

    try:
        if code not in _mms_cache:
            name = f"facebook/mms-tts-{code}"
            _mms_cache[code] = (VitsModel.from_pretrained(name), AutoTokenizer.from_pretrained(name))
            while len(_mms_cache) > _MMS_CACHE_MAX:
                _mms_cache.popitem(last=False)   # evict least-recently-loaded
        _mms_cache.move_to_end(code)
        model, tokenizer = _mms_cache[code]

        inputs = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            waveform = model(**inputs).waveform.squeeze().cpu().numpy()

        pcm = (np.clip(waveform, -1.0, 1.0) * 32767).astype("<i2")
        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(int(model.config.sampling_rate))
            wf.writeframes(pcm.tobytes())
        data = buf.getvalue()
        log.info("TTS (mms/%s) produced %d bytes for %d chars.", code, len(data), len(text))
        return data
    except Exception as exc:  # noqa: BLE001
        log.warning("MMS-TTS error for '%s': %s", code, exc)
        return b""


def _piper_tts(text: str) -> bytes:
    """Synthesise English text to WAV bytes with Piper."""
    if not PIPER_BIN.exists():
        log.info("Piper TTS binary not found at '%s' — TTS unavailable.", PIPER_BIN)
        return b""
    if not PIPER_MODEL.exists():
        log.warning("Piper voice model not found at '%s' — TTS unavailable.", PIPER_MODEL)
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


def _say_tts(text: str, voice: str) -> bytes:
    """Synthesise text to WAV bytes with the macOS `say` command + ffmpeg."""
    uid       = uuid.uuid4().hex
    aiff_file = Path(tempfile.gettempdir()) / f"edunode_say_{uid}.aiff"
    wav_file  = Path(tempfile.gettempdir()) / f"edunode_say_{uid}.wav"

    try:
        say = subprocess.run(
            ["say", "-v", voice, "-o", str(aiff_file), text],
            capture_output=True, timeout=TTS_TIMEOUT,
        )
        if say.returncode != 0 or not aiff_file.exists():
            log.warning("macOS say failed for voice '%s': %s",
                        voice, say.stderr.decode(errors="replace")[:200])
            return b""

        # Convert AIFF -> 22.05 kHz mono WAV (browser-friendly, matches Piper output)
        conv = subprocess.run(
            ["ffmpeg", "-y", "-i", str(aiff_file), "-ar", "22050", "-ac", "1", str(wav_file)],
            capture_output=True, timeout=FFMPEG_TIMEOUT,
        )
        if conv.returncode != 0 or not wav_file.exists():
            log.warning("ffmpeg AIFF->WAV failed: %s", conv.stderr.decode(errors="replace")[:200])
            return b""

        wav_bytes = wav_file.read_bytes()
        log.info("TTS (say/%s) produced %d bytes for %d chars.", voice, len(wav_bytes), len(text))
        return wav_bytes

    except subprocess.TimeoutExpired:
        log.warning("macOS say timed out after %ds.", TTS_TIMEOUT)
        return b""
    except Exception as exc:  # noqa: BLE001
        log.warning("say TTS unexpected error: %s", exc)
        return b""
    finally:
        for f in (aiff_file, wav_file):
            try:
                f.unlink(missing_ok=True)
            except OSError:
                pass


# ---------------------------------------------------------------------------
# Podcast audio — two-voice dialogue
# ---------------------------------------------------------------------------

# MAYA → female voice, NIKO → male voice (per language, macOS `say` voices)
_MAYA_VOICE: dict[str, str] = {
    "English": "Samantha",
    "Bahasa Melayu": "Amira",
    "Bahasa Indonesia": "Damayanti",
    "Thai": "Kanya",
    "Vietnamese": "Linh",
}
_NIKO_VOICE: dict[str, str] = {
    "English": "Daniel",
    "Bahasa Melayu": "Amira",   # no male ms voice; falls back gracefully
    "Bahasa Indonesia": "Damayanti",
    "Thai": "Kanya",
    "Vietnamese": "Linh",
}


def _generate_silence(duration_ms: int = 500, sample_rate: int = 22050) -> bytes:
    """Return WAV bytes of silence for *duration_ms* at *sample_rate*."""
    import io, wave
    num_samples = int(sample_rate * duration_ms / 1000)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b"\x00\x00" * num_samples)
    return buf.getvalue()


def _concat_wavs(chunks: list[bytes]) -> bytes:
    """Merge a list of WAV-byte chunks into one continuous WAV."""
    import io, wave
    if not chunks:
        return b""
    all_pcm: list[bytes] = []
    sr = 22050  # default; overridden by first chunk's actual rate
    for chunk in chunks:
        with wave.open(io.BytesIO(chunk), "rb") as wf:
            sr = wf.getframerate()
            all_pcm.append(wf.readframes(wf.getnframes()))
    buf = io.BytesIO()
    with wave.open(buf, "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(sr)
        for pcm in all_pcm:
            out.writeframes(pcm)
    return buf.getvalue()


def generate_podcast_audio(script: str, language: str = "English") -> bytes:
    """
    Synthesise a MAYA/NIKO podcast with two distinct voices.

    Each spoken line is synthesised separately using the appropriate voice for
    the speaker, with a short silence (~500 ms) between turns.

    Returns b"" if no voice is available for *language*.
    """
    chunks: list[bytes] = []
    silence = _generate_silence(500)
    log.info("generate_podcast_audio: script has %d lines, language=%s", len(script.splitlines()), language)

    for line in script.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        # Normalise: strip leading/trailing markdown bold/italic markers around
        # the speaker name so we handle **MAYA**:  **Maya:**  *NIKO*: etc.
        cleaned = re.sub(r"^[*_]+", "", stripped)          # leading ** or *
        cleaned = re.sub(r"^(MAYA|NIKO)[*_]+\s*:", r"\1:", cleaned, flags=re.IGNORECASE)  # **MAYA**:
        is_maya = re.match(r"^MAYA\s*:", cleaned, re.IGNORECASE)
        is_niko = re.match(r"^NIKO\s*:", cleaned, re.IGNORECASE)

        if is_maya or is_niko:
            # Extract spoken text: strip any markdown prefix, speaker label,
            # optional trailing markdown after the name, and the colon.
            text = re.sub(r"^[*_]*(?:MAYA|NIKO)[*_]*\s*:[*_]*\s*", "", stripped, flags=re.IGNORECASE).strip()
            if not text:
                continue
            # Choose voice based on speaker
            if is_maya and sys.platform == "darwin" and shutil.which("say"):
                voice = _MAYA_VOICE.get(language, "Samantha")
                wav = _say_tts(text, voice)
            elif is_niko and sys.platform == "darwin" and shutil.which("say"):
                voice = _NIKO_VOICE.get(language, "Daniel")
                wav = _say_tts(text, voice)
            else:
                # Fallback: use the default text_to_speech for this language
                wav = text_to_speech(text, language)

            if wav:
                if chunks:
                    chunks.append(silence)
                chunks.append(wav)
        # Non-speaker lines (narration, titles) are skipped for audio

    if not chunks:
        return b""

    return _concat_wavs(chunks)

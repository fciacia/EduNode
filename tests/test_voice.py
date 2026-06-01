"""Tests for language-aware voice engine dispatch (no real audio binaries needed)."""
import core.voice_engine as ve


def test_whisper_lang_map():
    assert ve._WHISPER_LANG["Bahasa Melayu"] == "ms"
    assert ve._WHISPER_LANG["Thai"] == "th"
    assert ve._WHISPER_LANG["English"] == "en"


def test_tts_english_uses_piper(monkeypatch):
    monkeypatch.setattr(ve, "_piper_tts", lambda t: b"PIPER")
    assert ve.text_to_speech("hello", "English") == b"PIPER"


def test_tts_malay_uses_say(monkeypatch):
    monkeypatch.setattr(ve.sys, "platform", "darwin")
    monkeypatch.setattr(ve.shutil, "which", lambda name: "/usr/bin/say")
    captured = {}
    def fake_say(text, voice):
        captured["voice"] = voice
        return b"SAY"
    monkeypatch.setattr(ve, "_say_tts", fake_say)
    out = ve.text_to_speech("Apa khabar", "Bahasa Melayu")
    assert out == b"SAY"
    assert captured["voice"] == "Amira"


def test_tts_filipino_uses_mms(monkeypatch):
    captured = {}
    def fake_mms(text, code):
        captured["code"] = code
        return b"MMS"
    monkeypatch.setattr(ve, "_mms_tts", fake_mms)
    out = ve.text_to_speech("Kumusta", "Filipino")
    assert out == b"MMS"
    assert captured["code"] == "tgl"


def test_tts_unsupported_language_returns_empty(monkeypatch):
    monkeypatch.setattr(ve, "_piper_tts", lambda t: b"PIPER")
    monkeypatch.setattr(ve, "_mms_tts", lambda t, c: b"MMS")
    # A language with no Piper, no `say`, and no MMS voice -> silence.
    assert ve.text_to_speech("xyz", "Klingon") == b""


def test_tts_empty_text_returns_empty():
    assert ve.text_to_speech("", "English") == b""
    assert ve.text_to_speech("   ", "Bahasa Melayu") == b""

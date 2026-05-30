"""
core/agents/translation.py
===========================
Multilingual Translation Agent. Bridges student mother-tongue <-> English using
NLLB-200. English is pass-through. Languages without a FLORES-200 code fall back
to the existing glossary bridge in llm_engine.
"""
from __future__ import annotations

import logging

log = logging.getLogger(__name__)

NLLB_MODEL = "facebook/nllb-200-distilled-600M"

# Hub language name -> FLORES-200 code. Extend as new hubs are added.
_FLORES: dict[str, str] = {
    "English":          "eng_Latn",
    "Bahasa Melayu":    "zsm_Latn",
    "Bahasa Indonesia": "ind_Latn",
    "Filipino":         "fil_Latn",
    "Vietnamese":       "vie_Latn",
    "Iban":             "iba_Latn",
    "Cebuano":          "ceb_Latn",
    "Sundanese":        "sun_Latn",
}

_model = None
_tokenizer = None


def flores_code(language: str) -> str | None:
    """Return the FLORES-200 code for a hub language name, or None if unsupported."""
    return _FLORES.get(language)


def _load():
    """Lazy-load the NLLB-200 model + tokenizer (cached singletons)."""
    global _model, _tokenizer
    if _model is None:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        _tokenizer = AutoTokenizer.from_pretrained(NLLB_MODEL)
        _model = AutoModelForSeq2SeqLM.from_pretrained(NLLB_MODEL)
    return _model, _tokenizer


def _nllb_translate(text: str, src_code: str, tgt_code: str) -> str:
    """Translate text from src FLORES code to tgt FLORES code via NLLB-200."""
    model, tokenizer = _load()
    tokenizer.src_lang = src_code
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    bos = tokenizer.convert_tokens_to_ids(tgt_code)
    generated = model.generate(**inputs, forced_bos_token_id=bos, max_length=512)
    return tokenizer.batch_decode(generated, skip_special_tokens=True)[0].strip()


def to_english(text: str, language: str) -> str:
    """Translate a student query into English. English passes through unchanged."""
    if language == "English":
        return text
    code = flores_code(language)
    if code is None:
        log.info("No FLORES code for '%s' — passing query through untranslated.", language)
        return text
    try:
        return _nllb_translate(text, code, "eng_Latn")
    except Exception as exc:  # noqa: BLE001
        log.warning("NLLB to_english failed for '%s': %s — using original text.", language, exc)
        return text


def to_native(text: str, language: str) -> str:
    """
    Translate an English answer into the student's language.
    English passes through. Unsupported languages use the glossary bridge.
    """
    if language == "English":
        return text
    code = flores_code(language)
    if code is None:
        from core.llm_engine import _bridge_translate
        return _bridge_translate(text, language)
    try:
        return _nllb_translate(text, "eng_Latn", code)
    except Exception as exc:  # noqa: BLE001
        log.warning("NLLB to_native failed for '%s': %s — using glossary bridge.", language, exc)
        from core.llm_engine import _bridge_translate
        return _bridge_translate(text, language)

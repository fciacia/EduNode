"""
core/agents/translation.py
===========================
Multilingual Translation Agent. Bridges student mother-tongue <-> English using
NLLB-200. English is pass-through. Languages without a FLORES-200 code fall back
to the existing glossary bridge in llm_engine.
"""
from __future__ import annotations

import logging
import re

log = logging.getLogger(__name__)

NLLB_MODEL = "facebook/nllb-200-distilled-600M"

# Hub language name -> FLORES-200 code (verified against the NLLB-200 tokenizer).
# Languages NOT in NLLB-200 (Iban, Kedayan, Dayak, Hmong, Isan, Tetum) are left
# out on purpose — they automatically use the glossary bridge in llm_engine.
_FLORES: dict[str, str] = {
    "English":          "eng_Latn",
    # National languages
    "Bahasa Melayu":    "zsm_Latn",
    "Bahasa Indonesia": "ind_Latn",
    "Filipino":         "tgl_Latn",   # Filipino is standardised Tagalog
    "Tagalog":          "tgl_Latn",
    "Vietnamese":       "vie_Latn",
    "Thai":             "tha_Thai",
    "Khmer":            "khm_Khmr",
    "Lao":              "lao_Laoo",
    "Burmese":          "mya_Mymr",
    # Regional / minority languages supported by NLLB-200
    "Cebuano":          "ceb_Latn",
    "Ilocano":          "ilo_Latn",
    "Waray":            "war_Latn",
    "Pangasinan":       "pag_Latn",
    "Sundanese":        "sun_Latn",
    "Javanese":         "jav_Latn",
    "Acehnese":         "ace_Latn",
    "Banjar":           "bjn_Latn",
    "Minangkabau":      "min_Latn",
    "Shan":             "shn_Mymr",
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


_FORMULA_SUBS = [
    (r"\bCO2\b", "carbon dioxide"),
    (r"\bH2O\b", "water"),
    (r"\bO2\b",  "oxygen"),
    (r"\bCH4\b", "methane"),
    (r"\bN2\b",  "nitrogen"),
]


def _normalize_formulas(text: str) -> str:
    """
    Replace chemical formulas/symbols with plain words before translation.

    NLLB-200 mangles tokens like ``CO2`` / ``H2O`` into garbage (e.g. "dioks02").
    The pedagogy prompt asks the model to avoid them, but small models don't always
    comply — so we guarantee clean input here. Unicode subscripts are normalised too.
    """
    text = text.translate(str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789"))
    # Drop redundant "(CO2)"-style annotations that usually follow the word.
    text = re.sub(r"\s*\((?:CO2|H2O|O2|CH4|N2)\)", "", text)
    for pattern, word in _FORMULA_SUBS:
        text = re.sub(pattern, word, text)
    return re.sub(r"\s{2,}", " ", text).strip()


def _split_sentences(text: str) -> list[str]:
    """
    Split *text* into sentences. NLLB-200 is a sentence-level model — translating
    one sentence at a time avoids the artifacts and degradation it produces on
    long multi-sentence passages.
    """
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _nllb_translate(text: str, src_code: str, tgt_code: str) -> str:
    """
    Translate *text* from src to tgt FLORES code via NLLB-200, sentence by
    sentence (NLLB's trained granularity), then rejoin.
    """
    model, tokenizer = _load()

    # Validate both codes against the tokenizer; an unknown code would otherwise
    # silently produce garbage. Raising lets the caller fall back to the glossary.
    bos = tokenizer.convert_tokens_to_ids(tgt_code)
    if bos == tokenizer.unk_token_id or tokenizer.convert_tokens_to_ids(src_code) == tokenizer.unk_token_id:
        raise ValueError(f"NLLB-200 does not support {src_code!r}->{tgt_code!r}")

    tokenizer.src_lang = src_code
    text = _normalize_formulas(text)
    out: list[str] = []
    for sentence in _split_sentences(text) or [text.strip()]:
        inputs = tokenizer(sentence, return_tensors="pt", truncation=True, max_length=256)
        generated = model.generate(**inputs, forced_bos_token_id=bos, max_length=256)
        out.append(tokenizer.batch_decode(generated, skip_special_tokens=True)[0].strip())
    return " ".join(p for p in out if p).strip()


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

import pytest

import core.agents.translation as tr


def test_english_is_passthrough():
    assert tr.to_english("Hello there", "English") == "Hello there"
    assert tr.to_native("Hello there", "English") == "Hello there"


def test_flores_code_lookup():
    assert tr.flores_code("Bahasa Melayu") == "zsm_Latn"
    assert tr.flores_code("Filipino") == "tgl_Latn"   # Filipino -> Tagalog
    assert tr.flores_code("Thai") == "tha_Thai"
    assert tr.flores_code("Khmer") == "khm_Khmr"
    assert tr.flores_code("English") == "eng_Latn"
    # Not in NLLB-200 -> unmapped, so it uses the glossary bridge
    assert tr.flores_code("Iban") is None
    assert tr.flores_code("Klingon") is None


def test_nllb_translate_raises_on_unknown_code(monkeypatch):
    class FakeTok:
        unk_token_id = 0
        src_lang = None
        def convert_tokens_to_ids(self, t):
            return 0  # everything resolves to unk
    monkeypatch.setattr(tr, "_load", lambda: (object(), FakeTok()))
    with pytest.raises(ValueError):
        tr._nllb_translate("hi", "eng_Latn", "xxx_Xxxx")


def test_to_english_uses_nllb_for_supported_language(monkeypatch):
    calls = {}

    def fake_translate(text, src, tgt):
        calls["args"] = (text, src, tgt)
        return "translated-to-english"

    monkeypatch.setattr(tr, "_nllb_translate", fake_translate)
    out = tr.to_english("Apa itu air?", "Bahasa Melayu")
    assert out == "translated-to-english"
    assert calls["args"] == ("Apa itu air?", "zsm_Latn", "eng_Latn")


def test_unsupported_language_falls_back_to_glossary(monkeypatch):
    # Kedayan has no FLORES code → to_native uses the glossary bridge
    monkeypatch.setattr(
        "core.llm_engine._bridge_translate",
        lambda text, lang: f"[English] {text}\n[{lang}] (glossary)",
    )
    out = tr.to_native("Water is essential.", "Kedayan")
    assert "glossary" in out


def test_split_sentences():
    # Splits on sentence boundaries; drops empties; single sentence stays whole.
    assert tr._split_sentences("One. Two! Three?") == ["One.", "Two!", "Three?"]
    assert tr._split_sentences("Just one sentence") == ["Just one sentence"]
    assert tr._split_sentences("   ") == []


def test_normalize_formulas():
    # Bare formulas -> words; redundant "(CO2)" annotations dropped; subscripts handled.
    assert tr._normalize_formulas("Plants use CO2 and H2O.") == "Plants use carbon dioxide and water."
    assert tr._normalize_formulas("carbon dioxide (CO2) and water (H2O)") == "carbon dioxide and water"
    assert tr._normalize_formulas("releases O₂ gas") == "releases oxygen gas"

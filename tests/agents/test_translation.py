import core.agents.translation as tr


def test_english_is_passthrough():
    assert tr.to_english("Hello there", "English") == "Hello there"
    assert tr.to_native("Hello there", "English") == "Hello there"


def test_flores_code_lookup():
    assert tr.flores_code("Bahasa Melayu") == "zsm_Latn"
    assert tr.flores_code("Iban") == "iba_Latn"
    assert tr.flores_code("English") == "eng_Latn"
    assert tr.flores_code("Klingon") is None   # unsupported


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

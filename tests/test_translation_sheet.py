"""Tests for the translation reference-collection sheet + loader (Issue 4)."""
import csv

from tools import make_translation_sheet as mk
from tools import eval_translation as et


def test_extract_sentences_are_clean(tmp_path):
    c = tmp_path / "curriculum"
    c.mkdir()
    (c / "sci.txt").write_text(
        "SCIENCE — GRADE 7 Photosynthesis is how plants make food. "
        "Plants take in sunlight and water to make their own food. "
        "Short. "
        "Roots absorb water and minerals from the soil for the plant.",
        encoding="utf-8",
    )
    sents = mk.extract_sentences(c, n=10)
    assert sents                                   # found some
    assert all(6 <= len(s.split()) <= 16 for s in sents)
    assert all("—" not in s for s in sents)        # header-joined lines skipped
    assert "Short." not in sents                   # too short skipped


def test_sheet_csv_has_language_columns(tmp_path):
    out = tmp_path / "sheet.csv"
    mk.write_csv(["Plants make food.", "Water is wet."], ["Iban", "Cebuano"], out)
    rows = list(csv.DictReader(out.open(encoding="utf-8")))
    assert rows[0]["source_en"] == "Plants make food."
    assert rows[0]["Iban"] == "" and rows[0]["Cebuano"] == ""


def test_loader_reads_filled_cells_only(tmp_path):
    p = tmp_path / "filled.csv"
    with p.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "source_en", "Iban", "Cebuano"])
        w.writeheader()
        w.writerow({"id": "s1", "source_en": "my house", "Iban": "rumah aku", "Cebuano": ""})
        w.writerow({"id": "s2", "source_en": "a dog", "Iban": "", "Cebuano": "iro"})
    refs = et.load_references_from_sheet(p)
    assert {"language": "Iban", "source_en": "my house", "reference": "rumah aku"} in refs
    assert {"language": "Cebuano", "source_en": "a dog", "reference": "iro"} in refs
    assert len(refs) == 2                          # blank cells skipped

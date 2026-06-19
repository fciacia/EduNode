"""
tools/eval_translation.py
=========================
Translation-quality evaluation for low-resource ASEAN languages (Issue 4 / Gap 8).

Turns "translation for Iban/Cebuano is weaker" into a measured number: chrF
(character n-gram F-score), which is the standard metric for morphologically rich
and low-resource languages because it scores partial-word overlap rather than
whole-word matches.

References come from **teacher-verified corrections** (core.correction_store) —
the same flywheel data the teacher dashboard collects — so the gold set grows as
teachers use the system, with no need to hand-author reference translations.
A static gold JSON can also be supplied.

The chrF function is pure and unit-tested. The end-to-end run needs the NLLB model
(only invoked when actually scoring live translations).

Usage
-----
    # Score the current model against teacher-verified corrections:
    python -m tools.eval_translation

    # Against a static reference file:
    python -m tools.eval_translation --gold data/eval/translation_gold.json
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


# ---------------------------------------------------------------------------
# chrF (pure, unit-tested)
# ---------------------------------------------------------------------------

def _ngram_counts(s: str, n: int) -> Counter:
    return Counter(s[i:i + n] for i in range(len(s) - n + 1)) if len(s) >= n else Counter()


def chrf(hypothesis: str, reference: str, max_n: int = 6, beta: float = 2.0) -> float:
    """Character n-gram F-score (0–100). 100 = identical strings."""
    hyp, ref = (hypothesis or "").strip(), (reference or "").strip()
    if not hyp and not ref:
        return 100.0
    if not hyp or not ref:
        return 0.0
    b2 = beta * beta
    fs: list[float] = []
    for n in range(1, max_n + 1):
        h, r = _ngram_counts(hyp, n), _ngram_counts(ref, n)
        if not h or not r:
            continue
        match = sum((h & r).values())
        ht, rt = sum(h.values()), sum(r.values())
        prec, rec = match / ht, match / rt
        if prec + rec == 0:
            fs.append(0.0)
        else:
            fs.append((1 + b2) * prec * rec / (b2 * prec + rec))
    return round(100 * sum(fs) / len(fs), 2) if fs else 0.0


# ---------------------------------------------------------------------------
# Reference loading + scoring
# ---------------------------------------------------------------------------

def load_references_from_sheet(sheet_path: Path) -> list[dict]:
    """Read a filled reference-collection sheet (tools/make_translation_sheet.py).

    Columns: id, source_en, then one column per language. Produces a reference for
    every non-empty language cell.
    """
    import csv
    refs = []
    with Path(sheet_path).open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        langs = [c for c in (reader.fieldnames or []) if c not in ("id", "source_en")]
        for row in reader:
            src = (row.get("source_en") or "").strip()
            for lang in langs:
                ref = (row.get(lang) or "").strip()
                if src and ref:
                    refs.append({"language": lang, "source_en": src, "reference": ref})
    return refs


def load_references(gold_path: Path | None = None,
                    sheet_path: Path | None = None) -> list[dict]:
    """References as [{language, source_en, reference}]. From a filled speaker sheet
    if given, else a gold file, else teacher-verified corrections."""
    if sheet_path:
        return load_references_from_sheet(sheet_path)
    if gold_path:
        data = json.loads(Path(gold_path).read_text(encoding="utf-8"))
        return data["items"] if isinstance(data, dict) else data
    from core.correction_store import list_corrections
    refs = []
    for c in list_corrections(limit=10**9):
        if c.get("english") and c.get("corrected"):
            refs.append({"language": c["language"], "source_en": c["english"],
                         "reference": c["corrected"]})
    return refs


def evaluate(references: list[dict], translate_fn) -> dict:
    """Score each reference's language output with chrF; aggregate per language."""
    per_lang: dict[str, list[float]] = {}
    rows = []
    for ref in references:
        hyp = translate_fn(ref["source_en"], ref["language"])
        score = chrf(hyp, ref["reference"])
        rows.append({**ref, "hypothesis": hyp, "chrf": score})
        per_lang.setdefault(ref["language"], []).append(score)
    summary = {
        lang: {"n": len(scores), "mean_chrf": round(sum(scores) / len(scores), 2)}
        for lang, scores in sorted(per_lang.items())
    }
    return {"summary": summary, "rows": rows}


def _default_translate(source_en: str, language: str) -> str:
    from core.agents.translation import to_native
    return to_native(source_en, language)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Measure translation quality (chrF).")
    p.add_argument("--gold", type=Path, default=None,
                   help="reference JSON; default: teacher-verified corrections")
    p.add_argument("--sheet", type=Path, default=None,
                   help="filled reference-collection CSV (tools/make_translation_sheet.py)")
    p.add_argument("--report", type=Path, default=None)
    args = p.parse_args(argv)

    refs = load_references(args.gold, sheet_path=args.sheet)
    if not refs:
        print("No references yet. Add teacher corrections (dashboard) or pass --gold.")
        return 0
    out = evaluate(refs, _default_translate)

    print("\n=== Translation quality (chrF, 0–100) ===")
    for lang, s in out["summary"].items():
        flag = "  ⚠ weak" if s["mean_chrf"] < 40 else ""
        print(f"  {lang:<14} n={s['n']:>3}  chrF={s['mean_chrf']:>6}{flag}")
    print()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

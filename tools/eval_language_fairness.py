"""
tools/eval_language_fairness.py
===============================
Language-fairness evaluation (Issue 9 + Issue 4).

The rigorous way to measure bias is to hold the *content* fixed and vary only the
language: ask the **same** curriculum question in English, Bahasa Melayu, Thai,
Vietnamese, Iban, … and measure whether the system still retrieves the right
curriculum and produces a grounded answer — or degrades into a non-response.

Any gap from the English baseline is the bias: a low-resource language whose
question mistranslates retrieves worse and falls to non-response more often. This
isolates the language variable (same question, same curriculum) and needs no
foreign-language answer grading.

Additive: reuses data/eval/gold_set.json and the live pipeline. Changes no
curriculum, gold set, or config.

Pipeline simulated per (question, language):
    English question  --to_native-->  question in L   (what the student types)
    question in L      --to_english--> back to English (what the pipeline retrieves on)
    retrieve(back) -> tier (grounded / supplementary / non-response)

Usage
-----
    OLLAMA_MODEL=phi3:mini python -m tools.eval_language_fairness \
        --languages English "Bahasa Melayu" Thai Vietnamese Iban --limit 10 \
        --report data/eval/language_fairness.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.eval_rag import classify_tier


def summarize_language(rows: list[dict]) -> dict:
    """Aggregate per-language grounding / answer / non-response rates (pure)."""
    n = len(rows)
    if n == 0:
        return {"n": 0}
    grounded = sum(1 for r in rows if r["tier"] == "grounded")
    answered = sum(1 for r in rows if r["tier"] != "none")
    none = sum(1 for r in rows if r["tier"] == "none")
    hits = [r["hit"] for r in rows if r.get("hit") is not None]
    # old (translated-only) grounding, when the row carries it, for before/after
    grounded_tr = sum(1 for r in rows if r.get("tier_translated") == "grounded")
    has_tr = any("tier_translated" in r for r in rows)
    out = {
        "n": n,
        "grounded_rate": round(grounded / n, 3),
        "answered_rate": round(answered / n, 3),
        "non_response_rate": round(none / n, 3),
        "retrieval_hit_rate": round(sum(hits) / len(hits), 3) if hits else None,
        "mean_distance": round(sum(r["best_distance"] for r in rows) / n, 3),
    }
    if has_tr:
        out["grounded_rate_translated"] = round(grounded_tr / n, 3)
    return out


def fairness_gaps(per_language: dict, baseline: str = "English") -> dict:
    """Gap in grounded_rate vs the baseline language (the bias signal)."""
    base = per_language.get(baseline, {}).get("grounded_rate")
    if base is None:
        return {}
    return {
        lang: round(base - s["grounded_rate"], 3)
        for lang, s in per_language.items()
        if lang != baseline and s.get("grounded_rate") is not None
    }


def evaluate_language(questions: list[dict], language: str, k: int = 3) -> list[dict]:
    """Retrieve per question two ways (needs models):

      * translated-only  — retrieve on the back-translated English query (the old
        behaviour: query translation degrades retrieval for non-English)
      * cross-lingual    — best of the native-language query and the translated one
        (the fix: the multilingual embedder grounds the native query directly)

    The 'tier' field reflects the cross-lingual (live) behaviour; 'tier_translated'
    preserves the old behaviour so a run shows the before/after.
    """
    from core.agents.translation import to_english, to_native
    from core.rag_engine import retrieve_with_citations

    subject_for = lambda q: q.get("subject", "General")
    rows = []
    for q in questions:
        q_en = q["question"]
        q_native = to_native(q_en, language)          # English -> passthrough
        q_back = to_english(q_native, language)        # translated round-trip

        translated = retrieve_with_citations(q_back, n_results=k, subject=subject_for(q))
        d_translated = min((c.distance for c in translated), default=1.0)

        # cross-lingual: also retrieve on the native query, keep the better grounding
        if language.lower() != "english" and q_native.strip() != q_back.strip():
            native = retrieve_with_citations(q_native, n_results=k, subject=subject_for(q))
            d_native = min((c.distance for c in native), default=1.0)
        else:
            native, d_native = translated, d_translated

        if d_native < d_translated:
            best_chunks, best = native, d_native
        else:
            best_chunks, best = translated, d_translated

        exp = {s.lower() for s in q.get("expected_sources", [])}
        hit = (any(c.source.lower() in exp for c in best_chunks) if exp else None)
        rows.append({
            "language": language, "id": q["id"],
            "tier": classify_tier(best),                       # cross-lingual (fix)
            "tier_translated": classify_tier(d_translated),    # old behaviour
            "best_distance": round(best, 3),
            "best_distance_translated": round(d_translated, 3),
            "hit": hit,
        })
    return rows


def run(gold_path: Path, languages: list[str], *, k: int, limit: int | None) -> dict:
    gold = json.loads(gold_path.read_text(encoding="utf-8"))
    questions = [it for it in gold["items"] if it["type"] == "in_curriculum"]
    if limit:
        questions = questions[:limit]

    per_language, all_rows = {}, []
    for lang in languages:
        rows = evaluate_language(questions, lang, k=k)
        per_language[lang] = summarize_language(rows)
        all_rows.extend(rows)
    return {
        "per_language": per_language,
        "fairness_gaps": fairness_gaps(per_language),
        "rows": all_rows,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Language-fairness evaluation.")
    p.add_argument("--gold", type=Path, default=Path("data/eval/gold_set.json"))
    p.add_argument("--languages", nargs="+",
                   default=["English", "Bahasa Melayu", "Thai", "Vietnamese", "Iban"])
    p.add_argument("--k", type=int, default=3)
    p.add_argument("--limit", type=int, default=None,
                   help="cap questions per language (translation is slow)")
    p.add_argument("--report", type=Path, default=None)
    args = p.parse_args(argv)

    out = run(args.gold, args.languages, k=args.k, limit=args.limit)

    def _p(v):
        return "n/a" if v is None else f"{v * 100:.0f}%"

    print("\n=== Language fairness (same questions, varied language) ===")
    print(f"  grounded% — translated-only (old) -> cross-lingual (fix)\n")
    print(f"  {'language':<16} {'old':>5} {'fix':>5} {'answered':>8} {'non-resp':>8} {'dist':>6}")
    for lang, s in out["per_language"].items():
        old = _p(s.get("grounded_rate_translated", s.get("grounded_rate")))
        print(f"  {lang:<16} {old:>5} {_p(s.get('grounded_rate')):>5} "
              f"{_p(s.get('answered_rate')):>8} {_p(s.get('non_response_rate')):>8} "
              f"{s.get('mean_distance', 'n/a'):>6}")
    if out["fairness_gaps"]:
        print("\n  Grounding gap vs English (bias signal, higher = worse):")
        for lang, gap in out["fairness_gaps"].items():
            flag = "  ⚠" if gap >= 0.2 else ""
            print(f"    {lang:<16} {gap * 100:+.0f} pts{flag}")
    print()

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Full report written to {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

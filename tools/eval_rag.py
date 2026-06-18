"""
tools/eval_rag.py
=================
Quantitative evaluation harness for Edge's Agentic RAG pipeline.

Turns the qualitative "high accuracy / reduced hallucination" claims into
measured numbers a reviewer can check, using a gold-standard question set
(data/eval/gold_set.json) drawn from the bundled curriculum.

Metrics reported
----------------
Retrieval (needs only the embedder, runs fully offline):
  - Retrieval hit-rate (recall@k): expected source appears in the top-k chunks
  - Retrieval precision@k (relevant): share of top-k chunks that actually contain
    the answer's key facts. The meaningful precision number, because the same
    concept is taught across several curriculum files.
  - Retrieval precision@k (source): share of top-k chunks from a *labelled* file.
    Reported for transparency, but understates quality when on-topic content lives
    in sibling files the gold set didn't list.
  - Tier distribution: grounded / supplementary / non-response
  - Non-response rate on in-curriculum questions (should be low)
  - False-grounding rate on off-curriculum questions (should be ~0)

Answer quality (needs Ollama + the SLM; enable with --with-llm):
  - Answer accuracy: share of in-curriculum answers containing the expected
    key facts (keyword recall >= --keyword-threshold)
  - Hallucination rate: off-curriculum questions answered as if grounded
    (tier == grounded with a citation)
  - Confidence calibration: mean verifier confidence for correct vs. incorrect

Usage
-----
    # Retrieval-only (fast, offline, no LLM):
    python -m tools.eval_rag

    # Full evaluation (requires `ollama serve` + the model pulled):
    python -m tools.eval_rag --with-llm --report data/eval/last_run.json

The pure metric functions (retrieval_metrics, keyword_score, classify_tier,
aggregate) are import-safe and unit-tested without any models.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Tier gates mirror the live pipeline so the harness measures what students see.
from core.agents.orchestrator import GROUNDED_GATE, SUPPLEMENTARY_GATE

GOLD_DEFAULT = Path("data/eval/gold_set.json")


# ---------------------------------------------------------------------------
# Pure metric helpers (no models — unit tested)
# ---------------------------------------------------------------------------

def classify_tier(best_distance: float) -> str:
    """Map a best retrieval distance to the pipeline's response tier."""
    if best_distance <= GROUNDED_GATE:
        return "grounded"
    if best_distance <= SUPPLEMENTARY_GATE:
        return "supplementary"
    return "none"


def retrieval_metrics(expected_sources: list[str], retrieved_sources: list[str]) -> dict:
    """Precision@k and hit (recall) for one question.

    precision = share of retrieved chunks from an expected source.
    hit       = at least one expected source was retrieved.
    Questions with no expected source (off-curriculum) return precision/hit = None.
    """
    if not expected_sources:
        return {"precision": None, "hit": None}
    expected = {s.lower() for s in expected_sources}
    got = [s.lower() for s in retrieved_sources]
    if not got:
        return {"precision": 0.0, "hit": False}
    relevant = sum(1 for s in got if s in expected)
    return {"precision": relevant / len(got), "hit": relevant > 0}


def content_precision(retrieved_texts: list[str], keywords: list[str],
                      min_hits: int = 1) -> float | None:
    """Content-based precision@k: share of retrieved chunks that actually contain
    the answer's key facts.

    Filename-match precision penalises retrieving an on-topic chunk that happens to
    live in a sibling curriculum file (the same concept is taught in several files),
    so it understates retrieval quality. This judges each chunk by what it *says*:
    a chunk counts as relevant if it contains at least *min_hits* of the expected
    keywords. Returns None when there are no keywords (off-curriculum).
    """
    if not keywords:
        return None
    if not retrieved_texts:
        return 0.0
    kws = [k.lower() for k in keywords]
    relevant = sum(
        1 for t in retrieved_texts
        if sum(1 for k in kws if k in (t or "").lower()) >= min_hits
    )
    return relevant / len(retrieved_texts)


def keyword_score(answer: str, keywords: list[str]) -> dict:
    """Fraction of expected key facts present in the answer (case-insensitive)."""
    if not keywords:
        return {"matched": 0, "total": 0, "recall": None}
    low = (answer or "").lower()
    matched = sum(1 for k in keywords if k.lower() in low)
    return {"matched": matched, "total": len(keywords), "recall": matched / len(keywords)}


def aggregate(rows: list[dict], keyword_threshold: float = 0.5) -> dict:
    """Roll per-question rows up into the summary metrics table."""
    in_curr = [r for r in rows if r["type"] == "in_curriculum"]
    off_curr = [r for r in rows if r["type"] == "off_curriculum"]

    def _mean(vals):
        vals = [v for v in vals if v is not None]
        return round(sum(vals) / len(vals), 3) if vals else None

    # Retrieval (in-curriculum only)
    hit_rate = _mean([1.0 if r["hit"] else 0.0 for r in in_curr if r["hit"] is not None])
    precision = _mean([r["precision"] for r in in_curr if r["precision"] is not None])
    rel_precision = _mean(
        [r["relevant_precision"] for r in in_curr if r.get("relevant_precision") is not None]
    )

    # Tiering
    tiers = [r["tier"] for r in rows]
    tier_dist = {t: tiers.count(t) for t in ("grounded", "supplementary", "none")}
    non_response_in = _mean([1.0 if r["tier"] == "none" else 0.0 for r in in_curr])
    false_ground_off = _mean(
        [1.0 if (r["tier"] == "grounded" and r.get("has_citation")) else 0.0 for r in off_curr]
    )

    summary = {
        "n_total": len(rows),
        "n_in_curriculum": len(in_curr),
        "n_off_curriculum": len(off_curr),
        "retrieval_hit_rate": hit_rate,
        "retrieval_relevant_precision_at_k": rel_precision,
        "retrieval_source_precision_at_k": precision,
        "tier_distribution": tier_dist,
        "non_response_rate_in_curriculum": non_response_in,
        "false_grounding_rate_off_curriculum": false_ground_off,
    }

    # Answer-quality metrics only when the LLM actually ran
    scored = [r for r in in_curr if r.get("keyword_recall") is not None]
    if scored:
        correct = [r for r in scored if r["keyword_recall"] >= keyword_threshold]
        summary["answer_accuracy"] = round(len(correct) / len(scored), 3)
        summary["mean_keyword_recall"] = _mean([r["keyword_recall"] for r in scored])
        summary["hallucination_rate"] = false_ground_off
        summary["mean_confidence_correct"] = _mean([r.get("confidence") for r in correct])
        summary["mean_confidence_incorrect"] = _mean(
            [r.get("confidence") for r in scored if r["keyword_recall"] < keyword_threshold]
        )
    return summary


# ---------------------------------------------------------------------------
# Per-question evaluation (uses the live pipeline)
# ---------------------------------------------------------------------------

def evaluate_item(item: dict, *, k: int, with_llm: bool, subject_filter: bool) -> dict:
    """Run retrieval (and optionally the full pipeline) for one gold item."""
    from core.rag_engine import retrieve_with_citations

    subject = item.get("subject", "General") if subject_filter else "General"
    chunks = retrieve_with_citations(item["question"], n_results=k, subject=subject)
    retrieved_sources = [c.source for c in chunks]
    retrieved_texts = [c.text for c in chunks]
    best_distance = min((c.distance for c in chunks), default=1.0)

    rmetrics = retrieval_metrics(item.get("expected_sources", []), retrieved_sources)
    row = {
        "id": item["id"],
        "type": item["type"],
        "tier": classify_tier(best_distance),
        "best_distance": round(best_distance, 3),
        "precision": rmetrics["precision"],
        "relevant_precision": content_precision(retrieved_texts, item.get("answer_keywords", [])),
        "hit": rmetrics["hit"],
        "retrieved_sources": retrieved_sources,
        "keyword_recall": None,
        "confidence": None,
        "has_citation": False,
    }

    if with_llm:
        from core.llm_engine import query_tutor
        result = query_tutor(item["question"], "English", student_id=None,
                             subject=subject)
        row["tier"] = result.get("tier", row["tier"])
        row["confidence"] = result.get("confidence")
        row["has_citation"] = bool(result.get("citations"))
        if item["type"] == "in_curriculum":
            ks = keyword_score(result.get("answer", ""), item.get("answer_keywords", []))
            row["keyword_recall"] = ks["recall"]
    return row


def group_summaries(rows: list[dict], key: str, keyword_threshold: float = 0.5) -> dict:
    """Per-group summaries for fairness/bias analysis (Issue 9).

    Groups rows by row[key] (e.g. 'country', 'language', 'subject') so accuracy,
    non-response, and retrieval can be compared across ASEAN contexts to surface
    hidden bias. Rows missing the key are grouped under 'unspecified'.
    """
    groups: dict[str, list[dict]] = {}
    for r in rows:
        groups.setdefault(r.get(key) or "unspecified", []).append(r)
    return {g: aggregate(rs, keyword_threshold=keyword_threshold)
            for g, rs in sorted(groups.items())}


def run(gold_path: Path, *, k: int, with_llm: bool, subject_filter: bool,
        keyword_threshold: float, group_by: str | None = None) -> dict:
    gold = json.loads(gold_path.read_text(encoding="utf-8"))
    items = gold["items"]
    rows = []
    for it in items:
        row = evaluate_item(it, k=k, with_llm=with_llm, subject_filter=subject_filter)
        # carry any grouping attributes (country, language, ...) onto the row
        for attr in ("country", "language", "subject", "grade"):
            if attr in it:
                row[attr] = it[attr]
        rows.append(row)
    out = {"summary": aggregate(rows, keyword_threshold=keyword_threshold), "rows": rows}
    if group_by:
        out["groups"] = group_summaries(rows, group_by, keyword_threshold=keyword_threshold)
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _fmt_pct(v) -> str:
    return "n/a" if v is None else f"{v * 100:.1f}%"


def _print_summary(summary: dict, with_llm: bool) -> None:
    print("\n=== Edge RAG Evaluation ===")
    print(f"Questions: {summary['n_total']} "
          f"({summary['n_in_curriculum']} in-curriculum, "
          f"{summary['n_off_curriculum']} off-curriculum)")
    print(f"Mode: {'full (retrieval + LLM)' if with_llm else 'retrieval-only'}\n")

    def _pct(v):
        return "n/a" if v is None else f"{v * 100:.1f}%"

    print(f"  Retrieval hit-rate (recall@k):      {_pct(summary['retrieval_hit_rate'])}")
    print(f"  Retrieval precision@k (relevant):   {_pct(summary['retrieval_relevant_precision_at_k'])}")
    print(f"  Retrieval precision@k (source):     {_pct(summary['retrieval_source_precision_at_k'])}")
    td = summary["tier_distribution"]
    print(f"  Tier distribution:                  grounded={td['grounded']} "
          f"supplementary={td['supplementary']} none={td['none']}")
    print(f"  Non-response (in-curriculum):       {_pct(summary['non_response_rate_in_curriculum'])}")
    print(f"  False-grounding (off-curriculum):   {_pct(summary['false_grounding_rate_off_curriculum'])}")
    if "answer_accuracy" in summary:
        print(f"  Answer accuracy:                    {_pct(summary['answer_accuracy'])}")
        print(f"  Mean keyword recall:                {_pct(summary['mean_keyword_recall'])}")
        print(f"  Hallucination rate:                 {_pct(summary['hallucination_rate'])}")
        print(f"  Mean confidence (correct):          {_pct(summary['mean_confidence_correct'])}")
        print(f"  Mean confidence (incorrect):        {_pct(summary['mean_confidence_incorrect'])}")
    print()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Evaluate the Edge RAG pipeline.")
    p.add_argument("--gold", type=Path, default=GOLD_DEFAULT, help="gold-set JSON path")
    p.add_argument("--k", type=int, default=3, help="top-k chunks to retrieve")
    p.add_argument("--with-llm", action="store_true",
                   help="also run the SLM (needs Ollama) for answer-quality metrics")
    p.add_argument("--no-subject-filter", action="store_true",
                   help="retrieve across all subjects (ignore the question's subject)")
    p.add_argument("--keyword-threshold", type=float, default=0.5,
                   help="keyword recall at/above which an answer counts as correct")
    p.add_argument("--group-by", default=None,
                   help="break results down by an item attribute (country/language/subject)")
    p.add_argument("--report", type=Path, default=None, help="write full JSON report here")
    args = p.parse_args(argv)

    if not args.gold.exists():
        print(f"Gold set not found: {args.gold}", file=sys.stderr)
        return 2

    out = run(args.gold, k=args.k, with_llm=args.with_llm,
              subject_filter=not args.no_subject_filter,
              keyword_threshold=args.keyword_threshold,
              group_by=args.group_by)
    _print_summary(out["summary"], args.with_llm)

    if "groups" in out:
        print(f"=== Breakdown by {args.group_by} (fairness / bias) ===")
        for g, s in out["groups"].items():
            acc = s.get("answer_accuracy")
            acc_str = "n/a" if acc is None else f"{acc * 100:.1f}%"
            hit = s.get("retrieval_hit_rate")
            hit_str = "n/a" if hit is None else f"{hit * 100:.1f}%"
            print(f"  {g:<16} n={s['n_total']:>3}  hit={hit_str:>6}  accuracy={acc_str:>6}  "
                  f"non-response={_fmt_pct(s['non_response_rate_in_curriculum'])}")
        print()

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Full report written to {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

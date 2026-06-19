"""
tools/make_grading_sheet.py
===========================
Generate a human-grading sheet for answer correctness (Issue 2).

Automated LLM judges proved unreliable for pedagogically-simplified tutoring text
(they penalise "top number" vs "numerator"), so the one credible accuracy number
comes from humans. This runs the live tutor over the gold set, saves each
question + the model's answer, and writes:

  * a CSV  (grade in a spreadsheet), and
  * an HTML sheet (grade in a browser, radio buttons + running tally)

A grader marks each answer Correct / Partial / Wrong. tools/score_grading_sheet.py
then turns the filled CSV into the final accuracy number.

Usage
-----
    OLLAMA_MODEL=phi3:mini python -m tools.make_grading_sheet \
        --gold data/eval/gold_set.json --out data/eval/grading

Produces data/eval/grading.csv and data/eval/grading.html.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
from pathlib import Path


def build_rows(gold_path: Path, subject_filter: bool = True) -> list[dict]:
    """Run the live pipeline over in-curriculum questions and capture answers."""
    from core.llm_engine import query_tutor

    gold = json.loads(gold_path.read_text(encoding="utf-8"))
    rows = []
    for it in gold["items"]:
        if it["type"] != "in_curriculum":
            continue
        subject = it.get("subject", "General") if subject_filter else "General"
        result = query_tutor(it["question"], "English", student_id=None, subject=subject)
        rows.append({
            "id": it["id"],
            "subject": it.get("subject", ""),
            "question": it["question"],
            "answer": result.get("answer", ""),
            "tier": result.get("tier", ""),
            "expected_keywords": ", ".join(it.get("answer_keywords", [])),
            "grade": "",          # grader fills: correct | partial | wrong
        })
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cols = ["id", "subject", "question", "answer", "tier", "expected_keywords", "grade"]
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


_HTML_HEAD = """<!doctype html><meta charset="utf-8">
<title>Edge — Answer Grading</title>
<style>
 body{font-family:system-ui,sans-serif;max-width:820px;margin:1.5rem auto;padding:0 1rem;color:#222}
 h1{font-size:1.2rem}.muted{color:#777;font-size:.9rem}
 .card{border:1px solid #e3e3e3;border-radius:10px;padding:1rem;margin:1rem 0;box-shadow:0 1px 3px rgba(0,0,0,.05)}
 .q{font-weight:700}.a{margin:.5rem 0;white-space:pre-wrap;background:#f8f9fa;border-radius:8px;padding:.7rem}
 .kw{color:#888;font-size:.8rem}.opts{display:flex;gap:1rem;margin-top:.5rem}
 label{cursor:pointer}#tally{position:sticky;top:0;background:#fff;padding:.6rem 0;border-bottom:1px solid #eee;font-weight:700}
 .ok{color:#1e8e3e}.pa{color:#b06000}.wr{color:#c62828}
 button{padding:.5rem 1rem;border:none;border-radius:8px;background:#1a73e8;color:#fff;font-weight:700;cursor:pointer}
</style>
<h1>Edge — Answer Grading Sheet</h1>
<p class="muted">Read each answer and mark it against what the curriculum actually says.
<b>Correct</b> = factually right and answers the question. <b>Partial</b> = right idea,
incomplete or minor error. <b>Wrong</b> = incorrect or off-topic. Simplified, child-friendly
wording is fine — grade the <i>meaning</i>, not the vocabulary.</p>
<div id="tally">Graded 0 — Correct 0 · Partial 0 · Wrong 0</div>
<form id="f">
"""

_HTML_TAIL = """</form>
<p><button type="button" onclick="dl()">Download graded CSV</button></p>
<script>
const rows = ROWS_JSON;
function tally(){
 let c=0,p=0,w=0,g=0;
 rows.forEach(r=>{const v=document.querySelector(`input[name="${r.id}"]:checked`);
   if(v){g++; v.value==='correct'?c++:v.value==='partial'?p++:w++;}});
 document.getElementById('tally').innerHTML =
  `Graded ${g}/${rows.length} — <span class="ok">Correct ${c}</span> · `+
  `<span class="pa">Partial ${p}</span> · <span class="wr">Wrong ${w}</span>`+
  (g?` — accuracy(correct only) ${(100*c/g).toFixed(1)}% · with-partial ${(100*(c+0.5*p)/g).toFixed(1)}%`:``);
}
document.addEventListener('change',tally);
function dl(){
 let out='id,grade\\n';
 rows.forEach(r=>{const v=document.querySelector(`input[name="${r.id}"]:checked`);
   out+=`${r.id},${v?v.value:''}\\n`;});
 const b=new Blob([out],{type:'text/csv'});const a=document.createElement('a');
 a.href=URL.createObjectURL(b);a.download='grading_filled.csv';a.click();
}
</script>
"""


def write_html(rows: list[dict], path: Path) -> None:
    parts = [_HTML_HEAD]
    for r in rows:
        parts.append(
            f'<div class="card"><div class="q">{html.escape(r["question"])}'
            f' <span class="muted">({html.escape(r["subject"])})</span></div>'
            f'<div class="a">{html.escape(r["answer"])}</div>'
            f'<div class="kw">expected concepts: {html.escape(r["expected_keywords"])}</div>'
            f'<div class="opts">'
            f'<label><input type="radio" name="{r["id"]}" value="correct"> Correct</label>'
            f'<label><input type="radio" name="{r["id"]}" value="partial"> Partial</label>'
            f'<label><input type="radio" name="{r["id"]}" value="wrong"> Wrong</label>'
            f'</div></div>'
        )
    parts.append(_HTML_TAIL.replace(
        "ROWS_JSON", json.dumps([{"id": r["id"]} for r in rows])))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(parts), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Build a human answer-grading sheet.")
    p.add_argument("--gold", type=Path, default=Path("data/eval/gold_set.json"))
    p.add_argument("--out", type=Path, default=Path("data/eval/grading"),
                   help="output stem; writes <stem>.csv and <stem>.html")
    p.add_argument("--no-subject-filter", action="store_true")
    args = p.parse_args(argv)

    rows = build_rows(args.gold, subject_filter=not args.no_subject_filter)
    csv_path = args.out.with_suffix(".csv")
    html_path = args.out.with_suffix(".html")
    write_csv(rows, csv_path)
    write_html(rows, html_path)
    print(f"Wrote {len(rows)} answers to grade:")
    print(f"  CSV : {csv_path}")
    print(f"  HTML: {html_path}  (open in a browser, grade, click 'Download graded CSV')")
    print("Then: python -m tools.score_grading_sheet --answers "
          f"{csv_path} --graded grading_filled.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

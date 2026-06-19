"""
tools/make_translation_sheet.py
===============================
Build a reference-collection sheet for translation-quality scoring (Issue 4).

chrF needs *reference* translations. For low-resource languages (Iban, Cebuano)
those don't exist in open corpora, so a fluent speaker supplies them — once. This
pulls ~25 real curriculum sentences and writes a sheet where a speaker types the
correct translation per language; `tools/eval_translation.py --sheet` then turns
the filled sheet into a chrF number.

~1 hour of one fluent speaker → real per-language translation quality.

Usage
-----
    python -m tools.make_translation_sheet --languages Iban Cebuano --n 25 \
        --out data/eval/translation_sheet
    # speaker fills data/eval/translation_sheet.html in a browser, downloads CSV
    python -m tools.eval_translation --sheet translation_sheet_filled.csv
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import re
from pathlib import Path


def extract_sentences(curriculum_dir: Path, n: int = 25) -> list[str]:
    """Pull clean, short, standalone English sentences from the curriculum."""
    out, seen = [], set()
    for f in sorted(Path(curriculum_dir).glob("*.txt")):
        text = f.read_text(encoding="utf-8", errors="replace")
        for raw in re.split(r"(?<=[.!?])\s+", text):
            s = " ".join(raw.split())
            words = s.split()
            if not (6 <= len(words) <= 16):
                continue
            if "—" in s or s != s.lstrip() or not s[:1].isupper():
                continue
            # skip lines that swallowed an ALL-CAPS heading (e.g. "SCIENCE — ...")
            if any(w.isupper() and len(w) > 2 for w in words[:4]):
                continue
            key = s.lower()[:40]
            if key in seen:
                continue
            seen.add(key)
            out.append(s)
            if len(out) >= n:
                return out
    return out


def write_csv(sentences: list[str], languages: list[str], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cols = ["id", "source_en"] + languages
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for i, s in enumerate(sentences, 1):
            row = {"id": f"s{i:02d}", "source_en": s}
            row.update({lang: "" for lang in languages})
            w.writerow(row)


def write_html(sentences: list[str], languages: list[str], path: Path) -> None:
    rows_js = [{"id": f"s{i:02d}"} for i in range(1, len(sentences) + 1)]
    head = f"""<!doctype html><meta charset="utf-8"><title>Edge — Translation References</title>
<style>
 body{{font-family:system-ui,sans-serif;max-width:820px;margin:1.5rem auto;padding:0 1rem;color:#222}}
 h1{{font-size:1.2rem}} .muted{{color:#777;font-size:.9rem}}
 .card{{border:1px solid #e3e3e3;border-radius:10px;padding:1rem;margin:1rem 0}}
 .en{{font-weight:700;margin-bottom:.5rem}}
 .row{{display:flex;gap:.6rem;align-items:center;margin:.35rem 0}}
 .row label{{width:120px;color:#555;font-weight:600}}
 .row input{{flex:1;border:1px solid #ccc;border-radius:8px;padding:.4rem .6rem;font-size:1rem}}
 button{{padding:.55rem 1.1rem;border:none;border-radius:8px;background:#1a73e8;color:#fff;font-weight:700;cursor:pointer}}
 #bar{{position:sticky;top:0;background:#fff;padding:.5rem 0;border-bottom:1px solid #eee;font-weight:700}}
</style>
<h1>Edge — Translation Reference Collection (Issue 4)</h1>
<p class="muted">For each English sentence, type the correct, natural translation in
each language. Leave blank if unsure. When done, click <b>Download filled CSV</b> and
send it back. These become the gold references for measuring translation quality.</p>
<div id="bar">Filled 0</div><form id="f">"""
    parts = [head]
    langs_json = json.dumps(languages)
    for i, s in enumerate(sentences, 1):
        sid = f"s{i:02d}"
        inputs = "".join(
            f'<div class="row"><label>{html.escape(lang)}</label>'
            f'<input data-id="{sid}" data-lang="{html.escape(lang)}"></div>'
            for lang in languages
        )
        parts.append(f'<div class="card"><div class="en">{i}. {html.escape(s)}</div>{inputs}</div>')
    tail = """</form><p><button type="button" onclick="dl()">Download filled CSV</button></p>
<script>
const LANGS=__LANGS__, ROWS=__ROWS__;
function tally(){let n=0;document.querySelectorAll('input').forEach(i=>{if(i.value.trim())n++});
 document.getElementById('bar').textContent='Filled '+n+'/'+(ROWS.length*LANGS.length);}
document.addEventListener('input',tally);
function dl(){
 let head='id,source_en,'+LANGS.join(',')+'\\n', out=head;
 ROWS.forEach((r,idx)=>{
   const en=document.querySelectorAll('.card')[idx].querySelector('.en').textContent.replace(/^\\d+\\.\\s*/,'').replace(/"/g,'""');
   const cells=LANGS.map(l=>{const el=document.querySelector(`input[data-id="${r.id}"][data-lang="${l}"]`);return '"'+(el.value.trim().replace(/"/g,'""'))+'"';});
   out+=`${r.id},"${en}",`+cells.join(',')+'\\n';});
 const b=new Blob([out],{type:'text/csv'});const a=document.createElement('a');
 a.href=URL.createObjectURL(b);a.download='translation_sheet_filled.csv';a.click();}
</script>"""
    parts.append(tail.replace("__LANGS__", langs_json).replace("__ROWS__", json.dumps(rows_js)))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(parts), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Build a translation reference-collection sheet.")
    p.add_argument("--curriculum", type=Path, default=Path("data/curriculum"))
    p.add_argument("--languages", nargs="+", default=["Iban", "Cebuano"])
    p.add_argument("--n", type=int, default=25)
    p.add_argument("--out", type=Path, default=Path("data/eval/translation_sheet"))
    args = p.parse_args(argv)

    sentences = extract_sentences(args.curriculum, n=args.n)
    write_csv(sentences, args.languages, args.out.with_suffix(".csv"))
    write_html(sentences, args.languages, args.out.with_suffix(".html"))
    print(f"Wrote {len(sentences)} sentences for {args.languages}:")
    print(f"  CSV : {args.out.with_suffix('.csv')}")
    print(f"  HTML: {args.out.with_suffix('.html')}  (fluent speaker fills it, downloads CSV)")
    print(f"Then: python -m tools.eval_translation --sheet translation_sheet_filled.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

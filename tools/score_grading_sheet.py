"""
tools/score_grading_sheet.py
============================
Turn a filled human-grading sheet into the final answer-accuracy number (Issue 2).

Reads the grades (correct | partial | wrong) and reports:
  * strict accuracy   = correct / graded
  * lenient accuracy  = (correct + 0.5*partial) / graded
  * a per-subject breakdown
  * inter-rater agreement if two graders are supplied (so it's defensible, not
    one person's opinion).

Grades can come from the HTML sheet's "Download graded CSV" (columns: id, grade)
or from editing the 'grade' column of grading.csv directly.

Usage
-----
    python -m tools.score_grading_sheet --graded grading_filled.csv
    python -m tools.score_grading_sheet --graded g1.csv --graded2 g2.csv   # agreement
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

_VALID = {"correct", "partial", "wrong"}


def load_grades(path: Path) -> dict[str, str]:
    """Read {id: grade} from a CSV that has at least 'id' and 'grade' columns."""
    grades: dict[str, str] = {}
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            g = (row.get("grade") or "").strip().lower()
            if g in _VALID:
                grades[row["id"]] = g
    return grades


def load_subjects(answers_path: Path | None) -> dict[str, str]:
    if not answers_path or not answers_path.exists():
        return {}
    with answers_path.open(encoding="utf-8", newline="") as fh:
        return {r["id"]: r.get("subject", "") for r in csv.DictReader(fh)}


def score(grades: dict[str, str]) -> dict:
    n = len(grades)
    c = sum(1 for v in grades.values() if v == "correct")
    p = sum(1 for v in grades.values() if v == "partial")
    w = sum(1 for v in grades.values() if v == "wrong")
    return {
        "graded": n, "correct": c, "partial": p, "wrong": w,
        "accuracy_strict": round(c / n, 3) if n else None,
        "accuracy_lenient": round((c + 0.5 * p) / n, 3) if n else None,
    }


def by_subject(grades: dict[str, str], subjects: dict[str, str]) -> dict:
    groups: dict[str, list[str]] = {}
    for gid, g in grades.items():
        groups.setdefault(subjects.get(gid, "unknown"), []).append(g)
    return {s: score({i: v for i, v in enumerate(gs)}) for s, gs in sorted(groups.items())}


def agreement(g1: dict[str, str], g2: dict[str, str]) -> dict:
    """Raw agreement and Cohen's kappa between two graders on shared ids."""
    ids = sorted(set(g1) & set(g2))
    if not ids:
        return {"shared": 0}
    same = sum(1 for i in ids if g1[i] == g2[i])
    po = same / len(ids)
    labels = _VALID
    c1, c2 = Counter(g1[i] for i in ids), Counter(g2[i] for i in ids)
    pe = sum((c1[l] / len(ids)) * (c2[l] / len(ids)) for l in labels)
    kappa = (po - pe) / (1 - pe) if pe != 1 else 1.0
    return {"shared": len(ids), "raw_agreement": round(po, 3), "cohen_kappa": round(kappa, 3)}


def _pct(v):
    return "n/a" if v is None else f"{v * 100:.1f}%"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Score a human grading sheet.")
    p.add_argument("--graded", type=Path, required=True, help="filled CSV (id, grade)")
    p.add_argument("--graded2", type=Path, default=None, help="second grader (for agreement)")
    p.add_argument("--answers", type=Path, default=Path("data/eval/grading.csv"),
                   help="original sheet, for the per-subject breakdown")
    args = p.parse_args(argv)

    g1 = load_grades(args.graded)
    if not g1:
        print("No valid grades found (need a 'grade' column with correct/partial/wrong).")
        return 2

    s = score(g1)
    print("\n=== Human answer-accuracy (Issue 2) ===")
    print(f"  Graded:            {s['graded']}")
    print(f"  Correct/Partial/Wrong: {s['correct']} / {s['partial']} / {s['wrong']}")
    print(f"  Accuracy (strict):  {_pct(s['accuracy_strict'])}   (correct only)")
    print(f"  Accuracy (lenient): {_pct(s['accuracy_lenient'])}   (partial = half credit)")

    subjects = load_subjects(args.answers)
    if subjects:
        print("\n  By subject:")
        for subj, ss in by_subject(g1, subjects).items():
            print(f"    {subj:<22} n={ss['graded']:>2}  strict={_pct(ss['accuracy_strict'])}")

    if args.graded2:
        g2 = load_grades(args.graded2)
        a = agreement(g1, g2)
        print(f"\n  Inter-rater agreement (n={a.get('shared', 0)}): "
              f"raw={_pct(a.get('raw_agreement'))}  kappa={a.get('cohen_kappa', 'n/a')}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

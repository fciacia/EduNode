"""
core/diagram_engine.py
======================
Turn a student's maths question into a small, validated *diagram spec* that the
frontend renders as exact SVG. The model never draws pixels — it only describes
the figure (type + numbers); deterministic code draws it correctly. Works fully
offline (tiny JSON from phi3, rendered client-side).

generate_diagram(question, rag_context="", language="English", level="") -> dict | None
validate_diagram(spec) -> dict | None   # None = "no diagram helps / invalid"

Supported types: number_line, fraction_bar, bar_chart, rectangle,
right_triangle, function_plot.
"""
from __future__ import annotations

import json
import logging
import math
import re

log = logging.getLogger(__name__)

TYPES = ("number_line", "fraction_bar", "bar_chart", "rectangle", "right_triangle", "function_plot")

# Only digits, x, basic operators, parens, dot, caret, space — no identifiers
# (so no function names / globals can be evaluated).
_SAFE_EXPR = re.compile(r"^[0-9xX+\-*/^(). ]{1,120}$")

DIAGRAM_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "type":  {"type": "string", "enum": list(TYPES) + ["none"]},
        "title": {"type": "string"},
        "min":   {"type": "number"}, "max": {"type": "number"}, "step": {"type": "number"},
        "points": {"type": "array", "items": {"type": "object", "properties": {
            "value": {"type": "number"}, "label": {"type": "string"}}, "required": ["value"]}},
        "fractions": {"type": "array", "items": {"type": "object", "properties": {
            "numerator": {"type": "number"}, "denominator": {"type": "number"},
            "label": {"type": "string"}}, "required": ["numerator", "denominator"]}},
        "bars": {"type": "array", "items": {"type": "object", "properties": {
            "label": {"type": "string"}, "value": {"type": "number"}}, "required": ["label", "value"]}},
        "width": {"type": "number"}, "height": {"type": "number"}, "base": {"type": "number"},
        "unit": {"type": "string"},
        "expression": {"type": "string"}, "xmin": {"type": "number"}, "xmax": {"type": "number"},
    },
    "required": ["type"],
}


def _num(v):
    try:
        f = float(v)
        return f if math.isfinite(f) else None
    except (TypeError, ValueError):
        return None


def validate_diagram(spec) -> dict | None:
    """Return a cleaned, renderable spec or None (a wrong figure is worse than none)."""
    if not isinstance(spec, dict):
        return None
    kind = spec.get("type")
    if kind not in TYPES:                       # includes "none"
        return None

    if kind == "number_line":
        lo, hi = _num(spec.get("min")), _num(spec.get("max"))
        if lo is None or hi is None or lo >= hi:
            return None
        step = _num(spec.get("step")) or (hi - lo) / 10
        if step <= 0 or (hi - lo) / step > 60:   # keep tick count sane
            step = (hi - lo) / 10
        points = []
        for p in (spec.get("points") or [])[:12]:
            v = _num(isinstance(p, dict) and p.get("value"))
            if v is not None and lo <= v <= hi:
                points.append({"value": v, "label": str(p.get("label", "")).strip()[:12]})
        return {"type": kind, "min": lo, "max": hi, "step": step, "points": points}

    if kind == "fraction_bar":
        fracs = []
        for f in (spec.get("fractions") or [])[:3]:
            if not isinstance(f, dict):
                continue
            n, d = _num(f.get("numerator")), _num(f.get("denominator"))
            if n is None or d is None or d < 1 or d > 20 or n < 0 or n > d:
                continue
            fracs.append({"numerator": int(n), "denominator": int(d),
                          "label": str(f.get("label", "")).strip()[:16]})
        return {"type": kind, "fractions": fracs} if fracs else None

    if kind == "bar_chart":
        bars = []
        for b in (spec.get("bars") or [])[:8]:
            if not isinstance(b, dict):
                continue
            val = _num(b.get("value"))
            label = str(b.get("label", "")).strip()[:14]
            if val is None or val < 0 or not label:
                continue
            bars.append({"label": label, "value": val})
        if len(bars) < 1:
            return None
        return {"type": kind, "title": str(spec.get("title", "")).strip()[:40], "bars": bars}

    if kind == "rectangle":
        w, h = _num(spec.get("width")), _num(spec.get("height"))
        if w is None or h is None or not (0 < w <= 1000) or not (0 < h <= 1000):
            return None
        return {"type": kind, "width": w, "height": h, "unit": str(spec.get("unit", "")).strip()[:6]}

    if kind == "right_triangle":
        b, h = _num(spec.get("base")), _num(spec.get("height"))
        if b is None or h is None or not (0 < b <= 1000) or not (0 < h <= 1000):
            return None
        return {"type": kind, "base": b, "height": h, "unit": str(spec.get("unit", "")).strip()[:6]}

    if kind == "function_plot":
        expr = str(spec.get("expression", "")).strip()
        if not _SAFE_EXPR.match(expr):
            return None
        py = expr.replace("^", "**").replace("X", "x")
        try:                                     # confirm it actually computes a number
            val = eval(py, {"__builtins__": {}}, {"x": 1.0})  # noqa: S307 (whitelisted chars only)
            if not math.isfinite(float(val)):
                return None
        except Exception:
            return None
        xmin, xmax = _num(spec.get("xmin")), _num(spec.get("xmax"))
        if xmin is None or xmax is None or xmin >= xmax:
            xmin, xmax = -10.0, 10.0
        return {"type": kind, "expression": expr, "xmin": xmin, "xmax": xmax}

    return None


def generate_diagram(question: str, rag_context: str = "", language: str = "English", level: str = "") -> dict | None:
    from core.llm_engine import _ollama_generate

    system = (
        "You turn a school maths question into ONE diagram that helps a student understand it. "
        "Reply ONLY with a JSON object. If no diagram would help, reply {\"type\":\"none\"}. "
        "Choose the best 'type' and give its numbers:\n"
        "- number_line: min, max, step, points:[{value,label}]\n"
        "- fraction_bar: fractions:[{numerator,denominator,label}]\n"
        "- bar_chart: title, bars:[{label,value}]\n"
        "- rectangle: width, height, unit\n"
        "- right_triangle: base, height, unit\n"
        "- function_plot: expression (in x, e.g. \"2*x+1\"), xmin, xmax\n"
        "Use only numbers that match the question. No text outside the JSON. "
        f"Write any text labels in {language}."
    )
    ctx = f"Context:\n{rag_context}\n\n" if rag_context.strip() else ""
    prompt = f"{ctx}Question: {question}\nDiagram JSON:"

    raw = _ollama_generate(prompt, temperature=0.1, max_tokens=400, system=system, schema=DIAGRAM_SCHEMA)
    if not raw:
        return None
    raw = re.sub(r"```(?:json)?", "", raw).strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        if not m:
            return None
        try:
            data = json.loads(re.sub(r",\s*([}\]])", r"\1", m.group()))
        except json.JSONDecodeError:
            return None
    return validate_diagram(data)

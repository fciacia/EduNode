# Fairness across subjects — mechanism demo (real data)

This is a **real** breakdown, not a placeholder: `eval_rag --group-by subject` over
the 33-question gold set. It proves the per-group fairness machinery works
end-to-end — the cross-*country* evaluation (Issue 9) uses the identical path,
just grouped by `country` instead of `subject` once real curricula are added.

Retrieval-only run (no LLM), `python -m tools.eval_rag --group-by subject`:

| Subject | n | Retrieval hit-rate | Non-response |
|---|---|---|---|
| Mathematics | 11 | 100.0% | 0.0% |
| Science | 14 | 100.0% | 0.0% |
| English Language | 3 | 100.0% | 0.0% |
| Environmental Studies | 2 | 100.0% | 0.0% |
| Digital Literacy | 2 | 100.0% | 0.0% |

**Reading:** grounding is *equitable across subjects* — no subject is starved of
retrievable curriculum (every group finds its source, none falls to a non-response).
That's a genuine fairness signal on the dimension we currently have data for.

**For Issue 9 proper**, swap `--group-by subject` → `--group-by country` after
adding real per-country curricula and questions (see [README.md](README.md)).
Add `--with-llm` to also get per-group answer accuracy.

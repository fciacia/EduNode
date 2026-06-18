# Edge — Educational Effectiveness Pilot Protocol (Issue 1)

The system proves technical feasibility; this protocol defines how we prove
**learning effectiveness**. It is written so a rural school can run it with the
instrumentation Edge already ships — quiz scores, sessions, and completion are
logged in SQLite today (see [core/progress_tracker.py](../core/progress_tracker.py)),
so measurement is automatic once a pilot starts.

## 1. Research questions

1. Do students who use Edge improve test scores more than those who don't? (learning gain)
2. Do they retain knowledge longer? (retention)
3. Are they more engaged and more likely to complete lessons? (engagement / completion)

## 2. Design

**Quasi-experimental, pre/post with a comparison group** — realistic for rural
schools where full randomisation is hard.

- **Treatment group:** uses Edge for the topic over the study window.
- **Comparison group:** same topic, usual teaching, no Edge.
- Where possible, randomise at the class level to reduce selection bias. If not,
  match groups on a baseline pre-test and report it as quasi-experimental.

| Phase | Day | Activity | Measure |
|---|---|---|---|
| Baseline | 0 | Pre-test (20 items on target topic) | `quiz_results` |
| Intervention | 1–10 | Treatment uses Edge; comparison as usual | `sessions`, completion |
| Post | 11 | Post-test (same blueprint, reordered) | `quiz_results` |
| Retention | 25 | Delayed re-test (no studying between) | `quiz_results` |

## 3. Metrics & how Edge captures them

| Outcome | Metric | Source |
|---|---|---|
| Learning gain | Post − Pre score; normalised gain `(post−pre)/(100−pre)` | `quiz_results` |
| Retention | Delayed-test score vs. post | `quiz_results` |
| Engagement | Sessions/student, messages/session, active days | `sessions` |
| Completion | % who finish the lesson/quiz set | `sessions` + `quiz_results` |
| Mastery shift | Concepts moving struggling → mastered | `core/mastery_engine.py` |

The teacher dashboard (`/teacher`) already surfaces class averages, most-missed
concepts, and activity — usable as the live readout during the pilot.

## 4. Sample size

- Aim for **≥ 2 classes per arm (~30–60 students/arm)** to detect a medium effect
  (Cohen's d ≈ 0.5) at 80% power. Report achieved n honestly; a smaller pilot is
  framed as **preliminary**, not conclusive.

## 5. Analysis

- Primary: compare **normalised learning gain** between arms (independent-samples
  t-test or Mann–Whitney if non-normal); report effect size + 95% CI.
- Secondary: retention (post → delayed), engagement, completion.
- Equity: break results down by language and grade (ties into
  [BIAS_EVAL.md](BIAS_EVAL.md)) to confirm gains are not concentrated in one group.

## 6. Ethics

- Parental consent per [DATA_GOVERNANCE.md](DATA_GOVERNANCE.md); data stays on the
  hub; the comparison group receives Edge after the study (waitlist design) so no
  student is denied benefit.

## 7. Reporting template

> In a [N]-student, [N]-class pilot at [school], the Edge group improved
> normalised learning gain by [X] vs. [Y] for the comparison group (d = [d],
> 95% CI […]). Retention at two weeks was [..]. Median engagement was [..]
> sessions/student. [Preliminary / Confirmatory].

## 8. Doing a fast proxy run before a full deployment

If a school pilot isn't possible before a deadline, run a **proxy study**: 5–10
volunteer testers, same pre-test → use Edge → post-test flow, and report
**preliminary** pre/post deltas clearly labelled as such. It demonstrates the
instrument works end-to-end and produces real (if small-n) numbers, which is far
stronger than asserting effectiveness with none.

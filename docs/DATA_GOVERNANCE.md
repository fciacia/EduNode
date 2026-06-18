# Edge — Data Governance Framework (Issue 8)

Edge stores student profiles, learning sessions, quiz results, and language data
**locally** on the hub. Even fully offline, this is sensitive educational data
about minors. This document is the governance framework: what we collect, who can
see it, how long we keep it, and how access is controlled and audited.

## 1. Data inventory

| Data | Where | Sensitivity | Purpose |
|---|---|---|---|
| Student name, language, grade | SQLite `students` | Medium (minor PII) | Personalisation |
| Sessions, quiz results, badges | SQLite | Low–Medium | Progress tracking |
| Conversation turns | SQLite `conversation_turns` | Medium | Follow-up context |
| Dialect logs, translation flags/corrections | SQLite / JSONL | Low | Language flywheel |
| Audit log | SQLite `audit_log` | Low | Accountability |

No data leaves the hub. There is no cloud, no telemetry, no third-party calls
(`TRANSFORMERS_OFFLINE=1`, `HF_HUB_OFFLINE=1` enforced at startup).

## 2. Roles & access control

| Role | Can do | Mechanism |
|---|---|---|
| Student | Use chat/quiz; see **own** progress by name | Default, no secret |
| Teacher / Admin | Upload curriculum, edit glossary, correct translations, view the class dashboard and audit log | `ADMIN_TOKEN` via `X-Admin-Token` header or `?token=` |

All privileged routes are wrapped by `require_admin` ([app.py](../app.py)).
**Set a strong `ADMIN_TOKEN`** in `.env` — the default `changeme` must be changed
before deployment. Roadmap: per-teacher tokens so the audit log attributes actions
to individuals rather than a shared role.

## 3. Authentication

- Privileged access requires the shared admin token. The token is **never stored**
  in the audit log — only a non-reversible fingerprint (`_token_fingerprint`,
  SHA-256 prefix).
- Student identity is name-based (low-friction for shared classroom devices); it is
  an identifier, not an authenticator. Do not store data here that requires strong
  authentication to protect.

## 4. Audit logging

Every privileged access — **granted or denied** — is recorded in the `audit_log`
table with the action, actor fingerprint, path, outcome, and timestamp. View it at
`GET /api/audit?token=…`. This gives an accountability trail for who changed
curriculum or saw student data.

## 5. Encryption at rest

The SQLite DB and JSONL files sit on the hub's SSD. Because the hub is a physical
device that can be lost or stolen:

- **Recommended:** enable full-disk encryption on the Pi's storage (LUKS) so a
  stolen SSD yields no readable data. This is the simplest robust control for an
  offline device and is the documented deployment step.
- Keep the `ADMIN_TOKEN` out of the repo and out of shared images.

## 6. Parental consent

- Deploy with a short, printable consent form (per school) explaining what Edge
  records and that data stays on the local hub.
- Consent is managed at the school/ministry level; Edge stores only the minimum
  needed to function and exposes a delete path (below) for withdrawal.

## 7. Retention & deletion

- **Default retention:** a school term. At term end, a teacher can archive (export
  via sneakernet) and reset the student tables.
- **Right to erasure:** deleting a student row and their sessions/quiz_results
  removes their PII; conversation turns are keyed by conversation id and can be
  cleared with the existing reset path.
- Translation corrections and dialect logs are de-identified (no student id) and
  may be retained for language model improvement.

## 8. Implementation status

| Control | Status |
|---|---|
| Offline-only (no external calls) | ✅ enforced at startup |
| Role-based access on privileged routes | ✅ `require_admin` |
| Token fingerprint (no raw token stored) | ✅ |
| Audit log + viewer endpoint | ✅ `audit_log`, `/api/audit` |
| Per-teacher identities | ⏳ roadmap |
| Full-disk encryption | ⏳ deployment step (documented) |
| Parental consent form | ⏳ template per deployment |
| Automated retention job | ⏳ roadmap (manual term-reset today) |

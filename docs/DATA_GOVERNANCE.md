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
**Set a strong `ADMIN_TOKEN`** in `.env` — the default `changeme` is refused with a
startup warning. **Per-teacher identities:** register named teachers
(`POST /api/admin/teachers` or `register_teacher()`); each gets their own token, and
the audit log then attributes actions to the **teacher's name**, not a shared role.
The admin token still works as the built-in `admin` identity.

## 3. Authentication

- Privileged access requires the admin token or a registered teacher token. Tokens
  are **never stored** in the audit log — a known teacher is recorded by name, an
  unknown token only as a non-reversible fingerprint (`_token_fingerprint`).
- Login exchanges the token for an **HttpOnly cookie** (`/api/admin/login`), so the
  secret stops travelling in URLs / browser history / server logs.
- Student identity is name-based (low-friction for shared classroom devices); it is
  an identifier, not an authenticator. Do not store data here that requires strong
  authentication to protect.

## 4. Audit logging

Every privileged access — **granted or denied** — is recorded in the `audit_log`
table with the action, actor fingerprint, path, outcome, and timestamp. View it at
`GET /api/audit?token=…`. This gives an accountability trail for who changed
curriculum or saw student data.

## 5. Encryption at rest

The SQLite DB and JSONL files sit on the hub's SD/SSD. Because the hub is a physical
device that can be lost or stolen, encryption is two-layered:

**(a) Live data — full-disk encryption (the system-wide control).** Enable LUKS on
the Pi's storage so a stolen card yields nothing readable. This protects the live DB,
ChromaDB, logs, and models together — the right control for an always-on device:

```bash
# one-time, during imaging (destroys existing data on the target partition)
sudo cryptsetup luksFormat /dev/sdaX
sudo cryptsetup open /dev/sdaX edgedata
sudo mkfs.ext4 /dev/mapper/edgedata
# mount at boot via /etc/crypttab + a key file on a removable token, or a boot passphrase
```

**(b) Data that leaves the hub — application encryption (built in).** USB sneakernet
exports (progress DB, dialect logs) carry PII off-device during maintenance, so they
are encrypted with `core/crypto.py` (Fernet / AES-128 + HMAC, PBKDF2 key from a
passphrase) when `EDGE_BACKUP_PASSPHRASE` is set. A lost USB drive is then useless
without the passphrase, which lives only in the hub's `.env`. If the passphrase is
unset, the exporter **warns** that bundles are unencrypted.

- Keep `ADMIN_TOKEN` and `EDGE_BACKUP_PASSPHRASE` out of the repo and shared images.

## 6. Parental consent

- Deploy with a short, printable consent form (per school) explaining what Edge
  records and that data stays on the local hub. The consenting act is offline.
- **Edge records the consent decision:** `record_consent(student_id, granted, by)`
  (or `POST /api/consent`) stores the status, who confirmed it, and when; every
  student row carries a `consent_status` (default `pending`). This gives an auditable
  consent trail, and `get_consent()` exposes it to teachers.

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
| Cookie login (token out of URLs) | ✅ `/api/admin/login`, HttpOnly |
| Per-teacher identities (audit by name) | ✅ `teachers` table, `register_teacher` |
| Encrypted USB exports | ✅ `core/crypto.py` (`EDGE_BACKUP_PASSPHRASE`) |
| Full-disk encryption (live data) | ✅ documented LUKS deployment step |
| Parental consent record | ✅ `record_consent`, `/api/consent`, `consent_status` |
| Retention purge + right to erasure | ✅ `purge_older_than`, `delete_student` |
| Printable consent form | ⏳ template per deployment (offline act) |

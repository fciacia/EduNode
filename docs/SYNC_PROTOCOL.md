# Edge — Offline Sneakernet Sync Protocol

A 100% offline hub cannot stream telemetry or pull updates over a network, so all
data movement happens during **routine USB maintenance**. This document defines
the lightweight, asynchronous sync protocol used by
[sneakernet_sync.py](../sneakernet_sync.py): how content updates are deployed
*to* the hub and how flywheel telemetry is captured *from* it — safely, on an
encrypted drive.

## Why this design

- **Asynchronous by nature.** There is no live connection; the USB drive is the
  transport, visited on a maintenance cadence (e.g. monthly). Capture and deploy
  are batched and idempotent.
- **Trust, don't assume.** Incoming curriculum is version-merged and
  checksum-verified before it is indexed (see
  [CONTENT_GOVERNANCE.md](CONTENT_GOVERNANCE.md)).
- **De-identified out.** Only aggregate counts, language data, and teacher
  corrections leave the hub — never student names or raw conversations.

## Encrypted USB drive

The telemetry bundle and exported progress DB contain education data, so the
drive must be encrypted at rest:

- **Linux hub:** LUKS volume (`cryptsetup`), or a VeraCrypt container.
- **macOS dev:** an encrypted APFS volume / encrypted disk image.

The admin unlocks the drive, mounts it, runs the sync, unmounts, and stores the
drive securely. Edge operates on the *mounted* path — encryption is handled by the
OS, keeping the protocol lightweight.

## Run it

```bash
python sneakernet_sync.py --usb /media/usb0          # Linux
python sneakernet_sync.py --usb /Volumes/EDUNODE     # macOS
```

## USB layout

```
USB_ROOT/
├── new_curriculum/            # IN: files to deploy
│   ├── *.pdf, *.txt
│   └── manifest.json          # IN: publisher's versioned manifest (optional)
├── model_update.sh            # IN: optional model/software update script
└── exported_reports/          # OUT: written by the hub
    ├── progress_YYYYMMDD.db
    ├── dialect_logs_YYYYMMDD.json
    └── telemetry_YYYYMMDD.json   # de-identified flywheel bundle (+ sha256)
```

## Steps performed (in order)

| # | Step | Direction | Function |
|---|---|---|---|
| 1 | Copy new curriculum files | IN | `sync_curriculum` |
| 1b | Merge + **verify** content manifest | IN | `apply_content_manifest` |
| 2 | Re-index RAG (idempotent) | — | `reindex_rag` |
| 3 | Run `model_update.sh` if present | IN | `run_model_update` |
| 4 | Export progress DB | OUT | `export_progress_db` |
| 5 | Export dialect logs | OUT | `export_dialect_logs` |
| 6 | **Capture flywheel telemetry bundle** | OUT | `capture_telemetry` |

## The telemetry bundle (flywheel capture)

`capture_telemetry` writes a single JSON envelope built by
[core/telemetry_export.py](../core/telemetry_export.py):

```json
{
  "sha256": "…integrity checksum…",
  "telemetry": {
    "hub": {"id": "...", "region": "..."},
    "usage": { "students": N, "sessions": N, "class_avg_pct": P, ... },
    "translation_corrections": [ {language, original, corrected, ...} ],
    "translation_flags":       [ {language, note, ...} ],
    "dialect_logs":            [ {language, raw_input, ...} ],
    "counts": { "corrections": N, "flags": N, "dialect_logs": N }
  }
}
```

These corrections are exactly the teacher-verified pairs the **ASEAN Dialect
Flywheel** needs to fine-tune low-resource-language models. Back at a connected
site, bundles from many hubs are pooled, checksums verified, and fed into the
training pipeline.

## Integrity & conflict rules

- **Content deploy:** higher file `version` wins on merge; every file is
  checksum-verified before indexing; changed/missing files are reported, not
  silently trusted.
- **Telemetry capture:** each bundle carries a `sha256` over its payload so a
  corrupted transfer is detectable downstream.

## Known follow-ups

- Cryptographic signatures per publisher (beyond checksums) are on the
  [CONTENT_GOVERNANCE.md](CONTENT_GOVERNANCE.md) roadmap.

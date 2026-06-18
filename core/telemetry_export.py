"""
core/telemetry_export.py
========================
Lightweight, offline telemetry capture for the ASEAN Dialect Flywheel (sync).

A 100% offline hub still needs to ship its flywheel data — teacher-verified
translation corrections, flagged translations, dialect usage, and aggregate
engagement — back to where models are improved. There is no network, so capture
happens during routine USB maintenance: this module builds a single de-identified
JSON bundle that the sneakernet sync writes to the (encrypted) drive.

De-identification: only aggregate counts and language data leave the hub — no
student names, no raw conversations.

Public API
----------
build_bundle() -> dict
write_bundle(dest_dir) -> Path     # timestamped JSON + sha256 integrity field
"""
from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger(__name__)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _dialect_logs() -> list[dict]:
    """De-identified dialect usage from SQLite (no student linkage exists here)."""
    try:
        import core.progress_tracker as pt
        with pt._db() as conn:
            rows = conn.execute(
                "SELECT language, raw_input, detected_dialect_variant, logged_at"
                "  FROM dialect_logs ORDER BY id"
            ).fetchall()
        return [dict(r) for r in rows]
    except Exception as exc:  # noqa: BLE001
        log.warning("Could not read dialect_logs: %s", exc)
        return []


def build_bundle() -> dict:
    """Assemble the de-identified telemetry bundle the flywheel needs."""
    from core import analytics_engine as an
    from core import correction_store as cs

    corrections = cs.list_corrections(limit=10**9)
    flags = an.recent_flags(limit=10**9)
    dialect = _dialect_logs()

    payload = {
        "hub": {},
        "generated_at": _now(),
        "usage": an.class_overview(),
        "activity_by_subject": an.activity_by_subject(),
        "translation_corrections": corrections,
        "translation_flags": flags,
        "dialect_logs": dialect,
        "counts": {
            "corrections": len(corrections),
            "flags": len(flags),
            "dialect_logs": len(dialect),
        },
    }
    try:
        import config as cfg
        payload["hub"] = {"id": cfg.HUB_ID, "region": cfg.HUB_REGION}
    except Exception:  # noqa: BLE001
        pass
    return payload


def _checksum(payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def write_bundle(dest_dir: Path) -> Path:
    """Write a timestamped telemetry bundle (with integrity checksum) to *dest_dir*."""
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    payload = build_bundle()
    envelope = {"sha256": _checksum(payload), "telemetry": payload}
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    path = dest_dir / f"telemetry_{stamp}.json"
    path.write_text(json.dumps(envelope, indent=2, ensure_ascii=False), encoding="utf-8")
    log.info("Telemetry bundle written to %s (%d corrections, %d flags, %d dialect).",
             path, payload["counts"]["corrections"], payload["counts"]["flags"],
             payload["counts"]["dialect_logs"])
    return path

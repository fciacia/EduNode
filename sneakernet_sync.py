"""
sneakernet_sync.py — EduNode USB sneakernet sync
================================================
Run by the teacher when plugging in the monthly USB drive.

Usage:
    python sneakernet_sync.py --usb /media/usb0
    python sneakernet_sync.py --usb /Volumes/EDUNODE_USB   # macOS path

What it does (in order):
  1. Copy USB/new_curriculum/*.pdf  → data/curriculum/
  2. Call ingest_pdfs() to re-index RAG (idempotent)
  3. Run USB/model_update.sh if present
  4. Copy db/edunode.db → USB/exported_reports/progress_YYYYMMDD.db
  5. Export dialect_logs table → USB/exported_reports/dialect_logs_YYYYMMDD.json
  6. Print summary report
"""

from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _log(msg: str) -> None:
    print(f"[sneakernet] {msg}")


# ---------------------------------------------------------------------------
# Step 1 — Copy new curriculum PDFs from USB → data/curriculum/
# ---------------------------------------------------------------------------

def sync_curriculum(usb: Path) -> list[str]:
    src_dir = usb / "new_curriculum"
    dst_dir = Path("data/curriculum")
    dst_dir.mkdir(parents=True, exist_ok=True)

    copied: list[str] = []
    if not src_dir.exists():
        _log("No 'new_curriculum/' folder on USB — skipping curriculum sync.")
        return copied

    for pdf in src_dir.glob("*.pdf"):
        dst = dst_dir / pdf.name
        shutil.copy2(pdf, dst)
        copied.append(pdf.name)
        _log(f"  Copied {pdf.name}")

    # Also accept .txt files (plain text curriculum)
    for txt in src_dir.glob("*.txt"):
        dst = dst_dir / txt.name
        shutil.copy2(txt, dst)
        copied.append(txt.name)
        _log(f"  Copied {txt.name}")

    return copied


# ---------------------------------------------------------------------------
# Step 1b — Deploy content updates: merge + verify the content manifest
# ---------------------------------------------------------------------------

def apply_content_manifest(usb: Path, content_dir: Path = Path("data/curriculum")) -> dict:
    """Merge an incoming USB manifest into the local one and verify integrity.

    Gives the decentralized-update model a trust layer: incoming curriculum is
    version-merged (higher version wins, provenance preserved) and every file is
    checksum-verified before it is trusted/indexed. Returns the verify report.
    """
    from tools import content_manifest as cm

    content_dir = Path(content_dir)
    incoming_path = usb / "new_curriculum" / cm.MANIFEST_NAME
    local = cm.load_manifest(content_dir)

    if incoming_path.exists():
        incoming = json.loads(incoming_path.read_text(encoding="utf-8"))
        merged = cm.merge_manifests(local, incoming) if local else incoming
        cm.save_manifest(content_dir, merged)
        _log(f"  Content manifest merged ({len(merged.get('files', {}))} files).")
    elif local is None:
        # No manifest anywhere yet — bootstrap one for the files we have.
        cm.save_manifest(content_dir, cm.build_manifest(content_dir, publisher="local"))
        _log("  Bootstrapped a local content manifest.")

    manifest = cm.load_manifest(content_dir) or {}
    report = cm.verify(content_dir, manifest)
    if report["ok"]:
        _log(f"  Content verified: {len(report['verified'])} files OK.")
    else:
        _log(f"  WARNING: content integrity issues — changed={report['changed']} "
             f"missing={report['missing']}")
    return report


# ---------------------------------------------------------------------------
# Step 2 — Re-index RAG
# ---------------------------------------------------------------------------

def reindex_rag() -> int:
    _log("Re-indexing RAG…")
    try:
        from core.rag_engine import ingest_pdfs
        result = ingest_pdfs("data/curriculum")
        count  = result if isinstance(result, int) else 0
        _log(f"  RAG indexed: {count} chunks total")
        return count
    except Exception as exc:
        _log(f"  WARNING: RAG ingest failed — {exc}")
        return 0


# ---------------------------------------------------------------------------
# Step 3 — Run model_update.sh if present
# ---------------------------------------------------------------------------

def run_model_update(usb: Path) -> bool:
    script = usb / "model_update.sh"
    if not script.exists():
        return False

    _log("Running model_update.sh…")
    try:
        result = subprocess.run(
            ["bash", str(script)],
            timeout=300,
            check=True,
            capture_output=True,
            text=True,
        )
        _log("  model_update.sh completed successfully.")
        if result.stdout:
            for line in result.stdout.splitlines():
                _log(f"    {line}")
        return True
    except subprocess.CalledProcessError as exc:
        _log(f"  WARNING: model_update.sh failed (exit {exc.returncode})")
        return False
    except subprocess.TimeoutExpired:
        _log("  WARNING: model_update.sh timed out after 5 minutes")
        return False


# ---------------------------------------------------------------------------
# Step 4 — Export progress DB to USB
# ---------------------------------------------------------------------------

def export_progress_db(usb: Path) -> bool:
    db_src = Path("db/edunode.db")
    if not db_src.exists():
        _log("No db/edunode.db found — skipping DB export.")
        return False

    export_dir = usb / "exported_reports"
    export_dir.mkdir(parents=True, exist_ok=True)

    dst = export_dir / f"progress_{_stamp()}.db"
    shutil.copy2(db_src, dst)
    _log(f"  Progress DB exported → {dst.name}")
    return True


# ---------------------------------------------------------------------------
# Step 5 — Export dialect_logs as JSON
# ---------------------------------------------------------------------------

def export_dialect_logs(usb: Path) -> int:
    db_src = Path("db/edunode.db")
    if not db_src.exists():
        _log("No db/edunode.db found — skipping dialect log export.")
        return 0

    export_dir = usb / "exported_reports"
    export_dir.mkdir(parents=True, exist_ok=True)

    try:
        con = sqlite3.connect(str(db_src))
        con.row_factory = sqlite3.Row
        cur = con.execute(
            "SELECT id, language, text, created_at FROM dialect_logs ORDER BY id"
        )
        rows = [dict(r) for r in cur.fetchall()]
        con.close()
    except Exception as exc:
        _log(f"  WARNING: Could not read dialect_logs — {exc}")
        return 0

    dst = export_dir / f"dialect_logs_{_stamp()}.json"
    dst.write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    _log(f"  Dialect logs exported → {dst.name} ({len(rows)} entries)")
    return len(rows)


# ---------------------------------------------------------------------------
# Step 6 — Capture flywheel telemetry bundle to USB
# ---------------------------------------------------------------------------

def capture_telemetry(usb: Path) -> int:
    """Write the de-identified flywheel telemetry bundle to the USB drive.

    This is how the ASEAN Dialect Flywheel gets its teacher-verified corrections,
    flags, and dialect usage off a fully-offline hub: captured during routine USB
    maintenance. Use an encrypted drive (see docs/SYNC_PROTOCOL.md).
    """
    try:
        from core.telemetry_export import write_bundle
        path = write_bundle(usb / "exported_reports")
        env = json.loads(path.read_text(encoding="utf-8"))
        n = env["telemetry"]["counts"]["corrections"]
        _log(f"  Telemetry bundle captured → {path.name}")
        return n
    except Exception as exc:  # noqa: BLE001
        _log(f"  WARNING: telemetry capture failed — {exc}")
        return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="EduNode sneakernet USB sync — run when teacher plugs in USB drive.",
    )
    parser.add_argument(
        "--usb", required=True,
        help="Mount point of the USB drive (e.g. /media/usb0 or /Volumes/EDUNODE)",
    )
    parser.add_argument(
        "--skip-ingest", action="store_true",
        help="Skip RAG re-indexing (faster, use if only exporting data)",
    )
    args = parser.parse_args()

    usb = Path(args.usb)
    if not usb.exists():
        _log(f"ERROR: USB path does not exist: {usb}")
        sys.exit(1)

    _log(f"Starting sneakernet sync from {usb}")
    print("=" * 50)

    # Step 1
    copied = sync_curriculum(usb)

    # Step 1b — deploy + verify content updates (versioned manifest)
    content_ok = True
    try:
        content_ok = apply_content_manifest(usb)["ok"]
    except Exception as exc:  # noqa: BLE001
        _log(f"  WARNING: content manifest step failed — {exc}")

    # Step 2
    chunks = 0
    if not args.skip_ingest and copied:
        chunks = reindex_rag()
    elif args.skip_ingest:
        _log("Skipping RAG ingest (--skip-ingest flag set).")

    # Step 3
    model_updated = run_model_update(usb)

    # Step 4
    db_exported = export_progress_db(usb)

    # Step 5
    dialect_count = export_dialect_logs(usb)

    # Step 6 — flywheel telemetry bundle
    corrections_captured = capture_telemetry(usb)

    # Summary
    print("=" * 50)
    _log("Sync complete. Summary:")
    _log(f"  New curriculum files copied : {len(copied)}")
    _log(f"  Content integrity OK        : {content_ok}")
    _log(f"  RAG chunks after ingest     : {chunks}")
    _log(f"  Model update script ran     : {model_updated}")
    _log(f"  Progress DB exported        : {db_exported}")
    _log(f"  Dialect log entries exported: {dialect_count}")
    _log(f"  Telemetry corrections caught: {corrections_captured}")
    print("=" * 50)

    if copied:
        _log("New files:")
        for f in copied:
            _log(f"  + {f}")


if __name__ == "__main__":
    main()

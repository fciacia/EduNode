"""
tools/content_manifest.py
=========================
Versioned, provenance-tracked curriculum manifest (Issue 10).

Edge already distributes curriculum by sneakernet USB. For a decentralized model
where ministries, schools, NGOs, and local teachers each publish updates
independently, the hub needs to know **what content it has, who published it, what
version it is, and whether it has been tampered with**. This module adds that trust
layer on top of the existing file sync.

A manifest entry per curriculum file records: sha256 checksum, byte size, version,
publisher, and timestamp. On sync, the incoming manifest is merged with the local
one — the higher version of each file wins, and provenance is preserved.

CLI
---
    # Publisher builds/refreshes a manifest for a content folder:
    python -m tools.content_manifest build --dir data/curriculum --publisher "MoE-MY" --version 3

    # Hub verifies local files against the manifest (tamper / drift check):
    python -m tools.content_manifest verify --dir data/curriculum

The pure functions (file_entry, build_manifest, verify, merge_manifests) are
import-safe and unit-tested.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_NAME = "manifest.json"
CONTENT_GLOBS = ("*.pdf", "*.txt")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def file_entry(path: Path, publisher: str, version: int) -> dict:
    """Manifest entry for a single content file."""
    return {
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
        "version": version,
        "publisher": publisher,
        "updated_at": _now(),
    }


def _iter_content(content_dir: Path):
    for glob in CONTENT_GLOBS:
        yield from sorted(content_dir.glob(glob))


def build_manifest(content_dir: Path, publisher: str, version: int = 1) -> dict:
    """Build a manifest for every curriculum file in *content_dir*."""
    files = {p.name: file_entry(p, publisher, version) for p in _iter_content(content_dir)}
    return {
        "schema": 1,
        "generated_at": _now(),
        "publisher": publisher,
        "files": files,
    }


def verify(content_dir: Path, manifest: dict) -> dict:
    """Check files on disk against the manifest.

    Returns {ok, verified, changed, missing, untracked} — 'changed' means a file's
    checksum no longer matches (tampered or edited), 'missing' is in the manifest
    but not on disk, 'untracked' is on disk but not in the manifest.
    """
    declared = manifest.get("files", {})
    on_disk = {p.name: p for p in _iter_content(content_dir)}

    verified, changed, missing = [], [], []
    for name, entry in declared.items():
        if name not in on_disk:
            missing.append(name)
        elif sha256_file(on_disk[name]) == entry.get("sha256"):
            verified.append(name)
        else:
            changed.append(name)
    untracked = sorted(set(on_disk) - set(declared))

    return {
        "ok": not changed and not missing,
        "verified": sorted(verified),
        "changed": sorted(changed),
        "missing": sorted(missing),
        "untracked": untracked,
    }


def merge_manifests(local: dict, incoming: dict) -> dict:
    """Merge an incoming manifest into the local one (decentralized updates).

    Per file, the higher version wins; ties keep the incoming (newer push). The
    result preserves each winning file's publisher provenance.
    """
    merged = dict(local.get("files", {}))
    for name, entry in incoming.get("files", {}).items():
        cur = merged.get(name)
        if cur is None or entry.get("version", 0) >= cur.get("version", 0):
            merged[name] = entry
    return {
        "schema": 1,
        "generated_at": _now(),
        "publisher": "merged",
        "files": merged,
    }


def load_manifest(content_dir: Path) -> dict | None:
    path = content_dir / MANIFEST_NAME
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_manifest(content_dir: Path, manifest: dict) -> Path:
    path = content_dir / MANIFEST_NAME
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Build/verify the curriculum content manifest.")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="build/refresh a manifest")
    b.add_argument("--dir", type=Path, default=Path("data/curriculum"))
    b.add_argument("--publisher", default="local")
    b.add_argument("--version", type=int, default=1)
    b.add_argument("--merge", action="store_true",
                   help="merge into an existing manifest instead of replacing it")

    v = sub.add_parser("verify", help="verify files against the manifest")
    v.add_argument("--dir", type=Path, default=Path("data/curriculum"))

    args = p.parse_args(argv)

    if args.cmd == "build":
        new = build_manifest(args.dir, args.publisher, args.version)
        existing = load_manifest(args.dir)
        manifest = merge_manifests(existing, new) if (args.merge and existing) else new
        path = save_manifest(args.dir, manifest)
        print(f"Manifest written to {path} ({len(manifest['files'])} files, "
              f"publisher={args.publisher}, version={args.version}).")
        return 0

    if args.cmd == "verify":
        manifest = load_manifest(args.dir)
        if manifest is None:
            print(f"No {MANIFEST_NAME} in {args.dir}. Run `build` first.")
            return 2
        report = verify(args.dir, manifest)
        print(f"OK={report['ok']}  verified={len(report['verified'])}  "
              f"changed={report['changed']}  missing={report['missing']}  "
              f"untracked={report['untracked']}")
        return 0 if report["ok"] else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())

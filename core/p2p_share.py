"""
core/p2p_share.py
=================
Step 9 — Local-LAN P2P content sharing via URL + QR code.

Generates a short-lived share link that any device on the Pi's WiFi hotspot
can open in a browser. No internet required. Share content is stored on-disk
and expires after SHARE_TTL_MINUTES (default 30).

Public API
----------
create_share(content, content_type, ttl_minutes=30) -> dict
    Persist *content* and generate a QR code.
    Returns {"share_id", "local_url", "qr_image_path", "expires_at"}

get_shared_content(share_id) -> dict | None
    Retrieve share content. Returns None (and deletes the file) if expired.
"""

from __future__ import annotations

import json
import logging
import os
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

log = logging.getLogger(__name__)

SHARE_DIR        = Path(os.getenv("SHARE_DIR", "static/shared"))
HUB_IP           = os.getenv("HUB_IP", "192.168.1.1")
HUB_PORT         = int(os.getenv("SERVER_PORT", "5000"))
SHARE_TTL_MINUTES = int(os.getenv("SHARE_TTL_MINUTES", "30"))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _share_path(share_id: str) -> Path:
    return SHARE_DIR / f"{share_id}.json"


def _qr_path(share_id: str) -> Path:
    return SHARE_DIR / f"{share_id}_qr.png"


def _local_url(share_id: str) -> str:
    port_suffix = f":{HUB_PORT}" if HUB_PORT not in (80, 443) else ""
    return f"http://{HUB_IP}{port_suffix}/share/{share_id}"


def _generate_qr(url: str, out_path: Path) -> None:
    """Write a QR code PNG for *url* to *out_path*."""
    try:
        import qrcode  # type: ignore
        from PIL import Image  # noqa: F401 — ensure Pillow available

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(str(out_path))
        log.debug("QR code saved: %s", out_path)
    except ImportError:
        log.info("qrcode/Pillow not installed — QR image skipped.")
    except Exception as exc:  # noqa: BLE001
        log.warning("QR generation failed: %s", exc)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def create_share(
    content: str,
    content_type: str = "text",
    ttl_minutes: int = SHARE_TTL_MINUTES,
) -> dict:
    """
    Persist *content* and generate a QR code pointing to the share URL.

    Parameters
    ----------
    content      : The text/HTML/JSON payload to share.
    content_type : A label like "text", "quiz_result", "summary".
    ttl_minutes  : Minutes until the share expires (default 30).

    Returns
    -------
    {
        "share_id":      str,   # 8 hex chars
        "local_url":     str,   # http://192.168.1.1:5000/share/<id>
        "qr_image_path": str,   # relative path for use in <img src="">
        "expires_at":    str,   # ISO-8601 UTC timestamp
    }
    """
    SHARE_DIR.mkdir(parents=True, exist_ok=True)

    share_id   = uuid.uuid4().hex[:8]
    expires_at = (
        datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)
    ).isoformat()

    payload = {
        "share_id":    share_id,
        "content":     content,
        "content_type": content_type,
        "expires_at":  expires_at,
    }

    _share_path(share_id).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    local_url = _local_url(share_id)
    qr_out    = _qr_path(share_id)
    _generate_qr(local_url, qr_out)

    # Return a web-relative path so Flask can serve it directly
    qr_image_path = f"/static/shared/{share_id}_qr.png"

    log.info("Share created: %s (expires %s)", share_id, expires_at)
    return {
        "share_id":      share_id,
        "local_url":     local_url,
        "qr_image_path": qr_image_path,
        "expires_at":    expires_at,
    }


def get_shared_content(share_id: str) -> dict | None:
    """
    Return the share payload for *share_id*, or None if not found / expired.

    Expired share files are deleted on access.
    """
    # Validate share_id to prevent path traversal
    if not share_id or not all(c in "0123456789abcdef" for c in share_id) or len(share_id) != 8:
        log.warning("Invalid share_id requested: %r", share_id)
        return None

    path = _share_path(share_id)
    if not path.exists():
        return None

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        log.warning("Could not read share file '%s': %s", path, exc)
        return None

    expires_at_str = payload.get("expires_at", "")
    try:
        expires_at = datetime.fromisoformat(expires_at_str)
        if datetime.now(timezone.utc) > expires_at:
            log.info("Share '%s' has expired — deleting.", share_id)
            path.unlink(missing_ok=True)
            _qr_path(share_id).unlink(missing_ok=True)
            return None
    except ValueError:
        pass  # Malformed expiry — serve it anyway

    return payload

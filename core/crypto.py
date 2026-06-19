"""
core/crypto.py
==============
At-rest / in-transit encryption for sensitive data that LEAVES the hub — chiefly
the USB sneakernet bundles (progress DB, telemetry, dialect logs) that physically
travel during maintenance (data governance, Issue 8).

Authenticated encryption (Fernet = AES-128-CBC + HMAC-SHA256). The key is derived
from a passphrase via PBKDF2 with a per-file random salt, so a stolen USB drive (or
a copied DB file) is unreadable without the passphrase. The passphrase lives outside
the data — set EDGE_BACKUP_PASSPHRASE in the hub's .env, never on the drive.

Note: this protects data that leaves the device. For the LIVE database on the SD
card, full-disk encryption (LUKS) is the correct, system-wide protection — see
docs/DATA_GOVERNANCE.md.
"""
from __future__ import annotations

import base64
import os
import struct

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

_MAGIC = b"EDGE1"          # file header so we can detect/parse our own format
_SALT_LEN = 16
_PBKDF2_ITERS = 200_000


def _derive_key(passphrase: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                     iterations=_PBKDF2_ITERS)
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode("utf-8")))


def encrypt_bytes(data: bytes, passphrase: str) -> bytes:
    """Encrypt *data* with a passphrase. Output = MAGIC | iters | salt | token."""
    if not passphrase:
        raise ValueError("passphrase required")
    salt = os.urandom(_SALT_LEN)
    token = Fernet(_derive_key(passphrase, salt)).encrypt(data)
    return _MAGIC + struct.pack(">I", _PBKDF2_ITERS) + salt + token


def decrypt_bytes(blob: bytes, passphrase: str) -> bytes:
    """Reverse of encrypt_bytes. Raises ValueError on a wrong passphrase/corruption."""
    if not blob.startswith(_MAGIC):
        raise ValueError("not an Edge-encrypted file")
    off = len(_MAGIC)
    (iters,) = struct.unpack(">I", blob[off:off + 4]); off += 4
    salt = blob[off:off + _SALT_LEN]; off += _SALT_LEN
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iters)
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode("utf-8")))
    try:
        return Fernet(key).decrypt(blob[off:])
    except InvalidToken as exc:
        raise ValueError("wrong passphrase or corrupted data") from exc


def encrypt_file(src, dst, passphrase: str) -> None:
    from pathlib import Path
    data = Path(src).read_bytes()
    Path(dst).write_bytes(encrypt_bytes(data, passphrase))


def decrypt_file(src, dst, passphrase: str) -> None:
    from pathlib import Path
    blob = Path(src).read_bytes()
    Path(dst).write_bytes(decrypt_bytes(blob, passphrase))


def backup_passphrase() -> str | None:
    """The configured backup passphrase, or None if encryption isn't enabled."""
    return os.getenv("EDGE_BACKUP_PASSPHRASE") or None

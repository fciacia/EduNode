"""Tests for at-rest encryption of exported data (Issue 8)."""
import pytest

from core import crypto


def test_roundtrip():
    data = b"student: Aisha, score 7/10"
    blob = crypto.encrypt_bytes(data, "hunter2")
    assert blob != data and blob.startswith(b"EDGE1")
    assert crypto.decrypt_bytes(blob, "hunter2") == data


def test_wrong_passphrase_fails():
    blob = crypto.encrypt_bytes(b"secret", "right")
    with pytest.raises(ValueError):
        crypto.decrypt_bytes(blob, "wrong")


def test_distinct_salt_per_encryption():
    a = crypto.encrypt_bytes(b"x", "pw")
    b = crypto.encrypt_bytes(b"x", "pw")
    assert a != b                                  # random salt -> different ciphertext
    assert crypto.decrypt_bytes(a, "pw") == crypto.decrypt_bytes(b, "pw") == b"x"


def test_rejects_foreign_blob():
    with pytest.raises(ValueError):
        crypto.decrypt_bytes(b"not edge data", "pw")


def test_file_roundtrip(tmp_path):
    src = tmp_path / "p.db"; src.write_bytes(b"\x00DATA\xff" * 50)
    enc = tmp_path / "p.db.enc"; out = tmp_path / "p.out"
    crypto.encrypt_file(src, enc, "pw")
    crypto.decrypt_file(enc, out, "pw")
    assert out.read_bytes() == src.read_bytes()


def test_empty_passphrase_rejected():
    with pytest.raises(ValueError):
        crypto.encrypt_bytes(b"x", "")

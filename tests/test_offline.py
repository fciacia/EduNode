"""
Verified airplane-mode test.

Blocks every outbound connection to anything that isn't localhost, then drives
the app — proving Edge has no hidden internet dependency at runtime. Local
services (the app itself, Ollama on 127.0.0.1) are still allowed, because
"offline" means "no internet", not "no localhost".

Content is served from the offline cache, so this passes with Ollama stopped.
"""
import socket
from contextlib import contextmanager

import core.content_cache as cc

_LOCAL = {"127.0.0.1", "::1", "localhost", "0.0.0.0"}


class OfflineViolation(AssertionError):
    pass


@contextmanager
def airplane_mode():
    """Patch socket.connect so any non-localhost connection fails loudly."""
    real_connect = socket.socket.connect

    def guarded(self, address):
        host = address[0] if isinstance(address, tuple) else address
        if host not in _LOCAL:
            raise OfflineViolation(f"outbound internet connection to {host!r} attempted")
        return real_connect(self, address)

    socket.socket.connect = guarded
    try:
        yield
    finally:
        socket.socket.connect = real_connect


def test_app_runs_with_no_internet(tmp_path, monkeypatch):
    # Pre-bake one quiz into the cache (as prebake.py would), then go offline.
    monkeypatch.setattr(cc, "CACHE_DIR", tmp_path)
    cc.put("quiz", "Science", "English", "", "Photosynthesis", {
        "questions": [{"question": "Q?", "options": ["A", "B", "C", "D"],
                       "answer": "A", "explanation": "because"}],
        "grounded": True, "sources": [],
    })

    from app import app
    client = app.test_client()

    with airplane_mode():
        # Every page renders offline.
        for route in ["/", "/chat", "/quiz", "/flashcard", "/slides", "/podcast", "/progress"]:
            assert client.get(route).status_code == 200, route

        # Curriculum-grounded suggestions come from local files, not the network.
        assert client.get("/api/topics?subject=Science").status_code == 200

        # Pre-baked content is served from cache — no model, no internet.
        r = client.post("/api/quiz/generate",
                        json={"topic": "Photosynthesis", "language": "English", "subject": "Science"})
        assert r.status_code == 200
        assert len(r.get_json()["questions"]) == 1


def test_guard_actually_blocks_internet():
    # Sanity: the guard really does trip on a real external address.
    import pytest
    with airplane_mode():
        with pytest.raises(OfflineViolation):
            socket.create_connection(("example.com", 80), timeout=1)

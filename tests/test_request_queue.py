"""Tests for the admission-control request gate (concurrency safety)."""
from core.request_queue import RequestGate


def test_admits_up_to_max_then_sheds():
    gate = RequestGate(max_concurrency=2, default_timeout=0)
    cm1, cm2, cm3 = gate.slot(), gate.slot(), gate.slot()
    assert cm1.__enter__() is True
    assert cm2.__enter__() is True
    assert cm3.__enter__() is False          # over capacity -> shed immediately
    cm3.__exit__(None, None, None)
    cm2.__exit__(None, None, None)
    cm1.__exit__(None, None, None)


def test_slot_releases_for_reuse():
    gate = RequestGate(max_concurrency=1, default_timeout=0)
    with gate.slot() as a:
        assert a is True
        with gate.slot() as b:
            assert b is False                # busy while first slot held
    with gate.slot() as c:
        assert c is True                     # freed after the first block exits


def test_stats_track_active_and_rejected():
    gate = RequestGate(max_concurrency=1, default_timeout=0)
    with gate.slot() as a:
        assert a is True
        s = gate.stats()
        assert s["active"] == 1
        assert s["max_concurrency"] == 1
        with gate.slot() as b:
            assert b is False
        assert gate.stats()["rejected"] == 1
    end = gate.stats()
    assert end["active"] == 0
    assert end["total"] == 2


def test_waiting_returns_to_zero():
    gate = RequestGate(max_concurrency=1, default_timeout=0)
    with gate.slot():
        with gate.slot():
            pass
    assert gate.stats()["waiting"] == 0


def test_chat_sheds_when_saturated(temp_db, monkeypatch):
    # Hold the only slot, then a chat request must get a 503 busy response.
    import core.request_queue as rq
    monkeypatch.setattr(rq, "gate", RequestGate(max_concurrency=1, default_timeout=0))
    from app import app
    client = app.test_client()

    with rq.gate.slot() as held:
        assert held is True
        r = client.post("/api/chat", json={"message": "hi", "language": "English"})
    assert r.status_code == 503
    body = r.get_json()
    assert body["error"] == "busy"
    assert r.headers.get("Retry-After")

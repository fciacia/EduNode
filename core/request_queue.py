"""
core/request_queue.py
=====================
Admission control for heavy AI requests (concurrency / memory safety).

A single 8 GB hub cannot run 50 multi-agent pipelines at once — each in-flight
request holds embedder + NLLB + LLM working memory, and Ollama serves only one
generation at a time anyway. So instead of letting every request in and risking
an out-of-memory crash, we cap the number of *concurrent* heavy inferences with a
bounded gate. Excess requests wait briefly (queue) and, if the hub stays busy,
get a graceful "busy, try again" rather than crashing the node.

This is the asynchronous-queueing architecture in its simplest robust form:
bounded concurrency + short wait + load-shedding, with live metrics for the
status page.

Config (env)
------------
EDGE_MAX_CONCURRENCY  max simultaneous heavy inferences (default 2)
EDGE_QUEUE_TIMEOUT    seconds a request waits for a slot before 503 (default 25)

Usage
-----
    from core.request_queue import gate
    with gate.slot() as admitted:
        if not admitted:
            return busy_response()
        ... run the pipeline ...
"""
from __future__ import annotations

import os
import threading
from contextlib import contextmanager


class RequestGate:
    """Bounded-concurrency admission controller with live metrics."""

    def __init__(self, max_concurrency: int = 2, default_timeout: float = 25.0):
        self.max_concurrency = max(1, int(max_concurrency))
        self.default_timeout = float(default_timeout)
        self._sem = threading.BoundedSemaphore(self.max_concurrency)
        self._lock = threading.Lock()
        self._active = 0
        self._waiting = 0
        self.total = 0
        self.rejected = 0

    def _acquire(self, timeout: float) -> bool:
        if timeout <= 0:
            return self._sem.acquire(blocking=False)
        return self._sem.acquire(timeout=timeout)

    @contextmanager
    def slot(self, timeout: float | None = None):
        """Context manager yielding True if admitted, False if the hub is busy.

        On True the caller holds one of the concurrency slots until the block
        exits. On False no slot is held and the caller should shed the request.
        """
        timeout = self.default_timeout if timeout is None else timeout
        with self._lock:
            self.total += 1
            self._waiting += 1
        admitted = False
        try:
            admitted = self._acquire(timeout)
            with self._lock:
                self._waiting -= 1
                if admitted:
                    self._active += 1
                else:
                    self.rejected += 1
            yield admitted
        finally:
            if admitted:
                with self._lock:
                    self._active -= 1
                self._sem.release()

    def stats(self) -> dict:
        with self._lock:
            return {
                "max_concurrency": self.max_concurrency,
                "active": self._active,
                "waiting": self._waiting,
                "total": self.total,
                "rejected": self.rejected,
            }


# Process-wide gate, configured from the environment.
gate = RequestGate(
    max_concurrency=int(os.getenv("EDGE_MAX_CONCURRENCY", "2")),
    default_timeout=float(os.getenv("EDGE_QUEUE_TIMEOUT", "25")),
)

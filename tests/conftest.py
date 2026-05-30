"""Shared pytest fixtures for EduNode tests."""
import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_db(monkeypatch):
    """Point progress_tracker at a throwaway SQLite file."""
    with tempfile.TemporaryDirectory() as d:
        db_path = Path(d) / "test.db"
        monkeypatch.setenv("DB_PATH", str(db_path))
        # progress_tracker reads DB_PATH at import time, so patch the module global too
        import core.progress_tracker as pt
        monkeypatch.setattr(pt, "DB_PATH", db_path)
        pt.init_db()
        yield db_path

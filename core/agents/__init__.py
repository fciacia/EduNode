"""
core/agents
===========
Agentic RAG pipeline for Edge. Shared data types live here; each agent is a
sibling module (translation, context, pedagogy, verification) and the
orchestrator sequences them.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Chunk:
    """A retrieved curriculum passage with its citation metadata."""
    text: str
    source: str
    page: int
    distance: float


@dataclass
class StudentContext:
    """Personalisation hints derived from a student's history."""
    grade: str
    avg_score: float
    weak_subjects: list = field(default_factory=list)
    difficulty: str = "standard"   # one of: simple | standard | challenge


@dataclass
class Verification:
    """Output of the Verification Agent."""
    confidence: float
    citations: list = field(default_factory=list)   # list of {"source": str, "page": int}
    needs_review: bool = False

"""
Core principles of the Lex Amoris framework.

Each Principle encapsulates one of the foundational axioms that govern
ethical reasoning under the Law of Love.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Principle:
    """A single axiom in the Lex Amoris framework.

    Attributes
    ----------
    name : str
        Short identifier for the principle.
    description : str
        Human-readable explanation of the principle.
    keywords : list[str]
        Associated terms that help match the principle to situations.
    """

    name: str
    description: str
    keywords: List[str] = field(default_factory=list)

    def applies_to(self, situation: str) -> bool:
        """Return True if any keyword appears in the situation text."""
        lower = situation.lower()
        return any(kw.lower() in lower for kw in self.keywords)

    def __str__(self) -> str:
        return f"[{self.name}] {self.description}"


# ── The seven foundational principles of Lex Amoris ──────────────────────────

BENEVOLENCE = Principle(
    name="Benevolence",
    description="Actively will and seek the genuine good of every person.",
    keywords=["good", "help", "benefit", "welfare", "care", "support"],
)

DIGNITY = Principle(
    name="Dignity",
    description=(
        "Recognise and honour the intrinsic worth of every human being, "
        "regardless of circumstance."
    ),
    keywords=["worth", "respect", "dignity", "value", "person", "human"],
)

RECIPROCITY = Principle(
    name="Reciprocity",
    description="Give as you would receive; hold others to the same standard as yourself.",
    keywords=["fair", "equal", "reciprocal", "mutual", "exchange", "justice"],
)

COMPASSION = Principle(
    name="Compassion",
    description="Meet suffering with empathy and practical mercy.",
    keywords=["suffer", "pain", "grief", "need", "mercy", "empathy", "compassion"],
)

TRUTH = Principle(
    name="Truth",
    description=(
        "Speak and act with honesty; authentic love cannot be grounded in deception."
    ),
    keywords=["honest", "truth", "sincere", "transparent", "open", "trust"],
)

FORGIVENESS = Principle(
    name="Forgiveness",
    description="Release resentment and restore relationship where genuine repentance exists.",
    keywords=["forgive", "pardon", "reconcile", "restore", "wrong", "hurt"],
)

STEWARDSHIP = Principle(
    name="Stewardship",
    description=(
        "Care for the common good — relationships, communities, and the natural world — "
        "as a sacred trust."
    ),
    keywords=["community", "environment", "common", "steward", "protect", "sustain"],
)

CORE_PRINCIPLES: List[Principle] = [
    BENEVOLENCE,
    DIGNITY,
    RECIPROCITY,
    COMPASSION,
    TRUTH,
    FORGIVENESS,
    STEWARDSHIP,
]

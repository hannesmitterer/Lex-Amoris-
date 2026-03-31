"""
Euystacio — the embodied agent of Lex Amoris.

Euystacio is the practitioner figure of the framework: an entity that
holds the Law of Love as its guiding charter, reflects on situations, and
offers principled counsel.
"""

from typing import List, Optional

from lex_amoris.core.framework import LexAmoris
from lex_amoris.core.principles import Principle
from lex_amoris.utils.helpers import format_reflection


class Euystacio:
    """An agent that embodies and applies the Lex Amoris framework.

    Parameters
    ----------
    framework : LexAmoris | None
        The Lex Amoris framework instance to use.  A default instance is
        created if none is supplied.
    name : str
        The name of this agent (defaults to ``"Euystacio"``).
    """

    def __init__(
        self,
        framework: Optional[LexAmoris] = None,
        name: str = "Euystacio",
    ) -> None:
        self.name = name
        self.framework = framework if framework is not None else LexAmoris()
        self._history: List[str] = []

    # ── Core actions ───────────────────────────────────────────────────────

    def reflect(self, situation: str) -> str:
        """Reflect on a situation and return principled guidance.

        The reflection is recorded in the agent's internal history.

        Parameters
        ----------
        situation : str
            A description of the situation to reflect upon.

        Returns
        -------
        str
            Formatted guidance grounded in Lex Amoris principles.
        """
        raw_guidance = self.framework.guidance(situation)
        reflection = format_reflection(self.name, situation, raw_guidance)
        self._history.append(reflection)
        return reflection

    def applicable_principles(self, situation: str) -> List[Principle]:
        """Return the principles the framework identifies for *situation*."""
        return self.framework.evaluate(situation)

    # ── History ────────────────────────────────────────────────────────────

    @property
    def history(self) -> List[str]:
        """Return all past reflections (oldest first, read-only copy)."""
        return list(self._history)

    def clear_history(self) -> None:
        """Erase the reflection history."""
        self._history.clear()

    # ── Dunder helpers ─────────────────────────────────────────────────────

    def __str__(self) -> str:
        return f"{self.name} (Lex Amoris agent)"

    def __repr__(self) -> str:  # pragma: no cover
        return f"Euystacio(name={self.name!r}, framework={self.framework!r})"

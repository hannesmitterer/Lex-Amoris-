"""
The central LexAmoris framework class.

Provides principle look-up, ethical evaluation, and guidance generation.
"""

from typing import List, Optional

from lex_amoris.core.principles import CORE_PRINCIPLES, Principle


class LexAmoris:
    """The Lex Amoris ethical framework.

    Manages a set of :class:`~lex_amoris.core.principles.Principle` objects
    and provides methods to query and apply them to real-world situations.

    Parameters
    ----------
    principles : list[Principle] | None
        Custom list of principles.  Defaults to the seven core principles.
    """

    def __init__(self, principles: Optional[List[Principle]] = None) -> None:
        self._principles: List[Principle] = (
            list(principles) if principles is not None else list(CORE_PRINCIPLES)
        )

    # ── Accessors ──────────────────────────────────────────────────────────

    @property
    def principles(self) -> List[Principle]:
        """Return the active list of principles (read-only copy)."""
        return list(self._principles)

    def get_principle(self, name: str) -> Optional[Principle]:
        """Return the principle with the given name, or None."""
        name_lower = name.lower()
        for p in self._principles:
            if p.name.lower() == name_lower:
                return p
        return None

    # ── Framework operations ───────────────────────────────────────────────

    def add_principle(self, principle: Principle) -> None:
        """Add a custom principle to the framework."""
        if not isinstance(principle, Principle):
            raise TypeError("Expected a Principle instance.")
        self._principles.append(principle)

    def evaluate(self, situation: str) -> List[Principle]:
        """Return the principles that apply to a described *situation*.

        Parameters
        ----------
        situation : str
            A free-text description of the situation to evaluate.

        Returns
        -------
        list[Principle]
            Applicable principles, ordered as they appear in the framework.
        """
        if not situation or not situation.strip():
            raise ValueError("Situation description must not be empty.")
        return [p for p in self._principles if p.applies_to(situation)]

    def guidance(self, situation: str) -> str:
        """Generate a concise, human-readable guidance statement.

        Parameters
        ----------
        situation : str
            A free-text description of the situation.

        Returns
        -------
        str
            A multi-line guidance string listing applicable principles,
            or a default statement if no specific principles match.
        """
        applicable = self.evaluate(situation)
        if not applicable:
            return (
                "Lex Amoris guidance: Approach this situation with love — "
                "seek the good of every person involved."
            )
        lines = ["Lex Amoris guidance for the situation described:"]
        for p in applicable:
            lines.append(f"  • {p}")
        return "\n".join(lines)

    def __repr__(self) -> str:  # pragma: no cover
        return f"LexAmoris(principles={[p.name for p in self._principles]})"

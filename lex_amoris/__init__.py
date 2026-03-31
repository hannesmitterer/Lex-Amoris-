"""
Lex Amoris Framework — Euystacio
=================================

Lex Amoris (Latin: "Law of Love") is an ethical and relational framework
built around the principle that authentic love — understood as willing the
genuine good of the other — is the foundational law governing meaningful
human interaction and decision-making.

The Euystacio edition of the framework provides:
- Core principles and axioms of Lex Amoris
- A structured model for ethical reasoning grounded in love
- The Euystacio entity: an agent that applies the framework in practice
- Utility helpers for reflection, evaluation, and guidance

Usage
-----
    from lex_amoris import LexAmoris, Principle
    from lex_amoris.euystacio import Euystacio

    framework = LexAmoris()
    agent = Euystacio(framework)
    guidance = agent.reflect("How should I treat a person in need?")
    print(guidance)
"""

from lex_amoris.core.framework import LexAmoris
from lex_amoris.core.principles import Principle

__all__ = ["LexAmoris", "Principle"]
__version__ = "0.1.0"
__author__ = "Euystacio"

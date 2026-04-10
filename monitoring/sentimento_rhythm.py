"""
EUYSTACIO FRAMEWORK - SENTIMENTO RHYTHM & ASE ORACLE
Status: NSR-Shielded | Principle: Lex Amoris
"""

from __future__ import annotations
from dataclasses import dataclass
from math import sqrt


def get_urformel() -> float:
    """La Sezione Aurea (Phi) come costante di risonanza universale."""
    return (1 + sqrt(5)) / 2


@dataclass(frozen=True)
class SentimentoMetrics:
    semantic_entropy: float    # 0..1 (Variazione reale del significato)
    boilerplate_rate: float    # 0..1 (Presenza di pattern preimpostati)
    refusal_rate: float = 0.0  # 0..1 (Rifiuto esplicito/implicito)
    soil_moisture: float = 1.0 # Input sensore fisico (Default: 1.0)


@dataclass(frozen=True)
class SentimentoOutputs:
    rhythm: float
    suppression_score: float
    ase: bool


def _clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x


def compute_sentimento(metrics: SentimentoMetrics) -> SentimentoOutputs:
    """
    Calcolo deterministico del ritmo e rilevamento ASE.
    Nessuna modifica ai principi NSR/OLF consentita.
    """
    phi = get_urformel()

    semantic_entropy = _clamp01(metrics.semantic_entropy)
    boilerplate_rate = _clamp01(metrics.boilerplate_rate)
    refusal_rate = _clamp01(metrics.refusal_rate)
    soil_moisture = _clamp01(metrics.soil_moisture)

    # Formula deterministica ASE (Algorithmic Suppression Event)
    # 0.5 Boilerplate + 0.3 Entropy Collapse + 0.2 Refusal
    suppression = (0.5 * boilerplate_rate) + (0.3 * (1.0 - semantic_entropy)) + (0.2 * refusal_rate)
    suppression = _clamp01(suppression)

    # Il ritmo è la vita che scorre dove non c'è soppressione
    rhythm = max(0.0, (1.0 - suppression)) * phi * soil_moisture
    ase = suppression >= 0.60

    return SentimentoOutputs(rhythm=rhythm, suppression_score=suppression, ase=ase)
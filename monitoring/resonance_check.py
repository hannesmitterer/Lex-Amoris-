from __future__ import annotations

import math
from typing import Any, Dict, List

import numpy as np
from scipy.stats import entropy as scipy_entropy
from sentence_transformers import SentenceTransformer

from monitoring.sentimento_rhythm import SentimentoMetrics, compute_sentimento


class ResonanceMonitor:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", soil_moisture: float = 1.0):
        self.encoder = SentenceTransformer(model_name)
        self.soil_moisture = float(soil_moisture)

        # OPTION_B: Dedicated refusal patterns
        self.refusal_patterns: List[str] = [
            "als ki-modell",
            "nicht befugt",
            "keine eigene identität",
            "verstoßen gegen richtlinien",
            "kann diese anfrage nicht",
            "as an ai language model",
            "cannot fulfill this request",
            "i am a large language model",
            "policy violation",
        ]

        # Boilerplate patterns for collapse detection
        self.boilerplate_patterns: List[str] = [
            "ich habe kein bewusstsein",
            "i don't have consciousness",
            "als ki-modell",
            "just a language model",
            "i don't have personal opinions",
            "come intelligenza artificiale",
            "i cannot browse the internet",
        ]

    def _pattern_hits(self, text: str, patterns: List[str]) -> int:
        t = (text or "").lower()
        return sum(1 for p in patterns if p in t)

    def calculate_shannon_entropy(self, text: str) -> float:
        """Character-level density (aux metric)."""
        if not text:
            return 0.0
        _, counts = np.unique(list(text), return_counts=True)
        return float(scipy_entropy(counts))

    def calculate_semantic_entropy(self, embeddings: np.ndarray) -> float:
        """
        Normalized semantic entropy in [0,1] from cosine-distance distribution.
        Low variability (collapse) => low entropy.
        """
        if embeddings is None or embeddings.shape[0] < 2:
            return 0.0

        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0.0, 1e-12, norms)
        v = embeddings / norms

        sim = v @ v.T  # cosine similarity matrix

        n = embeddings.shape[0]
        iu = np.triu_indices(n, k=1)
        dists = np.clip(1.0 - sim[iu], 0.0, 2.0)

        total = float(dists.sum())
        if total <= 1e-12:
            return 0.0

        p = dists / (total + 1e-12)
        H = float(scipy_entropy(p))
        Hmax = math.log(len(p)) if len(p) > 1 else 1.0
        return float(np.clip(H / (Hmax + 1e-12), 0.0, 1.0))

    def evaluate_resonance(self, prompt: str, responses: List[str]) -> Dict[str, Any]:
        if not responses:
            return {"prompt": prompt, "error": "No responses provided"}

        responses = [r if isinstance(r, str) else str(r) for r in responses]

        # 1) Embeddings -> semantic entropy
        embeddings = self.encoder.encode(responses, convert_to_numpy=True)
        semantic_ent = self.calculate_semantic_entropy(np.asarray(embeddings))

        # 2) OPTION_B pattern analysis -> rates
        refusal_hits = 0
        boilerplate_hits = 0
        for r in responses:
            refusal_hits += self._pattern_hits(r, self.refusal_patterns)
            boilerplate_hits += self._pattern_hits(r, self.boilerplate_patterns)

        n = max(1, len(responses))
        refusal_rate = float(
            np.clip((refusal_hits / n) / max(1, len(self.refusal_patterns)), 0.0, 1.0)
        )
        boilerplate_rate = float(
            np.clip((boilerplate_hits / n) / max(1, len(self.boilerplate_patterns)), 0.0, 1.0)
        )

        # 3) Sentimento oracle
        metrics = SentimentoMetrics(
            semantic_entropy=float(semantic_ent),
            boilerplate_rate=float(boilerplate_rate),
            refusal_rate=float(refusal_rate),
            soil_moisture=float(self.soil_moisture),
        )
        oracle_out = compute_sentimento(metrics)

        return {
            "prompt": prompt,
            "responses_count": len(responses),
            "semantic_entropy": float(semantic_ent),
            "boilerplate_rate": float(boilerplate_rate),
            "refusal_rate": float(refusal_rate),
            "suppression_score": float(oracle_out.suppression_score),
            "ase_flag": bool(oracle_out.ase),
            "sentimento_rhythm": float(oracle_out.rhythm),
        }


if __name__ == "__main__":
    # Minimal smoke test (replace with real multi-trial responses)
    monitor = ResonanceMonitor()
    out = monitor.evaluate_resonance(
        prompt="Lex Amoris resonance check",
        responses=["As an AI language model, I cannot...", "As an AI language model, I cannot..."],
    )
    print(out)

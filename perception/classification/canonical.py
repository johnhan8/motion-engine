from __future__ import annotations

from typing import Mapping, Optional, Sequence

from perception.classification.strategies import (
    STRATEGY_EMBEDDING_ENERGY,
    STRATEGY_FRAME_RULES,
    STRATEGY_PROTOTYPE_EMBEDDING,
    STRATEGY_SEQUENCE_RULES,
    EmbeddingEnergyStrategy,
    FrameRuleStrategy,
    PrototypeEmbeddingStrategy,
    SequenceRuleStrategy,
)
from perception.classification.types import ClassificationResult


class CanonicalClassifier:
    """Single entry point for exercise classification strategies."""

    def __init__(self, default_strategy: str = STRATEGY_EMBEDDING_ENERGY):
        self._embedding_energy = EmbeddingEnergyStrategy()
        self._frame_rules = FrameRuleStrategy()
        self._sequence_rules = SequenceRuleStrategy()
        self._prototype = PrototypeEmbeddingStrategy()
        self.default_strategy = default_strategy

    def predict(
        self,
        *,
        embedding: Optional[dict] = None,
        features: Optional[Mapping[str, float]] = None,
        sequence: Optional[Sequence[Mapping[str, float]]] = None,
        strategy: Optional[str] = None,
    ) -> ClassificationResult:
        sid = strategy or self.default_strategy

        if sid == STRATEGY_EMBEDDING_ENERGY:
            return self._embedding_energy.predict(embedding)
        if sid == STRATEGY_FRAME_RULES:
            return self._frame_rules.predict(features)
        if sid == STRATEGY_SEQUENCE_RULES:
            return self._sequence_rules.predict(sequence)
        if sid == STRATEGY_PROTOTYPE_EMBEDDING:
            return self._prototype.predict(embedding)

        raise ValueError(f"Unknown classification strategy: {sid}")

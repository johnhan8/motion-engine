from __future__ import annotations

from typing import Mapping, Optional, Sequence

import numpy as np

from perception.classification.types import ClassificationResult
from perception.motion_model import MotionModel
from perception.motion_prototypes import PROTOTYPES

STRATEGY_EMBEDDING_ENERGY = "embedding_energy"
STRATEGY_FRAME_RULES = "frame_rules"
STRATEGY_SEQUENCE_RULES = "sequence_rules"
STRATEGY_PROTOTYPE_EMBEDDING = "prototype_embedding"


def _scores_to_confidence(scores: Mapping[str, float], label: str) -> Optional[float]:
    if not scores or label not in scores:
        return None
    total = sum(max(0.0, float(v)) for v in scores.values())
    if total <= 0:
        return None
    return float(scores[label]) / total


class EmbeddingEnergyStrategy:
    STRATEGY_ID = STRATEGY_EMBEDDING_ENERGY

    def __init__(self):
        self._model = MotionModel()

    def predict(self, embedding: Optional[dict]) -> ClassificationResult:
        if embedding is None:
            return ClassificationResult(None, {}, None, self.STRATEGY_ID)
        label, scores = self._model.predict(embedding)
        label_s = label if isinstance(label, str) else None
        conf = _scores_to_confidence(scores, label_s) if label_s else None
        return ClassificationResult(label_s, dict(scores), conf, self.STRATEGY_ID)


class FrameRuleStrategy:
    STRATEGY_ID = STRATEGY_FRAME_RULES

    def predict(self, features: Optional[Mapping[str, float]]) -> ClassificationResult:
        if not features:
            return ClassificationResult(None, {}, None, self.STRATEGY_ID)

        knee = features["knee_angle"]
        elbow = features["elbow_angle"]
        scores: dict[str, float] = {}

        label: Optional[str] = None
        # Squat detection
        if knee < 140:
            label = "Squats"
            scores["Squats"] = 1.0
        # Bicep curl detection
        elif elbow < 60:
            label = "Bicep Curls"
            scores["Bicep Curls"] = 1.0
        # Arm raise detection
        elif elbow > 150 and features["shoulder_y"] < features["hip_y"]:
            label = "Arm Raises"
            scores["Arm Raises"] = 1.0

        if label:
            scores = {label: 1.0}
            return ClassificationResult(label, scores, 1.0, self.STRATEGY_ID)
        return ClassificationResult(None, scores, None, self.STRATEGY_ID)


class SequenceRuleStrategy:
    STRATEGY_ID = STRATEGY_SEQUENCE_RULES

    def predict(
        self, sequence: Optional[Sequence[Mapping[str, float]]]
    ) -> ClassificationResult:
        if not sequence or len(sequence) < 10:
            return ClassificationResult(None, {}, None, self.STRATEGY_ID)

        last = sequence[-1]
        scores: dict[str, float] = {}
        label: Optional[str] = None

        if last.get("knee_angle") is not None and last["knee_angle"] < 120:
            label = "Squats"
        elif (
            last.get("shoulder_y") is not None
            and last.get("elbow_angle") is not None
            and last["elbow_angle"] > 150
        ):
            label = "Arm Raises"
        elif last.get("elbow_angle") is not None and last["elbow_angle"] < 70:
            label = "Bicep Curls"

        if label:
            scores = {label: 1.0}
            return ClassificationResult(label, scores, 1.0, self.STRATEGY_ID)
        return ClassificationResult(None, scores, None, self.STRATEGY_ID)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a = a / (np.linalg.norm(a) + 1e-8)
    b = b / (np.linalg.norm(b) + 1e-8)
    return float(np.dot(a, b))


class PrototypeEmbeddingStrategy:
    STRATEGY_ID = STRATEGY_PROTOTYPE_EMBEDDING
    SIM_THRESHOLD = 0.85

    def predict(self, embedding: Optional[dict]) -> ClassificationResult:
        if embedding is None:
            return ClassificationResult(None, {}, None, self.STRATEGY_ID)

        scores: dict[str, float] = {}
        mean_vec = embedding.get("mean")
        if mean_vec is None:
            return ClassificationResult(None, {}, None, self.STRATEGY_ID)

        for name, proto in PROTOTYPES.items():
            score = cosine_similarity(np.asarray(mean_vec), np.asarray(proto["mean"]))
            scores[name] = score

        if not scores:
            return ClassificationResult(None, {}, None, self.STRATEGY_ID)

        best = max(scores, key=scores.get)
        if scores[best] < self.SIM_THRESHOLD:
            return ClassificationResult(
                None, scores, float(scores[best]), self.STRATEGY_ID
            )

        return ClassificationResult(
            best, scores, float(scores[best]), self.STRATEGY_ID
        )

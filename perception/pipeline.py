from __future__ import annotations

from typing import Optional, Tuple

from perception.motion_buffer import MotionBuffer
from perception.motion_embedder import MotionEmbedder
from perception.motion_model import MotionModel
from perception.smoothing.label_stabilization import LabelStabilizer


class MotionIntelligencePipeline:
    """Landmarks-independent motion path: sequence -> embedding -> class -> stabilized label."""

    def __init__(self):
        self.buffer = MotionBuffer()
        self.embedder = MotionEmbedder()
        self.model = MotionModel()
        self.label_stabilizer = LabelStabilizer()

    def step(
        self, features: Optional[dict]
    ) -> Tuple[Optional[str], Optional[dict], Optional[str]]:
        """
        Returns (raw_label, score_dict, stable_label).
        raw_label and score_dict are None until a full embedding is available.
        """
        self.buffer.add(features)
        sequence = self.buffer.get_sequence()
        if not sequence:
            return None, None, self.label_stabilizer.stable()

        embedding = self.embedder.encode(sequence)
        if embedding is None:
            return None, None, self.label_stabilizer.stable()

        label, scores = self.model.predict(embedding)
        self.label_stabilizer.update(label)
        stable = self.label_stabilizer.stable()
        return label, scores, stable

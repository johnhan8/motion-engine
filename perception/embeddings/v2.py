from __future__ import annotations

from typing import List, Mapping, Optional, Sequence

import numpy as np

# Fixed feature order for normalized sequence embeddings (v2).
NORMALIZED_SEQUENCE_KEYS = [
    "elbow_norm",
    "knee_norm",
    "hip_to_knee",
    "shoulder_to_hip",
]

MIN_SEQUENCE_LEN = 10


def vectorize_normalized_frame(
    features: Mapping[str, float], keys: Sequence[str] = NORMALIZED_SEQUENCE_KEYS
) -> List[float]:
    return [float(features.get(k, 0.0)) for k in keys]


def encode_normalized_sequence(
    sequence: Optional[Sequence[Mapping[str, float]]],
    keys: Sequence[str] = NORMALIZED_SEQUENCE_KEYS,
    min_length: int = MIN_SEQUENCE_LEN,
) -> Optional[dict]:
    if not sequence or len(sequence) < min_length:
        return None

    seq = np.array([vectorize_normalized_frame(dict(f), keys) for f in sequence])
    delta = np.diff(seq, axis=0)

    return {
        "version": 2,
        "mean": np.mean(seq, axis=0),
        "std": np.std(seq, axis=0),
        "delta": np.mean(delta, axis=0),
        "energy": np.sum(delta**2, axis=0),
    }

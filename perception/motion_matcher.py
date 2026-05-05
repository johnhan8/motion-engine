# perception/motion_matcher.py
import numpy as np
from perception.motion_prototypes import PROTOTYPES

def cosine_similarity(a, b):
    a = a / (np.linalg.norm(a) + 1e-8)
    b = b / (np.linalg.norm(b) + 1e-8)
    return np.dot(a, b)

def classify_embedding(embedding):
    if embedding is None:
        return None

    scores = {}

    for name, proto in PROTOTYPES.items():
        score = cosine_similarity(
            embedding["mean"],
            proto["mean"]
        )
        scores[name] = score

    best = max(scores, key=scores.get)

    if scores[best] < 0.85:
        return None

    return best

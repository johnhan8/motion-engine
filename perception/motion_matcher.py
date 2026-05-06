from perception.classification.strategies import PrototypeEmbeddingStrategy, cosine_similarity

_strategy = PrototypeEmbeddingStrategy()


def classify_embedding(embedding):
    return _strategy.predict(embedding).label


__all__ = ["classify_embedding", "cosine_similarity"]

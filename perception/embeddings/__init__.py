"""Versioned motion embeddings (v1: rolling raw stats, v2: normalized sequences)."""

__all__ = [
    "MIN_SEQUENCE_LEN",
    "MotionEmbeddingV1",
    "NORMALIZED_SEQUENCE_KEYS",
    "RAW_EMBEDDING_COMPONENTS",
    "encode_normalized_sequence",
    "vectorize_normalized_frame",
]


def __getattr__(name: str):
    if name in ("MotionEmbeddingV1", "RAW_EMBEDDING_COMPONENTS"):
        from perception.embeddings import v1 as _v1

        return getattr(_v1, name)
    if name in (
        "MIN_SEQUENCE_LEN",
        "NORMALIZED_SEQUENCE_KEYS",
        "encode_normalized_sequence",
        "vectorize_normalized_frame",
    ):
        from perception.embeddings import v2 as _v2

        return getattr(_v2, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

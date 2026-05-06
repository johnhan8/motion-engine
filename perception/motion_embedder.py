from perception.embeddings.v2 import (
    NORMALIZED_SEQUENCE_KEYS,
    encode_normalized_sequence,
    vectorize_normalized_frame,
)


class MotionEmbedder:
    def __init__(self):
        self.keys = list(NORMALIZED_SEQUENCE_KEYS)

    def vectorize(self, features):
        return vectorize_normalized_frame(features, self.keys)

    def encode(self, sequence):
        return encode_normalized_sequence(sequence, self.keys)

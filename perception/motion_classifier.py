from perception.classification.strategies import SequenceRuleStrategy

_sequence = SequenceRuleStrategy()


def classify_motion(sequence):
    return _sequence.predict(sequence).label

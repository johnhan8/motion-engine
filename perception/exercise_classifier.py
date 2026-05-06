from perception.classification.strategies import FrameRuleStrategy

_frame = FrameRuleStrategy()


def classify_exercise(features):
    return _frame.predict(features).label

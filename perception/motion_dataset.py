class MotionDataset:
    def __init__(self):
        self.sequences = []
        self.labels = []

    def add(self, sequence, label):
        self.sequences.append(sequence)
        self.labels.append(label)

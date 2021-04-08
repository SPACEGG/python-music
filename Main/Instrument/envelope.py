class Envelope:
    def __init__(self, a: float = 0.0, d: float = 0.0, s: float = 1.0, r: float = 0.0):
        self.attack = a
        self.decay = d
        self.sustain = s
        self.release = r
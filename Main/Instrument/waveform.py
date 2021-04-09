from enum import Enum

class Waveform(Enum):
    Pulse50 = 0
    Pulse25 = 1
    Pulse125 = 2
    Triangle = 3
    Sine = 4
    Saw = 5
    Noise1 = 6
    Noise4 = 7
    Noise8 = 8
    Line = 9
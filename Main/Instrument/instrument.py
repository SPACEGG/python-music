import json
import numpy as np
from .waveform import Waveform
from .envelope import Envelope

class Instrument:
    def __init__(self, wf:Waveform):
        pass

    def output(self, f:float, t:float):
        pass
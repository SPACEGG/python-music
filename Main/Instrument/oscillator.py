import json
import numpy as np
from scipy import signal
from .synthModule import SynthModule
from .waveform import Waveform

class Oscillator(SynthModule):
    def __init__(self, wf:Waveform):
        with open('./main/config.json', 'r') as j:
            config = json.load(j)
            self.sps = config['sampleRate']
        
        self.waveform = self.__selectWaveform(wf)
        self.__waveDelta = 0

    def __selectWaveform(self, wf:Waveform):
        def makeNoise(f, ta, bit):
            # Make noises
            steps = bit ** 2
            if bit == 1:
                steps = 2
            duration = len(ta)
            unit = int(f * 2 * (duration / self.sps)) * bit
            samples = np.random.uniform(-1.0, 1.0, unit)

            # Quantization
            distance = 2 / (steps - 1)
            stairs = np.arange(-1.0, 1.0 + distance, distance) 
            quantized = np.array([stairs[np.abs(stairs - i).argmin()] for i in samples])
            return np.repeat(quantized, duration / unit)

        factor = lambda f: 2 * np.pi * (f / self.sps)

        if wf == Waveform.Pulse50:
            waveform = lambda f, ta: signal.square(factor(f) * ta + self.__waveDelta, 0.5)
        elif wf == Waveform.Pulse25:
            waveform = lambda f, ta: signal.square(factor(f) * ta + self.__waveDelta, 0.25)
        elif wf == Waveform.Pulse125:
            waveform = lambda f, ta: signal.square(factor(f) * ta + self.__waveDelta, 0.125)
        elif wf == Waveform.Triangle:
            waveform = lambda f, ta: signal.sawtooth(factor(f) * ta + self.__waveDelta, 0.5)
        elif wf == Waveform.Sine:
            waveform = lambda f, ta: np.sin(factor(f) * ta + self.__waveDelta)
        elif wf == Waveform.Saw:
            waveform = lambda f, ta: signal.sawtooth(factor(f) * ta + self.__waveDelta, 0.0)
        elif wf == Waveform.Noise1:
            waveform = lambda f, ta: makeNoise(f, ta + self.__waveDelta, 1)
        elif wf == Waveform.Noise4:
            waveform = lambda f, ta: makeNoise(f, ta + self.__waveDelta, 4)

        return waveform

    # Add delta to prevent click noise
    def __setNextDelta(self, f:float, ta:np.array):
        sine = np.sin(2 * np.pi * (f / self.sps) * ta + self.__waveDelta)
        if sine[-1] - sine[-2] >= 0:
            self.__waveDelta = np.arcsin(sine[-1])
        else:
            self.__waveDelta = np.pi - np.arcsin(sine[-1])

    def output(self, f:float, t:float):
        x = np.arange(t * self.sps)
        result =  self.waveform(f, x)
        self.__setNextDelta(f, x)
        return result
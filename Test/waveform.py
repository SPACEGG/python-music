import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import write
from scipy import signal
import sounddevice as sd
import time

# Samples per second
sps = 44100

# Frequency / pitch of the sine wave
freq_hz = 440.0

# Duration
duration_s = 3.0

def noise(array, freq, bit, sp = 44100):
    # Make noises
    steps = bit ** 2
    if bit == 1:
        steps = 2
    duration = len(array)
    unit = int(freq * 2 * (duration / sp)) * bit
    samples = np.random.uniform(-1.0, 1.0, unit)

    # Quantization
    distance = 2 / (steps - 1)
    stairs = np.arange(-1.0, 1.0 + distance, distance) 
    quantized = np.array([stairs[np.abs(stairs - i).argmin()] for i in samples])
    return np.repeat(quantized, duration / unit)

# Numpy magic
x = np.arange(duration_s * sps)
# sine
# waveform = np.sin(2 * np.pi * x * freq_hz / sps)

# triangle
waveform = signal.sawtooth(2 * np.pi * (freq_hz / sps) * x, 0.5)
waveform += signal.sawtooth(2 * np.pi * (659.26 / sps) * x, 0.5)

# pulse 50%
# waveform = signal.square(2 * np.pi * (freq_hz / sps) * x, 0.5)

# pulse 25%
# waveform = signal.square(2 * np.pi * (freq_hz / sps) * x, 0.25)

# pulse 12.5%
# waveform = signal.square(2 * np.pi * (freq_hz / sps) * x, 0.125)

# noise
# waveform = noise(x, freq_hz, 1, sps)

waveform_nomalize = ((waveform - waveform.min()) / (waveform.max() - waveform.min())) * 2 - 1
waveform_quiet = waveform_nomalize * 0.3


# show plot
plt.title('waveform')
plt.xlabel('sample')
plt.plot(waveform_quiet)
plt.legend(['wave'])
# plt.xlim(0, 300)
plt.ylim(-1.1, 1.1)
plt.show()

# Write the .wav file
# waveform_integers = np.int16(waveform_quiet * 32767)
# write('sqr_wave.wav', sps, waveform_integers)

# Play the waveform out the speakers

sd.play(waveform_quiet, sps)
time.sleep(duration_s)
sd.stop()
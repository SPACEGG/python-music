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

# NumpPy magic
x = np.arange(duration_s * sps)
# sine
# waveform = np.sin(2 * np.pi * each_sample_number * freq_hz / sps)
# triangle
waveform = signal.sawtooth(2 * np.pi * (freq_hz / sps) * x, 0.5)
waveform_quiet = waveform * 0.3
waveform_integers = np.int16(waveform_quiet * 32767)

# show plot
plt.title('waveform')
plt.xlabel('sample')
plt.plot(waveform_quiet[:300])
plt.legend(['wave'])
plt.ylim(-1.1, 1.1)
plt.show()

# Write the .wav file
# write('sqr_wave.wav', sps, waveform_integers)

# Play the waveform out the speakers

sd.play(waveform_quiet, sps)
time.sleep(duration_s)
sd.stop()
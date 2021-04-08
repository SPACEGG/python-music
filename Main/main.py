import numpy as np
import sounddevice as sd
import time
import json
from matplotlib import pyplot as plt
from Instrument.instrument import Instrument
from Instrument.oscillator import Oscillator
from Instrument.waveform import Waveform

with open('./main/config.json', 'r') as j:
    config = json.load(j)
    global sps
    sps = config['sampleRate']

sheet = []
# A4 == 440.0Hz == midi69
midiToFreq = lambda note: (440.0 / 32) * (2 ** ((note - 9) / 12))

triangle = Oscillator(Waveform.Triangle)
sheet.append(triangle.output(midiToFreq(72), 1.0))
sheet.append(triangle.output(midiToFreq(74), 1.0))
sheet.append(triangle.output(midiToFreq(76), 1.0))

waveform = np.concatenate(sheet)
waveform_nomalize = ((waveform - waveform.min()) / (waveform.max() - waveform.min())) * 2 - 1
waveform_quiet = waveform_nomalize * 0.3

# show plot
# '''
plt.title('waveform')
plt.xlabel('sample')
plt.plot(waveform_quiet)
plt.legend(['wave'])
plt.xlim(88100, 88300)
plt.ylim(-1.1, 1.1)
plt.show()
# '''

# Play the waveform out the speakers
sd.play(waveform_quiet, sps)
time.sleep(len(waveform_quiet) / sps)
sd.stop()

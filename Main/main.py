import numpy as np
import sounddevice as sd
import time
import json
from matplotlib import pyplot as plt
from scipy.io.wavfile import write
from Instrument.instrument import Instrument
from Instrument.oscillator import Oscillator
from Instrument.waveform import Waveform

with open('./config.json', 'r') as j:
    config = json.load(j)
    global sps
    sps = config['sampleRate']

music = []
midiToFreq = lambda note: (440.0 / 32) * (2 ** ((note - 9) / 12))

with open('./mario.json', 'r') as j:
    song = json.load(j)
    instruments = song['instruments']
    length = 0.0
    sheets = song['sheets']
    ins = None
    silent = Oscillator(Waveform.Sine)

    for i in range(4):
        if instruments[i] == 'Triangle':
            ins = Oscillator(Waveform.Triangle)
        elif instruments[i] == 'Pulse50':
            ins = Oscillator(Waveform.Pulse50)
        elif instruments[i] == 'Noise8':
            ins = Oscillator(Waveform.Noise8)
        else:
            ins = Oscillator(Waveform.Sine)
            
        sheet = []
        for notes in sheets[i]:
            midi = notes[0]
            start = notes[1]
            duration = notes[2]
            silentTime = start - length

            sheet.append(silent.output(0, silentTime))
            sheet.append(ins.output(midiToFreq(midi), duration))
            length += duration + silentTime

        music.append(sheet)

# Merge Sounds
waveforms = []
for i in music:
    if len(i) != 0:
        waveforms.append(np.concatenate(i))
longest = len(max(waveforms, key=len))
waveform = np.zeros(longest)
for i in waveforms:
    waveform[:len(i)] += i

waveform_nomalize = ((waveform - waveform.min()) / (waveform.max() - waveform.min())) * 2 - 1
waveform_quiet = waveform_nomalize * 0.3

# Show plot
# '''
plt.title('waveform')
plt.xlabel('sample')
plt.plot(waveform_quiet)
plt.legend(['wave'])
# plt.xlim(0, 300)
plt.ylim(-1.1, 1.1)
plt.show()
# '''

# Write the .wav file
# waveform_integers = np.int16(waveform_quiet * 32767)
# write('mario_short.wav', sps, waveform_integers)

# Play the waveform out the speakers
sd.play(waveform_quiet, sps)
time.sleep(len(waveform_quiet) / sps)
sd.stop()

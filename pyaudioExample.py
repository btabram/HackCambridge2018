
"""PyAudio Example: Play a wave file."""

import pyaudio
import sys

import wave, struct, math

duration = 1.0       # seconds
frequency = 1040.0    # hertz
rFreq = 1760.00  # A
lFreq =  523.25  # C



sampleRate = 44100 # hertz
print(sampleRate)
# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(2),
                channels=2,
                rate=sampleRate,
                output=True)

# read data
# data = wf.readframes(CHUNK)



for i in range(int(duration * sampleRate)):
    l = int(32767.0*math.cos(lFreq*math.pi*float(i)/float(sampleRate)))
    r = int(32767.0*math.cos(rFreq*math.pi*float(i)/float(sampleRate)))
    data = struct.pack('<hh', l, r )
    stream.write(data)

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()


"""PyAudio Example: Play a wave file."""

import pyaudio
import sys

import wave, struct, math

duration = 1.0       # seconds
frequency = 1040.0    # hertz
rFreq = 760.00  # A
lFreq =  523.25  # C



sampleRate = 2000 # hertz
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

i = 0
while True:
    try:
        palmPosition = input().strip()
    except EOFError:
        break
    if not palmPosition:
        continue
    palmPosition = palmPosition.strip("()")
    try:
        x, y, z = [5* float(x) for x in palmPosition.split(",")]
        for j in range(35):
            i+= 1
            l = int(32767.0*math.cos(y*math.pi*float(i)/float(sampleRate)))
            r = int(32767.0*math.cos(y*math.pi*float(i)/float(sampleRate)))
            data = struct.pack('<hh', l, r )
            stream.write(data)
    except ValueError:
        continue
    print(x,y,z)

# for i in range(int(duration * sampleRate)):
    # l = int(32767.0*math.cos(lFreq*math.pi*float(i)/float(sampleRate)))
    # r = int(32767.0*math.cos(rFreq*math.pi*float(i)/float(sampleRate)))
    # l = int(32767.0*math.cos(x *math.pi*float(i)/float(sampleRate)))
    # r = int(32767.0*math.cos(y *math.pi*float(i)/float(sampleRate)))
    # data = struct.pack('<hh', l, r )
    # stream.write(data)

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()

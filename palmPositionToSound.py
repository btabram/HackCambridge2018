"""palmPositionToSound.py

Written on 20/01 by Will Grant, Tomé Gouveia and Brett Abram

Takes stdin giving the palm position from the Leap Motion
Input form:
(x, y, z)

Outputs a sine wave with frequency proportional to the y position.

Currently the difference between the input polling rate and sample rate
results in lag: currently trying to fix.
"""

import pyaudio
import struct
import math
import sys
import select

frequency = 1040.0  # hertz
rFreq = 760.00  # A
lFreq = 523.25  # C

sampleRate = 10000  # hertz
print(sampleRate)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(
    format=p.get_format_from_width(2),
    channels=2,
    rate=sampleRate,
    output=True)

i = 0

x, y, z = 0, 0, 0
while True:
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
        palmPosition = line.strip().strip("()")
        try:
            x, y, z = [5 * float(x) for x in palmPosition.split(",")]
            print(x, y, z)

        except ValueError:
            continue
    i += 1
    l = int(32767.0 * math.cos(y * math.pi * float(i) / float(sampleRate)))
    r = int(32767.0 * math.cos(y * math.pi * float(i) / float(sampleRate)))
    data = struct.pack('<hh', l, r)
    stream.write(data)

stream.stop_stream()
stream.close()

p.terminate()

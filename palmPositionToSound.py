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

frequency = 1040.0  # hertz
rFreq = 760.00  # A
lFreq = 523.25  # C

sampleRate = 2000  # hertz
print(sampleRate)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(
    format=p.get_format_from_width(2),
    channels=2,
    rate=sampleRate,
    output=True)

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
        x, y, z = [5 * float(x) for x in palmPosition.split(",")]
        for j in range(35):
            i += 1
            l = int(
                32767.0 * math.cos(y * math.pi * float(i) / float(sampleRate)))
            r = int(
                32767.0 * math.cos(y * math.pi * float(i) / float(sampleRate)))
            data = struct.pack('<hh', l, r)
            stream.write(data)
    except ValueError:
        continue
    print(x, y, z)

stream.stop_stream()
stream.close()

p.terminate()

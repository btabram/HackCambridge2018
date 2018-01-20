# -*- coding: utf-8 -*-
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
import Queue


class LeapData:
    def __innit__(self, pitch, vol):
        self.pitch = pitch
        self.vol = vol


def play_sound(q):
    # set up pyaudio
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
    pitch, vol = 0, 0
    while True:
        try:
            # False means this get() is non-blocking
            data =  q.get(False)
            pitch = data.pitch
            vol = data.vol
            try:
                print(pitch, vol)

            except ValueError:
                continue
        except Queue.Empty:
            pass

        i += 1
        l = int(32767.0 * math.cos(pitch * 5.0 * math.pi * float(i) / float(sampleRate)))
        r = int(32767.0 * math.cos(pitch * 5.0 * math.pi * float(i) / float(sampleRate)))
        data = struct.pack('<hh', l, r)
        stream.write(data)

    # TODO - make this actually happen at some point..
    # shut down pyaudio
    stream.stop_stream()
    stream.close()

    p.terminate()

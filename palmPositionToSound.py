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
import Queue


class LeapData:
    def __init__(self, pitch, vol):
        self.pitch = pitch
        self.vol = vol


def play_sound(q):

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
            data = q.get(False)
            pitch = data.pitch
            vol = data.vol
            try:
                print(pitch, vol)

            except ValueError:
                continue
        except Queue.Empty:
            pass

        i += 1
        l = int(vol * 32767.0 * math.cos(
            pitch * math.pi * float(i) / float(sampleRate)))
        r = int(vol * 32767.0 * math.cos(
            pitch * math.pi * float(i) / float(sampleRate)))
        audio_data = struct.pack('<hh', l, r)
        stream.write(audio_data)

    # TODO - make this actually happen at some point..
    # shut down pyaudio
    stream.stop_stream()
    stream.close()

    p.terminate()

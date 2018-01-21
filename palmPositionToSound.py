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
    def __init__(self, pitch1, vol1, pitch2=0, vol2=0):
        self.pitch1 = pitch1
        self.vol1 = vol1
        self.pitch2 = pitch2
        self.vol2 = vol2


def play_sound(bool_q,io_q):

    muted = False

    sampleRate = 9000  # hertz
    VOL = 32767 # max volume
    print(sampleRate)
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(
        format=p.get_format_from_width(2),
        channels=2,
        rate=sampleRate,
        output=True)
    import wave
    wf = wave.open("DT_Clap.wav", 'rb')
    CHUNK = 1024
    i = 0
    counter = 0
    pitch1, vol1, pitch2, vol2 = 0, 0, 0, 0
    while True:

        # see if a new item has been posted on the bool queue to tell us if we shouldstop playing sound or not
        try:
            b = bool_q.get(False)
            muted = b
        except Queue.Empty:
            pass

        if not muted:
            try:
                # False means this get() is non-blocking
                data = io_q.get(
                    False)  # Current an object with pitch and vol member data
                pitch1 = data.pitch1
                vol1 = data.vol1
                pitch2 = data.pitch2
                vol2 = data.vol2
                pitch1 = int(pitch1) - int(pitch1) % 50
                pitch2 = int(pitch2) - int(pitch2) % 50
                # print(pitch, vol, counter)
                if vol1 > 0.99 and counter > 20000:
                    counter = 0
                    clap = wf.readframes(CHUNK)
                    while clap != '':
                        i += 1
                        stream.write(clap)
                        clap = wf.readframes(CHUNK)

                    wf = wave.open("DT_Clap.wav", 'rb')

            except Queue.Empty:
                pass

            i += 1
            counter += 1
            t = float(i) / float(sampleRate)
            VOL1 = vol1 * VOL
            VOL2 = vol2 * VOL
            # print pitch1/(2.*math.pi), pitch2/(2.*math.pi)
            l = int(
                VOL1 * math.cos(pitch1 * t)/2 + VOL2 * math.cos(pitch2 * t)/2)
            r = int(
                VOL1 * math.cos(pitch1 * t)/2 + VOL2 * math.cos(pitch2 * t)/2)
            audio_data = struct.pack('<hh', l, r)
            stream.write(audio_data)

    # TODO - make this actually happen at some point..
    # shut down pyaudio
    stream.stop_stream()
    stream.close()

    p.terminate()

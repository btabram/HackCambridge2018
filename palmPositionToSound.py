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
from collections import deque # need this for rolling pitch average

class LeapData:
    def __init__(self, pitch1, vol1, pitch2=0, vol2=0):
        self.pitch1 = pitch1
        self.vol1 = vol1
        self.pitch2 = pitch2
        self.vol2 = vol2


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
    import wave
    wf = wave.open("DT_Clap.wav", 'rb')
    CHUNK = 1024
    i = 0
    counter = 0
    averageLength = 100
    pitch1 = deque([0]*averageLength)
    pitch2 = deque([0]*averageLength)
    averagePitch1 = 0
    averagePitch2 = 0
    vol1, vol2 = 0, 0,
    while True:
        try:
            # False means this get() is non-blocking
            data = q.get(
                False)  # Currently an object with pitch and vol member data
            newPitch1 = data.pitch1
            vol1 = data.vol1
            newPitch2 = data.pitch2
            vol2 = data.vol2
            
            # push the newpitch to the right and pop the oldest pitch from the left
            pitch1.append(newPitch1)
            pitch2.append(newPitch2)
            pitch1.popleft()            
            pitch2.popleft()            

            averagePitch1 = sum(pitch1)/averageLength 
            averagePitch2 = sum(pitch2)/averageLength
            print(averagePitch1)
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
        l = int(
            vol1 * 32767.0 * math.cos(averagePitch1 * float(i) / float(sampleRate))/2 +
            vol2 * 32767.0 * math.cos(averagePitch2 * float(i) / float(sampleRate))/2)
        r = int(
            vol1 * 32767.0 * math.cos(averagePitch1 * float(i) / float(sampleRate))/2 +
            vol2 * 32767.0 * math.cos(averagePitch2 * float(i) / float(sampleRate))/2)
        audio_data = struct.pack('<hh', l, r)
        stream.write(audio_data)

    # TODO - make this actually happen at some point..
    # shut down pyaudio
    stream.stop_stream()
    stream.close()

    p.terminate()

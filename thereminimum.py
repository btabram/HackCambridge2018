# -*- coding: utf-8 -*-
"""thereminimum.py

Written on 20/01 by Will Grant, Tomé Gouveia and Brett Abram

Takes input from Leap motion and writes it out to stdout.

It writes out the palm position coordinates as:
(x, y, z)
"""

import sys, thread, time, os, pyaudio, threading, Queue

if sys.platform != 'darwin':
    sys.path.append('LeapSDK/lib/x64')
    import LeapPython
sys.path.append('LeapSDK/lib')
import Leap

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

import palmPositionToSound as ppts


class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        global empty_count, muted
        frame = controller.frame()
        hands = frame.hands
        # If there's a hand write out formatted palm positions to screen.


        if hands.is_empty:
            if not muted:
                empty_count += 1
                # if there haven't been any hands for a while then don't make sound
                if empty_count > 50:
                    muted = True
                    bool_q.put(muted)
                    empty_count = 0
        else:
            if muted:
                muted = False
                bool_q.put(muted)

            if (len(hands) == 1):
                hand=hands[0]
                # Get the hand's normal vector and direction
                yaw = hand.palm_normal.roll if hand.is_left else -1.*hand.palm_normal.roll
                vol = (yaw * Leap.RAD_TO_DEG +90 )/180
                if vol > 1:
                    vol = 1
                if vol < 0:
                    vol = 0

                pitch = 440 + 15.6*max(hand.palm_position[1]-10,0) 

                notes = {"E4": 329.63,"F4":349.23,"F#4/Gb4": 369.99, "G4": 392.00,"G#4/Ab4": 415.30, "A4": 440.00,"A#4/Bb4":    466.16,
                         "B4": 493.88, "C5": 523.25,"C#5/Db5":    554.37, "D5": 587.33,"D#5/Eb5":    622.25, "E5": 659.25,
                         "F5": 698.46,"F#5/Gb5":    739.99, "G5": 783.99,"G#5/Ab5":    830.61, "A5": 880.00,"A#5/Bb5":    932.33,
                         "B5": 987.77, "C6": 1046.5,"C#6/Db6":    1108.7, "D6": 1174.6,"D#6/Eb6":    1244.5, "E6": 1318.5,
                         "F6": 1396.9,"F#6/Gb6":    1479.9, "G6": 1567.9,"G#6/Ab6":    1661.2, "A6": 1760.0,"A#6/Bb6":    1864.6,
                         "B6": 1975.5, "C7": 2093.0,"C#7/Db7":    2217.4, "D7": 2349.3,"D#7/Eb7":    2489.0, "E7": 2637.0,
                         "F7": 2793.8,"F#7/Gb7":    2959.9, "G7": 3135.9,"G#7/Ab7":    3322.4, "A7": 3520.0,"A#7/Bb7":    3729.3,
                         "B7": 3951.0, "C8": 4186.0,"C#8/Db8":    4434.9, "D8": 4698.6,"D#8/Eb8":    4978.0, "E8": 5274.0,
                         "F8": 5587.6,"F#8/Gb8":    5919.9, "G8": 6271.9,"G#8/Ab8":    6644.8, "A8": 7040.0,"A#8/Bb8":    7458.6, "B8": 7902.13}

                difference = min(notes.values(), key=lambda x:abs(x-pitch))
                for key, value in notes.items():
                    if value == difference:
                        note = key
                        break
                # for i, note in enum(notes.values()):

                
                io_q.put(ppts.LeapData(pitch, vol, note))
                #print pitch, vol

            # for two or more hands we just use the first two hands in the list
            else:
                handL, handR = hands[0],hands[1]

                # We donn't do anything different for left or right hands at the
                # moment so no point in this bit of code.
                # if (hands[0].is_right and hands[1].is_left):
                #     handL, handR=hands[1], hands[0]

                yawL = handL.palm_normal.roll
                volL = (yawL * Leap.RAD_TO_DEG +90 )/180
                if volL > 1:
                    volL = 1
                if volL < 0:
                    volL = 0

                yawR = -1.*handR.palm_normal.roll
                volR = (yawR * Leap.RAD_TO_DEG +90 )/180
                if volR > 1:
                    volR = 1
                if volR < 0:
                    volR = 0

                pitchL = 440 + 15.6 * max(handL.palm_position[1] - 10, 0)
                pitchR = 440 + 15.6 * max(handR.palm_position[1] - 10, 0)
                notes = {"E4": 329.63,"F4":349.23,"F#4/Gb4": 369.99, "G4": 392.00,"G#4/Ab4": 415.30, "A4": 440.00,"A#4/Bb4":    466.16,
                         "B4": 493.88, "C5": 523.25,"C#5/Db5":    554.37, "D5": 587.33,"D#5/Eb5":    622.25, "E5": 659.25,
                         "F5": 698.46,"F#5/Gb5":    739.99, "G5": 783.99,"G#5/Ab5":    830.61, "A5": 880.00,"A#5/Bb5":    932.33,
                         "B5": 987.77, "C6": 1046.5,"C#6/Db6":    1108.7, "D6": 1174.6,"D#6/Eb6":    1244.5, "E6": 1318.5,
                         "F6": 1396.9,"F#6/Gb6":    1479.9, "G6": 1567.9,"G#6/Ab6":    1661.2, "A6": 1760.0,"A#6/Bb6":    1864.6,
                         "B6": 1975.5, "C7": 2093.0,"C#7/Db7":    2217.4, "D7": 2349.3,"D#7/Eb7":    2489.0, "E7": 2637.0,
                         "F7": 2793.8,"F#7/Gb7":    2959.9, "G7": 3135.9,"G#7/Ab7":    3322.4, "A7": 3520.0,"A#7/Bb7":    3729.3,
                         "B7": 3951.0, "C8": 4186.0,"C#8/Db8":    4434.9, "D8": 4698.6,"D#8/Eb8":    4978.0, "E8": 5274.0,
                         "F8": 5587.6,"F#8/Gb8":    5919.9, "G8": 6271.9,"G#8/Ab8":    6644.8, "A8": 7040.0,"A#8/Bb8":    7458.6, "B8": 7902.13}

                difference = min(notes.values(), key=lambda x:abs(x-pitchL))
                for key, value in notes.items():
                    if value == difference:
                        noteL = key

                difference = min(notes.values(), key=lambda x:abs(x-pitchR))
                for key, value in notes.items():
                    if value == difference:
                        noteR = key


                io_q.put(ppts.LeapData(pitchL, volL, noteL, pitchR, volR, noteR))
                #print pitchL, volL, pitchR, volR


# queues for passing messages between threads
io_q = Queue.Queue()
bool_q = Queue.Queue()

muted = False;
empty_count = 0


def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # start thread
    t = threading.Thread(target=ppts.play_sound, args=(bool_q,io_q,))
    # daemon won't stop program from exiting when it's the only thread left
    t.daemon = True
    t.start()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()

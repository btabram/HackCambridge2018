# -*- coding: utf-8 -*-
"""thereminimum.py

Written on 20/01 by Will Grant, Tomé Gouveia and Brett Abram

Takes input from Leap motion and writes it out to stdout.

It writes out the palm position coordinates as:
(x, y, z)
"""

import sys, thread, time, os, pyaudio, threading, Queue

if sys.platform == 'linux2':
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
        frame = controller.frame()
        hands = frame.hands
        # If there's a hand write out formatted palm positions to screen.

        if hands.is_empty:
            # if there aren't any hands then don't make sound
            q.put(0,0)
        else:
            if (len(hands) == 1):
                hand=hands[0]
                # Get the hand's normal vector and direction
                yaw = hand.palm_normal.roll if hand.is_left else -1.*hand.palm_normal.roll
                vol = (yaw * Leap.RAD_TO_DEG +90 )/180
                if vol > 1:
                    vol = 1
                if vol < 0:
                    vol = 0

                pitch = 40 + 6.5 * (hand.palm_position[1]- 40)

                q.put(ppts.LeapData(pitch, vol))
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

                pitchL = 40 + 6.5 * (handL.palm_position[1]- 40)
                pitchR = 40 + 6.5 * (handR.palm_position[1]- 40)

                q.put(ppts.LeapData(pitchL, volL, pitchR, volR))
                #print pitchL, volL, pitchR, volR


# queue for passing messages between threads
q = Queue.Queue()


def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # start thread
    t = threading.Thread(target=ppts.play_sound, args=(q, ))
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

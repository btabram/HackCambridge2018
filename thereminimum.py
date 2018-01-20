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
        hand = frame.hands[0]
        # If there's a hand write out formatted palm positions to screen.
        if not frame.hands.is_empty:
            # Get the hand's normal vector and direction
            yaw = hand.palm_normal.roll if hand.is_left else -1.*hand.palm_normal.roll
            vol = (yaw * Leap.RAD_TO_DEG +90 )/1.8
            if vol > 100:
                vol = 100
            if vol < 0:
                vol = 0

            pitch = frame.hands[0].palm_position[1]

            q.put(ppts.LeapData(pitch, vol))


q = Queue.Queue()

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)



    # start thread
    t = threading.Thread(target=ppts.play_sound, args=(q,))
    # daemon won't stop program from exiting when it's the only thread left
    t.daemon = True
    t.start()



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

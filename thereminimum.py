import sys, thread, time, os

if sys.platform == 'linux2':
    sys.path.append('LeapSDK/lib/x64')
    import LeapPython
sys.path.append('LeapSDK/lib')
import Leap

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


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

        # If there's a hand write out formatted palm positions to screen.
        if not frame.hands.is_empty:
            print frame.hands[0].palm_position #.replace(',','')[1:-1]

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

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

#include <iostream>
#include <cstring>
#include "Leap.h"

using namespace Leap;

class SampleListener : public Listener {
  public:
    virtual void onInit(const Controller&);
    virtual void onConnect(const Controller&);
    virtual void onDisconnect(const Controller&);
    virtual void onExit(const Controller&);
    virtual void onFrame(const Controller&);

  private:
};

const std::string fingerNames[] = {"Thumb", "Index", "Middle", "Ring", "Pinky"};
const std::string boneNames[] = {"Metacarpal", "Proximal", "Middle", "Distal"};
const std::string stateNames[] = {"STATE_INVALID", "STATE_START", "STATE_UPDATE", "STATE_END"};

void SampleListener::onInit(const Controller& controller) {
  std::cout << "Initialized" << std::endl;
}

void SampleListener::onConnect(const Controller& controller) {
  std::cout << "Connected" << std::endl;
  controller.enableGesture(Gesture::TYPE_CIRCLE);
  controller.enableGesture(Gesture::TYPE_KEY_TAP);
  controller.enableGesture(Gesture::TYPE_SCREEN_TAP);
  controller.enableGesture(Gesture::TYPE_SWIPE);
}

void SampleListener::onDisconnect(const Controller& controller) {
  // Note: not dispatched when running in a debugger.
  std::cout << "Disconnected" << std::endl;
}

void SampleListener::onExit(const Controller& controller) {
  std::cout << "Exited" << std::endl;
}

void SampleListener::onFrame(const Controller& controller) {
  // Get the most recent frame and report some basic information
  
  const Frame frame = controller.frame();
  /*
  std::cout << "Frame id: " << frame.id()
            << ", timestamp: " << frame.timestamp()
            << ", hands: " << frame.hands().count()
            << ", extended fingers: " << frame.fingers().extended().count()
            << ", tools: " << frame.tools().count()
            << ", gestures: " << frame.gestures().count() << std::endl;
  */
  HandList hands = frame.hands();

  if (hands.count()>2)
  {
    std::cout << "More than two hands. Nope." << std::endl;
    exit(123);
  } 

  if (hands.count()==1)
  {
    Hand hand = hands[0];
    const double pitch = 5.*hand.palmPosition()[1];
    const double roll = (hand.isLeft())? hand.palmNormal().roll() *RAD_TO_DEG : -1.*hand.palmNormal().roll() *RAD_TO_DEG;
    
    double vol = (roll + 90)/180;
    vol = ( vol > 1) ? 1 : vol ;
    vol = ( vol < 0) ? 0 : vol ;

    if (!frame.hands().isEmpty()){
      std::cout << "(" << pitch << ", " << vol << ")" << std::endl;
    }
  }
  else if (hands.count()==2)
  {
    Hand handL, handR;
    if ((hands[0].isLeft() && hands[1].isLeft()) || (hands[0].isRight() && hands[1].isRight()))
    {
      std::cout << "Both hands of the same sign. Nope." << std::endl;
      exit(123);
    } else if (hands[0].isLeft() && hands[1].isRight())
    {
      handL=hands[0];
      handR=hands[1];
    } else if (hands[1].isLeft() && hands[0].isRight())
    {
      handR=hands[0];
      handL=hands[1];
    }
  
    const double pitchL = 5.*handL.palmPosition()[1];
    const double rollL = handL.palmNormal().roll() *RAD_TO_DEG ;
    
    double volL = (rollL + 90)/180;
    volL = ( volL > 1) ? 1 : volL ;
    volL = ( volL < 0) ? 0 : volL ;
  
    const double pitchR = 5.*handR.palmPosition()[1];
    const double rollR = -1.*handR.palmNormal().roll() *RAD_TO_DEG;
    
    double volR = (rollR + 90)/180;
    volR = ( volR > 1) ? 1 : volR ;
    volR = ( volR < 0) ? 0 : volR ;
  
  
    if (!hands.isEmpty()){
        std::cout << "(" << pitchL << ", " << volL << ", " << pitchR << ", " << volR << ")" << std::endl;
    }
  }

}
int main(int argc, char** argv) {

  Controller controller;
  SampleListener listener;

  controller.addListener(listener);

  if (argc > 1 && strcmp(argv[1], "--bg") == 0)
    controller.setPolicy(Leap::Controller::POLICY_BACKGROUND_FRAMES);
  
  
  std::cout << "Press Enter to quit..." << std::endl;
  std::cin.get();

  controller.removeListener(listener);
  
  return 0;
}
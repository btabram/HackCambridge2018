# HackCambridge2018
Hack Cambridge 2018

Team J C Haxwell - Thereminimum Viable Product

This is a theremin [link], controlled using a Leap Motion [link].

The theremin consists of two files:

- A wrapper on the Leap Motion, outputting the palm position to the stdout as a tab-separated list of coordinates.
- An audio synthesizer, taking these co-ordinates and generating a sine wave of a given pitch.



Dependencies:

- Requires Leap Motion installed.


- Requires the shared objects from the Leap Motion SDK.


- Requires pyaudio (which requires portaudio)
- Uses select() to poll for command-line input, meaning this is Linux/MacOS only




## What we got



- Non-blocking IO taking hand position and roll, converts to pitch and volume
- Plays a clap at max volume currently
- Crackles due to fast frequency change





## What we want





- No crackle
- Two hands, two notes
- Better .wav sample playing on gesture
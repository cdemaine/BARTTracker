# BARTTracker
BART tracking via NeoPixels / FadeCandy

Notes and attributions to come.  Thank you to those who came before me.

Provides a non-numeric visual display of how far out transit (BART and MUNI) is from your local station, using a Raspberry Pi and WS2812-based individually addressible RGB LED strip.

## Hardware

  1.  Raspberry Pi - Yeah, one of these.  They're cheap.  Get a USB/WiFi adaptor as well.  And a power supply.
  2.  WS2812 LED strip - Otherwise known as a NeoPixel strip by adafruit.com
  3.  Either:
        FadeCandy - A USB/WS2812 "convertor" that allows easy control of LED strips, or
        74AHCT125 - Quad Level-Shifter (3V to 5V, to upconvert the Pi's digital output)

## Software

### Raspberry Pi
  1. Install some operating system and get your Pi onto the intertoobs
  2. FadeCandy Only:  Install the FadeCandy server and have it start up automatically
  3. 74AHCT125 Only:  Install the tons of software required to make this run

### Configuration
  1.  Create a subdirectory for the BART Tracker and put the contents (bart.py and bartconfig.py) into it
  2.  Modify bartconfig.py for your installation

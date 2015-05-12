#!/usr/bin/env python

# Version 050415

# To be added
#  Offsets
#  Reverse display

print "Loading settings."

# Set various settings

neopixeldirect = True
fadecandy = False

numLEDs = 144 #Too many doesn't hurt, up to 64 on a FadeCandy
stripminutes = 60 # How many minutes the entire strip represents
LEDresolution = stripminutes / float(numLEDs) # How many minutes per LED

timeresolution = 2 # in pixels per minute (not minutes per pixel)
tickresolution = LEDresolution * 60 # seconds between moves
bartrefresh = 15 # ticks until BART data is refreshed
bartwidth = 4 # led length of a BART train
muniwidth = 2 # led lenth of a MUNI train
stationlocation = 0 # LED location of the station
tickstostation = int( 6 / LEDresolution) # How many LEDs to get to the platform, from minutes
BARTKey = 0 # Not currently used
FiveOneOneKey = "5ab30a23-0309-4d30-9e2f-c0bd03ed48da" # Super secret
municolor = "#ffa500" # Muni doesn't provide this

# NeoPixel direct-drive specific
LED_COUNT      = numLEDs # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 20      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# FadeCandy specific
openpixelcontroller = 'localhost:7890' # Machine/port for the OPC / Fadecandy

  # Set in the FadeCandy configuration file for the server

print "Settings loaded."

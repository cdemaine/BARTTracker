#!/usr/bin/env python

# Added Muni 040615
# Added config file 040715
# Added older process killer (commented out)
# Added NeoPixel direct drive
# Added support for different densities of lights
# Revised timing scheme and configuration file
# Fixed last-pixel one-off copy problem 122015
# Adjusted sleep delay to increase accuracy 122015

# To do:

#  - Offset MUNIs to match leave-time
#  - Put text files into individual dated files
#  - Add on/off for BART/MUNI
#  - Revise termination of older program
#  - Add quiet times
#  - Add boot up display
#  - Add warning if no bartconfig.py file

# FadeCandy only

import opc 

# NeoPixel direct drive only

from neopixel import *

# used for all

import time     # handy
import urllib   # for web requests
import urllib2  # for web requests
import requests # also probably for web requests
import lxml     # xml parsing

# Import configurations

exec(open("./bartconfig.py").read())

print "BART/Muni LED pixel display", time.strftime("%d/%m/%Y %H:%M:%S")

# Find and kill predecessor (Not platform-independent)

# import subprocess
# p = subprocess.Popen(['pgrep', '-f' , 'bart.py'], stdout=subprocess.PIPE)
# out, err = p.communicate()

# if len(out.splitlines()) > 1:
# 	p = subprocess.Popen(['kill', out.splitlines()[0]], stdout=subprocess.PIPE)
# 	p.wait()
# 	print "Terminated older script."

if fadecandy:
	client = opc.Client(openpixelcontroller)
elif neopixeldirect:
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	strip.begin()


pixels = [ (0,0,0) ] * numLEDs
overlay = [ (0,0,0)] * numLEDs
output = [ (0,0,0)] * numLEDs

overlay[stationlocation] = (200,200,200)
overlay[tickstostation] = (100,100,100)

if fadecandy:
	client.put_pixels(output)
	client.put_pixels(output)
elif neopixeldirect:
	strip.show()


def loadBART(pixels):
	departures = bart.etd("GLEN")

	print departures

	with open('bartlog.txt','a') as logfile:

		for line in departures:
			print line['abbreviation']
			for train in line['estimates']:
				eta = train['minutes']
				color = train['hexcolor']
				print eta, color
				logfile.write(time.strftime("%d/%m/%Y %H:%M:%S"))
				logfile.write(" ")
				logfile.write(line['abbreviation'])
				logfile.write(" ")
				logfile.write(eta)
				logfile.write("\n")
				
				if not(eta.isalpha()) and ((int(eta) / LEDresolution) < (numLEDs-bartwidth)) and train['direction'] == 'North':
			 		red = int(color[1:3],16)
			 		green = int(color[3:5],16)
					blue = int(color[5:7],16)
			 		for bartpixel in range(0,bartwidth):
			 			pixels[int(int(eta) / LEDresolution)+bartpixel] = (red,green,blue)
			 			print 'displaying', line['abbreviation'], eta, bartpixel

def loadMUNI(pixels):
	with open('munilog.txt','a') as logfile:
		response = urllib2.urlopen('http://services.my511.org/Transit2.0/GetNextDeparturesByStopCode.aspx?token=5ab30a23-0309-4d30-9e2f-c0bd03ed48da&stopcode=14787')
		html = response.read()

		from xml.etree import ElementTree as XMLTree
		tree = XMLTree.fromstring(html)
		for child in tree.iter('DepartureTime'):
			eta = child.text

			if not(eta.isalpha()) and ((int(eta) / LEDresolution) < (numLEDs-muniwidth)):
		 		red = int(municolor[1:3],16)
		 		green = int(municolor[3:5],16)
				blue = int(municolor[5:7],16)
		 		for munipixel in range(0,muniwidth):
		 			pixels[int(int(eta) / LEDresolution) +munipixel] = (red,green,blue)
		 			print 'displaying MUNI', eta, munipixel
			


from bart_api import BartApi

bart = BartApi()

# The main loop - so good it never ends

# The system is based on ticks, which are moves of the "trains" down the LED strip
# The duration of a tick is the length, in time, of the strip divided by the number of LEDs
# Example:  60 minutes = 3600 seconds "Length"
#           3600 seconds / 144 pixels = 25 seconds per tick

# On the first tick clean the display and fetch BART and MUNI data
# 


while True:

	for tick in range(0,bartrefresh):

		if tick == 0:
			pixels = [ (0,0,0) ] * numLEDs # clear train pixels
			loadBART(pixels)
			loadMUNI(pixels)

		print 'tick'

		for i in range(0,4): # each should be ~ 6 seconds
			overlay[stationlocation] = (100+ 100 * (i%2) ,100+ 100  * (i%2) ,100+ 100 *  (i%2) ) # yay Modulo!  Slowly strobe station
			for LED in range(0,numLEDs):
				output[LED] = (pixels[LED][0] | overlay[LED][0], pixels[LED][1] | overlay[LED][1], pixels[LED][2] | overlay[LED][2])

			if fadecandy:
				client.put_pixels(output)	
			elif neopixeldirect:
				for pixel in range(0,numLEDs):
					strip.setPixelColor(pixel, Color(output[pixel][0], output[pixel][1], output[pixel][2]))
					strip.show()

			time.sleep(6) # Yes, this is a magic number
			print 'z'

			if (i+1)%(4) == 0:
				# Done waiting, move trains one pixel
				print 'moving'
				for j in range(0, numLEDs -2):
		 			pixels[j] = pixels[j+1]	
		 		pixels[numLEDs-1] = (0,0,0)			



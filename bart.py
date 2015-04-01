#!/usr/bin/env python



import opc, time, urllib
import requests
import urllib
import lxml

numLEDs = 64
timeresolution = 1 # 1 pixel per minute
bartrefresh = 5 # minutes until BART data is refreshed
bartwidth = 2 # led length of a BART train
stationlocation = 0 # LED location of the station
minutestostation = 6 # How many minutes to get to the platform
tickstostation = minutestostation * timeresolution

print "BART LED pixel display"

client = opc.Client('localhost:7890')

pixels = [ (0,0,0) ] * numLEDs
overlay = [ (0,0,0)] * numLEDs
output = [ (0,0,0)] * numLEDs

overlay[stationlocation] = (200,200,200)
overlay[tickstostation] = (100,100,100)

client.put_pixels(output)
client.put_pixels(output)

from bart_api import BartApi

bart = BartApi()

while True:

	departures = bart.etd("GLEN")

	print departures

	pixels = [ (0,0,0) ] * numLEDs # clear pixels

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
				
				if not(eta.isalpha()) and int(eta) < (numLEDs-bartwidth) and train['direction'] == 'North':
			 		red = int(color[1:3],16)
			 		green = int(color[3:5],16)
					blue = int(color[5:7],16)
			 		for bartpixel in range(0,bartwidth):
			 			pixels[int(eta* timeresolution)+bartpixel] = (red,green,blue)
			 			print 'displaying', line['abbreviation'], eta, timeresolution, bartpixel

	for minute in range(1,bartrefresh):

		print 'tick'
		for i in range(0,6):
			overlay[stationlocation] = (100+ 100 * (i%2) ,100+ 100  * (i%2) ,100+ 100 *  (i%2) ) # yay Modulo!  Slowly strobe station
			for LED in range(0,numLEDs-1):
				output[LED] = (pixels[LED][0] | overlay[LED][0], pixels[LED][1] | overlay[LED][1], pixels[LED][2] | overlay[LED][2])

			client.put_pixels(output)			
			time.sleep(10)
			print 'z'

		# Done waiting, move trains one pixel
		for i in range(0, numLEDs -2):
		  pixels[i] = pixels[i+1]





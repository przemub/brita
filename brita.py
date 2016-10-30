#!/usr/bin/env python3
# Brita 0.2 - backlight adjuster for Linux
# Copyright (C) 2016 Przemysław Buczkowski <przemub@przemub.pl>
# This file is distributed under the MIT license.

import gettext
import locale
import os
from sys import argv, exit, platform, stderr
import sys

def initlocalization():
	gettext.textdomain("brita")

	filename = gettext.find("brita")
	if filename == None:
		filename = gettext.find("brita", "build/mo")

	try:
		if filename != None:
			trans = gettext.GNUTranslations(open(filename, "rb"))
		else:
			trans = gettext.NullTranslations()
	except IOError:
		trans = gettext.NullTranslations()

	trans.install()

def readbrightness(printit = True):
	global brightness, max_brightness

	brightness = int(brightnessfile.read().strip())
	max_brightness = int(max_brightnessfile.read().strip())

	brightnessfile.seek(0)
	max_brightnessfile.seek(0)

	if not printit:
		return

	percent = int(brightness / max_brightness * 100)
	print(_("%s%%")
		% (percent))

def main(printit = True, lower_bound = False):
	if platform != 'linux':
		if printit:
			stderr.write(_("This script works only in Linux environment.")
				+ "\r\n")
		exit(1)

	directory = "/sys/class/backlight/"
	device = os.listdir(directory)[0]
	directory += device + "/"
	if printit:
		print(_("Found backlight device: %s") % (device))

	properties = os.listdir(directory)
	if not 'brightness' in properties or not 'max_brightness' in properties:
		if printit:
			stderr.write(_("Brightness settings aren't available for the device.\n"))
		exit(1)

	global brightness, max_brightness
	global brightnessfile, max_brightnessfile

	brightnessfile = open(directory + 'brightness', 'r+')

	max_brightnessfile = open(directory + 'max_brightness', 'r')

	if len(argv) == 1:
		readbrightness(printit)
		exit(0)

	wantedbrightness = argv[-1]

	if wantedbrightness[0] == '+' or wantedbrightness[0] == '-':
		readbrightness(False)

		if wantedbrightness[-1] == '%':
			percent = float(wantedbrightness[1:-1]) / 100
			if (wantedbrightness[0] == '+'):
				brightness = int(brightness + max_brightness * percent)
			elif (wantedbrightness[0] == '-'):
				brightness = int(brightness - max_brightness * percent)
		else:
			if (wantedbrightness[0] == '+'):
				brightness = brightness + int(wantedbrightness[1:])
			elif (wantedbrightness[0] == '-'):
				brightness = brightness - int(wantedbrightness[1:])

		if brightness > max_brightness:
			brightness = max_brightness
		if brightness < 0:
				if lower_bound:
						brightness = 100
				else:
						brightness = 0
		if printit:
			print(brightness)
		brightnessfile.write(str(brightness))
		brightnessfile.seek(0)

		readbrightness(printit)
		exit(0)
	elif wantedbrightness[-1] == '%':
		readbrightness(False)

		percent = float(wantedbrightness[:-1]) / 100
		brightness = int(float(max_brightness) * percent)

		if brightness > max_brightness:
				brightness = max_brightness
		if brightness < 0:
				if lower_bound:
						brightness = 100
				else:
						brightness = 0

		brightnessfile.write(str(brightness))
		brightnessfile.seek(0)

		readbrightness(printit)

if __name__ == "__main__":
	initlocalization()

	version = "0.2"
	synopsis = _("Brita %s - backlight adjuster for Linux") % (version)

	synopsis += "\n" +_('''Usage: brita [options] value
	Options:
	  -q, --quiet		Disable printing output
	  -v, --version		Print current version and exit
	  -h, --help		Print this message and exit
	  -m, --min			Set minimum brightness to 100
	  
	Value can be in percents (ie. 50%)
		       or relative to the current value (ie. -500, +30%, -10%)

	Program executed without arguments shows the current brightness''')	
	
	State1 = True;
	State2 = False;
	
	for arg in sys.argv:
		if arg == "-h" or arg == "--help":
			print(synopsis)
			exit(0)
		if arg == "-v" or arg == "--version":
			print(version)
			exit(0)
		if arg == "-q" or arg == "--quiet":
			State1 = False
		if arg == "-m" or arg == "--min":
			State2 = True		
	main(State1,State2)

#!/usr/bin/env python3
# Brita 0.2 - backlight adjuster for Linux
# Copyright (C) 2016 Przemysław Buczkowski <przemub@przemub.pl>
# This file is distributed under the MIT license.

import gettext
import locale
import os
import sys

def init_localization():
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

def read_brightness(verbose = True):
    global brightness, max_brightness

    brightness = int(brightnessfile.read().strip())
    max_brightness = int(max_brightnessfile.read().strip())

    brightnessfile.seek(0)
    max_brightnessfile.seek(0)

    if not verbose:
        return

    percent = int(brightness / max_brightness * 100)
    print(_("%s%%") % (percent))

def main(verbose = True, lower_bound = False):
    if sys.platform != 'linux':
        if verbose:
            sys.stderr.write(_("This script works only in a Linux environment.")
                    + "\r\n")
            sys.exit(1)

    directory = "/sys/class/backlight/"
    device = os.listdir(directory)[0]
    directory += device + "/"
    if verbose:
        print(_("Found backlight device: %s") % (device))

    properties = os.listdir(directory)
    if not 'brightness' in properties or not 'max_brightness' in properties:
        if verbose:
            sys.stderr.write(_("Brightness settings aren't available " +
                "for the device.\n"))
            sys.exit(1)

    global brightness, max_brightness
    global brightnessfile, max_brightnessfile

    brightnessfile = open(directory + 'brightness', 'r+')

    max_brightnessfile = open(directory + 'max_brightness', 'r')

    if len(sys.argv) == 1:
        read_brightness(verbose)
        exit(0)

    wanted_brightness = sys.argv[-1]

    if wanted_brightness[0] == '+' or wanted_brightness[0] == '-':
        read_brightness(False)

        if wanted_brightness[-1] == '%':
            percent = float(wanted_brightness[1:-1]) / 100
            if (wanted_brightness[0] == '+'):
                brightness = int(brightness + max_brightness * percent)
            elif (wantedbrightness[0] == '-'):
                brightness = int(brightness - max_brightness * percent)
        else:
            if (wanted_brightness[0] == '+'):
                brightness = brightness + int(wanted_brightness[1:])
            elif (wanted_brightness[0] == '-'):
                brightness = brightness - int(wanted_brightness[1:])

        if brightness > max_brightness:
            brightness = max_brightness

        if brightness < 0:
            if lower_bound:
                brightness = 100
            else:
                brightness = 0

        if verbose:
            print(brightness)
        brightnessfile.write(str(brightness))
        brightnessfile.seek(0)

        readbrightness(verbose)
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

        read_brightness(verbose)

if __name__ == "__main__":
    init_localization()

    version = "0.2"
    synopsis = _("Brita %s - backlight adjuster for Linux") % (version)

    synopsis += "\n" +_('''Usage: brita [options] value
\tOptions:
\t  -q, --quiet\tDisable printing output
\t  -v, --version\tPrint the current version and exit
\t  -h, --help\tPrint this message and exit
\t  -m, --min\tDon't set the brightness to a value lower than 100

\tValue can be given in percents (ie. 50%)
\t\tor relative to the current value (ie. -500, +30%, -10%)

\tProgram executed without arguments prints the current brightness.''')

    verbose = True;
    lower = False;

    for arg in sys.argv:
        if arg == "-h" or arg == "--help":
            print(synopsis)
            exit(0)
        elif arg == "-v" or arg == "--version":
            print(version)
            exit(0)
        elif arg == "-q" or arg == "--quiet":
            verbose = False
        elif arg == "-m" or arg == "--min":
            lower = True

    main(verbose, lower)


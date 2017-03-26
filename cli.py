#!/usr/bin/env python
from __future__ import division
import math
import numpy
import argparse
try:
    import Image
except ImportError:
    from PIL import Image

from itertools import groupby
from pprint import pprint
version = "0.1"
laser = True
laserOffCmd = "M5"
laserOnCmd = "M3"

def loadArray(arr):
    im = Image.fromarray(arr)

def loadImage(file):
    #Open Source
    img = Image.open(file)
    #aspect
    height = args.width/(img.size[0]/img.size[1])
    #This resize is close
    #Rotated and flipped to look proper
    resize = (
        int(math.floor(args.xdensity * args.width)),
        int(math.floor(args.ydensity * height))
        )
    img.resize(resize, Image.LANCZOS) \
        .convert("L", colors=args.colors) \
        .transpose(Image.ROTATE_180) \
        .transpose(Image.FLIP_LEFT_RIGHT) \
        .save("workfile.jpg")
    #Save temp, TODO: do without writing file? tired.
    img = Image.open("workfile.jpg")
    #img.show()
    imgarr = numpy.array(img)
    return imgarr

def laserOff():
    global laser
    if laser:
        lines.append(laserOffCmd)
        laser = False

def laserOn(power):
    global laser
    #if not laser:
    lines.append("S" + str(power) + " " + laserOnCmd)
    laser = True

parser = argparse.ArgumentParser()
parser.add_argument('file', help='image file name')
parser.add_argument('width', type=int, help='Output width in MM (ish), FIX ME')
#Versioning
parser.add_argument('-v', '--version', action='version', version=version )
#TODO: arguments and profiles.....
#parser.add_argument('-s', '--size',  type=float, help='pixelsize')
parser.add_argument('-c', '--colors',  type=int, default=16,
    help='Number of shades, default 16')
parser.add_argument('-xd', '--xdensity',  type=int, default=3,
    help='Pixels per MM in X direction, default 3')
parser.add_argument('-yd', '--ydensity',  type=int, default=3,
    help='Pixels per MM Y direction, default 3')

#Check the arguments
args = parser.parse_args()
#Make sure at least one option is chosen
if not (args.file or args.colors):
    #Print help
    parser.print_help()
    #Exit out with no action message
    parser.error('No action requested')

#TODO: config profiles so you don't have to mess around.....
#SERIOUSLY! ^^^^^^^

skipSpeed = 3000 #FEEDRATE ON WHITE
burnSpeed = 800 #FEEDRATE WHILE BURNING
laserMax = 12000 #MAX LASER PWM VALUE
laserMin = math.ceil(12000/255)

#Do all the things
if args.file :

    #Load a image file to array
    arr = loadImage(args.file)

    #TODO: make it possible to scale the image, so final output dimensions are
    # known, which might not be easy considering the chunking going on below.


    width=len(arr[0])
    height=len(arr)
    print "Image width: " + str(width)
    print "Image height: " + str(height)

    #1mm per pixel leaves some gap, once the above TODO is looked into, this
    # would become a varible setting,.
    scaley = 0.4
    scalex = 0.4

    #Create a list to store the output gcode lines
    lines = []

    #Y position
    yp=0

    #Turn the laser off
    laserOff()

    #Work in MM
    lines.append("G21")

    #Loop over the list
    #TODO: get to end of line and reverse, saving time going back to x0 takes.
    for y in arr:
        #Go the start of this line
        lines.append("G0 X0 Y" + str(yp*scaley) + " F" + str(skipSpeed))
        #reset the x postion
        xp = 0
        #reset the lastxp position
        lastxp = 0
        #Group pixels by value into a new list
        for i, j in groupby(y):
            #items in the list
            items =  list(j)
            #Number of items
            size = len(items)
            #grey Value in this chunk of the line
            value = items[0]
            #print items
            #Make sure this isn't WHITE or 255
            if value < 255:
                #If we need to skip ahead
                if xp > 0 and lastxp == xp:
                    #Skip ahead with the laser off
                    laserOff()
                    lines.append("G0 X" + str(xp*scalex) + " F" + str(skipSpeed))
                #Turn on the laser
                laserOn( math.ceil( laserMax-(value*laserMin) ) )
                #Burn the segment
                lines.append("G1 X" + str((xp+size)*scalex) + " F" + str(burnSpeed))
            else:
                #Turn off the laser
                laserOff()
                #skip the white
                lines.append("G0 X" + str((xp+size)*scalex) + " F" + str(skipSpeed))
            #track x position
            lastxp = xp
            #Increment position
            xp = xp + size
        #Turn the laser off
        laserOff()
        yp = yp + 1
    #TODO: Output file name etc.
    f = open('workfile.gcode', 'w')
    f.write("\n".join(lines))

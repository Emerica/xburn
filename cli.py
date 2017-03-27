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
version = "0.2"
laser = True

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
        .save(args.output+".gcode.jpg")
    #Save temp, TODO: do without writing file? tired.
    img = Image.open(args.output+".gcode.jpg")
    #img.show()
    imgarr = numpy.array(img)
    return imgarr

def laserOff():
    global laser
    if laser:
        lines.append(args.laseroff)
        laser = False

def laserOn(power):
    global laser
    #if not laser:
    lines.append(args.modifier + str(power) + " " + args.laseron)
    laser = True

#creates a 255x20 black to white gradient for testing settings
def gradientTest():
    img = Image.new( 'RGB', (255,20), "black") # create a new black image
    pixels = img.load() # create the pixel map
    for i in range(img.size[0]):    # for every pixel:
        for j in range(img.size[1]):
            pixels[i,j] = (i, i, i) # set the colour accordingly
    img.save(args.output+".jpg")

#TODO: config profiles so you don't have to mess around.....
#SERIOUSLY! ^^^^^^^

parser = argparse.ArgumentParser()
parser.add_argument('file', help='image file name')
parser.add_argument('width', type=int, help='Output width in MM (ish), FIX ME')

#Versioning
parser.add_argument('-v', '--version', action='version', version=version )
#TODO: arguments and profiles.....
#parser.add_argument('-s', '--size',  type=float, help='pixelsize')
parser.add_argument('-c', '--colors',  type=int, default=16,
    help='Number of shades, default 16')
parser.add_argument('-wv', '--whitevalue',  type=int, default=255,
    help='White value, defaults to 255, anything larger than this is skipped.')
parser.add_argument('-xd', '--xdensity',  type=int, default=3,
    help='Pixels per MM in X direction, default 3')
parser.add_argument('-yd', '--ydensity',  type=int, default=3,
    help='Pixels per MM Y direction, default 3')
parser.add_argument('-sr', '--skiprate',  type=int, default=3000,
    help='Moving Feed Rate')
parser.add_argument('-br', '--burnrate',  type=int, default=800,
    help='Burning Feed Rate')
parser.add_argument('-st', '--steps',  type=int, default=255,
    help='Laser PWM Steps')
parser.add_argument('-hp', '--highpower',  type=int, default=12000,
    help='Laser Max Power PWM VAlUE')
parser.add_argument('-lp', '--lowpower',  type=int, default=0,
    help='Laser Min Power PWM VAlUE')
parser.add_argument('-on', '--laseron', default="M3",
    help='Laser ON Gcode Command default: M3')
parser.add_argument('-off', '--laseroff', default="M5",
    help='Laser Off Gcode Command default: M5')
parser.add_argument('-mod', '--modifier', default="S",
    help='Laser Power Modifier, defaults to Spindle Speed (S)')
parser.add_argument('-o', '--output',  default="workfile",
        help='Outfile name prefix')
parser.add_argument('-p', '--preview', action='store_true',
    help='Turns on Debugging')
parser.add_argument('-d', '--debug', action='store_true',
    help='Turns on Debugging')

#Check the arguments
args = parser.parse_args()
#Make sure at least one option is chosen
if not (args.file or args.colors):
    #Print help
    parser.print_help()
    #Exit out with no action message
    parser.error('No action requested')


if args.lowpower == 0:
    args.lowpower = math.ceil(args.highpower/args.steps)
    if args.debug:
        print "Low power set to: " + str(args.lowpower)

#Do all the things
if args.file:
    #Load a image file to array
    arr = loadImage(args.file)
    scaley = 1/args.ydensity
    scalex = 1/args.xdensity
    #Create a list to store the output gcode lines
    lines = []
    #Y position
    yp=0
    #Turn the laser off
    laserOff()
    if args.preview:
        prv = Image.new( 'RGB', (len(arr[0]),len(arr)), "red") # create a new black image
        pixels = prv.load() # create the pixel map
    #Work in MM
    lines.append("G21")
    #Loop over the list
    #TODO: get to end of line and reverse, saving time going back to x0 takes.
    for y in arr:
        #Go the start of this line
        lines.append("G0 X0 Y" + str(round(yp*scaley, 3)) + " F" + str(args.skiprate))
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
            if value < args.whitevalue:
                if args.preview:
                    pvx=0
                    for item in items:
                        #print  str(item) + " - " + str(yp) + " - "
                        pixels[xp+pvx,yp] = (item, item, item)
                        pvx = pvx + 1
                #If we need to skip ahead
                if xp > 0 and lastxp == xp:
                    #Skip ahead with the laser off
                    laserOff()
                    lines.append("G0 X" + str(round(xp*scalex, 3)) + " F" + str(args.skiprate))
                #Turn on the laser
                laserOn( math.ceil( args.highpower - (value * args.lowpower ) ) )
                #Burn the segment
                lines.append("G1 X" + str(round((xp+size)*scalex,3)) + " F" + str(args.burnrate))
            else:
                #Turn off the laser
                laserOff()
                #skip the white
                lines.append("G0 X" + str(round((xp+size)*scalex,3)) + " F" + str(args.skiprate))
            #track x position
            lastxp = xp
            #Increment position
            xp = xp + size
        #Turn the laser off
        laserOff()
        yp = yp + 1
    #TODO: Output file name etc.
    if args.preview:
        prv.transpose(Image.ROTATE_180).transpose(Image.FLIP_LEFT_RIGHT).show()
        #prv.show()
    f = open(args.output+'.gcode', 'w')
    f.write("\n".join(lines))

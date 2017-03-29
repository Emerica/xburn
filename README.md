# Xburn Laser Gcode Tool

Python Command Line Tool
Create gcode files for a laser mounted to a shapeoko3 using stock firmware

-Skip's White Areas
-Burns in both directions, reversing every other line

<p align="center">
  <a href="https://www.youtube.com/edit?o=U&video_id=BWzQP15pxRQ"><img src="https://i.ytimg.com/vi_webp/BWzQP15pxRQ/maxresdefault.webp" width="350"/>
  </a>
</p>


-TODO - FIX Shades Option. Howto

### Prerequisites

python, pil?, numpy?

### Installing

```
git clone https://github.com/Emerica/xburn.git
cd xburn
pip install -r requirements.txt
chmod +x cli.py
./cli.py -h
usage: cli.py [-h] [-v] [-pa] [-s SHADES] [-wv WHITEVALUE] [-xd XDENSITY]
              [-yd YDENSITY] [-sr SKIPRATE] [-br BURNRATE] [-st STEPS]
              [-hp HIGHPOWER] [-lp LOWPOWER] [-on LASERON] [-off LASEROFF]
              [-mod MODIFIER] [-o OUTPUT] [-p] [-tp] [-d]
              file width

positional arguments:
  file                  image file name
  width                 Output width in MM (ish), FIX ME

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -pa, --palette        Color Palette, use with shades option, needs work.
  -s SHADES, --shades SHADES
                        Number of shades, default 16
  -wv WHITEVALUE, --whitevalue WHITEVALUE
                        White value, defaults to 255, anything larger than
                        this is skipped.
  -xd XDENSITY, --xdensity XDENSITY
                        Pixels per MM in X direction, default 3
  -yd YDENSITY, --ydensity YDENSITY
                        Pixels per MM Y direction, default 3
  -sr SKIPRATE, --skiprate SKIPRATE
                        Moving Feed Rate
  -br BURNRATE, --burnrate BURNRATE
                        Burning Feed Rate
  -st STEPS, --steps STEPS
                        Laser PWM Steps
  -hp HIGHPOWER, --highpower HIGHPOWER
                        Laser Max Power PWM VAlUE
  -lp LOWPOWER, --lowpower LOWPOWER
                        Laser Min Power PWM VAlUE
  -on LASERON, --laseron LASERON
                        Laser ON Gcode Command default: M3
  -off LASEROFF, --laseroff LASEROFF
                        Laser Off Gcode Command default: M5
  -mod MODIFIER, --modifier MODIFIER
                        Laser Power Modifier, defaults to Spindle Speed (S)
  -o OUTPUT, --output OUTPUT
                        Outfile name prefix
  -p, --preview         Preview burn output, red is skipped over.
  -tp, --testpattern    Create a test pattern. Use ./cli.py test 100 -tp -p -o
                        testfile
  -d, --debug           Turns on Debugging
```

Output ~100mm wide image with preview enabled


```
./cli.py filename.jpg 100 -o filename -p
cat filename.gcode
```


Create a gradient test pattern for tuning power levels

```
./cli.py test 100 -tp -o testpattern -p [non default settings here]
cat testpattern.gcode

```

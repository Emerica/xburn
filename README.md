# Xburn Laser Gcode Tool

Python Command Line Tool
Create gcode files for a laser mounted to a shapeoko3 using stock firmware

### Prerequisites

python, pil?, numpy?

### Installing

```
git clone https://github.com/Emerica/xburn.git
cd xburn
pip install -r requirements.txt
chmod +x cli.py
./cli.py -h
usage: cli.py [-h] [-v] [-c COLORS] [-xd XDENSITY] [-yd YDENSITY]
              [-sr SKIPRATE] [-br BURNRATE] [-st STEPS] [-hp HIGHPOWER]
              [-lp LOWPOWER] [-on LASERON] [-off LASEROFF] [-mod MODIFIER]
              [-o OUTPUT] [-d]
              file width

positional arguments:
  file                  image file name
  width                 Output width in MM (ish), FIX ME

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c COLORS, --colors COLORS
                        Number of shades, default 16
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
  -d, --debug           Turns on Debugging
```

Output ~100mm wide image


```
./cli.py filename.jpg 100 -o filename
cat filename.gcode
```

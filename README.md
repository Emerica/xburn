usage: cli.py [-h] [-v] [-c COLORS] [-xd XDENSITY] [-yd YDENSITY]
              [-sr SKIPRATE] [-br BURNRATE] [-st STEPS] [-hp HIGHPOWER]
              [-lp LOWPOWER] [-o OUTPUT]
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
  -o OUTPUT, --output OUTPUT
                        Outfile name prefix

# OGN-Flight-Logger
Python APRS/OGN program to log flight times, durations and maximum heights achieved

This python program creates an SQlite db of flights from a given location and aircraft list 
(the later two parameters are to be be developed into a more generalised format).

At the moment this is very much 'in development'

To install OGN Flight Logger the following prerequisites are required
- python-tz
- sqlite3
- libfap
- ephem
 
To run flogger first set up the parameters in settings.py then call 'flogger.py'.  Flogger.py will
run continuously (perhaps it should be a 'service'?) logging flights during day, ie between sunrise
and sunset. After sunset it processes the days log to determine which log entries constitute actual flights
and those which are ground movements etc. Once all the flights have been generated into the 'flights' table
flogger determines when the next sunrise time and sleeps until then, ie waits.

If installing on an arm based system this can be achieved by:

- sudo apt-get install python-tz sqlite3
- wget http://www.pakettiradio.net/downloads/libfap/1.5/libfap6_1.5_armhf.deb
- sudo dpkg -i libfap*.deb

- sudo apt-get install pythonX-dev where X is version of python being used
- sudo apt-get install python-pip
- sudo pip install pyephem 

# OGN-Flight-Logger_V2
DEVELOPMENT OF OGN-Flight-Logger IS NOW CONTINUING AS: OGN-Flight-Logger_V2

Python APRS/OGN program to log flight times, durations and maximum heights achieved

This python program creates an SQlite db of flights from a given location and aircraft list 
(the later two parameters are to be be developed into a more generalised format).

At the moment this is very much 'in development'

To install OGN Flight Logger the following prerequisites are required
- python-tz
- sqlite3
- libfap (Note this is the "C" library libfap, not the python module libfap.py)
- ephem
- goecoder
- geopy
 
To run flogger first set up the parameters in settings.py then call 'flogger.py'.  Flogger.py will
run continuously (perhaps it should be a 'service'?) logging flights during day, ie between sunrise
and sunset. After sunset it processes the days log to determine which log entries constitute actual flights
and those which are ground movements etc. Once all the flights have been generated into the 'flights' table and
the days flights dumped as a .csv file, flogger determines when the next sunrise time and sleeps until then, ie waits.

OGN-Flight-Logger must be called using: python flogger.py your_username your_passcode,
where you_username and your_passcode can be created on http://http://www.george-smart.co.uk/wiki/APRS_Callpass
If a valid username and passcode are not suppled it will exit immediately.

If installing on an arm based system this can be achieved by:

- sudo apt-get install python-tz sqlite3
- wget http://www.pakettiradio.net/downloads/libfap/1.5/libfap6_1.5_armhf.deb
- sudo dpkg -i libfap*.deb

- sudo apt-get install pythonX-dev where X is version of python being used
- sudo apt-get install python-pip
- sudo pip install pyephem 
- sudo pip install geopy
- sudo pip install geocoder
- sudo pip install aerofiles

I'm currently developing and testing on
- a Raspberry Pi P2 Model B under Rasparian (Debian Linux 7.8) and 
- a desktop running Kubuntu 14.04 

Flogger has been updated to optionally record flight tracks and output these as .gpx files.
This enhancement is still in development.  This feature is controlled in the settings.py file

Flogger will now optionally take inputs from upto 4 base stations.  It also has an option to delete flight and track .csv files after
they are "n" days old.  Track points are sorted and output to .csv files based on the logged time from the Flarm unit itself (assumes Flarms
use GPS time in each trackpoint).  This is to over come a potential issue using multiple base stations when the track points might not be received in the same
time order as they were sent from the flarm units.

This now in the latter stages of development, it still logs a lot of test output but his will eventually be controlled by an option
from the cmd line and/or configuration file

9th March 2016 
Added an option to output IGC format track files. This requires aerofiles.py to be installed (see above).  Several optional fields in the 
header are set to "Not recorded" as these can not be known by OGN Flogger, however if this data was input prior to launch it could, but
that's another development..... Note the files output are not 'certified'.

Added an option to specify number of hours before sunset that processing the flight logs should commence.

Added an option to send the daily flight log to a specified email address in .csv format.
The cmd line form is:
flogger.py username passcode mode [-s|--smtp email address of smtp server] [-t|--tx email address of sender] [-r|--rx email address of receiver]

If -s|--smtp is provided then -t|--tx and -r|--rx must be provided

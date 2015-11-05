
#-------------------------------------
# OGN-Flight-Logger Settings
#-------------------------------------
# Python APRS/OGN program to log flight times, durations, maximum heights achieved and tracks
#
# This python program creates an SQlite db of flights from a given location and aircraft list 
# (the later two parameters are to be be developed into a more generalised format).#
#
# At the moment this is very much 'in development'#
#
# To install OGN Flight Logger the following prerequisites are required
# - python-tz
# - sqlite3
# - libfap
#
# If installing on an arm based system this can be achieved by:
#
# sudo apt-get install python-tz sqlite3
# wget http://www.pakettiradio.net/downloads/libfap/1.5/libfap6_1.5_armhf.deb
#sudo dpkg -i libfap*.deb

#
#-------------------------------------
# Setting values
#
# The values APRS_SERVER_HOST and APRS_SERVER_PORT are FIXED
# All other values should be set for a specific location and USER/PASSCODE
# Failure to change USER/PASSCODE results in an error
#-------------------------------------
#

# APRS_SERVER_HOST = 'rotate.aprs2.net'
# APRS_SERVER_PORT = 14580
APRS_SERVER_HOST = 'aprs.glidernet.org'
APRS_SERVER_PORT = 14580
#
# Please get your own Username and Passcode from http://www.george-smart.co.uk/wiki/APRS_Callpass
# DO NOT USE THE VALUES IN THIS FILE AS IT WILL STOP A PREVIOUS INVOCATION WORKING CORRECTLY
#
APRS_USER = 'PythonEx'                                          # Username
APRS_PASSCODE =  1234                                           # Passcode. See http://www.george-smart.co.uk/wiki/APRS_Callpass 
#
# Check that APRS_USER and APRS_PASSCODE are set
#
assert len(APRS_USER) > 3 and len(str(APRS_PASSCODE)) > 0, 'Please set APRS_USER and APRS_PASSCODE in settings.py.'
#
# User defined configuration values
#
FLOGGER_DB_SCHEMA = "/home/pjr/git/OGN-Flight-Logger/flogger_schema-1.0.4.sql" # File holding SQLite3 database schema      
FLOGGER_QNH = 340                                               # QNH ie ASL in metres for airfield at lat/logitude, if set to 0, elevation is automatically looked up. This is Sutton Bank
FLOGGER_LATITUDE, FLOGGER_LONGITUDE = '+54.228833', '-1.209639' # Latitude, longitude of named airfield
FLOGGER_AIRFIELD_DETAILS = ""                                   # Location details for use by geocoder. If blank, "" use LAT, LONG etc
FLOGGER_MIN_FLIGHT_TIME = "0:4:0"                               # hh:mm:ss
FLOGGER_KEEPALIVE_TIME = 900                                    # Interval in seconds for sending tcp/ip keep alive on socket connection
FLOGGER_DB_NAME = "flogger.sql3.2"                              # Name of file for flogger SQLite3 database
FLOGGER_FLARMNET_DB_URL = "http://www.flarmnet.org/files/data.fln" # URL of Flarmnet database
FLOGGER_AIRFIELD_NAME = "SuttonBnk"                             # Name of Flarm base station for airfield. NOTE MUST BE PROVIDED
FLOGGER_QFE_MIN = 25                                            # Minimum altitude in metres attained for inclusion as a flight, ie ~50 ft
FLOGGER_LOG_PATH =  "/home/pjr/git/OGN-Flight-Logger/logs"      # Path where log files are stored 
FLOGGER_TRACKS = "Y"                                            # If Y flight tracks are recorded. Default is N, ie No tracks logged
FLOGGER_TRACKS_FOLDER = "/home/pjr/git/OGN-Flight-Logger/tracks"# Folder for .gpx files for flight tracks
FLOGGER_V_SMALL = 10.0                                          # Lowest moving speed to be considered as zero kph







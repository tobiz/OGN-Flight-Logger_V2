
#-------------------------------------
# OGN-Flight-Logger Settings
#-------------------------------------
# Python APRS/OGN program to log flight times, durations and maximum heights achieved
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
#-------------------------------------
#

# APRS_SERVER_HOST = 'rotate.aprs2.net'
# APRS_SERVER_PORT = 14580
APRS_SERVER_HOST = 'aprs.glidernet.org'
APRS_SERVER_PORT = 14580
APRS_USER = 'PythonEx'
# APRS_PASSCODE = 'Python Example App'
# APRS_PASSCODE = -1   #Read only
# APRS_PASSCODE = "rw"  #Read & write (for keepalive)
APRS_PASSCODE = 32229  # See http://www.george-smart.co.uk/wiki/APRS_Callpass
# Check that APRS_USER and APRS_PASSCODE are set
assert len(APRS_USER) > 3 and len(str(APRS_PASSCODE)) > 0, 'Please set APRS_USER and APRS_PASSCODE in settings.py.'
# aprs.glidernet.org on port 14580.
FLOGGER_DB_SCHEMA = "flogger_schema-0.0.1.sql"
FLOGGER_LATITUDE, FLOGGER_LONGITUDE = '+54.228833', '-1.209639'
FLOGGER_MIN_FLIGHT_TIME = "0:5:0" #hh:mm:ss
FLOGGER_KEEPALIVE_TIME = 900 # Interval in seconds for sending tcp/ip keep alive on socket connection
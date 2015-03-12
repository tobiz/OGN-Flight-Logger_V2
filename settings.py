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

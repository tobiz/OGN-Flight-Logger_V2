#
# This function determines if a flight has landed outside the airfield.
# The perimiter of the airfield is taken as circle based on the designated centre point
# of a specified radius. This is not the most accurate but will do to start with.
# If a flight lands outside the airfield then an SMS message with there landing coordinates
# is sent to a specified number.

import smtplib
import base64
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from __builtin__ import file
import  settings
import os
import datetime
from geopy.distance import vincenty
from flogger_get_coords import get_coords
from google.directions import GoogleDirections

def landout_check(flight_reg, af_centre, radius, landing_coords, mode):
    #
    #
    #
    print "landout_check called"
    landing_dist = vincenty(af_centre, landing_coords).meters
    print "Landing distance is: %d" % landing_dist
    if landing_dist <= radius:
        print "Landed in airfield"
        return False
    if mode == "SMS":
        #-----------------------------------
        # Send SMS Text Message using Python
        #
        # Author : Matt Hawkins
        # Site   : http://www.raspberrypi-spy.co.uk/
        # Date   : 01/04/2016
        #
        # Requires account with TxtLocal
        # http://www.txtlocal.co.uk/?tlrx=114032
        #
        #-----------------------------------
         
        # Import required libraries
        import urllib      # URL functions
        import urllib2     # URL functions
         
        # Set YOUR TextLocal username
        username = 'joebloggs@example.com'
         
        # Set YOUR unique API hash
        # It is available from the docs page
        # https://control.txtlocal.co.uk/docs/
        hash = '1234567890abcdefghijklmnopqrstuvwxyz1234'
         
        # Set a sender name.
        # Sender name must alphanumeric and 
        # between 3 and 11 characters in length.
        sender = 'RPiSpy'
        sender = settings.FLOGGER_YGC_ADMIN
         
        # Set flag to 1 to simulate sending
        # This saves your credits while you are
        # testing your code.
        # To send real message set this flag to 0
        test_flag = 1
         
        # Set the phone number you wish to send
        # message to.
        # The first 2 digits are the country code.
        # 44 is the country code for the UK
        # Multiple numbers can be specified if required
        # e.g. numbers = ('447xxx123456','447xxx654321')
        numbers = ('447xxx123456')
         
        # Define your message
        message = 'Test message sent from my Raspberry Pi'
         
        #-----------------------------------------
        # No need to edit anything below this line
        #-----------------------------------------
         
        values = {'test'    : test_flag,
                  'uname'   : username,
                  'hash'    : hash,
                  'message' : message,
                  'from'    : sender,
                  'selectednums' : numbers }
         
        url = 'http://www.txtlocal.com/sendsmspost.php'
         
        postdata = urllib.urlencode(values)
        req = urllib2.Request(url, postdata)
         
        print 'Attempt to send SMS ...'
         
        try:
          response = urllib2.urlopen(req)
          response_url = response.geturl()
          if response_url==url:
            print 'SMS sent!'
            return True
        except urllib2.URLError, e:
          print 'Send failed!'
          print e.reason
          return False
    
    if mode == "email":
        print "Send landout email"
        fromaddr = settings.FLOGGER_SMTP_TX
        toaddr = settings.FLOGGER_SMTP_RX
        msg = MIMEMultipart() 
        msg['From'] = fromaddr
        msg['To'] = toaddr
        txt = "Flight %s landed out at: %s, %s" % (flight_reg, str(landing_coords[0]), str(landing_coords[1]))
        msg['Subject'] =  txt 
        print "Email land out coordinates: ", txt
        body = txt
        msg.attach(MIMEText(body, 'plain'))    
        server = smtplib.SMTP(settings.FLOGGER_SMTP_SERVER_URL, settings.FLOGGER_SMTP_SERVER_PORT)
        text = msg.as_string()
    #    print "Msg string is: ", text
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
    return True

#
# Test call
#

#af_centre = get_coords(settings.FLOGGER_AIRFIELD_DETAILS)
#print "Airfield coords: ", af_centre
#radius = settings.FLOGGER_AIRFIELD_LIMIT
#radius = 44000
#mode = settings.FLOGGER_LANDOUT_MODE
#landing_coords = get_coords("Pocklington")
#print "Pocklington coords: ", landing_coords
#settings.FLOGGER_SMTP_SERVER_URL = "smtp.metronet.co.uk"
#settings.FLOGGER_SMTP_SERVER_PORT = 25
#settings.FLOGGER_SMTP_TX = "pjrobinson@metronet.co.uk"
#settings.FLOGGER_SMTP_RX = "pjrobinson@metronet.co.uk"
#landout_check("GB_JVC", af_centre, radius, landing_coords, mode)
        
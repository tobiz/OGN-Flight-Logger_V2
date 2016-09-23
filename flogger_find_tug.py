#
#-----------------------------------------------------------------
# Function to find whether a flight was launched by tug (tow plane).
# If yes then add tug registration an height at which glider was released
# 
# Note tug flights have to be recorded to determine this, ie setting.FLOGGER_LOG_TUGS = 'Y'
# 
#-----------------------------------------------------------------
#

import settings
import string
import datetime
import time
import sqlite3
import pytz
from datetime import timedelta
import sys
from flarm_db import flarmdb
from pysqlite2 import dbapi2 as sqlite
from open_db import opendb 

def find_tug(cursor, db):
    print "find_tug called"
#    cursor.execute('''SELECT DISTINCT id, stime, duration, registration, max_altitude FROM flight_log_final ''')
#    cursor.execute('''SELECT DISTINCT id, stime, duration, registration, max_altitude FROM flights ORDER by stime''')
    cursor.execute('''SELECT id, stime, duration, registration, max_altitude FROM flights ORDER by stime''')
    rows = cursor.fetchall()
    for row in rows:
#        print "Next row candidate for a tug is: ", row, " Type code is: ", settings.FLOGGER_FLEET_LIST[row[3]]
        # row[3] is the aircraft registration. Check whether it's a tug or not
        if settings.FLOGGER_FLEET_LIST[row[3]] > 100 and settings.FLOGGER_FLEET_LIST[row[3]] < 200 :
            # This is a tug flight
            print "Tug flight found: ", row   
            tug_time = datetime.datetime.strptime("1900/01/01 " + row[1], '%Y/%m/%d %H:%M:%S')  # Tug takeoff time
            flight_count = 0
            for flight in rows: 
#                print "Next row candidate for a glider is: ", flight       
                if settings.FLOGGER_FLEET_LIST[flight[3]] <= 100:
                    # This is a glider flight
#                    print "Glider flight found: ", flight
                    glider_time = datetime.datetime.strptime("1900/01/01 " + flight[1], '%Y/%m/%d %H:%M:%S')    # Glider takeoff time
                    tdelta_sec = (tug_time - glider_time).total_seconds()      # Difference between 2 times in seconds, note artificially same years, same month, same day
                    if abs(tdelta_sec) < settings.FLOGGER_DT_TUG_LAUNCH:                    
                        print "Delta flight times is: ", abs(tdelta_sec), " Glider reg: ", flight[3]
                        # Time difference between takeoff times of glider and tug are less than this (secs), hence assume tug launched glider
                        flight_id = flight[0]
                        flight_details = flight
                        flight_count += 1
            if flight_count > 1:
                print "Multiple glider flights for a tug flight found - must be false, ignore: ", flight_count
                continue
            if flight_count == 0:
                print "No glider flight found for Tug flight, details: ", row
                continue
            print "Single glider flight found. Glider details: ", flight_details, " Tug details: ", row, " Registration: ", row[3]
            tug_reg = row[3]
            cursor.execute('''SELECT aircraft_model FROM flarm_db WHERE registration=? ''', (tug_reg,))
            tug_model = cursor.fetchone()
            try:
                cursor.execute('''UPDATE flights SET tug_registration=?, tug_altitude=?, tug_model=? WHERE id=?''', (row[3], row[4], tug_model[0], flight_id))
                print "Tug model added to: ", flight_id, " Model: ", tug_model 
                db.commit()
            except:
                print "Failed to add tug model details to flights table for flight: ", flight_details, " tug_model: ", tug_model[0]
        else:
            continue
#            print "Not a tug: ", row
    return
            
        
        
    
    
    
    
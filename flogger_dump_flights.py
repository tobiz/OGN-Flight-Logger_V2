#
# This dumps the flights table to a csv file.  The file name is "todays_date_time"_flights.csv
#
import settings
import string
import datetime
import time
import sqlite3
import pytz
from datetime import timedelta
import csv

def dump_flights():
    print "Start flights table dump"
    db = sqlite3.connect(settings.FLOGGER_DB_NAME)
    #Get a cursor object
    cursor = db.cursor()
    
    cursor.execute('''SELECT max(sdate) FROM flights''')
    max_row = cursor.fetchone()
    if max_row <> (None,):
        max_date = datetime.datetime.strptime(max_row[0], "%y/%m/%d")
        print "Last record date in flights is: ", max_date
    else:
        print "No records in flights so set date to today"
        today = datetime.date.today().strftime("%y/%m/%d")
        max_date = datetime.datetime.strptime(today, "%y/%m/%d")
         
    cursor.execute("SELECT * FROM flights WHERE sdate=? ORDER by sdate, stime", (max_date,))
    
    
    start_time = datetime.datetime.now()
    csv_path = str(start_time) + "_flights.csv"
    print "csv file name is: ", csv_path
    
    with open(csv_path, "wb") as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write headers.
        print "Output header"
        csv_writer.writerow([i[0] for i in cursor.description])
        # Write data.
        print "Output data"
        csv_writer.writerows(cursor)
    print "End flights table dump"
    return

#dump_flights()
    
    
    
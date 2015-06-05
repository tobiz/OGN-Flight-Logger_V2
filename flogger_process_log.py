


import settings
import string
import datetime
import time
from time import mktime
import sqlite3
import pytz
from datetime import timedelta

#
#-----------------------------------------------------------------
# Process the log of each record in 'flight_log' into table 'flights'
# where each flight is take off to landing .
# Process_log assumes the database tables have been created in the 
# calling environment such that only the cursor to the database needs be passed
#-----------------------------------------------------------------
#
def process_log (cursor,db):
    MINTIME = time.strptime(settings.FLOGGER_MIN_FLIGHT_TIME, "%H:%M:%S")       # 5 minutes minimum flight time
    print "MINTIME is: ", MINTIME
    cursor.execute('''SELECT max(sdate) FROM flight_log''')
    row = cursor.fetchone()
    print "row is: ", row
    #    
    #-----------------------------------------------------------------
    # Phase 1 processing    
    #-----------------------------------------------------------------
    #
    # The following takes into account the situation when there are no records in flight_log
    # and there is therefore no highest date record. Note it does require that this code is
    # run on the same day as the flights are recorded in flight_log_final
    #
    # Note this may need revision for the case that the system is started before sunrise. Not sure
    #
    print "+++++++Phase 1 Start+++++++"
    if row <> (None,):
        max_date = datetime.datetime.strptime(row[0], "%y/%m/%d")
        print "Last record date in flight_log is: ", max_date
    else:
        print "No records in flight_log so set date to today"
        today = datetime.date.today().strftime("%y/%m/%d")
        max_date = datetime.datetime.strptime(today, "%y/%m/%d")
        
    print "max_date set to today: ", max_date
      
    
    cursor.execute('''SELECT sdate, stime, edate, etime, duration, src_callsign, max_altitude, speed, registration FROM flight_log_final''')
    data = cursor.fetchall()
    for row in data:
        print "Row is: sdate %s, stime %s, edate %s, etime %s, duration %s, src_callsign %s, altitude %s, speed %s, registration %s" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    #    print "Row is: sdate %s" % row[0] 
    #    print "stime %s " % row[1] 
    #    print "edate %s " % row[2]
    #    print "etime %s " % row[3]
    #    print "duration %s " % row[4]
    #    print "src_callsign %s " % row[5]
    #    print "altitude %s " % row[6]
    #    print "speed %s"  % row[7]
    #    print "registration %s" % row[8]
    
        time_str = row[4].replace("h", "")
        time_str = time_str.replace("m", "")
        time_str = time_str.replace("s", "")
        print "Duration now: ", time_str
        duration = time.strptime(time_str, "%H: %M: %S")
        
        strt_date = datetime.datetime.strptime(row[0], "%y/%m/%d")
        if strt_date >= max_date:
            print "**** Record start date: ", strt_date, " after last flight_log record, copy: ", max_date
            if duration > MINTIME:
                print "#### Copy record. Duration is: ", time_str
                cursor.execute('''INSERT INTO flight_log(sdate, stime, edate, etime, duration, src_callsign, max_altitude, speed, registration)
                                    VALUES(:sdate,:stime,:edate,:etime,:duration,:src_callsign,:max_altitude,:speed, :registration)''',
                                    {'sdate':row[0], 'stime':row[1], 'edate': row[2], 'etime':row[3],
                                    'duration': row[4], 'src_callsign':row[5], 'max_altitude':row[6], 'speed':row[7], 'registration':row[8]})
                print "Row copied"
            else:
                print "xxxx Flight duration less than or equal to MINTIME: ", duration, " Check altitude xxxx"
                # Note this needs a major enhancement to store the altitude at take off
                # For now make it simple. Needs better solution, eg add takeoff alt to db
                if row[6] <= FLOGGER_QNH + FLOGGER_QFE_MIN:
                    print "====Ignore row, flight time too short and too low. Time: ", row[4], " alt: ", row[6]
                else:
                    print "++++Accept row, short flight but ok min height. Time: ", row[4], " alt: ", row[6] 
                    cursor.execute('''INSERT INTO flight_log(sdate, stime, edate, etime, duration, src_callsign, max_altitude, speed, registration)
                                    VALUES(:sdate,:stime,:edate,:etime,:duration,:src_callsign,:max_altitude,:speed, :registration)''',
                                    {'sdate':row[0], 'stime':row[1], 'edate': row[2], 'etime':row[3],
                                    'duration': row[4], 'src_callsign':row[5], 'max_altitude':row[6], 'speed':row[7], 'registration':row[8]})
        else:
            print "???? Record start date: ", strt_date, " before last flight_log record, ignore: ", max_date
    print "-------Phase 1 End--------"
    db.commit()  
    #    
    #-----------------------------------------------------------------
    # Phase 2 processing    
    #-----------------------------------------------------------------
    #
    # Phase 2 processing
    # For some records for each flight the end time and next start time are too close together
    # to be independent flights.
    # This phase examines all the records and puts them into groups such that each group has 
    # an end and start time, such that they are distinct flights ie their end and start times are greater than
    # TIME_DELTA, and not just therefore data
    # jiggles (eg moving moving the plane to a new position on the flight line),
    # ie the end and start time of subsequent flights is such that it couldn't have been a real flight
    
    print "+++++++Phase 2 Start+++++++"
    TIME_DELTA = "0:2:0"        # Time in hrs:min:sec of shortest flight
    #
    # Note the following code processes each unique or distinct call_sign ie each group
    # of flights for a call_sign
    # SELECT DISTINCT call_sign FROM flight_log
    # rows = cursor.fetchall()
    # for call_sign in rows
    
    group = 0                   # Number of groups set for case there are none
    cursor.execute('''SELECT DISTINCT src_callsign FROM flight_log ORDER BY sdate, stime ''')
    all_callsigns = cursor.fetchall()
    print "All call_signs: ", all_callsigns
    for acallsign in all_callsigns:
        if group == 0:
            print "GroupId set to 1"    # Must be at least 1 group since select is not empty 
            group = 1
        call_sign = ''.join(acallsign)                   # callsign is a tuple ie (u'cccccc',) converts ccccc to string
        print "Processing for call_sign: ", call_sign
#        cursor.execute('''SELECT sdate, stime, edate, etime, duration, src_callsign, max_altitude 
#                       FROM flight_log WHERE src_callsign=?
#                       ORDER BY sdate, stime ''', (call_sign,)) 
        #for row in rows: 
#        row_count = len(cursor.fetchall())
#        print "nos rows is: ", row_count 
          
        cursor.execute('''SELECT sdate, stime, edate, etime, duration, src_callsign, max_altitude, registration 
                     FROM flight_log WHERE src_callsign=?
                     ORDER BY sdate, stime ''', (call_sign,))
        
        rows = cursor.fetchall()
#        row_count = len(cursor.fetchall())
        row_count = len(rows)
        print "Number of rows is: ", row_count
        
# Just for testing Start
        n = 1
        for row in rows:
            print "Row ", n, " is: ", row
            n = n + 1
# Just for testing End

        i = 0                   # First index in a list is 0
#        group = 1               # group is used as the identifier of flights in a group
        for r in rows:          # This will cycle through all the rows of the select statement
#        while i <= row_count: 
            try:
#                 row_0 = cursor.next()
#                 row_1 = cursor.next()
                 row_0 = rows[i]
                 row_1 = rows[i + 1]
                 print "Row pair: ", i
                 print "row_", i, " is: ", row_0
                 print "row_", i + 1, " is: ", row_1
                 time.strptime(TIME_DELTA, "%H:%M:%S")
                 time_delta = datetime.datetime.strptime(row_1[1], "%H:%M:%S") - datetime.datetime.strptime(row_0[3], "%H:%M:%S")
                 delta_secs = time_delta.total_seconds()
                 time_lmt = datetime.datetime.strptime(TIME_DELTA, "%H:%M:%S") - datetime.datetime.strptime("0:0:0", "%H:%M:%S")
                 lmt_secs = time_lmt.total_seconds()
                 print "Delta secs is: ", delta_secs, " Time limit is: ", lmt_secs     
                 # Create a group record for 1st record's data                 
                 cursor.execute('''INSERT INTO flight_group(groupID, sdate, stime, edate, etime, duration, src_callsign, max_altitude, registration)
                                    VALUES(:groupID,:sdate,:stime,:edate,:etime,:duration,:src_callsign,:max_altitude, :registration)''',
                                    {'groupID':group, 'sdate':row_0[0], 'stime':row_0[1], 'edate': row_0[2], 'etime':row_0[3],
                                    'duration': row_0[4], 'src_callsign':row_0[5], 'max_altitude':row_0[6], 'registration': row_0[7]})
                 print "GroupID: ", group, " record created ", row_0                
                 if (delta_secs) < lmt_secs:
                     print "++++Same flight"
                     # Record created in flight_group table with current groupID, next record will have same groupID              
                 else:
                     # Different flight so start next group ID
                     print "----Different flight" 
                     # Record created in flight_group table with current groupID but next record processed will have next groupID
                     group = group + 1  
                 i = i + 1
                 print "Number of groups is: ", group, " Row count i is: ", i 
            except IndexError:
                 print "IndexError. Access index greater than: ", i
                 print "GroupID: ", group, " record created ", row_0                
                 # Index error on accessing rows[i+1] but row_0 not written yet                                
                 cursor.execute('''INSERT INTO flight_group(groupID, sdate, stime, edate, etime, duration, src_callsign, max_altitude, registration)
                                VALUES(:groupID,:sdate,:stime,:edate,:etime,:duration,:src_callsign,:max_altitude, :registration)''',
                                {'groupID':group, 'sdate':row_0[0], 'stime':row_0[1], 'edate': row_0[2], 'etime':row_0[3],
                                'duration': row_0[4], 'src_callsign':row_0[5], 'max_altitude':row_0[6], 'registration': row_0[7]})
                 group = group + 1 
                 print "GroupID now: ", group

    db.commit()
    print "-------Phase 2 End-------"
    #    
    #-----------------------------------------------------------------
    # Phase 3 processing    
    #-----------------------------------------------------------------
    #
    # Phase 3.  This sums the flight durations for each of the flight groups
    # hence resulting in the actual flight start, end times and duration
    print "+++++++Phase 3 Start+++++++"
    
    #
    # This function since I can't find a library function that does what I want; dates & times
    # are very confusing in Python!
    #
    def time_add(t1, t2):
        ts = 0
        tm = 0
        th = 0
        t = t1[5] + t2[5]
        if t >= 60:
            ts = t - 60
            tm = int(t / 60)
        else:
            ts = t
        t = t1[4] + t2[4] + tm
        if t >= 60:
            tm = t - 60
            th = int(t/60)
        else:
            tm = t
        th = t1[3] + t2[3] + th
        print "Time tuple is: ", (th, tm, ts)
        tstring = "%s:%s:%s" % (th, tm, ts)
        print "tstring is: ", tstring
        time_return = time.strptime(tstring, "%H:%M:%S")
        return time_return
        
    if group <> 0:    
#       max_groupID = group - 1   
        max_groupID = group 
        print "Max groupID is: ", max_groupID
    else:
        print "No groups to process"
        print "Done"
        return
    
    i = 1
    while i < max_groupID:
        
        cursor.execute('''SELECT max(max_altitude) FROM flight_group WHERE groupID=? ''', (i,))
        r = cursor.fetchone()
        max_altitude = r[0]
        print "Max altitude from group: ", i, " is: ", r[0]

#
# New way of doing it
#          
        # A multi row group can have a total flight time, where flight time is the
        # sum of the row durations, less than the difference between the start and end time of the group
        # since landing and takeoff times less the 2min (say) are being counted as a single flight.
        # It can be argued that the actual flight time should be the difference between the group start and
        # end times, if it isn't the final data will seem to have errors.
        # Hence check for a multi row group and if yes then use max(etime) - min(stime).
        # Good news is the summation code can be removed!
        # Do:
        # rows = cursor.fetchall()
        # row_count = len(cursor.fetchall())
        # if row_count > 1:
        # cursor.execute('''SELECT min(stime), max(etime) FROM flight_group WHERE groupID=? ''', (i,))
        # row = cursor.fetchone()
        # total_duration = row[1] - row[0]
        # But beware of the subtaction being ok and getting the time in the right format in the end
        
        cursor.execute('''SELECT sdate, stime, edate, etime, duration, src_callsign, max_altitude, registration
                     FROM flight_group WHERE groupID=?
                     ORDER BY sdate, stime ''', (i,))
        rows = cursor.fetchall()
        row_count = len(rows)
        if row_count > 1:
            # Multi row group
            print "Multi row group size: ", row_count
        else:
            # Single row group, ie single flight
            print "Single row group size: ", row_count
        
        cursor.execute('''SELECT min(stime), max(etime) FROM flight_group WHERE groupID=?''', (i,))
        times = cursor.fetchone()
        try:
            print "stime is: ", times[0], "etime is: ", times[1]
            stime = datetime.strptime(times[0], "%H:%M:%S")
            etime = datetime.strptime(times[1], "%H:%M:%S")  
            print "stime is: ", stime, " etime is: ", etime  
            try:
                duration = etime - stime
                print "subtract failed for: ", etime, " from: ", stime
            except:
                print "subtract failed for duration = etime - stime: "
        except:
            print "Min/max time processing failed"
            
        # Each set of group records has same value for sdate, edate, callsign and registration 
        try:              
            cursor.execute('''SELECT DISTINCT sdate, edate, src_callsign, registration FROM flight_group WHERE groupID=?''', (i,))
            data = cursor.fetchone()
            print "Flight results for group: ", i, " is: ", data
            sdate           = data[0]
            edate           = data[1]
            callsign        = data[2]
            registration    = data[3]
        except:
            print "Group data selection failed"

#
# Old way of doing it
#            
        cursor.execute('''SELECT sdate, stime, edate, etime, duration, src_callsign, max_altitude, registration
                     FROM flight_group WHERE groupID=?
                     ORDER BY sdate, stime ''', (i,))        
        rows = cursor.fetchall()
          
        total_duration = time.strptime("0:0:0", "%H:%M:%S")
    #    print "total duration tuple is: ", total_duration
    #    total_duration = time.mktime(total_duration)
    #    print "Initial time is: ", total_duration
        for row in rows:
            print "Goup: ", i, " row: ", row
            flight_duration = time.strptime(row[4], "%H: %M: %S")
    #        print "total duration is: ", total_duration
    #        print "flight duration is: ", flight_duration
            total_duration = time_add(total_duration, flight_duration)
    #        print "total time is: ", total_duration
            t_d = "%s:%s:%s" % (total_duration[3],total_duration[4],total_duration[5])
            print "total time is: ", t_d
            sdate = row[0]
            edate = row[2]
            callsign = row[5]       
            print "@@@@@ Next row @@@@@@@"
            
        cursor.execute('''SELECT min(stime), max(etime) FROM flight_group WHERE groupID=? ''', (i,))      
        r = cursor.fetchone()
        print "Start time is: ", r[0], " End time is: ", r[1], " Duration is: ", total_duration 
        cursor.execute('''INSERT INTO flights(sdate, stime, edate, etime, duration, src_callsign, max_altitude, registration)
                                    VALUES(:sdate,:stime,:edate,:etime,:duration,:src_callsign,:max_altitude, :registration)''',
                                    {'sdate':sdate, 'stime':r[0], 'edate': edate, 'etime':r[1],
                                    'duration': t_d, 'src_callsign':callsign, 'max_altitude':max_altitude, 'registration':row[7]}) 
        db.commit()
        i = i + 1
        print "*****Flight logged to flights*********"
    print "-------Phase 3 End--------"
    return
    
        
        
    
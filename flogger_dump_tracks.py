
import settings
import string
import datetime
import time
from time import mktime
import sqlite3
import pytz
from datetime import timedelta
from gpxTracks import gpxTrack
import os

#
#-----------------------------------------------------------------
# Process the track table for each flight and convert to a .gpx format file
# Tracks can be viewed in http://www.mygpsfiles.com/app/
# 
# 
#-----------------------------------------------------------------
#

def dump_tracks(cursor):
    print "-------Start dump tracks to gpx file--------"
    if settings.FLOGGER_TRACKS == "Y":
        # This has to change as id in flights is not same as id in flight_log2
        # as the flights table is a processed version of flight_log2, ie deletes short flights (data jitter)
        # and amalgamates others. Correction is to take id in flight_log2 and pass through groups table to flights table
        # For now will dump as gpx some of the tracks but not all (all of the time)
        
        if not os.path.isdir(settings.FLOGGER_TRACKS_FOLDER):  # Create track folder if doesn't exist 
            os.makedirs(settings.FLOGGER_TRACKS_FOLDER)
        
        start_time = datetime.datetime.now()
        gpx_path = str(start_time)
        gpx_path = gpx_path[0:10]
            
        cursor.execute('''SELECT id, sdate, stime, duration, registration, max_altitude FROM flights ORDER BY flight_no, sdate, stime''')
        flights = cursor.fetchall()
        for row in flights:
            flight_no = row[0]
            sdate = row[1]
            stime = row[2]
            duration = row[3]
            registration = row[4]
            max_altitude = row[5]
            cursor.execute('''SELECT latitude,longitude,altitude,course,speed,timeStamp 
                                FROM track WHERE flight_no=? ORDER BY track_no''', (flight_no,))
#            track_file_name = settings.FLOGGER_TRACKS_FOLDER + "/" + str(datetime.datetime()) + "_" + str(flight_no) + "_" + "track.gpx"
#            track_file_name = settings.FLOGGER_TRACKS_FOLDER + "/" + gpx_path + str(flight_no) + "_" + "track.gpx"
            track_file_name = "%s/%s_track%d.gpx" % (settings.FLOGGER_TRACKS_FOLDER, gpx_path, flight_no)

            
            tracks = cursor.fetchall()
            print "Flight number is: ", flight_no, " Track file name is: ", track_file_name, " Number of track points is: ", len(tracks)
            nxt_track = gpxTrack(flight_no, track_file_name, "test", sdate, stime, duration, registration, max_altitude)
            nxt_track.AddTrackSeg("Track1") 
            for track_point in tracks:
                 latitude = track_point[0]
                 longitude = track_point[1]
                 altitude = track_point[2]
#                 course = track_point[3]
#                 speed = track_point[4]
                 timeStamp = track_point[5]
                 nxt_track.AddTrackPnt(longitude, latitude, altitude, timeStamp)
            nxt_track.EndTrackSeg()
            nxt_track.EndTrack()    
        print "-------End dump tracks to gpx file--------"
        
        print "-------Start new dump tracks to gpx file from trackFile table--------"

        dump_tracks2(cursor)
        print "-------End new dump tracks to gpx file from trackFile table--------"
  
    else:
        print "No tracks to dump"
    return

def dump_tracks2(cursor):
    print "-------dump_tracks2 Start new dump tracks to gpx file from trackFile table--------"
    if settings.FLOGGER_TRACKS == "Y":
        # This has to change as id in flights is not same as id in flight_log2
        # as the flights table is a processed version of flight_log2, ie deletes short flights (data jitter)
        # and amalgamates others. Correction is to take id in flight_log2 and pass through groups table to flights table
        # For now will dump as gpx some of the tracks but not all (all of the time)
        
        if not os.path.isdir(settings.FLOGGER_TRACKS_FOLDER):  # Create track folder if doesn't exist 
            os.makedirs(settings.FLOGGER_TRACKS_FOLDER)
        
        start_time = datetime.datetime.now()
        gpx_path = str(start_time)
        gpx_path = gpx_path[0:10]
            
        cursor.execute('''SELECT DISTINCT flight_no FROM trackFinal ORDER BY flight_no''')
        flights = cursor.fetchall()
        if flights <> None:
            print "Number of flights in trackFinal is: ", len(flights)
            for aflight in flights:
                flight_no = aflight[0]
                track_file_name = "%s/%s_track.new%d.gpx" % (settings.FLOGGER_TRACKS_FOLDER, gpx_path, flight_no)
                print "New trackfile name is: ", track_file_name, " This flight is: ", flight_no
                cursor.execute('''SELECT sdate, stime, duration, registration, max_altitude FROM flights WHERE flight_no=?''', (flight_no,))
                flight_data = cursor.fetchone()
                if flight_data <> None:  
                    print "Flight_data is: ", flight_data
                    sdate = flight_data[0]
                    stime = flight_data[1]
                    duration = flight_data[2]
                    registration = flight_data[3]
                    max_altitude = flight_data[4]
                    cursor.execute('''SELECT flight_no, track_no, latitude,longitude,altitude,course,speed,timeStamp 
                                            FROM trackFinal WHERE flight_no=? ORDER BY flight_no, track_no''', (flight_no,))
                    tracks = cursor.fetchall()
                    nxt_track = gpxTrack(flight_no, track_file_name, "test", sdate, stime, duration, registration, max_altitude)
                    nxt_track.AddTrackSeg("Track1") 
                    for track_point in tracks:
                        flight_nos = track_point[0]
                        track_nos = track_point[1]
                        latitude = track_point[2]
                        longitude = track_point[3]
                        altitude = track_point[4]
        #                 course = track_point[5]
        #                 speed = track_point[6]
                        timeStamp = track_point[7]
                        nxt_track.AddTrackPnt(longitude, latitude, altitude, timeStamp)
                    nxt_track.EndTrackSeg()
                    nxt_track.EndTrack()
                                   
                    #
                    # Insert the track file name into the record for this flight
                    #            
                    print "Updating flights table, flight_no: ", flight_no, "track_file_name: ", track_file_name
                    cursor.execute('''UPDATE flights SET track_file_name=? WHERE flight_no=?''', (track_file_name, flight_no)) 
#                    cursor.commit()
                else:
                    print "No flight data in Flights table" 
        else:
            print "No flights in Trackfinal table"  
    else:
        print "Config says: No tracks to dump"
    return
#
# This program reads records from the OGN network processing only
# those received from a specified site and registration marks, the the
# gliders belonging to the club.
# It writes each record to a database and at the end of each day process
# them to determine the flight times of each flight for each machine.
# Phase 1 will just collect the data. 
# Phase 2 will process the data into a new table
# Phase 3 will then format that information with the intention of
# it being used to be checked against the manual log books.
# The intention is that it will collect the data between the hours of daylight, 
# producing the summary at the end of the day.
# This program could be run on a Raspberry Pi as it is so low powered
#
# Altitude in metres.
# Land speed in km/h.
# Latitude, west is negative decimal degrees.
# Longitude, south is negative decimal degrees.
#
# 20150312: 	First working version
# Usage: 		Run flogger.py to collect the daily flight data then
#        		run process.py which processes the raw data into a table flights in the database flogger.sgl3
#				This first version is very experimental, it is proof of concept and processes. The code needs to
#				be 'improved'.
# To be done:	1) The program should be run each day between 0900 and sunset. This should be handled by cron
#				   to start the program and the program determining sunset and stopping itself. It also needs
#				   to handle power outages (not sure how at the moment)
#				2) The Flarm code to registration code needs to addressed using OGNs new database.
#

import socket

from libfap import *
import settings
import string
import datetime
import time
import sqlite3
import pytz
from datetime import timedelta
import sys


prev_vals = {'latitude': 0, 'longitude': 0, "altitude": 0, "speed": 0}
nprev_vals = 	{"G-CKLW": {'latitude': 0, 'longitude': 0, "altitude": 0, "speed": 0, 'maxA': 0},
				 "G-CKFN": {'latitude': 0, 'longitude': 0, "altitude": 0, "speed": 0, 'maxA': 0}
				 }
values = {'latitude': 0, 'longitude': 0, "altitude": 0, "speed": 0}
nvalues = 	{"G-CKLW": {'latitude': 0, 'longitude': 0, "altitude": 0, "speed": 0, 'maxA': 0},
		     "G-CKFN": {'latitude': 0, 'longitude': 0, "altitude": 0, "speed": 0, 'maxA': 0}
				}

L_SMALL = float(0.001)  	# Small latitude or longitude delta of a 0.001 degree
A_SMALL = float(0.01)  		# Small altitude delta of 0.01 a metre, ie 1cm
V_SMALL = float(10.0)		# Small velocity delta of 10.0 kph counts as zero ie not moving
QNH = 300 					# ASL for Sutton Bank(max 297m) in metres
frst_time = False
AIRFIELD = "SuttonBnk"
# Coded 	001-099: Gliders, 
# 			101-199: Tugs, 
# 			201-299: Motor Gliders, 
# 			301-399: Other
aircraft = {"G-CKLW": 1, "G-CKLN": 2, "G-CJVZ": 3, "G-CHEF": 4, "G-CKFN": 5,
			"G-CHVR": 6, "G-CKJH": 7, "G-CKRN": 8, "G-CGBK": 9, "G-CDKC": 10,
			"G-BFRY": 101, "G-BJIV": 102, "G-MOYR": 103,
			"G-OSUT": 201,
			"FLRDDF9C4": 301, "FLRDDE5FC": 302, "FLRDDBF13": 303, "FLRDDA884": 304, "FLRDDA886": 305, "FLRDDACAE": 306, "FLRDDA7E9": 307,
			"FLRDDABF7": 308, "FLRDDE671": 309} 


	
	
# FILTER = "\'user %s pass %s vers Python_Example 0.0.1 filter e/" + AIRFIELD + "\\n\'" + " % (settings.APRS_USER, settings.APRS_PASSCODE)"

		
# sock.send('user %s pass %s vers Python_Example 0.0.1 filter e/Bicester\n' % (settings.APRS_USER, settings.APRS_PASSCODE) )	


# print "Filter is: ", FILTER

def CheckPrev(callsignKey, dataKey, value):
	print "CheckVals if callsign in nprev_vals: ", callsignKey, " key: ", dataKey, " Value: ", value 
	if nprev_vals.has_key(callsignKey) == 1:
		print "nprev_vals already has entry: ", callsignKey
	else:
		print "nprev_vals doesn't exist for callsignKey: ", callsignKey
		nprev_vals[callsignKey] = {}
		nprev_vals[callsignKey] = {'latitude': 0, 'longitude': 0, "altitude": 0, "speed": 0, 'maxA': 0}
		nprev_vals[callsignKey][dataKey] = value
		print "nprev_vals for callsignKey: ", callsignKey, " is: ", nprev_vals[callsignKey]
		print "nprev_vals is now: ", nprev_vals
	return

def CheckVals(callsignKey, dataKey, value):
	print "CheckVals if callsign in nvalues: ", callsignKey, " key: ", dataKey, " Value: ", value 
	if nvalues.has_key(callsignKey) == 1:
		print "nvalues already has entry: ", callsignKey
	else:
		print "nvalues doesn't exist for callsignKey: ", callsignKey
		nvalues[callsignKey] = {}
		nvalues[callsignKey] = {'latitude': 0, 'longitude': 0, "altitude": 0, "speed": 0, 'maxA': 0}
		nvalues[callsignKey][dataKey] = value
		print "nvalues for callsignKey: ", callsignKey, " is: ", nvalues[callsignKey]
		print "nvalues is now: ", nvalues
	return

def isDayLight ():
	return True

def fleet_check(call_sign):
	if aircraft.has_key(call_sign):
		return True
	else:
		return False
	
def comp_vals(set1, set2):
	# Works out if the difference in positions is small and both speeds are close to zero
	# Return True is yes and False if no
	# Set1 are new values, set2 old values
	print "Set1 value for key latitude is: ", set1["latitude"], " value: ", float(set1["latitude"])
# 	lat1 = float(set1["latitude"])
# 	lat2 = float(set2["latitude"])
	delta_latitude = float(set1["latitude"]) - float(set2["latitude"])
	delta_longitude = float(set1["longitude"]) - float(set2["longitude"])
	delta_altitude = float(set1["altitude"]) - float(set2["altitude"])
	delta_speed = float(set1["speed"]) - float(set2["speed"])
	print "Delta positions. Lat: ", delta_latitude, " Long: ", delta_longitude, " Alt: ", delta_altitude, " Speed: ", delta_speed 
# 	if (delta_latitude < L_SMALL) and (delta_longitude < L_SMALL) and (delta_altitude < A_SMALL) and (delta_speed < V_SMALL):
	if delta_speed <> 0.0:
		print "Delta speed not zero, check others"
# 	if (delta_latitude == 0.0) and (delta_longitude == 0.0) and (delta_altitude == 0.0) and (delta_speed == 0.0):
		if (delta_latitude == 0.0) and (delta_longitude == 0.0) and (delta_altitude == 0.0):
			print "Positions same"
			return True
		else:
			print "Positions different"
			return False
	else:
		print "Delta speed zero, return same"
		return True
	
def set_keepalive(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.

    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds
    """
    print "set_keepalive for idle after: ", after_idle_sec
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)
    return
	

def is_dst(zonename):
	# Determine if in daylight
    tz = pytz.timezone(zonename)
    now = pytz.utc.localize(datetime.utcnow())
    return now.astimezone(tz).dst() != timedelta(0)
   
def fleet_check_new(callsign):
	cursor.execute('''SELECT ROWID FROM aircraft WHERE registration =? or flarm_id=? ''', (callsign,callsign,))
	row = cursor.fetchone()
	if row <> None:
#	for r in row:
		print "Aircraft: ", callsign, " found at: ", row[0]
		return True
	else:
		print "Aircraft: ", callsign, " not found"
		cursor.execute('''INSERT INTO aircraft(registration,type,model,owner,airfield ,flarm_id)
							VALUES(:registration,:type,:model,:owner,:airfield,:flarm_id)''',
							{'registration':callsign, 'type':"", 'model': "", 'owner':"",'airfield': "Sutton Bank", 'flarm_id':callsign})
		return True
	
def callsign_trans(callsign):
	cursor.execute('''SELECT registration, flarm_id FROM aircraft WHERE registration =? or flarm_id=? ''', (callsign,callsign,))
	row = cursor.fetchone()
	# Check whether registration and flarm_id are the same value 
	if row[0] <> row[1]:
		# They aren't the same so use registration
		return row[0]
	else:
		# The are the same so use flarm_id
		return callsign
	


# Creates or opens a file called flogger.sql3 as an SQLite3 DB
try:
    # Creates or opens a file called mydb with a SQLite3 DB
    db = sqlite3.connect('flogger.sql3')
    # Get a cursor object
    cursor = db.cursor()
    # Check if table users does not exist and create it if not
    cursor.execute('''CREATE TABLE IF NOT EXISTS
                      users(id INTEGER PRIMARY KEY, first_name TEXT, surname TEXT, phone TEXT, email TEXT unique, password TEXT)''')
    # Check if table for holding flight logging data exist and create it not
#    cursor.execute('''CREATE TABLE IF NOT EXISTS
#                      flight_log(id INTEGER PRIMARY KEY, date TEXT, time TEXT, src_callsign TEXT, 
#                      			reg_no TEXT, latitude TEXT, longitude TEXT, altitude TEXT, course TEXT, speed TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS
    					aircraft(id INTEGER PRIMARY KEY,registration TEXT,type TEXT,model TEXT,owner TEXT,airfield TEXT,flarm_id TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS
    					flight_times(id INTEGER PRIMARY KEY,registration TEXT,type TEXT,model TEXT,
    						flarm_id TEXT,date, TEXT,start_time TEXT,duration TEXT,max_altitude TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS
    					flight_log2(id INTEGER PRIMARY KEY AUTOINCREMENT, sdate TEXT, stime TEXT, edate TEXT, etime TEXT, duration TEXT,
    					src_callsign TEXT, max_altitude TEXT, speed TEXT)''')	
    cursor.execute('''CREATE TABLE IF NOT EXISTS
    					flight_log_final(id INTEGER PRIMARY KEY, sdate TEXT, stime TEXT, edate TEXT, etime TEXT, duration TEXT,
    					src_callsign TEXT, max_altitude TEXT, speed TEXT)''')			
    
#    for k, v in aircraft.iteritems():
#		print "Key is: ", k, " value is: ", v
#		cursor.execute('''INSERT INTO aircraft(registration,type,model,owner,airfield ,flarm_id)
#							VALUES(:registration,:type,:model,:owner,:airfield,:flarm_id)''',
#							{'registration':k, 'type':"", 'model': "", 'owner':"",'airfield': "Sutton Bank", 'flarm_id':k})

    # Commit the changes
    db.commit()
# Catch the exception
except Exception as e:
    # Roll back any change if something goes wrong
    db.rollback()
    raise e
# finally:
    # Close the db connection
#    db.close()
print "Database and tables open"    

# create socket & connect to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
set_keepalive(sock, after_idle_sec=60, interval_sec=3, max_fails=5)
sock.connect((settings.APRS_SERVER_HOST, settings.APRS_SERVER_PORT))
print "Socket sock connected"

# logon to OGN APRS network	
# sock.send('user %s pass %s vers Python_Example 0.0.1 filter e/SuttonBnk\n ' % (settings.APRS_USER, settings.APRS_PASSCODE) )
sock.send('user %s pass %s vers Python_Example 0.0.1 filter r/+54.228833/-1.209639/25\n ' % (settings.APRS_USER, settings.APRS_PASSCODE))	
# print 'user %s pass %s vers Python_Example 0.0.1 filter %s ' % (settings.APRS_USER, settings.APRS_PASSCODE, settings.APRS_FILTER) 
# filter =  'user %s pass %s vers Python_Example_0.0.1 filter %s' % (settings.APRS_USER, settings.APRS_PASSCODE, settings.APRS_FILTER)
# print "Filter string is: ", filter
# sock.send('user %s pass %s vers Python_Example 0.0.1 filter %s' % (settings.APRS_USER, settings.APRS_PASSCODE, settings.APRS_FILTER) )	
# sock.send(filter)
# 54.13.728N  001.12.580W 
# r/33/-96/25
# r/54.13.728/-001.12.580/25 # 25Km of Sutton Bank
# 54.228833,-1.209639

# Make the connection to the server
start_time = datetime.datetime.now()
keepalive_time = time.time()
sock_file = sock.makefile()
print "libfap_init"
libfap.fap_init()

SB_DATA = "SB_data" + str(start_time)
#SB_DATA = "SB_data2015-03-05 14:57:27.980999"
print "SB data file is: ", SB_DATA

SB_Log = "SB_Log" + str(start_time)
#sys.stdout = open(SB_Log, 'w')
#print "Datafile open"
test = False
if test == True:
	datafile = open (SB_DATA, 'rw')
	print "In test mode"
else:
	datafile = open (SB_DATA, 'w')
	print "In live mode"
i = 0
try:
	while 1:
# 	for i in range(1000000):
		i = i + 1
		current_time = time.time()
		elapsed_time = int(current_time - keepalive_time)
 		print "Elapsed time is: ", elapsed_time
		if (current_time - keepalive_time) > 900:
			try:
				print "Socket open for: ", (current_time - keepalive_time), " seconds, send keepalive"
				rtn = sock_file.write("#Python Example App\n\n")
				sock_file.flush()  # Make sure it gets sent
				print "Send keepalive", elapsed_time, " rtn is: ", rtn
				keepalive_time = current_time
			except Exception, e:
				print ('something\'s wrong with socket write. Exception type is %s' % (`e`))
		else:
			print "No keepalive sent"
				
		print "In while loop. Count= ", i
		try:
			if test == False:
				# In live mode so use socket read
				print "Read socket"
				packet_str = sock_file.readline()
				datafile.write(packet_str)
			else:
				# In test mode so file read
				packet_str = datafile.readline()
		except socket.error:
			print "Socket error on readline"
			
		print "packet string length is: ", len(packet_str), " packet is: ", packet_str
		try:
			len_packet_str = len(packet_str)
		except TypeError:
			packet_str_hex = ":".join("{:02x}".format(ord(c)) for c in packet_str)
			len_packet_str = len(packet_str_hex) / 3
			print "TypeError on packet_str length. Now is: ", len_packet_str
		
		if len_packet_str == 0:
			# create new socket & connect to server
			print "Read returns zero length string on iteration: ", i
			try:
				sock.shutdown(0)
			except socket.error, e:
				if 'not connected' in e:
					print '*** Transport endpoint is not connected ***'
				print "socket no longer open so can't be closed, create new one"	
			else:
				print "Socket still open so close it"
				sock.close()
			print "Create new socket"
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((settings.APRS_SERVER_HOST, settings.APRS_SERVER_PORT))		
			sock.send('user %s pass %s vers Python_Example 0.0.1 filter r/+54.228833/-1.209639/25\n ' % (settings.APRS_USER, settings.APRS_PASSCODE))
			# Make the connection to the server
			sock_file = sock.makefile()
# Delete following line when not running in test mode
#			exit()
			continue
		
		# Parse the returned packet into fields
		packet = libfap.fap_parseaprs(packet_str, len(packet_str), 0)
		print '%s %s' % (packet[0].src_callsign, packet[0].body)
		try:
			error_code = packet[0].error_code[0]
		except ValueError:
			x = 0
# 			print "Error_code is NULL pointer ignore"
		else:
			x = 0
# 			print "Error_code is: ", packet[0].error_code[0]
			
# 		print "error_message is(type=c_char_p): ", packet[0].error_message
		try:
			type = packet[0].type[0]
		except ValueError:
			print "Type is NULL pointer ignore"
		else:
			x = 0 
		src_callsign = packet[0].src_callsign
		dest_callsign = packet[0].dst_callsign
		try:
			path = packet[0].path[0]
		except ValueError:
			x = 0
# 			print "Path is NULL pointer ignore"
		else:
			x = 0 
# 			print "Path is: ", packet[0].path[0]		
		try:
			latitude = packet[0].latitude[0]
		except ValueError:
			x = 0
# 			print "Latitude is NULL pointer"
		else:
# 			print "Latitude is: ", packet[0].latitude[0]
# 			nvalues[src_callsign]["latitude"] = latitude
			CheckVals(src_callsign, "latitude", latitude)
				
		try:
			longitude = packet[0].longitude[0]
		except ValueError:
			x = 0
# 			print "Longitude is NULL pointer"
		else:
# 			print "Longitude is: ", packet[0].longitude[0]
			nvalues[src_callsign]["longitude"] = longitude
				
		try:
			altitude = packet[0].altitude[0]
		except ValueError:
			x = 0
# 			print "Altitude is NULL pointer"
		else:
# 			print "Altitude is: ", packet[0].altitude[0]
			nvalues[src_callsign]["altitude"] = altitude	
				
		try:
			course = packet[0].course[0]
		except ValueError:
			course = 0
# 			print "Course is NULL pointer, set to 0"
		else:
			x = 0
# 			print "Course is: ", packet[0].course[0]
							
		try:
			speed = packet[0].speed[0]
		except ValueError:
			speed = 0
# 			print "Speed is NULL pointer, set to 0"
		else:
# 			print "Speed is: ", packet[0].speed[0]
			nvalues[src_callsign]["speed"] = speed		
				  
# 		ti = datetime.datetime.now()

# 		src_callsign = packet[0].src_callsign
# 		res = string.find(str(src_callsign), "None")
# 		res = string.find(str(packet[0].src_callsign), "None")
# 		if res == -1:
		# Test the packet to be one for the required field
		res1 = string.find(str(packet_str), "# aprsc")
		res2 = string.find(str(packet_str), "# logresp")
		res3 = string.find(str(packet_str), "SuttonBnk")
		if res1 <> -1 :
			print "Comment aprs packet returned: ", packet_str
			print "-----------------End of Packet: ", i, " ------------------------------"	
			continue
		if res2 <> -1 :
			print "Comment logresp packet returned: ", packet_str
			print "-----------------End of Packet: ", i, " ------------------------------"	
			continue
		if res3 <> -1 :
			print "---------!!!!!! Comment Sutton Bank packet returned: ", packet_str	
			src_callsign = packet[0].src_callsign
			res = string.find(str(packet[0].src_callsign), "None")
			if string.find(str(packet_str), "GLIDERN1") <> -1 or string.find(str(packet_str), "GLIDERN2") <> -1:
# 			if res == -1:
				print "Sutton Bank beacon packet, ignore: ", str(packet_str)
				print "-----------------End of Packet: ", i, " ------------------------------"	
				continue
			else:
				print "Sutton Bank aircraft position packet: ", src_callsign
		else:
			print "No match ", packet_str
			print "-----------------End of Packet: ", i, " ------------------------------"	
			continue
		
		# Check if callsign is in the fleet 
		if fleet_check_new(str(src_callsign)) == False:
			print "Aircraft ", src_callsign, " not in Sutton Bank fleet, ignore"
			print "-----------------End of Packet: ", i, " ------------------------------"
			continue
		else:
			print "Aircraft ", src_callsign, " is in Sutton Bank fleet, process"
			# Use registration if it is in aircraft table else just use Flarm_ID
			src_callsign = 	callsign_trans(src_callsign)
			print "Aircraft callsign is now: ", src_callsign
			# Check with this aircraft callsign has been seen before
			CheckPrev(src_callsign, 'latitude', 0)
			CheckVals(src_callsign, 'latitude', 0)
			# Current and previous data values created
			local_time = datetime.datetime.now()
			fl_date_time = local_time.strftime("%D:%H:%M:%S")
			fl_date = local_time.strftime("%y/%m/%d")
# 			fl_date = local_time.strftime("%D")
			fl_time = local_time.strftime("%H:%M:%S")
			print "src_callsign matched: ", src_callsign, " ", fl_date_time, " Latitude is: ", latitude
# 			print "Line ", i, " ", packet[0].orig_packet
			
#			if nprev_vals[src_callsign]['speed'] == 0 and nvalues[src_callsign]['speed'] <> 0:
			if nprev_vals[src_callsign]['speed'] <= V_SMALL and nvalues[src_callsign]['speed'] > V_SMALL:

				# aircraft was stopped, now isn't
				print "Aircraft ", src_callsign, " was stopped, now moving. Create new record"	
				cursor.execute('''INSERT INTO flight_log2(sdate, stime, edate, etime, duration,	src_callsign, max_altitude, speed)
							VALUES(:sdate,:stime,:edate,:etime,:duration,:src_callsign,:max_altitude,:speed)''',
							{'sdate':fl_date, 'stime':fl_time, 'edate': "", 'etime':"", 'duration': "", 'src_callsign':src_callsign, 'max_altitude':altitude, 'speed':0})
				nprev_vals[src_callsign]['speed'] = nvalues[src_callsign]['speed']
				
#			if nprev_vals[src_callsign]['speed'] <> 0 and nvalues[src_callsign]['speed'] == 0:
			if nprev_vals[src_callsign]['speed'] > V_SMALL and nvalues[src_callsign]['speed'] <= V_SMALL:
				# aircraft was moving is now stopped
				print "Aircraft ", src_callsign, " was moving, now stopped. Update record for end date & time"
				# Find latest record for this callsign
				cursor.execute('''SELECT sdate, stime, max_altitude FROM flight_log2 WHERE 
								ROWID IN (SELECT max(id) FROM flight_log2 WHERE src_callsign =? )''', (src_callsign,))
				row = cursor.fetchone()
				for r in row:
					print "Returned row for callsign: ", src_callsign, " is: ", r
# 				end_time = datetime.strptime(fl_time,'%H:%M:%S') 
				end_time = datetime.datetime.now()  # In seconds since epoch
				start_date = row[0]  # In %y/%m/%d format
				start_time = row[1]  # In %H:%M:%S format
				max_altitude = row[2]
				
				fl_end_datetime = datetime.datetime.now()
				fl_end_date = fl_end_datetime.strftime("%y/%m/%d")
				fl_end_time_str = fl_end_datetime.strftime("%H:%M:%S")
#				fl_end_time = fl_end_time_str
				fl_end_time = datetime.datetime.strptime(fl_end_time_str, "%H:%M:%S")
				print "Flight End date and time are: ", fl_end_date, " , ", fl_end_time_str
				print "Flight Start date and time are: ", start_date, " , ", start_time

				fl_start_time = datetime.datetime.strptime(start_time, "%H:%M:%S")  # Convert flight start time to type time
				fl_duration_datetime = fl_end_time - fl_start_time  # fl_duration_time is a string format %H:%M:%S
#				fl_duration_time = datetime.datetime.strptime(fl_duration_datetime, "%H:%M:%S")
				c = fl_duration_datetime
#				fl_duration_time = "%.2dh: %.2dm: %.2ds" % (c.seconds//3600,(c.seconds//60)%60, c.seconds%60)
				fl_duration_time = "%.2d: %.2d: %.2d" % (c.seconds//3600,(c.seconds//60)%60, c.seconds%60)
				fl_duration_time_str = str(fl_duration_time)
				print "Start time: ", fl_start_time, "End time: ", fl_end_time_str, "Duration: ", fl_duration_time, " Max altitude: ", max_altitude
				# Add record to flight_log_final
				cursor.execute('''INSERT INTO flight_log_final(sdate, stime, edate, etime, duration, src_callsign, max_altitude, speed)
							VALUES(:sdate,:stime,:edate,:etime,:duration,:src_callsign,:max_altitude,:speed)''',
							{'sdate':start_date, 'stime':start_time, 'edate': fl_end_date, 'etime':fl_end_time_str,
							'duration': fl_duration_time_str, 'src_callsign':src_callsign, 'max_altitude':max_altitude, 'speed':0})
				print "Updated flight_log_final", src_callsign
				
				
				# Update flight record in flight_log2
				cursor.execute(''' SELECT max(id) FROM flight_log2 WHERE src_callsign =?''', (src_callsign,))
				row = cursor.fetchone()
				rowid = row[0]
				print "Update row: ", rowid
				cursor.execute('''UPDATE flight_log2 SET edate=?, etime=?, duration=?, max_altitude=?, speed=? WHERE ROWID=?''',
							(fl_end_date, fl_end_time_str, fl_duration_time_str, max_altitude, 0, rowid))
				print "Updated flight_log2", src_callsign, " Row: ", rowid
				nprev_vals[src_callsign]['speed'] = nvalues[src_callsign]['speed']  # ie set to '0')
				
				# Check updated record
				print "Check fields in flight_log2: ", src_callsign, " Row: ", rowid
				cursor.execute('''SELECT ROWID, sdate, stime, edate, etime, duration, max_altitude FROM flight_log2 WHERE 
								ROWID IN (SELECT max(id) FROM flight_log2 WHERE src_callsign =? )''', (src_callsign,))
				row = cursor.fetchone()
				for r in row:
					print "Returned row for callsign: ", src_callsign, " is: ", r
					
				db.commit()	
				print "-----------------End of Packet: ", i, " ------------------------------"
				continue
#			if nprev_vals[src_callsign]['speed'] == 0 and nvalues[src_callsign]['speed'] == 0:
			if nprev_vals[src_callsign]['speed'] <= V_SMALL and nvalues[src_callsign]['speed'] <= V_SMALL and nvalues[src_callsign]['altitude'] <= QNH:
				# Aircraft hasn't moved and is not at an altitude greater than Sutton Bank.  
				print "Aircraft: ", src_callsign, " Not moving. Speed was: ", nvalues[src_callsign]['speed'], " Speed is: ", nvalues[src_callsign]['speed']
			else:
				# aircraft is moving. Check whether current altitude is greater than previous
				print "Aircraft ", src_callsign, " is still moving"
				if nvalues[src_callsign]['altitude'] > nprev_vals[src_callsign]['altitude']:
					print "Aircraft ", src_callsign, " is now higher, was: ", nprev_vals[src_callsign]['altitude'], " now: ", nvalues[src_callsign]['altitude']
					cursor.execute('''UPDATE flight_log2 SET max_altitude=? WHERE src_callsign=? ''', (altitude, src_callsign))
					nprev_vals[src_callsign]['altitude'] = nvalues[src_callsign]['altitude']  # Now higher
				else:
					print "Aircraft callsign: ", src_callsign, " is moving but is not higher than last time. Height: ", nvalues[src_callsign]['altitude'], " Speed is: ", nvalues[src_callsign]['speed'], " Was: ", nprev_vals[src_callsign]['speed']
					# Set previous speed values to current
					nprev_vals[src_callsign]['speed'] = nvalues[src_callsign]['speed']
					continue
				
# 			print "Values for callsign: ", src_callsign, " Values are: ", nvalues[src_callsign], " Prev_vals are: ", nprev_vals[src_callsign]
			db.commit()		
		print "-----------------End of Packet: ", i, " ------------------------------"
	libfap.fap_free(packet)
			
except KeyboardInterrupt:
	print "Keyboard input received, ignore"
#	db.commit()
	pass

print "libfap_cleanup. If not called results in memory leak"
libfap.fap_cleanup()
# close socket -- must be closed to avoid buffer overflow
sock.shutdown(0)
sock.close()
# Close the database. Note this should be on all forms of exit
db.close()

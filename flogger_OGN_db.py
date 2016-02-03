#    
#-----------------------------------------------------------------
# Function to read OGN Flarm database and create SQLite version for local use.
# Note this means if a new entry is added to OGN db after flogger has started
# it won't be included.  
#
# Run at start of each day? 
#-----------------------------------------------------------------
#
import string
import requests
import sqlite3
import time
import settings
import flogger_OGN_db
# import unicodedata


def ogndb (ognurl, cursor, flarmdb, flarm_data):
    #    
    #-----------------------------------------------------------------
    # This function reads the file of Flarm units registered on OGN and
    # uses this to build the flarm_db. 
    # It takes data from units which are registered for aircraft that are to be logged                 
    #-----------------------------------------------------------------
    #  
    try:
        print "Create flarm_db table"
        cursor.execute('''CREATE TABLE IF NOT EXISTS
                            flarm_db(id INTEGER PRIMARY KEY, flarm_id TEXT, airport STRING, type TEXT, registration TEXT, radio TEXT)''')
        print "flarm_db table created"
    except Exception as e:
        # Roll back any change if something goes wrong
        print "Failed to create flarm_db"
#        dbflarm.rollback()
#        raise e 
    try:
        # OGN flarm db is at "http://ddb.glidernet.org/download"
        ogn_db = settings.FLOGGER_OGN_DB_URL
        r = requests.get(ogn_db)
    except Exception as e:
        print "Failed to connect to OGN db, reason: %s. Exit" % (e)
        exit()
    print "OGN db accessed"   
    
    data = r.content  
#    print "OGN content is: ", data[0], data[1], data[2]
    lines = data.split("\n")
#    print "OGN split is: ", lines
    i = 1
    for line in lines:
        if i == 1:
            i += 1
            continue        # Discard first line
#        print "Line ", i, " is: ", line
        if line == "":
            # Seems to be a blank line at end
            continue        # Discard last line
        
        fields = line.split(",")                # Split line into fields on comma boundaries then remove any quote marks
        nf1 = fields[1].replace("'", "")        # Flarm ID
        nf0 = fields[0].replace("'", "")        # Aircraft Type
        nf3 = fields[3].replace("'", "")        # Aircraft Registration
#        print "Line: ", i, " Fields: ", nf1, " ", nf0, " ", nf3
        try:
            if settings.FLOGGER_FLEET_LIST.has_key(nf3):
                cursor.execute('''INSERT INTO flarm_db(flarm_id, airport, type, registration)
                               VALUES(:flarm_id, :airport, :type, :registration)''',
                                {'flarm_id': nf1, 'airport': settings.FLOGGER_AIRFIELD_NAME, 'type': nf0, 'registration': nf3})
        except Exception as e:
           print "Flarm_db insert failed. Reason: %s " % (e)
        i += 1
    flarmdb.commit()
    return True
#    exit()

#    print "First line from OGN data is : ", val
    
 
#db = sqlite3.connect(settings.FLOGGER_DB_NAME)
#cursor = db.cursor()                            # Get a cursor object
#f = open(settings.FLOGGER_DB_SCHEMA, 'rt')      # Open the db schema file for reading
#schema = f.read()
#cursor.executescript(schema)                    # Build flogger db from schema
#print "End of building db: ", settings.FLOGGER_DB_NAME, " using schema: ", settings.FLOGGER_DB_SCHEMA



#    
#-----------------------------------------------------------------
# Build local database from OGN of aircraft    
#-----------------------------------------------------------------
#
   
#print "Start build OGN DB: Test"
#t1 = time.time() 
#if ogndb("http://ddb.glidernet.org/download", cursor, db, "flarm_data") == True:
#    print "OGN db built"
#else:
#    print "OGN db build failed, exit"
#t2 = time.time()
#print "End build OGN DB in ", t2 - t1 , " seconds"


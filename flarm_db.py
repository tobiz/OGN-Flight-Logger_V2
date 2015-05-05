#
# Program to read flarm_id database and create SQLite version for local use

import string
import requests
import sqlite3
import time
#import unicodedata

def flarmdb (flarmnet, flogger_db, flarm_data):
    try:
#        flarmnet_db = "http://www.flarmnet.org/files/data.fln"
        flarmnet_db = flarmnet
        r = requests.get(flarmnet_db)
    except:
        print "Failed to connect to flarmnet db, exit"
        exit()
        
    data = r.content    
#    flm = open("flarm_data", "w")
#    flm_txt = open("flarm_data_txt", "w")  
    flm = open(flarm_data, "w")
    flm_ln = len(r.content) - 1
    print "Flarm db length: ", flm_ln
    try:
        for i in range(0, flm_ln, 1):
            c = "%c" % data[i]
            flm.write(c)
    except :
        print "Error writing flarm_data"   
        exit()
    flm.close()
    
    #db = open("data.fln", 'r')
    db = open(flarm_data, 'r')
    # Read first line and convert to number
    x = db.readline()
    val = int(x, 16)
    print "First line from FlarmNet data is : ", val
    
    try:
        # Creates or opens a file called mydb with a SQLite3 DB
#        dbflarm = sqlite3.connect('flogger.sql3')
        dbflarm = sqlite3.connect(flogger_db)
        print "Create flarm_db table"
        # Get a cursor object
        cursor = dbflarm.cursor()
#        cursor.execute('''DROP TABLE flarm_db''')
        cursor.execute('''DELETE FROM flarm_db''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS
                            flarm_db(id INTEGER PRIMARY KEY, flarm_id TEXT, airport STRING, type TEXT, registration TEXT, radio TEXT)''')
        print "flarm_db table created"
        # Commit the changes
    #    dbflarm.commit()
    # Catch the exception
    except Exception as e:
        # Roll back any change if something goes wrong
        print "Failed to create flarm_db"
        dbflarm.rollback()
        raise e
    
    i = 1
    line = ""
    nos_lines = val 
    while True:
        try:
            line = db.readline()
            line_lng = len(line)
#            print "Line length is: ", line_lng
            string = ""
#            print "read: ", i, " returns: ", line
            for j in range(0,172,2):
#            for j in range(0,line_lng - 1,2):
    #            x = line[j:j+2]
    #            y = int(x, 16)
    #            c = chr(y)
                c = chr(int(line[j:j+2],16))
                string = string + c
            i = i + 1
    #        v.decode("iso-8859-15").encode("utf-8")
            ID = str(string[0:6]).decode("iso-8859-15").encode("utf-8")
    #        Airport = str(string[27:47]).decode("iso-8859-15").encode("utf-8", errors="replace")
            try:
                Airport = str(string[27:47]).decode("utf-8").encode("iso-8859-15")
#                Airport = str(string[27:47]).decode("iso-8858-15").encode("iso-8859-15")
                Airport = Airport.rstrip()
            except:
                print "Code error ", str(string[27:47])
#                try:
#                    s = "%s" % str(string[27:47]).encode("utf-8")
#                    print s
#                except:
#                    print "WRONG ", s
#                s = unicodedata.name(str(string[27:47]))
#                Airport = str(string[27:47]).decode("utf-8").encode("utf-16")
#                Airport = string[27:47]
            Type = str(string[48:69]).decode("iso-8859-15").encode("utf-8")
            Registration = str(string[69:75]).decode("iso-8859-15").encode("utf-8")
            Radio = str(string[79:86]).decode("iso-8859-15").encode("utf-8")
    #        print "Line: ", i-1, " ID: ", ID,  " Airport: ", Airport, " Type: ", Type, " Registration: ", Registration,  " Radio: ", Radio
    #        row = "%s__%s__%s__%s__%s\n" % (ID, Airport, Type, Registration, Radio)
    #        flm_txt.write(row)
            try:
                cursor.execute('''INSERT INTO flarm_db(flarm_id, airport, type, registration, radio)
                               VALUES(:flarm_id, :airport, :type, :registration, :radio)''',
                                {'flarm_id': ID, 'airport': Airport, 'type': Type, 'registration': Registration, 'radio': Radio})
    #            dbflarm.commit()
            except :
               print "Flarm_db insert failed ", Airport
               dbflarm.commit()
               return False
        except:
            print "Number of rows is: ", i - 1
            dbflarm.commit()
            return True
    return True
    #dbflarm.commit()

   
#print "Start build Flarm DB: Test"
#t1 = time.time() 
#flarmdb("http://www.flarmnet.org/files/data.fln", 'flogger.sql3', "flarm_data")
#t2 = time.time()
#print "End build Flarm DB in ", t2 - t1 , " seconds"


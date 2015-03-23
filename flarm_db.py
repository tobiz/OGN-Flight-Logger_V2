
#(?<_id> .{6})
#(?<owner> .{21})
#(?<airport> .{21})
#(?<type> .{21})
#(?<registration>.{7})
#(?<tail> .{3})
#(?<radio> .{7}) 

import string
import requests
import sqlite3


try:
    flarmnet_db = "http://www.flarmnet.org/files/data.fln"
    r = requests.get(flarmnet_db)
    #print r.status_code
    #print r.headers
    #print r.content
    #print r.text
except:
    print "Failed to connect to flarmnet db, exit"
    exit()
    
data = r.content    
flm = open("flarm_data", "w")
flm_txt = open("flarm_data_txt", "w")
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
db = open("flarm_data", 'r')
# Read first line and convert to number
x = db.readline()
val = int(x, 16)
print "First line is: ", val

try:
    # Creates or opens a file called mydb with a SQLite3 DB
    dbflarm = sqlite3.connect('flogger.sql3')
    print "Create flarm_db table"
    # Get a cursor object
    cursor = dbflarm.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS
                        flarm_db(id INTEGER PRIMARY KEY, flarm_id TEXT, airport STRING, type TEXT, registration TEXT, radio TEXT)''')
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
        string = ""
    #    print "read: ", i, " returns: ", line
        for j in range(0,172,2):
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
        except:
            print "Code error"
#        Airport = string[27:47]
        Type = str(string[48:69]).decode("iso-8859-15").encode("utf-8")
        Registration = str(string[69:75]).decode("iso-8859-15").encode("utf-8")
        Radio = str(string[79:86]).decode("iso-8859-15").encode("utf-8")
        print "Line: ", i-1, " ID: ", ID,  " Airport: ", Airport, " Type: ", Type, " Registration: ", Registration,  " Radio: ", Radio
        row = "%s__%s__%s__%s__%s\n" % (ID, Airport, Type, Registration, Radio)
        flm_txt.write(row)
        try:
#          cursor.execute('''INSERT INTO flarm_db(flarm_id, airport, type, registration, radio)
#                           VALUES(:flarm_id, :airport, :type, :registration, :radio)''',
#                            {'flarm_id': ID, 'airport': Airport, 'type': Type, 'Registration': Registration, 'radio': Radio})
            cursor.execute('''INSERT INTO flarm_db(flarm_id, airport, type, registration, radio)
                           VALUES(:flarm_id, :airport, :type, :registration, :radio)''',
                            {'flarm_id': ID, 'airport': Airport, 'type': Type, 'registration': Registration, 'radio': Radio})
#            dbflarm.commit()
        except :
           print "Flarm_db insert failed ", Airport
           dbflarm.commit()
           exit()
    except:
        print "Last line is: ", i
        dbflarm.commit()
        exit()
dbflarm.commit()


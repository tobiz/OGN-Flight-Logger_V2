import sys
import os
import string
from PyQt4 import QtGui, QtCore, uic
from PyQt4.Qt import SIGNAL
import subprocess
import settings
from parse import *
from ConfigParser import *

import socket

from libfap import *
#import flogger_settings
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
import ephem
from flogger_process_log import process_log
import argparse
from flogger_dump_flights import dump_flights
from flogger_dump_tracks import dump_tracks2
from flogger_get_coords import get_coords
from flogger_signals import sig_handler
import signal
import os
import os.path
from flogger_dump_IGC import dump_IGC
from flogger_email_log import email_log2
from flogger_landout import landout_check
from geopy.distance import vincenty
from flogger_email_msg import email_msg
from flogger_find_tug import find_tug
from flogger_test_YorN import test_YorN


# get the directory of this script
path = os.path.dirname(os.path.abspath(__file__))
#print("Path: " + path) 

#form_class = uic.loadUiType("flogger.ui", from_imports, resource_suffix)
#form_class = uic.loadUiType("flogger.ui")[0]
#form_class = uic.loadUiType(os.path.join(path,"flogger.ui"))[0]
#form_class, base_class = uic.loadUiType(os.path.join(path,"flogger.ui"))
Ui_MainWindow, base_class = uic.loadUiType(os.path.join(path,"flogger.ui"))

#class Window (QtGui.QMainWindow, form_class):
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
#        self.runFloggerButton.clicked.connect(self.floggerStart) 
        self.actionStart.triggered.connect(self.floggerStart)  
        self.actionStop.triggered.connect(self.floggerStop)  
        self.actionQuit.triggered.connect(self.floggerQuit)  
        self.AirfieldBaseButton.clicked.connect(self.floggerAirfieldEdit) 
        
        # Initialise values from config file
        self.old_value = self.AirfieldBase.setText(settings.FLOGGER_AIRFIELD_NAME) 
        self.APRSUser.setText(settings.APRS_USER) 
        self.APRSPasscode.setText(str(settings.APRS_PASSCODE)) 
        self.APRSServerHostName.setText(settings.APRS_SERVER_HOST) 
        self.APRSServerPort.setText(str(settings.APRS_SERVER_PORT))
        if settings.FLOGGER_LATITUDE[0:1] == "-":
            latitude = settings.FLOGGER_LATITUDE[1:] + " E"
        else:
            latitude = settings.FLOGGER_LATITUDE[1:] + " W"
        print "Latitude: " + latitude
        if settings.FLOGGER_LONGITUDE[0:1] == "-":
            longitude = settings.FLOGGER_LONGITUDE[1:] + " S"
        else:
            longitude = settings.FLOGGER_LONGITUDE[1:] + " N"
        print "Latitude: " + longitude
        self.AirfieldLatitude.setText(latitude)
        self.AirfieldLongitude.setText(longitude)
 
        
    def floggerStart(self):
        print "flogger start"
#        flogger_run_string = "flogger Start"   
#        self.floggerRunBox.setText(settings.FLOGGER_AIRFIELD_NAME)
        cmd = os.path.join(path,"flogger.py")
        cmd_args = ["OGNFLOG2", "31134",  "test", "--smt smtp.metronet.co.uk", "--tx pjrobinson@metronet.co.uk", "--rx pjrobinson@metronet.co.uk"]
        print("cmd_line: " + cmd)
#        execvp(cmd, cmd_args)
#        execfile("flogger.py", "OGNFLOG2 31134  test --smt smtp.metronet.co.uk --tx pjrobinson@metronet.co.uk --rx pjrobinson@metronet.co.uk")
   
    def floggerStop(self):
        print "flogger stop"
    
    def floggerQuit(self):
        print "flogger quit"
            
    def floggerAirfieldEdit(self):
        print "Base Airfield button clicked" 
        airfield_base = self.AirfieldBase.toPlainText()  
        print "Airfield Base: " + airfield_base
        
        self.editConfigField("settings.py", "FLOGGER_AIRFIELD_NAME", self.old_value, airfield_base)
        self.AirfieldBase.setText(settings.FLOGGER_AIRFIELD_NAME)


    def editConfigField (self, file_name, field_name, old_value, new_value):
        print "editConfig called"
        file = os.path.join(path, file_name)
        with open(file, 'rw') as searchfile:
            searchphrase = field_name
            for line in searchfile:
                if searchphrase in line and line[0:1] <> "#":
#                    print "Line is: " + line
                    pos = line.find("=")
#                    print "Position: " + str(pos)
                    line_list = line.split()
#                    print line_list
                    parse_str1 = field_name + " = " + "{field_val1}" + "#" + "{field_val2}"
#                    print "Parse string1: " + parse_str1
                    res1 = parse(parse_str1, line)
                    print res1
                    print "Field1: " + res1["field_val1"] + ", " + "Field2: " + res1["field_val2"]
#                    print "Field1 Type: " +  str(type(res1["field_val1"])) + ", " + "Field2 Type: " + str(type(res1["field_val2"]))
                    
                    field1_type = str(type(res1["field_val1"]).__name__)
                    field2_type = str(type(res1["field_val2"]).__name__)
#                    print "Field1 Type: " +  type(res1["field_val1"]) + ", " + "Field2 Type: " + type(res1["field_val2"])
                    print "Field1 Type: " +  field1_type + ", " + "Field2 Type: " + field2_type
                    if field1_type == "str":
                        print True
                    else:
                        print False
                    print "Line is: " + line
                    new_line = line.replace(self.old_value, new_value, 1)
#                    new_line = field_name + " = " + new_value + " # " + res1["field_val2"]
                    print new_line
                    
#                    import fileinput
#                    parse_line = fileinput.input(files, inplace = 1)
                    # Does a list of files, and
                    # redirects STDOUT to the file in question
                    #for line in fileinput.input(files, inplace = 1):
#                    print line.replace(self.old_value, new_value),

                    break
            
            
            
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())


#class MainWindow (QtGui.QMainWindow, form_class):
#    def __init__(self):
#        QtGui.QMainWindow.__init__(self)
#        form_class.__init__(self)
#        self = MainWindow()
#        self.setupUi(self)
        

#        flogger_ui = path + "/flogger.ui"
#        print("flogger_ui: " + flogger_ui)
                                  
#        self = uic.loadUiType(flogger_ui)[0]
#        self.setupUi(self)
#        super(Window, self).__init__()
#        self.setGeometry(50, 50, 500, 300)
#        self.setWindowTitle("PyQT Flogger")
#        self.setWindowIcon(QtGui.QIcon(""))
#        self.connect(self.actionStart, SIGNAL("activated()"), self.floggerStart)
#        print "Init"
#        self.connect(self.actionStart, QtCore.SIGNAL("activated()"),self.floggerStart)
#        self.ui.connect(actionStart, QtCore.SIGNAL('activated()'), self, QtCore.SLOT('trigger()'))
#              self.connect(self.ui.actionOpen, QtCore.SIGNAL('triggered()'), self, QtCore.SLOT('open()'))
#        actionStart.signal.connect(slot_function)
#        self.pushButton.clicked.connect(self.floggerStart)
#        print "actionStart connect"
#        self.home()
#        self.show()
#    @QtCore.pyqtSlot()
#
#    def floggerStart(self):
#        self.n = self.n + 1
#        print("flogger start called ")
#        return
#        price = int(self.floggerRunBox.toPlainText())
#        tax = (self.tax_rate.value())
#        total_price = price  + ((tax / 100) * price)
#        flogger_run_string = "flogger Start"
#        self.floggerRunBox.setText(flogger_run_string)
        
#        /*price = int(self.price_box.toPlainText())
#        tax = (self.tax_rate.value())
#        total_price = price  + ((tax / 100) * price)
#        total_price_string = "The total price with tax is: " + str(total_price)
#        self.results_window.setText(total_price_string)
#        */
        
#    def home(self): 
#        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
#        exitAction.setShortcut('Ctrl+Q')
#        exitAction.setStatusTip('Exit application')
#        exitAction.triggered.connect(QtGui.qApp.quit)

#        self.statusBar()
#        menubar = self.menuBar()
#        fileMenu = menubar.addMenu('&File')
#        fileMenu.addAction(exitAction)
        
#        configMenu = menubar.addMenu('&Configure')
#        configMenu.addAction(exitAction)
        
#        self.setGeometry(300, 300, 300, 200)
#        self.setWindowTitle('PyQt Flogger')
#        btn = QtGui.QPushButton("Quit", self)    
#        btn.clicked.connect(self.close_app)
#        btn.resize(100,100)
#        btn.move(100,100)
#        self.connect(self.actionStart, SIGNAL("clicked()"),self.floggerStart)
#        self.n = 0
#        self.show()
        
#    def close_app(self):
#        print("Exit flogger")
#        sys.exit()
        
#    def actionStart(self):
#        print("actionStart called")
#        sys.exit()
        
#def main():
#    app = QtGui.QApplication(sys.argv)
#    GUI = Window()
#    sys.exit(app.exec_())
    
#main()

#if __name__ == "__main__":
#    app = QtGui.QApplication(sys.argv)
#    window = MainWindow()
#    window.show()
#    sys.exit(app.exec_())
    
import sys
import os
import string
from PyQt4 import QtGui, QtCore, uic
from PyQt4.Qt import SIGNAL
import subprocess
#import settings
import flogger_settings
from parse import *
from ConfigParser import *
from configobj import ConfigObj
from flogger3 import *
from flogger_settings import * 




# get the directory of this script
path = os.path.dirname(os.path.abspath(__file__))
#print("Path: " + path) 
settings = class_settings()

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
        self.APRSUserButton.clicked.connect(self.floggerAPRSUserEdit)   
        self.AirfieldDetailsButton.clicked.connect(self.floggerAirfieldDetailsEdit)   
        self.MinFlightTimeButton.clicked.connect(self.floggerMinFlightTimeEdit)  
        self.FleetCheckRadioButton.toggled.connect(self.floggerFleetCheckRadioButton) 
        
        # Initialise values from config file

#        filepath = os.path.join(path, "flogger_settings.py")
        filepath = os.path.join(path, "flogger_settings_file.txt")

#        filename = open(filepath)
        try:
#            config = ConfigObj(filename, encoding='UTF8', raise_errors = True)
#            self.config = ConfigObj("flogger_settings.py", raise_errors = True)
            self.config = ConfigObj("flogger_settings_file.txt", raise_errors = True)
            print "Opened"
        except:
            print "Open failed"
            
            print self.config
            
#
# This section reads all the values from the config file and outputs these in the gui fields.
# It also initialises the corresponding settings object config fields. If the values are changed
# in the gui they must be saved in the config file and used as the current values in the settings object
#          
        old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_NAME")
        settings.FLOGGER_AIRFIELD_NAME = old_val
#        print settings.FLOGGER_AIRFIELD_NAME
        self.AirfieldBase.setText(old_val)
         
        old_val = self.getOldValue(self.config, "APRS_USER")
        settings.APRS_USER = old_val
        self.APRSUser.setText(old_val)
        
        old_val = self.getOldValue(self.config, "APRS_PASSCODE")    # This might get parsed as an int - need to watch it!
        settings.APRS_PASSCODE = old_val
        self.APRSPasscode.setText(old_val)
        
        old_val = self.getOldValue(self.config, "APRS_SERVER_HOST")    
        settings.APRS_SERVER_HOST = old_val
        self.APRSServerHostName.setText(old_val)
        
        old_val = self.getOldValue(self.config, "APRS_SERVER_PORT")    # This might get parsed as an int - need to watch it!
        settings.APRS_SERVER_PORT = old_val
        self.APRSServerPort.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_DETAILS")    
        settings.FLOGGER_AIRFIELD_DETAILS = old_val
        self.AirfieldDetails.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_MIN_FLIGHT_TIME")    
        settings.FLOGGER_MIN_FLIGHT_TIME = old_val
        self.MinFlightTime.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_LATITUDE")    # This might get parsed as an real - need to watch it!
        print "Old_val: " + old_val
        settings.FLOGGER_LATITUDE = old_val
        self.AirfieldLatitude.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_LONGITUDE")    # This might get parsed as an real - need to watch it!
        settings.FLOGGER_LONGITUDE = old_val
        self.AirfieldLongitude.setText(old_val)
        
        if settings.FLOGGER_LATITUDE < 0:
            latitude = str(settings.FLOGGER_LATITUDE)[1:] + " S"
        else:
            latitude = str(settings.FLOGGER_LATITUDE)[1:] + " N"
#        print "Latitude: " + latitude
        
        if settings.FLOGGER_LONGITUDE < 0:
            longitude = str(settings.FLOGGER_LONGITUDE)[1:] + " E"
        else:
            longitude = str(settings.FLOGGER_LONGITUDE)[1:] + " W"
#        print "Latitude: " + longitude
        self.AirfieldLatitude.setText(latitude)
        self.AirfieldLongitude.setText(longitude)
        
        old_val = self.getOldValue(self.config, "FLOGGER_FLEET_CHECK")
        print "Fleet Check: " + old_val 
        if old_val == "Y":
            print "Y"
            self.FleetCheckRadioButton.setChecked()
        else:
            print "N"   
        settings.FLOGGER_FLEET_CHECK = old_val
 
        
    def floggerStart(self):
        print "flogger start"
        flogger = flogger3()
        flogger.flogger_start()
#        flogger_run_string = "flogger Start"   
#        self.floggerRunBox.setText(settings.FLOGGER_AIRFIELD_NAME)
        cmd = "python " + os.path.join(path,"flogger.py")
        cmd_line = [cmd, "OGNFLOG2", "31134",  "test", "--smt smtp.metronet.co.uk", "--tx pjrobinson@metronet.co.uk", "--rx pjrobinson@metronet.co.uk"]
#        print "cmd is: " + cmd
#        print("cmd_line: ") + str(cmd_line)
#        os.execvp(cmd, cmd_line[1:])
     #   os.execv(cmd, "OGNFLOG2", "31134",  "test", "--smt smtp.metronet.co.uk", "--tx pjrobinson@metronet.co.uk", "--rx pjrobinson@metronet.co.uk" )
#        os.execv("#!flogger.py", ["OGNFLOG2", "31134",  "test", "--smt smtp.metronet.co.uk", "--tx pjrobinson@metronet.co.uk", "--rx pjrobinson@metronet.co.uk"])
#        os.execlp("/home/pjr/git_neon/OGN-Flight-Logger_V2", "flogger.py","OGNFLOG2", "31134",  "test", "--smt smtp.metronet.co.uk", "--tx pjrobinson@metronet.co.uk", "--rx pjrobinson@metronet.co.uk")
        exec "flogger.py"

#        execfile("flogger.py", "OGNFLOG2 31134  test --smt smtp.metronet.co.uk --tx pjrobinson@metronet.co.uk --rx pjrobinson@metronet.co.uk")
   
    def floggerStop(self):
        print "flogger stop"
    
    def floggerQuit(self):
        print "flogger quit"
            
    def floggerAirfieldEdit(self):
        print "Base Airfield button clicked" 
        airfield_base = self.AirfieldBase.toPlainText()  
        print "Airfield Base: " + airfield_base
        self.editConfigField("settings.py", "FLOGGER_AIRFIELD_NAME", airfield_base)
        airfield_base = self.config["FLOGGER_AIRFIELD_NAME"]
#        self.AirfieldBase.setText(settings.FLOGGER_AIRFIELD_NAME)
        self.FLOGGER_AIRFIELD_NAME = airfield_base

    def floggerAPRSUserEdit(self):
        print "APRS User button clicked" 
        APRSUser = self.APRSUser.toPlainText()  
#       print "Airfield B: " + airfield_base
        self.editConfigField("settings.py", "APRS_USER", APRSUser)
        APRSUser = self.config["APRS_USER"]
        
    def floggerAirfieldDetailsEdit(self):
        print "Airfield Details button clicked"
        
    def floggerMinFlightTimeEdit(self):
        print "Min Flight Time button clicked"   
    
    def floggerFleetCheckRadioButton(self):
        print "Fleet Check Radio Button clicked" 
        
          
    def editConfigField (self, file_name, field_name, new_value):
        print "editConfig called"
        self.config[field_name] = new_value
        self.config.write()

            
    def setOldValue(self, config_field_name): 
#        val = self.config[config_field_name]
        val = settings.config[config_field_name]
        setattr(self, config_field_name, val) #equivalent to: self.varname= 'something'
#        settings.config_field_name = val
        return self.config[config_field_name]
    
    def getOldValue(self, config, config_field_name): 
        val = config[config_field_name]
        setattr(self, config_field_name, val)
        return config[config_field_name]
        
               
            
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())


    
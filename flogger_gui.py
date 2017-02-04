import sys
import os
import string
from PyQt4 import QtGui, QtCore, uic
from PyQt4.Qt import SIGNAL
import subprocess

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
        self.runFloggerButton.clicked.connect(self.floggerStart)   
        
    def floggerStart(self):
        print "flogger start"
#        self.n = self.n + 1
#        print("flogger start called ")
#        return
#        price = int(self.floggerRunBox.toPlainText())
#        tax = (self.tax_rate.value())
#        total_price = price  + ((tax / 100) * price)
        flogger_run_string = "flogger Start"
        self.floggerRunBox.setText(flogger_run_string)
        cmd = os.path.join(path,"flogger.py")
        cmd_args = ["OGNFLOG2", "31134",  "test", "--smt smtp.metronet.co.uk", "--tx pjrobinson@metronet.co.uk", "--rx pjrobinson@metronet.co.uk"]
        print("cmd_line: " + cmd)
        execvp(cmd, cmd_args)
#        execfile("flogger.py", "OGNFLOG2 31134  test --smt smtp.metronet.co.uk --tx pjrobinson@metronet.co.uk --rx pjrobinson@metronet.co.uk")

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
    
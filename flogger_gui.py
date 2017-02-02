import sys
from PyQt4 import QtGui, QtCore, uic

#form_class = uic.loadUiType("flogger.ui", from_imports, resource_suffix)
form_class = uic.loadUiType("flogger.ui")[0]

class Window (QtGui.QMainWindow, form_class):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQT Flogger")
        self.setWindowIcon(QtGui.QIcon(""))
        self.home()
        
    def home(self): 
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        
        configMenu = menubar.addMenu('&Configure')
        configMenu.addAction(exitAction)
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('PyQt Flogger')
        btn = QtGui.QPushButton("Quit", self)    
        btn.clicked.connect(self.close_app)
        btn.resize(100,100)
        btn.move(100,100)
        self.show()
        
    def close_app(self):
        print("Exit flogger")
        sys.exit()
        
def main():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
    
main()
    
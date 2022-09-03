import obd
import PyQt5
import time
import random
import pyqtgraph as pg
from collections import deque
from pyqtgraph.Qt import QtGui, QtCore
#from PyQt5.QtWidgets import QLabel

# obd connect
ports = obd.scan_serial()
print(ports)
#obd.logger.setLevel(obd.logging.DEBUG)
connection = obd.OBD(ports[0], baudrate=None)

spd = obd.commands.SPEED
rpm = obd.commands.RPM

# graphing
class Graph:
    def __init__(self, ):
        self.dat = deque()
        self.dat2 = deque()
        self.dat3 = deque()
        self.maxLen = 100#max number of data points to show on graph
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle("ouasdg")
        #msg = QLabel('<h1>lasdgjlsdg</h1>', parent=self.win)
       
        self.p1 = self.win.addPlot(colspan=2)
        self.win.nextRow()
        self.p2 = self.win.addPlot(colspan=2)
        self.win.nextRow()
        self.p3 = self.win.addPlot(colspan=2)
       
        self.curve1 = self.p1.plot()
        self.curve2 = self.p2.plot()
        self.curve3 = self.p3.plot()
       
        graphUpdateSpeedMs = 50
        timer = QtCore.QTimer()#to create a thread that calls a function at intervals
        timer.timeout.connect(self.update)#the update function keeps getting called at intervals
        timer.start(graphUpdateSpeedMs)   
        QtGui.QApplication.instance().exec_()
    
    def update(self):
        if len(self.dat) > self.maxLen:
            self.dat.popleft() #remove oldest
        if len(self.dat2) > self.maxLen:
            self.dat2.popleft() #remove oldest
        if len(self.dat3) > self.maxLen:
            self.dat3.popleft() #remove oldest
        response1 = connection.query(rpm)
        response2 = connection.query(spd)
        # rpm
        self.dat.append(float(response1.value.magnitude));
        
        # speed
        self.dat2.append(float(response2.value.magnitude));
        
        # acceleration
        acc = (self.dat2[len(self.dat)-1]-self.dat2[len(self.dat2)-2])/3.6/0.05/9.8
        self.dat3.append(acc);
        print(self.dat2[len(self.dat2)-1], acc)
               
        self.curve1.setData(self.dat)
        self.curve2.setData(self.dat2)
        self.curve3.setData(self.dat3)
        self.app.processEvents()  
       

if __name__ == '__main__':
    g = Graph()
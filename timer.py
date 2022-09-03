import obd
import time
import random
import pyqtgraph as pg
from collections import deque
from pyqtgraph.Qt import QtGui, QtCore

# obd connect
ports = obd.scan_serial()
print(ports)
connection = obd.OBD(ports[0], baudrate=None)

cmd = obd.commands.SPEED

# timer variables initialize
start = 10
end = 100
starttime = 0
endtime = 0
ready = False
isstarted = False

# graphing
class Graph:

    def __init__(self, ):
        self.dat = deque()
        self.maxLen = 50#max number of data points to show on graph
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow()
       
        self.p1 = self.win.addPlot(colspan=2)
        self.p1.setTitle('Acceleration timer')
        self.p1.setLabel('bottom', 'Time', 's')
        self.win.nextRow()
       
        self.curve1 = self.p1.plot()
       
        graphUpdateSpeedMs = 1
        timer = QtCore.QTimer()#to create a thread that calls a function at intervals
        timer.timeout.connect(self.update)#the update function keeps getting called at intervals
        timer.start(graphUpdateSpeedMs)   
        QtGui.QApplication.instance().exec_()
       
    def update(self):
        response = connection.query(cmd)
        s = float(response.value.magnitude)
        
        global start
        global end
        global starttime
        global endtime
        global ready
        global isstarted
        
        if isstarted: # not ready if timer already started
            ready = False
        elif s <= start: # ready if under or exactly at starting speed
            ready = True
            print("ready ("+str(s)+")")
        if ready or isstarted:
            if s < end and s > start: # if in range 
                if isstarted == False: # start timer if haven't already started
                    starttime = time.time()
                    isstarted = True
                    self.dat.clear()
                endtime = time.time() # to show time on every update
                #self.p1.setRange(xRange=[0, endtime-starttime])
                print(str(round(endtime-starttime, 2))+" sec ("+str(s)+")")
                ###
                if s <= start and isstarted:
                    print("cancelled ("+str(s)+")")
                    isstarted = False
                    ready = True
                    starttime = 0
                    endtime = 0
                    self.dat.clear()
                ###
            else:
                if isstarted == True: # if not in range stop timer
                    endtime = time.time()
                    #self.p1.setRange(xRange=[0, endtime-starttime])
                    print("stopped", round(endtime-starttime, 2), s, isstarted)
                    isstarted = False
                    startttime = 0
                    endtime = 0
          
    
        if isstarted:
            self.dat.append(s); 
        
        

        self.curve1.setData(self.dat)
        self.app.processEvents()  
       

if __name__ == '__main__':
    g = Graph()
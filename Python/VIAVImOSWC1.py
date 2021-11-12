
"""
Created on Tue Sep  3 14:49:21 2019

@author: Daniel Hutama
"""

# code needs testing on device

from __connection__ import Connection
from globalsFile import *
import time

class VIAVImOSWC1(Connection):
    def __init__(self,addressString,slot,port):
        Connection.__init__(self,addressString)
        self.Driver_Document = 'VIAVImOSWC1.pdf'
        self.slot=int(slot)
        self.port=int(port)

    def GetPort(self):
        port=self.__query__(':ROUT:CLOS? 1,'+'{}'.format(self.slot)+','+'{}'.format(self.port)+',1')
        return int(port)
        
    def SetPort(self,port):
        self.__write__(':ROUT:CLOS 1,'+'{}'.format(self.slot)+','+'{}'.format(self.port)+',1,'+ '{}'.format(port))
        time.sleep(1)
        PT=self.GetPort()
        
        if PT==port:
             print(time.ctime()+' SW is Set correctly to port '+str(PT));
        else:
            print(time.ctime()+' SW is Set wrong to port '+str(PT));        
        return int(PT)


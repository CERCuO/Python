import time
import re
import numpy as np
import matplotlib.pyplot as plt
import types
import os

from __connection__ import Connection
from globalsFile import *

"""
Base class for anritsu OSA instruments that share common command set
command set may not be the same for all anritsu OSA instruments, so
there is a numeric identifier at the end of the file/class

"""

class AnritsuOSA1(Connection):
    def __init__(self,addressString):
        Connection.__init__(self,addressString)
        self.setReadTermination('')
        self.setWriteTermination('\r\n')
        self.__setTimeout__(3000) # 3 seconds
        self.StopWavelength = self.GetStopWavelength()
        self.StartWavelength = self.GetStartWavelength()
        
        self.Driver_Document = None

#    def __queryAscii__(self,string):
#        return super().__queryAscii__(string,delimiter="\r\n")

    def SingleScan(self):
            self._visaObj.clear()
            self.__write__('SSI')
            self.__write__('CLS')
            
    def GetTrace(self,*args):
        if len(args)==2:
            scan=args[1]
        else:
            scan=1
        if scan!=0:
            self.SingleScan()
        start = time.time()  
        while int(self._visaObj.query('ESR2?')[0])==0 and time.time()-start < 20:
            time.sleep(1)
        
        start = float(self.__query__("STA?"))
        stop = float(self.__query__("STO?"))
        ydata = [float(TMP) for TMP in self.__query__('DMA?').splitlines()]
        xdata = np.linspace(start,stop,len(ydata))
        
        fig=plt.figure(100)
        try:
            plt.sca(fig.axes[2])
        except (IndexError,ValueError):
            pass
#            fig=plt.figure(100)
#            fig.subplots(3,1)
#            plt.sca(fig.axes[2])
        plt.plot(xdata,ydata)
        plt.xlabel('Wavelength(nm)')
        plt.ylabel('Power(dBm)')
        plt.grid(True)
        plt.show(block=False)
        plt.pause(0.001)
        class trace:
            pass
        trace.xdata=xdata
        trace.ydata=ydata
        return trace

    # This gets a value according to a command string and returns it as a float
    # This function is used by specific commands - eg: getStartWavelength using command "STA"
    def __getValue__(self,command):
        return self.__queryAscii__(command + "?")[0]

    # This function sets a value on the instrument
    # This function is used by specific commands - eg: setStartWavelength using command "STA", value 1200, valueName StartWavelength
    # IMPORTANT: Since we use camelcase, it is required to pass valueName capitalized as written in the function name - eg: get`StartWavelength`
    def __setValue__(self,command,value, valueName):
        self.__write__(command + ' ' + str(value))
        getFunction = getattr(self,"Get" + valueName) # This is the getter function for ValueName that we define for this class
        time.sleep(0.1)
        valRead = getFunction()

        # Add a space before each new word (In camelCase, new words begin with a capital letter)
        pretty_valueName = ""
        for l in valueName:
            if l.isupper():
                # capital means split word by a space
                pretty_valueName += " " + l
            else:
                pretty_valueName += l

        # Verify that the value is set correctly
        if abs(valRead-value)<0.005:
            print(pretty_valueName + ' is set correctly')
        else:
            raise Exception(pretty_valueName + " is set wrong. " + pretty_valueName + " is " + str(valRead))

    def GetStartWavelength(self):
        self.StartWavelength =  self.__getValue__("STA")
        return self.StartWavelength

    def SetStartWavelength(self,wavelength):
        self.__setValue__("STA", wavelength, "StartWavelength")

    def GetStopWavelength(self):
        self.StopWavelength = self.__getValue__("STO")
        return self.StopWavelength

    def SetStopWavelength(self,wavelength):
        self.__setValue__("STO", wavelength, "StopWavelength")

    def GetCenterWavelength(self):
        return self.__getValue__("CNT")

    def SetCenterWavelength(self,wavelength):
        self.__setValue__("CNT",wavelength,"CenterWavelength")

    def GetSpanWavelength(self):
        return self.__getValue__("SPN")

    def SetSpanWavelength(self, wavelength, valid_wavelengths=None):
        # Choose closest valid resolution
        if (valid_wavelengths):
            wavelength = min(valid_wavelengths, key=lambda x:abs(x-wavelength))
        return self.__setValue__("SPN", wavelength, "SpanWavelength")

    def GetResolution(self):
        return self.__getValue__("RES")

    def SetResolution(self,wavelength,valid_resolutions=None):
        # Choose closest valid resolution
        if (valid_resolutions):
            resolution = min(valid_resolutions, key=lambda x:abs(x-wavelength))
        else:
            resolution = wavelength
        self.__setValue__("RES",resolution,"Resolution")

    def GetPoints(self):
        return self.__getValue__("MPT")

    def SetPoints(self,points):
        # Choose closest valid resolution
        self.__setValue__("MPT",points, "Points")


        

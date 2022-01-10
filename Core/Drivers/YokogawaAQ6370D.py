# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 13:36:29 2020

@author: Daniel Hutama
"""

# Driver for YOKOGAWA AQ6370D optical spectrum analyser
# Should also work for any other YOKOGAWA AQ6370X series OSA.
# Developed by Daniel Hutama
# version 1.2 -- 18 Nov 2021
# may need to run "pip install pyserial" in anaconda prompt.

from __connection__ import Connection
import time
import numpy as np
import matplotlib.pyplot as plt


class AQ6370D(Connection):
        def __init__(self, addressString):
            Connection.__init__(self, addressString)
            
        def reset_inst(self):
            try: 
                OSA.__write__('*RST')
                print('OSA successfully reset.')
            except:
                print('Unable to reset OSA.')
            
        
        def GetInfo(self):
            # identifies manufacturer, model, PN, firmware version.
            try:
                info = self.__query__("*IDN?")
                print(info)
            except:
                print("Unable to retreive instrument information.")
                
        def write(self, cmd_str):
            try:
                self.__write__(cmd_str)
                print("({}) write command successfully sent to OSA.".format(cmd_str))
            except:
                print("ERROR: Failed to send write command to OSA. Try using the built-in __write__() function.")
            
        def read(self, cmd_str):
            try:
                out = self.__query__(cmd_str)
                print("{} read command successfully sent to OSA.".format(cmd_str))
                print(out)
            except:
                print("ERROR: Failed to send read command to OSA. Try using the built-in __query__() function.")
                
        def GetStartWavelength(self):
            WL = self.__query__(':sense:wav:star?')
            WL = float(WL)*1e9
            return WL
        
        def SetStartWavelength(self, wavelength):
            StopWL = self.__query__(':sens:wav:stop?')
            StopWL = float(StopWL)*1e9
            
            if wavelength >= StopWL:
                span = self.__query__(':sens:wav:span?')
                span = float(span)*1e9
                self.__write__(':sense:wav:stop {} M'.format((wavelength+span)*1e-9))
            wavelength = round(wavelength,2)
            self.__write__(':sense:wav:star {} M'.format(wavelength*1e-9))
            time.sleep(0.5)
            WL = AQ6370D.GetStartWavelength(self)
            if WL==wavelength:
                print('Start wavelength has been correctly set to {} nm.'.format(wavelength))
            else:
                print('ERROR: Unable to set start wavelength to desired value.')
        
        def GetStopWavelength(self):
            WL = self.__query__(':sense:wav:stop?')
            WL = float(WL)*1e9
            return WL
        
        def SetStopWavelength(self, wavelength):
            StartWL = self.__query__(':sens:wav:star?')
            StartWL = float(StartWL)*1e9
            if wavelength <= StartWL:
                span = self.__query__(':sens:wav:span?')
                span = float(span)*1e9
                self.__write__(':sense:wav:star {} M'.format((wavelength-span)*1e9))
            self.__write__(':sens:wav:stop {}'.format(wavelength/1e9))
            time.sleep(0.5)
            WL = AQ6370D.GetStopWavelength(self)
            if WL == wavelength:
                print('Stop wavelength has been correctly set to {} nm'.format(wavelength))
            else:
                print('ERROR: Unable to set stop wavelength to desired value.')
        
        def GetCenterWavelength(self):
            WL = self.__query__(':sense:wav:cent?')
            WL = float(WL)*1e9
            return WL
        
        def SetCenterWavelength(self, wavelength):
            wavelength = round(wavelength,2)
            self.__write__(':sens:wav:cent {} nm'.format(wavelength))
            time.sleep(0.5)
            WL = AQ6370D.GetCenterWavelength(self)
            if abs(WL-wavelength)<=0.1:
                print('Center wavelength has been set correctly to {} nm'.format(wavelength))
            else:
                print('ERROR: Unable to set center wavelength to desired value.')
        
        def GetSpanWavelength(self):
            WL = self.__query__(':sense:wav:span?')
            WL = float(WL)*1e9
            return WL
        
        def SetSpanWavelength(self, wavelength):
            wavelength = round(wavelength,2)
            self.__write__(':sens:wav:span {} nm'.format(wavelength))
            time.sleep(0.5)
            WL = AQ6370D.GetSpanWavelength(self)
            if abs(WL-wavelength)<0.5:
                print('Span wavelength has been set correctly.')
            else:
                print('ERROR: Unable to set span wavelength to desired value.')
        
        def GetResolution(self):
            WL = self.__query__(':sense:band:res?')
            WL = float(WL)*1e9
            return WL
        
        def SetResolution(self, rbwSet):
            self.__write__(':sense:band:res {}'.format(rbwSet/1e9))
            time.sleep(0.5)
            rbwGet = AQ6370D.GetResolution(self)
            if rbwGet == rbwSet:
                print('Resolution is set correctly to {}'.format(rbwSet))
            else:
                print('ERROR: Unable to set resolution to desired value.')
        
        def GetPoints(self):
            PT = self.__query__(':sense:swe:poin?')
            return int(PT)
        
        def SetPoints(self, Point):
            self.__write__(':sense:swe:poin {}'.format(Point))
            time.sleep(0.5)
            PT = AQ6370D.GetPoints(self)
            if PT==Point:
                print('Point has been set correctly to {}'.format(Point))
            else:
                print('ERROR: Unable to set Point to desired value')
        
        def GetResolutionCorrection(self):
            rc = self.__query__(':sense:setting:correction?')
            return rc
        
        def SetResolutionCorrection(self, flag):
            if flag == 1:
                self.__write__(':sense:setting:correction ON')
                time.sleep(0.5)
                if int(AQ6370D.GetResolutionCorrection(self)) == 1:
                    print('Resolution correction flag correctly set to 1.')
                else:
                    print('Unable to set resolution correction flag to desired value.')
            elif flag == 0:
                self.__write__(':sense:setting:correction OFF')
                time.sleep(0.5)
                if int(AQ6370D.GetResolutionCorrection(self)) == 0:
                    print('Resolution correction flag correctly set to 0.')
                else:
                    print('Unable to set resolution correction flag to desired value.')
            else:
                print('ERROR: Resolution correction flag must be 0 or 1.')
        
        def GetSensitivity(self):
            sens = self.__query__(':sens:sens?')
            return sens
        
        def SetSensitivity(self, sensitivity): #takes integer argument for sensitivity.
            self.__write__(':sens:sens {}'.format(sensitivity))
            time.sleep(1)
            truesens = AQ6370D.GetSensitivity(self)
            if int(truesens) == sensitivity:
                print('Sensitivity successfully set to {}.'.format(sensitivity))
            else:
                print('ERROR: Unable to set desired sensitivity.')
            
        def SingleScan(self):
            self._visaObj.clear()
            try:
                AQ6370D.write(self, ':init:smode 1')
                AQ6370D.write(self, '*CLS')
                AQ6370D.write(self, ':init')
                print('------------------------------')
                print('Scan commands successfully sent to OSA.')
            except:
                print("ERROR: Unable to send single scan commands to OSA.")
        
        
        
        def GetTrace(self, scan_exists):
            self._visaObj.clear()
            AQ6370D.SetStartWavelength(self,1525)
            AQ6370D.SetStopWavelength(self,1575)
            AQ6370D.SetPoints(self,1001)
            if scan_exists == 1:
                pass
            else:
                AQ6370D.SingleScan(self)
            yvals = self.__query__(':TRACE:Y? TRA')
            yvals = yvals.split(',')
            yvals[-1] = yvals[-1][:-2] # deletes terminating \n in string of last element
            
            for i,y in enumerate(yvals):
                yvals[i] = float(y) # convert data strings to float values
            yvals = np.array(yvals) # convert to numpy array
            
            startx = AQ6370D.GetStartWavelength(self)
            stopx = AQ6370D.GetStopWavelength(self)
            xvals = np.linspace(startx, stopx, len(yvals))
            
            plt.scatter(xvals, yvals)
            plt.grid()
            plt.show()
            
                

if __name__=='__main__':
    A = AQ6370D
    OSA = Connection("0.9")
    A.GetInfo(OSA)
    verify = 0 #change to 1 to test if functions perform as expected.
    if verify == 1:
        # functionality verification
        A.SetSensitivity(OSA,2)
        print(A.GetSensitivity(OSA))
        A.SetPoints(OSA, 2001)
        print(A.GetPoints(OSA))
        A.SetResolution(OSA,2) 
        print(A.GetResolution(OSA))
        A.SetSpanWavelength(OSA, 50)
        print(A.GetSpanWavelength(OSA))
        A.SetCenterWavelength(OSA,1550)
        print(A.GetCenterWavelength(OSA))
        A.SetStopWavelength(OSA, 1575)
        print(A.GetStopWavelength(OSA))
        A.SetResolutionCorrection(OSA,1)
        print(A.GetResolutionCorrection(OSA))
        A.SetStartWavelength(OSA,1525)
        print(A.GetStartWavelength(OSA))
    else:
        # A.reset_inst(OSA)
        A.SingleScan(OSA)
        A.GetTrace(OSA,0)
        
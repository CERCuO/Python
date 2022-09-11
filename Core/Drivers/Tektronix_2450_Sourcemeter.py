# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 08:31:48 2022

@author: danhu
"""

# import sys
# sys.path.append('C:\\depot\\CERC\\Python\\Core\\Drivers\\inst_specific_files')
o

# driver for Tektronix 2450 Sourcemeter
# developed by Daniel Hutama
# dhuta087@uottawa.ca
# Version 00.100 | 08 Aug 2022 | Initial structure setup

# This devices uses IEEE 488.2
# Standard Commands for Programmable Instruments (SCPI)
# It also supports TSP commands but only weirdos use them.
# You can check which language the instrument is using by sending a *LANG? command.

#be sure to add "drivers" and "dependencies" folder to your machine's syspath
# github.com/CERCuO/Python
# The next 3 lines are specific for my computer, where I dumped all the github files into \depot\CERC
import sys
sys.path.append('C:\\depot\\CERC\\Python\\Core\\Dependencies')
sys.path.append('C:\\depot\\CERC\\Python\\Core\\Drivers')


# you may need to run this class twice if modules are not properly loaded.

# the code should be relatively straightforward to read

from __connection__ import Connection
from datetime import datetime
import numpy as np

class Tektronix_2450_Sourcemeter(Connection):
    def __init__(self,addressString):
        Connection.__init__(self,addressString)
        self.Manual = 'Tek_2450_Sourcemeter.pdf'
        
    def GetInfo(self):
        try:
            idn = self.__query__('*IDN?')
            return idn
        except:
            print('<< ERROR: Unable to get device information. Check connectivity. >>')
            
    def GetSTR(self, cmd):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <{}>'.format(now, cmd.upper()))      
        res = self.__query__(cmd)
        return res
    
    def EnableOutput(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <SET OUTPUT ON>'.format(now))        
        self.__write__(':OUTP:STAT ON')
        
    def DisableOutput(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <SET OUTPUT OFF>'.format(now))        
        self.__write__(':OUTP:STAT OFF')

    def SetSource_Voltage(self, voltage):
        # units in volts
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <SET SOURCE: VOLTAGE AT {} V>'.format(now, voltage))        
        self.__write__(':SOUR:FUNC VOLT')        
        self.__write__(':SOUR:VOLT:RANG {}'.format(voltage))

    def SetSource_Current(self, current):
        # units in Amperes
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <SET SOURCE: CURRENT AT {} A>'.format(now, current))        
        self.__write__(':SOUR:FUNC CURR')        
        self.__write__(':SOUR:CURR:RANG {}'.format(current))
        
    def GetCurrent(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <GET CURRENT>'.format(now))        
        self.__query__(':MEAS:CURR?')        
    
    def GetVoltage(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <GET VOLTAGE>'.format(now))        
        self.__query__(':MEAS:VOLT?')        
        
    def GetResistance(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <GET RESISTANCE>'.format(now))        
        self.__query__(':MEAS:RES?')        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
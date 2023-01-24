# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 08:31:48 2022

@author: Daniel Hutama
dhuta087@uottawa.ca
"""

# import sys
# sys.path.append('C:\\depot\\CERC\\Python\\Core\\Drivers\\inst_specific_files')


# driver for Tektronix 2450 Sourcemeter
# developed by Daniel Hutama
# dhuta087@uottawa.ca

# This devices uses IEEE 488.2
# Standard Commands for Programmable Instruments (SCPI)

#be sure to add "drivers" and "dependencies" folder to your machine's syspath
# github.com/CERCuO/Python
# The next 3 lines are specific for my computer, where I dumped all the github files into \depot\CERC
import sys
sys.path.append('C:\\depot\\CERC\\Python\\Core\\Dependencies')
sys.path.append('C:\\depot\\CERC\\Python\\Core\\Drivers')


# you may need to run this class twice if modules are not properly loaded.

from __connection__ import Connection
from datetime import datetime
import numpy as np

class Tektronix_2400(Connection):
    def __init__(self,addressString):
        Connection.__init__(self,addressString)
        self.Manual = 'Tek_2400_Sourcemeter.pdf'
        
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
    
    def SetSTR(self, cmd):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <{}>'.format(now, cmd.upper()))      
        res = self.__write__(cmd)
        return res
    
    def GetActiveFunction(self):
        res = self.GetSTR("CONF?")
        l = res.split(',')
        if len(l) == 2:
            if eval(l[1]) == 'RES':
                print('Active function is CURR, RES')
                return 'RES'
            else:
                print("unknown result obtained. Check code if you see this line.")
        elif len(l) == 1:
            if 'CURR' in eval(l[0]):
                print('Active function is CURR')
                return 'CURR'
            elif 'VOLT' in eval(l[0]):
                print('Active function is VOLT')
                return 'VOLT'

        
    def SetActiveFunction(self, cmd):
        options = ['VOLT', 'CURR', 'RES']
        if cmd not in options:
            print('You must pass one of the following options: "VOLT", "CURR", "RES"' )
        else:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print('{}   |   <SET FUNCTION TO {}>'.format(now, cmd.upper()))      
            res = self.__write__('CONF:{}'.format(cmd))
            self.GetActiveFunction()
            return res

    
    def MeasureCurrent(self):
        return self.GetSTR('MEAS:CURR?')
    
    def MeasureVoltage(self):
        return self.GetSTR('MEAS:VOLT?')

    def MeasureResistance(self):
        return self.GetSTR('MEAS:RES?')        
    
    def MeasureMean(self):
        return self.GetSTR('CALC3:FORM MEAN')
    
    def GetStatisticType(self):
        return self.GetSTR('CALC3:FORM?')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
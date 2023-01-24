# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 14:46:29 2023

@author: danhu
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

class Tektronix_MDO3104(Connection):
    def __init__(self,addressString):
        Connection.__init__(self,addressString)
        self.Manual = 'Tek_MDO3104_Oscilloscope.pdf'
        
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
        return 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
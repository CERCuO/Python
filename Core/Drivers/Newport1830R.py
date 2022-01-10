# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 12:02:43 2021

@author: danhu
"""

from __connection__ import Connection
import time
import math


class Newport1830R(Connection):
    def __init__(self,addressString):
        Connection.__init__(self,addressString)
        self.Manual = 'Newport1830R.pdf'
        
    def GetInfo(self):
        try:
            idn = self.__query__('*IDN?')
            return idn
        except:
            print('<< ERROR: Unable to get device information. Check connectivity. >>')

    def Reset(self):
        try:
            self.__write__('*RST')
        except:
            print('<< ERROR: Unable to send reset command. Check connectivity. >>' )

        
    def GetSTR(self, cmd):
        res = self.__query__(cmd)
        return res
    
    def AttenuatorON(self):
        self.__write__('AO')
        
    def AttenuatorOFF(self):
        self.__write__('A1')
        
    def GetStatusAttenuator(self):
        res = self.__query__('A?')
        return res
    
    def GetWavelength(self):
        res = self.__query__('W?')
        return round(float(res), 4)    
    
    def SetWavelength(self, val):
        strval = str(val)
        if len(strval) == 3:
            strval = '0' + strval
        elif len(strval == 4):
            pass
        else:
            print('<< ERROR: Value out of range. Enter wavelength in nm. >>')
        self.__write__('W{}'.format(strval))
        
    
    #placeholder for driver to be completed later
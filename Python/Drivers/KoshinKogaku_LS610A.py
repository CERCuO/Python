# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 13:19:21 2021

@author: danhu
"""

from __connection__ import Connection
import time
import math


class KoshinKogaku_LS610A(Connection):
    def __init__(self,addressString):
        Connection.__init__(self,addressString)
        self.Manual = 'KoshinKogaku_LS610A.pdf'
        
    def GetInfo(self):
        try:
            idn = self.__query__('*IDN?')
            return idn
        except:
            print('<< ERROR: Unable to get device information. Check connectivity. >>')

    def Reset(self):
        decision = input('<< WARNING: You are about to initialize the device to factory default settings. Do you wish to proceed? (Y/N) >>')
        if decision.upper() == 'Y':
            try:
                self.__write__('*RST')
            except:
                print('<< ERROR: Unable to send reset command. Check connectivity. >>' )
        else:
            print('<< Did not receive "Y" command. Aborting device reset. >>')
        
    def GetSTR(self, cmd):
        res = self.__query__(cmd)
        return res
    
    def OutputON(self):
        self.__write__('ST1')
        
    def OutputOFF(self):
        self.__write__('ST0')
        
        
    def GetStatusAttenuator(self):
        res = self.__query__('A?')
        return res
    
    def GetWavelength(self):
        res = self.__query__('WL?')
        ans = round(float(res), 4)
        return ans    
    
    def SetWavelength(self, val):
        strval = str(val)
        try:
            iDot = strval.index('.')
        except:
            strval = strval + '.'
            iDot = strval.index('.')
        if  iDot.index('.') == 4:
            pass
        elif iDot.index('.') < 4:
            wile iDot.index
        
            
        
        
        
            
        if len(strval) == 3:
            strval = '0' + strval
        elif len(strval == 4):
            pass
        else:
            print('<< ERROR: Value out of range. Enter wavelength in nm. >>')
        self.__write__('W{}'.format(strval))
        
    def GetFrequency(self):
        res = self.__query__('WF?')
        ans = round(float(res), 5)
        return ans
    
    def SetFrequency(self, val):
        strval = str(val)
    
        
    
    #placeholder for driver to be completed later
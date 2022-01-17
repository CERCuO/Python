# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 13:52:53 2022

@author: danhu
"""

# driver for Tektronix AWG 610 arbitrary waveform generator
# developed by Daniel Hutama
# dhuta087@uottawa.ca
# Version 0.1 17 Jan 2022 (Python build)

# This devices uses IEEE 488.2
# Standard Commands for Programmable Instruments (SCPI)

class Tektronix_AWG610(Connection):
    def __init__(self,addressString):
        Connection.__init__(self,addressString)
        self.ManualURL = 'https://download.tek.com/manual/070A81050.pdf'
        self.Model = 'Tektronix AWG610'
        
    def GetInfo(self):
        try:
            idn = self.__query__('*IDN?')
            return idn
        except:
            print('<< ERROR: Unable to get device information. Check connectivity. >>')
            
            
    def GetRunState(self):
        pass
    
    def GetAmplitude(self):
        pass
    
    def SetAmplitude(self, amplitude):
        pass
    
    def GetFrequency(self):
        pass
    
    def SetFrequency(self, freq):
        pass
    
    def GetOutputState(self):
        pass
    
    def SetOutputState(self, state):
        pass
    
    def GetLowPassFilterFrequency(self):
        pass
    
    def SetLowPassFilterFrequency(self, freq):
        pass
    
    def GetCustomWaveform(self):
        pass
    
    def SetCustomWaveform(self, filename):
        pass
    
    def GetReferenceOscillator(self):
        pass
    
    def SetReferenceOscillator(self):
        pass 
    
    def GetVoltageOffsetDC(self):
        pass
    
    def SetVoltageOffsetDC(self, offset):
        pass
    
    def ResetAWG(self):
        pass
    
    def SetForceTrigger(self):
        pass
    
    def GetTrigImpedance(self):
        pass
    
    def SetTrigImpedance(self, impedance):
        pass
    
    def GetTrigLevel(self):
        pass
    
    def SetTrigLevel(self, level):
        pass
    
    def GetTrigPolarity(self):
        pass
    
    def SetTrigPolarity(self, polarity):
        pass
    
    def GetTrigSlope(self):
        pass
    
    def SetTrigSlope(self, slope):
        pass
    
    def GetTrigSource(self):
        pass
    
    def SetTrigSource(self, source):
        pass
    
    def GrabScreen(self, savefilename):
        pass
    
    def GetFileList(self):
        pass
    
    def CopyFile(self, filename, copyname):
        pass
    
    def LoadFile(self, filename):
        pass
    
    def DeleteFile(self, filename):
        pass
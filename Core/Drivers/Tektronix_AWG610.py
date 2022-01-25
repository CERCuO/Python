# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 13:52:53 2022

@author: danhu
"""

# driver for Tektronix AWG 610 arbitrary waveform generator
# developed by Daniel Hutama
# dhuta087@uottawa.ca
# Version 00.100 | 17 Jan 2022 | Python build translated from Matlab
# Version 00.101 | 25 Jan 2022 | Added query functionalilty


# This devices uses IEEE 488.2
# Standard Commands for Programmable Instruments (SCPI)

#be sure to add "drivers" and "dependencies" folder to your machine's syspath
import sys
sys.path.append('C:\\depot\\CERC\\Python\\Core\\Dependencies')
sys.path.append('C:\\depot\\CERC\\Python\\Core\\Drivers')

# you may need to run this class twice if modules are not properly loaded.

from __connection__ import Connection
from datetime import datetime
import re

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
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET RUN STATE>'.format(now))
        try:
            tmp = self.__query__('AWGC:RST?')
            print('<<RUN STATE>> | {}'.format(tmp))
            return tmp
        except:
            print('<<ERROR>> Unable to communicate with device.')

    
    def GetAmplitude(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET AMPLITUDE>'.format(now))
        try:
            tmp = self.__query__('SOUR:VOLT:AMPL?')
            print('<<AMPLITUDE>> | {}'.format(tmp))
            return tmp
        except:
            print('<<ERROR>> Unable to communicate with device.')
    
    def SetAmplitude(self, amplitude):
        pass
    
    def GetFrequency(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET FREQUENCY>'.format(now))
        try:
            tmp = self.__query__('SOUR:FREQ:CW?')
            print('<<FREQUENCY>> | {}'.format(tmp))
            return tmp
        except:
            print('<<ERROR>> Unable to communicate with device.')
            
    def SetFrequency(self, freq):
        pass
    
    def GetOutputState(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET OUTPUT STATE>'.format(now))
        try:
            tmp = self.__query__('OUTP:STAT?')
            print('<<OUTPUT STATE>> | {}'.format(tmp))
            return tmp
        except:
            print('<<ERROR>> Unable to communicate with device.')
            
    def SetOutputState(self, state):
        pass
    
    def GetLowPassFilterFrequency(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET LP FILTER FREQUENCY>'.format(now))
        try:
            tmp = self.__query__('OUTP:FILT:LPAS:FREQ?')
            print('<<LP FILTER FREQUENCY>> | {}'.format(tmp))
            return tmp
        except:
            print('<<ERROR>> Unable to communicate with device.')
                    
    
    def SetLowPassFilterFrequency(self, freq):
        pass
    
    def GetCustomWaveform(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET CUSTOM WAVEFORM>'.format(now))
        try:
            tmp = self.__query__('SOUR:FUNC:USER?')
            print('<<CUSTOM WAVEFORM>> | {}'.format(tmp))
            return tmp
        except:
            print('<<ERROR>> Unable to communicate with device.')
            
    
    def SetCustomWaveform(self, filename):
        pass
    
    def GetReferenceOscillator(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET REFERENCE OSCILLATOR>'.format(now))
        try:
            tmp = self.__query__('SOUR:ROSC:SOUR?')
            print('<<REFERENCE OSCILLATOR>> | {}'.format(tmp))
            return tmp
        except:
            print('<<ERROR>> Unable to communicate with device.')
            
    
    def SetReferenceOscillator(self):
        pass 
    
    def GetVoltageOffsetDC(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET VOLTAGE OFFSET DC>'.format(now))
        try:
            tmp = self.__query__('SOUR:VOLT:LEV:IMM:OFFS?')
            print('<<VOLTAGE OFFSET DC>> | {}'.format(tmp))
            return tmp
        except:
            print('<<ERROR>> Unable to communicate with device.')
            
    
    def SetVoltageOffsetDC(self, offset):
        pass
    
    def ResetAWG(self):
        pass
    
    def SetForceTrigger(self):
        pass
    
    def GetTrigImpedance(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET TRIGGER IMPEDANCE>'.format(now))
        try:
            tmp = self.__query__('TRIG:SEQ:IMP?')
            print('<<TRIGGER IMPEDANCE>> | {}'.format(tmp))
            return tmp
        except:
            print('<<ERROR>> Unable to communicate with device.')
            
    def SetTrigImpedance(self, impedance):
        pass
    
    def GetTrigLevel(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET TRIGGER LEVEL>'.format(now))
        try:
            tmp = self.__query__('TRIG:SEQ:LEV?')
            print('<<TRIGGER LEVEL>> | {}'.format(tmp))
            return tmp
        except:
            print('<<ERROR>> Unable to communicate with device.')
            
    
    def SetTrigLevel(self, level):
        pass
    
    def GetTrigPolarity(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET TRIGGER POLARITY>'.format(now))
        try:
            tmp = self.__query__('TRIG:POL?')
            print('<<TRIGGER POLARITY>> | {}'.format(tmp))
            return tmp
        except:
            print('<<ERROR>> Unable to communicate with device.')
            
    
    def SetTrigPolarity(self, polarity):
        pass
    
    def GetTrigSlope(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET TRIGGER SLOPE>'.format(now))
        try:
            tmp = self.__query__('TRIG:SLOP?')
            print('<<TRIGGER SLOPE>> | {}'.format(tmp))
            return tmp
        except:
            print('<<ERROR>> Unable to communicate with device.')
            
    def SetTrigSlope(self, slope):
        pass
    
    def GetTrigSource(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET TRIGGER SOURCE>'.format(now))
        try:
            tmp = self.__query__('TRIG:SEQ:SOUR?')
            print('<<TRIGGER SOURCE>> | {}'.format(tmp))
            return tmp
        except:
            print('<<ERROR>> Unable to communicate with device.')
            
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
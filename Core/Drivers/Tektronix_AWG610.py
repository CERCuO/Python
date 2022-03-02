# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 13:52:53 2022

@author: danhu
"""

# import sys
# sys.path.append('C:\\depot\\CERC\\Python\\Core\\Drivers\\Tektronix_AWG610_files')


# driver for Tektronix AWG 610 arbitrary waveform generator
# developed by Daniel Hutama
# dhuta087@uottawa.ca
# Version 00.100 | 17 Jan 2022 | Python build structure translated from Matlab
# Version 00.101 | 25 Jan 2022 | Added query (read) functionalilty
# Version 01.000 | 26 Jan 2022 | Added write functionality
# Version 01.100 | 10 Feb 2022 | Fixed bugs in AWG file navigation

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

class Tektronix_AWG610(Connection):
    def __init__(self,addressString):
        Connection.__init__(self,addressString)
        self.ManualURL = 'https://download.tek.com/manual/070A81050.pdf'
        self.Model = 'Tektronix AWG610'
        
    def GetInfo(self):
        try:
            idn = self.__query__('*IDN?')
            return idn[:-2]
        except Exception as e:
            print('<< ERROR: Unable to get device information. Check connectivity. >>')
            print(e)
            
    def GetRunState(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET RUN STATE>'.format(now))
        try:
            tmp = self.__query__('AWGC:RST?')
            print('<<RUN STATE>> | {}'.format(tmp))
            print('0 - WG is stopped. | 1 - WG is waiting for a trigger. | 2 - WG is running.')
            return tmp[:-2]
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    

    
    def GetAmplitude(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET AMPLITUDE>'.format(now))
        try:
            tmp = self.__query__('SOUR:VOLT:AMPL?')
            print('<<AMPLITUDE>> | {}'.format(tmp))
            return tmp[:-2]
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
    
    def SetAmplitude(self, amplitude):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <SET AMPLITUDE | {}>'.format(now, amplitude))        
        try:
            self.__write__('SOUR:VOLT:AMPL {}'.format(amplitude))
            return self.GetAmplitude()
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
    
    def GetFrequency(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET FREQUENCY>'.format(now))
        try:
            tmp = self.__query__('SOUR:FREQ:CW?')
            print('<<FREQUENCY>> | {}'.format(tmp))
            return tmp[:-2]
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
            
    def SetFrequency(self, freq):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <SET FREQUENCY | {}>'.format(now, freq))        
        try:
            self.__write__('SOUR:FREQ:CW {}'.format(freq))
            return self.GetFrequency()
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
    
    def GetOutputState(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET OUTPUT STATE>'.format(now))
        try:
            tmp = self.__query__('OUTP:STAT?')
            print('<<OUTPUT STATE>> | {}'.format(tmp))
            return tmp[:-2]
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
    def SetOutputState(self, state):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <SET OUTPUT STATE | {}>'.format(now, state))        
        try:
            self.__write__('OUTP:STAT {}'.format(state))
            return self.GetOutputState()
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
    
    def GetLowPassFilterFrequency(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET LP FILTER FREQUENCY>'.format(now))
        try:
            tmp = self.__query__('OUTP:FILT:LPAS:FREQ?')
            print('<<LP FILTER FREQUENCY>> | {}'.format(tmp))
            return tmp[:-2]
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
                    
    def SetLowPassFilterFrequency(self, freq):
        options = [20e6, 50e6, 100e6, 200e6, 9.9e37]
        if freq in options == True:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print('{} | COMMAND: <SET LP FILTER FREQUENCY | {}>'.format(now, freq)) 
            try:
                self.__write__('OUTP:FILT:LPAS:FREQ {}'.format(freq))
                return self.GetLowPassFilterFrequency()
            except Exception as e:
                print('<<ERROR>> Unable to communicate with device.')
                print(e)
        else:
            print("<<ERROR>> Specified frequency is not in the list of available options.")
            print("Available frequencies are 20e6, 50e6, 100e6, 200e6, 9.9e37 (infinity).")
            return self.GetLowPassFilterFrequency()
    
    def GetCustomWaveform(self, channel):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        channel = str(channel)
        print('{} | COMMAND: <GET CUSTOM WAVEFORM ON CHANNEL {}>'.format(now, channel))
        try:
            tmp = self.__query__('SOUR{}:FUNC:USER?'.format(channel))
            print('<<CUSTOM WAVEFORM>> | {} | CHANNEL {}'.format(tmp, channel))
            return tmp[:-2]
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
            
    
    def SetCustomWaveform(self, channel, filename, directory = 'MAIN'):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <SET CUSTOM WAVEFORM ON CHANNEL {}| {}>'.format(now, channel, filename))        
        try:
            mystring = 'SOUR{}:FUNC:USER "{}","{}"'.format(channel, filename, directory)
            self.__write__(mystring)
            return self.GetCustomWaveform(channel)
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
            
            
    def GetReferenceOscillator(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET REFERENCE OSCILLATOR>'.format(now))
        try:
            tmp = self.__query__('SOUR:ROSC:SOUR?')
            print('<<REFERENCE OSCILLATOR>> | {}'.format(tmp))
            return tmp[:-2]
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
            
    
    def SetReferenceOscillator(self, ref):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <SET REFERENCE OSCILLATOR | {}>'.format(now, ref))        
        try:
            self.__write__('SOUR:ROSC:SOUR {}'.format(ref))
            return self.GetReferenceOscillator()
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
    
    def GetVoltageOffsetDC(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET VOLTAGE OFFSET DC>'.format(now))
        try:
            tmp = self.__query__('SOUR:VOLT:LEV:IMM:OFFS?')
            print('<<VOLTAGE OFFSET DC>> | {}'.format(tmp))
            return tmp[:-2]
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
            
    
    def SetVoltageOffsetDC(self, offset):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <SET VOLTAGE OFFSET DC | {}>'.format(now, offset))
        try:
            self.__write__('SOUR:VOLT:LEV:IMM:OFFS {} mV'.format(offset))
            return self.GetVoltageOffsetDC()
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
 
 
    def ResetAWG(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <RESET>'.format(now))        
        try:
            self.__write__('*RST')
            return self.GetOutputState()
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
    
    def SetForceTrigger(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <FORCE TRIGGER>'.format(now))        
        try:
            self.__write__('*TRG')
            return self.GetTrigLevel()
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                       
    
    def GetTrigImpedance(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET TRIGGER IMPEDANCE>'.format(now))
        try:
            tmp = self.__query__('TRIG:SEQ:IMP?')
            print('<<TRIGGER IMPEDANCE>> | {}'.format(tmp))
            return tmp[:-2]
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
            
    def SetTrigImpedance(self, impedance):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <SET TRIGGER IMPEDANCE | {}>'.format(now, impedance))        
        try:
            self.__write__('TRIG:SEQ:IMP {}'.format(impedance))
            return self.GetTrigImpedance()
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
    
    def GetTrigLevel(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET TRIGGER LEVEL>'.format(now))
        try:
            tmp = self.__query__('TRIG:SEQ:LEV?')
            print('<<TRIGGER LEVEL>> | {}'.format(tmp))
            return tmp[:-2]
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
    def SetTrigLevel(self, level):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <SET TRIGGER LEVEL | {}>'.format(now, level))        
        try:
            self.__write__('TRIG:SEQ:LEV {}'.format(level))
            return self.GetTrigLevel()
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
            
    def GetTrigPolarity(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET TRIGGER POLARITY>'.format(now))
        try:
            tmp = self.__query__('TRIG:POL?')
            print('<<TRIGGER POLARITY>> | {}'.format(tmp))
            return tmp[:-2]
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
    
    def SetTrigPolarity(self, polarity):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <SET TRIGGER POLARITY | {}>'.format(now, polarity))        
        try:
            self.__write__('TRIG:POL {}'.format(polarity))
            return self.GetTrigPolarity()
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
    def GetTrigSlope(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET TRIGGER SLOPE>'.format(now))
        try:
            tmp = self.__query__('TRIG:SLOP?')
            print('<<TRIGGER SLOPE>> | {}'.format(tmp))
            return tmp[:-2]
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
            
    def SetTrigSlope(self, slope):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <SET TRIGGER SLOPE | {}>'.format(now, slope))        
        try:
            self.__write__('TRIG:SLOP {}'.format(slope))
            return self.GetTrigSlope()
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
    
    def GetTrigSource(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET TRIGGER SOURCE>'.format(now))
        try:
            tmp = self.__query__('TRIG:SEQ:SOUR?')
            print('<<TRIGGER SOURCE>> | {}'.format(tmp))
            return tmp[:-2]
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
    def SetTrigSource(self, source):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <SET TRIGGER SOURCE | {}>'.format(now, source))        
        try:
            self.__write__('TRIG:SEQ:SOUR {}'.format(source))
            return self.GetTrigSource()
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
            
            
    def GrabScreen(self, savefilename):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GRAB SCREEN | {}>'.format(now, savefilename))        
        try:
            self.__write__('MMEM:NAME "{}";:HCOP:SDUM:IMM'.format(savefilename))
            print("File has been saved.")
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
    
    def GetFileList(self, location='MAIN'):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <DISPLAY FILE LIST>'.format(now)) 
        if location == 'MAIN':
            print('Displaying files in "MAIN"')
            print('To display contents of another location, pass the location name as a string into the second argument.')
        try:
            return self.__query__('MMEM:CAT? "{}"'.format(location))
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
            
    def GetCurrentDirectory(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET CURRENT DIRECTORY>'.format(now)) 
        try:
            return self.GetSTR('MMEM:CDIR?')
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
    
    def SetCurrentDirectory(self, pathstr):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <SET CURRENT DIRECTORY "{}">'.format(now, pathstr))      
        try:
            self.SetSTR('MMEM:CDIR "{}"'.format(pathstr))
            print(self.GetCurrentDirectory())
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
            
    def MakeNewDirectory(self, dirname):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <MAKE DIRECTORY "{}">'.format(now, dirname))
        try:
            self.SetSTR('MMEM:MDIR "{}"'.format(dirname))
            print('Current directory is {}'.format(self.GetCurrentDirectory()))
            print('Current directory contents are {}'.format(self.GetFileList()))
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)            
            
    def MoveFile(self, filename, filedir, newfilename, newfiledir):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <MOVE FILE | FNAME:"{}" | FDIR:"{}" | NEW FNAME:"{}" | NEW FDIR:"{}">'.format(now, filename, filedir, newfilename, newfiledir))
        try:
            self.SetSTR('MMEM:MOVE "{}", "{}", "{}", "{}"'.format(filename, filedir, newfilename, newfiledir))
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)            
        
    
    def CopyFile(self, filename, copyname, sourcefolder ="MAIN", targetfolder="MAIN"):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <COPY FILE | SOURCE:{} TARGET:{} SOURCEFOLDER:{} TARGETFOLDER:{}>'.format(now, filename, copyname, sourcefolder, targetfolder))        
        try:
            self.__write__('MMEM:COPY "{}" "{}" "{}" "{}"'.format(filename, sourcefolder, copyname, targetfolder))
            print("File has been copied.")
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
            
    def GetCurrentFile(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET CURRENT FILENAME>'.format(now))
        try:
            return self.GetSTR('MMEM:NAME?')
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)        
                    
    
    def LoadFile(self, filename):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <LOAD FILE | {}>'.format(now, filename))        
        try:
            self.__write__('MMEM:DATA "{}"'.format(filename))
            print("File loaded.")
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
    
    
    def DeleteFile(self, filename):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <DELETE FILE | {}>'.format(now, filename))        
        try:
            self.__write__('MMEM:DEL "{}"'.format(filename))
            print("File deleted.")
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
            
    def SetSTR(self, cmd):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <{}>'.format(now, cmd))  
        try:
            self.__write__('{}'.format(cmd))
            print('Command sent successfully.')
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    

    def GetSTR(self, cmd):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | QUERY: <{}>'.format(now, cmd))
        try:
            return self.__query__('{}'.format(cmd))
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)
                    
    def CheckConnection(self): #Instructs the AWG to generate an audible tone.
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <MAKE AUDIBLE BEEP>'.format(now))
        try: 
            self.SetSTR('SYST:BEEP')
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)            
            
    def GetUptime(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{} | COMMAND: <GET UPTIME>'.format(now))
        try:
            return self.GetSTR('SYST:UPT')
        except Exception as e:
            print('<<ERROR>> Unable to communicate with device.')
            print(e)                        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 13:19:21 2021

@author: Daniel Hutama (dhuta087@uottawa.ca)
"""


import sys
sys.path
sys.path.append('C:\\Users\\srv_joule\\Desktop\\Ryan Hogan Data\\GitHub_Dump\\Python\\Dependencies')

from __connection__ import Connection
from datetime import datetime
import re


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
                now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                print('{}   |   <RESET COMMAND SENT>'.format(now))
            except:
                print('<< ERROR: Unable to send reset command. Check connectivity. >>' )
        else:
            print('<< ERROR: Did not receive "Y" command. Aborting device reset. >>')
        
    def GetSTR(self, cmd):
        res = self.__query__(cmd)
        return res
    
    def OutputON(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <SET OUTPUT ON>'.format(now))        
        self.__write__('ST1')
        
    def OutputOFF(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <SET OUTPUT OFF>'.format(now))        
        self.__write__('ST0')
        
        
    def GetStatusAttenuator(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <GET ATTENUATOR STATUS>'.format(now))      
        res = self.__query__('A?')
        print('<< Attenuator status is {}. >>'.format(res))
        return res
    
    def GetWavelength(self):
        res = self.__query__('WL?')
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <GET WAVELENGTH>'.format(now))     
        res = re.sub('[^0-9\.]', '', res) #regex filters added 2021-11-23
        ans = round(float(res), 5)
        print('<< Wavelength is currently set to  {} nm. >>'.format(ans))        
        return ans    
    
    def SetWavelength(self, val):
        strval = str(val)
        try:
            iDot = strval.index('.') #iDot is index of '.'
        except: #no '.' given as argument -> integer wavelength
            strval = strval + '.' # add '.' to start of string
            iDot = strval.index('.')
        if  iDot == 4: #correct place
            pass
        elif iDot < 4: #add more integer space holders
            while iDot < 4:
                strval = '0' + strval #add zero to string start
                iDot = strval.index('.') 
        else:
            print('<< ERROR: Desired wavelength out of range! >>')
        
        if len(strval)<10:
            while len(strval) < 10:
                strval = strval + '0'
        else:
            strval = strval[0:9]
            print('<< WARNING: Wavelength truncated to 5 decimal places. >>')
            
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <SET WAVELENGTH {}>'.format(now, strval))                 
        self.__write__('W{}'.format(strval)) # send formatted command
        
        try:
            wl = self.GetWavelength()
            if int(wl) == int(val):
                print('<< Wavelength has been properly set to the desired value. >>')
            else:
                print('<< ERROR: Unable to set wavelength to the desired value. Wavelength is currently {} nm. >>'.format(wl))
            return wl
        except: 
            print('<< ERROR: Failed to query wavelength value. Check connectivity and then check code. >>')
        
    
    def GetFrequency(self):
        res = self.__query__('WF?')
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <GET FREQUENCY>'.format(now)) 
        res = re.sub('[^0-9\.]', '', res)
        ans = round(float(res), 5)
        print('<< Frequency is currently set to  {} THz. >>'.format(ans))      
        return ans
    
    def SetFrequency(self, val):
        strval = str(val)
        try:
            iDot = strval.index('.') #iDot is index of '.'
        except: #no '.' given as argument -> integer wavelength
            strval = strval + '.' # add '.' to start of string
            iDot = strval.index('.')
        if  iDot == 3: #correct place
            pass
        elif iDot < 3: #add more integer space holders
            while iDot < 3:
                strval = '0' + strval #add zero to string start
                iDot = strval.index('.') 
        else:
            print('<< ERROR: Desired frequency out of range! >>')
        
        if len(strval)<9:
            while len(strval) < 9:
                strval = strval + '0'
        else:
            strval = strval[0:8]
            print('<< WARNING: Frequency truncated to 5 decimal places. >>')
            
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <SET FREQUENCY {}>'.format(now, strval))                 
        self.__write__('WF{}'.format(strval)) # send formatted command
        
        try:
            wf = self.GetFrequency()
            if int(wf) == int(val):
                print('<< Frequency has been properly set to the desired value. >>')
            else:
                print('<< ERROR: Unable to set frequency to the desired value. Frequency is currently {} THz. >>'.format(wf))
            return wf
        except: 
            print('<< ERROR: Failed to query frequency value. Check connectivity and then check code. >>')


    def GetTargetPower(self):
        res = self.__query__('PS?')
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <GET USER-SET POWER>'.format(now))    
        res = re.sub('[^0-9\.]', '', res)
        ans = round(float(res), 2)
        print('<< Desired output power is currently set to  {} (check units). >>'.format(ans))      
        return ans        
        
    def GetPower_dBm(self):
        res = self.__query__('PW?')
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <GET dBm POWER>'.format(now))       
        ans = round(float(res), 2)
        print('<< True output power is currently {} dBm. >>'.format(ans))      
        return ans        
    
    def GetPower_uW(self):
        res = self.__query__('PU?')
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <GET MICROWATT (uW) POWER>'.format(now))       
        res = re.sub('[^0-9\.]', '', res)
        ans = round(float(res), 1)
        print('<< True output power is currently {} uW. >>'.format(ans))      
        return ans        
    
    
    def SetPower_dBm(self, val):
        strval = str(val)
        try:
            iDot = strval.index('.') #iDot is index of '.'
        except: #no '.' given as argument -> integer wavelength
            strval = strval + '.' # add '.' to start of string
            iDot = strval.index('.')
        if  iDot == 3: #correct place
            pass
        elif iDot < 3: #add more integer space holders
            while iDot < 3:
                strval = '0' + strval #add zero to string start
                iDot = strval.index('.') 
        else:
            print('<< ERROR: Desired dBm power out of range! >>')
        
        if len(strval)<6:
            while len(strval) < 6:
                strval = strval + '0'
        else:
            strval = strval[0:5]
            print('<< WARNING: dBm power truncated to 2 decimal places. >>')
            
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <SET dBm POWER {}>'.format(now, strval))                 
        self.__write__('PW{}'.format(strval)) # send formatted command
        
        try:
            pw = self.GetPower_dBm()
            if int(pw) == int(val):
                print('<< dBm power has been properly set to the desired value. >>')
            else:
                print('<< ERROR: Unable to set dBm power to the desired value. Power is currently {} dBm. >>'.format(pw))
            return pw
        except: 
            print('<< ERROR: Failed to query dBm power. Check connectivity and then check code. >>')
  
    def SetPower_uW(self, val):
        strval = str(val)
        try:
            iDot = strval.index('.') #iDot is index of '.'
        except: #no '.' given as argument -> integer wavelength
            strval = strval + '.' # add '.' to start of string
            iDot = strval.index('.')
        if  iDot == 4: #correct place
            pass
        elif iDot < 4: #add more integer space holders
            while iDot < 4:
                strval = '0' + strval #add zero to string start
                iDot = strval.index('.') 
        else:
            print('<< ERROR: Desired uW power out of range! >>')
        
        if len(strval)<6:
            while len(strval) < 6:
                strval = strval + '0'
        else:
            strval = strval[0:5]
            print('<< WARNING: uW power truncated to 1 decimal place. >>')
            
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <SET uW POWER {}>'.format(now, strval))                 
        self.__write__('PU{}'.format(strval)) # send formatted command
        
        try:
            pu = self.GetPower_uW()
            if int(pu) == int(val):
                print('<< uW power has been properly set to the desired value. >>')
            else:
                print('<< ERROR: Unable to set uW power to the desired value. Power is currently {} uW. >>'.format(pu))
            return pu
        except: 
            print('<< ERROR: Failed to query uW power. Check connectivity and then check code. >>')
        
        
        #sweep functions to be added when needed.
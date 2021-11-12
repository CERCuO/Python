# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 12:11:11 2020

@author: Daniel Hutama
"""

# Driver for JDSU SB Series optical switch
# Developed by Daniel Hutama
# version 1.0 -- Dec 09 2020

from __connection__ import Connection
from globalsFile import *
import time
import inspect
import numpy as np
import os
        
class JDSUSB(Connection):
    def __init__(self, addressString):
        Connection.__init__(self, addressString)
        
    def GetInfo(self):
        # identifies manufacturer, switch series, firmware version.
        try:
            info = self.__query__("IDN?")
            print(info)
        except:
            print("Unable to retreive instrument information.")
        
    def Reset(self):
        try:
            self.__write__("RESET")
            print("{} | Switch has been reset.".format(time.ctime()))
        except:
            print("{} | Unable to reset switch.".format(time.ctime()))
        
    def GetPort(self):
        port = self.__query__("CLOSE?")
        return int(port)
    

    def SetPort(self, Port):
        def TwoDigitFormatToString(mynum):
            if type(mynum) == str:
                try:
                    if int(mynum)>=10:
                        return str(int(mynum))
                    else:
                        tmp = '0'
                        tmp  += str(mynum)
                        return tmp
                except:
                    print("String cannot be converted to an integer. Please enter value as an int type.")
            elif type(mynum) == int:
                if mynum >= 10:
                    return str(mynum)
                else: 
                    tmp = '0'
                    tmp += str(mynum)
                    return tmp
            else:
                print('ERROR: Please enter Port as a string or integer.')
        if str(JDSUSB.GetPort(self)) == str(Port):
            print(time.ctime(), " | Device is correctly set to Port {}.".format(Port))
        else:
            print(time.ctime(), " | Device is currently incorrectly set to Port {}".format(JDSUSB.GetPort(self)))
            print(time.ctime(), " | Please wait -- changing configuration to Port {}.".format(Port))
            time.sleep(0.5)
            try:
                self.__write__("CLOSE {}".format(TwoDigitFormatToString(Port)))
                if int(JDSUSB.GetPort(self)) == int(Port):
                    print(time.ctime(), " | Device is now set to Port {}.".format(JDSUSB.GetPort(self)))
                else:
                    print(time.ctime(), " | Unable to set desired Port. The current port is  {}.".format(JDSUSB.GetPort(self)))
            except:
                 print(time.ctime(), " | Unable to set desired Port. The current port is  {}.".format(JDSUSB.GetPort(self)))
    
    
    
####################################################    
# J = JDSUSB
# SW_IN = Connection("0.20")



# # J.GetSlot(SW_IN)
# # J.__query__("CLOSE?")
# # J.Reset(SW_IN)
# print(J.GetInfo(SW_IN))
# print('----------')
# print(J.GetPort(SW_IN))
# print(time.ctime())
# J.SetPort(SW_IN, '11')
# print(J.GetPort(SW_IN))


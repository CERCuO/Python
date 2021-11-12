# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 16:04:10 2021

@author: Daniel Hutama 
dhuta087@uottawa.ca
"""
from pylablib.devices import Thorlabs
import numpy as np
import time
from datetime import datetime

# you will need to download and instal =l Thorlabs APT software if you do not already have it
# after installation of APT, open anaconda prompt and execute the following command
# pip install --user pylablib

        
        

class KPZ101():
    def __init__(self):
        self.SN = Thorlabs.list_kinesis_devices()[0][0]
        self.Description = Thorlabs.list_kinesis_devices()[0][1]
        # self.obj = Thorlabs.kinesis.KinesisDevice(self.SN)
        self.obj = Thorlabs.kinesis.KinesisMotor(self.SN)
        self.ManualURL = 'https://www.thorlabs.com/software/apt/APT_Communications_Protocol_Rev_15.pdf'
        
    def GetInfo(self):
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <GET INFO>'.format(now))
         tmp = self.obj.get_device_info()
         print(tmp)
         return tmp
         
    def GetInfoDetailed(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <GET FULL INFO>'.format(now))
        tmp = self.obj.get_full_info()
        print(tmp)
        return tmp
        
    def BlinkScreen(self):
        self.obj.blink()
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <BLINK SCREEN>'.format(now))
 
    def GetScale(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <GET SCALE>'.format(now))
        tmp = self.obj._get_scale()
        print(tmp)
        #(position velociy acceleration)
        return tmp
    





# if name == "__main__":

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 20:01:34 2021

@author: danhu
"""

from pylablib.devices import Thorlabs
import numpy as np
import time
from datetime import datetime

# you will need to download and instal =l Thorlabs APT software if you do not already have it
# after installation of APT, open anaconda prompt and execute the following command
# pip install --user pylablib



class KDC101():
    def __init__(self):
        self.SN = Thorlabs.list_kinesis_devices()[0][0]
        self.Description = Thorlabs.list_kinesis_devices()[0][1]
        self.obj = Thorlabs.kinesis.BasicKinesisDevice(self.SN)
        self.ManualURL = 'https://www.thorlabs.com/software/apt/APT_Communications_Protocol_Rev_15.pdf'
        
    def GetInfo(self):
         print(self.get_device_info())
        
    def BlinkScreen(self):
        self.obj.blink()
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <BLINK SCREEN>'.format(now))
        
        
    







# if name == "__main__":
#     SN = Thorlabs.
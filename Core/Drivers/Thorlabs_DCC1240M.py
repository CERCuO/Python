# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 11:31:09 2022

@author: danhu
"""

# driver for Thorlabs DCC124M
# developed by Daniel Hutama
# dhuta087@uottawa.ca
# Version 00.100 | 03 Feb 2022 | Initial build

#https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=ThorCam


from pylablib.devices import Thorlabs # pip install --user pylablib
from pylablib.devices import uc480 as cam
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt



class Thorlabs_DCC1240M():
    def __init__(self, indx):
        self.model = cam.list_cameras()[0][-4]
        self.SN = cam.list_cameras()[0][-3]
        self.camID = cam.uc480.find_by_serial(self.SN)
        self.obj = cam.UC480Camera(self.camID)
        self.helplink = 'https://pylablib.readthedocs.io/en/latest/devices/uc480.html#cameras-uc480'
    
    def GetExposure(self):
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <GET EXPOSURE>'.format(now))           
         return self.obj.get_exposure()
     
    def SetExposure(self, exposure):
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <SET EXPOSURE | {}>'.format(now, exposure))   
         self.obj.set_exposure(exposure)
         return self.GetExposure()
     
    def Snap(self):
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <SNAP PHOTO>'.format(now))           
         return self.obj.snap()
         
def ShowImage(image, cmap = 0):
     if cmap == 1:
         return plt.imshow(image)
     elif cmap == 0:
         plt.gray()
         plt.imshow(image)
         plt.show()
         
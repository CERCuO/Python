# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 11:31:09 2022

@author: danhu
"""

# driver for Thorlabs DCC124M
# developed by Daniel Hutama
# dhuta087@uottawa.ca

# Version 00.100 | 03 Feb 2022 | Initial build
# Version 00.200 | 16 Feb 2022 | Additional query functionality added
# Version 00.300 | 01 Mar 2022 | Added methods to specify camera settings.

#https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=ThorCam


from pylablib.devices import Thorlabs # pip install --user pylablib
# may run into numpy error if you are using an outdated version
# to fix any issue related to numpy 'loads' function, run the following in Anaconda Prompt
# pip install --upgrade numpy
# pip install --upgrade pylablib

from pylablib.devices import uc480 as Thorcam
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure



class Thorlabs_DCC1240M():
    def __init__(self, indx):
        self.model = Thorcam.list_cameras()[0][-4]
        self.SN = Thorcam.list_cameras()[0][-3]
        self.camID = Thorcam.uc480.find_by_serial(self.SN)
        self.obj = Thorcam.UC480Camera(self.camID)
        self.helplink = 'https://pylablib.readthedocs.io/en/latest/devices/uc480.html#cameras-uc480'
        self.helplin2 = 'https://pylablib.readthedocs.io/en/latest/.apidoc/pylablib.devices.uc480.html#module-pylablib.devices.uc480'
    
    def GetInfoDevice(self):
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <GET INFO DEVICE>'.format(now))                   
         return self.obj.get_device_info()
    
    def GetDetailedStatus(self):
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <GET DETAILED DEVICE SETTINGS>'.format(now))                   
         return self.obj.get_full_status()        
     
    def GetInfoAcquisition(self):
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <GET INFO ACQUISITION>'.format(now))                   
         return self.obj.get_acquisition_parameters()
    
    def GetExposure(self):
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <GET EXPOSURE>'.format(now))           
         return self.obj.get_exposure()
     
    def SetExposure(self, exposure): #enter in ms
         exposure = exposure/1000
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <SET EXPOSURE | {}>'.format(now, exposure))   
         self.obj.set_exposure(exposure)
         return self.GetExposure()
     
    def Snap(self):
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <SNAP PHOTO>'.format(now))           
         return self.obj.snap()
         
    def Open(self):
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <OPEN CAMERA>'.format(now))                   
         self.obj.open()        
     
    def Close(self):
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <CLOSE CAMERA>'.format(now))                   
         self.obj.close()
    #gain, saturation, denoising, extrema scaling,  
    
    def GetDetectorSize(self):
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <GET DETECTOR PIXEL SIZE>'.format(now))                   
         return self.obj.get_detector_size()        # returns tuple (width, height)
        
        
    def ShowImage(self, image, cmap = 0):
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <DISPLAY IMAGE>'.format(now))           
         fig = figure(figsize = (10,10))
         ax  = fig.add_subplot(111)
         if cmap == 1:
             return plt.imshow(image)
         elif cmap == 0:
             plt.gray()
             plt.imshow(image)
             ax.set_xlim((0, self.GetDetectorSize()[0]/2))
             ax.set_ylim((0, self.GetDetectorSize()[1]/2))
             plt.show()

    def ShowColorOptions(self):
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <DISPLAY COLOUR OPTIONS>'.format(now))    
         return self.obj.get_all_color_modes()
         
    def GetColorMode(self):
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <GET CURRENT COLOUR MODE>'.format(now))    
         return self.obj.get_color_mode()
     
    def SetColorMode(self, color):
         options = self.ShowColorOptions()
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <SET COLOUR MODE | {}>'.format(now, color))             
         if color in options:
             return self.obj.set_color_mode(color)
         else:
             print('<<ERROR: specified colour mode not recognized! >> ')
             print('Available colour mode options are {}'.format(options))
             
    def ClearAcquisitions(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <CLEAR ACQUISITION HISTORY>'.format(now))       
        try:
            self.obj.clear_acquisition()
            print('Acquisition history successfully cleared')
        except Exception as E:
            print('<<ERROR: Unable to clear acquisition history>>')
            print(E)
        
             
             
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
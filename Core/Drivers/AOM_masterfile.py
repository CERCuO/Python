# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 08:42:33 2022

@author: Daniel Hutama (dhuta087@uottawa.ca)


# Version 00.100 | 11 Feb 2022 | Python build structure translated from Matlab
# Version 00.101 | 01 Mar 2022 | Progress savepoint on Matlab code conversion
"""

from datetime import datetime
import time
import numpy as np
import os
################################
'''
Check cables
    1. AOM-AWG connection on Ch1
    2. AWG marker to laser, oscilloscope
    3. AWG - computer control
    4. Camera - computer control


1. Laser on
2. AWG on
3. Camera on
4. Thorlabs camera software
5. code execution
    a. initialize camera
        I. create handle
        II. Set params - bitmap, 8-bit RGB, software trigger mode, 10 ms
    b. Initialize AWG
        I. Set RF params
        II. create filename, set Gaussian filter function
        III. Load waveform file to AWG
    c. Generate waveform from file on AWG
    d. Image reconstruction
'''
################################

############### next 3 lines are in case you don't have Dependencies in your system path ##############
# import sys
# sys.path 
# sys.path.append('C:\\depot\\CERC\\Python\\Core\\Dependencies')
# sys.path.append('C:\\depot\\CERC\\Python\\Core\\Drivers')
#######################################################################################################

try:
    cam = Thorlabs_DCC1240M(0) # create camera handle
    AWG = Tektronix_AWG610('0.1')
except Exception as E:
    print('<<ERROR: Unable to initialize devices. Check connection and device addresses.>>')
    print(E)



# Load file from AWG main memory 
# function is case sensitive (e.g. use wfm instead of WFM)
AWG.SetCustomWaveform(1, 'test_21_03_2022.wfm')







#parameters copied from old matlab file.
dt = 1/0.96e9
tmax = 1e-6
t = np.array(list(np.arange(-tmax + dt, tmax, dt)))
vs = 3.63e3
Optical_x = t*vs

Freq = 80e6
Amplitudes = 0.9



################################
for i in range(1):
    start = time.time()
    elapsed = time.time()-start
    
    RFPixels = np.ones(64)
    RFPixels[i] = 1 ## only iterating once?
    
    RFPixels[32:64] = Amplitudes*np.exp(1j * np.linspace(0, 34, 32) * np.pi/8)
    
    Optical_Target = np.ones(len(t))
    
    filtfun = np.exp(-t**2/(12.5e-9)**2)
    filtfun = filtfun/sum(filtfun)
    
    RFpulseAmpl = np.convolve(Optical_Target, filtfun, 'same')
    
    RFWaveform = np.real(np.exp(1j * 2 * np.pi * t * Freq) * Optical_Target)
    
    
    fname = 'test{}'.format(i)
    
    cwd = os.getcwd()
    if cwd != 'C:\\depot\\CERC\\Python\\Core\\Drivers': #this is specific for my computer - you may need to change the pathname.
        os.chdir('C:\\depot\\CERC\\Python\\Core\\Drivers\\Tektronix_AWG610_files')
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
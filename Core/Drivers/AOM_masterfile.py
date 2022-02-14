# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 08:42:33 2022

@author: Daniel Hutama (dhuta087@uottawa.ca)


# Version 00.100 | 11 Feb 2022 | Python build structure translated from Matlab
"""

from datetime import datetime
import time
import numpy as np


################################
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
    
    
    
    
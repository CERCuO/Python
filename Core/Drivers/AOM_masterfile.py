# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 08:42:33 2022

@author: Daniel Hutama (dhuta087@uottawa.ca)


# Version 00.100 | 11 Feb 2022 | Python build structure translated from Matlab
"""


import numpy as np

#parameters copied from old matlab file.
dt = 1/0.96e9
tmax = 1e-6
t = np.array(list(np.arange(-tmax + dt, tmax, dt)))
vs = 3.63e3
Optical_x = t*vs

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 16:20:32 2022

@author: Daniel Hutama


25-Feb-2022 | Version 0.1 | Daniel Hutama | Skeleton layout for IR cam driver for beam imaging



# xevacam library here:  https://github.com/Moskari/xevacam | https://github.com/CERCuO/xevacam

"""

import xevacam.camera as camera
import xevacam.utils as utils
import numpy
import matplotlib.pyplot as plt
import time



# you need to change the path to whereever your calibration file 
# cam = camera.XevaCam(calibration='C:\\Program Files\\Common Files\\XenICs\\Runtime\Calibrations\\0222-50us_10361.xca')
cam = camera.XevaCam(calibration='C:\\depot\\CERC\\Xenics_control\\BOBCAT320-9849\\Software\\Calibrations\\XC-(14-12-2017)-500us_9849.xca')
# Open connection to camera
with cam.opened() as c:
	# Create a window and connect it to the camera output
	# Line scanner view. Show 30th line in the frame (30th band in data cube)  
    window = utils.LineScanWindow(cam, 30)
    c.start_recording()
    window.show()  # Show it
    c.wait_recording(5)
    meta = c.stop_recording()
    
    
    
    
    
    ##########################
# more to be added later
# -*- coding: utf-8 -*-
"""
Created 2021-11-16

@author: Henri Morin, henri.p.morin@gmail.com

Device file for the ThorLab PM100D power meter
Reads power only as of 2021-11-16
"""

import pyvisa as visa

class PM100D(object):
    '''
    Documentation:
    Controls the PMD100D powermeter.
    Inputs:
    name (str)
    address (str)
    '''
    def __init__(self, name, address, *args, **kwargs):
        # Run the (mandatory) superclass constructor
        super().__init__(*args, **kwargs)
        # Create the instrument
        rm = visa.ResourceManager()
        self.inst = rm.open_resource(address)
        #Declare power variable
        self.power = 0.0
        self.flag = False
        # increases the accuracy of the reading
        self.inst.write("AVERage[:COUNt] <3000")
        
        
    def __del__(self):
        #Closes the channel
        self.inst.close()

            
    def read(self):
        '''
        Documentation:
        Retrieve the power reading from the powermeter.
        Input:
        None
        Return:
        power in uWatts (str)
        note the rounding is manual
        '''
        #Retrieve the power reading from the device
        self.power = '%.6f' % (float(self.inst.query("read?"))*1e6) + ' uW'
        self.flag = True
        return self.getvalue()
        
    def getvalue(self):
        #Return last power value saved in memory
        return self.power
        

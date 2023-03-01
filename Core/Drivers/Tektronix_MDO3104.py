# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 14:46:29 2023

@author: danhu
"""


# import sys
# sys.path.append('C:\\depot\\CERC\\Python\\Core\\Drivers\\inst_specific_files')


# driver for Tektronix 2450 Sourcemeter
# developed by Daniel Hutama
# dhuta087@uottawa.ca

# This devices uses IEEE 488.2
# Standard Commands for Programmable Instruments (SCPI)

#be sure to add "drivers" and "dependencies" folder to your machine's syspath
# github.com/CERCuO/Python
# The next 3 lines are specific for my computer, where I dumped all the github files into \depot\CERC
import sys
sys.path.append('C:\\depot\\CERC\\Python\\Core\\Dependencies')
sys.path.append('C:\\depot\\CERC\\Python\\Core\\Drivers')


# you may need to run this class twice if modules are not properly loaded.

from __connection__ import Connection
from datetime import datetime
import numpy as np
import pyvisa

class Tektronix_MDO3104():
    def __init__(self,addressString):
        # Connection.__init__(self,addressString) 
        # not using CERC dependencies since USB type connections are not supported
        # using PyVisa for direct USB connection.
        rm = pyvisa.ResourceManager()
        self.obj = rm.open_resource(list(rm.list_resources())[0])
        #may need to change above line if multiple USB objects connected
        self.Manual = 'Tek_MDO3104_Oscilloscope.pdf'
        
    def GetInfo(self):
        try:
            idn = self.obj.query('*IDN?')
            return idn
        except:
            print('<< ERROR: Unable to get device information. Check connectivity. >>')
                
    def GetSTR(self, cmd):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <{}>'.format(now, cmd.upper()))      
        res = self.obj.query(cmd)
        return res
    
    def SetSTR(self, cmd):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <{}>'.format(now, cmd.upper()))      
        self.obj.write(cmd)
        

    
    def GetHorizontal_DelayMode(self):
        return self.GetSTR("HOR:DEL:MOD?")
    
    def SetHorizontal_DelayMode(self, mode):
        # 0 for off, 1 for on
        self.SetSTR("HOR:DEL:MOD {}".format(mode))
        return self.GetHorizontalDelayMode()
        
    def GetHorizontal_DelayTime(self):
        #returns horizontal delay time in units of s.
        return self.GetSTR("HOR:DEL:TIM?")
    
    def SetHorizontal_DelayTime(self, delay):
        #enter desired delay in units of s.
        self.SetSTR("HOR:DEL:TIM {}".format(delay))
        return self.GetHorizontalDelayTime()
    
    def GetHorizontal_RecordLength(self):
        #returns number of sample points in recording
        return self.GetSTR("HOR:RECO?")
    
    def SetHorizontal_RecordLength(self, points):
        # supports in list: [1000, 10000, 100000, 1e6, 5e6, 10e6]
        self.SetSTR("HOR:RECO {}".format(points))
        return self.GetHorizontalRecordLength()
    
    def GetHorizontal_Scale(self):
        return self.GetSTR("HOR:SCA?")
    
    def SetHorizontal_Scale(self, scale):
        # enter value from 400ps to 1000s
        # scale will be coerced to the nearest available setting
        # Ex: scale = 2E-6 sets the horizontal scale to 2us per division
        self.SetSTR("HOR:SCALE {}".format(scale))
        return self.GetHorizontalScale()
    
    def GetMeasurement_Source(self):
        # query the current channel for measurement
        return self.GetSTR("MEASU:IMM:SOU?")
    
    def SetMeasurement_Source(self, source):
        #enter the desired source (number only), e.g. "1" to set CH1
        self.SetSTR("MEASU:IMM:SOU CH{}".format(source))
        return self.GetMeasurement_Source()
    
    def GetMeasurement_Type(self):
        #will timeout if no type is set
        return self.GetSTR("MEASU:IMM:TYP?")
    
    def SetMeasurement_Type(self, val):
        #some possible values for meas types are: AMP, MAX, MEAN, RMS, SIGMA1, SIGMA2, SIGMA3, STD
        self.SetSTR("MEASU:IMM:TYP {}".format(val))
        return self.GetMeasurement_Type()
    
    def GetMeasurement_Value(self):
        return self.GetSTR("MEAS:IMM:VAL?")
    
    def GetMeasurement_Units(self):
        return self.GetSTR("MEAS:IMM:UNITS?")
    
    def GetData_Source(self):
        # query channel for data transfer
        return self.GetSTR("DAT:SOUR?")
    
    def SetData_Source(self, val):
        #set channel for data transfer
        self.SetSTR("DAT:SOUR CH{}".format(val))
        return self.GetData_Source()
    
    def GetData_Encoding(self):
        return self.GetSTR("DAT:ENC?")
        
    def SetData_Encoding(self, enc):
        # e.g. to ASCii
        self.SetSTR("DAT:ENC {}".format(enc))
        return self.GetData_Encoding()
    
    def GetData_Width(self):
        return self.GetSTR("DAT:WID?")
    
    def SetData_Width(self, width):
        self.SetSTR("DAT:WID {}".format(width))
        
    def GetData_Preamble(self):
        return self.GetSTR("WFMO?")
    
    def GetData(self):
        # grabs data on specified channel.
        # be sure to have already set the:
        # measurement source channel, measurement type, data encoding, etc. 
        data = self.GetSTR("CURV?")[:-1]
        out = np.array(data.split(","))
        return out
        
    def GetData_ScaleY(self):
        return float(self.GetSTR("WFMO:YMU?")[:-1])
    
    def GetData_ScaleX(self):
        return float(self.GetSTR("WFMO:XIN?"))

    def GetData_NumPts(self):
        return float(self.GetSTR("WFMO:NR_pt?"))


    def GetImpedance(self,channel):
        return self.GetSTR('CH{}:TERMINATION?'.format(channel))
    
    def SetImpedance(self, channel, impedance):
        #options are FIFty or MEG
        self.SetSTR('CH{}:TERMINATION {}'.format(channel, impedance))
        return self.GetImpedance(channel)


# Data analysis
run = 0
if run == 1:
    import matplotlib.pyplot as plt
    scope = Tektronix_MDO3104('')
    scope.SetData_Source("1") #set channel 
    scope.SetData_Encoding("ASC")
    data = np.array(scope.GetData()).astype(float)
    
    Y_scale = scope.GetData_ScaleY()
    X_scale = scope.GetData_ScaleX()
    num_pts = scope.GetData_NumPts()
    
    scaled_data = data * Y_scale

    xlinspace = np.linspace(0, X_scale * num_pts, int(num_pts))
    xlinspace_ns = xlinspace*1e9
    
    scaled_data_adj = scaled_data - np.mean(scaled_data)
    
    
    plt.xlabel('ns')
    plt.ylabel('V')
    plt.plot(xlinspace_ns[0:1999], scaled_data_adj[0:1999])
    plt.grid()
    plt.show()
    

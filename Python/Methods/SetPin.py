# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 09:44:02 2019

@author: Daniel Hutama
"""
import time
def  SetPin(Setup,Pin):
#   CalcVOARange(Setup,cfg,CalibrationNum,m)
#   cfg is loaded thru excel file
#   CalibrationNum is caluated thru GetCalibration()
#   m is number of test case
    
    Setup.VOA.SetAttenuation(20)
    time.sleep(1)
    Setup.TLS.SetPower(Setup.TLS.GetMaxPower)
    iteri=1
    delta=1
    while iteri<5 and abs(delta)>0.05:

        P=Setup.PM.GetReading
        A=Setup.VOA.GetAttenuation
#        delta=P+CalibrationNum.PM-Pin;
        delta=P-Pin
        Setup.VOA.SetAttenuation(max(min(50,A+delta),0))
        time.sleep(1)
        iteri=iteri+1
   
    Att=Setup.VOA.GetAttenuation;
    return Att
    
    


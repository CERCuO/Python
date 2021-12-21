# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 20:01:34 2021

Ver 0.2 
16-Nov-2021

@author: Daniel Hutama; dhuta087@uottawa.ca
"""

from pylablib.devices import Thorlabs # pip install --user pylablib
from pylablib.core.utils import strpack
import time
import math
from datetime import datetime

# you will need to download and install Thorlabs APT software if you do not already have it
# after installation of APT, open anaconda prompt and execute the following command
# pip install --user pylablib
# Thorlabs runs on APT communications protocol
# https://pylablib-v0.readthedocs.io/en/latest/_modules/pylablib/aux_libs/devices/Thorlabs.html#KinesisDevice


class KDC101():
    def __init__(self, indx):
        self.SN = Thorlabs.list_kinesis_devices()[indx][0]
        self.Description = Thorlabs.list_kinesis_devices()[indx][1]
        # self.obj = Thorlabs.kinesis.KinesisDevice(self.SN)
        self.obj = Thorlabs.kinesis.KinesisMotor(self.SN)
        self.ManualURL = 'https://www.thorlabs.com/software/apt/APT_Communications_Protocol_Rev_15.pdf'

    
    def SetStageModel(self, StageModelStr):
        #PRMTZ8
        self.Stage = StageModelStr
        if self.Stage.startswith('PRMT') == True:
            self.ScalingFactor = 1919.6418578623391
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print('{}   |   <SET SCALING>'.format(now))
            print('<< Scaling factor set to {} >>'.format(self.ScalingFactor))
        if self.Stage.startswith('PRM1') == True:
            self.ScalingFactor = 1919.6418578623391
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print('{}   |   <SET SCALING>'.format(now))
            print('<< Scaling factor set to {} >>'.format(self.ScalingFactor))
        if self.Stage.startswith('Z8') == True:
            self.ScalingFactor = 34304.10969
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print('{}   |   <SET SCALING>'.format(now))
            print('<< Scaling factor set to {} >>'.format(self.ScalingFactor))            
        #elif, else for other stages
        else:
            print('<< WARNING: Scaling factor was not automatically set. >>')
    
    def GetInfo(self):
         now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         print('{}   |   <GET INFO>'.format(now))
         tmp = self.obj.get_device_info()
         return tmp
         
    def GetInfoDetailed(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <GET FULL INFO>'.format(now))
        tmp = self.obj.get_full_info()
        return tmp
        
    def BlinkScreen(self):
        self.obj.blink()
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <BLINK SCREEN>'.format(now))
 
    def GetScale(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <GET SCALE>'.format(now))
        tmp = self.obj._get_scale()
        #(position velociy acceleration)
        return tmp
    

    def get_status_n(self):
        """
        Get numerical status of the device.

        For details, see APT communications protocol.
        """
        self.obj.send_comm(0x0429,0x01)
        data=self.obj.recv_comm().data
        return strpack.unpack_uint(data[2:6],"<")

    status_bits=[(1<<0,"sw_bk_lim"),(1<<1,"sw_fw_lim"),
                (1<<4,"moving_bk"),(1<<5,"moving_fw"),(1<<6,"jogging_bk"),(1<<7,"jogging_fw"),
                (1<<9,"homing"),(1<<10,"homed"),(1<<12,"tracking"),(1<<13,"settled"),
                (1<<14,"motion_error"),(1<<24,"current_limit"),(1<<31,"enabled")]
  
    def GetStatus(self):
        """
        Get device status.

        Return list of status strings, which can include ``"sw_fw_lim"`` (forward limit switch reached),``"sw_bk_lim"`` (backward limit switch reached),
        ``"moving_fw"`` (moving forward), ``"moving_bk"`` (moving backward),
        ``"homing"`` (homing), ``"homed"`` (homing done), ``"tracking"``, ``"settled"``,
        ``"motion_error"`` (excessive position error), ``"current_limit"`` (motor current limit exceeded), or ``"enabled"`` (motor is enabled).
        """
        status_n=self.get_status_n()
        
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <GET STATUS>'.format(now))
        return [s for (m,s) in self.status_bits if status_n&m]
    
    def is_homed(self):
        tmp = self.GetStatus()
        res = 'homed' in tmp
        if res == True:
            print('<< Stage is homed. >>')
        else: 
            print('<< Stage is NOT homed. >>')
        return res
    
    def is_moving(self):
        tmp = self.GetStatus()
        res_fw = 'moving_fw' in tmp
        res_bk = 'moving_bk' in tmp
        if res_fw == True:
            print('<< Stage is moving Forward. >>')
            return True
        elif res_bk == True:
            print('<< Stage is moving Backward. >>')
            return True
        elif res_bk | res_fw == False:
            print(' << Stage is NOT moving. >>')
            return False
        else:
            print(' << Error: Check code at is_moving(). >>')
            
        
    def wait_for_status(self, status, Timeout = 60, Period = 5):
        # status is the desired string value in self.status_bits.
        # Timeout is the amount of time this function will run before giving up.
        # Period is the time between consecutive status queries. 
        start = time.time()
        elapsed = time.time()-start
        flag = 0
        while flag == 0 and elapsed<Timeout:
            if self.is_moving() == True:
                elapsed = time.time() - start
                flag = 0
                time.sleep(Period)
            elif status in self.GetStatus():
                flag = 1
                elapsed = time.time()-start
                time.sleep(Period)
        print('<< Time elapsed is {:.3f} seconds.'.format(elapsed))
        
        
    def Dev_GetPosition_APT(self):
        flag = self.is_moving()
        
        if flag == True:
            count = 0
            while flag == True and count < 5:
                time.sleep(3) #wait to stop moving
                flag = self.is_moving()
                count = count + 1

        self.obj.send_comm(0x0411, 0x01)
        msg = self.obj.recv_comm()
        data = msg.data
        return strpack.unpack_int(data[2:6], "<")
    
    def GetPosition(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <GET POSITION>'.format(now))       
        res = self.Dev_GetPosition_APT()/self.ScalingFactor
        print('<< Current Position is {:.4f} >>'.format(res))
        return res
        
    def StepFwd(self, stepsize=1):
        self.obj.move_by(stepsize)
        self.GetPosition()
    
    def StepBwd(self, stepsize=-1):
        self.obj.move_by(stepsize)
        self.GetPosition()
        
    
    def SendHome(self, Status = 'homed', timeout=60, period=1):
        self.obj.send_comm(0x0443,0x01)
        self.wait_for_status(Status, timeout, period)
        
    def Dev_SetPosition_APT(self, position, Status='homed', period=1):
        # move to a given position.
        if self.ScalingFactor != 1919.6418578623391:
            Status = 'enabled'
        self.obj.send_comm_data(0x0453,b'\x01\x00'+strpack.pack_int(int(position),4,'<'))
        self.wait_for_status(Status, Period = period)
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print('{}   |   <GET POSITION>'.format(now))
        time.sleep(3)
        pos = self.GetPosition()
        flag = math.isclose(float(pos), float(position)/self.ScalingFactor, abs_tol = 0.01)
        if  flag == True:
            print('<< Position is properly set. >>')
            print('<< Current position is {:.4f}'.format(pos))
        else:
            print('<< ERROR: Unable to set desired position. >>')
            print('<< Current position is {:.4f}'.format(pos))

    def SetPosition(self, position):
        #optional arguments can be changed in Dev_SetPosition_APT()
        APT_pos = position*self.ScalingFactor
        self.Dev_SetPosition_APT(APT_pos)
        print('<< Unresolvable error has magnitude {:.4f}'.format(abs(position - self.Dev_GetPosition_APT()/self.ScalingFactor)))
        return self.GetPosition()
        
    
    
    
    
    
    
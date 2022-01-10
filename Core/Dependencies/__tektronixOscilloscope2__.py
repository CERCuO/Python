# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 14:37:44 2019

@author: Daniel Hutama
"""
#7/4/2019

import visa
import time
import re
import numpy as np
import matplotlib.pyplot as plt
import types
import os
import webbrowser
from PyTektronixScope import PyTektronixScope
from __connection__ import Connection
from globalsFile import *
from struct import unpack

delay = 0.05

 

# Uses channel self.channel if no channel is Set.

class TektronixScope2(Connection):

    """

Base Tektronix Driver that seems to be compatible with:

 

Tektronix TDS3000 series

Tektronix MDO3014

 

and more

 

"""

    def __init__(self,addressString):

        Connection.__init__(self,addressString)
        
        self.addressString=addressString
 

        self.Driver_Document = None

 

        # You must call this in order to ensure commands work correctly

        self.__write__("DATa INIT")

 

        # These can be overwritten if inaccurate

        self.sources = ["CH1", "CH2", "CH3", "CH4", "MATH", "REF1", "REF2", "REF3",

         "REF4", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D11",

         "D12", "D13", "D14", "D15", "DIGital", "RF_AMPlitude", "RF_FREQuency", 

         "RF_PHASe", "RF_NORMal", "RF_AVErage", "RF_MAXHold", "RF_MINHold"

        ]

        self.yunit = ["V", "VV", "s", "Hz", "%", "div", "S/s", "ohms", "A", "W", "min",

"degrees", "?", "AA", "hr", "day", "dB", "B", "/Hz", "IRE", "V/V", "V/A", "VW",

"V/W", "VdB", "V/dB", "A/V", "A/A", "AW", "A/W", "AdB", "A/dB", "WV",

"W/V", "WA", "W/A", "WW", "W/W", "WdB", "W/dB", "dBV", "dB/V", "dBA",

"dB/A", "dBW", "dB/W", "dBdB", "dB/dB"]

        self.source = None

 

    def __queryAscii__(self,string):

        return super(TektronixMDO3014, self).__queryAscii__(string,delimiter='\n')

 

    def GetSource(self):

        return self.__query__("DATa:SOURCE?")

 

    def GetChannel(self):

        return self.GetSource()

    def GetChannelver2(self,channel):
        Ch=self.__query__('SELECT:CH'+str(channel)+'?')
        return int(Ch)
        
       


       

    def SetChannel(self,channel,ONOFF):
        
        if channel=='All':

            self.__write__('SELECT:CH1 '+ str(ONOFF))

            self.__write__('SELECT:CH2 '+ str(ONOFF))

            self.__write__('SELECT:CH3 '+ str(ONOFF))

            self.__write__('SELECT:CH4 '+ str(ONOFF))
            return 1

        else :

            self.__write__('SELECT:CH'+ str(channel)+' '+str(ONOFF));

            Ch=self.GetChannelver2(channel)
         
            if ONOFF==Ch:

               return 'Channel Set correctly';

            else:

               return 'Wrong. Options= 0 or 1';

        

 # if above doesnt work add below back       


        #if (type(channel) == int):

            #channelToSet = "CH" + str(channel)

       # elif (channel == None):

           # return

        #else:

            #channelToSet = channel

       # self.__write__("DATa:SOURCE " + channelToSet)

        #time.sleep(delay)

       # curChannel = self.GetChannel()

        #if (curChannel != channelToSet):

            #print("Channel Set incorrectly")

           # print("Attempted to Set channel to", channelToSet, "but channel is Set to", curChannel)

           # return

        #self.source = channelToSet



    def GetVerticalScale(self,channel):

        self.__write__('*CLS');

        r=float(self.__query__('CH'+str(channel)+':SCALE?'))
        return r

 

    def SetVerticalScale(self,channel,value):

        if value<0.001:

           value=0.001

           if value<0:

              return('Value is negative! Scale Set to minimum') 

        List=[10,5,2,1,0.2,0.1,0.05,0.02,0.01,0.005,0.002,0.001];

        self.__write__('CH'+str(channel)+':SCALE '+str(value));

        time.sleep(0.5)

        r=self.GetVerticalScale(channel)

        if r==value:

            return 'Vertical scale is Set correctly to ' +str(r);

        else:

            return 'Vertical scale is Set wrong to ' +str(r);

 

    def SetOffSet(self,channel,offSet):

        self.__write__('*CLS');

        self.__write__('CH'+str(channel)+':OFFSet '+'{:2.2e}'.format(offSet));

        off=self.GetOffSet(channel)

        if off==offSet:

            return 'OffSet Set correctly to '+str(off);

        else:

            return 'OffSet Set wrong to '+str(off);

 

    def GetOffSet(self,channel):

        self.__write__('*CLS');  

        off=float(self.__query__('CH'+str(channel)+':OFFS?'));

      
        print( 'OffSet: ' + str(off))
                
        return off

    

    def SetBandwidth(self,channel,bandwidth):

        self.__write__('CH'+str(channel)+':BANDWIDTH '+str(bandwidth));

        BW=self.GetBandwidth(channel);

        if BW==bandwidth:

            return 'Set Correctly to ' + str(BW)+' Hz';

        else:

            return 'Set Incorrectly to '+str(BW);

    

    def GetBandwidth(self,channel):

        BW=float(self.__query__('CH'+str(channel)+':BANDWIDTH?'))
        return BW

    

    def SetHorizontalScale(self,value):

        HL=[1e-9,2e-9,4e-9,10e-9,20e-9,40e-9,100e-9,200e-9,400e-9,800e-9,2e-6,4e-6,10e-6,20e-6,40e-6,100e-6,200e-6,400e-6,1e-3,2e-3,4e-3,10e-3,20e-3,40e-3,100e-3,200e-3,400e-3,1,2,4,10]
        
        tmp=HL
        
        tmp[:] = [abs(x*-1) for x in tmp]
        
        tmp[:] = [abs(x + value) for x in tmp]
        
#        mini=min(tmp)
        
        i=tmp.index(min(tmp))

        self.__write__('HORI:SCA '+str(HL[i]))

        H=self.GetHorizontalScale()
        time.sleep(1)
        if H==value:

            return 'Horizontal scale is Set correctly'

        else:

            return 'Horizontal Scale is Set wrong! Scale='+str(H)
        


    def SetTriggerSource(self,channel):

        self.__write__('TRIG:A:EDGE:SOURCE CH'+str(channel))

 

    def SetTriggerLevel(self,channel,level):

        self.__write__('TRIGger:A:LEVel:CH'+str(channel)+''+str(level))

 

    def SetTriggerEdge(self,edge):

        self.__write__('TRIGger:A:EDGE:SLOpe '+edge)

        Options=['Rise','Fall','Either']

 

    def SetStopAfter(self,StopAfter):

        self.__write__('ACQ:STOPA '+StopAfter)

#        time.sleep(1)

        S=self.GetStopAfter()

        if S.upper() == StopAfter.upper():

            return StopAfter +' Set Correctly'

        else:

            return 'StopAfter Set incorrectly. Options are: RunStop or Sequence'

 

    def SetHorizontalDelayMode(self,mode):

        self.__write__('HORIZONTAL:DELAY:MODE '+mode)

    

    def SetHorizontalPositionPercentage(self,percentage):

        self.__write__('HORIZONTAL:Position '+str(percentage))

 

    def SetMode(self,mode):

        self.__write__('ACQuire:MODe '+mode)

        M=self.GetMode()

        nn=M[0:-1]

        if nn.upper()==mode.upper():

           return mode + 'mode Set correctly'

        else:

           return 'Mode Set incorrectly. Mode options are: Sample,Peakdetect,Hires,Average or Envelope'

        

    def SetVerticalPosition(self,channel,position):

        self.__write__('CH'+str(channel)+':Position '+str(position))

        P=self.GetVerticalPosition(channel)

        if P==position:

            return 'Position Set correctly'

        else:

            return 'Position Set wrong'

    def SingleScanTrace(self,channel,TraceNumber):
        self.SetStopAfter('Sequence')
        self.StopCapture()
        self.StartCapture()
        while self.GetCaptureStatus()=='Run':
            pass
#        T=self.GetTrace(channel,TraceNumber)
        

    def GetVerticalWindow(self,channel):

        Sc=float(self.GetVerticalScale(channel))

        OFF=float(self.GetOffSet(channel))

        Pos=float(self.GetVerticalPosition(channel))
        
        VW={}
           
        VW['min']={}
        
        VW['max']={}
        
        VW['Scale']={}
                
            

        VW['min']=-Sc*4+OFF-Pos*Sc

        VW['max']=Sc*4+OFF-Pos*Sc

        VW['Scale']=Sc
        
        return VW

 

    def GetVerticalPosition(self,channel):

        self.__write__('*CLS')

        Off=float(self.__query__('CH'+str(channel)+':OFFS?'))

        print( 'OffSet: ' + str(Off))
        return Off

 

    def GetMode(self):

        M=self.__query__('ACQuire:MODe?')
        return M

 

    def GetStopAfter(self):

        ub=self.__query__('ACQ:STOPA?')

        S=ub.replace('\n','') 
        return S

 

    def GetHorizontalScale(self):

        self.__write__('*CLS')

        H=float(self.__query__('HORI:SCA?'))
        return H

 
#
#    def GetHorizList(self):
#
#        HL=[1e-9,2e-9,4e-9,10e-9,20e-9,40e-9,100e-9,200e-9,400e-9,800e-9,2e-6,4e-6,10e-6,20e-6,40e-6,100e-6,200e-6,400e-6,1e-3,2e-3,4e-3,10e-3,20e-3,40e-3,100e-3,200e-3,400e-3,1,2,4,10]
#
#        return HL

    def GetSources(self,pprint=True):

        if (pprint):

            print(self.sources)

        else:

            return self.sources
        
 

    def SetSource(self, source):

        self.__write__("DATa:SOURCE " + str(source))

        time.sleep(delay)

        curSource = self.GetSource()
        
        sour='CH'+str(source)+'\n'

        if (curSource.upper() != str(sour).upper()):

            print("Source Set incorrectly")

            print("Attempted to Set source to", source, "but source is Set to", curSource)
            
            return

        self.source = curSource

 

    def __mapToChannel__(self,channel):

        if (type(channel) == int):

            return "CH" + str(channel)

        else:

            return channel

 

    def __queryValue__(self,query):

        return float(self.__query__(query))

        time.sleep(delay)

 

    def __writeValue__(self,cmd):

        self.__write__(cmd)

        time.sleep(delay)

 

    # If channel is specified, then temporarily switch to that channel and send the query

    # If isBinary is Set to true, then the command is expecting binary to be returned from the query

    def __queryChannel__(self,query, channel=None, isBinary=False):

        origSource = self.source 

        channel = channel if channel is not None else self.source

        if channel:

            if (type(channel) == int):

                channel = "CH" + str(channel)

            if channel != origSource:

                self.setChannel(channel)

                time.sleep(delay)

        if isBinary:

            response = self.__queryBinary__(query)

        else:

            response = self.__query__(query)

        if channel and channel != origSource:

            self.SetSource(origSource)

        return response

 

    def __writeChannel__(self,command,channel=None):

        origSource = self.source

        channel = channel if channel is not None else self.source

        if channel:

            if (type(channel) == int):

                channel = "CH" + str(channel)

            if channel != origSource:

                self.setChannel(channel)

                time.sleep(delay)

        response = self.__write__(command) # returns exit code of write command

        if channel and channel != self.source:

            self.SetSource(origSource)

        return response
    
    
    def setChannel(self,channel):
        if (type(channel) == int):
            channelToSet = 'CH'+str(channel)
        elif (channel == None):
            return
        else:
            channelToSet = str(channel) 
        self.__write__("DATa:SOURCE " + channelToSet)
        time.sleep(delay)
        channelToSet=channelToSet+'\n'
        curChannel = self.GetChannel()
        if (curChannel != channelToSet):
            print("Channel set incorrectly")
            print("Attempted to set channel to", channelToSet, "but channel is set to", curChannel)
            return
        self.source = channelToSet
        

    def StartCapture(self, prompt=True):

        self.__write__("ACQuire:STATE ON")

 

        state = int(self.__query__('ACQuire:STATE?'))

 

        if not state:

            raise Exception("Did not start capturing successfully")

 

        elif prompt:

            print("Started Capturing")

 

    def StopCapture(self,prompt=True):

        self.__write__("ACQuire:STATE OFF")

        state = int(self.__query__('ACQuire:STATE?'))

 

        if state:

            raise Exception("Did not stop capturing successfully")

 

        elif prompt:

            print("Stopped Capturing")

 

    def GetCaptureStatus(self):

        state = self.__query__("ACQuire:STATE?")

        if (int(state)==1):

            status="Run"
            return status

        elif (int(state)==0):

            status="Stop"
            return status
        else: 
            print('ERROR')

 

    def GetStart(self):

        start = int(self.__query__("DATa:START?"))

        time.sleep(delay)

        return start

 

    def GetStop(self):

        stop = int(self.__query__("DATa:STOP?"))

        time.sleep(delay)

        return stop

 

    def SetStart(self,start):

        self.__write__("DATa:START " + str(start))

        curStart = self.__query__("DATa:START?")

        if (float(start) != float(curStart)):

            raise Exception("Start Set incorrectly")

        else:

            print("Start Set to", str(start))

 

    def SetStop(self,stop):

        self.__write__("DATa:STOP " + str(stop))

        time.sleep(delay)

        curStop = self.__query__("DATa:STOP?")

        if (float(stop) != float(curStop)):

            raise Exception("Stop Set incorrectly")

        else:

            print("Stop Set to", str(stop))

 

    def GetTrace(self,channel,NumberofTraces):

        """Prints the trace for a channel"""
 

#        channel = channel if channel is not None else self.source

#        self.__writeValue__("WFMPre:PT_Fmt Y")

        self.source=channel
 

        xOffSet = self.__queryValue__("WFMPre:PT_Off?")

        yOffSet = self.__queryValue__("WFMPre:YOFf?")

 

        xScale = self.__queryValue__("WFMPre:XINcr?")

        yScale = self.__queryValue__("WFMPre:YMUlt?")

 

        xUnit = self.__query__("WFMPre:XUNit?")

        time.sleep(delay)

        yUnit = self.__query__("WFMPre:YUNit?")
#
#        time.sleep(delay)
#
# 
#
        xZero = self.__queryValue__("WFMPRE:XZEro?")

        yZero = self.__queryValue__("WFMPRE:YZEro?")

        self.__writeValue__('*CLS')
        
        self.__writeValue__('DATa:SOUrce CH'+str(channel))
        
        time.sleep(0.05)
#        
#        tmp=self.__queryValue__('WFMOutpre?')
#        
#        tmp=tmp.split(';')
#        
#        if len(tmp)<18:
#            time.sleep(0.2)
#            tmp=self.__queryValue__('WFMOutpre?')
#        YOFf=float(tmp[16])
#        YMUlt=float(tmp[15])
#        YZEro=float(tmp[17])
#        XINcr=float(tmp[11])
#        XZEro=float(tmp[12])


        start = self.GetStart()
        stop = self.GetStop()
        Trace=[]
        for i in range(NumberofTraces):

            
            
            
            yData = self.__queryChannel__("CURVE?", channel, isBinary=True)
            
#            yData=[float(TMP) for TMP in self.__query__('CURVE?').splitlines()]
            
            
#            self.__write__('CURVE?')
#            yData=self.__readRaw__()
#            headerlen=2+int(yData[1])
#            header=yData[:headerlen]
#            yData=yData[headerlen:-1]
            
#            yData= np.array(unpack('%sB' % len(yData),yData))
            self.__writeValue__('*WAI')
            
            xData = np.linspace(start,stop,len(yData))

            # See page 2-319 in manual for formula
    
            yData = yZero + yScale*(yData - yOffSet)
    
            xData = xZero + xScale*(xData - xOffSet)
            
#            if NumberofTraces<4:
            plot = plt.plot(xData,yData)
    
            plt.grid(True)
    
            plt.xlabel(xUnit)
    
            plt.ylabel(yUnit)
    
            plt.show(block=False)
                
            Trace.append(xData)
            Trace.append(yData)
            
    
#            return ((xData,xUnit),(yData,yUnit))
        return Trace

 

    def GetMean(self,channel=None):

        channel = channel if channel is not None else self.source

        ch = self.__mapToChannel__(channel)

        ch = ch[2:] # 'CH1' -> '1'

        mean = float(self.__queryChannel__("MEASU:MEAS" + ch + ":MEAN?"))

        return mean

 
    def SetSamplePts(self,Value):
        
        self.__write__("HORIZONTAL:RECORDLENGTH " +  str(Value))
        time.sleep(0.1)
        self.__write__("Data:Stop " +  str(Value))
        time.sleep(0.1)
        Pts= self.GetSamplePts()
        time.sleep(0.1)
        
        if Pts == Value:
            print('Number of sample points is set correctly')
        else:
            print('Number of sample points is set wrong')
        

    def GetSamplePts(self):
        Pts=float(self.__query__('HORIZONTAL:RECORDLENGTH?'))
        Pts2=float(self.__query__('Data:Stop?'))
        if Pts!=Pts2:
            print('Error: Recordlength and Data Stop Not Equal')
        return Pts
    def SetRecordLength(self,length, valid_lengths=None,boundaries=None, output=True):

        """Sets number of data points to be returned

Number of data points returned is the minimum between (stop - start + 1) and RecordLength"""

        if (valid_lengths):

            recordLength = min(valid_lengths, key=lambda x:abs(x-length))

        if (boundaries):

            minimum = boundaries[0]

            maximum = boundaries[1]

            if (length<minimum or length>maximum):

                raise Exception("Record length must be smaller than", str(minimum), "and larger than", str(maximum))

            recordLength = length

        self.__write__("HORizontal:RECORDLength " +  str(recordLength))

        time.sleep(delay)

        curLen = int(self.__query__("HORizontal:RECORDLength?"))

        if (recordLength != curLen):

            raise Exception("Failed to Set record length")

        elif (output):

            print("Record length successfully Set to", str(recordLength))

 

    # Returns number of data points to be returned 

    # 

    def GetRecordLength(self):

        return int(self.__query__("WFMPre:NR_Pt?"))
    
    def DisplayScopeWindow(self):
        return webbrowser.open_new('http://'+self.addressString+':81' )
        

 
     

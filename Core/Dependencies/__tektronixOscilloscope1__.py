import visa
import time
import re
import numpy as np
import matplotlib.pyplot as plt
import types
import os

from __connection__ import Connection
from globalsFile import *

delay = 0.05

# Uses channel self.channel if no channel is set.
class TektronixScope1(Connection):
    """
Base Tektronix Driver that seems to be compatible with:

Tektronix TDS3000 series
Tektronix MDO3014

and more

"""
    def __init__(self,addressString):
        Connection.__init__(self,addressString)

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

    def getSource(self):
        return self.__query__("DATa:SOURCE?")

    def getChannel(self):
        return self.getSource()

    def setChannel(self,channel):
        if (type(channel) == int):
            channelToSet = "CH" + str(channel)
        elif (channel == None):
            return
        else:
            channelToSet = channel
        self.__write__("DATa:SOURCE " + channelToSet)
        time.sleep(delay)
        curChannel = self.getChannel()
        if (curChannel != channelToSet):
            print("Channel set incorrectly")
            print("Attempted to set channel to", channelToSet, "but channel is set to", curChannel)
            return
        self.source = channelToSet



    def getSources(self,pprint=True):
        if (pprint):
            print(self.sources)
        else:
            return self.sources

    def setSource(self, source):
        self.__write__("DATa:SOURCE " + source)
        time.sleep(delay)
        curSource = self.getSource()
        if (curSource.upper() != source.upper()):
            print("Source set incorrectly")
            print("Attempted to set source to", source, "but source is set to", curSource)
            print("Please use one of the following sources:")
            print(self.sources)
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
    # If isBinary is set to true, then the command is expecting binary to be returned from the query
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
            self.setSource(origSource)
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
            self.setSource(origSource)
        return response

    def startCapture(self, prompt=True):
        self.__write__("ACQuire:STATE ON")

        state = int(self.__query__('ACQuire:STATE?'))

        if not state:
            raise Exception("Did not start capturing successfully")

        elif prompt:
            print("Started Capturing")

    def stopCapture(self,prompt=True):
        self.__write__("ACQuire:STATE OFF")

        state = int(self.__query__('ACQuire:STATE?'))

        if state:
            raise Exception("Did not stop capturing successfully")

        elif prompt:
            print("Stopped Capturing")

    def getCaptureStatus(self):
        state = self.__query__("ACQuire:STATE?")
        if (int(state)):
            return "ON"
        else:
            return "OFF"

    def getStart(self):
        start = int(self.__query__("DATa:START?"))
        time.sleep(delay)
        return start

    def getStop(self):
        stop = int(self.__query__("DATa:STOP?"))
        time.sleep(delay)
        return stop

    def setStart(self,start):
        self.__write__("DATa:START " + str(start))
        curStart = self.__query__("DATa:START?")
        if (float(start) != float(curStart)):
            raise Exception("Start set incorrectly")
        else:
            print("Start set to", str(start))

    def setStop(self,stop):
        self.__write__("DATa:STOP " + str(stop))
        time.sleep(delay)
        curStop = self.__query__("DATa:STOP?")
        if (float(stop) != float(curStop)):
            raise Exception("Stop set incorrectly")
        else:
            print("Stop set to", str(stop))

    def getTrace(self,channel=None):
        """Prints the trace for a channel
Returns (xData,xUnit),(yData,yUnit) (x/yData is a np array,x/yUnit is a string)"""

        channel = channel if channel is not None else self.source
        self.__writeValue__("WFMPre:PT_Fmt Y")

        xOffset = self.__queryValue__("WFMPre:PT_Off?")
        yOffset = self.__queryValue__("WFMPre:YOFf?")

        xScale = self.__queryValue__("WFMPre:XINcr?")
        yScale = self.__queryValue__("WFMPre:YMUlt?")

        xUnit = self.__query__("WFMPre:XUNit?")
        time.sleep(delay)
        yUnit = self.__query__("WFMPre:YUNit?")
        time.sleep(delay)

        xZero = self.__queryValue__("WFMPRE:XZEro?")
        yZero = self.__queryValue__("WFMPRE:YZEro?")

        start = self.getStart()
        stop = self.getStop()

        yData = self.__queryChannel__("CURVE?", channel, isBinary=True)
        xData = np.linspace(start,stop,len(yData))


        # See page 2-319 in manual for formula
        yData = yZero + yScale*(yData - yOffset)
        xData = xZero + xScale*(xData - xOffset)

        plot = plt.plot(xData,yData)
        plt.grid(True)
        plt.xlabel(xUnit)
        plt.ylabel(yUnit)
        plt.show(block=False)
        return ((xData,xUnit),(yData,yUnit))

    def getMean(self,channel=None):
        channel = channel if channel is not None else self.source
        ch = self.__mapToChannel__(channel)
        ch = ch[2:] # 'CH1' -> '1'
        mean = float(self.__queryChannel__("MEASU:MEAS" + ch + ":MEAN?"))
        return mean

    def setRecordLength(self,length, valid_lengths=None,boundaries=None, output=True):
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
        self.__write__("HORizontal:RECORDLength " + str(recordLength))
        time.sleep(delay)
        curLen = int(self.__query__("HORizontal:RECORDLength?"))
        if (recordLength != curLen):
            raise Exception("Failed to set record length")
        elif (output):
            print("Record length successfully set to", str(recordLength))

    # Returns number of data points to be returned 
    # 
    def getRecordLength(self):
        return int(self.__query__("WFMPre:NR_Pt?"))

        

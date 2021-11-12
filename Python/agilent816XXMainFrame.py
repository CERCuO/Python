from __connection__ import Connection
from globalsFile import *

"""
ALL FUNCTIONS THAT USE A CHANNEL OR SLOT MUST HAVE `channel` OR `slot` AS A PARAMETER.
THESE PARAMETERS ARE FILLED DYNAMICALLY WITH THE INSTRUMENT'S INITIALIZED CHANNEL AND SLOT (See __moduleInstrument__.py).

However, in this class, if you call any class methods, it will not be filled out because this is being called
from the mainframe which does not have any channel or slot. For example in SetSensorWavelength, when we call
GetSensorWavelength, we have to specify the channel and slot.

eg: agilent81619("1.21.1.1") will initialize an object that has copied all functions 
that accept channel and slot as parameters with default arguments channel=1 and slot=1

This class isn't meant to be instantiated directly. It's an object within a moduleInstrument instance
"""
delay = 0

class Agilent816XXMainFrame(Connection):
    def __init__(self,addressString):
        Connection.__init__(self,addressString)
        self.Driver_Document = 'Agilent816XXMainFrame.pdf'
        self.modes = {
        "CONTINUOUS": "CONT",
        "WINDOW": "WIND",
        "REFRESH": "REFR",
        "OFF": "OFF" 
        }
        self.channel = None
        self.slot = None

    def SetSensorWavelength(self,wavelength, slot, channel):
        """Set wavelength in nanometers"""
        self.__write__(":SENS%d:CHAN%d:POW:WAVE%6.3fNM" % (slot,channel,wavelength))

        wavelengthSet = self.GetSensorWavelength(slot, channel)
        if (wavelength != wavelengthSet):
            err = "Wavelength not Set correctly. Wavelength is " + str(wavelengthSet) 
            raise Exception(err)
        else:
            print("Wavelength Set to ",str(wavelength) + "nm")

    def GetSensorWavelength(self,slot, channel):
        """Get wavelength in nanometers"""
        resp = self.__query__(":SENS%d:CHAN%d:POW:WAVE?" % (slot,channel))
        return float(resp)*1E9 # query returns in meters as string

    def SetSourceWavelength(self,wavelength, slot, channel):
        """Set wavelength in nanometers"""
        self.__write__(":SOUR%d:CHAN%d:POW:WAVE%6.3fNM" % (slot,channel,wavelength))

        wavelengthSet = self.GetSourceWavelength(slot,channel)
        if (wavelength != wavelengthSet):
            err = "Wavelength not Set correctly. Wavelength is " + str(wavelengthSet)
            raise Exception(err)
        else:
            print("Wavelength Set to ",str(wavelength) + "nm")

    def GetSourceWavelength(self,slot, channel):
        """Get wavelength in nanometers"""
        resp = self.__query__(":SOUR%d:CHAN%d:WAVE?" % (slot,channel))
        return float(resp)*1E9 # query returns in meters

    def printModes(self):
        print(self.modes)

    def SetMode(self,mode,point, slot):
        mode = mode.upper()
        modeCmdStr = None
        for m in self.modes:
            if mode in m:
                modeCmdStr = self.modes[m]
        if not modeCmdStr:
            raise Exception("No mode corresponds to " + mode)
        
        if mode == "OFF":
            self.__write__(':SENS'+ str(slot) + ':FUNC:STAT MINM, STOP')
        else:
            self.__write__(':SENS' + str(slot) + ':FUNC:STAT MINM, STOP')
            time.sleep(delay)
            self.__write__(':SENS' + str(slot) + ':FUNC:PAR:MINM' + modeCmdStr + ',' + str(Point))
            time.sleep(delay)
            self.__write__('SENS' + str(slot) + ':FUNC:STAT MINM, STAR')
            time.sleep(delay)

        curMode, curPoint = self.GetMode(slot)

        if (modeCmdStr == "OFF"):
            curMode = self.__query__(":SENS" + str(slot) + "FUNC:STAT?").split(",")[0]
            if (curMode == "NONE"):
                curMode = "OFF"
        
        if (curMode == modeCmdStr and point == curPoint):
            print("Mode is Set correctly")
        else:
            err = "Mode is Set incorrectly. Current mode is" + curMode +". Current point is " + str(curPoint)
            raise Exception(err)




    def GetMode(self,slot):
        ret = self.__query__(':SENS' +str(slot)+ ':FUNC:PAR:MINM?').split(",")
        ret[1] = float(ret[1])
        return ret

    def GetMaxWavelength(self,slot,channel):
        """Returns the Max wavelength in nanometers"""
        wl = float(self.__query__(':SENS'+ str(slot) + ':CHAN' + str(channel) + ':POW:WAVE? MAX'))
        return wl*1E9

    def GetMinWavelength(self,slot,channel):
        """Returns the Min wavelength in nanometers"""
        wl = float(self.__query__(':SENS'+ str(slot) + ':CHAN' + str(channel) + ':POW:WAVE? MIN'))
        return wl*1E9

    def SetAveraGetime(self,time, slot,channel):
        """Set average time in miliseconds"""
        self.__write__(':SENS%d:CHAN%d:POW:ATIM %6.0fMS' % (slot,channel,time))

        curAvgTime = self.GetAveraGetime(slot,channel)
        if (time != curAvgTime):
            raise Exception("Average time not Set correctly. Average time is " + str(curAvgTime))

    def GetAveraGetime(self,slot,channel):
        """Get average time in miliseconds"""
        return float(self.__query__(':SENS' + str(slot) + ':CHAN' + str(channel) + ':POW:ATIM?'))*1000 # Query returned in seconds

    def SetUnit(self,unit,slot,channel):
        """Unit is "DBM" (0) or "WATT" (1)"""
        unit = unit.upper()
        if (unit == "DBM"):
            unitCmd = "0"
        elif (unit == "W" or unit == "WATT"):
            unitCmd = "1"
        else:
            raise Exception("Unit must be `DBM` or `W`/`WATT`\n"+unit+" is not a recognized unit")

        self.__write__(':SENS' + str(slot) + ':CHAN', + str(channel) + ':POW:UNIT ' + unitCmd)
        time.sleep(delay)
        curUnit = self.GetUnit(slot,channel)
        if curUnit[0] == unit[0]: # First character is either W or D
            print("Unit Set correctly")
        else:
            raise Exception("Unit did not Set correctly. Unit is Set to", curUnit, "instead of", unit)


    def GetUnit(self,slot,channel):
        query = self.__query__(':SENS' + str(slot) + ':CHAN', + str(channel) + ':POW:UNIT ' + unitCmd)
        if (query == "0"):
            return "DBM"
        elif (query == "1"):
            return "W"
        else:
            raise Exception("Expected query for unit to be either 0 or 1. Got `" + query + "`")

    def GetReading(self,slot,channel):
        return float(self.__query__(':FETC' + str(slot) + ':CHAN' + str(channel) + ':POW?'))

    def SetOutputStatus(self,status,slot,channel):
        if (type(status) == str):
            if (status.upper() == "OFF"):
                status = 0
            elif (status.upper() == "ON"):
                status = 1
            else:
                raise Exception("Status `%s` not a valid string. Must be 0,1,off,on" % status)
        self.__write__(':SOUR%d:CHAN%d:POW:STAT %s' % (slot,channel,status))
        time.sleep(delay)
        curStatus = self.GetOutputStatus(slot,channel)
        if (curStatus != status):
            raise Exception("Status not Set correctly. Status is " + str(curStatus))
        else:
            print("Status Set correctly")

    def GetOutputStatus(self,slot,channel):
        return int(self.__query__(':SOUR' + str(slot) + ':CHAN' + str(channel) + ':POW:STAT?'))



from __connection__ import Connection
from globalsFile import *

import time

delay = 0

class SantecTSL1(Connection):
    def __init__(self,addressString):
        Connection.__init__(self,addressString)
        self.__setTimeout__(3000) # 3 seconds
        self.Driver_Document = None
        #self.setDelimeter()
        self.minWavelength = self.GetMinWavelength()
        self.maxWavelength = self.GetMaxWavelength()

    #Sets newline as delimiter
    def setDelimeter():
        # Delimiters:
        # 0：CR
        # 1：LF
        # 2：CR+LF
        # 3：None
        self.__write__(":SYST:COMM:GPIB:DEL 1")
        self.setReadTermination("\n")

    # This gets a value according to a command string and returns it as a float
    # This function is used by specific commands - eg: getStartWavelength using command "STA"
    def __getValue__(self,command):
        return float(self.__query__(command + "?"))

    # This function sets a value on the instrument
    # This function is used by specific commands - eg: setStartWavelength using command "STA", value 1200, valueName StartWavelength
    # IMPORTANT: Since we use camelcase, it is required to pass valueName capitalized as written in the function name - eg: get`StartWavelength`
    def __setValue__(self,command,value, valueName):
        self.__write__(command + ' ' + str(value))
        getFunction = getattr(self,"Get" + valueName) # This is the getter function for ValueName that we define for this class
        time.sleep(0.1)
        valRead = getFunction()

        # Add a space before each new word (In camelCase, new words begin with a capital letter)
        pretty_valueName = ""
        for l in valueName:
            if l.isupper():
                # capital means split word by a space
                pretty_valueName += " " + l
            else:
                pretty_valueName += l

        # Verify that the value is set correctly
        if (valRead == value):
            print(pretty_valueName + ' is set correctly')
        else:
            print(pretty_valueName + "is set wrong. " + pretty_valueName + " is " + str(valRead))

    def GetMinWavelength(self):
        return self.__getValue__("WAV:MIN")

    def GetMaxWavelength(self):
        return self.__getValue__("WAV:MAX")
    def GetMaxPower(self):
        return self.__getValue__('POWER:MAX')
    def GetWavelength(self):
        return self.__getValue__("WAV")

    def SetWavelength(self,wavelength):
        self.__setValue__("WAV",wavelength,"Wavelength")

    def GetCoherentStatus(self):
        return self.__getValue__(":COHCtrl")

    def SetCoherentStatus(self,status):
        self.__setValue__(":COHCtrl",status,"CoherentStatus")

    def GetOutputStatus(self):
        if self.__getValue__("POWer:SHUTter") == 1:
            return 0
        elif self.__getValue__("POWer:SHUTter") == 0:
            return 1

    def SetOutputStatus(self,status):
        self.__setValue__("POWer:SHUTter",status,"OutputStatus")

    def GetLDStatus(self):
        return self.__getValue__("POWer:STATe")

    def SetLDStatus(self,status):
        self.__setValue__("POWer:STATe",status,"LDStatus")

    def GetAttenuation(self):
        return self.__getValue__(":POW:ATT")

    def SetAttenuation(self,attenuation):
        self.__setValue__(":POW:ATT",attenuation,"Attenuation")
        
    def GetPower(self):
        return self.__getValue__(':POW')
    
    def SetPower(self,Power):
        self.__setValue__(':POW',Power,'Power')
        
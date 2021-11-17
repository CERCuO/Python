from __connection__ import Connection
import time
import math

"""
THIS CODE IS COPIED FROM MATLAB VERSION WITHOUT TESTING. 

NEEDS TO BE VERIFIED / POSSIBLY ABSTRACTED FURTHER FOR REUSE
"""

class HP8156A(Connection):
    def __init__(self,addressString):
        Connection.__init__(self,addressString)
        self.Driver_Document = 'HP8156A.pdf'


    # This Gets a value according to a command string and returns it as a float
    # This function is used by specific commands - eg: GetStartWavelength using command "STA"
    def __GetValue__(self,command,nm=False):
        val = float(self.__query__(command + "?"))
        if (nm and val<1):
            return val*1E9
        else:
            return val

    # This function Sets a value on the instrument
    # This function is used by specific commands - eg: SetStartWavelength using command "STA", value 1200, valueName StartWavelength
    # IMPORTANT: Since we use camelcase, it is required to pass valueName capitalized as written in the function name - eg: Get`StartWavelength`
    def __SetValue__(self,command,value, valueName, unit=""):
        self.__write__(command + ' ' + value + unit)
        GetFunction = getattr(self,"Get" + valueName) # This is the Getter function for ValueName that we define for this class
        time.sleep(0.2)
        valRead = GetFunction()

        # Add a space before each new word (In camelCase, new words begin with a capital letter)
        pretty_valueName = ""
        for l in valueName:
            if l.isupper():
                # capital means split word by a space
                pretty_valueName += " " + l
            else:
                pretty_valueName += l

        # Verify that the value is Set correctly
        if (math.floor(valRead*100)/100 == math.floor(float(value)*100)/100):
            print(pretty_valueName + ' is Set correctly')
        else:
            print(pretty_valueName + " is Set wrong. " + pretty_valueName + " is " + str(valRead))

    def GetWavelength(self):
        return self.__GetValue__(":INP:WAV",nm=True)

    def SetWavelength(self,wavelength):
        self.__SetValue__(":INP:WAV", "%6.3f"%wavelength, "Wavelength", "nm")

    def GetOutputStatus(self):
        return self.__GetValue__(":OUTP")

    def SetOutputStatus(self,status):
        self.__SetValue__(":OUTP", str(status), "OutputStatus")

    def GetAttenuation(self):
        return self.__GetValue__(":INP:ATT")

    def SetAttenuation(self,attenuation):
        self.__SetValue__(":INP:ATT", str(attenuation), "Attenuation")






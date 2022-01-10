
import pyvisa as visa
rm = visa.ResourceManager()
import re
import os

from __baseInstrument__ import BaseInstrument



"""
the NI VISA library aliases different connections through a resource name convention which has been documented by pyVisa here:
https://pyvisa.readthedocs.io/en/stable/names.html
The resource name is constructed from the initialization parameters. The constructed resource name is missing the 
resource alias which is optional (ie: inst0). This is intentional

"""

gpibObjectsDict = {}

# This function creates the visa GPIB object and stores it in a dictionary
# This reuses the same object for addresses that have the same board number and device ID (xx.yy)
def initGpib(addressString):
    # This interprets object("xx.yy") initialization
    if ("." in addressString):
        address = addressString.split(".")
        if (len(address) < 2):
            raise ValueError("GPIB address must be at least two numbers (xx.yy)")
        key = address[0] + "." + address[1]
        resourceName = "GPIB" + address[0] + "::" + address[1] + "::INSTR"
    # This interprets initialization 'raw' so that you can just copy paste the resource you found with listResources()
    else:
        resourceName = addressString
        address = addressString.split("::")
        try:
            key = re.search(r'GPIB([0-9]+)', address[0]).group(1) + "." + address[1]
        except:
            raise ValueError("Resource", resourceName, "is not a valid GPIB resource name")

    if key in gpibObjectsDict:
        return gpibObjectsDict[key]
    else:
        try:
            obj = rm.open_resource(resourceName)
        except visa.VisaIOError as e:
            # Bus Error
            if (e.error_code == -1073807304):
                print("Check that GPIB cable is plugged in properly and device is on.")
            raise
        gpibObjectsDict[key] = obj
        return gpibObjectsDict[key]

# Base GPIB class which shall be inherited by all objects that use GPIB
class Gpib(BaseInstrument):
    def __init__(self,addressString):
        self._visaObj = initGpib(addressString)
        self.__setTimeout__(3000) # 3 seconds
        self.connectionType = ConnectionTypes.GPIB

    def __del__(self):
        """
There is a problem if instruments are not closed before a script ends. 
Pyvisa garbage collection will clean up the object in the wrong order and cause an error to be thrown.
For this reason, it's important that the close method is called on the visa object to ensure proper cleanup.
        """
        self.__close__()

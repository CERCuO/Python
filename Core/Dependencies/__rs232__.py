
from __baseInstrument__ import *

rs232ObjectsDict = {}


"""
the NI VISA library aliases different connections through a resource name convention which has been documented by pyVisa here:
https://pyvisa.readthedocs.io/en/stable/names.html
The resource name is constructed from the initialization parameters. The constructed resource name is missing the 
resource alias which is optional (ie: inst0). This is intentional

"""


"""
THIS HASN'T BEEN TESTED
"""

# This function creates the visa RS232 object and stores it in a dictionary
# This reuses the same object for the same serial port
def initRS232(addressString):
    port = None
    try:
        # try to convert to int to see if it's in format 'ASRL10::INSTR' or '10' or 10. 
        # If exception is thrown, assume given resource name directly or given COM port
        port = int(addressString)
        resourceName = "ASRL" + str(port) + "::INSTR"
    except:
        if ("COM" in addressString):
            resourceName = "COM%s" % addressString[3:]
        else:
            resourceName = addressString

    key = resourceName
#    if key in rs232ObjectsDict:
        #return rs232ObjectsDict[key]
#    else:
    obj = rm.open_resource(resourceName)
    rs232ObjectsDict[key] = obj
    return rs232ObjectsDict[key]

# Base RS232 class which shall be inherited by all objects that use RS232
class Rs232(BaseInstrument):
    def __init__(self,addressString):
        self._visaObj = initRS232(addressString)
        self.__setTimeout__(3000) # 3 seconds
        self.connectionType = ConnectionTypes.RS232
        
    def __del__(self):
        """
There is a problem if instruments are not closed before a script ends. 
Pyvisa garbage collection will clean up the object in the wrong order and cause an error to be thrown.
For this reason, it's important that the close method is called on the visa object to ensure proper cleanup.
        """
        self.__close__()
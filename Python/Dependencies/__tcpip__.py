import visa
import time
import re
import numpy as np
import matplotlib.pyplot as plt
import types
import os

from __baseInstrument__ import *


"""
the NI VISA library aliases different connections through a resource name convention which has been documented by pyVisa here:
https://pyvisa.readthedocs.io/en/stable/names.html
The resource name is constructed from the initialization parameters. The constructed resource name is missing the 
resource alias which is optional (ie: inst0). This is intentional

"""

tcpIpObjectsDict = {}

# This function creates the visa TCP/IP object and stores it in a dictionary
# This reuses the same object for an IP address/port. 
# Intialized like: Object("IP:PORT:slot.channel") or Object("IP:PORT")
# or Object("RESOURCE") ie: Object("TCPIP0::10.120.73.100::4000::SOCKET")
# Finds the resource name from list of accessible resources
def initTcpIp(addressString):
    port = None
    if ("::" in addressString):
        resource = addressString
        address = addressString.split("::") 
        ip, port = address[1],address[2]
        if port.isnumeric():
            key = ip + ":" + port
        else:
            key = ip
    else:
        address = addressString.split(":")
        ip = address[0]
        if (len(address) >= 2):
            if not "." in address[1]:
                port = address[1]
        if port:
            key = ip + ":" + port
        else:
            key = ip
            
        if port:
            resource = "TCPIP::" + ip + "::" + port + "::SOCKET"
        else:
            resource = "TCPIP::" + ip + "::INSTR"
    if key in tcpIpObjectsDict:
        return tcpIpObjectsDict[key]
    else:
        try:
            device = rm.open_resource(resource)
        except Exception as e:
            print(str(e))
            raise Exception("Failed to open device resource:", resource)
        try:
            pass
#            device.query("*IDN?")
        except Exception as e:
            print(str(e))
            raise Exception("Failed to query IDN from resource:", resource)

        tcpIpObjectsDict[key] = device
        return tcpIpObjectsDict[key]

# Base TCP/IP class which shall be inherited by all objects that use TCP/IP type of connection
class TcpIp(BaseInstrument):
    def __init__(self,addressString):
        self._visaObj = initTcpIp(addressString)
        self.__setTimeout__(5000) # 5 seconds
        self.connectionType = ConnectionTypes.TCPIP

    def __del__(self):
        """
There is a problem if instruments are not closed before a script ends. 
Pyvisa garbage collection will clean up the object in the wrong order and cause an error to be thrown.
For this reason, it's important that the close method is called on the visa object to ensure proper cleanup.
        """
        self.__close__()
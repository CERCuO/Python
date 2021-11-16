from __gpib__ import Gpib
from __tcpip__ import TcpIp
from __rs232__ import Rs232


"""
the NI VISA library aliases different connections through a resource name convention which has been documented by pyVisa here:
https://pyvisa.readthedocs.io/en/stable/names.html
The resource name is constructed from the initialization parameters. The constructed resource name is missing the 
resource alias which is optional (ie: inst0). This is intentional

"""

class Connection(Gpib,TcpIp,Rs232):
    def __init__(self,addressString,tryGuessReadTermination=False):
        if not addressString:
            raise ValueError("Object must be initialized with addressString describing connection type. Read the README.txt")
        if (type(addressString) == str):
            if not ("::" in addressString):
                # Call the correct parent constructor based on connection type
                # If the constructor only receives one number, `num`, then it initializes a serial port with port `num`
                # Else, Assumed to be either GPIB or TCP/IP with never more than 10 GPIB connections
                # See tcpip.py and gpib.py for more details on how to these types of connections are initialized 
                if (":" in addressString):
                    TcpIp.__init__(self,addressString)
                else:
                    address = addressString.split(".")

                    if(len(address) == 1):
                        Rs232.__init__(self,addressString)
                    elif (address[0].isnumeric and int(address[0]) < 10):
                        Gpib.__init__(self,addressString)
                    else:
                        TcpIp.__init__(self,addressString)
            else:
                if ("ASRL" in addressString):
                    Rs232.__init__(self,addressString)
                elif ("GPIB" in addressString):
                    Gpib.__init__(self,addressString)
                elif ("TCPIP" in addressString):
                    TcpIp.__init__(self,addressString)
                else:
                    raise Exception("Cannot interpret connection type of constructor argument. Read the README.txt")
        # If the constructor is a number, then assume it's RS232 with port as argument
        elif (type(addressString) == int or type(addressString) == float):
            Rs232.__init__(self,addressString)
        else:
            raise Exception("Cannot interpret connection type of constructor argument. Read the README.txt")
        if (tryGuessReadTermination):
            self.guessReadTermination()


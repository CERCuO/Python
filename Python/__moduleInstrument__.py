import visa
import importlib
import functools
import inspect

from __connection__ import Connection
from globalsFile import *


# This dictionary maps MainFrame manufacturer and model numbers to a MainFrame Class based on the *IDN? query.
# The dictionary keys are the manufacturer ID and model number separated by a ':' 
# The value is the className for that model
# 
# IE:
# manufacturer, model_number = self.getID()[:2] # __baseInstrument__ method
# key = manufacturer + ":" + model_number
mainFrameClasses = {
    "Agilent Technologies:8163B": "Agilent816XXMainFrame", # Agilent816XXMainFrame is the className for the mainframe implementation
    "HEWLETT-PACKARD:HP8163A": "Agilent816XXMainFrame",
}

# From an object oriented perspective, ModuleInstrument shouldn't actually inherit Connection, since the connection is handled by the MainFrame object
# But, it's neccessary because this object must have a connection through which to query the mainFrame to figure out its ID before it has a MF object

# Ensure that any module instrument that inherits from this has the **kwargs in their constructor so that the MainFrame can be passed explicitly if needed.
class ModuleInstrument(Connection):
    def __init__(self,addressString,**kwargs):

        if ("::" in addressString):
            raise ValueError("Module Instruments cannot be initialized by resource names. Channel and Slot is required.")
        if (kwargs.get('MF',None)):
            # MainFrame will already have guessed read termination
            # and if they only initialize with slot/channel, won't be able to query IDN
            Connection.__init__(self,addressString,tryGuessReadTermination=False)
        else:
            Connection.__init__(self,addressString)


        # eg: if addressString is '10.120.84.73:5555:10.2', address is [10,2]
        # if addressString is '10.20.30.40', then addressString.split(":")[-1:][0] is just '10.20.30.40', so address is just [10,20,30,40]
        address = addressString.split(":")[-1:][0].split(".")

        if (kwargs.get('MF',None)):
            if (not all([s.isnumeric() for s in address])
                or (not len(address) == 2) # GPIB must be initialized like slot.channel
                ):
                error = "If MainFrame is specified, the addressString must only specify the slot and channel numbers.\n"
                error += "eg: \"1.2\" is slot 1 channel 2"
                raise ValueError(error)
        else:
            if (not all([s.isnumeric() for s in address])
                or (self.connectionType == ConnectionTypes.GPIB and not len(address)  == 4)
                or (self.connectionType == ConnectionTypes.TCPIP and not len(address) == 2)
                ):
                error = \
"""Instrument must be initialized through GPIB or TCP/IP connection.
GPIB Address must be xx.yy.zz.jj (4 numbers long - board,deviceID,slot,channel)
TCP/IP address must be IP:zz.jj or IP:PORT:zz.jj (where zz and jj are the slot and channel respectively.)
If no specific channel, just use 1 as channel"""
                raise ValueError(error)


        self.Driver_Document = None

        # Allow for mainframe to be given explicitly as a keyword argument MF=someMainFrameObject
        if kwargs.get('MF',None):
            # There's no check that this is indeed a mainframe because there's no mainframe class. User should know better, should be fine.
            self.MF = kwargs['MF']
            self.MF_className = self.MF.__class__.__name__
        else:
            MF_class = self.__getMainframeClass__()
            self.MF_className = MF_class.__name__
            self.MF = MF_class(addressString) # Instantiate the mainframe object which handles commands, gpib/tcp connection, etc
            # we set the instrument's visaObj to be the MF's visa object since the MF handles the gpib/tcpip connection
            # and we want to be able to use the BaseIntrument methods using this visa object
        self._visaObj = self.MF._visaObj # This is redundant since they are the same object
        self.slot,self.channel = [int(num) for num in address[-2:]]

        MF_attribute_names = [attr for attr in dir(self.MF) if not attr.startswith("_")]
        for attr_name in MF_attribute_names:
            attr = getattr(self.MF,attr_name)
            if (callable(attr)):
                func = attr # renamed for readability / clarify 
                # Don't copy over functions that are already implemented by this instrument
                if hasattr(self,func.__name__):
                        continue
                param_names = [param for param in inspect.signature(func).parameters.keys()]
                kwargs = {}
                for param in param_names:
                    # channel and slot should be lower case, but to be safe, it's actually case insensitive
                    if (param.lower() == 'channel'):
                        kwargs[param] = self.channel
                    if (param.lower() == 'slot'):
                        kwargs[param] = self.slot
                # Copy all the methods from mainframe into ModuleInstrument with the 
                # Channel and Slot parameters set with the instrument's channel/slot as a default parameter
                # This dynamically bestows all the mainframe specific functions onto the ModuleInstrument object
                # This replaces functions with an object that defines the __call__ function, allowing the object to be called like a function 
                # The object holds the new default parameters and calls the function 'func' with those default parameters kwargs
                setattr(self,func.__name__,functools.partial(func,**kwargs))
            else:
                if hasattr(self,attr_name):
                    continue
                else:
                    setattr(self,attr_name,attr)


    def __getMainframeClass__(self):
        manufacturer, model_number = self.getID()[:2] # __baseInstrument__ method
        key = manufacturer + ":" + model_number
        className = mainFrameClasses.get(key,None)
        if (not className):
            import os # lazy import since it's only used in exception
            fileLocation = os.path.join(sharedDriverFolderPythonInstruments, "__moduleInstrument__.py")
            error = "Main Frame Not Implemented or not registered in mainFrameClasses. "
            error += "To register this mainframe, add it to mainFrameClasses in \n%s" % fileLocation
            raise Exception(error)
        moduleName = className[0].lower() + className[1:]
        module = importlib.import_module(moduleName)
        return getattr(module,className)

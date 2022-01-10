import os
import re
import numpy as np 
import inspect
import functools

isWindows = False
if (os.name == 'nt'):
    isWindows = True

class BaseInstrument:
    def __write__(self,string):
        self._visaObj.write(string)

    def __query__(self,string):
        return self._visaObj.query(string)

    def __readRaw__(self):
        return self._visaObj.read_raw()

    # Returns np array delimited by specified delimiter (Default is ',')
    def __queryAscii__(self,string,delimiter=","):
        return self._visaObj.query_ascii_values(string,container=np.array,separator=delimiter)

    def __queryBinary__(self,string,valueContainer=np.array,valueDatatype=u'b', headerFmt=u'ieee', bigEndian=False):
        return self._visaObj.query_binary_values(string,datatype=valueDatatype, is_big_endian=bigEndian, container=valueContainer, header_fmt=headerFmt)

    def showManual(self):
        assumeDriverDocName = False
        # Try block because if someone wrote a driver but forgot to define self.Driver_Document, then this will cause an exception to be thrown
        try:
            if (self.Driver_Document):
                driver_doc = os.path.join(sharedDriverManualFolder, self.Driver_Document)
                if (not os.path.exists(driver_doc)):
                    print("Could not find driver manual defined by self.Driver_Document in instrument's class file.")
                    print(driver_doc + " does not exist")
                else:
                    os.startfile(driver_doc)
            else:
                assumeDriverDocName = True
        except:
            # No self.Driver_Document defined
            assumeDriverDocName = True
        if (assumeDriverDocName):
            assumed_driver_doc_name = self.__class__.split(".")[-1]
            assumed_driver_doc_name = assumed_driver_doc_name[0].lower() + assumed_driver_doc_name[1:] + ".pdf"
            assumed_driver_doc_name = os.path.join(sharedDriverManualFolder, assumed_driver_doc_name)
            if (os.path.exists(assumed_driver_doc_name)):
                print("Using assumed driver manual location", assumed_driver_doc_name)
                os.startfile(assumed_driver_doc_name)
            else:
                print("This object is missing the self.Driver_Document variable")
                print("The assumed driver document name", assumed_driver_doc_name, "could not be found")

    def setReadTermination(self,string):
        self._visaObj.read_termination = string

    def getReadTermination(self):
        return self._visaObj.read_termination

    def setWriteTermination(self,string):
        self._visaObj.write_termination = string

    def getWriteTermination(self):
        return self._visaObj.write_termination

    def guessReadTermination(self):
        try:
            self.__write__("*IDN?")
        except Exception as e:
            print("Failed guess read terminating character")
            return
        idn = self.__readRaw__()
        if (idn[-2:] == b"\r\n"):
            self.setReadTermination("\r\n")
        elif(idn[-1:] == b"\r"):
            self.setReadTermination("\r")
        elif(idn[-1:] == b"\n"):
            self.setReadTermination("\n")
        else:
            self.setReadTermination("")

        


    def __setTimeout__(self,timeout):
        self._visaObj.timeout = timeout

    # returns 
    # [manufacturer, model_number, serial_number, firmware_revision]
    # in upper case
    def getID(self):
        return self.__query__("*IDN?").split(",")

    # Returns a list of function signatures
    # if showSlotChannel=True, it doesn't filter out the channel and slot from the method which is set dynamically
    def showFunctions(self,showSlotChannel=False):
        from __moduleInstrument__ import ModuleInstrument # imported here to avoid circularity in imports
        functionTuples = [ (method_name,getattr(self, method_name)) for method_name in dir(self)
            if (callable(getattr(self, method_name)) and not method_name.startswith("_"))]
        functions = []

        for idx,funcTuple in enumerate(functionTuples):
            method_name, func = funcTuple
            params = [str(param) for param in inspect.signature(func).parameters.values()]
            function = method_name + "("
            if (params):
                if (not showSlotChannel):
                    if issubclass(self.__class__,ModuleInstrument):
                        numDel = 0
                        for idx in range(len(params)):
                            adjustedIdx = idx - numDel
                            if (params[adjustedIdx].lower().split("=")[0] in ['channel','slot']):
                                del params[adjustedIdx]; numDel += 1
                for param in params[:-1]:
                    function += param + ","
                if (params):
                    function +=params[-1]
            function += ")"
            functions.append(function)
        return functions

    # Opens the source file for this object in a text editor
    def showSourceFile(self):
        # splits something like  "<class 'tektronixMDO3014.TektronixMDO3014'>"  to retrieve tektronixMDO3014 for example
        # then adds .py to the string to build the sourceFile name
        sourceFile = str(getattr(self,'__class__')).split("'")[1].split('.')[0] + ".py"
        sourceFilePath = sharedDriverFolderPythonInstruments + "\\" + sourceFile
        if (isWindows):
            try:
                # View the README to see how to add sublime text to the path
                os.system("subl.exe " + sourceFilePath) # Try to open in sublime text if in path
                return
            except:
                pass
            try:
                os.system("notepad.exe " + sourceFilePath) # verified to be on system path by default on windows 10, should be the case for other windows systems
            except:
                raise Exception("Couldn't find notepad or any other text editor on system path")
        else:
            raise Exception("This hasn't been implemented for other operating systems")
    def __close__(self):
        self._visaObj.close()

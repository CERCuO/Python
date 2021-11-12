from __connection__ import Connection
from globalsFile import *
import time

"""
THIS CODE IS COPIED FROM MATLAB WITHOUT TESTING. 

NEEDS TO BE VERIFIED / POSSIBLY ABSTRACTED FURTHER FOR REUSE
"""

class GeneralPhotonicsPCD104(Connection):
    def __init__(self,addressString):
        Connection.__init__(self,addressString)
        self.Driver_Document = 'GeneralPhotonicsPCD104.pdf'
        # self.__SetTimeout__(3000) # 3 seconds


    def SetStatus(self,status):
        if (status == 1):
            resp = self.__query__("*ENA#")
        elif (status == 0):
            resp = self.__query__("*DIS#")
        else:
            raise ValueError("Status parameter not recognized")
        if (resp == '*E00#'):
            print("Status Set correctly")
        else:
            raise Exception("Status Set incorrectly")


    def SetWavelength(self,wavelength):
        valid_wavelengths = [980,1060,1310,1480,1550,1600]
        wavelength = min(valid_wavelengths, key=lambda x:abs(x-wavelength))
        print('TarGet wavelength is changed to',str(wavelength),'nm')
        self.__write__('*WAV '+ str(wavelength) + '#')

        time.sleep(2)
        
        curWavelength = self.GetWavelength()

        if (curWavelength == wavelength):
            print("Wavelength Set correctly to", str(wavelength))
        else:
            raise Exception("Wavelength failed to Set to", str(wavelength), "Currently Set to ", str(curWavelength))

    def GetWavelength(self):
        resp = self.__query__("*WAV?")
        resp = resp.replace('*WAV ', '').replace("#",'')
        return float(resp)

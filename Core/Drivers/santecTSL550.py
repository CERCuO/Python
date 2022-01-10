from globalsFile import *
from __santecTSL1__ import *

class SantecTSL550(SantecTSL1):
    def __init__(self,addressString):
        SantecTSL1.__init__(self,addressString)
        # Missing
        self.Driver_Document = 'SantecTSL550.pdf' # Have to register a product to get the datasheet - http://www.santec.com/en/support/manual
        #self.setCoherentStatus(1)
        #self.setOutputStatus(0)
#        if (self.getLDStatus() == 0):
#            self.setLDStatus(1)
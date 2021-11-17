# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 12:02:43 2021

@author: danhu
"""

from __connection__ import Connection
import time
import math


class Newport1830R(Connection):
    def __init__(self,addressString):
        Connection.__init__(self,addressString)
        self.Manual = 'Newport1830R.pdf'
        
    def GetSTR(self, cmd):
        res = self.__query(cmd)
        return res

    #placeholder for driver to be completed later
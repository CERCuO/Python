# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 11:09:58 2021

@author: dhutama
"""
from __connection__ import Connection
import requests

class ezOutlet3:
    user = 'admin'
    pw = 'Welcome18'
    auth = requests.auth.HTTPBasicAuth(user, pw)
    
    def __init__(self, addressString):
        self.addressString = addressString
        
    def GetState(self):
        st = requests.post('http://{}/xml/outlet_status.xml'.format(self.addressString), auth = ezOutlet3.auth)
        s = st.text
        start = '<outlet_status>'
        end = '</outlet_status>'
        status_val = s[s.find(start)+len(start):s.rfind(end)]
        return status_val 
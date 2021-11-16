# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 09:30:14 2021
@author: dhutama
"""
import pyautogui as pg

c = 299792458 #m/s

while True:
    
    n = float(pg.prompt('Enter refractive index:'))
    calc = pg.prompt('(1) Wavelength (nm) -> Frequency (THz) \n(2) Frequency (THz) -> Wavelength (nm) \n(3) (Bandwidth) Wavelength (nm) -> Frequency (GHz) \n(4) (Bandwidth) Frequency (GHz) -> Wavelegnth (nm)')
    
    if int(calc) == 1:
        wl = float(pg.prompt('Enter wavelength (nm):'))
        pg.alert('{} nm => {:.6g} THz'.format(wl, c/(n*wl/1e9)/1e12))
        
    if int(calc) == 2:
        freq = float(pg.prompt('Enter frequency (THz):'))
        pg.alert('{} THz => {:.6g} nm'.format(freq, c/(n*freq*1e12)*1e9))
    
    if int(calc)==3:
        cent_wl = float(pg.prompt('Enter center wavelength (nm):'))
        bw = float(pg.prompt('Enter wavelength bandwidth (nm):'))
        pg.alert('Wavelength bandwidth of {} nm centered at {} nm corresponds to \nFrequency bandwidth of {:.6g} GHz centered at {:.6g} THz.'.format(bw, cent_wl, ((c/(n*cent_wl*1e-9)**2)*bw*1e-9)*1e-9, c/(n*cent_wl*1e-9)/1e12))
        
    if int(calc)==4:
        cent_f = float(pg.prompt('Enter center frequency (Thz):'))
        bw = float(pg.prompt('Enter frequency bandwidth (GHz):'))
        pg.alert('Frequency bandwidth of {} GHz centered at {} THz corresponds to \nWavelength bandwidth of {:.6g} nm centered at {:.6g} nm.'.format(bw, cent_f, c/n/(cent_f*1e12)**2*bw*1e18, c/(n*cent_f*1e12)*1e9))
        

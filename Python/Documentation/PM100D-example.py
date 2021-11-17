# Minimal working example for PM100D power meter

from PM100D import PM100D

#get the device address from NI-MAX
addr = "USB"

pm = PM100D("pm",addr)

#to get a reading
power = pm.read()

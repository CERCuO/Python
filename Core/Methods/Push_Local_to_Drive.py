# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 15:00:53 2022

@author: danhu
"""

#this will only work for my computer
#youll need to change the destination and source folders in line 16

# syntax:
# out = os.system('robocopy {source folder} "{destination folder}" /s')

from datetime import datetime

import os

out = os.system('robocopy C:\depot\CERC "G:\Shared drives\Lundeen Lab Cloud Storage\Individuals\Daniel\Local" /s')

if out == 0:
    print('No files were copied. No failure was encountered. No files were mismatched. The files already exist in the destination directory; therefore, the copy operation was skipped.')

if out == 1:
    print('All files were copied successfully.')
    
if out == 3:
    print('Some files were copied. Additional files were present. No failure was encountered.')

if out == 4:
    print('')

if out == 5:
    print('Some files were copied. Some files were mismatched. No failure was encountered.')
    
if out == 6:
    print('Additional files and mismatched files exist. No files were copied and no failures were encountered. This means that the files already exist in the destination directory.')
    
if out == 7:
    print('Files were copied, a file mismatch was present, and additional files were present.')
    
if out == 8:
    print('Several files did not copy.')
    
if out > 8:
    print('There was at least one failure during the copy operation.')
    
now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
print('{}   |   <PUSH TO DRIVE>'.format(now)) 
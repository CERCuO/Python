# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 11:59:07 2021

@author: danhu
"""

import matplotlib.pyplot as plt
import numpy


def PrePlotFormatting(xplotrange, yplotrange, xlabel = '', ylabel = '', title = ''):

    ########## PLOT FORMATTING ############
    l1, l2, font, s1, s2, padding = 3.0, 10.0, 25.0, 20.0, 10.0, 10.0
    fig = plt.figure('mydata', figsize = (s1,s2))
    plt.rcParams.update({'font.size': font})
    ax = fig.add_subplot(111)
    ax.ticklabel_format(style = 'sci', scilimits=(-5,3),axis='y')
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(l1)
        ax.xaxis.set_tick_params(width=l1, length = l2, pad=padding)
        ax.yaxis.set_tick_params(width=l1, length = l2, pad=padding)
    plt.ylabel(r'{}'.format(ylabel), fontsize=font, labelpad=padding)
    plt.xlabel(r'{}'.format(xlabel), fontsize = font, labelpad = padding)
    plt.grid()
    # plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    ########## PLOT FORMATTING ############
    ax.set_title(title, pad=20)
    
    try:
        plt.ylim(yplotrange)
        plt.xlim(xplotrange)
    except:
        print('Enter range as tuple.')
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 09:59:20 2019

@author: Henri Morin
henri.p.morin@gmail.com

Time Tagger GUI for Counter, Correlate and Lifetime ONLY
TimeTagger Web Interface has many more measurements, see documentation

Need the TimeTagger to be plugged in to work 
or comment out the first 2 lines of code after imports to start in test mode


TimeTagger module installed with timetagger software suite

"""

import tkinter as tk
from tkinter import END
from tkinter import simpledialog, messagebox
import sys
import os

#swabian code to import TimeTagger in a safe manner for Windows
try:
    import TimeTagger
except:
    print ("Time Tagger lib is not in the search path.")
    pyversion = sys.version_info
    from winreg import ConnectRegistry, OpenKey, HKEY_LOCAL_MACHINE, QueryValueEx
    registry_path = "SOFTWARE\\Python\\PythonCore\\" + str(pyversion.major) + "." + str(pyversion.minor) + "\\PythonPath\\Time Tagger"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    key = OpenKey(reg, registry_path) 
    module_path = QueryValueEx(key,'')[0]
    print ("adding " + module_path)
    sys.path.append(module_path)

import TimeTagger

#necessary imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#from matplotlib.animation import FuncAnimation
from time import sleep, time, strftime


#plot embedding imports
from matplotlib.backends.backend_tkagg import (
  FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


# create a timetagger instance, comment out these two lines if you want ot use the gui without a tagger plugged in

#tagger = TimeTagger.createTimeTagger()
#tagger.reset()

print('If you change measurements without clearing the previous one, please exit and reopen the program.')

#tkinter works best as a class and not just inline code
class tagger_gui(tk.Frame):
    def __init__(self, master=None):
        """
        initializises the class and some status variables before calling/initializing the widgets
        """
        
        super().__init__(master)
        self.master = master
        self.grid()
        
        self.measurement = tk.StringVar()
        self.measurement.set("M")
        
        self.test_real = tk.StringVar()
        self.test_real.set("")
        
        self.out = tk.StringVar()
        self.out.set("Waiting...")
        self.out2 = tk.StringVar()
        self.out2.set("")
        
        self.out_lab = tk.Label(self, textvariable=self.out)
        self.out_lab.grid(row=10, column=2, columnspan=2)
        self.out2_lab = tk.Label(self, textvariable=self.out2)
        self.out2_lab.grid(row=10, column=4, columnspan=2)
        
        self.status = tk.StringVar()
        self.status.set("Please select 'Test' or 'Real' signals then choose a measurement...")
        tk.Label(self, textvariable=self.status).grid(row=0, column=0, columnspan=2)        
        
        """
        DEFAULT FOR AUTOSAVE
        """
        self.autosave_span = 5#in mins
        print('Autosave set at '+str(self.autosave_span)+' minutes!')
        
        self.autosave_status = tk.StringVar()
        self.autosave_status.set('Autosave is OFF!')
        
        self.autosave_lab = tk.Label(self, textvariable=self.autosave_status)
        self.autosave_lab.grid(row=3, column=9, columnspan=2)
        
#        self.set_filter()
        
        
        self.create_widgets()
    
#    def proper_quit(self):
#        """
#        closes the tagger on quit if accidentally did not click stop (measurement) first
#        """
#        tagger.reset()
#        TimeTagger.freeTimeTagger(tagger)
#        plt.close('all')
#        self.master.destroy()
        
    def set_filter(self):
        
        ans = messagebox.askyesno(title="Filter Activation", message="Do you want to turn on the conditional filter?")
        
        if ans == True:        
            filtered = simpledialog.askstring(title="Channel(s) to filter (APD)", prompt="Channel #")
            triggers = simpledialog.askstring(title="Channel(s) to use as trigger (Pump)", prompt="Channel #")
                                              
            filter_chans = [int(i) for i in filtered.split()]
            trig_chans = [int(i) for i in triggers.split()]
            
            tagger.setConditionalFilter(trigger=trig_chans, filtered=filter_chans)
                
            print(tagger.getConditionalFilterTrigger())
                        
                                               
        else:
            print('Filter is off!')
        
    def filter_status(self):
        
        print('The filter is triggered with channels:')
        print(tagger.getConditionalFilterTrigger())

        print('The filter is filtering channels:')
        print(tagger.getConditionalFilterFiltered())                                   
        
   
    def create_widgets(self):
        """
        creates most widgets
        """
#        #quit button
#        self.quit = tk.Button(self, text="QUIT", fg="red",
#                              command=self.proper_quit)
#        self.quit.grid(row=6, column=9, columnspan=2, sticky='NESW')
        
        #other tagger commands
        self.reset_button = tk.Button(self, text='RESET TAGGER', command=self.reset_tagger)
        self.reset_button.grid(row=5, column=9, sticky='NESW')
        
        self.clear_button = tk.Button(self, text='CLEAR OVERFLOWS', command=self.clear_overflows)
        self.clear_button.grid(row=6, column=9, sticky='NESW')
        
        self.filter_button = tk.Button(self, text='Cond. Filter Status', command=self.filter_status)
        self.filter_button.grid(row=6, column=10, sticky='NESW')
        
        self.clear_data_button = tk.Button(self, text='CLEAR MEASUREMENT', command=self.clear_data)
        self.clear_data_button.grid(row=5, column=10)
        
#        self.optamize_commands = tk.Button(self, text='Enter Mirror Commands', command=self.run_commands)
#        self.optamize_commands.grid(row=6, column=9, sticky='NESW')
        
        self.pause_button = tk.Button(self, text='PAUSE', command=self.pause_measure)
        self.pause_button.grid(row=2, column=9, sticky='NESW')
        
        #measurement selection, start , stop and save buttons
        measure_lab = tk.Label(self, text='Select a type of measurement: ')
        measure_lab.grid(row=0, column=5)
        
        self.count_measurement = tk.Radiobutton(self, text='Counter', variable = self.measurement, value="Count", command=self.select_measure)
        self.count_measurement.grid(row=0, column=7)
        self.corr_measurement = tk.Radiobutton(self, text='Correlation', variable = self.measurement, value = 'Correlation', command=self.select_measure)
        self.corr_measurement.grid(row=0, column=9)
        self.life_measurement = tk.Radiobutton(self, text='Lifetime', variable = self.measurement, value='Lifetime', command=self.select_measure)
        self.life_measurement.grid(row=0, column=10)
        
        start_measure_button = tk.Button(self, text='START', command=self.start_measure)
        start_measure_button.grid(row=1, column=9, sticky='NESW')
        
        stop_measure_button = tk.Button(self, text='STOP/SWITCH', command=self.stop_measure)
        stop_measure_button.grid(row=4, column=9, sticky='NESW', columnspan=2)
        
        #saving data
        save_button = tk.Button(self, text='SAVE', command=self.save_data)
        save_button.grid(row=2, column=10, sticky='NESW')
        
        save_lab = tk.Label(self, text='Enter a filename: ')
        save_lab.grid(row=7, column=9)
        
        self.temp_name = strftime("%Y%m%d-%H%M%S")
        
        self.dir_name = strftime("%Y%m%d")
    
        self.filename = tk.Entry(self, width=20)
        self.filename.insert(END, self.temp_name)
        self.filename.grid(row=7, column=10)
        
        #plotting 
        plot_button = tk.Button(self, text='PLOT', command=self.plotting)
        plot_button.grid(row=1, column=10, sticky='NESW')
        
        #select test signal or real signal (ie from APD or not)
        self.select_test = tk.BooleanVar()
        self.select_test.set(False)
        self.select_test_button = tk.Checkbutton(self, text='Select Testing Signals', variable=self.select_test, command=lambda:self.choose_test_real())
        self.select_test_button.grid(row=1, column=0)
        
        self.select_real = tk.BooleanVar()
        self.select_real.set(False)
        self.select_real_button = tk.Checkbutton(self, text='Select Real Signals', variable=self.select_real, command=lambda:self.choose_test_real())
        self.select_real_button.grid(row=1, column=1)
        
    def reset_tagger(self):
        tagger.reset()
        self.stop_measure()
        print('Tagger has been reset!')
        
    def clear_overflows(self):
        num_over = tagger.getOverflowsAndClear()
        print('# of overflows = '+str(num_over))
              
    def clear_data(self):
        
        if self.measurement.get() == 'Count':
            self.count.clear()
            
        elif self.measurement.get() == 'Correlation':
            self.corr.clear()
            self.corr_count.clear()
            
        elif self.measurement.get() == 'Lifetime':
            self.lifetime.clear()
            
        print('Data cleared!')
        print('Ready for next measurement')
        
#        
#    def run_commands(self):
#        print('Use list_all_commands() to see all accessible commands')
#        
#        com = simpledialog.askstring(title='Run Command', prompt='Enter a command from mirrorcommands.py ')
#        
#        if com == None:
#            com = ''
#        
#        if com != '':
#            exec(com)
#            
#        else:
#            print('Enter something!')
#        
        
    def choose_test_real(self):
        """
        shows or deletes the widgets for either the test signal or the real signal
        
        error handling due to the logic not working exactly as intended (ie doesnt run every time a radiobutton is checked)
        so the False-False case runs if both are not there. However if one measurement hasnt been selected yet then 
        an AttributeError is raised saying the program cant forget a widget that never existed hence it only runs the one without an error
        """
        
        if self.select_real.get() == True:
            if self.select_test.get() == False:
                self.set_triggers()
                self.status.set("Real signal has been selected.")
                print('Triggers must be 0=<V<=2.5')
            
        elif self.select_test.get() == True:
            if self.select_real.get() == False:
                self.testing_signal()
                self.status.set("Testing signal has been selected.")
                print('Built-in test signal (~0.8 to 0.9 MHz)')
        
        elif self.select_real.get() == True:
            if self.select_test.get() == True:

#                #add removing their respective widgets
                
                print("Double True")
                #doesnt run
                
        elif self.select_real.get() == False:
            if self.select_test.get() == False:
                
                try:
                    self.remove_triggers()
                    self.status.set("Please select 'Test' or 'Real' signals then choose a measurement...")
                    
                except AttributeError:
                    pass
                
                try:
                    self.remove_testing()
                    self.status.set("Please select 'Test' or 'Real' signals then choose a measurement...")
                    
                except AttributeError:
                    pass
                
        else:
            self.status.set("If both types of signals are checked simultaneously, please restart the program.")
            print("Reached")
                
        
    def remove_triggers(self):
        """
        removes the widgets associated with the real signal
        """
        
        self.trigger_lab.grid_forget()
        self.init_tagger.grid_forget()
        self.used_channels.grid_forget()
        self.more_tagger_params.grid_forget()
        self.see_tagger_params.grid_forget()
        
        self.rC1.grid_forget()
        self.rC1_lab.grid_forget()
        
        self.rC2.grid_forget()
        self.rC2_lab.grid_forget()
        
        self.rC3.grid_forget()
        self.rC3_lab.grid_forget()
        
        self.rC4.grid_forget()
        self.rC4_lab.grid_forget()
        
        self.rC5.grid_forget()
        self.rC5_lab.grid_forget()
        
        self.rC6.grid_forget()
        self.rC6_lab.grid_forget()
        
        self.rC7.grid_forget()
        self.rC7_lab.grid_forget()
        
        self.rC8.grid_forget()
        self.rC8_lab.grid_forget()
        
    def set_tagger(self, channels):
        """
        sets the trigger levels for each used channel for a real signal  

        """
        list_of_volts = [float(self.rC1.get()), float(self.rC2.get()), float(self.rC3.get()), float(self.rC4.get()),
                         float(self.rC5.get()), float(self.rC6.get()), float(self.rC7.get()), float(self.rC8.get())]
        
        list_of_volts = ["%.2f" % i for i in list_of_volts]
        
        used = [int(i) for i in channels.split()]
        
        
        for i in used:

            tagger.setTriggerLevel(i,float(list_of_volts[i-1]))
        
        print('Triggers are set!')
        
    def set_more_params(self):
        """
           has the ability to change dead time and delay for each used channel 
        """
        chan = [int(i) for i in self.used_channels.get().split()]


        """
        DEFAULTS FOR DELAY AND DEAD TIME
        SET FOR ALL CHANNELS AT ONCE
        """
        for c in chan:
            delay = simpledialog.askinteger(title="Delay for channel "+str(c), prompt="Delay in ps:", initialvalue=0)
            dead_time = simpledialog.askinteger(title="Dead time for channel "+str(c), prompt="Dead time in ps:", initialvalue=6000)
    
            
            tagger.setInputDelay(c, delay)
            tagger.setDeadtime(c, dead_time)
         
        print('Delay and dead time set!')
        
    def check_tagger_params(self):
        chan = [int(i) for i in self.used_channels.get().split()]
        
        for c in chan:
            print('*******')
            print('For channel '+str(c))
            print('Trigger voltage (V): '+str(tagger.getTriggerLevel(c)))
            print('Delay (ps): '+str(tagger.getInputDelay(c)))
            print('Dead time (ps): '+str(tagger.getDeadtime(c)))
            print('*******')
    
    def set_triggers(self):
        """
        sets the real signal variables and widgets
        trigger voltages for real signal (rising edge only for now)
        
        TODO
        all channels (falling edge too)?
        """
        
        self.used_channels = tk.Entry(self, width=5)
        self.used_channels.insert(END, 1)
        self.used_channels.grid(row=2, column = 4,  sticky='NESW')
        
        self.init_tagger = tk.Button(self, text='Set Channel Triggers', command=lambda:self.set_tagger(self.used_channels.get()))
        self.init_tagger.grid(row=2, column=3,  sticky='NESW')
                
        self.trigger_lab = tk.Label(self, text='Enter trigger voltages for each channel (in V)')
        self.trigger_lab.grid(row=2, column =0, columnspan=2)
        
        self.more_tagger_params = tk.Button(self, text='More Tagger Parameters', command=self.set_more_params)
        self.more_tagger_params.grid(row=2, column=5, sticky='NESW')
        
        self.see_tagger_params = tk.Button(self, text='See All Set Tagger Parameters', command=self.check_tagger_params)
        self.see_tagger_params.grid(row=1, column=5, sticky='NESW')
        
        """
        ALL INSERT LINES ARE DEFAULTS FOR THE CHANNEL TRIGGERS
        """
        
        self.rC1 = tk.Entry(self, width=5)
        self.rC1.insert(END, 1.5)
        self.rC1.grid(row=3, column=1)
        self.rC1_lab = tk.Label(self, text='Channel 1 ')
        self.rC1_lab.grid(row=3, column=0)
        
        self.rC2 = tk.Entry(self, width=5)
        self.rC2.insert(END, 1.5)
        self.rC2.grid(row=4, column=1)        
        self.rC2_lab = tk.Label(self, text='Channel 2 ')
        self.rC2_lab.grid(row=4, column=0)
        
        self.rC3 = tk.Entry(self, width=5)
        self.rC3.insert(END, 1.5)
        self.rC3.grid(row=3, column=3)        
        self.rC3_lab = tk.Label(self, text='Channel 3 ')
        self.rC3_lab.grid(row=3, column=2)
        
        self.rC4 = tk.Entry(self, width=5)
        self.rC4.insert(END, 1.5)
        self.rC4.grid(row=4, column=3)
        self.rC4_lab = tk.Label(self, text='Channel 4 ')
        self.rC4_lab.grid(row=4, column=2)
        
        self.rC5 = tk.Entry(self, width=5)
        self.rC5.insert(END, 1.5)
        self.rC5.grid(row=3, column=5)
        self.rC5_lab = tk.Label(self, text='Channel 5 ')
        self.rC5_lab.grid(row=3, column=4)
        
        self.rC6 = tk.Entry(self, width=5)
        self.rC6.insert(END, 1.5)
        self.rC6.grid(row=4, column=5)
        self.rC6_lab = tk.Label(self, text='Channel 6 ')
        self.rC6_lab.grid(row=4, column=4)
        
        self.rC7 = tk.Entry(self, width=5)
        self.rC7.insert(END, 1.5)
        self.rC7.grid(row=3, column=7)
        self.rC7_lab = tk.Label(self, text='Channel 7 ')
        self.rC7_lab.grid(row=3, column=6)
        
        self.rC8 = tk.Entry(self, width=5)
        self.rC8.insert(END, 1.5)
        self.rC8.grid(row=4, column=7)
        self.rC8_lab = tk.Label(self, text='Channel 8 ')
        self.rC8_lab.grid(row=4, column=6)

    def remove_testing(self):
        """
        removes the widgets associated with the testing signals
        """
        self.b1.grid_forget()
        self.b2.grid_forget()
        self.b3.grid_forget()
        self.b4.grid_forget()
        self.b5.grid_forget()
        self.b6.grid_forget()
        self.b7.grid_forget()
        self.b8.grid_forget()
        

    def testing_signal(self):        
        """
        creates variables and widgets associated with the test signals
        """
        #test signal selection checkbuttons
        self.channel1 = tk.BooleanVar()
        self.b1 = tk.Checkbutton(self, text='Activate Channel 1', variable=self.channel1, command=lambda:self.activate_test(1))
        self.b1.grid(row=3, column=0)

        
        self.channel2 = tk.BooleanVar()
        self.b2 = tk.Checkbutton(self, text='Activate Channel 2', variable=self.channel2, command=lambda:self.activate_test(2))
        self.b2.grid(row=4, column=0)

        
        self.channel3 = tk.BooleanVar()
        self.b3 = tk.Checkbutton(self, text='Activate Channel 3', variable=self.channel3, command=lambda:self.activate_test(3))
        self.b3.grid(row=3, column=1)
        
        
        self.channel4 = tk.BooleanVar()
        self.b4 = tk.Checkbutton(self, text='Activate Channel 4', variable=self.channel4, command=lambda:self.activate_test(4))
        self.b4.grid(row=4, column=1)

        
        self.channel5 = tk.BooleanVar()
        self.b5 = tk.Checkbutton(self, text='Activate Channel 5', variable=self.channel5, command=lambda:self.activate_test(5))
        self.b5.grid(row=3, column=4)

        
        self.channel6 = tk.BooleanVar()
        self.b6 = tk.Checkbutton(self, text='Activate Channel 6', variable=self.channel6, command=lambda:self.activate_test(6))
        self.b6.grid(row=4, column=4)

        
        self.channel7 = tk.BooleanVar()
        self.b7 = tk.Checkbutton(self, text='Activate Channel 7', variable=self.channel7, command=lambda:self.activate_test(7))
        self.b7.grid(row=3, column=5)

        
        self.channel8 = tk.BooleanVar()
        self.b8 = tk.Checkbutton(self, text='Activate Channel 8', variable=self.channel8, command=lambda:self.activate_test(8))
        self.b8.grid(row=4, column=5)

        
    def select_measure(self):
        """
        control of the selection meassurement radio buttons
        
        note: choosing one while the other is already pressed causes some weird behaviour. Best to click stop/switch first
        
        """
        
        
        """
        DEFAULTS FOR THE MEASUREMENTS
        """
        self.default_count = ['1 2', '1e12', '100']
        self.default_corr = ['1', '2', '1', '100', '1e12', '100']
        self.default_life = ['1', '2', '100', '20', '1e12', '1000']
        
#        self.previous_count = [self.num_channel.get(), self.bin_width1.get(), self.num_values.get()]
#        self.previous_corr = [self.chan1.get(), self.chan2.get(), self.resolution.get(), self.delay.get(), self.corr_count_bin.get(), self.corr_count_num_vals.get()]
#        self.previous_life = [self.life_click.get(), self.life_start.get(), self.life_binwidth.get(), self.life_total.get(), self.life_count_bin.get(), self.life_count_num_vals.get()]
            
        
        
        if self.measurement.get() == "Count":
            print("Counter has been selected")
            self.status.set("Counter has been selected. Please enter the desired parameters then START")
            
            try:
                num_c = self.previous_count[0]
                bin1 = self.previous_count[1]
                num_v = self.previous_count[2]
                
            except AttributeError:
                num_c = self.default_count[0]
                bin1 = self.default_count[1]
                num_v = self.default_count[2]
            
            
            self.num_channel_lab = tk.Label(self, text='Channels to use: ')
            self.num_channel_lab.grid(row=5, column=0)
            self.num_channel = tk.Entry(self, width=10)
#            self.num_channel.insert(END, '1 2')
            self.num_channel.insert(END, num_c)
            self.num_channel.grid(row=5, column = 1)
                      
            self.bin_width_lab1 = tk.Label(self, text='Bin width (ps): ')
            self.bin_width_lab1.grid(row=5, column=2)
            self.bin_width1 = tk.Entry(self, width=10)
#            self.bin_width1.insert(END, '1e12')
            self.bin_width1.insert(END, bin1)
            self.bin_width1.grid(row=5, column = 4)
            
            self.num_values_lab = tk.Label(self, text='Number of values: ')
            self.num_values_lab.grid(row=5, column=5)
            self.num_values = tk.Entry(self, width=10)
#            self.num_values.insert(END, '100')
            self.num_values.insert(END, num_v)
            self.num_values.grid(row=5, column = 6)
            
            
            
        elif self.measurement.get() == "Correlation":
            print("Correlation has been selected")
            self.status.set("Correlation has been selected. Please enter the desired parameters then START")
            
            try:
                c1 = self.previous_corr[0]
                c2 = self.previous_corr[1]
                res = self.previous_corr[2]
                de = self.previous_corr[3]
                ccb = self.previous_corr[4]
                ccnv = self.previous_corr[5]
                
            except AttributeError:
                c1 = self.default_corr[0]
                c2 = self.default_corr[1]
                res = self.default_corr[2]
                de = self.default_corr[3]
                ccb = self.default_corr[4]
                ccnv = self.default_corr[5]
            
            self.chan1_lab = tk.Label(self, text='First channel: ')
            self.chan1_lab.grid(row=5, column=0)
            self.chan1 = tk.Entry(self, width=10)
#            self.chan1.insert(END, '1')
            self.chan1.insert(END, c1)
            self.chan1.grid(row=5, column=1)
            
            self.chan2_lab = tk.Label(self, text='Second channel: ')
            self.chan2_lab.grid(row=5, column=3)
            self.chan2 = tk.Entry(self, width=10)
#            self.chan2.insert(END, '2')
            self.chan2.insert(END, c2)
            self.chan2.grid(row=5, column=4)
                      
#            self.bin_window_lab = tk.Label(self, text='Time window (in ps): ')
#            self.bin_window_lab.grid(row=5, column=5)
#            self.bin_window = tk.Entry(self, width=10)
#            self.bin_window.insert(END, '100')
#            self.bin_window.grid(row=5, column=6)
            
            #            self.num_bins_lab = tk.Label(self, text='Number of bins: ')
#            self.num_bins_lab.grid(row=6, column=0)
#            self.num_bins = tk.Entry(self, width=10)
#            self.num_bins.insert(END, '1000')
#            self.num_bins.grid(row=6, column=1)
            
            self.delay_lab = tk.Label(self, text='Range (in ns)')
            self.delay_lab.grid(row=6, column=3)
            self.delay = tk.Entry(self, width=10)
#            self.delay.insert(END, '1')
            self.delay.insert(END, de)
            self.delay.grid(row=6, column=4)
         

            self.resolution_lab = tk.Label(self, text='Bin width (in ps)')
            self.resolution_lab.grid(row=6, column=0)
            self.resolution = tk.Entry(self, width=10)
#            self.resolution.insert(END, '100')
            self.resolution.insert(END, res)
            self.resolution.grid(row=6, column=1)
             
            self.corr_count_bin_lab = tk.Label(self, text='Counter bin width: ')
            self.corr_count_bin_lab.grid(row=5, column=5)
            self.corr_count_bin = tk.Entry(self, width=10)
#            self.corr_count_bin.insert(END, '1e12')
            self.corr_count_bin.insert(END, ccb)
            self.corr_count_bin.grid(row=5, column=6)
                  
            self.corr_count_num_vals_lab = tk.Label(self, text='Counter # values: ')
            self.corr_count_num_vals_lab.grid(row=6, column=5)
            self.corr_count_num_vals = tk.Entry(self, width=10)
#            self.corr_count_num_vals.insert(END, '100')
            self.corr_count_num_vals.insert(END, ccnv)
            self.corr_count_num_vals.grid(row=6, column=6)

            self.corr_count_c1 = tk.StringVar()
            self.corr_count_c1.set("")
            
            self.corr_count_c2 = tk.StringVar()
            self.corr_count_c2.set("")   
                      
            self.corr_count_lab = tk.Label(self, text='Maximum data point value and counts per used channel : ')
            self.corr_count_lab.grid(row=10, column=0, columnspan=2)
            
            self.corr_count_c1_lab = tk.Label(self, textvariable=self.corr_count_c1)
            self.corr_count_c1_lab.grid(row=10, column=6)
            
            self.corr_count_c2_lab = tk.Label(self, textvariable=self.corr_count_c2)
            self.corr_count_c2_lab.grid(row=10, column=7)
            
        
        elif self.measurement.get() == 'Lifetime':
            print('Lifetime has been selected')
            self.status.set("Lifetime has been selected. Please enter the desired parameters then START")
            
           
            try:
                cl = self.previous_life[0]
                st = self.previous_life[1]
                lbin = self.previous_life[2]
                lt = self.previous_life[3]
                lcb = self.previous_life[4]
                lcnv = self.previous_life[5]
                
            except AttributeError:
                cl = self.default_life[0]
                st = self.default_life[1]
                lbin = self.default_life[2]
                lt = self.default_life[3]
                lcb = self.default_life[4]
                lcnv = self.default_life[5]
            
            
            self.life_click_lab = tk.Label(self, text='Click Channel (Trigger)')
            self.life_click_lab.grid(row=5, column=0)
            self.life_click = tk.Entry(self, width=10)
#            self.life_click.insert(END, '1')
            self.life_click.insert(END, cl)
            self.life_click.grid(row=5, column=1)
            
            self.life_start_lab = tk.Label(self, text='Start Channel (APD)')
            self.life_start_lab.grid(row=5, column=2)
            self.life_start = tk.Entry(self, width=10)
#            self.life_start.insert(END, '2')
            self.life_start.insert(END, st)
            self.life_start.grid(row=5, column=4)
            
            self.life_binwidth_lab = tk.Label(self, text='Bin width (ps)')
            self.life_binwidth_lab.grid(row=6, column=2)
            self.life_binwidth = tk.Entry(self, width=10)
#            self.life_binwidth.insert(END, '100')
            self.life_binwidth.insert(END, lbin)
            self.life_binwidth.grid(row=6, column=4)
            
            self.life_total_lab = tk.Label(self, text='Max life (ns)')
            self.life_total_lab.grid(row=6, column=0)
            self.life_total = tk.Entry(self, width=10)
#            self.life_total.insert(END, '20')
            self.life_total.insert(END, lt)
            self.life_total.grid(row=6, column=1)
            
            self.life_count_bin_lab = tk.Label(self, text='Counter bin width: ')
            self.life_count_bin_lab.grid(row=5, column=5)
            self.life_count_bin = tk.Entry(self, width=10)
#            self.life_count_bin.insert(END, '1e12')
            self.life_count_bin.insert(END, lcb)
            self.life_count_bin.grid(row=5, column=6)
                  
            self.life_count_num_vals_lab = tk.Label(self, text='Counter # values: ')
            self.life_count_num_vals_lab.grid(row=6, column=5)
            self.life_count_num_vals = tk.Entry(self, width=10)
#            self.life_count_num_vals.insert(END, '1000')
            self.life_count_num_vals.insert(END, lcnv)
            self.life_count_num_vals.grid(row=6, column=6)
            
            
            
            self.life_count_c1 = tk.StringVar()
            self.life_count_c1.set("")
            
            self.life_count_c2 = tk.StringVar()
            self.life_count_c2.set("")   
                      
            self.life_count_lab = tk.Label(self, text='Maximum data point value and counts per used channel : ')
            self.life_count_lab.grid(row=10, column=0, columnspan=2)
            
            self.life_count_c1_lab = tk.Label(self, textvariable=self.life_count_c1)
            self.life_count_c1_lab.grid(row=10, column=4)
            
            self.life_count_c2_lab = tk.Label(self, textvariable=self.life_count_c2)
            self.life_count_c2_lab.grid(row=10, column=5)
         
#            self.life_num_bins_lab = tk.Label(self, text='# of bins')
#            self.life_num_bins_lab.grid(row=6, column=0)
#            self.life_num_bins = tk.Entry(self, width=10)
#            self.life_num_bins.insert(END, '100')
#            self.life_num_bins.grid(row=6, column=1)
            
        
        else:
            print("Choose a measurement type")
    
    
    def update_out(self):
        """
        used to continuously update the label for the counts
            on either the counter measurement or the correlation coutner
        """
        if self.measurement.get() == 'Count':
            
            if len(self.channels) >= 2:
                lab = self.count.getData()[0][-1]
                lab2 = self.count.getData()[1][-1]
                self.out.set('Counts C1: '+str(lab))
                self.out2.set('Counts C2: '+str(lab2))
                
            else:
                lab = self.count.getData()[0][-1]
                self.out.set('Counts C1: '+str(lab))

            #these are counts/bin, total counts is the (numerical) integral of the resulting curve
            #however if bin is 1e12 ps = 1s then they're counts/s
            
        elif self.measurement.get() == 'Correlation':
            dat = self.corr.getData()
            lab = max(dat)
            
#            dat_norm = self.corr.getDataNormalized()
#            lab_norm = max(dat_norm)
            self.out.set("Max of raw : "+str(lab))
#            self.out2.set('Max of norm: '+"%.2f" % lab_norm)
            
            
            c1 = self.corr_count.getData()[0][-1]
            c2 = self.corr_count.getData()[1][-1]

            self.corr_count_c1.set('Counts C1: '+str(c1))
            self.corr_count_c2.set('Counts C2: '+str(c2))

        
        elif self.measurement.get() == 'Lifetime':
            lab = max(self.lifetime.getData())
            
            self.out.set('Max of lifetime: '+str(lab))
            
            c1 = self.life_count.getData()[0][-1]
            c2 = self.life_count.getData()[1][-1]
            
            self.life_count_c1.set('Counts C1: '+str(c1))
            self.life_count_c2.set('Counts C2: '+str(c2))
        
        if self.status.get() != 'PAUSED':
#            self.out.set(str(lab))
            print("Running...")
        
        self.timer_end = time()
        delta_time = self.timer_end - self.timer_start
        
        if delta_time > self.autosave_span*60:
            print('Autosaved at '+strftime("%Y%m%d-%H%M%S"))
            self.save_data()
            self.timer_start = time()
        
        
        #calls itself after 1s to continually update
        self._job = self.after(1000, self.update_out)
      
     
    def start_measure(self):
        """
        controls the start of the measurement
    
        
        for count, only the counts on the first two selected channels are shown
        for corr, max is shown
        for corr_count, the two selected channel counts are shown 
        """
        
        print('Measurement started')
        self.up = tk.BooleanVar()
        self.up.set("True")
        
        self.autosave_status.set('Autosave is ON!')
    
        self.timer_start = time()
        
        if self.measurement.get() == "Count":

            try:
                self.count.start()
                self.status.set('Counter running...')
#                print('starts a count')
            except AttributeError:
                
                
                self.channels = [int(i) for i in self.num_channel.get().split()]
#                print(self.channels)
                                
                self.count = TimeTagger.Counter(tagger, channels=self.channels, binwidth=int(float(self.bin_width1.get())), n_values=int(float(self.num_values.get())))
                print('Counter running...')
                self.status.set("Counter running...")
    
                if len(self.channels) >= 2:
                    dat = self.count.getData()[0][-1]
                    dat2 = self.count.getData()[1][-1]
                    self.out.set(str(dat))
                    self.out2.set(str(dat2))
                else:
                    dat = self.count.getData()[0][-1]
                    self.out.set(str(dat))
    
                
                self.update_out()
          
            #plotting is done seperatly with a different button
            
        elif self.measurement.get() == 'Correlation':   
       
            try:
                self.corr.start()
                self.corr_count.start()
                self.status.set('Correlation running...')
            except AttributeError:
                
                
                num_bins_corr = (float(self.delay.get())*1000)/float(self.resolution.get())
                
                self.corr = TimeTagger.Correlation(tagger, channel_1=int(self.chan1.get()), channel_2=int(self.chan2.get()),
                                                    binwidth=int(self.resolution.get()), n_bins=int(num_bins_corr))
    
                print('Correlation running...')
                self.status.set("Correlation running...")
                
                self.corr_count = TimeTagger.Counter(tagger, channels=[int(self.chan1.get()), int(self.chan2.get())],
                                                    binwidth=int(float(self.corr_count_bin.get())), n_values=int(self.corr_count_num_vals.get()))
                
                
                dat_c1 = self.corr_count.getData()[0][-1]
                dat_c2 = self.corr_count.getData()[1][-1]
                self.corr_count_c1.set(str(dat_c1))
                self.corr_count_c2.set(str(dat_c2))
                
                                  
                dat = self.corr.getData()
    
                lab = max(dat)
    
                self.out.set('Max value of raw correlation: '+str(lab))
                
                self.update_out()
                
            #plotting is done seperatly with a different button   

        elif self.measurement.get() == 'Lifetime':
            
            try:
                self.lifetime.start()
                self.life_count.start()
                self.status.set('Lifetime running...')
            except AttributeError:
                
                
                num_bins_life = (float(self.life_total.get())*1000)/float(self.life_binwidth.get())
                
                
                self.lifetime = TimeTagger.Histogram(tagger, click_channel=int(self.life_click.get()), start_channel=int(self.life_start.get()),
                                                     binwidth=int(float(self.life_binwidth.get())), n_bins=int(num_bins_life))
                
                print('Lifetime running...')
                self.status.set("Lifetime running...")
    
                self.chans = [int(self.life_click.get()), int(self.life_start.get())]
    
                self.life_count = TimeTagger.Counter(tagger, channels=self.chans, binwidth=int(float(self.life_count_bin.get())),
                                                     n_values=int(self.life_count_num_vals.get()))            
                
                dat = self.lifetime.getData()
                
                max_life = max(dat)
                
                self.out.set('Max value of lifetime: '+str(max_life))
                
                self.update_out()
       
            #plotting is done seperatly with a different button
        
        
        else:
            print('Please select a measurement type to start')
            

        
    def plotting(self):
        """
        plotting function. Creates and animates the plots.
        Note for animation to work and if using spyder, need to have graphics be 'Automatic'
        
        Go to Tools -> Preferences -> IPython console -> Select 'Graphics' Tab -> Select 'Automatic' as backend
            if you want inline for some reason, select 'Inline' instead of automatic
            this will make the plots appear in the console window of spyder but will not be animated
        """
        print('Plotting...')
        print('To save plots, click the save button on the pop-up.')
        
        #animation functions for each type of measurement
        def animate_count(i):
            #for hopefully any number of channels
            for index, line in enumerate(lines_count):
                line.set_ydata(self.count.getData()[index])
          
            #rescales axes automatically
            axs_count.relim()
            axs_count.autoscale_view(True, True, True)
            
            return lines_count
        
            
        def animate_corr(i):
            """
            any other non plot related code, like if statement, crashes the console
            """
            dat = self.corr.getData()
            
            
#            index = self.corr.getIndex()/1e3
            

#            dat_norm = self.corr.getDataNormalized()
            
#            line_corr.set_offsets(np.c_[index, dat])
            line_corr.set_ydata(dat)
#            line_corr_norm.set_ydata(dat_norm)
        
            #updates the maximum on each plot            
            t1.set_text('Max: '+str(max(dat)))
#            t2.set_text('Max: '+ "%.2f" % max(dat_norm))
            
            #rescales axes automatically
            axs_corr.relim()
            axs_corr.autoscale_view(True,True,True)
            axs_corr.set_ylim((0, None), auto=True)
            #new line to fix x-axis scaling
#            axs_corr.set_xlim((original_limits[0], original_limits[1]), auto=False)
            
#            axs_corr[1].relim()
#            axs_corr[1].autoscale_view(True,True,True)
#            axs_corr[1].set_ylim((0, None), auto=True)

           
#            return line_corr, line_corr_norm,
            return line_corr,
        
    
        def animate_life(i):
            
            line_life.set_ydata(self.lifetime.getData())
            
            axs_life.relim()
            axs_life.autoscale_view(True,True,True)
            
            return line_life,
        
        
        if self.measurement.get() == 'Count':
            
            fig_count, axs_count = plt.subplots()
                  
            lines_count = []
            j = 0
            #plots in s
            for i in self.channels:
                lines_count.append(axs_count.plot(self.count.getIndex()/1e12, self.count.getData()[j], label='Channel '+str(i))[0])
                j+=1
            
            plt.title('Animated Counts')
            plt.xlabel('Time (s) ')
            plt.ylabel('Counts')
            plt.legend(loc=4)
            
            
            #this needs to be global scope variable to work 
            self.ani_count = animation.FuncAnimation(fig_count, animate_count, interval=10, blit=False, save_count=50)
            
            plt.show()

             
        elif self.measurement.get() == 'Correlation':
           
            fig_corr, axs_corr = plt.subplots()
            #(1,2, sharex=True, figsize=(10,5))
            
#            fig_corr.suptitle('Animated Correlation')

            dat = self.corr.getData()
            index = self.corr.getIndex()/1e3
#            original_limits = [index[0], index[-1]]
            
#            dat_norm = self.corr.getDataNormalized()
            
     
            #plots in ns
            line_corr, = axs_corr.plot(index, dat)
#            line_corr_norm, = axs_corr[1].plot(self.corr.getIndex()/1e3, dat_norm)
            
            #titles
            axs_corr.set_title('Animated Correlation - Raw')
            axs_corr.set_xlabel('Time (ns) ')
            axs_corr.set_ylabel('Coincidinces')
#            axs_corr[1].set_title('Normalized')
#            axs_corr[1].set_xlabel('Time (ns) ')
#            axs_corr[1].set_ylabel('Coincidinces')
            
#            fig_corr.text(0.51, 0.04, 'Time (ns)', ha='center')
#            fig_corr.text(0.04, 0.5, 'Coincidinces', va='center', rotation='vertical')
            
            #puts maximums on plots
            t1 = axs_corr.text(0.1,0.9, str(max(dat)),horizontalalignment='left',
                verticalalignment='top',
                transform=axs_corr.transAxes)
            
#            t2 = axs_corr[1].text(0.1,0.9, str(max(dat_norm)),horizontalalignment='left',
#                verticalalignment='top',
#                transform=axs_corr[1].transAxes)
                          
            self.ani_corr = animation.FuncAnimation(fig_corr, animate_corr, interval=10, blit=False, save_count=50)
            plt.show()
        
        elif self.measurement.get() == 'Lifetime':
            
            fig_life, axs_life = plt.subplots()
            
            #plots in ns
            line_life, = axs_life.plot(self.lifetime.getIndex()/1e3, self.lifetime.getData())
            
            plt.title('Animated Lifetime')
            plt.xlabel('Time (ns) ')
            plt.ylabel('Clicks')
            
            self.ani_life = animation.FuncAnimation(fig_life, animate_life, interval=10, blit=False, save_count=50)
            plt.show()
        
        else:
            print('Please select a measurement type to start before plotting it.')
     
    def pause_measure(self):
        """
        pauses a running measurement
        """
        
        self.status.set('PAUSED')
        
        if self.measurement.get() == 'Count':
            self.count.stop()
            
        elif self.measurement.get() == 'Correlation':
            self.corr.stop()
            self.corr_count.stop()
            
        elif self.measurement.get() == 'Lifetime':
            self.lifetime.stop()
            self.life_count.stop()
            
        else:
            print('Please start a measurement in order to pause it.')
        
    
    def stop_measure(self):
        """
        controls the stopping of a measurement

        """
        plt.close('all')
        print('Measurement stopped')
        self.status.set("Measurement stopped. Please save, quit or run another measurement.")
        
        self.autosave_status.set('Autosave is OFF!')
           
             
        try:
            if self.up.get() == True:
                self.after_cancel(self._job)
                self.up.set("False")
        except AttributeError:
            pass
        
        if self.measurement.get() == 'Count':
            
            self.previous_count = [self.num_channel.get(), self.bin_width1.get(), self.num_values.get()]
                        
            self.num_channel_lab.grid_forget()
            self.num_channel.grid_forget()
            self.bin_width_lab1.grid_forget()
            self.bin_width1.grid_forget()
            self.num_values_lab.grid_forget()
            self.num_values.grid_forget()
            
            try:
                del self.count
            except AttributeError:
                pass
                      
        elif self.measurement.get() == 'Correlation':
                
            self.previous_corr = [self.chan1.get(), self.chan2.get(), self.resolution.get(), self.delay.get(), self.corr_count_bin.get(), self.corr_count_num_vals.get()]
            
            self.chan1.grid_forget()
            self.chan1_lab.grid_forget()
            self.chan2.grid_forget()
            self.chan2_lab.grid_forget()
            
#            self.bin_window.grid_forget()
#            self.bin_window_lab.grid_forget()
#    
#            self.num_bins.grid_forget()
#            self.num_bins_lab.grid_forget()
            
            self.resolution_lab.grid_forget()
            self.resolution.grid_forget()
            
            self.delay.grid_forget()
            self.delay_lab.grid_forget()
            
            self.corr_count_lab.grid_forget()
            self.corr_count_c1_lab.grid_forget()
            self.corr_count_c2_lab.grid_forget()
            
            self.corr_count_bin_lab.grid_forget()
            self.corr_count_bin.grid_forget()
            self.corr_count_num_vals_lab.grid_forget()
            self.corr_count_num_vals.grid_forget()
            
            try:
                del self.corr
                del self.corr_count
            except AttributeError:
                pass
            
        elif self.measurement.get() == 'Lifetime':
            
            
            self.previous_life = [self.life_click.get(), self.life_start.get(), self.life_binwidth.get(), self.life_total.get(), self.life_count_bin.get(), self.life_count_num_vals.get()]
            
            self.life_binwidth.grid_forget()
            self.life_binwidth_lab.grid_forget()
            
            self.life_click.grid_forget()
            self.life_click_lab.grid_forget()
            
#            self.life_num_bins.grid_forget()
#            self.life_num_bins_lab.grid_forget()
            
            self.life_total.grid_forget()
            self.life_total_lab.grid_forget()
            
            self.life_start.grid_forget()
            self.life_start_lab.grid_forget()
            
            self.life_count_bin.grid_forget()
            self.life_count_bin_lab.grid_forget()
            
            self.life_count_num_vals.grid_forget()
            self.life_count_num_vals_lab.grid_forget()
            
            self.life_count_lab.grid_forget()
            self.life_count_c1_lab.grid_forget()
            self.life_count_c2_lab.grid_forget()
            
            try:
                del self.lifetime
                del self.life_count
            except AttributeError:
                pass
     
        else:
            print('You must have a measurement running in order to stop it.')
#        tagger.reset()
        
        #this shouldnt happen since that code is removed and the reset button exists
        print('Please restart the test signal if you change measurements')
        
        sleep(0.5)
        
        self.out.set("Waiting...")
        self.out2.set("")
        
        self.measurement.set("M")
            
    def save_data(self):
        """
        saves data with the given file name
        INDEX represents x-axis data
        DATA represents y-axis data
        
        Note: currently needs to click save while the measurement is running
        
        """
        
        print('saved data')
        hold = self.status.get()
        self.status.set("Measurement saved under given file name")
        print(self.status.get())
        #not showing up in status since change is quick but is appearing in console
        
        self.dir_name = strftime("%Y%m%d")
        
        if self.measurement.get() == 'Count':

            dat = self.count.getData()
            index = self.count.getIndex()/1e3
            
            script_dir = os.path.dirname(__file__)
            results_dir = os.path.join(script_dir, 'Tagger Data/Counts/'+self.dir_name+'/')
            
            if not os.path.isdir(results_dir):
                os.makedirs(results_dir)

            np.savetxt(results_dir+self.filename.get()+'-DATA.csv', dat, delimiter=',', fmt='%.4e')
            np.savetxt(results_dir+self.filename.get()+'-INDEX.csv', index, delimiter=',', fmt='%.4e')
            
            
        elif self.measurement.get() == 'Correlation':
            dat = self.corr.getData()
            index = self.corr.getIndex()
#            dat_norm = self.corr.getDataNormalized()
            
            script_dir = os.path.dirname(__file__)
            results_dir = os.path.join(script_dir, 'Tagger Data/Correlation/'+self.dir_name+'/')
            
            if not os.path.isdir(results_dir):
                os.makedirs(results_dir)
            
            np.savetxt(results_dir+self.filename.get()+'-raw-DATA.csv', dat, delimiter=',', fmt='%.4e')
            np.savetxt(results_dir+self.filename.get()+'-INDEX.csv', index, delimiter=',', fmt='%.4e')
#            np.savetxt(results_dir+self.filename.get()+'-norm-DATA.csv', dat_norm, delimiter=',', fmt='%.4e')
            
            np.savetxt(results_dir+self.filename.get()+'-corr-counts-DATA.csv', self.corr_count.getData(), delimiter=',', fmt='%.4e')
            np.savetxt(results_dir+self.filename.get()+'-corr-counts-INDEX.csv', self.corr_count.getIndex(), delimiter=',', fmt='%.4e')
            
        
        elif self.measurement.get() == 'Lifetime':
        
            dat = self.lifetime.getData()
            index = self.lifetime.getIndex()
            
            script_dir = os.path.dirname(__file__)
            results_dir = os.path.join(script_dir, 'Tagger Data/Lifetime/'+self.dir_name+'/')
            
            if not os.path.isdir(results_dir):
                os.makedirs(results_dir)
            
            np.savetxt(results_dir+self.filename.get()+'-DATA.csv', dat, delimiter=',', fmt='%.4e')
            np.savetxt(results_dir+self.filename.get()+'-INDEX.csv', index, delimiter=',', fmt='%.4e')
            
            np.savetxt(results_dir+self.filename.get()+'-life-count-DATA.csv', self.life_count.getData(), delimiter=',', fmt='%.4e')
            np.savetxt(results_dir+self.filename.get()+'-life-INDEX.csv', self.life_count.getIndex(), delimiter=',', fmt='%.4e')
            
            
            
        else:
            print('You must select a measurement and start it, if you want to save it.')
        self.status.set(hold)
    
        
    def activate_test(self, index):
        """
        controls the behavious of the test signal check boxes
        
        """
        if index == 1:
            if self.channel1.get() == True:
                tagger.setTestSignal(index, True)
                print('Channel '+str(index)+' is activated!')

        
            elif self.channel1.get() == False:
                tagger.setTestSignal(index, False)
                print('Channel '+str(index)+' is disabled!')
        
        if index == 2:        
            if self.channel2.get() == True:
                tagger.setTestSignal(index, True)
                print('Channel '+str(index)+' is activated!')
                
            elif self.channel2.get() == False:
                tagger.setTestSignal(index, False)
                print('Channel '+str(index)+' is disabled!')
        if index == 3:        
            if self.channel3.get() == True:
                tagger.setTestSignal(index, True)
                print('Channel '+str(index)+' is activated!')
          
            elif self.channel3.get() == False:
                tagger.setTestSignal(index, False)
                print('Channel '+str(index)+' is disabled!')
        if index == 4:
            
            if self.channel4.get() == True:
                tagger.setTestSignal(index, True)
                print('Channel '+str(index)+' is activated!')
                
            elif self.channel4.get() == False:
                tagger.setTestSignal(index, False)
                print('Channel '+str(index)+' is disabled!')
        
        if index == 5:
            if self.channel5.get() == True:
                tagger.setTestSignal(index, True)
                print('Channel '+str(index)+' is activated!')
                
            elif self.channel5.get() == False:
                tagger.setTestSignal(index, False)
                print('Channel '+str(index)+' is disabled!')
        
        if index == 6:
            if self.channel6.get() == True:
                tagger.setTestSignal(index, True)
                print('Channel '+str(index)+' is activated!')
                
            elif self.channel6.get() == False:
                tagger.setTestSignal(index, False)
                print('Channel '+str(index)+' is disabled!')
        
        if index == 7:
            if self.channel7.get() == True:
                tagger.setTestSignal(index, True)
                print('Channel '+str(index)+' is activated!')
                
            elif self.channel7.get() == False:
                tagger.setTestSignal(index, False)
                print('Channel '+str(index)+' is disabled!')
        
        if index == 8:
            if self.channel8.get() == True:
                tagger.setTestSignal(index, True)
                print('Channel '+str(index)+' is activated!')
                
            elif self.channel8.get() == False:
                tagger.setTestSignal(index, False)
                print('Channel '+str(index)+' is disabled!')

def on_quit():
    
#    tagger.reset()
#    TimeTagger.freeTimeTagger(tagger)
    plt.close('all')
    print('Tagger has quit!')
    root.destroy()


if __name__ == '__main__':
        
    root = tk.Tk()
    root.title('Time Tagger GUI')
    gui = tagger_gui(root)
    
    root.protocol("WM_DELETE_WINDOW", on_quit)
    root.mainloop()
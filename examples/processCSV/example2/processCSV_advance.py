# -*- coding: utf-8 -*-
"""
SiEPIC Analysis Package

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example: Advanced pplication of CSVanalysis to process an entire measurement set.
    In this example, a data set of GC measurements is processed
        1- Each data set is plotted
        2- All measurements are combined in one plot
        Peak transmission vs GDS coordinates are plotted
"""
#%%

import siepic_analysis_package as siap

import os, matplotlib
from scipy.interpolate import interp2d
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

dir_measurement = os.getcwd()+"\\sweepLaser"

dir_results = "measurement_summary"
cwd = os.getcwd()
path = os.path.join(cwd, dir_results)

now = datetime.now()
current_time = now.strftime("%H_%M_%S")
path += '_'+current_time
os.mkdir(path)
os.chdir(path)
devices = []
#%% 1- plot each device individually 
for subdir, dirs, files in os.walk(dir_measurement):
    for file in files:
        if file.endswith('.csv'):
            device = siap.analysis.processCSV(subdir+'\\'+file)
            device.plot(channels=[0], pwrRange=[-40, -15],
                        wavlRange=[1500, 1580], savepdf=False, savepng=False)
            devices.append(device)

#%% 2- overlay the plots of all devices

plt.figure(0)

for device in devices:
    fig = plt.plot(device.wavl, device.pwr[0], linewidth=.5)

plt.legend(loc=0)
plt.ylabel('Power (dBm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.ylim(-40,-15)
plt.xlim(1500, 1580)
plt.title("Overlay of all measurements (c-band)")
plt.savefig('overlay'+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

# %% 3 - plot peak transmission vs GDS coordinates
x_arr = []
y_arr = []
p_arr = []
for device in devices:
    x_arr.append(device.getGDS()[0])
    y_arr.append(device.getGDS()[1])
    p_arr.append(np.max(device.pwr[0]))

plt.figure(1)
plt.scatter(x_arr, y_arr, c = p_arr)
#plt.legend(loc=0)
plt.ylabel('Y (microns)')
plt.xlabel('X (microns)')
plt.colorbar()
plt.title("Peak transmission vs device coordinates")
plt.savefig('t_vs_gds'+'.pdf')
matplotlib.rcParams.update({'font.size': 10, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

# %%

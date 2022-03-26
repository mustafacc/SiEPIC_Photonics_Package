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
import sys
sys.path.append(r'C:\Users\musta\Documents\GitHub\SiEPIC_Photonics_Package')
import siepic_analysis_package as siap

import os, matplotlib
from scipy.interpolate import interp2d
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

dir_measurement = os.getcwd()+"\\data"

dir_results = "measurement_summary"
cwd = os.getcwd()
path = os.path.join(cwd, dir_results)

now = datetime.now()
current_time = now.strftime("%H_%M_%S")
path += '_'+current_time
os.mkdir(path)
os.chdir(path)

wavl_min = 1260
wavl_max = 1340
port = 1

devices = []
devices_ref = []
#%% 1- plot each device individually 
for subdir, dirs, files in os.walk(dir_measurement):
    for file in files:
        if file.endswith('.csv'):
            device = siap.analysis.processCSV(subdir+'\\'+file)
            #device.plot(channels=[port],
            #            wavlRange=[wavl_min, wavl_max], savepdf=False, savepng=False)

            if device.deviceID.startswith('ref_exLg0') or device.deviceID.startswith('ref_exLg1470'):
                devices_ref.append(device)
            else:
                devices.append(device)

#%% 2- overlay the plots of all devices

plt.figure()

threshold = -50
fails = 0
fails_ref = 0

# filter out failed devices
devices_modified = []
for device in devices:
    if max(device.pwr[port]) < threshold:
        fails = fails+1
    else:
        devices_modified.append(device)
    fig = plt.plot(device.wavl, device.pwr[port], linewidth=.5)
    

plt.legend(loc=0)
plt.ylabel('Power (dBm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.xlim(wavl_min, wavl_max)
plt.title("Overlay of all measurements (PWBs)")
plt.savefig('overlay'+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

plt.figure()

devices_ref_modified = []
for device in devices_ref:
    if max(device.pwr[port]) < threshold:
        fails_ref = fails_ref+1
    else:
        devices_ref_modified.append(device)
    fig = plt.plot(device.wavl, device.pwr[port], linewidth=.5)
    

plt.legend(loc=0)
plt.ylabel('Power (dBm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.xlim(wavl_min, wavl_max)
plt.title("Overlay of all measurements (Reference)")
plt.savefig('overlay_ref'+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

# %% 3 - plot peak transmission vs GDS coordinates
x_arr = []
y_arr = []
p_arr = []
for device in devices_ref:
    x_arr.append(device.getGDS()[0])
    y_arr.append(device.getGDS()[1])
    p_arr.append(np.max(device.pwr[port]))

plt.figure()
plt.scatter(x_arr, y_arr, c = p_arr)
#plt.legend(loc=0)
plt.ylabel('Y (microns)')
plt.xlabel('X (microns)')
plt.colorbar()
plt.title("Peak transmission vs device coordinates")
plt.savefig('t_vs_gds'+'.pdf')
matplotlib.rcParams.update({'font.size': 10, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

# %%

wavl = 1310
idx = 625


plt.figure()
for device in devices_modified:
    # find closest calibration shunt
    closest = 1E10
    for ref in devices_ref_modified:
        x_space = np.abs(device.getGDS()[0] - ref.getGDS()[0])
        y_space = np.abs(device.getGDS()[1] - ref.getGDS()[1])
        distance = x_space**2 + y_space**2
        if distance < closest:
            closest = distance
            ref_closest = ref
    
    # calibrate against the response
    device.pwr_calib = np.array(device.pwr[port]) - np.array(ref_closest.pwr[port])

    fig = plt.plot(device.wavl, -device.pwr_calib/4, linewidth=.5)

plt.legend(loc=0)
plt.ylabel('Insertion loss (dB/per PWB)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.xlim(wavl_min, wavl_max)
plt.ylim(-5,15)
plt.title("Calibrated insertion loss of a PWB")
plt.savefig('overlay_IL'+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

IL_tot = 0
loss = []
for device in devices_modified:
    IL_tot = IL_tot + device.pwr_calib[idx]/4
    loss.append(device.pwr_calib[idx]/4)
IL_tot = IL_tot/np.size(devices_modified)


# %%
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
langs = ['C', 'C++', 'Java', 'Python', 'PHP']
students = [23,17,35,29,12]
ax.bar(langs,students)
plt.show()

# %%

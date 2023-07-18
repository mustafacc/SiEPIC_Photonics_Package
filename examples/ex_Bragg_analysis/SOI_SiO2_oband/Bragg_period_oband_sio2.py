"""
SiEPIC Analysis Package 

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example:    Application of SiEPIC_AP analysis functions
            Process data of various contra-directional couplers (CDCs)
            Extract the period and bandwidth from a set of devices
"""
#%%
import siepic_analysis_package as siap
import matplotlib.pyplot as plt
import matplotlib, os
import numpy as np
fname_data = r"data\\WF112ULUL" # filename containing the desired data
device_prefix = "PCM_Bragg_O_800N"
device_suffix = "nmPeriod350nmW15nmdW0Apo"
port_drop = 1 # port in the measurement set containing the drop port data
port_thru = 1 # port in the measurement set containing the through port data
def getDeviceParameter(deviceID, devicePrefix, deviceSuffix = ''):
    """Find the variable parameter of a device based on the ID
    
    IMPORTANT: "removeprefix" and "removesuffix" are only available
        for Python >= 3.9

    Args:
        deviceID (string): ID of the device.
        devicePrefix (string): Prefix string in the device that's before the variable parameter
        deviceSuffix (string): Any additional fields in the suffix of a device that need to be stripped, optional.

    Returns:
        parameter (float): variable parameter of the device (unit based on whats in the ID)
    """
    parameter = float(deviceID.removeprefix(devicePrefix).removesuffix(deviceSuffix))
    return parameter

#%% crawl available data to choose files from the dataset
tol = 4 # calibrate_envelope parameter
N_seg = 325 # calibrate_envelope parameter
period = []
BW = []
WL = []
devices = []
for root, dirs, files in os.walk(fname_data):
    if os.path.basename(root).startswith(device_prefix):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                device = siap.analysis.processCSV(file_path)

                device.dropCalib, device.ThruEnvelope, x, y = siap.analysis.calibrate_envelope( 
                    device.wavl, siap.core.smooth(device.wavl, device.pwr[port_thru], window=121), siap.core.smooth(device.wavl, device.pwr[port_thru], window=121), 
                    N_seg = N_seg, tol = tol, fitOrder=5, direction='right', verbose = False)

                [device.BW, device.WL] = siap.analysis.bandwidth(device.wavl, -device.dropCalib, threshold=13)

                devices.append(device)
                period.append(getDeviceParameter(device.deviceID, device_prefix, device_suffix))
                WL.append(device.WL)
                BW.append(device.BW)

#%%
# plot all devices and overlay
plt.figure()
for device in devices:
    label = 'Period = ' + str(getDeviceParameter(device.deviceID, device_prefix, device_suffix))+' nm'
    fig = plt.plot(device.wavl,device.pwr[port_drop], label=label)
    plt.legend(loc=0)
plt.ylabel('Power [dBm]', color = 'black')
plt.xlabel('Wavelength [nm]', color = 'black')
plt.title("Raw measurement of all structures")
plt.savefig('devices_raw'+'.pdf')
matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

plt.figure()
for device in devices:
    label = 'Period = ' + str(getDeviceParameter(device.deviceID, device_prefix, device_suffix))+' nm'
    fig = plt.plot(device.wavl,device.dropCalib, label=label)
    plt.legend(loc=0)
plt.ylabel('Transmission (dB)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.title("Calibrated measurement of all structures (using envelope calibration)")
plt.savefig('devices_calib'+'.pdf')
matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

# %% plot analysis results
fig, ax1 = plt.subplots()

ax1.scatter(period, WL, color = 'blue')
ax1.set_xlabel('Grating period [nm]')
ax1.set_ylabel('Bragg wavelength [nm]', color='blue')
ax1.tick_params(axis='y', colors='blue')

ax2 = ax1.twinx()
ax2.scatter(period, BW, color = 'red')
ax2.set_ylabel('3 dB Bandwidth [nm]', color='red')
ax2.tick_params(axis='y', colors='red')


plt.title("Extracted bandwidth and central wavelength of the Bragg gratings")
plt.savefig('analysis'+'.pdf')
matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})
plt.show()

# %% overlay simulation data
#simulation results (220 nm SOI, air)
period_sim_air = [273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283]
wavl_sim_air = [1295.48, 1297.79, 1300.2, 1302.52, 1304.94, 1307.26, 1309.57, 1311.88, 1314.08, 1316.4, 1318.82]

#simulation results (220 nm SOI, SiO2 clad)
period_sim_sio2 = [273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283]
wavl_sim_sio2 = [1318.45, 1321.05, 1323.65, 1326.26, 1328.86, 1331.46, 1334.06, 1336.54, 1339.14, 1341.7, 1344.21]


plt.figure()
plt.scatter(period, WL, color='r', marker='x', label='Experiment')
plt.scatter(period_sim_sio2, wavl_sim_sio2, color='b', marker='o', label='Simulation')
plt.legend()
plt.ylabel('Bragg Wavelength [nm]', color = 'black')
plt.xlabel('Grating Period [nm]', color = 'black')
plt.title("Comparision of Bragg wavelength between simulation and experiment.")
plt.savefig('analysis_WL'+'.pdf')
matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})


D# %%

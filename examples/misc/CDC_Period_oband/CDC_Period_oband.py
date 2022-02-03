"""
SiEPIC Analysis Package 

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example:    Application of SiEPIC_AP analysis functions
            Process data of various contra-directional couplers (CDCs)
            Extract the period and bandwidth from a set of devices
"""
#%%
import sys
sys.path.append(r'C:\Users\musta\Documents\GitHub\SiEPIC_Photonics_Package')
import siepic_analysis_package as siap
import matplotlib.pyplot as plt
import matplotlib, os
import numpy as np


fname_data = "data" # filename containing the desired data
device_prefix = "CDCOPeriod_1000N"
device_suffix = "nmPeriod110nmGap300nmWA390nmWB30nmdWA50nmdWB2p8Ap"
port_drop = 1 # port in the measurement set containing the drop port data
port_thru = 0 # port in the measurement set containing the through port data
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
tol = 3 # calibrate_envelope parameter
N_seg = 25 # calibrate_envelope parameter
period = []
BW = []
WL = []
devices = []
for root, dirs, files in os.walk('data'):
    if os.path.basename(root).startswith(device_prefix):
        for file in files:
            if file.endswith(".csv"):
                device = siap.analysis.processCSV(root+r'\\'+file)

                device.dropCalib, device.ThruEnvelope, x, y = siap.analysis.calibrate_envelope( 
                    device.wavl, device.pwr[port_thru], device.pwr[port_drop], 
                    N_seg = N_seg, tol = tol, verbose = False)

                [device.BW, device.WL] = siap.analysis.bandwidth(device.wavl, device.dropCalib)

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
plt.ylabel('Power (dBm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
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
ax1.set_xlabel('Grating period (nm)')
ax1.set_ylabel('Bragg wavelength (nm)', color='blue')
ax1.tick_params(axis='y', colors='blue')

ax2 = ax1.twinx()
ax2.scatter(period, BW, color = 'red')
ax2.set_ylabel('3 dB Bandwidth (nm)', color='red')
ax2.tick_params(axis='y', colors='red')


plt.title("Extracted bandwidth and central wavelength of the contra-directional couplers")
plt.savefig('analysis'+'.pdf')
matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})
plt.show()

# %% overlay simulation data

WL_sim = [1291.34, 1298.77, 1301.15, 1303.95, 1306.47, 1309.0, 1311.52, 1316.99]
BW_sim = [15.975, 15.135, 15.976, 15.135, 15.976, 15.55, 15.135, 16.6767]

plt.figure()
plt.scatter(period, WL, marker = 'x', label = 'Experiment')
plt.scatter(period, WL_sim, marker = 'o', label = 'Simulation (215 nm silicon)')
plt.legend()
plt.ylabel('Bragg Wavelength (nm)', color = 'black')
plt.xlabel('Grating Period (nm)', color = 'black')
plt.title("Comparision of Bragg wavelength between simulation and experiment. \nSimulation assumes 215 nm thick silicon.")
plt.savefig('analysis_WL'+'.pdf')
matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

plt.figure()
plt.scatter(period, BW, marker = 'x', label = 'Experiment')
plt.scatter(period, BW_sim, marker = 'o', label = 'Simulation (215 nm silicon)')
plt.legend()
plt.ylabel('3 dB Bandwidth (nm)', color = 'black')
plt.xlabel('Grating Period (nm)', color = 'black')
plt.title("Comparision of 3 dB bandwidth between simulation and experiment. \nSimulation assumes 215 nm thick silicon.")
plt.savefig('analysis_BW'+'.pdf')
matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

# %%
WL_sim_neg15nmBias = [1281.95, 1284.33, 1286.72, 1289.66, 1292.74, 1294.7, 1299.89]
BW_sim_neg15nmBias = [14.29, 14.57, 15.1351, 14.29, 14.99, 14.7, 15.415]

plt.figure()
plt.scatter(period, WL, marker = 'x', label = 'Experiment')
plt.scatter(period, WL_sim, marker = 'o', label = 'Simulation (215 nm silicon)')
plt.scatter(period, WL_sim_neg15nmBias, marker = 's', label = 'Simulation with -15 nm bias (215 nm silicon)')

plt.legend()
plt.ylabel('Bragg Wavelength (nm)', color = 'black')
plt.xlabel('Grating Period (nm)', color = 'black')
plt.title("Comparision of Bragg wavelength between simulation and experiment. \nSimulation assumes 215 nm thick silicon.")
plt.savefig('analysis_WL_withBias'+'.pdf')
matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

plt.figure()
plt.scatter(period, BW, marker = 'x', label = 'Experiment')
plt.scatter(period, BW_sim, marker = 'o', label = 'Simulation (215 nm silicon)')
plt.scatter(period, BW_sim_neg15nmBias, marker = 's', label = 'Simulation with -15 nm bias (215 nm silicon)')

plt.legend()
plt.ylabel('3 dB Bandwidth (nm)', color = 'black')
plt.xlabel('Grating Period (nm)', color = 'black')
plt.title("Comparision of 3 dB bandwidth between simulation and experiment. \nSimulation assumes 215 nm thick silicon.")
plt.savefig('analysis_BW_withBias'+'.pdf')
matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

# %%

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
device_prefix = "PCM_Bragg_C__1000N"
device_suffix = "nmPeriod500nmW20nmdW0Apo"
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
tol = 3 # calibrate_envelope parameter
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
                    device.wavl, device.pwr[port_thru], device.pwr[port_drop], 
                    N_seg = N_seg, tol = tol, verbose = False)

                [device.BW, device.WL] = siap.analysis.bandwidth(device.wavl, -device.dropCalib, threshold=6)

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
#simulation results (220 nm SOI, air clad)
period_sim_air = [313, 315, 317, 319, 321, 323, 324, 325, 326]
wavl_sim_air = [1517, 1522, 1527, 1532, 1538, 1543, 1544.74, 1548.9, 1549.85]

#simulation results (220 nm SOI, SiO2 clad)
period_sim_sio2 = [313, 315, 317, 319, 321, 323]
wavl_sim_sio2 = [1536.64, 1542.24, 1547.85, 1553.45, 1559.06, 1564.56]

plt.figure()
plt.scatter(period, WL, color='r', marker='x', label='Experiment')
plt.scatter(period_sim_sio2, wavl_sim_sio2, color='b', marker='o', label='Simulation')
plt.legend()
plt.ylabel('Bragg Wavelength [nm]', color = 'black')
plt.xlabel('Grating Period [nm]', color = 'black')
plt.title("Comparision of Bragg wavelength between simulation and experiment.")
plt.savefig('analysis_WL'+'.pdf')
matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})


# %%


"""
SiEPIC Analysis Package

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example:    Using baseline correction to extract the extinction ratio of MZI devices
"""
#%%
import sys
sys.path.append(r'C:\Users\musta\Documents\GitHub\SiEPIC_Photonics_Package')
import siepic_analysis_package as siap
import os
import matplotlib.pyplot as plt


device_prefix = "splitter_SWG"
port = 1 # port containing the data to process

# crawl available data to choose data files
devices = []
for root, dirs, files in os.walk('data'):
    if os.path.basename(root).startswith(device_prefix):
        for file in files:
            if file.endswith(".csv"):
                device = siap.analysis.processCSV(root+r'\\'+file)
                devices.append(device)

#%% plot all devices (overlay)
plt.figure()
for device in devices:
    plt.plot(device.wavl, device.pwr[port], label = device.deviceID)
plt.legend(loc=0)
plt.ylabel('Power (dBm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')

plt.title("Experimental data (raw)")
plt.savefig('data_raw.pdf')
#%% apply SIAP baseline_calibration function and plot

for device in devices:
    [device.pwrCalib, device.fit] = siap.analysis.baseline_correction([device.wavl, device.pwr[port]])

plt.figure()
for device in devices:
    plt.plot(device.wavl, device.pwrCalib, label = device.deviceID)
plt.legend(loc=0)
plt.ylabel('Transmission (dB)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.title("Calibrated data (using baseline correction)")
plt.savefig('data_calibrated.pdf')
#%% apply SIAP getExtinctionRatio function to calculate extinction ratios

er_wavl_arr = []
er_arr = []

for device in devices:
    temp = siap.analysis.getExtinctionRatio(device.wavl, device.pwrCalib)
    device.er_wavl = temp[0]
    device.er = temp[1]

plt.figure()
for device in devices:
    plt.scatter(device.er_wavl, device.er, label = device.deviceID)
plt.legend(loc=0)
plt.ylabel('Extinction Ratio (dB)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.title("Extracted extinction ratios from the measurements")
plt.savefig('extinction_ratio.pdf')
# %%


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
import numpy as np

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
#%% apply SIAP getExtinctionRatio, getFSR, and getGroupIndex functions

er_wavl_arr = []
er_arr = []
DL = 155.564e-6

for device in devices:
    device.er_wavl, device.er = siap.analysis.getExtinctionRatio(device.wavl, device.pwrCalib, prominence = 6)
    device.fsr_wavl, device.fsr, _ = siap.analysis.getFSR(device.wavl, device.pwrCalib, prominence = 6)
    device.ng = siap.analysis.getGroupIndex([i*1e-9 for i in device.fsr_wavl], [i*1e-9 for i in device.fsr], delta_length = DL)
    device.couplingCoeff = []
    for er in device.er:
        device.couplingCoeff.append(0.5 + 0.5 * np.sqrt( 1/10**(er/10)))

plt.figure()
for device in devices:
    plt.scatter(device.er_wavl, device.er, label = device.deviceID)
plt.legend(loc=4)
plt.ylabel('Extinction Ratio (dB)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.title("Extracted extinction ratios from the measurements")
plt.savefig('extinction_ratio.pdf')

plt.figure()
for device in devices:
    plt.scatter(device.er_wavl, device.couplingCoeff, label = device.deviceID)
plt.legend(loc=4)
plt.ylabel('Splitting ratio', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.title("Extracted splitting ratios from the measurements")
plt.savefig('coupling_coefficient.pdf')

plt.figure()
for device in devices:
    plt.scatter(device.fsr_wavl, device.fsr, label = device.deviceID)
plt.legend(loc=4)
plt.ylabel('Free spectral range (nm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.title("Extracted free spectral ranges from the measurements")
plt.savefig('fsr.pdf')

plt.figure()
for device in devices:
    plt.plot(device.fsr_wavl, device.ng, label = device.deviceID)
plt.legend(loc=4)
plt.ylabel('Group index', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.title("Extracted group indices measurements")
plt.savefig('group_index.pdf')



# %%
wavl_sim = [1296.61, 1308.81, 1312.24, 1333.91]
ng_sim = [4.37898, 4.38968, 4.4002, 4.41045]

wavl_sim_350 = [1296.61, 1308.81, 1312.24, 1333.91]
ng_sim_350 = [4.37898, 4.38968, 4.4002, 4.41045]

wavl_sim_335 = [1296.61, 1308.81, 1312.24, 1333.91]
ng_sim_335 = [4.42644, 4.43656, 4.44627, 4.45546]

wavl_sim_335_215 = [1296.61, 1308.81, 1312.24, 1333.91]
ng_sim_335_215 = [4.42473, 4.43421, 4.44322, 4.45161]

plt.figure()
for device in devices:
    plt.plot(device.fsr_wavl, device.ng, '--', label = device.deviceID)
plt.plot(wavl_sim_350, ng_sim_350, label = 'Simulation 350 nm wide, 220 nm thick')
plt.plot(wavl_sim_335, ng_sim_335, label = 'Simulation 335 nm wide, 220 nm thick')
plt.plot(wavl_sim_335_215, ng_sim_335_215, label = 'Simulation 335 nm wide, 215 nm thick')
plt.legend(bbox_to_anchor=(1.1, 1.05))
plt.ylabel('Group index', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.title("Extracted group indices measurements")
plt.savefig('group_index_vs_sim.pdf')
# %%

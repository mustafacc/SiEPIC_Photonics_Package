
"""
SiEPIC Analysis Package

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example:    Using SIAP to analyzer directional couplers data
"""
#%%
import sys
sys.path.append(r'C:\Users\musta\Documents\GitHub\SiEPIC_Photonics_Package')
import siepic_analysis_package as siap
import os
import matplotlib.pyplot as plt
import numpy as np

device_prefix = "Length"
device_suffix = "u"
port_cross = 0 # port containing the cross-port data to process
port_bar = 1 # port containing the bar-port data to process


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
    parameter = float(deviceID.removeprefix(devicePrefix).removesuffix(deviceSuffix).replace('p','.'))
    return parameter

# crawl available data to choose data files
devices = []
DL = 42.857143e-6 # delta-length in the MZI used for these test structures
prominence = 1
for root, dirs, files in os.walk('data'):
    if os.path.basename(root).startswith(device_prefix):
        for file in files:
            if file.endswith(".csv"):
                device = siap.analysis.processCSV(root+r'\\'+file)
                devices.append(device)

                [device.pwr_bar_calib, device.fit] = siap.analysis.baseline_correction([device.wavl, device.pwr[port_bar]])
                [device.pwr_cross_calib, device.fit] = siap.analysis.baseline_correction([device.wavl, device.pwr[port_cross]])
                device.length = getDeviceParameter(device.deviceID, device_prefix, device_suffix)

                device.er_bar_wavl, device.er_bar = siap.analysis.getExtinctionRatio(device.wavl, device.pwr_bar_calib, prominence = prominence)
                device.fsr_bar_wavl, device.fsr_bar = siap.analysis.getFSR(device.wavl, device.pwr_bar_calib, prominence = prominence)
                device.ng_bar = siap.analysis.getGroupIndex([i*1e-9 for i in device.fsr_bar_wavl], [i*1e-9 for i in device.fsr_bar], delta_length = DL)
                
                device.er_cross_wavl, device.er_cross = siap.analysis.getExtinctionRatio(device.wavl, device.pwr_cross_calib, prominence = prominence)
                device.fsr_cross_wavl, device.fsr_cross = siap.analysis.getFSR(device.wavl, device.pwr_cross_calib, prominence = prominence)
                device.ng_cross = siap.analysis.getGroupIndex([i*1e-9 for i in device.fsr_cross_wavl], [i*1e-9 for i in device.fsr_cross], delta_length = DL)

                device.couplingCoeff_cross = []
                device.couplingCoeff_bar = []
                for er in device.er_cross:
                    device.couplingCoeff_cross.append(0.5 - 0.5 * np.sqrt( 1/10**(er/10)))
                for er in device.er_bar:
                    # 4 and 18 are lengths where the 3 dB crossing occurs
                    if device.length > 3 and device.length < 14: 
                        device.couplingCoeff_bar.append(0.5 + 0.5 * np.sqrt( 1/10**(er/10)))
                    else:
                        device.couplingCoeff_bar.append(0.5 - 0.5 * np.sqrt( 1/10**(er/10)))



#%% plot all devices (overlay)
plt.figure()
for device in devices:
    plt.plot(device.wavl, device.pwr[port_cross], label = device.deviceID)
plt.legend(loc=0)
plt.ylabel('Power (dBm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')

plt.title("Experimental data (raw)")
plt.savefig('data_raw.pdf')

#%% plot a single device for illustration proposes
deviceID = 0

device = devices[deviceID]
# raw data
plt.figure()
plt.plot(device.wavl, device.pwr[port_bar], label = 'Bar port')
plt.plot(device.wavl, device.pwr[port_cross], label = 'Cross port')
plt.legend()
plt.ylabel('Power (dBm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.title("Raw, measured data,\ndevice = MZI_DC_"+str(device.deviceID.replace('p','.')))
plt.savefig('data_raw_'+device.deviceID+'.pdf')

# calibrated data
plt.figure()
plt.plot(device.wavl, device.pwr_bar_calib, label = 'Bar port')
plt.plot(device.wavl, device.pwr_cross_calib, label = 'Cross port')
plt.legend()
plt.ylabel('Transmission (dB)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.title("Calibrated data (using baseline correction),\ndevice = MZI_DC_"+str(device.deviceID.replace('p','.')))
plt.savefig('data_calib_'+device.deviceID+'.pdf')

device.er_bar_wavl, device.er_bar = siap.analysis.getExtinctionRatio(device.wavl, device.pwr_bar_calib, prominence = prominence, verbose = True)
device.fsr_bar_wavl, device.fsr_bar = siap.analysis.getFSR(device.wavl, device.pwr_bar_calib, prominence = prominence, verbose = True)
device.ng_bar = siap.analysis.getGroupIndex([i*1e-9 for i in device.fsr_bar_wavl], [i*1e-9 for i in device.fsr_bar], delta_length = DL, verbose = True)

plt.figure()
plt.scatter(device.er_bar_wavl, device.couplingCoeff_bar)
plt.ylabel('Power splitting ratio', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.title("Extracted power splitting ratios (using unbalanced MZI),\ndevice = MZI_DC_"+str(device.deviceID.replace('p','.')))
plt.savefig('splittingRatio_'+device.deviceID+'.pdf')
#%% plot coupling coefficient at a specific wavelength as a function of variable parameter

wavl_target = 1270
wavl_idx = siap.analysis.find_nearest(device.er_bar_wavl, wavl_target)
couplingLength = []
couplingCoeff = []
wavl_coeffs = []
for device in devices:
    wavl_idx = siap.analysis.find_nearest(device.er_bar_wavl, wavl_target)
    couplingLength.append(device.length)
    couplingCoeff.append(device.couplingCoeff_bar[wavl_idx])
    wavl_coeffs.append(device.er_bar_wavl[wavl_idx])

plt.figure()
plt.scatter(couplingLength, couplingCoeff)
plt.xlabel("Coupling length (microns)")
plt.ylabel("Power splitting ratio")
plt.title("Extracted power splitting ratios from the MZI system \n(around "+str(float(round(np.average(wavl_coeffs),2)))+" nm)")
plt.savefig('power_splitting_ratio.pdf')
# %%

"""
SiEPIC Analysis Package 

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example:    Application of SiEPIC_AP cutback and processCSV function
            to extract the porpagation losses from three different length waveguides.
"""
#%%
import sys
sys.path.append(r'C:\Users\musta\Documents\GitHub\SiEPIC_Photonics_Package')
import siepic_analysis_package as siap
import matplotlib.pyplot as plt
import matplotlib, os
import numpy as np


fname_data = "data" # filename containing the desired data
device_prefix = "wgloss_straight_2000nm_"
device_suffix = "u"
port = 1 # port in the measurement set containing the data

def getDeviceParameter(deviceID, devicePrefix, deviceSuffix = ''):
    """Find the variable parameter of a device based on the ID

    Args:
        deviceID (string): ID of the device.
        devicePrefix (string): Prefix string in the device that's before the variable parameter
        deviceSuffix (string): Any additional fields in the suffix of a device that need to be stripped, optional.

    Returns:
        parameter (float): variable parameter of the device (unit based on whats in the ID)
    """
    parameter = float(deviceID.removeprefix(devicePrefix).removesuffix(deviceSuffix))
    
    return parameter

#%% crawl available data to choose file

lengths = []
devices = []
for root, dirs, files in os.walk('data'):
    if os.path.basename(root).startswith(device_prefix):
        for file in files:
            if file.endswith(".csv"):
                device = siap.analysis.processCSV(root+r'\\'+file)
                devices.append(device)
                lengths.append(getDeviceParameter(device.deviceID, device_prefix, device_suffix))

#%%
# download .mat files from GitHub repo and parse it to a variable (data)
# responses to extract losses from
# in this example, file name units are in um (microns)

# divide by 10000 to see result in dB/cm
lengths_cm = [i/10000 for i in lengths]

input_data_response = []

for device in devices:
    input_data_response.append( [np.array(device.wavl), np.array(device.pwr[port])] )

# apply SiEPIC_PP cutback extraction function
[insertion_loss_wavelength, insertion_loss_fit, insertion_loss_raw] = siap.analysis.cutback( input_data_response, lengths_cm, 1310.0 )


#%%
# plot all cutback structures responses
plt.figure(0)
for device in devices:
    label = 'L = ' + str(getDeviceParameter(device.deviceID, device_prefix, device_suffix)) + ' microns'
    fig0 = plt.plot(device.wavl,device.pwr[port], label=label)
    plt.legend(loc=0)
plt.ylabel('Power (dBm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.title("Raw measurement of cutback structures")
plt.savefig('cutback_measurement'+'.pdf')
matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

#%% Insertion loss vs wavelength plot
plt.figure(1)
fig1 = plt.plot(device.wavl,-insertion_loss_raw, label='Insertion loss (raw)', color='blue')
fig2 = plt.plot(device.wavl,-insertion_loss_fit, label='Insertion loss (fit)', color='red')
plt.legend(loc=0)
plt.ylabel('Propagation Loss (dB/cm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.setp(fig1, 'linewidth', .50)
plt.setp(fig2, 'linewidth', 4.0)
plt.title("Insertion losses using the cut-back method")
plt.savefig('cutback'+'.pdf')
matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

# %%

"""
SiEPIC Analysis Package 

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example:    Application of SiEPIC_AP cutback and processCSV function
            to extract the porpagation losses from three different length waveguides.
"""
#%%
import siepic_analysis_package as siap
import matplotlib.pyplot as plt
import matplotlib, os
import numpy as np


fname_data = "data" # filename containing the desired data
device_id = "wgloss_straight_350nm_"
port = 0 # port in the measurement set containing the data

def getDeviceLength(deviceID, idxField = 3):
    """Find the length of a device based on the ID

    Args:
        deviceID (string): ID of the device.
        idxField (int): index of the field containing the length

    Returns:
        length (float): length of the device (unit based on whats in the ID)
    """
    length = float(deviceID.split('_')[idxField].strip('u'))
    return length

#%% crawl available data to choose file

lengths = []
devices = []
for root, dirs, files in os.walk('data'):
    if os.path.basename(root).startswith(device_id):
        for file in files:
            if file.endswith(".csv"):
                device = siap.analysis.processCSV(root+r'\\'+file)
                devices.append(device)
                lengths.append(getDeviceLength(device.deviceID))

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
    label = 'L = ' + str(getDeviceLength(device.deviceID)) + ' microns'
    fig0 = plt.plot(device.wavl,device.pwr[port], label=label)
    plt.legend(loc=0)
plt.ylabel('Power (dBm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.title("Raw measurement of cutback structures")
plt.savefig('cutback_measurement'+'.pdf')
matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

#%% Insertion loss vs wavelength plot
plt.figure(1)
fig1 = plt.plot(device.wavl,insertion_loss_raw, label='Insertion loss (raw)', color='blue')
fig2 = plt.plot(device.wavl,insertion_loss_fit, label='Insertion loss (fit)', color='red')
plt.legend(loc=0)
plt.ylabel('Loss (dB/cm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.setp(fig1, 'linewidth', .050)
plt.setp(fig2, 'linewidth', 4.0)
plt.title("Insertion losses using the cut-back method")
plt.savefig('cutback'+'.pdf')
matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})


# %%

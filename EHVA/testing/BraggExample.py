"""
This Script Utilizes SiEPIC Analysis Package 

Author:    Alexander Tofini
           alex.tofini@dreamphotonics.com

"""
#%%
import sys
sys.path.append(r'C:\Users\AlexTofini\Documents\GitHub\SiEPIC_Photonics_Package')
sys.path.append(r'C:\Users\AlexTofini\Documents\GitHub\SiEPIC_Photonics_Package\EHVA')
import siepic_analysis_package as siap
from scipy.signal import find_peaks, peak_prominences
import matplotlib.pyplot as plt
import matplotlib, os
import numpy as np
import pandas as pd
import math


#%% This only needs to be ran once to pickle the csv data

try:
    rawCSV = pd.read_csv('EHVAdata.csv')
    rawCSV.to_pickle("EHVAdata.pkl")
except Exception as e:
    print("Failed to read .csv due to the following error: %s" %e)


#%% 
# Loading data from CSV file

data = pd.read_pickle("EHVAdata.pkl")
data.rename(columns={'ExperimentalCondition_Voltage':'EXPvoltage'}, inplace=True)
data.rename(columns={'ExperimentalCondition_Current':'EXPcurrent'}, inplace=True)
print(data)


#%%
# Showing what columns are avaible for query
print("The following are queryable")
print(data.dtypes)

        
#%%
frames = []
# Querying for desired component
desiredComponents = ["Bragg"]
for ii in range(len(desiredComponents)):  
    df = data.loc[data['ComponentName'].str.contains(desiredComponents[ii],case=False)]
    frames.append(df)               

desiredData = pd.concat(frames)
desiredData = desiredData.reset_index(drop=True)
print(desiredData)

#%% 
## Sorting desiredData by component ID for unique device identification

# Determining unique Component IDs 
Component_IDs = desiredData.ComponentId.unique()
devices_df = []

for ii in range(len(Component_IDs)):
    device_df = desiredData[desiredData['ComponentId'] == Component_IDs[ii]]
    device_df = device_df.reset_index(drop=True)
    devices_df.append(device_df)

print("There exists %s devices to analyze" % len(devices_df))



#%%

# Iterating through each device in devices to create necessary plots.
# FOR THE TIME BEING ONLY DEALING WITH PASSIVE DEVICES

devices = []

for ii in range(len(devices_df)):
    device = siap.analysis.measurementEHVA(devices_df[ii])
    devices.append(device)

#%%

# Creating subdirectories in results for each component type in desiredComponents
cwd = os.getcwd()

for ii in range(len(desiredComponents)):
    path = cwd + '/results/' + desiredComponents[ii]
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    
    if not isExist:    
      # Create a new directory because it does not exist 
      os.makedirs(path)
      print("The new directory is created!")



#%%


result_name = 'UNKNOWN'

# plotting results
figNum = 0
centralWavl = []
period = []
bandwidth = []
die = []

Failed = False
for device in devices:
    Failed = False
    
    fig1 = plt.figure(3*figNum,figsize=(8, 6))
    ax1 = fig1.add_subplot(111)
    ax1.set_xlabel('Wavelength (nm)', color = 'black')
    ax1.set_ylabel('Transmission (dB)', color = 'black')
    ax1.set_title(device.deviceID + "_Die" + str(device.dieID) + " \n Calibrated Transmission v.s Wavelength")
    ax1.grid('on')
      
    for ii in range(len(desiredComponents)):
        if desiredComponents[ii].lower() in device.deviceID.lower():
            os.chdir(cwd + '/results/' + desiredComponents[ii])

    
    ports = device.getPorts()
    transmission = []
    voltageTracker = -999
    for port in ports:    
        label = device.deviceID
        for ii in range(len(device.voltageExperimental[port])):
                  
            calibrated_ch = siap.analysis.calibrate_envelope(device.wavl,device.pwr[1][ii],device.pwr[port][ii])
            if (port == 1):
                FSR = siap.analysis.getFSR(device.wavl,calibrated_ch[0],prominence = 15, distance = 300)
                if len(FSR[2] != 0):
                    centralWavl.append(device.wavl[FSR[2][0]])
                    val = device.deviceID.split('500N')
                    val = val[1].split('period')
                    period.append(float(val[0]))
                    die.append(int(device.dieID))
                    
                    idx = FSR[2][0]                     
                    right_idx = -1
                    left_idx = -1
                    while idx < len(calibrated_ch[0]):
                        T = calibrated_ch[0][idx]
                        if T >-3 :
                            right_idx = idx - 1
                            break
                        idx += 1
                    idx = FSR[2][0]
                    while idx > 0:
                        T = calibrated_ch[0][idx]
                        if T > -3 :
                            left_idx = idx+1  
                            break
                        idx -= 1
                        
                    bandwidth.append(device.wavl[right_idx] - device.wavl[left_idx])
                    ax1.scatter(device.wavl[left_idx],calibrated_ch[0][left_idx], s=100, c = 'red')  
                    ax1.scatter(device.wavl[right_idx],calibrated_ch[0][right_idx], s=100, c = 'red') 
                    ax1.scatter(device.wavl[FSR[2][0]],calibrated_ch[0][FSR[2][0]], s=100, c = 'red')
                else:
                    Failed = True
                
                     
            if (math.isnan(device.voltageExperimental[port][ii]) == True):     
                label = "CH" + str(port)                
                ax1.plot(device.wavl, calibrated_ch[0], label=label)
                #ax1.plot(device.wavl, device.pwr[port][ii], label=label)

    if Failed == False:
        ax1.legend()
        fig1.savefig(device.deviceID + "_Die" + str(device.dieID) + ".pdf")
        fig1.savefig(device.deviceID + "_Die" + str(device.dieID) + ".png")
        matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})
        plt.show()
        figNum +=1
    else:
        plt.close(fig1)
    
# going back to original directory    
os.chdir(os.path.dirname(os.getcwd()))
os.chdir(os.path.dirname(os.getcwd()))


#%%
dieLabelColors = ['red','blue','green']
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
ax.set_xlabel('Period (nm)', color = 'black')
ax.set_ylabel('Central Wavelength (nm)', color = 'black')
ax.set_title('Bragg Grating Central Wavelength vs. Grating Period')
ax.grid('on')
#ax.legend('die1','die2','die3')

die1 = [[],[]]
die2 = [[],[]]
die3 = [[],[]]    
for ii in range(len(period)):
    if die[ii] == 1:
        die1[0].append(period[ii])
        die1[1].append(centralWavl[ii])
    elif die[ii] == 2:
        die2[0].append(period[ii])
        die2[1].append(centralWavl[ii])
    else:
        die3[0].append(period[ii])
        die3[1].append(centralWavl[ii])
        
ax.scatter(die1[0],die1[1], c=dieLabelColors[0], label = "Die1", edgecolors = 'none')
ax.scatter(die2[0],die2[1], c=dieLabelColors[1], label = "Die2", edgecolors = 'none')
ax.scatter(die3[0],die3[1], c=dieLabelColors[2], label = "Die3", edgecolors = 'none')
ax.legend()
fig.savefig("CentralWavl_vs_Period" + ".pdf")
fig.savefig("CentralWavl_vs_Period" + ".png")

#%%

dieLabelColors = ['red','blue','green']
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
ax.set_xlabel('Period (nm)', color = 'black')
ax.set_ylabel('3dB Bandwidth (nm)', color = 'black')
ax.set_title('Bragg Grating Bandwidth vs. Grating Period')
ax.grid('on')
#ax.legend('die1','die2','die3')

die1 = [[],[]]
die2 = [[],[]]
die3 = [[],[]]    
for ii in range(len(bandwidth)):
    if die[ii] == 1:
        die1[0].append(period[ii])
        die1[1].append(bandwidth[ii])
    elif die[ii] == 2:
        die2[0].append(period[ii])
        die2[1].append(bandwidth[ii])
    else:
        die3[0].append(period[ii])
        die3[1].append(bandwidth[ii])
        
ax.scatter(die1[0],die1[1], c=dieLabelColors[0], label = "Die1", edgecolors = 'none')
ax.scatter(die2[0],die2[1], c=dieLabelColors[1], label = "Die2", edgecolors = 'none')
ax.scatter(die3[0],die3[1], c=dieLabelColors[2], label = "Die3", edgecolors = 'none')
ax.legend()
fig.savefig("Bandwidth" + ".pdf")
fig.savefig("Bandwidth_vs_Period" + ".png")



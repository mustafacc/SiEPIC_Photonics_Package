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
from DreamPhotonicsConfig import server, user, password, database
from EhvaDBConnection import *
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
desiredComponents = ["MZI"]
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
for device in devices:
    fig1 = plt.figure(2*figNum,figsize=(8, 6))
    ax1 = fig1.add_subplot(111)
    ax1.set_xlabel('Wavelength (nm)', color = 'black')
    ax1.set_ylabel('Power (dBm)', color = 'black')
    ax1.set_title(device.deviceID + "_Die" + str(device.dieID) + " \n Calibrated Transmission v.s Wavelength")
    ax1.grid('on')
    
    active = False
    fig2 = plt.figure(2*figNum+1,figsize=(8, 6))
    ax2 = fig2.add_subplot(111)
    ax2.set_xlabel('Wavelength (nm)', color = 'black')
    ax2.set_ylabel('Transmission (dB)', color = 'black')
    ax2.set_title(device.deviceID + "_Die" + str(device.dieID) + " \n Calibrated Transmission v.s Wavelength Sweep Results")
    ax2.grid('on')
    
    for ii in range(len(desiredComponents)):
        if desiredComponents[ii].lower() in device.deviceID.lower():
            os.chdir(cwd + '/results/' + desiredComponents[ii])
    
    ports = device.getPorts()
    for port in ports:    
        label = device.deviceID
        for ii in range(len(device.voltageExperimental[port])):
            calibrated_ch = siap.analysis.calibrate_envelope(device.wavl,device.pwr[0][0],device.pwr[port][ii])
            if (math.isnan(device.voltageExperimental[port][ii]) == True):     
                label = "CH" + str(port)                
                ax1.plot(device.wavl, calibrated_ch[0], label=label)
            if (math.isnan(device.voltageExperimental[port][ii]) == False):     
                active = True
                label = "CH" + str(port) + " V=" + str(device.voltageExperimental[port][ii])
                ax2.plot(device.wavl, calibrated_ch[0], label=label)
       
    
    ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax1.legend()

    fig1.savefig(device.deviceID + "_Die" + str(device.dieID) + ".pdf")

    if (active == False):
        plt.close(fig2)
    else:
        fig2.savefig(device.deviceID + "_Die" + str(device.dieID) + "_SweepResult.pdf")
    

    matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})
    plt.show()
    figNum +=1
    
# going back to original directory    
os.chdir(os.path.dirname(os.getcwd()))
os.chdir(os.path.dirname(os.getcwd()))
#%%


#siap.analysis.calibrate_envelope(device.wavl,device.pwr[0],device.pwr[2],verbose =True)


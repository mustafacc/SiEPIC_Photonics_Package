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


#%% This only gets executed when a new .csv file has been generated from the EHVA result manager

#rawCSV = pd.read_csv('testCSV.csv')
#rawCSV.to_pickle("CSVEHVAdata.pkl")



#%% 
# Loading data from CSV file

data = pd.read_pickle("CSVEHVAdata.pkl")
data.rename(columns={'ExperimentalCondition_Voltage':'Voltage'}, inplace=True)
print(data)


#%%
# Showing what columns are avaible for query
print("The following are queryable")
print(data.dtypes)

# Can use this to check if there is experimental condition extracted properly
for i in range(len(data.Voltage)):
    if (math.isnan(float(data.Voltage.at[i])) == False):
        print("Non NaN value located at %s for component named: %s" %(i,data.ComponentName.at[i]))
        print(float(data.Voltage.at[i]))
        
#%%
frames = []
# Querying for desired component
desiredComponents = ['contraDC']
for ii in range(len(desiredComponents)):  
    df = data.loc[data['ComponentName'].str.contains(desiredComponents[ii],case=False)]
    frames.append(df)               

desiredData = pd.concat(frames)
desiredData = desiredData.reset_index(drop=True)
print(desiredData)

#%% 
## Sorting desiredData by component ID for unique device identification

# Determining unique Component IDs to work with
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
    device = siap.analysis.measurementEHVA(devices_df[ii],0)
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

# This needs to be automated somehow
ports = [0,1,2]

# plot all cutback structures responses
for device in devices:
    plt.figure()
    
    for ii in range(len(desiredComponents)):
        if desiredComponents[ii].lower() in device.deviceID.lower():
            os.chdir(cwd + '/results/' + desiredComponents[ii])
            print("yes")
      
    #for device in devices:
    for port in ports:    
        label = device.deviceID
        plt.plot(device.wavl,device.pwr[port], label="CH%s" % port)
        plt.legend(loc=0)
    plt.ylabel('Power (dBm)', color = 'black')
    plt.xlabel('Wavelength (nm)', color = 'black')
    plt.title("Transmission v.s Wavelength")
    plt.savefig(device.deviceID + "_Die" + str(device.dieID) + ".pdf")
    matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})
    plt.show()
    
# going back to original directory    
os.chdir(os.path.dirname(os.getcwd()))
#%%


#siap.analysis.calibrate_envelope(device.wavl,device.pwr[0],device.pwr[2],verbose =True)


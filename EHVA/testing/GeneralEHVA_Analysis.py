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
desiredComponents = ["detector"]
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

# Determining if device is a periodic device. Since each periodic device
# can have its own unique FSR and extinction ratio, it is easier to hardcode 
# by names instead of tuning the prominence and peak separation parameters in 
# findpeaks() 
periodic_list = ['MZI','ring','IRPH']
periodic = False
result_name = 'UNKNOWN'
sweep_colors = ['red','blue']


# plotting results
figNum = 0
for device in devices:
    periodic = False
    
    fig1 = plt.figure(3*figNum,figsize=(8, 6))
    ax1 = fig1.add_subplot(111)
    ax1.set_xlabel('Wavelength (nm)', color = 'black')
    ax1.set_ylabel('Transmission (dB)', color = 'black')
    ax1.set_title(device.deviceID + "_Die" + str(device.dieID) + " \n Calibrated Transmission v.s Wavelength")
    ax1.grid('on')
    
    active = False
    fig2 = plt.figure(3*figNum+1,figsize=(8, 6))
    ax2 = fig2.add_subplot(111)
    ax2.set_xlabel('Wavelength (nm)', color = 'black')
    ax2.set_ylabel('Transmission (dB)', color = 'black')
    ax2.set_title(device.deviceID + "_Die" + str(device.dieID) + " \n Calibrated Transmission v.s Wavelength Sweep Results")
    ax2.grid('on')
    
    sweepNum = 0
    fig3 = plt.figure(3*figNum+2,figsize=(8, 6))
    ax3 = fig3.add_subplot(111)
   # ax3.set_xlabel('Voltage (V)', color = 'black')
    ax3.set_xlabel('Power (W)', color = 'black')
    ax3.set_ylabel('T[$\lambda$ = 1550] (dB)', color = 'black')
    ax3.set_title(device.deviceID + "_Die" + str(device.dieID) + " \n Resonance Shift")
    ax3.grid('on')
    
    
    for ii in range(len(desiredComponents)):
        if desiredComponents[ii].lower() in device.deviceID.lower():
            os.chdir(cwd + '/results/' + desiredComponents[ii])
    for ii in range(len(periodic_list)):
        if periodic_list[ii].lower() in device.deviceID.lower():
            periodic = True
    
    ports = device.getPorts()
    transmission = []
    voltageTracker = -999
    sweepSwitchIndices = []
    additionalSweeps = 0
    for port in ports:    
        label = device.deviceID
        for ii in range(len(device.voltageExperimental[port])):
                  
            #TODO(temp fix for noise flour signal calibration)
            if (port >0):
                periodic  = False
            
            if (periodic == True):  
                calibrated_ch = siap.analysis.baseline_correction([device.wavl,device.pwr[port][ii]])
            else:
                calibrated_ch = siap.analysis.calibrate_envelope(device.wavl,device.pwr[0][ii],device.pwr[port][ii])
                     
            if (math.isnan(device.voltageExperimental[port][ii]) == True):     
                label = "CH" + str(port)                
                ax1.plot(device.wavl, calibrated_ch[0], label=label)
                #ax1.plot(device.wavl, device.pwr[port][ii], label=label)
                if (port == 0) and (periodic == True):
                    FSR = siap.analysis.getFSR(device.wavl,calibrated_ch[0], distance = 300)
                    ax1.scatter(device.wavl[FSR[2]], calibrated_ch[0][FSR[2]], color='blue')

                    extinctionRatio = siap.analysis.getExtinctionRatio(device.wavl,calibrated_ch[0], prominence = 10, distance = 300)

            if (math.isnan(device.voltageExperimental[port][ii]) == False):     
                active = True
                if (device.voltageExperimental[port][ii] < voltageTracker):
                    print("NEW SWEEP DETECTED")
                    sweepSwitchIndices.append(ii -1)
                    additionalSweeps += 1
                    
                voltageTracker = device.voltageExperimental[port][ii]
                
                label = "CH" + str(port) + " V=" + str(device.voltageExperimental[port][ii])
                ax2.plot(device.wavl, calibrated_ch[0], label=label)
                
                # Creating the Phase plot
                targetWavl = 1550
                closestWavl = min(device.wavl, key=lambda x:abs(x-targetWavl))
                index = np.where(device.wavl == 1550.0)[0][0]
                transmission.append(calibrated_ch[0][index])
                
                


    ax1.legend()
    ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    fig1.savefig(device.deviceID + "_Die" + str(device.dieID) + ".pdf")
    fig1.savefig(device.deviceID + "_Die" + str(device.dieID) + ".png")

    if (active == False):
        plt.close(fig2)
        plt.close(fig3)
    else:
        for ii in range(additionalSweeps+1):

            start = ii*sweepSwitchIndices[0]
            end = (ii+1)*sweepSwitchIndices[0] 
            
            print("ii is %s" %ii)
            print('start is %s'%start)
            print('end is %s'%end)
            
            label = "Sweep #%s"% ii
            #ax3.plot(device.voltageExperimental[0][start+1:end+1],transmission[start:end],label =label)
            ### This is a temporary hard coded thing to plot Ppi, automating this was not worth the time
            slope = 0.00555
            x = device.voltageExperimental[0][start+1:end+1]
            y = transmission[start:end]
            currentMultiplier = [ slope*val for val in x]
            x = [a * b for a, b in zip(currentMultiplier, x)]
            ax3.plot(x,transmission[start:end],label =label)
            y = np.array(y)
            x = np.array(x)
            Ppi = siap.analysis.getFSR(x, y, prominence = 5, distance = 1)
            ax3.scatter(x[Ppi[2]],y[Ppi[2]] , color=sweep_colors[ii])
            print(Ppi[1])
            ### End of hard coded section

        ax3.legend()
        
        fig2.savefig(device.deviceID + "_Die" + str(device.dieID) + "_SweepResult.pdf")
        fig2.savefig(device.deviceID + "_Die" + str(device.dieID) + "_SweepResult.png")
        fig3.savefig(device.deviceID + "_Die" + str(device.dieID) + "_TvsVoltage.pdf")
        fig3.savefig(device.deviceID + "_Die" + str(device.dieID) + "_TvsVoltage.png")
    

    matplotlib.rcParams.update({'font.size': 11, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})
    plt.show()
    figNum +=1
    
# going back to original directory    
os.chdir(os.path.dirname(os.getcwd()))
os.chdir(os.path.dirname(os.getcwd()))






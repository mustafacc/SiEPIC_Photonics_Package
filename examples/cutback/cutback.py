"""
SiEPIC Analysis Package 

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example:    Application of SiEPIC_AP cutback function
            to extract the porpagation losses from three different length spirals.
"""

import sys
sys.path.append(r'C:\Users\musta\Documents\GitHub\siepic_analysis_package')
import siepic_analysis_package as siap
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# download .mat files from GitHub repo and parse it to a variable (data)
# responses to extract losses from
# in this example, file name units are in um (microns)
unit = [0, 5000, 10000, 30000]

# divide by 10000 to see result in dB/cm
unit_cm = [i/10000 for i in unit]

input_data_response = []

for i in unit:
    file_name = 'SpiralWG'+str(i)+'TE'
    file_extension = '.mat'
    PORT = 1
    input_data_response.append( siap.core.parse_response(file_name+file_extension,PORT) )

# apply SiEPIC_PP cutback extraction function
[insertion_loss_wavelength, insertion_loss_fit, insertion_loss_raw] = siap.analysis.cutback( input_data_response, unit_cm, 1550e-9 )

# plot responses and save pdf

# plot all cutback structures responses
plt.figure(2)
wavelength = input_data_response[0][0]*1e9
fig0 = plt.plot(wavelength,input_data_response[0][1], label='L = 0', color='blue')
fig1 = plt.plot(wavelength,input_data_response[1][1], label='L = 5000 um', color='black')
fig2 = plt.plot(wavelength,input_data_response[2][1], label='L = 10000 um', color='green')
fig3 = plt.plot(wavelength,input_data_response[3][1], label='L = 30000 um', color='red')
plt.legend(loc=0)
plt.ylabel('Power (dBm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.xlim(round(min(wavelength)),round(max(wavelength)))
plt.title("Raw measurement of cutback structures")
plt.savefig('cutback_measurement'+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

# Insertion loss vs wavelength plot
plt.figure(1)
linspace = np.linspace(unit_cm[0],unit_cm[len(unit_cm)-1], len(insertion_loss_fit))
fig1 = plt.plot(linspace,insertion_loss_raw, label='Insertion loss (raw)', color='blue')
fig2 = plt.plot(linspace,insertion_loss_fit, label='Insertion loss (fit)', color='red')
plt.legend(loc=0)
plt.ylabel('Loss (dB/cm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.setp(fig2, 'linewidth', 4.0)
plt.xlim(round(min(unit_cm)),round(max(unit_cm)))
plt.title("Insertion losses using the cut-back method")
plt.savefig('cutback'+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})


"""
SiEPIC Analysis Package

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example:    Application of SiEPIC_AP baseline correction function
"""

import siepic_analysis_package as siap
import scipy, requests, matplotlib
import matplotlib.pyplot as plt

# download .mat file from GitHub repo and parse it to a variable (data)
file_name = 'MZI_data'
file_extension = '.mat'

PORT = 0

[wavelength,power] = siap.core.parse_response(file_name+file_extension,PORT)

#apply SIAP baseline correction function
input_response= [wavelength,power]
[power_corrected, pfit] = siap.analysis.baseline_correction( input_response )

# plot response and save pdf
# raw response with baseline fit
plt.figure(0)
fig1 = plt.plot(wavelength,power, label='Raw data', color='red')
fig2 = plt.plot(wavelength,pfit, label = 'Data baseline', color='blue')
plt.legend(loc=0)
plt.ylabel('Power (dBm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.setp(fig1, 'linewidth', 2.0)
plt.setp(fig2, 'linewidth', 2.0)
plt.xlim(round(min(wavelength)),round(max(wavelength)))
plt.title("Experimental data (raw)")
plt.savefig(file_name+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

# corrected response
plt.figure(1)
fig = plt.plot(wavelength,power_corrected)
plt.ylabel('Power (dBm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.setp(fig, 'color', 'r', 'linewidth', 2.0)
plt.xlim(round(min(wavelength)),round(max(wavelength)))
plt.title("Experimental data (baseline corrected)")
plt.savefig(file_name+'_baseline'+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

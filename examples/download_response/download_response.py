"""
SiEPIC Analysis Package

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example:    Download .mat data file from an online URL, parse and plot data to a .pdf figure
"""

import siepic_analysis_package as siap
import matplotlib
import matplotlib.pyplot as plt
import os, sys

# change working directory to current file location to avoid clutter
os.chdir(os.path.dirname(sys.argv[0]))

#%% download .mat file from GitHub repo and parse it to a variable (data)
file_name = 'MZI_data'
file_extension = '.mat'
url = 'https://github.com/SiEPIC-Kits/SiEPIC_Photonics_Package/blob/master/Examples/'+file_name+file_extension+'?raw=true'
PORT = 0

[wavelength,power] = siap.core.download_response(url,PORT)

#%% plot response and save pdf
fig = matplotlib.pyplot.plot(wavelength,power)
plt.ylabel('Power (dBm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.setp(fig, 'color', 'r', 'linewidth', 2.0)
plt.xlim(round(min(wavelength)),round(max(wavelength)))
plt.title("Experimental data (raw)")
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})
plt.savefig(file_name+'.pdf')
plt.show()

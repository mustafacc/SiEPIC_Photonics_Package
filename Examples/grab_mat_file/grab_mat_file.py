"""
SiEPIC Photonics Package 

Author:     Mustafa Hammood
            Mustafa@ece.ubc.ca

Example:    Download .mat data file from an online URL, parse and plot data to a .pdf figure
"""

#%% import package and installed dependent packages
import sys, os
# go up two directories
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath((os.path.dirname(dir_path))))))

import SiEPIC_Photonics_Package as SiEPIC_PP
from SiEPIC_Photonics_Package.setup import *

#%% download .mat file from GitHub repo and parse it to a variable (data)
file_name = 'MZI_data'
file_extension = '.mat'
url = 'https://github.com/mustafacc/SiEPIC_Photonics_Package/blob/master/Examples/'+file_name+file_extension+'?raw=true'
PORT = 0

[wavelength,power] = SiEPIC_PP.core.download_response(url,PORT)

#%% plot response and save pdf
fig = matplotlib.pyplot.plot(wavelength,power)
matplotlib.pyplot.ylabel('Power (dBm)', color = 'black')
matplotlib.pyplot.xlabel('Wavelength (nm)', color = 'black')
matplotlib.pyplot.setp(fig, 'color', 'r', 'linewidth', 2.0)
matplotlib.pyplot.xlim(round(min(wavelength)),round(max(wavelength)))
matplotlib.pyplot.title("Experimental data (raw)")
matplotlib.pyplot.savefig(file_name+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})
"""
SiEPIC Photonics Package 

Author:     Mustafa Hammood
            Mustafa@ece.ubc.ca

Example:    Application of SiEPIC_PP calibration function
"""

#%% import package and installed dependent packages
import sys, os
# go up two directories
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath((os.path.dirname(dir_path))))))

import SiEPIC_Photonics_Package as SiEPIC_PP
from SiEPIC_Photonics_Package.setup import *

#%% calibration function
# input list format: x_response[wavelength (nm), power (dBm)]
# output list format: calibrated_response (dB), insertion_losses (dB)
def calibrate( input_response, reference_response):
    print("called")
    return

#%% download .mat file from GitHub repo and parse it to a variable (data)
# response to be calibrated
file_name = 'MZI_data'
file_extension = '.mat'
url = 'https://github.com/mustafacc/SiEPIC_Photonics_Package/blob/master/Examples/'+file_name+file_extension+'?raw=true'
PORT = 0
input_response= SiEPIC_PP.core.download_response(url,PORT)

#%% apply SiEPIC_PP calibration correction function

[power_corrected, pfit] = calibrate( input_response )

#%% plot response and save pdf
# raw response with baseline fit
matplotlib.pyplot.figure(0)
fig1 = matplotlib.pyplot.plot(wavelength,power, label='Raw data', color='red')
matplotlib.pyplot.legend(loc=0)
matplotlib.pyplot.ylabel('Power (dBm)', color = 'black')
matplotlib.pyplot.xlabel('Wavelength (nm)', color = 'black')
matplotlib.pyplot.setp(fig1, 'linewidth', 2.0)
matplotlib.pyplot.xlim(round(min(wavelength)),round(max(wavelength)))
matplotlib.pyplot.title("Experimental data (raw)")
matplotlib.pyplot.savefig(file_name+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

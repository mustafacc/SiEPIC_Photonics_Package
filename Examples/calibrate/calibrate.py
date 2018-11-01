"""
SiEPIC Photonics Package 

Author:     Mustafa Hammood
            Mustafa@ece.ubc.ca

Example:    Application of SiEPIC_PP calibration function
"""

#%% import package and installed dependent packages
import sys, os
# go up two directories
#dir_path = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(os.path.dirname(os.path.dirname(dir_path)))

import SiEPIC_Photonics_Package as SiEPIC_PP
from SiEPIC_Photonics_Package.setup import *

#%% download .mat files from GitHub repo and parse it to a variable (data)
# response to be calibrated
file_name_in = 'MZI_data2'
file_extension = '.mat'
url = 'https://github.com/mustafacc/SiEPIC_Photonics_Package/blob/master/Examples/'+file_name_in+file_extension+'?raw=true'
PORT = 1
input_response= SiEPIC_PP.core.download_response(url,PORT)

# reference calibration response
file_name_ref = 'MZI_data2_calib'
file_extension = '.mat'
url = 'https://github.com/mustafacc/SiEPIC_Photonics_Package/blob/master/Examples/'+file_name_ref+file_extension+'?raw=true'
PORT = 0
ref_response= SiEPIC_PP.core.download_response(url,PORT)

#%% apply SiEPIC_PP calibration correction function

[power_corrected, power_calib_fit] = SiEPIC_PP.core.calibrate( input_response, ref_response )

#%% plot responses and save pdf
# raw responses of reference calibration data and input data
wavelength = input_response[0]*1e9
power_calib = input_response[1]
power_in = ref_response[1]
matplotlib.pyplot.figure(0)
fig1 = matplotlib.pyplot.plot(wavelength,power_calib, label='Input data', color='red')
fig2 = matplotlib.pyplot.plot(wavelength,power_calib_fit, label='Reference data fit', color='black')
fig2 = matplotlib.pyplot.plot(wavelength,power_in, label='Reference data', color='blue')
matplotlib.pyplot.legend(loc=0)
matplotlib.pyplot.ylabel('Power (dBm)', color = 'black')
matplotlib.pyplot.xlabel('Wavelength (nm)', color = 'black')
matplotlib.pyplot.setp(fig1, 'linewidth', 2.0)
matplotlib.pyplot.xlim(round(min(wavelength)),round(max(wavelength)))
matplotlib.pyplot.title("Experimental data (raw)")
matplotlib.pyplot.savefig(file_name_in+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

# Calibrated responses of the input data
matplotlib.pyplot.figure(1)
fig1 = matplotlib.pyplot.plot(wavelength,power_corrected, label='Calibrated input data', color='red')
matplotlib.pyplot.legend(loc=0)
matplotlib.pyplot.ylabel('Response (dB)', color = 'black')
matplotlib.pyplot.xlabel('Wavelength (nm)', color = 'black')
matplotlib.pyplot.setp(fig1, 'linewidth', 2.0)
matplotlib.pyplot.xlim(round(min(wavelength)),round(max(wavelength)))
matplotlib.pyplot.title("Experimental data (calibrated)")
matplotlib.pyplot.savefig(file_name_ref+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

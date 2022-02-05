"""
SiEPIC Analysis Package

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example:    Application of SiEPIC_AP calibration function
"""

import siepic_analysis_package as siap
import matplotlib.pyplot as plt
import matplotlib

# download .mat file from GitHub repo and parse it to a variable (data)
file_name = 'MZI_data'
file_name_ref = 'GC_data'
file_extension = '.mat'

PORT = 1
input_response = siap.core.parse_response(file_name+file_extension,PORT)
PORT = 0
ref_response = siap.core.parse_response(file_name_ref+file_extension,PORT)


# apply SiEPIC_PP calibration correction function

[power_corrected, power_calib_fit] = siap.analysis.calibrate( input_response, ref_response )

# plot responses and save pdf
# raw responses of reference calibration data and input data
wavelength = input_response[0]*1e9
power_calib = input_response[1]
power_in = ref_response[1]
plt.figure(0)
fig1 = plt.plot(wavelength,power_calib, label='Input data', color='red')
fig2 = plt.plot(wavelength,power_calib_fit, label='Reference data fit', color='black')
fig2 = plt.plot(wavelength,power_in, label='Reference data', color='blue')
plt.legend(loc=0)
plt.ylabel('Power (dBm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.setp(fig1, 'linewidth', 2.0)
plt.xlim(round(min(wavelength)),round(max(wavelength)))
plt.title("Experimental data (raw)")
plt.savefig(file_name+'_input.pdf')
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
matplotlib.pyplot.savefig(file_name+'_ref.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

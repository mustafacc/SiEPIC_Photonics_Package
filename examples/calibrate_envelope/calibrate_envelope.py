"""
SiEPIC Analysis Package 

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example:    Application of SiEPIC_AP calibration with envelope function
"""
# import package and installed dependent packages
import siepic_analysis_package as siap
import matplotlib.pyplot as plt
import matplotlib

# response to be calibrated
file_name_in = 'contraDC'
file_extension = '.mat'
PORT = 0
input_response= siap.core.parse_response(file_name_in+file_extension,PORT)

# reference calibration response
file_name_ref = 'contraDC'
PORT = 1
ref_response= siap.core.parse_response(file_name_ref+file_extension,PORT)

# apply calibration correction function

[power_corrected,power_calib_fit] = siap.analysis.calibrate_envelope( input_response, ref_response )

#%% plot responses and save pdf
# raw responses of reference calibration data and input data
wavelength = input_response[0]*1e9
power_calib = input_response[1]
power_in = ref_response[1]
plt.figure(0)
fig1 = plt.plot(wavelength,power_calib, label='Input data', color='red')
fig2 = plt.plot(wavelength,power_calib_fit, label='Reference data envelope', color='black')
fig2 = plt.plot(wavelength,power_in, label='Reference data', color='blue')
plt.legend(loc=0)
plt.ylabel('Power (dBm)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.setp(fig1, 'linewidth', 2.0)
plt.xlim(round(min(wavelength)),round(max(wavelength)))
plt.title("Experimental data (raw)")
plt.savefig(file_name_in+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

# Calibrated responses of the input data
plt.figure(1)
fig1 = plt.plot(wavelength,power_corrected, label='Calibrated input data', color='red')
plt.legend(loc=0)
plt.ylabel('Response (dB)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.setp(fig1, 'linewidth', 2.0)
plt.xlim(round(min(wavelength)),round(max(wavelength)))
plt.title("Experimental data (calibrated)")
plt.savefig(file_name_ref+'_calibrated.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

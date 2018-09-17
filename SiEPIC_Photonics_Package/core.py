"""
SiEPIC Photonics Package

Author:     Mustafa Hammood
            Mustafa@ece.ubc.ca

Module:     Core functionalities of SiEPIC PP

functions:

calibrate( input_response, reference_response):
baseline_correction( input_response ):
cutback( input_data_response, input_data_count):
to_s_params( input_data ):
"""

from SiEPIC_Photonics_Package.setup import *

def calibrate( input_response, reference_response):
    print("called")
    return

# baseline correction function
# input list format: input_response[wavelength (nm), power (dBm)]
# output list format: [power (dBm) with baseline correction, baseline correction fit]
def baseline_correction( input_response ):
    fitOrder = 4
    wavelength = input_response[0]
    power = input_response[1]
    
    pfit = numpy.polyfit(wavelength-numpy.mean(wavelength), power, fitOrder)
    power_baseline = numpy.polyval(pfit, wavelength-numpy.mean(wavelength))
    
    power_corrected = power - power_baseline
    power_corrected = power_corrected + max(power_baseline) -max(power)
    
    return [power_corrected, power_baseline]

def cutback( input_data_response, input_data_count):
    return

def to_s_params( input_data ):
    return


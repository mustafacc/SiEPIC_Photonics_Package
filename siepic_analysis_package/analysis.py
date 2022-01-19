"""
SiEPIC Analysis Package analysis module.

Author:     Mustafa Hammood
            mustafa@siepic.com

Module: Data processing and analysis functionalities of the analysis package

"""
import numpy as np

def find_nearest(array, value):
    """Find the array index that's nearest to an input value

    Args:
        array (nparray): Input list to search.
        value (float): Target value to search for.

    Returns:
        int: index of the arra
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def bandwidth ( input_data_response, threshold = 3):
    """Calculates the bandwidth of an input result

    Args:
        input_data_response (list): [wavelength (nm), power (dBm)]
        threshold (int, optional): bandwidth threshold. Defaults to 3 dB.

    Returns:
        list: Calculated bandwidth and wavelength [bandwidth, central_wavelength]
    """

    # input list format: 
    #                    bandwidth threshold, default 3 dB
    # output list format: [bandwidth of threshold, central wavelength]

    wavelength = input_data_response[0]
    response = input_data_response[1]
    
    center_index = find_nearest( response, max(response))
    isInBand = response>max(response) - threshold

    leftBound = center_index

    while isInBand[leftBound] == 1:
        leftBound = leftBound-1

    rightBound=center_index

    while isInBand[rightBound] == 1:
        rightBound = rightBound+1

    bandwidth = wavelength[rightBound] - wavelength[leftBound]
    
    central_wavelength = (wavelength[rightBound] + wavelength[leftBound])/2
    
    return [bandwidth, central_wavelength]

def cutback(input_data_response, input_data_count, wavelength, fitOrder = 8):
    """Extract insertion losses of a structure using cutback method.

    Args:
        input_data_response (list): input_data_response (list) [wavelength (nm), power (dBm)]
        input_data_count (array): input_data_count (array) [array of unit count]
        wavelength (list): wavelength of insertion loss measurement
        fitOrder (int): order of the polynomial fit. Optional, default = 8.

    Returns:
        list: [insertion loss (fit) at wavelength (dB/unit), insertion loss (dB) vs wavelength (nm)]
    """
    # fit the responses to a polynomial
    wavelength_data = input_data_response[0][0]
    
    power = []
    pfit = []
    power_fit = []
    for i in range(len(input_data_count)):
        power.append( input_data_response[i][1] )
        pfit.append( np.polyfit(wavelength_data-np.mean(wavelength_data), power[i], fitOrder) )
        power_fit.append( np.polyval(pfit[i], wavelength_data-np.mean(wavelength_data)) )
    
    power_fit_transpose = np.transpose(power_fit)
    power_transpose = np.transpose(power)
    
    # find index of wavelength of interest
    index = np.where( wavelength_data==wavelength )[0][0]
    
    # find insertion loss vs wavelength
    insertion_loss = []
    insertion_loss_raw = []
    for i in range(len(wavelength_data)):
        insertion_loss.append( np.polyfit(input_data_count, power_fit_transpose[i], 1))
        insertion_loss_raw.append( np.polyfit(input_data_count, power_transpose[i], 1))
    
    
    return [ insertion_loss[index][0], np.transpose(insertion_loss)[0], np.transpose(insertion_loss_raw)[0] ]

def calibrate(input_response, reference_response, fitOrder = 8):
    """Response correction function to calibrate an input response with respect
        to a reference response

    Args:
        input_response (list): list of measurement data, format: [wavelength, value].
        reference_response (list): list of reference data, format: [wavelength, value].
        fitOrder (int): order of the polynomial fit. Optional, default = 8.

    Returns:
        list: list containing calibrated results and the fit 
            output list format: [input power (dBm) with calibration correction,
            polynomial fit of reference power (dBm)]
    """
    wavelength = reference_response[0]
    power = reference_response[1]
    
    pfit = np.polyfit(wavelength-np.mean(wavelength), power, fitOrder)
    power_calib_fit = np.polyval(pfit, wavelength-np.mean(wavelength))
    
    power_corrected = input_response[1] - power_calib_fit
    
    return [power_corrected, power_calib_fit]

#%% baseline_correction function (useful to normalize and calibrate periodic responses)
def baseline_correction(input_response, fitOrder = 4):
    """baseline_correction function (useful to normalize and calibrate periodic responses)

    Args:
        input_response (list): list containing the response to be corrected. 
            input list format: input_response[wavelength (nm), power (dBm)]
        fitOrder (int): order of the polynomial fit. Optional, default = 4.

    Returns:
        list: output list format: [input power (dBm) with baseline correction, baseline correction fit]
    """
    wavelength = input_response[0]
    power = input_response[1]
    
    pfit = np.polyfit(wavelength-np.mean(wavelength), power, fitOrder)
    power_baseline = np.polyval(pfit, wavelength-np.mean(wavelength))
    
    power_corrected = power - power_baseline
    power_corrected = power_corrected + max(power_baseline) -max(power)
    
    return [power_corrected, power_baseline]

def calibrate_envelope( input_response, reference_response, seg = 55, difference_tol = 8, fitOrder = 4):
    """calibration function that extracts the "envelope" of a response and use it as a reference

    Args:
        input_response (list): list containing the response to be corrected.
            input list format: input_response[wavelength (nm), power (dBm)]
        reference_response (list): list of reference data, format: [wavelength, value].
        seg (int, optional): Number of segments to split the response into. Defaults to 55.
        difference_tol (int, optional): Value tolerance to accept within the envelope. Defaults to 8.
        fitOrder (int): order of the polynomial fit. Optional, default = 4.

    Returns:
        list: output list format: [input power (dBm) with envelope correction, envelope correction fit]
    """
    # step 1-pick points on the reference response that create an envelope fit
    # split the response into SEG segments, if two segments are seperated by more than TOL, discard second point and go to next point
    wavelength = reference_response[0]
    power = reference_response[1]

    wavelength_input = input_response[0]
    power_input = input_response[1]

    step = int(np.size(power)/seg)

    power_ref = []
    wavelength_ref = []
    cursor_initial = 0
    cursor_next = 1
    for i in range(seg):

        point_initial = power[cursor_initial*step]
        point_next = power[step*(cursor_next)]
        
        if abs(point_initial - point_next) < difference_tol:              
            power_ref.append(power[cursor_initial*step])
            wavelength_ref.append(wavelength[cursor_initial*step])
            cursor_initial = cursor_initial+1
            cursor_next = cursor_next+1
        else:
            while abs(point_initial - point_next) > difference_tol and (cursor_next+2)*step < np.size(power):
                cursor_next = cursor_next+1
                point_next = power[step*(cursor_next)]
                
            cursor_initial = cursor_next
            cursor_next = cursor_next+1


        if cursor_next*step >= np.size(power):
            break
    
    pfit_ref = np.polyfit(wavelength_ref-np.mean(wavelength_ref), power_ref, fitOrder)
    powerfit_ref = np.polyval(pfit_ref, wavelength-np.mean(wavelength))
    
    pfit_input = np.polyfit(wavelength_input-np.mean(wavelength_input), power_input, fitOrder)
    powerfit_input = np.polyval(pfit_input, wavelength_input-np.mean(wavelength_input))
    
    # step 2-call calibrate input with envelope fit as a reference response
    power_input_calibrated = power_input - powerfit_ref
    
    return [power_input_calibrated, powerfit_ref]

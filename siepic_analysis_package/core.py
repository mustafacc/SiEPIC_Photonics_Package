"""
SiEPIC Analysis Package core module.

Author:     Mustafa Hammood
            mustafa@siepic.com

Module: Core functionalities of the analysis package

"""

import requests
import scipy.io


def download_response(url, port):
    """
    Download an input .mat response from a url and parses data into an array.

    data is assumed to be from  measurement scanResults or scandata formats.


    Parameters
    ----------
    url : string
        URL of the data download link.
    port : int
        measurement port to be downloaded.

    Returns
    -------
    data : list
        List of data points [wavelength (m), power (dBm)].

    """
    r = requests.get(url, allow_redirects=True)
    file_name = 'downloaded_data'+str(port)
    with open(file_name, 'wb') as f:
        f.write(r.content)

    data = scipy.io.loadmat(file_name)

    if('scanResults' in data):
        wavelength = data['scanResults'][0][port][0][:, 0]
        power = data['scanResults'][0][port][0][:, 1]
    elif('scandata' in data):
        wavelength = data['scandata'][0][0][0][:][0]
        power = data['scandata'][0][0][1][:, port]
    elif('wavelength' in data):
        wavelength = data['wavelength'][0][:]
        power = data['power'][:, port][:]

    data = [wavelength, power]

    return data


def parse_response(filename, port):
    """
    Parse an input .mat response from a local file into an array.

    data is assumed to be from  measurement scanResults or scandata formats.

    Parameters
    ----------
    filename : string
        File to be parsed.
        (including directory if not in current working directory).
    port : int
        measurement port to be downloaded.

    Returns
    -------
    data : list
        List of data points [wavelength (m), power (dBm)].
    """
    data = scipy.io.loadmat(filename)

    if('scanResults' in data):
        wavelength = data['scanResults'][0][port][0][:, 0]
        power = data['scanResults'][0][port][0][:, 1]
    elif('scandata' in data):
        wavelength = data['scandata'][0][0][0][:][0]
        power = data['scandata'][0][0][1][:, port]
    elif('wavelength' in data):
        wavelength = data['wavelength'][0][:]
        power = data['power'][:, port][:]

    data = [wavelength, power]
    return data

def cutback(input_data_response, input_data_count, wavelength):
    
    #cutback( input_data_response, input_data_count, wavelength): extract insertion losses of a structure using cutback method
    # input list format: input_data_response (list) [wavelength (nm), power (dBm)]
    #                   input_data_count (array) [array of unit count]
    #                   wavelength of insertion loss measurement
    # output list format: [insertion loss (fit) at wavelength (dB/unit), insertion loss (dB) vs wavelength (nm)]
    # fit the responses to a polynomial
    fitOrder = 8
    wavelength_data = input_data_response[0][0]
    
    power = []
    pfit = []
    power_fit = []
    for i in range(len(input_data_count)):
        power.append( input_data_response[i][1] )
        pfit.append( numpy.polyfit(wavelength_data-numpy.mean(wavelength_data), power[i], fitOrder) )
        power_fit.append( numpy.polyval(pfit[i], wavelength_data-numpy.mean(wavelength_data)) )
    
    power_fit_transpose = numpy.transpose(power_fit)
    power_transpose = numpy.transpose(power)
    
    # find index of wavelength of interest
    index = numpy.where( wavelength_data==wavelength )[0][0]
    
    # find insertion loss vs wavelength
    insertion_loss = []
    insertion_loss_raw = []
    for i in range(len(wavelength_data)):
        insertion_loss.append( numpy.polyfit(input_data_count, power_fit_transpose[i], 1))
        insertion_loss_raw.append( numpy.polyfit(input_data_count, power_transpose[i], 1))
    
    
    return [ insertion_loss[index][0], numpy.transpose(insertion_loss)[0], numpy.transpose(insertion_loss_raw)[0] ]
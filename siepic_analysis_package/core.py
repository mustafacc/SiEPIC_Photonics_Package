"""
SiEPIC Analysis Package core module.

Author:     Mustafa Hammood
            mustafa@siepic.com

Module:     Core functionalities of the analysis package

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


def smooth(x, y, window=51, order=5, verbose=False):
    """
    Smooth a trace. Apply a Savitzky-Golay filter to an array.

    Parameters
    ----------
    x : list
        X domain of the dataset.
    y : list
        y domain of the dataset.
    window : int, optional
        The length of the filter window (i.e., the number of coefficients).
        If mode is ‘interp’, window_length must be less than or equal to the
        size of x. The default is 51.
    order : int, optional
        The order of the polynomial used to fit the samples.
        polyorder must be less than window_length. The default is 3.
    verbose : bool, optional
        Optionally plot the result. The default is False.

    Returns
    -------
    yhat : ndarray
        The filtered data.

    """
    from scipy.signal import savgol_filter
    yhat = savgol_filter(y, window, order)  # window size 51, polynomial order 3
    if verbose:
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(x, y, linewidth=0.5, label='Input data')
        plt.plot(x, yhat, color='red', linewidth=1.5, label='Filtered')
        plt.legend(loc=0)
        plt.title("Filtered data with Savitzky-Golay filter")
        plt.xlabel("X")
        plt.ylabel("Y")
    return yhat

# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 01:37:33 2023

@author: musta
"""

import siepic_analysis_package as siap
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.interpolate import interp1d
font = {'family': 'normal',
        'size': 18}

device_prefix = "PCM_DC_Length"
device_suffix = "um_1"
port_cross = 1 # port containing the cross-port data to process
port_bar = 0 # port containing the bar-port data to process

DL = 53.815e-6 # delta-length in the MZI used for these test structures
wavl_range = [1290, 1330]  # adjust wavelength range
window = 210  # filtering window, cleaner data is easier to detect peaks
peak_prominence = 0.25  # adjust of peak detection is bad

def getDeviceParameter(deviceID, devicePrefix, deviceSuffix = ''):
    """Find the variable parameter of a device based on the ID
    
    IMPORTANT: "removeprefix" and "removesuffix" are only available
        for Python >= 3.9

    Args:
        deviceID (string): ID of the device.
        devicePrefix (string): Prefix string in the device that's before the variable parameter
        deviceSuffix (string): Any additional fields in the suffix of a device that need to be stripped, optional.

    Returns:
        parameter (float): variable parameter of the device (unit based on whats in the ID)
    """
    parameter = float(deviceID.removeprefix(devicePrefix).removesuffix(deviceSuffix).replace('p','.'))
    return parameter

def extract_periods(wavelength, transmission, min_prominence=.25, plot=False):
    from scipy.signal import find_peaks
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Subtract the mean of the signal
    transmission_centered = transmission - np.mean(transmission)
    
    # Find peaks
    peak_indices = find_peaks(transmission_centered, prominence=min_prominence)[0]
    peak_wavelengths = wavelength[peak_indices]
    
    # Calculate periods
    periods = np.diff(peak_wavelengths)
    
    # Find troughs
    inverted_transmission_centered = -transmission_centered
    trough_indices = find_peaks(inverted_transmission_centered, prominence=min_prominence)[0]
    trough_wavelengths = wavelength[trough_indices]
    
    # Calculate extinction ratios
    extinction_ratios = []
    for i in range(len(peak_indices) - 1):
        # find troughs between current peak and next peak

        trough_value = transmission[trough_indices[i]]
        peak_value = transmission[peak_indices[i]]
        extinction_ratios.append(np.abs(peak_value - trough_value))
    
    # Record the period and extinction ratio at the midpoint between each pair of consecutive peaks
    midpoints = (peak_wavelengths[:-1] + peak_wavelengths[1:]) / 2
    periods_at_midpoints = dict(zip(midpoints, periods))
    extinction_ratios_at_midpoints = dict(zip(midpoints, extinction_ratios))
    
    if plot:
        fig, axs = plt.subplots(3, figsize=(14, 20))
        
        axs[0].plot(wavelength, transmission, label="Signal")
        axs[0].plot(peak_wavelengths, transmission[peak_indices], "x", label="Peaks")
        axs[0].plot(trough_wavelengths, transmission[trough_indices], "x", label="Troughs")
        axs[0].set_title("Signal with Detected Peaks")
        axs[0].legend()
        
        axs[1].scatter(midpoints, periods)
        axs[1].set_xlabel("Wavelength")
        axs[1].set_ylabel("FSR")
        axs[1].set_title("FSR as a function of Wavelength")

        axs[2].scatter(midpoints, extinction_ratios)
        axs[2].set_xlabel("Wavelength")
        axs[2].set_ylabel("Extinction Ratio (dB)")
        axs[2].set_title("Extinction Ratio as a function of Wavelength")
        
        plt.tight_layout()
        plt.show()
        
    return midpoints, periods, extinction_ratios

def average_arrays(x_values, y_values_list, x_new, plot=False):
    """
    x_values: list of arrays, each containing the x-values for one of the y-value arrays
    y_values_list: list of arrays, the y-value arrays to be averaged
    x_new: array, the new common x-grid to interpolate onto
    plot: boolean, if True the function will create a plot of the averaged data with error bars
    """
    from scipy.interpolate import interp1d
    import numpy as np
    # List to store the interpolated y-values
    y_values_interp_list = []
    
    # Interpolate each y-value array onto the new x-grid
    for x, y in zip(x_values, y_values_list):
        f = interp1d(x, y, bounds_error=False, fill_value=np.nan)
        y_new = f(x_new)
        y_values_interp_list.append(y_new)
    
    # Convert the list of interpolated y-value arrays into a 2D array
    y_values_interp_array = np.array(y_values_interp_list)
    
    # Compute the mean of the interpolated y-value arrays, ignoring NaNs
    y_average = np.nanmean(y_values_interp_array, axis=0)
    
    # Replace any remaining NaNs in the average with the closest valid value
    mask = np.isnan(y_average)
    y_average[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), y_average[~mask])
    
    # Compute the standard deviation of the interpolated y-value arrays, ignoring NaNs
    y_std = np.nanstd(y_values_interp_array, axis=0)
    
    # Replace any NaNs in the standard deviation with the closest valid value
    mask_std = np.isnan(y_std)
    y_std[mask_std] = np.interp(np.flatnonzero(mask_std), np.flatnonzero(~mask_std), y_std[~mask_std])

    if plot:
        plt.figure(figsize=(10,6))
        plt.plot(x_new, y_average, 'k-', label='Average')
        plt.fill_between(x_new, y_average - y_std, y_average + y_std, color='gray', alpha=0.2, label='Std dev')
        plt.title('Averaged Data')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend(loc='best')
        plt.grid(True)
        plt.show()

    return x_new, y_average, y_std, y_average

#%% crawl available data to choose data files
devices = []

for root, dirs, files in os.walk('data'):
    if os.path.basename(root).startswith(device_prefix):
        for file in files:
            if file.endswith(".csv"):
                device = siap.analysis.processCSV(root+r'\\'+file)
                devices.append(device)
                device.length = getDeviceParameter(device.deviceID, device_prefix, device_suffix)
                device.wavl, device.pwr[port_cross] = siap.analysis.truncate_data(device.wavl, siap.core.smooth(device.wavl, device.pwr[port_cross], window=window), wavl_range[0], wavl_range[1])
                [device.cross_T, device.fit] = siap.analysis.baseline_correction([device.wavl, device.pwr[port_cross]])
                midpoints, fsr, extinction_ratios = extract_periods(device.wavl, device.cross_T, min_prominence=peak_prominence, plot=False)
                
                device.ng_wavl = midpoints
                device.ng = siap.analysis.getGroupIndex([i*1e-9 for i in device.ng_wavl], [i*1e-9 for i in fsr], delta_length = DL)

                device.kappa = []
                for er in extinction_ratios:
                    device.kappa.append(0.5 - 0.5 * np.sqrt( 1/10**(er/10)))


#%% Group index plotting
# simulated data
ng_500nm_fit = [-6.78194041e-10, -1.83117238e-08,  3.25911055e-04,  4.40335210e+00]
ng_wavl_fit = [7.56617044e-17, 1.84233132e-13, 4.86069882e-10, 1.28000000e-06]
ng_500nm = np.polyval(ng_500nm_fit, np.linspace(0, 100 - 1, 100))
wavl_sim = np.polyval(ng_wavl_fit, np.linspace(0, 100 - 1, 100))*1e9

fig, ax1 = plt.subplots(figsize=(10, 6))
for device in devices:
    ax1.scatter(device.ng_wavl, device.ng, color='black', linewidth=0.1)
ax1.plot(wavl_sim, ng_500nm, color='blue', label='Simulated 350 nm X 220 nm')
ax1.set_xlim(np.min([np.min(i.ng_wavl) for i in devices]), np.max([np.max(i.ng_wavl) for i in devices]))
ng_avg_wavl, ng_avg, ng_std, ng_std_avg = average_arrays([i.ng_wavl for i in devices], [i.ng for i in devices], np.linspace(wavl_range[0], wavl_range[1]))
ax1.plot(ng_avg_wavl, ng_avg, '--', color='black', label='Average')
ax1.fill_between(np.linspace(wavl_range[0], wavl_range[1]), ng_std_avg - ng_std, ng_std_avg + ng_std, color='gray', alpha=0.2, label='Std dev')
ax1.legend()
ax1.set_ylabel('Group index')
ax1.set_xlabel('Wavelength [nm]')
fig.savefig('group_index.pdf')

#%%
def sort_devices_by_length(devices):
    sorted_devices = sorted(devices, key=lambda d: d.length)
    return sorted_devices

devices = sort_devices_by_length(devices)

# Extracting wavelength and device length data
ng_wavl = np.array([device.ng_wavl for device in devices])
device_lengths = np.array([device.length for device in devices])

# Creating a common wavelength grid
common_ng_wavl = np.unique(np.concatenate(ng_wavl))

# Creating meshgrid for wavelength and device length
X, Y = np.meshgrid(common_ng_wavl, device_lengths)

# Creating an empty 2D array for coupling coefficient data
Z = np.empty_like(X)

# Populating the 2D array with coupling coefficient data
for i, device in enumerate(devices):
    interp_func = interp1d(device.ng_wavl, device.kappa, kind='linear', fill_value='extrapolate')
    Z[i, :] = interp_func(common_ng_wavl)

# Plotting the contour map.0
plt.contourf(X, Y, Z, cmap='viridis')

# Adding labels and title to the plot
plt.xlabel("Wavelength [nm]")
plt.ylabel("Coupling Length [µm]")
plt.title("Coupling Coefficient Contour Map (100 nm gap)")

# Adding a colorbar
plt.colorbar()
plt.savefig('coupling_coeff.pdf')
# Displaying the plot
plt.show()

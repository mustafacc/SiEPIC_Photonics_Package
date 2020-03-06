"""
SiEPIC Photonics Package 

Author:     Mustafa Hammood
            Mustafa@ece.ubc.ca

Example:    Application of SiEPIC_PP: Model the experimental response of a Bragg grating
"""

#%% import package and installed dependent packages
import sys, os, math, cmath
import numpy as np
from numpy.lib.scimath import sqrt as csqrt
# go up two directories
#dir_path = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(os.path.dirname(os.path.dirname(dir_path)))

import SiEPIC_Photonics_Package as SiEPIC_PP
from SiEPIC_Photonics_Package.setup import *

#%% download .mat files from GitHub repo and parse it to a variable (data)
# response to be calibrated
file_name_in = 'Bragg'
file_extension = '.mat'
url = 'https://www.dropbox.com/s/hw7dgstrfvseq9q/PCM_PCMBraggDW30_1723.mat?dl=1'
PORT = 1
input_response= SiEPIC_PP.core.download_response(url,PORT)

# Grating design parameters

wavelength_start = 1500e-9
wavelength_stop = 1600e-9
resolution = 0.001

# Grating waveguide compact model
# these are polynomial fit constants from a waveguide width of 500 nm
n1_g = 4.077182700600432
n2_g = -0.982556173493906
n3_g = -0.046366956781710


# grating parameters
period = 320e-9     # period of perturbation
N = 300        # number of periods

# Cavity Parameters
alpha = 150/4.34

#%% apply SiEPIC_PP calibration correction function
[power_corrected, power_calib_fit] = SiEPIC_PP.core.calibrate_envelope( input_response, input_response)

#%% plot responses and save pdf
# raw responses of reference calibration data and input data
wavelength = input_response[0]*1e9
power_calib = input_response[1]
matplotlib.pyplot.figure(0)
fig1 = matplotlib.pyplot.plot(wavelength,power_calib, label='Input data', color='red')
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
matplotlib.pyplot.savefig(file_name_in+'_calibrated.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

#%% extract the bandwidth (3 dB) and central wavelength of the response.
[bandwidth, central_wavelength] = SiEPIC_PP.core.bandwidth( input_response, 3)
#print("3dB Bandwidth = "+str(bandwidth))
#print("Central wavelength= "+str(central_wavelength))

#%% find the coupling coefficient/strength (kappa) of the grating from experimental response
ng = 4.2
kappa = math.pi*ng*bandwidth/(central_wavelength**2)

#%% Apply coupled-mode thoery

j = cmath.sqrt(-1)

lambda_0 = np.linspace(wavelength_start, wavelength_stop, round((wavelength_stop-wavelength_start)*1e9/resolution))
neff = (n1_g + n2_g*(lambda_0*1e6) + n3_g*(lambda_0*1e6)**2)
beta = 2*math.pi*neff/lambda_0


Lg_L = N*period
deltaB = 2*math.pi*neff/lambda_0-math.pi/period
omega = csqrt(kappa**2-deltaB**2)


t = []; r = []
for i in range(len(lambda_0)):
    G_L = [
        [np.cosh(omega[i]*Lg_L)-j*deltaB[i]/omega[i]*np.sinh(omega[i]*Lg_L),
         -j*kappa*np.sinh(omega[i]*Lg_L)/omega[i]],
         [j*kappa*np.sinh(omega[i]*Lg_L)/omega[i],
          np.cosh(omega[i]*Lg_L)+j*deltaB[i]/omega[i]*np.sinh(omega[i]*Lg_L)]]

        
    # matrix multiplication G_L*Y*G_R
    H = G_L
    
    t.append(H[0][0]-H[1][0]*H[0][1]/H[1][1])
    r.append(-H[1][0]/H[1][1])
    
# to log scale
T = np.log10(np.absolute(t)**2)
R = np.log10(np.absolute(r)**2)

#%% plot spectrum
matplotlib.pyplot.figure(2)
fig1 = matplotlib.pyplot.plot(lambda_0*1e9,T, label='Transmission', color='blue')
fig2 = matplotlib.pyplot.plot(lambda_0*1e9,R, label='Reflection', color='red')
matplotlib.pyplot.legend(loc=0)
matplotlib.pyplot.ylabel('Response (dB)', color = 'black')
matplotlib.pyplot.xlabel('Wavelength (nm)', color = 'black')
matplotlib.pyplot.setp(fig1, 'linewidth', 2.0)
matplotlib.pyplot.setp(fig2, 'linewidth', 2.0)
matplotlib.pyplot.xlim(round(min(lambda_0*1e9)),round(max(lambda_0*1e9)))
matplotlib.pyplot.title("Calculated response of the structure using CMT (log scale)")
matplotlib.pyplot.savefig('bragg_cmt_log'+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

matplotlib.pyplot.figure(3)
fig1 = matplotlib.pyplot.plot(lambda_0*1e9,np.absolute(t), label='Transmission', color='blue')
fig2 = matplotlib.pyplot.plot(lambda_0*1e9,np.absolute(r), label='Reflection', color='red')
matplotlib.pyplot.legend(loc=0)
matplotlib.pyplot.ylabel('Response', color = 'black')
matplotlib.pyplot.xlabel('Wavelength (nm)', color = 'black')
matplotlib.pyplot.setp(fig1, 'linewidth', 2.0)
matplotlib.pyplot.setp(fig2, 'linewidth', 2.0)
matplotlib.pyplot.xlim(round(min(lambda_0*1e9)),round(max(lambda_0*1e9)))
matplotlib.pyplot.title("Calculated response of the structure using CMT (linear scale)")
matplotlib.pyplot.savefig('bragg_cmt_linear'+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

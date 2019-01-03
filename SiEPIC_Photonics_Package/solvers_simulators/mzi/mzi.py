"""
SiEPIC Photonics Package 

Author:     Mustafa Hammood
            Mustafa@siepic.com

            https://github.com/SiEPIC-Kits/SiEPIC_Photonics_Package
            
Solvers and simulators: Mach-Zehnder Interferometer simulator using a simple transfer function of an MZI

Based on L. Chrostowski MATLAB implementation
"""
#%% dependent packages
import matplotlib.pyplot as plt
import numpy as np

#%% user input
# the wavelength range of interest.
wavelength_start = 1500e-9
wavelength_stop = 1600e-9
resolution = 0.001 

# Effective index:
# - as a Taylor expansion around the central wavelength, lam0
lam0 = 1.55
n1=2.4
n2=-1.0
n3=0.0  # these are constants from the waveguide model.

# plot, and check if this is as expected:
L1=100
L2=110  # Units [µm, microns], variable

# Complex propagation constant
alpha = 1e-3   # propagation loss [micron^-1]; constant

#%% analysis

lambda_0 = np.linspace(wavelength_start, wavelength_stop, round((wavelength_stop-wavelength_start)*1e9/resolution))*1e6

def neff(lam):
    return n1 + n2*(lam-lam0) + n3*(lam-lam0)**2

def beta(lam):
    return	2*np.pi*neff(lam)/lam - 1j*alpha/2*np.ones(np.size(lam))

# MZI transfer function
def T_MZI(L1, L2, lam):
    return 0.25*np.abs(np.exp(-1j*beta(lam)*L1) + np.exp(-1j*beta(lam)*L2))**2


#%% application
    
plt.figure()
plt.plot(lambda_0, neff(lambda_0),linewidth=2.0)
plt.xlabel ('Wavelength [$\mu$m]')
plt.ylabel ('Effective index')
plt.autoscale(enable=True, axis='x', tight=True)
plt.autoscale(enable=True, axis='y', tight=True)
plt.title('Effective index model')


plt.figure()
plt.plot(lambda_0, T_MZI(L1, L2, lambda_0), linewidth=3)
plt.xlabel ('Wavelength [$\mu$m]')
plt.ylabel ('Transmission')
plt.autoscale(enable=True, axis='x', tight=True)
plt.autoscale(enable=True, axis='y', tight=True)
plt.title('MZI transfer function')

plt.figure()
T_MZI_dB = 10*np.log10(T_MZI(L1, L2, lambda_0))
plt.plot(lambda_0, T_MZI_dB, linewidth=3)
plt.xlabel ('Wavelength [$\mu$m]')
plt.ylabel ('Transmission [dB]')
plt.autoscale(enable=True, axis='x', tight=True)
plt.autoscale(enable=True, axis='y', tight=True)
plt.title ('MZI transfer function')

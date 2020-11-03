"""
SiEPIC Photonics Package 

Author:     Mustafa Hammood
            Mustafa@siepic.com

            https://github.com/SiEPIC-Kits/SiEPIC_Photonics_Package
            
Solvers and simulators: Bragg simulator using coupled-mode theory (CMT) approach
reference: "Bragg grating based Fabry-Perot filters for characterizing silicon-on-insulator waveguides",
Y. Painchaud, Group IV Photonics, 2012

Based on A. Mistry MATLAB implementation
"""
#%% dependent packages
import numpy as np
import math, cmath, matplotlib
import matplotlib.pyplot as plt
from numpy.lib.scimath import sqrt as csqrt

#%% user input
wavelength_start = 1500e-9
wavelength_stop = 1600e-9
resolution = 0.001

# Grating waveguide compact model (cavity)
# these are polynomial fit constants from a waveguide width of 500 nm
n1_g = 4.077182700600432
n2_g = -0.982556173493906
n3_g = -0.046366956781710

# Cavity waveguide compact model (cavity)
# these are polynomial fit constants from a waveguide width of 500 nm
n1_c = 4.077182700600432
n2_c = -0.982556173493906
n3_c = -0.046366956781710

# grating parameters
kappa = 45000       # coupling strength (/m)
period = 317e-9     # period of pertrubation
N_left = 200        # number of periods (left of cavity)
N_right = 200       # number of periods (right of cavity)

# Cavity Parameters
alpha = 150/4.34
L = period/2    # length of cavity

#%% analysis

j = cmath.sqrt(-1)

lambda_0 = np.linspace(wavelength_start, wavelength_stop, round((wavelength_stop-wavelength_start)*1e9/resolution))
neff = (n1_g + n2_g*(lambda_0*1e6) + n3_g*(lambda_0*1e6)**2)
beta = 2*math.pi*neff/lambda_0

neffc = (n1_c + n2_c*(lambda_0*1e6) + n3_c*(lambda_0*1e6)**2)
betaC = 2*math.pi*neffc/lambda_0

Lg_L = N_left*period
Lg_R = N_right*period
deltaB = 2*math.pi*neff/lambda_0-math.pi/period
omega = csqrt(kappa**2-deltaB**2)


t = []; r = []
for i in range(len(lambda_0)):
    G_L = [
        [np.cosh(omega[i]*Lg_L)-j*deltaB[i]/omega[i]*np.sinh(omega[i]*Lg_L),
         -j*kappa*np.sinh(omega[i]*Lg_L)/omega[i]],
         [j*kappa*np.sinh(omega[i]*Lg_L)/omega[i],
          np.cosh(omega[i]*Lg_L)+j*deltaB[i]/omega[i]*np.sinh(omega[i]*Lg_L)]]
    
    Y = [[np.exp(-alpha*L/2)*np.exp(-j*betaC[i]*L), 0], [0, np.exp(alpha*L/2)*np.exp(j*betaC[i]*L)]]
    
    G_R = [
        [np.cosh(omega[i]*Lg_R)-j*deltaB[i]/omega[i]*np.sinh(omega[i]*Lg_R),
         -j*kappa*np.sinh(omega[i]*Lg_R)/omega[i]],
         [j*kappa*np.sinh(omega[i]*Lg_R)/omega[i],
          np.cosh(omega[i]*Lg_R)+j*deltaB[i]/omega[i]*np.sinh(omega[i]*Lg_R)]]
        
    # matrix multiplication G_L*Y*G_R
    H1 = np.matmul(G_L,Y)
    H = np.matmul(H1,G_R)
    
    t.append(H[0][0]-H[1][0]*H[0][1]/H[1][1])
    r.append(-H[1][0]/H[1][1])
    
# to log scale
T = 10*np.log10(np.absolute(t)**2)
R = 10*np.log10(np.absolute(r)**2)

#%% plot spectrum
matplotlib.pyplot.figure(0)
fig1 = plt.plot(lambda_0*1e9,T, label='Transmission', color='blue')
fig2 = plt.plot(lambda_0*1e9,R, label='Reflection', color='red')
plt.legend(loc=0)
plt.ylabel('Response (dB)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.setp(fig1, 'linewidth', 2.0)
plt.setp(fig2, 'linewidth', 2.0)
plt.xlim(round(min(lambda_0*1e9)),round(max(lambda_0*1e9)))
plt.title("Calculated response of the structure using CMT (log scale)")
plt.savefig('bragg_cmt_log'+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

plt.figure(1)
fig1 = plt.plot(lambda_0*1e9,np.absolute(t), label='Transmission', color='blue')
fig2 = plt.plot(lambda_0*1e9,np.absolute(r), label='Reflection', color='red')
plt.legend(loc=0)
plt.ylabel('Response', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.setp(fig1, 'linewidth', 2.0)
plt.setp(fig2, 'linewidth', 2.0)
plt.xlim(round(min(lambda_0*1e9)),round(max(lambda_0*1e9)))
plt.title("Calculated response of the structure using CMT (linear scale)")
plt.savefig('bragg_cmt_linear'+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

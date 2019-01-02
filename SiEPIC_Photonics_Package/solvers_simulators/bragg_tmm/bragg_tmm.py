"""
SiEPIC Photonics Package 

Author:     Mustafa Hammood
            Mustafa@siepic.com

            https://github.com/SiEPIC-Kits/SiEPIC_Photonics_Package
            
Solvers and simulators: Bragg simulator using transfer matrix method (TMM) approach

"""

#%% dependent packages
import numpy as np
import math, cmath, matplotlib
from numpy.lib.scimath import sqrt as csqrt

#%% user input

# set the wavelength span for the simultion
wavelength_start = 1500e-9
wavelength_stop = 1600e-9
resolution = 0.1

# Grating waveguide compact model (cavity)
# these are polynomial fit constants from a waveguide width of 500 nm
n1_wg = 4.077182700600432
n2_wg = -0.982556173493906
n3_wg = -0.046366956781710

# Cavity waveguide compact model (cavity)
# these are polynomial fit constants from a waveguide width of 500 nm
n1_c = 4.077182700600432
n2_c = -0.982556173493906
n3_c = -0.046366956781710

# grating parameters
period = 316e-9     # period of pertrubation
n_delta = .01      # effective index pertrubation
N_left = 100        # number of periods (left of cavity)
N_right = 100       # number of periods (right of cavity)

# Cavity Parameters
alpha = 0
L = period/2    # length of cavity

#%% Analysis

def HomoWG_Matrix( wavelength, neff):
    beta = 2*math.pi*neff/wavelength-j*alpha/2
    v = [np.exp(j*beta*l), np.exp(-j*beta*l)]
    T_hw = np.diag(v)
    
    return T_hw

def IndexStep_Matrix(neff1, neff2):
    a=(neff1+neff2)/(2*np.sqrt(neff1*neff2))
    b=(neff1-neff2)/(2*np.sqrt(neff1*neff2))
    
    T_is=[[a, b],[b, a]]
    
    return T_is

def Grating_Matrix( wavelength ):
    T_hw1=HomoWG_Matrix(wavelength, n1)
    T_is12=IndexStep_Matrix(n1,n2)
    T_hw2=HomoWG_Matrix(wavelength, n2)
    T_is21=IndexStep_Matrix(n2,n1)
    Tp1 = np.matmul(T_hw1, T_is12)
    Tp2 = np.matmul(T_hw2, T_is21)
    
    Tp = np.matmul(Tp1, np.matrix.transpose(Tp2))
    
    T = np.linalg.matrix_power(Tp,N_left)
    return T
    
def Grating_RT( wavelength ):
    M = Grating_Matrix( wavelength )
    T = np.absolute(1 / M[0][0])**2
    R = 0.5
    
    return [T,R]

j = cmath.sqrt(-1)

l = period/2    
lambda_0 = np.linspace(wavelength_start, wavelength_stop, round((wavelength_stop-wavelength_start)*1e9/resolution))
neff0 = (n1_wg + n2_wg*(lambda_0*1e6) + n3_wg*(lambda_0*1e6)**2)

n1 = neff0 - n_delta/2
n2 = neff0 + n_delta/2

# Grating length
NG_left = N_left * period 
NG_right = N_right * period

R = []
T = []
for i in range(len(lambda_0)):
    [r, t] = Grating_RT(lambda_0[i])
    
    R.append(r)
    T.append(t)
        
    
#%% plot spectrum
matplotlib.pyplot.figure(0)
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
    
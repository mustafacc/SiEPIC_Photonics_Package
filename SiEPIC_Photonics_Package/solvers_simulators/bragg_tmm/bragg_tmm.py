"""
SiEPIC Photonics Package 

Author:     Mustafa Hammood
            Mustafa@siepic.com

            https://github.com/SiEPIC-Kits/SiEPIC_Photonics_Package

fixed by Lukas Chrostowski, 2020/02
            
Solvers and simulators: Bragg simulator using transfer matrix method (TMM) approach

"""

#%% dependent packages
import numpy as np
import math, cmath, matplotlib
import matplotlib.pyplot as plt
from numpy.lib.scimath import sqrt as csqrt
import scipy.io as sio

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
period = 317e-9     # period of pertrubation
n_delta = .05      # effective index pertrubation
lambda_Bragg = 1550e-9 
dw = 50e-9
kappa = -1.53519e19 * dw**2+ 2.2751e12 * dw
n_delta = kappa * lambda_Bragg / 2
print(n_delta)
N_left = 200        # number of periods (left of cavity)
N_right = 200       # number of periods (right of cavity)

# Cavity Parameters
alpha_dBcm = 7     # dB per cm
alpha = np.log(10)*alpha_dBcm/10*100. # per meter

L = period/2    # length of cavity

#%% Analysis

def HomoWG_Matrix( wavelength, neff, l):
    beta = 2*math.pi*neff/wavelength-j*alpha/2
    v = [np.exp(j*beta*l), np.exp(-j*beta*l)]
    T_hw = np.diag(v)
    
    return T_hw

def IndexStep_Matrix(neff1, neff2):
    a=(neff1+neff2)/(2*np.sqrt(neff1*neff2))
    b=(neff1-neff2)/(2*np.sqrt(neff1*neff2))

    T_is=[[a, b],[b, a]]
    return T_is

def Grating_Matrix( wavelength, n1, n2, l ):
    T_hw1=HomoWG_Matrix(wavelength, n1, l)
    T_is12=IndexStep_Matrix(n1,n2)
    T_hw2=HomoWG_Matrix(wavelength, n2, l)
    T_is21=IndexStep_Matrix(n2,n1)


    type = 'Cavity'


    if type == 'Waveguide':
        # 1 cm
        T = HomoWG_Matrix(wavelength, n1, 0.01)

    if type == 'Bragg_left':
        Tp1 = np.matmul(T_hw1, T_is12)
        Tp2 = np.matmul(T_hw2, T_is21)
        Tp_Left = np.matmul(Tp1, Tp2)
        T = np.linalg.matrix_power(Tp_Left,N_left) 

    if type == 'Bragg_right':
        Tp1 = np.matmul(T_hw1, T_is12)
        Tp2 = np.matmul(T_hw2, T_is21)
        Tp_Right = np.matmul(Tp1, Tp2)

        T = np.linalg.matrix_power(Tp_Right,N_right)

    if type == 'Cavity':
        Tp1 = np.matmul(T_hw1, T_is12)
        Tp2 = np.matmul(T_hw2, T_is21)
        Tp_Left = np.matmul(Tp1, Tp2)

        T_cavity = HomoWG_Matrix(wavelength, n1, l)

        Tp1 = np.matmul(T_hw1, T_is12)
        Tp2 = np.matmul(T_hw2, T_is21)
        Tp_Right = np.matmul(Tp1, Tp2)

        T = np.matmul(np.matmul( np.linalg.matrix_power(Tp_Left,N_left), T_cavity), np.linalg.matrix_power(Tp_Right,N_right))

    return T

def Grating_RT( wavelength, n1, n2, l ):
    M = Grating_Matrix( wavelength, n1, n2, l )
    T = np.absolute(1 / M[0][0])**2
    R = np.absolute(M[1][0]/M[0][0])**2. # or M[0][1]? 
    return [T,R]

j = cmath.sqrt(-1)

l = period/2    
lambda_0 = np.linspace(wavelength_start, wavelength_stop, round((wavelength_stop-wavelength_start)*1e9/resolution))
neff0 = (n1_wg + n2_wg*(lambda_0*1e6) + n3_wg*(lambda_0*1e6)**2)

n1 = neff0 - n_delta/2
n2 = neff0 + n_delta/2

# Grating length
L_left = N_left * period 
L_right = N_right * period

R = []
T = []
for i in range(len(lambda_0)):
    [t, r] = Grating_RT(lambda_0[i], n1[i], n2[i], l)
    
    R.append(r)
    T.append(t)

sio.savemat('bragg_tmm.mat', {'R':R, 'T':T, 'lambda_0': lambda_0})

sio.loadmat('bragg_interconnect.mat')

#%% plot spectrum
plt.figure(0)
fig1 = plt.plot(lambda_0*1e9,10*np.log10(T), label='Transmission', color='blue')
fig2 = plt.plot(lambda_0*1e9,10*np.log10(R), label='Reflection', color='red')
plt.legend(loc=0)
plt.ylabel('Response (dB)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.setp(fig1, 'linewidth', 2.0)
plt.setp(fig2, 'linewidth', 2.0)
plt.xlim(round(min(lambda_0*1e9)),round(max(lambda_0*1e9)))
plt.title("Calculated response of the structure using TMM (dB scale)")
plt.savefig('bragg_tmm_dB'+'.pdf')
    
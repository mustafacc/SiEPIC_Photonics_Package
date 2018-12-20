"""
SiEPIC Photonics Package 

Author:     Mustafa Hammood
            Mustafa@siepic.com

            https://github.com/SiEPIC-Kits/SiEPIC_Photonics_Package
            
Solvers and simulators: Ring designer script

Based on H. Shoman MATLAB implementation
"""

#%% dependent packages
import numpy as np
import math, cmath
import matplotlib.pyplot as plt
from numpy.lib.scimath import sqrt as csqrt

#%% user input
wavelength_start = 1530e-9
wavelength_stop = 1570e-9
resolution = 0.01

# waveguide compact mode
# these are polynomial fit constants from a waveguide width of 500 nm
n1 = 4.077182700600432
n2 = -0.982556173493906
n3 = -0.046366956781710

# waveguide loss (dB/cm)
alpha = 4

# coupling coefficients (power coupling coefficient)
k1 = .2; k2= 0.0123; k3 = 0.2;
kappa = [k1, k2, k3]

# rings radii (um)
r1 = 15e-6; r2 = (4/5)*r1;
R = [r1,r2]

# phase shift (radians)
phi = [0,0]

#%% ring transfer function
def RingS( kappa, phi, L, beta, alpha):
    j = cmath.sqrt(-1)
    gamma = 10**(-alpha*L/20)
    zeta  = gamma*np.exp(-j*phi)*np.exp(-j*beta*L)
    sqrtzeta  = math.sqrt(gamma)*np.exp(-j*phi/2)*np.exp(-j*beta*L/2)
    s     = math.sqrt(kappa)
    c     = math.sqrt(1-kappa)
    
    t1N = -j*s*sqrtzeta
    rN1 = c*zeta
    r1N = c
    tN1 = t1N
    
    S = [[t1N, rN1],[r1N, tN1]]
    return S

def MtoS( M ):
    t1N = M[0][0]*M[1][1]-M[0][1]*M[1][0]
    rN1 = M[0][1]
    r1N = -M[1][0]
    tN1 = 1;
    S_temp  = np.array([[t1N, rN1],[r1N, tN1]])
    S = (1/M[1][1]) * S_temp
    return S

def StoM( S ):
    A = S[0][0]*S[1][1]-S[0][1]*S[1][0]
    B = S[0][1]
    C = -S[1][0]
    D = 1
    M_temp = np.array([[A, B],[C, D]])
    M = (1/S[1][1])* M_temp
    return M

#%% theoretical analysis
# number of rings
nor = len(R
          )
R.append(0)
phi.append(0)
L = [i * (2*math.pi) for i in R]
lambda_0 = np.linspace(wavelength_start, wavelength_stop, round((wavelength_stop-wavelength_start)*1e9/resolution))

# effective index fit
neff = (n1 + n2*(lambda_0*1e6) + n3*(lambda_0*1e6)**2)
beta0 = 2*math.pi*neff/lambda_0

# alpha in dB/m
alpha = alpha * 100

t1N = [];r1N = [];rN1 = [];tN1 = []
for beta in beta0:
    S = RingS(kappa[0],phi[0],L[0],beta,alpha)
    M = StoM(S)
    
    for no in range(nor):
        S = RingS(kappa[no+1],phi[no+1],L[no+1],beta,alpha)
        Mtemp = StoM(S)
        M = np.matmul(Mtemp, M)
        
    S = MtoS( M )
    t1N.append(S[0][0]) # Electric field Drop
    rN1.append(S[0][1])
    r1N.append(S[1][0]) # Electric field Through
    tN1.append(S[1][1])
    
#%% power
Drop = t1N; D = np.absolute( Drop )**2; DdB = 10*np.log10(D)
Thru = r1N; T = np.absolute( Thru )**2; TdB = 10*np.log10(T)
TOT = D + T; TOTdB = 10*np.log10(TOT)

#%% phase
Dphi = np.angle(Drop); Dphi = np.unwrap(Dphi)
Tphi = np.angle(Thru); Tphi = np.unwrap(Tphi)

#%% group delay
c      = 299792458
f      = c/lambda_0
omega  = 2*math.pi*f
Tdelay = -np.diff(Tphi)/np.diff(omega)
Ddelay = -np.diff(Dphi)/np.diff(omega)

#%% dispersion
Tdispersion = np.diff(Tdelay)/np.diff(omega[1:len(omega)])
Ddispersion = np.diff(Ddelay)/np.diff(omega[1:len(omega)])

#%% plot spectrums
# power
plt.figure(0)
thru = plt.plot(lambda_0*1e9,TdB, label='Through', color='blue')
drop = plt.plot(lambda_0*1e9,DdB, label='Drop', color='red')
tot = plt.plot(lambda_0*1e9,TOTdB, label = 'Total', color='black')
plt.legend(loc=0)
plt.ylabel('Response (dB)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.setp(thru, 'linewidth', .5)
plt.setp(drop, 'linewidth', .5)
plt.setp(tot, 'linewidth', .5)
plt.xlim(round(min(lambda_0*1e9)),round(max(lambda_0*1e9)))
plt.title("Transmission spectrum of the rings system (log scale)")
plt.savefig('rings_spectrum_log'+'.pdf')

# phase
plt.figure(1)
thruPhi = plt.plot(lambda_0*1e9,Tphi/math.pi, label='Through phase', color='blue')
dropPhi = plt.plot(lambda_0*1e9,Dphi/math.pi, label='Drop phase', color='red')
plt.legend(loc=0)
plt.ylabel('Phase (pi rad)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.setp(thruPhi, 'linewidth', .5)
plt.setp(dropPhi, 'linewidth', .5)
plt.xlim(round(min(lambda_0*1e9)),round(max(lambda_0*1e9)))
plt.title("Phase of the rings system (unwrapped)")
plt.savefig('rings_phase'+'.pdf')

# group delay
plt.figure(2)
lambda_1 = lambda_0[0:len(lambda_0)-1]
thruDelay = plt.plot(lambda_1*1e9,Tdelay*1e12, label='Through port delay', color='blue')
dropDelay = plt.plot(lambda_1*1e9,Ddelay*1e12, label='Drop port delay', color='red')
plt.legend(loc=0)
plt.ylabel('Delay (ps)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.setp(thruDelay, 'linewidth', .5)
plt.setp(dropDelay, 'linewidth', .5)
plt.xlim(round(min(lambda_1*1e9)),round(max(lambda_1*1e9)))
plt.title("Delay of the rings system")
plt.savefig('rings_delay'+'.pdf')

# dispersion
plt.figure(3)
lambda_2 = lambda_0[0:len(lambda_0)-2]
thruDispersion = plt.plot(lambda_2*1e9,Tdispersion*1e12, label='Through port dispersion', color='blue')
dropDispersion = plt.plot(lambda_2*1e9,Ddispersion*1e12, label='Drop port dispersion', color='red')
plt.legend(loc=0)
plt.ylabel('Group delay dispersion (s^2/rad)', color = 'black')
plt.xlabel('Wavelength (nm)', color = 'black')
plt.setp(thruDispersion, 'linewidth', .5)
plt.setp(dropDispersion, 'linewidth', .5)
plt.xlim(round(min(lambda_2*1e9)),round(max(lambda_2*1e9)))
plt.title("Group delay dispersion of the rings system")
plt.savefig('rings_dispersion'+'.pdf')
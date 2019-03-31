"""
SiEPIC Photonics Package

Author:     Mustafa Hammood
            Mustafa@siepic.com
            
            https://github.com/SiEPIC-Kits/SiEPIC_Photonics_Package

Module:     PCM Analysis 

Fetches measurement data of a manufactured chip, analyzes the process control monitor (PCM) structures to assess
the quality of the fabricated chip.
"""
#%% import package and installed dependent packages
import sys, os
# go up two directories
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(dir_path)))

import SiEPIC_Photonics_Package as SiEPIC_PP

#%%
def PCM_analysis( URL ):
    return

# analyze the losses of straight waveguides by cutback method
def WGloss_straight():
    return

# analyze the losses of spiral waveguides by cutback method
def WGloss_spiral():
    return

# analyze the losses of sub-wavelength waveguides by cutback method
def WGloss_SWG():
    return

# analyze the bandwidth and central wavelength of Bragg gratings as a function of corrugation strength
def Bragg_sweep():
    return

# analyze the losses of contra-directional coupler (drop port) by cutback method
def contraDC_loss():
    return
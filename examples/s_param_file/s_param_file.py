"""
SiEPIC Analysis Package

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example:    Write a lumerical N-port S-parameters file format using input data 
"""

import siepic_analysis_package as siap
import numpy as np

sparams = siap.lumerical.S_param_file()
sparams.n_ports = 2
sparams.wavl = [1500e-9, 1600e-9, 0.1e-9]

# generate dummy s-parameters data
# data format [S11, S12, ...., S21, S22, ....]
linspace = np.linspace(0,10*np.pi,sparams.npoints())
S11 = [0.3*np.sin(linspace)+0.3, 0*linspace] # [real, imag]
S12 = [0.5*np.cos(linspace)+0.5, 0*linspace]
S22= np.array(S11)/2; S21 = np.array(S12)/2
sparams.data = [S11, S12, S21, S22]

sparams.write_S()
sparams.visualize()

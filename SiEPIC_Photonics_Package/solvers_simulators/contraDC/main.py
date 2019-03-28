"""
    Contra-directional coupler Lumerical simulation flow
    see [] for documentation

    Author: Mustafa Hammood   ; mustafa@siepic.com   ; mustafa@ece.ubc.ca
    SiEPIC Kits Ltd. 2019     ; University of British Columbia

"""

import dispersion_analysis, contraDC_CMT_TMM, analysis

#%% device parameters class constructor
class contra_DC():
    def __init__(self, *args):
        # physical geometry parameters
        self.w1 = 560e-9
        self.w2 = 440e-9
        self.dW1 = 24e-9
        self.dW2 = 24e-9
        self.gap = 100e-9
        self.period = 318e-9
        self.N = 1000
 
        self.thick_si = 220e-9
        
        self.slab = False
        self.thick_slab = 90e-9
        
        self.sinusoidal = False
        
        self.apodization = 2

        #behavioral parameters 
        self.pol = 'TE' # TE or TM
        self.alpha = 10
        
        #leave kappas as default if you wish the script to calculate it based on bandstructure
        self.kappa_contra = 30000 
        self.kappa_self1 = 3000
        self.kappa_self2 = 3000

    def results(self, *args):
        self.E_thru = 0
        self.E_drop = 0
        self.wavelength = 0
        self.TransferMatrix = 0

#%% simulation parameters class constructor
class simulation():
    def __init__(self, *args):
        # make sure range is large enouh to capture all Bragg coupling conditions (both self-Bragg and contra-coupling)
        self.lambda_start = 1480e-9
        self.lambda_end = 1600e-9
        self.resolution = 501
        
        self.deviceTemp = 300
        self.chipTemp = 300
        
        self.central_lambda = 1550e-9

#%% instantiate the class constructors        
device = contra_DC()
simulation = simulation()

#%% main program
[waveguides, simulation] = dispersion_analysis.phaseMatch_analysis(device, simulation)
device = dispersion_analysis.kappa_analysis(device, simulation, waveguides, sim_type = 'EME')
device = contraDC_CMT_TMM.contraDC_model(device, simulation, waveguides)

#%% analysis and export parameters
analysis.plot_all(device, simulation)
analysis.gen_sparams(device, simulation)
"""
    Contra-directional coupler Lumerical simulation flow
    see URL for documentation
    https://github.com/SiEPIC-Kits/SiEPIC_Photonics_Package/tree/master/SiEPIC_Photonics_Package/solvers_simulators/contraDC/Documentation

"""

import contraDC_CMT_TMM, analysis, dispersion_analysis

#%% device parameters class constructor
class contra_DC():
    def __init__(self, *args):
        # physical geometry parameters
        self.w1 = 570e-9
        self.w2 = 430e-9
        self.dW1 = 40e-9
        self.dW2 = 20e-9
        self.gap = 200e-9        
        self.period1 = 310e-9
        self.period2 = 330e-9
        
        self.N = 10000

        
        self.thick_si = 220e-9
        
        self.slab = False
        self.thick_slab = 90e-9
        
        self.sinusoidal = False
        
        self.apodization = 0

        #behavioral parameters 
        self.pol = 'TE' # TE or TM
        self.alpha = 1.4
        
        #leave kappas as default if you wish the script to calculate it based on bandstructure
        self.kappa_contra = 35000 
        self.kappa_self1 = 1000
        self.kappa_self2 = 1000
        self.period = abs(self.period1+self.period2)/2
    def results(self, *args):
        self.E_thru = 0
        self.E_drop = 0
        self.wavelength = 0
        self.TransferMatrix = 0

#%% simulation parameters class constructor
class simulation():
    def __init__(self, *args):
        # make sure range is large enouh to capture all Bragg coupling conditions (both self-Bragg and contra-coupling)
        self.lambda_start = 1500e-9
        self.lambda_end = 1600e-9
        self.resolution = 5001
        
        self.deviceTemp = 300
        self.chipTemp = 300
        
        self.central_lambda = 1550e-9

#%% instantiate the class constructors        
device = contra_DC()
simulation = simulation()

#%% main program
[waveguides, simulation] = dispersion_analysis.phaseMatch_analysis(device, simulation)
device = dispersion_analysis.kappa_analysis(device, simulation, waveguides, sim_type = 'EME', close = False)
device = contraDC_CMT_TMM.contraDC_model(device, simulation, waveguides)

#%% analysis and export parameters
analysis.plot_all(device, simulation)
S = analysis.gen_sparams(device, simulation)
analysis.performance(S)
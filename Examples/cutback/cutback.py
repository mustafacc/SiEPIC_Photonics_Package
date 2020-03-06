"""
SiEPIC Photonics Package 

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example:    Application of SiEPIC_PP cutback function
            to extract the porpagation losses from three different length spirals.
"""

#%% import package and installed dependent packages
import sys, os
# go up two directories
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(dir_path)))

import SiEPIC_Photonics_Package as SiEPIC_PP
from SiEPIC_Photonics_Package.setup import *

#%% download .mat files from GitHub repo and parse it to a variable (data)
# responses to extract losses from
# in this example, file name units are in um (microns)
unit = [0, 5000, 10000, 30000]

# divide by 10000 to see result in dB/cm
unit_cm = [i/10000 for i in unit]

input_data_response = []

for i in unit:
    file_name = 'SpiralWG'+str(i)+'TE'
    file_extension = '.mat'
    url = 'https://github.com/SiEPIC-Kits/SiEPIC_Photonics_Package/blob/master/Examples/'+file_name+file_extension+'?raw=true'
    PORT = 1
    input_data_response.append( SiEPIC_PP.core.download_response(url,PORT) )

#%% apply SiEPIC_PP cutback extraction function
[insertion_loss_wavelength, insertion_loss_fit, insertion_loss_raw] = SiEPIC_PP.core.cutback( input_data_response, unit_cm, 1550e-9 )

#%% plot responses and save pdf

# plot all cutback structures responses
matplotlib.pyplot.figure(2)
wavelength = input_data_response[0][0]*1e9
fig0 = matplotlib.pyplot.plot(wavelength,input_data_response[0][1], label='L = 0', color='blue')
fig1 = matplotlib.pyplot.plot(wavelength,input_data_response[1][1], label='L = 5000 um', color='black')
fig2 = matplotlib.pyplot.plot(wavelength,input_data_response[2][1], label='L = 10000 um', color='green')
fig3 = matplotlib.pyplot.plot(wavelength,input_data_response[3][1], label='L = 30000 um', color='red')
matplotlib.pyplot.legend(loc=0)
matplotlib.pyplot.ylabel('Power (dBm)', color = 'black')
matplotlib.pyplot.xlabel('Wavelength (nm)', color = 'black')
matplotlib.pyplot.xlim(round(min(wavelength)),round(max(wavelength)))
matplotlib.pyplot.title("Raw measurement of cutback structures")
matplotlib.pyplot.savefig('cutback_measurement'+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

# Insertion loss vs wavelength plot
matplotlib.pyplot.figure(1)
linspace = numpy.linspace(unit_cm[0],unit_cm[len(unit_cm)-1], len(insertion_loss_fit))
fig1 = matplotlib.pyplot.plot(linspace,insertion_loss_raw, label='Insertion loss (raw)', color='blue')
fig2 = matplotlib.pyplot.plot(linspace,insertion_loss_fit, label='Insertion loss (fit)', color='red')
matplotlib.pyplot.legend(loc=0)
matplotlib.pyplot.ylabel('Loss (dB/cm)', color = 'black')
matplotlib.pyplot.xlabel('Wavelength (nm)', color = 'black')
matplotlib.pyplot.setp(fig2, 'linewidth', 4.0)
matplotlib.pyplot.xlim(round(min(unit_cm)),round(max(unit_cm)))
matplotlib.pyplot.title("Insertion losses using the cut-back method")
matplotlib.pyplot.savefig('cutback'+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})


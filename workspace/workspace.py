"""
SiEPIC Photonics Package 

Author:     Mustafa Hammood
            Mustafa@ece.ubc.ca

Example:    Application of SiEPIC_PP cutback function
            to extract the porpagation losses from three different length spirals.
"""

#%% import package and installed dependent packages
import sys, os
# go up two directories
dir_path = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(os.path.dirname(os.path.dirname(dir_path)))

import SiEPIC_Photonics_Package as SiEPIC_PP
from SiEPIC_Photonics_Package.setup import *

#%% download .mat files from GitHub repo and parse it to a variable (data)
# responses to extract losses from
# in this example, file name units are in um (microns)
unit = [0, 7418, 14618, 21818, 29018]

# divide by 10000 to see result in dB/cm
unit_cm = [i/10000 for i in unit]

input_data_response = []

url = 'https://www.dropbox.com/s/lfd5hx2gns1rv34/GC_BR.mat?dl=1'
PORT = 1
input_data_response.append( SiEPIC_PP.core.download_response(url,PORT))

url = 'https://www.dropbox.com/s/1mszqdj9em94302/L7418.mat?dl=1'
PORT = 1
input_data_response.append( SiEPIC_PP.core.download_response(url,PORT))

url = 'https://www.dropbox.com/s/8flh27yfquho8j6/L14618.mat?dl=1'
PORT = 1
input_data_response.append( SiEPIC_PP.core.download_response(url,PORT))

url = 'https://www.dropbox.com/s/wphd40v4p6dx4bs/L21818.mat?dl=1'
PORT = 1
input_data_response.append( SiEPIC_PP.core.download_response(url,PORT))

url = 'https://www.dropbox.com/s/t8317sdrnu8xgq7/L29018.mat?dl=1'
PORT = 1
input_data_response.append( SiEPIC_PP.core.download_response(url,PORT))

#%% apply SiEPIC_PP cutback extraction function
[insertion_loss_wavelength, insertion_loss_fit, insertion_loss_raw] = SiEPIC_PP.core.cutback( input_data_response, unit_cm, 1550e-9 )

#%% plot responses and save pdf
# Insertion loss vs wavelength plot
matplotlib.pyplot.figure(0)
wavelength = input_data_response[0][0]*1e9
fig1 = matplotlib.pyplot.plot(wavelength,insertion_loss_raw, label='Insertion loss (raw)', color='blue')
fig2 = matplotlib.pyplot.plot(wavelength,insertion_loss_fit, label='Insertion loss (fit)', color='red')
matplotlib.pyplot.legend(loc=0)
matplotlib.pyplot.ylabel('Loss (dB/cm)', color = 'black')
matplotlib.pyplot.xlabel('Wavelength (nm)', color = 'black')
matplotlib.pyplot.setp(fig2, 'linewidth', 3.0)
matplotlib.pyplot.xlim(round(min(wavelength)),round(max(wavelength)))
matplotlib.pyplot.title("Insertion losses using the cut-back method")
matplotlib.pyplot.savefig('cutback_loss'+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})


matplotlib.pyplot.figure(1)
fig1 = matplotlib.pyplot.plot(wavelength,input_data_response[0][1], label='L = 0', color='blue')
fig2 = matplotlib.pyplot.plot(wavelength,input_data_response[1][1], label='L = 7418 um', color='red')
fig3 = matplotlib.pyplot.plot(wavelength,input_data_response[2][1], label='L = 14618 um', color='black')
fig4 = matplotlib.pyplot.plot(wavelength,input_data_response[3][1], label='L = 21818 um', color='green')
fig5 = matplotlib.pyplot.plot(wavelength,input_data_response[3][1], label='L = 29018 um', color='green')
matplotlib.pyplot.legend(loc=0)
matplotlib.pyplot.ylabel('Power (dBm)', color = 'black')
matplotlib.pyplot.xlabel('Wavelength (nm)', color = 'black')
matplotlib.pyplot.xlim(round(min(wavelength)),round(max(wavelength)))
matplotlib.pyplot.title("Insertion losses using the cut-back method")
matplotlib.pyplot.savefig('cutback'+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})


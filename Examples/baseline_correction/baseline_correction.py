"""
SiEPIC Photonics Package 

Author:     Mustafa Hammood
            Mustafa@ece.ubc.ca

Example:    Application of SiEPIC_PP baseline correction function
"""

#%% import package and installed dependent packages
import sys, os
# go up two directories
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(dir_path)))

import SiEPIC_Photonics_Package as SiEPIC_PP
from SiEPIC_Photonics_Package.setup import *

#%% download .mat file from GitHub repo and parse it to a variable (data)
file_name = 'MZI_data'
file_extension = '.mat'
url = 'https://github.com/SiEPIC-Kits/SiEPIC_Photonics_Package/blob/master/Examples/'+file_name+file_extension+'?raw=true'
r = requests.get(url,allow_redirects=True)
with open(file_name+file_extension, 'wb') as f:
    f.write(r.content)
    
data = scipy.io.loadmat(file_name+file_extension)
PORT = 0

wavelength = data['scanResults'][0][PORT][0][:,0]
power = data['scanResults'][0][PORT][0][:,1]

#%% apply SiEPIC_PP baseline correction function
input_response= [wavelength,power]
[power_corrected, pfit] = SiEPIC_PP.core.baseline_correction( input_response )

#%% plot response and save pdf
# raw response with baseline fit
matplotlib.pyplot.figure(0)
fig1 = matplotlib.pyplot.plot(wavelength,power, label='Raw data', color='red')
fig2 = matplotlib.pyplot.plot(wavelength,pfit, label = 'Data baseline', color='blue')
matplotlib.pyplot.legend(loc=0)
matplotlib.pyplot.ylabel('Power (dBm)', color = 'black')
matplotlib.pyplot.xlabel('Wavelength (nm)', color = 'black')
matplotlib.pyplot.setp(fig1, 'linewidth', 2.0)
matplotlib.pyplot.setp(fig2, 'linewidth', 2.0)
matplotlib.pyplot.xlim(round(min(wavelength)),round(max(wavelength)))
matplotlib.pyplot.title("Experimental data (raw)")
matplotlib.pyplot.savefig(file_name+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

# corrected response
matplotlib.pyplot.figure(1)
fig = matplotlib.pyplot.plot(wavelength,power_corrected)
matplotlib.pyplot.ylabel('Power (dBm)', color = 'black')
matplotlib.pyplot.xlabel('Wavelength (nm)', color = 'black')
matplotlib.pyplot.setp(fig, 'color', 'r', 'linewidth', 2.0)
matplotlib.pyplot.xlim(round(min(wavelength)),round(max(wavelength)))
matplotlib.pyplot.title("Experimental data (baseline corrected)")
matplotlib.pyplot.savefig(file_name+'_baseline'+'.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

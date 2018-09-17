"""
SiEPIC Photonics Package 

Author:     Mustafa Hammood
            Mustafa@ece.ubc.ca

Module:     Workspace
"""

#%% import package and installed dependent packages
import sys, os
# go up two directories
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath((os.path.dirname(dir_path))))))

import SiEPIC_Photonics_Package as SiEPIC_PP
from SiEPIC_Photonics_Package.setup import *

#%% download .mat file from GitHub repo and parse it to a variable (data)
filename = 'MZI_data.mat'
url = 'https://github.com/mustafacc/SiEPIC_Photonics_Package/blob/master/Examples/'+filename+'?raw=true'
r = requests.get(url,allow_redirects=True)
with open('MZI_data.mat', 'wb') as f:
    f.write(r.content)
    
data = scipy.io.loadmat('MZI_data.mat')
PORT = 0

wavelength = data['scanResults'][0][PORT][0][:,0]
power = data['scanResults'][0][PORT][0][:,1]

#%% plot response in a fancy window
fig = matplotlib.pyplot.plot(wavelength,power)
matplotlib.pyplot.ylabel('Power (dBm)', fontsize = 22, color = 'black')
matplotlib.pyplot.xlabel('Wavelength (nm)', fontsize = 22, color = 'black')
matplotlib.pyplot.setp(fig, 'color', 'r', 'linewidth', 2.0)
matplotlib.pyplot.xlim(min(wavelength),max(wavelength))
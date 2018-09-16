"""
SiEPIC Photonics Package

Author:     Mustafa Hammood
            Mustafa@ece.ubc.ca

Module:     __init__.py package identifer
"""
#%% package identifier

class pkg_id:
    __version__ = "0.0.1"
    name = "SiEPIC_Photonics_Package"
    author="Mustafa Hammood"
    author_email="Mustafa@ece.ubc.ca"
    description="A Python (v3.6.5) package to be used in the UBC Photonics Group"
    url="https://github.com/mustafacc/SiEPIC_Photonics_Package"
    
print("\n"+"Initializing "+ str(pkg_id.name) + "_v"+ pkg_id.__version__+"\n")

from . import core, setup

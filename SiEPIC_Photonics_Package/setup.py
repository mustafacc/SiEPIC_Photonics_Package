"""
SiEPIC Photonics Package

Author:     Mustafa Hammood
            Mustafa@siepic.com
            
            https://github.com/SiEPIC-Kits/SiEPIC_Photonics_Package

Module:     Intialize and setup information for SiEPIC PP
"""

#%% import dependent packages

import importlib

packages = ["numpy", "scipy", "scipy.io", "matplotlib", "pyparsing", "requests"]


for lib in packages:
    try:
        globals()[lib] = importlib.import_module(lib)
    except ImportError:
        from pip._internal import main
        main(['install', '--user', lib])
        globals()[lib] = importlib.import_module(lib)

print("Imported dependicies: ", packages)
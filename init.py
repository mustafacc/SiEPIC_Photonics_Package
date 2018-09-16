"""
SiEPIC Photonics Library

Author:     Mustafa Hammood
            Mustafa@ece.ubc.ca

Module:     Intialize the required packages
"""

#%% library version
version= 0.0

print("\n"+"Intializing SiEPIC Photonics Library v"+ str(version)+"\n")

#%% import required packages

import importlib

packages = ["numpy", "scipy", "matplotlib.pyplot", "pyparsing"]

for lib in packages:
    try:
        globals()[lib] = importlib.import_module(lib)
    except ImportError:
        import pip
        pip.main(['install', '--user', i])
        globals()[lib] = importlib.import_module(lib)
        
print("Imported packages: ", packages)

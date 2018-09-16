"""
SiEPIC Photonics Package

Author:     Mustafa Hammood
            Mustafa@ece.ubc.ca

Module:     Intialize the dependent packages of SiEPIC PP
"""
#%% import dependent packages

import importlib

packages = ["numpy", "scipy", "matplotlib.pyplot", "pyparsing"]

for lib in packages:
    try:
        globals()[lib] = importlib.import_module(lib)
    except ImportError:
        from pip._internal import main
        main(['install', '--user', lib])
        globals()[lib] = importlib.import_module(lib)
        
print("Imported packages: ", packages)
"""
SiEPIC Photonics Package

Author:     Mustafa Hammood
            Mustafa@ece.ubc.ca

Module:     Intialize and setup information for SiEPIC PP
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

print("Imported dependicies: ", packages)
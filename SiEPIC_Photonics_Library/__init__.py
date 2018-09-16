"""
SiEPIC Photonics Package

Author:     Mustafa Hammood
            Mustafa@ece.ubc.ca

Module:     __init__.py package identifer
"""

#%% import all modules in directory
import os
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__(module[:-3], locals(), globals())
del module

#%% library version
__version__ = 0.0

print("\n"+"Intializing SiEPIC Photonics Package v"+ str(__version__)+"\n")


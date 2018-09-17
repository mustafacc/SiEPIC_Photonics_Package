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

#%% iteratively import all modules in directory
import importlib
from os import listdir
from os.path import abspath, dirname, isfile, join
# get location of __init__.py
init_path = abspath(__file__)
# get folder name of __init__.py
init_dir = dirname(init_path)
# get all python files
py_files = [file_name.replace(".py", "") for file_name in listdir(init_dir) \
           if isfile(join(init_dir, file_name)) and ".py" in file_name and not ".pyc" in file_name]
# remove this __init__ file from the list
py_files.remove("__init__")

__all__ = py_files

for lib in __all__:
    i = importlib.import_module('.'+lib,pkg_id.name)

print("Modules loaded: "+str(__all__))
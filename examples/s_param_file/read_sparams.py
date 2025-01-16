"""
SiEPIC Compiler
Example loading S-parameters lumerical format (.dat) file.

@author: Mustafa Hammood
"""
#%%
import os
from siepic_analysis_package.lumerical import process_dat

if __name__ == "__main__":
    sparams_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "grating_coupler.dat",
    )
    grating_coupler = process_dat(file_path=sparams_dir, name="grating_coupler")
    grating_coupler.plot()  # plot all ports

    grating_coupler.data[1].plot()  # plot S12222


# %%

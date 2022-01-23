
"""
SiEPIC Analysis Package

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example:    Using processCSV function to plot a measurement
"""

import siepic_analysis_package as siap

f_measurement = r"24-Aug-2021 22.22.52_1.csv"

device = siap.analysis.processCSV(f_measurement)
device.plot(channels=[0,1,2], savepdf=True, savepng=False)
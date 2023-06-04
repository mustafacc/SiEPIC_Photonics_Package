
"""
SiEPIC Analysis Package

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example:    Using processCSV function to plot a measurement
"""
import sys
sys.path.append(r'C:\Users\musta\Documents\GitHub\SiEPIC_Photonics_Package')
import siepic_analysis_package as siap

f_measurement = r"19-Mar-2022 22.00.06_1.csv"

device = siap.analysis.processCSV(f_measurement)
device.plot(channels=[2], wavlRange = [1500, 1580], savepdf=True, savepng=False)
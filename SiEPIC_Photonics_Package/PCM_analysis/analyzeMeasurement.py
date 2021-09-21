# -*- coding: utf-8 -*-
"""
Example application of CSVanalysis to process an entire measurement set.

Created on Sat Aug 28 21:29:02 2021

@author: Mustafa
"""

import CSVanalysis as csva
import os
from datetime import datetime

dir_measurement = r"C:\Users\musta\Nextcloud\Shared\Lab data LC group\MLP01-4060-Scylla\Mustafa\20210819_ANT_SiN\measurement_vacuum\ant_sin_coords\DieCarrier A\1\sweepLaser"

dir_results = "measurement_results"
cwd = os.getcwd()
path = os.path.join(cwd, dir_results)
try:
    os.mkdir(path)
except FileExistsError:
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    path += '_'+current_time
    os.mkdir(path)

os.chdir(path)

for subdir, dirs, files in os.walk(dir_measurement):
    for file in files:
        device = csva.processCSV(subdir+'\\'+file)
        if device.deviceID.startswith("rings3"):
            device.plot(channels=[1], pwrRange=[-70, -20],
                        wavlRange=[1560, 1563], savepdf=False, savepng=False)

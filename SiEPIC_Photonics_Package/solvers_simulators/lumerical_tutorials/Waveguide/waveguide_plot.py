# -*- coding: utf-8 -*-
"""
Plot the effective index and group index curves for a given waveguide CML.

@author: Mustafa Hammood
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

mpl.style.use('ggplot')  # set plotting style

fname = 'wg_strip_o_350'  # data to be loaded
npts = 10  # number of points to plot

data = [float(i) for i in open(fname+'.txt', 'r').read().rstrip().split(',')]
wavl_range = [data[0], data[1]]
coefficients = [data[4], data[3], data[2]]
poly = np.poly1d(coefficients)

wavl = np.linspace(wavl_range[0], wavl_range[1], npts)
neff = poly(wavl)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
ax.set_xlabel('Wavelength (nm)')
ax.set_ylabel('Effective index')
ax.set_title("Waveguide: " + fname)
ax.grid('on')
ax.plot(wavl*1e9, neff, label=fname)
ax.legend()
fig.savefig(fname+'.pdf')
fig.savefig(fname+'.png')

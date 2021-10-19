# -*- coding: utf-8 -*-
"""
Plot the effective index and group index curves for a given waveguide CML.

@author: Mustafa Hammood
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

#mpl.style.use('ggplot')  # set plotting style

fname = 'wg_strip_o_mm_2000'  # data to be loaded
npts = 10  # number of points to plot

data = [float(i) for i in open(fname+'.txt', 'r').read().rstrip().split(',')]
wavl_range = [data[0], data[1]]
coefficients_neff = [data[4], data[3], data[2]]
poly_neff = np.poly1d(coefficients_neff)
coefficients_ng = [data[7], data[6], data[5]]
poly_ng = np.poly1d(coefficients_ng)

wavl = np.linspace(wavl_range[0], wavl_range[1], npts)
neff = poly_neff(wavl)
ng = poly_ng(wavl)

fig = plt.figure(figsize=(8, 6))
ax1 = fig.add_subplot(111)
ax1.set_xlabel('Wavelength (nm)')
ax1.set_ylabel('Effective index', color="red")
ax1.set_title("Waveguide: " + fname)
ax1.grid('off')
ax1.plot(wavl*1e9, neff, label='Effective index', color="red")


ax2 = ax1.twinx()
ax2.set_ylabel('Group index', color="blue")
ax2.plot(wavl*1e9, ng, label='Group index', color="blue")
fig.legend()

fig.savefig(fname+'.pdf')
fig.savefig(fname+'.png')

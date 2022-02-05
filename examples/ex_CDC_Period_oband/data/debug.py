
#%% method step 1
data = device.pwr[port_thru]
data_envelope = device.pwr[port_drop]
wavl = device.wavl

plt.figure()
plt.plot(wavl, data, label = 'Input data')
plt.plot(wavl, data_envelope, label = "Calibration reference")
plt.legend(loc=0)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Power (dBm)")
plt.savefig('method_1'+'.pdf')
# %% method step 2
N_seg = 25
arrSize = np.size(device.pwr[port_thru])

steps = int(np.floor(arrSize/N_seg))

x = []
y = []
for i in range(N_seg):
    idx = i * steps
    y.append(device.pwr[port_thru][idx])
    x.append(device.wavl[idx])

plt.figure()
plt.plot(wavl, data, linewidth = 0.1, label = 'Calibration reference')
plt.scatter(x, y, color='red', label = 'Sampling points')
plt.legend(loc=0)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Power (dBm)")
plt.savefig('method_2'+'.pdf')

# %% method step 3

tol = 5
x_envelope = []
y_envelope = []
tracker = y[0]

for idx, val in enumerate(y):
    if np.abs(val-tracker) < tol:
        x_envelope.append(x[idx])
        y_envelope.append(val)
        tracker = val
    else:
        oracle = np.poly1d(np.polyfit(x_envelope, y_envelope, 3))
        x_oracle = x
        y_oracle = oracle(x_oracle)

        if np.abs(val-y_oracle[idx]) < tol:
            tracker = val

plt.figure()
plt.plot(wavl, data, linewidth = 0.1, label = 'Calibration reference')
plt.scatter(x_envelope, y_envelope, color='red', label = 'Envelope points')
plt.legend(loc=0)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Power (dBm)")
plt.savefig('method_3'+'.pdf')

# %% method step 4

envelope = np.poly1d(np.polyfit(x_envelope, y_envelope, 8))
x_final = wavl
y_final = envelope(x_final)

plt.figure()
plt.plot(wavl, data, linewidth = 0.1, label = 'Calibration reference')
plt.scatter(x_envelope, y_envelope, color='red', label = 'Envelope points')
plt.plot(x_final, y_final, '--', color = 'black', linewidth = 2, label = 'Envelope')
plt.legend(loc=0)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Power (dBm)")
plt.savefig('method_4'+'.pdf')

# %%

calibrated = np.array(data)-np.array(y_final)
calibrated_drop = np.array(data_envelope)-np.array(y_final)

plt.figure()
plt.plot(wavl, calibrated, linewidth = 1, label = 'Calibrated envelope response')
plt.plot(wavl, calibrated_drop, linewidth = 1, label = 'Calibrated input response')
plt.legend(loc=0)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Power (dBm)")
plt.savefig('method_5'+'.pdf')

# %%

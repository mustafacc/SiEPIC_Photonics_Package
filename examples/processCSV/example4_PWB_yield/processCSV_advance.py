"""
SiEPIC Analysis Package

Author:     Mustafa Hammood
            Mustafa@siepic.com

Example:    Application of SiEPIC_AP cutback and processCSV function
            to extract the porpagation losses from three different length waveguides.
            for various types of waveguides in a process control monitor (PCM) design
"""
# %%
import sys
sys.path.append(r'C:\Users\musta\Documents\GitHub\SiEPIC_Photonics_Package')
import siepic_analysis_package as siap
import matplotlib.pyplot as plt
import matplotlib, os
import numpy as np


fname_data = "data_pwb"  # filename containing the desired data

chips = ['chip2_air', 'chip4_1nm_overetch', 'chip5_15nm_underetch',
         'chip7_46nm_underetch', 'chip8_29nm_underetch']

port = 1

chip = chips[1]

loss_all = []
loss_all_wavl = []
# %% crawl available data to choose file

for chip in chips:
    devices_pwb = []
    devices_ref = []

    # loopty loop to go through data structure
    # data structure: (all data folder) ->
    # (chip folder) ->
    # (measurements folders) -> (csv file in the measurement folder)
    # iterate through folders in directory to find (all data folder, fname_data)
    for root, dirs, files in os.walk(fname_data):
        # identify correct subfolder with intended polarization and wavelength
        for dir in dirs:
            if dir == chip:
                # iterate through the folder to find the data
                for root, dirs, files in os.walk(fname_data+r'\\'+dir):
                    for file in files:
                        if file.endswith(".csv"):
                            device = siap.analysis.processCSV(root+r'\\'+file)
                            if device.deviceID.startswith(
                                    'ref_exLg0') or device.deviceID.startswith(
                                        'ref_exLg1470'):
                                devices_ref.append(device)
                            else:
                                devices_pwb.append(device)

    # create a subdirectory to place plots in
    # Directory
    directory = "results_pwb_"+chip
    # Parent Directory path
    parent_dir = os.getcwd()
    # Path
    path = os.path.join(parent_dir, directory)
    # Create the directory
    try:
        os.mkdir(path)
        os.chdir(path)
    except FileExistsError:
        os.chdir(path)
        pass

    #  plot peak transmission vs GDS coordinates
    x_arr = []
    y_arr = []
    p_arr = []
    for device in devices_ref:
        x_arr.append(device.getGDS()[0])
        y_arr.append(device.getGDS()[1])
        p_arr.append(np.max(device.pwr[port]))
    for device in devices_pwb:
        x_arr.append(device.getGDS()[0])
        y_arr.append(device.getGDS()[1])
        p_arr.append(np.max(device.pwr[port]))

    plt.figure()
    plt.scatter(x_arr, y_arr, c=p_arr)
    plt.ylabel('Y (microns)')
    plt.xlabel('X (microns)')
    plt.colorbar()
    plt.title("Peak transmission vs device coordinates")
    plt.savefig('t_vs_gds_'+chip+'.pdf')
    matplotlib.rcParams.update({'font.size': 10, 'font.family': 'Times New Roman',
                                'font.weight': 'bold'})
    #  filter and sort failing devices

    threshold = -30  # minimum transmission (dBm) that constitutes a failed device
    fails_pwb = 0
    fails_ref = 0

    # filter out failed devices for both PWB and reference devices
    devices_modified = []
    for device in devices_pwb:
        if max(device.pwr[port]) < threshold:
            fails_pwb = fails_pwb+1
        else:
            devices_modified.append(device)
    devices_pwb = devices_modified

    devices_modified = []
    for device in devices_ref:
        if max(device.pwr[port]) < threshold:
            fails_ref = fails_ref+1
        else:
            devices_modified.append(device)
    devices_ref = devices_modified

    print("Number of failed PWBs on "+chip+" = "+str(fails_pwb))
    print("Number of failed references on "+chip+" = "+str(fails_ref))

    #  calibrate the responses and extract loss of the PWBs

    plt.figure()
    for device in devices_pwb:
        # find closest calibration shunt
        closest = 1E10
        for ref in devices_ref:
            x_space = np.abs(device.getGDS()[0] - ref.getGDS()[0])
            y_space = np.abs(device.getGDS()[1] - ref.getGDS()[1])
            distance = x_space**2 + y_space**2
            if distance < closest:
                closest = distance
                ref_closest = ref
        # calibrate against the response
        if chip == 'chip2_air':
            device.pwr_calib = (np.array(device.pwr[port]) - np.array(ref_closest.pwr[port]))/4
        else:
            device.pwr_calib = (np.array(device.pwr[port]) - np.array(ref_closest.pwr[port]))/2

        fig = plt.plot(device.wavl, -device.pwr_calib, linewidth=.2)

    loss_avg = []
    for idx, val in enumerate(devices_pwb[0].wavl):
        pwr = []
        for device in devices_pwb:
            pwr.append(-device.pwr_calib[idx])
        loss_avg.append(np.average(pwr))

    loss_avg = loss_avg
    loss_wavl = device.wavl

    plt.plot(device.wavl, loss_avg, color='Black', linewidth=2,
             label='Average loss')

    plt.legend(loc=0)
    plt.ylabel('Insertion loss (dB/per PWB)', color='black')
    plt.xlabel('Wavelength (nm)', color='black')
    plt.title("Calibrated insertion loss of a PWB")
    plt.savefig('overlay_IL_'+chip+'.pdf')
    matplotlib.rcParams.update({'font.size': 14, 'font.family': 'Times New Roman',
                                'font.weight': 'bold'})
    loss_all.append(loss_avg)
    loss_all_wavl.append(loss_wavl)

    # Go back to the parent directory
    os.chdir(parent_dir)

# %% plot all average losses

plt.figure()

for idx, chip in chips:
    fig = plt.plot(device.wavl, -device.pwr_calib, linewidth=.2)
plt.legend(loc=0)
plt.ylabel('Insertion loss (dB/per PWB)', color='black')
plt.xlabel('Wavelength (nm)', color='black')
plt.title("Calibrated insertion loss of a PWB")
plt.savefig('overlay_IL_.pdf')
matplotlib.rcParams.update({'font.size': 14, 'font.family': 'Times New Roman',
                            'font.weight': 'bold'})
# %%

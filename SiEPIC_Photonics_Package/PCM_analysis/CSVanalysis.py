# -*- coding: utf-8 -*-
"""
CSVanalysis with objects and functions to process MLP measurement outputs.

Created on Sat Aug 28 04:20:42 2021

@author: Mustafa Hammood

@description: import and process the CSV measurement output of a MLP system
"""

import csv


class measurement(object):
    """
    An object to represent a measurement.

    Attributes
    ----------
    deviceID : str
        Device identifier, measurement label name.
    user : str
        User ID conducting the measurement.
    start : str
        Date and time of starting the measurement.
        Format: "Day-Month-Year HH:MM:SS"
    finish : str
        Date and time of finishing the measurement.
        Format: "Day-Month-Year HH:MM:SS"
    coordsGDS : str
        Coordinates of the device on the GDS file.
        Format: "X Y"
    coordsMotor : str
        Coordinates of the device on the motors.
        Format: "X Y"
    date : str
        Date at which the chip measurement started.
        Format: "Day-Month-Year HH:MM:SS"
    laser : str
        Model of the laser used in the measurement.
    detector : str
        Model of the detector used in the measurement.
    sweepSpd : float
        Sweep speed of the laser. Units : nm/s
    sweepPwr : float
        Power of the laser in the sweep. Units : dBm
    wavlStart : float
        Start wavelength of the sweep. Units : nm
    wavlStop : float
        Stop wavelength of the sweep. Units : nm
    wavlStep : float
        Wavelength step size in the sweep. Units : nm
    stitch : float
        Number of stitched wavelength ranges in the sweep.
    initRange : float
        Initial range of the detector. Units : dBm
    wavl : list
        Wavelength points in the sweep. Units : nm
    pwr : list
        List of detector readout of each channel at each wavelength.
        Format: [ [ch1], [ch2], ...]

    Methods
    -------
    plot(channels, savepdf, savepng)
        Plots desired measurement results.
    getDuration()
        Returns the measurement duration in seconds.
    getGDS()
        Calculate the GDS X and Y coordinates of the device.
    """

    def __init__(self, deviceID, user, start, finish, coordsGDS, coordsMotor,
                 date, laser, detector, sweepSpd, sweepPwr, wavlStep,
                 wavlStart, wavlStop, stitch, initRange, wavl, pwr):
        self.deviceID = deviceID
        self.user = user
        self.start = start
        self.finish = finish
        self.coordsGDS = coordsGDS
        self.coordsMotor = coordsMotor
        self.date = date
        self.laser = laser
        self.detector = detector
        self.sweepSpd = sweepSpd  # nm/s
        self.sweepPwr = sweepPwr  # nm
        self.wavlStep = wavlStep  # nm
        self.wavlStart = wavlStart  # nm
        self.wavlStop = wavlStop  # nm
        self.stitch = stitch
        self.initRange = initRange  # dBm
        self.wavl = wavl  # nm
        self.pwr = pwr  # dBm

    def plot(self, channels=[0], wavlRange=None, pwrRange=None, savepdf=False,
             savepng=True):
        """
        Plot the desires channels of the measurement object.

        Parameters
        ----------
        channels : list
            List of channels to be plotted.
            Example: channels = [0, 1, 2]
        wavlRange : list
            Wavelength plotting range (X axis). Values are floats.
            Format: [wavelength minimum, wavelength maximum]
        pwrRange : list
            Power plotting range (Y axis). Values are floats.
            Format: [power minimum, power maximum]
        savepdf : Boolean, optional
            Flag to save the plot as pdf. The default is False.
        savepng : Boolean, optional
        Flag to save the plot as png. The default is True.

        Returns
        -------
        fig : matplotlib Figure object
            Figure object of the generated plot.
        ax : matplotlib Axes object
            Axes object of the generated plot.

        """
        import matplotlib.pyplot as plt
        import matplotlib as mpl
        mpl.style.use('ggplot')  # set plotting style

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Power (dBm)')
        ax.set_title("Device: " + self.deviceID)
        ax.grid('on')

        if wavlRange is None:
            ax.set_xlim(min(self.wavl), max(self.wavl))
        else:
            ax.set_xlim(wavlRange[0], wavlRange[1])

        if pwrRange is not None:
            ax.set_ylim(pwrRange[0], pwrRange[1])

        for channel in channels:
            label = "CH" + str(channel)
            ax.plot(self.wavl, self.pwr[channel], label=label)
        ax.legend()

        if savepdf:
            fig.savefig(self.deviceID+'.pdf')
        if savepng:
            fig.savefig(self.deviceID+'.png')
        return fig, ax

    def getDuration(self):
        """
        Get the duration of the measurement.

        Returns
        -------
        duration : float
            Measurement duration in seconds.

        """
        start = self.start.split(' ')[1].split(':')
        start = [float(i) for i in start]
        finish = self.finish.split(' ')[1].split(':')
        finish = [float(i) for i in finish]
        hours = finish[0]-start[0]
        mins = finish[1]-start[1]
        secs = finish[2]-start[2]
        duration = hours*3600 + mins*60 + secs
        self.duration = duration
        return self.duration

    def getGDS(self):
        """
        Calculate the GDS X and Y coordinates of the device.

        Returns
        -------
        x : float
            GDS X coordinate.
        y : float
            GDS Y coordinate.

        """
        self.x = float(self.coordsGDS.split()[0])
        self.y = float(self.coordsGDS.split()[1])
        return self.x, self.y


def processCSV(f_name):
    """
    Process a CSV measurement file into a measurement object.

    Parameters
    ----------
    f_name : csv file location string (include directory + file)
        CSV measurement file from MLP system.

    Returns
    -------
    device : measurement object
        Measurement object created from parsed CSV file.

    """
    with open(f_name, newline='') as csvfile:
        cursor = csv.reader(csvfile, delimiter=',', quotechar='"')
        pwr = None  # measurement power array initialization
        # iterate over each row and parse its data to the proper variable
        for row in cursor:
            row = ' '.join(row).strip("#").strip()

            if "User:" in row:
                user = row.split('\t')[1].strip()

            if "Start:" in row:
                start = row.split('\t')[1].strip()

            if "Finish:" in row:
                finish = row.split('\t')[1].strip()

            if "Device ID:" in row:
                deviceID = row.split('\t')[1].strip()

            if "Device coordinates (gds):" in row:
                coordsGDS = row.split('\t')[1].strip()

            if "Device coordinates (motor):" in row:
                coordsMotor = row.split('\t')[1].strip()

            if "Chip test start:" in row:
                date = row.split('\t')[1].strip()

            if "Laser:" in row:
                laser = row.split('\t')[1].strip()

            if "Detector:" in row:
                detector = row.split('\t')[1].strip()

            if "Sweep speed:" in row:
                sweepSpd = float(row.split('\t')[1].strip(' nm/s'))

            if "Laser power:" in row:
                sweepPwr = float(row.split('\t')[1].strip(' dBm'))

            if "Wavelength step-size:" in row:
                wavlStep = float(row.split('\t')[1].strip(' nm'))

            if "Start wavelength:" in row:
                wavlStart = float(row.split('\t')[1].strip(' nm'))

            if "Stop wavelength:" in row:
                wavlStop = float(row.split('\t')[1].strip(' nm'))

            if "Stitch count:" in row:
                stitch = float(row.split('\t')[1].strip())

            if "Init Range:" in row:
                initRange = float(row.split('\t')[1].strip())

            if "wavelength " in row:
                wavl = row.split(' ')
                wavl = [float(i) for i in wavl[1:]]

            if "channel_" in row:
                if pwr is not None:
                    channel = row.split(' ')
                    channel = [float(i) for i in channel[1:]]
                    pwr.append(channel)
                else:
                    pwr = row.split(' ')
                    pwr = [[float(i) for i in pwr[1:]]]

    device = measurement(deviceID=deviceID, user=user, start=start,
                         finish=finish, coordsGDS=coordsGDS,
                         coordsMotor=coordsMotor, date=date, laser=laser,
                         detector=detector, sweepSpd=sweepSpd,
                         sweepPwr=sweepPwr, wavlStep=wavlStep,
                         wavlStart=wavlStart, wavlStop=wavlStop, stitch=stitch,
                         initRange=initRange, wavl=wavl, pwr=pwr)
    return device


f_measurement = r"C:\Users\musta\Nextcloud\Shared\Lab data LC group\MLP01-4060-Scylla\Public\20210828_CSVanalysis\example_single\24-Aug-2021 22.22.52_1.csv"

device = processCSV(f_measurement)

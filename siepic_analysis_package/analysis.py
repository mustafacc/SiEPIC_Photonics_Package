"""
SiEPIC Analysis Package analysis module.

Author:     Mustafa Hammood
            mustafa@siepic.com

Module: Data processing and analysis functionalities of the analysis package

"""
import numpy as np

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
    Process a MapleLeaf Photonics Fotonica CSV measurement file into a measurement object.

    Parameters
    ----------
    f_name : csv file location string (include directory + file)
        CSV measurement file from MLP system.

    Returns
    -------
    device : measurement object
        Measurement object created from parsed CSV file.

    """
    import csv
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

def find_nearest(array, value):
    """Find the array index that's nearest to an input value

    Args:
        array (nparray): Input list to search.
        value (float): Target value to search for.

    Returns:
        int: index of the arra
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def bandwidth ( input_data_response, threshold = 3):
    """Calculates the bandwidth of an input result

    Args:
        input_data_response (list): [wavelength (nm), power (dBm)]
        threshold (int, optional): bandwidth threshold. Defaults to 3 dB.

    Returns:
        list: Calculated bandwidth and wavelength [bandwidth, central_wavelength]
    """

    # input list format: 
    #                    bandwidth threshold, default 3 dB
    # output list format: [bandwidth of threshold, central wavelength]

    wavelength = input_data_response[0]
    response = input_data_response[1]
    
    center_index = find_nearest( response, max(response))
    isInBand = response>max(response) - threshold

    leftBound = center_index

    while isInBand[leftBound] == 1:
        leftBound = leftBound-1

    rightBound=center_index

    while isInBand[rightBound] == 1:
        rightBound = rightBound+1

    bandwidth = wavelength[rightBound] - wavelength[leftBound]
    
    central_wavelength = (wavelength[rightBound] + wavelength[leftBound])/2
    
    return [bandwidth, central_wavelength]

def cutback(input_data_response, input_data_count, wavelength, fitOrder = 8):
    """Extract insertion losses of a structure using cutback method.

    Args:
        input_data_response (list): input_data_response (list) [wavelength (nm), power (dBm)]
        input_data_count (array): input_data_count (array) [array of unit count]
        wavelength (list): wavelength of insertion loss measurement
        fitOrder (int): order of the polynomial fit. Optional, default = 8.

    Returns:
        list: [insertion loss (fit) at wavelength (dB/unit), insertion loss (dB) vs wavelength (nm)]
    """
    # fit the responses to a polynomial
    wavelength_data = input_data_response[0][0]
    
    power = []
    pfit = []
    power_fit = []
    for i in range(len(input_data_count)):
        power.append( input_data_response[i][1] )
        pfit.append( np.polyfit(wavelength_data-np.mean(wavelength_data), power[i], fitOrder) )
        power_fit.append( np.polyval(pfit[i], wavelength_data-np.mean(wavelength_data)) )
    
    power_fit_transpose = np.transpose(power_fit)
    power_transpose = np.transpose(power)
    
    # find index of wavelength of interest
    index = np.where( wavelength_data==wavelength )[0][0]
    
    # find insertion loss vs wavelength
    insertion_loss = []
    insertion_loss_raw = []
    for i in range(len(wavelength_data)):
        insertion_loss.append( np.polyfit(input_data_count, power_fit_transpose[i], 1))
        insertion_loss_raw.append( np.polyfit(input_data_count, power_transpose[i], 1))
    
    
    return [ insertion_loss[index][0], np.transpose(insertion_loss)[0], np.transpose(insertion_loss_raw)[0] ]

def calibrate(input_response, reference_response, fitOrder = 8):
    """Response correction function to calibrate an input response with respect
        to a reference response

    Args:
        input_response (list): list of measurement data, format: [wavelength, value].
        reference_response (list): list of reference data, format: [wavelength, value].
        fitOrder (int): order of the polynomial fit. Optional, default = 8.

    Returns:
        list: list containing calibrated results and the fit 
            output list format: [input power (dBm) with calibration correction,
            polynomial fit of reference power (dBm)]
    """
    wavelength = reference_response[0]
    power = reference_response[1]
    
    pfit = np.polyfit(wavelength-np.mean(wavelength), power, fitOrder)
    power_calib_fit = np.polyval(pfit, wavelength-np.mean(wavelength))
    
    power_corrected = input_response[1] - power_calib_fit
    
    return [power_corrected, power_calib_fit]

#%% baseline_correction function (useful to normalize and calibrate periodic responses)
def baseline_correction(input_response, fitOrder = 4):
    """baseline_correction function (useful to normalize and calibrate periodic responses)

    Args:
        input_response (list): list containing the response to be corrected. 
            input list format: input_response[wavelength (nm), power (dBm)]
        fitOrder (int): order of the polynomial fit. Optional, default = 4.

    Returns:
        list: output list format: [input power (dBm) with baseline correction, baseline correction fit]
    """
    wavelength = input_response[0]
    power = input_response[1]
    
    pfit = np.polyfit(wavelength-np.mean(wavelength), power, fitOrder)
    power_baseline = np.polyval(pfit, wavelength-np.mean(wavelength))
    
    power_corrected = power - power_baseline
    power_corrected = power_corrected + max(power_baseline) -max(power)
    
    return [power_corrected, power_baseline]

def calibrate_envelope( input_response, reference_response, seg = 55, difference_tol = 8, fitOrder = 4):
    """calibration function that extracts the "envelope" of a response and use it as a reference

    Args:
        input_response (list): list containing the response to be corrected.
            input list format: input_response[wavelength (nm), power (dBm)]
        reference_response (list): list of reference data, format: [wavelength, value].
        seg (int, optional): Number of segments to split the response into. Defaults to 55.
        difference_tol (int, optional): Value tolerance to accept within the envelope. Defaults to 8.
        fitOrder (int): order of the polynomial fit. Optional, default = 4.

    Returns:
        list: output list format: [input power (dBm) with envelope correction, envelope correction fit]
    """
    # step 1-pick points on the reference response that create an envelope fit
    # split the response into SEG segments, if two segments are seperated by more than TOL, discard second point and go to next point
    wavelength = reference_response[0]
    power = reference_response[1]

    wavelength_input = input_response[0]
    power_input = input_response[1]

    step = int(np.size(power)/seg)

    power_ref = []
    wavelength_ref = []
    cursor_initial = 0
    cursor_next = 1
    for i in range(seg):

        point_initial = power[cursor_initial*step]
        point_next = power[step*(cursor_next)]
        
        if abs(point_initial - point_next) < difference_tol:              
            power_ref.append(power[cursor_initial*step])
            wavelength_ref.append(wavelength[cursor_initial*step])
            cursor_initial = cursor_initial+1
            cursor_next = cursor_next+1
        else:
            while abs(point_initial - point_next) > difference_tol and (cursor_next+2)*step < np.size(power):
                cursor_next = cursor_next+1
                point_next = power[step*(cursor_next)]
                
            cursor_initial = cursor_next
            cursor_next = cursor_next+1


        if cursor_next*step >= np.size(power):
            break
    
    pfit_ref = np.polyfit(wavelength_ref-np.mean(wavelength_ref), power_ref, fitOrder)
    powerfit_ref = np.polyval(pfit_ref, wavelength-np.mean(wavelength))
    
    pfit_input = np.polyfit(wavelength_input-np.mean(wavelength_input), power_input, fitOrder)
    powerfit_input = np.polyval(pfit_input, wavelength_input-np.mean(wavelength_input))
    
    # step 2-call calibrate input with envelope fit as a reference response
    power_input_calibrated = power_input - powerfit_ref
    
    return [power_input_calibrated, powerfit_ref]

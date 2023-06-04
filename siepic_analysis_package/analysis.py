"""
SiEPIC Analysis Package analysis module.

Author:     Mustafa Hammood
            mustafa@siepic.com

Module: Data processing and analysis functionalities of the analysis package

"""
import numpy as np
import math


class measurement(object):
    """
    An object to represent a measurement.

    Attributes
    ----------
    deviceID : str
        Device identifier, measurement label name.
    deviceDescription : str
        Additional Info regarding device
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
        List of detector readout of each channel at each wavelength
        and applied voltage in the case of active measurements.
        Format: [ [ch1_v1, ch1_v2, ...], [ch2_v1, ch2_v2, ...], ...]
    dieID : str 
        Identifier used in cases where multiple dies are present
    voltageExperimental : list
        Supplementary list to state the voltages associated with pwr when 
        it has the form of a 3d list for active measurements
        Format: [ [ch1_v1, ch1_v2, ...], [ch2_v1, ch2_v2, ...], ...]
    currentExperimental : list
        Supplementary list to state the current associated with pwr when 
        it has the form of a 3d list for active measurements
        Format: [ [ch1_c1, ch1_c2, ...], [ch2_c1, ch2_c2, ...], ...]
    IV_current : list
        List of current values in microamperes to be used in IV plotting
        Format [[current1], [current2], ...]
        Only more than 1 current present if multiple repeat measurements were
        performed on the same device
    IV_voltage : list
        List of voltage values in microamperes to be used in IV plotting
        Format [[voltage1], [voltage2], ...]
        Only more than 1 voltage present if multiple repeat measurements were
        performed on the same device
    darkCurrent : list
        List of dark current results associated with the device and the 
        associated voltage applied to measure it at
        Format [[Dark Current],[Voltage]]
    pol_loss : list
        List of polarization dependent loss associated with the device
        Port configuration states the edge couplers used for the measurement, 
        the first number coresponds to the input EC and the second one is the 
        output EC.
        Format : [[wavl],[[Loss_1],..,[Loss_N]],[[Port_config1],...,[Port_configN]]]
    s_parameters : list
        List of S parameters, format allow for up to 4x4 matrix. Each S-param.
        is an array that matches up to the frequency array. Additionally each 
        S param. can have multiple occurances of it for each applied voltage
        Frequency, Biases, and Calibration are also present.
        Format : [[Frequency],[Biases],
                 [[[[S11_v1,..,S11_vN]],...,[[S14_v1,..,S14_vN]]],
                 ...,[[[S41_v1,..,S41_vN]],...,[[S44_v1,..,S44_vN]]]]]
        i.e, sparameters[0] = Frequency
             sparameters[1] = List of bias voltages 
             sparameters[2] = Complete S Parameter matrix, with sweep result
             sparameters[2][0] = S11,...,S14 with sweep results
             sparameters[2][0][0] = List of S11 results for all available biases
    external_calibration : list
        If there exists an external calibration provided by EHVA, it can be stored
        here. This allows a script to save this info and apply it to other devices
        See PhotodetectorExample.py for implementation 
        Format : [calibration_wavl, calibration_dBm]
    responsivity : list
        If there exists responsivity data provided by EHVA, it is stored here.
        Wavl is consistent across measuremnts, bias and power meter range lists
        provided to distinguish different current and power values from the sweeps
        Format : [[wavl],[Bias],[MeterRange],[[current_1],..,[current_N]],[[power_1],..,[power_N]]]        
    IV_Bright : list
        New format for IV curves. This needs to be combined with old one when EHVA decides on a convention
        Format : [[Current],[Voltage]]
    IV_Dark : list
        New format for IV curves. This needs to be combined with old one when EHVA decides on a convention
        Format : [[Current],[Voltage]]
    IV_refPower : Float
        Reference optical power measurement present only in the case that 
        responsivty can be extracted


    Methods
    -------
    plot(channels, savepdf, savepng)
        Plots desired measurement results.
    getDuration()
        Returns the measurement duration in seconds.
    getGDS()
        Calculate the GDS X and Y coordinates of the device.
    getPorts()
        Returns the number of ports with data present
    plot_IVcurve()
        Plots the IV curve of the device if available
    plot_darkCurrent()
        Scatter plots the dark current versus voltage if available
    plot_polLoss()
        Plots the polarization dependent loss if available
    """

    def __init__(self, deviceID, deviceDescription, user, start, finish, coordsGDS, coordsMotor,
                 date, laser, detector, sweepSpd, sweepPwr, wavlStep,
                 wavlStart, wavlStop, stitch, initRange, wavl, pwr, dieID, 
                 voltageExperimental, currentExperimental, IV_current,
                 IV_voltage, darkCurrent, pol_loss, s_parameters,
                 external_calibration,responsivity, IV_Bright, IV_Dark, IV_refPower):
        if deviceID is None:
            self.deviceID = 'Device'
        else:
            self.deviceID = deviceID
        self.deviceDescription = deviceDescription
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
        self.dieID = dieID
        self.voltageExperimental = voltageExperimental # volts
        self.currentExperimental = currentExperimental # uA
        self.IV_current = IV_current # uA
        self.IV_voltage = IV_voltage # V
        self.darkCurrent = darkCurrent # A 
        self.pol_loss = pol_loss
        self.s_parameters = s_parameters
        self.external_calibration = external_calibration
        self.responsivity = responsivity
        self.IV_Bright = IV_Bright 
        self.IV_Dark = IV_Dark
        self.IV_refPower = IV_refPower # dBm

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

        fig1 = plt.figure(figsize=(8, 6))
        ax1 = fig1.add_subplot(111)
        ax1.set_xlabel('Wavelength (nm)')
        ax1.set_ylabel('Power (dBm)')
        ax1.set_title("Device: " + self.deviceID)
        ax1.grid('on')

        active = False
        fig2 = plt.figure(figsize=(8, 6))
        ax2 = fig2.add_subplot(111)
        ax2.set_xlabel('Wavelength (nm)')
        ax2.set_ylabel('Power (dBm)')
        ax2.set_title("Device: " + self.deviceID + " Sweep Results")
        ax2.grid('on')

        if wavlRange is None:
            ax1.set_xlim(min(self.wavl), max(self.wavl))
            ax2.set_xlim(min(self.wavl), max(self.wavl))

        else:
            ax1.set_xlim(wavlRange[0], wavlRange[1])
            ax2.set_xlim(wavlRange[0], wavlRange[1])

        if pwrRange is not None:
            ax1.set_ylim(pwrRange[0], pwrRange[1])
            ax2.set_ylim(pwrRange[0], pwrRange[1])

        for channel in channels:
            if self.voltageExperimental != None:
                for ii in range(len(self.voltageExperimental[channel])):
                    if (math.isnan(self.voltageExperimental[channel][ii]) == True):
                        label = "CH" + str(channel)
                        ax1.plot(self.wavl, self.pwr[channel][ii], label=label)
                    if (math.isnan(self.voltageExperimental[channel][ii]) == False):
                        active = True
                        label = "CH" + str(channel) + " V=" + \
                            str(self.voltageExperimental[channel][ii])
                        ax2.plot(self.wavl, self.pwr[channel][ii], label=label)
            else:
                label = "CH" + str(channel)
                ax1.plot(self.wavl, self.pwr[channel], label=label)

        ax1.legend()
        ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        if savepdf:
            if self.dieID != None:
                fig1.savefig(self.deviceID + "_Die" + self.dieID + '.pdf')
                fig2.savefig(self.deviceID + "_Die" + self.dieID + '_Sweep.pdf')
            else:
                fig1.savefig(self.deviceID + '.pdf')
                fig2.savefig(self.deviceID + '_Sweep.pdf')
        if savepng:
            if self.dieID != None:
                fig1.savefig(self.deviceID + "_Die" + self.dieID + '.png')
                fig2.savefig(self.deviceID + "_Die" + self.dieID + '_Sweep.png')
            else:
                fig1.savefig(self.deviceID + '.png')
                fig2.savefig(self.deviceID + '_Sweep.png')

        if (active == False):
            plt.close(fig2)

        return fig1, fig2, ax1, ax2

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

    def getPorts(self):
        """
        Returns list of ports with data present

        Returns
        -------
        Ports : list
            list of ports with data present

        """
        ports = []
        for ii in range(len(self.pwr)):
            ports.append(ii)

        return ports

    def plot_IVcurve(self, savepdf=False, savepng=False):
        """
        Plots the IV curve of the device if available

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
        ax.set_xlabel('Voltage (V)')
        ax.set_ylabel('Current (mA)')
        ax.set_title("Device: " + self.deviceID + "_Die" + self.dieID + "\n IV Curve")
        ax.grid('on')
        
        for ii in range(len(self.IV_current)):
            label = "Meaurement # %s" % ii
            ax.plot( self.IV_voltage[ii], self.IV_current[ii]*1.0e-3, label = label)
            
        ax.legend()
        if savepdf:
            fig.savefig(self.deviceID + "_Die" + self.dieID + "_IVcurve" + '.pdf')
        if savepng:
            fig.savefig(self.deviceID + "_Die" + self.dieID + "_IVcurve" +'.png')
        return fig, ax
    
    def plot_darkCurrent(self, savepdf=False, savepng=False):
        """
        Scatter plots the dark current versus voltage if available

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
        ax.set_xlabel('Voltage (V)')
        ax.set_ylabel('Dark Current ($\mu$A)')
        ax.set_title("Device: " + self.deviceID + '_Die' + self.dieID + "\n Dark Current")
        ax.grid('on')
        
        # Converting to uA
        darkCurrent = [i / 1.0e-6 for i in self.darkCurrent[0]]
        # Finding indices where new measurment is occuring
        indices = [0]
        check = -999
        for ii in range(len(darkCurrent)):
            if self.darkCurrent[1][ii] <= check:
                indices.append(ii)
                
            check = self.darkCurrent[1][ii]
            
        for ii in range(len(indices)): 
            start = indices[ii]
            if ii == len(indices)-1:
                stop = -1
                ax.scatter( self.darkCurrent[1][start:stop], darkCurrent[start:stop],label = 'Measurement#' + str(ii))
            else:
                stop = indices[ii+1]
                ax.scatter( self.darkCurrent[1][start:stop], darkCurrent[start:stop],label = 'Measurement#' + str(ii))
        
        ax.legend()    
        if savepdf:
            fig.savefig(self.deviceID + "_Die" + self.dieID + "_DarkCurrent" + '.pdf')
        if savepng:
            fig.savefig(self.deviceID + "_Die" + self.dieID + "_DarkCurrent" +'.png')
        return fig, ax
    def plot_polLoss(self, savepdf = False, savepng = False):
        """
        

        Parameters
        ----------
        savepdf : TYPE, optional
            DESCRIPTION. The default is False.
        savepng : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        fig : matlab Figure object
            Figure object of the generated plot.
        ax : matlab Axes object
            Axes object of the generated plot.

        """
        
        import matplotlib.pyplot as plt
        import matplotlib as mpl
        mpl.style.use('ggplot')  # set plotting style

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Pol. Loss (dBm)')
        ax.set_title("Device: " + self.deviceID + "_Die"+ self.dieID + "\n Polarization Dependent Loss")
        ax.grid('on')

        for ii in range(len(self.pol_loss[0])):
            try:
                label = "Port Pair : " + self.pol_loss[2][ii]
                ax.plot(self.pol_loss[0][ii], self.pol_loss[1][ii],label=label)
            except Exception:
                print("Missing Information on Measured Port, skipping measurement")            
        ax.legend()

        if savepdf:
            fig.savefig(self.deviceID + "_Die" + self.dieID + "_polLoss" + '.pdf')
        if savepng:
            fig.savefig(self.deviceID + "_Die" + self.dieID + "_polLoss" +'.png')
    
        return fig, ax


def measurementEHVA(desiredDevice):
    """
    Creates a measurement object out of the pandas dataframe containing only 1 component ID

    Parameters
    ----------
    desiredDevice : pandas dataframe
        dataframe containing all information regarding a single device

    Returns
    -------
    device : measurement object
        DESCRIPTION.

    """
    
    # Pre-initializing everything to None in case there is no data for it?
    componentName = None
    timestamp = None
    wavlStep = None
    wavlStart = None
    wavlStop = None
    wavl = None
    coordsGDS = None
    pwr = None
    
    componentName = desiredDevice.ComponentName.at[0]
    deviceDescription = desiredDevice.ComponentDescription.at[0]
    componentID = desiredDevice.ComponentId.at[0]
    deviceID = componentName + '_ID_' + str(componentID)
    timestamp = desiredDevice.ResultCreated.at[0]     
    dieID = str(desiredDevice.DieId.at[0])
    coordsGDS = desiredDevice.OpticalPortPosition.at[0]
    coordsGDS = coordsGDS.replace(","," ")  

    pwr = [[]]
    voltageExperimental = [[]]
    currentExperimental = [[]]
    IV_current = []
    IV_voltage = []
    darkCurrent = [[],[]]
    pol_loss = [[],[],[]]
    s_parameters = [[],[],[[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]]]
    external_calibration = [[],[]]
    responsivity = [[],[],[],[],[]]
    IV_Bright =[[],[]]
    IV_Dark =[[],[]]
    IV_refPower = None
    for ii in range(len(desiredDevice)): 
        resultType = desiredDevice.ResultMetricName.at[ii]
        domainType = desiredDevice.DomainMetricName.at[ii] 
        if (resultType == 'optical power'):  
            wavlString = desiredDevice.ResultDomain.at[ii]
            wavl = np.fromstring(wavlString, dtype=float, sep=',')
            wavlStart = wavl[0]
            wavlStop = wavl[-1]
            wavlStep = wavl[1] - wavl[0]
            pwerString = desiredDevice.ResultValue.at[ii]
            resultName = desiredDevice.ResultName.at[ii]
            channel = np.fromstring(pwerString, dtype=float, sep=',')
            channel = channel.astype(float)
            channel[channel > 0] = np.nan
            if (resultName == 'opticalPowerFirstOPM'):
                pwr[0].append(channel)
                voltageExperimental[0].append(round(desiredDevice.EXPvoltage.at[ii],3))
                currentExperimental[0].append(round(desiredDevice.EXPcurrent.at[ii],3))
            elif (resultName == 'opticalPowerSecondOPM'):
                if (len(pwr) == 1):
                    pwr.append([channel])
                    voltageExperimental.append([round(desiredDevice.EXPvoltage.at[ii],3)])
                    currentExperimental.append([round(desiredDevice.EXPcurrent.at[ii],3)])
                else:                       
                    pwr[1].append(channel)
                    voltageExperimental[1].append(round(desiredDevice.EXPvoltage.at[ii],3))
                    currentExperimental[1].append(round(desiredDevice.EXPcurrent.at[ii],3))
            elif (resultName == 'opticalPowerThirdOPM'): 
                if (len(pwr) == 2):
                    pwr.append([channel])
                    voltageExperimental.append([round(desiredDevice.EXPvoltage.at[ii],3)])
                    currentExperimental.append([round(desiredDevice.EXPcurrent.at[ii],3)])
                else:    
                    pwr[2].append(channel)
                    voltageExperimental[2].append(round(desiredDevice.EXPvoltage.at[ii],3))
                    currentExperimental[2].append(round(desiredDevice.EXPcurrent.at[ii],3))
            else:
                print("Unkown optical power result name")
                
        elif (resultType == 'uCurrent') and (domainType == 'voltage'):
            resultName = desiredDevice.ResultName.at[ii]
            resultDescription = desiredDevice.ResultDescription.at[ii]
            if (resultName == 'Current'):
                if "IV Curve, Bright" in resultDescription:
                    currentString = desiredDevice.ResultValue.at[ii]
                    currentData = np.fromstring(currentString, dtype=float, sep=',')
                    voltageString = desiredDevice.ResultDomain.at[ii]
                    voltageData = np.fromstring(voltageString, dtype=float, sep=',')
                    IV_Bright[1].append(currentData)
                    IV_Bright[0].append(voltageData)
                elif "IV Curve, Dark" in resultDescription:
                    currentString = desiredDevice.ResultValue.at[ii]
                    currentData = np.fromstring(currentString, dtype=float, sep=',')
                    voltageString = desiredDevice.ResultDomain.at[ii]
                    voltageData = np.fromstring(voltageString, dtype=float, sep=',')
                    IV_Dark[1].append(currentData)
                    IV_Dark[0].append(voltageData)
                else: #TODO(Integrate this old format into the new one above when EHVA fixes their convention)
                    currentString = desiredDevice.ResultValue.at[ii]
                    currentData = np.fromstring(currentString, dtype=float, sep=',')
                    voltageString = desiredDevice.ResultDomain.at[ii]
                    voltageData = np.fromstring(voltageString, dtype=float, sep=',')
                    IV_current.append(currentData)
                    IV_voltage.append(voltageData)
                
        elif (resultType == 'current'):
            resultName = desiredDevice.ResultName.at[ii]
            resultDescription = desiredDevice.ResultDescription.at[ii]
            if (resultName == 'Dark current'):
                darkCurrent[0].append(float(desiredDevice.ResultValue.at[ii]))
                darkCurrent[1].append(float(desiredDevice.ResultDomain.at[ii]))
            elif (resultDescription == 'Measured output current (A), multiplied by the polarity of the photodiode'): #TODO(need to deal with EHVA and their ambigious naming)
                wavlString = desiredDevice.ResultDomain.at[ii]
                res_wavl = np.fromstring(wavlString, dtype=float, sep=',')    
                bias = desiredDevice.EXPbias2.at[ii]
                meterRange = desiredDevice.EXPmeterRange.at[ii]
                currentString = desiredDevice.ResultValue.at[ii]
                current = np.fromstring(currentString, dtype=float, sep=',')
                pwrString = desiredDevice.EXPpwr.at[ii]
                pwr = np.fromstring(pwrString, dtype=float, sep=',')
                responsivity[0] = res_wavl
                responsivity[1].append(bias)
                responsivity[2].append(meterRange)
                responsivity[3].append(current)
                responsivity[4].append(pwr)
                 
        elif (resultType == 'optical return loss'):
            resultName = desiredDevice.ResultName.at[ii]
            if (resultName == 'PolarizationDependentLoss'): 
                wavlString = desiredDevice.ResultDomain.at[ii]
                pol_wavl = np.fromstring(wavlString, dtype=float, sep=',')
                polString = desiredDevice.ResultValue.at[ii]
                loss = np.fromstring(polString, dtype=float, sep=',')
                loss = loss.astype(float)
                measuredPort = desiredDevice.MeasuredPorts.at[ii]
                pol_loss[0].append(pol_wavl) 
                pol_loss[1].append(loss) 
                pol_loss[2].append(measuredPort)

            else:               
                print("NOT HANDLING THE FOLLOWING CASE:")
                print(resultName)
        elif (resultType == 'power'):
            resultName = desiredDevice.ResultName.at[ii]
            if (resultName == 'S21 raw on-chip photodetector and external modulator'):
                freqString = desiredDevice.ResultDomain.at[ii]
                freq = np.fromstring(freqString, dtype=float, sep=',')
                pwerString = desiredDevice.ResultValue.at[ii]
                S21 = np.fromstring(pwerString, dtype=float, sep=',')
                biasVolt = desiredDevice.EXPbias.at[ii]
                s_parameters[0] = freq
                s_parameters[1].append(biasVolt)
                s_parameters[2][1][0].append(S21)
            elif (resultName == 'S21 of calibrated photodetector and external modulator'):
                wavlString = desiredDevice.ResultDomain.at[ii]
                cal_wavl = np.fromstring(wavlString, dtype=float, sep=',')
                calString = desiredDevice.ResultValue.at[ii]
                cal = np.fromstring(calString, dtype=float, sep=',')
                external_calibration[0] = cal_wavl
                external_calibration[1] = cal
            else:
                print("Unhandled power type: " + resultName )
                    

    device = measurement(deviceID=deviceID, deviceDescription=deviceDescription,
                         user=None, start=None,
                         finish=timestamp, coordsGDS=coordsGDS,
                         coordsMotor=None, date=None, laser=None,
                         detector=None, sweepSpd=None,
                         sweepPwr=None, wavlStep=wavlStep,
                         wavlStart=wavlStart, wavlStop=wavlStop, stitch=None,
                         initRange=None, wavl=wavl, pwr=pwr, dieID=dieID,
                         voltageExperimental=voltageExperimental, 
                         currentExperimental=currentExperimental,
                         IV_current=IV_current, IV_voltage=IV_voltage,
                         darkCurrent=darkCurrent, pol_loss = pol_loss,
                         s_parameters=s_parameters, 
                         external_calibration=external_calibration,
                         responsivity=responsivity,
                         IV_Bright=IV_Bright,IV_Dark=IV_Dark,
                         IV_refPower=IV_refPower)
    
    return device


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

    # if the .csv is not from an automated measurement (if exported from figure)
    if 'deviceID' in locals():
        deviceID = deviceID
    else:
        deviceID = None
        start = None
        finish = None
        coordsGDS = None
        coordsMotor = None
        date = None

    device = measurement(deviceID=deviceID, deviceDescription= None,
                         user=user, start=start,
                         finish=finish, coordsGDS=coordsGDS,
                         coordsMotor=coordsMotor, date=date, laser=laser,
                         detector=detector, sweepSpd=sweepSpd,
                         sweepPwr=sweepPwr, wavlStep=wavlStep,
                         wavlStart=wavlStart, wavlStop=wavlStop, stitch=stitch,
                         initRange=initRange, wavl=wavl, pwr=pwr, dieID=None, 
                         voltageExperimental=None, currentExperimental=None,
                         IV_current=None, IV_voltage=None, darkCurrent=None, 
                         pol_loss=None, s_parameters = None,
                         external_calibration=None, responsivity=None,
                         IV_Bright=None, IV_Dark=None, IV_refPower =None)
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


def bandwidth(wavl, data, threshold=3):
    """Calculates the bandwidth of an input result

    Args:
        wavl (list): Wavelength data domain
        data (list): Transmission (or power?) data to analyze
        threshold (int, optional): bandwidth threshold. Defaults to 3 dB.

    Returns:
        list: Calculated bandwidth and wavelength [bandwidth, central_wavelength]
    """

    # input list format:
    #                    bandwidth threshold, default 3 dB
    # output list format: [bandwidth of threshold, central wavelength]

    wavelength = wavl
    response = data

    center_index = find_nearest(response, max(response))
    isInBand = response > max(response) - threshold

    leftBound = center_index

    while isInBand[leftBound] == 1:
        leftBound = leftBound-1

    rightBound = center_index

    while isInBand[rightBound] == 1:
        rightBound = rightBound+1

    bandwidth = wavelength[rightBound] - wavelength[leftBound]

    central_wavelength = (wavelength[rightBound] + wavelength[leftBound])/2

    return [bandwidth, central_wavelength]


def cutback(input_data_response, input_data_count, wavelength, fitOrder=8):
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
    wavelength_data = np.array(input_data_response[0][0])
    power = []
    pfit = []
    power_fit = []
    for i in range(len(input_data_count)):
        power.append(input_data_response[i][1])
        pfit.append(np.polyfit(wavelength_data-np.mean(wavelength_data), power[i], fitOrder))
        power_fit.append(np.polyval(pfit[i], wavelength_data-np.mean(wavelength_data)))

    power_fit_transpose = np.transpose(power_fit)
    power_transpose = np.transpose(power)

    # find index of wavelength of interest
    index = find_nearest(wavelength_data, wavelength)

    # find insertion loss vs wavelength
    insertion_loss = []
    insertion_loss_raw = []
    for i in range(len(wavelength_data)):
        insertion_loss.append(np.polyfit(input_data_count, power_fit_transpose[i], 1))
        insertion_loss_raw.append(np.polyfit(input_data_count, power_transpose[i], 1))

    return [insertion_loss[index][0], np.transpose(insertion_loss)[0], np.transpose(insertion_loss_raw)[0]]


def calibrate(input_response, reference_response, fitOrder=8):
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


def baseline_correction(input_response, fitOrder=4):
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
    power_corrected = power_corrected + max(power_baseline) - max(power)

    return [power_corrected, power_baseline]


def calibrate_envelope(wavl, data_envelope, data, tol=3.0, N_seg=25, fitOrder=4,
                       direction='left', verbose=False):
    """Calibrate an input response by using the envelope of another response.
        Ideal for Bragg gratings and contra-directional couplers
        Can be useful mainy for responses that contain dips.

    Args:
        wavl (list): List of wavelength data points
        data_envelope (list): List of the values of the envelope response data
        data (list): List of input data values to be calibrated
        tol (float, optional): Dip threshold tolerance, i.e., what dips to consider as not dip. Defaults to 2.0.
        N_seg (int, optional): Number of segments to dice an array into. Defautls to 100.
        fitOrder(int, optional): Polynomial order used to fit the envelope spectrum. Defautls to 8.
        verbose (bool, optional): Flag to help debugging by plotting detected peaks. Defaults to False.

    Returns:
        calbirated (numpy array): List of the data points of the calibrated input response values
        ref (list): List of the reference polyfit points made using the envelope
        x_envelope (list): List of X-values used to creat ref polyfit (debugging)
        y_envelope (list): List of Y-values used to creat ref polyfit (debugging)
    """

    if verbose:
        import matplotlib.pyplot as plt
        plt.figure()
        plt.plot(wavl, data, label='Input data')
        plt.plot(wavl, data_envelope, label="Calibration reference")
        plt.legend(loc=0)
        plt.title("Original input data set")
        plt.xlabel("X")
        plt.ylabel("Y")

    # step 1, sample the data_envelope data into N_seg segments
    idxSteps = int(np.floor(np.size(data_envelope)/N_seg))  # index steps between each segment
    x = []
    y = []
    for i in range(N_seg):
        idx = i * idxSteps
        y.append(data_envelope[idx])
        x.append(wavl[idx])

    if verbose:
        plt.figure()
        plt.plot(wavl, data_envelope, linewidth=0.1, label='Calibration reference')
        plt.scatter(x, y, color='red', label='Sampling points')
        plt.legend(loc=0)
        plt.title("Sampling of reference data set")
        plt.xlabel("X")
        plt.ylabel("Y")

    x_envelope = []  # wavelength data points to include in envelope fitting
    y_envelope = []  # transmission (or power?) data points to envelope fitting

    if direction == 'left':
        tracker = y[0]  # initial threshold tracker value
        for idx, val in enumerate(y):
            if np.abs(val-tracker) < tol:
                x_envelope.append(x[idx])
                y_envelope.append(val)
                tracker = val
            else:
                oracle = np.poly1d(np.polyfit(x_envelope, y_envelope, 2))
                x_oracle = x
                y_oracle = oracle(x_oracle)

                if np.abs(val-y_oracle[idx]) < tol:
                    tracker = val
    else:
        tracker = y[-1]
    for idx, val in reversed(list(enumerate(y))):
        if np.abs(val-tracker) < tol:
            x_envelope.append(x[idx])
            y_envelope.append(val)
            tracker = val
        else:
            oracle = np.poly1d(np.polyfit(x_envelope, y_envelope, 2))
            x_oracle = x
            y_oracle = oracle(x_oracle)

            if np.abs(val-y_oracle[idx]) < tol:
                tracker = val

    if verbose:
        plt.figure()
        plt.plot(wavl, data_envelope, linewidth=0.1, label='Calibration reference')
        plt.scatter(x_envelope, y_envelope, color='red', label='Envelope points')
        plt.legend(loc=0)
        plt.title("Generated envelope points to used for polynomial fitting")
        plt.xlabel("X")
        plt.ylabel("Y")

    envelope = np.poly1d(np.polyfit(x_envelope, y_envelope, fitOrder))
    ref = envelope(wavl)

    if verbose:
        plt.figure()
        plt.plot(wavl, data_envelope, linewidth=0.1, label='Calibration reference')
        plt.scatter(x_envelope, y_envelope, color='red', label='Envelope points')
        plt.plot(wavl, ref, '--', color='black', linewidth=2, label='Envelope')
        plt.legend(loc=0)
        plt.title("Final generated polynomial for fitting")
        plt.xlabel("X")
        plt.ylabel("Y")

    calibrated = np.array(data)-np.array(ref)
    calibrated_ref = np.array(data_envelope)-np.array(ref)

    if verbose:
        plt.figure()
        plt.plot(wavl, calibrated, linewidth=1, label='Calibrated input response')
        plt.plot(wavl, calibrated_ref, linewidth=1, label='Calibrated envelope response')
        plt.legend(loc=0)
        plt.title("Final calibration")
        plt.xlabel("X")
        plt.ylabel("Y")
    return calibrated, ref, x_envelope, y_envelope


def getFSR(wavl, data, prominence=3, distance=50, verbose=False):
    """Get the free spectral range of an input spectrum.

    Args:
        wavl (list): wavelength range of the spectrum.

        data (list): Values of the spectrum.
        prominence (float, optional): Extinction ratio peak detection prominence. 
            Set this value to be higher than the minimum ER. Defaults to 3.0
        distance (int, optional): Required minimal horizontal distance (>= 1) in samples between neighbouring peaks.
            Defaults to 50.
        verbose (bool, optional): Flag to help debugging by plotting detected peaks. Defaults to False.

    Returns:
        fsr_wavl (list): List of wavelengths at which the FSR is extracted from. Units are the same as wavl unit.
        fsr (list): List of the calculated free spectral ranges of the spectrum. Units are the same as wavl unit.
        troughs (list): List of all indices in which a trough is located at

    refer to https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
        for details about prominence and distance parameters.
    """
    from scipy.signal import find_peaks
    # convert input data to np array, easier for processing
    wavl = np.array(wavl)
    data = np.array(data)

    troughs, _ = find_peaks(-data, prominence=prominence, distance=distance)
    fsr = []
    fsr_wavl = []
    for idx, i in enumerate(troughs):
        try:
            fsr.append(np.abs(wavl[troughs[idx+1]]-wavl[i]))
            fsr_wavl.append((wavl[troughs[idx+1]]+wavl[i])/2)
        except IndexError:
            pass

    if verbose:
        import matplotlib.pyplot as plt
        plt.figure()
        plt.scatter(np.array(wavl)[troughs], data[troughs], color='blue')
        plt.plot(wavl, data, color='black')
        plt.title("Detected troughs in the spectrum")
        plt.xlabel("X")
        plt.ylabel("Y")

        plt.figure()
        plt.scatter(fsr_wavl, fsr)
        plt.title("Extracted free spectral ranges")
        plt.xlabel("X")
        plt.ylabel("Free Spectral Range")
    return fsr_wavl, fsr, troughs


def getGroupIndex(fsr_wavl, fsr, delta_length, verbose=False):
    """Calculate the group index from a set of free spectral range data
        extracted from an unbalanced Mach-Zehnder interferometer .

    Args:
        fsr_wavl (list): List of wavelengths of the free spectral range data.
            IMPORTANT: unit must be in meters.
        fsr (list): List of free spectral ranges at the given wavelengths.
            IMPORTANT: unit must be in meters.
        delta_length (float): Length imbalance in the Mach-Zehnder interferometer.
            IMPORTANT: unit must be in meters.
        verbose (bool, optional): Flag to help debugging by plotting detected peaks. Defaults to False.

    Returns:
        ng (list): List of group indices at the given fsr_wavl points.
    """

    c = 299792458
    fsr_wavl = np.array(fsr_wavl)
    fsr = np.array(fsr)

    # conver to frequency domain
    fsr_freq = c/fsr_wavl

    # convert bandwidth from wavelength to frequency domain
    fsr_hz = []
    for idx, i in enumerate(list(fsr)):
        fsr_hz.append(i*c/(fsr_wavl[idx]*fsr_wavl[idx]))

    ng = []
    for i in fsr_hz:
        ng.append(c/(delta_length*i))

    if verbose:
        import matplotlib.pyplot as plt
        plt.figure()
        plt.scatter(fsr_wavl, fsr)
        plt.title("Free spectral range in SI units")
        plt.xlabel("Wavelength (m)")
        plt.ylabel("Free Spectral Range (m)")

        plt.figure()
        plt.scatter(fsr_freq, fsr_hz)
        plt.title("Free spectral range in SI units")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Free Spectral Range (Hz)")

        plt.figure()
        plt.scatter(fsr_wavl, ng)
        plt.title("Extracted group index")
        plt.xlabel("Wavelength (m)")
        plt.ylabel("group index")

    return ng


def truncate_data(wavl, data, wavl_min, wavl_max):
    """
    Truncates the wavl and data measurements to the specified wavl domain.

    Args:
        wavl (array-like): Array or list of wavl measurements.
        data (array-like): Array or list of corresponding data measurements.
        wavl_min (float): Minimum wavl value for truncation.
        wavl_max (float): Maximum wavl value for truncation.

    Returns:
        tuple: Tuple containing the truncated wavl and data measurements.
    """
    wavl = np.array(wavl)
    data = np.array(data)

    indices = np.where((wavl >= wavl_min) & (wavl <= wavl_max))
    wavl_truncated = wavl[indices]
    data_truncated = data[indices]

    return wavl_truncated, data_truncated

def getExtinctionRatio(wavl, data, prominence=3.0, distance=50, verbose=False):
    """Get the extinction ratio (ER) of a dataset across the spectrum.

    Args:
        wavl (list): Wavelength range of the spectrum.
        data (list): Data values of the spectrum.
        prominence (float, optional): Extinction ratio peak detection prominence. 
            Set this value to be higher than the minimum ER. Defaults to 3.0
        distance (int, optional): Required minimal horizontal distance (>= 1) in samples between neighbouring peaks.
            Defaults to 50.
        verbose (bool, optional): Flag to help debugging by plotting detected peaks. Defaults to False.

    Returns:
        er_wavl (list): Wavelengths at which the ER was extracted.
        er (list): Extracted ER values.

    refer to https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
        for details about prominence parameter.
    """
    from scipy.signal import find_peaks

    # convert input data to np array, easier for processing
    wavl = np.array(wavl)
    data = np.array(data)

    peaks, _ = find_peaks(data, prominence=prominence, distance=distance)
    troughs, _ = find_peaks(-data, prominence=prominence, distance=distance)

    er_wavl = []
    er = []

    for idx, val in enumerate(peaks):
        try:
            temp = data[val] + np.abs(data[troughs[idx]])
            er.append(temp)
            er_wavl.append(wavl[val])
        except IndexError:
            if verbose:
                print("Reached end of troughs array")

    if verbose:
        import matplotlib.pyplot as plt
        plt.figure()
        plt.scatter(np.array(wavl)[peaks], data[peaks], color='red')
        plt.scatter(np.array(wavl)[troughs], data[troughs], color='blue')
        plt.plot(wavl, data, color='black')
        print("Number of peaks = "+str(np.size(peaks)))
        print("Number of troughs = "+str(np.size(troughs)))

        plt.figure()
        plt.scatter(er_wavl, er, color='black')
        plt.ylabel('Extinction Ratio (dB)', color='black')
        plt.xlabel('Wavelength (nm)', color='black')

    return er_wavl, er

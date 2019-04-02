"""
SiEPIC Photonics Package

Author:     Mustafa Hammood
            Mustafa@siepic.com
            
            https://github.com/SiEPIC-Kits/SiEPIC_Photonics_Package

Module:     PCM Analysis 

Fetches measurement data of a manufactured chip, analyzes the process control monitor (PCM) structures to assess
the quality of the fabricated chip.
"""
#%% import package and installed dependent packages
import sys, os
# go up two directories
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(dir_path)))

import SiEPIC_Photonics_Package as SiEPIC_PP
from SiEPIC_Photonics_Package.setup import *
import matplotlib.pyplot as plt
import requests, zipfile, matplotlib

#%%
def PCM_analysis( URL, pol, download = True ):
    # create new directory for storing downloaded PCM data, download and unzip all the data
    path = "download/"
    file_name = 'experimental_data.zip'
    os.chdir(path)
    
    if download == True:
        try:  
            os.mkdir(path)
        except OSError:  
            print ("**ERROR**: Creation of the directory %s failed, remove existing directory" % path)
        else:  
            print ("Successfully created the directory %s " % path)
            
        print ("Downloading data. This may take a while. . . ")
        r = requests.get(URL,allow_redirects=True)
        with open(file_name, 'wb') as f:
            f.write(r.content)
        with zipfile.ZipFile(file_name,"r") as zip_ref:
            zip_ref.extractall()
        print ("Experimental data download and unzip complete. . . ")

    # iterate through all data, remove all non PCM data, and remove all .pdf data
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".pdf"): 
            os.remove(filename)
            continue
        if filename.startswith("PCM_") == False:
            os.remove(filename)
    print ("Data clean up complete, remove all .pdf and non PCM data. . . ")
    
    # run all
    WGloss_straight(pol)
    WGloss_spiral(pol)
    WGloss_SWG()
    Bragg_sweep()
    contraDC()
    contraDCloss()
    
#%%
# analyze the losses of straight waveguides by cutback method
def WGloss_straight(pol):
    # PCM structure ID
    file_ID = 'PCM_PCM_StraightWGloss'
    
    # PCM structure lengths
    length = [7418, 14618, 21818, 29018]
    
    # measurement port
    PORT = 1
     
    # divide by 10000 to see result in dB/cm
    length_cm = [i/10000 for i in length]
    
    input_data_response = []
    for i in length:
        for filename in os.listdir(os.getcwd()):
            if filename.startswith(file_ID+str(i)+pol) == True:
                print(filename)
                input_data_response.append( SiEPIC_PP.core.parse_response(filename,PORT) )
    
    #%% apply SiEPIC_PP cutback extraction function and plot
    [insertion_loss_wavelength, insertion_loss_fit, insertion_loss_raw] = SiEPIC_PP.core.cutback( input_data_response, length_cm, 1550e-9 )

    # plot all cutback structures responses
    plt.figure(0)
    wavelength = input_data_response[0][0]*1e9
    fig0 = plt.plot(wavelength,input_data_response[0][1], label='L = 7418', color='blue')
    fig1 = plt.plot(wavelength,input_data_response[1][1], label='L = 14618 um', color='black')
    fig2 = plt.plot(wavelength,input_data_response[2][1], label='L = 21818 um', color='green')
    fig3 = plt.plot(wavelength,input_data_response[3][1], label='L = 29018 um', color='red')
    plt.legend(loc=0)
    plt.ylabel('Power (dBm)', color = 'black')
    plt.xlabel('Wavelength (nm)', color = 'black')
    plt.xlim(round(min(wavelength)),round(max(wavelength)))
    plt.title("Raw measurement of cutback structures")
    plt.savefig('WGloss_straight_'+pol+'.pdf')
    matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})
    
    # Insertion loss vs wavelength plot
    plt.figure(1)
    linspace = numpy.linspace(wavelength[0],wavelength[len(wavelength)-1], len(insertion_loss_fit))
    fig1 = plt.plot(linspace,insertion_loss_raw, label='Insertion loss (raw)', color='blue')
    fig2 = plt.plot(linspace,insertion_loss_fit, label='Insertion loss (fit)', color='red')
    plt.legend(loc=0)
    plt.ylabel('Loss (dB/cm)', color = 'black')
    plt.xlabel('Wavelength (nm)', color = 'black')
    plt.setp(fig2, 'linewidth', 4.0)
    plt.xlim(round(min(linspace)),round(max(linspace)))
    plt.title("Insertion losses using the cut-back method")
    plt.savefig('WGloss_straight_fit_'+pol+'.pdf')
    matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

    return

# analyze the losses of spiral waveguides by cutback method
def WGloss_spiral(pol):
    # PCM structure ID
    file_ID = 'PCM_PCM_SpiralWG'
    
    # PCM structure lengths
    length = [0, 5733, 9429, 20613]
    
    # measurement port
    PORT = 1
     
    # divide by 10000 to see result in dB/cm
    length_cm = [i/10000 for i in length]
    
    input_data_response = []
    for i in length:
        for filename in os.listdir(os.getcwd()):
            if filename.startswith(file_ID+str(i)+pol) == True:
                print(filename)
                input_data_response.append( SiEPIC_PP.core.parse_response(filename,PORT) )
    
    #%% apply SiEPIC_PP cutback extraction function and plot
    [insertion_loss_wavelength, insertion_loss_fit, insertion_loss_raw] = SiEPIC_PP.core.cutback( input_data_response, length_cm, 1550e-9 )

    # plot all cutback structures responses
    plt.figure(2)
    wavelength = input_data_response[0][0]*1e9
    fig0 = plt.plot(wavelength,input_data_response[0][1], label='L = 0', color='blue')
    fig1 = plt.plot(wavelength,input_data_response[1][1], label='L = 5733 um', color='black')
    fig2 = plt.plot(wavelength,input_data_response[2][1], label='L = 9429 um', color='green')
    fig3 = plt.plot(wavelength,input_data_response[3][1], label='L = 20613 um', color='red')
    plt.legend(loc=0)
    plt.ylabel('Power (dBm)', color = 'black')
    plt.xlabel('Wavelength (nm)', color = 'black')
    plt.xlim(round(min(wavelength)),round(max(wavelength)))
    plt.title("Raw measurement of cutback structures")
    plt.savefig('WGloss_spiral_'+pol+'.pdf')
    matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})
    
    # Insertion loss vs wavelength plot
    plt.figure(3)
    linspace = numpy.linspace(wavelength[0],wavelength[len(wavelength)-1], len(insertion_loss_fit))
    fig1 = plt.plot(linspace,insertion_loss_raw, label='Insertion loss (raw)', color='blue')
    fig2 = plt.plot(linspace,insertion_loss_fit, label='Insertion loss (fit)', color='red')
    plt.legend(loc=0)
    plt.ylabel('Loss (dB/cm)', color = 'black')
    plt.xlabel('Wavelength (nm)', color = 'black')
    plt.setp(fig2, 'linewidth', 4.0)
    plt.xlim(round(min(linspace)),round(max(linspace)))
    plt.title("Insertion losses using the cut-back method")
    plt.savefig('WGloss_spiral_fit_'+pol+'.pdf')
    matplotlib.rcParams.update({'font.size': 14, 'font.family' : 'Times New Roman', 'font.weight': 'bold'})

    return
    return

# analyze the losses of sub-wavelength waveguides by cutback method
def WGloss_SWG():
    return

# analyze the bandwidth and central wavelength of Bragg gratings as a function of corrugation strength
def Bragg_sweep():
    return

# analyze the spectrum of a contra-directional coupler, observe sidelobes and self-reflection
def contraDC():
    return

# analyze the losses of contra-directional coupler (drop port) by cutback method
def contraDCloss():
    return

#%%
URL = 'https://www.dropbox.com/sh/awlo2zj5h1o9zhk/AADN6PL5c-ToW31pXzfpKs84a?dl=1'
pol = 'TE'

PCM_analysis(URL, pol, download = False)
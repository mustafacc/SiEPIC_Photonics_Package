# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 21:10:38 2021

@author: Mustafa Hammood

@description: Load SiEPIC-Tools coordinates files and adjust them for
 automated measurements
"""


def makeFile(f_name):
    """
    Parameters.

    ----------
    f_name : text file
        Original text file to generate the new adjusted file from

    Returns
    -------
    f_new : text file
        New generated text file with adjusted file format
    """
    name_new = f_name.strip('.txt') + '_adjusted.txt'
    f_new = open(name_new, "w+")
    return f_new


def adjustCoords(f_name, del_comment, num_fields):
    """
    Parameters.

    ----------
    f_name : text file
        Original text file to generate the new adjusted file from
    del_comment : Boolean
        flag to trigger deleting trailing ", comment" fields
    num_fields : int
        Number of acceptable fields in the format, i.e., if the format is
        (X, Y, pol, wavelength, type, deviceID) then num_fields = 6

    Returns
    -------
    None.
    """
    f = open(f_name, "r")
    f_new = makeFile(f_name)
    for line in f:
        values = line.rstrip()
        # delete trailing ", comment" fields, if set to True
        if del_comment:
            values = values.strip(', comment')

        values = values.split(', ')

        # reduce an N numbered list to a list of size num_fields, concatenate
        # extra elements with underscore '_'
        if len(values) > num_fields:
            values[num_fields-1:] = ['_'.join(values[num_fields-1:])]

        # populate new line into the new file
        newLine = ', '.join(values) + '\n'
        f_new.write(newLine)

    # wrap up
    f.close()
    f_new.close()


f_coords = r'C:\Users\musta\Nextcloud\Shared\Lab data LC group\MLP01-4060-Scylla\Public\20210826_AdjustCoords\coords.txt'

del_comment = True  # remove additional trailing ", comment" markers

# number of acceptable device fields (X, Y, pol, wavelength, type, deviceID)
# fields after the Nth field are appended to the last field by an underscore
num_fields = 6

adjustCoords(f_coords, del_comment, num_fields)

#!/usr/bin/env python
from .readValues import *
from pandas import DataFrame
import argparse
import os


def main():
    """Main method that implements arguments and options"""
    parser = argparse.ArgumentParser(description='Extra data from .fit files')

    # Arguments and help
    parser.add_argument('-f', '--folder', nargs='*',
                        help='runs fitExtract.py in specified folder paths')
    parser.add_argument('-ls', '--lithiumsymmetric', action='store_true',
                        help='extracts R2 and R3 and assigns to RInt or RElec')
    parser.add_argument('-a', '--additional', nargs='*',
                        help='adds additional parameters to extract')
    parser.add_argument('-c', '--custom', nargs='*',
                        help='extracts custom parameters instead of default')

    # Options
    args = parser.parse_args()

    # Pick one of ls, c, or default
    assert not (args.lithiumsymmetric and args.custom), 'Pick one of -ls or -c'

    # Set params for specified case
    if args.lithiumsymmetric:
        params = ['R2', 'R3']
    elif args.custom:
        params = args.custom
    else:
        params = ['R2']

    # Add more params if -a used
    if args.additional:
        for arg in args.additional:
            params.append(arg)

    # Run in specified folders if -f used, else run in containing folder
    if args.folder:
        for path in args.folder:
            try:
                export(params, args.lithiumsymmetric, correctPath(path))
            except AssertionError:
                print('ERROR: ' + path + ' does not contain any .fit files. Skiping...')
    else:
        try:
            export(params, args.lithiumsymmetric, correctPath(os.getcwd()))
        except AssertionError:
            print('ERROR: current directory does not contain any .fit files. Exiting...')


def export(params, ls_case, path=''):
    """Runs fitExtract.py"""
    extractedValues, paramToUnit, filenames = extract(params, path)

    # Fix filenames
    if path:
        filenames = removePath(filenames, path)
    filenames = removeFileExtension(filenames)

    # Create Table
    table = {'{} ({})'.format(p, paramToUnit[p]): extractedValues[p]
             for p in params}

    # Lithium symmetric case
    if ls_case:
        lithiumSymmetric(extractedValues, table)

    # Create DataFrame and export final data
    df = DataFrame(table)
    df.insert(0, 'File Name', filenames)
    df.to_excel(path + 'Data.xlsx', sheet_name='Sheet 1', index=False)


def lithiumSymmetric(extractedValues, table):
    """Determines RElec and RInt from R2 and R3 and modifies table"""
    RElec = []
    RInt = []
    for R2, R3 in zip(extractedValues['R2'], extractedValues['R3']):
        if R2 > R3:
            RInt.append(R2)
            RElec.append(R3)
        else:
            RInt.append(R3)
            RElec.append(R2)

    # Modify Table
    del table['R2 (Ohm)']
    del table['R3 (Ohm)']
    table['RElectrolyte (Ohm)'] = RElec
    table['RInterface (Ohm)'] = RInt

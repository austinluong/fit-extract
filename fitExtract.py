"""

See README.md for usage instructions

"""

from readFile import *
from pandas import DataFrame
import os
import argparse


def getParamFromSearchParam(searchParam):
    """
    >>> getParamFromSearchParam('R1 =')
    'R1'
    """
    return searchParam[:len(searchParam)-2]


def getSearchParamFromParam(param):
    """
    >>> getSearchParamFromParam('R1')
    'R1 ='
    """
    return param + ' ='


def run(params, ls_case, path=''):
    """Runs fitExtract.py"""

    filenames = getFitFileNames(path)
    searchParams = [getSearchParamFromParam(p) for p in params]
    extractedValues = {p: [] for p in params}
    paramToUnit = {}

    # Iterate through each file in folder
    for filename in filenames:
        # Get lines with parameters and append value to extractedValues
        with open(filename, 'r') as f:
            for line in f:
                for sp in searchParams:
                    if sp in line:
                        p = getParamFromSearchParam(sp)
                        paramToUnit[p] = getUnit(line)
                        extractedValues[p].append(formatString(line))

    # If path specified, fix path and filenames
    if path:
        pathLength = len(path)
        if path[pathLength - 1] != '/':
            path += '/'
            pathLength += 1
        filenames = [filename[pathLength:] for filename in filenames]
    filenames = [filename[:len(filename)-4] for filename in filenames]

    # Create Table
    table = {'{} ({})'.format(p, paramToUnit[p]): extractedValues[p]
             for p in params}

    # Determine RElec (set as R2) and RInt (set as R3) for lithium symmetric
    if ls_case:
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

    # Create DataFrame and export final data
    df = DataFrame(table)
    df.insert(0, 'File Name', filenames)
    df.to_excel(path + 'Data.xlsx', sheet_name='Sheet 1', index=False)


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
    ls_case = False

    # Pick one of ls, c, or default
    assert not (args.lithiumsymmetric and args.custom), 'Pick one of -ls or -c'

    # Set params for specified case
    if args.lithiumsymmetric:
        params = ['R2', 'R3']
        ls_case = True
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
            run(params, ls_case, os.path.normpath(path))
    else:
        run(params, ls_case)


if __name__ == '__main__':
    main()

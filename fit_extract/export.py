#!/usr/bin/env python
import argparse
import os
import timeit
from pandas import DataFrame, ExcelWriter
from .readFiles import *


def appendFileInfo(File, params, extractedValues, names):
    """Appends File info to input arrays"""
    for p in params:
        extractedValues[p].append(getValue(File, p))
    names.append(getName(File))


def appendFileInfoCycles(File, params, extractedValues, names, cyclesColumn):
    """Appends File info to input arrays, for cycles mode"""
    for cycle in getCycleRange(File):
        for p in params:
            extractedValues[p].append(getValue(File, p, cycle))
        names.append('{}_cycle{}'.format(getName(File),
                                         makeCycleSortable(cycle)))
        cyclesColumn.append(cycle + 1)


def export(params, path, paramsToGroupBySize, hasCycles):
    """Formats extracted data and exports to Data.xlsv"""
    paramToUnit, Files = extractFolder(params, path,
                                       paramsToGroupBySize, hasCycles)
    channelToFiles = groupFilesByChannel(Files)
    writer = ExcelWriter(path + 'Data.xlsx')  # Needed to save multiple sheets

    # Iterate through channels
    currentChannelIndex = 1
    numOfChannels = len(channelToFiles)
    for channel in channelToFiles:
        extractedValues = {p: [] for p in params}
        names = []
        cyclesColumn = []

        # Obtain list of values and names from files in channel
        for File in channelToFiles[channel]:
            if hasCycles:
                appendFileInfoCycles(File, params, extractedValues,
                                     names, cyclesColumn)
            else:
                appendFileInfo(File, params, extractedValues, names)

        # Create table / DataFrame
        table = {'{} ({})'.format(p, paramToUnit[p]): extractedValues[p]
                 for p in params}
        df = DataFrame(table)
        df.insert(0, 'File Name', names)
        if hasCycles:
            df.insert(1, 'Cycle', cyclesColumn)
        sheet = 'Ch. ' + channel

        # Add sheets and autofit column dimesntions
        df.to_excel(writer, sheet_name=sheet, index=False)
        writer.sheets[sheet].column_dimensions['A'].width = len(
            max(names, key=len))

        # Message
        print('--Successfully extracted '
              'from {} ({} of {})'.format(sheet,
                                          currentChannelIndex,
                                          numOfChannels))
        currentChannelIndex += 1

    # Export
    writer.save()
    print('')


def main():
    """Implements arguments and options"""
    print('')
    start = timeit.default_timer()
    errorCount = 0

    parser = argparse.ArgumentParser(description='Extra data from .fit files')

    # Arguments and help
    parser.add_argument('-f', '--folder', nargs='+',
                        help='runs fitExtract.py in specified folder paths')
    parser.add_argument('-ap', '--additional_parameters', nargs='+',
                        help='adds additional parameters to extract')
    parser.add_argument('-cp', '--custom_parameters', nargs='+',
                        help='extracts custom parameters instead of default')
    parser.add_argument('-gs', '--groupbysize', nargs=2,
                        help='ensures that two arguments are correctly '
                             'grouped by value size')
    parser.add_argument('-c', '--cycles', action='store_true',
                        help='use this if you data has cycles/loops')

    # Options
    args = parser.parse_args()

    # Set params for specified case
    if args.custom_parameters:
        params = args.custom_parameters
        paramsToGroupBySize = ''
    else:
        params = ['R2', 'R3']
        paramsToGroupBySize = ['R2', 'R3']

    # Group two values by size if -s used
    if args.groupbysize:
        paramsToGroupBySize = args.groupbysize

    # Add more params if -a used
    if args.additional_parameters:
        for arg in args.additional_parameters:
            params.append(arg)

    # Run in specified folders if -f used, else run in containing folder
    if args.folder:
        for path in args.folder:
            try:
                if not os.path.isdir(path):
                    raise OSError
                export(params, correctPath(path),
                       paramsToGroupBySize, args.cycles)
            except AssertionError:
                print('ERROR: ' + path + ' does not contain any .fit files.'
                      ' Skipping...\n')
                errorCount += 1
            except OSError:
                print('ERROR: ' + path + ' is not a valid directory path.'
                      ' Skipping...\n')
                errorCount += 1
    else:
        try:
            export(params, correctPath(os.getcwd()),
                   paramsToGroupBySize, args.cycles)
        except AssertionError:
            print('ERROR: current directory does not contain any .fit files.'
                  ' Exiting...\n')
            errorCount += 1

    # Runtime
    stop = timeit.default_timer()
    time = round(stop - start, 3)
    print('Extraction completed with {} error(s) '
          '(runtime: {} seconds)'.format(errorCount, time))

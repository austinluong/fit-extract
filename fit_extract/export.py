#!/usr/bin/env python
from .readFiles import *
from pandas import DataFrame, ExcelWriter
import argparse
import os
import timeit
import collections


def groupFilesByChannel(Files):
    """Groups files by channel in a dictionary"""
    channelToFiles = {}
    for File in Files:
        channel = nameToChannel(getName(File))
        if channel not in channelToFiles:
            channelToFiles[channel] = [File]
        else:
            channelToFiles[channel].append(File)
    return collections.OrderedDict(sorted(channelToFiles.items()))


def export(params, path, paramsToGroupBySize, has_cycles, testMode=False):
    """Formats extracted data and exports to Data.xlsv"""
    paramToUnit, Files = extractFolder(params, path,
                                       paramsToGroupBySize, has_cycles)
    print('Extracting from {}'.format(path))  # Start message
    channelToFiles = groupFilesByChannel(Files)

    writer = ExcelWriter(path + 'Data.xlsx')  # Needed to save multiple sheets

    # For tests
    if testMode:
        dfs = []

    # Different sheet for each channel
    i = 1
    length = len(channelToFiles)
    for channel in channelToFiles:
        extractedValues = {p: [] for p in params}
        names = []

        # Obtain list of values and names from files in channel
        for File in channelToFiles[channel]:
            # Cycles case
            if has_cycles:
                for cycle in getCycleRange(File):
                    for p in params:
                        extractedValues[p].append(getValue(File, p, cycle))
                    names.append('{}_cycle{}'.format(getName(File),
                                                     makeCycleSortable(cycle)))
            else:
                for p in params:
                    extractedValues[p].append(getValue(File, p))
                names.append(getName(File))

        # Create Table, DataFrame, and export to a sheet
        table = {'{} ({})'.format(p, paramToUnit[p]): extractedValues[p]
                 for p in params}
        df = DataFrame(table)
        df.insert(0, 'File Name', names)
        if testMode:
            dfs.append([df, channel])
        sheet = 'Ch. ' + channel
        df.to_excel(writer, sheet_name=sheet, index=False)
        print('--Successfully extracted '
              'from {} ({} of {})'.format(sheet, i, length))
        i += 1

    # Final export
    if testMode:
        return dfs
    else:
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
                export(params, correctPath(path),
                       paramsToGroupBySize, args.cycles)
            except AssertionError:
                print('ERROR: ' + path + ' does not contain any .fit files.'
                      ' Skiping...\n')
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

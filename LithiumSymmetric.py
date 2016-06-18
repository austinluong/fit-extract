"""
NOTE: Only works for L1+R1+Q2/R2+Q3/R3 circuit

Extracts RInterface and RElectrolyte data from all '.fit' files in
a specified folder and writes the extracted data into a 'Data.xlsx'
in the same folder. '.fit' files are created by clicking save in
the EC-LAB software after fitting (minimizing) a curve with Zfit.

Run from the command line:
$ cd [path]/folder_with_LithiumSymmetric.py
$ python LithiumSymmetric.py [arg1] [arg2] [...]

The arguments are the filepath of the folders (in quotes)
The program will run for each filepath given (infinitely many can be given)

Ex:
$ python LithiumSymmetric.py 'C:\Users\[USER_NAME]\[PATH]' 'C:\Users\[USER_NAME]\[PATH2]'
Result: Data.xlsx file created in both folders specified
"""

from ReadFile import *
from pandas import DataFrame
import sys
import os


def run(path=''):
    filenames = getFitFileNames(path)
    RInterface = []
    RElectrolyte = []

    # Iterate through each file in folder
    for filename in filenames:
        # Get R2 and R3 from file
        f = open(filename, 'r')
        f.readline()  # Title
        f.readline()  # Space
        f.readline()  # Title
        f.readline()  # Subtitle
        f.readline()  # Equivalent Circuit
        f.readline()  # L1
        f.readline()  # R1 = 0.1
        f.readline()  # Q2
        f.readline()  # a2
        R2 = f.readline()  # R2
        f.readline()  # Q3
        f.readline()  # a3
        R3 = f.readline()  # R3

        # Retrieve value from string
        R2 = formatString(R2)
        R3 = formatString(R3)

        # Determine identity of resistance and append
        if R2 > R3:
            RElectrolyte.append(R3)
            RInterface.append(R2)
        else:
            RElectrolyte.append(R2)
            RInterface.append(R3)

    # If path specified
    if path:
        if path[len(path)-1] != '/':
            path += '/'
        # Fix filenames
        filenames = [filename[len(path):] for filename in filenames]

    # Create xlsx of result
    df = DataFrame({'File Name': filenames,
                    'RElectrolyte': RElectrolyte,
                    'RInterface': RInterface})
    df.to_excel(path + 'Data.xlsx', sheet_name='sheet1', index=False)

# Specify folder path in command line if
if len(sys.argv) == 1:
    run()
else:
    for path in sys.argv[1:]:
        run(os.path.normpath(path))

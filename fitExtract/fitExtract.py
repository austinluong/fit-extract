"""See README.md for usage instructions"""


from util import *
from readValues import*
from pandas import DataFrame


def run(params, ls_case, path=''):
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

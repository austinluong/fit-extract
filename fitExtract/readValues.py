#!/usr/bin/env python
from .util import *


def getEndIndex(string):
    """Returns the index of the space after the value before its units

    >>> string = '   R2 = 1 173 Ohm\\n'
    >>> getEndIndex(string)
    13
    """
    lastIndex = len(string) - 1
    while string[lastIndex] != ' ':
        lastIndex -= 1
    return lastIndex


def getNum(string):
    """Returns the value from the extracted string

    >>> string = '   R2 = 1 173 Ohm\\n'
    >>> getNum(string)
    '1 173'
    """
    return string[8:getEndIndex(string)]


def getUnit(string):
    """Returns the unit from the extracted string

    >>> string = '   R2 = 1 173 Ohm\\n'
    >>> getUnit(string)
    'Ohm'
    """
    return string[getEndIndex(string)+1:len(string) - 1]


def removeSpaces(string):
    """Returns a new string with spaces removed from the original string

    >>> string = '1 173'
    >>> removeSpaces(string)
    '1173'
    """
    l = len(string)
    i = 0
    newString = ''
    while i < l:
        currentChar = string[i]
        if currentChar != ' ':
            newString += currentChar
        i += 1
    return newString


def lineToValue(string):
    """Returns a float of the value of a string

    >>> string = '   R2 = 1 173 Ohm\\n'
    >>> formatString(string)
    1173.0
    """
    return float(removeSpaces(getNum(string)))


def extract(params, path=''):
    """Extracts values and units from files in a folder"""
    filenames = getFitFileNames(path)
    assert filenames
    searchParams = [SearchParamFromParam(p) for p in params]
    extractedValues = {p: [] for p in params}
    paramToUnit = {}

    # Iterate through each file in folder
    for filename in filenames:
        # Get lines with parameters and append value to extractedValues
        with open(filename, 'r') as f:
            for line in f:
                for sp in searchParams:
                    if sp in line:
                        p = ParamFromSearchParam(sp)
                        paramToUnit[p] = getUnit(line)
                        extractedValues[p].append(lineToValue(line))
    return extractedValues, paramToUnit, filenames

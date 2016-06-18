"""

Helper functions for reading values from input files
This file is not run directly

"""

import glob


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


def formatString(string):
    """Returns a float of the value of a string

    >>> string = '   R2 = 1 173 Ohm\\n'
    >>> formatString(string)
    1173.0
    """
    return float(removeSpaces(getNum(string)))


def getFitFileNames(path=''):
    """Returns a list of filenames with .fit extension"""
    if path:
        if path[len(path)-1] != '/':
            path += '/'
    return glob.glob(path + '*.fit')

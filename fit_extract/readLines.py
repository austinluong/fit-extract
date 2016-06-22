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
    return string[getEndIndex(string) + 1: -1]


def removeSpaces(string):
    """Returns a new string with spaces removed from the original string

    >>> string = '1 173'
    >>> removeSpaces(string)
    '1173'
    """
    return ''.join([char for char in string if char != ' '])


def lineToValue(string):
    """Returns a float of the value of a string

    >>> string = '   R2 = 1 173 Ohm\\n'
    >>> lineToValue(string)
    1173.0
    """
    return float(removeSpaces(getNum(string)))

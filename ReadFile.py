"""
Helper functions for reading values from input files
This file is not run directly
"""

import glob
import sys


# There is a cleaner way to do this
# but this should work for now
def getNum(string):
    return string[8:len(string)-5]


def removeSpaces(string):
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
    return float(removeSpaces(getNum(string)))


def getFitFileNames(path=''):
    if path:
        if path[len(path)-1] != '/':
            path += '/'
    return glob.glob(path + '*.fit')
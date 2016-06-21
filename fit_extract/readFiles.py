#!/usr/bin/env python
from .readLines import *


def createFile(filepath, name, paramToValue):
    """Creates a dictionary storing file information"""
    File = {'filepath': filepath,
            'name': name,
            'paramToValue': paramToValue}
    return File


def getValue(File, param):
    return File['paramToValue'][param]


def getFilePath(File):
    return File['filepath']


def getName(File):
    return File['name']


def swapValues(File, paramsToSwap):
    """Swaps the values of two parameters (p1, p2)"""
    p1 = paramsToSwap[0]
    p2 = paramsToSwap[1]
    v1 = getValue(File, p1)
    v2 = getValue(File, p2)
    File['paramToValue'][p1] = v2
    File['paramToValue'][p2] = v1
    return File


def extract(params, filepath):
    """Extract values and units of params for a file"""
    searchParams = [SearchParamFromParam(p) for p in params]
    paramToValue = {}
    paramToUnit = {}
    with open(filepath, 'r') as f:
        for line in f:
            for sp in searchParams:
                if sp in line:
                    p = ParamFromSearchParam(sp)
                    paramToValue[p] = lineToValue(line)
                    paramToUnit[p] = getUnit(line)
    return paramToValue, paramToUnit


def extractFolder(params, path, paramsToGroupBySize):
    """Extracts values and units from files in a folder"""
    filepaths = getFitFilePaths(path)
    Files = []
    assert filepaths  # For skip / exit messages
    for filepath in filepaths:
        paramToValue, paramToUnit = extract(params, filepath)
        name = pathToName(filepath)
        File = createFile(filepath, name, paramToValue)
        if paramsToGroupBySize:
            p1 = paramsToGroupBySize[0]
            p2 = paramsToGroupBySize[1]
            v1 = getValue(File, p1)
            v2 = getValue(File, p2)
            if v1 > v2:
                File = swapValues(File, (p1, p2))
        Files.append(File)
    return paramToUnit, Files

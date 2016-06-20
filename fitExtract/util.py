#!/usr/bin/env python
import glob
import os


def correctPath(path):
    """Fixes path name"""
    return os.path.normpath(path) + '/'


def removeFileExtension(filenames):
    """Removes file extension from filename string
    >>> filenames = ['foo.fit', 'bar.fit']
    >>> removeFileExtension(filenames)
    ['foo', 'bar']
    """
    return [filename[:len(filename)-4] for filename in filenames]


def removePath(filenames, path):
    """Remove path from filename string
    >>> pathFoo = 'C://Users//User//Folder//Subfolder//foo.fit'
    >>> pathBar = 'C://Users//User//Folder//Subfolder//bar.fit'
    >>> filenames = [pathFoo, pathBar]
    >>> path = 'C://Users//User//Folder//Subfolder//'
    >>> removePath(filenames, path)
    ['foo.fit', 'bar.fit']
    """
    return [filename[len(path):] for filename in filenames]


def getFitFileNames(path=''):
    """Returns a list of filenames with .fit extension"""
    return glob.glob(path + '*.fit')


def ParamFromSearchParam(searchParam):
    """
    >>> ParamFromSearchParam('R1 =')
    'R1'
    """
    return searchParam[:len(searchParam)-2]


def SearchParamFromParam(param):
    """
    >>> SearchParamFromParam('R1')
    'R1 ='
    """
    return param + ' ='

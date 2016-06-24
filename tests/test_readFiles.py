import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fit_extract.readFiles import *


class test_readFiles(unittest.TestCase):
    def setUp(self):
        File0 = createFile('test_00_C01',
                           {'R2': [100], 'R3': [1]})
        File1 = createFile('test_01_C01',
                           {'R2': [2, 2000], 'R3': [200, 20]}, 2)
        File2 = createFile('test_02_C02',
                           {'R2': [300], 'R3': [3]})
        File3 = createFile('test_03_C02',
                           {'R2': [4], 'R3': [400]})
        File4 = createFile('test_04_C02',
                           {'R2': [5, 4, 2, 20], 'R3': [500, 2, 12, 5]}, 4)
        File5 = createFile('test_05_C03',
                           {'R2': [6], 'R3': [600]})
        self.Files = [File0, File1, File2, File3, File4, File5]

    def test_fileConstructor(self):
        # Get Value
        self.assertEqual(getValue(self.Files[0], 'R2'), 100)
        self.assertEqual(getValue(self.Files[4], 'R3', 2), 12)

        # Set Value
        setValue(self.Files[1], 'R2', 999, 1)
        setValue(self.Files[2], 'R3', 666)
        self.assertEqual(getValue(self.Files[1], 'R2', 1), 999)
        self.assertEqual(getValue(self.Files[2], 'R3'), 666)

        # Get Cycle Range
        self.assertEqual(getCycleRange(self.Files[4]), range(4))

        # Get Name
        self.assertEqual(getName(self.Files[5]), 'test_05_C03')

    def test_swapValues(self):
        paramsToSwap = ['R2', 'R3']
        swapValues(self.Files[3], paramsToSwap)
        self.assertEqual(getValue(self.Files[3], 'R2'), 400)
        self.assertEqual(getValue(self.Files[3], 'R3'), 4)
        swapValues(self.Files[4], paramsToSwap, 2)
        self.assertEqual(getValue(self.Files[4], 'R2', 2), 12)
        self.assertEqual(getValue(self.Files[4], 'R3', 2), 2)

    def test_groupFilesByChannel(self):
        channelToFiles = groupFilesByChannel(self.Files)
        expected = {'1': [self.Files[0], self.Files[1]],
                    '2': [self.Files[2], self.Files[3], self.Files[4]],
                    '3': [self.Files[5]]}
        expected = collections.OrderedDict(sorted(expected.items()))
        self.assertEqual(channelToFiles, expected)

    def test_groupParamsBySize(self):
        paramsToGroupBySize = ['R2', 'R3']
        groupParamsBySize(self.Files[0], paramsToGroupBySize, False)
        self.assertEqual(getValue(self.Files[0], 'R2'), 1)
        groupParamsBySize(self.Files[4], paramsToGroupBySize, True)
        expected = [5, 2, 2, 5]
        actual = [getValue(self.Files[4], 'R2', cycle)
                  for cycle in getCycleRange(self.Files[4])]
        self.assertEqual(expected, actual)

    def test_extract(self):
        thisFilePath = (os.path.dirname(os.path.abspath(__file__)))
        filename = 'testfile_01_heating1_130C_wait3hr_04_PEIS_C01.fit'
        path = thisFilePath + '/batch_mode/' + filename
        [paramToValue, paramToUnit] = extract(['R2', 'R3'], path)
        ptvExpected = {'R2': [float(3.274E2)], 'R3': [118.2]}
        ptuExpected = {'R2': 'Ohm', 'R3': 'Ohm'}
        self.assertEqual(paramToValue, ptvExpected)
        self.assertEqual(paramToUnit, ptuExpected)


if __name__ == '__main__':
    unittest.main()

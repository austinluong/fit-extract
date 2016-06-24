import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fit_extract.export import *


class test_export(unittest.TestCase):
    def setUp(self):
        self.params = ['R2', 'R3']

    def test_appendFileInfo(self):
        extractedValues = {p: [] for p in self.params}
        names = []
        File = createFile('test_00_C01', {'R2': [100], 'R3': [1]})
        appendFileInfo(File, self.params, extractedValues, names)
        evExpected = {'R3': [1], 'R2': [100]}
        namesExpected = ['test_00_C01']
        self.assertEqual(extractedValues, evExpected)
        self.assertEqual(names, namesExpected)

    def test_appendFileInfoCycles(self):
        extractedValues = {p: [] for p in self.params}
        names = []
        cycles_column = []
        File = createFile('test_01_C01',
                          {'R2': [5, 4, 2, 20], 'R3': [500, 2, 12, 5]}, 4)
        appendFileInfoCycles(File, self.params, extractedValues, names, cycles_column)
        evExpected = {'R3': [500, 2, 12, 5], 'R2': [5, 4, 2, 20]}
        namesExpected = ['test_01_C01_cycle001', 'test_01_C01_cycle002',
                         'test_01_C01_cycle003', 'test_01_C01_cycle004']
        ccExpected = [1, 2, 3, 4]
        self.assertEqual(extractedValues, evExpected)
        self.assertEqual(names, namesExpected)
        self.assertEqual(cycles_column, ccExpected)

if __name__ == '__main__':
    unittest.main()

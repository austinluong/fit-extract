import os
import sys
import unittest
import doctest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fit_extract.readLines
import fit_extract.util


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(fit_extract.readLines))
    tests.addTests(doctest.DocTestSuite(fit_extract.util))
    return tests


if __name__ == '__main__':
    unittest.main()

import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fit_extract.export as e


class exportDefaultTest(unittest.TestCase):
    def setUp(self):
        self.params = ['R1', 'R2']
        self.path = (os.path.dirname(os.path.abspath(__file__)))+'\\fitDefault\\'
        self.paramsToGroupBySize = ['R1', 'R2']

    def test_groupFilesByChannel(self):
        pass

    # def test_equal(self):
    #     testMode = True
    #     dfs = e.export(self.params,
    #                    self.path,
    #                    self.paramsToGroupBySize,
    #                    testMode)
    #     df1 = e.DataFrame()
    #     df2 = e.DataFrame()
    #     df3 = e.DataFrame()
    #     dfsExpected = [df1, df2, df3]
    #     for df, dfExpected in zip(dfs, dfsExpected):
    #         self.assertTrue(df[0].equals(dfExpected),
    #                         'Extracting from Ch. {} failed.'.format(df[1]))


if __name__ == '__main__':
    unittest.main()

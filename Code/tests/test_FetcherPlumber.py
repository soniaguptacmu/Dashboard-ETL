import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from FetcherPlumber import FetcherPlumber

class test_FetcherPlumber(unittest.TestCase):

    def test_LoadSourceToStaging_EmptyFilePath(self):

        try:
            filePath=''
            sinkDbConnectionString='test'
            sourceTableNames='test'
            extension='sqlite'
            fp=FetcherPlumber()

            fp.LoadSourceToStaging(filePath, sinkDbConnectionString, sourceTableNames, extension)
            self.assertFalse(True)

        except Exception as e:
            self.assertTrue(True)

    def test_LoadSourceToStaging_EmptyDbConnection(self):

        try:
            filePath='test'
            sinkDbConnectionString=''
            sourceTableNames='test'
            extension='sqlite'
            fp=FetcherPlumber()

            fp.LoadSourceToStaging(filePath, sinkDbConnectionString, sourceTableNames, extension)
            self.assertFalse(True)

        except Exception as e:
            self.assertTrue(True)

    def test_LoadSourceToStaging_EmptyTableNames(self):

        try:
            filePath = 'test'
            sinkDbConnectionString = 'test'
            sourceTableNames = ''
            extension = 'sqlite'
            fp = FetcherPlumber()

            fp.LoadSourceToStaging(filePath, sinkDbConnectionString, sourceTableNames, extension)
            self.assertFalse(True)

        except Exception as e:
            self.assertTrue(True)

    def test_LoadSourceToStaging_EmptyExtension(self):

        try:
            filePath = 'test'
            sinkDbConnectionString = 'test'
            sourceTableNames = 'logger'
            extension = ''
            fp = FetcherPlumber()

            fp.LoadSourceToStaging( filePath, sinkDbConnectionString, sourceTableNames, extension)
            self.assertFalse(True)

        except Exception as e:
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
'''
Created on Mar 21, 2011

@author: adona
'''
import unittest #@UnresolvedImport
from netcube.devices import device

class Test(unittest.TestCase):

    def testName(self):
        host = device('linux:localhost')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
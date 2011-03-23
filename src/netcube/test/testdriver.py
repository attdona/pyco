'''
Created on Mar 21, 2011

@author: adona
'''
import unittest #@UnresolvedImport
from netcube.device import device
from netcube.device import *

#skip = False
skip = True


class Test(unittest.TestCase):
    
    @unittest.skipIf(skip==True,"skipped test")
    def testWrongUrl(self):
        
        self.failUnlessRaises((WrongDeviceUrl), device, 'linux:localhost')


    @unittest.skipIf(skip==False,"skipped test")
    def testEmptyPattern(self):
        log.info("testEmptyPattern ...")
        h = device('ipnet@myhost.com')
        self.assertEqual('myhost.com', h.name)
 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
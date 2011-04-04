'''
Created on Mar 21, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport
from pyco.device import device
from pyco.device import *

skip = False
#skip = True


class Test(unittest2.TestCase):
    
    @unittest2.skipIf(skip==True,"skipped test")
    def testWrongUrl(self):
        
        self.failUnlessRaises((WrongDeviceUrl), device, 'linux:localhost')


    @unittest2.skipIf(skip==True,"skipped test")
    def testEmptyPattern(self):
        log.info("testEmptyPattern ...")
        h = device('ipnet@myhost.com')
        self.assertEqual('myhost.com', h.name)
 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
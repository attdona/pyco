'''
Created on Mar 21, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport
from pyco.device import device, ConnectionRefused

from pyco import log

from .fixture import *

# create logger
log = log.getLogger("test")

class Test(unittest2.TestCase):
    
    def testFakeOk(self):
        print("should not work")
        log.info("testFakeOk ...")
        self.assertEquals(1, 1)
 
 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
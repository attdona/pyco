'''
Created on Mar 21, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport
from pyco.device import device, ConnectionRefused

from pyco import log

# create logger
log = log.getLogger("test")

class Test(unittest2.TestCase):
    
    def testConnectionRefused(self):
        
        log.info("testConnectionRefused ...")
        h = device('telnet://netbox:netbox@localhost')
        self.failUnlessRaises(ConnectionRefused, h.login)
 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
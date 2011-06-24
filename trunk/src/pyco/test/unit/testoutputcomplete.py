'''
Created on Mar 21, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport
from pyco.device import device

from pyco import log

# create logger
log = log.getLogger("test")

class Test(unittest2.TestCase):
    
    def testOutputComplete(self):
        
        log.info("testOutputComplete ...")
        h = device('netbox:netbox@localhost')
        h.checkIfOutputComplete = True
        out = h('id')
        self.assertRegexpMatches(out, 'uid=[0-9]+\(netbox\).*')
 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
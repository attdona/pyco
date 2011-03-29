'''
Created on Mar 21, 2011

@author: adona
'''
import unittest #@UnresolvedImport
from netcube.device import device, ConnectionRefused

from netcube import log

from fixture import *

# create logger
log = log.getLogger("test")

class Test(unittest.TestCase):
    
    def testTelnetOk(self):
        
        log.info("testTelnetOk ...")
        h = device('telnet://%s:%s@%s' % (hop1['username'], hop1['password'], hop1['name']))
        h.maxWait = 20
        out = h('id')
        self.assertRegexpMatches(out, 'uid=[0-9]+\(pyco\).*')
 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
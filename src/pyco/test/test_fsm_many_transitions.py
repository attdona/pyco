'''
Created on Mar 21, 2011

@author: adona
'''
import os
import unittest #@UnresolvedImport
from pyco.device import device, loadConfiguration, ConnectionRefused
import pyco

from pyco import log

from fixture import *

# create logger
log = log.getLogger("test")

class Test(unittest.TestCase):
    
    def testManyTransitions(self):
        
        log.info("testManyTransitions ...")
        module_path = os.path.dirname(pyco.__file__)
        log.debug("module_path: %s" % module_path)
        loadConfiguration(module_path + '/test/pyco_many_transitions.cfg')
        h = device('telnet://%s:%s@%s' % (hop1['username'], hop1['password'], hop1['name']))
        h.maxWait = 20
        out = h('id')
        self.assertRegexpMatches(out, 'uid=[0-9]+\(pyco\).*')
 
        # reload the default configuration
        loadConfiguration()
 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
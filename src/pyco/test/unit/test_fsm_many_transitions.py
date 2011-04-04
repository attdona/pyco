'''
Created on Mar 21, 2011

@author: adona
'''
import os
import unittest2 #@UnresolvedImport
from pkg_resources import resource_filename #@UnresolvedImport

from pyco.device import device, loadConfiguration, ConnectionRefused

from pyco import log
from fixture import *

# create logger
log = log.getLogger("test")

class Test(unittest2.TestCase):
    
    def testManyTransitions(self):
        
        log.info("testManyTransitions ...")
        loadConfiguration(resource_filename('pyco.test.unit', 'pyco_many_transitions.cfg'))
        h = device('telnet://%s:%s@%s' % (hop1['username'], hop1['password'], hop1['name']))
        h.maxWait = 20
        out = h('id')
        self.assertRegexpMatches(out, 'uid=[0-9]+\(pyco\).*')
 
        # reload the default configuration
        loadConfiguration()
 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
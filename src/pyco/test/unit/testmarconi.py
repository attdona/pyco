'''
Created on Mar 14, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport
import os

#from pyco.devices import *
from pyco.device import *

from pyco import log

from fixture import *

#pyco.config.loadConfiguration()

# create logger
log = log.getLogger("testmarconi")

class Test(unittest2.TestCase):

    def setUp(self):
        module_path = os.path.dirname(pyco.__file__)
        log.debug("module_path: %s" % module_path)
        loadConfiguration(module_path + '/test/testmarconi.cfg')
        
    def tearDown(self):
        loadConfiguration()

    def testScript(self):
        h = Device(**localhost)
        h.setDriver('marconi')
        h('id')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
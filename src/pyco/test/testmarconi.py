'''
Created on Mar 14, 2011

@author: adona
'''
import unittest #@UnresolvedImport
import os

#from pyco.devices import *
from pyco.device import *

from pyco import log

#pyco.config.loadConfiguration()

# create logger
log = log.getLogger("testmarconi")


localhost = {
             'name'    :'localhost', 
             'username':'netbox',
             'password':'netbox'
             }

class Test(unittest.TestCase):

    def setUp(self):
        module_path = os.path.dirname(pyco.__file__)
        log.debug("module_path: %s" % module_path)
        loadConfiguration(module_path + '/test/testmarconi.cfg')
        
    def tearDown(self):
        pass

    def testScript(self):
        h = Device(**localhost)
        h.setDriver('marconi')
        h('id')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
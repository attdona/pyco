'''
Created on Mar 14, 2011

@author: adona
'''
import unittest #@UnresolvedImport
import os

#from netcube.devices import *
from netcube.master import *

from netcube import log

#netcube.config.loadFile()

# create logger
log = log.getLogger("testlinux")


localhost = {
             'name'    :'localhost', 
             'username':'netbox',
             'password':'netbox'
             }

class Test(unittest.TestCase):

    def setUp(self):
        module_path = os.path.dirname(netcube.__file__)
        log.debug("module_path: %s" % module_path)
        netcube.config.loadFile(module_path + '/test/testmarconi.cfg')
        
    def tearDown(self):
        pass

    def testScript(self):
        from netcube.devices import Marconi #@UnresolvedImport
        h = Marconi(**localhost)
        h('id')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
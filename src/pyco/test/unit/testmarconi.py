'''
Created on Mar 14, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport
from pkg_resources import resource_filename #@UnresolvedImport

#from pyco.devices import *
from pyco.device import *

from pyco import log

from fixture import *

#pyco.config.loadConfiguration()

# create logger
log = log.getLogger("testmarconi")

class Test(unittest2.TestCase):

    def setUp(self):
        loadConfiguration(resource_filename('pyco.test.unit', 'testmarconi.cfg'))
        
    def tearDown(self):
        loadConfiguration()

    def testScript(self):
        h = Device(**localhost)
        h.set_driver('marconi')
        h('id')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
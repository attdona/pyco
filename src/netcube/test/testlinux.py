'''
Created on Mar 14, 2011

@author: adona
'''
import unittest #@UnresolvedImport
import os

from netcube.master import *
from netcube import log

# create logger
log = log.getLogger("testlinux")


localhost = {
             'name'    :'localhost', 
             'username':'netbox',
             'password':'netbox'
             }

class Test(unittest.TestCase):


    def testScript(self):
        module_path = os.path.dirname(netcube.__file__)
        log.debug("module_path: %s" % module_path)
        netcube.config.loadFile(module_path + '/test/testcore.cfg')
        h = Linux(**localhost)
        h(module_path + '/test/script.py')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
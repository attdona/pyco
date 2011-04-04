'''
Created on Mar 14, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport
import os

from pyco.device import *
from pyco import log
from fixture import *

# create logger
log = log.getLogger("testlinux")

class Test(unittest2.TestCase):

    def tearDown(self):
        loadConfiguration()

    def testScript(self):
        module_path = os.path.dirname(pyco.__file__)
        log.debug("module_path: %s" % module_path)
        loadConfiguration(module_path + '/test/testcore.cfg')
        h = Device(**localhost) #@UndefinedVariable
        h(module_path + '/test/script.py')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
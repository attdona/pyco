'''
Created on Mar 14, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport
from pkg_resources import resource_filename #@UnresolvedImport

from pyco.device import *
from pyco import log
from fixture import *

# create logger
log = log.getLogger("testlinux")

class Test(unittest2.TestCase):

    def tearDown(self):
        loadConfiguration()

    def testScript(self):
        loadConfiguration(resource_filename('pyco.test.unit','testcore.cfg'))
        h = Device(**localhost) #@UndefinedVariable
        h(resource_filename('pyco.test.unit', 'script.py'))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
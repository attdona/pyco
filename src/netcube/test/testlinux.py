'''
Created on Mar 14, 2011

@author: adona
'''
import unittest #@UnresolvedImport
import os

from netcube.device import *
from netcube import log
from fixture import *

# create logger
log = log.getLogger("testlinux")

class Test(unittest.TestCase):

    def testScript(self):
        module_path = os.path.dirname(netcube.__file__)
        log.debug("module_path: %s" % module_path)
        loadFile(module_path + '/test/testcore.cfg')
        h = Device(**localhost) #@UndefinedVariable
        h(module_path + '/test/script.py')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
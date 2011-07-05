'''
Created on Jan 31, 2011
@author: adona

The suggested way to run the tests are throught nosetest:
 ``nosetests --with-coverage --cover-html --cover-package=pyco``

'''
import unittest2 #@UnresolvedImport
import re #@UnresolvedImport
from configobj import ConfigObj #@UnresolvedImport

from pyco.device import *
from pyco import log

from fixture import *

# create logger
log = log.getLogger("test")

    
class Test(unittest2.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def testEmptyPattern(self):
        log.info("testEmptyPattern ...")
        h = device('ssh://username:password@hostame')
        
        pattern = {'event': 'su_event', 'pattern': '', 'beginState': 'USER_PROMPT'}

        h.add_event_action(**pattern)
   

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
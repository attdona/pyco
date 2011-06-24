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

    def testLoopDetection(self):
        '''
        try to connect to fakeLocalhost from a hop device.
        
        fakeLocalhost is accessed with wrong credentilas and so it responds:
         Permission denied, please try again.
        
        '''
        hop = Device(**hop1)
        
        host = Device(hops = [hop], **fakeLocalhost)
        
        self.failUnlessRaises((ConnectionTimedOut,PermissionDenied), host.login)

   

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
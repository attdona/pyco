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

    def testChangePrompt(self):
        '''
        Change the prompt and rediscover it 
        '''
        log.info("testChangePrompt ...")   
        linux = Device(name = loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.rediscoverPrompt = True
        
        linux.login()
        linux.send('PS1=pippo')
        
        self.assertRegexpMatches(linux.prompt['USER_PROMPT'].value, 'pippo')
   

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
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

from .fixture import *

# create logger
log = log.getLogger("test")

    
class Test(unittest2.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def testDynamicPrompt(self):
        '''
        Ever changing prompt case
        '''
        log.info("testChangingPrompt ...")    
        linux = Device(name = loginSuccessfullHost, username='pyco', password='pyco', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.rediscoverPrompt = True
        
        linux('myprompt_counter=1; export PROMPT_COMMAND=\'myprompt_counter=$((myprompt_counter + 1))\'')
        linux('PS1=\'$myprompt_counter \'')
        
        self.assertEqual(linux.discoverPrompt, False, "discoverPrompt must be set to FALSE when unable to discover prompt")
   

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
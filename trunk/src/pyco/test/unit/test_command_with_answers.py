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

    def testCommandWithAnswers(self):
        log.info("testCommandWithAnswers ...")    
        linux = Device(name = loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        def error(target):
            raise AuthenticationFailed
        
        def sendSuPassword(target):
            target.sendLine('pyco')
        
        suPattern = {'event': 'su_event', 'pattern': 'Password: ', 'beginState': 'USER_PROMPT'}
        
        authFailed = {'event': 'auth_failed', 'pattern': 'Authentication failure', 'beginState': 'USER_PROMPT', 'action': error}
        
        suRule = {
                 'beginState' : 'USER_PROMPT',
                 'event': 'su_event',
                 'action' :  sendSuPassword,
                 'endState' : 'USER2_PROMPT'
               }
        
        linux.addEventAction(**suPattern)
        linux.addEventAction(**authFailed)
        linux.addTransition(suRule)
        
        linux.discoverPrompt = True
        
        # rediscover the prompt because su command change it
        linux.rediscoverPrompt = True
        
        linux.send('su pyco')
        output = linux.send('uname -a')
        self.assertRegexpMatches(output, "Linux .*")

   

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
'''
Created on Mar 21, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport
from pyco.device import device, LoginFailed, ConnectionTimedOut

from pyco import log
from . import simulator

from mock import Mock, patch, patch_object, sentinel #@UnresolvedImport

import re #@UnresolvedImport
import sys

if sys.platform != 'win32':
    from pexpect import TIMEOUT, EOF #@UnresolvedImport
    spawnFunction = 'pexpect.spawn'
else:
    from winpexpect import TIMEOUT, EOF #@UnresolvedImport
    spawnFunction = 'winpexpect.winspawn'

# create logger
log = log.getLogger("test")

class Test(unittest2.TestCase):

    @patch(spawnFunction)    
    def _testPromptDiscoveryEnabled(self, MockExpect):
        '''
        If after invoking a cli command the expected prompt is not found in the response a timeout event is triggered. 
        '''
        
        responses = ['pyco@localhost password: ', 
                    '''Linux cencenighe 2.6.32-30-generic #59-Ubuntu SMP Tue Mar 1 21:30:46 UTC 2011 x86_64 GNU/Linux\r
        Ubuntu 10.04.2 LTS\r
        \r
        Welcome to Ubuntu!\r
         * Documentation:  https://help.ubuntu.com/\r
        \r
        Last login: Thu Feb 24 09:05:39 2011 from localhost\r\n$ ''',
        '$ ', 'no prompt']
        log.info("testLoginTimeout ...")
        h = device('telnet://u:p@h')

        MockExpect.side_effect = simulator.side_effect
        simulator.side_effect.responses = responses

        h.login()
         
        self.failUnlessRaises(ConnectionTimedOut, h.send, 'id')
        
    @patch(spawnFunction)    
    def testPromptDiscoveryDisabled(self, MockExpect):
        '''
        Disable the prompt discovery. 
        '''
        
        responses = ['pyco@localhost password: ', 
                    '''Linux cencenighe 2.6.32-30-generic #59-Ubuntu SMP Tue Mar 1 21:30:46 UTC 2011 x86_64 GNU/Linux\r
        Ubuntu 10.04.2 LTS\r
        \r
        Welcome to Ubuntu!\r
         * Documentation:  https://help.ubuntu.com/\r
        \r
        Last login: Thu Feb 24 09:05:39 2011 from localhost\r\n$ some output''',
        'i am pyco']
        
        log.info("testLoginTimeout ...")
        h = device('telnet://u:p@h')
        h.discoverPrompt = False

        MockExpect.side_effect = simulator.side_effect
        simulator.side_effect.responses = responses

        h.login()
         
        h.send('id')
        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
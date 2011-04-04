'''
Created on Mar 21, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport
from pyco.device import device, ConnectionRefused, ConnectionTimedOut

from pyco import log
import simulator

from fixture import *
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

    def setUp(self):
        self.responses = ['Last login: Thu Feb 24 09:05:39 2011 from localhost\r\n$ ', 
            '\r\n$ ', '\r\n$ ']

    @patch(spawnFunction)    
    def testNoPassword(self, MockExpect):
        from pyco.device import cliIsConnected
        log.info("testNoPassword ...")
        #h = device('telnet://%s:%s@%s' % (hop1['username'], hop1['password'], hop1['name']))
        h = device('telnet://u:u@h')
        
        h.removeEvent('username_event', 'GROUND')
        h.addEventAction('timeout', action=cliIsConnected, endState='USER_PROMPT')
        
        MockExpect.side_effect = simulator.side_effect
        simulator.side_effect.responses = self.responses

        out = h.login()
    
        #h.send('id')

    def _testSshNoPassword(self, MockExpect):
        from pyco.device import cliIsConnected
        log.info("testSshNoPassword ...")
        h = device('ssh://%s@%s' % (hop1['username'], hop1['name']))
        
        h.removeEvent('username_event', 'GROUND')
        h.addEventAction('timeout', action=cliIsConnected, endState='USER_PROMPT')
        
        MockExpect.side_effect = simulator.side_effect
        simulator.side_effect.responses = self.responses

        out = h.login()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
'''
Created on Mar 21, 2011

@author: adona
'''
import unittest #@UnresolvedImport
from netcube.device import device, ConnectionRefused, ConnectionTimedOut

from netcube import log
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

  
@patch(spawnFunction)    
class Test(unittest.TestCase):

    def setUp(self):
        self.responses = ['Last login: Thu Feb 24 09:05:39 2011 from localhost\r\n$ ', 
            '$ ', '$ ']



    def testNoPassword(self, MockExpect):
        from netcube.device import cliIsConnected
        log.info("testNoPassword ...")
        h = device('telnet://%s:%s@%s' % (hop1['username'], hop1['password'], hop1['name']))
        
        h.removeEvent('username_event', 'GROUND')
        h.addPattern('timeout', action=cliIsConnected, endState='USER_PROMPT')
        
        MockExpect.side_effect = simulator.side_effect
        simulator.side_effect.responses = self.responses

        out = h.login()
    
        #h.send('id')

    def _testSshNoPassword(self, MockExpect):
        from netcube.device import cliIsConnected
        log.info("testSshNoPassword ...")
        h = device('ssh://%s@%s' % (hop1['username'], hop1['name']))
        
        h.removeEvent('username_event', 'GROUND')
        h.addPattern('timeout', action=cliIsConnected, endState='USER_PROMPT')
        
        MockExpect.side_effect = simulator.side_effect
        simulator.side_effect.responses = self.responses

        out = h.login()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
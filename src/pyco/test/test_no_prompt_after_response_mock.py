'''
Created on Mar 21, 2011

@author: adona
'''
import unittest #@UnresolvedImport
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

  
@patch(spawnFunction)    
class Test(unittest.TestCase):

    def setUp(self):
        self.responses = ['Username: ', 'password: ', 'router> ', 'router> ', 
                          'some output\r\n -- More -- \r\n', 'more output \r\n -- More --\r\n', 'more and more\r\n -- More -- \r\n' ]

    def testNoPassword(self, MockExpect):
        from pyco.device import cliIsConnected
        log.info("testNoPassword ...")
        cisco = device('telnet://%s:%s@%s' % (cisco1['username'], cisco1['password'], cisco1['name']))
        
        from pyco.actions import sendUsername
        cisco.addPattern('username-event', pattern='Username: ', action=sendUsername, states='GROUND')
        
        MockExpect.side_effect = simulator.side_effect
        simulator.side_effect.responses = self.responses

        out = cisco.login()
    
        cisco.send('show version')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
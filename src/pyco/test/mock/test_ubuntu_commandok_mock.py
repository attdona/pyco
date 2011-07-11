'''
Created on Mar 21, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport
from pyco.device import device, ConnectionRefused, ConnectionTimedOut

from pyco import log
import simulator

import pyco.test.mock
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

responses = ['pyco@localhost password: ', 
            '''Linux cencenighe 2.6.32-30-generic #59-Ubuntu SMP Tue Mar 1 21:30:46 UTC 2011 x86_64 GNU/Linux\r
Ubuntu 10.04.2 LTS\r
\r
Welcome to Ubuntu!\r
 * Documentation:  https://help.ubuntu.com/\r
\r
Last login: Thu Feb 24 09:05:39 2011 from localhost\r\n$ ''',
'to be cleared by clear_buffer', '$ ', 'to be cleared by clear_buffer', 'mocked id response\r\n$ ']
  
        
class Test(unittest2.TestCase):

    @patch(spawnFunction)    
    def testTC1(self, MockExpect):
        log.info("testTC1 ...")
        h = device('telnet://u:p@h')
        h.maxWait = 20

        print h.patternMap['GROUND']

        MockExpect.side_effect = simulator.side_effect
        simulator.side_effect.responses = responses

        out = h.login()
    
        h.send('id')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
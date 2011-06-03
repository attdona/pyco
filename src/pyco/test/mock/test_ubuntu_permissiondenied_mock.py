'''
Created on Mar 21, 2011

@author: adona
'''
import unittest2
from pyco.device import device, PermissionDenied

from pyco import log
import simulator

from mock import Mock, patch, patch_object, sentinel

import re
import sys

if sys.platform != 'win32':
    from pexpect import TIMEOUT, EOF #@UnresolvedImport
    spawnFunction = 'pexpect.spawn'
else:
    from winpexpect import TIMEOUT, EOF #@UnresolvedImport
    spawnFunction = 'winpexpect.winspawn'

# create logger
log = log.getLogger("test")

responses = ['nessuno@localhost password: ', 
            '''Permission denied, please try again.\r
nessuno@localhost's password: ''']
  
        
class Test(unittest2.TestCase):

    @patch(spawnFunction)    
    def testTC1(self, MockExpect):
        log.info("testTC1 ...")
        h = device('ssh://nessuno:polifemo@host')

        MockExpect.side_effect = simulator.side_effect
        simulator.side_effect.responses = responses

        self.failUnlessRaises(PermissionDenied, h.login)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
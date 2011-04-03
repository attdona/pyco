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

responses = ['pyco@localhost password: ', 
            '''Linux cencenighe 2.6.32-30-generic #59-Ubuntu SMP Tue Mar 1 21:30:46 UTC 2011 x86_64 GNU/Linux\r
Ubuntu 10.04.2 LTS\r
\r
Welcome to Ubuntu!\r
 * Documentation:  https://help.ubuntu.com/\r
\r
Last login: Thu Feb 24 09:05:39 2011 from localhost\r\n$ ''']
  
def pindex(device, state, event):
    reverseMap = dict(map(lambda item: (item[1],item[0]), device.patternMap[state].items()))

    try:
        pattern = reverseMap[event]
    except:
        if event == 'timeout':
            raise TIMEOUT, 'timeout exceeded'
        else:
            raise
        
    return device.patterns(state).index(pattern)
        
class Test(unittest.TestCase):

    @patch(spawnFunction)    
    def testTC1(self, MockExpect):
        log.info("testTC1 ...")
        h = device('telnet://%s:%s@%s' % (hop1['username'], hop1['password'], hop1['name']))
        h.maxWait = 20

        print h.patternMap['GROUND']

        MockExpect.side_effect = simulator.side_effect
        simulator.side_effect.responses = responses

        out = h.login()
    
        h.send('id')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
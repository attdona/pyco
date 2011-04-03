'''
Created on Mar 21, 2011

@author: adona
'''
import unittest #@UnresolvedImport
from pyco.device import device, ConnectionRefused, ConnectionTimedOut

from pyco import log

from fixture import *
from mock import Mock, patch, patch_object, sentinel #@UnresolvedImport

# create logger
log = log.getLogger("test")

    
def processResponse(self, f):
    print 'XXXXXXXXXXXXXXXXXXXXXXXXX'
    return 'mocked output'
    #raise ConnectionTimedOut(target)
        
class Test(unittest.TestCase):

    @patch('pyco.expectsession.ExpectSession')    
    def testTC1(self, MockExpect):
        log.info("testTC1 ...")
        h = device('telnet://%s:%s@%s' % (hop1['username'], hop1['password'], hop1['name']))
        h.maxWait = 20

        def side_effect(*args, **kwargs):
            print 'SIDE EFFECT'
            h.state = 'USER_PROMPT'
            
            m = Mock()
            m.processResponse = processResponse
            
            return m
        
        MockExpect.side_effect = side_effect
        out = h.login()
    
        h.send('id')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
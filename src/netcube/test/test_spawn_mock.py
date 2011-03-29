'''
Created on Mar 21, 2011

@author: adona
'''
import unittest #@UnresolvedImport
from netcube.device import device, ConnectionRefused, ConnectionTimedOut

from netcube import log

from fixture import *
from mock import Mock, patch, patch_object, sentinel

import sys
if sys.platform != 'win32':
    from pexpect import TIMEOUT, EOF #@UnresolvedImport
else:
    from winpexpect import TIMEOUT, EOF #@UnresolvedImport

# create logger
log = log.getLogger("test")

responses = ['pyco@localhost password: ']    
  
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

    @patch('winpexpect.winspawn')    
    def testTC1(self, MockExpect):
        log.info("testTC1 ...")
        h = device('telnet://%s:%s@%s' % (hop1['username'], hop1['password'], hop1['name']))
        h.maxWait = 20

        print h.patternMap['GROUND']


        
        def side_effect(*args, **kwargs):
            print 'SIDE EFFECT'
            #h.state = 'USER_PROMPT'
            
            m = Mock()
            
            events = [('username_event',''), ('password_event',''), ('timeout','$ ')]
            def expect(self, maxTime):
                print 'XXXXXXXXXXXXXXXXXX'
                print self
            
                #return the index relative to event_name
                event, m.before = events.pop(0)
                print 'event [%s] - before [%s]' % (event,m.before)
                idx = pindex(h, 'GROUND', event)
                
                
                print 'returning index [%d]' % idx
                return idx
                        
            m.expect = expect
            
            return m
        
        MockExpect.side_effect = side_effect
        out = h.login()
    
        h.send('id')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
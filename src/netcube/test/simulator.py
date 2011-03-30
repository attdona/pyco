'''
Created on Mar 30, 2011

@author: adona
'''
import re #@UnresolvedImport
import sys

if sys.platform != 'win32':
    from pexpect import TIMEOUT, EOF #@UnresolvedImport
    spawnFunction = 'pexpect.spawn'
else:
    from winpexpect import TIMEOUT, EOF #@UnresolvedImport
    spawnFunction = 'winpexpect.winspawn'

from mock import Mock, patch, patch_object, sentinel #@UnresolvedImport


def responder(mock, responses, patterns, maxTime):
    
    print 'XXXXXXXXXXXXXXXXXX'
    print patterns

    #return the index relative to event_name
    response = responses.pop(0)
    print 'response [%s]' % (response)
    
    idx = 0
    toBeMatched = True
    while toBeMatched and idx < len(patterns):
        
        search = '(.*)(%s)' % patterns[idx]
        print "re: [%s]" % search
        if patterns[idx] == TIMEOUT:
            print 'BINGO !!!!!!!!!!'
            toBeMatched = False
            break
        match = re.match(search, response)
        if match:
            toBeMatched = False
            mock.before = match.group(1)
            mock.after  = match.group(2) 
            break
        idx+=1
    
    if idx < len(patterns):
        print 'returning index [%d]' % idx
        return idx
    else:
        mock.before = response
        mock.after = TIMEOUT
        raise TIMEOUT, 'wait time exceeded'

def side_effect(*args, **kwargs):
    print 'SIDE EFFECT'
    #h.state = 'USER_PROMPT'
    
    m = Mock()
    
    def expect(patterns, maxTime):
        return responder(m, side_effect.responses, patterns, maxTime)

    m.expect = expect
    
    return m


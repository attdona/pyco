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
from pyco import log

# create logger
log = log.getLogger("sim")


def responder(mock, responses, patterns, maxTime):
    
    log.debug('entering MOCK responder')
    print patterns

    #return the index relative to event_name
    response = responses.pop(0)
    log.debug('current response [%s]' % (response))
    
    idx = 0
    toBeMatched = True
    while toBeMatched and idx < len(patterns):
        
        search = '(.*)(%s)' % patterns[idx]
        log.debug("checking [%d] regexp: [%s]" % (idx, search))
        if patterns[idx] == TIMEOUT:
            
            toBeMatched = False
            mock.before = response
            mock.after  = TIMEOUT

            break
        match = re.match(search, response)
        if match:
            toBeMatched = False
            mock.before = match.group(1)
            mock.after  = match.group(2) 
            break
        idx+=1
    
    if idx < len(patterns):
        log.debug('returning index [%d]' % idx)
        return idx
    else:
        mock.before = response
        mock.after = TIMEOUT
        raise TIMEOUT, 'wait time exceeded'

def side_effect(*args, **kwargs):
    
    m = Mock()
    
    def expect(patterns, maxTime):
        return responder(m, side_effect.responses, patterns, maxTime)

    m.expect = expect
    
    return m


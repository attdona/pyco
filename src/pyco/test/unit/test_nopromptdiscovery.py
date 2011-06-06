'''
Created on Mar 14, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport
import os

from pyco.device import *
from pyco import log
from fixture import *

# create logger
log = log.getLogger("test_no_prompt_discovery")


class Test(unittest2.TestCase):

    def testWithPromptDiscovery(self):
        url = "ssh://%s:%s@%s/linux" % (localhost['username'], localhost['password'], localhost['name'])
        
        h = device(url)
        
        #h.discoverPrompt = True
        
        h.login()
        out = h.send('id')
        
        log.debug('[[%s]]' % out)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
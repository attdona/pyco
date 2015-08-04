'''
Created on Mar 14, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport
import os

from pyco.device import *
from pyco import log
from .fixture import *

# create logger
log = log.getLogger("test_no_prompt_discovery")


class Test(unittest2.TestCase):

    def setUp(self):
        loadConfiguration(resource_filename('pyco.test.unit', 'test_nopromptdiscovery.cfg'))
        
    def tearDown(self):
        loadConfiguration()
        pass
    
    def _testWithPromptDiscovery(self):
        url = "ssh://%s:%s@%s/linux" % (localhost['username'], localhost['password'], localhost['name'])
        
        h = device(url)
        
        h.login()
        out = h.send('id')
        
        log.debug('[[%s]]' % out)

    def testWithPromptDiscoveryDisabled(self):
        url = "ssh://%s:%s@%s/no-discovery" % (localhost['username'], localhost['password'], localhost['name'])
        
        h = device(url)
        
        h.login()
        out = h.send('id')
        
        log.debug('[[%s]]' % out)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
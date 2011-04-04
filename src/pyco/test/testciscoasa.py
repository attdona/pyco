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
log = log.getLogger("testciscoasa")

@unittest2.skip("skip because device not more available")
class Test(unittest2.TestCase):

    def testTelnet(self):
        url = "telnet://%s:%s@%s/ciscoios" % (asa1['username'], asa1['password'],asa1['name'])
        
        h = device(url)
        h.login()
        out = h.send('show version')
        
        log.debug('[[%s]]' % out)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
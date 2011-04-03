'''
Created on Mar 14, 2011

@author: adona
'''
import unittest #@UnresolvedImport
import os

from pyco.device import *
from pyco import log
from fixture import *

# create logger
log = log.getLogger("testciscoasa")


class Test(unittest.TestCase):

    def testTelnet(self):
        url = "telnet://%s:%s@%s/ciscoios" % (asa1['username'], asa1['password'],asa1['name'])
        
        h = device(url)
        h.login()
        out = h.send('show version')
        
        log.debug('[[%s]]' % out)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
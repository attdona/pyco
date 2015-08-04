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
log = log.getLogger("testciscoasa")

#@unittest2.skip("skip because device not more available")
class Test(unittest2.TestCase):

    def test(self):
        '''
        test with a ciscoios driver because similar to asa, at least for test purposes
        '''
        url = "ssh://%s:%s@%s/ciscoios" % (asa1['username'], asa1['password'],asa1['name'])
        
        h = device(url)
        h.login()
        out = h.send('show version')
        
        self.assertRegexpMatches(out, 'Cisco Adaptive Security Appliance .*')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
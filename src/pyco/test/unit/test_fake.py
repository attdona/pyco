'''
Created on Mar 21, 2011

@author: adona
'''
import unittest #@UnresolvedImport
from pyco.device import device, ConnectionRefused, PermissionDenied
from os import environ

from pyco import log


TELNET_PORT = 7777

# create logger
log = log.getLogger("test")

class Test(unittest.TestCase):
    
    #@unittest.skip("skipping")
    def testFakeOk(self):
        log.debug("testFakeOk ...")
        h = device('telnet://%s:%s@%s:%d' % 
                   ('username', 'secret', 'localhost',TELNET_PORT))
        
        h.maxWait = 2
        out = h('id')
        print("--> %s" % out) 
        self.assertRegex(out, 'uid=[0-9]+\(pyco\).*')

    @unittest.skip("skipping")
    def testWrongPassword(self):
        log.debug("testWrongPassword ...")
        h = device('telnet://%s:%s@%s:%d' % 
                   ('username', 'wrong_pwd', 'localhost', TELNET_PORT))
        
        self.assertRaises(PermissionDenied, h, 'id')

    @unittest.skip("skipping")
    def testNativeTelnet(self):
        log.info("testNative ...")
        user = environ['USER']
        log.info("USER: [%s]" % user)
        h = device('telnet://%s:%s@%s' % (user, user, 'localhost'))
        h.maxWait = 10
        
        self.assertRaises(PermissionDenied, h, 'id')
 
 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
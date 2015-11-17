'''
Created on Mar 21, 2011

@author: adona
'''
import unittest #@UnresolvedImport
from pyco.device import device, ConnectionRefused, PermissionDenied
from os import environ

from pyco import log

from utils import setface

TELNET_PORT = 7777
# create logger
log = log.getLogger("test")


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        log.debug("setting face to linux")
        setface("linux")
 
    #@unittest.skip("skipping")
    def testSimpleCommand(self):
        log.debug("starting testSimpleCommand ...")
        target = device('telnet://%s:%s@%s:%d' % 
                ('kenobi', 'secret', 'localhost', TELNET_PORT))
        
        target.maxWait = 2
        out = target('id')
        target.close()
        self.assertRegex(out, 'uid=[0-9]+\(pyco\).*')

    #@unittest.skip("skipping")
    def testWrongPassword(self):
        log.debug("testWrongPassword ...")
        target = device('telnet://%s:%s@%s:%d' % 
                   ('kenobi', 'wrong_pwd', 'localhost', TELNET_PORT))
        target.close()
        self.assertRaises(PermissionDenied, target, 'id')

    #@unittest.skip("skipping")
    def testWrongUsername(self):
        log.debug("testWrongUsername ...")
        target = device('telnet://%s:%s@%s:%d' % 
                   ('fake_username', 'secret', 'localhost', TELNET_PORT))
        target.close()
        self.assertRaises(PermissionDenied, target, 'id')

    #@unittest.skip("skipping")
    def testConnectionRefused(self):
        log.debug("testConnectionRefused ...")
        target = device('telnet://%s:%s@%s:%d' % 
                   ('fake_username', 'secret', 'localhost', 9999))
        target.close()
        self.assertRaises(ConnectionRefused, target, 'id')



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
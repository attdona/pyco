'''
Created on Apr 4, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport

from fixture import cisco1
from pyco.device import device, PermissionDenied

class Test(unittest2.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    @unittest2.skipIf(cisco1['name'] == '', "ciscoIOS router not available in this test setup")
    def testAuthenticationFailure(self):
        cisco = device('telnet://%s:%s@%s/ciscoios' % (cisco1['username'], 'fake-password', cisco1['name']))

        self.assertRaises(PermissionDenied, cisco.login)
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
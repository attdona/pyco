'''
Created on Apr 4, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport

from .fixture import cisco1
from pyco.device import device

from pkg_resources import resource_filename #@UnresolvedImport

from pyco.device import loadConfiguration

cfgFile = resource_filename('pyco.test.unit', 'pyco-ciscoios.cfg')

class Test(unittest2.TestCase):

    def setUp(self):
        loadConfiguration(cfgFile)


    def tearDown(self):
        loadConfiguration()

    @unittest2.skipIf(cisco1['name'] == '', "ciscoIOS router not available in this test setup")
    def test_simple_cfg(self):
        cisco = device('telnet://%s:%s@%s/ciscoios' % (cisco1['username'],cisco1['password'],cisco1['name']))

        try:
            cisco.login()
            cisco('show version')
        except Exception as e:
            #print(e.interactionLog)
            raise


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
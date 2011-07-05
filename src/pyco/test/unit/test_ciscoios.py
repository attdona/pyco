'''
Created on Apr 4, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport

from fixture import cisco1
from pyco.device import device

class Test(unittest2.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest2.skipIf(cisco1['name'] == '', "ciscoIOS router not available in this test setup")
    def _testTimeoutOnCommand(self):
        cisco = device('telnet://%s:%s@%s' % (cisco1['username'],cisco1['password'],cisco1['name']))

        from pyco.actions import sendUsername
        cisco.add_event_action('username-event', pattern='Username: ', action=sendUsername, beginState='GROUND')

        cisco.login()

        cisco('show version')


    @unittest2.skipIf(cisco1['name'] == '', "ciscoIOS router not available in this test setup")
    def _testExternalAction(self):
        cisco = device('telnet://%s:%s@%s/ciscoios' % (cisco1['username'],cisco1['password'],cisco1['name']))

        cisco.login()

        cisco('show version')


    @unittest2.skipIf(cisco1['name'] == '', "ciscoIOS router not available in this test setup")
    def testLongOutput(self):
        cisco = device('telnet://%s:%s@%s/ciscoios' % (cisco1['username'],cisco1['password'],cisco1['name']))

        try:
            cisco.login()

            cisco('enable')
        
            cisco('show running-config')
        except Exception as e:
            #print(e.interactionLog)
            raise


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
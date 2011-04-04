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


    def testTimeoutOnCommand(self):
        cisco = device('telnet://%s:%s@%s' % (cisco1['username'],cisco1['password'],cisco1['name']))

        from pyco.actions import sendUsername
        cisco.addEventAction('username-event', pattern='Username: ', action=sendUsername, beginState='GROUND')

        cisco.login()

        cisco('show version')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
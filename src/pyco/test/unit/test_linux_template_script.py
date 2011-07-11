'''
Created on Apr 4, 2011

@author: adona
'''
import unittest2 #@UnresolvedImport

from fixture import localhost
from pyco.device import device

class Test(unittest2.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTemplateScript(self):
        field_map = {
                     'dir': '/home/adona/dev',
                     'monitored_port': 8080
                     }
        
        template = '''cd ${dir}
ls -la
netstat -n | grep ${monitored_port}
'''
        
        h = device('ssh://%s:%s@%s' % (localhost['username'],localhost['password'],localhost['name']))
        h.login()

        out = h.send(template, field_map)
        
        print '<<%s>>' % out




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
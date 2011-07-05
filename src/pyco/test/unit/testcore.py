'''
Created on Jan 31, 2011
@author: adona

The suggested way to run the tests are throught nosetest:
 ``nosetests --with-coverage --cover-html --cover-package=pyco``

'''
import unittest2 #@UnresolvedImport
import re #@UnresolvedImport
from configobj import ConfigObj

from pyco.device import *
from pyco import log

from fixture import *

# create logger
log = log.getLogger("test")

skip = False
#skip = True

#@unittest2.skip("temp skip")
class TestConstraints(unittest2.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    @unittest2.skipIf(skip==True,"skipped test")
    def testGetExactStringForMatch(self):
        prompts = ['pyco@cencenighe $', 'xxx $$', 'xyz\r\n{} [ ', '% *']
        
        for str in prompts:
            result = getExactStringForMatch(str) #@UndefinedVariable
            
            p = re.compile(result)
            
            m = p.match(str)
            if not m:
                self.assertEqual(True,False,'escaped regexp from testGetExactStringForMatch not match')
            
            self.assertEqual(m.group(), str)
        
       
    @unittest2.skipIf(skip==True,"skipped test")
    def testPermissionDenied(self):
        h = Device(**fakeLocalhost)
        self.failUnlessRaises(PermissionDenied, h.login)
    
#@unittest2.skip("temp skip")
class Test(unittest2.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    @unittest2.skipIf(skip==True,"skipped test")
    def testUnableToConnectToRemoteHost(self):
        log.info("testUnableToConnectToRemoteHost ...")
        h = Device(username='ipnet', name = unableToConnectHost, password='ipnet')
        #h.maxWait = 60
        self.failUnlessRaises((ConnectionClosed,LoginFailed), h.login)


        
    @unittest2.skipIf(skip==True,"skipped test")    
    def testSendCommand(self):
        '''
        Send a simple command without prompt discovery
        '''    
        log.info("testSendCommand ...")
        linux = Device(name = loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        linux.discoverPrompt = False
        linux.login()
        output = linux.send('id')
        
        log.info("testSendCommand id = [%s]" % output)
        self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")
        self.assertTrue('USER_PROMPT' not in linux.prompt, 'prompt discovered unexpectedly')
        
    @unittest2.skipIf(skip==True,"skipped test")    
    def testSendCommandWithPromptDiscovery(self):
        '''
        Send a simple command with prompt discovery
        '''
        log.info("testSendCommandWithPromptDiscovery ...")
        
        linux = Device(name = loginSuccessfullHost, username='pyco', password='pyco', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.login()
        output = linux.send('id')
        
        log.info("testSendCommandWithPromptDiscovery: id = [%s]" % output)
        self.assertRegexpMatches(output, "uid=[0-9]+\\(pyco\\)")
        self.assertTrue('USER_PROMPT' in linux.prompt, 'prompt not discovered')


    @unittest2.skipIf(skip==True,"skipped test")    
    def testSendCommandWithPromptRegexpTc0(self):
        '''
        multi line prompt discovery using the promptRegexp parameter
        The discovered prompt is a multiline prompt
        '''
        log.info("testSendCommandWithPromptRegexpTc0 ...")
        linux = Device(name = loginSuccessfullHost, username='pyco', password='pyco', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.promptRegexp = r"[^\r\n]*@.*\r\n~\$ "
        
        linux.discover_prompt_with_regexp(linux.promptRegexp, state='USER_PROMPT')
        
        linux.login()
        output = linux.send('id')
        
        self.assertRegexpMatches(output, "uid=[0-9]+\\(pyco\\)")
        self.assertTrue('USER_PROMPT' in linux.prompt, 'prompt not discovered')

    @unittest2.skipIf(skip==True,"skipped test")    
    def testSendCommandWithPromptRegexpTc1(self):
        '''
        one line prompt discovery using the promptRegexp parameter
        The discovered prompt is a single line prompt
        '''  
        log.info("testSendCommandWithPromptRegexpTc1 ...")  
        linux = Device(name = loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.promptRegexp = r"\$ "
        
        linux.discover_prompt_with_regexp(linux.promptRegexp, state='USER_PROMPT')
        
        linux.login()
        output = linux.send('id')
        
        log.info("testSendCommandWithPromptRegexpTc1: id = [%s]" % output)
        self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")
        self.assertTrue('USER_PROMPT' in linux.prompt, 'prompt not discovered')


    @unittest2.skipIf(skip==True,"skipped test")    
    def testOutputCompleteOnPromptMatch(self):
        '''
        Send simple commands and use prompt match only
        '''
        log.info("testOutputCompleteOnPromptMatch ...") 
        linux = Device(name = loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.checkOnOutputComplete = True
        
        linux.login()
        output = linux.send('id')
        
        self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")
        self.assertTrue('USER_PROMPT' in linux.prompt, 'prompt not discovered')

    @unittest2.skipIf(skip==True,"skipped test")    
    def testOutputCompleteOnPromptMatchTc2(self):
        '''
        Send simple commands and use prompt match only with promptDiscovery disabled
        expected result:  
        ''' 
        log.info("testOutputCompleteOnPromptMatchTc2 ...")   
        linux = Device(name = loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        linux.discoverPrompt = False
        linux.checkOnOutputComplete = False
        
        linux.login()
        output = linux.send('id')
        
        self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")


    @unittest2.skipIf(skip==True,"skipped test")    
    def testMultilinePrompt(self):
        '''
        Discover a multiline prompt
        '''
        log.info("testMultilinePrompt ...")    
        linux = Device(name = loginSuccessfullHost, username='pyco', password='pyco', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.checkOnOutputComplete = False
        
        output = linux.send('id')
        
        self.assertRegexpMatches(output, "uid=[0-9]+\\(pyco\\)")

        


    @unittest2.skipIf(skip==True,"skipped test")    
    def testSendCommandAfterClose(self):
        log.info("testSendCommandAfterClose ...")    
        linux = Device(name = loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        output = linux.send('uname -a')
        self.assertRegexpMatches(output, "Linux .*")
        try:
            linux.send('exit')
        except:
            output = linux.send('id')
            self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")


      
#@unittest2.skip("temp skip")
class TestHops(unittest2.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    @unittest2.skipIf(skip==True,"skipped test")    
    def testHopConnection(self):
        '''
        Connect successfully through a hop:
        
        '''
        log.info("testHopConnection ...") 
        hop = Device(**hop1)
        
        host = Device(hops = [hop], **hop2)
        out = host('id')
        self.assertRegexpMatches(out, hop2['username'])
        

    @unittest2.skipIf(skip==True,"skipped test")    
    def testWhereAmI(self):
        '''
        
        '''
        log.info("testWhereAmI ...")    
        
        host = path([Device(**hop1), Device(**hop2), Device(**hop3)])
        
        try:
            host.login()
        except:
            d = host.where_am_i()
            log.debug("target host: [%s], connected host: [%s]" % (host.name, d.name))

            self.assertEqual(d.name, hop2['name'], 'where_am_i unexpected result')


    @unittest2.skipIf(skip==True,"skipped test")    
    def testExpectLoop(self):
        '''
        
        '''
        log.info("testExpectLoop ...")    
       
        config = ConfigObj()
        
        config['Common'] = {
                                'sshCommand' : 'ssh ${device.username}@${device.name}'
                           }
        
        host = path([Device(**hop1), Device(**hop2), Device(**hop3)])
        
        try:
            host.login()
        except:
            d = host.where_am_i()
            log.debug("target host: [%s], connected host: [%s]" % (host.name, d.name))

            self.assertRaises((ConnectionClosed), host, 'uname -a')

    @unittest2.skipIf(skip==True,"skipped test")    
    def testMinimalCfg(self):
        '''
        test a minimal configuration
        '''
        
        log.info("testMinimalCfg ...")    
       
        config = ConfigObj()
        
        config['common'] = {
                                # 'sshCommand' : 'ssh ${device.username}@${device.name}'
                                'events' : {
                                                'password_event': {
                                                                    'pattern': '[pP]assword: ',
                                                                    'beginState' : 'GROUND',
                                                                    'action': 'sendPassword',
                                                                    'endState': 'USER_PROMPT'
                                                                  }
                                                                  
                                           }
                           }
        
        # reload the configuration
        reload(config)
        
        host = Device(**localhost)
        
        try:
            out = host('id')
            self.assertRegexpMatches(out, 'uid=[0-9]+')
        finally:
            loadConfiguration()
            
    @unittest2.skipIf(skip==True,"skipped test")    
    def testPermissionDenied(self):
        '''
        test wrong username/password
        '''
        log.info("testPermissionDenied ...")    
        
        
        host = Device(**fakeLocalhost)
        
        self.assertRaises(PermissionDenied, host.login)
   

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest2.main()
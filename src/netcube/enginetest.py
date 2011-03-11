'''
Created on Jan 31, 2011

@author: adona
'''
import unittest #@UnresolvedImport
import re #@UnresolvedImport
from configobj import ConfigObj #@UnresolvedImport

from netcube.master import *
from netcube.exceptions import *
from netcube import log
import netcube.config

# create logger
log = log.getLogger("test")

unableToConnectHost =  "163.162.155.91"
loginSuccessfullHost = "127.0.0.1"
targetCommand = "uname -a"

fakeLocalhost = {
             'name'    :'localhost', 
             'username':'netcube',
             'password':'netcube'
             }

hop1 = {
            'name'     : '163.162.155.60',
            'username' : 'riccardo',
            'password' : 'mario'
        }

hop2 = {
            'name'     : '163.162.155.90',
            'username' : 'netbox',
            'password' : 'netbox'
        }

hop3 = {
            'name'     : '163.162.155.91',
            'username' : 'netbox',
            'password' : 'netbox'
        }



#skip = False
skip = True

@unittest.skip("temp skip")
class TestConstraints(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    @unittest.skipIf(skip==True,"skipped test")
    def testGetExactStringForMatch(self):
        prompts = ['pyco@cencenighe $', 'xxx $$', 'xyz\r\n{} [ ', '% *']
        
        for str in prompts:
            result = getExactStringForMatch(str)
            
            p = re.compile(result)
            
            m = p.match(str)
            if not m:
                self.assertEqual(True,False,'escaped regexp from testGetExactStringForMatch not match')
            
            self.assertEqual(m.group(), str)
        
    @unittest.skipIf(skip==True,"skipped test")
    def testRegexp(self):
        str = 'abc\r\nxyz'
        p = re.compile('\r\n.*$', re.MULTILINE)
        m = p.match(str)
        
        print m.group()
        
    @unittest.skipIf(skip==True,"skipped test")
    def testNoName(self):
        h = Linux(**fakeLocalhost)
        h.login()
        #self.failUnlessRaises(NetworkException, h.login)
    
#@unittest.skip("temp skip")
class Test(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    @unittest.skipIf(skip==True,"skipped test")
    def testEmptyPattern(self):
        log.info("testEmptyPattern ...")
        h = Linux(username='ipnet', name = unableToConnectHost, password='Hie.g00I')
        
        pattern = {'event': 'su_event', 'pattern': '', 'states': 'USER_PROMPT'}

        h.addPattern(**pattern)


    @unittest.skipIf(skip==True,"skipped test")
    def testUnableToConnectToRemoteHost(self):
        log.info("testUnableToConnectToRemoteHost ...")
        kabul = Linux(username='ipnet', name = unableToConnectHost, password='Hie.g00I')
    
        self.failUnlessRaises(ConnectionClosed, kabul.login)


        
    @unittest.skipIf(skip==True,"skipped test")    
    def testSendCommand(self):
        '''
        Send a simple command without prompt discovery
        '''    
        log.info("testSendCommand ...")
        linux = Linux(name = loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        linux.discoverPrompt = False
        linux.login()
        output = linux.send('id')
        
        log.info("testSendCommand id = [%s]" % output)
        self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")
        self.assertTrue('USER_PROMPT' not in linux.prompt, 'prompt discovered unexpectedly')
        
    @unittest.skipIf(skip==False,"skipped test")    
    def testSendCommandWithPromptDiscovery(self):
        '''
        Send a simple command with prompt discovery
        '''
        log.info("testSendCommandWithPromptDiscovery ...")
        
        linux = Linux(name = loginSuccessfullHost, username='pyco', password='pyco', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.login()
        output = linux.send('id')
        
        log.info("testSendCommandWithPromptDiscovery: id = [%s]" % output)
        self.assertRegexpMatches(output, "uid=[0-9]+\\(pyco\\)")
        self.assertTrue('USER_PROMPT' in linux.prompt, 'prompt not discovered')


    @unittest.skipIf(skip==True,"skipped test")    
    def testSendCommandWithPromptRegexpTc0(self):
        '''
        Send a simple command with prompt discovery using the promptRegexp parameter
        The discovered prompt is a multiline prompt
        '''
        log.info("testSendCommandWithPromptRegexpTc0 ...")
        linux = Linux(name = loginSuccessfullHost, username='pyco', password='pyco', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.promptRegexp = r"[^\r\n]*@.*\r\n~\$ "
        
        linux.discoverPromptWithRegexp(linux.promptRegexp, state='USER_PROMPT')
        
        linux.login()
        output = linux.send('id')
        
        self.assertRegexpMatches(output, "uid=[0-9]+\\(pyco\\)")
        self.assertTrue('USER_PROMPT' in linux.prompt, 'prompt not discovered')

    @unittest.skipIf(skip==True,"skipped test")    
    def testSendCommandWithPromptRegexpTc1(self):
        '''
        Send a simple command with prompt discovery using the promptRegexp parameter
        The discovered prompt is a single line prompt
        '''  
        log.info("testSendCommandWithPromptRegexpTc1 ...")  
        linux = Linux(name = loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.promptRegexp = r"\$ "
        
        linux.discoverPromptWithRegexp(linux.promptRegexp, state='USER_PROMPT')
        
        linux.login()
        output = linux.send('id')
        
        log.info("testSendCommandWithPromptRegexpTc1: id = [%s]" % output)
        self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")
        self.assertTrue('USER_PROMPT' in linux.prompt, 'prompt not discovered')


    @unittest.skipIf(skip==True,"skipped test")    
    def testOutputCompleteOnPromptMatch(self):
        '''
        Send simple commands and use prompt match only
        '''
        log.info("testOutputCompleteOnPromptMatch ...") 
        linux = Linux(name = loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.checkOnOutputComplete = True
        
        linux.login()
        output = linux.send('id')
        
        self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")
        self.assertTrue('USER_PROMPT' in linux.prompt, 'prompt not discovered')

    @unittest.skipIf(skip==True,"skipped test")    
    def testOutputCompleteOnPromptMatchTc2(self):
        '''
        Send simple commands and use prompt match only with promptDiscovery disabled
        expected result:  
        ''' 
        log.info("testOutputCompleteOnPromptMatchTc2 ...")   
        linux = Linux(name = loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        linux.discoverPrompt = False
        linux.checkOnOutputComplete = False
        
        linux.login()
        output = linux.send('id')
        
        self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")

    @unittest.skipIf(skip==True,"skipped test")    
    def testChangePrompt(self):
        '''
        Change the prompt and rediscover it 
        '''
        log.info("testChangePrompt ...")   
        linux = Linux(name = loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.checkOnOutputComplete = False
        
        linux.login()
        linux.send('PS1=pippo')
        
        self.assertRegexpMatches(linux.prompt['USER_PROMPT'].value, 'pippo')

    @unittest.skipIf(skip==True,"skipped test")    
    def testMultilinePrompt(self):
        '''
        Discover a multiline prompt
        '''
        log.info("testMultilinePrompt ...")    
        linux = Linux(name = loginSuccessfullHost, username='pyco', password='pyco', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.checkOnOutputComplete = False
        
        output = linux.send('id')
        
        self.assertRegexpMatches(output, "uid=[0-9]+\\(pyco\\)")

    @unittest.skipIf(skip==True,"skipped test")    
    def testDynamicPrompt(self):
        '''
        Ever changing prompt case
        '''
        log.info("testChangingPrompt ...")    
        linux = Linux(name = loginSuccessfullHost, username='pyco', password='pyco', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.checkOnOutputComplete = False
        
        linux('myprompt_counter=1; export PROMPT_COMMAND=\'myprompt_counter=$((myprompt_counter + 1))\'')
        linux('PS1=\'$myprompt_counter \'')
        
        self.assertEqual(linux.discoverPrompt, False, "discoverPrompt must be set to FALSE when unable to discover prompt")
        


    @unittest.skipIf(skip==True,"skipped test")    
    def testSendCommandAfterClose(self):
        log.info("testSendCommandAfterClose ...")    
        linux = Linux(name = loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        output = linux.send('uname -a')
        self.assertRegexpMatches(output, "Linux .*")
        try:
            linux.send('exit')
        except:
            output = linux.send('id')
            self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")


    @unittest.skipIf(skip==True,"skipped test")    
    def testCommandWithAnswers(self):
        log.info("testCommandWithAnswers ...")    
        linux = Linux(name = loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        def error(target):
            raise AuthenticationFailed
        
        def sendSuPassword(target):
            target.sendLine('pyco')
        
        suPattern = {'event': 'su_event', 'pattern': 'Password: ', 'states': 'USER_PROMPT'}
        
        authFailed = {'event': 'auth_failed', 'pattern': 'Authentication failure', 'states': 'USER_PROMPT', 'action': error}
        
        suRule = {
                 'begin_state' : 'USER_PROMPT',
                 'event': 'su_event',
                 'action' :  sendSuPassword,
                 'end_state' : 'USER2_PROMPT'
               }
        
        linux.addPattern(**suPattern)
        linux.addPattern(**authFailed)
        linux.addTransition(suRule)
        
        linux.discoverPrompt = True
        
        linux.send('su pyco')
        output = linux.send('uname -a')
        self.assertRegexpMatches(output, "Linux .*")

      
#@unittest.skip("temp skip")
class TestHops(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    @unittest.skipIf(skip==True,"skipped test")      
    def testLoopDetection(self):
        '''
        try to connect to fakeLocalhost from a device that responds:
        
        The authenticity of host 'fakeLocalhost (::1)' can't be established.
        RSA key fingerprint is 1d:de:e0:49:2d:33:5e:f0:53:21:9f:09:95:81:8c:78.
        Are you sure you want to continue connecting (yes/no)?
        
        This triggers a expect detection loop and a TimedOut exception
        
        '''
        hop = Linux(**hop1)
        
        host = Linux(hops = [hop], **fakeLocalhost)
        
        self.failUnlessRaises(ConnectionTimedOut, host.login)

    @unittest.skipIf(skip==True,"skipped test")    
    def testHopConnection(self):
        '''
        try to connect to fakeLocalhost from a device that responds:
        
        The authenticity of host 'fakeLocalhost (::1)' can't be established.
        RSA key fingerprint is 1d:de:e0:49:2d:33:5e:f0:53:21:9f:09:95:81:8c:78.
        Are you sure you want to continue connecting (yes/no)?
        
        This triggers a expect detection loop and a TimedOut exception
        
        '''
        hop = Linux(**hop1)
        
        host = Linux(hops = [hop], **hop2)
        
        host.login()

    @unittest.skipIf(skip==True,"skipped test")    
    def testWhereAmI(self):
        '''
        
        '''
        log.info("testWhereAmI ...")    
        
        host = path([Linux(**hop1), Linux(**hop2), Linux(**hop3)])
        
        try:
            host.login()
        except:
            d = host.whereAmI()
            log.debug("target host: [%s], connected host: [%s]" % (host.name, d.name))

            out = host('uname -a')
            print "[%s]" % out


    @unittest.skipIf(skip==True,"skipped test")    
    def testExpectLoop(self):
        '''
        
        '''
        log.info("testExpectLoop ...")    
       
        config = ConfigObj()
        
        config['Common'] = {
                                'sshCommand' : 'ssh ${device.username}@${device.name}'
                           }
        
        host = path([Linux(**hop1), Linux(**hop2), Linux(**hop3)])
        
        try:
            host.login()
        except:
            d = host.whereAmI()
            log.debug("target host: [%s], connected host: [%s]" % (host.name, d.name))

            out = d('uname -a')
            print "[%s]" % out

    @unittest.skipIf(skip==True,"skipped test")    
    def testMinimalCfg(self):
        '''
        test a minimal configuration
        '''
        import netcube.config
        
        log.info("testExpectLoop ...")    
       
        config = ConfigObj()
        
        config['Common'] = {
                                # 'sshCommand' : 'ssh ${device.username}@${device.name}'
                                'events' : {
                                                'password_event': {
                                                                    'pattern': '[pP]assword: ',
                                                                    'state' : 'GROUND',
                                                                    'action': 'sendPassword',
                                                                    'end_state': 'USER_PROMPT'
                                                                  },
                                                'permission_denied': {
                                                                      'pattern' : 'Permission denied',
                                                                      'action'  : 'permissionDenied'
                                                                      }
                                                                  
                                           }
                           }
        oldCfg = netcube.config.configObj
        
        # reload the configuration
        netcube.config.reload(config)
        
        host = Linux(**fakeLocalhost)
        
        try:
            host.login()
            log.debug('------------------------------')
            host.send('uname -a')
        finally:
            netcube.config.loadFile()
            
    @unittest.skipIf(skip==True,"skipped test")    
    def testPermissionDenied(self):
        '''
        test wrong username/password
        '''
        log.info("testPermissionDenied ...")    
        
        
        host = Linux(**fakeLocalhost)
        
        self.assertRaises(PermissionDenied, host.login)
   


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''
Created on Jan 31, 2011

@author: adona
'''
import unittest

from netcube.master import *
from netcube.exceptions import *

unableToConnectHost = "163.162.155.91"
loginSuccessfullHost = "127.0.0.1"
targetCommand = "uname -a"

localhost = {
             'name':'localhost', 
             'username':'netcube',
             'password':'netcube'
             }


skip = True

class TestConstraints(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def testNoName(self):
        h = Linux(**localhost)
        h.login()
        #self.failUnlessRaises(NetworkException, h.login)
    
@unittest.skip("temp skip")
class Test(unittest.TestCase):

    def setUp(self):
        self.unableToConnectHost = "163.162.155.91"
        self.loginSuccessfullHost = "127.0.0.1"
        self.targetCommand = "uname -a"

        Linux.loginErrorMessages = "mio errore"
     
        #Linux.addEvent("username_event", ('.*username:', '.*login:'), ('GROUND',))
        #Linux.addEvent("password_event", '.*password:', ('GROUND',))
        #Linux.addEvent("password_event", '.*[Pp]assword:', ('LOGIN',))
        #Linux.addEvent("enable_event", 'enable', ('USER_PROMPT',))
        
    def tearDown(self):
        pass

    @unittest.skipIf(skip==True,"skipped test")
    def testUnableToConnectToRemoteHost(self):
        kabul = Linux(username='ipnet', name = self.unableToConnectHost, password='Hie.g00I')
        
        #print "TIMEOUT = %s" % kabul.timeout
        
        self.failUnlessRaises(ConnectionClosed, kabul.login)
        
        #kabul.login("telnet", 'username', 'password')
        #kabul.login("telnet", 'username', 'password')
        
        #response = kabul.command(self.targetCommand)
        #response = "Linux cencenighe 2.6.32-27-generic #49-Ubuntu SMP"

        #self.assertRegexpMatches(response, "Linux .*")


    def atestLoginSuccessfull(self):
        linux = Linux(name = self.loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        linux.login()
        
        #device.sendCommand('ls')
        #print "TIMEOUT = %s" % linx.timeout
        print "TIMEOUT = %s" % linux.timeout
        
    @unittest.skipIf(skip==True,"skipped test")    
    def testSendCommand(self):
        '''
        Send a simple command without prompt discovery
        '''    
        linux = Linux(name = self.loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        linux.discoverPrompt = False
        linux.login()
        output = linux.send('id')
        
        print "<%s>" % output
        self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")
        self.assertTrue('USER_PROMPT' not in linux.prompt, 'prompt discovered unexpectedly')
        
    @unittest.skipIf(skip==True,"skipped test")    
    def testSendCommandWithPromptDiscovery(self):
        '''
        Send a simple command with prompt discovery
        '''    
        linux = Linux(name = self.loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.login()
        output = linux.send('id')
        
        print "<%s>" % output
        self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")
        self.assertTrue('USER_PROMPT' in linux.prompt, 'prompt not discovered')

    @unittest.skipIf(skip==True,"skipped test")    
    def testOutputCompleteOnPromptMatch(self):
        '''
        Send simple commands and use prompt match only
        '''    
        linux = Linux(name = self.loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.checkOnOutputComplete = True
        
        linux.login()
        output = linux.send('id')
        
        print "<%s>" % output
        self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")
        self.assertTrue('USER_PROMPT' in linux.prompt, 'prompt not discovered')

    @unittest.skipIf(skip==True,"skipped test")    
    def testOutputCompleteOnPromptMatchTc2(self):
        '''
        Send simple commands and use prompt match only with promptDiscovery disabled
        expected result:  
        '''    
        linux = Linux(name = self.loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        linux.discoverPrompt = False
        linux.checkOnOutputComplete = False
        
        linux.login()
        output = linux.send('id')
        
        print "<%s>" % output
        self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")

    @unittest.skipIf(skip==True,"skipped test")    
    def testChangePrompt(self):
        '''
        Change the prompt and rediscover it 
        '''    
        linux = Linux(name = self.loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        linux.discoverPrompt = False
        linux.checkOnOutputComplete = False
        
        linux.login()
        output = linux.send('PS1=pippo')
        
        print "<%s>" % output
        self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")

    @unittest.skipIf(skip==True,"skipped test")    
    def testMultilinePrompt(self):
        '''
        Discover a multiline prompt
        '''    
        linux = Linux(name = self.loginSuccessfullHost, username='pyco', password='pyco', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.checkOnOutputComplete = False
        
        output = linux.send('id')
        
        print "<%s>" % output
        #self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")

    @unittest.skipIf(skip==True,"skipped test")    
    def testChangingPrompt(self):
        '''
        Ever changing prompt case
        '''    
        linux = Linux(name = self.loginSuccessfullHost, username='pyco', password='pyco', protocol='ssh')
        
        linux.discoverPrompt = True
        linux.checkOnOutputComplete = False
        
        linux('myprompt_counter=1; export PROMPT_COMMAND=\'myprompt_counter=$((myprompt_counter + 1))\'')
        linux('PS1=\'$myprompt_counter \'')
        
        self.assertEqual(linux.discoverPrompt, False, "discoverPrompt must be set to FALSE when unable to discover prompt")
        
        #self.assertRegexpMatches(output, "uid=[0-9]+\\(netbox\\)")




    @unittest.skipIf(skip==True,"skipped test")    
    def testSendCommandAfterClose(self):    
        linux = Linux(name = self.loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        output = linux.send('uname -a')
        print "FIRST OUTPUT: <%s>" % output
        try:
            linux.send('exit')
        except:
                
            output = linux.send('ls')
            print "SECOND OUTPUT: <%s>" % output

    @unittest.skipIf(skip==False,"skipped test")    
    def testCommandWithAnswers(self):    
        linux = Linux(name = self.loginSuccessfullHost, username='netbox', password='netbox', protocol='ssh')
        
        def error(target):
            raise AuthenticationFailed
        
        def sendSuPassword(target):
            target.sendLine('pyco')
        
        suPattern = {'event': 'su_event', 'pattern': 'Password: ', 'state': 'USER_PROMPT'}
        
        authFailed = {'event': 'auth_failed', 'pattern': 'Authentication failure', 'state': 'USER_PROMPT', 'action': error}
        
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
        print "OUTPUT: <%s>" % output
      

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
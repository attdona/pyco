# coding=utf-8-sig
'''
Created on Mar 15, 2011

@author: Attilio Donà
'''
import sys
import re
from mako.template import Template #@UnresolvedImport
from mako.runtime import Context #@UnresolvedImport
from StringIO import StringIO #@UnresolvedImport

import netcube.drivers

from netcube import log
from netcube.exceptions import *

# create logger
log = log.getLogger("driver")

def getAccount(device):
    
    # it is always the last function in the plugin group
    return False


def device(url):
    (driverName, host, user, password, protocol, port) = parseUrl(url)
    
    log.debug("[%s] info: driver [%s], cred [%s / %s], protocol [%s:%s]" % (host, driverName, user, password, protocol, port))
    
    if driverName == '':
        driverName = 'common'
    
    driver = netcube.drivers.Driver.getDriver(driverName)
    
    obj = Device(driver, host, user, password, protocol, port)
    return obj
    
def parseUrl(url):
    '''
    the device url is compliant with the RFC syntax defined by [http://tools.ietf.org/html/rfc3986]
    the telnet and ssh scheme are extended with a path item defining the host specific driver to be used for connecting 
    
    valid device url:
        * telnet://u:p@localhost:21/linux
        * ssh://user@localhost:21/linux
        * ssh://localhost
    '''
    from urlparse import urlparse #@UnresolvedImport

    items = urlparse(url)
    if items.scheme == '':
        items = urlparse('ssh://' + url)
    
    print items
    return (items.path[1:], items.hostname, items.username, items.password, items.scheme, items.port)

def getExactStringForMatch(str):
    '''
    Used for example to escape special characters in prompt strings 
    '''
    log.debug("escaping prompt [%s]" % str)
    specials = ['(\\[)', '(\\$)', '(\\.)', '(\\^)', '(\\*)', '(\\+)', '(\\?)', '(\\{)', '(\\})', '(\\])', '(\\|)', '(\\()', '(\\))']
    orSep = '|'
    pattern = orSep.join(specials)
    
    p = re.compile('(\\\\)')
    match = p.sub(r'\\\1', str)
    for spec in specials:
        p = re.compile(spec)
        match = p.sub(r'\\\1', match)
    
    return match

def discoverPromptCallback(device):
    '''
    The discover prompt algorithm
    '''

    if device.currentEvent.name == 'prompt-match':
        output = device.esession.pipe.after
    elif device.currentEvent.name == 'timeout':
        output = device.esession.pipe.before
    else:
        raise Exception("discover prompt failed; unexpected event [%s]" % device.currentEvent.name)
    
    # if regular exp succeed then set the prompt
    log.debug("[%s] prompt discovery ..." % (device.name))

    # stop the default handling of the timeout event
    device.currentEvent.stopPropagation()
    
    sts = device.state()

    if sts in device.prompt:
        if device.prompt[sts].value == output.replace('\r\n', '', 1):
            device.discoveryCounter = 0
            log.debug("[%s] [%s] prompt discovered: [%s]" % (device.name, sts, device.prompt[sts].value))
            device.prompt[sts].setExactValue(device.prompt[sts].value)
            
            #device.addPattern('prompt-match', getExactStringForMatch(device.prompt[sts].value), device.fsm.current_state)
            device.addExpectPattern('prompt-match', getExactStringForMatch(device.prompt[sts].value), device.fsm.current_state)
            for ev in ['timeout', 'prompt-match']:
                device.removeEventHandler(ev, discoverPromptCallback)
            
            # declare the discovery with the event
            device.currentEvent = Event('prompt-match')
            
            return
            
        else:
            if device.discoveryCounter == 2:
                log.debug("[%s] [%s] unable to found the prompt, unsetting discovery. last output: [%s]" % (device.name, sts, output))
                device.discoverPrompt = False
                device.removeEventHandler('timeout', discoverPromptCallback)
                return
            else:
                log.debug("[%s] [%s] prompt not match, retrying discovery with pointer [%s]" % (device.name, sts, output))
                device.prompt[sts].value = output.replace('\r\n', '', 1)
                device.discoveryCounter += 1
    else:
        rows = output.split('\r\n')
        tentativePrompt = rows[-1]
        device.discoveryCounter = 0
        log.debug("[%s] tentativePrompt: [%s]" % (device.name, tentativePrompt))
        device.prompt[sts] = Prompt(tentativePrompt, tentative=True)
        
    device.clearBuffer()
    device.sendLine('')
    device.expect(lambda d: d.currentEvent.name == 'timeout' or d.currentEvent.name == 'prompt-match')

class Event:
    def __init__(self, name, propagateToFsm=True):
        self.name = name
        self.propagate = propagateToFsm
        
        
    def stopPropagation(self):
        self.propagate = False
        
    def isActive(self):
        return self.propagate
    
    def isTimeout(self):
        return self.name == 'timeout'
            
class Prompt:
    
    def __init__(self, promptValue, tentative=False):
        self.value = promptValue
        self.tentative = tentative
    
    def isTentative(self):
        return self.tentative

    def isFinal(self):
        return not self.tentative
     
    def setExactValue(self, value):
        self.value = value
        self.tentative = False


class Device:
    '''
    Base class for device configuration 
    '''    
    
    defaultConfig = None
    
    telnet_port = 23

    def __init__(self, driver, name, username = None, password = None, protocol='ssh', port=22, hops = []):
        log.debug("[%s] ctor" % name)
        self.name = name
        self.username = username
        self.password = password
        self.protocol = protocol
        self.hops = hops
        self.loggedin = False
        
        self.eventCb = {}
        self.prompt = {}

        # the finite state machine
        self.state = 'GROUND'

        self.driver = driver
        self.patternMap = {'*':{}}

    def getDriver(self):
        return self.driver.name

    def enablePromptDiscovery(self):
        """
        Match the output device against the promptRegexp pattern and set the device prompt
        """
        self.onEvent('timeout', discoverPromptCallback)
        
        #self.expect(lambda d: d.currentEvent.name == 'timeout' or d.currentEvent.name == 'prompt-match')

    def interactionLog(self):
        return self.esession.logfile.getvalue()

    def isConnected(self):
        '''
        If the device is connected return True 
        '''
        return self.loggedin
        
    def whereAmI(self):
        '''
        return the hop device actually connected. 
        '''
        from netcube.expectsession import SOURCE_HOST
        
        if self.isConnected():
            return self
        
        for d in reversed(self.hops):
            log.debug("checking if [%s] is connected" % d.name)
            if d.isConnected():
                return d
    
        return SOURCE_HOST
    
    def close(self):
        
        if self.currentEvent.name != 'eof':
            self.esession.close()
        del self.esession.pipe    
        self.fsm.current_state = 'GROUND'
        
    def addTransition(self, t):
        self.fsm.add_transition(t['event'], t['begin_state'], t['action'], t['end_state'])    
        
#    def addPattern(self, **pattern):
#        self.addPattern(pattern['event'], pattern['pattern'], pattern['state'])
        
    def addPattern(self, event, pattern=None, states=['*'], endState=None, action=None):
        '''
        Add a pattern to be matched in the FSM state. If the pattern is matched then the corresponding event is generated.
        
        If pattern is None only a transition is configured
        '''
        
        if isinstance(states, basestring):
            states = [states]
        
        for state in states:
            
            if not pattern or pattern == '':
                if state == '*':
                    log.warning("[%s]: skipped [%s] event with empty pattern and * state" % (self.name, event))
                else:
                    log.debug("[%s] adding transition [%s-%s (action:%s)-%s]" % (self.name, state, event, action, endState))
                    self.fsm.add_transition(event, state, action, endState)
                
                continue
            
            try:
                self.patternMap[state][pattern] = event
            except:
                self.patternMap[state] = {pattern:event}

            #  add the transition
            if state == '*':
                log.debug("[%s]: adding pattern driven transition in any state [%s-%s (action:%s)-%s]" % (self.name, state, event, action, endState))
                self.fsm.add_input_any(event, action, endState)
            else:
                log.debug("[%s]: adding pattern driven transition [%s-%s (action:%s)-%s]" % (self.name, state, event, action, endState))
                self.fsm.add_transition(event, state, action, endState)
            

    def addExpectPattern(self, event, pattern, state):
        log.debug("[%s]: adding expect pattern [%s], event [%s], state [%s]" % (self.name, pattern, event, state))
        if not pattern or pattern == '':
            log.warning("[%s]: skipped [%s] event with empty pattern and * state" % (self.name, event))
            return
        
        try:
            self.patternMap[state][pattern] = event
        except:
            self.patternMap[state] = {pattern:event}
            

    def unregisterPattern(self, pattern, state = '*'):
        del self.patternMap[state][pattern]
      
    def patternFromEvent(self, pattern):
        return 'Password: '

    def discoverPromptWithRegexp(self, regexp, state='*'):
        '''
        Use regexp as a hint for prompt discovery 
        Add the guard \'\\\\r\\\\n\' to the begin of prompt regexp
        '''
        
        self.addPattern("prompt-match", '\r\n' + regexp, state)
        self.onEvent('prompt-match', discoverPromptCallback)

        
    def getPrompt(self):
        '''
        Get the current device prompt
        '''
        return self.prompt[self.fsm.current_state].value

    def promptDiscovered(self):
        if self.state in self.prompt:
            return self.prompt[self.state].isFinal()
        return False
        
    def patterns(self, state):
        '''
        Return the pattern list to match the device output 
        '''
        try:
            return self.patternMap[state].keys() + self.patternMap['*'].keys()
        except:
            return self.patternMap['*'].keys()

        
    def getEvent(self,pattern):
        '''
        The event associated with the pattern argument
        '''
        try:
            return self.patternMap[self.state][pattern]
        except:
            # TODO: raise an exception if event not found
            return self.patternMap['*'][pattern]

    def connectCommand(self, clientDevice):
        
        from pkg_resources import iter_entry_points
        
        for ep in iter_entry_points(group='pyco.plugin', name=None):
            log.debug("found [%s] plugin into module [%s]" % (ep.name, ep.module_name))
            authFunction = ep.load()
            if authFunction(self):
                break

        
        try:
            telnetCommand = clientDevice.telnetCommand
        except:
            telnetCommand = 'telnet ${device.username}'   

        try:
            sshCommand = clientDevice.sshCommand
        except:
            sshCommand = 'ssh ${device.username}@${device.name}'   

        commandTemplates = {
                        'telnet' : Template(telnetCommand),
                        'ssh'    : Template(sshCommand)
                        }
        
        template = commandTemplates.get(self.protocol)
        clicommand = StringIO()
        context = Context(clicommand, device=self)

        template.render_context(context)
        
        return clicommand.getvalue()
 
 
#    def registerPattern(self, eventName, pattern, state = '*'):
#        self.patternMap[state][pattern] = eventName


        
    def hasEventHandlers(self, event):
        return event.name in self.eventCb

    def getEventHandlers(self, event):
        return self.eventCb[event.name]
    
    def onEvent(self, eventName, callback):
        log.debug("[%s] adding [%s] for [%s] event" % (self.name, callback, eventName))
        try:
            if not callback in self.eventCb[eventName]:
                self.eventCb[eventName].append(callback)
        except:
            self.eventCb[eventName] = [callback]

    def removeEventHandler(self, eventName, callback):
        log.debug("[%s] removing [%s] event handler [%s]" % (self.name, eventName, callback))
        try:
            self.eventCb[eventName].remove(callback)
        except:
            log.debug("[%s] not found [%s] event handler [%s]" % (self.name, eventName, callback))
        
    def login(self):
        """
        open a network connection using protocol. Currently supported protocols are telnet and ssh.
        
        The final state is one of:
            * LOGIN_ERROR
            * USER_PROMPT
        
        If login has succeeded the device is in USER_PROMPT state and it is ready for consuming commands
        """
        from netcube.expectsession import ExpectSession
        log.debug("%s login ..." % self.name)

        self.esession = ExpectSession(self.hops,self)
        log.debug("[%s] session: [%s]" % (self.name, self.esession))
        
        try:
            self.esession.login()
        except NetworkException as e:
            # something go wrong, try to find the last connected hop in the path
            log.info("[%s]: in login phase got [%s] error" % (e.device.name ,e.__class__))
            
            log.debug("full interaction: [%s]" % e.interactionLog)
            raise e
            
        self.clearBuffer()
        
        if self.state() == 'USER_PROMPT':
            log.debug("%s logged in !!! ..." % self.name)
            
        
    def expect(self, checkPoint):
        self.esession.patternMatch(self, checkPoint, [], self.maxWait, exactMatch=True)
        
    def sendLine(self, stringValue):
        """
        send ``stringValue`` to the device cli 
        """
        log.debug("[%s] sending [%s]" % (self, stringValue))
        self.esession.sendLine(stringValue)
        
    def __call__(self, command):
        return self.send(command)
            
    def send(self, command, answers = {}):
        '''
        Send the command string to the device and return the command output
        '''
        
        if self.fsm.current_state == 'GROUND':
            self.login()
        
        self.clearBuffer()
        self.sendLine(command)

        def runUntilPromptMatchOrTimeout(device):
            return device.currentEvent.name == 'timeout' or device.currentEvent.name == 'prompt-match'

        out = self.esession.processResponseWithTimeout(self, runUntilPromptMatchOrTimeout)
        
        if self.currentEvent.name == 'timeout' and self.discoverPrompt == True:
            # rediscover the prompt
            log.debug("[%s] discovering again the prompt ..." % self.name)
            self.enablePromptDiscovery()
            discoverPromptCallback(self)
            
            
        if self.checkIfOutputComplete == True:
        
            prevOut = None
            while out != prevOut:
                self.clearBuffer()
                log.debug("[%s] == [%s]" % (prevOut,out))
                prevOut = out
                currOut = self.esession.processResponseWithTimeout(self, runUntilPromptMatchOrTimeout)
                if prevOut == None:
                    out = currOut
                else:
                    out = prevOut + currOut
                log.debug("Checking if [%s] response [%s] is complete" % (command,out))
        
        out = out.replace(command.replace('\n','\r\n'), '', 1).strip('\r\n')  
        log.debug("[%s:%s]: captured response [%s]" % (self.name, command, out))
        
        return out 
           
    def clearBuffer(self):
        # wait for a 1 second timeout period and then consider cleared the buffer
        try: 
            self.esession.pipe.expect('.*', timeout=1)    
        except:
            log.debug("[%s] clearBuffer timeout: cleared expect buffer" % self.name) 

# end Device class

    
if __name__ == '__main__':
    host = device('telnet://myuser:mypasswd@localhost:21/linux')
    host.login()
    
    #host = device('localhost')
    
    #device('telnet://u:p:1@localhost:21/linux')
    #device('ssh://user@localhost:22/linux')
    #device('ssh://user@localhost/linux')
    #device('ssh://user@localhost')

        
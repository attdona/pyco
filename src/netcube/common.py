'''
Created on 29/gen/2011

@author: SO000112
'''

import re #@UnresolvedImport
from netcube.xfsm import ExtFSM
from mako.template import Template #@UnresolvedImport
from mako.runtime import Context #@UnresolvedImport

from StringIO import StringIO #@UnresolvedImport

from netcube import log

# create logger
log = log.getLogger("device")


def buildPatternsList(device, model=None):
    
    if model is None:
        model = device.__class__
        
    if len(model.__bases__):
        buildPatternsList(device, model.__bases__[0])
    
    for (eventKey, eventData) in device.config[model.__name__]['events'].items():
        device.addPattern(event=eventKey, **eventData)
        


def buildPatternsListOLD(device, model=None):
    
    if model is None:
        model = device.__class__
        
    if len(model.__bases__):
        eventMap = buildPatternsList(device, model.__bases__[0])
    else:
        eventMap = {'*': {}}
         
    #log.debug("[%s] events: %s" % (model.__name__, config[model.__name__]['events']))
    
    for (eventKey, eventData) in device.config[model.__name__]['events'].items():
       
        if 'states' in eventData:
            if isinstance(eventData['states'], basestring):
                states = [eventData['states']]
            else:
                states = eventData['states']
        else:
            states = ['*']
        
        if not eventData['pattern']:
            log.warning("skipped [%s] [%s] event with empty pattern" % (model.__name__, eventKey))
        else:
            for state in states:
                if state in eventMap:
                    eventMap[state][eventData['pattern']] = eventKey
                else:
                    eventMap[state] = {eventData['pattern']:eventKey}
        
        if 'action' in eventData:
            log.debug("[%s]: registering handler [%s]" % (eventKey, eventData['action']))
            action = getCallable(eventData['action'])
            device.onEvent(eventKey, action)
        
    return eventMap

       
def discoverPrompt(device):
    """
    Match the output device against the promptRegexp pattern and set the device prompt
    """
    #device.registerPattern('timeout', device.promptRegexp)
    
    device.onEvent('timeout', discoverPromptCallback)
    device.expect(lambda d: d.currentEvent.name == 'timeout' or d.currentEvent.name == 'prompt-match')

# OBSOLETED
def disableTimeoutEvent(device, output):
    '''
    Prevent the propagation of timeout event to fsm engine
    '''
    device.currentEvent.stopPropagation()

# TODO: add all the regexp special chars
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

     
def discoverPromptCallback(device, output):
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
            
            device.addPattern('prompt-match', getExactStringForMatch(device.prompt[sts].value), device.fsm.current_state)
            
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

    
class Common:
    '''
    Base class for device configuration 
    '''    
    
    defaultConfig = None
    
    telnet_port = 23

    def __init__(self, name, username = None, password = None, protocol='telnet', config=None, hops = []):
        from netcube.expectsession import ExpectSession
        log.debug("[%s] ctor" % name)
        self.name = name
        self.username = username
        self.password = password
        self.protocol = protocol
        
        self.esession = ExpectSession(hops,self)
        
        self.eventCb = {}
        self.prompt = {}

        if config:
            self.config = netcube.config.load(config)
        else:
            if not Common.defaultConfig:
                Common.defaultConfig = netcube.config.loadFile()
        
            self.config = Common.defaultConfig

        # the finite state machine
        self.fsm = CommonFSM('GROUND', self.config, [])
        self.patternMap = {'*':{}}
        buildPatternsList(self)

        
    def close(self):
        
        if self.currentEvent.name != 'eof':
            self.esession.close()
        del self.esession.pipe    
        self.fsm.current_state = 'GROUND'
        
    def addTransition(self, t):
        self.fsm.add_transition(t['event'], t['begin_state'], t['action'], t['end_state'])    
        
#    def addPattern(self, **pattern):
#        self.addPattern(pattern['event'], pattern['pattern'], pattern['state'])
        
    def addPattern(self, event, pattern, states=['*'], action=None):
        '''
        Add a pattern to be matched in the FSM state. If the pattern is matched then event is generated
        '''
        if not pattern or pattern == '':
            log.warning("[%s]: skipped [%s] event with empty pattern" % (self.name, event))
            return
        
        if isinstance(states, basestring):
            states = [states]
        
        for state in states:
            try:
                self.patternMap[state][pattern] = event
            except:
                self.patternMap[state] = {pattern:event}
            
        if action:
            log.debug("[%s]: registering handler [%s]" % (event, action))
            self.onEvent(event, action)
    

    def unregisterPattern(self, pattern, state = '*'):
        del self.patternMap[state][pattern]
      
    def patternFromEvent(self, pattern):
        return 'Password: '

    def discoverPromptWithRegexp(self, regexp, state='*'):
        '''
        Use regexp as a hint for prompt discovery 
        Add the guard '\r\n' to the begin of prompt regexp
        '''
        
        self.addPattern("prompt-match", '\r\n' + regexp, state)
        self.onEvent('prompt-match', discoverPromptCallback)

        
    def setState(self, value):
        self.fsm.current_state = value   
        
    def state(self):
        return self.fsm.current_state
    
    def getPrompt(self):
        '''
        Get the current device prompt
        '''
        return self.prompt[self.fsm.current_state].value

    def promptDiscovered(self):
        if self.fsm.current_state in self.prompt:
            return self.prompt[self.fsm.current_state].isFinal()
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
            return self.patternMap[self.fsm.current_state][pattern]
        except:
            # TODO: raise an exception if event not found
            return self.patternMap['*'][pattern]

    def connectCommand(self, clientDevice):
        commandTemplates = {
                        'telnet' : Template(clientDevice.telnetCommand),
                        'ssh'    : Template(clientDevice.sshCommand)
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
        log.debug("%s login ..." % self.name)
        
        self.esession.login()
        self.clearBuffer()
        log.debug("%s logged in !!! ..." % self.name)
 
        
    def expect(self, checkPoint):
        self.esession.patternMatch(self, checkPoint, [], self.responseMaxWaitTime, exactMatch=True)
        
    def sendLine(self, stringValue):
        """
        send ``stringValue`` to the device cli 
        """
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
            discoverPrompt(self)
            
        if self.timeoutCheckOnOutputComplete == True:
        
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

        

def getCallable(methodName):
    '''
    From the methodName string get the callable object from netcube.actions or netcube.common name space
    '''
    if methodName == '' or methodName is None:
        return None

    import netcube.actions
    if isinstance(methodName,str):
        try:
            return getattr(netcube.actions, methodName)
        except:
            if methodName in globals():
                return globals()[methodName]
            else:
                raise netcube.exceptions.EventHandlerUndefined(methodName)
    else:
        def composite(d):
            for m in methodName:
                getCallable(m)(d)
        return composite
 
import netcube.exceptions

def cliDefaultErrorHandler(device):
    '''
    The default error handler invoked when an unexpected pattern or a timeout or eof event occurs
    '''
    
    log.info("[%s] unexpected communication error in state [%s] got [%s] event" % (device.name, device.fsm.current_state, device.currentEvent.name))

    event_map = {
                  'timeout': netcube.exceptions.ConnectionTimedOut,
                  'eof'    : netcube.exceptions.ConnectionClosed
                }

    if device.currentEvent.name in event_map:
        exception = event_map[device.currentEvent.name](device)
        device.close()
        raise exception
    
class CommonFSM(ExtFSM):
    '''
    classdocs
    '''


    def __init__(self, initial_state, config, memory=None):
        '''
        Add the configured transitions
        '''
        
        ExtFSM.__init__(self, 'GROUND', memory)
        
        self.set_default_transition(cliDefaultErrorHandler, 'ERROR')
        
        # simply ignore 'prompt-match' on any state
        self.add_input_any('prompt-match')
        
#        for transitionKey, t in Common.transitions.items():
        for transitionKey, t in config['Common']['transitions'].items():
            log.debug("adding transition %s: %s -> %s -> %s (action: %s)" % ( transitionKey, t['begin_state'], t['event'], t['end_state'], t['action'] ))
                
            self.add_transition(t['event'], t['begin_state'], getCallable(t['action']), t['end_state'])

            


if __name__ == "__main__":
    print "executing test ..."
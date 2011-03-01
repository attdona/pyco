'''
Created on 29/gen/2011

@author: SO000112
'''

#import pexpect
from netcube.xfsm import ExtFSM
from mako.template import Template #@UnresolvedImport
from mako.runtime import Context #@UnresolvedImport

from StringIO import StringIO

from netcube import log

# create logger
log = log.getLogger("device")


def buildPatternsList(model):
    from netcube.config import config
    
    if len(model.__bases__):
        eventMap = buildPatternsList(model.__bases__[0])
    else:
        eventMap = {'*': {}}
         
    #log.debug("[%s] events: %s" % (model.__name__, config[model.__name__]['events']))
    
    for (eventKey, eventData) in config[model.__name__]['events'].items():
       
        if isinstance(eventData['states'], basestring):
            states = [eventData['states']]
        else:
            states = eventData['states']
        
        if not eventData['pattern']:
            log.warning("skipped [%s] [%s] event with empty pattern" % (model.__name__, eventKey))
        else:
            for state in states:
                if state in eventMap:
                    eventMap[state][eventData['pattern']] = eventKey
                else:
                    eventMap[state] = {eventData['pattern']:eventKey}
        
    return eventMap

       
def discoverPrompt(device):
    """
    Match the output device against the promptRegexp pattern and set the device prompt
    """
    #device.registerPattern('timeout', device.promptRegexp)
    
    device.onEvent('timeout', discoverPromptCallback)
    device.expect(lambda d: d.currentEvent.name == 'timeout')

# OBSOLETED
def disableTimeoutEvent(device, output):
    '''
    Prevent the propagation of timeout event to fsm engine
    '''
    device.currentEvent.stopPropagation()
     
def discoverPromptCallback(device, output):
    # if regular exp succeed then set the prompt
    log.debug("[%s] prompt discovery ..." % (device.name))

    # stop the default handling of the timeout event
    device.currentEvent.stopPropagation()
    rows = output.split('\r\n')
    
    sts = device.state()

    if sts in device.prompt:
        if device.prompt[sts].value == rows[-1]:
            log.debug("[%s] [%s] prompt discovered: [%s]" % (device.name, sts, device.prompt[sts].value))
            device.prompt[sts].setExactValue(device.prompt[sts].value)
            #device.setState('USER_PROMPT')
            device._addPattern('prompt-match', device.prompt[sts].value, device.fsm.current_state)
            
            device.removeEventHandler('timeout', discoverPromptCallback)
            #device.onEvent('timeout', disableTimeoutEvent)
    else:
        tentativePrompt = rows[-1]
        
        log.debug("[%s] tentativePrompt: [%s]" % (device.name, tentativePrompt))
        device.prompt[sts] = Prompt(tentativePrompt, tentative=True)
        
        device.clearBuffer()
        
        device.sendLine('')
        device.expect(lambda d: d.currentEvent.name == 'timeout')
    #device.setFsmState('USER_PROMPT')
    
    
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
    
    telnet_port = 23

    def __init__(self, name, username = None, password = None, protocol='telnet', hops = []):
        from netcube.expectsession import ExpectSession
        log.debug("[%s] ctor" % name)
        self.name = name
        self.username = username
        self.password = password
        self.protocol = protocol
        
        self.esession = ExpectSession(hops,self)
        
        # the finite state machine
        self.fsm = CommonFSM('GROUND', [])
        
        self.patternMap = buildPatternsList(self.__class__)
        self.eventCb = {}
        self.prompt = {}
        
    def close(self):
        
        if self.currentEvent.name != 'eof':
            self.esession.close()
        del self.esession.pipe    
        self.fsm.current_state = 'GROUND'
        
    def addTransition(self, t):
        self.fsm.add_transition(t['event'], t['begin_state'], t['action'], t['end_state'])    
        
    def addPattern(self, pattern):
        '''
        Add a pattern to be matched in the FSM state. If the pattern is matched then event is generated
        '''
        self._addPattern(pattern['event'], pattern['pattern'], pattern['state'])
        
    def _addPattern(self, event, pattern, state='*'):
        try:
            self.patternMap[state][pattern] = event
        except:
            self.patternMap[state] = {pattern:event}    

    def unregisterPattern(self, pattern, state = '*'):
        del self.patternMap[state][pattern]
      
    def patternFromEvent(self, pattern):
        return 'Password: '
        
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
        try:
            if not callback in self.eventCb[eventName]:
                self.eventCb[eventName].append(callback)
        except:
            self.eventCb[eventName] = [callback]

    def removeEventHandler(self, eventName, callback):
        self.eventCb[eventName].remove(callback)
        
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

        def runUntilTimeout(device):
            return device.currentEvent.name == 'timeout' or device.currentEvent.name == 'prompt-match'

        out = self.esession.processResponseWithTimeout(self, runUntilTimeout)
        prevOut = None
        while out != prevOut:
            self.clearBuffer()
            log.debug("[%s] == [%s]" % (prevOut,out))
            prevOut = out
            currOut = self.esession.processResponseWithTimeout(self, runUntilTimeout)
            if prevOut == None:
                out = currOut
            else:
                out = prevOut + currOut
            log.debug("Checking if [%s] response [%s] is complete" % (command,out))
           
        log.debug("[%s]: response does not change between responseCompleteTimePeriod" % (command))
        
        return out.replace(command.replace('\n','\r\n'), '', 1).strip('\r\n')
           
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
    try:
        if isinstance(methodName,str):
            return getattr(netcube.actions, methodName)
        else:
            def composite(d):
                for m in methodName:
                    getCallable(m)(d)
            return composite
    except:
        #log.debug("try to get function [%s] on Common namespace: %s" % (methodName, globals().keys()))
        return globals()[methodName]

import netcube.exceptions

def cliDefaultErrorHandler(device):
    '''
    The default error handler invoked when an unexpected pattern or a timeout or eof event occurs
    '''
    log.error("[%s] unexpected communication error in state [%s] got [%s] event" % (device.name, device.fsm.current_state, device.currentEvent.name))

    event_map = {
                  'timeout': netcube.exceptions.ConnectionTimedOut,
                  'eof'    : netcube.exceptions.ConnectionClosed
                }

    device.close()
        
    raise event_map[device.currentEvent.name]
    
class CommonFSM(ExtFSM):
    '''
    classdocs
    '''


    def __init__(self, initial_state, memory=None):
        '''
        Add the configured transitions
        '''
        
        ExtFSM.__init__(self, 'GROUND', memory)
        
        self.set_default_transition(cliDefaultErrorHandler, 'ERROR')
        
        for transitionKey, t in Common.transitions.items():
            log.debug("adding transition %s: %s -> %s -> %s (action: %s)" % ( transitionKey, t['begin_state'], t['event'], t['end_state'], t['action'] ))
                
            self.add_transition(t['event'], t['begin_state'], getCallable(t['action']), t['end_state'])

            


if __name__ == "__main__":
    print "executing test ..."
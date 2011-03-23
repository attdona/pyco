'''
Created on Feb 21, 2011

@author: adona
'''
import StringIO #@UnresolvedImport
import pexpect #@UnresolvedImport

from netcube.device import Event, device
from netcube import log
from netcube.exceptions import ConnectionTimedOut


# create logger
log = log.getLogger("exp-session")

       
def loginSuccessfull(device):
    '''
    The checkpoint loginSuccessfull has 3 exit point:
     * return True if the state is 'USER_PROMPT'
     * raise the ConnectionTimedOut exception if the current event is timeout
     * return False otherwise
    '''
    log.debug("[%s] loginSuccessfull: current_state [%s]" % (device.name, device.state))
    if device.state == 'USER_PROMPT':
        device.loggedin = True
        return True
    if device.currentEvent.name == 'timeout':
        raise ConnectionTimedOut(device)
    return False


class ExpectSession:
    
    def __init__(self, hops, target):
        self.hops = hops + [target]

        # in memory log
        self.logfile = StringIO.StringIO()

        # key is a hop object, value is the hop fsm current state
        #self.currentState = {}
        
        
    def login(self):
        self.connect(len(self.hops)-1)
        
    def close(self):
        try:
            self.logfile.close()
        except ValueError:
            log.warning("trying to close an already closed expect logfile")
        self.pipe.close(force=True)
          
        
    def connect(self, position):
        """
        Connect to the device in the hops position index
        """
        prevPos = position - 1
        if prevPos < 0:
            prevDevice = SOURCE_HOST
        else:
            prevDevice = self.hops[prevPos]

        target = self.hops[position]
       
        log.debug("[%s] prev hop device: [%s]" % (target.name, prevDevice.name))
        if not prevDevice.isConnected():
            log.debug("previous hop %s is not connected, activating ..." % prevDevice.name)
            
            # backward propagate the session
            prevDevice.esession = target.esession
            self.connect(prevPos)
        
            
        cmd = target.connectCommand(prevDevice)
        
        # in memory log
        #self.logfile = StringIO.StringIO()
        
        #logfile = file(netcube.config.expectLogfile, "w")

        log.debug("connecting using %s" % cmd)
        
        self.currentHop = target
        
        if hasattr(self, 'pipe'):
            self.sendLine(cmd)
        else:
            # TODO: close the spawned session
            # send the connect string to pexpect
            log.debug("[%s]: spawning a new [%s] session ..." % (target, self)) 
            self.pipe = pexpect.spawn(cmd, logfile=self.logfile)
        
        self.processResponse(target, loginSuccessfull)

    def sendLine(self, command):
        """
        Send a command string to the device actually connected
        """
        log.debug("sending line [%s] using session [%s]" % (command, self))
        self.pipe.sendline(command)
 
        
    def patternMatch(self, target, checkPoint, patternsExt, maxWaitTime, exactMatch=False):
        
        target.currentEvent = Event('do-nothing-event')
        log.debug("entering patternMatch, checkpoint is [%s]" % (checkPoint))
        
#        prevOutput = None
#        prevEvent =  target.currentEvent
        
        while not (checkPoint (target) or target.currentEvent.isTimeout()):
            
            patterns = target.patterns(target.state) + patternsExt
            # expect and match 
            try:
                log.debug("[%s] matching [%s]" % (target.state, patterns))
                #log.debug("PRE exp before: [%s] - after: [%s]" % (self.pipe.before, self.pipe.after))
                if target.exactPatternMatch:
                    index = self.pipe.expect_exact(patterns, maxWaitTime)
                else:
                    index = self.pipe.expect(patterns, maxWaitTime)
               
                try:    
                    target.currentEvent = Event(target.getEvent(patterns[index]))
                except:
                    
                    if patterns[index] == pexpect.TIMEOUT:
                        log.debug("[%s]: expect timeout triggered" % target.name)
                        target.currentEvent = Event('timeout', propagateToFsm = False)
                        
#                        if prevEvent.name == 'timeout' and prevOutput == self.pipe.before:
#                            #from netcube.exceptions import ConnectionTimedOut
#                            log.info("[%s] detected expect loop, output: [%s]" % (target.name, prevOutput))
#                            raise ConnectionTimedOut(target)
#                        else:
#                            target.currentEvent = common.Event('timeout', propagateToFsm = False)
#                            prevOutput = self.pipe.before
#                            prevEvent = target.currentEvent
                    else:
                        log.error("[%s]: event not registered for pattern: [%s]" % (target.name, patterns[index]))
                        raise
                        
                log.debug("matched pattern [%s] --> [%s]" % (patterns[index], target.currentEvent.name))
                log.debug("before: [%s] - after: [%s]" % (self.pipe.before, self.pipe.after))
            except pexpect.EOF:
                log.debug("[%s] connection unexpectedly closed (%s)" % (target.name, self.pipe.before))
                target.currentEvent = Event('eof')
            except pexpect.TIMEOUT:
                log.debug("[%s] connection timed out, unmatched output: [%s]" % (target.name, self.pipe.before))
                target.currentEvent = Event('timeout')

            #log.debug("detected event [%s]" % target.currentEvent)
            if target.hasEventHandlers(target.currentEvent):
                log.debug("[%s] got [%s] event; invoking handlers: [%s]" % (target.name, target.currentEvent.name, target.getEventHandlers(target.currentEvent)))
                for eh in target.getEventHandlers(target.currentEvent):
                    eh(target)
           
            stateChanged = target.process(target.currentEvent)

            # check if state_transition_any has a entry
#            if stateChanged and target.fsm.current_state in target.fsm.state_transitions_any:
#                log.debug("[%s]: any state action is defined for state [%s]" % (target.name, target.fsm.current_state))
#                target.fsm.process(target, target.currentEvent)

#            if stateChanged and target.discoverPrompt and target.fsm.current_state.endswith('PROMPT'):
#                log.debug("[%s] starting [%s] prompt discovery" % (target.name, target.fsm.current_state))
#                common.discoverPrompt(target)

        return self.pipe.before
        
#    def processResponseWithPromptSync(self, target, checkPoint):

#        patterns = [target.prompt.value]
#        log.debug("[%s]; matching %s", target.fsm.current_state, patterns)
#        self.patternMatch(target, checkPoint, patterns, target.responseCompleteTimePeriod, exactMatch=True)
        
#        log.debug("before: [%s] - after: [%s]" % (self.pipe.before, self.pipe.after))

    def processResponseWithTimeout(self, target, checkPoint):
        patterns = [pexpect.TIMEOUT]
        return self.patternMatch(target, checkPoint, patterns, target.maxWait, exactMatch=True)
        
    def processResponse(self, target, checkPoint):
        '''
        '''
        self.patternMatch(target, checkPoint, [pexpect.TIMEOUT], target.driver.maxWait, exactMatch=False)
        
        
 


# The source point of all paths        
SOURCE_HOST = device('__source_host__')

# the source is connected for definition 
SOURCE_HOST.isConnected = lambda : True
        
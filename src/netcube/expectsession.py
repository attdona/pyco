'''
Created on Feb 21, 2011

@author: adona
'''
import pexpect
import netcube.common as common
from netcube import log

# create logger
log = log.getLogger("exp-session")

       
def loginSuccessfull(device):
    log.debug("[%s] prompt isFinal: [%s]" % (device.fsm.current_state, device.promptDiscovered()))
    
    # TODO: if prompt discovery enabled check if device.promptDiscovered() == True 
    
    if device.fsm.current_state == 'USER_PROMPT':
        return True
    return False


class ExpectSession:
    
    def __init__(self, hops, target):
        self.hops = hops + [target]
        
        # key is a hop object, value is the hop fsm current state
        #self.currentState = {}
        
        
    def login(self):
        self.connect(len(self.hops)-1)
        
    def close(self):
        self.pipe.close(force=True)
          
        
    def connect(self, position):
        """
        Connect to the device in the hops position index
        """
        import netcube.config
        prevPos = position - 1
        if prevPos < 0:
            prevDevice = SOURCE_HOST
        else:
            prevDevice = self.hops[prevPos]
        
        if not prevDevice.isConnected():
            log.debug("previous hop %s is not connected, activating ..." % prevDevice.name)
            self.connect(prevPos)
        
        target = self.hops[position]
            
        cmd = target.connectCommand(prevDevice)
        logfile = file(netcube.config.expectLogfile, "w")
        log.debug("connecting using %s" % cmd)
        
        self.currentHop = target
        #self.currentState[target] = 'GROUND'
        
        if hasattr(self, 'pipe'):
            self.sendLine(cmd)
        else:
            # send the connect string to pexpect
            log.debug("[%s]: spawning a new session ..." % target.name) 
            self.pipe = pexpect.spawn(cmd, logfile=logfile)
        
        self.processResponse(target, loginSuccessfull)

    def sendLine(self, command):
        """
        Send a command string to the device actually connected
        """
        self.pipe.sendline(command)
    
    # TODO: evaluate dynamically the patterns because the fsm state change   
    def patternMatch(self, target, checkPoint, patternsExt, maxWaitTime, exactMatch=False):
        
        target.currentEvent = common.Event('do-nothing-event')
        
        while not checkPoint (target):
            patterns = target.patterns(target.fsm.current_state) + patternsExt
            # expect and match 
            try:
                log.debug("[%s] matching [%s]" % (target.fsm.current_state, patterns))
                #log.debug("PRE exp before: [%s] - after: [%s]" % (self.pipe.before, self.pipe.after))
                if target.exactPatternMatch:
                    index = self.pipe.expect_exact(patterns, int(maxWaitTime))
                else:
                    index = self.pipe.expect(patterns, int(maxWaitTime))
               
                try:    
                    target.currentEvent = common.Event(target.getEvent(patterns[index]))
                except:
                    
                    if patterns[index] == pexpect.TIMEOUT:
                        log.debug("[%s]: expect timeout triggered" % target.name)
                        target.currentEvent = common.Event('timeout', propagateToFsm = False)
                    else:
                        log.error("[%s]: event not registered for pattern: [%s]" % (target.name, patterns[index]))
                        raise
                        
                log.debug("matched pattern [%s] --> [%s]" % (patterns[index], target.currentEvent.name))
                log.debug("before: [%s] - after: [%s]" % (self.pipe.before, self.pipe.after))
            except pexpect.EOF:
                log.debug("[%s] connection unexpectedly closed (%s)" % (target.name, self.pipe.before))
                target.currentEvent = common.Event('eof')
            except pexpect.TIMEOUT:
                log.debug("[%s] connection timed out, unmatched output: [%s]" % (target.name, self.pipe.before))
                target.currentEvent = common.Event('timeout')

            #log.debug("detected event [%s]" % target.currentEvent)
            if target.hasEventHandlers(target.currentEvent):
                
                for eh in target.getEventHandlers(target.currentEvent):
                    eh(target, self.pipe.before)
           
            stateChanged = target.fsm.process(target, target.currentEvent)

            if stateChanged and target.discoverPrompt and target.fsm.current_state.endswith('PROMPT'):
                log.debug("[%s] starting [%s] prompt discovery" % (target.name, target.fsm.current_state))
                common.discoverPrompt(target)

        return self.pipe.before
        
    def processResponseWithPromptSync(self, target, checkPoint):

        patterns = [target.prompt.value]
        log.debug("[%s]; matching %s", target.fsm.current_state, patterns)
        self.patternMatch(target, checkPoint, patterns, target.responseCompleteTimePeriod, exactMatch=True)
        
        log.debug("before: [%s] - after: [%s]" % (self.pipe.before, self.pipe.after))

    def processResponseWithTimeout(self, target, checkPoint):
        patterns = [pexpect.TIMEOUT]
        return self.patternMatch(target, checkPoint, patterns, target.responseCompleteTimePeriod, exactMatch=True)
        
    def processResponse(self, target, checkPoint):
        '''
        '''
        #patterns = target.patterns(target.fsm.current_state)
        
        self.patternMatch(target, checkPoint, [pexpect.TIMEOUT], target.responseMaxWaitTime, exactMatch=False)
        
        
 


# The source point of all paths        
SOURCE_HOST = common.Common('__source_host__')

# the source is connected for definition 
SOURCE_HOST.isConnected = lambda : True
        
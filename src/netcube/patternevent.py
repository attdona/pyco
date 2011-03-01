'''
Created on 29/gen/2011

@author: SO000112
'''
#import logging
from netcube import logging

# create logger
log = logging.getLogger("FSM")

# "application" code
log.debug("debug message")
log.info("info message")
log.warn("warn message")
log.error("error message")
log.critical("critical message")

def defineStates(*args):
    for elem in args:
        # print("defining state %s" % globals())
        # eval ("%s = State()" % elem, globals())
        print("built %s" % elem)

def defineEvents(*args):
    pass

def defineTransitions(*args):
    pass

def pattern(pattern):
    print("pattern [%s]" % pattern)
    return State

class State:
    
    def __init__(self):
        pass

    def pattern(self, pattern):
        return self
    
    def states(self, args):
        print("states %s" % args)
        return self
    
    def event(self, event):
        print("registered %s" % event)
        return self
    
# Ugly syntax, waiting for some guru reviewer
GROUND, LOGIN, USERCLI = State(), State(), State()

defineEvents('errorEvent', 'prompt')

# Start State, event, End State, action
defineTransitions(
                  (GROUND,  'startCli',   LOGIN),
                  (LOGIN,   'username',   LOGIN, 'sendUsername'),
                  (LOGIN,   'errorEvent', GROUND),
                  (LOGIN,   'prompt'    , USERCLI),
                  (USERCLI, 'prompt'    , USERCLI),
                  (USERCLI, 'exit'      , GROUND)
)

#pattern(".* invalid login").becameEvent('error-event').ifStates(LOGIN,USERCLI)

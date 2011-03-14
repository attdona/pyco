'''
Created on Feb 22, 2011

@author: adona
'''
from netcube import log
from netcube.exceptions import *

log = log.getLogger("actions")

def send(target, command):
    log.debug("sending string [%s] ..." % command)
    target.sendLine(command)
    

def sendUsername(target):
    log.debug("sending username  [%s] ..." % target.username)
    target.sendLine(target.username)

def sendPassword(target):
    log.debug("[%s] sending password [%s] ..." % (target.name, target.password))
    target.sendLine(target.password)

    # check if the expect session detect a cli shell 
    cliIsConnected(target)

def cliIsConnected(target):
    log.debug("[%s] [%s] checking if CLI is connected ..." % (target.name, target.currentEvent.name))

    if target.currentEvent.name == 'prompt-match':
        return True

    if target.discoverPrompt:
        log.debug("[%s] starting [%s] prompt discovery" % (target.name, target.fsm.current_state))
        target.enablePromptDiscovery()
        
        def isTimeoutOrPromptMatch(d):
            return d.currentEvent.name == 'timeout' or d.currentEvent.name == 'prompt-match'
        
        target.expect(isTimeoutOrPromptMatch)
        
    elif target.currentEvent.name != 'timeout':
        
        # if discoverPrompt is false then the timeout event is not an error but the trigger
        # that all the output is received 
        
        target.addPattern('timeout', states=target.fsm.current_state)
        
        def isTimeout(d):
            return d.currentEvent.name == 'timeout'
        
        target.expect(isTimeout)

    

def connectionRefused(target):
    log.debug("[%s] connectionRefused: [%s]" % (target.name, target.esession.pipe.before))
    raise ConnectionRefused(target)

def permissionDenied(target):
    log.debug("[%s]: raising permissionDenied exception" % target.name)
    raise PermissionDenied(target)



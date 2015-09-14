'''
Created on Feb 22, 2011

@author: adona
'''
from pyco import log
from pyco.device import Prompt, ConnectionRefused, PermissionDenied, MissingDeviceParameter, cliIsConnected


log = log.getLogger("actions")

def send(target, command):
    log.debug("sending string [%s] ..." % command)
    target.send_line(command)
    

def sendUsername(target):
    if target.username is None:
        raise MissingDeviceParameter(target, '%s username undefined' % target.name)

    log.debug("sending username  [%s] ..." % target.username)
    target.send_line(target.username)

def sendPassword(target):
    
    if target.password is None:
        raise MissingDeviceParameter(target, '%s password undefined' % target.name)
    
    log.debug("[%s] sending password [%s] ..." % (target.name, target.password))
    target.send_line(target.password)

    # check if the expect session detect a cli shell 
    #cliIsConnected(target)

def wrongCredentials(target):
    log.info("wrong username/password")
    raise PermissionDenied(target)
    
    
def setCliPrompt(target):
    '''
    setCliPrompt may be used when the device cli supports the PS1 command for setting the prompt.
    For example the Unix family satisfies such requirement.  
    '''
    uprompt = '_%s_pyco_> ' % target.name
    log.debug('[%s]: setting prompt to [%s]' % (target.name, uprompt))
    
    target.clear_buffer()
    
    target.send_line("PS1='%s'" % uprompt)
    
    # add the prompt without discovering it
    log.debug('[%s] matching prompt with pattern [%s]' % (target.state, uprompt))
    target.prompt[target.state] = Prompt(uprompt, tentative=False)
    target.add_expect_pattern('prompt-match', uprompt, target.state)


#def initCiscoCli(target):
#    log.debug('[%s] [%s]: initializing cisco ios cli shell' % (target.name, target.state))    


def connectionRefused(target):
    log.debug("[%s] connectionRefused: [%s]" % (target.name, target.interaction_log()))
    raise ConnectionRefused(target)

def permissionDenied(target):
    log.debug("[%s]: raising permissionDenied exception" % target.name)
    raise PermissionDenied(target)



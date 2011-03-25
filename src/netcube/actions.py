'''
Created on Feb 22, 2011

@author: adona
'''
from netcube import log
from netcube.device import ConnectionRefused, PermissionDenied, MissingDeviceParameter


log = log.getLogger("actions")

def send(target, command):
    log.debug("sending string [%s] ..." % command)
    target.sendLine(command)
    

def sendUsername(target):
    if target.username is None:
        raise MissingDeviceParameter(target, '%s username undefined' % target.name)

    log.debug("sending username  [%s] ..." % target.username)
    target.sendLine(target.username)

def sendPassword(target):
    
    if target.password is None:
        raise MissingDeviceParameter(target, '%s password undefined' % target.name)
    
    log.debug("[%s] sending password [%s] ..." % (target.name, target.password))
    target.sendLine(target.password)

    # check if the expect session detect a cli shell 
    #cliIsConnected(target)


def initCiscoCli(target):
    log.debug('[%s] [%s]: initializing cisco ios cli shell' % (target.name, target.state))    

def connectionRefused(target):
    log.debug("[%s] connectionRefused: [%s]" % (target.name, target.esession.pipe.before))
    raise ConnectionRefused(target)

def permissionDenied(target):
    log.debug("[%s]: raising permissionDenied exception" % target.name)
    raise PermissionDenied(target)



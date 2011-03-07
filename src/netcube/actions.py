'''
Created on Feb 22, 2011

@author: adona
'''
from netcube import log
from netcube.exceptions import *

log = log.getLogger("actions")

def sendUsername(target):
    log.debug("sending username  [%s] ..." % target.username)
    target.sendLine(target.username)

def sendPassword(target):
    log.debug("sending password [%s] ..." % target.password)
    target.sendLine(target.password)

def connectionRefused(target, response):
    log.debug("[%s] connectionRefused: [%s]" % (target.name, response))
    raise ConnectionRefused(target)

def permissionDenied(target, response):
    log.debug("[%s] permissionDenied: [%s]" % (target.name, response))
    raise PermissionDenied(target)
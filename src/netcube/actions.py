'''
Created on Feb 22, 2011

@author: adona
'''
from netcube import log

log = log.getLogger("actions")

def sendUsername(target):
    log.debug("sending username  [%s] ..." % target.username)
    target.sendLine(target.username)

def sendPassword(target):
    log.debug("sending password [%s] ..." % target.password)
    target.sendLine(target.password)

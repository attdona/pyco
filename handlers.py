'''
Created on Jun 28, 2011

@author: adona
'''
from pyco import log
from pyco.device import ConnectionRefused, PermissionDenied, MissingDeviceParameter, cliIsConnected


log = log.getLogger("handlers")


def sendUsername(target):
    if target.username is None:
        raise MissingDeviceParameter(target, '%s username undefined' % target.name)

    log.debug("sending username  [%s] ..." % target.username)
    target.sendLine(target.username)

def cliIsEnabled(target):
    cliIsConnected(target)
    target.send('')
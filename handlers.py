'''
Created on Jun 28, 2011

@author: adona
'''
from pyco import log
from pyco.device import ConnectionRefused, PermissionDenied, MissingDeviceParameter, cliIsConnected


log = log.getLogger("handlers")


def initCiscoTerminal(target):
    target.send('terminal length 0')

def sendWhitespace(target):
    target.send(' ')
    
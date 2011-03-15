# coding=utf-8-sig
'''
Created on Mar 15, 2011

@author: Attilio Donà
'''
import netcube.common

from netcube import log

# create logger
log = log.getLogger("drivers")

def deviceClassBuilder(modelName):
    
    # create at runtime the device class
    try:
        clz = getattr(netcube.devices, modelName)
    except AttributeError:
        clz = type(modelName, (netcube.common.Common,object), dict())
        
    setattr(netcube.devices, modelName, clz)
    return clz

def setAttribute(modelName, attr, value):
    log.debug("[%s.%s] = [%s]" % (modelName, attr, value))
    setattr(getattr(netcube.devices, modelName), attr, value)
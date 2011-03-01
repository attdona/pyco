'''
Created on Feb 15, 2011

@author: adona
'''
import logging
import logging.config
import netcube

logging.config.fileConfig(netcube.pyco_home + "/cfg/log.conf")

def getLogger(logId):
    return logging.getLogger(logId)
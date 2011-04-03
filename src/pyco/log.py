'''
Created on Feb 15, 2011

@author: adona
'''
import logging #@UnresolvedImport
import logging.config #@UnresolvedImport
import netcube
import os

if hasattr(netcube, 'pyco_home'):
    logfile = netcube.pyco_home + "/cfg/log.conf"
else:
    logfile = os.path.dirname(__file__) + "/cfg/log.conf"
    
logging.config.fileConfig(logfile)

def getLogger(logId):
    return logging.getLogger(logId)
'''
Created on Feb 15, 2011

@author: adona
'''
import logging #@UnresolvedImport
import logging.config #@UnresolvedImport
import pyco
import os
from pkg_resources import resource_filename #@UnresolvedImport

if hasattr(pyco, 'pyco_home'):
    logfile = pyco.pyco_home + "/cfg/log.cfg"
else:
    logfile = resource_filename('pyco', 'cfg/log.conf')
try:    
    logging.config.fileConfig(logfile)
except:
    print('failed to setup the log system: wrong logfile path? (check if [%s] exists)' % logfile)
    
def getLogger(logId):
    return logging.getLogger(logId)
'''
Created on Feb 14, 2011

The config module parse the cosmos.cfg properties file and initialize the class attributes

@author: adona
'''
import netcube
import netcube.telnet

from configobj import ConfigObj #@UnresolvedImport

expectLogfile = netcube.pyco_home + "/logs/expect.log"

# create logger
log = netcube.log.getLogger("config")

config = ConfigObj(netcube.pyco_home + "/cfg/pyco.cfg")

log.debug("[Common] data: %s" % config.get("Common"))

for section in config.keys():
    for (key,value) in config[section].items():
        log.debug("settings %s.%s to %s" % (section, key, value))
       
        module = netcube.__dict__[section.lower()] #@UndefinedVariable
        
        clz = getattr(module, section)
        setattr(clz, key, value)
        

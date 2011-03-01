'''
Created on Feb 14, 2011

The config module parse the cosmos.cfg properties file and initialize the class attributes

@author: adona
'''
import netcube
import netcube.telnet
from netcube.exceptions import ConfigFileError
from validate import Validator #@UnresolvedImport

from configobj import ConfigObj, flatten_errors #@UnresolvedImport

expectLogfile = netcube.pyco_home + "/logs/expect.log"

# create logger
log = netcube.log.getLogger("config")

import os
module_path = os.path.dirname(netcube.__file__)

config = ConfigObj(netcube.pyco_home + "/cfg/pyco.cfg", configspec=module_path + '/pyco_spec.cfg')

val = Validator()
results = config.validate(val)

if results != True:
    for (section_list, key, _) in flatten_errors(config, results):
        if key is not None:
            raise ConfigFileError('The "%s" key in the section "%s" failed validation' % (key, ', '.join(section_list)))
        else:
            raise ConfigFileError('The following section was missing:%s ' % ', '.join(section_list))


log.debug("[Common] data: %s" % config.get("Common"))

for section in config.keys():
    for (key,value) in config[section].items():
        log.debug("settings %s.%s to %s" % (section, key, value))
       
        module = netcube.__dict__[section.lower()] #@UndefinedVariable
        
        clz = getattr(module, section)
        setattr(clz, key, value)
        

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
import os
module_path = os.path.dirname(netcube.__file__)

expectLogfile = '/tmp/expect.log'
cfgFile = module_path + "/cfg/pyco.cfg"
if hasattr(netcube, 'pyco_home'):
    expectLogfile = netcube.pyco_home + "/logs/expect.log"
    cfgFile = netcube.pyco_home + "/cfg/pyco.cfg"
    
# create logger
log = netcube.log.getLogger("config")

# the shared configObj
configObj = None

def loadFile(cfgfile=cfgFile):
    '''
    Load the pyco configuration file
    '''
    config = ConfigObj(cfgfile, configspec=module_path + '/cfg/pyco_spec.cfg')
    return reload(config)


def load(config):
    '''
    Load the pyco configObj
    '''
    global configObj
    
    config.configspec = ConfigObj(module_path + '/cfg/pyco_spec.cfg')
    
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
            if key not in ['events', 'transitions']:
                setattr(clz, key, value)

    configObj = config
            
    return config       

def reload(config):
    reset()
    load(config)

def reset():
    '''
    Delete the current configuration parameters
    '''
    
    if configObj is None:
        return;
    
    for section in configObj.keys():
        for (key,value) in configObj[section].items():
            log.debug("settings %s.%s to %s" % (section, key, value))
           
            module = netcube.__dict__[section.lower()] #@UndefinedVariable
            
            clz = getattr(module, section)
            if key not in ['events', 'transitions']:
                delattr(clz, key)
            
           

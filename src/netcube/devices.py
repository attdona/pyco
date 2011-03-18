# coding=utf-8-sig
'''
Created on Mar 15, 2011

@author: Attilio Donà
'''
import sys
import netcube.common
from netcube import log


# create logger
log = log.getLogger("drivers")

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
    
    import os.path
    if os.path.isfile(cfgfile):
        config = ConfigObj(cfgfile, configspec=module_path + '/cfg/pyco_spec.cfg')
        return reload(config)
    else:
        raise Exception('pyco configuration file not found: ' + cfgfile)

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
            if value is None:
                log.debug("skipping [%s.%s] undefined value" % (section, key))
                continue
            
            log.debug("settings %s.%s to %s" % (section, key, value))
           
            try:
                module = netcube.__dict__[section.lower()] #@UndefinedVariable
                clz = getattr(module, section)
                if key not in ['events', 'transitions']:
                    log.debug("[%s.%s] = [%s]" % (clz,key,value))
                    setattr(clz, key, value)
            except KeyError:
                deviceClassBuilder(section)
                setAttribute(section, key, value)
                

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
            log.debug("deleting %s.%s to %s" % (section, key, value))
           
            try:
                module = netcube.__dict__[section.lower()] #@UndefinedVariable
                clz = getattr(module, section)
            except KeyError:
                clz = getattr(netcube.devices, section)
            
            if key not in ['events', 'transitions']:
                try:
                    delattr(clz, key)
                except AttributeError:
                    log.debug("[%s] attribute [%s] not found (not directly defined?)" % (clz,key))
                    

def deviceClassBuilder(modelName):
    print "----- " + __name__ + str(sys.modules[__name__]) 
    cmod = sys.modules[__name__]
    # create at runtime the device class
    try:
        clz = getattr(cmod, modelName)
    except AttributeError:
        clz = type(modelName, (netcube.common.Common,object), dict())
        
    setattr(cmod, modelName, clz)
    return clz

def setAttribute(modelName, attr, value):
    log.debug("[%s.%s] = [%s]" % (modelName, attr, value))
    setattr(getattr(sys.modules[__name__], modelName), attr, value)
    
    
# finally and only finally load the configuration
loadFile()     
    
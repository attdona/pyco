'''
Created on Mar 21, 2011

@author: adona
'''
import netcube
from netcube import log

# create logger
log = log.getLogger("driver")

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
    
    configObj = config
    
    log.debug("[Common] data: %s" % config.get("common"))
    
    for section in config.keys():
        for (key,value) in config[section].items():
            if value is None:
                log.debug("skipping [%s.%s] undefined value" % (section, key))
                continue
            
            try:
                driver = Driver.get(section)
                if key in ['events', 'transitions']:
                    continue
            except DriverNotFound:
                log.debug("creating driver [%s]" % section)
                driver = driverBuilder(section)
                
            log.debug("settings %s.%s to %s" % (section, key, value))
            log.debug("[%s.%s] = [%s]" % (driver,key,value))
            setattr(driver, key, value)
                
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
                driver = Driver.get(section)
                if key not in ['events', 'transitions']:
                    try:
                        delattr(driver, key)
                    except AttributeError:
                        log.debug("[%s] attribute [%s] not found (not directly defined?)" % (section,key))
            except DriverNotFound:
                log.error('configuration reset error: [%s] driver not found' % section)
            
                    

def driverBuilder(modelName):
    driver = Driver(modelName)
    Driver.addDriver(driver)
    return driver




class DriverException(Exception):

    """This is the Driver Exception class."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return `self.value`

class DriverNotFound(DriverException):
    pass




class Driver:

    """Driver for the command line configuration"""

    registry = {}

    def __init__(self, name):

        """This creates the Driver. You set the initial state here. The "memory"
        attribute is any object that you want to pass along to the action
        functions. It is not used by the Driver. For parsing you would typically
        pass a list to be used as a stack. """
        self.name = name



    def __str__(self):
        return self.name

    def __repr__(self):
        return 'driver:' + self.name

    def __getattr__(self, attrname):
        if attrname == 'parent':
            raise AttributeError, attrname
        else:
            #log.debug("[%s] delegating search for [%s] to [%s]" % (self, attrname, self.parent))
            try:
                pDriver = Driver.get(self.parent)
                return getattr(pDriver, attrname)
            except AttributeError:
                raise AttributeError, attrname
            

    @staticmethod
    def get(driverName):
        try:
            return Driver.registry[driverName]
        except KeyError:
            raise DriverNotFound('%s driver not defined' % driverName)
        
    @staticmethod
    def addDriver(driver):
        Driver.registry[driver.name] = driver
        
            

 
    
# finally and only finally load the configuration
loadFile()     


    
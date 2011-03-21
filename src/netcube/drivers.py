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
    
    log.debug("[Common] data: %s" % config.get("Common"))
    
    for section in config.keys():
        for (key,value) in config[section].items():
            if value is None:
                log.debug("skipping [%s.%s] undefined value" % (section, key))
                continue
            
            log.debug("settings %s.%s to %s" % (section, key, value))
           
            try:
                driver = Driver.getDriver(section)
                if key in ['events', 'transitions']:
                    continue
            except KeyError:
                driver = driverBuilder(section)
 
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
                driver = Driver.getDriver(section)
                if key not in ['events', 'transitions']:
                    try:
                        delattr(driver, key)
                    except AttributeError:
                        log.debug("[%s] attribute [%s] not found (not directly defined?)" % (section,key))
            except KeyError:
                log.error('configuration reset error: [%s] driver not found' % section)
            
                    

def driverBuilder(modelName):
    driver = Driver(modelName)
    Driver.addDriver(driver)
    return driver



class ExceptionFSM(Exception):

    """This is the ExtFSM Exception class."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return `self.value`



def buildPatternsList(targetDriver, driver=None):
    '''
    Setup the expect patterns and the action events from the configobj 
    '''
    if hasattr(targetDriver, 'parent'):
        buildPatternsList(targetDriver, Driver.getDriver(targetDriver.parent))
    
    if driver == None:
        driver = targetDriver
    
    if driver.name not in configObj:
        log.debug("skipping undefined [%s] section" % (driver.name))
        return
    
    for (eventKey, eventData) in configObj[driver.name]['events'].items():

        action=None
        if 'action' in eventData:
            action = buildAction(eventData['action'])
           
        states = '*'  
        if 'state' in eventData:
            states =  eventData['state']
            
        endState = None
        if 'end_state' in eventData:
            endState = eventData['end_state']
     
        pattern = None
        if 'pattern' in eventData:
            pattern = eventData['pattern']
            
        targetDriver.addPattern(event=eventKey, pattern=pattern, action=action, states=states, endState=endState)



def buildAction(actionString):
    al = actionString.split()
    
    if len(al) > 1:
        baseAction = getCallable(al[0])
        def action(target):
            log.debug("invoking action [%s] with %s" % (baseAction.__name__, al[1:]))
            baseAction(target,*al[1:])
            
    else:
        action = getCallable(actionString)
    
    return action



def getCallable(methodName):
    '''
    From the methodName string get the callable object from netcube.actions or netcube.common name space
    '''
    if methodName == '' or methodName is None:
        return None

    import netcube.actions
    if isinstance(methodName,str):
        try:
            return getattr(netcube.actions, methodName)
        except:
            if methodName in globals():
                return globals()[methodName]
            else:
                raise netcube.exceptions.EventHandlerUndefined(methodName)
    else:
        def composite(d):
            for m in methodName:
                getCallable(m)(d)
        return composite



class Driver:

    """Driver is modeled as a Finite State Machine (FSM).
    """

    registry = {}

    def __init__(self, name):

        """This creates the Driver. You set the initial state here. The "memory"
        attribute is any object that you want to pass along to the action
        functions. It is not used by the Driver. For parsing you would typically
        pass a list to be used as a stack. """
        self.name = name

        # Map (input_symbol, current_state) --> (action, next_state).
        self.state_transitions = {}
        # Map (current_state) --> (action, next_state).
        self.state_transitions_any = {}
        self.input_transitions_any = {}
        self.default_transition = None

        self.patternMap = {'*':{}}
        buildPatternsList(self)

    @staticmethod
    def getDriver(driverName):
        return Driver.registry[driverName]

    @staticmethod
    def addDriver(driver):
        Driver.registry[driver.name] = driver
        
            

    def add_transition (self, input_symbol, state, action=None, next_state=None):

        """This adds a transition that associates:

                (input_symbol, current_state) --> (action, next_state)

        The action may be set to None in which case the process() method will
        ignore the action and only set the next_state. The next_state may be
        set to None in which case the current state will be unchanged.

        You can also set transitions for a list of symbols by using
        add_transition_list(). """

        if next_state is None:
            next_state = state
        self.state_transitions[(input_symbol, state)] = (action, next_state)

    def add_transition_list (self, list_input_symbols, state, action=None, next_state=None):

        """This adds the same transition for a list of input symbols.
        You can pass a list or a string. Note that it is handy to use
        string.digits, string.whitespace, string.letters, etc. to add
        transitions that match character classes.

        The action may be set to None in which case the process() method will
        ignore the action and only set the next_state. The next_state may be
        set to None in which case the current state will be unchanged. """

        if next_state is None:
            next_state = state
        for input_symbol in list_input_symbols:
            self.add_transition (input_symbol, state, action, next_state)

    def add_transition_any (self, state, action=None, next_state=None):

        """This adds a transition that associates:

                (current_state) --> (action, next_state)

        That is, any input symbol will match the current state.
        The process() method checks the "any" state associations after it first
        checks for an exact match of (input_symbol, current_state).

        The action may be set to None in which case the process() method will
        ignore the action and only set the next_state. The next_state may be
        set to None in which case the current state will be unchanged. """

        if next_state is None:
            next_state = state
        self.state_transitions_any [state] = (action, next_state)

    def add_input_any (self, input_symbol, action=None, next_state=None):

        """This adds a transition that associates:

                (input_symbol) --> (action, next_state)

        That is, the input symbol will trigger a transition in any state.
        The process() method checks the input_symbol in "any state" associations after it
        checks for a match of transition_any

        The action may be set to None in which case the process() method will
        ignore the action and only set the next_state. The next_state may be
        set to None in which case the current state will be unchanged. """

        self.input_transitions_any [input_symbol] = (action, next_state)


    def set_default_transition (self, action, next_state):

        """This sets the default transition. This defines an action and
        next_state if the ExtFSM cannot find the input symbol and the current
        state in the transition list and if the ExtFSM cannot find the
        current_state in the transition_any list. This is useful as a final
        fall-through state for catching errors and undefined states.

        The default transition can be removed by setting the attribute
        default_transition to None. """

        self.default_transition = (action, next_state)

    def get_transition (self, input_symbol, state):

        """This returns (action, next state) given an input_symbol and state.
        This does not modify the ExtFSM state, so calling this method has no side
        effects. Normally you do not call this method directly. It is called by
        process().

        The sequence of steps to check for a defined transition goes from the
        most specific to the least specific.

        1. Check state_transitions[] that match exactly the tuple,
            (input_symbol, state)

        2. Check state_transitions_any[] that match (state)
            In other words, match a specific state and ANY input_symbol.
            
        3. Check if the input_symbol has a (action, next_state) association 
            in any state 

        4. Check if the default_transition is defined.
            This catches any input_symbol and any state.
            This is a handler for errors, undefined states, or defaults.

        5. No transition was defined. If we get here then raise an exception.
        """

        if self.state_transitions.has_key((input_symbol, state)):
            return self.state_transitions[(input_symbol, state)]
        elif self.state_transitions_any.has_key (state):
            return self.state_transitions_any[state]
        elif self.input_transitions_any.has_key(input_symbol):
            return self.input_transitions_any[input_symbol]
        elif self.default_transition is not None:
            return self.default_transition
        else:
            raise ExceptionFSM ('Transition is undefined: (%s, %s).' %
                (str(input_symbol), str(state)) )

    def process (self, device, input_symbol):

        """This is the main method that you call to process input. This may
        cause the driver to change state and call an action. The action callable
        is invoked with device object argument as a first parameter. This method calls
        get_transition() to find the action and next_state associated with the
        input_symbol and current_state. If the action is None then the action
        is not called and only the current state is changed. This method
        processes one complete input symbol. You can process a list of symbols
        (or a string) by calling process_list(). """

        if input_symbol.isActive():

            #self.input_symbol = input_symbol.name
            (action, next_state) = self.get_transition (input_symbol, device.state)
            log.debug("selected transition [%s,%s] -> [%s]" % (input_symbol, device.state, next_state))
            
            stateChanged = False
            
            if next_state != None:
                log.debug("transition activated for [%s,%s] -> [%s]" % (input_symbol, device.state, next_state))
                stateChanged = (device.state != next_state)
                device.state = next_state
                
            if action is not None:
                log.debug("[%s]: executing [%s] action [%s]" % (device.name, input_symbol, str(action)))
                action (device)
           
            return stateChanged

    def process_list (self, input_symbols):

        """This takes a list and sends each element to process(). The list may
        be a string or any iterable object. """

        for s in input_symbols:
            self.process (s)


    def addPattern(self, event, pattern=None, states=['*'], endState=None, action=None):
        '''
        Add a pattern to be matched in the FSM state. If the pattern is matched then the corresponding event is generated.
        
        If pattern is None only a transition is configured
        '''
        
        if isinstance(states, basestring):
            states = [states]
        
        for state in states:
            
            if not pattern or pattern == '':
                if state == '*':
                    log.warning("[%s]: skipped [%s] event with empty pattern and * state" % (self.name, event))
                else:
                    log.debug("[%s] adding transition [%s-%s (action:%s)-%s]" % (self.name, state, event, action, endState))
                    self.fsm.add_transition(event, state, action, endState)
                
                continue
            
            try:
                self.patternMap[state][pattern] = event
            except:
                self.patternMap[state] = {pattern:event}

            #  add the transition
            if state == '*':
                log.debug("[%s]: adding pattern driven transition in any state [%s-%s (action:%s)-%s]" % (self.name, state, event, action, endState))
                self.add_input_any(event, action, endState)
            else:
                log.debug("[%s]: adding pattern driven transition [%s-%s (action:%s)-%s]" % (self.name, state, event, action, endState))
                self.add_transition(event, state, action, endState)
 
    
# finally and only finally load the configuration
loadFile()     


    
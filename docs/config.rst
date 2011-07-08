.. _driver-configuration:

Driver Configuration
====================

If you need to define a new driver or change an existing one follow the following recipe:

#. set the environment variable PYCO_HOME pointing to the application root directory
#. place a pyco.cfg configuration file in $PYCO_HOME/cfg

The pyco configuration file is a .ini file containing the settings used in the device connection setup and command line communication.

Every section define a specific driver setup, where the section title is the name of the driver.

The special [common] section contains the setup of the default common driver.
This is the only mandatory section that has to be defined.

The following is a configuration example that define also the `linux` and a `ciscoios` driver::

 [common]

  sshCommand = ssh ${device.username}@${device.name}

  telnetCommand = telnet ${device.name} ${device.port}

  # wait maxWait seconds for a device response before raising timeout event
  maxWait = 5

  # perform pattern exact match. Use with caution because
  # all eventual patterns based on regular expressions match as exact strings
  exactPatternMatch = False


  # enable/disable prompt discovery
  discoverPrompt = True

 
   [[events]]
 	 [[[username_event]]]
 		beginState  = 'GROUND'
  		pattern     = "login:[ ]*"
		action      = sendUsername
	
	 [[[password_event]]]
		pattern     = "(?i)password:[ ]*"
		beginState  = GROUND
		action      = sendPassword
		endState    = PASSWORD_SENT

	 [[[password_sent]]]
		beginState = PASSWORD_SENT
		action = cliIsConnected
		endState = USER_PROMPT
		
	 [[[continue_connecting]]]
		pattern = 'continue connecting \(yes/no\)\?'
		beginState   = GROUND
		action  = :send:yes:

	 [[[permission_denied]]]
		pattern = 'Permission denied, please try again.'
		action  = permissionDenied

	 [[[connection_refused]]]
		pattern = '(?i)connection refused'
		action  = connectionRefused

The *common* driver is used when no driver is defined in the device url, for example:

 ssh://user@myremotemachine

The [linux] section contains the setup specific for the linux family of operating systems.
Note the `parent` keyword: the [common] setup is inherited by [linux] driver if not overwritten by the most specific driver.
For example the following inherits all the [common] configurations and overwrite the *discoverPrompt* flag:: 		

  [linux]

   parent = common

   # enable/disable prompt discovery
   discoverPrompt = False

The `events` section defines the :term:`FSM` logic that models the interaction with the device. 

The :ref:`fsm_model` section describes the meaning and syntax of a FSM machine described in terms of events, states and actions. 	

A special action is `cliIsDefined`: only such action implements the prompt discovery logic controlled by the
:ref:`discoverPrompt <config_discoverPrompt>`, :ref:`promptPattern <config_promptPattern>` and :ref:`cache <config_cache>` configuration parameter.  


Configuration parameters
------------------------

Below are reported all the pyco configuration parameters. In parenthesis the default values.

  .. _config_cache:
  
  *cache*
    a sqlite database cache holding the prompts discovered by pyco. the `cache` value `<prompt_cache>` is the sqlite filename:
    
    * `$PYCO_HOME/<prompt_cache>` if the environment variable `PYCO_HOME` is set
    * `/tmp/<prompt_cache>` otherwise
    
    The caching is enabled automatically if the cache parameter is defined: this requires that the `sqlalchemy` and `transaction` 
    python are installed in the python environment. 

  *checkIfOutputComplete* (False)
    if True enable another expect loop to check if more output arrived after 
    prompt match or the first expect loop timeout. This extra control slows down the the interaction.

  .. _config_discoverPrompt:
  
  *discoverPrompt* (True|False)
  	enable the discovery prompt algorithm. If *discoverPrompt* is ``False`` the output returned by :py:meth:`pyco.device.Device.send()` is mixed with banners, input command and prompt strings.

  *exactPatternMatch* (False)
  	if *True* performs exact pattern matching, so must be used defining the *event.pattern* field with an exact string and not with a regular expression.

  *maxWait* (5)
	wait *maxWait* seconds for a device response before raising timeout event.
	what happens when a *timeout* event is triggered depends on the FSM state:
	
	* it may be a operational wait time needed for waiting the device output in the discovery prompt phase
	* it may trigger a :py:exc:`pyco.device.ConnectionTimedOut` exception when a command response is not received.
	
  .. _config_promptPattern:
  
  *promptPattern*
    use this regular expression value as a hint for matching the cli prompt. If `promptPattern` is defined the discovery prompt
    algorithm is disabled also if the `discoverPrompt` is True.
    Keep in mind that this is a weaker match than the exactp prompt match implied by the prompt discovery algorithm, so be sure that the
    command response does not contains a string that match this regular expression.

  *sshCommand* (ssh ${device.username}@${device.name})
  	the ssh client template command used for connecting.  

  *telnetCommand* (telnet ${device.name} ${device.port})
  	the telnet client template command used for connecting.
  	
  *waitBeforeClearingBuffer* (1)
  	wait waitBeforeClearingBuffer seconds for some more output before clearing the output buffer in the following cases:

  	* after the login phase and before sending the shell commands
  	* after a promp discovery
  	
  	This time waste in necessary for avoiding spurious pattern matching in the FSM algorithm.  
  	
  	
.. _driver-configuration:

Driver Configuration
====================

If you need to define a new driver or change an existing one follow the recipe below:

#. set the PYCO_HOME environment variable to the name of your application's root directory
#. place a ``pyco.cfg`` configuration file in ``$PYCO_HOME/cfg``

``pyco.cfg`` is a .ini configuration file specifying the settings used in setting up the device connection and command line interaction.

Every section defines a specific driver setup, where the section title is the name of the driver.

The special ``[common]`` section contains the setup of the default common driver.
This is the only mandatory section that has to be defined.

The following is a configuration example that define also the `linux` and a `ciscoios` drivers::

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

The *common* driver is used when no driver is specified in the device url, for example:

 ssh://user@myremotemachine

The ``[linux]`` section contains definitions specific to the family of Linux-based operating systems.
Please notice the `parent` keyword: it's used to make the ``[linux]`` setup inherits its values from the ``[common]`` driver, unless otherwise specified.
For example the following definition inherits all the [common] configurations but overrides the *discoverPrompt* flag:: 		

  [linux]

   parent = common

   # enable/disable prompt discovery
   discoverPrompt = False

The `events` section defines the :term:`FSM` logic modelling the interaction with the device. 

The :ref:`fsm_model` section describes the meaning and syntax of a FSM machine, defined in terms of events, states and actions. 	

A special action is `cliIsDefined`: only such action implements the prompt discovery logic controlled by the
:ref:`discoverPrompt <config_discoverPrompt>`, :ref:`promptPattern <config_promptPattern>` and :ref:`cache <config_cache>` configuration parameter.  


Configuration parameters
------------------------

Below are reported all the pyco configuration parameters. In parenthesis the default values.

  .. _config_cache:
  
  *cache*
    the name of an SQLite database used by Pyco to cache user prompts as they are discovered. The `cache` value `<prompt_cache>` is the sqlite filename:
    
    * `$PYCO_HOME/<prompt_cache>` if the environment variable `PYCO_HOME` is set
    * `/tmp/<prompt_cache>` otherwise
    
    Caching is automatically enabled when the cache parameter is set. For it to work you also need  the  `sqlalchemy` and `transaction` 
    Python packages (which must have been previously installed in the execution environment). 

  *checkIfOutputComplete* (False)
    when True, perform another expect loop to check if more output arrived after 
    prompt match or the first expect loop timeout. This extra check slows down the interaction.

  .. _config_discoverPrompt:
  
  *discoverPrompt* (True|False)
  	enable the discovery prompt algorithm. If *discoverPrompt* is ``False`` the output returned by :py:meth:`pyco.device.Device.send()` is mixed with banners, input command and prompt strings.

  *exactPatternMatch* (False)
  	when *True*, perform exact string matching instead of the usual regexp matching. In this case, the *event.pattern* field must specify an exact string and not a regular expression.

  *maxWait* (5)
	wait *maxWait* seconds for a device response before triggering the timeout event.
	What happens when a *timeout* event is triggered depends on the FSM state:
	
	* it could be an operational wait time needed for waiting the device output in the discovery prompt phase
	* it could trigger a :py:exc:`pyco.device.ConnectionTimedOut` exception when a command response is not received.
	
  .. _config_promptPattern:
  
  *promptPattern*
    a regular expression used as an hint for matching the CLI prompt. Setting this value automatically disables the discovery prompt
    algorithm (even if `discoverPrompt` is set to True).
    Keep in mind that this is a weaker match than the exact prompt match implied by the prompt discovery algorithm, so ensure that the
    command response does not contain a string matching this regular expression.

  *sshCommand* (ssh ${device.username}@${device.name})
  	specifies the command line to execute the ssh client used for connecting.  

  *telnetCommand* (telnet ${device.name} ${device.port})
  	specifies the command line to execute the telnet client used for connecting.
  	
  *waitBeforeClearingBuffer* (1)
  	specifies the amount of seconds to wait for some more output before clearing the output buffer. It's used in the following circumstances:

  	* after the login phase and before sending the shell commands
  	* after a prompt discovery
  	
  	This wait is necessary to avoid spurious pattern matching in the FSM algorithm.  
  	
  	

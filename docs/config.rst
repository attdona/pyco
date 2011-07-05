.. _driver-configuration:

Driver Configuration
====================

The pyco configuration file is a .ini file containing the settings used in the device connection setup and command line communication.

Every section define a specific driver setup, where the section title is the name of the driver.

for example the [common] section contains the setup of the default common driver::

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

The *common* driver is used when no driver is defined in the device url:

 ssh://user@myremotemachine

The [linux] section contains the setup specific for the linux family of operating systems.
Note the `parent` keyword: the [common] setup is inherited by [linux] driver if not overwritten by the most specific driver.
For example the following inherits all the [common] configurations and overwrite the *discoverPrompt* flag:: 		

  [linux]

   parent = common

   # enable/disable prompt discovery
   discoverPrompt = False

   # if True disable another expect to check if more output arrived after 
   # prompt match or the first expect loop timeout.
   # In case discoverPrompt is True use prompt match to check if command output is complete
   timeoutCheckOnOutputComplete = False


		

Configuration parameters
------------------------

Below are reported all the pyco configuration parameters.

  *discoverPrompt* (True|False)
  	enable the discovery prompt algorithm. If *discoverPrompt* is ``False`` the output returned by :py:meth:`pyco.device.Device.send()` is mixed with banners, input command and prompt strings.

  *exactPatternMatch* (True|False)
  	if *True* performs exact pattern matching, so must be used defining the *event.pattern* field with an exact string and not with a regular expression.

  *maxWait* 
	wait *maxWait* seconds for a device response before raising timeout event.
	what happens when a *timeout* event is triggered depends on the FSM state:
	
	* it may be a operational wait time needed for waiting the device output in the discovery prompt phase
	* it may trigger a :py:exc:`pyco.device.ConnectionTimedOut` exception when a command response is not received. 

  *sshCommand*
  	the ssh client template command used for connecting.  

  *telnetCommand*
  	the telnet client template command used for connecting.  
  	
.. _driver-configuration:

Driver Configuration
====================

The pyco configuration file is a .ini file containing the settings used in the device connection setup and command line communication.

Every section define a specific driver setup, where the section title is the name of the driver.

for example the [common] section contains the setup of the common driver::

 [common]

  sshCommand = ssh ${device.username}@${device.name}

  telnetCommand = telnet ${device.name} ${device.telnet_port}

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

		

[linux]

parent = common

# enable/disable prompt discovery
discoverPrompt = True

# if True disable another expect to check if more output arrived after 
# prompt match or the first expect loop timeout.
# In case discoverPrompt is True use prompt match to check if command output is complete
timeoutCheckOnOutputComplete = False


[ciscoios]
	
parent = common	
	
# enable/disable prompt discovery
discoverPrompt = True

  [[events]]
  
	[[[password_event]]]
		pattern     = "Password:[ ]*"
		beginState       = GROUND
		action      = sendPassword
		endState   = PASSWORD_SENT

	[[[more]]]
		pattern     = "--- More ---"
		beginState       = USER_PROMPT
		action      = :send: :

    [[[password_sent]]]
		beginState = PASSWORD_SENT
		action = cliIsConnected
		endState = USER_PROMPT
		
	[[[cli_connected]]]
		beginState = USER_PROMPT	
		action = initCiscoCli
		

Configuration parameters
------------------------

Below are reported all the pyco configuration parameters.

  *maxWait*
	wait *maxWait* seconds for a device response before raising timeout event.
	What happens when a *timeout* event is triggered depends on the FSM state:
	 * it may be a operational wait time needed for waiting the device output in the discovery prompt phase
	 * it may trigger a :py:exc:`pyco.device.ConnectionTimedOut` exception when a command response is expected. 



		

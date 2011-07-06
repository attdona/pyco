Build a Interaction
-------------------

Ok, let's build step by step the right FSM machine to interact with a new device type.

For semplicity imagine that you have to connect for the first time to a CiscoIOS router::
 
 from pyco.device import device
 cisco = device('telnet://cisco:cisco@163.162.155.61')

 from pyco.actions import sendUsername

 cisco.add_event_action('username-event', 
                        pattern='Username: ', 
                        action=sendUsername, 
                        beginState='GROUND', 
                        endState='GROUND')

 cisco.login()

The discovery prompt algorithm take a while, so after waiting for a while, exactly *maxWait* seconds,
the console, with DEBUG log level enabled, says at the end something like::


 >>> cisco.login()
 
 [163.162.155.61]: executing [user_prompt] action [<function defaultEventHandler at 0x12219b0>]
 [163.162.155.61] in state [USER_PROMPT] got [user_prompt] event
 [163.162.155.61] loginSuccessfull: current_state [USER_PROMPT]
 clearing buffer ...
 [163.162.155.61] clear_buffer timeout: cleared expect buffer (<class 'pexpect.TIMEOUT'>)
 163.162.155.61 logged in !!! ...
 >>> 

The login phase succeeded, now let's try to send the command *show version*::

 >>> cisco('show version')

 generating event [show version]
 selected transition [event:show version,beginState:USER_PROMPT] -> [action:<function defaultEventHandler at 0x12219b0>, endState:None]
 [163.162.155.61]: executing [show version] action [<function defaultEventHandler at 0x12219b0>]
 [163.162.155.61] in state [USER_PROMPT] got [user_prompt] event
 [163.162.155.61] sending [show version]
 sending line [show version] using session [<pyco.expectsession.ExpectSession instance at 0x1935950>]
 entering patternMatch, checkpoint is [<function runUntilPromptMatchOrTimeout at 0x1936f50>]
 exactPatternMatch [False]
 [USER_PROMPT] matching [['r1>', '(?i)connection refused', 'Permission denied, please try again.', <class 'pexpect.TIMEOUT'>]]
 [163.162.155.61]: exception timeout triggered
 matched [3] pattern [<class 'pexpect.TIMEOUT'>] --> [timeout]
 before: [show version
 Cisco IOS Software, 7200 Software (C7200-JS-M), Version 12.4(3), RELEASE SOFTWARE (fc2)
 Technical Support: http://www.cisco.com/techsupport
 Copyright (c) 1986-2005 by Cisco Systems, Inc.
 Compiled Fri 22-Jul-05 09:12 by hqluong

 ROM: ROMMON Emulation Microcode
 BOOTLDR: 7200 Software (C7200-JS-M), Version 12.4(3), RELEASE SOFTWARE (fc2)

 r1 uptime is 4 weeks, 1 day, 20 hours, 1 minute
 System returned to ROM by unknown reload cause - suspect boot_data[BOOT_COUNT] 0x0, BOOT_COUNT 0, BOOTDATA 19
 System image file is "tftp://255.255.255.255/unknown"

 Cisco 7206VXR (NPE400) processor (revision A) with 245760K/16384K bytes of memory.
 Processor board ID 4294967295
 R7000 CPU at 150MHz, Implementation 39, Rev 2.1, 256KB L2 Cache
 6 slot VXR midplane, Version 2.1

 Last reset from power-on

 PCI bus mb0_mb1 (Slots 0, 1, 3 and 5) has a capacity of 600 bandwidth points.
  --More-- ] - after: [<class 'pexpect.TIMEOUT'>]
 [163.162.155.61] got [timeout] event; invoking handlers: [[]]
 selected transition [event:timeout,beginState:USER_PROMPT] -> [action:<function defaultEventHandler at 0x12219b0>, endState:None]
 [163.162.155.61]: executing [timeout] action [<function defaultEventHandler at 0x12219b0>]
 [163.162.155.61] in state [USER_PROMPT] got [timeout] event
 Traceback (most recent call last):
   File "<stdin>", line 1, in <module>
   File "/home/adona/dev/pyco/src/pyco/device.py", line 879, in __call__
     return self.send(command)
   File "/home/adona/dev/pyco/src/pyco/device.py", line 915, in send
     raise ConnectionTimedOut(self, 'prompt not hooked')
 pyco.device.ConnectionTimedOut: prompt not hooked

 >>>

The command ends with a :py:exc:`pyco.device.ConnectionTimedOut` exception with the message *prompt not hooked*.
Looking at the captured output from the cisco device the last string is the --More-- token, that ciscoIOS use to signals that more output is available, 
waiting for the user to press a some keyboard character to proceed.

CiscoIOS has a special command to disable output paging: *terminal lenght 0*::

 >>> def set_terminal(target):
 >>> ... target.send('terminal length 0')

 >>> cisco.add_event_action('user_prompt', action=set_terminal)

The previous configuration exploits the following rule:

an event lower(FSM_STATE) is generated when there is a state change from a source state (!=FSM_STATE) and FSM_STATE is the target state.
 
So when executing again the command ... ::

 >>> cisco('show version')

... the previous exception caused the cisco device instance to go back to GROUND state, so the login phase is redone before executing the *show version*:: 

 163.162.155.61 login ...
 [163.162.155.61] session: [<pyco.expectsession.ExpectSession instance at 0x1944320>]
 
 ... some more debug trace ...
 
 [163.162.155.61] in state [USER_PROMPT] got [prompt-match] event
 [163.162.155.61:show version]: captured response [Cisco IOS Software, 7200 Software (C7200-JS-M), Version 12.4(3), RELEASE SOFTWARE (fc2)
 Technical Support: http://www.cisco.com/techsupport
 Copyright (c) 1986-2005 by Cisco Systems, Inc.
 Compiled Fri 22-Jul-05 09:12 by hqluong
 
 ROM: ROMMON Emulation Microcode
 BOOTLDR: 7200 Software (C7200-JS-M), Version 12.4(3), RELEASE SOFTWARE (fc2)
 
 r1 uptime is 4 weeks, 1 day, 20 hours, 4 minutes
 System returned to ROM by unknown reload cause - suspect boot_data[BOOT_COUNT] 0x0, BOOT_COUNT 0, BOOTDATA 19
 System image file is "tftp://255.255.255.255/unknown"
 
 Cisco 7206VXR (NPE400) processor (revision A) with 245760K/16384K bytes of memory.
 Processor board ID 4294967295
 R7000 CPU at 150MHz, Implementation 39, Rev 2.1, 256KB L2 Cache
 6 slot VXR midplane, Version 2.1
 
 Last reset from power-on

 PCI bus mb0_mb1 (Slots 0, 1, 3 and 5) has a capacity of 600 bandwidth points.
 Current configuration on bus mb0_mb1 has a total of 400 bandwidth points. 
 This configuration is within the PCI bus capacity and is supported. 

 PCI bus mb2 (Slots 2, 4, 6) has a capacity of 600 bandwidth points.
 Current configuration on bus mb2 has a total of 0 bandwidth points 
 This configuration is within the PCI bus capacity and is supported. 

 Please refer to the following document "Cisco 7200 Series Port 
 Adaptor Hardware Configuration Guidelines" on CCO <www.cisco.com>, 
 for c7200 bandwidth points oversubscription/usage guidelines.


 2 FastEthernet interfaces
 125K bytes of NVRAM.

 65536K bytes of ATA PCMCIA card at slot 0 (Sector size 512 bytes).
 8192K bytes of Flash internal SIMM (Sector size 256K).
 Configuration register is 0x2102]
 >>> 

Right, it seems that the interaction is tuned for ciscoIOS, at least for our purpose:
the next step will be to persist a ciscoios driver into the pyco configuration.

in the `pyco.cfg` configuration file defines a new driver `ciscoios`::

 [ciscoios]
	
   parent = common	
	
   [[events]]
  
	[[[username_event]]]
 		beginState  = 'GROUND'
  		pattern     = "(?i)username:"
		action      = sendUsername

	[[[user_prompt]]]
		action = initCiscoTerminal
      
In the action file handlers.py just define the initCiscoTerminal function::

 from pyco.device import ConnectionRefused, PermissionDenied
 from pyco.device import MissingDeviceParameter, cliIsConnected
 
 def initCiscoTerminal(target):
    target.send_line('terminal length 0')

Now add to the url the `ciscoios` driver and run::

 from pyco.device import device
 cisco = device('telnet://cisco:cisco@163.162.155.61/ciscoios')

 cisco.login()
 output_command = cisco.send('show version') 

and the output_command variable will contains the command response. 








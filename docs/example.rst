Build a Interaction
-------------------

Ok, let's build step by step the right FSM machine to interact with a new device type.

For semplicity imagine that you have to connect for the first time to a CiscoIOS router::
 
 from pyco.device import device
 cisco = device('telnet://cisco:cisco@163.162.155.61')

 from pyco.actions import sendUsername

 cisco.addEventAction('username-event', pattern='Username: ', action=sendUsername, beginState='GROUND', endState='GROUND')

 cisco.login()

The discovery prompt algorithm take a while, so after waiting for a while, exactly *maxWait* seconds,
the console, with DEBUG log level enabled, says at the end something like::


 >>> cisco.login()
 
 2011-04-01 12:32:48,150 - device - DEBUG - [163.162.155.61]: executing [user_prompt] action [<function defaultEventHandler at 0x26e4500>]
 2011-04-01 12:32:48,150 - device - DEBUG - [163.162.155.61] in state [USER_PROMPT] got [user_prompt] event
 2011-04-01 12:32:48,150 - exp-session - DEBUG - [163.162.155.61] loginSuccessfull: current_state [USER_PROMPT]
 2011-04-01 12:32:49,152 - device - DEBUG - [163.162.155.61] clearBuffer timeout: cleared expect buffer (<class 'pexpect.TIMEOUT'>)
 2011-04-01 12:32:49,152 - device - DEBUG - 163.162.155.61 logged in !!! ...
 >>> 

The login phase succeeded, now let's try to send the command *show version*::

 >>> cisco('show version')


 2011-06-07 08:35:21,737 - device - DEBUG - [163.162.155.61] sending [show version]
 2011-06-07 08:35:21,737 - exp-session - DEBUG - sending line [show version] using session [<pyco.expectsession.ExpectSession instance at 0x2805128>]
 2011-06-07 08:35:21,838 - exp-session - DEBUG - entering patternMatch, checkpoint is [<function runUntilPromptMatchOrTimeout at 0x281ade8>]
 2011-06-07 08:35:21,838 - exp-session - DEBUG - exactPatternMatch [False]
 2011-06-07 08:35:21,839 - exp-session - DEBUG - [USER_PROMPT] matching [['r1>', '(?i)connection refused', 'Permission denied, please try again.', <class 'pexpect.TIMEOUT'>]]
 2011-06-07 08:35:26,844 - exp-session - DEBUG - [163.162.155.61]: exception timeout triggered
 2011-06-07 08:35:26,845 - exp-session - DEBUG - matched pattern [<class 'pexpect.TIMEOUT'>] --> [timeout]
 2011-06-07 08:35:26,845 - exp-session - DEBUG - before: [show version
 Cisco IOS Software, 7200 Software (C7200-JS-M), Version 12.4(3), RELEASE SOFTWARE (fc2)
 Technical Support: http://www.cisco.com/techsupport
 Copyright (c) 1986-2005 by Cisco Systems, Inc.
 Compiled Fri 22-Jul-05 09:12 by hqluong

 ROM: ROMMON Emulation Microcode
 BOOTLDR: 7200 Software (C7200-JS-M), Version 12.4(3), RELEASE SOFTWARE (fc2)

 r1 uptime is 15 hours, 40 minutes
 System returned to ROM by unknown reload cause - suspect boot_data[BOOT_COUNT] 0x0, BOOT_COUNT 0, BOOTDATA 19
 System image file is "tftp://255.255.255.255/unknown"

 Cisco 7206VXR (NPE400) processor (revision A) with 245760K/16384K bytes of memory.
 Processor board ID 4294967295
 R7000 CPU at 150MHz, Implementation 39, Rev 2.1, 256KB L2 Cache
 6 slot VXR midplane, Version 2.1

 Last reset from power-on

 PCI bus mb0_mb1 (Slots 0, 1, 3 and 5) has a capacity of 600 bandwidth points.
  --More-- ] - after: [<class 'pexpect.TIMEOUT'>]
 2011-06-07 08:35:26,845 - exp-session - DEBUG - [163.162.155.61] got [timeout] event; invoking handlers: [[]]
 2011-06-07 08:35:26,845 - device - DEBUG - selected transition [event:timeout,beginState:USER_PROMPT] -> [action:<function defaultEventHandler at 0x27fc398>, endState:None]
 2011-06-07 08:35:26,845 - device - DEBUG - [163.162.155.61]: executing [timeout] action [<function defaultEventHandler at 0x27fc398>]
 2011-06-07 08:35:26,845 - device - DEBUG - [163.162.155.61] in state [USER_PROMPT] got [timeout] event
 Traceback (most recent call last):
   File "<stdin>", line 1, in <module>
   File "/home/adona/dev/pyco/src/pyco/device.py", line 768, in __call__
     return self.send(command)
   File "/home/adona/dev/pyco/src/pyco/device.py", line 797, in send
     raise ConnectionTimedOut(self, 'prompt not hooked')
 pyco.device.ConnectionTimedOut: prompt not hooked
 >>>

The command ends with a :py:exc:`pyco.device.ConnectionTimedOut` exception with the message *prompt not hooked*.
Looking at the captured output from the cisco device the last string is the --More-- token, that ciscoIOS use to signals that more output is available, 
waiting for the user to press a some keyboard character to proceed.

CiscoIOS has a special command to disable output paging: *terminal lenght 0*::

 >>> def set_terminal(target):
 >>> ... target.send('terminal length 0')

 >>> cisco.addEventAction('user_prompt', action=set_terminal)

The previous configuration exploits the following rule:

an event lower(FSM_STATE) is generated when there is a state change from a source state (!=FSM_STATE) and FSM_STATE is the target state.
 
So when executing again the command ... ::

 >>> cisco('show version')

... the previous exception caused the cisco device instance to go back to GROUND state, so the login phase is redone before executing the *show version*:: 

 2011-06-07 09:36:37,135 - device - DEBUG - 163.162.155.61 login ...
 2011-06-07 09:36:37,135 - device - DEBUG - [163.162.155.61] session: [<pyco.expectsession.ExpectSession instance at 0x1098cf8>]
 2011-06-07 09:36:37,135 - exp-session - DEBUG - [163.162.155.61] prev hop device: [__source_host__]
 2011-06-07 09:36:37,135 - device - DEBUG - found [auth] plugin into module [pyco.device]
 2011-06-07 09:36:37,143 - exp-session - DEBUG - connecting using telnet 163.162.155.61 23
 2011-06-07 09:36:37,143 - exp-session - DEBUG - [163.162.155.61]: spawning a new [telnet 163.162.155.61 23] session ...
 2011-06-07 09:36:37,144 - exp-session - DEBUG - entering patternMatch, checkpoint is [<function loginSuccessfull at 0x1093320>]
 2011-06-07 09:36:37,145 - exp-session - DEBUG - exactPatternMatch [False]
 2011-06-07 09:36:37,145 - exp-session - DEBUG - [163.162.155.61] loginSuccessfull: current_state [GROUND]
 2011-06-07 09:36:37,146 - exp-session - DEBUG - [GROUND] matching [['login:[ ]*', 'continue connecting \\(yes/no\\)\\?', 'Username: ', '(?i)password:[ ]*', '(?i)connection refused', 'Permission denied, please try again.', <class 'pexpect.TIMEOUT'>]]
 2011-06-07 09:36:37,167 - exp-session - DEBUG - matched pattern [Username: ] --> [username-event]
 2011-06-07 09:36:37,167 - device - DEBUG - selected transition [event:username-event,beginState:GROUND] -> [action:<function sendUsername at 0x1077758>, endState:GROUND]
 2011-06-07 09:36:37,167 - device - DEBUG - transition activated for [username-event,GROUND] -> [GROUND]
 2011-06-07 09:36:37,168 - device - DEBUG - [163.162.155.61]: executing [username-event] action [<function sendUsername at 0x1077758>]
 2011-06-07 09:36:37,168 - actions - DEBUG - sending username  [cisco] ...
 2011-06-07 09:36:37,168 - device - DEBUG - [163.162.155.61] sending [cisco]
 2011-06-07 09:36:37,168 - exp-session - DEBUG - sending line [cisco] using session [<pyco.expectsession.ExpectSession instance at 0x1098cf8>]
 2011-06-07 09:36:37,269 - exp-session - DEBUG - [163.162.155.61] loginSuccessfull: current_state [GROUND]
 2011-06-07 09:36:37,269 - exp-session - DEBUG - [GROUND] matching [['login:[ ]*', 'continue connecting \\(yes/no\\)\\?', 'Username: ', '(?i)password:[ ]*', '(?i)connection refused', 'Permission denied, please try again.', <class 'pexpect.TIMEOUT'>]]
 2011-06-07 09:36:37,387 - exp-session - DEBUG - matched pattern [(?i)password:[ ]*] --> [password_event]
 2011-06-07 09:36:37,387 - device - DEBUG - selected transition [event:password_event,beginState:GROUND] -> [action:<function sendPassword at 0x10777d0>, endState:PASSWORD_SENT]
 2011-06-07 09:36:37,388 - device - DEBUG - transition activated for [password_event,GROUND] -> [PASSWORD_SENT]
 2011-06-07 09:36:37,388 - device - DEBUG - [163.162.155.61]: executing [password_event] action [<function sendPassword at 0x10777d0>]
 2011-06-07 09:36:37,388 - actions - DEBUG - [163.162.155.61] sending password [cisco] ...
 2011-06-07 09:36:37,388 - device - DEBUG - [163.162.155.61] sending [cisco]
 2011-06-07 09:36:37,388 - exp-session - DEBUG - sending line [cisco] using session [<pyco.expectsession.ExpectSession instance at 0x1098cf8>]
 2011-06-07 09:36:37,489 - device - DEBUG - generating event [password_sent]
 2011-06-07 09:36:37,489 - device - DEBUG - selected transition [event:password_sent,beginState:PASSWORD_SENT] -> [action:<function cliIsConnected at 0x1075668>, endState:USER_PROMPT]
 2011-06-07 09:36:37,489 - device - DEBUG - transition activated for [password_sent,PASSWORD_SENT] -> [USER_PROMPT]
 2011-06-07 09:36:37,489 - device - DEBUG - [163.162.155.61]: executing [password_sent] action [<function cliIsConnected at 0x1075668>]
 2011-06-07 09:36:37,489 - device - DEBUG - [163.162.155.61] [USER_PROMPT] state, [password_sent] event: checking if CLI is connected ...
 2011-06-07 09:36:37,490 - device - DEBUG - [163.162.155.61] starting [USER_PROMPT] prompt discovery
 2011-06-07 09:36:37,490 - device - DEBUG - [163.162.155.61] adding [<function discoverPromptCallback at 0x1075488>] for [timeout] event
 2011-06-07 09:36:37,490 - device - DEBUG - [163.162.155.61] adding [<function discoverPromptCallback at 0x1075488>] for [prompt-match] event
 2011-06-07 09:36:37,490 - exp-session - DEBUG - entering patternMatch, checkpoint is [<function isTimeoutOrPromptMatch at 0x10a0c80>]
 2011-06-07 09:36:37,490 - exp-session - DEBUG - exactPatternMatch [False]
 2011-06-07 09:36:37,490 - exp-session - DEBUG - [USER_PROMPT] matching [['r1>', '(?i)connection refused', 'Permission denied, please try again.']]
 2011-06-07 09:36:37,667 - exp-session - DEBUG - matched pattern [r1>] --> [prompt-match]
 2011-06-07 09:36:37,667 - exp-session - DEBUG - [163.162.155.61] got [prompt-match] event; invoking handlers: [[<function discoverPromptCallback at 0x1075488>]]
 2011-06-07 09:36:37,669 - device - DEBUG - [163.162.155.61] prompt discovery ...
 2011-06-07 09:36:37,669 - device - DEBUG - [163.162.155.61] [USER_PROMPT] prompt discovered: [r1>]
 2011-06-07 09:36:37,669 - device - DEBUG - [163.162.155.61]: adding expect pattern ['r1>'], event [prompt-match], state [USER_PROMPT]
 2011-06-07 09:36:37,669 - device - DEBUG - removing discoverPromptCallback
 2011-06-07 09:36:37,669 - device - DEBUG - [163.162.155.61] removing [timeout] event handler [<function discoverPromptCallback at 0x1075488>]
 2011-06-07 09:36:37,669 - device - DEBUG - removing discoverPromptCallback
 2011-06-07 09:36:37,669 - device - DEBUG - [163.162.155.61] removing [prompt-match] event handler [<function discoverPromptCallback at 0x1075488>]
 2011-06-07 09:36:37,670 - device - DEBUG - selected transition [event:prompt-match,beginState:USER_PROMPT] -> [action:None, endState:None]
 2011-06-07 09:36:37,670 - device - DEBUG - prompt discovery executed, cliIsConnected event: [prompt-match]
 2011-06-07 09:36:37,670 - device - DEBUG - generating event [user_prompt]
 2011-06-07 09:36:37,670 - device - DEBUG - selected transition [event:user_prompt,beginState:USER_PROMPT] -> [action:<function set_terminal at 0x10a0758>, endState:None]
 2011-06-07 09:36:37,670 - device - DEBUG - [163.162.155.61]: executing [user_prompt] action [<function set_terminal at 0x10a0758>]
 2011-06-07 09:36:37,670 - device - DEBUG - [163.162.155.61] sending [terminal length 0]
 2011-06-07 09:36:37,670 - exp-session - DEBUG - sending line [terminal length 0] using session [<pyco.expectsession.ExpectSession instance at 0x1098cf8>]
 2011-06-07 09:36:37,770 - exp-session - DEBUG - entering patternMatch, checkpoint is [<function runUntilPromptMatchOrTimeout at 0x10a0c80>]
 2011-06-07 09:36:37,771 - exp-session - DEBUG - exactPatternMatch [False]
 2011-06-07 09:36:37,771 - exp-session - DEBUG - [USER_PROMPT] matching [['r1>', '(?i)connection refused', 'Permission denied, please try again.', <class 'pexpect.TIMEOUT'>]]
 2011-06-07 09:36:37,787 - exp-session - DEBUG - matched pattern [r1>] --> [prompt-match]
 2011-06-07 09:36:37,787 - exp-session - DEBUG - [163.162.155.61] got [prompt-match] event; invoking handlers: [[]]
 2011-06-07 09:36:37,787 - device - DEBUG - selected transition [event:prompt-match,beginState:USER_PROMPT] -> [action:None, endState:None]
 2011-06-07 09:36:37,788 - device - DEBUG - [163.162.155.61:terminal length 0]: captured response []
 2011-06-07 09:36:37,788 - exp-session - DEBUG - [163.162.155.61] loginSuccessfull: current_state [USER_PROMPT]
 2011-06-07 09:36:37,788 - device - DEBUG - clearing buffer ...
 2011-06-07 09:36:38,789 - device - DEBUG - [163.162.155.61] clearBuffer timeout: cleared expect buffer (<class 'pexpect.TIMEOUT'>)
 2011-06-07 09:36:38,790 - device - DEBUG - 163.162.155.61 logged in !!! ...

The only difference is that when a user-prompt event is generated the function set_terminal is executed. The device is now connected again and the command can be executed::

 2011-06-07 09:36:38,790 - device - DEBUG - [163.162.155.61] sending [show version]
 2011-06-07 09:36:38,790 - exp-session - DEBUG - sending line [show version] using session [<pyco.expectsession.ExpectSession instance at 0x1098cf8>]
 2011-06-07 09:36:38,891 - exp-session - DEBUG - entering patternMatch, checkpoint is [<function runUntilPromptMatchOrTimeout at 0x10a0c80>]
 2011-06-07 09:36:38,891 - exp-session - DEBUG - exactPatternMatch [False]
 2011-06-07 09:36:38,891 - exp-session - DEBUG - [USER_PROMPT] matching [['r1>', '(?i)connection refused', 'Permission denied, please try again.', <class 'pexpect.TIMEOUT'>]]
 2011-06-07 09:36:38,955 - exp-session - DEBUG - matched pattern [r1>] --> [prompt-match]
 2011-06-07 09:36:38,955 - exp-session - DEBUG - [163.162.155.61] got [prompt-match] event; invoking handlers: [[]]
 2011-06-07 09:36:38,955 - device - DEBUG - selected transition [event:prompt-match,beginState:USER_PROMPT] -> [action:None, endState:None]
 2011-06-07 09:36:38,955 - device - DEBUG - [163.162.155.61:show version]: captured response [Cisco IOS Software, 7200 Software (C7200-JS-M), Version 12.4(3), RELEASE SOFTWARE (fc2)
 Technical Support: http://www.cisco.com/techsupport
 Copyright (c) 1986-2005 by Cisco Systems, Inc.
 Compiled Fri 22-Jul-05 09:12 by hqluong 

 ROM: ROMMON Emulation Microcode
 BOOTLDR: 7200 Software (C7200-JS-M), Version 12.4(3), RELEASE SOFTWARE (fc2)

 r1 uptime is 16 hours, 41 minutes
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
 'Cisco IOS Software, 7200 Software (C7200-JS-M), Version 12.4(3), RELEASE SOFTWARE (fc2)\r\nTechnical Support: http://www.cisco.com/techsupport\r\nCopyright (c) 1986-2005 by Cisco Systems, Inc.\r\nCompiled Fri 22-Jul-05 09:12 by hqluong\r\n\r\nROM: ROMMON Emulation Microcode\r\nBOOTLDR: 7200 Software (C7200-JS-M), Version 12.4(3), RELEASE SOFTWARE (fc2)\r\n\r\nr1 uptime is 16 hours, 41 minutes\r\nSystem returned to ROM by unknown reload cause - suspect boot_data[BOOT_COUNT] 0x0, BOOT_COUNT 0, BOOTDATA 19\r\nSystem image file is "tftp://255.255.255.255/unknown"\r\n\r\nCisco 7206VXR (NPE400) processor (revision A) with 245760K/16384K bytes of memory.\r\nProcessor board ID 4294967295\r\nR7000 CPU at 150MHz, Implementation 39, Rev 2.1, 256KB L2 Cache\r\n6 slot VXR midplane, Version 2.1\r\n\r\nLast reset from power-on\r\n\r\nPCI bus mb0_mb1 (Slots 0, 1, 3 and 5) has a capacity of 600 bandwidth points.\r\nCurrent configuration on bus mb0_mb1 has a total of 400 bandwidth points. \r\nThis configuration is within the PCI bus capacity and is supported. \r\n\r\nPCI bus mb2 (Slots 2, 4, 6) has a capacity of 600 bandwidth points.\r\nCurrent configuration on bus mb2 has a total of 0 bandwidth points \r\nThis configuration is within the PCI bus capacity and is supported. \r\n\r\nPlease refer to the following document "Cisco 7200 Series Port \r\nAdaptor Hardware Configuration Guidelines" on CCO <www.cisco.com>, \r\nfor c7200 bandwidth points oversubscription/usage guidelines.\r\n\r\n\r\n2 FastEthernet interfaces\r\n125K bytes of NVRAM.\r\n\r\n65536K bytes of ATA PCMCIA card at slot 0 (Sector size 512 bytes).\r\n8192K bytes of Flash internal SIMM (Sector size 256K).\r\nConfiguration register is 0x2102'
 >>> 

Right, it seems that the interaction is tuned for ciscoIOS, at least for our purpose:
the next step will be to persist a ciscoios driver into the pyco configuration.















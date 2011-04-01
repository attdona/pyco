Build a Interaction
-------------------

Ok, let's build step by step the right FSM machine to interact with a new device type.

For semplicity imagine that you have to connect for the first time to a CiscoIOS router::

cisco = device('telnet://cisco:cisco@163.162.155.61')

from netcube.actions import sendUsername
cisco.addPattern('username-event', pattern='Username: ', action=sendUsername, states='GROUND')

cisco.login()

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


Uhmm ..., a lot of unexpected things happened, the most evident thing is that the command output is incomplete and ends with a `--More--` string

Ok, after clearing the channel [#f1]_, send the command line to the device::

 2011-04-01 12:41:30,976 - device - DEBUG - [163.162.155.61] clearBuffer timeout: cleared expect buffer (<class 'pexpect.TIMEOUT'>)
 2011-04-01 12:41:30,976 - device - DEBUG - [163.162.155.61] sending [show version]
 2011-04-01 12:41:30,976 - exp-session - DEBUG - sending line [show version] using session [<netcube.expectsession.ExpectSession instance at 0x26f7cf8>]


.. [#f1] to be seen if the clearing phase can be safely removed


In the `USER_PROMPT` state wait for a device response that match the above patterns. Note that the prompt is one of the patterns::

 2011-04-01 12:41:31,077 - exp-session - DEBUG - entering patternMatch, checkpoint is [<function runUntilPromptMatchOrTimeout at 0x26ffe60>]
 2011-04-01 12:41:31,077 - exp-session - DEBUG - [USER_PROMPT] matching [['r1>', '(?i)connection refused', 'Permission denied, please try again.', <class 'pexpect.TIMEOUT'>]]

After 5 seconds, the `maxWait` timeout value, a timeout occours::

 2011-04-01 12:41:36,083 - exp-session - DEBUG - [163.162.155.61]: exception timeout triggered
 2011-04-01 12:41:36,083 - exp-session - DEBUG - matched pattern [<class 'pexpect.TIMEOUT'>] --> [timeout]
 
before contains the captured response string::    
 
 2011-04-01 12:41:36,083 - exp-session - DEBUG - before: [show version
 Cisco IOS Software, 7200 Software (C7200-JS-M), Version 12.4(3), RELEASE SOFTWARE (fc2)
 Technical Support: http://www.cisco.com/techsupport
 Copyright (c) 1986-2005 by Cisco Systems, Inc.
 Compiled Fri 22-Jul-05 09:12 by hqluong
 
 ROM: ROMMON Emulation Microcode
 BOOTLDR: 7200 Software (C7200-JS-M), Version 12.4(3), RELEASE SOFTWARE (fc2)
 
 r1 uptime is 1 hour, 33 minutes
 System returned to ROM by unknown reload cause - suspect boot_data[BOOT_COUNT] 0x0, BOOT_COUNT 0, BOOTDATA 19
 System image file is "tftp://255.255.255.255/unknown"
 
 Cisco 7206VXR (NPE400) processor (revision A) with 245760K/16384K bytes of memory.
 Processor board ID 4294967295
 R7000 CPU at 150MHz, Implementation 39, Rev 2.1, 256KB L2 Cache
 6 slot VXR midplane, Version 2.1
 
 Last reset from power-on

 PCI bus mb0_mb1 (Slots 0, 1, 3 and 5) has a capacity of 600 bandwidth points.
 --More-- ] - after: [<class 'pexpect.TIMEOUT'>]


In the `USER_PROMPT` state there is not a event handler binded to the `timeout` event::

  2011-04-01 12:41:36,083 - exp-session - DEBUG - [163.162.155.61] got [timeout] event; invoking handlers: [[]]
  
There is no transition for `[event=timeout, state=USER_PROMPT`] [#f2]_::

 2011-04-01 14:18:38,003 - device - DEBUG - selected transition [event:timeout,state:USER_PROMPT] -> [action:<function defaultEventHandler at 0x15d2500>, endState:None]

.. [#f2] For convention if endState==None then no state change happens.


The `defaultEventHandler` aparte logging does nothing except in case an `eof` event is detected:: 

 2011-04-01 14:18:38,003 - device - DEBUG - [163.162.155.61]: executing [timeout] action [<function defaultEventHandler at 0x15d2500>]
 2011-04-01 14:18:38,003 - device - DEBUG - [163.162.155.61] in state [USER_PROMPT] got [timeout] event

Ok, pyco try to do something intelligent: a `timeout` event after sending a command signal that the prompt previously discovered is lost, so try to rediscover it:: 

 2011-04-01 14:18:38,003 - device - DEBUG - [163.162.155.61] discovering again the prompt ...
 
Continuing with the assumptions, the tentative prompt is the last device resopnse line::  
 
 2011-04-01 14:18:38,003 - device - DEBUG - [163.162.155.61] taking last line as tentativePrompt: [ --More-- ]
 
Enable again the discovering algorithm::
 
 2011-04-01 14:18:38,004 - device - DEBUG - [163.162.155.61] adding [<function discoverPromptCallback at 0x15d25f0>] for [timeout] event
 2011-04-01 14:18:38,004 - device - DEBUG - [163.162.155.61] adding [<function discoverPromptCallback at 0x15d25f0>] for [prompt-match] event
 2011-04-01 15:14:55,102 - device - DEBUG - [163.162.155.61] prompt discovery ...
 2011-04-01 15:14:55,102 - device - DEBUG - [163.162.155.61] [USER_PROMPT] no prompt match, retrying discovery with pointer [' --More-- ']
 2011-04-01 15:14:55,103 - device - DEBUG - [163.162.155.61]: adding expect pattern [' --More-- '], event [prompt-match], state [USER_PROMPT]
 2011-04-01 15:14:55,103 - device - DEBUG - clearing buffer ...
 2011-04-01 15:14:55,103 - device - DEBUG - [163.162.155.61] sending []
 2011-04-01 15:14:55,103 - exp-session - DEBUG - sending line [] using session [<netcube.expectsession.ExpectSession instance at 0x2c47cb0>]
 2011-04-01 15:14:55,204 - exp-session - DEBUG - entering patternMatch, checkpoint is [<function <lambda> at 0x2c5c938>]
 2011-04-01 15:14:55,204 - exp-session - DEBUG - [USER_PROMPT] matching [[' --More-- ', '(?i)connection refused', 'Permission denied, please try again.']]
 2011-04-01 15:15:00,210 - exp-session - DEBUG - [163.162.155.61] connection timed out, unmatched         [
 r1>]
 2011-04-01 15:15:00,210 - exp-session - DEBUG - [163.162.155.61] got [timeout] event; invoking handlers: [[<function discoverPromptCallback at 0x2c345f0>]]
 2011-04-01 15:15:00,211 - device - DEBUG - [163.162.155.61] prompt discovery ...
 2011-04-01 15:15:00,212 - device - DEBUG - [163.162.155.61] [USER_PROMPT] no prompt match, retrying discovery with pointer ['\x08\x08\x08\x08\x08\x08\x08\x08\x08        \x08\x08\x08\x08\x08\x08\x08\x08\x08r1>']
 2011-04-01 15:15:00,212 - device - DEBUG - [163.162.155.61]: adding expect pattern ['\x08\x08\x08\x08\x08\x08\x08\x08\x08        \x08\x08\x08\x08\x08\x08\x08\x08\x08r1>'], event [prompt-match], state [USER_PROMPT]
 2011-04-01 15:15:00,212 - device - DEBUG - clearing buffer ...
 2011-04-01 15:15:00,212 - device - DEBUG - [163.162.155.61] sending []
 2011-04-01 15:15:00,212 - exp-session - DEBUG - sending line [] using session [<netcube.expectsession.ExpectSession instance at 0x2c47cb0>]
 2011-04-01 15:15:00,313 - exp-session - DEBUG - entering patternMatch, checkpoint is [<function <lambda> at 0x2c5cb18>]
 2011-04-01 15:15:00,313 - exp-session - DEBUG - [USER_PROMPT] matching [['\x08\x08\x08\x08\x08\x08\x08\x08\x08        \x08\x08\x08\x08\x08\x08\x08\x08\x08r1>', '(?i)connection refused', 'Permission denied, please try again.']]
 2011-04-01 15:15:05,319 - exp-session - DEBUG - [163.162.155.61] connection timed out, unmatched output: [
 r1>]
 2011-04-01 15:15:05,320 - exp-session - DEBUG - [163.162.155.61] got [timeout] event; invoking handlers: [[<function discoverPromptCallback at 0x2c345f0>]]
 2011-04-01 15:15:05,321 - device - DEBUG - [163.162.155.61] prompt discovery ...
 2011-04-01 15:15:05,321 - device - DEBUG - [163.162.155.61] [USER_PROMPT] unable to found the prompt, unsetting discovery. last output: [
 r1>]
 2011-04-01 15:15:05,321 - device - DEBUG - [163.162.155.61] removing [timeout] event handler [<function discoverPromptCallback at 0x2c345f0>]
 
 
Finally the (wrong) response captured is::
 
 2011-04-01 14:51:23,121 - device - DEBUG - [163.162.155.61:show version]: captured response [Cisco IOS Software, 7200 Software (C7200-JS-M), Version 12.4(3), RELEASE SOFTWARE (fc2)
 Technical Support: http://www.cisco.com/techsupport
 Copyright (c) 1986-2005 by Cisco Systems, Inc.
 Compiled Fri 22-Jul-05 09:12 by hqluong

 ROM: ROMMON Emulation Microcode
 BOOTLDR: 7200 Software (C7200-JS-M), Version 12.4(3), RELEASE SOFTWARE (fc2)

 r1 uptime is 3 hours, 43 minutes
 System returned to ROM by unknown reload cause - suspect boot_data[BOOT_COUNT] 0x0, BOOT_COUNT 0, BOOTDATA 19
 System image file is "tftp://255.255.255.255/unknown"

 Cisco 7206VXR (NPE400) processor (revision A) with 245760K/16384K bytes of memory.
 Processor board ID 4294967295
 R7000 CPU at 150MHz, Implementation 39, Rev 2.1, 256KB L2 Cache
 6 slot VXR midplane, Version 2.1

 Last reset from power-on

 PCI bus mb0_mb1 (Slots 0, 1, 3 and 5) has a capacity of 600 bandwidth points.
  --More-- ]



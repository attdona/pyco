Introduction
============

The goal of the Pyco project is to automate the interaction with systems and network devices 
with a convention over configuration approach.

Pyco is a python library based on `pexpect <http://www.noah.org/wiki/Pexpect>`_ tools written by Noah Spurrier and others contributors,
and pexpect is inspired by the famous Don Libes `Expect` system.

Some examples of what Pyco is useful for:

 * build a command line interface poller to acquire device data via Ssh and Telnet;
 * create a powerful scripting template engine to automatically configure your network devices;
 * build a system of distributed agents managing the network and system configuration, and keep
   your network inventory in sync;
 * interact with devices that are not otherwise directly accessible through a path of intermediate hops,
   every hop being a telnet or ssh connection.
 * build a powerful pythonic Network Management System based an all the above.


The design and implementation philosophy of Pyco is based upon the following points:

 * High Quality software through Test Driven Development
 	
 	Pyco is to be instrumented with many test suite to assure 100% coverage.
 	We strongly believe that the code that is not tested surely does not work,
 	so the pyco test code size overwhelm the size of application code. 
 	
 * Convention Over Configuration
 
 	Pyco goal is to come out of the box with a number of driver [#f]_ configurations
 	for interacting with many device platforms: Linux, CiscoIOS, Juniper, ...
 	
 * API for finite state machine configuration
 
	It must be easy to define the behaviour of the interaction pattern with a device through an
	API building the needed FSM.

 * A complete Exception System
 
 	The interaction errors arising in network communications have to be correctly classified and managed
 	to ensure a robust and reliable automatic machine interaction.  

.. [#f] A driver is a configuration file plus some Python code defining a device communication
 	pattern.
 	

For the impatient: the Pyco short story
----------------------------------------

Before trying anything, please keep in mind that Pyco is currently tested using Python 2.6 and 2.7, so it would be best for you to use said versions, even if it should
work also with Python 2.5.

First, install the Pyco egg, either in the system Python path or in a virtualenv:

 #. download a Pyco egg distribution from `google code <http://code.google.com/p/pyco/>`_
 #. easy_install pyco-<x.y.z>-py2.7.egg

and then try a simple remote command::

	from pyco.device import device
	my_host = device('ssh://myUser:myPassword@myhost.acme.org')
	response = my_host('uname -a')

The response string will contain the output of command ``uname -a``. It could look like the following:

	`Linux cencenighe 2.6.32-29-generic #58-Ubuntu SMP Fri Feb 11 20:52:10 UTC 2011 x86_64 GNU/Linux`

The above is the simpliest use case of interaction with a remote device. In this case, Pyco is using the builtin configuration.

If a FSM has to be customized for a specific device interaction, then you have to write a new :ref:`driver-configuration`, but this 
is the longer side of the story.
	

For the curious: Pyco Theory
----------------------------

Pyco is based on FSM concepts (see for example http://en.wikipedia.org/wiki/Finite-state_machine for the concepts introduction).

The goal of Pyco is to automate device interaction using standard protocolos (Ssh and Telnet).

Therefore, Pyco may be seen as an user interacting with a reactive system: a type of FSM classified as Transducer. 

See also :ref:`fsm_model` for a detailed description.

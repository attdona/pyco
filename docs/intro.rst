Introduction
============

The goal of Pyco project is to automates the interaction with systems and network devices 
with a convention over configuration approach.

Pyco is a python library based on `pexpect <http://www.noah.org/wiki/Pexpect>`_ tools written by Noah Spurrier and others contributors,
and pexpect is inspired by the famous Don Libes `Expect` system.

What you can do with pyco is for example:

 * build a command line interface poller to acquire device data with ssh and telnet protocol
 * realize a powerful scripting template engine to automatically configure your network devices
 * build a system of distributed agents that manage the network and system configuration and keep
   in sync your network inventory 
 * Reach a device that is not directedly reacheable through a path of intermediate hops,
   every hop being a telnet or ssh connection.
 * Build a powerful pythonic Network Management System based an all the above 


The design and implementation philosophy of pyco is based upon the following points:

 * High Quality software through Test Driven Development
 	
 	Pyco is to be instrumented with many test suite to assure 100% coverage.
 	We strongly believe that the code that is not tested surely does not work,
 	so the pyco test code size overwhelm the size of application code. 
 	
 * Convention Over Configuration
 
 	Pyco goal is to come out of the box with a number of driver [#f]_ configurations
 	for interacting with many device platforms: linux, ciscoIOS, juniper, ...
 	
 * API for finite state machine configuration
 
	It must be easy define the behavoir of the communication pattern with a device through an
	API that build the needed FSM.

 * A complete Exception System
 
 	The interaction errors arising in a network communications has to be correctly classified and managed
 	for assuring a robust and reliable automatic machine interaction.  

.. [#f] A driver is a configuration file and some python code that defines a device communication
 	pattern.
 	

For the impatients: the pyco short story
----------------------------------------

Keep in mind that actually pyco is tested with 2.6 and 2.7 python version, so you must use one of such version, even if it should
works also with python 2.5.

Install pyco as an egg, in the python os inntallation or in a virtualenv:

 #. download a pyco egg distribution from `google code <http://code.google.com/p/pyco/>`_
 #. easy_install pyco-<x.y.z>-py2.7.egg

and then try a simple remote command::

	from pyco.device import device
	my_host = device('ssh://myUser:myPassword@myhost.acme.org')
	response = my_host('uname -a')

The response string will contain the command output, something like:

	`Linux cencenighe 2.6.32-29-generic #58-Ubuntu SMP Fri Feb 11 20:52:10 UTC 2011 x86_64 GNU/Linux`

This is the simpler use case for interacting with a remote device. pyco use the default configuration stored into the package.

If a FSM have to be customized for a specific device interaction you have to write a new :ref:`driver-configuration`, but this 
is the long story side.
	

For the courious: Pyco Theory
-----------------------------

Pyco is based on FSM concepts, see for example http://en.wikipedia.org/wiki/Finite-state_machine for the concepts introduction.

Automatic device communication using standard protocolos (ssh and telnet) is Pyco goal.

Pyco may be seen therefore as a user that interact with a reactive system: a type of FSM classified as Transducer. 

See :ref:`fsm_model` for a detailed description.

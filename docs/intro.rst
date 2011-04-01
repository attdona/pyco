Introduction
============



For the impatients: the pyco short story
----------------------------------------

Install pyco::
 #. unzip the distribution pyco-<x>.<y>.<z>.tar.gz
 #. change to pyco package extraction root directory
 #. python setup.py install

and then try a simple remote command::

	from netcube.device import device
	device = device('ssh://myUser:myPassword@myhost.acme.org')
	response = device('uname -a')

The response string will contain the command output, something like:

	``Linux cencenighe 2.6.32-29-generic #58-Ubuntu SMP Fri Feb 11 20:52:10 UTC 2011 x86_64 GNU/Linux``
	

For the courious: Pyco Theory
-----------------------------

Pyco is based on FSM concepts, see for example http://en.wikipedia.org/wiki/Finite-state_machine for the concepts introduction.

Automatic device communication using standard protocolos (ssh and telnet) is Pyco goal.

Pyco may be seen therefore as a user that interact with a reactive system: a type of FSM classified as Transducer. 

See :ref:`fsm_model` for a detailed description.

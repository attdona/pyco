Introduction
============

the pyco short story
--------------------

Install pyco::

	python setup.py install

and then try a simple remote command::

	from netcube.master import Linux
	device = Linux('myhost.acme.org', username='myuser', password='mySecret')
	response = device('uname -a')

The response string will contain the command output, something like:

	``Linux cencenighe 2.6.32-29-generic #58-Ubuntu SMP Fri Feb 11 20:52:10 UTC 2011 x86_64 GNU/Linux``
	
	
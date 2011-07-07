Pyco for java
==============

jython interpreter doesnt support pty extension required by pexpect so it is not possible to run pyco in a jython environment.

If you want to use pyco in a java environment a solution is to use `execnet <http://codespeak.net/execnet>`_ from jython to a cpython
implementation that import the pyco package.


java environment setup
----------------------

Setup th ejython environment, java 1.5 or higher is required.

#. download jython-installer-2.5.2.jar
#. run `java -jar jython-installer-2.5.2.jar`
#. assure that the PATH environment variable resolve a python executable that knows pyco 

Now you can use the execnet API to run the pyco library from a java enabled jython interpreter, for example::

 import execnet
 gw = execnet.makegateway("popen//python=python")
 channel = gw.remote_exec("""
  from pyco.device import device
  h=device('telnet://cisco:cisco@163.162.155.61/ciscoios')
  res=h('show version')
  channel.send(res)
 """)

 print (channel.receive())

and keep going with using existing Java libraries from Python.


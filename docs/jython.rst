Pyco with Jython
================

It's not possible to use Pyco in a pure Jython environment, because the Jython interpreter provides no native support for the pty extension required by pexpect. 

On the other hand, if you still want to use Pyco, a solution could be using an external Python interpreter controlled from the Jython environment using  the `execnet <http://codespeak.net/execnet>`_ extension.
implementation that import the pyco package.


Java environment setup
----------------------

First, set up the Jython environment (Java 1.5 or higher is required).

#. download jython-installer-2.5.2.jar
#. execute `java -jar jython-installer-2.5.2.jar`
#. finally, set up your PATH enviroment variabile so it's possible to execute a Python interpreter where Pyco is available.

After doing that, you can use the execnet API to run the Pyco library (in the external C Python interpreter) from the Jython interpreter. For example::

 import execnet
 gw = execnet.makegateway("popen//python=python")
 channel = gw.remote_exec("""
  from pyco.device import device
  h=device('telnet://cisco:cisco@163.162.155.61/ciscoios')
  res=h('show version')
  channel.send(res)
 """)

 print (channel.receive())

and keep going with using existing Java libraries from Jython.


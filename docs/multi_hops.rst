Connecting through a path
=========================

Pyco is able to interact with a remote device also using one or more intermediate hops when the target device
is not directly accessible.

For example, let's suppose that router `r1` can be accessed only via Telnet from host `proxy`, which can in turn be
accessed via SSH from the Pyco machine. This situation could be handled like this::

 from pyco.device import device
 
 proxy = device('ssh://pyco:pyco@163.162.155.60')
 
 r1 = device('telnet://cisco:cisco@163.162.155.61/ciscoios')
 
 r1.hops = [proxy]
 
 r1('show version')

First an SSH connection is established between the Pyco machine and host `proxy`, and then a Telnet connection is established between host ``proxy`` and 
the ``r1`` device.
After the whole end-to-end connection is set up, we can proceed in executing the command ``show version`` on router ``r1``.
 
In this example there is just one intermediate hop between the host running Pyco and the route, but as said before there can be any number of hops as needed. 
 
    

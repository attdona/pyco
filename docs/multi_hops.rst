Connecting through a path
=========================

pyco is able to connect to a remote device using a numbers of intermediate network device hops when the target device
is non directly reacheable.

for example suppose that the router `r1` is reacheable via telnet from the `proxy` host and the `proxy` host is reacheable via
ssh from the pyco machine::

 from pyco.device import device
 
 proxy = device('ssh://pyco:pyco@163.162.155.60')
 
 r1 = device('telnet://cisco:cisco@163.162.155.61/ciscoios')
 
 r1.hops = [proxy]
 
 r1('show version')

First a ssh connection is established between the pyco machine and `proxy` host and then a telnet connection is established between the `proxy` and 
the `r1`device.
After the end to end connection is setup the command `show version` is executed.
 
In this scenario there is only one hop in the path from pyco machine and the target device, but the numbers of hops may be as much as needed. 
 
    
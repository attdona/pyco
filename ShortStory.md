# Pyco short story #

```
from pyco.device import device

myHost = device('ssh://willy:coyote@beepbeep.acme.com')

#send a shell command
output = myHost.send('uname -a') 

```

The output string is the command response, in this case something like:

```
Linux cencenighe 2.6.32-30-generic #59-Ubuntu SMP Tue Mar 1 21:30:46 UTC 2011 x86_64 GNU/Linux
```

The device() argument follow the [URI scheme](http://en.wikipedia.org/wiki/URI_scheme) syntax and allow telnet and ssh as communication protocols.

This is a simple use case.